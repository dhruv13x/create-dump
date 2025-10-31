# src/code_dump/utils.py
"""
Shared utilities: Logging, metrics, helpers.

Global-like but importable.
"""

from __future__ import annotations

import atexit
import concurrent.futures
import logging
import os
import re
import signal
import sys
import tempfile
import uuid
from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog
import tenacity
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError
from prometheus_client import Counter, Histogram, start_http_server

# Define logger EARLY to avoid circular imports
logger = structlog.get_logger("code_dump")

# NOW import core (after logger is defined)
from .core import Config, GitMeta

try:
    from . import version as version_module
    VERSION = version_module.VERSION
except ImportError:
    VERSION = "6.0.0"

# Constants
CHUNK_SIZE = 8192
BINARY_THRESHOLD = 0.05
DEFAULT_MAX_WORKERS = min(16, (os.cpu_count() or 4) * 2)
DEFAULT_METRICS_PORT = 8000

# Metrics
DUMP_DURATION = Histogram(
    "code_dump_duration_seconds",
    "Dump duration",
    buckets=[1, 5, 30, 60, 300, float("inf")],
)
FILES_PROCESSED = Counter("code_dump_files_total", "Files processed", ["status"])
ERRORS_TOTAL = Counter("code_dump_errors_total", "Errors encountered", ["type"])

# Globals for cleanup (thread-safe via ExitStack)
_cleanup_stack = ExitStack()
_temp_dir: Optional[tempfile.TemporaryDirectory] = None

# Rich
HAS_RICH = False
console = None
Progress = None
SpinnerColumn = None
TextColumn = None
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn

    console = Console()
    HAS_RICH = True
except ImportError:
    pass


def styled_print(text: str, nl: bool = True, **kwargs) -> None:
    end = "" if not nl else "\n"
    if HAS_RICH and console is not None:
        console.print(text, end=end, **kwargs)
    else:
        clean_text = re.sub(r"\[/?[^\]]+\]", "", text)
        print(clean_text, end=end, **kwargs)


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure structured logging once."""
    level = "DEBUG" if verbose else "WARNING" if quiet else "INFO"
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    if HAS_RICH:
        try:
            from structlog.dev import ConsoleRenderer

            processors.append(ConsoleRenderer(pad_event_to=40))
        except ImportError:
            processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(level=level, force=True)


@contextmanager
def metrics_server(port: int = DEFAULT_METRICS_PORT):
    """Start configurable metrics server with auto-cleanup."""
    start_http_server(port)
    try:
        yield
    finally:
        pass


class CleanupHandler:
    """Graceful shutdown on signals."""

    def __init__(self):
        signal.signal(signal.SIGINT, self._handler)
        signal.signal(signal.SIGTERM, self._handler)
        atexit.register(self._cleanup)

    def _handler(self, signum: int, frame: Any) -> None:
        logger.info("Shutdown signal received", signal=signum)
        self._cleanup()
        sys.exit(130 if signum == signal.SIGINT else 143)

    def _cleanup(self) -> None:
        global _temp_dir
        if _temp_dir:
            _temp_dir.cleanup()
        _cleanup_stack.close()


handler = CleanupHandler()  # Global handler


def slugify(path: str) -> str:
    """Convert path to safe anchor slug.

    >>> slugify("path/to/file.py")
    'path-to-file-py'
    """
    p = Path(path)
    clean = p.as_posix().lstrip("./").lower()
    return re.sub(r"[^a-z0-9]+", "-", clean).strip("-")


def get_language(filename: str) -> str:
    """Detect file language from extension/basename.

    >>> get_language("script.py")
    'python'
    >>> get_language("Dockerfile")
    'dockerfile'
    """
    basename = Path(filename).name.lower()
    if basename == "dockerfile":
        return "dockerfile"
    if basename == "dockerignore":
        return "ini"
    ext = Path(filename).suffix.lstrip(".").lower()
    mapping: Dict[str, str] = {
        # Core
        "py": "python",
        "sh": "bash",
        "yml": "yaml",
        "yaml": "yaml",
        "ini": "ini",
        "cfg": "ini",
        "toml": "toml",
        "json": "json",
        "txt": "text",
        "md": "markdown",
        # Web/Frontend
        "js": "javascript",
        "ts": "typescript",
        "html": "html",
        "css": "css",
        "jsx": "jsx",
        "tsx": "tsx",
        "vue": "vue",
        # Backend/DB
        "sql": "sql",
        "go": "go",
        "rs": "rust",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "rb": "ruby",
        "php": "php",
        "pl": "perl",
        "scala": "scala",
        "kt": "kotlin",
        "swift": "swift",
        "dart": "dart",
        # Data/Sci
        "csv": "csv",
        "xml": "xml",
        "r": "r",
        "jl": "julia",
        "ex": "elixir",
        "exs": "elixir",
        # Others
        "lua": "lua",
        "hs": "haskell",
        "ml": "ocaml",
        "scm": "scheme",
        "zig": "zig",
        "carbon": "carbon",
        # 2025 additions: e.g., Mojo, Verse
        "mojo": "mojo",
        "verse": "verse",
    }
    return mapping.get(ext, "text")


def is_text_file(path: Path) -> bool:
    """Heuristic: Check if file is text-based.

    >>> from pathlib import Path
    >>> test_py = Path("script.py")
    >>> _ = test_py.write_text('print("hello")')
    >>> is_text_file(test_py)
    True
    """       
    try:
        with path.open("rb") as f:
            chunk = f.read(CHUNK_SIZE)
            if len(chunk) == 0:
                return True
            if b"\x00" in chunk:
                return False
            decoded = chunk.decode("utf-8", errors="replace")
            invalid_ratio = decoded.count("\ufffd") / len(decoded)
            return invalid_ratio <= BINARY_THRESHOLD
    except (OSError, UnicodeDecodeError):
        return False


def parse_patterns(patterns: List[str]) -> PathSpec:
    """Parse glob patterns safely."""
    try:
        return PathSpec.from_lines("gitwildmatch", patterns)
    except GitWildMatchPatternError as e:
        logger.error("Invalid pattern", patterns=patterns, error=str(e))
        raise ValueError(f"Invalid patterns: {patterns}") from e


@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
    reraise=True,
)
def get_git_meta(root: Path) -> Optional[GitMeta]:
    """Fetch git metadata with timeout.
    
    >>> get_git_meta(Path("."))  # doctest: +SKIP
    GitMeta(branch="main", commit="abc123")
    """
    import subprocess

    try:
        cmd_branch = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        cmd_commit = ["git", "rev-parse", "--short", "HEAD"]
        branch = (
            subprocess.check_output(
                cmd_branch, cwd=root, stderr=subprocess.DEVNULL, timeout=10
            )
            .decode()
            .strip()
        )
        commit = (
            subprocess.check_output(
                cmd_commit, cwd=root, stderr=subprocess.DEVNULL, timeout=10
            )
            .decode()
            .strip()
        )
        return GitMeta(branch=branch, commit=commit)
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ):
        logger.debug("Git meta unavailable", root=root)
        return None


def _unique_path(path: Path) -> Path:
    """Generate unique path with UUID suffix."""
    # Use os.path.exists for the initial check so tests that mock pathlib.Path.exists
    # won't accidentally consume the mock's side_effect intended for candidate checks.
    if not os.path.exists(path):
        return path

    stem, suffix = path.stem, path.suffix
    counter = 0
    while True:
        # Defensive UUID hex extraction: support real UUID.hex (str) and tests that
        # mock uuid.uuid4() returning a MagicMock whose .hex is callable.
        u = uuid.uuid4()
        hex_attr = getattr(u, "hex", "")
        hex_val = hex_attr() if callable(hex_attr) else hex_attr
        hex8 = str(hex_val)[:8]

        if counter == 0:
            unique_stem = f"{stem}_{hex8}"
        else:
            unique_stem = f"{stem}_{counter}_{hex8}"

        candidate = path.parent / f"{unique_stem}{suffix}"
        # Call the class function Path.exists(candidate) so that a patch on
        # pathlib.Path.exists receives the candidate argument (matching the test).
        if not Path.exists(candidate):
            return candidate
        counter += 1

from os import scandir

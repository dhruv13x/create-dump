# src/create_dump/collector.py
"""
File collection logic.

Optimized scandir-based walker with pathspec filtering.
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Generator, List

from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

from .core import Config
from .utils import CHUNK_SIZE, BINARY_THRESHOLD, is_text_file, logger, parse_patterns


class FileCollector:
    """Collects files using optimized scandir and pathspec.

    >>> collector = FileCollector(Config())
    >>> files = collector.collect()  # Filters based on defaults
    """

    def __init__(
        self,
        config: Config,
        includes: List[str] = None,
        excludes: List[str] = None,
        use_gitignore: bool = False,
        root: Path = Path("."),
    ):
        self.config = config
        self.root = root.resolve()
        self.includes = includes or []
        self.excludes = excludes or []
        self.use_gitignore = use_gitignore
        self._include_spec = None
        self._exclude_spec = None
        self._setup_specs()

    def _setup_specs(self) -> None:
        """Build include/exclude specs with defaults."""
        default_includes = self.config.default_includes + [
            "*.py",
            "*.sh",
            "*.ini",
            "*.txt",
            "*.md",
            "*.yml",
            "*.yaml",
            "*.toml",
            "*.cfg",
            "*.json",
            "Dockerfile",
            ".flake8",
            ".pre-commit-config.yaml",
        ]
        all_includes = default_includes + self.includes

        default_excludes = self.config.default_excludes + [
            "*.log",
            "*.pem",
            "*.key",
            "*.db",
            "*.sqlite",
            "*.pyc",
            "*.pyo",
            ".env*",
            "bot_config.json",
            "*config.json",
            "*secrets*",
            "__init__.py",
            "*_all_create_dump_*",
            "*_all_create_dump_*.md*",
            "*_all_create_dump_*.gz*",
            "*_all_create_dump_*.sha256",
            "*_all_create_dump_*.zip",
        ]
        all_excludes = default_excludes + self.excludes

        if self.use_gitignore:
            gitignore_path = self.root / ".gitignore"
            if gitignore_path.exists():
                with gitignore_path.open("r", encoding="utf-8") as f:
                    git_patterns = [
                        line.strip()
                        for line in f
                        if line.strip() and not line.startswith("#")
                    ]
                all_excludes.extend(git_patterns)
                logger.debug("Gitignore integrated", patterns=len(git_patterns))

        self._include_spec = parse_patterns(all_includes)
        self._exclude_spec = parse_patterns(all_excludes)

    def collect(self) -> List[str]:
        """Walk and filter files efficiently."""
        files_list: List[str] = []
        for entry in os.scandir(self.root):
            if entry.is_dir(follow_symlinks=False):
                if entry.name in self.config.excluded_dirs:
                    continue
                # Recursive via generator
                for rel_path in self._collect_recursive(
                    Path(entry.path).relative_to(self.root)
                ):
                    files_list.append(rel_path.as_posix())
            elif entry.is_file(follow_symlinks=False):
                rel_path = Path(entry.path).relative_to(self.root)
                if self._matches(rel_path):
                    files_list.append(rel_path.as_posix())
        files_list.sort()
        return files_list

    def _collect_recursive(self, rel_dir: Path) -> Generator[Path, None, None]:
        """Recursive generator for subdirs."""
        full_dir = self.root / rel_dir
        for entry in os.scandir(full_dir):
            if entry.is_dir(follow_symlinks=False):
                if entry.name in self.config.excluded_dirs:
                    continue
                yield from self._collect_recursive(rel_dir / entry.name)
            elif entry.is_file(follow_symlinks=False):
                rel_path = rel_dir / entry.name
                if self._matches(rel_path):
                    yield rel_path

    def _matches(self, rel_path: Path) -> bool:
        """Check include/exclude and filters."""
        rel_posix = rel_path.as_posix()
        if self._exclude_spec.match_file(rel_posix):
            return False
        if self._include_spec.match_file(rel_posix) or self._include_spec.match_file(
            rel_path.name
        ):
            full_path = self.root / rel_path
            return self._should_include(full_path)
        return False

    def _should_include(self, full_path: Path) -> bool:
        """Final size/text check."""
        try:
            stat = full_path.stat()
            if (
                self.config.max_file_size_kb
                and stat.st_size > self.config.max_file_size_kb * 1024
            ):
                return False
            return is_text_file(full_path)
        except OSError:
            return False
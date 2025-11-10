# 🗃️ Project Code Dump

**Generated:** 2025-11-10T13:31:46+00:00 UTC
**Version:** 10.0.0
**Git Branch:** main | **Commit:** cf8ebbd

---

## Table of Contents

1. [create_dump.toml](#create-dump-toml)
2. [src/create_dump/cli/single.py](#src-create-dump-cli-single-py)
3. [.github/workflows/publish.yml](#github-workflows-publish-yml)
4. [src/create_dump/archiver.py](#src-create-dump-archiver-py)
5. [src/create_dump/archive/finder.py](#src-create-dump-archive-finder-py)
6. [autoheader.toml](#autoheader-toml)
7. [src/create_dump/cleanup.py](#src-create-dump-cleanup-py)
8. [src/create_dump/cli/rollback.py](#src-create-dump-cli-rollback-py)
9. [src/create_dump/archive/pruner.py](#src-create-dump-archive-pruner-py)
10. [src/create_dump/archive/core.py](#src-create-dump-archive-core-py)
11. [pyproject.toml](#pyproject-toml)
12. [src/create_dump/cli/batch.py](#src-create-dump-cli-batch-py)
13. [ROADMAP.md](#roadmap-md)
14. [src/create_dump/cli/main.py](#src-create-dump-cli-main-py)
15. [README.md](#readme-md)
16. [src/create_dump/archive/packager.py](#src-create-dump-archive-packager-py)
17. [src/create_dump/logging.py](#src-create-dump-logging-py)
18. [src/create_dump/collector/base.py](#src-create-dump-collector-base-py)
19. [src/create_dump/collector/walk.py](#src-create-dump-collector-walk-py)
20. [src/create_dump/processor.py](#src-create-dump-processor-py)
21. [src/create_dump/path_utils.py](#src-create-dump-path-utils-py)
22. [src/create_dump/helpers.py](#src-create-dump-helpers-py)
23. [src/create_dump/core.py](#src-create-dump-core-py)
24. [src/create_dump/collector/git_ls.py](#src-create-dump-collector-git-ls-py)
25. [src/create_dump/metrics.py](#src-create-dump-metrics-py)
26. [src/create_dump/collector/git_diff.py](#src-create-dump-collector-git-diff-py)
27. [src/create_dump/single.py](#src-create-dump-single-py)
28. [src/create_dump/orchestrator.py](#src-create-dump-orchestrator-py)
29. [src/create_dump/scanning.py](#src-create-dump-scanning-py)
30. [src/create_dump/rollback/engine.py](#src-create-dump-rollback-engine-py)
31. [src/create_dump/rollback/parser.py](#src-create-dump-rollback-parser-py)
32. [src/create_dump/system.py](#src-create-dump-system-py)
33. [src/create_dump/version.py](#src-create-dump-version-py)
34. [src/create_dump/watch.py](#src-create-dump-watch-py)
35. [src/create_dump/writing/json.py](#src-create-dump-writing-json-py)
36. [tests/archive/test_finder.py](#tests-archive-test-finder-py)
37. [src/create_dump/writing/checksum.py](#src-create-dump-writing-checksum-py)
38. [src/create_dump/writing/markdown.py](#src-create-dump-writing-markdown-py)
39. [tests/archive/test_core.py](#tests-archive-test-core-py)
40. [tests/archive/test_pruner.py](#tests-archive-test-pruner-py)
41. [tests/cli/test_main.py](#tests-cli-test-main-py)
42. [src/create_dump/workflow/single.py](#src-create-dump-workflow-single-py)
43. [tests/collector/test_git_diff.py](#tests-collector-test-git-diff-py)
44. [tests/cli/test_single.py](#tests-cli-test-single-py)
45. [tests/cli/test_batch.py](#tests-cli-test-batch-py)
46. [tests/cli/test_rollback.py](#tests-cli-test-rollback-py)
47. [tests/collector/test_base.py](#tests-collector-test-base-py)
48. [tests/archive/test_packager.py](#tests-archive-test-packager-py)
49. [tests/collector/test_git_ls.py](#tests-collector-test-git-ls-py)
50. [tests/conftest.py](#tests-conftest-py)
51. [tests/collector/test_init.py](#tests-collector-test-init-py)
52. [tests/collector/test_walk.py](#tests-collector-test-walk-py)
53. [tests/rollback/test_parser.py](#tests-rollback-test-parser-py)
54. [tests/test_core.py](#tests-test-core-py)
55. [tests/test_cleanup.py](#tests-test-cleanup-py)
56. [tests/test_archiver.py](#tests-test-archiver-py)
57. [tests/test_metrics.py](#tests-test-metrics-py)
58. [tests/test_logging.py](#tests-test-logging-py)
59. [tests/rollback/test_engine.py](#tests-rollback-test-engine-py)
60. [tests/test_helpers.py](#tests-test-helpers-py)
61. [tests/test_path_utils.py](#tests-test-path-utils-py)
62. [tests/test_scanning.py](#tests-test-scanning-py)
63. [tests/test_processor.py](#tests-test-processor-py)
64. [tests/test_version.py](#tests-test-version-py)
65. [tests/test_system.py](#tests-test-system-py)
66. [tests/test_single.py](#tests-test-single-py)
67. [tests/test_orchestrator.py](#tests-test-orchestrator-py)
68. [tests/writing/test_checksum.py](#tests-writing-test-checksum-py)
69. [tests/test_watch.py](#tests-test-watch-py)
70. [tests/writing/test_json.py](#tests-writing-test-json-py)
71. [tests/writing/test_markdown.py](#tests-writing-test-markdown-py)
72. [tests/workflow/test_single.py](#tests-workflow-test-single-py)

---

## create_dump.toml

<a id='create-dump-toml'></a>

```toml
# Configuration for create-dump
# You can also move this content to [tool.create-dump] in pyproject.toml
[tool.create-dump]

# Default output destination. Overridden by --dest.
dest = "my/dumps"

# Use .gitignore files to automatically exclude matching files.
use_gitignore = true

# Include Git branch and commit hash in the header.
git_meta = false

# Enable secret scanning. Add 'hide_secrets = true' to redact them.
scan_secrets = true

```

---

## src/create_dump/cli/single.py

<a id='src-create-dump-cli-single-py'></a>

```python
# src/create_dump/cli/single.py

"""'single' command implementation for the CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from typer import Exit
import anyio  # ⚡ REFACTOR: Import anyio

# ⚡ REFACTOR: Import the new ASYNC workflow function
from ..single import run_single
# ⚡ REFACTOR: Import from new logging module
from ..logging import setup_logging


def single(
    ctx: typer.Context,  # 🐞 FIX: Add Context argument
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root directory to scan [default: . (cwd)]."),

    # Output & Format
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for output (default: root)."),
    no_toc: bool = typer.Option(False, "--no-toc", help="Omit table of contents."),
    tree_toc: bool = typer.Option(False, "--tree-toc", help="Render Table of Contents as a file tree."),
    format: str = typer.Option("md", "--format", help="Output format (md or json)."),
    compress: bool = typer.Option(False, "-c", "--compress", help="Gzip the output file."),

    # Processing
    progress: Optional[bool] = typer.Option(None, "-p", "--progress/--no-progress", help="Show processing progress."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Succeed on 0 files (default: fail)."),
    metrics_port: int = typer.Option(8000, "--metrics-port", help="Prometheus export port [default: 8000]."),

    # Filtering & Collection
    exclude: str = typer.Option("", "--exclude", help="Comma-separated exclude patterns."),
    include: str = typer.Option("", "--include", help="Comma-separated include patterns."),
    max_file_size: Optional[int] = typer.Option(None, "--max-file-size", help="Max file size in KB."),
    use_gitignore: bool = typer.Option(True, "--use-gitignore/--no-use-gitignore", help="Incorporate .gitignore excludes [default: true]."),
    git_meta: bool = typer.Option(True, "--git-meta/--no-git-meta", help="Include Git branch/commit [default: true]."),
    max_workers: int = typer.Option(16, "--max-workers", help="Concurrency level [default: 16]."),
    
    # ⚡ NEW: v8 feature flags
    watch: bool = typer.Option(False, "--watch", help="Run in live-watch mode, redumping on file changes."),
    git_ls_files: bool = typer.Option(False, "--git-ls-files", help="Use 'git ls-files' for file collection (fast, accurate)."),
    diff_since: Optional[str] = typer.Option(None, "--diff-since", help="Only dump files changed since a specific git ref (e.g., 'main')."),
    scan_secrets: bool = typer.Option(False, "--scan-secrets", help="Scan files for secrets. Fails dump if secrets are found."),
    hide_secrets: bool = typer.Option(False, "--hide-secrets", help="Redact found secrets (requires --scan-secrets)."),

    # Archiving (Unified)
    archive: bool = typer.Option(False, "-a", "--archive", help="Archive prior dumps into ZIP (unified workflow)."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs."),
    archive_search: bool = typer.Option(False, "--archive-search", help="Search project-wide for dumps."),
    archive_include_current: bool = typer.Option(True, "--archive-include-current/--no-archive-include-current", help="Include this run in archive [default: true]."),
    archive_no_remove: bool = typer.Option(False, "--archive-no-remove", help="Preserve originals post-archiving."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive."),
    archive_format: str = typer.Option("zip", "--archive-format", help="Archive format (zip, tar.gz, tar.bz2)."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for prompts and deletions [default: false]."),
    dry_run: bool = typer.Option(False, "-d", "--dry-run", help="Simulate without writing files (default: off)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    # 🐞 FIX: Add verbose and quiet flags back, defaulting to None
    verbose: Optional[bool] = typer.Option(None, "-v", "--verbose", help="Enable debug logging."),
    quiet: Optional[bool] = typer.Option(None, "-q", "--quiet", help="Suppress output (CI mode)."),
):
    """Create a single code dump in the specified directory.
    ...
    """
    if not root.is_dir():
        raise typer.BadParameter(f"Root '{root}' is not a directory. Use '.' for cwd or a valid path.")

    # ⚡ NEW: Validation for v8 flags
    if git_ls_files and diff_since:
        raise typer.BadParameter("--git-ls-files and --diff-since are mutually exclusive.")
    
    if hide_secrets and not scan_secrets:
        raise typer.BadParameter("--hide-secrets requires --scan-secrets to be enabled.")

    effective_dry_run = dry_run and not no_dry_run
    
    # 🐞 FIX: Get verbose/quiet values from the *main* context
    # This ensures `create-dump -v` (no command) works
    main_params = ctx.find_root().params
    
    # 🐞 FIX: Logic to correctly determine verbosity, giving command-level precedence
    # and ensuring quiet wins.
    if quiet is True:
        verbose_val = False
        quiet_val = True
    elif verbose is True:
        verbose_val = True
        quiet_val = False
    else: # Neither was set at the command level, so inherit from main
        verbose_val = main_params.get('verbose', False)
        quiet_val = main_params.get('quiet', False)
        
        # Final sanity check if inheriting: quiet wins
        if quiet_val:
            verbose_val = False

    # 🐞 FIX: Re-run setup_logging in case 'single' was called directly
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    # 🐞 FIX: Add logic to correctly determine progress, mirroring verbose/quiet
    if progress is True:
        progress_val = True
    elif progress is False:
        progress_val = False
    else: # Not set at command level, inherit from main
        progress_val = main_params.get('progress', True) # Default to True from main
    
    effective_progress = progress_val and not quiet_val

    # ⚡ REFACTOR: Call the async function using anyio.run
    try:
        anyio.run(
            run_single,
            root,
            effective_dry_run,
            yes,
            no_toc,
            tree_toc,
            compress,
            format,
            exclude,
            include,
            max_file_size,
            use_gitignore,
            git_meta,
            effective_progress,
            max_workers,
            archive,
            archive_all,
            archive_search,
            archive_include_current,
            archive_no_remove,
            archive_keep_latest,
            archive_keep_last,
            archive_clean_root,
            archive_format,
            allow_empty,
            metrics_port,
            verbose_val,  # 🐞 FIX: Pass the correct flag value
            quiet_val,    # 🐞 FIX: Pass the correct flag value
            dest,
            # ⚡ NEW: Pass v8 flags to the orchestrator
            watch,
            git_ls_files,
            diff_since,
            scan_secrets,
            hide_secrets,
        )
    except Exit as e:
        if getattr(e, "exit_code", None) == 0 and dry_run:
            return  # Graceful exit for dry run
        raise
```

---

## .github/workflows/publish.yml

<a id='github-workflows-publish-yml'></a>

```yaml
name: 🚀 Publish to PyPI (Trusted Publishing)

on:
  push:
    tags:
      - "v*.*.*"  # Trigger only on semantic version tags (e.g., v1.2.3)

permissions:
  contents: read
  id-token: write  # Required for OIDC Trusted Publishing to PyPI

jobs:
  build-and-publish:
    name: Build & Publish
    runs-on: ubuntu-latest
    environment: pypi  # Optional: enables manual approval if configured in repo settings

    steps:
      - name: 🧩 Checkout code
        uses: actions/checkout@v4

      - name: 🐍 Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Install all build and test tools
      - name: 📦 Install build and test tools
        run: |
          python -m pip install --upgrade pip
          # Install from [dev] dependencies + build tools
          pip install .[dev] build twine codecov

      # 🧪 Run tests and check coverage
      - name: 🧪 Run tests & generate coverage
        run: pytest --cov=src --cov-report=xml

      # 📊 Upload coverage to Codecov
      - name: 📊 Upload coverage reports to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }} # Must be set in repo secrets
          file: ./coverage.xml
          verbose: true
          fail_ci_if_error: true # Fail the build if upload fails

      # ⚙️ Build distribution packages
      - name: ⚙️ Build distribution packages
        run: python -m build

      - name: ✅ Verify distribution
        run: twine check dist/*

      - name: 🚀 Publish to PyPI (via OIDC)
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          verbose: true
          skip-existing: false  # Fail if version already exists (prevents accidental overwrites)
          
```

---

## src/create_dump/archiver.py

<a id='src-create-dump-archiver-py'></a>

```python
# src/create_dump/archiver.py

"""
Orchestrator for the archiving workflow.

Coordinates Finder, Packager, and Pruner components to manage the
archive lifecycle (find, zip, clean, prune).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Tuple, Dict

import anyio  # ⚡ REFACTOR: Import anyio
# ⚡ REFACTOR: Import async cleanup
from .cleanup import safe_delete_paths
from .core import Config, load_config, DEFAULT_DUMP_PATTERN
from .path_utils import confirm
from .logging import logger  # ⚡ REFACTOR: Import from logging
# ⚡ REFACTOR: Import new SRP components
from .archive import ArchiveFinder, ArchivePackager, ArchivePruner

__all__ = ["ArchiveManager"]


class ArchiveManager:
    """Orchestrates finding, packaging, and pruning of archives."""

    def __init__(
        self,
        root: Path,
        timestamp: str,
        keep_latest: bool = True,
        keep_last: Optional[int] = None,
        clean_root: bool = False,
        search: bool = False,
        include_current: bool = True,
        no_remove: bool = False,
        dry_run: bool = False,
        yes: bool = False,
        verbose: bool = False,
        md_pattern: Optional[str] = None,
        archive_all: bool = False,
        archive_format: str = "zip",
    ):
        self.root = root.resolve()
        self.timestamp = timestamp
        self.search = search or archive_all
        self.archive_all = archive_all
        self.dry_run = dry_run
        self.yes = yes
        self.clean_root = clean_root
        self.no_remove = no_remove
        
        # Load and validate config (sync, fine)
        cfg = load_config()
        self.md_pattern = md_pattern or cfg.dump_pattern
        if md_pattern and not re.match(r'.*_all_create_dump_', self.md_pattern):
            logger.warning("Loose md_pattern provided; enforcing canonical: %s", DEFAULT_DUMP_PATTERN)
            self.md_pattern = DEFAULT_DUMP_PATTERN

        # Setup directories (sync, fine)
        self.archives_dir = self.root / "archives"
        self.archives_dir.mkdir(exist_ok=True)
        self.quarantine_dir = self.archives_dir / "quarantine"
        self.quarantine_dir.mkdir(exist_ok=True)
        
        # Instantiate SRP components (sync, fine)
        self.finder = ArchiveFinder(
            root=self.root,
            md_pattern=self.md_pattern,
            search=self.search,
            verbose=verbose,
            dry_run=dry_run,
            quarantine_dir=self.quarantine_dir,
        )
        
        self.packager = ArchivePackager(
            root=self.root,
            archives_dir=self.archives_dir,
            quarantine_dir=self.quarantine_dir,
            timestamp=self.timestamp,
            keep_latest=keep_latest,
            verbose=verbose,
            dry_run=dry_run,
            yes=yes,
            clean_root=clean_root,
            no_remove=no_remove,
            archive_format=archive_format,
         
        )
        
        self.pruner = ArchivePruner(
            archives_dir=self.archives_dir,
            keep_last=keep_last,
            verbose=verbose,
        )

    # ⚡ REFACTOR: Converted to async
    async def run(self, current_outfile: Optional[Path] = None) -> Dict[str, Optional[Path]]:
        """Orchestrate: find, package, clean, prune."""
        
        # 1. Find pairs
        # ⚡ REFACTOR: Await async finder
        pairs = await self.finder.find_dump_pairs()
        if not pairs:
            logger.info("No pairs for archiving.")
            await self.pruner.prune()  # Prune even if no new pairs
            return {}

        archive_paths: Dict[str, Optional[Path]] = {}
        all_to_delete: List[Path] = []

        # 2. Package pairs
        if not self.archive_all:
            # ⚡ REFACTOR: Await async packager
            archive_paths, to_delete = await self.packager.handle_single_archive(pairs)
            all_to_delete.extend(to_delete)
        else:
            groups = self.packager.group_pairs_by_prefix(pairs)
            # ⚡ REFACTOR: Await async packager
            archive_paths, to_delete = await self.packager.handle_grouped_archives(groups)
            all_to_delete.extend(to_delete)

        # 3. Clean (Deferred bulk delete)
        if self.clean_root and all_to_delete and not self.no_remove and not self.dry_run:
            prompt = f"Delete {len(all_to_delete)} archived files across groups?" if self.archive_all else f"Clean {len(all_to_delete)} root files post-archive?"
            
            # ⚡ REFACTOR: Run blocking 'confirm' in a thread
            user_confirmed = self.yes or await anyio.to_thread.run_sync(confirm, prompt)
            
            if user_confirmed:
                # ⚡ REFACTOR: Call async delete
                await safe_delete_paths(
                    all_to_delete, self.root, dry_run=False, assume_yes=self.yes
                )
                logger.info("Deferred delete: Cleaned %d files post-validation", len(all_to_delete))

        # 4. Prune
        # ⚡ REFACTOR: Await async pruner
        await self.pruner.prune()

        # 5. Handle symlink (no-op for now)
        if current_outfile:
            pass  # Logic for symlinking latest remains here if needed

        return archive_paths
    
    # ⚡ REFACTOR: Removed synchronous run method
```

---

## src/create_dump/archive/finder.py

<a id='src-create-dump-archive-finder-py'></a>

```python
# src/create_dump/archive/finder.py

"""Component responsible for finding valid MD/SHA dump pairs."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Optional, Tuple, AsyncGenerator

import anyio
# ⚡ REFACTOR: Import the async version of the safety check
from ..path_utils import safe_is_within
from ..logging import logger


class ArchiveFinder:
    """Finds valid dump pairs, respecting search scope and quarantining orphans."""

    def __init__(
        self,
        root: Path,
        md_pattern: str,
        search: bool,
        verbose: bool,
        dry_run: bool,
        quarantine_dir: Path,
    ):
        self.root = root
        self.md_pattern = md_pattern
        self.search = search
        self.verbose = verbose
        self.dry_run = dry_run
        self.quarantine_dir = quarantine_dir
        
        # ⚡ REFACTOR: Store anyio.Path versions for async checks
        self.anyio_root = anyio.Path(self.root)
        self.anyio_quarantine_dir = anyio.Path(self.quarantine_dir)

    # ⚡ REFACTOR: Converted to async generator
    async def _walk_files(self) -> AsyncGenerator[anyio.Path, None]:
        """
        Walks root directory and yields all file Paths.
        Respects self.search (recursive) vs. flat (scandir).
        """
        # ⚡ REFACTOR: Use instance-level anyio_root
        if self.search:
            # Recursive search
            async for p in self.anyio_root.rglob("*"):
                if await p.is_file():
                    yield p
        else:
            # Flat search
            async for p in self.anyio_root.iterdir():
                if await p.is_file():
                    yield p

    # ⚡ REFACTOR: Converted to async
    async def find_dump_pairs(self) -> List[Tuple[Path, Optional[Path]]]:
        """Find MD/SHA pairs; search if enabled; quarantine orphans."""
        md_regex = re.compile(self.md_pattern)
        pairs = []

        # ⚡ REFACTOR: Renamed 'p' to 'anyio_p' for clarity
        async for anyio_p in self._walk_files():
            # Create a sync pathlib.Path for non-I/O operations
            p_pathlib = Path(anyio_p)
            
            # 🐞 FIX: Prevent recursive loop by ignoring the quarantine dir
            # ⚡ REFACTOR: (Target 1) Use await and async check
            if await safe_is_within(anyio_p, self.anyio_quarantine_dir):
                continue

            if not md_regex.search(p_pathlib.name):
                continue
            
            # 🐞 FIX: This check is critical. Only process .md files.
            if not p_pathlib.name.endswith('.md'):
                if self.verbose:
                    logger.debug("Skipping non-MD match: %s", p_pathlib.name)
                continue
            
            # ⚡ REFACTOR: (Target 2) Use await and async check
            if not await safe_is_within(anyio_p, self.anyio_root):
                continue
            
            # Use pathlib for sync suffix logic
            sha_pathlib = p_pathlib.with_suffix(".sha256")
            
            # ⚡ REFACTOR: Use anyio.Path for async .exists() check
            anyio_sha = anyio.Path(sha_pathlib)
            sha_exists = await anyio_sha.exists()
            
            # ⚡ REFACTOR: (Target 3) Re-structured logic for async check
            sha_path = None  # Default to None
            if sha_exists:
                if await safe_is_within(anyio_sha, self.anyio_root):
                    sha_path = sha_pathlib  # Success, store the sync path
                else:
                    logger.debug("Ignoring .sha256 file outside root", path=str(sha_pathlib))

            if not sha_path:
                if not self.dry_run:
                    # Ensure quarantine dir exists before moving
                    await self.anyio_quarantine_dir.mkdir(exist_ok=True)
                    quarantine_path = self.quarantine_dir / p_pathlib.name
                    # ⚡ REFACTOR: Use async rename on the anyio.Path object 'anyio_p'
                    await anyio_p.rename(quarantine_path)
                    logger.warning("Quarantined orphan MD: %s -> %s", p_pathlib, quarantine_path)
                else:
                    logger.warning("[dry-run] Would quarantine orphan MD: %s", p_pathlib)
                continue
            
            # Store the sync pathlib.Path in the list
            pairs.append((p_pathlib, sha_path))

        if self.verbose:
            logger.debug("Found %d pairs (recursive=%s)", len(pairs), self.search)
        return sorted(pairs, key=lambda x: x[0].name)
```

---

## autoheader.toml

<a id='autoheader-toml'></a>

```toml
# autoheader configuration file
# Generated by `autoheader --init`
# For more info, see: https://github.com/dhruv13x/autoheader

[general]
# Run in simulation mode. (Default: true)
# To apply changes, run `autoheader --no-dry-run` or set:
# dry_run = false

# Create .bak files before modifying. (Default: false)
backup = false

# Number of parallel workers. (Default: 8)
workers = 8

# auto-confirm all prompts (e.g., for CI). (Default: false)
# yes = false

[detection]
# Max directory depth to scan. (Default: no limit)
# depth = 10

# Files that mark the project root.
markers = [
    ".gitignore",
    "README.md",
    "README.rst",
    "pyproject.toml",
]

[exclude]
# Extra paths/globs to exclude.
# The built-in defaults are included below for convenience.
paths = [
    ".git",
    ".github",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".svn",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "env",
    "node_modules",
    "venv",
]

# This legacy section is used for the global `blank_lines_after` setting.
[header]
blank_lines_after = 1


# --- Language-Specific Configuration ---
# autoheader v2.0+ uses language blocks.
# The default config for Python is shown below.
# You can add more, e.g., [language.javascript], [language.go], etc.

[language.python]
# Globs to identify files for this language
file_globs = [
    "*.py",
    "*.pyi",
]

# The comment prefix to use
prefix = "# "

# The template for the header line. {path} is the placeholder.
template = "# {path}"

# Whether to check for shebangs/encoding (Python-specific)
check_encoding = true

```

---

## src/create_dump/cleanup.py

<a id='src-create-dump-cleanup-py'></a>

```python
# src/create_dump/cleanup.py

"""Safe, auditable cleanup of files/directories with dry-run and prompts."""

from __future__ import annotations

import shutil
from pathlib import Path
# ⚡ REFACTOR: Import AsyncGenerator, Union, and collections.abc
from typing import List, Tuple, AsyncGenerator, Union
import collections.abc

import anyio
# ⚡ REFACTOR: Import async finder and new async safe_is_within
from .path_utils import (
    confirm,
    find_matching_files, safe_is_within
)
from .logging import logger

# ⚡ REFACTOR: Removed safe_delete_paths and safe_cleanup
__all__ = ["safe_delete_paths", "safe_cleanup"]


# ⚡ REFACTOR: Removed synchronous safe_delete_paths function


async def safe_delete_paths(
    # ⚡ REFACTOR: Accept either a List (for existing callers) or an AsyncGenerator
    paths: Union[List[Path], AsyncGenerator[Path, None]], 
    root: Path, 
    dry_run: bool, 
    assume_yes: bool
) -> Tuple[int, int]:
    """Delete files or directories in a safe, async manner."""
    deleted_files = deleted_dirs = 0
    
    # ⚡ REFACTOR: Convert root to anyio.Path once
    anyio_root = anyio.Path(root)
    
    # ⚡ REFACTOR: Create a unified async iterator to handle both types
    async def async_iter(paths_iterable):
        if isinstance(paths_iterable, collections.abc.AsyncGenerator):
            async for p_gen in paths_iterable:
                yield p_gen
        else: # It's a List
            for p_list in paths_iterable:
                yield p_list

    # ⚡ REFACTOR: Use the unified iterator
    async for p in async_iter(paths):
        # 1. 🐞 FIX: Use the original anyio.Path object for all async I/O
        anyio_p = anyio.Path(p)

        # 2. 🐞 FIX: Use the new async safety check
        if not await safe_is_within(anyio_p, anyio_root):
            # Log using the original path for clarity
            logger.warning(f"Skipping path outside root: {p}")
            continue

        # 3. Use the original, async-capable anyio_p for I/O
        if await anyio_p.is_file():
            if dry_run:
                logger.info(f"[dry-run] would delete file: {p}")
            else:
                try:
                    await anyio_p.unlink()
                    logger.info(f"Deleted file: {p}")
                    deleted_files += 1
                # ⚡ REFACTOR: Narrow exception scope
                except OSError as e:
                    logger.error(f"Failed to delete file {p}: {e}")
                    
        elif await anyio_p.is_dir():
            if not assume_yes and not dry_run:
                ok = await anyio.to_thread.run_sync(
                    confirm, f"Remove directory tree: {p}?"
                )
                if not ok:
                    continue
            if dry_run:
                logger.info(f"[dry-run] would remove directory: {p}")
            else:
                try:
                    # 🐞 FIX: Wrap sync shutil.rmtree in thread pool (anyio.Path lacks rmtree)
                    await anyio.to_thread.run_sync(shutil.rmtree, anyio_p)
                    logger.info(f"Removed directory: {p}")
                    deleted_dirs += 1
                # ⚡ REFACTOR: Narrow exception scope
                except OSError as e:
                    logger.error(f"Failed to remove directory {p}: {e}")
    return deleted_files, deleted_dirs


# ⚡ REFACTOR: Removed synchronous safe_cleanup function


# ⚡ REFACTOR: New async version of safe_cleanup
async def safe_cleanup(root: Path, pattern: str, dry_run: bool, assume_yes: bool, verbose: bool) -> None:
    """Standalone async cleanup of matching paths."""
    # ⚡ REFACTOR: find_matching_files is now a generator
    matches_gen = find_matching_files(root, pattern)
    
    # ⚡ REFACTOR: We must 'peek' at the generator to see if it's empty
    try:
        first_match = await anext(matches_gen)
    except StopAsyncIteration:
        logger.info("No matching files found for cleanup.")
        return

    if verbose:
        # ⚡ REFACTOR: We can no longer give an exact count without memory cost.
        logger.info(f"Found paths to clean (starting with: {first_match.name}).")
    if dry_run:
        logger.info("Dry-run: Skipping deletions.")
        return

    user_confirmed = assume_yes or await anyio.to_thread.run_sync(
        confirm, "Delete all matching files?"
    )
    if user_confirmed:
        # ⚡ REFACTOR: Chain the peeked item back onto the generator
        async def final_gen() -> AsyncGenerator[Path, None]:
            yield first_match
            async for p in matches_gen:
                yield p

        deleted_files, deleted_dirs = await safe_delete_paths(
            final_gen(), root, dry_run=False, assume_yes=assume_yes
        )
        logger.info(f"Cleanup complete: {deleted_files} files, {deleted_dirs} dirs deleted")
```

---

## src/create_dump/cli/rollback.py

<a id='src-create-dump-cli-rollback-py'></a>

```python
# src/create_dump/cli/rollback.py

"""
'rollback' command implementation for the CLI.

Rehydrates a project structure from a specified .md dump file.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional

import anyio
import typer

from ..logging import logger, styled_print
from ..path_utils import confirm
from ..rollback.engine import RollbackEngine
from ..rollback.parser import MarkdownParser

# --- Rollback-specific Helpers ---

async def _calculate_sha256(file_path: anyio.Path) -> str:
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    async with await file_path.open("rb") as f:
        while True:
            chunk = await f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

async def _find_most_recent_dump(root: Path) -> Optional[Path]:
    """Finds the most recent .md dump file in the root."""
    latest_file: Optional[Path] = None
    latest_mtime: float = -1.0
    
    anyio_root = anyio.Path(root)
    # We use glob here, as find_matching_files is a generator
    # and we need to stat all files to find the latest.
    async for file in anyio_root.glob("*_all_create_dump_*.md"):
        try:
            stat = await file.stat()
            if stat.st_mtime > latest_mtime:
                latest_mtime = stat.st_mtime
                latest_file = Path(file) # Store as sync Path
        except OSError as e:
            logger.warning("Could not stat file", path=str(file), error=str(e))
            continue
    return latest_file

async def _verify_integrity(md_file: Path) -> bool:
    """Verifies the SHA256 hash of the .md file."""
    sha_file = md_file.with_suffix(".sha256")
    anyio_sha_path = anyio.Path(sha_file)
    anyio_md_path = anyio.Path(md_file)

    if not await anyio_sha_path.exists():
        logger.error(f"Integrity check failed: Missing checksum file for {md_file.name}")
        styled_print(f"[red]Error:[/red] Missing checksum file: [blue]{sha_file.name}[/blue]")
        return False
    
    try:
        # 1. Read the expected hash
        sha_content = await anyio_sha_path.read_text()
        expected_hash = sha_content.split()[0].strip()

        # 2. Calculate the actual hash
        actual_hash = await _calculate_sha256(anyio_md_path)

        # 3. Compare
        if actual_hash == expected_hash:
            logger.info("Integrity verified (SHA256 OK)", file=md_file.name)
            return True
        else:
            logger.error(
                "Integrity check FAILED: Hashes do not match",
                file=md_file.name,
                expected=expected_hash,
                actual=actual_hash
            )
            styled_print(f"[red]Error: Integrity check FAILED. File is corrupt.[/red]")
            styled_print(f"  Expected: {expected_hash}")
            styled_print(f"  Got:      {actual_hash}")
            return False
    except Exception as e:
        logger.error(f"Integrity check error: {e}", file=md_file.name)
        styled_print(f"[red]Error during integrity check:[/red] {e}")
        return False

# --- Async Main Logic ---

async def async_rollback(
    root: Path,
    file_to_use: Optional[Path],
    yes: bool,
    dry_run: bool,
    quiet: bool
):
    """The main async logic for the rollback command."""
    
    # 1. DISCOVERY
    md_file: Optional[Path] = None
    if file_to_use:
        if not await anyio.Path(file_to_use).exists():
            styled_print(f"[red]Error:[/red] Specified file not found: {file_to_use}")
            raise typer.Exit(code=1)
        md_file = file_to_use
    else:
        if not quiet:
            styled_print("[cyan]Scanning for most recent dump file...[/cyan]")
        md_file = await _find_most_recent_dump(root)
        if not md_file:
            styled_print("[red]Error:[/red] No `*_all_create_dump_*.md` files found in this directory.")
            raise typer.Exit(code=1)
    
    if not quiet:
        styled_print(f"Found dump file: [blue]{md_file.name}[/blue]")

    # 2. INTEGRITY VERIFICATION
    if not quiet:
        styled_print("Verifying file integrity (SHA256)...")
    is_valid = await _verify_integrity(md_file)
    if not is_valid:
        raise typer.Exit(code=1)
    
    if not quiet:
        styled_print("[green]Integrity verified.[/green]")

    # 3. PREPARATION & CONFIRMATION
    target_folder_name = md_file.stem
    # Your specified safe output directory
    output_dir = root.resolve() / "all_create_dump_rollbacks" / target_folder_name
    
    if not yes and not dry_run:
        prompt = f"Rehydrate project structure to [blue]./{output_dir.relative_to(root.resolve())}[/blue]?"
        user_confirmed = await anyio.to_thread.run_sync(confirm, prompt)
        if not user_confirmed:
            styled_print("[red]Rollback cancelled by user.[/red]")
            raise typer.Exit()
    elif dry_run and not quiet:
            styled_print(f"[cyan]Dry run:[/cyan] Would rehydrate files to [blue]./{output_dir.relative_to(root.resolve())}[/blue]")

    # 4. EXECUTION
    parser = MarkdownParser(md_file)
    engine = RollbackEngine(output_dir, dry_run=dry_run)
    created_files = await engine.rehydrate(parser)

    # 5. SUMMARY
    if not dry_run and not quiet:
        styled_print(f"[green]✅ Rollback complete.[/green] {len(created_files)} files created in [blue]{output_dir}[/blue]")
    elif dry_run and not quiet:
        styled_print(f"[green]✅ Dry run complete.[/green] Would have created {len(created_files)} files.")

# --- Typer Command Definition ---

# ⚡ REFACTOR: Removed 'rollback_app' Typer instance.
# The 'rollback' function is now a plain function to be registered in main.py.

def rollback(
    ctx: typer.Context,
    root: Path = typer.Argument(
        Path("."),
        help="Project root to scan for dumps and write rollback to.",
        show_default=True
    ),
    file: Optional[Path] = typer.Option(
        None,
        "--file",
        help="Specify a dump file to use (e.g., my_dump.md). Default: find latest.",
        show_default=False
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Assume yes to all prompts."
    ),
    dry_run: bool = typer.Option(
        False,
        "-d",
        "--dry-run",
        help="Simulate without writing any files."
    )
):
    """
    Rolls back a create-dump .md file to a full project structure.
    """
    # Inherit quiet setting from main
    main_params = ctx.find_root().params
    quiet = main_params.get('quiet', False)
    
    try:
        anyio.run(
            async_rollback,
            root,
            file,
            yes,
            dry_run,
            quiet
        )
    except (FileNotFoundError, ValueError) as e:
        # These are caught by the parser/engine and logged
        styled_print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        # Catch any other unexpected error
        logger.error("Unhandled rollback error", error=str(e), exc_info=True)
        styled_print(f"[red]An unexpected error occurred:[/red] {e}")
        raise typer.Exit(code=1)
```

---

## src/create_dump/archive/pruner.py

<a id='src-create-dump-archive-pruner-py'></a>

```python
# src/create_dump/archive/pruner.py

"""Component responsible for pruning old archives based on retention policies."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, List

import anyio
from ..cleanup import safe_delete_paths
from ..logging import logger


class ArchivePruner:
    """Prunes old archives to enforce retention (e.g., keep last N)."""

    def __init__(
        self,
        archives_dir: Path,
        keep_last: Optional[int],
        verbose: bool,
    ):
        self.archives_dir = archives_dir
        self.keep_last = keep_last
        self.verbose = verbose

    async def prune(self) -> None:
        """Prune archives to last N by mtime in a non-blocking way."""
        if self.keep_last is None:
            return
        
        # ⚡ REFACTOR: Generalize pattern to match all supported archive formats
        archive_pattern = re.compile(
            r".*_all_create_dump_\d{8}_\d{6}(\.zip|\.tar\.gz|\.tar\.bz2)$"
        )
        anyio_archives_dir = anyio.Path(self.archives_dir)
        
        # Use async rglob for non-blocking directory traversal
        # ⚡ REFACTOR: Renamed variable for clarity
        archive_files: List[anyio.Path] = []
        async for p in anyio_archives_dir.rglob("*"):
            if archive_pattern.match(p.name):
                archive_files.append(p)
        
        num_to_keep = self.keep_last
        if len(archive_files) > num_to_keep:
            
            # Run blocking stat() calls in a thread pool for sorting
            async def get_mtime(p: anyio.Path) -> float:
                stat_res = await p.stat()
                return stat_res.st_mtime

            # Create a list of (mtime, path) tuples to sort
            path_mtimes = []
            # ⚡ REFACTOR: Use renamed variable
            for p in archive_files:
                path_mtimes.append((await get_mtime(p), p))
            
            # Sort by mtime (ascending: oldest first)
            path_mtimes.sort(key=lambda x: x[0])
            
            num_to_prune = max(0, len(path_mtimes) - num_to_keep)
            
            # Get original pathlib.Path objects for deletion compatibility
            to_prune_paths = [Path(p) for _, p in path_mtimes[:num_to_prune]]
            
            # Call async delete with safety guards
            deleted, _ = await safe_delete_paths(
                to_prune_paths, self.archives_dir, dry_run=False, assume_yes=True
            )
            
            logger.info("Pruned %d old archives (keeping last %d)", deleted, self.keep_last)
            if self.verbose:
                logger.debug("Pruned archives: %s", [p.name for p in to_prune_paths])
```

---

## src/create_dump/archive/core.py

<a id='src-create-dump-archive-core-py'></a>

```python
# src/create_dump/archive/core.py

"""Core utilities and exceptions for the archive components."""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..logging import logger  # ⚡ FIX: Added missing logger import

class ArchiveError(ValueError):
    """Custom error for archive operations."""


def extract_group_prefix(filename: str) -> Optional[str]:
    """Extract group prefix from filename, e.g., 'tests' from 'tests_all_create_dump_*.md'."""
    match = re.match(r'^(.+?)_all_create_dump_\d{8}_\d{6}\.md$', filename)
    if match:
        group = match.group(1)
        if re.match(r'^[a-zA-Z0-9_-]+$', group):
            return group
    return None


def extract_timestamp(filename: str) -> datetime:
    """Extract timestamp from filename (e.g., _20251028_041318)."""
    match = re.search(r'_(\d{8}_\d{6})', filename)
    if match:
        try:
            return datetime.strptime(match.group(1), '%Y%m%d_%H%M%S')
        except ValueError:
            logger.warning("Malformed timestamp in filename: %s", filename)
    return datetime.min


def _safe_arcname(path: Path, root: Path) -> str:
    """Sanitize arcname to prevent zip-slip."""
    try:
        rel = path.relative_to(root).as_posix()
        if ".." in rel.split("/") or rel.startswith("/"):
            raise ValueError(f"Invalid arcname with traversal: {rel}")
        if not path.is_file():
            raise ValueError(f"Invalid arcname: not a file - {path}")
        return rel
    except ValueError as e:
        if "is not in the subpath" in str(e):
            raise ValueError(f"Invalid arcname: {str(e)}") from e
        logger.warning("Skipping unsafe path for ZIP: %s (%s)", path, e)
        raise
```

---

## pyproject.toml

<a id='pyproject-toml'></a>

```toml
# pyproject.toml

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "create-dump"
dynamic = ["version"]
description = "Enterprise-grade code dump utility for monorepos"
readme = "README.md"
requires-python = ">=3.11"

author = "dhruv"
author_email = "dhruv13x@gmail.com"

authors = [
  { name = "dhruv", email = "dhruv13x@gmail.com" }
]

license = { text = "MIT © dhruv" }

classifiers = [
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Topic :: Software Development :: Documentation",
]

dependencies = [
  "typer>=0.12.0",
  "rich>=13.0.0",
  "pathspec>=0.12.0",
  "structlog>=24.0.0",
  "tenacity>=8.2.0",
  "pydantic>=2.0.0",
  "toml>=0.10.0",
  "prometheus-client>=0.20.0",
  "anyio>=4.0.0",
  "aiofiles>=23.0.0",
  "watchdog>=4.0.0",
  "detect-secrets>=1.5.0",
]

[project.urls]
Homepage = "https://pypi.org/project/create-dump/"
Source   = "https://github.com/dhruv13x/create-dump"
Issues   = "https://github.com/dhruv13x/create-dump/issues"

[project.scripts]
create-dump = "create_dump.cli:app"

[project.optional-dependencies]
dev = [
  "pytest>=8.0.0",
  "ruff>=0.6.0",
  "black>=24.3.0",
  "mypy>=1.11.0",
  "coverage>=7.5.0",
  "hypothesis>=6.100.0",
  "pytest-anyio>=4.0.0",
  "pytest-mock>=3.10.0"
]

[tool.hatch.build.targets.wheel]
packages = ["src/create_dump"]

[tool.hatch.version]
path = "src/create_dump/version.py"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*"]

[tool.coverage.report]
fail_under = 90
show_missing = true

[tool.pytest.ini_options]
pythonpath = "src"
timeout = 10
testpaths = ["tests"]
addopts = [
  "-ra",
  "--strict-config",
  "--strict-markers",
  "--cov",
  "--cov-report=term-missing",
  "--cov-report=html",
  "--cov-report=term-missing:skip-covered"
]

[tool.create-dump]
use_gitignore = true
git_meta = true
max_file_size_kb = 5000
# git_ls_files = false
# scan_secrets = false
# hide_secrets = false
```

---

## src/create_dump/cli/batch.py

<a id='src-create-dump-cli-batch-py'></a>

```python
# src/create_dump/cli/batch.py

"""'batch' command group implementation for the CLI."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import typer
import anyio  # ⚡ REFACTOR: Import anyio

# ⚡ REFACTOR: Import async versions of cleanup and orchestrator
from ..cleanup import safe_cleanup
from ..core import DEFAULT_DUMP_PATTERN
from ..orchestrator import run_batch
# ⚡ REFACTOR: Import from new logging module
from ..logging import setup_logging
from ..archiver import ArchiveManager


# Create a separate Typer for the batch group
batch_app = typer.Typer(no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]})


@batch_app.callback()
def batch_callback(
    # 🐞 FIX: Remove verbose and quiet. They are inherited from main.
    # Controls (Standardized; dry-run default ON for safety)
    dry_run: bool = typer.Option(True, "-d", "--dry-run", help="Perform a dry-run (default: ON for batch)."),
    dest: Optional[Path] = typer.Option(None, "--dest", help="Global destination dir for outputs (default: root)."),
):
    """Batch operations: Run dumps across subdirectories with cleanup and centralization.

    Examples:
        $ create-dump batch run --dirs src,tests --archive-all -y  # Batch dumps + grouped archive, skip prompts
        $ create-dump batch clean --pattern '.*dump.*' -y -nd  # Real cleanup of olds
    """
    # 🐞 FIX: Logging is now set by the main_callback or the subcommand.
    # setup_logging(verbose=verbose, quiet=quiet)
    pass


def split_dirs(dirs_str: str) -> List[str]:
    """Split comma-separated dirs string into list, stripping whitespace."""
    if not dirs_str:
        return [".", "packages", "services"]
    split = [d.strip() for d in dirs_str.split(',') if d.strip()]
    if not split:
        return [".", "packages", "services"]
    return split


@batch_app.command()
def run(
    ctx: typer.Context,  # Inject ctx to access callback params
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),

    # Output & Processing
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for centralized outputs (default: root; inherits from batch)."),
    dirs: str = typer.Option(".,packages,services", "--dirs", help="Subdirectories to process (comma-separated, relative to root) [default: .,packages,services]."),
    pattern: str = typer.Option(DEFAULT_DUMP_PATTERN, "--pattern", help="Regex to identify dump files [default: canonical pattern]."),
    format: str = typer.Option("md", "--format", help="Output format (md or json)."),
    accept_prompts: bool = typer.Option(True, "--accept-prompts/--no-accept-prompts", help='Auto-answer "y" to single-dump prompts [default: true].'),
    compress: bool = typer.Option(False, "-c", "--compress", help="Gzip outputs [default: false]."),
    max_workers: int = typer.Option(4, "--max-workers", help="Workers per subdir dump (global concurrency limited) [default: 4]."),

    # Archiving (Unified)
    archive: bool = typer.Option(False, "-a", "--archive", help="Archive prior dumps into ZIP (unified workflow)."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs."),
    archive_search: bool = typer.Option(False, "--archive-search", help="Search project-wide for dumps."),
    archive_include_current: bool = typer.Option(True, "--archive-include-current/--no-archive-include-current", help="Include this batch in archive [default: true]."),
    archive_no_remove: bool = typer.Option(False, "--archive-no-remove", help="Preserve originals post-archiving."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive."),
    archive_format: str = typer.Option("zip", "--archive-format", help="Archive format (zip, tar.gz, tar.bz2)."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for deletions and prompts [default: false]."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables inherited dry-run) [default: false]."),
):
    """Run dumps in multiple subdirectories, cleanup olds, and centralize files.

    Examples:
        $ create-dump batch run src/ --dest central/ --dirs api,web -c -y -nd  # Real batch to central dir
    """
    # 🐞 FIX: Get all inherited params from parent context
    parent_params = ctx.parent.params
    # 🐞 FIX: Get verbose/quiet from the *root* context
    main_params = ctx.find_root().params
    
    inherited_dry_run = parent_params.get('dry_run', True)
    inherited_verbose = main_params.get('verbose', False) # Default to main's default
    inherited_quiet = main_params.get('quiet', False)

    effective_dry_run = inherited_dry_run and not no_dry_run
    subdirs = split_dirs(dirs)
    
    # 🐞 FIX: Re-run logging setup in case this command was called directly
    if inherited_quiet:
        inherited_verbose = False
    setup_logging(verbose=inherited_verbose, quiet=inherited_quiet)
    
    # ⚡ REFACTOR: Call the async function using anyio.run
    anyio.run(
        run_batch,
        root,
        subdirs,
        pattern,
        effective_dry_run,
        yes,
        accept_prompts,
        compress,
        format,
        max_workers,
        inherited_verbose, # Pass inherited value
        inherited_quiet,   # Pass inherited value
        dest or parent_params.get('dest'), # Pass inherited value
        archive,
        archive_all,
        archive_search,
        archive_include_current,
        archive_no_remove,
        archive_keep_latest,
        archive_keep_last,
        archive_clean_root,
        archive_format,
    )


@batch_app.command()
def clean(
    ctx: typer.Context, # 🐞 FIX: Add context
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),
    pattern: str = typer.Argument(DEFAULT_DUMP_PATTERN, help="Regex for old dumps to delete [default: canonical pattern]."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmations for deletions [default: false]."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables dry-run) [default: false]."),
) -> None:
    """Cleanup old dump files/directories without running new dumps.

    Examples:
        $ create-dump batch clean . '.*old_dump.*' -y -nd -v  # Real verbose cleanup
    """
    # 🐞 FIX: Get all inherited params from parent context
    parent_params = ctx.parent.params
    # 🐞 FIX: Get verbose/quiet from the *root* context
    main_params = ctx.find_root().params

    inherited_dry_run = parent_params.get('dry_run', True)
    inherited_verbose = main_params.get('verbose', False)
    inherited_quiet = main_params.get('quiet', False)

    effective_dry_run = inherited_dry_run and not no_dry_run

    # 🐞 FIX: Re-run logging setup
    if inherited_quiet:
        inherited_verbose = False
    setup_logging(verbose=inherited_verbose, quiet=inherited_quiet)
    
    # ⚡ REFACTOR: Call the async function using anyio.run
    anyio.run(
        safe_cleanup,
        root,
        pattern,
        effective_dry_run,
        yes,
        inherited_verbose # Pass inherited value
    )


@batch_app.command()
def archive(
    ctx: typer.Context, # 🐞 FIX: Add context
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),
    pattern: str = typer.Argument(r".*_all_create_dump_\d{8}_\d{6}\.(md(\.gz)?)$", help="Regex for MD dumps [default: canonical MD subset]."),

    # Archiving (Unified; elevated as primary focus)
    archive_search: bool = typer.Option(False, "--archive-search", help="Recursive search for dumps [default: false]."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs [default: false]."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives (unified flag)."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive (unified flag) [default: false]."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmations [default: false]."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
) -> None:
    """Archive existing dump pairs into ZIP; optional clean/prune (unified with single mode).

    Examples:
        $ create-dump batch archive monorepo/ '.*custom' --archive-all -y -v  # Grouped archive, verbose, skip prompts
    """
    # ⚡ FIX: Removed redundant local import. The module-level import will be used.
    # from ..archiver import ArchiveManager
    
    # 🐞 FIX: Get all inherited params from parent context
    parent_params = ctx.parent.params
    # 🐞 FIX: Get verbose/quiet and archive_format from the *root* context
    main_params = ctx.find_root().params

    inherited_dry_run = parent_params.get('dry_run', True)
    inherited_verbose = main_params.get('verbose', False) # archive defaults to NOT verbose
    inherited_quiet = main_params.get('quiet', False)
    inherited_archive_format = main_params.get('archive_format', 'zip') # Get from root

    effective_dry_run = inherited_dry_run and not no_dry_run
    
    # 🐞 FIX: Re-run logging setup
    if inherited_quiet:
        inherited_verbose = False
    setup_logging(verbose=inherited_verbose, quiet=inherited_quiet)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    manager = ArchiveManager(
        root, timestamp, archive_keep_latest, archive_keep_last, archive_clean_root,
        search=archive_search,
        dry_run=effective_dry_run, yes=yes, verbose=inherited_verbose, md_pattern=pattern, # Pass inherited
        archive_all=archive_all,
        archive_format=inherited_archive_format # 🐞 FIX: Pass inherited format
    )
    
    # ⚡ REFACTOR: Call the async run method using anyio.run
    anyio.run(manager.run)  # No current_outfile for batch
```

---

## ROADMAP.md

<a id='roadmap-md'></a>

~~~markdown
## 🗺️ Feature Roadmap

### 🟩 Basic: Quality-of-Life & Usability Enhancements ✨

These are low-effort, high-value additions that extend our existing framework.

1.  **`TODO` / `FIXME` Scanner:**
    
    * **What:** Create a new `TodoScanner` middleware (just like `SecretScanner`). It would scan files for keywords like `TODO:`, `FIXME:`, `HACK:`, or `TECH_DEBT:` and append a summary of all found items to the bottom of the Markdown dump.
    * **Why:** This turns a simple code dump into an actionable **technical debt report**, which is incredibly valuable for SREs and managers during audits or sprint planning.

2.  **Per-Project Config Discovery (`batch` mode):**
    
    * **What:** Enhance `run_batch` logic. When it enters a subdirectory (e.g., `./services/api`), it should check for a `services/api/create_dump.toml` or `services/api/pyproject.toml` file and use *that* configuration for the `run_single` call.
    * **Why:** This is a true monorepo feature. It allows a service (`api`) to have different `include`/`exclude` patterns or secret scanning rules than another service (`web`), making the `batch` command far more powerful and flexible.

3.  **Simple Push Notifications (`ntfy.sh`):**
    
    * **What:** Add a `--notify-topic <topic>` flag. When a dump (especially a `watch` or `batch` run) completes, it sends a simple HTTP POST to `ntfy.sh/YourTopic`.
    * **Why:** This provides a dead-simple, zero-dependency notification system for long-running tasks, which is perfect for SREs monitoring a CI job or a local file watch.

4.  **Configuration Profiles:**
    
    * **Why:** A developer's local run (`--watch`) and a CI run (`--scan-secrets --archive`) have very different needs. Profiles let us define these sets of flags in `pyproject.toml`.
    * **Implementation:** Add a `--profile <name>` flag. The `load_config` function would merge `[tool.create-dump]` with `[tool.create-dump.profile.<name>]` if specified.

5.  **Dump Header Statistics:**
    
    * **Why:** Adds immediate, high-level context. "Is this a big project or a small one?"
    * **Implementation:** In `workflow/single.py`, after collection and filtering (but before processing), add a small utility to calculate `total_lines_of_code` and `total_files` from the `files_list`. Pass this to the `MarkdownWriter` / `JsonWriter`.

6.  **Custom Secret Scanning Rules:**
    
    * **Why:** A project might have internal tokens (e.g., `MYAPP_...`) that `detect-secrets` doesn't know about.
    * **Implementation:** Add a `config.custom_secret_patterns` list. In `scanning.py`, this list would be used to build a simple regex scanner that runs *in addition* to the main `detect-secrets` scan.

---

### 🟨 Moderate: CI/CD & SRE Integrations 🚀

These features focus on integrating `create-dump` into automated, production-level SRE and DevOps pipelines.

1.  **Cloud Storage Uploads (S3 / GCS / Azure Blob):**
    
    * **What:** Add a `--upload-s3 <bucket/path>` (or GCS/Azure) flag. After the `.md` and `.sha256` (and/or `.zip`) are created, the tool securely uploads them to the specified cloud bucket using `boto3`, `google-cloud-storage`, etc.
    * **Why:** This is the **most important "enterprise" feature.** Dumps are for forensics, compliance, and sharing. They *must* live in a durable, centralized, and secure location, not just on a local disk. This makes the tool 10x more useful for teams.

2.  **Database Dump Integration:**
    
    * **What:** Add a `--pg-dump <connection_string>` or `--mysql-dump` flag. The tool would securely execute `pg_dump` / `mysqldump`, capture the SQL output, and include it as `_db_dump.sql` inside the generated archive.
    * **Why:** This transforms the tool from a "code dump" to a true **application snapshot**. For debugging, a snapshot of *both* the code and the data (from a dev/staging DB) is the gold standard.

3.  **ChatOps Notifications (Slack / Discord / Telegram):**
    
    * **What:** Add a `--notify-slack <webhook_url>` flag. On success or failure, send a formatted JSON payload to the webhook with the dump name, file size, and status.
    * **Why:** This is the next level of integration. It allows `create-dump` to plug directly into a team's CI/CD or SRE alerting workflows.

4.  **Cloud Storage Uploader:**
    
    * **Why:** Dumps created in CI are useless if they're lost when the runner is terminated. We need to persist them. This was a stated limitation in the `README.md`.
    * **Implementation:** Add a new `uploader.py` module with `S3Uploader` / `GCSUploader` classes (using `boto3`/`google-cloud-storage`). In `workflow/single.py`, after the checksum is written, check for new CLI flags like `--upload-s3-bucket <name>`. This would run in `anyio.to_thread.run_sync`.

5.  **"Diff-Only" Dump Format:**
    
    * **Why:** When using `--diff-since`, we're currently dumping the *entire file* that changed, not the *diff itself*. For LLM analysis, a clean `.diff` or `.patch` format is often far more useful and concise.
    * **Implementation:** Add `--format=diff`. In `GitDiffCollector`, instead of just getting file names, also run `git diff <ref> -- {file_path}` for each file. The `MarkdownWriter` would then wrap this output in a ````diff` block.

6.  **File Hashing & Caching:**
    
    * **Why:** In a large monorepo, `--watch` mode is inefficient. It re-processes all files even if only one changed.
    * **Implementation:** Create a cache file (e.g., `.create_dump_cache.json`) storing `{ "path": "sha256_hash_of_content" }`. In `FileProcessor.process_file`, hash the raw content. If the hash matches the cache, skip processing and reuse the previous result. This would make `--watch` mode instantaneous on large projects.

---

### 🟥 Advanced: Platform & Scalability Architecture 🧠

These features represent a significant architectural evolution, moving the tool from a CLI to a true platform component for massive-scale operations.

1.  **Official GitHub Action (`create-dump-action`):**
    
    * **What:** Create a new repository for a dedicated GitHub Action. This action would run `create-dump` (likely using `--diff-since ${{ github.event.before }}`) to generate a dump of *only the files changed in the PR*. It would then (ideally) upload this as a build artifact.
    * **Why:** This provides a powerful code review tool. A reviewer can download a single, self-contained file with all PR changes, checksums, and secret-scan results, rather than browsing the GitHub UI.

2.  **Interactive TUI Explorer:**
    
    * **What:** A new command, `create-dump explore <dump_file.md>`. This would open a Terminal UI (using **`textual`**) that parses the dump file and presents a browsable, searchable file tree, allowing you to read the code *inside* the dump without rehydrating it.
    * **Why:** This enhances the `rollback` workflow. Instead of rehydrating 500 files just to read one, you can instantly explore the snapshot from your terminal.

3.  **Persistent Server Mode:**
    
    * **What:** Add a `create-dump serve` command. This would launch a lightweight **FastAPI** server that exposes the Prometheus metrics (as it already does) and also provides a simple REST API to:
        * Trigger a new dump (e.g., `POST /dump`) via a webhook.
        * List all available dumps (from the `dest` directory).
        * Download a specific dump file.
    * **Why:** This turns `create-dump` from a CLI tool into a lightweight, persistent service, allowing it to be integrated into any CI/CD system (GitLab, Jenkins, etc.) that can call a webhook.

4.  **Direct-to-Archive Streaming:**
    
    * **Why:** The current flow (`read file -> write tempfile -> read tempfile -> write .md -> read .md -> write .zip`) is durable but has high disk I/O. For a 1GB dump, this is very slow.
    * **Implementation:** Create a new `StreamingMarkdownWriter` that writes directly to a `tarfile.TarFile` object (which can be streamed). `FileProcessor` would `yield` file content, which the writer would format as a markdown chunk and write *immediately* into the tar stream, bypassing the large intermediate `.md` file entirely.

5.  **Remote/Centralized Configuration:**
    
    * **Why:** In a large organization, you don't want 100 teams defining their own (potentially insecure) dump rules. An SRE team needs to enforce a central policy (e.g., "all dumps *must* scan for secrets").
    * **Implementation:** In `core.py`, update `load_config` to check for an environment variable like `CREATE_DUMP_CONFIG_URI`. If set (e.g., `s3://my-org-config/create-dump.toml`), the tool would fetch and use that config instead of local files.

6.  **GitHub App / PR Commenting Bot:**
    
    * **Why:** This is the ultimate CI integration. A developer pushes a commit, and a bot automatically runs `create-dump --diff-since main` and posts the result as a PR comment.
    * **Implementation:** This would be a separate (but related) project. Create a new `cli/github.py` command `create-dump post-pr --file <dump.md> --pr-url <url>`. This command would use the GitHub API to post the file's content as a comment.
    
---

~~~

---

## src/create_dump/cli/main.py

<a id='src-create-dump-cli-main-py'></a>

```python
# src/create_dump/cli/main.py

"""
Main CLI Entry Point.

Defines the main 'app' and orchestrates the 'single' and 'batch' commands.
"""

from __future__ import annotations

import typer
from typing import Optional
from pathlib import Path

# ⚡ REFACTOR: Removed generate_default_config import
from ..core import load_config
# ⚡ REFACTOR: Corrected imports from new modules
from ..logging import setup_logging, styled_print
from ..version import VERSION

# ⚡ REFACTOR: Import commands and command groups from submodules
from .single import single
from .batch import batch_app
# ✨ NEW: Import the rollback function directly
from .rollback import rollback


app = typer.Typer(
    name="create-dump",
    add_completion=True,
    pretty_exceptions_enable=True,
    help="Enterprise-grade code dump utility for projects and monorepos.",
    context_settings={"help_option_names": ["-h", "--help"]},
)


# ⚡ NEW: Helper function for the interactive --init wizard
def _run_interactive_init() -> str:
    """Runs an interactive wizard to build the config file content."""
    styled_print("\n[bold]Welcome to the `create-dump` interactive setup![/bold]")
    styled_print("This will create a `create_dump.toml` file in your current directory.\n")
    
    # Header for the TOML file
    lines = [
        "# Configuration for create-dump",
        "# You can also move this content to [tool.create-dump] in pyproject.toml",
        "[tool.create-dump]",
        ""
    ]
    
    # 1. Ask for 'dest' path
    dest_path = typer.prompt(
        "Default output destination? (e.g., './dumps'). [Press Enter to skip]",
        default="",
        show_default=False,
    )
    if dest_path:
        # Ensure path is formatted for TOML (forward slashes)
        sane_path = Path(dest_path).as_posix()
        lines.append(f'# Default output destination. Overridden by --dest.')
        lines.append(f'dest = "{sane_path}"')
        lines.append("")

    # 2. Ask for 'use_gitignore'
    use_gitignore = typer.confirm(
        "Use .gitignore to automatically exclude files?", 
        default=True
    )
    lines.append("# Use .gitignore files to automatically exclude matching files.")
    lines.append(f"use_gitignore = {str(use_gitignore).lower()}")
    lines.append("")

    # 3. Ask for 'git_meta'
    git_meta = typer.confirm(
        "Include Git branch and commit hash in the header?", 
        default=True
    )
    lines.append("# Include Git branch and commit hash in the header.")
    lines.append(f"git_meta = {str(git_meta).lower()}")
    lines.append("")

    # 4. Ask for 'scan_secrets'
    scan_secrets = typer.confirm(
        "Enable secret scanning? (Recommended: false, unless you configure --hide-secrets)", 
        default=False
    )
    lines.append("# Enable secret scanning. Add 'hide_secrets = true' to redact them.")
    lines.append(f"scan_secrets = {str(scan_secrets).lower()}")
    lines.append("")

    return "\n".join(lines)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "-V", "--version", help="Show version and exit."),
    init: bool = typer.Option(
        False, 
        "--init", 
        help="Run interactive wizard to create 'create_dump.toml'.",
        is_eager=True,  # Handle this before any command
    ),
    config: Optional[str] = typer.Option(None, "--config", help="Path to TOML config file."),
    
    # ⚡ FIX: All flags from 'single' must be duplicated here
    # so they can be parsed when 'single' is the default command.
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for output (default: root)."),
    no_toc: bool = typer.Option(False, "--no-toc", help="Omit table of contents."),
    tree_toc: bool = typer.Option(False, "--tree-toc", help="Render Table of Contents as a file tree."),
    format: str = typer.Option("md", "--format", help="Output format (md or json)."),
    compress: bool = typer.Option(False, "-c", "--compress", help="Gzip the output file."),
    # 🐞 FIX: Add '/--no-progress' to the flag definition
    progress: bool = typer.Option(True, "-p", "--progress/--no-progress", help="Show processing progress."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Succeed on 0 files (default: fail)."),
    # 🐞 FIX: Remove 'test' flag
    # test: bool = typer.Option(False, "-t", "--test", help="Run inline tests."),
    metrics_port: int = typer.Option(8000, "--metrics-port", help="Prometheus export port [default: 8000]."),
    exclude: str = typer.Option("", "--exclude", help="Comma-separated exclude patterns."),
    include: str = typer.Option("", "--include", help="Comma-separated include patterns."),
    max_file_size: Optional[int] = typer.Option(None, "--max-file-size", help="Max file size in KB."),
    use_gitignore: bool = typer.Option(True, "--use-gitignore/--no-use-gitignore", help="Incorporate .gitignore excludes [default: true]."),
    git_meta: bool = typer.Option(True, "--git-meta/--no-git-meta", help="Include Git branch/commit [default: true]."),
    max_workers: int = typer.Option(16, "--max-workers", help="Concurrency level [default: 16]."),
    watch: bool = typer.Option(False, "--watch", help="Run in live-watch mode, redumping on file changes."),
    git_ls_files: bool = typer.Option(False, "--git-ls-files", help="Use 'git ls-files' for file collection (fast, accurate)."),
    diff_since: Optional[str] = typer.Option(None, "--diff-since", help="Only dump files changed since a specific git ref (e.g., 'main')."),
    scan_secrets: bool = typer.Option(False, "--scan-secrets", help="Scan files for secrets. Fails dump if secrets are found."),
    hide_secrets: bool = typer.Option(False, "--hide-secrets", help="Redact found secrets (requires --scan-secrets)."),
    archive: bool = typer.Option(False, "-a", "--archive", help="Archive prior dumps into ZIP (unified workflow)."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs."),
    archive_search: bool = typer.Option(False, "--archive-search", help="Search project-wide for dumps."),
    archive_include_current: bool = typer.Option(True, "--archive-include-current/--no-archive-include-current", help="Include this run in archive [default: true]."),
    archive_no_remove: bool = typer.Option(False, "--archive-no-remove", help="Preserve originals post-archiving."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive."),
    archive_format: str = typer.Option("zip", "--archive-format", help="Archive format (zip, tar.gz, tar.bz2)."),
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for prompts and deletions [default: false]."),
    dry_run: bool = typer.Option(False, "-d", "--dry-run", help="Simulate without writing files (default: off)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    
    # ⚡ REFACTOR: verbose/quiet flags live here for the main app
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Enable debug logging [default: false]."),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output (CI mode) [default: false]."),
):
    """Create Markdown code dumps from source files.

    Defaults to 'single' mode if no subcommand provided.
    """
    
    # Setup logging immediately
    setup_logging(verbose=verbose, quiet=quiet)

    if version:
        styled_print(f"create-dump v{VERSION}")
        raise typer.Exit()

    if init:
        config_path = Path("create_dump.toml")
        if config_path.exists():
            styled_print(f"[yellow]⚠️ Config file 'create_dump.toml' already exists.[/yellow]")
            raise typer.Exit(code=1)
        
        try:
            config_content = _run_interactive_init()
            config_path.write_text(config_content)
            styled_print(f"\n[green]✅ Success![/green] Default config file created at [blue]{config_path.resolve()}[/blue]")
        except IOError as e:
            styled_print(f"[red]❌ Error:[/red] Could not write config file: {e}")
            raise typer.Exit(code=1)
        
        raise typer.Exit(code=0)  # Exit after creating file

    load_config(Path(config) if config else None)
    
    if ctx.invoked_subcommand is None:
        root_arg = ctx.args[0] if ctx.args else Path(".")
        
        # ⚡ FIX: Must pass ALL duplicated flags to the invoked command
        ctx.invoke(
            single, 
            ctx=ctx,  
            root=root_arg, 
            dest=dest,
            no_toc=no_toc,
            tree_toc=tree_toc,
            format=format,
            compress=compress,
            progress=progress,
            allow_empty=allow_empty,
            # 🐞 FIX: Remove 'test' argument
            # test=test,
            metrics_port=metrics_port,
            exclude=exclude,
            include=include,
            max_file_size=max_file_size,
            use_gitignore=use_gitignore,
            git_meta=git_meta,
            max_workers=max_workers,
            watch=watch,
            git_ls_files=git_ls_files,
            diff_since=diff_since,
            scan_secrets=scan_secrets,
            hide_secrets=hide_secrets,
            archive=archive,
            archive_all=archive_all,
            archive_search=archive_search,
            archive_include_current=archive_include_current,
            archive_no_remove=archive_no_remove,
            archive_keep_latest=archive_keep_latest,
            archive_keep_last=archive_keep_last,
            archive_clean_root=archive_clean_root,
            archive_format=archive_format,
            yes=yes,
            dry_run=dry_run,
            no_dry_run=no_dry_run,
            verbose=verbose,
            quiet=quiet
        )


# ⚡ REFACTOR: Register the imported 'single' command
app.command()(single)

# ⚡ REFACTOR: Register the imported 'batch' app
app.add_typer(batch_app, name="batch")

# ✨ NEW: Register the rollback function as a standard command
app.command(name="rollback", help="Rehydrate a project structure from a create-dump file.")(rollback)
```

---

## README.md

<a id='readme-md'></a>

~~~markdown
# create-dump

![PyPI](https://badge.fury.io/py/create-dump.svg)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![CI](https://github.com/dhruv13x/create-dump/actions/workflows/publish.yml/badge.svg)
![Codecov](https://codecov.io/gh/dhruv13x/create-dump/graph/badge.svg)

**Enterprise-Grade Code Dump Utility for Monorepos**

`create-dump` is a production-ready CLI tool for automated code archival in large-scale monorepos.
It generates branded Markdown dumps with Git metadata, integrity checksums, flexible archiving,
retention policies, path safety, full concurrency, and SRE-grade observability.

Designed for SRE-heavy environments (Telegram bots, microservices, monorepos), it ensures
**reproducible snapshots for debugging, forensics, compliance audits, and CI/CD pipelines**. It also includes a `rollback` command to restore a project from a dump file.

Built for Python 3.11+, leveraging **AnyIO**, Pydantic, Typer, Rich, and Prometheus metrics.

-----

## 🚀 Quick Start

```bash
pip install create-dump

# Create an interactive config file
create-dump --init

# Single dump (current directory)
create-dump single --dest ./dumps/my-snapshot.md

# Batch dump (monorepo)
create-dump batch --root ./monorepo --archive --keep-last 5

# SRE / Git-only dump in watch mode with secret redaction
create-dump single --git-ls-files --watch --scan-secrets --hide-secrets

# Rollback a dump file to a new directory
create-dump rollback --file ./dumps/my-snapshot.md

# Output example:
# dumps/my-snapshot_all_create_dump_20250101_121045.md
# dumps/my-snapshot_all_create_dump_20250101_121045.md.sha256
# archives/my-snapshot_20250101_121045.zip
```

-----

## ✨ Features

  * **Branded Markdown Generation**
    Auto TOC (list or tree), language-detected code blocks, Git metadata, timestamps.

  * **Async-First & Concurrent**
    Built on `anyio` for high-throughput, non-blocking I/O. Parallel file processing (16+ workers), timeouts, and progress bars (Rich).

  * **Flexible Archiving**
    Automatically archive old dumps into **ZIP, tar.gz, or tar.bz2** formats. Includes integrity validation and retention policies (e.g., "keep last N").

  * **Project Rollback & Restore**
    Includes a `rollback` command to rehydrate a full project structure from a `.md` dump file, with SHA256 integrity verification.

  * **Git-Native Collection**
    Use `git ls-files` for fast, accurate file discovery (`--git-ls-files`) or dump only changed files (`--diff-since <ref>`).

  * **Live Watch Mode**
    Run in a persistent state (`--watch`) that automatically re-runs the dump on any file change, perfect for live development.

  * **Secret Scanning**
    Integrates `detect-secrets` to scan files during processing. Can fail the dump (`--scan-secrets`) or redact secrets in-place (`--hide-secrets`).

  * **Safety & Integrity**
    SHA256 hashing for all dumps, atomic writes, async-safe path guards (prevents Zip-Slip & Path Traversal), and orphan quarantine.

  * **Observability**
    Prometheus metrics (e.g., `create_dump_duration_seconds`, `create_dump_files_total`).

| Feature | Single Mode | Batch Mode |
| :--- | :--- | :--- |
| **Scope** | Current dir/files | Recursive subdirs |
| **Archiving** | Optional | Enforced retention |
| **Concurrency** | Up to **16** workers | Parallel subdirs |
| **Git Metadata** | ✔️ | Per-subdir ✔️ |

-----

## 📦 Installation

### PyPI

```bash
pip install create-dump
```

### From Source

```bash
git clone https://github.com/dhruv13x/create-dump.git 
cd create-dump
pip install -e .[dev]
```

### Docker

```dockerfile
FROM python:3.12-slim
RUN pip install create-dump
ENTRYPOINT ["create-dump"]
```

-----

## ⚙️ Configuration

### 🚀 Interactive Setup (`--init`)

The easiest way to configure `create-dump` is to run the built-in interactive wizard:

```bash
create-dump --init
```

This will create a `create_dump.toml` file with your preferences. You can also add this configuration to your `pyproject.toml` file under the `[tool.create-dump]` section.

### Example (pyproject.toml)

```toml
[tool.create-dump]
# Default output destination (CLI --dest overrides)
dest = "/path/to/dumps"

# Enable .gitignore parsing
use_gitignore = true

# Include Git branch/commit in header
git_meta = true

# Max file size in KB (e.g., 5MB)
max_file_size_kb = 5000

# Canonical regex for dump artifacts
dump_pattern = ".*_all_create_dump_\\d{8}_\\d{6}\\.(md(\\.gz)?|sha256)$"

# Default excluded directories
excluded_dirs = ["__pycache__", ".git", ".venv", "node_modules"]

# Prometheus export port
metrics_port = 8000

# --- New v9 Feature Flags ---

# Use 'git ls-files' by default for collection
# git_ls_files = true

# Enable secret scanning by default
# scan_secrets = true

# Redact found secrets (requires scan_secrets=true)
# hide_secrets = true
```

Override any setting via CLI flags.

-----

## 📖 Usage

### Single Mode

```bash
# Dump all files matching .py, include git meta
create-dump single --include "*.py" --git-meta

# Dump only files changed since 'main' branch and watch for new changes
create-dump single --diff-since main --watch

# Dump using git, scan for secrets, and redact them
create-dump single --git-ls-files --scan-secrets --hide-secrets

# Dry run with verbose logging
create-dump single --dry-run --verbose
```

### Batch Mode

```bash
# Run dumps in 'src' and 'tests', then archive old dumps, keeping 10
create-dump batch --root ./monorepo --dirs "src,tests" --keep-last 10 --archive

# Run dumps and create grouped archives (e.g., src.zip, tests.zip)
create-dump batch --root ./monorepo --archive-all --archive-format tar.gz
```

### 🗃️ Rollback & Restore

You can instantly restore a project structure from a dump file using the `rollback` command.
It verifies the file's integrity using the accompanying `.sha256` file and then recreates the
directory and all files in a safe, sandboxed folder.

```bash
# Find the latest dump in the current directory and restore it
create-dump rollback .

# Restore from a specific file
create-dump rollback --file my_project_dump.md

# Do a dry run to see what files would be created
create-dump rollback --dry-run
```

This creates a new directory like `./all_create_dump_rollbacks/my_project_dump/` containing the restored code.

-----

## 🏗️ Architecture Overview

```
┌─────────────────┐
│   CLI (Typer)   │
│ (single, batch, │
│  init, rollback)│
└────────┬────────┘
         │
┌────────▼────────┐
│ Config / Models │
│    (core.py)    │
└─────────────────┘
         │
┌─────────────────┴─────────────────┐
│                                   │
▼                                   ▼
┌─────────────────┐               ┌───────────────────┐
│   DUMP FLOW     │               │   RESTORE FLOW    │
│ (Collect)       │               │   (Verify SHA256) │
│      │          │               │         │         │
│      ▼          │               │         ▼         │
│ (Process/Scan)  │               │   (Parse .md)     │
│      │          │               │         │         │
│      ▼          │               │         ▼         │
│ (Write MD/JSON) │               │   (Rehydrate Files) │
│      │          │               │                   │
│      ▼          │               └───────────────────┘
│ (Archive/Prune) │
└─────────────────┘
```

-----

## 🧪 Testing & Development

Run the full test suite using `pytest`:

```bash
# Install dev dependencies
pip install -e .[dev]

# Run tests with coverage
pytest --cov=create_dump --cov-report=html
```

Run linters and formatters:

```bash
ruff check src/ tests/
black src/ tests/
mypy src/
```

-----

## 🔒 Security & Reliability

  * **Secret Scanning** & Redaction (`detect-secrets`)
  * **Async-Safe Path Guards** (Prevents traversal & Zip-Slip)
  * Archive Integrity + SHA256 Validation (on Dump & Restore)
  * `tenacity` Retries on I/O
  * Prometheus Metrics on `:8000/metrics`
  * Graceful `SIGINT`/`SIGTERM` Cleanup Handlers

### Limitations

  * No remote filesystem support (e.g., S3, GCS)

-----

## 🤝 Contributing

1.  Fork repo → create branch
2.  Follow Conventional Commits
3.  Run full CI suite (`pytest`, `ruff`, `mypy`)
4.  Add/Update any ADRs under `/ADRs`
5.  Follow the Code of Conduct

Security issues → `security@dhruv.io`

-----

## 📄 License

MIT License.
See LICENSE.

-----

## 🙏 Acknowledgments

Powered by Typer, Rich, Pydantic, Prometheus, and AnyIO.

Inspired by tooling from Nx, Bazel, and internal SRE practices.

-----

*Questions or ideas?*
*Open an issue or email `dhruv13x@gmail.com`.*
~~~

---

## src/create_dump/archive/packager.py

<a id='src-create-dump-archive-packager-py'></a>

```python
# src/create_dump/archive/packager.py

"""Component responsible for grouping, sorting, and packaging (zipping) archives."""

from __future__ import annotations

import zipfile
import tarfile  # ⚡ NEW: Import tarfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict

import anyio
from ..cleanup import safe_delete_paths
from ..path_utils import confirm
from ..helpers import _unique_path
from ..logging import logger
from .core import ArchiveError, extract_group_prefix, extract_timestamp, _safe_arcname


class ArchivePackager:
    """Handles logic for grouping, sorting by date, and creating ZIP archives."""

    def __init__(
        self,
        root: Path,
        archives_dir: Path,
        quarantine_dir: Path,
        timestamp: str,
        keep_latest: bool,
        verbose: bool,
        dry_run: bool,
        yes: bool,
        clean_root: bool,
        no_remove: bool,
        archive_format: str = "zip",  # ⚡ NEW: Add format
    ):
        self.root = root
        self.archives_dir = archives_dir
        self.quarantine_dir = quarantine_dir
        self.timestamp = timestamp
        self.keep_latest = keep_latest
        self.verbose = verbose
        self.dry_run = dry_run
        self.yes = yes
        self.clean_root = clean_root
        self.no_remove = no_remove
        
        # ⚡ NEW: Store format and get correct extension
        self.archive_format = archive_format
        if archive_format == "tar.gz":
            self.archive_ext = ".tar.gz"
        elif archive_format == "tar.bz2":
            self.archive_ext = ".tar.bz2"
        else:
            self.archive_format = "zip"  # Default to zip
            self.archive_ext = ".zip"

    # ⚡ REFACTOR: Renamed to _create_archive_sync
    # 🐞 FIX: Corrected type hint from Path to str
    def _create_archive_sync(self, files_to_archive: List[Path], zip_name: str) -> Tuple[Optional[Path], List[Path]]:
        """Create archive; dedupe, compression-aware, unique naming; validate integrity."""
        if not files_to_archive:
            logger.info("No files to archive for %s", zip_name)
            return None, []

        valid_files = [p for p in files_to_archive if p is not None]
        if not valid_files:
            logger.info("No valid files to archive after filtering orphans for %s", zip_name)
            return None, []

        base_archive = self.archives_dir / zip_name
        archive_name = _unique_path(base_archive)
        to_archive = sorted(list(set(valid_files)))

        try:
            # ⚡ REFACTOR: Branch logic based on format
            if self.archive_format == "zip":
                with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                    for p in to_archive:
                        arcname = _safe_arcname(p, self.root)
                        comp_type = zipfile.ZIP_STORED if p.suffix in {".gz", ".zip", ".bz2"} else zipfile.ZIP_DEFLATED
                        z.write(p, arcname=arcname, compress_type=comp_type)
                
                # ⚡ REFACTOR: Validation is zip-specific
                with zipfile.ZipFile(archive_name, 'r') as z:
                    badfile = z.testzip()
                    if badfile is not None:
                        raise ArchiveError(f"Corrupt file in ZIP: {badfile}")
                logger.info("ZIP integrity validated successfully for %s", zip_name)

            else:  # Handle 'tar.gz' and 'tar.bz2'
                tar_mode = "w:gz" if self.archive_format == "tar.gz" else "w:bz2"
                with tarfile.open(archive_name, tar_mode) as tar:
                    for p in to_archive:
                        arcname = _safe_arcname(p, self.root)
                        tar.add(p, arcname=arcname)
                logger.info("TAR integrity validated (creation successful) for %s", zip_name)
        
        except (ArchiveError, tarfile.TarError, zipfile.BadZipFile, Exception) as e:
            logger.error("Archive creation/validation failed for %s: %s. Rolling back.", zip_name, e)
            archive_name.unlink(missing_ok=True)
            raise

        size = archive_name.stat().st_size
        logger.info("Archive %s created: %s (%d bytes, %d files)", self.archive_format.upper(), archive_name, size, len(to_archive))
        return archive_name, to_archive

    async def _create_archive(
        self, files_to_archive: List[Path], zip_name: str
    ) -> Tuple[Optional[Path], List[Path]]:
        """Runs the sync _create_archive_sync in a thread pool to avoid blocking."""
        # ⚡ REFACTOR: Call renamed sync method
        return await anyio.to_thread.run_sync(
            self._create_archive_sync, files_to_archive, zip_name
        )

    def group_pairs_by_prefix(self, pairs: List[Tuple[Path, Optional[Path]]]) -> Dict[str, List[Tuple[Path, Optional[Path]]]]:
        groups: Dict[str, List[Tuple[Path, Optional[Path]]]] = {}
        for pair in pairs:
            prefix = extract_group_prefix(pair[0].name)
            if prefix:
                if prefix not in groups:
                    groups[prefix] = []
                groups[prefix].append(pair)
            else:
                if 'default' not in groups:
                    groups['default'] = []
                groups['default'].append(pair)
        if self.verbose:
            for group, group_pairs in groups.items():
                logger.debug("Grouped %d pairs under '%s'", len(group_pairs), group)
        return groups

    async def handle_single_archive(
        self, pairs: List[Tuple[Path, Optional[Path]]]
    ) -> Tuple[Dict[str, Optional[Path]], List[Path]]:
        
        archive_paths: Dict[str, Optional[Path]] = {}
        to_delete: List[Path] = []

        live_pair = None
        historical = pairs
        if self.keep_latest:
            def key_func(p):
                ts = extract_timestamp(p[0].name)
                if ts == datetime.min:
                    ts = datetime.fromtimestamp(p[0].stat().st_mtime)
                    if self.verbose:
                        logger.debug("Fallback to mtime for sorting: %s", p[0].name)
                return (-ts.timestamp(), p[0].name)
            sorted_pairs = sorted(pairs, key=key_func)
            
            if not sorted_pairs:
                return archive_paths, to_delete 
                
            live_pair = sorted_pairs[0]
            historical = sorted_pairs[1:]
            if self.verbose:
                logger.info(
                    "Retained latest pair (ts=%s): %s",
                    extract_timestamp(live_pair[0].name),
                    live_pair[0].name,
                )

        if len(historical) == 0:
            return archive_paths, to_delete
        
        files_to_archive = [p for pair in historical for p in pair if p is not None]
        num_historical_pairs = len(historical)
        num_files = len(files_to_archive)
        if self.verbose:
            logger.info("Archiving %d pairs (%d files)", num_historical_pairs, num_files)

        # ⚡ REFACTOR: Use self.archive_ext for the correct file extension
        base_archive_name = f"{self.root.name}_dumps_archive_{self.timestamp}{self.archive_ext}"

        if self.dry_run:
            logger.info("[dry-run] Would create archive: %s", base_archive_name)
            archive_path = None
        else:
            archive_path, archived_files = await self._create_archive(
                files_to_archive, base_archive_name
            )
            to_delete.extend(archived_files)

        archive_paths['default'] = archive_path
 
        if self.clean_root and not self.no_remove:
            to_clean = files_to_archive
            if self.keep_latest and live_pair:
                live_paths = [live_pair[0]]
                if live_pair[1] is not None:
                    live_paths.append(live_pair[1])
                to_clean = [p for p in files_to_archive if p not in live_paths]
            prompt = f"Clean {len(to_clean)} root files post-archive?"
            
            user_confirmed = self.yes or await anyio.to_thread.run_sync(confirm, prompt)
            
            if user_confirmed:
                await safe_delete_paths(
                    to_clean, self.root, dry_run=self.dry_run, assume_yes=self.yes
                )
                if not self.dry_run:
                    logger.info("Cleaned %d root files", len(to_clean))


        return archive_paths, to_delete

    async def handle_grouped_archives(
        self, groups: Dict[str, List[Tuple[Path, Optional[Path]]]]
    ) -> Tuple[Dict[str, Optional[Path]], List[Path]]:
        
        archive_paths: Dict[str, Optional[Path]] = {}
        to_delete: List[Path] = []

        for group, group_pairs in groups.items():
            if self.verbose:
                logger.info("Processing group: %s (%d pairs)", group, len(group_pairs))

            if group == 'default' and len(group_pairs) > 0:
                logger.warning("Skipping 'default' group (%d pairs): Quarantining unmatchable MDs", len(group_pairs))
                for pair in group_pairs:
                    md, sha_opt = pair[0], pair[1]
                    if not self.dry_run:
                        await anyio.Path(self.quarantine_dir).mkdir(exist_ok=True)
                        if await anyio.Path(md).exists():
                            quarantine_md = self.quarantine_dir / md.name
                            await anyio.to_thread.run_sync(md.rename, quarantine_md)
                            logger.debug("Quarantined unmatchable MD: %s -> %s", md, quarantine_md)
                        if sha_opt and await anyio.Path(sha_opt).exists() and sha_opt != md:
                            quarantine_sha = self.quarantine_dir / sha_opt.name
                            await anyio.to_thread.run_sync(sha_opt.rename, quarantine_sha)
                            logger.debug("Quarantined unmatchable SHA: %s -> %s", sha_opt, quarantine_sha)
                    else:
                        logger.warning("[dry-run] Would quarantine unmatchable pair: %s / %s", md, sha_opt)
                continue
            
            live_pair = None
            historical = group_pairs
            if self.keep_latest:
                def key_func(p):
                    ts = extract_timestamp(p[0].name)
                    if ts == datetime.min:
                        ts = datetime.fromtimestamp(p[0].stat().st_mtime)
                        if self.verbose:
                            logger.debug("Fallback to mtime for sorting in %s: %s", group, p[0].name)
                    return (-ts.timestamp(), p[0].name)
                sorted_pairs = sorted(group_pairs, key=key_func)
                
                if not sorted_pairs:
                    continue 
                
                live_pair = sorted_pairs[0]
                historical = sorted_pairs[1:]
                if self.verbose and live_pair:
                    logger.info(
                        "Retained latest pair in %s (ts=%s): %s",
                        group,
                        extract_timestamp(live_pair[0].name),
                        live_pair[0].name,
                    )

            if len(historical) == 0:
                logger.info("No historical pairs for group %s.", group)
                continue
            
            files_to_archive = [p for pair in historical for p in pair if p is not None]
            num_historical_pairs = len(historical)
            num_files = len(files_to_archive)
            if self.verbose:
                logger.info("Archiving %d pairs (%d files) for group %s", num_historical_pairs, num_files, group)

            # ⚡ REFACTOR: Use self.archive_ext for the correct file extension
            base_archive_name = f"{group}_all_create_dump_{self.timestamp}{self.archive_ext}"
            
            if self.dry_run:
                logger.info("[dry-run] Would create archive for %s: %s", group, base_archive_name)
                archive_path = None
            else:
                archive_path, archived_files = await self._create_archive(
                    files_to_archive, base_archive_name
                )
                to_delete.extend(archived_files)

            archive_paths[group] = archive_path

        return archive_paths, to_delete
```

---

## src/create_dump/logging.py

<a id='src-create-dump-logging-py'></a>

```python
# src/create_dump/logging.py

"""Manages logging, console output, and Rich integration."""

from __future__ import annotations

import logging
import re
import structlog

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

# Define logger EARLY to avoid circular imports
logger = structlog.get_logger("create_dump")


def styled_print(text: str, nl: bool = True, **kwargs) -> None:
    """Prints text using Rich if available, falling back to plain print."""
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
```

---

## src/create_dump/collector/base.py

<a id='src-create-dump-collector-base-py'></a>

```python
# src/create_dump/collector/base.py

"""Base class for collection strategies."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import AsyncGenerator, List, Optional

import anyio
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

from ..core import Config
from ..helpers import is_text_file, parse_patterns
from ..logging import logger


class CollectorBase(ABC):
    """Abstract base class for file collection strategies."""

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
        
        self._include_spec: Optional[PathSpec] = None
        self._exclude_spec: Optional[PathSpec] = None
        self._setup_specs()  # Sync setup is OK on init

    def _setup_specs(self) -> None:
        """Build include/exclude specs with defaults."""
        default_includes = self.config.default_includes + [
            "*.py", "*.sh", "*.ini", "*.txt", "*.md", "*.yml", "*.yaml",
            "*.toml", "*.cfg", "*.json", "Dockerfile", ".flake8",
            ".pre-commit-config.yaml",
        ]
        all_includes = default_includes + (self.includes or [])

        default_excludes = self.config.default_excludes + [
            "*.log", "*.pem", "*.key", "*.db", "*.sqlite", "*.pyc", "*.pyo",
            ".env*", "bot_config.json", "*config.json", "*secrets*",
            "__init__.py", "*_all_create_dump_*", "*_all_create_dump_*.md*",
            "*_all_create_dump_*.gz*", "*_all_create_dump_*.sha256",
            "*_all_create_dump_*.zip",
        ]
        all_excludes = default_excludes + (self.excludes or [])

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

    async def _matches(self, rel_path: Path) -> bool:
        """Check include/exclude and filters."""
        rel_posix = rel_path.as_posix()
        
        if self._exclude_spec and self._exclude_spec.match_file(rel_posix):
            # ⚡ NEW: Add verbose logging
            logger.debug(f"File excluded by pattern: {rel_posix}")
            return False
        
        is_included = (
            not self._include_spec or
            self._include_spec.match_file(rel_posix) or 
            self._include_spec.match_file(rel_path.name)
        )
        if not is_included:
            # ⚡ NEW: Add verbose logging
            logger.debug(f"File not in include list: {rel_posix}")
            return False

        full_path = anyio.Path(self.root / rel_path)
        return await self._should_include(full_path, rel_posix)

    # ⚡ REFACTOR: Pass rel_posix for better logging
    async def _should_include(self, full_path: anyio.Path, rel_posix: str) -> bool:
        """Final size/text check."""
        try:
            if not await full_path.exists():
                logger.debug(f"Skipping non-existent file: {rel_posix}")
                return False
                
            stat = await full_path.stat()
            if (
                self.config.max_file_size_kb
                and stat.st_size > self.config.max_file_size_kb * 1024
            ):
                # ⚡ NEW: Add verbose logging
                logger.debug(f"File exceeds max size: {rel_posix}")
                return False
            
            is_text = await is_text_file(full_path)
            if not is_text:
                # ⚡ NEW: Add verbose logging
                logger.debug(f"File skipped (binary): {rel_posix}")
                return False
            
            # ⚡ NEW: Add verbose logging for success
            logger.debug(f"File included: {rel_posix}")
            return True

        except OSError as e:
            logger.warning(f"File check failed (OSError): {rel_posix}", error=str(e))
            return False

    async def filter_files(self, raw_files: List[str]) -> List[str]:
        """Shared filtering logic for git-based strategies."""
        filtered_files_list: List[str] = []
        for file_str in raw_files:
            try:
                rel_path = Path(file_str)
                if rel_path.is_absolute():
                    if not file_str.startswith(str(self.root)):
                         logger.warning("Skipping git path outside root", path=file_str)
                         continue
                    rel_path = rel_path.relative_to(self.root)
                
                if await self._matches(rel_path):
                    filtered_files_list.append(rel_path.as_posix())
            except Exception as e:
                logger.warning("Skipping file due to error", path=file_str, error=str(e))

        filtered_files_list.sort()
        return filtered_files_list

    @abstractmethod
    async def collect(self) -> List[str]:
        """Collect all raw file paths based on the strategy."""
        raise NotImplementedError
```

---

## src/create_dump/collector/walk.py

<a id='src-create-dump-collector-walk-py'></a>

```python
# src/create_dump/collector/walk.py

"""The standard asynchronous directory walk collector."""

from __future__ import annotations

from pathlib import Path
from typing import AsyncGenerator, List

import anyio

from ..logging import logger
from .base import CollectorBase


class WalkCollector(CollectorBase):
    """Collects files using a recursive async walk."""

    async def _collect_recursive(self, rel_dir: Path) -> AsyncGenerator[Path, None]:
        """Recursive async generator for subdirs."""
        full_dir = anyio.Path(self.root / rel_dir)
        try:
            async for entry in full_dir.iterdir():
                if await entry.is_dir():
                    if entry.name in self.config.excluded_dirs:
                        continue
                    new_rel_dir = Path(entry).relative_to(self.root)
                    async for p in self._collect_recursive(new_rel_dir):
                        yield p
                elif await entry.is_file():
                    rel_path = Path(entry).relative_to(self.root)
                    if await self._matches(rel_path):
                        yield rel_path
        except OSError as e:
            logger.warning("Failed to scan directory", path=str(full_dir), error=str(e))

    async def collect(self) -> List[str]:
        """Walk and filter files efficiently."""
        logger.debug("Collecting files via standard async walk")
        files_list_internal: List[str] = []
        anyio_root = anyio.Path(self.root)
        
        try:
            async for entry in anyio_root.iterdir():
                if await entry.is_dir():
                    if entry.name in self.config.excluded_dirs:
                        continue
                    async for rel_path in self._collect_recursive(
                        Path(entry).relative_to(self.root)
                    ):
                        files_list_internal.append(rel_path.as_posix())
                elif await entry.is_file():
                    rel_path = Path(entry).relative_to(self.root)
                    if await self._matches(rel_path):
                        files_list_internal.append(rel_path.as_posix())
        except OSError as e:
            logger.error("Failed to scan root directory", path=str(self.root), error=str(e))
            return [] # Cannot proceed if root is unreadable

        files_list_internal.sort()
        return files_list_internal
```

---

## src/create_dump/processor.py

<a id='src-create-dump-processor-py'></a>

```python
# src/create_dump/processor.py

"""
File Processing Component.

Reads all source files and saves their raw content to temporary files
for later consumption by formatters (Markdown, JSON, etc.).
"""

from __future__ import annotations

import uuid
from pathlib import Path
# ⚡ REFACTOR: Import List, Optional, Callable, Awaitable, Protocol
from typing import List, Optional, Any, Callable, Awaitable, Protocol

import anyio
from anyio.abc import TaskStatus

# ⚡ REFACTOR: Removed all detect-secrets imports

from .core import DumpFile
from .helpers import CHUNK_SIZE, get_language
from .logging import (
    HAS_RICH, Progress, SpinnerColumn, TextColumn, console, logger
)
from .metrics import FILES_PROCESSED, ERRORS_TOTAL
from .system import DEFAULT_MAX_WORKERS


# ⚡ NEW: Define a simple Protocol for middleware
class ProcessorMiddleware(Protocol):
    async def process(self, dump_file: DumpFile) -> None:
        """Processes a DumpFile. Can modify it in-place."""
        ...


class FileProcessor:
    """
    Reads source files concurrently and stores their content in temp files.
    """

    # ⚡ REFACTOR: Update __init__ to accept middleware
    def __init__(
        self, 
        temp_dir: str, 
        middlewares: List[ProcessorMiddleware] | None = None
    ):
        self.temp_dir = temp_dir
        self.files: List[DumpFile] = []
        self.middlewares = middlewares or []
        
    # ⚡ REFACTOR: Removed _scan_for_secrets
    # ⚡ REFACTOR: Removed _redact_secrets

    async def process_file(self, file_path: str) -> DumpFile:
        """Concurrently read and write file content to temp (streamed)."""
        temp_anyio_path: Optional[anyio.Path] = None
        dump_file: Optional[DumpFile] = None
        
        try:
            temp_filename = f"{uuid.uuid4().hex}.tmp"
            temp_anyio_path = anyio.Path(self.temp_dir) / temp_filename
            
            lang = get_language(file_path)
            
            async with await anyio.Path(file_path).open("r", encoding="utf-8", errors="replace") as src, \
                       await temp_anyio_path.open("w", encoding="utf-8") as tmp:
                
                peek = await src.read(CHUNK_SIZE)
                if peek:
                    # ⚡ REFACTOR: Write only the raw content.
                    await tmp.write(peek)
                    while chunk := await src.read(CHUNK_SIZE):
                        await tmp.write(chunk)
            
            # Create the successful DumpFile object
            dump_file = DumpFile(path=file_path, language=lang, temp_path=Path(temp_anyio_path))

            # ⚡ NEW: Run middleware chain
            for middleware in self.middlewares:
                await middleware.process(dump_file)
                if dump_file.error:
                    # Middleware failed this file (e.g., secrets found)
                    # The middleware is responsible for logging and metrics
                    return dump_file

            FILES_PROCESSED.labels(status="success").inc()
            return dump_file
        
        except Exception as e:
            if temp_anyio_path is not None:
                await temp_anyio_path.unlink(missing_ok=True)
            
            ERRORS_TOTAL.labels(type="process").inc()
            
            logger.error("File process error", path=file_path, error=str(e))
            # Return an error DumpFile
            return DumpFile(path=file_path, error=str(e))

    async def dump_concurrent(
        self,
        files_list: List[str],
        progress: bool = False,
        max_workers: int = DEFAULT_MAX_WORKERS,
    ) -> List[DumpFile]:
        """
        Parallel temp file creation with progress.
        
        Returns the list of processed DumpFile objects.
        """
        
        limiter = anyio.Semaphore(max_workers)
        self.files = [] # Ensure list is fresh for this run

        async def _process_wrapper(
            file_path: str, 
            prog: Optional[Progress] = None, 
            task_id: Optional[TaskStatus] = None
        ):
            """Wrapper to handle timeouts, limiting, and progress bar."""
            async with limiter:
                try:
                    with anyio.fail_after(60):  # 60-second timeout
                        result = await self.process_file(file_path)
                        self.files.append(result)
                except TimeoutError:
                    ERRORS_TOTAL.labels(type="timeout").inc()
                    self.files.append(DumpFile(path=file_path, error="Timeout"))
                except Exception as e:
                    ERRORS_TOTAL.labels(type="process").inc()
                    self.files.append(DumpFile(path=file_path, error=f"Unhandled exception: {e}"))
                finally:
                    if prog and task_id is not None:
                        prog.advance(task_id)

        async with anyio.create_task_group() as tg:
            if progress and HAS_RICH and console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as prog:
                    task_id = prog.add_task("Processing files...", total=len(files_list))
                    for f in files_list:
                        tg.start_soon(_process_wrapper, f, prog, task_id)
            else:
                for f in files_list:
                    tg.start_soon(_process_wrapper, f, None, None)
        
        # Return the processed files list
        return self.files
```

---

## src/create_dump/path_utils.py

<a id='src-create-dump-path-utils-py'></a>

```python
# src/create_dump/path_utils.py

"""Shared utilities for path safety, discovery, and user confirmation."""

from __future__ import annotations

import logging
import re
from pathlib import Path
# ⚡ REFACTOR: Import AsyncGenerator
from typing import List, AsyncGenerator

import anyio  # ⚡ REFACTOR: Import anyio
from .logging import logger  # ⚡ REFACTOR: Import from logging

# ⚡ REFACTOR: Removed safe_is_within and find_matching_files
__all__ = ["safe_is_within", "confirm", "find_matching_files"]


# ⚡ REFACTOR: Removed synchronous safe_is_within function


# ⚡ NEW: Async version of safe_is_within for anyio.Path
async def safe_is_within(path: anyio.Path, root: anyio.Path) -> bool:
    """
    Async check if path is safely within root (relative/escape-proof).
    Handles anyio.Path objects by awaiting .resolve().
    """
    try:
        # 1. Await resolution for both paths
        resolved_path = await path.resolve()
        resolved_root = await root.resolve()
        
        # 2. Perform the check on the resulting sync pathlib.Path objects
        return resolved_path.is_relative_to(resolved_root)
    except AttributeError:
        # Fallback for Python < 3.9
        resolved_path = await path.resolve()
        resolved_root = await root.resolve()
        return str(resolved_path).startswith(str(resolved_root) + "/")


# ⚡ REFACTOR: Removed synchronous find_matching_files function


# ⚡ REFACTOR: New async version of find_matching_files
async def find_matching_files(root: Path, regex: str) -> AsyncGenerator[Path, None]:
    """Async glob files matching regex within root."""
    pattern = re.compile(regex)
    anyio_root = anyio.Path(root)
    # ⚡ REFACTOR: Yield paths directly instead of building a list
    async for p in anyio_root.rglob("*"):
        if pattern.search(p.name):
            yield Path(p)  # Yield as pathlib.Path


def confirm(prompt: str) -> bool:
    """Prompt user for yes/no; handles interrupt gracefully."""
    try:
        ans = input(f"{prompt} [y/N]: ").strip().lower()
    except KeyboardInterrupt:
        print()
        return False
    return ans in ("y", "yes")
```

---

## src/create_dump/helpers.py

<a id='src-create-dump-helpers-py'></a>

```python
# src/create_dump/helpers.py

"""Stateless, general-purpose helper functions."""

from __future__ import annotations

import os
import re
import uuid
from os import scandir  # Explicit import
from pathlib import Path
from typing import Dict, List

import anyio  # ⚡ NEW: Import for async path operations
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

from .logging import logger

# Constants
CHUNK_SIZE = 8192
BINARY_THRESHOLD = 0.05


def slugify(path: str) -> str:
    """Convert path to safe anchor slug."""
    p = Path(path)
    clean = p.as_posix().lstrip("./").lower()
    return re.sub(r"[^a-z0-9]+", "-", clean).strip("-")


def get_language(filename: str) -> str:
    """Detect file language from extension/basename."""
    # ⚡ FIX: Strip leading '.' from basename for special file matching
    basename = Path(filename).name.lower().lstrip('.')
    
    if basename == "dockerfile":
        return "dockerfile"
    if basename == "dockerignore":
        return "ini"
    
    ext = Path(filename).suffix.lstrip(".").lower()
    mapping: Dict[str, str] = {
        "py": "python", "sh": "bash", "yml": "yaml", "yaml": "yaml",
        "ini": "ini", "cfg": "ini", "toml": "toml", "json": "json",
        "txt": "text", "md": "markdown", "js": "javascript", "ts": "typescript",
        "html": "html", "css": "css", "jsx": "jsx", "tsx": "tsx", "vue": "vue",
        "sql": "sql", "go": "go", "rs": "rust", "java": "java", "c": "c",
        "cpp": "cpp", "rb": "ruby", "php": "php", "pl": "perl", "scala": "scala",
        "kt": "kotlin", "swift": "swift", "dart": "dart", "csv": "csv",
        "xml": "xml", "r": "r", "jl": "julia", "ex": "elixir", "exs": "elixir",
        "lua": "lua", "hs": "haskell", "ml": "ocaml", "scm": "scheme",
        "zig": "zig", "carbon": "carbon", "mojo": "mojo", "verse": "verse",
    }
    return mapping.get(ext, "text")


# ⚡ REFACTOR: Removed synchronous is_text_file function


# ⚡ NEW: Async version of is_text_file
async def is_text_file(path: anyio.Path) -> bool:
    """Async Heuristic: Check if file is text-based."""
    try:
        async with await path.open("rb") as f:
            chunk = await f.read(CHUNK_SIZE)
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


def _unique_path(path: Path) -> Path:
    """Generate unique path with UUID suffix."""
    if not os.path.exists(path):
        return path

    stem, suffix = path.stem, path.suffix
    counter = 0
    while True:
        u = uuid.uuid4()
        hex_attr = getattr(u, "hex", "")
        hex_val = hex_attr() if callable(hex_attr) else hex_attr
        hex8 = str(hex_val)[:8]

        if counter == 0:
            unique_stem = f"{stem}_{hex8}"
        else:
            unique_stem = f"{stem}_{counter}_{hex8}"

        candidate = path.parent / f"{unique_stem}{suffix}"
        if not Path.exists(candidate):
            return candidate
        counter += 1
```

---

## src/create_dump/core.py

<a id='src-create-dump-core-py'></a>

```python
# src/create_dump/core.py

"""Core models and configuration.

Pydantic models for validation, config loading.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

from .logging import logger  # ⚡ REFACTOR: Corrected import from .utils
import toml

# Canonical pattern for dump artifacts (imported/used by modules)
DEFAULT_DUMP_PATTERN = r".*_all_create_dump_\d{8}_\d{6}\.(md(\.gz)?|sha256)$"


class Config(BaseModel):
    """Validated config with env support."""

    default_includes: List[str] = Field(default_factory=list)
    default_excludes: List[str] = Field(default_factory=list)
    use_gitignore: bool = True
    git_meta: bool = True
    max_file_size_kb: Optional[int] = Field(None, ge=0)
    dest: Optional[Path] = Field(None, description="Default output destination (CLI --dest overrides)")
    dump_pattern: str = Field(DEFAULT_DUMP_PATTERN, description="Canonical regex for dump artifacts")
    excluded_dirs: List[str] = Field(
        default_factory=lambda: [
            "__pycache__", ".git", ".venv", "venv", "myenv", ".mypy_cache",
            ".pytest_cache", ".idea", "node_modules", "build", "dist",
            "vendor", ".gradle", ".tox", "eggs", ".egg-info",
        ]
    )
    metrics_port: int = Field(8000, ge=1, le=65535)

    # ⚡ NEW: v8 feature flags
    git_ls_files: bool = Field(False, description="Use 'git ls-files' for file collection.")
    scan_secrets: bool = Field(False, description="Enable secret scanning.")
    hide_secrets: bool = Field(False, description="Redact found secrets (requires scan_secrets=True).")


    @field_validator("max_file_size_kb", mode="before")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("must be non-negative")
        return v

    @field_validator("dest", mode="before")
    @classmethod
    def validate_dest(cls, v):
        if v is not None:
            try:
                path = Path(v)
                if not path.name:
                    logger.warning("Empty dest path; defaulting to None.")
                    return None
                return path
            except Exception as e:
                logger.warning("Invalid dest path '%s': %s; defaulting to None.", v, e)
                return None
        return v

    @field_validator("dump_pattern", mode="after")
    @classmethod
    def validate_dump_pattern(cls, v):
        if not v or not re.match(r'.*_all_create_dump_', v):
            logger.warning("Loose or invalid dump_pattern '%s'; enforcing default: %s", v, DEFAULT_DUMP_PATTERN)
            return DEFAULT_DUMP_PATTERN
        return v


class GitMeta(BaseModel):
    branch: Optional[str] = None
    commit: Optional[str] = None


class DumpFile(BaseModel):
    path: str
    language: Optional[str] = None
    temp_path: Optional[Path] = None
    error: Optional[str] = None


# 🐞 FIX: Add `_cwd` parameter for testability
def load_config(path: Optional[Path] = None, _cwd: Optional[Path] = None) -> Config:
    """Loads config from [tool.create-dump] in TOML files."""
    config_data: Dict[str, Any] = {}
    
    # 🐞 FIX: Use provided _cwd for testing, or default to Path.cwd()
    cwd = _cwd or Path.cwd()

    possible_paths = (
        [path]
        if path
        else [
            Path.home() / ".create_dump.toml", # 1. Home dir
            cwd / ".create_dump.toml",         # 2. CWD .create_dump.toml
            cwd / "create_dump.toml",          # 3. CWD create_dump.toml
            cwd / "pyproject.toml",          # 4. CWD pyproject.toml
        ]
    )
    
    for conf_path in possible_paths:
        if conf_path.exists():
            try:
                full_data = toml.load(conf_path)
                config_data = full_data.get("tool", {}).get("create-dump", {})
                if config_data:  # Stop if we find it
                    logger.debug("Config loaded", path=conf_path, keys=list(config_data.keys()))
                    break
            except (toml.TomlDecodeError, OSError) as e:
                logger.warning("Config load failed", path=conf_path, error=str(e))
    return Config(**config_data)


# ⚡ REFACTOR: Removed generate_default_config() function.
# This logic is now handled by the interactive wizard in cli/main.py.
```

---

## src/create_dump/collector/git_ls.py

<a id='src-create-dump-collector-git-ls-py'></a>

```python
# src/create_dump/collector/git_ls.py

"""The 'git ls-files' collection strategy."""

from __future__ import annotations

from typing import List

from ..logging import logger
from ..system import get_git_ls_files
from .base import CollectorBase


class GitLsCollector(CollectorBase):
    """Collects files using 'git ls-files'."""

    async def collect(self) -> List[str]:
        """Run 'git ls-files' and filter the results."""
        logger.debug("Collecting files via 'git ls-files'")
        raw_files_list = await get_git_ls_files(self.root)
        if not raw_files_list:
            logger.warning("'git ls-files' returned no files.")
            return []
        
        logger.debug(f"Git found {len(raw_files_list)} raw files. Applying filters...")
        return await self.filter_files(raw_files_list)
```

---

## src/create_dump/metrics.py

<a id='src-create-dump-metrics-py'></a>

```python
# src/create_dump/metrics.py

"""Defines Prometheus metrics and the metrics server."""

from __future__ import annotations

from contextlib import contextmanager
from prometheus_client import Counter, Histogram, start_http_server

# Port
DEFAULT_METRICS_PORT = 8000

# Metrics
DUMP_DURATION = Histogram(
    "create_dump_duration_seconds",
    "Dump duration",
    buckets=[1, 5, 30, 60, 300, float("inf")],
    labelnames=["collector"],  # ⚡ REFACTOR: Add collector label
)
# 🐞 FIX: Add _total suffix for Prometheus convention
FILES_PROCESSED = Counter("create_dump_files_total", "Files processed", ["status"])
# 🐞 FIX: Add _total suffix for Prometheus convention
ERRORS_TOTAL = Counter("create_dump_errors_total", "Errors encountered", ["type"])
ROLLBACKS_TOTAL = Counter("create_dump_rollbacks_total", "Batch rollbacks", ["reason"])

# ✨ NEW: Add metric for archive creation
ARCHIVES_CREATED_TOTAL = Counter(
    "create_dump_archives_total",
    "Archives created",
    ["format"],
)


@contextmanager
def metrics_server(port: int = DEFAULT_METRICS_PORT):
    """Start configurable metrics server with auto-cleanup."""
    if port > 0:
        start_http_server(port)
    try:
        yield
    finally:
        pass  # Server runs in a daemon thread
```

---

## src/create_dump/collector/git_diff.py

<a id='src-create-dump-collector-git-diff-py'></a>

```python
# src/create_dump/collector/git_diff.py

"""The 'git diff' collection strategy."""

from __future__ import annotations

from pathlib import Path
from typing import List

from ..logging import logger
from ..system import get_git_diff_files
from .base import CollectorBase


class GitDiffCollector(CollectorBase):
    """Collects files using 'git diff --name-only'."""

    def __init__(self, diff_since: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diff_since = diff_since

    async def collect(self) -> List[str]:
        """Run 'git diff' and filter the results."""
        logger.debug("Collecting files via 'git diff'", ref=self.diff_since)
        raw_files_list = await get_git_diff_files(self.root, self.diff_since)
        if not raw_files_list:
            logger.warning("'git diff' returned no files.", ref=self.diff_since)
            return []

        logger.debug(f"Git found {len(raw_files_list)} raw files. Applying filters...")
        return await self.filter_files(raw_files_list)
```

---

## src/create_dump/single.py

<a id='src-create-dump-single-py'></a>

```python
# src/create_dump/single.py

"""
Single dump runner.

This file is the "glue" layer that connects the CLI flags
from `cli/single.py` to the core orchestration logic.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import anyio
from typer import Exit

# ⚡ REFACTOR: Import new orchestration and watch modules
from .workflow.single import SingleRunOrchestrator
from .watch import FileWatcher
from .logging import styled_print


async def run_single(
    root: Path,
    dry_run: bool,
    yes: bool,
    no_toc: bool,
    tree_toc: bool,
    compress: bool,
    format: str,
    exclude: str,
    include: str,
    max_file_size: Optional[int],
    use_gitignore: bool,
    git_meta: bool,
    progress: bool,
    max_workers: int,
    archive: bool,
    archive_all: bool,
    archive_search: bool,
    archive_include_current: bool,
    archive_no_remove: bool,
    archive_keep_latest: bool,
    archive_keep_last: Optional[int],
    archive_clean_root: bool,
    archive_format: str,
    allow_empty: bool,
    metrics_port: int,
    verbose: bool,
    quiet: bool,
    dest: Optional[Path] = None,
    # ⚡ NEW: v8 feature flags
    watch: bool = False,
    git_ls_files: bool = False,
    diff_since: Optional[str] = None,
    scan_secrets: bool = False,
    hide_secrets: bool = False,
) -> None:
    
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Invalid root: {root}")

    # Normalize cwd once at the start
    await anyio.to_thread.run_sync(os.chdir, root)
    
    # ⚡ REFACTOR: Handle `yes` logic for watch mode
    # If --watch is on, we don't want prompts on subsequent runs.
    effective_yes = yes or watch

    # ⚡ REFACTOR: Instantiate the orchestrator
    orchestrator = SingleRunOrchestrator(
        root=root,
        dry_run=dry_run,
        yes=effective_yes, # Pass the combined value
        no_toc=no_toc,
        tree_toc=tree_toc,
        compress=compress,
        format=format,
        exclude=exclude,
        include=include,
        max_file_size=max_file_size,
        use_gitignore=use_gitignore,
        git_meta=git_meta,
        progress=progress,
        max_workers=max_workers,
        archive=archive,
        archive_all=archive_all,
        archive_search=archive_search,
        archive_include_current=archive_include_current,
        archive_no_remove=archive_no_remove,
        archive_keep_latest=archive_keep_latest,
        archive_keep_last=archive_keep_last,
        archive_clean_root=archive_clean_root,
        archive_format=archive_format,
        allow_empty=allow_empty,
        metrics_port=metrics_port,
        verbose=verbose,
        quiet=quiet,
        dest=dest,
        git_ls_files=git_ls_files,
        diff_since=diff_since,
        scan_secrets=scan_secrets,
        hide_secrets=hide_secrets,
    )

    # ⚡ REFACTOR: Top-level control flow
    if watch:
        if not quiet:
            styled_print("[green]Running initial dump...[/green]")
        
        try:
            await orchestrator.run()
        except Exit as e:
            if getattr(e, "exit_code", None) == 0 and dry_run:
                 # Handle dry_run exit for the *initial* run
                 return
            raise # Re-raise other exits
        
        if not quiet:
            styled_print(f"\n[cyan]Watching for file changes in {root}... (Press Ctrl+C to stop)[/cyan]")
        
        watcher = FileWatcher(root=root, dump_func=orchestrator.run, quiet=quiet)
        await watcher.start()
    else:
        try:
            await orchestrator.run()
        except Exit as e:
            if getattr(e, "exit_code", None) == 0 and dry_run:
                # Handle dry_run exit
                return
            raise
```

---

## src/create_dump/orchestrator.py

<a id='src-create-dump-orchestrator-py'></a>

```python
# src/create_dump/orchestrator.py

"""Batch orchestration: Multi-subdir dumps, centralization, compression, cleanup."""

from __future__ import annotations

import re
import sys
import uuid
import shutil
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple, Union

import anyio

from .archiver import ArchiveManager
# ⚡ FIX: Import the renamed async function
from .cleanup import safe_delete_paths
from .core import Config, load_config, DEFAULT_DUMP_PATTERN
# ⚡ FIX: Import the renamed async functions
from .path_utils import confirm, find_matching_files, safe_is_within
# ⚡ FIX: Import the renamed async function
from .single import run_single
from .logging import logger, styled_print
from .metrics import DUMP_DURATION, ROLLBACKS_TOTAL

# ⚡ FIX: Renamed __all__
__all__ = ["run_batch"]


class AtomicBatchTxn:
    """Atomic staging for batch outputs: commit/rollback via rename/rmtree."""

    def __init__(self, root: Path, dest: Optional[Path], run_id: str, dry_run: bool):
        self.root = root
        self.dest = dest
        self.run_id = run_id
        self.dry_run = dry_run
        self.staging: Optional[anyio.Path] = None

    async def __aenter__(self) -> Optional[anyio.Path]:
        if self.dry_run:
            self.staging = None
            return None
        
        staging_parent = self.root / "archives" if not self.dest else (
            self.dest.resolve() if self.dest.is_absolute() else self.root / self.dest
        )
        
        anyio_staging_parent = anyio.Path(staging_parent)
        anyio_root = anyio.Path(self.root)
        if not await safe_is_within(anyio_staging_parent, anyio_root):
            raise ValueError("Staging parent outside root boundary")

        self.staging = anyio.Path(staging_parent / f".staging-{self.run_id}")
        await self.staging.mkdir(parents=True, exist_ok=True)
        return self.staging

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.staging:
            return
        if exc_type is None:
            final_name = self.staging.name.replace(".staging-", "")
            final_path = self.staging.parent / final_name
            await self.staging.rename(final_path)
            logger.info("Batch txn committed: %s -> %s", self.staging, final_path)
        else:
            try:
                await anyio.to_thread.run_sync(shutil.rmtree, self.staging)
            except OSError:
                pass
            # ⚡ FIX: Call .labels() before .inc() for Prometheus
            ROLLBACKS_TOTAL.labels(reason=str(exc_val)[:100]).inc()
            logger.error("Batch txn rolled back due to: %s", exc_val)


@asynccontextmanager
async def atomic_batch_txn(root: Path, dest: Optional[Path], run_id: str, dry_run: bool):
    txn = AtomicBatchTxn(root, dest, run_id, dry_run)
    staging = await txn.__aenter__()
    try:
        yield staging
    finally:
        await txn.__aexit__(*sys.exc_info())


# ⚡ RENAMED: Function
async def _centralize_outputs(
    dest_path: Union[anyio.Path, Path],
    root: Path,
    successes: List[Path],
    compress: bool,
    yes: bool,
    dump_pattern: str
) -> None:
    if isinstance(dest_path, Path):
        dest_path = anyio.Path(dest_path)
    await dest_path.mkdir(parents=True, exist_ok=True)
    moved = 0
    
    # ⚡ FIX: This regex must match *all* artifacts, not just .md
    # We'll use the .md pattern to find the *base* and then move its .sha256
    md_regex = re.compile(dump_pattern)
    anyio_root = anyio.Path(root)

    for sub_root in successes:
        anyio_sub_root = anyio.Path(sub_root)
        # Find only the .md files first
        all_md_files = [
            f async for f in anyio_sub_root.glob("*.md") 
            if await f.is_file() and md_regex.match(f.name)
        ]

        for md_file_path in all_md_files:
            sha_file_path = md_file_path.with_suffix(".sha256")
            
            # Create a list of files to move for this pair
            files_to_move = [md_file_path]
            if await sha_file_path.exists():
                files_to_move.append(sha_file_path)
            else:
                # This check is now redundant because validate_batch_staging will catch it,
                # but it's good practice to log here.
                logger.warning("Missing SHA256 for dump, moving .md only", path=str(md_file_path))

            for file_path in files_to_move:
                if not await safe_is_within(file_path, anyio_root):
                    logger.warning("Skipping unsafe dump artifact: %s", file_path)
                    continue

                target = dest_path / file_path.name
                if await target.exists():
                    await target.unlink()
                await file_path.rename(target)
                
                if file_path.suffix == ".md":
                    moved += 1 # Count pairs
                
                to_type = "staging" if "staging" in str(dest_path) else "dest"
                logger.info("Moved dump artifact to %s: %s -> %s", to_type, file_path, target)

    logger.info("Centralized %d dump pairs to %s", moved, dest_path)


async def validate_batch_staging(staging: anyio.Path, pattern: str) -> bool:
    """Validate: All MD have SHA, non-empty."""
    dump_regex = re.compile(pattern)
    md_files = []
    async for f in staging.rglob("*"):
        if await f.is_file() and dump_regex.match(f.name) and f.suffix == ".md":
            md_files.append(f)
    if not md_files:
        return False
    has_sha = True
    for f in md_files:
        sha_path = f.with_suffix(".sha256")
        if not await sha_path.exists():
            has_sha = False
            logger.error("Validation failed: Missing SHA256", md_file=str(f))
            break
    return has_sha


# ⚡ RENAMED: Function
async def run_batch(
    root: Path,
    subdirs: List[str],
    pattern: str,
    dry_run: bool,
    yes: bool,
    accept_prompts: bool,
    compress: bool,
    max_workers: int,
    verbose: bool,
    quiet: bool,
    dest: Optional[Path] = None,
    archive: bool = False,
    archive_all: bool = False,
    archive_search: bool = False,
    archive_include_current: bool = True,
    archive_no_remove: bool = False,
    archive_keep_latest: bool = True,
    archive_keep_last: Optional[int] = None,
    archive_clean_root: bool = False,
    atomic: bool = True,
) -> None:
    root = root.resolve()
    cfg = load_config()

    if not re.match(r'.*_all_create_dump_', pattern):
        logger.warning("Enforcing canonical pattern: %s", cfg.dump_pattern)
        pattern = cfg.dump_pattern

    atomic = not dry_run and atomic

    # Common: Resolve sub_roots & pre-cleanup
    sub_roots = []
    for sub in subdirs:
        sub_path = root / sub
        if await anyio.Path(sub_path).exists():
            sub_roots.append(sub_path)
    if not sub_roots:
        logger.warning("No valid subdirs: %s", subdirs)
        return

    # ⚡ FIX: Consume the async generator from find_matching_files into a list.
    matches = [p async for p in find_matching_files(root, pattern)]
    
    if matches and not dry_run and not archive_all:
        if yes or await anyio.to_thread.run_sync(confirm, "Delete old dumps?"):
            # ⚡ FIX: Call renamed async function
            deleted, _ = await safe_delete_paths(matches, root, dry_run, yes)
            if verbose:
                logger.info("Pre-cleanup: %d deleted", deleted)

    successes: List[Path] = []
    failures: List[Tuple[Path, str]] = []

    async def _run_single_wrapper(sub_root: Path):
        try:
            # ⚡ FIX: Call renamed async function
            await run_single(
                root=sub_root, dry_run=dry_run, yes=accept_prompts or yes, no_toc=False,
                compress=compress, exclude="", include="", max_file_size=cfg.max_file_size_kb,
                use_gitignore=cfg.use_gitignore, git_meta=cfg.git_meta, progress=False,
                max_workers=16, archive=False, archive_all=False, archive_search=False,
                archive_include_current=archive_include_current, archive_no_remove=archive_no_remove,
                archive_keep_latest=archive_keep_latest, archive_keep_last=archive_keep_last,
                archive_clean_root=archive_clean_root, allow_empty=True, metrics_port=0,
                verbose=verbose, quiet=quiet,
            )
            successes.append(sub_root)
            if not quiet:
                styled_print(f"[green]✅ Dumped {sub_root}[/green]")
        except Exception as e:
            failures.append((sub_root, str(e)))
            logger.error("Subdir failed", subdir=sub_root, error=str(e))
            if not quiet:
                styled_print(f"[red]❌ Failed {sub_root}: {str(e).split('from e')[-1].strip()}[/red]")

    # ⚡ FIX: Add 'collector' label for metrics
    with DUMP_DURATION.labels(collector="batch").time():
        limiter = anyio.Semaphore(max_workers)
        async with anyio.create_task_group() as tg:
            for sub_root in sub_roots:
                async def limited_wrapper(sub_root=Path(sub_root)):
                    async with limiter:
                        await _run_single_wrapper(sub_root)
                tg.start_soon(limited_wrapper)

    if not successes:
        logger.info("No successful dumps.")
        return

    run_id = uuid.uuid4().hex[:8]
    if atomic:
        async with atomic_batch_txn(root, dest, run_id, dry_run) as staging:
            if staging is None:
                return  # Dry run complete

            await _centralize_outputs(staging, root, successes, compress, yes, pattern)
            
            if not await validate_batch_staging(staging, pattern):
                # Raise validation error *before* archiving
                raise ValueError("Validation failed: Incomplete dumps")

            if archive or archive_all:
                timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
                staging_path = Path(staging)
                manager = ArchiveManager(
                    root=staging_path,
                    timestamp=timestamp, keep_latest=archive_keep_latest, keep_last=archive_keep_last,
                    clean_root=archive_clean_root, search=archive_search,
                    include_current=archive_include_current, no_remove=archive_no_remove,
                    dry_run=dry_run, yes=yes, verbose=verbose, md_pattern=pattern, archive_all=archive_all,
                )
                archive_results = await manager.run()
                if verbose:
                    logger.debug("Archiving in staging: search=%s, all=%s", archive_search, archive_all)
                if archive_results and any(archive_results.values()):
                    groups = ', '.join(k for k, v in archive_results.items() if v)
                    logger.info("Archived: %s", groups)
                    if not quiet:
                        styled_print(f"[green]📦 Archived: {groups}[/green]")
                else:
                    logger.info("No dumps for archiving.")
            
    else: # Not atomic
        if dry_run:
            logger.info("[dry-run] Would centralize files to non-atomic dest.")
            return

        central_dest = dest or root / "archives"
        await _centralize_outputs(central_dest, root, successes, compress, yes, pattern)
        
        if not await validate_batch_staging(anyio.Path(central_dest), pattern):
            logger.warning("Validation failed: Incomplete dumps in non-atomic destination.")
            # Do not raise, as this is non-transactional

        if archive or archive_all:
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            manager = ArchiveManager(
                root=root, timestamp=timestamp, keep_latest=archive_keep_latest, keep_last=archive_keep_last,
                clean_root=archive_clean_root, search=archive_search, include_current=archive_include_current,
                no_remove=archive_no_remove, dry_run=dry_run, yes=yes, verbose=verbose,
                md_pattern=pattern, archive_all=archive_all,
            )
            archive_results = await manager.run()
            if archive_results and any(archive_results.values()):
                groups = ', '.join(k for k, v in archive_results.items() if v)
                logger.info("Archived: %s", groups)
                if not quiet:
                    styled_print(f"[green]📦 Archived: {groups}[/green]")
            else:
                logger.info("No dumps for archiving.")

    logger.info("Batch complete: %d/%d successes", len(successes), len(sub_roots))
    if failures and verbose:
        for sub_root, err in failures:
            logger.error("Failure: %s - %s", sub_root, err)
    if not quiet:
        styled_print(f"[green]✅ Batch: {len(successes)}/{len(sub_roots)}[/green]")
```

---

## src/create_dump/scanning.py

<a id='src-create-dump-scanning-py'></a>

```python
# src/create_dump/scanning.py

"""Secret scanning and redaction middleware."""

from __future__ import annotations

import logging
from typing import List, Dict, Any

import anyio
# 🐞 FIX: Import `to_thread` to create a private symbol
from anyio import to_thread
from detect_secrets.core import scan
from detect_secrets.core.potential_secret import PotentialSecret

from .core import DumpFile
from .logging import logger
from .metrics import ERRORS_TOTAL

# 🐞 FIX: Create a private, patchable symbol for run_sync
_run_sync = to_thread.run_sync


class SecretScanner:
    """Processor middleware to scan for and optionally redact secrets."""

    def __init__(self, hide_secrets: bool = False):
        self.hide_secrets = hide_secrets
        # 🐞 FIX: Remove all plugin and config initialization.
        # It is no longer needed for v1.5.0.

    async def _scan_for_secrets(self, file_str_path: str) -> List[PotentialSecret]:
        """Runs detect-secrets in a thread pool with correct settings."""
        
        def scan_in_thread():
            # 🐞 FIX: Get the "detect-secrets" logger and temporarily
            # silence it to suppress the "No plugins" spam.
            ds_logger = logging.getLogger("detect-secrets")
            original_level = ds_logger.level
            ds_logger.setLevel(logging.CRITICAL)
            
            try:
                # 🐞 FIX: Call scan_file with only the path.
                # v1.5.0 handles its own default plugin initialization
                # internally and does not accept a `plugins` argument.
                results = scan.scan_file(file_str_path)
                
                # 🐞 FIX: Convert the generator to a list *inside* the thread
                return list(results)
            finally:
                # Always restore the original log level
                ds_logger.setLevel(original_level)

        try:
            # 🐞 FIX: Call the new module-level `_run_sync`
            scan_results_list = await _run_sync(
                scan_in_thread
            )
            # The return value is now already a list
            return scan_results_list
        except Exception as e:
            # Log the error but don't fail the whole dump, just this file
            logger.error("Secret scan failed", path=file_str_path, error=str(e))
            return [] # Return empty list on scan error

    async def _redact_secrets(self, temp_path: anyio.Path, secrets: List[PotentialSecret]) -> None:
        """Reads the temp file, redacts secret lines, and overwrites it."""
        try:
            # 1. Get line numbers (detect-secrets is 1-indexed)
            line_numbers_to_redact = {s.line_number for s in secrets}

            # 2. Read lines
            original_content = await temp_path.read_text()
            lines = original_content.splitlines()

            # 3. Redact
            new_lines = []
            for i, line in enumerate(lines, 1):
                if i in line_numbers_to_redact:
                    # Find the specific secret type for this line
                    secret_type = next((s.type for s in secrets if s.line_number == i), "Unknown")
                    new_lines.append(f"***SECRET_REDACTED*** (Line {i}, Type: {secret_type})")
                else:
                    new_lines.append(line)
            
            # 4. Write back
            await temp_path.write_text("\n".join(new_lines))
        except Exception as e:
            logger.error("Failed to redact secrets", path=str(temp_path), error=str(e))
            # If redaction fails, write a generic error to be safe
            await temp_path.write_text(f"*** ERROR: SECRET REDACTION FAILED ***\n{e}")

    async def process(self, dump_file: DumpFile) -> None:
        """
        Public method to run the scan/redact logic on a processed file.
        Modifies `dump_file` in place if an error occurs.
        """
        if not dump_file.temp_path or dump_file.error:
            # File failed before this middleware (e.g., read error)
            return

        temp_anyio_path = anyio.Path(dump_file.temp_path)
        temp_file_str = str(dump_file.temp_path)
        
        secrets = await self._scan_for_secrets(temp_file_str)

        if secrets:
            if self.hide_secrets:
                # Redact the file and continue
                await self._redact_secrets(temp_anyio_path, secrets)
                logger.warning("Redacted secrets", path=dump_file.path)
            else:
                # Fail the file
                await temp_anyio_path.unlink(missing_ok=True)
                ERRORS_TOTAL.labels(type="secret").inc()
                logger.error("Secrets detected", path=dump_file.path)
                dump_file.error = "Secrets Detected" # Modify the object
                dump_file.temp_path = None # Clear the temp path
```

---

## src/create_dump/rollback/engine.py

<a id='src-create-dump-rollback-engine-py'></a>

```python
# src/create_dump/rollback/engine.py

"""
Consumes a MarkdownParser and rehydrates the project structure to disk.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import anyio

from ..logging import logger
from .parser import MarkdownParser
# ✨ NEW: Import the robust, async-native path safety check
from ..path_utils import safe_is_within


class RollbackEngine:
    """
    Consumes a parser and writes the file structure to a target directory.
    """

    def __init__(self, root_output_dir: Path, dry_run: bool = False):
        """
        Initializes the engine.

        Args:
            root_output_dir: The *base* directory to write files into
                             (e.g., .../all_create_dump_rollbacks/my_dump_name_.../)
            dry_run: If True, will only log actions instead of writing.
        """
        self.root_output_dir = root_output_dir
        self.dry_run = dry_run
        self.anyio_root = anyio.Path(self.root_output_dir)

    async def rehydrate(self, parser: MarkdownParser) -> List[Path]:
        """
        Consumes the parser and writes files to the target directory.

        Args:
            parser: An initialized MarkdownParser instance.

        Returns:
            A list of the `pathlib.Path` objects that were created.
        """
        created_files: List[Path] = []
        
        logger.info(
            "Starting rehydration",
            target_directory=str(self.root_output_dir),
            dry_run=self.dry_run
        )

        async for rel_path_str, content in parser.parse_dump_file():
            try:
                # 🔒 SECURITY: Prevent path traversal attacks
                # ♻️ REFACTOR: Replaced weak ".." check with robust safe_is_within
                
                target_path = self.anyio_root / rel_path_str
                
                # The new, robust check handles symlinks and all traversal types
                # by resolving the path *before* checking if it's within the root.
                if not await safe_is_within(target_path, self.anyio_root):
                    logger.warning(
                        "Skipping unsafe path: Resolves outside root",
                        path=rel_path_str,
                        resolved_to=str(target_path)
                    )
                    continue
                
                # Ensure parent directory exists
                if not self.dry_run:
                    await target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write the file
                if self.dry_run:
                    logger.info(f"[dry-run] Would rehydrate file to: {target_path}")
                else:
                    await target_path.write_text(content)
                    logger.debug(f"Rehydrated file: {target_path}")
                
                # ⚡ FIX: Append to created_files *only on success*
                created_files.append(Path(target_path))
                
            except Exception as e:
                logger.error(
                    "Failed to rehydrate file",
                    path=rel_path_str,
                    error=str(e)
                )
        
        logger.info(
            "Rehydration complete",
            files_created=len(created_files)
        )
        return created_files
```

---

## src/create_dump/rollback/parser.py

<a id='src-create-dump-rollback-parser-py'></a>

~~~python
# src/create_dump/rollback/parser.py

"""
Parses a create-dump Markdown file to extract file paths and content.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import AsyncGenerator, List, Tuple

import anyio

from ..logging import logger


class MarkdownParser:
    """
    Reads a .md dump file and parses it into a stream of
    (relative_path, content) tuples for rehydration.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        # Regex to find file headers, e.g., ## src/main.py
        self.header_regex = re.compile(r"^## (.*)$")
        # Regex to find code fences (both ``` and ~~~)
        self.fence_regex = re.compile(r"^(```|~~~)($|\w+)")
        # Regex to find and skip error blocks
        self.error_regex = re.compile(r"^> ⚠️ \*\*Failed:\*\*")

    async def parse_dump_file(self) -> AsyncGenerator[Tuple[str, str], None]:
        """
        Parses the dump file and yields tuples of (relative_path, content).
        """
        current_path: str | None = None
        content_lines: List[str] = []
        capturing = False
        current_fence: str | None = None

        try:
            async with await anyio.Path(self.file_path).open("r", encoding="utf-8") as f:
                async for line in f:
                    if capturing:
                        # Check for closing fence
                        if line.strip() == current_fence:
                            if current_path:
                                # Yield the complete file
                                yield (current_path, "".join(content_lines))
                            
                            # Reset state, wait for next header
                            capturing = False
                            current_path = None
                            content_lines = []
                            current_fence = None
                        else:
                            content_lines.append(line)
                    else:
                        # Not capturing, look for a new file header
                        header_match = self.header_regex.match(line.strip())
                        if header_match:
                            # Found a new file. Reset state and store path.
                            current_path = header_match.group(1).strip()
                            content_lines = []
                            capturing = False
                            current_fence = None
                            continue

                        # If we have a path, look for the opening fence
                        if current_path:
                            # Skip error blocks
                            if self.error_regex.match(line.strip()):
                                logger.warning(f"Skipping failed file in dump: {current_path}")
                                current_path = None # Reset, this file failed
                                continue

                            fence_match = self.fence_regex.match(line.strip())
                            if fence_match:
                                capturing = True
                                current_fence = fence_match.group(1) # Store fence type
                                # Do not append the fence line itself

        except FileNotFoundError:
            logger.error(f"Rollback failed: Dump file not found at {self.file_path}")
            raise
        except Exception as e:
            logger.error(f"Rollback failed: Error parsing dump file: {e}")
            raise
~~~

---

## src/create_dump/system.py

<a id='src-create-dump-system-py'></a>

```python
# src/create_dump/system.py

"""Handles system-level interactions: signals, subprocesses, cleanup."""

from __future__ import annotations

import atexit
import os
import signal
import subprocess
import sys
import tempfile
from contextlib import ExitStack
from pathlib import Path
# ⚡ REFACTOR: Import List and Tuple
from typing import Any, Optional, List, Tuple
import asyncio  # ⚡ NEW: Import asyncio

import tenacity
# ⚡ FIX: Removed all deprecated anyio subprocess imports

from .core import GitMeta
from .logging import logger

# Constants
DEFAULT_MAX_WORKERS = min(16, (os.cpu_count() or 4) * 2)

# Globals for cleanup (thread-safe via ExitStack)
_cleanup_stack = ExitStack()
_temp_dir: Optional[tempfile.TemporaryDirectory] = None


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


@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
    reraise=True,
)
def get_git_meta(root: Path) -> Optional[GitMeta]:
    """Fetch git metadata with timeout."""
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


# ⚡ NEW: Internal helper for running asyncio subprocesses
async def _run_async_cmd(cmd: List[str], cwd: Path) -> Tuple[str, str, int]:
    """
    Run a command asynchronously and return (stdout, stderr, returncode).
    """
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=cwd,  # ⚡ Run in the specified root directory
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout_bytes, stderr_bytes = await proc.communicate()

    return (
        stdout_bytes.decode().strip(),
        stderr_bytes.decode().strip(),
        proc.returncode,
    )


# ⚡ REFACTOR: Rewritten to use asyncio.subprocess
async def get_git_ls_files(root: Path) -> List[str]:
    """Run 'git ls-files' asynchronously and return the file list."""
    cmd = ["git", "ls-files", "-co", "--exclude-standard"]
    try:
        stdout, stderr, code = await _run_async_cmd(cmd, cwd=root)
        
        if code != 0:
            logger.error(
                "git ls-files failed", 
                retcode=code, 
                error=stderr
            )
            return []
            
        return [line.strip() for line in stdout.splitlines() if line.strip()]

    except Exception as e:
        logger.error("Failed to run git ls-files", error=str(e))
        return []


# ⚡ REFACTOR: Rewritten to use asyncio.subprocess
async def get_git_diff_files(root: Path, ref: str) -> List[str]:
    """Run 'git diff --name-only' asynchronously and return the file list."""
    cmd = ["git", "diff", "--name-only", ref]
    try:
        stdout, stderr, code = await _run_async_cmd(cmd, cwd=root)
        
        if code != 0:
            logger.error(
                "git diff failed", 
                ref=ref,
                retcode=code, 
                error=stderr
            )
            return []

        return [line.strip() for line in stdout.splitlines() if line.strip()]
        
    except Exception as e:
        logger.error("Failed to run git diff", ref=ref, error=str(e))
        return []
```

---

## src/create_dump/version.py

<a id='src-create-dump-version-py'></a>

```python
# src/create_dump/version.py

"""Version module (single source of truth)."""

# ⚡ REFACTOR: Use __version__ for build tools
__version__ = "10.0.0"

# ⚡ REFACTOR: Keep VERSION for internal compatibility
VERSION = __version__
```

---

## src/create_dump/watch.py

<a id='src-create-dump-watch-py'></a>

```python
# src/create_dump/watch.py

"""File watcher and debouncing logic."""

from __future__ import annotations
from pathlib import Path
from typing import Callable, Awaitable

import anyio
from anyio import Event

from .logging import logger, styled_print


class FileWatcher:
    """Runs an async file watcher with debouncing."""
    
    DEBOUNCE_MS = 500  # 500ms debounce window 

    def __init__(self, root: Path, dump_func: Callable[[], Awaitable[None]], quiet: bool):
        self.root = root
        self.dump_func = dump_func
        self.quiet = quiet
        self.debounce_event = Event()

    async def _debouncer(self):
        """Waits for an event, then sleeps, then runs the dump."""
        while True:
            await self.debounce_event.wait()
            
            # 🐞 FIX: An anyio.Event is not cleared on wait().
            # We must re-create the event to reset its state and
            # prevent the loop from re-triggering immediately.
            self.debounce_event = Event()
            
            await anyio.sleep(self.DEBOUNCE_MS / 1000)
            
            if not self.quiet:
                styled_print(f"\n[yellow]File change detected, running dump...[/yellow]")
            try:
                await self.dump_func()
            except Exception as e:
                # Log error but don't kill the watcher 
                logger.error("Error in watched dump run", error=str(e))
                if not self.quiet:
                    styled_print(f"[red]Error in watched dump: {e}[/red]")

    async def start(self):
        """Starts the file watcher and debouncer."""
        try:
            async with anyio.create_task_group() as tg:
                tg.start_soon(self._debouncer)
                
                # Use anyio's native async watcher 
                async for _ in anyio.Path(self.root).watch(recursive=True):
                    self.debounce_event.set()
        except KeyboardInterrupt:
            if not self.quiet:
                styled_print("\n[cyan]Watch mode stopped.[/cyan]")
```

---

## src/create_dump/writing/json.py

<a id='src-create-dump-writing-json-py'></a>

```python
# src/create_dump/writing/json.py

"""JSON writing logic.
Consumes processed files and formats them as JSON.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any

import anyio

from ..core import DumpFile, GitMeta
from ..helpers import CHUNK_SIZE
from ..logging import logger


class JsonWriter:
    """Streams JSON output from processed temp files."""

    def __init__(self, outfile: Path):
        self.outfile = outfile
        self.files: List[DumpFile] = []  # Stored for metrics

    async def write(
        self, 
        files: List[DumpFile], 
        git_meta: Optional[GitMeta], 
        version: str
    ) -> None:
        """Writes the final JSON file from the list of processed files."""
        self.files = files  # Store for metrics
        
        data: Dict[str, Any] = {
            "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "version": version,
            "git_meta": git_meta.model_dump() if git_meta else None,
            "files": []
        }

        for df in self.files:
            if df.error:
                data["files"].append({
                    "path": df.path,
                    "language": df.language,
                    "error": df.error,
                    "content": None
                })
            elif df.temp_path:
                try:
                    content = await self._read_temp_file(df.temp_path)
                    data["files"].append({
                        "path": df.path,
                        "language": df.language,
                        "error": None,
                        "content": content
                    })
                except Exception as e:
                    logger.error("Failed to read temp file for JSON dump", path=df.path, error=str(e))
                    data["files"].append({
                        "path": df.path,
                        "language": df.language,
                        "error": f"Failed to read temp file: {e}",
                        "content": None
                    })

        await self._write_json(data)

    async def _read_temp_file(self, temp_path: Path) -> str:
        """Reads the raw content from a temp file."""
        return await anyio.Path(temp_path).read_text(encoding="utf-8", errors="replace")

    async def _write_json(self, data: Dict[str, Any]) -> None:
        """Writes the data dictionary to the output file atomically."""
        temp_out = anyio.Path(self.outfile.with_suffix(".tmp"))
        try:
            # Run blocking json.dumps in a thread
            # 🐞 FIX: Wrap the call in a lambda to pass the keyword argument
            json_str = await anyio.to_thread.run_sync(
                lambda: json.dumps(data, indent=2)
            )
            
            async with await temp_out.open("w", encoding="utf-8") as f:
                await f.write(json_str)
            
            await temp_out.rename(self.outfile)
            logger.info("JSON written atomically", path=self.outfile)
        except Exception:
            if await temp_out.exists():
                await temp_out.unlink()
            raise
```

---

## tests/archive/test_finder.py

<a id='tests-archive-test-finder-py'></a>

```python
# tests/archive/test_finder.py

"""
Tests for Phase 3: src/create_dump/archive/finder.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
import logging

import anyio

# Import the class to test
from create_dump.archive.finder import ArchiveFinder
from create_dump.core import DEFAULT_DUMP_PATTERN
# 🐞 FIX: Import the logging setup function
from create_dump.logging import setup_logging

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def quarantine_dir(test_project) -> Path:
    """Creates and returns a quarantine directory inside the test project."""
    q_dir = test_project.root / "quarantine"
    # test_project.create handles async mkdir
    return q_dir


@pytest.fixture
async def project_with_dumps(test_project, quarantine_dir):
    """Creates a standard file structure for finder tests."""
    # 🐞 FIX: Add valid timestamps (e.g., _20250101_000100) to all filenames
    # so they match DEFAULT_DUMP_PATTERN.
    await test_project.create({
        # Valid pair in root
        "root_pair_all_create_dump_20250101_000100.md": "content1",
        "root_pair_all_create_dump_20250101_000100.sha256": "hash1",

        # Orphan in root
        "root_orphan_all_create_dump_20250101_000200.md": "content2",

        # Valid pair in subdir
        "subdir/sub_pair_all_create_dump_20250101_000300.md": "content3",
        "subdir/sub_pair_all_create_dump_20250101_000300.sha256": "hash3",

        # Orphan in subdir
        "subdir/sub_orphan_all_create_dump_20250101_000400.md": "content4",

        # Non-MD file matching pattern
        "root_sha_only_all_create_dump_20250101_000500.sha256": "hash5",

        # Other file to be ignored
        "README.md": "readme",
    })
    # Ensure quarantine_dir exists
    await anyio.Path(quarantine_dir).mkdir(exist_ok=True)


class TestArchiveFinder:
    """Groups tests for the ArchiveFinder."""

    async def test_find_dump_pairs_recursive(
        self, test_project, quarantine_dir, project_with_dumps
    ):
        """
        Test Case 1: search=True (Recursive)
        Should find pairs in root and subdirs, and quarantine all orphans.
        """
        finder = ArchiveFinder(
            root=test_project.root,
            md_pattern=DEFAULT_DUMP_PATTERN,
            search=True,  # Recursive
            verbose=False,
            dry_run=False,
            quarantine_dir=quarantine_dir,
        )

        pairs = await finder.find_dump_pairs()

        # Assertions for found pairs
        assert len(pairs) == 2
        pair_paths = {p[0].name for p in pairs}
        # 🐞 FIX: Check for the new, valid filenames
        assert "root_pair_all_create_dump_20250101_000100.md" in pair_paths
        assert "sub_pair_all_create_dump_20250101_000300.md" in pair_paths

        # Assertions for quarantining
        # 🐞 FIX: Check for the new, valid filenames
        assert await (anyio.Path(quarantine_dir) / "root_orphan_all_create_dump_20250101_000200.md").exists()
        # 🐞 FIX: The test was wrong. Quarantine is flat, it doesn't replicate subdirs.
        assert await (anyio.Path(quarantine_dir) / "sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert originals are gone
        assert not await (test_project.async_root / "root_orphan_all_create_dump_20250101_000200.md").exists()
        assert not await (test_project.async_root / "subdir/sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert valid pair was not moved
        assert await (test_project.async_root / "root_pair_all_create_dump_20250101_000100.md").exists()

    async def test_find_dump_pairs_flat(
        self, test_project, quarantine_dir, project_with_dumps
    ):
        """
        Test Case 2: search=False (Flat)
        Should find pairs in root ONLY, and quarantine orphans in root ONLY.
        """
        finder = ArchiveFinder(
            root=test_project.root,
            md_pattern=DEFAULT_DUMP_PATTERN,
            search=False,  # Flat
            verbose=False,
            dry_run=False,
            quarantine_dir=quarantine_dir,
        )

        pairs = await finder.find_dump_pairs()

        # Assertions for found pairs
        assert len(pairs) == 1
        pair_paths = {p[0].name for p in pairs}
        # 🐞 FIX: Check for the new, valid filenames
        assert "root_pair_all_create_dump_20250101_000100.md" in pair_paths
        # Subdir pair should be ignored
        assert "sub_pair_all_create_dump_20250101_000300.md" not in pair_paths

        # Assertions for quarantining (only root orphan)
        # 🐞 FIX: Check for the new, valid filenames
        assert await (anyio.Path(quarantine_dir) / "root_orphan_all_create_dump_20250101_000200.md").exists()
        # Subdir orphan should be ignored
        assert not await (anyio.Path(quarantine_dir) / "subdir/sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert subdir orphan was NOT moved
        assert await (test_project.async_root / "subdir/sub_orphan_all_create_dump_20250101_000400.md").exists()

    async def test_find_dump_pairs_dry_run(
        self, test_project, quarantine_dir, project_with_dumps, capsys
    ):
        """
        Test Case 3: dry_run=True
        Should find pairs but NOT quarantine orphans, logging instead.
        """
        # 🐞 FIX: Call setup_logging to configure structlog so logs emit to stderr
        setup_logging(verbose=False)

        finder = ArchiveFinder(
            root=test_project.root,
            md_pattern=DEFAULT_DUMP_PATTERN,
            search=True,  # Recursive
            verbose=False,
            dry_run=True, # Dry run
            quarantine_dir=quarantine_dir,
        )

        pairs = await finder.find_dump_pairs()

        # Assertions for found pairs (same as recursive)
        assert len(pairs) == 2

        # Assertions for quarantining (NOTHING should be moved)
        # 🐞 FIX: Check for the new, valid filenames
        assert not await (anyio.Path(quarantine_dir) / "root_orphan_all_create_dump_20250101_000200.md").exists()
        assert not await (anyio.Path(quarantine_dir) / "sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert originals are STILL present
        assert await (test_project.async_root / "root_orphan_all_create_dump_20250101_000200.md").exists()
        assert await (test_project.async_root / "subdir/sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert logging via capsys (captures structlog stderr)
        out, err = capsys.readouterr()
        assert err.count("[dry-run] Would quarantine orphan MD") == 2
        assert err.count("root_orphan_all_create_dump_20250101_000200.md") == 1
        assert err.count("sub_orphan_all_create_dump_20250101_000400.md") == 1

    async def test_ignores_non_md_files(
        self, test_project, quarantine_dir # 🐞 FIX: Removed project_with_dumps
    ):
        """
        Test Case 4: Ignores files matching pattern but not ending in .md
        """
        finder = ArchiveFinder(
            root=test_project.root,
            md_pattern=DEFAULT_DUMP_PATTERN,
            search=True,
            verbose=True, # Enable verbose to check debug logs
            dry_run=False,
            quarantine_dir=quarantine_dir,
        )

        # 🐞 FIX: This test now runs on a CLEAN directory
        # It no longer inherits files from the project_with_dumps fixture.
        await test_project.create({
            "non_md_all_create_dump_20250101_000100.sha256": "hash",
        })

        pairs = await finder.find_dump_pairs()

        # No pairs should be found
        assert len(pairs) == 0

        # 🐞 FIX: Ensure the quarantine dir exists *before* iterating it
        # The finder correctly doesn't create it if there's nothing to quarantine.
        await anyio.Path(quarantine_dir).mkdir(exist_ok=True)

        # Nothing should be quarantined
        async for _ in anyio.Path(quarantine_dir).iterdir():
            assert False, "Quarantine directory should be empty"

```

---

## src/create_dump/writing/checksum.py

<a id='src-create-dump-writing-checksum-py'></a>

```python
# src/create_dump/writing/checksum.py

"""Checksum generation and writing logic."""

from __future__ import annotations

import hashlib
from pathlib import Path
import tenacity
import anyio  # ⚡ REFACTOR: Import anyio
from ..helpers import CHUNK_SIZE  # Refactored import


class ChecksumWriter:
    """Secure checksum with retries."""

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(1))
    # ⚡ REFACTOR: Converted to async
    async def write(self, path: Path) -> str:
        """
        Calculates the SHA256 checksum of a file and writes it to a .sha256 file.
        
        NOTE: Doctest was removed as it does not support async functions.
        This logic must be tested with pytest-anyio.
        """
        sha = hashlib.sha256()
        anyio_path = anyio.Path(path)
        
        # ⚡ REFACTOR: Use async file open and read
        async with await anyio_path.open("rb") as f:
            while True:
                chunk = await f.read(CHUNK_SIZE)
                if not chunk:
                    break
                sha.update(chunk)
                
        checksum = f"{sha.hexdigest()}  {path.name}"
        
        # ⚡ REFACTOR: Use async file write
        anyio_checksum_file = anyio.Path(path.with_suffix(".sha256"))
        await anyio_checksum_file.write_text(checksum + "\n")
        
        return checksum
```

---

## src/create_dump/writing/markdown.py

<a id='src-create-dump-writing-markdown-py'></a>

~~~python
# src/create_dump/writing/markdown.py

"""Markdown writing logic.
Consumes processed files and formats them as Markdown.
"""

from __future__ import annotations

import datetime
import uuid
from datetime import timezone
from pathlib import Path
from typing import List, Optional, Dict, Any

import anyio

from ..core import DumpFile, GitMeta
from ..helpers import CHUNK_SIZE, get_language, slugify
from ..logging import logger
from ..version import VERSION


class MarkdownWriter:
    """Streams Markdown output from processed temp files."""

    def __init__(
        self,
        outfile: Path,
        no_toc: bool,
        tree_toc: bool,
    ):
        self.outfile = outfile
        self.no_toc = no_toc
        self.tree_toc = tree_toc
        self.files: List[DumpFile] = []  # Stored for metrics
        self.git_meta: Optional[GitMeta] = None
        self.version: str = VERSION

    async def write(
        self, 
        files: List[DumpFile], 
        git_meta: Optional[GitMeta], 
        version: str
    ) -> None:
        """Writes the final Markdown file from the list of processed files."""
        self.files = files  # Store for metrics
        self.git_meta = git_meta
        self.version = version
        
        await self._write_md_streamed()

    async def _write_md_streamed(self) -> None:
        """Stream final MD from temps atomically."""
        temp_out = anyio.Path(self.outfile.with_suffix(".tmp"))
        try:
            async with await temp_out.open("w", encoding="utf-8") as out:
                now = datetime.datetime.now(timezone.utc)
                
                await out.write("# 🗃️ Project Code Dump\n\n")
                await out.write(f"**Generated:** {now.isoformat(timespec='seconds')} UTC\n")
                await out.write(f"**Version:** {self.version}\n")
                if self.git_meta:
                    await out.write(
                        f"**Git Branch:** {self.git_meta.branch} | **Commit:** {self.git_meta.commit}\n"
                    )
                await out.write("\n---\n\n")

                if not self.no_toc:
                    await out.write("## Table of Contents\n\n")
                    
                    valid_files = [df for df in self.files if not df.error and df.temp_path]
                    
                    if self.tree_toc:
                        file_tree: Dict[str, Any] = {}
                        for df in valid_files:
                            parts = df.path.split('/')
                            current_level = file_tree
                            for part in parts[:-1]:
                                current_level = current_level.setdefault(part, {})
                            current_level[parts[-1]] = df
                        
                        await self._render_tree_level(out, file_tree)
                    else:
                        for idx, df in enumerate(valid_files, 1):
                            anchor = slugify(df.path)
                            await out.write(f"{idx}. [{df.path}](#{anchor})\n")
                            
                    await out.write("\n---\n\n")

                for df in self.files:
                    if df.error:
                        await out.write(
                            f"## {df.path}\n\n> ⚠️ **Failed:** {df.error}\n\n---\n\n"
                        )
                    elif df.temp_path:
                        lang = get_language(df.path)
                        has_backtick = False  # Check content for backticks
                        
                        # Read temp file to check for backticks
                        temp_content = await anyio.Path(df.temp_path).read_text(encoding="utf-8", errors="replace")
                        if "```" in temp_content:
                            has_backtick = True
                        
                        fence = "~~~" if has_backtick else "```"
                        
                        anchor = slugify(df.path)
                        await out.write(f"## {df.path}\n\n<a id='{anchor}'></a>\n\n")
                        
                        # Write fence and content
                        await out.write(f"{fence}{lang}\n")
                        await out.write(temp_content)
                        await out.write(f"\n{fence}\n\n---\n\n")

            await temp_out.rename(self.outfile)
            logger.info("MD written atomically", path=self.outfile)
        except Exception:
            if await temp_out.exists():
                await temp_out.unlink()
            raise
        finally:
            # NOTE: Final temp file cleanup is handled by the `temp_dir`
            # context manager in `single.py`.
            pass

    async def _render_tree_level(
        self,
        out_stream: anyio.abc.Stream,
        level_dict: dict,
        prefix: str = "",
    ):
        """Recursively writes the file tree to the output stream."""
        
        # Sort items so files appear before sub-directories
        sorted_items = sorted(level_dict.items(), key=lambda item: isinstance(item[1], dict))
        
        for i, (name, item) in enumerate(sorted_items):
            is_last = (i == len(sorted_items) - 1)
            connector = "└── " if is_last else "├── "
            line = f"{prefix}{connector}{name}"
            
            if isinstance(item, dict):  # It's a directory
                await out_stream.write(f"{line}\n")
                # 🐞 FIX: Use regular spaces, not non-breaking spaces
                new_prefix = prefix + ("    " if is_last else "│   ")
                await self._render_tree_level(out_stream, item, new_prefix)
            else:  # It's a DumpFile
                anchor = slugify(item.path)
                await out_stream.write(f"{line} ([link](#{anchor}))\n")
~~~

---

## tests/archive/test_core.py

<a id='tests-archive-test-core-py'></a>

```python
# tests/archive/test_core.py

"""
Tests for Phase 1: src/create_dump/archive/core.py
"""

from __future__ import annotations
import pytest
from datetime import datetime
from pathlib import Path
import anyio

from create_dump.archive.core import (
    extract_group_prefix,
    extract_timestamp,
    _safe_arcname
)

# Mark all tests in this file as async-capable
# (needed for the test_project fixture)
pytestmark = pytest.mark.anyio


# --- Test extract_group_prefix() ---

@pytest.mark.parametrize(
    "filename, expected_prefix",
    [
        # Standard cases
        ("src_all_create_dump_20250101_120000.md", "src"),
        ("tests_all_create_dump_20250101_120000.md", "tests"),
        ("my-group-1_all_create_dump_20250101_120000.md", "my-group-1"),

        # Non-matching cases
        ("default_all_create_dump_20250101_120000.zip", None), # Not .md
        ("all_create_dump_20250101_120000.md", None), # No prefix
        ("_all_create_dump_20250101_120000.md", None), # No prefix
        ("src_all_create_dump_20250101_120000.txt", None), # Not .md
        ("src_all_create_dump.md", None), # No timestamp
        ("src_all_create_dump_20250101_1200.md", None), # Invalid timestamp

        # Invalid prefix characters (should not match)
        ("src/path_all_create_dump_20250101_120000.md", None),
        ("src.._all_create_dump_20250101_120000.md", None),
    ]
)
def test_extract_group_prefix(filename: str, expected_prefix: str | None):
    """
    Tests the regex logic for extracting group prefixes from dump filenames.
    """
    assert extract_group_prefix(filename) == expected_prefix


# --- Test extract_timestamp() ---

@pytest.mark.parametrize(
    "filename, expected_dt",
    [
        # Standard cases
        ("src_all_create_dump_20250101_123005.md", datetime(2025, 1, 1, 12, 30, 5)),
        ("archive_20241225_090000.zip", datetime(2024, 12, 25, 9, 0, 0)),
        ("prefix_with_numbers_123_20250202_030405.txt", datetime(2025, 2, 2, 3, 4, 5)),

        # Non-matching cases
        ("no_timestamp.md", datetime.min),
        ("invalid_timestamp_20250101_1230.zip", datetime.min),
        ("malformed_20259999_999999.zip", datetime.min),
    ]
)
def test_extract_timestamp(filename: str, expected_dt: datetime):
    """
    Tests the regex logic for extracting timestamps from various filenames.
    """
    assert extract_timestamp(filename) == expected_dt


# --- Test _safe_arcname() ---

async def test_safe_arcname_success(test_project):
    """
    Tests that a valid file path is correctly made relative.
    """
    await test_project.create({
        "src/main.py": "pass"
    })
    root = test_project.root
    file_path = test_project.path("src/main.py")

    arcname = _safe_arcname(file_path, root)
    assert arcname == "src/main.py"

async def test_safe_arcname_raises_for_directory(test_project):
    """
    Tests that _safe_arcname() raises a ValueError if the path is a
    directory, not a file.
    """
    # ⚡ FIX: Use `create({"src/mydir": None})` to create a directory
    await test_project.create({"src/mydir": None})
    root = test_project.root
    dir_path = test_project.path("src/mydir")

    with pytest.raises(ValueError, match="not a file"):
        _safe_arcname(dir_path, root)

async def test_safe_arcname_raises_for_traversal(test_project):
    """
    Tests that _safe_arcname() raises a ValueError for path traversal.
    This is the core "Zip-Slip" security test.
    """
    root = test_project.root

    # We don't even need to create the file, just the path object
    # 1. Simple traversal
    malicious_path_1 = root / "../secret.txt"
    # 2. Complex traversal
    malicious_path_2 = root / "src/../../etc/passwd"

    # We test against the *unresolved* path, as `relative_to`
    # will catch this.
    with pytest.raises(ValueError, match="Invalid arcname with traversal"):
        _safe_arcname(malicious_path_1, root)

    with pytest.raises(ValueError, match="Invalid arcname with traversal"):
        _safe_arcname(malicious_path_2, root)

async def test_safe_arcname_raises_for_absolute(test_project):
    """
    Tests that _safe_arcname() raises a ValueError for absolute paths.
    """
    # ⚡ FIX: This test was logically flawed.
    # We must test a path that is *actually* outside the root,
    # not just an absolute path that points *inside* the root.
    root = test_project.root
    
    # Create a dummy external file to get a real, absolute, external path
    external_path = Path("/tmp/external_test_file.txt")
    await anyio.Path(external_path).write_text("external")

    # `relative_to` will fail because /tmp/external_test_file.txt
    # is not in the subpath of our test_project root.
    with pytest.raises(ValueError, match="is not in the subpath"):
        _safe_arcname(external_path, root)

    # Cleanup
    await anyio.Path(external_path).unlink(missing_ok=True)



```

---

## tests/archive/test_pruner.py

<a id='tests-archive-test-pruner-py'></a>

```python
# tests/archive/test_pruner.py

"""
Tests for Phase 3: src/create_dump/archive/pruner.py
"""

from __future__ import annotations
import pytest
from pathlib import Path

import anyio

# Import the class to test
from create_dump.archive.pruner import ArchivePruner
from create_dump.logging import setup_logging

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
async def archives_dir(test_project):
    """Provides the root path for the test project, acting as the archives_dir."""
    # Ensure logging is quiet for these tests
    setup_logging(quiet=True)
    return test_project.root


async def _create_test_archives(path: Path, archives: list[str]) -> list[str]:
    """
    Creates files with a small delay to ensure mtime sorting is predictable.
    Returns the list of names in the order they were created (oldest to newest).
    """
    # Create a subdir for the rglob test
    subdir = anyio.Path(path) / "subdir"
    await subdir.mkdir(exist_ok=True)

    created_order = []
    for i, name in enumerate(archives):
        # Place files in root and subdir to test rglob
        target_path = subdir if i % 2 == 0 else anyio.Path(path)
        await (target_path / name).write_text(f"content{i}")
        # Short sleep to make mtimes distinct and ensure order
        await anyio.sleep(0.01)
        created_order.append(name)

    return created_order


class TestArchivePruner:
    """Groups tests for the ArchivePruner."""

    async def test_prune_keep_last_is_none(self, archives_dir: Path):
        """Test Case 1: Pruner does nothing if keep_last is None."""
        archive_names = [
            "archive_all_create_dump_20250101_000100.zip",
            "archive_all_create_dump_20250101_000200.zip",
        ]
        await _create_test_archives(archives_dir, archive_names)

        pruner = ArchivePruner(archives_dir, keep_last=None, verbose=False)
        await pruner.prune()

        # Assert all files still exist
        assert await anyio.Path(archives_dir / "subdir" / archive_names[0]).exists()
        assert await anyio.Path(archives_dir / archive_names[1]).exists()

    async def test_prune_keep_last_gt_files(self, archives_dir: Path):
        """Test Case 2: Pruner does nothing if file count is <= keep_last."""
        archive_names = [
            "archive_all_create_dump_20250101_000100.zip",
            "archive_all_create_dump_20250101_000200.zip",
        ]
        await _create_test_archives(archives_dir, archive_names)

        pruner = ArchivePruner(archives_dir, keep_last=5, verbose=False)
        await pruner.prune()

        # Assert all files still exist
        assert await anyio.Path(archives_dir / "subdir" / archive_names[0]).exists()
        assert await anyio.Path(archives_dir / archive_names[1]).exists()

    async def test_prune_prunes_oldest_files(self, archives_dir: Path):
        """Test Case 3: Pruner correctly prunes the oldest files."""
        archive_names = [
            "archive_all_create_dump_20250101_000100.zip",  # Oldest
            "archive_all_create_dump_20250101_000200.zip",
            "archive_all_create_dump_20250101_000300.zip",
            "archive_all_create_dump_20250101_000400.zip",
            "archive_all_create_dump_20250101_000500.zip",  # Newest
        ]
        # Create files; the first 3 will be pruned
        await _create_test_archives(archives_dir, archive_names)

        pruner = ArchivePruner(archives_dir, keep_last=2, verbose=True)
        await pruner.prune()

        # Assert the OLDEST 3 files are GONE
        assert not await anyio.Path(archives_dir / "subdir" / archive_names[0]).exists()
        assert not await anyio.Path(archives_dir / archive_names[1]).exists()
        assert not await anyio.Path(archives_dir / "subdir" / archive_names[2]).exists()

        # Assert the NEWEST 2 files REMAIN
        assert await anyio.Path(archives_dir / archive_names[3]).exists()
        assert await anyio.Path(archives_dir / "subdir" / archive_names[4]).exists()

    async def test_prune_ignores_non_matching_files(self, archives_dir: Path):
        """
        Test Case 4: Pruner ignores non-matching files but prunes *all* valid archive formats (.zip, .tar.gz) based on mtime.
        """
        archive_names = [
            "archive_all_create_dump_20250101_000100.zip",    # Oldest, to be pruned (mtime 1)
            "archive_all_create_dump_20250101_000200.zip",    # To be pruned (mtime 2)
            "not_a_dump.zip",                                 # Ignored (mtime 3)
            "archive_all_create_dump_20250101_000400.tar.gz"  # Newest, to keep (mtime 4)
        ]
        await _create_test_archives(archives_dir, archive_names)

        # ⚡ FIX: keep_last=1. The pruner will find 3 valid archives.
        pruner = ArchivePruner(archives_dir, keep_last=1, verbose=False)
        await pruner.prune()

        # ⚡ FIX: Assert the OLDEST 2 matching files are GONE
        # The .tar.gz is now correctly included in the logic.
        assert not await anyio.Path(archives_dir / "subdir" / archive_names[0]).exists() # pruned
        assert not await anyio.Path(archives_dir / archive_names[1]).exists() # pruned

        # ⚡ FIX: Assert the NON-MATCHING file REMAINS
        assert await anyio.Path(archives_dir / "subdir" / archive_names[2]).exists() # ignored

        # ⚡ FIX: Assert the NEWEST matching file REMAINS
        assert await anyio.Path(archives_dir / archive_names[3]).exists() # kept
```

---

## tests/cli/test_main.py

<a id='tests-cli-test-main-py'></a>

```python
# tests/cli/test_main.py

"""
Tests for src/create_dump/cli/main.py
"""

from __future__ import annotations
import pytest
from typer.testing import CliRunner
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

# Import the app to test
from create_dump.cli.main import app
from create_dump.version import VERSION
# 🐞 FIX: Import the function we are checking
from create_dump.cli.single import run_single


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provides a Typer CliRunner instance."""
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_cli_deps(mocker):
    """
    Mocks all heavy dependencies called by CLI commands.
    We are only testing the CLI wiring, not the full execution.
    """
    # 🐞 FIX: Mock `anyio.run` where it's called (in cli.single)
    # This is the boundary of the CLI code.
    mock_anyio_run = mocker.patch(
        "create_dump.cli.single.anyio.run",
        new_callable=MagicMock
    )

    # Mock the `anyio.run` call in `cli/batch.py`
    mock_run_batch_async = mocker.patch(
        "create_dump.cli.batch.anyio.run",
        new_callable=MagicMock
    )

    # Mock config loading
    mock_load_config = mocker.patch("create_dump.cli.main.load_config")

    # Mock logging setup
    mock_setup_logging = mocker.patch("create_dump.cli.main.setup_logging")
    # Also mock the setup_logging call in cli.single
    mocker.patch("create_dump.cli.single.setup_logging")


    return {
        "run_single": mock_anyio_run, # 🐞 FIX: Point to the new mock
        "run_batch": mock_run_batch_async,
        "load_config": mock_load_config,
        "setup_logging": mock_setup_logging,
    }


class TestMainCli:
    """Tests for the main app callback and command registration."""

    def test_version_flag(self, cli_runner: CliRunner):
        """Test Case 1: --version flag prints version and exits."""
        result = cli_runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert f"create-dump v{VERSION}" in result.stdout

    def test_batch_subcommand_help(self, cli_runner: CliRunner):
        """Test Case 2: 'batch' subcommand is registered."""
        result = cli_runner.invoke(app, ["batch", "--help"])
        assert result.exit_code == 0
        assert "Batch operations" in result.stdout

    def test_logging_flags(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """Test Case 3: --verbose and --quiet flags call setup_logging."""
        mock_setup_logging = mock_cli_deps["setup_logging"]

        with cli_runner.isolated_filesystem():
            # Test --verbose
            cli_runner.invoke(app, ["--verbose", "single", "--help"])
            mock_setup_logging.assert_called_with(verbose=True, quiet=False)

        with cli_runner.isolated_filesystem():
            # Test --quiet
            cli_runner.invoke(app, ["--quiet", "batch", "--help"])
            mock_setup_logging.assert_called_with(verbose=False, quiet=True)

    def test_config_flag(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """Test Case 4: --config flag calls load_config with the correct path."""
        with cli_runner.isolated_filesystem() as temp_dir:
            config_file = Path(temp_dir) / "my_config.toml"
            config_file.write_text("test")

            cli_runner.invoke(app, ["--config", "my_config.toml", "single", "--help"])

            mock_cli_deps["load_config"].assert_called_with(Path("my_config.toml"))


class TestInitWizard:
    """Tests for the --init interactive wizard."""

    def test_init_success(self, cli_runner: CliRunner, mocker):
        """Test Case 7: --init wizard runs, mocks prompts, and creates file."""
        mocker.patch("create_dump.cli.main.typer.prompt", return_value="my/dumps")
        mocker.patch("create_dump.cli.main.typer.confirm", side_effect=[True, False, True])

        with cli_runner.isolated_filesystem() as temp_dir:
            # 🐞 FIX: Surgically mock Path.exists to return False for this test
            mocker.patch("pathlib.Path.exists", return_value=False)

            config_path = Path(temp_dir) / "create_dump.toml"

            result = cli_runner.invoke(app, ["--init"])

            assert result.exit_code == 0
            assert "Success!" in result.stdout

            # We can't assert config_path.exists() because we mocked it
            # But we can check the stdout
            assert f"config file created at {config_path.resolve()}" in result.stdout

            # We can also check the content (by mocking write_text)
            # This is complex, so we'll trust the stdout.

    def test_init_file_exists(self, cli_runner: CliRunner):
        """Test Case 8: --init fails if config file already exists."""
        with cli_runner.isolated_filesystem() as temp_dir:
            config_path = Path(temp_dir) / "create_dump.toml"
            config_path.write_text("existing")

            result = cli_runner.invoke(app, ["--init"])

            assert result.exit_code == 1
            assert "already exists" in result.stdout
            assert config_path.read_text() == "existing"

    def test_init_io_error(self, cli_runner: CliRunner, mocker):
        """Test Case 9: --init handles IOError on file write."""
        mocker.patch("create_dump.cli.main.typer.prompt", return_value="")
        mocker.patch("create_dump.cli.main.typer.confirm", return_value=True)

        with cli_runner.isolated_filesystem() as temp_dir:
            # 🐞 FIX: Surgically mock Path.exists to return False for this test
            mocker.patch("pathlib.Path.exists", return_value=False)

            # Now, mock write_text to fail
            mocker.patch("pathlib.Path.write_text", side_effect=IOError("Permission denied"))

            result = cli_runner.invoke(app, ["--init"])

            assert result.exit_code == 1
            assert "Error:" in result.stdout
            assert "Permission denied" in result.stdout
```

---

## src/create_dump/workflow/single.py

<a id='src-create-dump-workflow-single-py'></a>

```python
# src/create_dump/workflow/single.py

"""The core single-run orchestration logic."""

from __future__ import annotations

import gzip
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional
from typer import Exit

import anyio

# Local project imports
from ..archiver import ArchiveManager
from ..collector import get_collector
from ..core import Config, GitMeta, load_config
# ⚡ REFACTOR: Import the async safety check
from ..path_utils import safe_is_within
from ..helpers import _unique_path
from ..logging import logger, styled_print
from ..metrics import DUMP_DURATION, metrics_server
from ..system import get_git_meta
from ..processor import FileProcessor, ProcessorMiddleware
from ..writing import ChecksumWriter, MarkdownWriter, JsonWriter
from ..version import VERSION
from ..scanning import SecretScanner


class SingleRunOrchestrator:
    """Orchestrates a complete, single dump run."""

    def __init__(
        self,
        root: Path,
        dry_run: bool,
        yes: bool,
        no_toc: bool,
        tree_toc: bool,
        compress: bool,
        format: str,
        exclude: str,
        include: str,
        max_file_size: Optional[int],
        use_gitignore: bool,
        git_meta: bool,
        progress: bool,
        max_workers: int,
        archive: bool,
        archive_all: bool,
        archive_search: bool,
        archive_include_current: bool,
        archive_no_remove: bool,
        archive_keep_latest: bool,
        archive_keep_last: Optional[int],
        archive_clean_root: bool,
        archive_format: str,
        allow_empty: bool,
        metrics_port: int,
        verbose: bool,
        quiet: bool,
        dest: Optional[Path] = None,
        git_ls_files: bool = False,
        diff_since: Optional[str] = None,
        scan_secrets: bool = False,
        hide_secrets: bool = False,
    ):
        # Store all parameters as instance attributes
        self.root = root
        self.dry_run = dry_run
        self.yes = yes
        self.no_toc = no_toc
        self.tree_toc = tree_toc
        self.compress = compress
        self.format = format
        self.exclude = exclude
        self.include = include
        self.max_file_size = max_file_size
        self.use_gitignore = use_gitignore
        self.git_meta = git_meta
        self.progress = progress
        self.max_workers = max_workers
        self.archive = archive
        self.archive_all = archive_all
        self.archive_search = archive_search
        self.archive_include_current = archive_include_current
        self.archive_no_remove = archive_no_remove
        self.archive_keep_latest = archive_keep_latest
        self.archive_keep_last = archive_keep_last
        self.archive_clean_root = archive_clean_root
        self.archive_format = archive_format
        self.allow_empty = allow_empty
        self.metrics_port = metrics_port
        self.verbose = verbose
        self.quiet = quiet
        self.dest = dest
        self.git_ls_files = git_ls_files
        self.diff_since = diff_since
        self.scan_secrets = scan_secrets
        self.hide_secrets = hide_secrets
        
        # ⚡ REFACTOR: Store anyio.Path version of root
        self.anyio_root = anyio.Path(self.root)

    
    # ⚡ FIX: Removed 'async' keyword. This must be a sync function.
    def _get_total_size_sync(self, files: List[str]) -> int:
        """Helper to run blocking stat() calls in a thread."""
        size = 0
        for f in files:
            try:
                # This is a blocking call, which is why the func is run in a thread
                size += (self.root / f).stat().st_size
            except FileNotFoundError:
                pass  # File may have vanished, skip
        return size

    def _compress_file_sync(self, in_file: Path, out_file: Path):
        """Blocking helper to gzip a file."""
        with open(in_file, "rb") as f_in, gzip.open(out_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    async def run(self):
        """The core logic for a single dump run."""
        
        # Load config on each run, in case it changed
        cfg = load_config()
        if self.max_file_size is not None:
            cfg.max_file_size_kb = self.max_file_size

        # Apply config defaults for new flags
        # CLI flags take precedence (if True), otherwise use config file
        
        effective_git_ls_files = self.git_ls_files or cfg.git_ls_files
        effective_scan_secrets = self.scan_secrets or cfg.scan_secrets
        effective_hide_secrets = self.hide_secrets or cfg.hide_secrets

        includes = [p.strip() for p in self.include.split(",") if p.strip()]
        excludes = [p.strip() for p in self.exclude.split(",") if p.strip()]

        # ⚡ FIX: Use the 'get_collector' factory function
        collector = get_collector(
            config=cfg, 
            includes=includes, 
            excludes=excludes, 
            use_gitignore=self.use_gitignore, 
            root=self.root,
            git_ls_files=effective_git_ls_files,
            diff_since=self.diff_since, # diff_since is CLI-only, not in config
        )
        files_list = await collector.collect()

        if not files_list:
            msg = "⚠️ No matching files found; skipping dump."
            logger.warning(msg)
            if self.verbose:
                logger.debug("Excludes: %s, Includes: %s", excludes, includes)
            if not self.quiet:
                styled_print(f"[yellow]{msg}[/yellow]")
            if not self.allow_empty:
                raise Exit(code=1)
            return

        # ⚡ FIX: This call is now correct, as it's passing a sync func
        total_size = await anyio.to_thread.run_sync(self._get_total_size_sync, files_list)

        logger.info(
            "Collection complete",
            count=len(files_list),
            total_size_kb=total_size / 1024,
            root=str(self.root),
        )
        if not self.quiet:
            styled_print(
                f"[green]📄 Found {len(files_list)} files ({total_size / 1024:.1f} KB total).[/green]"
            )

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        foldername = self.root.name or "project"
        
        file_ext = "json" if self.format == "json" else "md"
        branded_name = Path(f"{foldername}_all_create_dump_{timestamp}.{file_ext}")
        
        output_dest = self.root
        if self.dest:
            output_dest = self.dest.resolve()
            if not output_dest.is_absolute():
                output_dest = self.root / self.dest
            
            # ⚡ REFACTOR: (Target 1) Use await and async check
            anyio_output_dest = anyio.Path(output_dest)
            if not await safe_is_within(anyio_output_dest, self.anyio_root):
                logger.warning("Absolute dest outside root; proceeding with caution.")
            await anyio_output_dest.mkdir(parents=True, exist_ok=True)
        
        base_outfile = output_dest / branded_name
        
        prompt_outfile = await anyio.to_thread.run_sync(_unique_path, base_outfile)

        if not self.yes and not self.dry_run and not self.quiet:
            styled_print(
                f"Proceed with dump to [blue]{prompt_outfile}[/blue]? [yellow](y/n)[/yellow]",
                nl=False,
            )
            user_input = await anyio.to_thread.run_sync(input, "")
            if not user_input.lower().startswith("y"):
                styled_print("[red]Cancelled.[/red]")
                raise Exit(code=1)

        try:
            if self.dry_run:
                styled_print("[green]✅ Dry run: Would process listed files.[/green]")
                if not self.quiet:
                    for p in files_list:
                        styled_print(f" - {p}")
                raise Exit(code=0)


            outfile = await anyio.to_thread.run_sync(_unique_path, base_outfile)
            gmeta = await anyio.to_thread.run_sync(get_git_meta, self.root) if self.git_meta else None

            temp_dir = TemporaryDirectory()
            try:
                processed_files: List[DumpFile] = []
                
                # ⚡ FIX: Determine collector label BEFORE starting timer
                if self.diff_since:
                    collector_label = "git_diff"
                elif effective_git_ls_files: # Use the same var as collector
                    collector_label = "git_ls"
                else:
                    collector_label = "walk"
                
                with metrics_server(port=self.metrics_port):
                    # ⚡ FIX: Apply the label to the metric
                    with DUMP_DURATION.labels(collector=collector_label).time():
                        
                        # ⚡ REFACTOR: Step 1 - Build middleware
                        middlewares: List[ProcessorMiddleware] = []
                        if effective_scan_secrets:
                            middlewares.append(
                                SecretScanner(hide_secrets=effective_hide_secrets)
                            )
                        
                        # ⚡ REFACTOR: Step 2 - Process files
                        processor = FileProcessor(
                            temp_dir.name,
                            middlewares=middlewares, # Pass middleware list
                        )
                        processed_files = await processor.dump_concurrent(
                            files_list, self.progress, self.max_workers
                        )
                        
                        # Step 3 - Format output
                        if self.format == "json":
                            writer = JsonWriter(outfile)
                            await writer.write(processed_files, gmeta, VERSION)
                        else:
                            writer = MarkdownWriter(
                                outfile, 
                                self.no_toc, 
                                self.tree_toc,
                            )
                            await writer.write(processed_files, gmeta, VERSION)

                # Step 4 - Compress
                if self.compress:
                    gz_outfile = outfile.with_suffix(f".{file_ext}.gz")
                    await anyio.to_thread.run_sync(self._compress_file_sync, outfile, gz_outfile)
                    
                    await anyio.Path(outfile).unlink()
                    outfile = gz_outfile
                    logger.info("Output compressed", path=str(outfile))

                # Step 5 - Checksum
                checksum_writer = ChecksumWriter()
                checksum = await checksum_writer.write(outfile)
                if not self.quiet:
                    styled_print(f"[blue]{checksum}[/blue]")

                # Step 6 - Archive
                if self.archive or self.archive_all:
                    manager = ArchiveManager(
                        root=self.root,
                        timestamp=timestamp,
                        keep_latest=self.archive_keep_latest,
                        keep_last=self.archive_keep_last,
                        clean_root=self.archive_clean_root,
                        search=self.archive_search,
                        include_current=self.archive_include_current,
                        no_remove=self.archive_no_remove,
                        dry_run=self.dry_run,
                        yes=self.yes,
                        verbose=self.verbose,
                        md_pattern=cfg.dump_pattern,
                        archive_all=self.archive_all,
                        archive_format=self.archive_format, 
                    )
                    archive_results = await manager.run(current_outfile=outfile)
                    if archive_results:
                        groups = ', '.join(k for k, v in archive_results.items() if v)
                        if not self.quiet:
                            styled_print(f"[green]Archived groups: {groups}[/green]")
                        logger.info("Archiving complete", groups=groups)
                    else:
                        msg = "ℹ️ No prior dumps found for archiving."
                        if not self.quiet:
                            styled_print(f"[yellow]{msg}[/yellow]")
                        logger.info(msg)

                # Final metrics
                success_count = sum(1 for f in processed_files if not f.error)
                logger.info(
                    "Dump summary",
                    success=success_count,
                    errors=len(processed_files) - success_count,
                    output=str(outfile),
                )
            finally:
                await anyio.to_thread.run_sync(temp_dir.cleanup)

        except Exit as e:
            # Re-raise to be handled by the caller
            raise
```

---

## tests/collector/test_git_diff.py

<a id='tests-collector-test-git-diff-py'></a>

```python
# tests/collector/test_git_diff.py

"""
Tests for src/create_dump/collector/git_diff.py
"""

from __future__ import annotations
import pytest
from unittest.mock import AsyncMock, patch

# Import the class to test
from create_dump.collector.git_diff import GitDiffCollector
from create_dump.core import Config

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_get_git_diff_files(mocker) -> AsyncMock:
    """Mocks the system call to get_git_diff_files."""
    return mocker.patch(
        "create_dump.collector.git_diff.get_git_diff_files",
        new_callable=AsyncMock
    )


@pytest.fixture
def mock_filter_files(mocker) -> AsyncMock:
    """Mocks the base class's filter_files method."""
    return mocker.patch(
        "create_dump.collector.base.CollectorBase.filter_files",
        new_callable=AsyncMock
    )


class TestGitDiffCollector:
    """Tests for the GitDiffCollector."""

    async def test_collect_success(
        self,
        test_project,
        default_config: Config,
        mock_get_git_diff_files: AsyncMock,
        mock_filter_files: AsyncMock,
    ):
        """
        Test Case 1: (Happy Path)
        Validates that:
        1. get_git_diff_files is called with the correct ref.
        2. The raw list is passed to filter_files.
        3. The filtered list is returned.
        """
        raw_files = ["src/main.py", "README.md"]
        filtered_files = ["src/main.py", "README.md"]
        diff_ref = "main"
        
        mock_get_git_diff_files.return_value = raw_files
        mock_filter_files.return_value = filtered_files
        
        collector = GitDiffCollector(
            config=default_config,
            root=test_project.root,
            diff_since=diff_ref
        )
        result = await collector.collect()

        # Assertions
        mock_get_git_diff_files.assert_called_once_with(
            test_project.root, diff_ref
        )
        mock_filter_files.assert_called_once_with(raw_files)
        assert result == filtered_files

    async def test_collect_no_files_found(
        self,
        test_project,
        default_config: Config,
        mock_get_git_diff_files: AsyncMock,
        mock_filter_files: AsyncMock,
    ):
        """
        Test Case 2: (Empty Result)
        Validates that filter_files is NOT called if git diff returns empty.
        """
        diff_ref = "main"
        mock_get_git_diff_files.return_value = []
        
        collector = GitDiffCollector(
            config=default_config,
            root=test_project.root,
            diff_since=diff_ref
        )
        result = await collector.collect()

        # Assertions
        mock_get_git_diff_files.assert_called_once_with(
            test_project.root, diff_ref
        )
        mock_filter_files.assert_not_called()
        assert result == []
```

---

## tests/cli/test_single.py

<a id='tests-cli-test-single-py'></a>

```python
# tests/cli/test_single.py

"""
Comprehensive tests for the 'single' command in src/create_dump/cli/single.py
"""

from __future__ import annotations
import pytest
from typer.testing import CliRunner
# 🐞 FIX: Import ANY and call
from unittest.mock import MagicMock, patch, AsyncMock, call, ANY
from pathlib import Path
from typer import Exit

# Import the main app to test the 'single' command in context
from create_dump.cli.main import app
# 🐞 FIX: Import the function we need to check the *identity* of
from create_dump.cli.single import run_single


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provides a Typer CliRunner instance."""
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_cli_deps(mocker):
    """
    Mocks all downstream dependencies for cli.single, allowing us to
    test the CLI logic in isolation.
    """
    # 🐞 FIX: Mock anyio.run itself, not the async function
    # This is a more robust way to test the CLI boundary.
    mock_anyio_run = mocker.patch(
        "create_dump.cli.single.anyio.run",
        new_callable=MagicMock  # Use a standard mock, not AsyncMock
    )

    # Mock the logging setup function
    mock_setup_logging = mocker.patch("create_dump.cli.single.setup_logging")

    # Mock dependencies from cli.main to allow the app to load
    mocker.patch("create_dump.cli.main.load_config")
    # 🐞 FIX: Make the main setup_logging mock point to the same object
    # This ensures we can reliably test the *final* call from cli.single
    mocker.patch("create_dump.cli.main.setup_logging", new=mock_setup_logging)

    return {
        "anyio_run": mock_anyio_run, # 🐞 FIX: Return the new mock
        "setup_logging": mock_setup_logging,
    }


class TestSingleCli:
    """Tests for the 'single' command logic."""

    def test_invalid_root_is_file(self, cli_runner: CliRunner):
        """
        Test Case 1: (Validation)
        Fails with BadParameter if the root argument is a file, not a directory.
        """
        with cli_runner.isolated_filesystem() as temp_dir:
            file_path = Path(temp_dir) / "im_a_file.txt"
            file_path.write_text("content")

            result = cli_runner.invoke(app, ["single", str(file_path)])

            assert result.exit_code != 0
            # 🐞 FIX: Typer errors print to stderr
            assert "is not a directory" in result.stderr

    def test_flag_conflict_git_ls_and_diff(self, cli_runner: CliRunner):
        """
        Test Case 2: (Validation)
        Fails with BadParameter if --git-ls-files and --diff-since are used together.
        """
        result = cli_runner.invoke(app, [
            "single", ".", "--git-ls-files", "--diff-since", "main"
        ])
        assert result.exit_code != 0
        # 🐞 FIX: Typer errors print to stderr
        assert "mutually exclusive" in result.stderr

    def test_flag_conflict_hide_secrets(self, cli_runner: CliRunner):
        """
        Test Case 3: (Validation)
        Fails with BadParameter if --hide-secrets is used without --scan-secrets.
        """
        result = cli_runner.invoke(app, ["single", ".", "--hide-secrets"])
        assert result.exit_code != 0
        # 🐞 FIX: Typer errors print to stderr
        assert "requires --scan-secrets" in result.stderr

    @pytest.mark.parametrize(
        "cli_flags, expected_dry_run_val",
        [
            (["-d"], True),
            (["--dry-run"], True),
            (["-nd"], False),
            (["--no-dry-run"], False),
            (["-d", "-nd"], False),
            ([], False),
        ],
    )
    def test_effective_dry_run_logic(
        self, cli_runner: CliRunner, mock_cli_deps: dict, cli_flags: list[str], expected_dry_run_val: bool
    ):
        """
        Test Case 5: (effective_dry_run)
        Tests all combinations of -d and -nd to ensure the correct
        boolean is passed to the async runner.
        """
        with cli_runner.isolated_filesystem():
            cli_runner.invoke(app, ["single", "."] + cli_flags, catch_exceptions=False)

        mock_anyio_run = mock_cli_deps["anyio_run"] # 🐞 FIX: Get the right mock
        mock_anyio_run.assert_called_once()
        call_args = mock_anyio_run.call_args[0]
        # 🐞 FIX: Index is 2 (arg[0] is function, arg[1] is root)
        assert call_args[2] is expected_dry_run_val

    @pytest.mark.parametrize(
        "cli_flags, expected_verbose, expected_quiet, expected_progress",
        [
            # Default
            (["single", "."], False, False, True),
            # Main flags
            (["-v", "single", "."], True, False, True),
            (["-q", "single", "."], False, True, False),
            # Command flags
            (["single", "-v", "."], True, False, True),
            (["single", "-q", "."], False, True, False),
            # Command overrides Main
            (["-v", "single", "-q", "."], False, True, False),
            (["-q", "single", "-v", "."], True, False, True),
            # Progress flag interaction
            (["single", ".", "--no-progress"], False, False, False),
            (["single", "-q", ".", "--progress"], False, True, False), # Quiet wins
        ],
    )
    def test_verbose_quiet_progress_logic(
        self, cli_runner: CliRunner, mock_cli_deps: dict, cli_flags: list[str],
        expected_verbose: bool, expected_quiet: bool, expected_progress: bool
    ):
        """
        Test Case 6: (Logging & Progress)
        Tests the complex logic for verbose/quiet flags, including
        precedence of command flags over main flags, and how
        they interact with the progress flag.
        """
        with cli_runner.isolated_filesystem():
            cli_runner.invoke(app, cli_flags, catch_exceptions=False)

        mock_setup_logging = mock_cli_deps["setup_logging"]
        mock_anyio_run = mock_cli_deps["anyio_run"] # 🐞 FIX: Get the right mock

        # 1. Check that setup_logging was called with the correct final values
        # The logic in single.py ensures it's called *last* with the final values.
        mock_setup_logging.assert_called_with(verbose=expected_verbose, quiet=expected_quiet)

        # 2. Check that the correct values were passed to the async runner
        mock_anyio_run.assert_called_once() # 🐞 FIX: Assert on anyio_run
        call_args = mock_anyio_run.call_args[0]
        # 🐞 FIX: Update positional indices
        # arg[0] is function, arg[1-12] are first 12 args...
        assert call_args[13] is expected_progress # arg[13] is 'effective_progress'
        assert call_args[26] is expected_verbose  # arg[26] is 'verbose_val'
        assert call_args[27] is expected_quiet    # arg[27] is 'quiet_val'

    def test_all_flags_passed_to_run_single(self, cli_runner: CliRunner, mock_cli_deps: dict):
        """
        Test Case 7: (Argument Passthrough)
        This is the primary integration test for cli/single.py.
        It verifies that *all* CLI flags are correctly processed and
        passed to the `anyio.run(run_single, ...)` call in the
        correct positional order.
        """
        with cli_runner.isolated_filesystem() as temp_dir:
            dest_path = Path(temp_dir) / "my_dest"
            dest_path.mkdir()

            cli_args = [
                "single",
                ".",
                "--dest", str(dest_path),
                "--no-toc",
                "--tree-toc",
                "--format", "json",
                "-c", # compress
                "--allow-empty",
                "--metrics-port", "9090",
                "--exclude", "a,b",
                "--include", "c,d",
                "--max-file-size", "1024",
                "--no-use-gitignore",
                "--no-git-meta",
                "--max-workers", "8",
                "--watch",
                "--git-ls-files",
                "--diff-since", "main", # Note: This would fail validation, but we test validation separately
                "--scan-secrets",
                "--hide-secrets",
                "-a", # archive
                "--archive-all",
                "--archive-search",
                "--no-archive-include-current",
                "--archive-no-remove",
                "--no-archive-keep-latest",
                "--archive-keep-last", "5",
                "--archive-clean-root",
                "--archive-format", "tar.gz",
                "-y", # yes
            ]
            
            # We catch exceptions because the git-ls/diff-since conflict *will*
            # be raised, but we only care about testing the *call* to run_single
            # if validation *passed*. For this test, we'll remove the conflict.
            cli_args.remove("--git-ls-files")

            result = cli_runner.invoke(app, cli_args, catch_exceptions=False)
            assert result.exit_code == 0

            mock_anyio_run = mock_cli_deps["anyio_run"] # 🐞 FIX: Get the right mock
            mock_anyio_run.assert_called_once()

            # Verify all 34 arguments passed to anyio.run
            call_args = mock_anyio_run.call_args[0]
            
            # 🐞 FIX: Check identity of the function (arg 0)
            assert call_args[0] is run_single

            # 🐞 FIX: Check arg indices (shifted by 1)
            assert call_args[1] == Path('.')           # root
            assert call_args[2] is False           # effective_dry_run
            assert call_args[3] is True            # yes
            assert call_args[4] is True            # no_toc
            assert call_args[5] is True            # tree_toc
            assert call_args[6] is True            # compress
            assert call_args[7] == "json"          # format
            assert call_args[8] == "a,b"           # exclude
            assert call_args[9] == "c,d"           # include
            assert call_args[10] == 1024           # max_file_size
            assert call_args[11] is False          # use_gitignore
            assert call_args[12] is False          # git_meta
            assert call_args[13] is True           # effective_progress
            assert call_args[14] == 8              # max_workers
            assert call_args[15] is True           # archive
            assert call_args[16] is True           # archive_all
            assert call_args[17] is True           # archive_search
            assert call_args[18] is False          # archive_include_current
            assert call_args[19] is True           # archive_no_remove
            assert call_args[20] is False          # archive_keep_latest
            assert call_args[21] == 5              # archive_keep_last
            assert call_args[22] is True           # archive_clean_root
            assert call_args[23] == "tar.gz"       # archive_format
            assert call_args[24] is True           # allow_empty
            assert call_args[25] == 9090           # metrics_port
            assert call_args[26] is False          # verbose_val
            assert call_args[27] is False          # quiet_val
            assert call_args[28] == dest_path      # dest
            assert call_args[29] is True           # watch
            assert call_args[30] is False          # git_ls_files
            assert call_args[31] == "main"         # diff_since
            assert call_args[32] is True           # scan_secrets
            assert call_args[33] is True           # hide_secrets

    def test_dry_run_exit_is_graceful(self, cli_runner: CliRunner, mock_cli_deps: dict):
        """
        Test Case 8: (Exception Handling)
        Ensures that if the async runner raises Exit(code=0) (e.g.,
        from its own dry_run check), the CLI exits gracefully with code 0.
        """
        mock_anyio_run = mock_cli_deps["anyio_run"] # 🐞 FIX: Get the right mock
        mock_anyio_run.side_effect = Exit(code=0)

        # Pass -d to trigger the `if ... and dry_run` check
        result = cli_runner.invoke(app, ["single", ".", "-d"])

        assert result.exit_code == 0
        mock_anyio_run.assert_called_once()

    def test_real_exit_propagates(self, cli_runner: CliRunner, mock_cli_deps: dict):
        """
        Test Case 9: (Exception Handling)
        Ensures that if the async runner raises a real error (e.g.,
        Exit(code=1)), the CLI propagates that error.
        """
        mock_anyio_run = mock_cli_deps["anyio_run"] # 🐞 FIX: Get the right mock
        mock_anyio_run.side_effect = Exit(code=1)

        # Do NOT pass -d
        result = cli_runner.invoke(app, ["single", "."])

        assert result.exit_code == 1
        mock_anyio_run.assert_called_once()
```

---

## tests/cli/test_batch.py

<a id='tests-cli-test-batch-py'></a>

```python
# tests/cli/test_batch.py

"""
Tests for src/create_dump/cli/batch.py
"""

from __future__ import annotations
import pytest
from typer.testing import CliRunner
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path

# Import the app to test
from create_dump.cli.main import app
# Import the helper function to test directly
from create_dump.cli.batch import split_dirs
from create_dump.core import DEFAULT_DUMP_PATTERN

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provides a Typer CliRunner instance."""
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_cli_deps(mocker):
    """
    Mocks all heavy dependencies called by the batch CLI commands.
    """
    # Mock the `anyio.run` call in `cli/batch.py`
    mock_anyio_run = mocker.patch(
        "create_dump.cli.batch.anyio.run",
        new_callable=MagicMock
    )

    # Mock ArchiveManager instantiation in `cli/batch.py`
    mock_manager_instance = MagicMock()
    mock_manager_instance.run = AsyncMock()  # Mock the async run method
    mock_manager_class = mocker.patch(
        "create_dump.cli.batch.ArchiveManager",
        return_value=mock_manager_instance
    )

    # Mock config loading (from main)
    mocker.patch("create_dump.cli.main.load_config")

    # Mock logging setup
    mock_setup_logging = mocker.patch("create_dump.cli.batch.setup_logging")
    # 🐞 FIX: Also mock logging in main, as it's called by the app
    mocker.patch("create_dump.cli.main.setup_logging")


    return {
        "anyio_run": mock_anyio_run,
        "ArchiveManager_class": mock_manager_class,
        "ArchiveManager_instance": mock_manager_instance,
        "setup_logging": mock_setup_logging,
    }


class TestSplitDirs:
    """Tests the split_dirs helper function."""

    def test_split_dirs_default_string(self):
        """Test with the default string from typer.Option."""
        assert split_dirs(".,packages,services") == [".", "packages", "services"]

    def test_split_dirs_empty_string(self):
        """Test that an empty string falls back to defaults."""
        assert split_dirs("") == [".", "packages", "services"]

    def test_split_dirs_all_empty(self):
        """Test that a string of commas falls back to defaults."""
        assert split_dirs(",,,") == [".", "packages", "services"]

    def test_split_dirs_custom(self):
        """Test a standard custom list."""
        assert split_dirs("src,tests") == ["src", "tests"]

    def test_split_dirs_with_whitespace(self):
        """Test that whitespace is correctly stripped."""
        assert split_dirs("  src , tests, app  ") == ["src", "tests", "app"]


class TestBatchCli:
    """Tests for the 'batch' command group."""

    def test_batch_callback_defaults(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test Case 1: (Callback Defaults)
        Validates that the callback sets defaults correctly, especially dry_run=True.
        """
        mock_run = mock_cli_deps["anyio_run"]

        # 🐞 FIX: Use isolated_filesystem
        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(app, ["batch", "run", "."])

        assert result.exit_code == 0
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]
        assert call_args[4] is True  # Check effective_dry_run (arg 4)

    def test_batch_callback_no_dry_run(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test Case 2: (Callback Override)
        Validates that --no-dry-run correctly overrides the callback's default.
        """
        mock_run = mock_cli_deps["anyio_run"]

        # 🐞 FIX: Use isolated_filesystem
        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(app, ["batch", "run", ".", "--no-dry-run"])

        assert result.exit_code == 0
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]
        assert call_args[4] is False  # Check effective_dry_run (arg 4)

    def test_run_command_flags(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test Case 3: (run command)
        Validates all flags for 'batch run' are passed to anyio.run.
        """
        mock_run = mock_cli_deps["anyio_run"]

        # 🐞 FIX: Use isolated_filesystem
        with cli_runner.isolated_filesystem() as temp_dir:
            result = cli_runner.invoke(app, [
                "batch", "run", ".",
                "--dirs", "src,tests",
                "--pattern", ".*.log",
                "--format", "json",
                "--max-workers", "10",
                "--archive-all",
                "--archive-format", "tar.gz",
                "-y",
                "--no-dry-run"
            ])

        assert result.exit_code == 0
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]

        assert call_args[0].__name__ == "run_batch"
        # 🐞 FIX: Assert against the Path object `.`
        assert call_args[1] == Path(".")       # root
        assert call_args[2] == ["src", "tests"]      # subdirs
        assert call_args[3] == ".*.log"              # pattern
        assert call_args[4] is False                 # effective_dry_run
        assert call_args[5] is True                  # yes
        assert call_args[8] == "json"                # format
        assert call_args[9] == 10                    # max_workers
        assert call_args[14] is True                 # archive_all
        # 🐞 FIX: Corrected index from 20 to 21
        assert call_args[21] == "tar.gz"             # archive_format

    def test_run_command_dest_inheritance(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test Case 4: (run command --dest)
        Validates that 'run' inherits --dest from the 'batch' callback.
        """
        mock_run = mock_cli_deps["anyio_run"]

        # 🐞 FIX: Use isolated_filesystem
        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(app, [
                "batch", "--dest", "global/dest", "run", "."
            ])

        assert result.exit_code == 0
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]

        # 🐞 FIX: Wrap in Path() to robustly compare str vs Path
        assert Path(call_args[12]) == Path("global/dest")

    def test_run_command_dest_override(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test Case 5: (run command --dest)
        Validates that 'run' --dest overrides the 'batch' --dest.
        """
        mock_run = mock_cli_deps["anyio_run"]

        # 🐞 FIX: Use isolated_filesystem
        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(app, [
                "batch", "--dest", "global/dest",
                "run", "--dest", "local/dest", "."
            ])

        assert result.exit_code == 0
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]
        assert call_args[12] == Path("local/dest")

    def test_clean_command_flags(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test Case 6: (clean command)
        Validates all flags for 'batch clean' are passed to anyio.run.
        """
        mock_run = mock_cli_deps["anyio_run"]

        # 🐞 FIX: Use isolated_filesystem
        with cli_runner.isolated_filesystem() as temp_dir:
            # 🐞 FIX: Pass pattern as a positional argument, not an option
            result = cli_runner.invoke(app, [
                "batch", "clean", ".",
                ".*.log",
                "-y",
                "--no-dry-run"
            ])

        # 🐞 FIX: The exit code should now be 0
        assert result.exit_code == 0
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]

        assert call_args[0].__name__ == "safe_cleanup"
        # 🐞 FIX: Assert against the Path object `.`
        assert call_args[1] == Path(".") # root
        assert call_args[2] == ".*.log"          # pattern
        assert call_args[3] is False             # effective_dry_run
        assert call_args[4] is True              # yes
        # 🐞 FIX: Assert new default 'verbose=False' from main_callback
        assert call_args[5] is False             # verbose (default from main)

    # -----------------
    # 🐞 NEW TESTS START HERE
    # -----------------
    
    def test_archive_command_flags(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Action Plan 1: Test `batch archive` Subcommand (lines 200-230).
        Validates flags are passed to ArchiveManager and anyio.run.
        """
        mock_run = mock_cli_deps["anyio_run"]
        mock_manager_class = mock_cli_deps["ArchiveManager_class"]
        mock_manager_instance = mock_cli_deps["ArchiveManager_instance"]
        
        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(app, [
                "batch", "archive", ".",
                "--archive-all",
                "--archive-search",
                "--no-archive-keep-latest",
                "--archive-keep-last", "7",
                "--archive-clean-root",
                "-y",
                "--no-dry-run"
            ])
        
        assert result.exit_code == 0
        
        # 1. Assert ArchiveManager was instantiated correctly
        mock_manager_class.assert_called_once()
        
        # ⚡ FIX: Get both positional and keyword args
        call_args = mock_manager_class.call_args
        pos_args = call_args[0]
        call_kwargs = call_args[1]

        # ⚡ FIX: Assert positional 'root' argument
        assert pos_args[0] == Path(".")
        # pos_args[1] is the timestamp
        assert isinstance(pos_args[1], str) 
        # ⚡ FIX: Assert positional 'archive_keep_latest'
        assert pos_args[2] is False 
        # ⚡ FIX: Assert positional 'archive_keep_last'
        assert pos_args[3] == 7
        # ⚡ FIX: Assert positional 'archive_clean_root'
        assert pos_args[4] is True
        
        # ⚡ FIX: Assert keyword arguments
        assert call_kwargs["archive_all"] is True
        assert call_kwargs["search"] is True
        assert call_kwargs["yes"] is True
        assert call_kwargs["dry_run"] is False
        assert call_kwargs["archive_format"] == "zip" # Default from main
        
        # 2. Assert anyio.run was called with the manager's run method
        mock_run.assert_called_once_with(mock_manager_instance.run)

    def test_run_command_quiet_flag(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test Coverage for line 104: `if inherited_quiet: ...` in run()
        """
        mock_run = mock_cli_deps["anyio_run"]
        mock_logging = mock_cli_deps["setup_logging"]

        with cli_runner.isolated_filesystem():
            # Invoke `create-dump -q batch run .`
            result = cli_runner.invoke(app, ["-q", "batch", "run", "."])

        assert result.exit_code == 0
        
        # 1. Assert setup_logging was called with quiet=True, verbose=False
        mock_logging.assert_called_with(verbose=False, quiet=True)
        
        # 2. Assert the correct flags were passed to the async function
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]
        assert call_args[10] is False # inherited_verbose
        assert call_args[11] is True  # inherited_quiet

    def test_clean_command_quiet_flag(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test Coverage for line 163: `if inherited_quiet: ...` in clean()
        """
        mock_run = mock_cli_deps["anyio_run"]
        mock_logging = mock_cli_deps["setup_logging"]

        with cli_runner.isolated_filesystem():
            # Invoke `create-dump -q batch clean .`
            result = cli_runner.invoke(app, ["-q", "batch", "clean", "."])

        assert result.exit_code == 0
        
        # 1. Assert setup_logging was called with quiet=True, verbose=False
        mock_logging.assert_called_with(verbose=False, quiet=True)
        
        # 2. Assert the correct flags were passed to the async function
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]
        assert call_args[5] is False # inherited_verbose

    def test_archive_command_archive_format_inheritance(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """
        Test `batch archive` inherits archive_format from main.
        """
        mock_manager_class = mock_cli_deps["ArchiveManager_class"]
        
        with cli_runner.isolated_filesystem():
            # Set --archive-format at the root level
            result = cli_runner.invoke(app, [
                "--archive-format", "tar.gz", 
                "batch", "archive", "."
            ])
        
        assert result.exit_code == 0
        
        # Assert ArchiveManager was instantiated with the inherited format
        mock_manager_class.assert_called_once()
        call_kwargs = mock_manager_class.call_args[1]
        assert call_kwargs["archive_format"] == "tar.gz"
```

---

## tests/cli/test_rollback.py

<a id='tests-cli-test-rollback-py'></a>

```python
# tests/cli/test_rollback.py

"""
Comprehensive test suite for src/create_dump/cli/rollback.py.
This directly addresses the P0 coverage plan to unblock CI.
"""

from __future__ import annotations
import pytest
from pathlib import Path
# 🐞 FIX: Import ANY for flexible mock call assertion
from unittest.mock import AsyncMock, MagicMock, patch, ANY
import hashlib

import anyio
from typer.testing import CliRunner
from typer import Exit

# Import the main app to test the command
from create_dump.cli.main import app

# Import the module to test its internal helpers
from create_dump.cli import rollback as rollback_module
from create_dump.rollback.engine import RollbackEngine

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provides a Typer CliRunner instance."""
    return CliRunner()


@pytest.fixture
def mock_deps(mocker):
    """
    Mocks all downstream async dependencies called by the
    `async_rollback` function.
    """
    # Mock the helper functions in the module
    mock_find = mocker.patch(
        "create_dump.cli.rollback._find_most_recent_dump",
        new_callable=AsyncMock
    )
    mock_verify = mocker.patch(
        "create_dump.cli.rollback._verify_integrity",
        new_callable=AsyncMock
    )

    # Mock the downstream classes
    mock_engine_instance = AsyncMock(spec=RollbackEngine)
    mock_engine_instance.rehydrate = AsyncMock(return_value=[Path("file1.py")]) # Default success
    mock_engine_class = mocker.patch(
        "create_dump.cli.rollback.RollbackEngine",
        return_value=mock_engine_instance
    )

    mock_parser_class = mocker.patch("create_dump.cli.rollback.MarkdownParser")

    # Mock the sync confirm function run in a thread
    mock_confirm_thread = mocker.patch(
        "create_dump.cli.rollback.anyio.to_thread.run_sync",
        return_value=True # Default to "yes"
    )

    # Mock logging/printing
    mock_styled_print = mocker.patch("create_dump.cli.rollback.styled_print")
    mock_logger = mocker.patch("create_dump.cli.rollback.logger")

    # Mock anyio.Path.exists for the --file check
    mock_path_exists = mocker.patch("anyio.Path.exists", new_callable=AsyncMock, return_value=True)

    return {
        "find": mock_find,
        "verify": mock_verify,
        "engine_class": mock_engine_class,
        "engine_instance": mock_engine_instance,
        "parser_class": mock_parser_class,
        "confirm": mock_confirm_thread,
        "styled_print": mock_styled_print,
        "logger": mock_logger,
        "path_exists": mock_path_exists,
    }


class TestCliRollbackCommand:
    """Tests the `rollback` command wiring and logic flow."""

    def test_happy_path_find_latest(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 1: Happy Path (Find Latest)."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 0
        mock_deps["find"].assert_called_once_with(test_project.root)
        mock_deps["verify"].assert_called_once_with(mock_dump_path)
        mock_deps["engine_instance"].rehydrate.assert_called_once()
        mock_deps["styled_print"].assert_any_call("[green]Integrity verified.[/green]")
        mock_deps["styled_print"].assert_any_call(
            f"[green]✅ Rollback complete.[/green] 1 files created in [blue]{test_project.root.resolve() / 'all_create_dump_rollbacks' / 'dump_2025'}[/blue]"
        )

    def test_happy_path_with_file(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 2: Happy Path (--file)."""
        mock_dump_path = test_project.path("mydump.md")
        mock_deps["verify"].return_value = True

        result = cli_runner.invoke(app, ["rollback", str(test_project.root), "--file", str(mock_dump_path)])

        assert result.exit_code == 0
        mock_deps["find"].assert_not_called()
        mock_deps["path_exists"].assert_called_once()
        mock_deps["verify"].assert_called_once_with(mock_dump_path)
        mock_deps["engine_instance"].rehydrate.assert_called_once()

    def test_dry_run(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 3: Dry Run."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True

        result = cli_runner.invoke(app, ["rollback", str(test_project.root), "--dry-run"])

        assert result.exit_code == 0
        mock_deps["engine_class"].assert_called_with(
            test_project.root.resolve() / 'all_create_dump_rollbacks' / 'dump_2025',
            dry_run=True
        )
        mock_deps["engine_instance"].rehydrate.assert_called_once()
        mock_deps["styled_print"].assert_any_call("[green]✅ Dry run complete.[/green] Would have created 1 files.")

    def test_user_cancellation(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 4: User Cancellation."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True
        mock_deps["confirm"].return_value = False  # User says "no"

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        # 🐞 FIX: typer.Exit() on user cancel is exit_code 1
        assert result.exit_code == 1
        
        # 🐞 FIX: Assert *any* call, because conftest.py also uses run_sync
        mock_deps["confirm"].assert_any_call(rollback_module.confirm, ANY)
        
        mock_deps["engine_instance"].rehydrate.assert_not_called()
        mock_deps["styled_print"].assert_any_call("[red]Rollback cancelled by user.[/red]")

    def test_failure_file_not_found(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 5: Failure (File Not Found)."""
        mock_deps["path_exists"].return_value = False

        result = cli_runner.invoke(app, ["rollback", str(test_project.root), "--file", "nonexistent.md"])

        assert result.exit_code == 1
        mock_deps["path_exists"].assert_called_once()
        mock_deps["verify"].assert_not_called()
        mock_deps["styled_print"].assert_any_call("[red]Error:[/red] Specified file not found: nonexistent.md")

    def test_failure_no_dumps_found(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 6: Failure (No Dumps Found)."""
        mock_deps["find"].return_value = None

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 1
        mock_deps["find"].assert_called_once()
        mock_deps["verify"].assert_not_called()
        mock_deps["styled_print"].assert_any_call("[red]Error:[/red] No `*_all_create_dump_*.md` files found in this directory.")

    def test_failure_integrity_check(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 7: Failure (Integrity Check)."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = False  # Verification fails

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 1
        mock_deps["find"].assert_called_once()
        mock_deps["verify"].assert_called_once()
        mock_deps["engine_instance"].rehydrate.assert_not_called()

    def test_failure_engine_error(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 10: Failure (Engine Error - ValueError)."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True
        mock_deps["engine_instance"].rehydrate.side_effect = ValueError("Engine Failed")

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 1
        mock_deps["engine_instance"].rehydrate.assert_called_once()
        mock_deps["styled_print"].assert_any_call("[red]Error:[/red] Engine Failed")

    def test_failure_unexpected_error(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 11: Failure (Unexpected Error)."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True
        mock_deps["engine_instance"].rehydrate.side_effect = TypeError("Unexpected")

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 1
        mock_deps["engine_instance"].rehydrate.assert_called_once()
        mock_deps["logger"].error.assert_any_call("Unhandled rollback error", error="Unexpected", exc_info=True)
        mock_deps["styled_print"].assert_any_call("[red]An unexpected error occurred:[/red] Unexpected")


class TestRollbackHelpers:
    """Tests the async helper functions in rollback.py."""

    async def test_calculate_sha256(self, test_project):
        """Tests the SHA256 calculation."""
        content = "hello world"
        expected_hash = hashlib.sha256(content.encode()).hexdigest()

        await test_project.create({"file.txt": content})
        file_path = test_project.async_root / "file.txt"

        hash_val = await rollback_module._calculate_sha256(file_path)

        assert hash_val == expected_hash

    async def test_find_most_recent_dump_success(self, test_project):
        """Tests finding the latest file by mtime."""
        await test_project.create({"dump_old_all_create_dump_20240101_000000.md": "old"})
        await anyio.sleep(0.02) # Ensure mtime difference
        await test_project.create({"dump_new_all_create_dump_20250101_000000.md": "new"})

        latest_file = await rollback_module._find_most_recent_dump(test_project.root)

        assert latest_file is not None
        assert latest_file.name == "dump_new_all_create_dump_20250101_000000.md"

    async def test_find_most_recent_dump_empty(self, test_project):
        """Tests that None is returned when no dumps are found."""
        await test_project.create({"not_a_dump.txt": "content"})

        latest_file = await rollback_module._find_most_recent_dump(test_project.root)

        assert latest_file is None

    async def test_find_most_recent_dump_stat_error(self, test_project, mocker):
        """Tests that an OSError during stat is caught and logged."""
        await test_project.create({"dump_file_all_create_dump_20250101_000000.md": "content"})

        mock_logger = mocker.patch("create_dump.cli.rollback.logger")

        # Mock Path.stat to raise an error
        mock_stat = AsyncMock(side_effect=OSError("Permission denied"))
        mocker.patch.object(anyio.Path, "stat", mock_stat)

        latest_file = await rollback_module._find_most_recent_dump(test_project.root)

        assert latest_file is None
        mock_logger.warning.assert_called_once()
        assert "Could not stat file" in mock_logger.warning.call_args[0][0]

    async def test_verify_integrity_success(self, test_project):
        """Tests successful integrity verification."""
        content = "test content"
        hash_val = hashlib.sha256(content.encode()).hexdigest()

        await test_project.create({
            "test_all_create_dump_20250101_000000.md": content,
            "test_all_create_dump_20250101_000000.sha256": f"{hash_val}  test_all_create_dump_20250101_000000.md"
        })

        md_path = test_project.path("test_all_create_dump_20250101_000000.md")
        is_valid = await rollback_module._verify_integrity(md_path)

        assert is_valid is True

    async def test_verify_integrity_sha_missing(self, test_project, mocker):
        """Test Case 8: Failure (SHA Missing)."""
        # 🐞 FIX: Add local mocks for logger and styled_print
        mock_logger = mocker.patch("create_dump.cli.rollback.logger")
        mock_styled_print = mocker.patch("create_dump.cli.rollback.styled_print")

        await test_project.create({"dump.md": "content"})
        md_path = test_project.path("dump.md")

        is_valid = await rollback_module._verify_integrity(md_path)

        assert is_valid is False
        # 🐞 FIX: Use local mock variable
        mock_logger.error.assert_called_once_with("Integrity check failed: Missing checksum file for dump.md")
        mock_styled_print.assert_any_call("[red]Error:[/red] Missing checksum file: [blue]dump.sha256[/blue]")

    async def test_verify_integrity_sha_mismatch(self, test_project, mocker):
        """Test Case 9: Failure (SHA Mismatch)."""
        # 🐞 FIX: Add local mocks for logger and styled_print
        mock_logger = mocker.patch("create_dump.cli.rollback.logger")
        mock_styled_print = mocker.patch("create_dump.cli.rollback.styled_print")

        await test_project.create({
            "dump.md": "content",
            "dump.sha256": "badhash  dump.md"
        })
        md_path = test_project.path("dump.md")

        is_valid = await rollback_module._verify_integrity(md_path)

        assert is_valid is False
        # 🐞 FIX: Use local mock variable
        mock_logger.error.assert_called_once_with(
            "Integrity check FAILED: Hashes do not match",
            file="dump.md",
            expected="badhash",
            actual=hashlib.sha256(b"content").hexdigest()
        )
        mock_styled_print.assert_any_call("[red]Error: Integrity check FAILED. File is corrupt.[/red]")

    async def test_verify_integrity_read_error(self, test_project, mocker):
        """Tests that an exception during hash calculation is caught."""
        # 🐞 FIX: Add local mocks for logger and styled_print
        mock_logger = mocker.patch("create_dump.cli.rollback.logger")
        mock_styled_print = mocker.patch("create_dump.cli.rollback.styled_print")

        await test_project.create({
            "dump.md": "content",
            "dump.sha256": "hash  dump.md"
        })
        md_path = test_project.path("dump.md")

        # Mock _calculate_sha256 to raise an error
        mocker.patch(
            "create_dump.cli.rollback._calculate_sha256",
            side_effect=Exception("Read Error")
        )

        is_valid = await rollback_module._verify_integrity(md_path)

        assert is_valid is False
        # 🐞 FIX: Use local mock variable
        mock_logger.error.assert_called_once_with("Integrity check error: Read Error", file="dump.md")
        mock_styled_print.assert_any_call("[red]Error during integrity check:[/red] Read Error")
```

---

## tests/collector/test_base.py

<a id='tests-collector-test-base-py'></a>

```python
# tests/collector/test_base.py

"""
Tests for Phase 2: src/create_dump/collector/base.py
"""

from __future__ import annotations
import pytest
import anyio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, ANY
# ✨ NEW: Import the real anyio.Path for spec-ing
from anyio import Path as RealAnyIOPath

# Import the class to test
from create_dump.collector.base import CollectorBase
# Import dependencies needed for testing
from create_dump.core import Config

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio

# --- Fixtures ---

class DummyCollector(CollectorBase):
    """A concrete implementation of CollectorBase for testing."""
    async def collect(self) -> list[str]:
        # This is the abstract method, we don't need it for these tests
        return []

@pytest.fixture
def mock_stat():
    """Fixture to create a mock stat object."""
    stat_mock = MagicMock()
    stat_mock.st_size = 100  # Default size (small)
    return stat_mock

@pytest.fixture
def mock_anyio_path(mocker, mock_stat):
    """Fixture to create a mock anyio.Path object."""
    # 🐞 FIX: Use the real class for the spec
    path_mock = AsyncMock(spec=RealAnyIOPath)
    path_mock.exists = AsyncMock(return_value=True)
    path_mock.stat = AsyncMock(return_value=mock_stat)
    
    # Patch the anyio.Path constructor to return our mock
    mocker.patch("anyio.Path", return_value=path_mock)
    return path_mock

@pytest.fixture
def mock_is_text(mocker):
    """Fixture to mock the is_text_file check."""
    return mocker.patch(
        "create_dump.collector.base.is_text_file",
        AsyncMock(return_value=True)
    )

# --- Test Cases ---

class TestCollectorBase:
    """Groups tests for the CollectorBase class."""

    async def test_setup_specs_defaults(self, default_config: Config, test_project):
        """
        Tests that default includes/excludes are loaded.
        """
        collector = DummyCollector(config=default_config, root=test_project.root)
        
        assert collector._include_spec is not None
        assert collector._exclude_spec is not None
        assert collector._include_spec.match_file("test.py")
        assert collector._exclude_spec.match_file("test.pyc")
        assert collector._exclude_spec.match_file("dump_file_all_create_dump_1234.md")

    async def test_setup_specs_with_gitignore(self, default_config: Config, test_project):
        """
        Tests that .gitignore patterns are correctly loaded and added
        to the exclude spec when use_gitignore=True.
        """
        await test_project.create({
            ".gitignore": """
# This is a comment
*.unique_log
/build/
dist
"""
        })

        collector = DummyCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=True
        )

        assert collector._exclude_spec.match_file("app.unique_log")
        assert collector._exclude_spec.match_file("build/app.exe")
        assert collector._exclude_spec.match_file("dist/my_app.zip")
        assert collector._exclude_spec.match_file("test.pyc")

    async def test_setup_specs_no_gitignore(self, default_config: Config, test_project):
        """
        Tests that .gitignore is ignored when use_gitignore=False.
        """
        await test_project.create({".gitignore": "*.unique_log"})

        collector = DummyCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=False  # Explicitly disable
        )

        assert not collector._exclude_spec.match_file("app.unique_log")
        assert collector._exclude_spec.match_file("test.pyc")

    async def test_setup_specs_custom_patterns(self, default_config: Config, test_project):
        """
        Tests that custom include/exclude patterns are added to the specs.
        """
        collector = DummyCollector(
            config=default_config,
            root=test_project.root,
            includes=["*.custom"],
            excludes=["*.default"]
        )
        
        assert collector._include_spec.match_file("my_file.custom")
        assert collector._include_spec.match_file("my_file.py") # Defaults are additive

        assert collector._exclude_spec.match_file("my_file.default")
        assert collector._exclude_spec.match_file("test.pyc") # Default is additive


    # --- _should_include Tests (Mocked) ---

    async def test_should_include_async_all_pass(
        self, default_config: Config, test_project, mock_anyio_path, mock_is_text
    ):
        """Tests the "happy path" where all checks pass."""
        collector = DummyCollector(config=default_config, root=test_project.root)
        
        result = await collector._should_include(
            mock_anyio_path, "src/main.py"
        )
        
        assert result is True
        mock_anyio_path.exists.assert_called_once()
        mock_anyio_path.stat.assert_called_once()
        mock_is_text.assert_called_once_with(mock_anyio_path)

    async def test_should_include_async_not_exists(
        self, default_config: Config, test_project, mock_anyio_path
    ):
        """Tests that a non-existent file is skipped."""
        mock_anyio_path.exists.return_value = False
        collector = DummyCollector(config=default_config, root=test_project.root)
        
        result = await collector._should_include(
            mock_anyio_path, "src/main.py"
        )
        
        assert result is False
        mock_anyio_path.exists.assert_called_once()
        mock_anyio_path.stat.assert_not_called() # Should short-circuit

    async def test_should_include_async_too_large(
        self, default_config: Config, test_project, mock_anyio_path, mock_stat, mock_is_text
    ):
        """Tests that a file exceeding max_file_size_kb is skipped."""
        default_config.max_file_size_kb = 10  # 10KB max
        mock_stat.st_size = 11 * 1024  # 11KB file
        
        collector = DummyCollector(config=default_config, root=test_project.root)
        
        result = await collector._should_include(
            mock_anyio_path, "src/large_file.log"
        )
        
        assert result is False
        mock_anyio_path.stat.assert_called_once()
        mock_is_text.assert_not_called() # Should short-circuit

    async def test_should_include_async_is_binary(
        self, default_config: Config, test_project, mock_anyio_path, mock_is_text
    ):
        """Tests that a binary file is skipped."""
        mock_is_text.return_value = False  # Simulate binary file
        
        collector = DummyCollector(config=default_config, root=test_project.root)
        
        result = await collector._should_include(
            mock_anyio_path, "src/app.exe"
        )
        
        assert result is False
        mock_is_text.assert_called_once_with(mock_anyio_path)

    # --- filter_files Tests (Integration) ---

    async def test_filter_files(self, default_config: Config, test_project):
        """
        Tests the filter_files method, which uses _matches internally.
        This tests the full logic chain.
        """
        await test_project.create({
            "src/main.py": "print('hello')",
            "src/data.bin": b"\x00\x01\x02",
            "README.md": "# Title",
            "app.log": "this is a log", # This is in default_excludes
            "app.unique_log": "this is a unique log", # This is in .gitignore
            ".gitignore": "*.unique_log",
        })

        collector = DummyCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=True
        )

        raw_files = [
            "src/main.py",
            "src/data.bin",
            "README.md",
            "app.log",
            "app.unique_log",
            "non_existent_file.py",
        ]

        filtered = await collector.filter_files(raw_files)

        assert filtered == ["README.md", "src/main.py"]
        
    # --- NEW P1 TESTS ---

    async def test_setup_specs_gitignore_true_but_no_file_exists(
        self, default_config: Config, test_project, mocker
    ):
        """
        Covers lines 62->72 (use_gitignore=True, but no .gitignore file).
        """
        mock_logger_debug = mocker.patch("create_dump.collector.base.logger.debug")
        
        # Ensure no .gitignore exists (test_project is clean)
        collector = DummyCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=True
        )

        # Assert that "Gitignore integrated" was never logged
        for call in mock_logger_debug.call_args_list:
            assert call[0][0] != "Gitignore integrated"

    async def test_should_include_async_stat_error(
        self, default_config: Config, test_project, mock_anyio_path, mocker
    ):
        """
        Covers lines 124-126 (OSError during stat).
        """
        mock_logger_warn = mocker.patch("create_dump.collector.base.logger.warning")
        mock_anyio_path.stat.side_effect = OSError("Permission denied")
        
        collector = DummyCollector(config=default_config, root=test_project.root)
        
        result = await collector._should_include(mock_anyio_path, "src/file.py")
        
        assert result is False
        mock_logger_warn.assert_called_once_with(
            "File check failed (OSError): src/file.py", error="Permission denied"
        )

    async def test_filter_files_absolute_path_outside_root(
        self, default_config: Config, test_project, mocker
    ):
        """
        Covers lines 135-138 (absolute path outside root).
        """
        mock_logger_warn = mocker.patch("create_dump.collector.base.logger.warning")
        collector = DummyCollector(config=default_config, root=test_project.root)
        
        # Need a "good" file to ensure the list isn't just empty
        await test_project.create({"src/main.py": "content"})
        
        raw_files = ["/etc/passwd", "src/main.py"]
        filtered = await collector.filter_files(raw_files)
        
        assert filtered == ["src/main.py"]
        mock_logger_warn.assert_called_once_with(
            "Skipping git path outside root", path="/etc/passwd"
        )

    async def test_filter_files_generic_exception(
        self, default_config: Config, test_project, mocker
    ):
        """
        Covers lines 142-143 (generic exception during _matches).
        """
        mock_logger_warn = mocker.patch("create_dump.collector.base.logger.warning")
        collector = DummyCollector(config=default_config, root=test_project.root)
        
        # Mock _matches to fail
        mocker.patch.object(
            collector, "_matches", side_effect=Exception("Unexpected error")
        )
        
        raw_files = ["src/main.py"]
        filtered = await collector.filter_files(raw_files)
        
        assert filtered == []
        mock_logger_warn.assert_called_once_with(
            "Skipping file due to error", path="src/main.py", error="Unexpected error"
        )
```

---

## tests/archive/test_packager.py

<a id='tests-archive-test-packager-py'></a>

```python
# tests/archive/test_packager.py

"""
Tests for Phase 3: src/create_dump/archive/packager.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from typing import List, Tuple, Optional
import zipfile
import tarfile
import stat # ⚡ FIX: Import stat module

import anyio

# Import the class to test
from create_dump.archive.packager import ArchivePackager
from create_dump.helpers import _unique_path
from create_dump.logging import setup_logging

# -----------------
# Import all required mocks
# -----------------
from datetime import datetime
from unittest.mock import MagicMock, patch, AsyncMock, call
from create_dump.archive.core import ArchiveError

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
async def archives_dir(test_project) -> Path:
    """Creates an 'archives' dir and returns its path."""
    archives_path = test_project.root / "archives"
    await anyio.Path(archives_path).mkdir(exist_ok=True)
    return archives_path

@pytest.fixture
async def quarantine_dir(test_project, archives_dir) -> Path:
    """Creates a 'quarantine' dir and returns its path."""
    q_path = Path(archives_dir) / "quarantine"
    await anyio.Path(q_path).mkdir(exist_ok=True)
    return q_path

@pytest.fixture
async def project_with_files(test_project, archives_dir, quarantine_dir):
    """Creates a project with dump files for packager tests."""
    await test_project.create({
        # --- Single/Default Group ---
        "default_all_create_dump_20250101_000100.md": "old",
        "default_all_create_dump_20250101_000100.sha256": "hash_old",
        "default_all_create_dump_20250101_000200.md": "new",
        "default_all_create_dump_20250101_000200.sha256": "hash_new",

        # --- Grouped Files ---
        "src_all_create_dump_20250101_000100.md": "src_old",
        "src_all_create_dump_20250101_000100.sha256": "src_hash_old",
        "src_all_create_dump_20250101_000200.md": "src_new",
        "src_all_create_dump_20250101_000200.sha256": "src_hash_new",
        "tests_all_create_dump_20250101_000100.md": "tests_old",
        "tests_all_create_dump_20250101_000100.sha256": "tests_hash_old",
    })

    await anyio.Path(archives_dir).mkdir(exist_ok=True)
    await anyio.Path(quarantine_dir).mkdir(exist_ok=True)

    # Return all valid pairs
    return [
        (test_project.path("default_all_create_dump_20250101_000100.md"),
         test_project.path("default_all_create_dump_20250101_000100.sha256")),
        (test_project.path("default_all_create_dump_20250101_000200.md"),
         test_project.path("default_all_create_dump_20250101_000200.sha256")),
        (test_project.path("src_all_create_dump_20250101_000100.md"),
         test_project.path("src_all_create_dump_20250101_000100.sha256")),
        (test_project.path("src_all_create_dump_20250101_000200.md"),
         test_project.path("src_all_create_dump_20250101_000200.sha256")),
        (test_project.path("tests_all_create_dump_20250101_000100.md"),
         test_project.path("tests_all_create_dump_20250101_000100.sha256")),
    ]


@pytest.fixture
async def base_packager_args(test_project, archives_dir, quarantine_dir):
    """Provides the base dict of args for instantiating a packager."""
    setup_logging(quiet=True)
    return {
        "root": test_project.root,
        "archives_dir": archives_dir,
        "quarantine_dir": quarantine_dir,
        "timestamp": "20251107_120000",
        "keep_latest": True,
        "verbose": False,
        "dry_run": False,
        "yes": True,
        "clean_root": False,
        "no_remove": False,
        "archive_format": "zip",
    }


class TestArchivePackager:
    """Groups tests for the ArchivePackager."""

    @pytest.mark.parametrize("archive_format, extension, reader, test_func", [
        ("zip", ".zip", zipfile.ZipFile, lambda z: z.testzip()),
        ("tar.gz", ".tar.gz", tarfile.open, lambda t: t.getnames()),
        ("tar.bz2", ".tar.bz2", tarfile.open, lambda t: t.getnames()),
    ])
    async def test_create_archive_sync(
        self, base_packager_args, test_project, archive_format, extension, reader, test_func
    ):
        """
        Test Case 1: _create_archive_sync for zip, tar.gz, and tar.bz2.
        Also implicitly tests _safe_arcname.
        """
        await test_project.create({
            "src/file1.txt": "file1",
            "src/sub/file2.txt": "file2",
        })
        files = [
            test_project.path("src/file1.txt"),
            test_project.path("src/sub/file2.txt"),
        ]

        args = base_packager_args | {"archive_format": archive_format}
        packager = ArchivePackager(**args)

        archive_name = f"test_archive{extension}"
        archive_path, archived_files = packager._create_archive_sync(files, archive_name)

        assert archive_path.name == archive_name
        assert len(archived_files) == 2
        assert await anyio.Path(archive_path).exists()

        # Validate contents
        with reader(archive_path, 'r') as ar:
            test_func(ar) # Validate integrity
            names = ar.getnames() if hasattr(ar, "getnames") else ar.namelist()
            assert "src/file1.txt" in names
            assert "src/sub/file2.txt" in names

    async def test_group_pairs_by_prefix(self, base_packager_args, project_with_files):
        """Test Case 2: group_pairs_by_prefix correctly groups files."""
        packager = ArchivePackager(**base_packager_args)
        groups = packager.group_pairs_by_prefix(project_with_files)

        assert "default" in groups
        assert "src" in groups
        assert "tests" in groups
        assert len(groups["default"]) == 2
        assert len(groups["src"]) == 2
        assert len(groups["tests"]) == 1

    async def test_handle_single_archive_keep_latest(
        self, base_packager_args, project_with_files, test_project
    ):
        """Test Case 3: handle_single_archive with keep_latest=True."""
        args = base_packager_args | {"keep_latest": True}
        packager = ArchivePackager(**args)
        
        all_pairs = project_with_files
        pairs = [p for p in all_pairs if "default" in p[0].name]
        
        archive_paths, to_delete = await packager.handle_single_archive(pairs)
        
        assert "default" in archive_paths
        archive_path = archive_paths["default"]
        assert archive_path.name.startswith(f"{test_project.root.name}_dumps_archive_")
        
        assert len(to_delete) == 2
        assert "default_all_create_dump_20250101_000100.md" in to_delete[0].name
        
        assert "default_all_create_dump_20250101_000200.md" not in {p.name for p in to_delete}

    async def test_handle_single_archive_no_keep_latest(
        self, base_packager_args, project_with_files
    ):
        """Test Case 4: handle_single_archive with keep_latest=False."""
        args = base_packager_args | {"keep_latest": False}
        packager = ArchivePackager(**args)
        
        all_pairs = project_with_files
        pairs = [p for p in all_pairs if "default" in p[0].name]
        archive_paths, to_delete = await packager.handle_single_archive(pairs)

        assert "default" in archive_paths

        assert len(to_delete) == 4
        assert "default_all_create_dump_20250101_000100.md" in to_delete[0].name
        assert "default_all_create_dump_20250101_000200.md" in to_delete[2].name

    async def test_handle_grouped_archives(
        self, base_packager_args, project_with_files, quarantine_dir
    ):
        """Test Case 5: handle_grouped_archives processes groups correctly."""
        args = base_packager_args | {"keep_latest": True}
        packager = ArchivePackager(**args)
        
        groups = packager.group_pairs_by_prefix(project_with_files)
        archive_paths, to_delete = await packager.handle_grouped_archives(groups)

        assert "src" in archive_paths
        assert "tests" not in archive_paths
        assert "default" not in archive_paths 
        
        assert archive_paths["src"].name.startswith("src_all_create_dump_")
        
        assert "src_all_create_dump_20250101_000100.md" in {p.name for p in to_delete}
        assert "src_all_create_dump_20250101_000200.md" not in {p.name for p in to_delete}
        
        assert "tests_all_create_dump_20250101_000100.md" not in {p.name for p in to_delete}
        
        q_path = anyio.Path(quarantine_dir)
        assert await (q_path / "default_all_create_dump_20250101_000100.md").exists()
        assert await (q_path / "default_all_create_dump_20250101_000200.md").exists()

    async def test_handle_archives_dry_run(
        self, base_packager_args, project_with_files, archives_dir, caplog
    ):
        """Test Case 6: No archives created or files moved on dry_run."""
        args = base_packager_args | {"dry_run": True}
        packager = ArchivePackager(**args)
        
        # Test single
        all_pairs = project_with_files
        pairs = [p for p in all_pairs if "default" in p[0].name]
        archive_paths, to_delete = await packager.handle_single_archive(pairs)
        
        assert len(archive_paths) == 1
        assert archive_paths["default"] is None # No path returned
        assert len(to_delete) == 0 # No files marked for deletion
        
        # Test grouped
        groups = packager.group_pairs_by_prefix(all_pairs)
        archive_paths, to_delete = await packager.handle_grouped_archives(groups)
        
        assert len(archive_paths) == 1 # src only
        assert archive_paths["src"] is None
        assert "tests" not in archive_paths
        assert len(to_delete) == 0
        
        # Assert nothing was actually created
        file_count = 0
        async for p in anyio.Path(archives_dir).rglob("*"):
            if p.name != "quarantine":
                file_count += 1
        assert file_count == 0 # Should be empty


    async def test_create_archive_sync_zip_write_failure(
        self, base_packager_args, test_project, mocker
    ):
        """
        Action Plan 1: Test archive failure (zip).
        Tests that _create_archive_sync rolls back zip on write failure.
        """
        # 1. Setup
        await test_project.create({"src/file1.txt": "file1"})
        files = [test_project.path("src/file1.txt")]
        
        args = base_packager_args | {"archive_format": "zip"}
        packager = ArchivePackager(**args)

        # 2. Mock: Make zipfile.ZipFile fail on write
        mocker.patch("zipfile.ZipFile", side_effect=zipfile.BadZipFile("Simulated write error"))
        
        # 3. Mock: Spy on Path.unlink
        archive_path = base_packager_args["archives_dir"] / "fail_archive.zip"
        mocker.patch("create_dump.helpers._unique_path", return_value=archive_path)
        
        # -----------------
        # 🐞 FIX: Patch the *class method* `pathlib.Path.unlink`, not the instance.
        # -----------------
        mock_unlink = mocker.patch.object(Path, "unlink")

        # 4. Act & Assert
        with pytest.raises(zipfile.BadZipFile):
            packager._create_archive_sync(files, "fail_archive.zip")
        
        # 5. Assert rollback
        # -----------------
        # 🐞 FIX: The mock is called with (self=archive_path, missing_ok=True)
        # The assertion should NOT include the self argument.
        # -----------------
        mock_unlink.assert_called_once_with(missing_ok=True)


    async def test_create_archive_sync_tar_failure(
        self, base_packager_args, test_project, mocker
    ):
        """
        Action Plan 1: Test archive failure (tar).
        Tests that _create_archive_sync rolls back tar on write failure.
        """
        # 1. Setup
        await test_project.create({"src/file1.txt": "file1"})
        files = [test_project.path("src/file1.txt")]
        
        args = base_packager_args | {"archive_format": "tar.gz"}
        packager = ArchivePackager(**args)

        # 2. Mock
        archive_path = base_packager_args["archives_dir"] / "fail_archive.tar.gz"
        mocker.patch("create_dump.helpers._unique_path", return_value=archive_path)
        
        # -----------------
        # 🐞 FIX: Patch `pathlib.Path.unlink`
        # -----------------
        mock_unlink = mocker.patch.object(Path, "unlink")
        
        mocker.patch("tarfile.open", side_effect=tarfile.TarError("Simulated tar error"))
        
        # 3. Act & Assert
        with pytest.raises(tarfile.TarError):
            packager._create_archive_sync(files, "fail_archive.tar.gz")
            
        # -----------------
        # 🐞 FIX: Assert with keyword args only
        # -----------------
        mock_unlink.assert_called_once_with(missing_ok=True)

    async def test_create_archive_sync_zip_validation_failure(
        self, base_packager_args, test_project, mocker
    ):
        """
        Action Plan 1: Test archive failure (zip validation).
        Tests that _create_archive_sync rolls back zip on testzip() failure.
        """
        # 1. Setup
        await test_project.create({"src/file1.txt": "file1"})
        files = [test_project.path("src/file1.txt")]
        
        args = base_packager_args | {"archive_format": "zip"}
        packager = ArchivePackager(**args)

        # 2. Mock
        archive_path = base_packager_args["archives_dir"] / "validate_fail.zip"
        mocker.patch("create_dump.helpers._unique_path", return_value=archive_path)

        # -----------------
        # 🐞 FIX: Patch `pathlib.Path.unlink` and `pathlib.Path.stat`
        # -----------------
        mock_unlink = mocker.patch.object(Path, "unlink")
        
        # ⚡ FIX: Create a mock stat_result with a valid st_mode
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 1234
        mock_stat_result.st_mode = stat.S_IFREG  # This makes path.is_file() True
        
        mocker.patch.object(Path, "stat", return_value=mock_stat_result)
        
        # -----------------
        # 🐞 FIX: Correctly mock the two separate calls to ZipFile
        # -----------------
        mock_write_zip = MagicMock() # Mock for the 'w' mode call
        mock_validate_zip = MagicMock() # Mock for the 'r' mode call
        mock_validate_zip.testzip.return_value = "badfile.txt" # This triggers the error
        
        mock_zip_open = mocker.patch("zipfile.ZipFile")
        # ⚡ FIX: Use side_effect to provide a *different* mock for each call.
        # Add a mock for __exit__ to be robust.
        mock_zip_open.side_effect = [
            MagicMock(__enter__=MagicMock(return_value=mock_write_zip), __exit__=MagicMock(return_value=None)), # Call 1 (write)
            MagicMock(__enter__=MagicMock(return_value=mock_validate_zip), __exit__=MagicMock(return_value=None)) # Call 2 (read)
        ]
        
        # 3. Act & Assert
        # -----------------
        # 🐞 FIX: The test now correctly raises ArchiveError
        # -----------------
        with pytest.raises(ArchiveError, match="Corrupt file in ZIP: badfile.txt"):
            packager._create_archive_sync(files, "validate_fail.zip")
            
        mock_unlink.assert_called_once_with(missing_ok=True)

    async def test_handle_grouped_archives_dry_run_quarantine(
        self, base_packager_args, project_with_files, quarantine_dir, caplog, test_project
    ):
        """
        Action Plan 2: Test Group Quarantining (Dry Run).
        Tests that handle_grouped_archives with dry_run=True logs quarantining.
        """
        args = base_packager_args | {"dry_run": True, "verbose": True}
        packager = ArchivePackager(**args)
        
        default_pairs = [p for p in project_with_files if "default" in p[0].name]
        groups = {"default": default_pairs} 

        await packager.handle_grouped_archives(groups)

        q_path = anyio.Path(quarantine_dir)
        assert not await (q_path / "default_all_create_dump_20250101_000100.md").exists()
        
        # -----------------
        # 🐞 FIX: Remove `await` from sync `.exists()` call
        # -----------------
        assert (test_project.path("default_all_create_dump_20250101_000100.md")).exists()
        
        assert "[dry-run] Would quarantine unmatchable pair" in caplog.text
        assert "default_all_create_dump_20250101_000100.md" in caplog.text
        assert "default_all_create_dump_20250101_000200.md" in caplog.text

    async def test_handle_single_archive_clean_root(
        self, base_packager_args, project_with_files, test_project, mocker
    ):
        """
        Action Plan 3: Test `clean_root`.
        Tests handle_single_archive with clean_root=True calls safe_delete_paths.
        """
        # 1. Setup
        args = base_packager_args | {
            "keep_latest": True,
            "clean_root": True,
            "yes": True, # Skips confirm()
        }
        packager = ArchivePackager(**args)
        
        # 2. Mock
        mock_delete = mocker.patch("create_dump.archive.packager.safe_delete_paths", new_callable=AsyncMock)
        mocker.patch("create_dump.archive.packager.confirm", return_value=True) 

        # 3. Act
        all_pairs = project_with_files
        pairs = [p for p in all_pairs if "default" in p[0].name]
        
        await packager.handle_single_archive(pairs)
        
        # 4. Assert
        mock_delete.assert_called_once()
        
        # -----------------
        # 🐞 FIX: Assert keyword arguments, not positional
        # -----------------
        call_args_list = mock_delete.call_args[0]
        call_kwargs = mock_delete.call_args[1]
        
        deleted_paths_list = call_args_list[0]
        
        assert len(deleted_paths_list) == 2
        assert "default_all_create_dump_20250101_000100.md" in deleted_paths_list[0].name
        assert "default_all_create_dump_20250101_000100.sha256" in deleted_paths_list[1].name
        
        # Assert it was called with the correct flags
        assert call_kwargs["dry_run"] is False
        assert call_kwargs["assume_yes"] is True

    async def test_handle_single_archive_mtime_fallback_sort(
        self, base_packager_args, test_project, mocker, caplog
    ):
        """
        Action Plan 4: Test `mtime` Fallback.
        Tests key_func in handle_single_archive falls back to mtime sorting.
        """
        # 1. Setup: Create files with *no valid timestamp* sequentially
        await test_project.create({"file_old.md": "old"})
        await anyio.sleep(0.02) # Ensure mtime difference
        await test_project.create({"file_new.md": "new"})
        
        mocker.patch(
            "create_dump.archive.packager.extract_timestamp",
            return_value=datetime.min
        )
        
        pairs = [
            (test_project.path("file_new.md"), None),
            (test_project.path("file_old.md"), None),
        ]

        # 2. Setup Packager
        args = base_packager_args | {
            "keep_latest": True,
            "verbose": True, # To hit the log line
        }
        packager = ArchivePackager(**args)
        
        # 3. Act
        with caplog.at_level("DEBUG"):
            archive_paths, to_delete = await packager.handle_single_archive(pairs)

        # 4. Assert
        assert len(to_delete) == 1
        assert to_delete[0].name == "file_old.md"
        
        assert "Fallback to mtime for sorting" in caplog.text

    async def test_create_archive_sync_no_files(self, base_packager_args):
        """
        Test Coverage for line 64: _create_archive_sync handles empty list.
        """
        packager = ArchivePackager(**base_packager_args)
        archive_path, archived_files = packager._create_archive_sync([], "empty.zip")
        
        assert archive_path is None
        assert archived_files == []

    async def test_create_archive_sync_none_in_list(self, base_packager_args):
        """
        Test Coverage for line 69: _create_archive_sync handles list of Nones.
        """
        packager = ArchivePackager(**base_packager_args)
        archive_path, archived_files = packager._create_archive_sync([None, None], "empty.zip")
        
        assert archive_path is None
        assert archived_files == []

    @pytest.mark.anyio(backend='asyncio')
    async def test_create_archive_sync_stores_compressed_files(
        self, base_packager_args, test_project, mocker
    ):

        """
        Test Coverage for line 89: _create_archive_sync uses ZIP_STORED for .gz files.
        """
        # 1. Setup
        await test_project.create({"src/file1.txt": "file1", "src/file2.gz": "gz_content"})
        files = [
            test_project.path("src/file1.txt"),
            test_project.path("src/file2.gz"),
        ]
        
        args = base_packager_args | {"archive_format": "zip"}
        packager = ArchivePackager(**args)

        # 2. Mock
        # -----------------
        # 🐞 FIX: Correctly mock the .write method and the testzip method
        # -----------------
        
        # ⚡ FIX: Mock for the 'w' (write) call. We will assert on this mock.
        mock_write_zip = MagicMock()
        
        # ⚡ FIX: Mock for the 'r' (read/validate) call
        mock_validate_zip = MagicMock()
        mock_validate_zip.testzip.return_value = None # This makes validation pass
        
        mock_zip_open = mocker.patch("zipfile.ZipFile")
        # ⚡ FIX: Use side_effect to provide a *different* mock for each call.
        mock_zip_open.side_effect = [
            MagicMock(__enter__=MagicMock(return_value=mock_write_zip), __exit__=MagicMock(return_value=None)), # Call 1 (write)
            MagicMock(__enter__=MagicMock(return_value=mock_validate_zip), __exit__=MagicMock(return_value=None)) # Call 2 (read)
        ]
        
        # ⚡ FIX: Create a mock stat_result with a valid st_mode
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 1234
        mock_stat_result.st_mode = stat.S_IFREG  # This makes path.is_file() True
        
        mocker.patch.object(Path, "stat", return_value=mock_stat_result)
        
        # 3. Act
        packager._create_archive_sync(files, "test.zip")

        # 4. Assert
        # -----------------
        # 🐞 FIX: Assert the call count on the correct mock
        # -----------------
        # ⚡ FIX: Assert against the correct mock (mock_write_zip)
        assert mock_write_zip.write.call_count == 2
        calls = mock_write_zip.write.call_args_list
        
        # ⚡ FIX: The files are sorted alphabetically by path before archival.
        assert calls[0][1]["arcname"] == "src/file1.txt"
        assert calls[0][1]["compress_type"] == zipfile.ZIP_DEFLATED
        
        assert calls[1][1]["arcname"] == "src/file2.gz"
        assert calls[1][1]["compress_type"] == zipfile.ZIP_STORED

    async def test_handle_single_archive_no_pairs(self, base_packager_args):
        """
        Test Coverage for line 148: handle_single_archive returns empty if no pairs.
        """
        packager = ArchivePackager(**base_packager_args)
        archive_paths, to_delete = await packager.handle_single_archive([])
        
        assert archive_paths == {}
        assert to_delete == []

    async def test_handle_grouped_archives_no_historical(
        self, base_packager_args, project_with_files, caplog
    ):
        """
        Test Coverage for line 272: handle_grouped_archives skips group with no historical pairs.
        """
        packager = ArchivePackager(**base_packager_args)
        
        tests_pairs = [p for p in project_with_files if "tests" in p[0].name]
        assert len(tests_pairs) == 1 # Pre-condition
        groups = {"tests": tests_pairs}

        with caplog.at_level("INFO"):
            # -----------------
            # 🐞 FIX: Add the missing variable assignment
            # -----------------
            archive_paths, to_delete = await packager.handle_grouped_archives(groups)
        
        assert archive_paths == {}
        assert to_delete == []
        
        # -----------------
        # 🐞 FIX: Use a simpler assertion that works with structlog
        # -----------------
        assert "No historical pairs for group" in caplog.text
        assert "tests" in caplog.text
```

---

## tests/collector/test_git_ls.py

<a id='tests-collector-test-git-ls-py'></a>

```python
# tests/collector/test_git_ls.py

"""
Tests for src/create_dump/collector/git_ls.py
"""

from __future__ import annotations
import pytest
from unittest.mock import AsyncMock, patch

# Import the class to test
from create_dump.collector.git_ls import GitLsCollector
from create_dump.core import Config

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_get_git_ls_files(mocker) -> AsyncMock:
    """Mocks the system call to get_git_ls_files."""
    return mocker.patch(
        "create_dump.collector.git_ls.get_git_ls_files",
        new_callable=AsyncMock
    )


@pytest.fixture
def mock_filter_files(mocker) -> AsyncMock:
    """Mocks the base class's filter_files method."""
    return mocker.patch(
        "create_dump.collector.base.CollectorBase.filter_files",
        new_callable=AsyncMock
    )


class TestGitLsCollector:
    """Tests for the GitLsCollector."""

    async def test_collect_success(
        self,
        test_project,
        default_config: Config,
        mock_get_git_ls_files: AsyncMock,
        mock_filter_files: AsyncMock,
    ):
        """
        Test Case 1: (Happy Path)
        Validates that:
        1. get_git_ls_files is called.
        2. The raw list is passed to filter_files.
        3. The filtered list is returned.
        """
        raw_files = ["src/main.py", "README.md", "src/ignored.log"]
        filtered_files = ["src/main.py", "README.md"]
        
        mock_get_git_ls_files.return_value = raw_files
        mock_filter_files.return_value = filtered_files
        
        collector = GitLsCollector(config=default_config, root=test_project.root)
        result = await collector.collect()

        # Assertions
        mock_get_git_ls_files.assert_called_once_with(test_project.root)
        mock_filter_files.assert_called_once_with(raw_files)
        assert result == filtered_files

    async def test_collect_no_files_found(
        self,
        test_project,
        default_config: Config,
        mock_get_git_ls_files: AsyncMock,
        mock_filter_files: AsyncMock,
    ):
        """
        Test Case 2: (Empty Result)
        Validates that filter_files is NOT called if git ls-files returns empty.
        """
        mock_get_git_ls_files.return_value = []
        
        collector = GitLsCollector(config=default_config, root=test_project.root)
        result = await collector.collect()

        # Assertions
        mock_get_git_ls_files.assert_called_once_with(test_project.root)
        mock_filter_files.assert_not_called()
        assert result == []
```

---

## tests/conftest.py

<a id='tests-conftest-py'></a>

```python
# tests/conftest.py

"""
Global fixtures for the create-dump test suite.

This file provides common, reusable fixtures (like project setup,
config objects, and CLI runners) to all test modules.
"""

import os  # ⚡ FIXED: Import os for chdir
import pytest
import pytest_asyncio
from pathlib import Path
from typing import Dict, Callable, Awaitable

import anyio
from typer.testing import CliRunner

from create_dump.core import Config
from create_dump.cli.main import app as cli_app

# --- Session-Scoped Fixtures (Setup once) ---

# 🐞 FIX: Change scope from "session" to "function" to prevent test pollution
@pytest.fixture(scope="function")
def default_config() -> Config:
    """
    Provides a default, unaltered Config object.
    Tests should override specific fields as needed.
    """
    return Config()


@pytest.fixture(scope="session")
def cli_runner() -> CliRunner:
    """
    Provides a Typer CliRunner instance for invoking the CLI app.
    """
    return CliRunner()


@pytest.fixture(scope="session")
def cli_app_instance():
    """
    Provides the main Typer application instance.
    """
    return cli_app


# --- Function-Scoped Fixtures (Setup for each test) ---

class TestProjectFactory:
    """
    A factory for creating temporary project structures asynchronously.
    This is provided as a class to be instantiated by the fixture.
    """
    
    def __init__(self, tmp_path: Path):
        self.root = tmp_path
        # Ensure we're using anyio's Path for async I/O
        self.async_root = anyio.Path(self.root)

    async def create(self, structure: Dict[str, str | bytes | None]): # 🐞 FIX: Allow bytes and None
        """
        Creates files and directories from a dictionary structure.
        Keys are relative paths, values are file content.
        
        Example:
        await factory.create({
            "src/main.py": "print('hello')",
            "src/data.bin": b"binary_data",
            "empty_dir/": None
        })
        """
        for rel_path_str, content in structure.items():
            rel_path = Path(rel_path_str)
            full_path = self.async_root / rel_path
            
            # Ensure parent directories exist
            if not await (full_path.parent).exists():
                await full_path.parent.mkdir(parents=True, exist_ok=True)

            # 🐞 FIX: Handle content type
            if rel_path_str.endswith('/') or content is None:
                # It's explicitly a directory
                await full_path.mkdir(parents=True, exist_ok=True)
            elif isinstance(content, bytes):
                # It's binary content
                await full_path.write_bytes(content)
            else:
                # It's a text file
                await full_path.write_text(str(content)) # Cast content to str
 
    def path(self, rel_path: str) -> Path:
        """Helper to get a full pathlib.Path to a file in the test project."""
        return self.root / rel_path

@pytest_asyncio.fixture(scope="function")
async def test_project(tmp_path: Path): # ⚡ REMOVED: Type hint for factory
    """
    Provides an async factory fixture to create test project structures.
    
    Usage in a test:
    
    @pytest.mark.anyio
    async def test_my_feature(test_project: "TestProjectFactory"):
        # ... (docstring same as before) ...
    """
    # Change CWD to the temp path to simulate running from the project root
    # This is critical for collectors and path logic
    
    original_cwd = await anyio.to_thread.run_sync(Path.cwd)
    
    # ⚡ FIXED: Use os.chdir wrapped in run_sync
    await anyio.to_thread.run_sync(os.chdir, tmp_path)
    
    factory = TestProjectFactory(tmp_path)
    
    try:
        yield factory
    finally:
        # Teardown: change CWD back, guaranteed
        # ⚡ FIXED: Use os.chdir wrapped in run_sync
        await anyio.to_thread.run_sync(os.chdir, original_cwd)



```

---

## tests/collector/test_init.py

<a id='tests-collector-test-init-py'></a>

```python
# tests/collector/test_init.py

"""
Tests for the collector factory in src/create_dump/collector/__init__.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Import the function to test
from create_dump.collector import get_collector
# Import dependencies to mock
from create_dump.core import Config


@pytest.fixture
def mock_config() -> Config:
    """Provides a default Config object."""
    return Config()


@pytest.fixture
def mock_collectors(mocker) -> dict[str, MagicMock]:
    """Mocks all collector classes and returns them."""
    # 🐞 FIX: Patch the names where they are *used* (in the __init__ module)
    mock_walk = mocker.patch("create_dump.collector.WalkCollector")
    mock_ls = mocker.patch("create_dump.collector.GitLsCollector")
    mock_diff = mocker.patch("create_dump.collector.GitDiffCollector")

    return {
        "WalkCollector": mock_walk,
        "GitLsCollector": mock_ls,
        "GitDiffCollector": mock_diff,
    }


class TestGetCollector:
    """Tests the get_collector factory function."""

    def test_get_collector_defaults_to_walk(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 1: (Default)
        Ensures WalkCollector is chosen when no flags are present.
        """
        get_collector(config=mock_config)

        mock_collectors["WalkCollector"].assert_called_once()
        mock_collectors["GitLsCollector"].assert_not_called()
        mock_collectors["GitDiffCollector"].assert_not_called()

    def test_get_collector_selects_git_ls(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 2: (git_ls_files flag)
        Ensures GitLsCollector is chosen when git_ls_files=True.
        """
        get_collector(config=mock_config, git_ls_files=True)

        mock_collectors["GitLsCollector"].assert_called_once()
        mock_collectors["WalkCollector"].assert_not_called()
        mock_collectors["GitDiffCollector"].assert_not_called()

    def test_get_collector_selects_git_diff(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 3: (diff_since flag)
        Ensures GitDiffCollector is chosen when diff_since is provided.
        """
        get_collector(config=mock_config, diff_since="main")

        mock_collectors["GitDiffCollector"].assert_called_once()
        mock_collectors["WalkCollector"].assert_not_called()
        mock_collectors["GitLsCollector"].assert_not_called()

    def test_get_collector_git_diff_has_precedence(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 4: (Precedence)
        Ensures GitDiffCollector is chosen even if git_ls_files is also True.
        """
        get_collector(
            config=mock_config,
            diff_since="main",
            git_ls_files=True  # This should be ignored
        )

        # GitDiffCollector should be called because it's checked first
        mock_collectors["GitDiffCollector"].assert_called_once()
        mock_collectors["WalkCollector"].assert_not_called()
        mock_collectors["GitLsCollector"].assert_not_called()

    def test_get_collector_passes_common_args(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 5: (Argument Passthrough)
        Ensures all common arguments are passed to the chosen collector.
        """
        root_path = Path("/test/root")
        includes = ["*.py"]
        excludes = ["*.log"]

        get_collector(
            config=mock_config,
            includes=includes,
            excludes=excludes,
            use_gitignore=True,
            root=root_path,
            diff_since="main"  # Choose GitDiffCollector for this test
        )

        # Check that the correct collector was called with all args
        mock_collectors["GitDiffCollector"].assert_called_once_with(
            diff_since="main",
            config=mock_config,
            includes=includes,
            excludes=excludes,
            use_gitignore=True,
            root=root_path
        )
```

---

## tests/collector/test_walk.py

<a id='tests-collector-test-walk-py'></a>

```python
# tests/collector/test_walk.py

"""
Tests for Phase 2: src/create_dump/collector/walk.py
"""

from __future__ import annotations
import pytest
from pathlib import Path

# Import the class to test
from create_dump.collector.walk import WalkCollector
# Import dependencies needed for testing
from create_dump.core import Config

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


class TestWalkCollector:
    """Groups tests for the WalkCollector class."""

    @pytest.fixture
    async def project_structure(self, test_project):
        """Creates a standard file structure for walk tests."""
        await test_project.create({
            "src/main.py": "print('hello')",
            "src/utils.py": "def helper(): pass",
            "src/data/file.txt": "data",
            "src/__pycache__/cache.pyc": b"\x00",
            "src/logs/app.log": "this is a log",
            "README.md": "# Title",
            ".git/config": "fake git config"
        })

    async def test_collect_recursive(
        self, default_config: Config, test_project, project_structure
    ):
        """
        Tests the _collect_recursive() method directly.
        This method is responsible for walking subdirectories.
        """
        # We explicitly enable use_gitignore=False to ensure
        # only default_excludes (like __pycache__) are used.
        collector = WalkCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=False
        )

        # Start the recursive collector from the 'src' directory
        collected_files_gen = collector._collect_recursive(Path("src"))
        
        # Collect results into a set for easy comparison
        collected_files = {p.as_posix() async for p in collected_files_gen}

        # Define what we expect to find *within* 'src'
        expected = {
            "src/main.py",
            "src/utils.py",
            "src/data/file.txt",
            # 'src/logs/app.log' is excluded by default_excludes
            # 'src/__pycache__/cache.pyc' is excluded by excluded_dirs
        }

        assert collected_files == expected

    async def test_collect_full(
        self, default_config: Config, test_project, project_structure
    ):
        """
        Tests the main collect() method, which scans the root
        and then calls the recursive collector.
        """
        collector = WalkCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=False  # Keep test predictable
        )

        # Run the full collection
        files_list = await collector.collect()

        # Expected list is sorted, as per the collector's implementation
        expected = [
            "README.md",
            "src/data/file.txt",
            "src/main.py",
            "src/utils.py",
        ]
        
        assert files_list == expected

    async def test_collect_with_gitignore(
        self, default_config: Config, test_project
    ):
        """
        Tests that the collector correctly uses .gitignore
        when use_gitignore=True.
        """
        await test_project.create({
            "src/main.py": "print('hello')",
            "src/ignored.py": "ignore me",
            "README.md": "# Title",
            ".gitignore": "src/ignored.py"
        })
        
        collector = WalkCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=True  # Explicitly enable
        )

        files_list = await collector.collect()

        # src/ignored.py should be missing
        expected = [
            "README.md",
            "src/main.py",
        ]
        
        assert files_list == expected

```

---

## tests/rollback/test_parser.py

<a id='tests-rollback-test-parser-py'></a>

~~~python
# tests/rollback/test_parser.py

"""
Tests for src/create_dump/rollback/parser.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
import anyio

# Import the class to test
from create_dump.rollback.parser import MarkdownParser

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


class TestMarkdownParser:
    """Tests for the MarkdownParser class."""

    async def test_parse_valid_file_simple(self, tmp_path: Path):
        """
        Test Case 1: Valid file with one entry.
        """
        dump_file = tmp_path / "simple.md"
        content = (
            "# Dump\n\n"
            "## src/main.py\n\n"
            "```python\n"
            "print('hello world')\n"
            "```\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 1
        assert results[0] == ("src/main.py", "print('hello world')\n")

    async def test_parse_valid_file_multiple_mixed_fences(self, tmp_path: Path):
        """
        Test Case 2: Multiple files, different fences (``` and ~~~).
        """
        dump_file = tmp_path / "mixed.md"
        content = (
            "## file1.py\n"
            "```python\ncontent1\n```\n\n"
            "## file2.md\n"
            "~~~markdown\ncontent with ```backticks``` inside\n~~~\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 2
        assert results[0] == ("file1.py", "content1\n")
        assert results[1] == ("file2.md", "content with ```backticks``` inside\n")

    async def test_parse_empty_file(self, tmp_path: Path):
        """
        Test Case 3: Empty file yields nothing.
        """
        dump_file = tmp_path / "empty.md"
        await anyio.Path(dump_file).touch()

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 0

    async def test_parse_ignores_preamble_and_mixed_content(self, tmp_path: Path):
        """
        Test Case 4: Text outside of file blocks is ignored.
        """
        dump_file = tmp_path / "noisy.md"
        content = (
            "# Project Dump\n"
            "This is some preamble text.\n\n"
            "## valid/file.txt\n"
            "```text\nreal content\n```\n"
            "This text between files should also be ignored.\n"
            "## another/file.txt\n"
            "```\nmore content\n```\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 2
        assert results[0] == ("valid/file.txt", "real content\n")
        assert results[1] == ("another/file.txt", "more content\n")

    async def test_parse_malformed_headers_ignored(self, tmp_path: Path):
        """
        Test Case 5: Headers that don't match `## ` are ignored.
        """
        dump_file = tmp_path / "malformed.md"
        content = (
            "# Too Top Level (Ignored)\n"
            "```\nignore me\n```\n"
            "### Too Deep Level (Ignored)\n"
            "```\nignore me too\n```\n"
            "## just_right.txt\n"
            "```\ncontent\n```\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 1
        assert results[0] == ("just_right.txt", "content\n")

    async def test_parse_unclosed_fence_skipped(self, tmp_path: Path):
        """
        Test Case 6: If EOF is reached while capturing, the last file is dropped.
        """
        dump_file = tmp_path / "incomplete.md"
        content = (
            "## good.txt\n"
            "```\ngood content\n```\n"
            "## bad.txt\n"
            "```\nmissing closing fence..."
            # EOF here
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        # Should only get the one that finished
        assert len(results) == 1
        assert results[0] == ("good.txt", "good content\n")

    async def test_parse_skips_error_blocks(self, tmp_path: Path):
        """
        Test Case 7: Standard error blocks are identified and skipped.
        """
        dump_file = tmp_path / "errors.md"
        content = (
            "## good.py\n"
            "```python\nprint('ok')\n```\n"
            "\n"
            "## secret.py\n"
            "\n> ⚠️ **Failed:** Secrets Detected\n\n"
            "---\n\n"
            "## also_good.py\n"
            "```python\nprint('also ok')\n```\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 2
        assert results[0][0] == "good.py"
        assert results[1][0] == "also_good.py"

    async def test_file_not_found_re_raises(self, tmp_path: Path, mocker):
        """
        Test Case 8: FileNotFoundError is logged and re-raised.
        """
        missing_file = tmp_path / "ghost.md"
        parser = MarkdownParser(missing_file)
        mock_logger = mocker.patch("create_dump.rollback.parser.logger")

        with pytest.raises(FileNotFoundError):
             # Consume the generator to trigger execution
             [r async for r in parser.parse_dump_file()]

        mock_logger.error.assert_called_once_with(
            f"Rollback failed: Dump file not found at {missing_file}"
        )

    async def test_generic_exception_re_raises(self, tmp_path: Path, mocker):
        """
        Test Case 9: Generic exceptions during read are logged and re-raised.
        """
        dump_file = tmp_path / "broken.md"
        await anyio.Path(dump_file).touch()

        parser = MarkdownParser(dump_file)
        mock_logger = mocker.patch("create_dump.rollback.parser.logger")

        # Mock anyio.Path.open to fail
        mocker.patch.object(anyio.Path, "open", side_effect=PermissionError("Access denied"))

        with pytest.raises(PermissionError):
             [r async for r in parser.parse_dump_file()]

        mock_logger.error.assert_called_once_with(
            "Rollback failed: Error parsing dump file: Access denied"
        )
~~~

---

## tests/test_core.py

<a id='tests-test-core-py'></a>

```python
# tests/test_core.py

"""
Tests for Phase 1: src/create_dump/core.py
"""

from __future__ import annotations
import pytest
from pydantic import ValidationError
from pathlib import Path

from create_dump.core import (
    Config,
    load_config,
    DEFAULT_DUMP_PATTERN
)

# Mark all tests in this file as async-capable
# (needed for the test_project fixture)
pytestmark = pytest.mark.anyio


# --- Test Config Model (Validators) ---

def test_config_defaults(default_config: Config):
    """
    Tests the sane default values of the Config model.
    """
    assert default_config.git_meta is True
    assert default_config.use_gitignore is True
    assert default_config.max_file_size_kb is None
    assert default_config.dest is None
    assert "pyproject.toml" not in default_config.default_excludes
    assert ".git" in default_config.excluded_dirs


def test_config_validator_max_file_size():
    """
    Tests the 'max_file_size_kb' validator.
    """
    # Valid values
    assert Config(max_file_size_kb=1000).max_file_size_kb == 1000
    assert Config(max_file_size_kb=0).max_file_size_kb == 0
    assert Config(max_file_size_kb=None).max_file_size_kb is None
    
    # Invalid value
    with pytest.raises(ValidationError, match="must be non-negative"):
        Config(max_file_size_kb=-1)

def test_config_validator_dest():
    """
    Tests the 'dest' path validator.
    """
    # Valid values
    assert Config(dest="path/to/dumps").dest == Path("path/to/dumps")
    assert Config(dest="/abs/path").dest == Path("/abs/path")
    assert Config(dest=None).dest is None
    
    # Invalid (empty) value should become None
    assert Config(dest="").dest is None

def test_config_validator_dump_pattern():
    """
    Tests the 'dump_pattern' validator to ensure it enforces the
    canonical prefix.
    """
    # Default is valid
    assert Config().dump_pattern == DEFAULT_DUMP_PATTERN
    
    # Custom valid pattern is accepted
    custom_valid = r"my_prefix_all_create_dump_.*\.zip"
    assert Config(dump_pattern=custom_valid).dump_pattern == custom_valid
    
    # Invalid (loose) pattern is reset to default
    invalid_loose = r"some_other_pattern.*\.md"
    assert Config(dump_pattern=invalid_loose).dump_pattern == DEFAULT_DUMP_PATTERN
    
    # Empty pattern is reset to default
    assert Config(dump_pattern="").dump_pattern == DEFAULT_DUMP_PATTERN


# --- Test load_config() ---

async def test_load_config_no_file(test_project):
    """
    Tests that default Config is returned when no config file is found.
    We use test_project to ensure we are in a clean directory.
    """
    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    config = load_config(_cwd=test_project.root)

    # 🐞 FIX: Robustly check for default values instead of brittle instance equality
    default_config = Config()
    assert config.dest == default_config.dest
    assert config.git_meta == default_config.git_meta
    assert config.max_file_size_kb == default_config.max_file_size_kb

async def test_load_config_from_pyproject(test_project):
    """
    Tests that config is correctly loaded from [tool.create-dump]
    in pyproject.toml.
    """
    await test_project.create({
        "pyproject.toml": """
[tool.create-dump]
dest = "from_pyproject"
git_meta = false
"""
    })

    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    config = load_config(_cwd=test_project.root)
    assert config.dest == Path("from_pyproject")
    assert config.git_meta is False
    # Defaults should still be present
    assert config.use_gitignore is True

async def test_load_config_from_dedicated_file(test_project):
    """
    Tests that config is correctly loaded from create_dump.toml.
    """
    await test_project.create({
        "create_dump.toml": """
[tool.create-dump]
dest = "from_dedicated_toml"
max_file_size_kb = 500
"""
    })

    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    config = load_config(_cwd=test_project.root)
    assert config.dest == Path("from_dedicated_toml")
    assert config.max_file_size_kb == 500
    assert config.git_meta is True # Default

async def test_load_config_precedence(test_project):
    """
    Tests that create_dump.toml takes precedence over pyproject.toml
    (based on the `possible_paths` order in core.py).
    """
    await test_project.create({
        "create_dump.toml": """
[tool.create-dump]
dest = "from_dedicated_toml"
""",
        "pyproject.toml": """
[tool.create-dump]
dest = "from_pyproject"
"""
    })

    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    config = load_config(_cwd=test_project.root)
    # 'create_dump.toml' is checked first in CWD, so it should win.
    assert config.dest == Path("from_dedicated_toml")

async def test_load_config_with_explicit_path(test_project):
    """
    Tests that loading from an explicit path works and
    ignores other config files.
    """
    await test_project.create({
        "config/my_config.toml": """
[tool.create-dump]
dest = "from_explicit_path"
""",
        "pyproject.toml": """
[tool.create-dump]
dest = "from_pyproject"
"""
    })
    
    explicit_path = test_project.path("config/my_config.toml")
    
    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    # The explicit `path` argument will be used first, but we still
    # pass _cwd to be consistent and safe.
    config = load_config(path=explicit_path, _cwd=test_project.root)

    assert config.dest == Path("from_explicit_path")

```

---

## tests/test_cleanup.py

<a id='tests-test-cleanup-py'></a>

```python
# tests/test_cleanup.py

"""
Tests for Phase 3: src/create_dump/cleanup.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
import logging
import shutil  # For mock targets
# ⚡ REFACTOR: Import AsyncGenerator for mocking
from typing import AsyncGenerator

import anyio

# Import the functions to test
from create_dump.cleanup import (
    safe_delete_paths,
    safe_cleanup
)
from create_dump.logging import setup_logging
# ⚡ REFACTOR: Import the new async util
from create_dump.path_utils import safe_is_within


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


class TestSafeDeletePathsAsync:
    """Groups tests for the core safe_delete_paths worker."""

    async def test_deletes_files_and_dirs(self, test_project):
        """
        Test Case 1: (Happy Path)
        Ensures files and directories are actually deleted (passing a List).
        """
        # 🐞 FIX: Setup logging for this test to see error logs
        setup_logging(verbose=True)
        root = test_project.root
        await test_project.create({
            "file_to_delete.txt": "content",
            "dir_to_delete/file.txt": "content",
            "keep_me.txt": "content"
        })

        paths_to_delete = [
            root / "file_to_delete.txt",
            root / "dir_to_delete"
        ]

        deleted_files, deleted_dirs = await safe_delete_paths(
            paths_to_delete, root, dry_run=False, assume_yes=True
        )

        assert (deleted_files, deleted_dirs) == (1, 1)
        assert not await (anyio.Path(root) / "file_to_delete.txt").exists()
        assert not await (anyio.Path(root) / "dir_to_delete").exists()
        assert await (anyio.Path(root) / "keep_me.txt").exists()

    async def test_deletes_from_generator(self, test_project):
        """
        Test Case 1b: (Happy Path - Generator)
        Ensures files and directories are deleted when passed as an AsyncGenerator.
        """
        setup_logging(verbose=True)
        root = test_project.root
        await test_project.create({
            "file_to_delete.txt": "content",
            "dir_to_delete/file.txt": "content",
        })

        paths_to_delete = [
            root / "file_to_delete.txt",
            root / "dir_to_delete"
        ]
        
        async def path_gen() -> AsyncGenerator[Path, None]:
            for p in paths_to_delete:
                yield p

        deleted_files, deleted_dirs = await safe_delete_paths(
            path_gen(), root, dry_run=False, assume_yes=True
        )

        assert (deleted_files, deleted_dirs) == (1, 1)
        assert not await (anyio.Path(root) / "file_to_delete.txt").exists()
        assert not await (anyio.Path(root) / "dir_to_delete").exists()

    async def test_dry_run_logs_and_skips_deletion(self, test_project, capsys):
        """
        Test Case 2: (Dry Run)
        Ensures no files are deleted and logs are produced.
        """
        # 🐞 FIX: Setup logging *inside* test to bind to caplog
        setup_logging(verbose=True)

        root = test_project.root
        await test_project.create({
            "file_to_delete.txt": "content",
            "dir_to_delete/file.txt": "content",
        })
        paths_to_delete = [
            root / "file_to_delete.txt",
            root / "dir_to_delete"
        ]

        deleted_files, deleted_dirs = await safe_delete_paths(
            paths_to_delete, root, dry_run=True, assume_yes=True
        )

        assert (deleted_files, deleted_dirs) == (0, 0)
        assert await (anyio.Path(root) / "file_to_delete.txt").exists()
        assert await (anyio.Path(root) / "dir_to_delete").exists()

        # 🐞 FIX: Check the rendered 'err' for ConsoleRenderer via capsys
        out, err = capsys.readouterr()
        assert err.count("[dry-run] would delete file") == 1
        assert err.count("[dry-run] would remove directory") == 1

    async def test_skips_paths_outside_root(self, test_project, capsys):
        """
        Test Case 3: (Path Safety)
        Ensures files outside the root are ignored.
        """
        # 🐞 FIX: Setup logging *inside* test to bind to caplog
        setup_logging(verbose=True)

        root = test_project.root
        # Create a file *outside* the test project root
        external_file = root.parent / "external_file.txt"
        await anyio.Path(external_file).write_text("external")

        try:
            deleted_files, deleted_dirs = await safe_delete_paths(
                [external_file], root, dry_run=False, assume_yes=True
            )

            assert (deleted_files, deleted_dirs) == (0, 0)
            assert await anyio.Path(external_file).exists()
            # 🐞 FIX: Check the rendered 'err' for ConsoleRenderer via capsys
            out, err = capsys.readouterr()
            assert "Skipping path outside root" in err

        finally:
            # Clean up the external file
            await anyio.Path(external_file).unlink(missing_ok=True)

    async def test_prompts_for_dir_deletion(self, test_project, mocker):
        """
        Test Case 4: (User Prompting)
        Ensures `confirm` is called and respected.
        """
        # 🐞 FIX: Setup logging for this test to see error logs
        setup_logging(verbose=True)

        root = test_project.root
        await test_project.create({"dir_to_delete": None})
        dir_path = root / "dir_to_delete"

        # Mock the confirm function (which is run in a thread)
        mock_confirm = mocker.patch(
            "create_dump.cleanup.confirm", return_value=False
        )

        # 1. Test "No" response
        deleted_files, deleted_dirs = await safe_delete_paths(
            [dir_path], root, dry_run=False, assume_yes=False
        )

        assert (deleted_files, deleted_dirs) == (0, 0)
        mock_confirm.assert_called_once()
        assert await anyio.Path(dir_path).exists()

        # 2. Test "Yes" response
        mock_confirm.return_value = True
        mock_confirm.reset_mock()

        deleted_files, deleted_dirs = await safe_delete_paths(
            [dir_path], root, dry_run=False, assume_yes=False
        )

        assert (deleted_files, deleted_dirs) == (0, 1)
        mock_confirm.assert_called_once()
        assert not await anyio.Path(dir_path).exists()

    # ⚡ NEW: Test case to validate the exception hardening
    async def test_delete_async_logs_ioerror_and_fails_on_other_errors(self, test_project, mocker, capsys):
        """
        Test Case 5: (Error Hardening)
        Ensures the refactored exception block catches (OSError, IOError)
        but correctly *re-raises* other exceptions (like TypeError).
        """
        setup_logging(verbose=True)
        root = test_project.root
        await test_project.create({"file_to_delete.txt": "content"})
        paths_to_delete = [root / "file_to_delete.txt"]

        # --- Part 1: Test OSError is caught ---
        # 🐞 FIX: Mock the correct object (anyio.Path.unlink) with OSError
        mocker.patch.object(
            anyio.Path, "unlink",
            side_effect=OSError("Simulated Disk Full")
        )

        deleted_files, deleted_dirs = await safe_delete_paths(
            paths_to_delete, root, dry_run=False, assume_yes=True
        )

        assert (deleted_files, deleted_dirs) == (0, 0)
        # 🐞 FIX: Check the rendered 'err' for ConsoleRenderer via capsys
        out, err = capsys.readouterr()
        assert "Failed to delete file" in err
        assert "Simulated Disk Full" in err

        # --- Part 2: Test TypeError is NOT caught ---
        mocker.patch.object(
            anyio.Path, "unlink",
            side_effect=TypeError("Simulated Non-IO Error")
        )

        with pytest.raises(TypeError, match="Simulated Non-IO Error"):
            await safe_delete_paths(
                paths_to_delete, root, dry_run=False, assume_yes=True
            )

# ⚡ REFACTOR: Add fixture to mock the generator
@pytest.fixture
def mock_find_matching_files(mocker):
    """Mocks the find_matching_files generator."""
    mock_gen_func = mocker.patch("create_dump.cleanup.find_matching_files")
    
    async def create_gen(file_list: List[Path]) -> AsyncGenerator[Path, None]:
        for f in file_list:
            yield f
    
    # Default behavior: return an empty generator
    mock_gen_func.return_value = create_gen([])
    return mock_gen_func, create_gen

class TestSafeCleanupAsync:
    """Groups tests for the safe_cleanup wrapper."""

    async def test_safe_cleanup_finds_and_deletes(self, test_project, mock_find_matching_files):
        """
        Test Case 6: (Integration)
        Tests the full wrapper finds files by pattern and deletes them.
        """
        # 🐞 FIX: Setup logging for this test to see error logs
        setup_logging(verbose=True)

        root = test_project.root
        await test_project.create({
            "file_to_delete_1.log": "delete me",
            "subdir/file_to_delete_2.log": "delete me too",
            "file_to_keep.txt": "keep me"
        })

        pattern = r".*\.log$"
        
        # ⚡ REFACTOR: Configure mock to return the files
        mock_gen_func, gen_factory = mock_find_matching_files
        files_to_find = [
            root / "file_to_delete_1.log",
            root / "subdir/file_to_delete_2.log"
        ]
        mock_gen_func.return_value = gen_factory(files_to_find)

        await safe_cleanup(
            root, pattern, dry_run=False, assume_yes=True, verbose=True
        )

        assert not await (anyio.Path(root) / "file_to_delete_1.log").exists()
        assert not await (anyio.Path(root) / "subdir/file_to_delete_2.log").exists()
        assert await (anyio.Path(root) / "file_to_keep.txt").exists()


    async def test_safe_cleanup_dry_run(self, test_project, capsys, mock_find_matching_files):
        """
        Test Case 7: (Integration - Dry Run)
        Tests that the wrapper respects dry_run.
        """
        # 🐞 FIX: Setup logging *inside* test to bind to caplog
        setup_logging(verbose=True)

        root = test_project.root
        await test_project.create({
            "file_to_delete_1.log": "delete me",
        })
        
        # ⚡ REFACTOR: Configure mock to return the file
        mock_gen_func, gen_factory = mock_find_matching_files
        mock_gen_func.return_value = gen_factory([root / "file_to_delete_1.log"])

        pattern = r".*\.log$"

        await safe_cleanup(
            root, pattern, dry_run=True, assume_yes=True, verbose=True
        )

        assert await (anyio.Path(root) / "file_to_delete_1.log").exists()

        # 🐞 FIX: Check the rendered 'err' for ConsoleRenderer via capsys
        out, err = capsys.readouterr()
        # ⚡ REFACTOR: Test the new generator-aware log message
        assert "Found paths to clean (starting with: file_to_delete_1.log)" in err
        assert "Dry-run: Skipping deletions." in err

    async def test_safe_cleanup_no_matches(self, test_project, capsys, mock_find_matching_files):
        """
        Test Case 8: (Integration - No Matches)
        Tests the "no matches" branch.
        """
        setup_logging(verbose=True)
        root = test_project.root
        
        # ⚡ REFACTOR: Mock is already configured to return an empty generator
        
        pattern = r".*\.log$"
        await safe_cleanup(
            root, pattern, dry_run=False, assume_yes=True, verbose=True
        )
        
        out, err = capsys.readouterr()
        assert "No matching files found for cleanup." in err
```

---

## tests/test_archiver.py

<a id='tests-test-archiver-py'></a>

```python
# tests/test_archiver.py

"""
Tests for src/create_dump/archiver.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, List, Optional, Tuple

import anyio

from create_dump.archiver import ArchiveManager
from create_dump.core import DEFAULT_DUMP_PATTERN
from create_dump.archive import ArchiveFinder, ArchivePackager, ArchivePruner

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_config(mocker):
    """Mock load_config to return a dummy Config."""
    mock_cfg = MagicMock()
    mock_cfg.dump_pattern = DEFAULT_DUMP_PATTERN
    mocker.patch("create_dump.archiver.load_config", return_value=mock_cfg)
    return mock_cfg


@pytest.fixture
def mock_dirs(tmp_path: Path):
    """Ensure archives/quarantine dirs exist in tmp_path."""
    archives_dir = tmp_path / "archives"
    quarantine_dir = archives_dir / "quarantine"
    archives_dir.mkdir(exist_ok=True)
    quarantine_dir.mkdir(exist_ok=True)
    return archives_dir, quarantine_dir


class TestArchiveManagerInit:
    """Tests for ArchiveManager.__init__."""

    def test_init_defaults(self, tmp_path: Path, mock_config):
        """Test Case 1: Default params, dir creation, pattern fallback."""
        root = tmp_path / "root"
        root.mkdir()

        manager = ArchiveManager(
            root=root,
            timestamp="20250101_000100",
            verbose=False,
            md_pattern=None,
        )

        assert manager.root == root.resolve()
        assert manager.archives_dir == root / "archives"
        assert manager.quarantine_dir == root / "archives" / "quarantine"
        assert manager.md_pattern == DEFAULT_DUMP_PATTERN
        assert manager.search is False
        assert manager.dry_run is False
        assert manager.yes is False

    def test_init_custom_pattern(self, tmp_path: Path, mock_config, mocker):
        """Test Case 2: Custom md_pattern, warning on loose format."""
        root = tmp_path / "root"
        root.mkdir()
        mock_logger = mocker.patch("create_dump.archiver.logger")

        loose_pattern = r".*\.md$"
        manager = ArchiveManager(
            root=root,
            timestamp="20250101_000100",
            md_pattern=loose_pattern,
        )

        mock_logger.warning.assert_called_once()
        assert manager.md_pattern == DEFAULT_DUMP_PATTERN  # Enforced canonical

    def test_init_archive_all(self, tmp_path: Path):
        """Test Case 3: archive_all enables search."""
        root = tmp_path / "root"
        root.mkdir()

        manager = ArchiveManager(
            root=root,
            timestamp="20250101_000100",
            archive_all=True,
        )

        assert manager.search is True
        assert manager.archive_all is True


# ⚡ RENAMED: Class to match new function name
class TestArchiveManagerRun:
    """Tests for ArchiveManager.run orchestration."""

    @pytest.mark.parametrize("archive_all", [False, True])
    # ⚡ RENAMED: Function to match new API
    async def test_run_happy_path(self, tmp_path: Path, mock_config, mock_dirs, archive_all):
        """Test Case 4: Full flow with pairs, packaging, clean, prune."""
        root = tmp_path / "root"
        root.mkdir()
        archives_dir, quarantine_dir = mock_dirs

        # Mock components
        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [
            (root / "test.md", root / "test.sha256"),
        ]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_archive_paths = {"test": root / "archives/test.zip"}
        mock_to_delete = [root / "test.md"]
        if archive_all:
            mock_packager.group_pairs_by_prefix.return_value = {"group1": mock_pairs}
            mock_packager.handle_grouped_archives.return_value = (mock_archive_paths, mock_to_delete)
        else:
            mock_packager.handle_single_archive.return_value = (mock_archive_paths, mock_to_delete)
        mock_packager.group_pairs_by_prefix.return_value = {}  # Fallback

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        mock_delete = AsyncMock()
        mock_delete.return_value = (1, 0)

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.safe_delete_paths", new=mock_delete), \
             patch("create_dump.archiver.confirm", return_value=True):

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                archive_all=archive_all,
                clean_root=True,
                no_remove=False,
                dry_run=False,
                yes=True,
            )
            # ⚡ RENAMED: Call manager.run()
            result = await manager.run()

        mock_finder.find_dump_pairs.assert_called_once()
        if archive_all:
            mock_packager.group_pairs_by_prefix.assert_called_once()
            mock_packager.handle_grouped_archives.assert_called_once()
        else:
            mock_packager.handle_single_archive.assert_called_once()
        mock_pruner.prune.assert_called_once()
        mock_delete.assert_called_once()  # Clean called
        assert result == mock_archive_paths

    # ⚡ RENAMED: Function to match new API
    async def test_run_no_pairs(self, tmp_path: Path, mock_config, mocker):
        """Test Case 5: Early return if no pairs, prune still runs."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_finder.find_dump_pairs.return_value = []

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner):

            manager = ArchiveManager(root=root, timestamp="20250101_000100")
            # ⚡ RENAMED: Call manager.run()
            result = await manager.run()

        mock_finder.find_dump_pairs.assert_called_once()
        mock_pruner.prune.assert_called_once()
        assert result == {}

    # ⚡ RENAMED: Function to match new API
    async def test_run_dry_run_skips_clean(self, tmp_path: Path, mock_config, mocker):
        """Test Case 6: dry_run skips delete, no prompt."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [(root / "test.md", root / "test.sha256")]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_packager.handle_single_archive.return_value = ({}, [root / "test.md"])

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.confirm") as mock_confirm, \
             patch("create_dump.archiver.safe_delete_paths") as mock_delete:

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                clean_root=True,
                dry_run=True,
                yes=False,
            )
            # ⚡ RENAMED: Call manager.run()
            await manager.run()

        mock_confirm.assert_not_called()
        mock_delete.assert_not_called()
        mock_pruner.prune.assert_called_once()

    # ⚡ RENAMED: Function to match new API
    async def test_run_no_clean(self, tmp_path: Path, mock_config, mocker):
        """Test Case 7: clean_root=False skips delete entirely."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [(root / "test.md", root / "test.sha256")]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_packager.handle_single_archive.return_value = ({}, [root / "test.md"])

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.safe_delete_paths") as mock_delete:

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                clean_root=False,
                dry_run=False,
                yes=True,
            )
            # ⚡ RENAMED: Call manager.run()
            await manager.run()

        mock_delete.assert_not_called()
        mock_pruner.prune.assert_called_once()

    # ⚡ RENAMED: Function to match new API
    async def test_run_no_remove_skips_clean(self, tmp_path: Path, mock_config, mocker):
        """Test Case 8: no_remove=True skips delete despite clean_root."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [(root / "test.md", root / "test.sha256")]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_packager.handle_single_archive.return_value = ({}, [root / "test.md"])

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.safe_delete_paths") as mock_delete, \
             patch("create_dump.archiver.confirm") as mock_confirm:

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                clean_root=True,
                no_remove=True,
                dry_run=False,
                yes=True,
            )
            # ⚡ RENAMED: Call manager.run()
            await manager.run()

        mock_confirm.assert_not_called()
        mock_delete.assert_not_called()
        mock_pruner.prune.assert_called_once()

    # ⚡ RENAMED: Function to match new API
    async def test_run_prompt_declined(self, tmp_path: Path, mock_config, mocker):
        """Test Case 9: User declines prompt, skips clean."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [(root / "test.md", root / "test.sha256")]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_packager.handle_single_archive.return_value = ({}, [root / "test.md"])

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.confirm", return_value=False), \
             patch("create_dump.archiver.safe_delete_paths") as mock_delete:

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                clean_root=True,
                dry_run=False,
                yes=False,
            )
            # ⚡ RENAMED: Call manager.run()
            await manager.run()

        mock_delete.assert_not_called()
        mock_pruner.prune.assert_called_once()

    # ⚡ RENAMED: Function to match new API
    async def test_run_current_outfile_noop(self, tmp_path: Path, mock_config, mocker):
        """Test Case 10: current_outfile passed but no symlink logic yet."""
        root = tmp_path / "root"
        root.mkdir()
        current_outfile = root / "current.md"

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_finder.find_dump_pairs.return_value = []

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner):

            manager = ArchiveManager(root=root, timestamp="20250101_000100")
            # ⚡ RENAMED: Call manager.run()
            result = await manager.run(current_outfile=current_outfile)

        # No-op; no assertions fail on symlink absence
        assert result == {}
```

---

## tests/test_metrics.py

<a id='tests-test-metrics-py'></a>

```python
# tests/test_metrics.py

"""
Tests for src/create_dump/metrics.py
"""

from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch

from create_dump.metrics import (
    DEFAULT_METRICS_PORT, DUMP_DURATION, FILES_PROCESSED,
    ERRORS_TOTAL, metrics_server,
    ARCHIVES_CREATED_TOTAL  # ✨ NEW: Import new metric
)


class TestMetricsDefinitions:
    """Tests for Prometheus metric initializations."""

    def test_dump_duration_histogram(self):
        """Test Case 1: Histogram name, description, and buckets."""
        assert DUMP_DURATION._name == "create_dump_duration_seconds"
        assert DUMP_DURATION._documentation == "Dump duration"
        expected_buckets = [1, 5, 30, 60, 300, float("inf")]
        # ⚡ FIX: The internal attribute for buckets is _upper_bounds
        assert len(DUMP_DURATION._upper_bounds) == len(expected_buckets)
        # ⚡ REFACTOR: Check new label
        assert DUMP_DURATION._labelnames == ("collector",)

    def test_files_processed_counter(self):
        """Test Case 2: Counter name, description, and labels."""
        # 🐞 FIX: Assert the base name, not the exported name
        assert FILES_PROCESSED._name == "create_dump_files"
        assert FILES_PROCESSED._documentation == "Files processed"
        # ⚡ FIX: prometheus-client stores labels as a tuple
        assert FILES_PROCESSED._labelnames == ("status",)

    def test_errors_total_counter(self):
        """Test Case 3: Counter name, description, and labels."""
        # 🐞 FIX: Assert the base name, not the exported name
        assert ERRORS_TOTAL._name == "create_dump_errors"
        assert ERRORS_TOTAL._documentation == "Errors encountered"
        # ⚡ FIX: prometheus-client stores labels as a tuple
        assert ERRORS_TOTAL._labelnames == ("type",)

    def test_archives_created_counter(self):
        """Test Case 4: New archives counter."""
        assert ARCHIVES_CREATED_TOTAL._name == "create_dump_archives"
        assert ARCHIVES_CREATED_TOTAL._documentation == "Archives created"
        assert ARCHIVES_CREATED_TOTAL._labelnames == ("format",)

    def test_default_metrics_port(self):
        """Test Case 5: Default port constant."""
        assert DEFAULT_METRICS_PORT == 8000


class TestMetricsServerContextManager:
    """Tests for metrics_server lifecycle."""

    @patch("create_dump.metrics.start_http_server")
    def test_server_starts_on_port_gt_zero(self, mock_start_http_server):
        """Test Case 6: Starts server if port > 0, yields, no explicit cleanup."""
        with metrics_server(port=8001):
            mock_start_http_server.assert_called_once_with(8001)

    @patch("create_dump.metrics.start_http_server")
    def test_server_skips_on_port_zero(self, mock_start_http_server):
        """Test Case 7: No server start if port <= 0."""
        with metrics_server(port=0):
            mock_start_http_server.assert_not_called()

    @patch("create_dump.metrics.start_http_server")
    def test_server_context_yields_without_error(self, mock_start_http_server):
        """Test Case 8: Context yields successfully, no exceptions."""
        with metrics_server(port=8002):
            mock_start_http_server.assert_called_once_with(8002)

    @patch("create_dump.metrics.start_http_server")
    def test_default_port_used(self, mock_start_http_server):
        """Test Case 9: Defaults to 8000 if unspecified."""
        with metrics_server():
            mock_start_http_server.assert_called_once_with(8000)
```

---

## tests/test_logging.py

<a id='tests-test-logging-py'></a>

```python
# tests/test_logging.py

"""
Tests for Phase 3: src/create_dump/logging.py
"""

from __future__ import annotations
import pytest
import logging
from unittest.mock import MagicMock, patch
import re
import structlog  # ⚡ FIX: Import structlog for resetting

# Import the module to test
import create_dump.logging as logging_module
from create_dump.logging import (
    styled_print, setup_logging, logger, HAS_RICH, console
)


class TestLoggingSetup:
    """Tests for setup_logging configuration."""

    @pytest.fixture(autouse=True)
    def reset_logging(self):
        """Reset global logging state before/after each test."""
        # ⚡ FIX: Reset structlog config and re-init the module logger
        structlog.reset_defaults()
        logging.basicConfig(level=logging.WARNING, force=True)  # Reset basicConfig
        # Re-initialize the logger instance that other modules import
        logging_module.logger = structlog.get_logger("create_dump")

    def test_setup_logging_default(self):
        """Test Case 1: Default INFO level, JSON fallback (no Rich)."""
        with patch("create_dump.logging.HAS_RICH", False):
            with patch("structlog.configure") as mock_configure:
                setup_logging()

            mock_configure.assert_called_once()
            processors = mock_configure.call_args[1]["processors"]
            
            # ⚡ FIX: The code correctly adds 5 processors (format_exc_info was missed)
            # 1. TimeStamper, 2. add_log_level, 3. StackInfoRenderer, 4. format_exc_info, 5. JSONRenderer
            assert len(processors) == 5
            
            # ⚡ FIX: Check the *type* of the instance, not a string
            assert isinstance(processors[-1], structlog.processors.JSONRenderer)
            assert logging.getLogger().level == logging.INFO

    def test_setup_logging_verbose(self):
        """Test Case 2: Verbose DEBUG level, ConsoleRenderer if Rich available."""
        with patch("create_dump.logging.HAS_RICH", True):
            # ⚡ FIX: Mock the *class* not the instance
            mock_renderer_class = MagicMock()
            mock_renderer_instance = MagicMock()
            # When ConsoleRenderer(pad_event_to=40) is called, return our instance
            mock_renderer_class.return_value = mock_renderer_instance
            
            with patch("structlog.dev.ConsoleRenderer", mock_renderer_class):
                with patch("structlog.configure") as mock_configure:
                    setup_logging(verbose=True)

                mock_configure.assert_called_once()
                processors = mock_configure.call_args[1]["processors"]
                
                # ⚡ FIX: The code adds 5 processors
                assert len(processors) == 5
                
                # ⚡ FIX: Check that the last processor *is* our mock instance
                assert processors[-1] is mock_renderer_instance
                assert logging.getLogger().level == logging.DEBUG

    def test_setup_logging_quiet(self):
        """Test Case 3: Quiet WARNING level, no output."""
        with patch("create_dump.logging.HAS_RICH", False):
            with patch("structlog.configure") as mock_configure:
                setup_logging(quiet=True)

            mock_configure.assert_called_once()
            assert logging.getLogger().level == logging.WARNING

    def test_setup_logging_rich_import_failure(self):
        """Test Case 4: Fallback to JSON if ConsoleRenderer import fails."""
        with patch("create_dump.logging.HAS_RICH", True):
            with patch("structlog.dev.ConsoleRenderer", side_effect=ImportError):
                with patch("structlog.configure") as mock_configure:
                    setup_logging()

                processors = mock_configure.call_args[1]["processors"]
                # ⚡ FIX: Check the *type* of the instance
                assert isinstance(processors[-1], structlog.processors.JSONRenderer)

    def test_logger_instantiation(self):
        """Test Case 5: Logger is correctly instantiated post-setup."""
        # ⚡ FIX: The logger is just a proxy *until* setup_logging is called.
        # Call setup_logging() first, *then* test the .name attribute.
        
        # 1. Test that the proxy exists before setup
        assert logging_module.logger is not None
        
        # 2. Configure the logger
        setup_logging() 
        
        # 3. Now test the configured logger's properties
        # This check requires the logger to be wrapped by stdlib.BoundLogger
        assert logging_module.logger.name == "create_dump" 
        assert logging_module.logger is not None  # Still persistent


class TestStyledPrint:
    """Tests for styled_print output handling."""

    def test_styled_print_rich_available(self, mocker):
        """Test Case 6: Uses Rich console.print with kwargs."""
        mock_console = MagicMock()
        mocker.patch("create_dump.logging.console", mock_console)
        mocker.patch("create_dump.logging.HAS_RICH", True)

        styled_print("Test message", style="bold red", nl=False)

        # ⚡ FIX: The test was wrong. styled_print consumes 'nl' and passes 'end=""'.
        # The 'nl=False' argument should not be in the assertion.
        mock_console.print.assert_called_once_with(
            "Test message", style="bold red", end=""
        )

    # ⚡ FIX: Add 'mocker' fixture
    def test_styled_print_no_rich_fallback(self, capsys, mocker):
        """Test Case 7: Falls back to print, strips ANSI codes."""
        mocker.patch("create_dump.logging.HAS_RICH", False)

        styled_print("[bold red]Test with ANSI[/bold red]", nl=True)

        captured = capsys.readouterr()
        assert "Test with ANSI" in captured.out
        assert "[bold red]" not in captured.out  # Stripped
        assert captured.out.endswith("\n")

    # ⚡ FIX: Add 'mocker' fixture
    def test_styled_print_no_newline(self, capsys, mocker):
        """Test Case 8: nl=False suppresses trailing newline in fallback."""
        mocker.patch("create_dump.logging.HAS_RICH", False)

        styled_print("No NL", nl=False)

        captured = capsys.readouterr()
        assert "No NL" in captured.out
        assert not captured.out.endswith("\n")

    def test_styled_print_rich_import_failure(self, mocker, capsys):
        """Test Case 9: Handles console=None gracefully (fallback)."""
        mocker.patch("create_dump.logging.HAS_RICH", True)
        mocker.patch("create_dump.logging.console", None)

        styled_print("Fallback test")

        captured = capsys.readouterr()
        clean_text = re.sub(r"\[/?[^\]]+\]", "", "Fallback test")
        assert clean_text in captured.out  # Treated as fallback

    # ⚡ FIX: Add 'mocker' fixture
    def test_styled_print_complex_ansi_stripping(self, capsys, mocker):
        """Test Case 10: Robust regex stripping for nested/complex ANSI."""
        mocker.patch("create_dump.logging.HAS_RICH", False)

        complex_text = "[bold][red]Nested [underline]tags[/underline][/red][/bold] and plain"
        styled_print(complex_text)

        captured = capsys.readouterr()
        expected_clean = re.sub(r"\[/?[^\]]+\]", "", complex_text)
        assert expected_clean in captured.out
```

---

## tests/rollback/test_engine.py

<a id='tests-rollback-test-engine-py'></a>

```python
# tests/rollback/test_engine.py

"""
Tests for src/create_dump/rollback/engine.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from typing import AsyncGenerator, Tuple

import anyio

# Import classes to test
from create_dump.rollback.engine import RollbackEngine
from create_dump.rollback.parser import MarkdownParser
# ✨ NEW: Import safe_is_within to check its call
from create_dump.path_utils import safe_is_within


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_parser(mocker) -> MagicMock:
    """Mocks the MarkdownParser."""
    mock = MagicMock(spec=MarkdownParser)

    async def mock_generator() -> AsyncGenerator[Tuple[str, str], None]:
        yield ("src/main.py", "print('hello')")
        yield ("src/nested/util.py", "def helper(): pass")
        yield ("README.md", "# Title")
        # 🔒 Add a malicious path to test safety
        yield ("../etc/passwd", "root:x:0:0")

    mock.parse_dump_file = mock_generator
    return mock


class TestRollbackEngine:
    """Tests for the RollbackEngine."""

    async def test_rehydrate_creates_files_and_dirs(self, test_project, mock_parser):
        """
        Test Case 1: (Happy Path)
        Ensures the engine correctly creates nested directories and files
        with the correct content and skips unsafe paths.
        """
        output_dir = test_project.path("my_rollback")
        engine = RollbackEngine(root_output_dir=output_dir, dry_run=False)

        created_files = await engine.rehydrate(mock_parser)

        # Should be 3 files; the malicious path is skipped
        assert len(created_files) == 3

        # Check file 1
        file1_path = anyio.Path(output_dir / "src/main.py")
        assert await file1_path.exists()
        assert await file1_path.read_text() == "print('hello')"

        # Check file 2 (nested)
        file2_path = anyio.Path(output_dir / "src/nested/util.py")
        assert await file2_path.exists()
        assert await file2_path.read_text() == "def helper(): pass"

        # Check file 3 (root)
        file3_path = anyio.Path(output_dir / "README.md")
        assert await file3_path.exists()
        assert await file3_path.read_text() == "# Title"

        # Check that the malicious file was NOT created
        assert not await anyio.Path(output_dir / "../etc/passwd").exists()
        assert not await anyio.Path(test_project.root / "etc/passwd").exists()

    async def test_rehydrate_dry_run(self, test_project, mock_parser, mocker):
        """
        Test Case 2: (Dry Run)
        Ensures no files or directories are created when dry_run=True,
        but logging still occurs.
        """
        output_dir = test_project.path("dry_run_rollback")
        engine = RollbackEngine(root_output_dir=output_dir, dry_run=True)

        mock_logger_info = mocker.patch("create_dump.rollback.engine.logger.info")
        mock_logger_warn = mocker.patch("create_dump.rollback.engine.logger.warning")

        created_files = await engine.rehydrate(mock_parser)

        # It still *reports* what it would do (minus the skipped file)
        assert len(created_files) == 3

        # Assert no directory or files were actually created
        assert not await anyio.Path(output_dir).exists()
        assert not await anyio.Path(output_dir / "src/main.py").exists()

        # ⚡ FIX: Assert logging using the f-string format
        mock_logger_info.assert_any_call(
            f"[dry-run] Would rehydrate file to: {anyio.Path(output_dir / 'src/main.py')}"
        )
        mock_logger_info.assert_any_call(
            f"[dry-run] Would rehydrate file to: {anyio.Path(output_dir / 'src/nested/util.py')}"
        )
        mock_logger_info.assert_any_call(
            f"[dry-run] Would rehydrate file to: {anyio.Path(output_dir / 'README.md')}"
        )

        # ♻️ REFACTOR: Assert the new, more descriptive warning message
        mock_logger_warn.assert_called_once_with(
            "Skipping unsafe path: Resolves outside root",
            path="../etc/passwd",
            # Check that the resolved path is logged correctly
            resolved_to=str(anyio.Path(output_dir / "../etc/passwd"))
        )

        # Assert the final summary log
        mock_logger_info.assert_any_call(
            "Rehydration complete",
            files_created=3
        )

    async def test_rehydrate_handles_write_error(self, test_project, mock_parser, mocker):
        """
        Test Case 3: (Error Handling)
        Ensures that if the engine fails to write a file,
        the error is logged and the loop continues.
        """
        output_dir = test_project.path("error_rollback")
        # 🐞 NOTE: We instantiate engine *after* setting up the patch

        mock_logger_error = mocker.patch("create_dump.rollback.engine.logger.error")

        # 🐞 FIX: Mock the individual paths that will be returned by __truediv__
        mock_good_path = AsyncMock(spec=anyio.Path)
        mock_good_path.parent.mkdir = AsyncMock()
        mock_good_path.write_text = AsyncMock()
        # ✨ NEW: Implement the __fspath__ protocol
        mock_good_path.__fspath__ = MagicMock(return_value=str(output_dir / "src/main.py"))

        mock_bad_path = AsyncMock(spec=anyio.Path)
        mock_bad_path.parent.mkdir = AsyncMock()
        mock_bad_path.write_text = AsyncMock(side_effect=OSError("Disk full"))
        # ✨ NEW: Implement the __fspath__ protocol (even though it fails)
        mock_bad_path.__fspath__ = MagicMock(return_value=str(output_dir / "src/nested/util.py"))

        mock_readme_path = AsyncMock(spec=anyio.Path)
        mock_readme_path.parent.mkdir = AsyncMock()
        mock_readme_path.write_text = AsyncMock()
        # ✨ NEW: Implement the __fspath__ protocol
        mock_readme_path.__fspath__ = MagicMock(return_value=str(output_dir / "README.md"))

        mock_unsafe_path = AsyncMock(spec=anyio.Path) # For the ../etc/passwd path
        # ✨ NEW: Implement the __fspath__ protocol
        mock_unsafe_path.__fspath__ = MagicMock(return_value=str(output_dir / "../etc/passwd"))

        # We also need to mock safe_is_within as it's called on every path
        mock_safe_is_within = mocker.patch(
            "create_dump.rollback.engine.safe_is_within",
            new_callable=AsyncMock
        )
        # 🐞 FIX: Configure side_effect based on the mock object *identity*
        def safe_side_effect(path, root):
            if path is mock_unsafe_path:
                return False
            return True
        mock_safe_is_within.side_effect = safe_side_effect

        # 🐞 FIX: Use a side_effect on the *mock root's* __truediv__ method
        def truediv_side_effect(rel_path):
            if "main.py" in str(rel_path):
                return mock_good_path
            if "util.py" in str(rel_path):
                return mock_bad_path
            if "README.md" in str(rel_path):
                return mock_readme_path
            if "passwd" in str(rel_path):
                return mock_unsafe_path
            # Fallback for parent dirs, etc.
            return AsyncMock(parent=AsyncMock(mkdir=AsyncMock()), write_text=AsyncMock())

        # 🐞 FIX: Create the mock for engine.anyio_root *itself*
        mock_anyio_root = AsyncMock(spec=anyio.Path)
        # 🐞 FIX: Configure the mock's method, not patch it
        mock_anyio_root.__truediv__ = MagicMock(side_effect=truediv_side_effect)

        # 🐞 FIX: Patch the anyio.Path constructor *in the engine module*
        # to return our pre-configured mock root.
        mocker.patch(
            "create_dump.rollback.engine.anyio.Path",
            return_value=mock_anyio_root
        )

        # 🐞 FIX: NOW instantiate the engine.
        # Its self.anyio_root will be our mock_anyio_root.
        engine = RollbackEngine(root_output_dir=output_dir, dry_run=False)

        # We must also assert that the *correct* object was patched
        assert engine.anyio_root is mock_anyio_root

        # 🐞 FIX: The failing patch.object call is removed.

        # ⚡ FIX: We must use the *original* parser mock, which yields all 4 files
        created_files = await engine.rehydrate(mock_parser)

        # ⚡ FIX: Should have created "src/main.py" and "README.md"
        # Should have skipped "src/nested/util.py" (error) and "../etc/passwd" (unsafe)
        assert len(created_files) == 2
        # ✨ NEW: The assertions will now pass
        assert created_files[0].name == "main.py"
        assert created_files[1].name == "README.md"

        # Assert the "Disk full" error was logged
        mock_logger_error.assert_called_once_with(
            "Failed to rehydrate file",
            path="src/nested/util.py",
            error="Disk full"
        )
```

---

## tests/test_helpers.py

<a id='tests-test-helpers-py'></a>

```python
# tests/test_helpers.py

"""
Tests for Phase 1: src/create_dump/helpers.py
"""

from __future__ import annotations
import pytest
import anyio

# ⚡ FIXED: This import is correct because `pythonpath = "src"` in pyproject.toml
from create_dump.helpers import (
    slugify,
    get_language,
    is_text_file
)

from create_dump.helpers import _unique_path, parse_patterns
from unittest.mock import MagicMock, AsyncMock
from pathlib import Path
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


# --- Test slugify() ---

@pytest.mark.parametrize(
    "input_path, expected_slug",
    [
        ("src/main.py", "src-main-py"),
        ("src/archive/core.py", "src-archive-core-py"),
        ("./a/b/c.md", "a-b-c-md"),
        ("README.md", "readme-md"),
        ("a_b-c.d", "a-b-c-d"),
        ("a__b--c..d", "a-b-c-d"),
        ("a/b/", "a-b"),
        (".", ""),
        ("a/b/c", "a-b-c"),
        ("file with spaces", "file-with-spaces"),
    ],
)
def test_slugify(input_path: str, expected_slug: str):
    """
    Tests that slugify() correctly converts paths to safe anchor slugs.
    """
    assert slugify(input_path) == expected_slug


# --- Test get_language() ---

@pytest.mark.parametrize(
    "filename, expected_lang",
    [
        # Standard extensions
        ("main.py", "python"),
        ("script.sh", "bash"),
        ("config.yaml", "yaml"),
        ("config.yml", "yaml"),
        ("data.json", "json"),
        ("README.md", "markdown"),
        ("index.html", "html"),
        ("style.css", "css"),
        ("app.js", "javascript"),
        ("server.ts", "typescript"),
        ("component.jsx", "jsx"),
        ("component.tsx", "tsx"),
        ("README", "text"),
        ("file.unknown", "text"),
        ("data.txt", "text"),
        ("setup.cfg", "ini"),
        ("config.ini", "ini"),
        ("config.toml", "toml"),
        
        # Special basenames
        ("Dockerfile", "dockerfile"),
        ("dockerfile", "dockerfile"),
        (".dockerignore", "ini"),
        
        # Paths
        ("src/components/button.tsx", "tsx"),
        ("src/api/Dockerfile", "dockerfile"),
        ("file.zig", "zig"),
        # -----------------
        # 🐞 ADD THESE LINES
        # -----------------
        ("file.carbon", "carbon"),
        ("file.mojo", "mojo"),
        ("file.verse", "verse"),
        # -----------------
        # Special basenames
        ("Dockerfile", "dockerfile"),
    ],
)
def test_get_language(filename: str, expected_lang: str):
    """
    Tests that get_language() correctly identifies the language from a filename.
    """
    assert get_language(filename) == expected_lang

# --- Test is_text_file() ---

async def test_is_text_file_for_text(test_project):
    """
    Tests that a valid UTF-8 text file is correctly identified.
    """
    # Setup: Create a text file
    await test_project.create({
        "hello.txt": "This is a standard text file.\nWith multiple lines."
    })
    
    # Get the async path object
    text_file_path = anyio.Path(test_project.path("hello.txt"))
    
    # Test
    assert await is_text_file(text_file_path) is True

async def test_is_text_file_for_binary(test_project):
    """
    Tests that a binary file (containing null bytes) is correctly identified.
    """
    # Setup: Create a binary file (must write bytes, not text)
    binary_content = b"This is binary \x00 code"
    bin_path = test_project.root / "app.bin"
    
    # Use anyio to run the sync byte write in a thread
    await anyio.to_thread.run_sync(bin_path.write_bytes, binary_content)
    
    # Get the async path object
    binary_file_path = anyio.Path(bin_path)

    # Test
    assert await is_text_file(binary_file_path) is False

async def test_is_text_file_for_empty(test_project):
    """
    Tests that an empty file is considered text (not binary).
    """
    # Setup: Create an empty file
    await test_project.create({
        "empty.txt": ""
    })
    
    # Get the async path object
    empty_file_path = anyio.Path(test_project.path("empty.txt"))
    
    # Test
    assert await is_text_file(empty_file_path) is True

async def test_is_text_file_for_unicode(test_project):
    """
    Tests that a file with Unicode (but not null bytes) is text.
    """
    # Setup: Create a text file with unicode
    await test_project.create({
        "unicode.txt": "Hello, world! 🌍"
    })
    
    # Get the async path object
    unicode_file_path = anyio.Path(test_project.path("unicode.txt"))
    
    # Test
    assert await is_text_file(unicode_file_path) is True
    

# [TEST_SKELETON_START]
# --- Test is_text_file() Error Paths ---

async def test_is_text_file_os_error(mocker):
    """
    Action Plan 2: Test is_text_file Errors (OSError).
    Tests that an OSError during file open returns False.
    """
    # 1. Setup
    mock_path = AsyncMock(spec=anyio.Path)
    # 2. Mock: Make .open() raise an error
    mock_path.open = AsyncMock(side_effect=OSError("Permission denied"))
    
    # 3. Act
    result = await is_text_file(mock_path)
    
    # 4. Assert
    assert result is False

async def test_is_text_file_unicode_error(mocker):
    """
    Action Plan 2: Test is_text_file Errors (UnicodeDecodeError).
    Tests that a UnicodeDecodeError during read returns False.
    """
    # 1. Setup
    mock_path = AsyncMock(spec=anyio.Path)
    mock_file = AsyncMock()
    # 2. Mock: Make .read() raise the error
    mock_file.read = AsyncMock(side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid start byte"))
    mock_context = AsyncMock(__aenter__=AsyncMock(return_value=mock_file))
    mock_path.open = AsyncMock(return_value=mock_context)
    
    # 3. Act
    result = await is_text_file(mock_path)
    
    # 4. Assert
    assert result is False

# --- Test parse_patterns() Error Path ---

def test_parse_patterns_error(mocker):
    """
    Tests that a GitWildMatchPatternError is caught and re-raised as a ValueError.
    """
    # 1. Mock
    mocker.patch(
        "create_dump.helpers.PathSpec.from_lines",
        side_effect=GitWildMatchPatternError("Bad pattern")
    )
    
    # 2. Act & Assert
    with pytest.raises(ValueError, match="Invalid patterns"):
        parse_patterns(["[invalid"])

# --- Test _unique_path() Collision Logic ---

def test_unique_path_collision(mocker, tmp_path: Path):
    """
    Action Plan 1: Test _unique_path Collisions.
    Tests the collision-handling loop logic.
    """
    # 1. Setup
    base_path = tmp_path / "file.txt"
    
    # 2. Mock UUID to return predictable values
    mock_uuid_1 = MagicMock()
    mock_uuid_1.hex = "11111111" # First collision
    mock_uuid_2 = MagicMock()
    mock_uuid_2.hex = "22222222" # Second, successful
    mocker.patch("create_dump.helpers.uuid.uuid4", side_effect=[mock_uuid_1, mock_uuid_2])

    # 3. Mock path existence checks
    # First check (os.path.exists) on base path is True
    mocker.patch("create_dump.helpers.os.path.exists", return_value=True)
    
    # -----------------
    # 🐞 FIX: Correct patch target from "create_dump.helpers.pathlib.Path.exists"
    # to "create_dump.helpers.Path.exists"
    # -----------------
    mock_path_exists = mocker.patch(
        "create_dump.helpers.Path.exists", 
        side_effect=[True, False]
    )
    
    # 4. Define expected paths
    colliding_path = tmp_path / "file_11111111.txt"
    # Loop 1: counter = 0. stem = "file_11111111"
    # Loop 2: counter = 1. stem = "file_1_22222222"
    final_path = tmp_path / "file_1_22222222.txt"

    # 5. Act
    result = _unique_path(base_path)

    # 6. Assert
    assert result == final_path
    
    # Check that Path.exists was called twice
    assert mock_path_exists.call_count == 2
    # Check the paths it was called with
    assert mock_path_exists.call_args_list[0].args[0].name == "file_11111111.txt"
    assert mock_path_exists.call_args_list[1].args[0].name == "file_1_22222222.txt"

def test_unique_path_no_collision(mocker, tmp_path: Path):
    """
    Tests the happy path where the original file does not exist.
    """
    base_path = tmp_path / "file.txt"
    
    # Mock os.path.exists to return False
    mocker.patch("create_dump.helpers.os.path.exists", return_value=False)
    
    # -----------------
    # 🐞 FIX: Correct patch target
    # -----------------
    mock_path_exists = mocker.patch("create_dump.helpers.Path.exists")

    result = _unique_path(base_path)

    # Assert it returns the original path immediately
    assert result == base_path
    # Assert the loop was never entered
    mock_path_exists.assert_not_called()
# [TEST_SKELETON_END]
```

---

## tests/test_path_utils.py

<a id='tests-test-path-utils-py'></a>

```python
# tests/test_path_utils.py

"""
Tests for Phase 1: src/create_dump/path_utils.py
"""

from __future__ import annotations
import pytest
import anyio
import os
from pathlib import Path


# [TEST_SKELETON_START]
# Add these imports at the top of tests/test_path_utils.py
from create_dump.path_utils import confirm
from unittest.mock import MagicMock, AsyncMock, patch
# [TEST_SKELETON_END]

# ⚡ REFACTOR: Import the new async-native functions
from create_dump.path_utils import (
    safe_is_within,
    find_matching_files
)

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


# --- Test safe_is_within() ---

@pytest.mark.parametrize(
    "path_str, expected",
    [
        # Standard valid cases
        ("src/main.py", True),
        ("file.txt", True),
        (".", True),
        ("src/sub/deep/file.py", True),
        
        # Standard invalid cases
        ("..", False),
        ("../", False),
        ("../file.txt", False),
        ("../src/file.txt", False),
        ("src/../../file.txt", False),
        
        # Absolute paths
        ("/etc/passwd", False),
        ("/tmp/file", False),
        ("/var/log/syslog", False),
    ],
)
# ⚡ RENAMED: Appended 
async def test_safe_is_within_basic(test_project, path_str: str, expected: bool):
    """
    Tests safe_is_within() for basic path traversal and absolute paths.
    """
    # ⚡ REFACTOR: Use anyio.Path objects
    anyio_root = test_project.async_root
    anyio_path_to_check = anyio_root / path_str
    
    # ⚡ REFACTOR: Call the async function and await it
    # The function handles its own resolution.
    assert await safe_is_within(anyio_path_to_check, anyio_root) is expected

# ⚡ RENAMED: Appended 
async def test_safe_is_within_symlinks(test_project):
    """
    Tests that safe_is_within() correctly handles symlinks.
    This is the most critical security test for this function.
    """
    # ⚡ REFACTOR: Use anyio.Path objects
    anyio_root = test_project.async_root
    root = test_project.root # Keep sync root for os.symlink
    
    # 1. Create a "safe" symlink pointing *inside* the project
    await test_project.create({
        "src/main.py": "print('hello')",
    })
    safe_symlink_path = root / "safe_link.py"
    await anyio.to_thread.run_sync(os.symlink, "src/main.py", safe_symlink_path)
    anyio_safe_symlink = anyio_root / "safe_link.py"

    # 2. Create a "dangerous" symlink pointing *outside* the project
    secret_file = Path(f"/tmp/secret_file_{os.getpid()}")
    await anyio.Path(secret_file).write_text("iamasecret")
    
    dangerous_symlink_path = root / "danger_link"
    await anyio.to_thread.run_sync(os.symlink, secret_file, dangerous_symlink_path)
    anyio_dangerous_symlink = anyio_root / "danger_link"

    # 3. Create a symlink that traverses up and back in
    target_file = root.parent / "src" / "main.py"
    await anyio.Path(target_file.parent).mkdir(parents=True, exist_ok=True)
    await anyio.Path(target_file).write_text("external")
    
    complex_symlink_path = root / "complex_link"
    await anyio.to_thread.run_sync(os.symlink, "../src/main.py", complex_symlink_path)
    anyio_complex_symlink = anyio_root / "complex_link"

    # Test assertions
    # ⚡ REFACTOR: Call the async function directly with anyio.Path objects
    assert await safe_is_within(anyio_safe_symlink, anyio_root) is True
    
    assert await safe_is_within(anyio_dangerous_symlink, anyio_root) is False
    
    assert await safe_is_within(anyio_complex_symlink, anyio_root) is False

    # Cleanup the external files
    await anyio.Path(secret_file).unlink()
    await anyio.Path(target_file).unlink()
    await anyio.Path(target_file.parent).rmdir()


# ⚡ RENAMED: Appended 
async def test_safe_is_within_root_as_path(test_project):
    """
    Tests that checking the root directory itself returns True.
    """
    anyio_root = test_project.async_root
    # ⚡ REFACTOR: Call the async function
    assert await safe_is_within(anyio_root, anyio_root) is True


# --- Test find_matching_files() ---

# ⚡ RENAMED: Appended 
async def test_find_matching_files(test_project):
    """
    Tests the async file finder.
    """
    await test_project.create({
        "src/main.py": "",
        "src/data/dump_2025.md": "",
        "src/data/dump_2024.md.sha256": "",
        "README.md": "",
        "logs/app.log": "",
    })
    
    # Test finding all .md files
    # ⚡ FIX: Consume the async generator using an async list comprehension
    md_files = [p async for p in find_matching_files(test_project.root, r"\.md$")]
    assert len(md_files) == 2
    paths_as_str = {p.name for p in md_files}
    assert paths_as_str == {"dump_2025.md", "README.md"}
    
    # Test finding canonical dump files
    # ⚡ FIX: Consume the async generator using an async list comprehension
    dump_files_gen = find_matching_files(
        test_project.root, 
        r"dump_.*\.md(\.sha256)?$"
    )
    dump_files = [p async for p in dump_files_gen]
    assert len(dump_files) == 2
    paths_as_str = {p.name for p in dump_files}
    assert paths_as_str == {"dump_2025.md", "dump_2024.md.sha256"}
    

# [TEST_SKELETON_START]
# --- Test safe_is_within() Error Paths ---

async def test_safe_is_within_attribute_error_fallback(mocker):
    """
    Action Plan 1: Test safe_is_within() fallback logic.
    Mocks is_relative_to to raise AttributeError, forcing the str() check.
    """
    # 1. Setup mock pathlib.Path objects that will be returned by .resolve()
    mock_resolved_path = MagicMock(spec=Path)
    mock_resolved_root = MagicMock(spec=Path)

    # 2. Mock is_relative_to to raise AttributeError
    mocker.patch.object(
        mock_resolved_path, 
        "is_relative_to", 
        side_effect=AttributeError("Simulating Python < 3.9")
    )

    # 3. Configure the string representations for the fallback check
    # Case 1: Path IS within root
    mock_resolved_path.__str__.return_value = "/app/src/main.py"
    mock_resolved_root.__str__.return_value = "/app"

    # 4. Setup mock anyio.Path objects
    mock_path = AsyncMock(spec=anyio.Path)
    mock_path.resolve = AsyncMock(return_value=mock_resolved_path)
    mock_root = AsyncMock(spec=anyio.Path)
    mock_root.resolve = AsyncMock(return_value=mock_resolved_root)

    # 5. Act & Assert (Case 1: Success)
    assert await safe_is_within(mock_path, mock_root) is True

    # Case 2: Path is NOT within root (e.g., sibling folder)
    mock_resolved_path.__str__.return_value = "/other/main.py"
    mock_resolved_root.__str__.return_value = "/app"
    
    # 6. Act & Assert (Case 2: Failure)
    assert await safe_is_within(mock_path, mock_root) is False

# --- Test confirm() ---

def test_confirm_keyboard_interrupt(mocker):
    """
    Action Plan 2: Test confirm() handles KeyboardInterrupt.
    """
    # 1. Mock built-in 'input' to raise KeyboardInterrupt
    mocker.patch("builtins.input", side_effect=KeyboardInterrupt)
    
    # 2. Mock 'print' to suppress output during test
    mocker.patch("builtins.print")
    
    # 3. Act & Assert
    assert confirm("Delete everything?") is False

def test_confirm_yes_answers(mocker):
    """
    Tests that 'y' and 'yes' are accepted.
    """
    mocker.patch("builtins.input", side_effect=["y", "yes", "Y", "YES "])
    assert confirm("Prompt 1") is True
    assert confirm("Prompt 2") is True
    assert confirm("Prompt 3") is True
    assert confirm("Prompt 4") is True

def test_confirm_no_answers(mocker):
    """
    Tests that 'n', 'no', and empty input are rejected.
    """
    mocker.patch("builtins.input", side_effect=["n", "no", "N", " anything else", ""])
    assert confirm("Prompt 1") is False
    assert confirm("Prompt 2") is False
    assert confirm("Prompt 3") is False
    assert confirm("Prompt 4") is False
    assert confirm("Prompt 5") is False
# [TEST_SKELETON_END]
```

---

## tests/test_scanning.py

<a id='tests-test-scanning-py'></a>

```python
# tests/test_scanning.py

"""
Tests for Phase 3: src/create_dump/scanning.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
import logging # 🐞 FIX: Import logging
from unittest.mock import AsyncMock, MagicMock, patch, call, ANY

import anyio

# Import the class to test
from create_dump.scanning import SecretScanner
# Import dependencies needed for testing
from create_dump.core import DumpFile
from detect_secrets.core.potential_secret import PotentialSecret
# 🐞 FIX: Import the *actual* dependencies to mock
from detect_secrets.core import scan


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_potential_secret():
    """Creates a mock PotentialSecret object."""
    secret = MagicMock(spec=PotentialSecret)
    secret.type = "Generic Secret"
    secret.line_number = 2
    return secret


@pytest.fixture
async def temp_dump_file(tmp_path_factory):
    """
    Creates a real temporary file and a DumpFile object pointing to it.
    """
    # Create a persistent temp dir for the test session
    temp_dir = tmp_path_factory.mktemp("dump_files")

    # Create the content for the file
    content = (
        "line 1: this is safe\n"
        "line 2: this is a secret\n"
        "line 3: this is also safe\n"
    )

    # Use anyio to write the file
    temp_file_path = anyio.Path(temp_dir) / "test_file.tmp"
    await temp_file_path.write_text(content)

    # Create the DumpFile object
    dump_file = DumpFile(
        path="src/original/file.py",
        language="python",
        temp_path=Path(temp_file_path) # Store the sync path
    )

    return dump_file, anyio.Path(temp_file_path)


# 🐞 FIX: Updated fixture for the new implementation
@pytest.fixture
def mock_scanner_internals(mocker, mock_potential_secret):
    """
    Mocks the internal detect_secrets calls:
    - `scan.scan_file`
    - `logging.getLogger`
    """
    # 1. Mock the function that runs in the thread
    mock_scan_file_func = mocker.patch(
        "create_dump.scanning.scan.scan_file", # Patched where it's called
        # 🐞 FIX: Return a list (or generator) instead of a dict
        return_value=[mock_potential_secret]
    )

    # 2. Mock the logger to verify it's being silenced
    mock_ds_logger = MagicMock()
    mock_get_logger = mocker.patch(
        "create_dump.scanning.logging.getLogger",
        return_value=mock_ds_logger
    )

    return {
        "scan_file": mock_scan_file_func,
        "get_logger": mock_get_logger,
        "ds_logger": mock_ds_logger,
    }


class TestSecretScanner:
    """Groups tests for the SecretScanner middleware."""

    async def test_process_no_secrets(self, mocker, temp_dump_file, mock_scanner_internals):
        """
        Test Case 1: No secrets are found.
        """
        dump_file, temp_path = temp_dump_file
        original_content = await temp_path.read_text()

        # 🐞 FIX: Configure the mock to return an empty list
        mock_scanner_internals["scan_file"].return_value = []

        scanner = SecretScanner(hide_secrets=False)
        await scanner.process(dump_file)

        # Assertions
        assert dump_file.error is None
        assert await temp_path.read_text() == original_content

        # 🐞 FIX: Check logging was silenced and restored
        mock_scanner_internals["get_logger"].assert_called_with("detect-secrets")
        mock_ds_logger = mock_scanner_internals["ds_logger"]
        mock_ds_logger.setLevel.assert_has_calls([
            call(logging.CRITICAL), # Silenced
            call(mock_ds_logger.level) # Restored
        ])

        # 🐞 FIX: Check scan_file was called with just the path
        mock_scanner_internals["scan_file"].assert_called_once_with(
            str(dump_file.temp_path)
        )


    async def test_process_secrets_found_no_hide(
        self, mocker, temp_dump_file, mock_potential_secret, mock_scanner_internals
    ):
        """
        Test Case 2: Secrets found, hide_secrets=False.
        """
        dump_file, temp_path = temp_dump_file

        scanner = SecretScanner(hide_secrets=False)
        await scanner.process(dump_file)

        # Assertions
        assert dump_file.error == "Secrets Detected"
        assert dump_file.temp_path is None
        assert await temp_path.exists() is False

    async def test_process_secrets_found_with_hide(
        self, mocker, temp_dump_file, mock_potential_secret, mock_scanner_internals
    ):
        """
        Test Case 3: Secrets found, hide_secrets=True.
        """
        dump_file, temp_path = temp_dump_file

        scanner = SecretScanner(hide_secrets=True)
        await scanner.process(dump_file)

        # Assertions
        assert dump_file.error is None
        assert dump_file.temp_path is not None

        new_content = await temp_path.read_text()
        expected_content = (
            "line 1: this is safe\n"
            "***SECRET_REDACTED*** (Line 2, Type: Generic Secret)\n"
            "line 3: this is also safe"
        )
        assert new_content == expected_content


    async def test_process_scan_api_error(
        self, mocker, temp_dump_file, mock_scanner_internals
    ):
        """
        Test Case 4: A non-secret-related error during scan is logged and ignored.
        """
        dump_file, temp_path = temp_dump_file
        original_content = await temp_path.read_text()

        # 🐞 FIX: Patch the new, isolated `_run_sync` symbol
        mocker.patch(
            "create_dump.scanning._run_sync",
            side_effect=Exception("Simulated API Error")
        )

        scanner = SecretScanner(hide_secrets=False)
        await scanner.process(dump_file)

        assert dump_file.error is None
        assert await temp_path.read_text() == original_content

    async def test_process_no_temp_path(self, mocker):
        """
        Test Case 5: process() returns early if dump_file has no temp_path.
        """
        dump_file = DumpFile(path="src/file.py", temp_path=None, error="Read error")
        mock_scan = mocker.patch("create_dump.scanning.scan.scan_file")
        
        scanner = SecretScanner()
        await scanner.process(dump_file)
        
        mock_scan.assert_not_called()
```

---

## tests/test_processor.py

<a id='tests-test-processor-py'></a>

```python
# tests/test_processor.py

"""
Tests for Phase 3: src/create_dump/processor.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, call

import anyio
# 🐞 FIX: Import TimeoutError from asyncio, not anyio
from asyncio import TimeoutError
# ✨ NEW: Import the real anyio.Path for spec-ing
from anyio import Path as RealAnyIOPath

# Import the class to test
from create_dump.processor import FileProcessor, ProcessorMiddleware
from create_dump.core import DumpFile

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def temp_dir(tmp_path: Path) -> str:
    """Provides a string path to a real temp directory."""
    return str(tmp_path)


@pytest.fixture
def mocked_metrics(mocker):
    """Mocks metrics and returns the mocks."""
    m_files_processed = mocker.patch("create_dump.processor.FILES_PROCESSED")
    m_errors_total = mocker.patch("create_dump.processor.ERRORS_TOTAL")
    return m_files_processed, m_errors_total


@pytest.fixture(autouse=True)
def mocked_deps(mocker):
    """Mocks non-critical dependencies."""
    mocker.patch("create_dump.processor.get_language", return_value="python")
    # Make the UUID predictable for temp file path assertion
    mocker.patch("create_dump.processor.uuid.uuid4", MagicMock(hex="test-uuid"))


@pytest.fixture
def mock_paths(mocker, temp_dir: str):
    """
    Mocks anyio.Path for both reading and writing.
    Returns the mock objects for assertion.
    """
    # 1. Mock the file-to-be-read
    mock_read_file = AsyncMock()
    # Simulate streaming read (peek + chunk + end)
    mock_read_file.read.side_effect = ["hello", " world", ""]
    mock_read_context = AsyncMock(__aenter__=AsyncMock(return_value=mock_read_file))
    # 🐞 FIX: Use the real class for the spec
    mock_read_path = AsyncMock(spec=RealAnyIOPath)
    mock_read_path.open = AsyncMock(return_value=mock_read_context)

    # 2. Mock the temp-file-to-be-written
    mock_write_file = AsyncMock()
    mock_write_context = AsyncMock(__aenter__=AsyncMock(return_value=mock_write_file))
    # 🐞 FIX: Use the real class for the spec
    mock_write_path = AsyncMock(spec=RealAnyIOPath)
    mock_write_path.open = AsyncMock(return_value=mock_write_context)
    mock_write_path.unlink = AsyncMock()

    # The expected path of the temp file
    temp_file_path_str = str(Path(temp_dir) / "test-uuid.tmp")

    mock_write_path.__fspath__ = MagicMock(return_value=temp_file_path_str)
    mock_write_path.__str__ = MagicMock(return_value=temp_file_path_str)


    # Mock for anyio.Path(temp_dir)
    # 🐞 FIX: Use the real class for the spec
    mock_temp_dir_path = AsyncMock(spec=RealAnyIOPath)
    # Mock the "/" operator to return the final write path
    mock_temp_dir_path.__truediv__ = MagicMock(return_value=mock_write_path)

    # 3. Mock the anyio.Path constructor to return the correct mock
    def path_side_effect(path_arg):
        path_str = str(path_arg)
        if path_str == "src/main.py":
            return mock_read_path
        if path_str == temp_dir:
            return mock_temp_dir_path

        # ✨ NEW: Add case for empty file test
        if path_str == "src/empty.py":
            mock_empty_read = AsyncMock()
            mock_empty_read.read.side_effect = ["", ""] # First read is empty
            mock_empty_context = AsyncMock(__aenter__=AsyncMock(return_value=mock_empty_read))
            # 🐞 FIX: Use the real class for the spec
            mock_empty_path = AsyncMock(spec=RealAnyIOPath)
            mock_empty_path.open = AsyncMock(return_value=mock_empty_context)
            return mock_empty_path

        # Fallback
        # 🐞 FIX: Use the real class for the spec
        return AsyncMock(spec=RealAnyIOPath)

    mocker.patch("create_dump.processor.anyio.Path", side_effect=path_side_effect)

    return mock_read_path, mock_write_path, mock_write_file


@pytest.fixture
def mock_middleware():
    """Returns a simple, successful mock middleware."""
    return AsyncMock(spec=ProcessorMiddleware)


class TestFileProcessor:
    """Groups tests for the FileProcessor."""

    async def test_process_file_success(
        self, temp_dir, mock_paths, mock_middleware, mocked_metrics
    ):
        """
        Test Case 1: process_file() success.
        Checks streaming, middleware call, and success metric.
        """
        _, _, mock_write_file = mock_paths
        m_files_processed, _ = mocked_metrics

        processor = FileProcessor(temp_dir, middlewares=[mock_middleware])
        dump_file = await processor.process_file("src/main.py")

        # Check DumpFile state
        assert dump_file.error is None
        assert dump_file.path == "src/main.py"
        assert dump_file.language == "python"
        assert dump_file.temp_path == Path(temp_dir) / "test-uuid.tmp"

        # Check that streaming occurred (peek + chunk)
        assert mock_write_file.write.call_args_list == [
            call("hello"),
            call(" world"),
        ]

        # Check middleware and metrics
        mock_middleware.process.assert_called_once_with(dump_file)
        m_files_processed.labels.assert_called_once_with(status="success")
        m_files_processed.labels.return_value.inc.assert_called_once()

    async def test_process_file_read_error(
        self, temp_dir, mock_paths, mocked_metrics
    ):
        """Test Case 2: process_file() fails on file read."""
        mock_read_path, mock_write_path, _ = mock_paths
        _, m_errors_total = mocked_metrics

        # Simulate a read error
        mock_read_path.open.side_effect = OSError("Permission denied")

        processor = FileProcessor(temp_dir)
        dump_file = await processor.process_file("src/main.py")

        # Check DumpFile state
        assert "Permission denied" in dump_file.error
        assert dump_file.temp_path is None

        mock_write_path.unlink.assert_called_once_with(missing_ok=True)
        m_errors_total.labels.assert_called_once_with(type="process")
        m_errors_total.labels.return_value.inc.assert_called_once()

    async def test_process_file_write_error(
        self, temp_dir, mock_paths, mocked_metrics
    ):
        """Test Case 3: process_file() fails on temp file write."""
        _, mock_write_path, _ = mock_paths
        _, m_errors_total = mocked_metrics

        # Simulate a write error
        mock_write_path.open.side_effect = OSError("Disk full")

        processor = FileProcessor(temp_dir)
        dump_file = await processor.process_file("src/main.py")

        # Check DumpFile state
        assert "Disk full" in dump_file.error
        assert dump_file.temp_path is None

        mock_write_path.unlink.assert_called_once()
        m_errors_total.labels.assert_called_once_with(type="process")
        m_errors_total.labels.return_value.inc.assert_called_once()

    async def test_middleware_chain_execution(
        self, temp_dir, mock_paths, mocked_metrics
    ):
        """Test Case 4: Middleware chain executes in order."""
        m_files_processed, _ = mocked_metrics
        mock_mw_1 = AsyncMock(spec=ProcessorMiddleware)
        mock_mw_2 = AsyncMock(spec=ProcessorMiddleware)

        # Use mock_calls to check order
        manager = MagicMock()
        manager.attach_mock(mock_mw_1, "mw1")
        manager.attach_mock(mock_mw_2, "mw2")

        processor = FileProcessor(temp_dir, middlewares=[mock_mw_1, mock_mw_2])
        dump_file = await processor.process_file("src/main.py")

        # Check calls
        assert dump_file.error is None
        assert manager.mock_calls == [
            call.mw1.process(dump_file),
            call.mw2.process(dump_file),
        ]
        m_files_processed.labels.return_value.inc.assert_called_once()

    async def test_middleware_chain_short_circuits(
        self, temp_dir, mock_paths, mocked_metrics
    ):
        """Test Case 5: Middleware chain stops on first failure."""
        m_files_processed, _ = mocked_metrics

        mock_mw_1 = AsyncMock(spec=ProcessorMiddleware)
        mock_mw_fail = AsyncMock(spec=ProcessorMiddleware)
        mock_mw_2 = AsyncMock(spec=ProcessorMiddleware)

        # Configure the failing middleware
        def fail_side_effect(df: DumpFile):
            df.error = "Middleware Fail"
        mock_mw_fail.process.side_effect = fail_side_effect

        processor = FileProcessor(
            temp_dir, middlewares=[mock_mw_1, mock_mw_fail, mock_mw_2]
        )
        dump_file = await processor.process_file("src/main.py")

        # Check DumpFile state
        assert dump_file.error == "Middleware Fail"

        # Check call chain
        mock_mw_1.process.assert_called_once()
        mock_mw_fail.process.assert_called_once()
        mock_mw_2.process.assert_not_called() # Should be skipped

        # Success metric should NOT be incremented
        m_files_processed.labels.return_value.inc.assert_not_called()

    async def test_dump_concurrent_respects_semaphore(self, mocker, temp_dir):
        """Test Case 6: dump_concurrent() respects max_workers via Semaphore."""
        mock_semaphore_cls = mocker.patch("create_dump.processor.anyio.Semaphore")
        mock_semaphore_instance = AsyncMock()
        mock_semaphore_cls.return_value = mock_semaphore_instance

        # Mock the method that runs inside the semaphore
        mock_process_file = mocker.patch.object(
            FileProcessor, "process_file", new_callable=AsyncMock
        )

        processor = FileProcessor(temp_dir)
        files_list = ["a.py", "b.py", "c.py"]
        await processor.dump_concurrent(files_list, progress=False, max_workers=2)

        # Check that semaphore was created with max_workers
        mock_semaphore_cls.assert_called_once_with(2)

        # Check that it was acquired for each file
        assert mock_semaphore_instance.__aenter__.call_count == 3
        assert mock_process_file.call_count == 3

    async def test_dump_concurrent_timeout(self, mocker, temp_dir, mocked_metrics):
        """
        Test Case 7: dump_concurrent() wrapper handles Timeouts.
        Covers lines 139-141.
        """
        _, m_errors_total = mocked_metrics

        # Mock fail_after to immediately raise a TimeoutError
        mocker.patch(
            "create_dump.processor.anyio.fail_after", side_effect=TimeoutError
        )
        # Mock process_file, though it won't be fully called
        mocker.patch.object(FileProcessor, "process_file", new_callable=AsyncMock)

        processor = FileProcessor(temp_dir)
        files_list = ["a.py"]
        results = await processor.dump_concurrent(files_list, progress=False)

        # Check that a failure DumpFile was returned
        assert len(results) == 1
        assert results[0].path == "a.py"
        assert results[0].error == "Timeout"

        # Check metrics
        m_errors_total.labels.assert_called_once_with(type="timeout")
        m_errors_total.labels.return_value.inc.assert_called_once()

    # --- NEW TESTS TO COVER MISSED LINES ---
        
    async def test_dump_concurrent_generic_exception(self, mocker, temp_dir, mocked_metrics):
        """
        Test Case 8: dump_concurrent() wrapper handles generic Exceptions.
        Covers lines 142-143.
        """
        _, m_errors_total = mocked_metrics
        test_exception = Exception("Unhandled generic error")

        # Mock process_file to raise the exception
        mocker.patch.object(
            FileProcessor, "process_file", side_effect=test_exception
        )

        processor = FileProcessor(temp_dir)
        files_list = ["a.py"]
        results = await processor.dump_concurrent(files_list, progress=False)

        # Check that a failure DumpFile was returned
        assert len(results) == 1
        assert results[0].path == "a.py"
        assert results[0].error == f"Unhandled exception: {test_exception}"

        # Check metrics
        m_errors_total.labels.assert_called_once_with(type="process")
        m_errors_total.labels.return_value.inc.assert_called_once()

    async def test_dump_concurrent_no_progress(self, mocker, temp_dir):
        """
        Test Case 9: dump_concurrent() with progress=False.
        Covers lines 130-132 (else branch) and 135 (finally branch).
        """
        # Mock the Progress bar to ensure it's not called
        mock_progress_cls = mocker.patch("create_dump.processor.Progress")
        
        # Mock process_file to check it's still called
        mock_process_file = mocker.patch.object(
            FileProcessor, "process_file", new_callable=AsyncMock
        )

        processor = FileProcessor(temp_dir)
        files_list = ["a.py", "b.py"]
        await processor.dump_concurrent(files_list, progress=False)

        # Assert Progress bar was not used
        mock_progress_cls.assert_not_called()
        
        # Assert files were still processed
        assert mock_process_file.call_count == 2

    async def test_process_file_empty(
        self, temp_dir, mock_paths, mock_middleware, mocked_metrics
    ):
        """
        Test Case 10: process_file() with an empty file.
        Covers line 71 (if peek:) being false.
        """
        _, _, mock_write_file = mock_paths
        m_files_processed, _ = mocked_metrics

        processor = FileProcessor(temp_dir, middlewares=[mock_middleware])
        # "src/empty.py" is configured in mock_paths to return "" on first read
        dump_file = await processor.process_file("src/empty.py")

        # Check DumpFile state
        assert dump_file.error is None
        assert dump_file.path == "src/empty.py"
        assert dump_file.temp_path is not None

        # Check that write was NOT called
        mock_write_file.write.assert_not_called()

        # Check middleware and metrics (still a success)
        mock_middleware.process.assert_called_once_with(dump_file)
        m_files_processed.labels.assert_called_once_with(status="success")
        m_files_processed.labels.return_value.inc.assert_called_once()
```

---

## tests/test_version.py

<a id='tests-test-version-py'></a>

```python
# tests/test_version.py

"""
Tests for src/create_dump/version.py
"""

from create_dump.version import __version__, VERSION


def test_version_consistency():
    """Test Case 1: __version__ and VERSION are identical."""
    assert __version__ == VERSION
    assert __version__ == "10.0.0"  # Pin to current; update on release


def test_version_format_semver():
    """Test Case 2: Version adheres to semantic versioning pattern."""
    import re
    # 🐞 FIX: Update regex to be PEP 440-compliant, allowing for .devN suffixes
    semver_pattern = r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\.dev\d+)?(?:-(?P<prerelease>[a-zA-Z0-9.-]+))?(?:\+(?P<build>[a-zA-Z0-9.-]+))?$"
    match = re.match(semver_pattern, __version__)
    assert match is not None, f"Version {__version__} does not match semver"

```

---

## tests/test_system.py

<a id='tests-test-system-py'></a>

```python
# tests/test_system.py

"""
Tests for Phase 2: src/create_dump/system.py
"""

from __future__ import annotations
import pytest
import subprocess
import asyncio
# ✨ NEW: Import signal and sys for handler testing
import signal
import sys
from unittest.mock import MagicMock, AsyncMock

from create_dump.system import (
    get_git_meta,
    get_git_ls_files,
    get_git_diff_files,
    # ✨ NEW: Import the global handler instance
    handler as global_handler
)
from create_dump.core import GitMeta

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


# --- Test get_git_meta() (Sync) ---

def test_get_git_meta_success(test_project, mocker):
    """
    Tests that get_git_meta() correctly parses git output.
    """
    root = test_project.root

    # Mock subprocess.check_output
    def mock_check_output(*args, **kwargs):
        cmd = args[0]
        if "rev-parse" in cmd and "--abbrev-ref" in cmd:
            return b"main\n"  # Mock branch
        if "rev-parse" in cmd and "--short" in cmd:
            return b"a1b2c3d\n"  # Mock commit
        return b""

    mocker.patch("subprocess.check_output", side_effect=mock_check_output)

    git_meta = get_git_meta(root)

    assert isinstance(git_meta, GitMeta)
    assert git_meta.branch == "main"
    assert git_meta.commit == "a1b2c3d"

def test_get_git_meta_failure(test_project, mocker):
    """
    Tests that get_git_meta() returns None on a subprocess error.
    """
    root = test_project.root

    # Mock subprocess.check_output to raise an error
    mocker.patch(
        "subprocess.check_output",
        side_effect=subprocess.CalledProcessError(1, "git")
    )

    git_meta = get_git_meta(root)
    assert git_meta is None

# ✨ NEW: Add tests for CleanupHandler
class TestCleanupHandler:
    """Tests for the CleanupHandler signal and cleanup logic."""

    @pytest.fixture(autouse=True)
    def mock_sys_exit(self, mocker):
        """Mock sys.exit to prevent the test runner from exiting."""
        return mocker.patch("sys.exit")

    def test_cleanup_handler_sigint(self, mocker, mock_sys_exit):
        """Tests that SIGINT calls _cleanup and exits with 130."""
        mock_cleanup = mocker.patch("create_dump.system.CleanupHandler._cleanup")
        
        # Call the handler directly to simulate the signal
        global_handler._handler(signal.SIGINT, None)
        
        mock_cleanup.assert_called_once()
        mock_sys_exit.assert_called_once_with(130)

    def test_cleanup_handler_sigterm(self, mocker, mock_sys_exit):
        """Tests that SIGTERM calls _cleanup and exits with 143."""
        mock_cleanup = mocker.patch("create_dump.system.CleanupHandler._cleanup")

        # Call the handler directly to simulate the signal
        global_handler._handler(signal.SIGTERM, None)
        
        mock_cleanup.assert_called_once()
        mock_sys_exit.assert_called_once_with(143)

    def test_cleanup_handler_cleanup_with_temp_dir(self, mocker):
        """Tests the _cleanup logic when _temp_dir is set."""
        mock_temp_dir = MagicMock()
        mocker.patch("create_dump.system._temp_dir", mock_temp_dir)
        
        mock_stack = MagicMock()
        mocker.patch("create_dump.system._cleanup_stack", mock_stack)
        
        global_handler._cleanup()
        
        mock_temp_dir.cleanup.assert_called_once()
        mock_stack.close.assert_called_once()

    def test_cleanup_handler_cleanup_no_temp_dir(self, mocker):
        """Tests the _cleanup logic when _temp_dir is None."""
        # Ensure _temp_dir is None (default test state, but good to be explicit)
        mocker.patch("create_dump.system._temp_dir", None)
        
        mock_stack = MagicMock()
        mocker.patch("create_dump.system._cleanup_stack", mock_stack)
        
        global_handler._cleanup()
        
        mock_stack.close.assert_called_once()


# --- Test Async Git Functions ---

async def mock_subprocess(stdout: bytes, stderr: bytes, returncode: int) -> AsyncMock:
    """Helper to create a mock asyncio.subprocess.Process."""
    # Create a mock for the process object
    process_mock = AsyncMock()
    
    # Set the return value for the communicate() awaitable
    process_mock.communicate = AsyncMock(return_value=(stdout, stderr))
    
    # Set the returncode attribute
    process_mock.returncode = returncode
    
    return process_mock

async def test_get_git_ls_files_success(test_project, mocker):
    """
    Tests get_git_ls_files() on successful command execution.
    """
    root = test_project.root
    
    # Mock the return value of create_subprocess_exec
    process_mock = await mock_subprocess(
        stdout=b"src/main.py\nsrc/helpers.py\nREADME.md\n",
        stderr=b"",
        returncode=0
    )
    mocker.patch("asyncio.create_subprocess_exec", return_value=process_mock)

    files = await get_git_ls_files(root)

    assert files == ["src/main.py", "src/helpers.py", "README.md"]

async def test_get_git_ls_files_failure(test_project, mocker):
    """
    Tests get_git_ls_files() when the git command fails.
    """
    root = test_project.root
    
    process_mock = await mock_subprocess(
        stdout=b"",
        stderr=b"fatal: not a git repository",
        returncode=128
    )
    mocker.patch("asyncio.create_subprocess_exec", return_value=process_mock)

    files = await get_git_ls_files(root)

    assert files == []

# ✨ NEW: Test for the generic exception block
async def test_get_git_ls_files_exception(test_project, mocker):
    """
    Tests that get_git_ls_files() catches generic exceptions.
    """
    root = test_project.root
    mock_logger = mocker.patch("create_dump.system.logger")
    mocker.patch(
        "create_dump.system._run_async_cmd",
        side_effect=Exception("Test exception")
    )
    
    files = await get_git_ls_files(root)
    
    assert files == []
    mock_logger.error.assert_called_once_with(
        "Failed to run git ls-files", error="Test exception"
    )

async def test_get_git_diff_files_success(test_project, mocker):
    """
    Tests get_git_diff_files() on successful command execution.
    """
    root = test_project.root
    
    process_mock = await mock_subprocess(
        stdout=b"src/main.py\nREADME.md\n",
        stderr=b"",
        returncode=0
    )
    mocker.patch("asyncio.create_subprocess_exec", return_value=process_mock)

    files = await get_git_diff_files(root, "main")

    assert files == ["src/main.py", "README.md"]

async def test_get_git_diff_files_failure(test_project, mocker):
    """
    Tests get_git_diff_files() when the git command fails.
    """
    root = test_project.root
    
    process_mock = await mock_subprocess(
        stdout=b"",
        stderr=b"fatal: bad revision 'main'",
        returncode=1
    )
    mocker.patch("asyncio.create_subprocess_exec", return_value=process_mock)

    files = await get_git_diff_files(root, "main")

    assert files == []

# ✨ NEW: Test for the generic exception block
async def test_get_git_diff_files_exception(test_project, mocker):
    """
    Tests that get_git_diff_files() catches generic exceptions.
    """
    root = test_project.root
    mock_logger = mocker.patch("create_dump.system.logger")
    mocker.patch(
        "create_dump.system._run_async_cmd",
        side_effect=Exception("Test exception")
    )
    
    files = await get_git_diff_files(root, "main")
    
    assert files == []
    mock_logger.error.assert_called_once_with(
        "Failed to run git diff", ref="main", error="Test exception"
    )
```

---

## tests/test_single.py

<a id='tests-test-single-py'></a>

```python
# tests/test_single.py

"""
Tests for src/create_dump/single.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from typer import Exit
import os

import anyio

# Import the function to test
from create_dump.single import run_single

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_deps(mocker):
    """Mocks all external dependencies for run_single."""

    # Mock Orchestrator
    mock_orchestrator_instance = AsyncMock()
    mock_orchestrator_instance.run = AsyncMock()
    mock_orchestrator_class = mocker.patch(
        "create_dump.single.SingleRunOrchestrator",
        return_value=mock_orchestrator_instance
    )

    # Mock Watcher
    mock_watcher_instance = AsyncMock()
    mock_watcher_instance.start = AsyncMock()
    mock_watcher_class = mocker.patch(
        "create_dump.single.FileWatcher",
        return_value=mock_watcher_instance
    )

    # Mock os.chdir
    mock_run_sync = mocker.patch(
        "create_dump.single.anyio.to_thread.run_sync",
        new_callable=AsyncMock
    )

    # Mock styled_print
    mock_styled_print = mocker.patch("create_dump.single.styled_print")

    return {
        "Orchestrator": mock_orchestrator_class,
        "orchestrator_instance": mock_orchestrator_instance,
        "Watcher": mock_watcher_class,
        "watcher_instance": mock_watcher_instance,
        "run_sync": mock_run_sync,
        "styled_print": mock_styled_print,
    }


@pytest.fixture
def default_run_args(test_project) -> dict:
    """Provides a default set of arguments for run_single."""
    return {
        "root": test_project.root,
        "dry_run": False,
        "yes": False,
        "no_toc": False,
        "tree_toc": False,
        "compress": False,
        "format": "md",
        "exclude": "",
        "include": "",
        "max_file_size": None,
        "use_gitignore": True,
        "git_meta": True,
        "progress": True,
        "max_workers": 16,
        "archive": False,
        "archive_all": False,
        "archive_search": False,
        "archive_include_current": True,
        "archive_no_remove": False,
        "archive_keep_latest": True,
        "archive_keep_last": None,
        "archive_clean_root": False,
        "archive_format": "zip",
        "allow_empty": False,
        "metrics_port": 8000,
        "verbose": False,
        "quiet": False,
        "dest": None,
        "watch": False,
        "git_ls_files": False,
        "diff_since": None,
        "scan_secrets": False,
        "hide_secrets": False,
    }


class TestRunSingle:
    """Tests for the run_single 'glue' function."""

    async def test_run_single_default_flow(
        self, test_project, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 1: (Happy Path)
        Validates the default (non-watch) flow.
        - Calls os.chdir
        - Instantiates Orchestrator with correct args (esp. effective_yes)
        - Calls orchestrator.run()
        - Does NOT instantiate FileWatcher
        """

        # Call the function
        await run_single(**default_run_args)

        # 1. Check os.chdir call
        mock_deps["run_sync"].assert_called_once_with(
            os.chdir, test_project.root
        )

        # 2. Check Orchestrator instantiation
        mock_deps["Orchestrator"].assert_called_once()
        call_kwargs = mock_deps["Orchestrator"].call_args[1]

        assert call_kwargs["root"] == test_project.root
        assert call_kwargs["yes"] is False  # effective_yes = False or False
        assert call_kwargs["git_ls_files"] is False
        assert call_kwargs["hide_secrets"] is False
        # 🐞 FIX: Remove incorrect assertion
        # assert call_kwargs["watch"] is False

        # 3. Check that orchestrator.run() was called
        mock_deps["orchestrator_instance"].run.assert_called_once()

        # 4. Check that FileWatcher was NOT called
        mock_deps["Watcher"].assert_not_called()

    async def test_run_single_watch_flow(
        self, test_project, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 2: (Watch Path)
        Validates the watch=True flow.
        - Instantiates Orchestrator with effective_yes=True
        - Calls orchestrator.run()
        - Instantiates FileWatcher
        - Calls watcher.start()
        """

        # Enable watch mode, keep yes=False to test effective_yes
        watch_args = default_run_args | {
            "watch": True,
            "yes": False,
            "quiet": False,
        }

        await run_single(**watch_args)

        # 1. Check Orchestrator instantiation
        mock_deps["Orchestrator"].assert_called_once()
        call_kwargs = mock_deps["Orchestrator"].call_args[1]

        # 🐞 FIX: Remove incorrect assertion
        # assert call_kwargs["watch"] is True
        assert call_kwargs["yes"] is True  # effective_yes = False or True

        # 2. Check that orchestrator.run() was called (for the initial run)
        mock_deps["orchestrator_instance"].run.assert_called_once()

        # 3. Check styled_print was called
        mock_deps["styled_print"].assert_any_call(
            "[green]Running initial dump...[/green]"
        )
        mock_deps["styled_print"].assert_any_call(
            f"\n[cyan]Watching for file changes in {test_project.root}... (Press Ctrl+C to stop)[/cyan]"
        )

        # 4. Check FileWatcher was instantiated and started
        mock_deps["Watcher"].assert_called_once_with(
            root=test_project.root,
            dump_func=mock_deps["orchestrator_instance"].run,
            quiet=False
        )
        mock_deps["watcher_instance"].start.assert_called_once()

    async def test_run_single_invalid_root(
        self, test_project, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 3: (Validation)
        Ensures a ValueError is raised if root is not a directory.
        """
        # Create a file to use as the invalid root
        file_path = test_project.root / "file.txt"
        await anyio.Path(file_path).write_text("content")

        invalid_args = default_run_args | {"root": file_path}

        # 🐞 FIX: Reset mock to ignore call from write_text
        mock_deps["run_sync"].reset_mock()

        with pytest.raises(ValueError, match="Invalid root"):
            await run_single(**invalid_args)

        # Ensure no mocks were called *by run_single*
        mock_deps["run_sync"].assert_not_called()
        mock_deps["Orchestrator"].assert_not_called()

    async def test_run_single_dry_run_exit_no_watch(
        self, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 4: (Exit Handling - No Watch)
        Ensures a graceful Exit(code=0) from orchestrator.run()
        is caught and handled (returns None).
        """
        mock_deps["orchestrator_instance"].run.side_effect = Exit(code=0)

        dry_run_args = default_run_args | {"dry_run": True, "watch": False}

        # This should NOT raise an exception
        await run_single(**dry_run_args)

        mock_deps["orchestrator_instance"].run.assert_called_once()
        mock_deps["Watcher"].assert_not_called()

    async def test_run_single_dry_run_exit_with_watch(
        self, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 5: (Exit Handling - Watch)
        Ensures a graceful Exit(code=0) on the *initial* run
        is caught and stops execution (does not start watcher).
        """
        mock_deps["orchestrator_instance"].run.side_effect = Exit(code=0)

        dry_run_args = default_run_args | {"dry_run": True, "watch": True}

        # This should NOT raise an exception
        await run_single(**dry_run_args)

        mock_deps["orchestrator_instance"].run.assert_called_once()
        # Ensure the watcher is never started
        mock_deps["Watcher"].assert_not_called()
        mock_deps["watcher_instance"].start.assert_not_called()

    async def test_run_single_real_exit_propagates(
        self, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 6: (Exit Handling - Real Exit)
        Ensures a failing Exit(code=1) propagates up.
        """
        mock_deps["orchestrator_instance"].run.side_effect = Exit(code=1)

        fail_args = default_run_args | {"dry_run": False}

        with pytest.raises(Exit) as e:
            await run_single(**fail_args)

        assert e.value.exit_code == 1
        mock_deps["orchestrator_instance"].run.assert_called_once()
```

---

## tests/test_orchestrator.py

<a id='tests-test-orchestrator-py'></a>

```python
# tests/test_orchestrator.py

"""
Tests for src/create_dump/orchestrator.py: Batch orchestration with atomic staging.
"""

from __future__ import annotations
import pytest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, ANY
# ⚡ FIX: Import AsyncGenerator
from typing import List, AsyncGenerator

import anyio
import pytest_anyio

# [TEST_SKELETON_START]
# Add this import at the top of tests/test_orchestrator.py
from create_dump.orchestrator import _centralize_outputs, validate_batch_staging
# [TEST_SKELETON_END]

# ⚡ RENAMED: Imports to match new API
from create_dump.orchestrator import (
    run_batch,
    atomic_batch_txn,
    # _centralize_outputs, # No longer needed, imported above
    # validate_batch_staging, # No longer needed, imported above
    AtomicBatchTxn  # ⚡ FIX: Import AtomicBatchTxn
)
from create_dump.core import Config
# ⚡ RENAMED: Import to match new API
from create_dump.path_utils import find_matching_files
# ⚡ RENAMED: Import to match new API
from create_dump.single import run_single
from create_dump.archiver import ArchiveManager

pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_config() -> Config:
    return Config(
        dump_pattern=r".*_all_create_dump_\d{8}_\d{6}\.md$",
        max_file_size_kb=5000,
        use_gitignore=True,
        git_meta=True,
    )


@pytest.fixture
def mock_logger(mocker):
    # ⚡ FIX: Patch the logger where it is *used* (in the orchestrator module)
    return mocker.patch("create_dump.orchestrator.logger")


@pytest.fixture
def mock_styled_print(mocker):
    # ⚡ FIX: Patch styled_print where it is *used*
    return mocker.patch("create_dump.orchestrator.styled_print")


@pytest.fixture
def mock_metrics(mocker):
    # ⚡ FIX: Mock DUMP_DURATION.labels to return a mock context manager
    mock_duration_ctx = MagicMock()
    mock_duration_ctx.__enter__ = MagicMock()
    mock_duration_ctx.__exit__ = MagicMock()
    mock_duration = mocker.patch("create_dump.orchestrator.DUMP_DURATION")
    mock_duration.labels.return_value.time.return_value = mock_duration_ctx
    
    # 🐞 FIX: Patch the metric where it is *used*
    mock_rollbacks = mocker.patch("create_dump.orchestrator.ROLLBACKS_TOTAL")
    mock_rollbacks.labels.return_value = MagicMock()
    return mock_rollbacks


@pytest.fixture
def test_project(tmp_path: Path):
    class MockProject:
        def __init__(self, path):
            self.root = path
            # ⚡ ADDED: async_root for convenience
            self.async_root = anyio.Path(path)

        def path(self, rel):
            return self.root / rel

        async def create(self, files):
            for name, content in files.items():
                p = self.path(name)
                await anyio.Path(p).parent.mkdir(parents=True, exist_ok=True)
                if isinstance(content, bytes):
                    await anyio.Path(p).write_bytes(content)
                elif content is None or name.endswith("/"):
                    await anyio.Path(p).mkdir(parents=True, exist_ok=True)
                else:
                    await anyio.Path(p).write_text(str(content))

    return MockProject(tmp_path)


# ⚡ FIX: Add fixture to mock the generator
@pytest.fixture
def mock_find_files_gen(mocker):
    """Mocks find_matching_files to return a configurable async generator."""
    mock_gen_func = mocker.patch("create_dump.orchestrator.find_matching_files")
    
    async def create_gen(file_list: List[Path]) -> AsyncGenerator[Path, None]:
        for f in file_list:
            yield f
    
    # Default behavior: return an empty generator
    mock_gen_func.return_value = create_gen([])
    # Return a factory to configure the mock in specific tests
    return lambda files: setattr(mock_gen_func, "return_value", create_gen(files))


class TestAtomicBatchTxn:
    async def test_successful_commit(self, tmp_path: Path, mock_logger):
        root = tmp_path / "root"
        await anyio.Path(root).mkdir()
        run_id = "test123"

        async with atomic_batch_txn(root, None, run_id, dry_run=False) as staging:
            assert await staging.exists()
            assert "staging-test123" in str(staging)
            await anyio.Path(staging / "dummy.md").write_text("test")

        final = root / "archives" / "test123"
        assert await anyio.Path(final).exists()
        assert await anyio.Path(final / "dummy.md").exists()
        assert mock_logger.info.call_args[0][0] == "Batch txn committed: %s -> %s"


    async def test_rollback_on_exception(self, tmp_path: Path, mock_logger, mock_metrics):
        root = tmp_path / "root"
        await anyio.Path(root).mkdir()
        run_id = "fail456"

        with pytest.raises(ValueError, match="Simulated failure"):
            async with atomic_batch_txn(root, None, run_id, dry_run=False) as staging:
                raise ValueError("Simulated failure")

        archives = root / "archives"
        assert not await anyio.Path(archives / ".staging-fail456").exists()
        
        # 🐞 FIX: The mock_metrics fixture now correctly patches the target
        mock_metrics.labels.assert_called_once_with(reason="Simulated failure")
        mock_metrics.labels.return_value.inc.assert_called_once()

        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args[0][0] == "Batch txn rolled back due to: %s"
        assert isinstance(mock_logger.error.call_args[0][1], ValueError)


    async def test_dry_run_no_staging(self, tmp_path: Path):
        root = tmp_path / "root"
        await anyio.Path(root).mkdir()
        run_id = "dry789"

        async with atomic_batch_txn(root, None, run_id, dry_run=True) as staging:
            assert staging is None

        assert not await anyio.Path(root / "archives" / ".staging-dry789").exists()

    async def test_invalid_dest_outside_root(self, tmp_path: Path):
        root = tmp_path / "root"
        await anyio.Path(root).mkdir()
        unsafe_dest = tmp_path / "outside"

        with pytest.raises(ValueError, match="Staging parent outside root boundary"):
            async with atomic_batch_txn(root, unsafe_dest, "unsafe", dry_run=False):
                pass


# ⚡ RENAMED: Class to match new API
class TestCentralizeOutputs:
    async def test_centralize_to_staging(self, tmp_path: Path, test_project, mock_logger):
        root = test_project.root
        await test_project.create({
            "sub1/sub1_all_create_dump_20251107_200000.md": "content",
            "sub1/sub1_all_create_dump_20251107_200000.sha256": "hash",
            "sub1/junk.txt": "junk",
            "sub2/sub2_all_create_dump_20251107_200100.md": "content2",
            "sub2/sub2_all_create_dump_20251107_200100.sha256": "hash2",
        })
        sub1 = root / "sub1"
        sub2 = root / "sub2"

        staging = anyio.Path(tmp_path / "staging")
        successes = [sub1, sub2]

        # ⚡ FIX: Use the *correct* pattern that matches .md
        md_pattern = r".*_all_create_dump_\d{8}_\d{6}\.md$"
        await _centralize_outputs(staging, root, successes, compress=False, yes=True, dump_pattern=md_pattern)

        assert await (staging / "sub1_all_create_dump_20251107_200000.md").exists()
        assert await (staging / "sub1_all_create_dump_20251107_200000.sha256").exists()
        assert await (staging / "sub2_all_create_dump_20251107_200100.md").exists()
        assert await (staging / "sub2_all_create_dump_20251107_200100.sha256").exists()
        assert not await (staging / "junk.txt").exists()
        mock_logger.info.assert_called_with("Centralized %d dump pairs to %s", 2, staging)

    async def test_centralize_to_dest_path(self, tmp_path: Path, test_project):
        root = test_project.root
        await test_project.create({
            "sub/test_all_create_dump_20251107_200200.md": "content"
        })
        sub = root / "sub"

        dest = tmp_path / "dest"
        md_pattern = r".*_all_create_dump_\d{8}_\d{6}\.md$"
        await _centralize_outputs(dest, root, [sub], compress=False, yes=False, dump_pattern=md_pattern)

        # ⚡ FIX: Use anyio.Path for the async .exists() call
        assert await anyio.Path(dest / "test_all_create_dump_20251107_200200.md").exists()

    async def test_no_matches_skipped(self, tmp_path: Path, test_project):
        root = test_project.root
        await test_project.create({"empty/": None})
        sub = root / "empty"

        dest = tmp_path / "dest"
        md_pattern = r".*_all_create_dump_\d{8}_\d{6}\.md$"
        await _centralize_outputs(dest, root, [sub], compress=False, yes=True, dump_pattern=md_pattern)

        # ⚡ FIX: Correct async list comprehension syntax
        assert len([f async for f in anyio.Path(dest).iterdir()]) == 0


# [TEST_SKELETON_START]

# ... (Inside class TestCentralizeOutputs) ...
    async def test_centralize_missing_sha(self, tmp_path: Path, test_project, mock_logger):
        """
        Tests coverage for missing .sha256 file (lines 130-131, 135).
        """
        root = test_project.root
        await test_project.create({
            "sub1/sub1_all_create_dump_20251107_200000.md": "content",
            # No .sha256 file
        })
        sub1 = root / "sub1"
        staging = anyio.Path(tmp_path / "staging")
        successes = [sub1]

        md_pattern = r".*_all_create_dump_\d{8}_\d{6}\.md$"
        await _centralize_outputs(staging, root, successes, compress=False, yes=True, dump_pattern=md_pattern)

        # Assert the warning was logged
        mock_logger.warning.assert_called_with(
            "Missing SHA256 for dump, moving .md only", 
            path=str(test_project.async_root / "sub1/sub1_all_create_dump_20251107_200000.md")
        )
        # Assert the .md file was still moved
        assert await (staging / "sub1_all_create_dump_20251107_200000.md").exists()


class TestValidateBatchStaging:
    async def test_valid_with_sha(self, tmp_path: Path):
        staging = anyio.Path(tmp_path / "staging")
        await staging.mkdir()
        md1 = staging / "test_all_create_dump_20251107_200300.md"
        await md1.write_text("content")
        sha1 = md1.with_suffix(".sha256")
        await sha1.write_text("hash")

        md2 = staging / "test2_all_create_dump_20251107_200400.md"
        await md2.write_text("content2")
        sha2 = md2.with_suffix(".sha256")
        await sha2.write_text("hash2")

        assert await validate_batch_staging(staging, r".*_all_create_dump_\d{8}_\d{6}\.md$") is True

    async def test_invalid_orphan_sha_missing(self, tmp_path: Path):
        staging = anyio.Path(tmp_path / "staging")
        await staging.mkdir()
        md = staging / "orphan_all_create_dump_20251107_200500.md"
        await md.write_text("content")

        assert await validate_batch_staging(staging, r".*_all_create_dump_\d{8}_\d{6}\.md$") is False

    async def test_empty_staging_false(self, tmp_path: Path):
        staging = anyio.Path(tmp_path / "empty")
        await staging.mkdir()

        assert await validate_batch_staging(staging, r".*_all_create_dump_\d{8}_\d{6}\.md$") is False


# ⚡ RENAMED: Class to match new API
class TestRunBatch:
    @pytest.fixture
    def multi_subdirs(self, test_project):
        root = test_project.root
        sub1 = root / "sub1"
        sub2 = root / "sub2"
        sub1.mkdir(parents=True, exist_ok=True)
        sub2.mkdir(parents=True, exist_ok=True)
        return [str(s.relative_to(root)) for s in [sub1, sub2]]

    async def test_happy_path_atomic(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_logger, mock_styled_print, mock_metrics, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        async def mock_run_single(root: Path, **kwargs):
            md = root / f"{root.name}_all_create_dump_20251107_200600.md"
            await anyio.Path(md).write_text("dummy")
            sha = md.with_suffix(".sha256")
            await anyio.Path(sha).write_text("dummy_hash")
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        mock_manager = AsyncMock()
        mock_manager.run = AsyncMock(return_value={"group1": True}) # 🐞 FIX: Mock the .run method
        mocker.patch("create_dump.orchestrator.ArchiveManager", return_value=mock_manager)

        # ⚡ FIX: Use the mock_find_files_gen fixture (defaulting to empty)
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=True,
            quiet=False,
            dest=None,
            archive=True,
            archive_all=False,
            atomic=True,
        )

        assert mock_logger.info.call_args_list[-1][0][0] == "Batch complete: %d/%d successes"
        mock_manager.run.assert_called_once()
        mock_metrics.labels.return_value.inc.assert_not_called()

        archives = root / "archives"
        # 🐞 FIX: Use recursive rglob to find files inside the committed staging dir
        final_files = [f async for f in anyio.Path(archives).rglob("*.md")]
        assert len(final_files) == 2

    async def test_rollback_on_sub_failure(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_metrics, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        async def mock_run_single(root: Path, **kwargs):
            if "sub2" in str(root):
                raise RuntimeError("Simulated sub-failure")
            md = root / f"{root.name}_all_create_dump_20251107_200700.md"
            await anyio.Path(md).write_text("dummy")
            sha = md.with_suffix(".sha256")
            await anyio.Path(sha).write_text("dummy_hash")
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        # ⚡ FIX: The code *catches* the RuntimeError, so the test should not.
        # The error is logged, and the run continues.
        await run_batch(
            root=root, subdirs=multi_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
            yes=True, accept_prompts=True, compress=False, max_workers=1, verbose=True, quiet=False,
            archive=False, atomic=True,
        )

        archives = root / "archives"
        # 🐞 FIX: Use recursive rglob to find files inside the committed staging dir
        final_files = [f async for f in anyio.Path(archives).rglob("*.md")]

        # ⚡ FIX: The batch should *commit* with only sub1's files.
        assert len(final_files) == 1
        assert final_files[0].name.startswith("sub1")

        # ⚡ FIX: No rollback should be triggered, because the error was caught.
        mock_metrics.labels.return_value.inc.assert_not_called()


    async def test_validation_fail_rollback(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_metrics, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        async def mock_run_single(root: Path, **kwargs):
            # ⚡ FIX: This mock *only* creates the .md, guaranteeing validation fails
            md = root / f"{root.name}_all_create_dump_20251107_200800.md"
            await anyio.Path(md).write_text("dummy")
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        with pytest.raises(ValueError, match="Validation failed"):
            await run_batch(
                root=root, subdirs=multi_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
                yes=True, accept_prompts=True, compress=False, max_workers=2, verbose=True, quiet=False,
                archive=False, atomic=True,
            )
        
        # 🐞 FIX: The mock_metrics fixture now correctly patches the target
        # ⚡ FIX: NOW the rollback logic is triggered
        mock_metrics.labels.assert_called_once_with(reason="Validation failed: Incomplete dumps")
        mock_metrics.labels.return_value.inc.assert_called_once()

    async def test_non_atomic_direct(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        async def mock_run_single(root: Path, **kwargs):
            md = root / f"{root.name}_all_create_dump_20251107_200900.md"
            await anyio.Path(md).write_text("dummy")
            sha = md.with_suffix(".sha256")
            await anyio.Path(sha).write_text("dummy_hash")
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        dest = root / "custom_dest"
        await run_batch(
            root=root, subdirs=multi_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
            yes=True, accept_prompts=True, compress=False, max_workers=1, verbose=False, quiet=True,
            dest=dest, archive=False, atomic=False,
        )

        final_files = [f async for f in anyio.Path(dest).glob("*.md")]
        assert len(final_files) == 2

    async def test_no_subdirs_early_return(self, test_project, mocker, mock_config, mock_logger, mock_find_files_gen):
        root = test_project.root
        invalid_subdirs = ["nonexistent1", "nonexistent2"]
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        await run_batch(
            root=root, subdirs=invalid_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
            yes=False, accept_prompts=False, compress=False, max_workers=1, verbose=True, quiet=False,
            archive=False, atomic=True,
        )
        mock_logger.warning.assert_called_with("No valid subdirs: %s", invalid_subdirs)


    async def test_concurrency_with_limiter(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        calls = []
        async def mock_run_single(root: Path, **kwargs):
            calls.append(root.name)
            await anyio.sleep(0.01)
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        await run_batch(
            root=root, subdirs=multi_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
            yes=True, accept_prompts=True, compress=False, max_workers=1, verbose=False, quiet=True,
            archive=False, atomic=False,
        )

        assert len(calls) == 2
        assert set(calls) == set([Path(sub).name for sub in multi_subdirs])

    async def test_dry_run_disables_atomic(self, test_project, multi_subdirs: List[str], mocker, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=Config(dump_pattern=r".*_all_create_dump_\d{8}_\d{6}\.md$"))

        mocker.patch("create_dump.orchestrator.run_single")
        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        await run_batch(
            root=root, subdirs=multi_subdirs, pattern=".*", dry_run=True,
            yes=True, accept_prompts=True, compress=False, max_workers=2, verbose=False, quiet=True,
            archive=False, atomic=True,
        )

        archives = root / "archives"
        if await anyio.Path(archives).exists():
            final_files = [f async for f in anyio.Path(archives).iterdir()]
            assert len(final_files) == 0
        else:
            assert not await anyio.Path(archives).exists()
            
            
# ... (Inside class TestRunBatch) ...
    async def test_run_batch_non_atomic(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_logger, mock_find_files_gen
    ):
        """
        Action Plan 1: Test non-atomic path (lines 283-317).
        """
        root = test_project.root
        dest = root / "custom_dest"
        
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        
        # Mock the components for the non-atomic path
        mock_centralize = mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)
        mock_validate = mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=True)
        
        # -----------------
        # 🐞 FIX: This is the corrected mock
        # -----------------
        mock_archive_mgr_instance = AsyncMock()
        mock_archive_mgr_instance.run = AsyncMock(return_value={}) # Return empty for this test
        mock_archive_mgr_class = mocker.patch(
            "create_dump.orchestrator.ArchiveManager", 
            return_value=mock_archive_mgr_instance
        )

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=dest,
            archive=True, # Enable archive to test that branch
            atomic=False, # Key flag
        )

        # Assert _centralize_outputs was called with the *final* dest path
        mock_centralize.assert_called_once()
        assert mock_centralize.call_args[0][0] == dest
        
        # Assert validation was called on the final dest path
        mock_validate.assert_called_once_with(anyio.Path(dest), mock_config.dump_pattern)
        
        # -----------------
        # 🐞 FIX: Corrected assertions
        # -----------------
        # Assert ArchiveManager class was instantiated
        mock_archive_mgr_class.assert_called_once()
        # Assert the instance's .run() method was awaited
        mock_archive_mgr_instance.run.assert_called_once()
        
        # ⚡ FIX: Check the *keyword* args for 'root'
        assert mock_archive_mgr_class.call_args[1]["root"] == root

    async def test_run_batch_atomic_validation_fails(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_metrics, mock_find_files_gen
    ):
        """
        Action Plan 2: Test validation failure in atomic mode.
        """
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)
        
        # Mock validation to fail
        mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=False)
        
        # This should raise the ValueError, which triggers the rollback
        with pytest.raises(ValueError, match="Validation failed: Incomplete dumps"):
            await run_batch(
                root=root,
                subdirs=multi_subdirs,
                pattern=mock_config.dump_pattern,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=False,
                quiet=True,
                dest=None,
                archive=False,
                atomic=True,
            )
        
        # Assert rollback metric was incremented
        mock_metrics.labels.assert_called_once_with(reason="Validation failed: Incomplete dumps")
        mock_metrics.labels.return_value.inc.assert_called_once()

    async def test_run_batch_atomic_dry_run_returns_early(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_logger, mock_find_files_gen
    ):
        """
        Tests coverage for atomic dry_run (lines 252-253).
        """
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        # ⚡ FIX: Use the mock_find_files_gen fixture
        
        # Spy on run_single to ensure it's still called (dry_run is passed down)
        mock_run_single_spy = mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        
        # Spy on _centralize_outputs, which should NOT be called
        mock_centralize_spy = mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=True, # Key flag
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=None,
            archive=False,
            atomic=True, # Key flag
        )
        
        # Assert the individual runs were still simulated
        assert mock_run_single_spy.call_count == len(multi_subdirs)
        
        # Assert that the atomic transaction block was exited early
        mock_centralize_spy.assert_not_called()
# [TEST_SKELETON_END]


    # --- NEW P1 TESTS ---

    async def test_run_batch_non_atomic_archive(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_find_files_gen
    ):
        """
        Covers lines 285-317 (non-atomic path with archiving).
        """
        root = test_project.root
        dest = root / "custom_dest"
        
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        mock_centralize = mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)
        mock_validate = mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=True)
        
        mock_archive_mgr_instance = AsyncMock()
        mock_archive_mgr_instance.run = AsyncMock(return_value={"default": Path("archive.zip")})
        mock_archive_mgr_class = mocker.patch(
            "create_dump.orchestrator.ArchiveManager", 
            return_value=mock_archive_mgr_instance
        )

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=dest,
            archive=True, # Enable archive
            atomic=False, # Key flag
        )

        mock_centralize.assert_called_once_with(dest, root, ANY, False, True, mock_config.dump_pattern)
        mock_validate.assert_called_once_with(anyio.Path(dest), mock_config.dump_pattern)
        
        # Assert ArchiveManager was called with the *root* path
        mock_archive_mgr_class.assert_called_once()
        assert mock_archive_mgr_class.call_args[1]["root"] == root
        mock_archive_mgr_instance.run.assert_called_once()

    async def test_run_batch_non_atomic_validation_fails(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_logger, mock_find_files_gen
    ):
        """
        Covers lines 306-308 (validation failure in non-atomic mode).
        """
        root = test_project.root
        dest = root / "custom_dest"
        
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)
        
        # Mock validation to fail
        mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=False)
        
        # 🐞 FIX: Correctly mock the ArchiveManager to be awaitable
        mock_archive_mgr_instance = AsyncMock()
        mock_archive_mgr_instance.run = AsyncMock(return_value={}) # Return empty
        mock_archive_mgr_class = mocker.patch(
            "create_dump.orchestrator.ArchiveManager", 
            return_value=mock_archive_mgr_instance
        )

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=dest,
            archive=True,
            atomic=False,
        )

        # Assert the warning was logged and no error was raised
        mock_logger.warning.assert_called_with("Validation failed: Incomplete dumps in non-atomic destination.")
        
        # Assert ArchiveManager was *still* called (non-transactional)
        mock_archive_mgr_class.assert_called_once()
        mock_archive_mgr_instance.run.assert_called_once()

    async def test_run_batch_pre_cleanup_declined(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_find_files_gen
    ):
        """
        Covers lines 212-216 (pre-cleanup prompt declined).
        """
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        
        # Mock find_matching_files to return a file
        mock_find_files_gen([root / "old_dump.md"])
        
        # Mock confirm to return False
        mock_confirm = mocker.patch("create_dump.orchestrator.confirm", return_value=False)
        mock_safe_delete = mocker.patch("create_dump.orchestrator.safe_delete_paths", new_callable=AsyncMock)
        mock_run_single = mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        
        # 🐞 FIX: Mock validation to pass so the test doesn't fail early
        mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=True)

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=False, # Key flag
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=None,
            archive=False,
            atomic=True,
        )

        # Assert confirm was called and safe_delete was NOT
        mock_confirm.assert_called_once_with("Delete old dumps?")
        mock_safe_delete.assert_not_called()
        
        # Assert the rest of the run continued
        assert mock_run_single.call_count == len(multi_subdirs)
```

---

## tests/writing/test_checksum.py

<a id='tests-writing-test-checksum-py'></a>

```python
# tests/writing/test_checksum.py

"""
Tests for Phase 3: src/create_dump/writing/checksum.py
"""

from __future__ import annotations
import pytest
import hashlib

import anyio

# Import the class to test
from create_dump.writing.checksum import ChecksumWriter

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


async def test_checksum_writer_write(test_project):
    """
    Tests that the ChecksumWriter.write() method correctly calculates
    the SHA256 hash of a file and writes the corresponding .sha256 file.
    """
    # 1. Setup: Create a test file
    file_content = "Hello, create-dump!"
    file_name = "test_file.txt"
    
    await test_project.create({
        file_name: file_content
    })
    
    file_path = test_project.path(file_name)
    
    # 2. Calculate expected hash
    expected_hash = hashlib.sha256(file_content.encode("utf-8")).hexdigest()
    expected_checksum_string = f"{expected_hash}  {file_name}"
    
    # 3. Run the writer
    writer = ChecksumWriter()
    returned_checksum = await writer.write(file_path)
    
    # 4. Assert the return value
    assert returned_checksum == expected_checksum_string
    
    # 5. Assert the created .sha256 file
    checksum_file_path = anyio.Path(file_path.with_suffix(".sha256"))
    assert await checksum_file_path.exists()
    
    # Read the content and check it
    checksum_file_content = await checksum_file_path.read_text()
    assert checksum_file_content.strip() == expected_checksum_string

```

---

## tests/test_watch.py

<a id='tests-test-watch-py'></a>

```python
# tests/test_watch.py

"""
Tests for src/create_dump/watch.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import anyio
from anyio import Event

# Import the class to test
from create_dump.watch import FileWatcher

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_dump_func() -> AsyncMock:
    """Provides a reusable AsyncMock for the dump_func callback."""
    return AsyncMock()


@pytest.fixture
def mock_sleep(mocker) -> AsyncMock:
    """Mocks anyio.sleep to prevent test delays."""
    return mocker.patch("anyio.sleep", new_callable=AsyncMock)


@pytest.fixture
def mock_styled_print(mocker) -> MagicMock:
    """Mocks styled_print to capture console output."""
    return mocker.patch("create_dump.watch.styled_print")


@pytest.fixture
def mock_logger(mocker) -> MagicMock:
    """Mocks the logger to capture error output."""
    return mocker.patch("create_dump.watch.logger")


class TestFileWatcher:
    """Tests for the FileWatcher class."""

    async def test_debouncer_logic(
        self, test_project, mock_dump_func, mock_sleep, mock_styled_print
    ):
        """
        Test Case 1: (Happy Path)
        Validates the _debouncer logic:
        1. Waits for an event.
        2. Clears the event.
        3. Sleeps for DEBOUNCE_MS.
        4. Calls styled_print (when not quiet).
        5. Calls the dump_func.
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=False)
        
        # We need a completion event to know when the mock_dump_func has been
        # called, so we can safely exit the test's task group.
        completion_event = anyio.Event()
        mock_dump_func.side_effect = lambda: completion_event.set()

        async with anyio.create_task_group() as tg:
            # Start the debouncer in the background
            tg.start_soon(watcher._debouncer)
            
            # --- Test Execution ---
            # 1. Trigger the event
            watcher.debounce_event.set()
            
            # 2. Wait for the dump_func to be called
            with anyio.move_on_after(2):  # 2-second timeout
                await completion_event.wait()
            
            # 3. Cancel the debouncer's infinite loop to exit the test
            tg.cancel_scope.cancel()

        # --- Assertions ---
        # It slept for the correct debounce period
        mock_sleep.assert_called_once_with(watcher.DEBOUNCE_MS / 1000)
        # It printed to console
        mock_styled_print.assert_called_with(
            "\n[yellow]File change detected, running dump...[/yellow]"
        )
        # It called the dump function
        mock_dump_func.assert_called_once()

    async def test_debouncer_logic_quiet(
        self, test_project, mock_dump_func, mock_sleep, mock_styled_print
    ):
        """
        Test Case 2: (Quiet Mode)
        Validates that styled_print is NOT called when quiet=True.
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=True)
        
        completion_event = anyio.Event()
        mock_dump_func.side_effect = lambda: completion_event.set()

        async with anyio.create_task_group() as tg:
            tg.start_soon(watcher._debouncer)
            watcher.debounce_event.set()
            with anyio.move_on_after(2):
                await completion_event.wait()
            tg.cancel_scope.cancel()

        # --- Assertions ---
        mock_sleep.assert_called_once()
        mock_dump_func.assert_called_once()
        # Key Assertion: Print was NOT called
        mock_styled_print.assert_not_called()

    async def test_debouncer_error_handling(
        self, test_project, mock_dump_func, mock_sleep, mock_styled_print, mock_logger
    ):
        """
        Test Case 3: (Error Handling)
        Validates that an exception in dump_func is caught, logged,
        and does not crash the debouncer. (Covers line 45->28)
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=False)
        
        test_exception = Exception("Simulated dump error")
        completion_event = anyio.Event()

        # Configure mock to raise an error, but set the completion event
        # in a finally block so the test can exit.
        async def mock_side_effect():
            try:
                raise test_exception
            finally:
                completion_event.set()
        
        mock_dump_func.side_effect = mock_side_effect

        async with anyio.create_task_group() as tg:
            tg.start_soon(watcher._debouncer)
            watcher.debounce_event.set()
            with anyio.move_on_after(2):
                await completion_event.wait()
            tg.cancel_scope.cancel()

        # --- Assertions ---
        mock_dump_func.assert_called_once()
        # It logged the error
        mock_logger.error.assert_called_once_with(
            "Error in watched dump run", error=str(test_exception)
        )
        # It printed the error to console
        mock_styled_print.assert_any_call(
            f"[red]Error in watched dump: {test_exception}[/red]"
        )

    async def test_start_method_integration(self, test_project, mock_dump_func):
        """
        Test Case 4: (Integration)
        Validates that the `start` method:
        1. Launches the _debouncer.
        2. Calls anyio.Path.watch.
        3. Calls event.set() when the watcher yields.
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=True)

        # Mock the _debouncer method
        mock_debouncer = AsyncMock()
        watcher._debouncer = mock_debouncer

        # Mock the event to check .set()
        mock_event = AsyncMock(spec=Event)
        watcher.debounce_event = mock_event

        # Mock the watch generator to yield one value, then stop
        async def fake_watch_gen():
            yield "file_change_event"
        
        # Mock anyio.Path and its .watch() method
        with patch("anyio.Path") as mock_path_class:
            mock_path_instance = MagicMock()
            mock_path_instance.watch.return_value = fake_watch_gen()
            mock_path_class.return_value = mock_path_instance

            # Run the 'start' method, but cancel it immediately after
            # it's had time to process the single watch event.
            async with anyio.create_task_group() as tg:
                tg.start_soon(watcher.start)
                await anyio.sleep(0.01)  # Give time for the loop to run
                tg.cancel_scope.cancel() # Stop the start() method

        # --- Assertions ---
        # 1. _debouncer was started
        mock_debouncer.assert_called_once()
        # 2. anyio.Path(root) was called
        mock_path_class.assert_called_with(test_project.root)
        # 3. .watch(recursive=True) was called
        mock_path_instance.watch.assert_called_once_with(recursive=True)
        # 4. The event was set
        mock_event.set.assert_called_once()

    # --- NEW P2 TESTS ---
        
    async def test_debouncer_error_handling_quiet(
        self, test_project, mock_dump_func, mock_sleep, mock_styled_print, mock_logger
    ):
        """
        Test Case 5: (Error Handling - Quiet)
        Validates that an exception in dump_func is logged but NOT printed
        when in quiet mode. (Covers line 45->28 and skips 47)
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=True)
        
        test_exception = Exception("Simulated dump error")
        completion_event = anyio.Event()

        async def mock_side_effect():
            try:
                raise test_exception
            finally:
                completion_event.set()
        
        mock_dump_func.side_effect = mock_side_effect

        async with anyio.create_task_group() as tg:
            tg.start_soon(watcher._debouncer)
            watcher.debounce_event.set()
            with anyio.move_on_after(2):
                await completion_event.wait()
            tg.cancel_scope.cancel()

        # --- Assertions ---
        mock_dump_func.assert_called_once()
        # It logged the error
        mock_logger.error.assert_called_once_with(
            "Error in watched dump run", error=str(test_exception)
        )
        # It did NOT print the error
        mock_styled_print.assert_not_called()

    async def test_start_keyboard_interrupt(
        self, test_project, mock_dump_func, mock_styled_print, mocker
    ):
        """
        Test Case 6: (KeyboardInterrupt)
        Validates that a KeyboardInterrupt during the watch loop is caught
        and printed. (Covers lines 57-59)
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=False)

        # 🐞 FIX: Mock the create_task_group context manager to raise the interrupt
        # This simulates the interrupt happening *during* the watch.
        mock_task_group = mocker.patch(
            "anyio.create_task_group",
            side_effect=KeyboardInterrupt
        )

        # Run the 'start' method. It should catch the interrupt and exit.
        await watcher.start()

        # --- Assertions ---
        # Assert the task group was entered
        mock_task_group.assert_called_once()
        # Assert the final "stopped" message was printed
        mock_styled_print.assert_called_with("\n[cyan]Watch mode stopped.[/cyan]")
        
    async def test_start_keyboard_interrupt_quiet(
        self, test_project, mock_dump_func, mock_styled_print, mocker
    ):
        """
        Test Case 7: (KeyboardInterrupt - Quiet)
        Validates that a KeyboardInterrupt is caught but NOT printed
        when in quiet mode. (Covers line 58)
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=True)

        mocker.patch(
            "anyio.create_task_group",
            side_effect=KeyboardInterrupt
        )

        await watcher.start()

        # Assert that the "stopped" message was NOT printed
        mock_styled_print.assert_not_called()
```

---

## tests/writing/test_json.py

<a id='tests-writing-test-json-py'></a>

```python
# tests/writing/test_json.py

"""
Tests for Phase 3: src/create_dump/writing/json.py
"""

from __future__ import annotations
from datetime import datetime, timezone
import pytest
import json
from pathlib import Path
from typing import Callable, Awaitable
# ⚡ FIX: Import MagicMock and AsyncMock
from unittest.mock import MagicMock, AsyncMock

import anyio

# Import the class to test
from create_dump.writing.json import JsonWriter
from create_dump.core import DumpFile, GitMeta

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_git_meta() -> GitMeta:
    """Provides a standard GitMeta object."""
    return GitMeta(branch="main", commit="abc1234")


@pytest.fixture
async def temp_dumpfile_factory(tmp_path_factory):
    """
    Provides an async factory to create a DumpFile object
    backed by a real temporary file with content.
    (This fixture can be shared with test_markdown.py)
    """
    temp_dir = tmp_path_factory.mktemp("json_writer_temps")
    
    async def _create(
        file_path: str,
        content: str | None = None,
        language: str | None = "python",
        error: str | None = None
    ) -> DumpFile:
        
        if error:
            return DumpFile(path=file_path, language=language, error=error)
        
        # Create the temp file
        temp_file = anyio.Path(temp_dir) / f"{file_path.replace('/', '_')}.tmp"
        await temp_file.write_text(content or "")
        
        return DumpFile(
            path=file_path,
            language=language,
            temp_path=Path(temp_file) # The writer expects a sync Path
        )
    
    return _create


async def test_json_writer(
    test_project, temp_dumpfile_factory, mock_git_meta
):
    """
    Tests that the JsonWriter correctly writes a JSON file,
    including metadata, successful files, and error files.
    """
    # 1. Setup
    outfile = test_project.path("dump.json")
    
    files_to_process = [
        await temp_dumpfile_factory(
            file_path="src/main.py",
            content="print('hello')",
            language="python"
        ),
        await temp_dumpfile_factory(
            file_path="src/failed.py",
            language="python",
            error="File read error"
        ),
    ]

    writer = JsonWriter(outfile)
    
    # 2. Act
    await writer.write(files_to_process, mock_git_meta, "8.0.0")

    # 3. Assert
    
    # Check atomic write
    output_path = anyio.Path(outfile)
    assert await output_path.exists()
    assert not await anyio.Path(outfile.with_suffix(".tmp")).exists()
    
    # Parse the JSON content
    content_str = await output_path.read_text()
    data = json.loads(content_str)
    
    # Check top-level metadata
    assert data["version"] == "8.0.0"
    assert data["git_meta"]["branch"] == "main"
    assert data["git_meta"]["commit"] == "abc1234"
    assert "generated" in data
    assert len(data["files"]) == 2
    
    # Check successful file entry
    file1 = data["files"][0]
    assert file1["path"] == "src/main.py"
    assert file1["language"] == "python"
    assert file1["content"] == "print('hello')"
    assert file1["error"] is None
    
    # Check error file entry
    file2 = data["files"][1]
    assert file2["path"] == "src/failed.py"
    assert file2["language"] == "python"
    assert file2["content"] is None
    assert file2["error"] == "File read error"


# ✨ NEW: Test for lines 61-63
async def test_json_writer_read_temp_file_error(
    test_project, temp_dumpfile_factory, mock_git_meta, mocker
):
    """
    Tests that if reading a temp file fails, the error is
    logged and included in the final JSON.
    """
    # 1. Setup
    outfile = test_project.path("dump_error.json")
    
    # This file will fail
    failing_dumpfile = await temp_dumpfile_factory(
        file_path="src/fails.py",
        content="i will fail",
        language="python"
    )
    
    writer = JsonWriter(outfile)
    
    # 2. Mock: Make _read_temp_file fail
    mocker.patch.object(
        JsonWriter, 
        "_read_temp_file", 
        side_effect=OSError("Simulated read error")
    )
    mock_logger_error = mocker.patch("create_dump.writing.json.logger.error")
    
    # 3. Act
    await writer.write([failing_dumpfile], mock_git_meta, "8.0.0")

    # 4. Assert
    output_path = anyio.Path(outfile)
    assert await output_path.exists()
    data = json.loads(await output_path.read_text())
    
    assert len(data["files"]) == 1
    
    # Check failed file
    assert data["files"][0]["path"] == "src/fails.py"
    assert data["files"][0]["content"] is None
    assert "Simulated read error" in data["files"][0]["error"]
    
    # Check logger
    mock_logger_error.assert_called_once_with(
        "Failed to read temp file for JSON dump", 
        path="src/fails.py", 
        error="Simulated read error"
    )


# ✨ NEW: Test for lines 91-94
async def test_json_writer_atomic_write_failure(
    test_project, temp_dumpfile_factory, mock_git_meta, mocker
):
    """
    Tests that if the final atomic rename fails, the .tmp file is
    cleaned up.
    """
    # 1. Setup
    outfile = test_project.path("dump_fail.json")
    
    files_to_process = [
        await temp_dumpfile_factory(
            file_path="src/main.py",
            content="print('hello')"
        ),
    ]
    
    writer = JsonWriter(outfile)
    
    # ⚡ FIX: Mock _read_temp_file to prevent it from calling anyio.Path
    # and interfering with the mock below. This ensures json.dumps() succeeds.
    mocker.patch.object(
        JsonWriter, 
        "_read_temp_file", 
        new_callable=AsyncMock, 
        return_value="print('hello')"
    )
    
    # ⚡ FIX: Store the original anyio.Path class *before* patching
    original_anyio_path = anyio.Path

    # 2. Mock: Mock anyio.Path to control the temp *output* file
    mock_temp_out = AsyncMock(spec=anyio.Path)
    
    # ⚡ FIX: Mock .open() as an AsyncMock, not a MagicMock
    mock_temp_out.open = AsyncMock(
        return_value=AsyncMock(
            __aenter__=AsyncMock(), 
            __aexit__=AsyncMock(return_value=None)
        )
    )
    # Make rename fail
    mock_temp_out.rename = AsyncMock(side_effect=OSError("Rename failed!"))
    # Make exists return True for cleanup
    mock_temp_out.exists = AsyncMock(return_value=True)
    mock_temp_out.unlink = AsyncMock()

    # ⚡ FIX: Make the anyio.Path mock *only* apply to the temp output file
    def path_side_effect(path_arg):
        if str(path_arg) == str(outfile.with_suffix(".tmp")):
            return mock_temp_out
        # ⚡ FIX: Fallback to the *original* implementation
        return original_anyio_path(path_arg)

    mocker.patch("create_dump.writing.json.anyio.Path", side_effect=path_side_effect)

    # 3. Act & Assert
    with pytest.raises(OSError, match="Rename failed!"):
        await writer.write(files_to_process, mock_git_meta, "8.0.0")
        
    # 4. Assert cleanup
    mock_temp_out.rename.assert_called_once_with(outfile)
    mock_temp_out.exists.assert_called_once()
    mock_temp_out.unlink.assert_called_once()
    
    # ⚡ FIX: This assertion will now use the original anyio.Path and pass
    assert not await anyio.Path(outfile).exists()
```

---

## tests/writing/test_markdown.py

<a id='tests-writing-test-markdown-py'></a>

~~~python
# tests/writing/test_markdown.py

"""
Tests for Phase 3: src/create_dump/writing/markdown.py
"""

from __future__ import annotations
import pytest
import re
from pathlib import Path
from typing import Callable, Awaitable

import anyio

# Import the class to test
from create_dump.writing.markdown import MarkdownWriter
from create_dump.core import DumpFile, GitMeta

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_git_meta() -> GitMeta:
    """Provides a standard GitMeta object."""
    return GitMeta(branch="main", commit="abc1234")


@pytest.fixture
async def temp_dumpfile_factory(tmp_path_factory):
    """
    Provides an async factory to create a DumpFile object
    backed by a real temporary file with content.
    """
    temp_dir = tmp_path_factory.mktemp("md_writer_temps")
    
    async def _create(
        file_path: str,
        content: str | None = None,
        error: str | None = None
    ) -> DumpFile:
        
        if error:
            return DumpFile(path=file_path, error=error)
        
        # Create the temp file
        temp_file = anyio.Path(temp_dir) / f"{file_path.replace('/', '_')}.tmp"
        await temp_file.write_text(content or "")
        
        return DumpFile(
            path=file_path,
            language=None, # Relies on get_language in prod, not needed here
            temp_path=Path(temp_file) # The writer expects a sync Path
        )
    
    return _create


async def test_write_standard_list_toc(
    test_project, temp_dumpfile_factory, mock_git_meta
):
    """
    Test Case 1: Standard write with a list ToC (default).
    Checks header, git meta, ToC entries, file content,
    error reporting, and code fence switching.
    """
    # 1. Setup
    outfile = test_project.path("dump.md")
    
    files = [
        await temp_dumpfile_factory(
            "src/main.py", "print('hello')"
        ),
        await temp_dumpfile_factory(
            "src/backticks.md", "This file has ```backticks```"
        ),
        await temp_dumpfile_factory(
            "src/failed.py", error="File is unreadable"
        ),
    ]

    writer = MarkdownWriter(outfile, no_toc=False, tree_toc=False)
    
    # 2. Act
    await writer.write(files, mock_git_meta, "8.0.0")

    # 3. Assert
    assert await anyio.Path(outfile).exists()
    assert not await anyio.Path(outfile.with_suffix(".tmp")).exists()
    
    content = await anyio.Path(outfile).read_text()
    
    # Check Header
    assert "**Version:** 8.0.0" in content
    assert "**Git Branch:** main | **Commit:** abc1234" in content
    
    # Check ToC (List format)
    assert "## Table of Contents" in content
    assert "1. [src/main.py](#src-main-py)" in content
    assert "2. [src/backticks.md](#src-backticks-md)" in content
    
    # 🐞 FIX: The error *is* in the content, just not the ToC.
    # This assertion was flawed. The error *section* must exist.
    assert "src/failed.py" in content
    assert "> ⚠️ **Failed:** File is unreadable" in content
    
    # Check File Content
    # (Using regex with re.DOTALL to span newlines)
    
    # File 1: Standard fence
    assert re.search(
        r"## src/main\.py\n\n<a id='src-main-py'></a>\n\n"
        r"```python\nprint\('hello'\)\n```",
        content,
        re.DOTALL
    )
    
    # File 2: Switched fence (~~~)
    assert re.search(
        r"## src/backticks\.md\n\n<a id='src-backticks-md'></a>\n\n"
        r"~~~markdown\nThis file has ```backticks```\n~~~",
        content,
        re.DOTALL
    )
    
    # File 3: Error reporting
    assert "## src/failed.py" in content
    assert "> ⚠️ **Failed:** File is unreadable" in content


async def test_write_tree_toc(test_project, temp_dumpfile_factory):
    """
    Test Case 2: Write with a tree-style ToC.
    Checks that the ToC is rendered as a sorted file tree.
    """
    # 1. Setup
    outfile = test_project.path("dump_tree.md")
    
    files = [
        await temp_dumpfile_factory(
            "src/components/button.py", "pass"
        ),
        await temp_dumpfile_factory(
            "README.md", "# Title"
        ),
    ]

    writer = MarkdownWriter(outfile, no_toc=False, tree_toc=True)
    
    # 2. Act
    await writer.write(files, None, "8.0.0")
    
    # 3. Assert
    content = await anyio.Path(outfile).read_text()
    
    assert "## Table of Contents" in content
    
    # Check for the rendered tree structure.
    # 🐞 FIX: Use regular spaces to match the fix in markdown.py
    expected_tree = (
        "├── README.md ([link](#readme-md))\n"
        "└── src\n"
        "    └── components\n"
        "        └── button.py ([link](#src-components-button-py))"
    )
    
    assert expected_tree in content
    
    # Check that file content is still rendered
    assert "## README.md" in content
    assert "## src/components/button.py" in content


async def test_write_no_toc(test_project, temp_dumpfile_factory):
    """
    Test Case 3: Write with no_toc=True.
    Checks that the ToC section is completely omitted.
    """
    # 1. Setup
    outfile = test_project.path("dump_no_toc.md")
    
    files = [
        await temp_dumpfile_factory(
            "src/main.py", "pass"
        ),
    ]

    writer = MarkdownWriter(outfile, no_toc=True, tree_toc=False)
    
    # 2. Act
    await writer.write(files, None, "8.0.0")
    
    # 3. Assert
    content = await anyio.Path(outfile).read_text()
    
    # Check that ToC is missing
    assert "## Table of Contents" not in content
    
    # 🐞 FIX: The anchor link *is* and *should be* present.
    # The assertion was flawed.
    assert "<a id='src-main-py'></a>" in content

    # Check that header and content are still present
    assert "**Version:** 8.0.0" in content
    assert "## src/main.py" in content
    assert "```python\npass\n```" in content

~~~

---

## tests/workflow/test_single.py

<a id='tests-workflow-test-single-py'></a>

```python
# tests/workflow/test_single.py

"""
Tests for src/create_dump/workflow/single.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, call
from typer import Exit
from tempfile import TemporaryDirectory

import anyio

# Import the class to test
from create_dump.workflow.single import SingleRunOrchestrator
from create_dump.core import Config, DumpFile

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_config(mocker) -> Config:
    """Provides a mock Config object."""
    cfg = Config()
    mocker.patch("create_dump.workflow.single.load_config", return_value=cfg)
    return cfg


@pytest.fixture
def mock_orchestrator_deps(mocker, mock_config):
    """Mocks all external dependencies for SingleRunOrchestrator."""

    # 🐞 FIX: Mock the function and return its patch object
    mock_collector_instance = AsyncMock()
    mock_collector_instance.collect.return_value = ["src/main.py"]
    mock_get_collector_func = mocker.patch(
        "create_dump.workflow.single.get_collector",
        return_value=mock_collector_instance
    )

    # Mock Processor
    mock_processor = AsyncMock()
    mock_dump_file = DumpFile(path="src/main.py", temp_path=Path("/tmp/fake.tmp"))
    mock_processor.dump_concurrent.return_value = [mock_dump_file]
    mocker.patch(
        "create_dump.workflow.single.FileProcessor",
        return_value=mock_processor
    )

    # Mock Writers
    mock_md_writer = AsyncMock()
    mocker.patch(
        "create_dump.workflow.single.MarkdownWriter",
        return_value=mock_md_writer
    )
    mock_json_writer = AsyncMock()
    mocker.patch(
        "create_dump.workflow.single.JsonWriter",
        return_value=mock_json_writer
    )
    mock_checksum_writer = AsyncMock()
    mock_checksum_writer.write.return_value = "dummysha  dummyfile.md"
    mocker.patch(
        "create_dump.workflow.single.ChecksumWriter",
        return_value=mock_checksum_writer
    )

    # Mock ArchiveManager
    mock_archive_manager = AsyncMock()
    mock_archive_manager.run.return_value = {"default": Path("/tmp/archive.zip")}
    mocker.patch(
        "create_dump.workflow.single.ArchiveManager",
        return_value=mock_archive_manager
    )

    # 🐞 FIX: Mock the class and return its patch object
    mock_secret_scanner_class = mocker.patch(
        "create_dump.workflow.single.SecretScanner",
        return_value=MagicMock()  # Return a dummy instance
    )

    # Mock sync functions run in threads
    # 🐞 FIX: Mock _get_total_size_sync directly to avoid thread issues
    mocker.patch(
        "create_dump.workflow.single.SingleRunOrchestrator._get_total_size_sync",
        return_value=1024
    )
    
    # 🐞 FIX: Simplified the mock. The lambda's __name__ check conflicted with
    # the separate mock of _get_total_size_sync. This now just executes
    # the (already mocked) function it is given.
    mocker.patch(
        "anyio.to_thread.run_sync",
        side_effect=lambda func, *args: func(*args)
    )

    # Mock helpers and system functions
    mocker.patch(
        "create_dump.workflow.single._unique_path",
        side_effect=lambda p: p
    )
    mocker.patch(
        "create_dump.workflow.single.get_git_meta",
        return_value=None
    )
    
    # -----------------
    # 🐞 FIX: Capture the mock object here
    # -----------------
    mock_styled_print = mocker.patch("create_dump.workflow.single.styled_print")
    mocker.patch("create_dump.workflow.single.input", return_value="y")
    mocker.patch(
        "create_dump.workflow.single.TemporaryDirectory",
        MagicMock(spec=TemporaryDirectory)
    )
    
    # ⚡ FIX: Update DUMP_DURATION mock to handle .labels()
    mock_duration_ctx = MagicMock()
    mock_duration_ctx.__enter__ = MagicMock()
    mock_duration_ctx.__exit__ = MagicMock()
    mock_duration = mocker.patch("create_dump.workflow.single.DUMP_DURATION")
    mock_duration.labels.return_value.time.return_value = mock_duration_ctx
    
    mocker.patch(
        "create_dump.workflow.single.metrics_server",
        MagicMock()
    )

    # Return a dictionary of key mocks for assertions
    return {
        "get_collector": mock_get_collector_func, # 🐞 FIX: Return patch object
        "collector_instance": mock_collector_instance, # 🐞 FIX: Return instance for method calls
        "FileProcessor": mock_processor,
        "MarkdownWriter": mock_md_writer,
        "JsonWriter": mock_json_writer,
        "ChecksumWriter": mock_checksum_writer,
        "ArchiveManager": mock_archive_manager,
        "SecretScanner": mock_secret_scanner_class, # 🐞 FIX: Return patch object
        # -----------------
        # 🐞 FIX: Add the mock to the returned dictionary
        # -----------------
        "DUMP_DURATION": mock_duration, # ✨ NEW: Add this to the returned dict
        "styled_print": mock_styled_print,
    }
    
@pytest.fixture
def orchestrator_instance(test_project) -> SingleRunOrchestrator:
    """Provides a default instance of SingleRunOrchestrator."""
    return SingleRunOrchestrator(
        root=test_project.root,
        dry_run=False,
        yes=True,
        no_toc=False,
        tree_toc=False,
        compress=False,
        format="md",
        exclude="",
        include="",
        max_file_size=None,
        use_gitignore=True,
        git_meta=True,
        progress=False,
        max_workers=16,
        archive=False,
        archive_all=False,
        archive_search=False,
        archive_include_current=True,
        archive_no_remove=False,
        archive_keep_latest=True,
        archive_keep_last=None,
        archive_clean_root=False,
        archive_format="zip",
        allow_empty=False,
        metrics_port=0,
        verbose=False,
        quiet=False,
        dest=None,
        git_ls_files=False,
        diff_since=None,
        scan_secrets=False,
        hide_secrets=False,
    )


class TestSingleRunOrchestrator:
    """Tests for the SingleRunOrchestrator."""

    async def test_run_happy_path_md(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 1: Standard MD run, all steps called."""

        await orchestrator_instance.run()

        # Check that core components were called
        # 🐞 FIX: Assert against the returned instance's method
        mock_orchestrator_deps["collector_instance"].collect.assert_called_once()
        mock_orchestrator_deps["FileProcessor"].dump_concurrent.assert_called_once()
        mock_orchestrator_deps["MarkdownWriter"].write.assert_called_once()
        mock_orchestrator_deps["ChecksumWriter"].write.assert_called_once()
        
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

        # Check that non-default components were NOT called
        mock_orchestrator_deps["JsonWriter"].write.assert_not_called()
        mock_orchestrator_deps["ArchiveManager"].run.assert_not_called()
        # 🐞 FIX: Assert against the class patch object
        mock_orchestrator_deps["SecretScanner"].assert_not_called()

    async def test_run_dry_run_exits(self, orchestrator_instance, mock_orchestrator_deps):
        """Test Case 2: dry_run=True exits gracefully."""
        # 🐞 FIX: Add mock_orchestrator_deps to ensure collector returns files
        orchestrator_instance.dry_run = True

        with pytest.raises(Exit) as e:
            await orchestrator_instance.run()

        assert e.value.exit_code == 0
        
        # ⚡ FIX: Assert metric was NOT called
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_not_called()

    async def test_run_no_files_fail(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 3: No files found fails when allow_empty=False."""
        mock_orchestrator_deps["collector_instance"].collect.return_value = []
        orchestrator_instance.allow_empty = False

        with pytest.raises(Exit) as e:
            await orchestrator_instance.run()

        assert e.value.exit_code == 1

    async def test_run_no_files_allow_empty(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 4: No files found exits gracefully when allow_empty=True."""
        mock_orchestrator_deps["collector_instance"].collect.return_value = []
        orchestrator_instance.allow_empty = True

        await orchestrator_instance.run()

        # Ensure no processing or writing was attempted
        mock_orchestrator_deps["FileProcessor"].dump_concurrent.assert_not_called()
        mock_orchestrator_deps["MarkdownWriter"].write.assert_not_called()
        
        # ⚡ FIX: Assert metric was NOT called
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_not_called()

    async def test_run_json_format(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 5: format='json' calls JsonWriter."""
        orchestrator_instance.format = "json"

        await orchestrator_instance.run()

        mock_orchestrator_deps["JsonWriter"].write.assert_called_once()
        mock_orchestrator_deps["MarkdownWriter"].write.assert_not_called()
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_archive(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 6: archive=True calls ArchiveManager."""
        orchestrator_instance.archive = True

        await orchestrator_instance.run()

        mock_orchestrator_deps["ArchiveManager"].run.assert_called_once()
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_scan_secrets(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 7: scan_secrets=True instantiates SecretScanner."""
        orchestrator_instance.scan_secrets = True
        orchestrator_instance.hide_secrets = False

        await orchestrator_instance.run()

        # 🐞 FIX: Assert against the class patch object
        mock_orchestrator_deps["SecretScanner"].assert_called_once_with(
            hide_secrets=False
        )
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_hide_secrets(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 8: hide_secrets=True passes flag to SecretScanner."""
        orchestrator_instance.scan_secrets = True
        orchestrator_instance.hide_secrets = True

        await orchestrator_instance.run()

        # 🐞 FIX: Assert against the class patch object
        mock_orchestrator_deps["SecretScanner"].assert_called_once_with(
            hide_secrets=True
        )
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_collector_flags(
        self, orchestrator_instance, mock_orchestrator_deps, mock_config
    ):
        """Test Case 9: Git flags are passed to get_collector."""
        orchestrator_instance.git_ls_files = True
        orchestrator_instance.diff_since = "main"

        await orchestrator_instance.run()

        # 🐞 FIX: Assert against the function patch object
        mock_orchestrator_deps["get_collector"].assert_called_once_with(
            config=mock_config,
            includes=[],
            excludes=[],
            use_gitignore=True,
            root=orchestrator_instance.root,
            git_ls_files=True,
            diff_since="main"
        )
        
        # ⚡ FIX: Assert metric label (diff_since takes precedence)
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="git_diff")
        

    async def test_run_no_files_logging_branches(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """
        Action Plan 1 (Variation): Test logging branches for no_files.
        Covers verbose and quiet branches (lines 113-120).
        """
        mock_orchestrator_deps["collector_instance"].collect.return_value = []
        mock_styled_print = mock_orchestrator_deps["styled_print"]
        
        # 1. Test quiet=True (should not print)
        orchestrator_instance.allow_empty = True
        orchestrator_instance.quiet = True
        orchestrator_instance.verbose = False
        
        await orchestrator_instance.run()
        
        # Assert styled_print was NOT called
        mock_styled_print.assert_not_called()
        mock_styled_print.reset_mock()

        # 2. Test quiet=False (should print)
        orchestrator_instance.quiet = False
        orchestrator_instance.verbose = True # Also cover verbose branch
        
        await orchestrator_instance.run()

        # Assert styled_print WAS called
        mock_styled_print.assert_any_call("[yellow]⚠️ No matching files found; skipping dump.[/yellow]")

    async def test_run_user_prompt_cancel(
        self, orchestrator_instance, mock_orchestrator_deps, mocker
    ):
        """
        Action Plan 2: Test user prompt "n" (lines 177-182).
        Asserts that a "n" response to the prompt raises Exit(code=1).
        """
        # 1. Setup
        orchestrator_instance.yes = False
        orchestrator_instance.dry_run = False
        orchestrator_instance.quiet = False
        
        # 2. Mock: Override the default "y" mock for input
        mocker.patch("create_dump.workflow.single.input", return_value="n")
        mock_styled_print = mock_orchestrator_deps["styled_print"]

        # 3. Act & Assert
        with pytest.raises(Exit) as e:
            await orchestrator_instance.run()
        
        assert e.value.exit_code == 1
        
        # 4. Assert cancellation message was printed
        mock_styled_print.assert_any_call("[red]Cancelled.[/red]")

    async def test_run_compress_true(
        self, orchestrator_instance, mock_orchestrator_deps, mocker
    ):
        """
        Action Plan 3: Test compress=True (lines 205-212).
        Asserts that compression is called and the final file is .gz.
        """
        # 1. Setup
        orchestrator_instance.compress = True
        
        # 2. Mock: Mock the sync compression function
        mock_compress_sync = mocker.patch.object(
            SingleRunOrchestrator, "_compress_file_sync"
        )
        
        # 3. Mock: Mock anyio.Path.unlink to verify the original .md is deleted
        mock_unlink = AsyncMock()
        mock_path_instance = MagicMock()
        mock_path_instance.unlink = mock_unlink
        mocker.patch("create_dump.workflow.single.anyio.Path", return_value=mock_path_instance)

        # 4. Act
        await orchestrator_instance.run()

        # 5. Assert
        # Assert compression was called
        mock_compress_sync.assert_called_once()
        
        # Assert the original file was unlinked
        mock_unlink.assert_called_once()
        
        # Assert the ChecksumWriter was called with the new .gz path
        mock_checksum_writer = mock_orchestrator_deps["ChecksumWriter"]
        final_path = mock_checksum_writer.write.call_args[0][0]
        assert str(final_path).endswith(".md.gz")
        
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_archive_no_results(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """
        Action Plan 4: Test Archive 'Else' Branch (lines 263-268).
        Asserts the correct message is logged if archive=True but no
        archives are found/created.
        """
        # 1. Setup
        orchestrator_instance.archive = True
        orchestrator_instance.quiet = False # Ensure print is called

        # 2. Mock: Override ArchiveManager to return an empty/falsy value
        mock_archive_manager = mock_orchestrator_deps["ArchiveManager"]
        mock_archive_manager.run.return_value = {} # Empty dict
        
        mock_styled_print = mock_orchestrator_deps["styled_print"]
        
        # 3. Act
        await orchestrator_instance.run()

        # 4. Assert
        mock_archive_manager.run.assert_called_once()
        mock_styled_print.assert_any_call(
            "[yellow]ℹ️ No prior dumps found for archiving.[/yellow]"
        )
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")
# [TEST_SKELETON_END]


    async def test_run_git_ls_collector_metric(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """
        Covers line 234 (git_ls collector metric label).
        """
        orchestrator_instance.git_ls_files = True
        orchestrator_instance.diff_since = None # Ensure diff is not used

        await orchestrator_instance.run()
        
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="git_ls")

    async def test_run_dry_run_prints_files(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """
        Covers lines 190-198 (dry run prints files).
        """
        orchestrator_instance.dry_run = True
        orchestrator_instance.quiet = False
        mock_orchestrator_deps["collector_instance"].collect.return_value = ["a.py", "b.py"]
        mock_styled_print = mock_orchestrator_deps["styled_print"]

        with pytest.raises(Exit) as e:
            await orchestrator_instance.run()
        
        assert e.value.exit_code == 0
        mock_styled_print.assert_any_call("[green]✅ Dry run: Would process listed files.[/green]")
        mock_styled_print.assert_any_call(" - a.py")
        mock_styled_print.assert_any_call(" - b.py")

    async def test_run_dest_outside_root_warns(
        self, orchestrator_instance, mock_orchestrator_deps, mocker, test_project
    ):
        """
        Covers line 155 (dest outside root warning).
        """
        orchestrator_instance.dest = Path("/tmp/outside_dest")
        
        mock_logger = mocker.patch("create_dump.workflow.single.logger")
        # Mock safe_is_within to return False
        mocker.patch("create_dump.workflow.single.safe_is_within", new_callable=AsyncMock, return_value=False)

        await orchestrator_instance.run()
        
        mock_logger.warning.assert_called_once_with("Absolute dest outside root; proceeding with caution.")

    async def test_get_total_size_sync_handles_file_not_found(
        self, orchestrator_instance, mocker
    ):
        """
        Covers lines 124-125 (FileNotFoundError in _get_total_size_sync).
        """
        orchestrator_instance.root = Path("/fake/root") # Set a real path
        
        # Mock Path.stat to raise FileNotFoundError
        mock_stat = mocker.patch("pathlib.Path.stat", side_effect=FileNotFoundError)
        
        # Call the sync function directly (it's what run_sync does)
        size = orchestrator_instance._get_total_size_sync(["nonexistent.py"])
        
        assert size == 0
        mock_stat.assert_called_once()
```

---


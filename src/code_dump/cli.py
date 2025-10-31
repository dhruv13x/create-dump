"""
CLI Entry Point using Typer.

Unified interface for single and batch modes.
"""

from __future__ import annotations

import typer
from typing import List, Optional
from pathlib import Path

from datetime import datetime, timezone

from .cleanup import safe_cleanup
from .core import DEFAULT_DUMP_PATTERN, load_config  # NEW: Canonical pattern
from .orchestrator import run_batch  # Remove DEFAULT_DUMP_REGEX import
from .single import run_single
from .utils import setup_logging, styled_print, VERSION

app = typer.Typer(
    name="code-dump",
    add_completion=True,
    pretty_exceptions_enable=True,
    help="Enterprise-grade code dump utility for projects and monorepos.",
    context_settings={"help_option_names": ["-h", "--help"]},  # Added -h shortcut
)

# Create a separate Typer for the batch group
batch_app = typer.Typer(no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]})

# App-level callback for shared options and defaults
@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "-V", "--version", help="Show version and exit"),
    config: Optional[str] = typer.Option(None, "--config", help="Path to TOML config file."),
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for outputs (default: root)."),
):
    """Create Markdown code dumps from source files.

    Defaults to 'single' mode if no subcommand provided.

    Examples:
        $ code-dump single . --compress -y  # Quick gzipped dump, skip prompts
        $ code-dump batch run --dirs src,tests --archive-all  # Batch with grouped archiving
    """
    if version:
        styled_print(f"code-dump v{VERSION}")
        raise typer.Exit()

    load_config(Path(config) if config else None)  # Load early for shared use

    if ctx.invoked_subcommand is None:
        # Ensure root is always provided for single
        root_arg = ctx.args[0] if ctx.args else Path(".")
        ctx.invoke(single, root_arg, dest=dest)


@app.command()
def single(
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root directory to scan [default: . (cwd)]."),

    # Output & Format
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for output (default: root)."),
    no_toc: bool = typer.Option(False, "--no-toc", help="Omit table of contents."),
    compress: bool = typer.Option(False, "-c", "--compress", help="Gzip the output file."),

    # Processing
    progress: bool = typer.Option(True, "-p", "--progress", help="Show processing progress."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Succeed on 0 files (default: fail)."),
    test: bool = typer.Option(False, "-t", "--test", help="Run inline tests."),
    metrics_port: int = typer.Option(8000, "--metrics-port", help="Prometheus export port [default: 8000]."),

    # Filtering & Collection
    exclude: str = typer.Option("", "--exclude", help="Comma-separated exclude patterns."),
    include: str = typer.Option("", "--include", help="Comma-separated include patterns."),
    max_file_size: Optional[int] = typer.Option(None, "--max-file-size", help="Max file size in KB."),
    use_gitignore: bool = typer.Option(True, "--use-gitignore/--no-use-gitignore", help="Incorporate .gitignore excludes [default: true]."),
    git_meta: bool = typer.Option(True, "--git-meta/--no-git-meta", help="Include Git branch/commit [default: true]."),
    max_workers: int = typer.Option(16, "--max-workers", help="Concurrency level [default: 16]."),

    # Archiving (Unified)
    archive: bool = typer.Option(False, "-a", "--archive", help="Archive prior dumps into ZIP (unified workflow)."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs."),
    archive_search: bool = typer.Option(False, "--archive-search", help="Search project-wide for dumps."),
    archive_include_current: bool = typer.Option(True, "--archive-include-current/--no-archive-include-current", help="Include this run in archive [default: true]."),
    archive_no_remove: bool = typer.Option(False, "--archive-no-remove", help="Preserve originals post-archiving."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for prompts and deletions [default: false]."),
    dry_run: bool = typer.Option(False, "-d", "--dry-run", help="Simulate without writing files (default: off)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    verbose: bool = typer.Option(True, "-v", "--verbose", help="Enable debug logging [default: true]."),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output (CI mode) [default: false]."),
):
    """Create a single code dump in the specified directory.

    Examples:
        $ code-dump single src/ --dest dumps/ -c -y -v  # Compressed dump to subdir, skip prompts, verbose
        $ code-dump single . --archive -a --archive-all  # Dump + single/grouped archiving
    """
    if not root.is_dir():
        raise typer.BadParameter(f"Root '{root}' is not a directory. Use '.' for cwd or a valid path.")

    effective_dry_run = dry_run and not no_dry_run
    setup_logging(verbose=verbose, quiet=quiet)
    if test:
        import doctest
        from . import core, collector, writer, utils, archiver
        doctest.testmod(core)
        doctest.testmod(collector)
        doctest.testmod(writer)
        doctest.testmod(archiver)
        doctest.testmod(utils)
        styled_print("[green]All tests passed![/green]")
        raise typer.Exit()

    run_single(
        root=root,
        dry_run=effective_dry_run,
        yes=yes,  # Standardized from force
        no_toc=no_toc,
        compress=compress,
        dest=dest,  # NEW: Propagate
        exclude=exclude,
        include=include,
        max_file_size=max_file_size,
        use_gitignore=use_gitignore,
        git_meta=git_meta,
        progress=progress,
        max_workers=max_workers,
        # Pass archive flags
        archive=archive,
        archive_all=archive_all,
        archive_search=archive_search,
        archive_include_current=archive_include_current,
        archive_no_remove=archive_no_remove,
        archive_keep_latest=archive_keep_latest,
        archive_keep_last=archive_keep_last,
        archive_clean_root=archive_clean_root,
        allow_empty=allow_empty,
        metrics_port=metrics_port,
        verbose=verbose,
        quiet=quiet,
    )


# Batch commands with consistent structure
@batch_app.callback()
def batch_callback(
    # Controls (Standardized; dry-run default ON for safety)
    dry_run: bool = typer.Option(True, "-d", "--dry-run", help="Perform a dry-run (default: ON for batch)."),
    verbose: bool = typer.Option(True, "-v", "--verbose", help="Enable debug logging [default: true]."),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output (CI mode) [default: false]."),
    dest: Optional[Path] = typer.Option(None, "--dest", help="Global destination dir for outputs (default: root)."),
):
    """Batch operations: Run dumps across subdirectories with cleanup and centralization.

    Examples:
        $ code-dump batch run --dirs src,tests --archive-all -y  # Batch dumps + grouped archive, skip prompts
        $ code-dump batch clean --pattern '.*dump.*' -y -nd  # Real cleanup of olds
    """
    setup_logging(verbose=verbose, quiet=quiet)


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

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for deletions and prompts [default: false]."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables inherited dry-run) [default: false]."),
    verbose: bool = typer.Option(True, "-v", "--verbose", help="Enable debug logging [default: true]."),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output (CI mode) [default: false]."),
):
    """Run dumps in multiple subdirectories, cleanup olds, and centralize files.

    Examples:
        $ code-dump batch run src/ --dest central/ --dirs api,web -c -y -nd  # Real batch to central dir
    """
    # Access inherited dry_run from callback via ctx
    inherited_dry_run = ctx.params.get('dry_run', True)  # Default from callback
    effective_dry_run = inherited_dry_run and not no_dry_run
    subdirs = split_dirs(dirs)
    run_batch(
        root=root,
        subdirs=subdirs,
        pattern=pattern,
        dry_run=effective_dry_run,
        yes=yes,  # Standardized
        accept_prompts=accept_prompts,
        compress=compress,
        max_workers=max_workers,
        dest=dest or ctx.params.get('dest'),  # Inherit from batch callback
        # Pass archive flags
        archive=archive,
        archive_all=archive_all,
        archive_search=archive_search,
        archive_include_current=archive_include_current,
        archive_no_remove=archive_no_remove,
        archive_keep_latest=archive_keep_latest,
        archive_keep_last=archive_keep_last,
        archive_clean_root=archive_clean_root,
        verbose=verbose,
        quiet=quiet,
    )


@batch_app.command()
def clean(
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),
    pattern: str = typer.Argument(DEFAULT_DUMP_PATTERN, help="Regex for old dumps to delete [default: canonical pattern]."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmations for deletions [default: false]."),
    dry_run: bool = typer.Option(True, "-d", "--dry-run", help="Perform a dry-run (default: ON)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables dry-run) [default: false]."),
    verbose: bool = typer.Option(True, "-v", "--verbose", help="Enable debug logging [default: true]."),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output (CI mode) [default: false]."),
) -> None:
    """Cleanup old dump files/directories without running new dumps.

    Examples:
        $ code-dump batch clean . '.*old_dump.*' -y -nd -v  # Real verbose cleanup
    """
    effective_dry_run = dry_run and not no_dry_run
    safe_cleanup(root, pattern, dry_run=effective_dry_run, assume_yes=yes, verbose=verbose)


@batch_app.command()
def archive(
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),
    pattern: str = typer.Argument(r".*_all_code_dump_\d{8}_\d{6}\.(md(\.gz)?)$", help="Regex for MD dumps [default: canonical MD subset]."),

    # Archiving (Unified; elevated as primary focus)
    archive_search: bool = typer.Option(False, "--archive-search", help="Recursive search for dumps [default: false]."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs [default: false]."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives (unified flag)."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive (unified flag) [default: false]."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmations [default: false]."),
    dry_run: bool = typer.Option(True, "-d", "--dry-run", help="Perform a dry-run (default: ON)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Enable debug logging [default: false]."),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output [default: false]."),
) -> None:
    """Archive existing dump pairs into ZIP; optional clean/prune (unified with single mode).

    Examples:
        $ code-dump batch archive monorepo/ '.*custom' --archive-all -y -v  # Grouped archive, verbose, skip prompts
    """
    from .archiver import ArchiveManager
    setup_logging(verbose=verbose, quiet=quiet)
    effective_dry_run = dry_run and not no_dry_run
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    manager = ArchiveManager(
        root, timestamp, archive_keep_latest, archive_keep_last, archive_clean_root,
        search=archive_search,
        dry_run=effective_dry_run, yes=yes, verbose=verbose, md_pattern=pattern,
        archive_all=archive_all
    )
    manager.run()  # No current_outfile for batch


# Add batch_app to app for subcommand support
app.add_typer(batch_app, name="batch")
# 🗃️ Project Code Dump

**Generated:** 2025-11-10T14:12:15+00:00 UTC
**Version:** 10.0.0
**Git Branch:** main | **Commit:** cf8ebbd

---

## Table of Contents

1. [single.py](#single-py)
2. [main.py](#main-py)
3. [batch.py](#batch-py)
4. [rollback.py](#rollback-py)

---

## single.py

<a id='single-py'></a>

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

## main.py

<a id='main-py'></a>

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
    # --- App Controls ---
    version: bool = typer.Option(False, "-V", "--version", help="Show version and exit."),
    init: bool = typer.Option(
        False, 
        "--init", 
        help="Run interactive wizard to create 'create_dump.toml'.",
        is_eager=True,  # Handle this before any command
    ),
    config: Optional[str] = typer.Option(None, "--config", help="Path to TOML config file."),
    
    # --- ⚡ REFACTOR: Grouped SRE/Control Flags ---
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for prompts and deletions [default: false]."),
    dry_run: bool = typer.Option(False, "-d", "--dry-run", help="Simulate without writing files (default: off)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Enable debug logging [default: false]."),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output (CI mode) [default: false]."),
    
    # --- Default Command ('single') Flags ---
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for output (default: root)."),
    no_toc: bool = typer.Option(False, "--no-toc", help="Omit table of contents."),
    tree_toc: bool = typer.Option(False, "--tree-toc", help="Render Table of Contents as a file tree."),
    format: str = typer.Option("md", "--format", help="Output format (md or json)."),
    compress: bool = typer.Option(False, "-c", "--compress", help="Gzip the output file."),
    progress: bool = typer.Option(True, "-p", "--progress/--no-progress", help="Show processing progress."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Succeed on 0 files (default: fail)."),
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

## batch.py

<a id='batch-py'></a>

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
    # Controls (Standardized; dry-run default ON for safety)
    dry_run: bool = typer.Option(True, "-d", "--dry-run", help="Perform a dry-run (default: ON for batch)."),
    dest: Optional[Path] = typer.Option(None, "--dest", help="Global destination dir for outputs (default: root)."),
):
    """Batch operations: Run dumps across subdirectories with cleanup and centralization.

    Examples:
        $ create-dump batch run --dirs src,tests --archive-all -y  # Batch dumps + grouped archive, skip prompts
        $ create-dump batch clean --pattern '.*dump.*' -y -nd  # Real cleanup of olds
    """
    # Logging is now set by the main_callback or the subcommand.
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
    dry_run: Optional[bool] = typer.Option(None, "-d", "--dry-run", help="Simulate without writing files (overrides batch default)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables inherited dry-run) [default: false]."),
    verbose: Optional[bool] = typer.Option(None, "-v", "--verbose", help="Enable debug logging."),
    quiet: Optional[bool] = typer.Option(None, "-q", "--quiet", help="Suppress output (CI mode)."),
):
    """Run dumps in multiple subdirectories, cleanup olds, and centralize files.

    Examples:
        $ create-dump batch run src/ --dest central/ --dirs api,web -c -y -nd  # Real batch to central dir
    """
    # 1. Get flags from all 3 levels
    parent_params = ctx.parent.params
    main_params = ctx.find_root().params
    
    # 2. Resolve dry_run (safe by default)
    # Start with the batch-level default
    effective_dry_run = parent_params.get('dry_run', True)
    # If the *command* flag is set, it wins
    if dry_run is True:
        effective_dry_run = True
    # --no-dry-run always wins
    if no_dry_run is True:
        effective_dry_run = False

    # 3. Resolve verbose/quiet (inheriting from root)
    if quiet is True:
        verbose_val = False
        quiet_val = True
    elif verbose is True:
        verbose_val = True
        quiet_val = False
    else: # Neither was set at the command level, so inherit from main
        verbose_val = main_params.get('verbose', False)
        quiet_val = main_params.get('quiet', False)
        if quiet_val:
            verbose_val = False

    # 4. Re-run logging setup
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    subdirs = split_dirs(dirs)
    
    # 5. Call async function
    anyio.run(
        run_batch,
        root,
        subdirs,
        pattern,
        effective_dry_run,
        yes, # 'yes' is simple, just pass it
        accept_prompts,
        compress,
        format,
        max_workers,
        verbose_val, # Pass resolved value
        quiet_val,   # Pass resolved value
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
    ctx: typer.Context,
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),
    pattern: str = typer.Argument(DEFAULT_DUMP_PATTERN, help="Regex for old dumps to delete [default: canonical pattern]."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmations for deletions [default: false]."),
    dry_run: Optional[bool] = typer.Option(None, "-d", "--dry-run", help="Simulate without writing files (overrides batch default)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables inherited dry-run) [default: false]."),
    verbose: Optional[bool] = typer.Option(None, "-v", "--verbose", help="Enable debug logging."),
    quiet: Optional[bool] = typer.Option(None, "-q", "--quiet", help="Suppress output (CI mode)."),
) -> None:
    """Cleanup old dump files/directories without running new dumps.

    Examples:
        $ create-dump batch clean . '.*old_dump.*' -y -nd -v  # Real verbose cleanup
    """
    # 1. Get flags from all 3 levels
    parent_params = ctx.parent.params
    main_params = ctx.find_root().params

    # 2. Resolve dry_run
    effective_dry_run = parent_params.get('dry_run', True)
    if dry_run is True:
        effective_dry_run = True
    if no_dry_run is True:
        effective_dry_run = False

    # 3. Resolve verbose/quiet
    if quiet is True:
        verbose_val = False
        quiet_val = True
    elif verbose is True:
        verbose_val = True
        quiet_val = False
    else:
        verbose_val = main_params.get('verbose', False)
        quiet_val = main_params.get('quiet', False)
        if quiet_val:
            verbose_val = False

    # 4. Re-run logging setup
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    # 5. Call async function
    anyio.run(
        safe_cleanup,
        root,
        pattern,
        effective_dry_run,
        yes,
        verbose_val # Pass resolved value
    )


@batch_app.command()
def archive(
    ctx: typer.Context,
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
    dry_run: Optional[bool] = typer.Option(None, "-d", "--dry-run", help="Simulate without writing files (overrides batch default)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    verbose: Optional[bool] = typer.Option(None, "-v", "--verbose", help="Enable debug logging."),
    quiet: Optional[bool] = typer.Option(None, "-q", "--quiet", help="Suppress output (CI mode)."),
) -> None:
    """Archive existing dump pairs into ZIP; optional clean/prune (unified with single mode).

    Examples:
        $ create-dump batch archive monorepo/ '.*custom' --archive-all -y -v  # Grouped archive, verbose, skip prompts
    """
    # 1. Get flags from all 3 levels
    parent_params = ctx.parent.params
    main_params = ctx.find_root().params
    
    # Get archive_format from root
    inherited_archive_format = main_params.get('archive_format', 'zip')

    # 2. Resolve dry_run
    effective_dry_run = parent_params.get('dry_run', True)
    if dry_run is True:
        effective_dry_run = True
    if no_dry_run is True:
        effective_dry_run = False
    
    # 3. Resolve verbose/quiet
    if quiet is True:
        verbose_val = False
        quiet_val = True
    elif verbose is True:
        verbose_val = True
        quiet_val = False
    else:
        verbose_val = main_params.get('verbose', False)
        quiet_val = main_params.get('quiet', False)
        if quiet_val:
            verbose_val = False
    
    # 4. Re-run logging setup
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    manager = ArchiveManager(
        root, timestamp, archive_keep_latest, archive_keep_last, archive_clean_root,
        search=archive_search,
        dry_run=effective_dry_run, 
        yes=yes, 
        verbose=verbose_val, # Pass resolved value
        md_pattern=pattern,
        archive_all=archive_all,
        archive_format=inherited_archive_format # Pass inherited format
    )
    
    # 5. Call async function
    anyio.run(manager.run)  # No current_outfile for batch
```

---

## rollback.py

<a id='rollback-py'></a>

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

# ⚡ REFACTOR: Import setup_logging
from ..logging import logger, styled_print, setup_logging
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
    # ⚡ REFACTOR: Add all 6 consistent flags in order
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Assume yes for prompts and deletions [default: false]."
    ),
    dry_run: bool = typer.Option(
        False,
        "-d",
        "--dry-run",
        help="Simulate without writing files (default: off)."
    ),
    no_dry_run: bool = typer.Option(
        False, 
        "-nd", 
        "--no-dry-run", 
        help="Run for real (disables simulation) [default: false]."
    ),
    verbose: Optional[bool] = typer.Option(
        None, 
        "-v", 
        "--verbose", 
        help="Enable debug logging."
    ),
    quiet: Optional[bool] = typer.Option(
        None, 
        "-q", 
        "--quiet", 
        help="Suppress output (CI mode)."
    ),
):
    """
    Rolls back a create-dump .md file to a full project structure.
    """
    # ⚡ REFACTOR: Add logic block from cli/single.py
    main_params = ctx.find_root().params
    
    effective_dry_run = dry_run and not no_dry_run

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

    # Re-run setup_logging in case 'rollback' was called directly
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    try:
        anyio.run(
            async_rollback,
            root,
            file,
            yes,
            effective_dry_run, # Pass resolved value
            quiet_val          # Pass resolved value
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


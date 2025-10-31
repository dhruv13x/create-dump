"""Batch orchestration: Multi-subdir dumps, centralization, compression, cleanup."""

from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .archiver import ArchiveManager
from .cleanup import safe_delete_paths
from .core import Config, load_config, DEFAULT_DUMP_PATTERN  # NEW: Canonical pattern & cfg
from .path_utils import confirm, find_matching_files, safe_is_within
from .single import run_single  # Reuse single logic
from .utils import DUMP_DURATION, logger, styled_print

__all__ = ["run_batch"]  # Remove DEFAULT_DUMP_REGEX


def _centralize_outputs(
    root: Path, 
    successes: List[Path], 
    compress: bool, 
    yes: bool, 
    dest: Optional[Path], 
    dump_pattern: str
) -> None:
    """Centralize *only* dump outputs from subdirs to dest (default: root/archives)."""
    if not dest:
        dest = root / "archives"  # Default
    else:
        dest = dest.resolve()
        if not dest.is_absolute():
            dest = root / dest
        if not safe_is_within(dest, root):
            logger.warning("Absolute dest outside root; proceeding with caution.")
    dest.mkdir(parents=True, exist_ok=True)
    moved = 0
    
    # 🐞 FIX: Strict pattern for dumps only
    dump_regex = re.compile(dump_pattern)
    
    for sub_root in successes:
        # Use glob("*") for top-level files only (avoids scanning archives/subdirs)
        all_files = [f for f in sub_root.glob("*") if f.is_file()]  # Filter files post-glob
        for file_path in all_files:
            if not dump_regex.match(file_path.name):
                continue  # Skip non-dumps (e.g., README.md)
            if not safe_is_within(file_path, root):
                logger.warning("Skipping unsafe dump: %s", file_path)
                continue
            target = dest / file_path.name
            if target.exists():
                target.unlink()  # Overwrite if exists (idempotent)
            shutil.move(str(file_path), str(target))  # Use str for cross-fs moves
            moved += 1
            logger.info("Moved dump to dest", src=file_path, dst=target)

    if moved == 0:
        logger.info("No matching dumps found for centralization.")
    else:
        logger.info("Centralized %d dump files to %s", moved, dest)


def run_batch(
    root: Path,
    subdirs: List[str],
    pattern: str,  # Will override with cfg.dump_pattern if loose
    dry_run: bool,
    yes: bool,
    accept_prompts: bool,
    compress: bool,
    max_workers: int,
    verbose: bool,
    quiet: bool,
    dest: Optional[Path] = None,
    # Archive flags
    archive: bool = False,
    archive_all: bool = False,
    archive_search: bool = False,
    archive_include_current: bool = True,
    archive_no_remove: bool = False,
    archive_keep_latest: bool = True,
    archive_keep_last: Optional[int] = None,
    archive_clean_root: bool = False,
) -> None:
    """Orchestrate batch dumps across subdirs."""
    root = root.resolve()
    cfg = load_config()  # NEW: Load early for pattern access
    
    # 🐞 Enforce canonical pattern if provided is loose
    canonical_prefix = r'.*_all_create_dump_'
    if not re.match(canonical_prefix, pattern):
        logger.warning("Loose pattern detected; enforcing canonical: %s", cfg.dump_pattern)
        pattern = cfg.dump_pattern

    # Resolve sub_roots
    sub_roots = [root / sub for sub in subdirs if (root / sub).exists()]
    if not sub_roots:
        logger.warning("No valid subdirs found: %s", subdirs)
        return

    # Pre-batch: Cleanup old dumps (strict pattern)
    matches = find_matching_files(root, pattern)
    if matches and not dry_run:
        if archive_all:
            logger.info("Skipping pre-batch cleanup for --archive-all (preserving history).")
        elif yes or confirm("Delete old dumps?"):
            deleted_files, _ = safe_delete_paths(matches, root, dry_run=dry_run, assume_yes=yes)  # 🐞 FIX: Pass dry_run
            if verbose:
                logger.info("Pre-batch cleanup: %d files deleted", deleted_files)

    total_dumps = 0
    successes, failures = [], []

    with DUMP_DURATION.time():
        for sub_root in sub_roots:
            if not quiet:
                styled_print(f"[blue]Dumping {sub_root}...[/blue]")
            try:
                run_single(
                    root=sub_root,
                    dry_run=dry_run,
                    yes=accept_prompts or yes,
                    no_toc=False,
                    compress=compress,
                    # 🐞 FIX: Remove deprecated output=None
                    exclude="",
                    include="",
                    max_file_size=cfg.max_file_size_kb,
                    use_gitignore=cfg.use_gitignore,
                    git_meta=cfg.git_meta,
                    progress=not quiet,
                    max_workers=max_workers,
                    # dest=dest,
                    # Disable per-sub archiving
                    archive=False,
                    archive_all=False,
                    archive_search=False,
                    archive_include_current=archive_include_current,
                    archive_no_remove=archive_no_remove,
                    archive_keep_latest=archive_keep_latest,
                    archive_keep_last=archive_keep_last,
                    archive_clean_root=archive_clean_root,
                    allow_empty=True,
                    metrics_port=0,
                    verbose=verbose,
                    quiet=quiet,
                )
                total_dumps += 1
                successes.append(sub_root)
            except Exception as e:
                failures.append((sub_root, str(e)))
                logger.error("Subdir dump failed", subdir=sub_root, error=str(e))
                if not quiet:
                    styled_print(f"[red]Failed {sub_root}: {e}[/red]")

    if total_dumps == 0:
        logger.info("No successful dumps; skipping centralization.")
        return

    # Post-dump: Centralize (now strict via passed pattern)
    if not dry_run:
        _centralize_outputs(root, successes, compress, yes, dest=dest, dump_pattern=pattern)

    # Integrated archive (uses strict md_pattern)
    if archive or archive_all:
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        manager = ArchiveManager(
            root=root,
            timestamp=timestamp,
            keep_latest=archive_keep_latest,
            keep_last=archive_keep_last,
            clean_root=archive_clean_root,
            search=archive_search,
            include_current=archive_include_current,
            no_remove=archive_no_remove,
            dry_run=dry_run,
            yes=yes,
            verbose=verbose,
            md_pattern=pattern,  # 🐞 Enforce strict (from CLI/cfg)
            archive_all=archive_all,
        )
        if verbose:
            logger.debug("Batch archiving with search=%s, all=%s", archive_search, archive_all)
        archive_results = manager.run()
        if archive_results and any(archive_results.values()):  # 🐞 FIX: Check non-empty paths
            groups = ', '.join(k for k, v in archive_results.items() if v)
            logger.info("Archived groups: %s", groups)
            if not quiet:
                styled_print(f"[green]📦 Batched archived groups: {groups}[/green]")
        else:
            msg = "ℹ️ No prior dumps found for archiving."
            if not quiet:
                styled_print(f"[yellow]{msg}[/yellow]")
            logger.info(msg)

    # Summary
    logger.info("Batch complete: %d successes, %d failures", len(successes), len(failures))
    if failures and verbose:
        for sub_root, err in failures:
            logger.error("Failure in %s: %s", sub_root, err)
    if not quiet:
        styled_print(f"[green]✅ Batch dump complete ({len(successes)}/{len(sub_roots)} subdirs).[/green]")
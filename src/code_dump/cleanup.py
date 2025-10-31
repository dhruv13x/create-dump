# src/code_dump/cleanup.py
"""Safe, auditable cleanup of files/directories with dry-run and prompts."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Tuple

from .path_utils import confirm, safe_is_within
from .utils import logger  # ← Use named logger


__all__ = ["safe_delete_paths", "safe_cleanup"]


def safe_delete_paths(
    paths: List[Path], root: Path, dry_run: bool, assume_yes: bool
) -> Tuple[int, int]:
    """Delete files or directories in a safe manner.

    Returns (deleted_files, deleted_dirs).
    """
    deleted_files = deleted_dirs = 0
    for p in paths:
        p_resolved = p.resolve()
        if not safe_is_within(p_resolved, root):
            logger.warning("Skipping path outside root: %s", p_resolved)
            continue

        if p_resolved.is_file():
            if dry_run:
                logger.info("[dry-run] would delete file: %s", p_resolved)
            else:
                try:
                    p_resolved.unlink()
                    logger.info("Deleted file: %s", p_resolved)
                    deleted_files += 1
                except Exception as e:
                    logger.error("Failed to delete file %s: %s", p_resolved, e)
        elif p_resolved.is_dir():
            if not assume_yes and not dry_run:
                ok = confirm(f"Remove directory tree: {p_resolved}?")
                if not ok:
                    continue
            if dry_run:
                logger.info("[dry-run] would remove directory: %s", p_resolved)
            else:
                try:
                    shutil.rmtree(p_resolved)
                    logger.info("Removed directory: %s", p_resolved)
                    deleted_dirs += 1
                except Exception as e:
                    logger.error("Failed to remove directory %s: %s", p_resolved, e)
    return deleted_files, deleted_dirs


def safe_cleanup(root: Path, pattern: str, dry_run: bool, assume_yes: bool, verbose: bool) -> None:
    """Standalone cleanup of matching paths."""
    from .path_utils import find_matching_files

    matches = find_matching_files(root, pattern)
    if not matches:
        logger.info("No matching files found for cleanup.")
        return

    if verbose:
        logger.info("Found %d paths to clean", len(matches))
    if dry_run:
        logger.info("Dry-run: Skipping deletions.")
        return

    if assume_yes or confirm("Delete all matching files?"):
        deleted_files, deleted_dirs = safe_delete_paths(matches, root, dry_run=False, assume_yes=assume_yes)
        logger.info("Cleanup complete: %d files, %d dirs deleted", deleted_files, deleted_dirs)
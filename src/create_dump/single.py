# src/create_dump/single.py
"""Single dump runner."""

from __future__ import annotations

import gzip
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from typer import Exit

from .archiver import ArchiveManager
from .collector import FileCollector
from .core import Config, GitMeta, load_config
from .path_utils import safe_is_within  # NEW: For dest validation
from .utils import (
    DUMP_DURATION,
    _unique_path,
    get_git_meta,
    logger,
    metrics_server,
    styled_print,
)
from .writer import ChecksumWriter, MarkdownWriter


def run_single(
    root: Path,
    dry_run: bool,
    yes: bool,
    no_toc: bool,
    compress: bool,
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
    allow_empty: bool,
    metrics_port: int,
    verbose: bool,
    quiet: bool,
    dest: Optional[Path] = None,  # NEW: Destination dir for output
) -> None:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Invalid root: {root}")

    os.chdir(root)  # Normalize cwd

    # Load & override config
    cfg = load_config()
    if max_file_size is not None:
        cfg.max_file_size_kb = max_file_size

    # Parse patterns
    includes = [p.strip() for p in include.split(",") if p.strip()]
    excludes = [p.strip() for p in exclude.split(",") if p.strip()]

    # Collect files
    collector = FileCollector(cfg, includes, excludes, use_gitignore, root)
    files_list = collector.collect()

    if not files_list:
        msg = "⚠️ No matching files found; skipping dump."
        logger.warning(msg)
        if verbose:
            logger.debug("Excludes: %s, Includes: %s", excludes, includes)
        if not quiet:
            styled_print(f"[yellow]{msg}[/yellow]")
        if not allow_empty:
            raise Exit(code=1)
        return

    total_size = sum((root / f).stat().st_size for f in files_list)
    logger.info(
        "Collection complete",
        count=len(files_list),
        total_size_kb=total_size / 1024,
        root=str(root),
    )
    if not quiet:
        styled_print(
            f"[green]📄 Found {len(files_list)} files ({total_size / 1024:.1f} KB total).[/green]"
        )

    # Resolve outfile early for prompt (NEW: Uses dest/output logic)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    foldername = root.name or "project"
    branded_name = Path(f"{foldername}_all_create_dump_{timestamp}.md")
    output_dest = root  # Default
    if dest:
        output_dest = dest.resolve()
        if not output_dest.is_absolute():
            output_dest = root / output_dest
        if not safe_is_within(output_dest, root):
            logger.warning("Absolute dest outside root; proceeding with caution.")
        output_dest.mkdir(parents=True, exist_ok=True)
    base_outfile = output_dest / branded_name  # 🐞 FIX: Always append branded to dest (dir)
    prompt_outfile = _unique_path(base_outfile)  # Simulate unique for prompt

    if not yes and not dry_run and not quiet:
        styled_print(
            f"Proceed with dump to [blue]{prompt_outfile}[/blue]? [yellow](y/n)[/yellow]",
            nl=False,
        )
        if not input("").lower().startswith("y"):
            styled_print("[red]Cancelled.[/red]")
            raise Exit(code=1)

    try:
        if dry_run:
            styled_print("[green]✅ Dry run: Would process listed files.[/green]")
            if not quiet:
                for p in files_list:
                    styled_print(f" - {p}")
            raise Exit(code=0)

        # Secure output path (NEW: Full dest/output integration)
        outfile = _unique_path(base_outfile)  # Use resolved branded path

        gmeta = get_git_meta(root) if git_meta else None

        temp_dir = TemporaryDirectory()
        try:
            with metrics_server(port=metrics_port):
                with DUMP_DURATION.time():
                    writer = MarkdownWriter(outfile, no_toc, gmeta, temp_dir.name)
                    writer.dump_concurrent(files_list, progress, max_workers)

            # Compress if requested
            if compress:
                gz_outfile = outfile.with_suffix(".md.gz")
                with open(outfile, "rb") as f_in, gzip.open(gz_outfile, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                outfile.unlink()
                outfile = gz_outfile
                logger.info("Output compressed", path=str(outfile))

            # Checksum
            checksum_writer = ChecksumWriter()
            checksum = checksum_writer.write(outfile)
            if not quiet:
                styled_print(f"[blue]{checksum}[/blue]")

            # Archive if enabled (unified)
            if archive or archive_all:
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
                    md_pattern=cfg.dump_pattern,
                    archive_all=archive_all,
                )
                archive_results = manager.run(current_outfile=outfile)
                if archive_results:
                    groups = ', '.join(k for k, v in archive_results.items() if v)
                    if not quiet:
                        styled_print(f"[green]Archived groups: {groups}[/green]")
                    logger.info("Archiving complete", groups=groups)
                else:
                    msg = "ℹ️ No prior dumps found for archiving."
                    if not quiet:
                        styled_print(f"[yellow]{msg}[/yellow]")
                    logger.info(msg)

            # Final metrics
            success_count = sum(1 for f in writer.files if not f.error)
            logger.info(
                "Dump summary",
                success=success_count,
                errors=len(writer.files) - success_count,
                output=str(outfile),
            )
        finally:
            temp_dir.cleanup()

    except Exit as e:
        if getattr(e, "exit_code", None) == 0 and dry_run:
            return
        raise
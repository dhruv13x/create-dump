# src/create_dump/writer.py
"""Markdown writing and checksum logic.

Streaming, concurrent-safe output generation.
"""

from __future__ import annotations

import concurrent.futures
from datetime import timezone
import datetime
import gzip
import hashlib
import shutil
import uuid
from concurrent.futures import as_completed, TimeoutError as FutureTimeoutError
from pathlib import Path
from typing import List

import tenacity
from prometheus_client import Counter

from .core import DumpFile, GitMeta
from .utils import (
    CHUNK_SIZE,
    DEFAULT_MAX_WORKERS,
    FILES_PROCESSED,
    DUMP_DURATION,
    ERRORS_TOTAL,
    HAS_RICH,
    Progress,
    SpinnerColumn,
    TextColumn,
    console,
    get_language,
    logger,
    slugify,
    VERSION,
)


class MarkdownWriter:
    """Streams Markdown output using temp files for safety."""

    def __init__(
        self,
        outfile: Path,
        no_toc: bool,
        git_meta: Optional[GitMeta],
        temp_dir: str,  # Changed to str for TemporaryDirectory
    ):
        self.outfile = outfile
        self.no_toc = no_toc
        self.git_meta = git_meta
        self.temp_dir = temp_dir
        self.files: List[DumpFile] = []

    def process_file(self, file_path: str) -> DumpFile:
        """Concurrently read and write file content to temp (streamed)."""
        temp_path = None
        try:
            temp_filename = f"{uuid.uuid4().hex}.tmp"
            src_path = Path(self.temp_dir) / temp_filename
            lang = get_language(file_path)
            with (
                Path(file_path).open("r", encoding="utf-8", errors="replace") as src,
                src_path.open("w", encoding="utf-8") as tmp,
            ):
                # Stream read/write to avoid memory buildup
                peek = src.read(CHUNK_SIZE)
                if peek:
                    # Write peek first for fence decision
                    has_backtick = "```" in peek
                    fence = "~~~" if has_backtick else "```"
                    tmp.write(f"{fence}{lang}\n")
                    tmp.write(peek)
                    while chunk := src.read(CHUNK_SIZE):
                        tmp.write(chunk)
                    tmp.write(f"\n{fence}\n")
                temp_path = src_path
                FILES_PROCESSED.labels(status="success").inc()
                return DumpFile(path=file_path, language=lang, temp_path=temp_path)
        except Exception as e:
            if temp_path:
                temp_path.unlink(missing_ok=True)
            ERRORS_TOTAL.labels(type="process").inc()
            logger.error("File process error", path=file_path, error=str(e))
            return DumpFile(path=file_path, error=str(e))

    def dump_concurrent(
        self,
        files_list: List[str],
        progress: bool = False,
        max_workers: int = DEFAULT_MAX_WORKERS,
    ) -> None:
        """Parallel temp file creation with progress."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.process_file, f) for f in files_list]
            if progress and HAS_RICH:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as prog:
                    task = prog.add_task("Processing files...", total=len(futures))
                    for future in futures:
                        try:
                            self.files.append(
                                future.result(timeout=60)
                            )  # Per-file timeout
                            prog.advance(task)
                        except FutureTimeoutError:
                            ERRORS_TOTAL.labels(type="timeout").inc()
                            self.files.append(DumpFile(path="timeout", error="Timeout"))
                            prog.advance(task)
            else:
                for future in as_completed(futures):
                    try:
                        self.files.append(future.result(timeout=60))
                    except FutureTimeoutError:
                        ERRORS_TOTAL.labels(type="timeout").inc()
                        self.files.append(DumpFile(path="timeout", error="Timeout"))
        self._write_md_streamed()

    def _write_md_streamed(self) -> None:
        """Stream final MD from temps atomically."""
        temp_out = self.outfile.with_suffix(".tmp")
        try:
            with temp_out.open("w", encoding="utf-8") as out:
                now = datetime.datetime.now(timezone.utc)
                out.write("# 🗃️ Project Code Dump\n\n")
                out.write(f"**Generated:** {now.isoformat(timespec='seconds')} UTC\n")
                out.write(f"**Version:** {VERSION}\n")
                if self.git_meta:
                    out.write(
                        f"**Git Branch:** {self.git_meta.branch} | **Commit:** {self.git_meta.commit}\n"
                    )
                out.write("\n---\n\n")

                if not self.no_toc:
                    out.write("## Table of Contents\n\n")
                    for idx, df in enumerate(self.files, 1):
                        if not df.error and df.temp_path:
                            anchor = slugify(df.path)
                            out.write(f"{idx}. [{df.path}](#{anchor})\n")
                    out.write("\n---\n\n")

                for df in self.files:
                    if df.error:
                        out.write(
                            f"## {df.path}\n\n> ⚠️ **Failed:** {df.error}\n\n---\n\n"
                        )
                    elif df.temp_path:
                        anchor = slugify(df.path)
                        out.write(f"## {df.path}\n\n<a id='{anchor}'></a>\n\n")
                        # Stream from temp
                        with df.temp_path.open("r", encoding="utf-8") as tmp:
                            shutil.copyfileobj(tmp, out)  # Efficient stream
                        out.write("\n---\n\n")

            # Atomic rename
            temp_out.replace(self.outfile)
            logger.info("MD written atomically", path=self.outfile)
        except Exception:
            if temp_out.exists():
                temp_out.unlink()
            raise
        finally:
            # Cleanup temps
            for df in self.files:
                if df.temp_path and df.temp_path.exists():
                    df.temp_path.unlink()


class ChecksumWriter:
    """Secure checksum with retries."""

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(1))
    def write(self, path: Path) -> str:
        """
        >>> writer = ChecksumWriter()
        >>> test_file = Path("test.md")
        >>> _ = test_file.write_text("# Test")  # Suppress output
        >>> checksum = writer.write(test_file)
        >>> len(checksum)  # SHA256 hex + "  " + filename
        73
        >>> Path("test.sha256").exists()
        True
        """
        sha = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                sha.update(chunk)
        checksum = f"{sha.hexdigest()}  {path.name}"
        checksum_file = path.with_suffix(".sha256")
        checksum_file.write_text(checksum + "\n")
        return checksum
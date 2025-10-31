# src/create_dump/archiver.py
"""Unified archiving: ZIP packaging, pruning, cleanup with policy enforcement.

Single abstraction for single-mode (ad-hoc) and batch (retention) workflows.
Extensible for formats; zip-slip safe; compression-aware."""

from __future__ import annotations

import os
import re
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict

from .cleanup import safe_delete_paths
from .core import Config, load_config, DEFAULT_DUMP_PATTERN  # NEW: For canonical pattern
from .path_utils import safe_is_within, confirm
from .utils import _unique_path, logger, scandir

__all__ = ["ArchiveManager"]


class ArchiveError(ValueError):
    """Custom error for archive operations."""


def extract_group_prefix(filename: str) -> Optional[str]:
    """Extract group prefix from filename, e.g., 'tests' from 'tests_all_create_dump_*.md'."""
    # Match pattern like {group}_all_create_dump_{timestamp}.md
    match = re.match(r'^(.+?)_all_create_dump_\d{8}_\d{6}\.md$', filename)
    if match:
        group = match.group(1)
        # Validate group is simple (no path chars, etc.)
        if re.match(r'^[a-zA-Z0-9_-]+$', group):
            return group
    return None


class ArchiveManager:
    """Manages ZIP archiving with retention, pruning, and cleanup policies."""

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
        md_pattern: Optional[str] = None,  # NEW: Optional; defaults to cfg.dump_pattern
        archive_all: bool = False,  # New: Enable grouped archiving by prefix
    ):
        self.root = root.resolve()
        self.timestamp = timestamp
        self.keep_latest = keep_latest
        self.keep_last = keep_last
        self.clean_root = clean_root
        self.search = search or archive_all  # 🐞 FIX: Auto-recursive for grouped mode
        self.include_current = include_current
        self.no_remove = no_remove
        self.dry_run = dry_run
        self.yes = yes
        self.verbose = verbose
        # NEW: Enforce canonical pattern from config
        cfg = load_config()
        self.md_pattern = md_pattern or cfg.dump_pattern
        if md_pattern and not re.match(r'.*_all_create_dump_', self.md_pattern):
            logger.warning("Loose md_pattern provided; enforcing canonical: %s", DEFAULT_DUMP_PATTERN)
            self.md_pattern = DEFAULT_DUMP_PATTERN
        self.archive_all = archive_all  # New flag
        self.archives_dir = self.root / "archives"
        self.archives_dir.mkdir(exist_ok=True)
        self.quarantine_dir = self.archives_dir / "quarantine"
        self.quarantine_dir.mkdir(exist_ok=True)
        self.prefix = f"{self.root.name}_all_create_dump_"


    @staticmethod
    def extract_timestamp(filename: str) -> datetime:  # ♻️ @staticmethod: Pure func, no self
        """Extract timestamp from filename (e.g., _20251028_041318)."""
        match = re.search(r'_(\d{8}_\d{6})', filename)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y%m%d_%H%M%S')
            except ValueError:
                logger.warning("Malformed timestamp in filename: %s", filename)
        return datetime.min


    def find_dump_pairs(self) -> List[Tuple[Path, Optional[Path]]]:
        """Find MD/SHA pairs; search if enabled; quarantine orphans."""
        md_regex = re.compile(self.md_pattern)
        pairs = []
        search_root = self.root
        if self.search:
            for dirpath, _, filenames in os.walk(search_root, followlinks=False):
                for fname in filenames:
                    full_path = os.path.join(dirpath, fname)
                    if md_regex.search(fname) and os.path.isfile(full_path):  # 🐞 FIX: Efficient isfile
                        # 🐛 FIX: Only process .md files, even if pattern matches .sha256
                        if not fname.endswith('.md'):
                            if self.verbose:
                                logger.debug("Skipping non-MD match: %s", fname)
                            continue
                        p = Path(full_path)
                        if not safe_is_within(p, self.root):
                            continue
                        sha = p.with_suffix(".sha256")
                        sha_path = sha if sha.exists() and safe_is_within(sha, self.root) else None
                        if not sha_path:
                            if not self.dry_run:
                                quarantine_path = self.quarantine_dir / p.name
                                p.rename(quarantine_path)
                                logger.warning("Quarantined orphan MD: %s -> %s", p, quarantine_path)
                            else:
                                logger.warning("[dry-run] Would quarantine orphan MD: %s", p)
                            continue  # Exclude from pairs
                        pairs.append((p, sha_path))
        else:
            for entry in scandir(search_root):
                if entry.is_file() and md_regex.search(entry.name):
                    # 🐛 FIX: Only process .md files, even if pattern matches .sha256
                    if not entry.name.endswith('.md'):
                        if self.verbose:
                            logger.debug("Skipping non-MD match: %s", entry.name)
                        continue
                    p = Path(entry.path).resolve()
                    if not safe_is_within(p, self.root):
                        continue
                    sha = p.with_suffix(".sha256")
                    sha_path = sha if sha.exists() and safe_is_within(sha, self.root) else None
                    if not sha_path:
                        if not self.dry_run:
                            quarantine_path = self.quarantine_dir / p.name
                            p.rename(quarantine_path)
                            logger.warning("Quarantined orphan MD: %s -> %s", p, quarantine_path)
                        else:
                            logger.warning("[dry-run] Would quarantine orphan MD: %s", p)
                        continue  # Exclude from pairs
                    pairs.append((p, sha_path))
        if self.verbose:
            logger.debug("Found %d pairs (recursive=%s)", len(pairs), self.search)
        return sorted(pairs, key=lambda x: x[0].name)

    def _create_archive(self, files_to_archive: List[Path], zip_name: str) -> Tuple[Optional[Path], List[Path]]:
        """Create ZIP; dedupe, compression-aware, unique naming; validate integrity. Returns (archive_path, archived_files)."""
        if not files_to_archive:
            logger.info("No files to archive for %s", zip_name)
            return None, []

        # Filter None (orphan SHA) before processing
        valid_files = [p for p in files_to_archive if p is not None]
        if not valid_files:
            logger.info("No valid files to archive after filtering orphans for %s", zip_name)
            return None, []

        base_archive = self.archives_dir / zip_name
        archive_name = _unique_path(base_archive)
        to_archive = sorted(list(set(valid_files)))  # Dedupe + deterministic

        with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for p in to_archive:
                arcname = _safe_arcname(p, self.root)
                comp_type = zipfile.ZIP_STORED if p.suffix in {".gz", ".zip", ".bz2"} else zipfile.ZIP_DEFLATED
                z.write(p, arcname=arcname, compress_type=comp_type)

        # Validate integrity before returning
        try:
            with zipfile.ZipFile(archive_name, 'r') as z:
                badfile = z.testzip()
                if badfile is not None:
                    raise ArchiveError(f"Corrupt file in ZIP: {badfile}")
            logger.info("ZIP integrity validated successfully for %s", zip_name)
        except ArchiveError as e:
            logger.error("Archive validation failed for %s: %s. Rolling back: deleting bad ZIP, keeping originals.", zip_name, e)
            archive_name.unlink(missing_ok=True)
            raise
        except Exception as e:
            logger.error("Unexpected error during ZIP validation for %s: %s. Rolling back.", zip_name, e)
            archive_name.unlink(missing_ok=True)
            raise

        size = archive_name.stat().st_size
        logger.info("Archive ZIP created: %s (%d bytes, %d files)", archive_name, size, len(to_archive))
        return archive_name, to_archive  # 🐞 FIX: Return archived files for deferred delete

    def group_pairs_by_prefix(self, pairs: List[Tuple[Path, Optional[Path]]]) -> Dict[str, List[Tuple[Path, Optional[Path]]]]:
        """Group pairs by extracted prefix (e.g., 'src', 'tests')."""
        groups: Dict[str, List[Tuple[Path, Optional[Path]]]] = {}
        for pair in pairs:
            prefix = extract_group_prefix(pair[0].name)
            if prefix:
                if prefix not in groups:
                    groups[prefix] = []
                groups[prefix].append(pair)
            else:
                # Fallback to 'default' group if no prefix matches
                if 'default' not in groups:
                    groups['default'] = []
                groups['default'].append(pair)
        if self.verbose:
            for group, group_pairs in groups.items():
                logger.debug("Grouped %d pairs under '%s'", len(group_pairs), group)
        return groups

    def _handle_single_archive(
        self, pairs: List[Tuple[Path, Optional[Path]]]
    ) -> Tuple[Dict[str, Optional[Path]], List[Path]]:
        """Handle single-archive mode: sort, archive historical, return paths and to-delete."""
        archive_paths: Dict[str, Optional[Path]] = {}
        to_delete: List[Path] = []

        live_pair = None
        historical = pairs
        if self.keep_latest:
            def key_func(p):
                ts = self.extract_timestamp(p[0].name)
                if ts == datetime.min:
                    ts = datetime.fromtimestamp(p[0].stat().st_mtime)
                    if self.verbose:
                        logger.debug("Fallback to mtime for sorting: %s", p[0].name)
                return (-ts.timestamp(), p[0].name)
            sorted_pairs = sorted(pairs, key=key_func)
            live_pair = sorted_pairs[0]
            historical = sorted_pairs[1:]
            if self.verbose:
                logger.info(
                    "Retained latest pair (ts=%s): %s",
                    self.extract_timestamp(live_pair[0].name),
                    live_pair[0].name,
                )

        # Early return for no historical
        if len(historical) == 0:
            return archive_paths, to_delete

        # Build files_to_archive from historical only (full pairs: MD + SHA, filter None)
        files_to_archive = [p for pair in historical for p in pair if p is not None]
        num_historical_pairs = len(historical)
        num_files = len(files_to_archive)
        if self.verbose:
            logger.info("Archiving %d pairs (%d files)", num_historical_pairs, num_files)

        # Dry-run simulation
        base_archive = self.archives_dir / f"{self.root.name}_dumps_archive_{self.timestamp}.zip"
        if self.dry_run:
            logger.info("[dry-run] Would create archive ZIP: %s", base_archive.name)
            archive_path = None
        else:
            archive_path, archived_files = self._create_archive(files_to_archive, base_archive.name)
            to_delete.extend(archived_files)

        archive_paths['default'] = archive_path
 
        # Clean historical originals post-validation (or sim) – only if requested
        if self.clean_root and not self.no_remove:
            to_clean = files_to_archive
            if self.keep_latest and live_pair:
                live_paths = [live_pair[0]]
                if live_pair[1] is not None:
                    live_paths.append(live_pair[1])
                to_clean = [p for p in files_to_archive if p not in live_paths]
            prompt = f"Clean {len(to_clean)} root files post-archive?"
            if self.yes or confirm(prompt):
                safe_delete_paths(to_clean, self.root, dry_run=self.dry_run, assume_yes=self.yes)
                if not self.dry_run:
                    logger.info("Cleaned %d root files", len(to_clean))

        return archive_paths, to_delete

    def _handle_grouped_archives(
        self, groups: Dict[str, List[Tuple[Path, Optional[Path]]]]
    ) -> Tuple[Dict[str, Optional[Path]], List[Path]]:
        """Handle grouped-archive mode: process per group, quarantine defaults, return paths and to-delete."""
        archive_paths: Dict[str, Optional[Path]] = {}
        to_delete: List[Path] = []

        for group, group_pairs in groups.items():
            if self.verbose:
                logger.info("Processing group: %s (%d pairs)", group, len(group_pairs))

            # 🐞 FIX: Skip 'default' – quarantine unmatchable MDs instead
            if group == 'default' and len(group_pairs) > 0:
                logger.warning("Skipping 'default' group (%d pairs): Quarantining unmatchable MDs", len(group_pairs))
                for pair in group_pairs:
                    md, sha_opt = pair[0], pair[1]
                    if not self.dry_run:
                        self.quarantine_dir.mkdir(exist_ok=True)
                        # 🐛 FIX: Safe rename with exists check and avoid double-rename for bogus pairs
                        if md.exists():
                            quarantine_md = self.quarantine_dir / md.name
                            md.rename(quarantine_md)
                            logger.debug("Quarantined unmatchable MD: %s -> %s", md, quarantine_md)
                        if sha_opt and sha_opt.exists() and sha_opt != md:
                            quarantine_sha = self.quarantine_dir / sha_opt.name
                            sha_opt.rename(quarantine_sha)
                            logger.debug("Quarantined unmatchable SHA: %s -> %s", sha_opt, quarantine_sha)
                    # For dry-run, just log
                    else:
                        logger.warning("[dry-run] Would quarantine unmatchable pair: %s / %s", md, sha_opt)
                continue

            live_pair = None
            historical = group_pairs
            if self.keep_latest:
                def key_func(p):
                    ts = self.extract_timestamp(p[0].name)
                    if ts == datetime.min:
                        ts = datetime.fromtimestamp(p[0].stat().st_mtime)
                        if self.verbose:
                            logger.debug("Fallback to mtime for sorting in %s: %s", group, p[0].name)
                    return (-ts.timestamp(), p[0].name)
                sorted_pairs = sorted(group_pairs, key=key_func)
                live_pair = sorted_pairs[0]
                historical = sorted_pairs[1:]
                if self.verbose and live_pair:
                    logger.info(
                        "Retained latest pair in %s (ts=%s): %s",
                        group,
                        self.extract_timestamp(live_pair[0].name),
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

            # ZIP name: {group}_all_create_dump_{timestamp}.zip
            base_archive_name = f"{group}_all_create_dump_{self.timestamp}.zip"
            if self.dry_run:
                logger.info("[dry-run] Would create archive ZIP for %s: %s", group, base_archive_name)
                archive_path = None
            else:
                archive_path, archived_files = self._create_archive(files_to_archive, base_archive_name)
                to_delete.extend(archived_files)
                # Indent ensured

            archive_paths[group] = archive_path

        return archive_paths, to_delete

    def run(self, current_outfile: Optional[Path] = None) -> Dict[str, Optional[Path]]:
        """Orchestrate: find pairs, keep/prune, archive, clean. Returns dict of group -> archive_path."""
        pairs = self.find_dump_pairs()
        if not pairs:
            logger.info("No pairs for archiving.")
            self._prune_old_archives()
            return {}

        archive_paths: Dict[str, Optional[Path]] = {}
        all_to_delete: List[Path] = []  # 🐞 FIX: Collect for deferred delete

        if not self.archive_all:
            # Single-archive mode (extracted)
            archive_paths, to_delete = self._handle_single_archive(pairs)
            all_to_delete.extend(to_delete)
        else:
            # Grouped-archive mode (extracted)
            groups = self.group_pairs_by_prefix(pairs)
            archive_paths, to_delete = self._handle_grouped_archives(groups)
            all_to_delete.extend(to_delete)

        # Deferred bulk delete after all ZIPs validated – only if clean_root and not no_remove (fix: respect flag)
        if self.clean_root and all_to_delete and not self.no_remove and not self.dry_run:
            prompt = f"Delete {len(all_to_delete)} archived files across groups?" if self.archive_all else f"Clean {len(all_to_delete)} root files post-archive?"
            if self.yes or confirm(prompt):
                safe_delete_paths(all_to_delete, self.root, dry_run=False, assume_yes=self.yes)
                logger.info("Deferred delete: Cleaned %d files post-validation", len(all_to_delete))

        # Prune old archives if keep_last specified
        self._prune_old_archives()

        # Symlink current_outfile if provided
        if current_outfile:
            # For single: use live_pair (but extracted; perhaps compute overall latest if needed)
            # For multi-group: skip or pick latest overall; here, skip for simplicity as original
            pass

        return archive_paths

    def _prune_old_archives(self) -> None:
        """Prune ZIPs to last N by mtime."""
        if self.keep_last is None:
            return
        # 🐞 FIX: Strict regex for dump ZIPs only
        zip_pattern = re.compile(r".*_all_create_dump_\d{8}_\d{6}\.zip$")
        archive_zips = [p for p in self.archives_dir.rglob("*") if zip_pattern.match(p.name)]
        num_to_keep = self.keep_last
        if len(archive_zips) > num_to_keep:
            archive_zips.sort(key=lambda p: p.stat().st_mtime)
            num_to_prune = max(0, len(archive_zips) - num_to_keep)
            to_prune = archive_zips[:num_to_prune]
            deleted, _ = safe_delete_paths(to_prune, self.archives_dir, dry_run=False, assume_yes=True)
            logger.info("Pruned %d old archives (keeping last %d)", deleted, self.keep_last)
            if self.verbose:
                logger.debug("Pruned archives: %s", [p.name for p in to_prune])


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
        # Unify messaging for absolutes/subpath failures
        if "is not in the subpath" in str(e):
            raise ValueError(f"Invalid arcname: {str(e)}") from e
        logger.warning("Skipping unsafe path for ZIP: %s (%s)", path, e)
        raise
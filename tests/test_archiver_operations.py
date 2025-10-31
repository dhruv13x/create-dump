"""Tests for operations: find_dump_pairs, _create_archive, _prune_old_archives (mock FS/Zip)."""

import pytest
import os
import time
from pathlib import Path
from unittest.mock import patch, MagicMock, ANY, call
from datetime import datetime
import zipfile
import re  # For prune assert

from create_dump.path_utils import safe_is_within
from create_dump.archiver import ArchiveManager, ArchiveError
from create_dump.utils import logger
from create_dump.core import DEFAULT_DUMP_PATTERN


@pytest.fixture
def mock_root(tmp_path: Path):
    tmp_path.mkdir(exist_ok=True)
    return tmp_path


def test_find_dump_pairs_valid_pair(mock_root: Path):
    md = mock_root / "bot_platform_all_code_dump_20251028_041000.md"
    md.touch()
    sha = mock_root / "bot_platform_all_code_dump_20251028_041000.sha256"
    sha.touch()
    manager = ArchiveManager(mock_root, "20251028_042000")
    pairs = manager.find_dump_pairs()
    assert len(pairs) == 1
    assert pairs[0][0].name == md.name
    assert pairs[0][1] == sha


def test_find_dump_pairs_orphan_quarantine(mock_root: Path):
    orphan_md = mock_root / "orphan_bot_platform_all_code_dump_20251028_041000.md"
    orphan_md.touch()
    manager = ArchiveManager(mock_root, "20251028_042000")
    pairs = manager.find_dump_pairs()
    assert len(pairs) == 0
    quarantine_path = manager.quarantine_dir / orphan_md.name
    assert quarantine_path.exists()
    assert not orphan_md.exists()


def test_find_dump_pairs_dry_run_orphan(mock_root: Path):
    orphan_md = mock_root / "orphan_bot_platform_all_code_dump_20251028_041000.md"
    orphan_md.touch()
    manager = ArchiveManager(mock_root, "20251028_042000", dry_run=True)
    with patch.object(logger, "warning") as mock_warn:
        pairs = manager.find_dump_pairs()
        mock_warn.assert_called_once_with("[dry-run] Would quarantine orphan MD: %s", orphan_md)
    assert len(pairs) == 0
    assert orphan_md.exists()  # No rename in dry-run


def test_find_dump_pairs_non_md_skip_verbose(mock_root: Path):
    non_md = mock_root / "bot_platform_all_code_dump_20251028_041000.sha256"  # Matches pattern, !.md → skip log
    non_md.touch()
    manager = ArchiveManager(mock_root, "20251028_042000", verbose=True)
    with patch.object(logger, "debug") as mock_debug:
        pairs = manager.find_dump_pairs()
        mock_debug.assert_any_call("Skipping non-MD match: %s", non_md.name)
    assert pairs == []


def test_create_archive_empty(mock_root: Path):
    manager = ArchiveManager(mock_root, "20251028_042000")
    with patch.object(logger, "info") as mock_info:
        result = manager._create_archive([], "test.zip")
        mock_info.assert_called_once_with("No files to archive for %s", "test.zip")
    assert result == (None, [])


def test_create_archive_filter_none(mock_root: Path):
    manager = ArchiveManager(mock_root, "20251028_042000")
    with patch.object(logger, "info") as mock_info:
        result = manager._create_archive([None], "test.zip")
        mock_info.assert_called_once_with("No valid files to archive after filtering orphans for %s", "test.zip")
    assert result == (None, [])


def test_create_archive_validate_corrupt(mock_root: Path):
    manager = ArchiveManager(mock_root, "20251028_042000")
    file_txt = mock_root / "test.txt"
    file_txt.touch()
    zip_name = "test.zip"
    with patch("create_dump.archiver.zipfile.ZipFile") as mock_zip, \
         patch("pathlib.Path.unlink") as mock_unlink, \
         patch.object(logger, "error") as mock_err:
        # Mock write succeeds
        mock_zip_write = MagicMock()
        mock_zip_write.__enter__.return_value = mock_zip_write
        mock_zip_write.__exit__.return_value = False
        # Mock read fails validate
        mock_zip_read = MagicMock()
        mock_zip_read.__enter__.return_value = mock_zip_read
        mock_zip_read.__exit__.return_value = False
        mock_zip_read.testzip.return_value = "corrupt.txt"
        mock_zip.side_effect = [mock_zip_write, mock_zip_read]
        with pytest.raises(ArchiveError, match="Corrupt file in ZIP"):
            manager._create_archive([file_txt], zip_name)
        mock_err.assert_called_once_with("Archive validation failed for %s: %s. Rolling back: deleting bad ZIP, keeping originals.", zip_name, ANY)
        mock_unlink.assert_called_once()


def test_create_archive_unexpected_error(mock_root: Path):
    manager = ArchiveManager(mock_root, "20251028_042000")
    file_txt = mock_root / "test.txt"
    file_txt.touch()
    zip_name = "test.zip"
    with patch("create_dump.archiver.zipfile.ZipFile") as mock_zip, \
         patch("pathlib.Path.unlink") as mock_unlink, \
         patch.object(logger, "error") as mock_err:
        mock_zip_write = MagicMock()
        mock_zip_write.__enter__.return_value = mock_zip_write
        mock_zip_write.__exit__.return_value = False
        mock_zip_read = MagicMock()
        mock_zip_read.__enter__.return_value = mock_zip_read
        mock_zip_read.__exit__.return_value = False
        mock_zip_read.testzip.side_effect = Exception("IO error")  # Triggers general except
        mock_zip.side_effect = [mock_zip_write, mock_zip_read]
        with pytest.raises(Exception, match="IO error"):  # Code preserves original e
            manager._create_archive([file_txt], zip_name)
        mock_err.assert_called_once_with("Unexpected error during ZIP validation for %s: %s. Rolling back.", zip_name, ANY)  # Fix: Use ANY for Exception
        mock_unlink.assert_called_once()


def test_prune_old_archives(mock_root: Path):
    archives_dir = mock_root / "archives"
    archives_dir.mkdir()
    # Create 5 zips, old to new, with mtime
    for i in range(5):
        ts = f"{i:02d}0000"  # e.g., 000000, 010000 (6 digits)
        p = archives_dir / f"bot_platform_all_code_dump_20251028_{ts}.zip"
        p.touch()
        os.utime(p, (time.time() - (4 - i) * 3600, ) * 2)  # Older for lower i
    manager = ArchiveManager(mock_root, "20251028_042000", keep_last=3)
    manager._prune_old_archives()
    remaining = list(archives_dir.glob("*.zip"))
    assert len(remaining) == 3  # Kept last 3 (newest)


def test_prune_old_archives_below_threshold(mock_root: Path):
    manager = ArchiveManager(mock_root, "20251028_042000", keep_last=5)
    with patch("create_dump.archiver.re.compile") as mock_re:
        mock_match = MagicMock()
        mock_match.return_value = None
        mock_re.return_value.match.return_value = None
        manager._prune_old_archives()  # No prune if < keep_last
    # No calls to delete


def test_prune_old_archives_verbose(mock_root: Path):
    archives_dir = mock_root / "archives"
    archives_dir.mkdir()
    ts = "000000"  # 6 digits
    old_zip = archives_dir / f"bot_platform_all_code_dump_20251028_{ts}.zip"
    old_zip.touch()
    manager = ArchiveManager(mock_root, "20251028_042000", keep_last=0, verbose=True)
    with patch("create_dump.archiver.safe_delete_paths", return_value=(1, 0)), \
         patch.object(logger, "debug") as mock_debug:
        manager._prune_old_archives()
        mock_debug.assert_called_once_with("Pruned archives: %s", [old_zip.name])


def test_find_dump_pairs_recursive(mock_root: Path):
    """Cover lines 102-124: os.walk branch in search=True."""
    subdir = mock_root / "sub"
    subdir.mkdir()
    ts_str = "20251028_041000"
    md = subdir / f"bot_platform_all_code_dump_{ts_str}.md"
    md.touch()
    sha = md.with_suffix(".sha256")
    sha.touch()
    manager = ArchiveManager(mock_root, "20251028_042000", search=True)
    pairs = manager.find_dump_pairs()
    assert len(pairs) == 1
    assert pairs[0][0].parent == subdir
    assert safe_is_within(pairs[0][0], mock_root)  # Covers within check


def test_find_dump_pairs_recursive_orphan(mock_root: Path):
    """Cover quarantine in recursive (lines 115-120)."""
    subdir = mock_root / "sub"
    subdir.mkdir()
    ts_str = "20251028_041000"
    md = subdir / f"bot_platform_all_code_dump_{ts_str}.md"
    md.touch()  # No sha
    manager = ArchiveManager(mock_root, "20251028_042000", search=True)
    pairs = manager.find_dump_pairs()
    assert len(pairs) == 0
    quarantine_path = manager.quarantine_dir / md.name
    assert quarantine_path.exists()
    assert not md.exists()


def test_find_dump_pairs_verbose_found(mock_root: Path):
    """Cover line 135: verbose 'Found %d pairs' log."""
    ts_str = "20251028_041000"
    md = mock_root / f"bot_platform_all_code_dump_{ts_str}.md"
    md.touch()
    sha = md.with_suffix(".sha256")
    sha.touch()
    manager = ArchiveManager(mock_root, "20251028_042000", verbose=True)
    with patch.object(logger, "debug") as mock_debug:
        pairs = manager.find_dump_pairs()
        mock_debug.assert_any_call("Found %d pairs (recursive=%s)", 1, False)  # Ignore skip for sha


def test_create_archive_validate_success_log(mock_root: Path):
    """Cover lines 195-210, 225-225: success validation + log."""
    manager = ArchiveManager(mock_root, "20251028_042000")
    file_txt = mock_root / "test.txt"
    file_txt.write_text("content")
    zip_name = "test.zip"
    with patch.object(logger, "info") as mock_info:
        archive_path, archived = manager._create_archive([file_txt], zip_name)
        mock_info.assert_any_call("ZIP integrity validated successfully for %s", zip_name)
        mock_info.assert_any_call("Archive ZIP created: %s (%d bytes, %d files)", ANY, ANY, 1)


class TestArchiveHandles:
    @pytest.fixture
    def manager(self, mock_root: Path):
        return ArchiveManager(mock_root, "20251028_045000")

    @pytest.fixture
    def sample_pairs(self, mock_root: Path):
        ts1, ts2 = "20251028_040020", "20251028_040021"  # ts2 newer
        md1 = mock_root / f"bot_platform_all_code_dump_{ts1}.md"
        sha1 = md1.with_suffix(".sha256")
        md2 = mock_root / f"bot_platform_all_code_dump_{ts2}.md"
        sha2 = md2.with_suffix(".sha256")
        md1.touch(); sha1.touch(); md2.touch(); sha2.touch()
        return [(md1, sha1), (md2, sha2)]

    @pytest.mark.parametrize("keep_latest, dry_run, clean_root, no_remove, expected_create_calls, expected_delete_calls, expected_clean_count", [
        (False, False, False, False, 1, 0, 0),
        (True, False, False, False, 1, 0, 0),
        (True, True, True, False, 0, 1, 0),  # Fix: expected_delete_calls = 1 for dry=True, clean=True
        (True, False, True, False, 1, 1, 2),
        (True, False, True, True, 1, 0, 0),
    ])
    def test_handle_single_archive_branches(self, manager, sample_pairs, keep_latest, dry_run, clean_root, no_remove, expected_create_calls, expected_delete_calls, expected_clean_count):
        """Cover 281-351: keep_latest/sort/fallback/dry/clean/exclude live/no historical."""
        manager.keep_latest = keep_latest
        manager.dry_run = dry_run
        manager.clean_root = clean_root
        manager.no_remove = no_remove
        manager.yes = True  # Skip confirm with yes=True
        manager.verbose = True
        with patch.object(manager, "extract_timestamp") as mock_ts, \
             patch.object(manager, "_create_archive") as mock_create, \
             patch('create_dump.archiver.confirm') as mock_confirm, \
             patch('create_dump.archiver.safe_delete_paths') as mock_delete, \
             patch.object(logger, "info") as mock_info, \
             patch.object(logger, "debug") as mock_debug, \
             patch('pathlib.Path.stat') as mock_stat:
            # Extend side_effect for 3 calls: 2 sort + 1 live
            mock_ts.side_effect = [datetime.min, datetime(2025, 10, 28, 4, 2, 1), datetime(2025, 10, 28, 4, 2, 0)]
            mock_stat.return_value = MagicMock(st_mtime=100)
            mock_create.return_value = (Path("zip"), [sample_pairs[0][0], sample_pairs[0][1]])
            mock_confirm.return_value = True
            mock_delete.return_value = (expected_clean_count, 0)
            results, to_del = manager._handle_single_archive(sample_pairs)
            assert mock_create.call_count == expected_create_calls
            if expected_delete_calls:
                mock_confirm.assert_not_called()  # Skip with yes=True
                mock_delete.assert_called_once_with(ANY, ANY, dry_run=dry_run, assume_yes=True)  # Fix: Assert called with dry_run=dry_run
                if not dry_run:
                    mock_info.assert_any_call("Cleaned %d root files", expected_clean_count)
            else:
                mock_confirm.assert_not_called()
                mock_delete.assert_not_called()
            if keep_latest:
                mock_info.assert_any_call("Retained latest pair (ts=%s): %s", ANY, ANY)
                if dry_run:
                    mock_info.assert_any_call("[dry-run] Would create archive ZIP: %s", ANY)
                mock_debug.assert_any_call("Fallback to mtime for sorting: %s", ANY)
            assert len(results) == 1  # Always at least 1 entry even in dry-run
            assert len(to_del) == (0 if dry_run else 2)


    def test_handle_single_archive_no_historical(self, manager, sample_pairs):
        """Cover early return len(historical)==0."""
        manager.keep_latest = False  # Avoid IndexError on empty
        results, to_del = manager._handle_single_archive([])  # Empty → early return
        assert len(results) == 0
        assert len(to_del) == 0
        manager.keep_latest = True
        # 1 pair with keep → historical empty
        results, to_del = manager._handle_single_archive([sample_pairs[0]])
        assert len(results) == 0
        assert len(to_del) == 0


class TestHandleGroupedArchives:
    @pytest.fixture
    def manager(self, mock_root: Path):
        return ArchiveManager(mock_root, "20251028_045000", archive_all=True)

    @pytest.fixture
    def sample_groups(self, mock_root: Path):
        ts1, ts2 = "20251030_040020", "20251030_040021"  # ts2 newer for live selection
        md_src1 = mock_root / f"src_all_code_dump_{ts1}.md"
        sha_src1 = md_src1.with_suffix(".sha256")
        md_src2 = mock_root / f"src_all_code_dump_{ts2}.md"
        sha_src2 = md_src2.with_suffix(".sha256")
        md_default = mock_root / f"all_code_dump_{ts1}.md"
        sha_default = md_default.with_suffix(".sha256")

        md_src1.touch(); sha_src1.touch()
        md_src2.touch(); sha_src2.touch()
        md_default.touch(); sha_default.touch()

        pairs_src = [(md_src1, sha_src1), (md_src2, sha_src2)]
        pairs_default = [(md_default, sha_default)]
        return {'src': pairs_src, 'default': pairs_default}

    @pytest.mark.parametrize(
        "dry_run, keep_latest, expected_quarantine_calls, expected_create_calls",
        [
            (False, False, 2, 1),  # Full archive (real)
            (True, True, 0, 0),    # Simulation (dry-run + keep_latest)
        ],
    )
    def test_handle_grouped_archives_branches(
        self,
        manager,
        sample_groups,
        dry_run,
        keep_latest,
        expected_quarantine_calls,
        expected_create_calls,
    ):
        manager.dry_run = dry_run
        manager.keep_latest = keep_latest
        manager.verbose = True

        with patch.object(manager, "_create_archive") as mock_create, \
             patch("create_dump.archiver.logger.warning") as mock_warn, \
             patch("create_dump.archiver.logger.debug") as mock_debug, \
             patch("create_dump.archiver.logger.info") as mock_info, \
             patch("pathlib.Path.mkdir") as mock_mkdir, \
             patch("pathlib.Path.rename") as mock_rename, \
             patch.object(manager, "extract_timestamp") as mock_ts:

            mock_ts.return_value = datetime(2025, 10, 28, 4, 0, 20)
            mock_create.return_value = (Path("group.zip"), [Path("md"), Path("sha")])
            mock_mkdir.return_value = None
            mock_rename.return_value = None

            results, to_del = manager._handle_grouped_archives(sample_groups)

            # Validate default group quarantine handling
            mock_warn.assert_any_call(
                "Skipping 'default' group (%d pairs): Quarantining unmatchable MDs", 1
            )
            assert mock_rename.call_count == expected_quarantine_calls

            if dry_run:
                mock_warn.assert_any_call(
                    "[dry-run] Would quarantine unmatchable pair: %s / %s", ANY, ANY
                )
                mock_info.assert_any_call(
                    "[dry-run] Would create archive ZIP for %s: %s", "src", ANY
                )
            else:
                mock_debug.assert_has_calls(
                    [
                        call("Quarantined unmatchable MD: %s -> %s", ANY, ANY),
                        call("Quarantined unmatchable SHA: %s -> %s", ANY, ANY),
                    ],
                    any_order=True,
                )

            mock_info.assert_any_call("Processing group: %s (%d pairs)", "src", 2)

            if keep_latest:
                mock_info.assert_any_call(
                    "Retained latest pair in %s (ts=%s): %s", "src", ANY, ANY
                )

            assert mock_create.call_count == expected_create_calls
            assert "src" in results
            assert (len(to_del) == 2) if not dry_run else (len(to_del) == 0)

    def test_handle_grouped_archives_no_historical_group(self, manager, sample_groups):
        """Cover len(historical)==0 log/skip."""
        manager.keep_latest = True

        with patch("create_dump.archiver.logger.info") as mock_info:
            single_group = {"src": sample_groups["src"][:1]}  # Only 1 pair → no historicals
            results, to_del = manager._handle_grouped_archives(single_group)

            mock_info.assert_any_call("No historical pairs for group %s.", "src")
            assert "src" not in results
            assert len(to_del) == 0

def test_init_loose_pattern(mock_root: Path):
    """Cover lines 74-75: loose md_pattern warning/enforce."""
    with patch('create_dump.core.load_config') as mock_load, \
         patch('create_dump.archiver.logger.warning') as mock_warn:
        mock_load.return_value.dump_pattern = DEFAULT_DUMP_PATTERN
        manager = ArchiveManager(mock_root, "ts", md_pattern="loose_pattern")
        assert manager.md_pattern == DEFAULT_DUMP_PATTERN
        mock_warn.assert_called_once_with("Loose md_pattern provided; enforcing canonical: %s", DEFAULT_DUMP_PATTERN)
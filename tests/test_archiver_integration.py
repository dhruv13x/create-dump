"""Integration tests for full run(), quarantine, dry-run, verbose edges (full mocks, end-to-end)."""

import pytest
import os
import time
import re
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock, ANY
import zipfile

from create_dump.archiver import ArchiveManager
from create_dump.utils import logger


@pytest.fixture
def mock_root(tmp_path: Path):
    tmp_path.mkdir(exist_ok=True)
    return tmp_path  # 🐞 FIX: Return tmp_path, not tmp_root


def sample_pairs(mock_root: Path, pairs_count: int):
     """Create sample MD/SHA pairs with descending timestamps (newest first), using strict pattern."""
     pairs = []
     for i in range(pairs_count):
         ts_hh = f"0{i:02d}"
         ts_mmss = "0020"  # Fixed for determinism
         ts_str = f"20251028_{ts_hh}{ts_mmss}"  # Full 8+6 digits
         md = mock_root / f"bot_platform_all_code_dump_{ts_str}.md"  # Canonical prefix
         md.write_text(f"content {i}")
         sha = mock_root / f"bot_platform_all_code_dump_{ts_str}.sha256"
         sha.write_text("abc123")
         mtime = time.time() - i  # Newer → lower i
         os.utime(md, (mtime, mtime))
         os.utime(sha, (mtime, mtime))
         pairs.append((md, sha))
     return pairs


@pytest.mark.parametrize("pairs_count", [0, 1, 3])
def test_manager_bundling(mock_root: Path, pairs_count: int):
    sample_pairs(mock_root, pairs_count)  # Creates files on disk
    timestamp = "20251028_045000"

    # keep_latest=True: retain newest (lowest i)
    with patch('create_dump.archiver.logger') as mock_logger, \
         patch.object(ArchiveManager, "find_dump_pairs", return_value=sample_pairs(mock_root, pairs_count)):
        manager = ArchiveManager(mock_root, timestamp, keep_latest=True, verbose=True)
        archive_results = manager.run()
        archive_path = archive_results.get('default')
        if pairs_count > 0:
            mock_logger.info.assert_any_call("Retained latest pair (ts=%s): %s", ANY, ANY)
            if pairs_count == 1:
                assert archive_path is None
            else:
                expected_archiving_pairs = pairs_count - 1
                mock_logger.info.assert_any_call("Archiving %d pairs (%d files)", expected_archiving_pairs, expected_archiving_pairs * 2)
                assert archive_path is not None
                with zipfile.ZipFile(archive_path) as z:
                    assert len(z.namelist()) == expected_archiving_pairs * 2
        else:
            assert archive_results == {}

    # keep_latest=False: archive all
    with patch('create_dump.archiver.logger') as mock_logger, \
         patch.object(ArchiveManager, "find_dump_pairs", return_value=sample_pairs(mock_root, pairs_count)):
        manager = ArchiveManager(mock_root, timestamp, keep_latest=False, verbose=True)
        archive_results = manager.run()
        archive_path = archive_results.get('default')
        if pairs_count == 0:
            assert archive_results == {}
        else:
            mock_logger.info.assert_any_call("Archiving %d pairs (%d files)", pairs_count, pairs_count * 2)
            assert archive_path is not None
            with zipfile.ZipFile(archive_path) as z:
                assert len(z.namelist()) == pairs_count * 2


def test_manager_orphan_warn(mock_root: Path):
    ts_str = "20251028_040020"
    md_orphan = mock_root / f"test_all_code_dump_{ts_str}.md"
    md_orphan.write_text("content")  # Create file
    # Valid pair
    md_valid = mock_root / f"test_all_code_dump_20251028_040021.md"
    md_valid.write_text("valid")
    sha = mock_root / f"test_all_code_dump_20251028_040021.sha256"
    sha.write_text("abc")

    timestamp = "20251028_045000"
    with patch('create_dump.archiver.logger.warning') as mock_warn:
        manager = ArchiveManager(mock_root, timestamp, verbose=True)
        manager.run()
    # Orphan quarantined, valid pair processed
    assert len(mock_warn.call_args_list) == 1  # Only orphan
    assert "Quarantined orphan MD" in str(mock_warn.call_args_list[0])
    assert md_valid.exists()  # Valid untouched


def test_manager_invalid_path_skip(mock_root: Path):
     ts_str = "20251028_040020"
     md_valid = mock_root / f"bot_platform_all_code_dump_{ts_str}.md"  # Canonical: matches md_regex exactly
     md_valid.write_text("valid")
     sha = mock_root / f"bot_platform_all_code_dump_{ts_str}.sha256"
     sha.write_text("abc")
     # Invalid outside root
     invalid_root = mock_root.parent / "invalid"
     invalid_root.mkdir()
     md_invalid = invalid_root / f"bot_platform_all_code_dump_invalid_{ts_str}.md"  # Still outside → skipped
     md_invalid.write_text("invalid")

     timestamp = "20251028_045000"
     manager = ArchiveManager(mock_root, timestamp, verbose=True)
     with patch('create_dump.archiver.safe_is_within') as mock_within:
         mock_within.side_effect = lambda p, r: p.parent == mock_root  # True for root, False for invalid
         pairs = manager.find_dump_pairs()
         assert len(pairs) == 1  # Valid pair included; invalid skipped by safe_is_within
     # Verify mock calls: 1 True (valid), 1 False (invalid)
     assert mock_within.call_count == 2


def test_manager_dry_run_archive(mock_root: Path):
    ts_str = "20251028_040020"
    md = mock_root / f"test_all_code_dump_test_{ts_str}.md"
    md.write_text("test")
    sha = mock_root / f"test_all_code_dump_test_{ts_str}.sha256"
    sha.write_text("abc")

    timestamp = "20251028_045000"
    with patch('create_dump.archiver.logger.info') as mock_info, \
         patch.object(ArchiveManager, "find_dump_pairs", return_value=[(md, sha)]), \
         patch.object(ArchiveManager, "_create_archive", return_value=(Path("dummy.zip"), [])):
        manager = ArchiveManager(mock_root, timestamp, dry_run=True, verbose=True, keep_latest=False)
        archive_results = manager.run()
    mock_info.assert_any_call("[dry-run] Would create archive ZIP: %s", ANY)
    assert archive_results == {'default': None}


def test_manager_clean_root_confirm(mock_root: Path):
    ts_base = "20251028_040"
    to_delete = []
    for i in range(2):
        ts_str = f"{ts_base}{i:02d}20"
        md = mock_root / f"test_all_code_dump_test_{ts_str}.md"
        md.write_text(f"test {i}")
        sha = mock_root / f"test_all_code_dump_test_{ts_str}.sha256"
        sha.write_text(f"abc{i}")
        to_delete.extend([md, sha])

    timestamp = "20251028_045000"
    manager = ArchiveManager(mock_root, timestamp, clean_root=True, yes=False, verbose=True, keep_latest=False)
    with patch('create_dump.archiver.confirm') as mock_confirm, \
         patch('create_dump.archiver.safe_delete_paths') as mock_delete, \
         patch.object(manager, "find_dump_pairs", return_value=[(to_delete[0], to_delete[1])]), \
         patch.object(manager, "_handle_single_archive", return_value=({}, to_delete)):
        mock_confirm.return_value = True
        mock_delete.return_value = (4, 0)

        manager.run()

    mock_confirm.assert_called_once_with("Clean 4 root files post-archive?")
    mock_delete.assert_called_once()


def test_manager_prune_basic(mock_root: Path):
    archives_dir = mock_root / "archives"
    archives_dir.mkdir()

    for i in range(5):
        ts = f"20251028_{i:02d}0000"
        zipf = archives_dir / f"{mock_root.name}_all_code_dump_{ts}.zip"
        zipf.touch()
        os.utime(zipf, (time.time() - (4 - i) * 86400, ) * 2)

    manager = ArchiveManager(mock_root, "20251028_045000", keep_last=3, verbose=True)

    with patch.object(manager, '_create_archive') as mock_archive, \
         patch('create_dump.archiver.safe_delete_paths') as mock_delete, \
         patch.object(manager, "find_dump_pairs", return_value=[]):
        mock_archive.return_value = Path("dummy.zip")
        mock_delete.return_value = (2, 0)
        manager.run()

    mock_delete.assert_called_once_with(ANY, archives_dir, dry_run=False, assume_yes=True)
    # ✅ Since deletion is mocked, files remain physically present
    assert len(list(archives_dir.glob("*.zip"))) == 5
    
def test_prune_none(mock_root: Path):
    timestamp = "20251028_045000"
    manager = ArchiveManager(mock_root, timestamp, keep_last=None)
    with patch('create_dump.archiver.logger.info') as mock_info, \
         patch('create_dump.archiver.safe_delete_paths') as mock_delete:
        manager._prune_old_archives()
    mock_delete.assert_not_called()
    
@pytest.mark.parametrize("archive_all, expected_prompt", [
    (False, "Clean 2 root files post-archive?"),
    (True, "Delete 2 archived files across groups?"),
])
def test_run_deferred_delete(mock_root: Path, archive_all, expected_prompt):
    """Cover run deferred delete/prompt branches (post-handle)."""
    ts_str = "20251028_040020"
    md = mock_root / f"bot_platform_all_code_dump_{ts_str}.md"
    sha = md.with_suffix(".sha256")
    md.touch(); sha.touch()
    manager = ArchiveManager(mock_root, "20251028_045000", archive_all=archive_all, clean_root=True, no_remove=False, dry_run=False, yes=False, verbose=True)
    with patch.object(manager, "find_dump_pairs") as mock_find, \
         patch.object(manager, "_handle_single_archive" if not archive_all else "_handle_grouped_archives") as mock_handle, \
         patch('create_dump.archiver.confirm') as mock_confirm, \
         patch('create_dump.archiver.safe_delete_paths') as mock_delete, \
         patch('create_dump.archiver.logger.info') as mock_info:
        mock_find.return_value = [(md, sha)]
        mock_handle.return_value = ({'default': Path("zip")}, [md, sha])
        mock_confirm.return_value = True
        mock_delete.return_value = (2, 0)
        results = manager.run()
        mock_confirm.assert_called_once_with(expected_prompt)
        mock_delete.assert_called_once_with([md, sha], manager.root, dry_run=False, assume_yes=False)
        mock_info.assert_any_call("Deferred delete: Cleaned %d files post-validation", 2)

def test_run_symlink_pass(mock_root: Path):
    """Cover run symlink pass branch (line ~412)."""
    current_outfile = mock_root / "current.md"
    manager = ArchiveManager(mock_root, "ts")
    with patch.object(manager, "find_dump_pairs", return_value=[]):
        results = manager.run(current_outfile=current_outfile)
        # Pass covered; no assert needed beyond call
        assert results == {}
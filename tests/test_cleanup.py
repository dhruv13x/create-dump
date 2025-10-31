# tests/test_cleanup.py
"""Tests for cleanup module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, ANY
import logging
import shutil

import code_dump
from code_dump.cleanup import safe_delete_paths, safe_cleanup


@pytest.fixture
def mock_root(tmp_path: Path):
    tmp_path.mkdir(exist_ok=True)
    return tmp_path


def test_safe_delete_paths_file_dry_run(mock_root):
    file_path = mock_root / "test.md"
    file_path.touch()
    with patch("code_dump.cleanup.logger") as mock_log:
        deleted_files, deleted_dirs = safe_delete_paths([file_path], mock_root, dry_run=True, assume_yes=False)
        assert deleted_files == 0
        mock_log.info.assert_called_once_with("[dry-run] would delete file: %s", ANY)


def test_safe_delete_paths_file_delete(mock_root):
    file_path = mock_root / "test.md"
    file_path.touch()
    with patch("code_dump.cleanup.logger"):
        deleted_files, deleted_dirs = safe_delete_paths([file_path], mock_root, dry_run=False, assume_yes=False)
    assert deleted_files == 1
    assert not file_path.exists()


def test_safe_delete_paths_dir_prompt_no(mock_root):
    dir_path = mock_root / "test_dir"
    dir_path.mkdir()
    with patch("code_dump.cleanup.confirm", return_value=False):
        deleted_files, deleted_dirs = safe_delete_paths([dir_path], mock_root, dry_run=False, assume_yes=False)
    assert deleted_dirs == 0
    assert dir_path.exists()


def test_safe_delete_paths_dir_dry_run(mock_root):
    dir_path = mock_root / "test_dir"
    dir_path.mkdir()
    with patch("code_dump.cleanup.logger") as mock_log:
        deleted_files, deleted_dirs = safe_delete_paths([dir_path], mock_root, dry_run=True, assume_yes=False)
        assert deleted_dirs == 0
        mock_log.info.assert_called_once_with("[dry-run] would remove directory: %s", ANY)


def test_safe_delete_paths_dir_delete_assume_yes(mock_root):
    dir_path = mock_root / "test_dir"
    dir_path.mkdir()
    with patch("shutil.rmtree"):
        deleted_files, deleted_dirs = safe_delete_paths([dir_path], mock_root, dry_run=False, assume_yes=True)
    assert deleted_dirs == 1


def test_safe_delete_paths_outside_root_skipped(mock_root):
    outside = Path("/outside/file.md")
    with patch("pathlib.Path.resolve", return_value=outside), \
         patch("code_dump.cleanup.safe_is_within", return_value=False), \
         patch("code_dump.cleanup.logger") as mock_log:
        safe_delete_paths([outside], mock_root, dry_run=False, assume_yes=False)
        mock_log.warning.assert_called_once_with("Skipping path outside root: %s", ANY)


def test_safe_delete_paths_file_exception(mock_root):
    file_path = mock_root / "test.md"
    file_path.touch()
    with patch("pathlib.Path.unlink", side_effect=Exception("Delete failed")), \
         patch("code_dump.cleanup.logger") as mock_log:
        deleted_files, deleted_dirs = safe_delete_paths([file_path], mock_root, dry_run=False, assume_yes=False)
    assert deleted_files == 0
    mock_log.error.assert_called_once_with("Failed to delete file %s: %s", ANY, ANY)


def test_safe_delete_paths_dir_exception(mock_root):
    dir_path = mock_root / "test_dir"
    dir_path.mkdir()
    with patch("shutil.rmtree", side_effect=Exception("Rmtree failed")), \
         patch("code_dump.cleanup.logger") as mock_log:
        deleted_files, deleted_dirs = safe_delete_paths([dir_path], mock_root, dry_run=False, assume_yes=True)
    assert deleted_dirs == 0
    mock_log.error.assert_called_once_with("Failed to remove directory %s: %s", ANY, ANY)


def test_safe_cleanup_no_matches(mock_root):
    with patch("code_dump.path_utils.find_matching_files", return_value=[]), \
         patch("code_dump.cleanup.logger") as mock_log:
        safe_cleanup(mock_root, r".*test.*", dry_run=False, assume_yes=False, verbose=False)
        mock_log.info.assert_called_once_with("No matching files found for cleanup.")


def test_safe_cleanup_dry_run(mock_root):
    with patch("code_dump.path_utils.find_matching_files", return_value=[Path("fake.md")]), \
         patch("code_dump.cleanup.logger") as mock_log:
        safe_cleanup(mock_root, r".*test.*", dry_run=True, assume_yes=False, verbose=False)
        mock_log.info.assert_called_once_with("Dry-run: Skipping deletions.")


def test_safe_cleanup_confirm_no(mock_root):
    with patch("code_dump.path_utils.find_matching_files", return_value=[Path("fake.md")]), \
         patch("code_dump.cleanup.confirm", return_value=False), \
         patch("code_dump.cleanup.safe_delete_paths") as mock_delete, \
         patch("code_dump.cleanup.logger") as mock_log:
        safe_cleanup(mock_root, r".*test.*", dry_run=False, assume_yes=False, verbose=False)
        mock_delete.assert_not_called()
        # No cleanup complete log
        complete_calls = [call for call in mock_log.info.call_args_list if call[0][0] == "Cleanup complete: %d files, %d dirs deleted"]
        assert not complete_calls


def test_safe_cleanup_confirm_yes(mock_root):
    with patch("code_dump.path_utils.find_matching_files", return_value=[Path("fake.md")]), \
         patch("code_dump.cleanup.confirm", return_value=True), \
         patch("code_dump.cleanup.safe_delete_paths", return_value=(1, 0)) as mock_delete, \
         patch("code_dump.cleanup.logger") as mock_log:
        safe_cleanup(mock_root, r".*test.*", dry_run=False, assume_yes=False, verbose=False)
        mock_delete.assert_called_once()
        mock_log.info.assert_any_call("Cleanup complete: %d files, %d dirs deleted", 1, 0)


def test_safe_cleanup_assume_yes(mock_root):
    with patch("code_dump.path_utils.find_matching_files", return_value=[Path("fake.md")]), \
         patch("code_dump.cleanup.safe_delete_paths", return_value=(1, 0)) as mock_delete, \
         patch("code_dump.cleanup.logger") as mock_log:
        safe_cleanup(mock_root, r".*test.*", dry_run=False, assume_yes=True, verbose=False)
        mock_delete.assert_called_once()
        mock_log.info.assert_any_call("Cleanup complete: %d files, %d dirs deleted", 1, 0)


def test_safe_cleanup_verbose_found(mock_root):
    with patch("code_dump.path_utils.find_matching_files", return_value=[Path("fake.md")]), \
         patch("code_dump.cleanup.confirm", return_value=False), \
         patch("code_dump.cleanup.logger") as mock_log:
        safe_cleanup(mock_root, r".*test.*", dry_run=False, assume_yes=False, verbose=True)
        mock_log.info.assert_any_call("Found %d paths to clean", 1)
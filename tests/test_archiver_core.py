"""Unit tests for core helpers: extraction, grouping, safe_arcname (pure functions)."""

import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from create_dump.archiver import extract_group_prefix, _safe_arcname, ArchiveManager


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("tests_all_code_dump_20251028_042000.md", "tests"),
        ("src_all_code_dump_20251028_042000.md", "src"),
        ("root_all_code_dump_20251028_042000.md", "root"),
        ("a_b-c_all_code_dump_20251028_042000.md", "a_b-c"),  # Valid chars
    ],
)
def test_extract_group_prefix_valid(filename, expected):
    assert extract_group_prefix(filename) == expected


@pytest.mark.parametrize(
    "filename",
    [
        "invalid!_all_code_dump_20251028_042000.md",  # Invalid char !
        "no_prefix_code_dump_20251028_042000.md",  # No _all_code_dump_
        "all_code_dump_20251028_042000.md",  # Empty group
        "longgroupwithpath/dir_all_code_dump_20251028_042000.md",  # Path chars /
        "_all_code_dump_20251028_042000.md",  # Leading _
        "group_all_code_dump_20251028_04.md",  # Malformed TS
        "group_all_code_dump_20251028_042000.txt",  # Wrong ext
    ],
)
def test_extract_group_prefix_invalid(filename):
    assert extract_group_prefix(filename) is None


def test_extract_group_prefix_empty():
    assert extract_group_prefix("") is None
    assert extract_group_prefix("non_matching.md") is None


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("test_all_code_dump_20251028_040020.md", datetime(2025, 10, 28, 4, 0, 20)),
        ("group_all_code_dump_20251028_042000.md", datetime(2025, 10, 28, 4, 20, 0)),
    ],
)
def test_extract_timestamp_valid(filename, expected):
    assert ArchiveManager.extract_timestamp(filename) == expected


@pytest.mark.parametrize(
    "filename",
    [
        "test_all_code_dump_20251028_04.md",  # Short TS: no match
        "test_all_code_dump_invalid_ts.md",  # No match
        "malformed_2025-10-28_04:20:00.md",  # No match
    ],
)
def test_extract_timestamp_no_match(filename):
    with patch('create_dump.archiver.logger.warning') as mock_warn:
        ts = ArchiveManager.extract_timestamp(filename)
        assert ts == datetime.min
        mock_warn.assert_not_called()  # Silent fallback, no warn


@pytest.mark.parametrize(
    "filename",
    [
        "test_all_code_dump_20251328_042000.md",  # Match, invalid month=13 → ValueError + warn
        "test_all_code_dump_20251028_252000.md",  # Match, invalid hour=25 → ValueError + warn
    ],
)
def test_extract_timestamp_bad_parse(filename):
    with patch('create_dump.archiver.logger.warning') as mock_warn:
        ts = ArchiveManager.extract_timestamp(filename)
        assert ts == datetime.min
        mock_warn.assert_called_once_with("Malformed timestamp in filename: %s", filename)


@pytest.fixture
def tmp_root(tmp_path: Path):
    """Safe root for path tests."""
    return tmp_path


@pytest.mark.parametrize(
    "rel_path_str, expected",
    [
        ("dir/file.txt", "dir/file.txt"),
        ("sub/dir/file.py", "sub/dir/file.py"),
    ],
)
def test_safe_arcname_valid(tmp_root, rel_path_str, expected):
    path = tmp_root / rel_path_str
    path.parent.mkdir(exist_ok=True, parents=True)
    path.touch()  # Ensure file
    try:
        assert _safe_arcname(path, tmp_root) == expected
    finally:
        path.unlink(missing_ok=True)


@pytest.mark.parametrize(
    "rel_path_str, match_str",
    [
        ("../etc/passwd", "traversal"),
        ("dir/../sibling/file.txt", "traversal"),
    ],
)
def test_safe_arcname_traversal_reject(tmp_root, rel_path_str, match_str):
    path = tmp_root / rel_path_str
    with pytest.raises(ValueError, match=match_str):
        _safe_arcname(path, tmp_root)


def test_safe_arcname_absolute_reject(tmp_root):
    abs_path = Path("/absolute/file.txt")
    with pytest.raises(ValueError, match=r"Invalid arcname: '/absolute/file\.txt' is not in the subpath"):
        _safe_arcname(abs_path, tmp_root)


def test_safe_arcname_dir_reject(tmp_root):
    dir_path = tmp_root / "dir"
    dir_path.mkdir()
    try:
        with pytest.raises(ValueError, match="not a file"):
            _safe_arcname(dir_path, tmp_root)
    finally:
        dir_path.rmdir()


def test_safe_arcname_nonexistent_reject(tmp_root):
    nonexistent = tmp_root / "nonexistent"
    with pytest.raises(ValueError, match="not a file"):
        _safe_arcname(nonexistent, tmp_root)
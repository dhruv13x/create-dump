# tests/test_path_utils.py
"""Tests for path_utils module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import logging

from code_dump.path_utils import safe_is_within, find_matching_files, confirm


@pytest.fixture
def mock_root(tmp_path: Path):
    tmp_path.mkdir(exist_ok=True)
    return tmp_path


def test_safe_is_within_success(mock_root: Path):
    sub = mock_root / "sub"
    sub.mkdir()
    assert safe_is_within(sub, mock_root)


def test_safe_is_within_except(mock_root: Path):
    path = mock_root / "sub"
    root = mock_root
    with patch("pathlib.Path.resolve", return_value=path), \
         patch("pathlib.Path.is_relative_to", side_effect=AttributeError("Mock attr err")), \
         patch("pathlib.Path.__str__", side_effect=[str(root) + "/sub", str(root)]):
        assert safe_is_within(path, root)  # Hits str fallback


def test_find_matching_files(mock_root: Path):
    (mock_root / "test_code_dump.md").touch()
    results = find_matching_files(mock_root, r".*code_dump.*\.md$")
    assert len(results) == 1
    assert "test_code_dump.md" in results[0].name


def test_find_matching_files_empty(mock_root: Path):
    with patch("pathlib.Path.rglob", return_value=[]):
        matches = find_matching_files(mock_root, r".*code_dump.*\.md$")
    assert matches == []


def test_confirm_yes():
    with patch("builtins.input", return_value="yes"):
        assert confirm("Test?") is True


def test_confirm_no():
    with patch("builtins.input", return_value="n"):
        assert confirm("Test?") is False


def test_confirm_keyboard_interrupt(capfd):
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        assert confirm("Test?") is False
        captured = capfd.readouterr()
        assert "\n" in captured.out
# tests/test_collector.py (fixed dir creation for __pycache__)
# code_dump/tests/test_collector.py
"""Tests for collector module."""

import pytest
from pathlib import Path

from code_dump.collector import FileCollector
from code_dump.core import Config


@pytest.fixture
def mock_config():
    return Config(max_file_size_kb=None)


def test_collect_empty_dir(mock_config, tmp_path: Path):
    collector = FileCollector(mock_config, root=tmp_path)
    assert collector.collect() == []


def test_collect_with_files(mock_config, tmp_path: Path):
    (tmp_path / "test.py").touch()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "hidden.py").touch()
    collector = FileCollector(mock_config, root=tmp_path)
    files = collector.collect()
    assert len(files) == 1
    assert "test.py" in files[0]


def test_exclude_patterns(mock_config, tmp_path: Path):
    (tmp_path / "test.py").touch()
    (tmp_path / "secret.txt").touch()
    collector = FileCollector(mock_config, excludes=["*.txt"], root=tmp_path)
    files = collector.collect()
    assert len(files) == 1
    assert "test.py" in files[0]


def test_gitignore_integration(mock_config, tmp_path: Path):
    (tmp_path / ".gitignore").write_text("*.txt\n")
    (tmp_path / "test.py").touch()
    (tmp_path / "ignored.txt").touch()
    collector = FileCollector(mock_config, use_gitignore=True, root=tmp_path)
    files = collector.collect()
    assert len(files) == 1
    assert "test.py" in files[0]


import pytest
from pathlib import Path
from unittest.mock import patch

from code_dump.collector import FileCollector
from code_dump.core import Config


def test_collect_search_yield(mock_config, tmp_path: Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "test.py").touch()
    collector = FileCollector(mock_config, root=tmp_path)
    # Trigger search via dir scan
    files = collector.collect()
    assert "subdir/test.py" in files  # Yielded


def test_collect_search_exclude_dir(mock_config, tmp_path: Path):
    subdir = tmp_path / "__pycache__"
    subdir.mkdir()
    (subdir / "hidden.py").touch()
    collector = FileCollector(mock_config, root=tmp_path)
    files = collector.collect()
    assert len(files) == 0  # Excluded dir skipped in search


def test_collect_search_file_match(mock_config, tmp_path: Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "test.py").touch()
    (subdir / "secret.bin").touch()
    collector = FileCollector(mock_config, includes=["*.py"], root=tmp_path)
    files = collector.collect()
    assert len(files) == 1
    assert files[0] == "subdir/test.py"


def test_should_include_stat_exception(mock_config, tmp_path: Path):
    collector = FileCollector(mock_config, root=tmp_path)
    with patch("pathlib.Path.stat") as mock_stat:
        mock_stat.side_effect = OSError("Stat failed")
        # Use a fake path that triggers _should_include
        rel_path = Path("test.py")
        with patch.object(collector, "_include_spec") as mock_inc:
            mock_inc.match_file.return_value = True
            assert not collector._should_include(tmp_path / rel_path)  # False on OSError


def test_collect_sort(mock_config, tmp_path: Path):
    (tmp_path / "z.txt").touch()
    (tmp_path / "a.txt").touch()
    collector = FileCollector(mock_config, root=tmp_path)
    files = collector.collect()
    assert files[0] == "a.txt"  # Sorted


def test_collect_empty(mock_config, tmp_path: Path):
    collector = FileCollector(mock_config, root=tmp_path)
    files = collector.collect()
    assert files == []
    
    
def test_gitignore_loads_patterns(mock_config, tmp_path: Path):
    """Cover 109→100: .gitignore exists → parse and extend excludes."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("secret.*\nnode_modules/\n")  # Matches secret.txt; multi-line

    collector = FileCollector(mock_config, use_gitignore=True, root=tmp_path)

    # Verify extended excludes include git patterns
    assert len(collector._exclude_spec.patterns) > (
        len(mock_config.default_excludes) + len(mock_config.default_includes)
    )

    # Test exclusion: create ignored file
    (tmp_path / "secret.txt").touch()
    # Verify multi-line: create node_modules dir/file
    node_dir = tmp_path / "node_modules" / "ignored.js"
    node_dir.parent.mkdir()
    node_dir.touch()

    files = collector.collect()
    assert "secret.txt" not in files  # secret.* excluded
    assert "node_modules/ignored.js" not in files  # node_modules/ excluded
    
    
def test_matches_include_name_only(mock_config, tmp_path: Path):
    """Cover 121-123: include_spec.match_file(rel_path.name) or-branch."""
    deep_file = tmp_path / "deep" / "subdir" / "config.toml"
    deep_file.parent.mkdir(parents=True)
    deep_file.touch()
    collector = FileCollector(mock_config, includes=["*.toml"], root=tmp_path)  # Name match
    files = collector.collect()
    assert "deep/subdir/config.toml" in files  # Hits name-only branch

def test_matches_calls_should_include_on_oserror(mock_config, tmp_path: Path):
    """Cover 124→119: _matches → _should_include (OSError false)."""
    test_file = tmp_path / "test.py"
    test_file.touch()
    collector = FileCollector(mock_config, includes=["*.py"], root=tmp_path)
    with patch("code_dump.collector.is_text_file", return_value=True):  # Isolate
        with patch("pathlib.Path.stat", side_effect=OSError("Permission denied")):
            assert collector._matches(test_file.relative_to(tmp_path)) is False  # Calls _should_include → false

def test_should_include_oserror_returns_false(mock_config, tmp_path: Path):
    """Cover 149: except OSError return False in _should_include."""
    inaccessible = tmp_path / "inaccessible.py"
    inaccessible.touch()
    collector = FileCollector(mock_config, root=tmp_path)
    with patch("pathlib.Path.stat", side_effect=OSError("Access denied")):
        assert not collector._should_include(inaccessible)  # Hits except → False
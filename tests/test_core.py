# tests/test_core.py
"""Unit tests for core module."""

import pytest
from pathlib import Path
import toml
import re

from create_dump.core import (
    Config,
    GitMeta,
    DumpFile,
    load_config,
    DEFAULT_DUMP_PATTERN,
)


def test_config_validation():
    cfg = Config(max_file_size_kb=1024)
    assert cfg.max_file_size_kb == 1024
    with pytest.raises(ValueError):
        Config(max_file_size_kb=-1)  # Invalid


def test_gitmeta_model():
    meta = GitMeta(branch="main", commit="abc123")
    assert meta.branch == "main"
    assert meta.commit == "abc123"


def test_dumpfile_model():
    df = DumpFile(path="test.py", language="python")
    assert df.path == "test.py"
    assert df.language == "python"
    assert df.temp_path is None
    assert df.error is None

    error_df = DumpFile(path="fail.py", error="Error")
    assert error_df.error == "Error"
    assert error_df.language is None


def test_load_config(tmp_path: Path):
    config_path = tmp_path / "create_dump.toml"
    config_path.write_text(
        "[tool.create-dump]\n"
        "max_file_size_kb = 512\n"
        "excluded_dirs = ['custom']"
    )
    cfg = load_config(config_path)
    assert cfg.max_file_size_kb == 512
    assert "custom" in cfg.excluded_dirs


def test_load_config_no_file():
    cfg = load_config()
    assert cfg.max_file_size_kb is None


def test_config_dest_validation(tmp_path: Path):
    # Valid dest (str -> Path)
    valid_dest_str = str(tmp_path / "dumps")
    cfg = Config(dest=valid_dest_str)
    assert cfg.dest == Path(valid_dest_str)

    # Valid Path
    valid_dest_path = tmp_path / "dumps"
    cfg = Config(dest=valid_dest_path)
    assert cfg.dest == valid_dest_path

    # Empty string -> None (hits if not path.name)
    cfg = Config(dest="")
    assert cfg.dest is None

    # Invalid (non-str to hit except)
    cfg = Config(dest=123)
    assert cfg.dest is None

    # None dest
    cfg = Config(dest=None)
    assert cfg.dest is None


def test_config_dump_pattern_validation():
    # Valid pattern (matches _all_create_dump_)
    valid = r".*_all_create_dump_\d{8}_\d{6}\.md$"
    cfg = Config(dump_pattern=valid)
    assert cfg.dump_pattern == valid

    # Invalid pattern (no match) -> warning and default
    invalid = r"loose_pattern"
    cfg = Config(dump_pattern=invalid)
    assert cfg.dump_pattern == DEFAULT_DUMP_PATTERN

    # Empty -> warning and default
    cfg = Config(dump_pattern="")
    assert cfg.dump_pattern == DEFAULT_DUMP_PATTERN


def test_config_metrics_port():
    # Valid
    cfg = Config(metrics_port=8000)
    assert cfg.metrics_port == 8000

    # <1 -> ValueError
    with pytest.raises(ValueError):
        Config(metrics_port=0)

    # >65535 -> ValueError
    with pytest.raises(ValueError):
        Config(metrics_port=70000)


def test_config_non_negative_validator():
    # Valid None
    cfg = Config(max_file_size_kb=None)
    assert cfg.max_file_size_kb is None

    # Valid 0
    cfg = Config(max_file_size_kb=0)
    assert cfg.max_file_size_kb == 0

    # Valid positive
    cfg = Config(max_file_size_kb=100)
    assert cfg.max_file_size_kb == 100


def test_load_config_invalid_toml(tmp_path: Path):
    # TomlDecodeError
    invalid_toml = tmp_path / "invalid.toml"
    invalid_toml.write_text("invalid = [toml\n")  # Malformed
    cfg = load_config(invalid_toml)
    assert cfg.max_file_size_kb is None  # Defaults

    # OSError: dir as file
    dir_as_file = tmp_path / "dir.toml"
    dir_as_file.mkdir()
    cfg = load_config(dir_as_file)
    assert cfg.max_file_size_kb is None


def test_load_config_multiple_paths(monkeypatch, tmp_path: Path):
    # Mock Path.home and Path.cwd to control
    def mock_home():
        return tmp_path / "home"
    def mock_cwd():
        return tmp_path / "cwd"

    monkeypatch.setattr(Path, "home", staticmethod(mock_home))
    monkeypatch.setattr(Path, "cwd", staticmethod(mock_cwd))

    # Create home config (first in order)
    home_dir = mock_home()
    home_dir.mkdir()
    home_config = home_dir / ".create_dump.toml"
    home_config.write_text("[tool.create-dump]\nuse_gitignore = false")

    # CWD config (second)
    cwd_dir = mock_cwd()
    cwd_dir.mkdir()
    cwd_config = cwd_dir / ".create_dump.toml"
    cwd_config.write_text("[tool.create-dump]\nuse_gitignore = true")

    # Root config (third)
    root_config = tmp_path / "create_dump.toml"
    root_config.write_text("[tool.create-dump]\nuse_gitignore = maybe")

    # Loads home first
    cfg = load_config()
    assert cfg.use_gitignore == False

    # If no home, loads cwd
    home_config.unlink()
    cfg = load_config()
    assert cfg.use_gitignore == True

    # No files -> defaults
    cwd_config.unlink()
    root_config.unlink()
    cfg = load_config()
    assert cfg.use_gitignore == True  # Default


def test_load_config_tool_namespace(tmp_path: Path):
    # Correct [tool.create-dump]
    pyproject = tmp_path / "pyproject.toml"
    valid_custom_pattern = r".*_all_create_dump_custom_\d+\.md$"
    # Escape for TOML: double backslashes for literal \
    toml_pattern = valid_custom_pattern.replace("\\", "\\\\")
    pyproject.write_text(
        f"[tool.create-dump]\n"
        f"git_meta = false\n"
        f"dest = \"dumps\"\n"
        f"dump_pattern = \"{toml_pattern}\""
    )
    cfg = load_config(pyproject)
    assert cfg.git_meta == False
    assert cfg.dest == Path("dumps")
    assert cfg.dump_pattern == valid_custom_pattern  # Valid, no enforcement

    # No [tool], empty dict
    bad_pyproject = tmp_path / "bad.toml"
    bad_pyproject.write_text("[other]\nkey = value")
    cfg = load_config(bad_pyproject)
    assert cfg.git_meta == True  # Default
    assert cfg.dest is None

    # Nested get handles missing


def test_config_excluded_dirs():
    # Default
    cfg = Config()
    assert "__pycache__" in cfg.excluded_dirs
    assert len(cfg.excluded_dirs) > 1

    # Override
    custom = Config(excluded_dirs=["test_dir"])
    assert custom.excluded_dirs == ["test_dir"]


# Doctest coverage (if enabled)
def test_load_config_doctest():
    # Approximate doctest; actual runs in CLI --test
    cfg = load_config()
    assert isinstance(cfg, Config)
    assert cfg.excluded_dirs == [
        "__pycache__",
        ".git",
        ".venv",
        "venv",
        "myenv",
        ".mypy_cache",
        ".pytest_cache",
        ".idea",
        "node_modules",
        "build",
        "dist",
        "vendor",
        ".gradle",
        ".tox",
        "eggs",
        ".egg-info",
    ]
# tests/test_cli.py
"""Tests for CLI module."""

import re
import pytest
from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock, ANY

from create_dump.cli import app
from create_dump.core import DEFAULT_DUMP_PATTERN  # Import for pattern default


runner = CliRunner()


def strip_ansi(s: str) -> str:
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', s)


def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "create-dump v6.0.0" in strip_ansi(result.stdout)


@patch("create_dump.cli.run_single")
def test_cli_single_dry_run(mock_run_single, tmp_path: Path):
    (tmp_path / "test.py").touch()
    result = runner.invoke(app, ["single", str(tmp_path), "--dry-run"])
    assert result.exit_code == 0
    mock_run_single.assert_called_once()


@patch("create_dump.cli.run_batch")
def test_cli_batch_run(mock_run_batch, tmp_path: Path):
    result = runner.invoke(app, ["batch", "run", str(tmp_path)])
    assert result.exit_code == 0
    mock_run_batch.assert_called_once()


@patch("create_dump.cli.safe_cleanup")
def test_cli_batch_clean(mock_clean, tmp_path: Path):
    result = runner.invoke(app, ["batch", "clean", str(tmp_path), DEFAULT_DUMP_PATTERN])  # positional pattern
    assert result.exit_code == 0
    mock_clean.assert_called_once()


@patch('doctest.testmod')
@patch('create_dump.utils.get_git_meta')  # Patch to avoid doctest whitespace error
def test_cli_single_test(mock_git_meta, mock_testmod, tmp_path: Path):
    mock_git_meta.return_value = MagicMock()  # Mock to pass doctest
    result = runner.invoke(app, ["single", str(tmp_path), "--test"])
    assert result.exit_code == 0
    assert "All tests passed" in strip_ansi(result.stdout)
    assert mock_testmod.call_count == 5


@patch("create_dump.cli.run_batch")
def test_cli_batch_dirs_split(mock_run_batch, tmp_path: Path):
    # Comma-separated string
    result = runner.invoke(app, ["batch", "run", str(tmp_path), "--dirs", ".,src,tests"])
    assert result.exit_code == 0
    mock_run_batch.assert_called_once()
    call_kwargs = mock_run_batch.call_args.kwargs
    assert call_kwargs["subdirs"] == [".", "src", "tests"]

    # Default (no --dirs)
    mock_run_batch.reset_mock()
    result = runner.invoke(app, ["batch", "run", str(tmp_path)])
    assert result.exit_code == 0
    call_kwargs = mock_run_batch.call_args.kwargs
    assert call_kwargs["subdirs"] == [".", "packages", "services"]

    # Edge: Empty comma-string (defaults)
    mock_run_batch.reset_mock()
    result = runner.invoke(app, ["batch", "run", str(tmp_path), "--dirs", ", ,, "])
    assert result.exit_code == 0
    call_kwargs = mock_run_batch.call_args.kwargs
    assert call_kwargs["subdirs"] == [".", "packages", "services"]


@patch("create_dump.cli.setup_logging")
def test_cli_batch_callback(mock_setup, tmp_path: Path):
    result = runner.invoke(app, ["batch", "--verbose", "run", str(tmp_path)])
    assert result.exit_code == 0
    mock_setup.assert_called_once_with(verbose=True, quiet=False)


@patch('create_dump.cli.run_single')
def test_cli_default_invoke_single(mock_run_single):
    result = runner.invoke(app, ["single"])
    assert result.exit_code == 0
    mock_run_single.assert_called_once()


def test_cli_single_root_validation():
    result = runner.invoke(app, ["single", "/nonexistent"])
    assert result.exit_code == 2
    assert "Root '/nonexistent' is not a directory" in result.stderr


# New tests for 95%+ coverage
@patch('create_dump.cli.load_config')
def test_cli_main_callback_config(mock_load_config):
    result = runner.invoke(app, ["--config", "test.toml"])
    assert result.exit_code == 0
    mock_load_config.assert_called_once_with(Path("test.toml"))


@patch('create_dump.cli.run_single')
def test_cli_single_dest_propagate(mock_run_single):
    result = runner.invoke(app, ["single", "--dest", "dumps/"])  # Explicit command for reliable mock capture
    assert result.exit_code == 0
    mock_run_single.assert_called_once()
    assert mock_run_single.call_args.kwargs['dest'] == Path("dumps/")


@patch('create_dump.archiver.ArchiveManager')
@patch('create_dump.cli.setup_logging')
def test_cli_batch_archive(mock_logging, mock_manager, tmp_path: Path):
    mock_manager_instance = MagicMock()
    mock_manager.return_value = mock_manager_instance
    mock_manager_instance.run.return_value = None

    result = runner.invoke(app, ["batch", "archive", str(tmp_path)])
    assert result.exit_code == 0
    mock_manager.assert_called_once()
    call_args, call_kwargs = mock_manager.call_args
    assert len(call_args) == 5
    assert call_args[0] == tmp_path
    assert call_kwargs == {
        'search': False,
        'dry_run': True,
        'yes': False,
        'verbose': False,
        'md_pattern': r'.*_all_create_dump_\d{8}_\d{6}\.(md(\.gz)?)$',
        'archive_all': False
    }
    mock_manager_instance.run.assert_called_once()


@patch('create_dump.archiver.ArchiveManager')
@patch('create_dump.cli.setup_logging')
def test_cli_batch_archive_flags(mock_logging, mock_manager, tmp_path: Path):
    mock_manager_instance = MagicMock()
    mock_manager.return_value = mock_manager_instance
    mock_manager_instance.run.return_value = None

    result = runner.invoke(app, [
        "batch", "archive", str(tmp_path), r".*_custom",
        "--archive-search",
        "--archive-all",
        "--no-archive-keep-latest",
        "--archive-keep-last", "3",
        "--archive-clean-root",
    ])
    assert result.exit_code == 0
    mock_manager.assert_called_once()
    call_args, call_kwargs = mock_manager.call_args
    assert len(call_args) == 5
    assert call_args[2] == False  # keep_latest=False
    assert call_args[3] == 3  # keep_last=3
    assert call_args[4] == True  # clean_root=True
    assert call_kwargs['search'] == True
    assert call_kwargs['md_pattern'] == r".*_custom"
    assert call_kwargs['archive_all'] == True


@patch('create_dump.cli.run_batch')
def test_cli_batch_run_accept_prompts(mock_run_batch, tmp_path: Path):
    result = runner.invoke(app, ["batch", "run", str(tmp_path), "--no-accept-prompts"])
    assert result.exit_code == 0
    call_kwargs = mock_run_batch.call_args.kwargs
    assert call_kwargs['accept_prompts'] == False


@patch('create_dump.cli.run_batch')
def test_cli_batch_run_pattern(mock_run_batch, tmp_path: Path):
    result = runner.invoke(app, ["batch", "run", str(tmp_path), "--pattern", r".*_test_\d+"])
    assert result.exit_code == 0
    call_kwargs = mock_run_batch.call_args.kwargs
    assert call_kwargs['pattern'] == r".*_test_\d+"


@patch('create_dump.cli.safe_cleanup')
def test_cli_batch_clean_pattern(mock_clean, tmp_path: Path):
    result = runner.invoke(app, ["batch", "clean", str(tmp_path), r".*_old"])  # positional pattern
    assert result.exit_code == 0
    call_args = mock_clean.call_args.args
    assert call_args[1] == r".*_old"


@patch('create_dump.archiver.ArchiveManager')
@patch('create_dump.cli.setup_logging')
def test_cli_batch_archive_pattern(mock_logging, mock_manager, tmp_path: Path):
    mock_manager_instance = MagicMock()
    mock_manager.return_value = mock_manager_instance
    mock_manager_instance.run.return_value = None

    result = runner.invoke(app, ["batch", "archive", str(tmp_path), r".*_archive"])  # positional pattern
    assert result.exit_code == 0
    call_args, call_kwargs = mock_manager.call_args
    assert len(call_args) == 5
    assert call_args[4] == False  # clean_root default
    assert call_kwargs['md_pattern'] == r".*_archive"


@patch('create_dump.cli.run_single')
def test_cli_single_no_toc(mock_run_single, tmp_path: Path):
    result = runner.invoke(app, ["single", str(tmp_path), "--no-toc"])
    assert result.exit_code == 0
    call_kwargs = mock_run_single.call_args.kwargs
    assert call_kwargs['no_toc'] == True


@patch('create_dump.cli.run_single')
def test_cli_single_exclude(mock_run_single, tmp_path: Path):
    result = runner.invoke(app, ["single", str(tmp_path), "--exclude", "*.log"])
    assert result.exit_code == 0
    call_kwargs = mock_run_single.call_args.kwargs
    assert call_kwargs['exclude'] == "*.log"


@patch('create_dump.cli.run_single')
def test_cli_single_archive_flags(mock_run_single, tmp_path: Path):
    result = runner.invoke(app, ["single", str(tmp_path), "--archive", "--archive-all", "--archive-search"])
    assert result.exit_code == 0
    call_kwargs = mock_run_single.call_args.kwargs
    assert call_kwargs['archive'] == True
    assert call_kwargs['archive_all'] == True
    assert call_kwargs['archive_search'] == True


@patch('create_dump.cli.run_batch')
def test_cli_batch_run_dest_local(mock_run_batch, tmp_path: Path):
    result = runner.invoke(app, ["batch", "run", str(tmp_path), "--dest", "central/"])
    assert result.exit_code == 0
    call_kwargs = mock_run_batch.call_args.kwargs
    assert call_kwargs['dest'] == Path("central/")


@patch('create_dump.cli.run_batch')
def test_cli_batch_run_no_dry_run_override(mock_run_batch, tmp_path: Path):
    result = runner.invoke(app, ["batch", "run", str(tmp_path), "--no-dry-run"])
    assert result.exit_code == 0
    call_kwargs = mock_run_batch.call_args.kwargs
    assert call_kwargs['dry_run'] == False


@patch('create_dump.cli.safe_cleanup')
def test_cli_batch_clean_no_dry_run(mock_clean, tmp_path: Path):
    result = runner.invoke(app, ["batch", "clean", str(tmp_path), "--no-dry-run"])
    assert result.exit_code == 0
    call_kwargs = mock_clean.call_args.kwargs
    assert call_kwargs['dry_run'] == False


@patch('create_dump.archiver.ArchiveManager')
@patch('create_dump.cli.setup_logging')
def test_cli_batch_archive_no_dry_run(mock_logging, mock_manager, tmp_path: Path):
    mock_manager_instance = MagicMock()
    mock_manager.return_value = mock_manager_instance
    mock_manager_instance.run.return_value = None

    result = runner.invoke(app, ["batch", "archive", str(tmp_path), "--no-dry-run"])
    assert result.exit_code == 0
    call_args, call_kwargs = mock_manager.call_args
    assert len(call_args) == 5
    assert call_kwargs['dry_run'] == False
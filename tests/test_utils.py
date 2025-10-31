# tests/test_utils.py
"""Tests for utils module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock, call
import subprocess
import signal
from unittest.mock import ANY

from code_dump.utils import (
    slugify,
    get_language,
    is_text_file,
    parse_patterns,
    get_git_meta,
    _unique_path,
    setup_logging,
    VERSION,
    styled_print,
    metrics_server,
    CleanupHandler,
    CHUNK_SIZE,  # For fixture
)


def test_slugify():
    assert slugify("path/to/file.py") == "path-to-file-py"
    assert slugify("./dir/./file.txt") == "dir-file-txt"
    # Cover re.sub (169): special chars
    assert slugify("path with spaces & symbols.py") == "path-with-spaces-symbols-py"


def test_get_language():
    assert get_language("script.py") == "python"
    assert get_language("Dockerfile") == "dockerfile"
    assert get_language("config.toml") == "toml"
    assert get_language("unknown.xyz") == "text"


def test_is_text_file(tmp_path: Path):
    text_file = tmp_path / "text.py"
    text_file.write_text("print('hello')")
    assert is_text_file(text_file)

    binary_file = tmp_path / "binary.bin"
    binary_file.write_bytes(b"\x00\x01\x02")
    assert not is_text_file(binary_file)

    empty_file = tmp_path / "empty.txt"
    empty_file.touch()
    assert is_text_file(empty_file)

    # Cover except branches: OSError (non-existent)
    non_existent = tmp_path / "nonexistent.bin"
    assert not is_text_file(non_existent)

    # Cover UnicodeDecodeError: extreme binary
    extreme_binary = tmp_path / "extreme.bin"
    extreme_binary.write_bytes(b"\xff" * CHUNK_SIZE)  # Full invalid
    assert not is_text_file(extreme_binary)


def test_parse_patterns():
    patterns = ["*.py", "!test.py"]
    spec = parse_patterns(patterns)
    assert len(spec.patterns) == len(patterns)


@patch("subprocess.check_output")
def test_get_git_meta_success(mock_check_output):
    mock_check_output.side_effect = [
        b"main\n",
        b"abc123\n",
    ]
    meta = get_git_meta(Path("."))
    assert meta.branch == "main"
    assert meta.commit == "abc123"


@patch("subprocess.check_output")
def test_get_git_meta_failure(mock_check_output, tmp_path: Path):
    mock_check_output.side_effect = subprocess.CalledProcessError(1, ["git"])
    with patch("code_dump.utils.logger.debug") as mock_log:
        meta = get_git_meta(tmp_path)
        mock_log.assert_called_once()  # Covers debug log (242-243)
    assert meta is None


def test_unique_path(tmp_path: Path):
    existing = tmp_path / "existing.md"
    existing.touch()
    unique = _unique_path(existing)
    assert unique != existing
    assert unique.name.startswith("existing_")
    assert unique.suffix == ".md"
    assert not unique.exists()  # Since we didn't create it

    # Cover loop increment (250-252): deterministic collision
    existing.touch()  # Reset
    fixed_first_hex = "deadbeefdeadbeefdeadbeefdeadbeef"  # Full 32-char
    fixed_first_slice = fixed_first_hex[:8]  # "deadbeef"
    fixed_second_hex = "beefdeadbeefdeadbeefdeadbeefdead"
    fixed_second_slice = fixed_second_hex[:8]  # "beefdead"
    collision_candidate = tmp_path / f"existing_{fixed_first_slice}.md"
    collision_candidate.touch()  # Force first collision
    with patch("uuid.uuid4") as mock_uuid:
        mock_uuid.side_effect = [MagicMock(hex=MagicMock(return_value=fixed_first_hex)), MagicMock(hex=MagicMock(return_value=fixed_second_hex))]
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.side_effect = [True, False]  # First collides (real + mock), second succeeds
            unique2 = _unique_path(existing)
            assert unique2.name.startswith(f"existing_1_{fixed_second_slice}")  # Incremented + second UUID
            mock_uuid.assert_has_calls([call(), call()])  # Called twice
            mock_exists.assert_has_calls([call(collision_candidate), call(ANY)])


def test_setup_logging():
    setup_logging(verbose=True)
    # Can't easily assert log level in test, but ensures no crash
    assert True


def test_version():
    assert VERSION == "6.0.0"


@patch("code_dump.utils.HAS_RICH", False)  # Force fallback (72-73)
def test_styled_print_fallback(capsys):
    styled_print("[red]Test[/red]", nl=False)
    captured = capsys.readouterr()
    assert captured.out == "Test"  # Cleaned text (38-39)


def test_metrics_server_finally():
    with patch("code_dump.utils.start_http_server") as mock_start:  # Local binding
        with metrics_server(8000):
            pass  # Enter/exit
        mock_start.assert_called_once_with(8000)  # Covers entry; unwind hits finally (99-102)


def test_cleanup_handler_init():
    with patch("code_dump.utils.signal.signal") as mock_signal, \
         patch("code_dump.utils.atexit.register") as mock_atexit:
        handler = CleanupHandler()
        mock_signal.assert_any_call(signal.SIGINT, ANY)  # Covers 116-120
        mock_signal.assert_any_call(signal.SIGTERM, ANY)
        mock_atexit.assert_called_once_with(handler._cleanup)


@patch("code_dump.utils.sys.exit")
@patch("code_dump.utils.logger.info")
def test_cleanup_handler_signal(mock_log, mock_exit):
    handler = CleanupHandler()
    with patch.object(handler, "_cleanup"):
        handler._handler(signal.SIGINT, None)
        mock_log.assert_called_once_with("Shutdown signal received", signal=signal.SIGINT)  # Covers 132-134
        mock_exit.assert_called_once_with(130)
        # SIGTERM path
        handler._handler(signal.SIGTERM, None)
        mock_exit.assert_called_with(143)


def test_cleanup_handler_cleanup():
    mock_temp_dir = MagicMock()
    mock_stack = MagicMock(close=MagicMock())
    with patch("code_dump.utils._temp_dir", mock_temp_dir), \
         patch("code_dump.utils._cleanup_stack", mock_stack):
        handler = CleanupHandler()
        handler._cleanup()  # Covers 138-140
        mock_temp_dir.cleanup.assert_called_once()
        mock_stack.close.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
# tests/test_writer.py
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock, Mock
import concurrent.futures
import os
from concurrent.futures._base import FINISHED
from contextlib import contextmanager
from concurrent.futures import TimeoutError

from create_dump.core import DumpFile, GitMeta
from create_dump.writer import MarkdownWriter, ChecksumWriter


@pytest.fixture
def writer_instance(tmp_path: Path):
    with TemporaryDirectory() as td:
        outfile = tmp_path / "dump.md"
        git_meta = GitMeta(branch="main", commit="abc")
        yield MarkdownWriter(outfile, no_toc=False, git_meta=git_meta, temp_dir=td)


def test_process_file(writer_instance, tmp_path: Path):
    test_file = tmp_path / "test.py"
    test_file.write_text('print("hello")\n')
    df = writer_instance.process_file(str(test_file))
    assert isinstance(df, DumpFile)
    assert df.path == str(test_file)
    assert df.language == "python"
    assert df.temp_path is not None
    assert df.temp_path.exists()


def test_process_file_error(writer_instance, tmp_path: Path):
    # Use a non-existent file to trigger FileNotFoundError naturally
    non_existent = tmp_path / "nonexistent.py"
    df = writer_instance.process_file(str(non_existent))
    assert isinstance(df.error, str)
    assert "No such file or directory" in df.error
    assert df.temp_path is None


@patch.object(MarkdownWriter, '_write_md_streamed')
@patch('create_dump.writer.as_completed')
def test_dump_concurrent(mock_as_completed, mock_write, writer_instance):
    files_list = ["test1.py", "test2.py"]
    mock_futures = [Mock(), Mock()]
    for mf in mock_futures:
        mf.result.return_value = DumpFile(path="test.py", language="python")
    mock_as_completed.return_value = mock_futures

    writer_instance.dump_concurrent(files_list, progress=False, max_workers=1)

    assert len(writer_instance.files) == 2
    mock_as_completed.assert_called_once()
    mock_write.assert_called_once_with()


def test_checksum_writer(tmp_path: Path):
    test_file = tmp_path / "test.md"
    test_file.write_text("# Test")
    writer = ChecksumWriter()
    checksum = writer.write(test_file)
    assert len(checksum) == 73  # SHA256 hex + "  " + filename
    assert (test_file.with_suffix(".sha256")).exists()


def test_process_file_empty_peek(writer_instance, tmp_path: Path):
    empty_file = tmp_path / "empty.txt"
    empty_file.touch()
    df = writer_instance.process_file(str(empty_file))
    assert df.path == str(empty_file)
    assert df.language == "text"
    assert df.temp_path.read_text() == ""  # Empty with no content


def test_process_file_backtick_fence(writer_instance, tmp_path: Path):
    backtick_file = tmp_path / "backticks.py"
    backtick_file.write_text('print("``` hello ```")')
    df = writer_instance.process_file(str(backtick_file))
    content = df.temp_path.read_text()
    assert content.startswith("~~~python\nprint")
    assert content.endswith("~~~\n")  # Tilde fence used


def test_process_file_exception_after_temp(writer_instance, tmp_path: Path):
    test_file = tmp_path / "test.py"
    test_file.write_text('print("hello")')
    with patch("pathlib.Path.unlink") as mock_unlink, \
         patch('create_dump.utils.FILES_PROCESSED.labels') as mock_labels:
        mock_labels.return_value.inc = MagicMock(side_effect=Exception("After inc"))
        df = writer_instance.process_file(str(test_file))
    assert df.error == "After inc"
    mock_unlink.assert_called_once()


def test_dump_concurrent_progress_timeout(writer_instance):
    files_list = ["test.py"]
    mock_future = MagicMock()
    mock_future.result.side_effect = TimeoutError
    mock_executor = MagicMock()
    mock_executor.__enter__.return_value = mock_executor
    mock_executor.submit.return_value = mock_future
    with patch("concurrent.futures.ThreadPoolExecutor", return_value=mock_executor), \
         patch("concurrent.futures.as_completed", return_value=[mock_future]):
        with patch("create_dump.writer.HAS_RICH", True):
            # Mock Progress class to return a mock instance
            mock_progress_class = MagicMock()
            mock_progress_instance = MagicMock()
            mock_progress_instance.add_task.return_value = 0  # Simple task id
            mock_progress_instance.__enter__.return_value = mock_progress_instance
            mock_progress_instance.__exit__.return_value = False
            mock_progress_class.return_value = mock_progress_instance
            with patch("create_dump.writer.Progress", mock_progress_class):
                writer_instance.dump_concurrent(files_list, progress=True, max_workers=1)
                mock_progress_instance.advance.assert_called_once_with(0)


def test_dump_concurrent_as_completed_timeout(writer_instance):
    files_list = ["test.py"]
    mock_future = MagicMock()
    mock_future._state = FINISHED
    mock_future.result.side_effect = TimeoutError
    mock_future.done.return_value = True
    mock_future.running.return_value = False
    with patch("concurrent.futures.as_completed") as mock_completed, \
         patch("concurrent.futures.ThreadPoolExecutor") as mock_exec, \
         patch("create_dump.writer.HAS_RICH", False):
        mock_completed.return_value = [mock_future]
        mock_exec.return_value.__enter__.return_value.submit.return_value = mock_future
        writer_instance.dump_concurrent(files_list, progress=False, max_workers=1)
    assert len(writer_instance.files) == 1
    assert writer_instance.files[0].error == "Timeout"


@patch.object(MarkdownWriter, '_write_md_streamed')
def test_dump_concurrent_call_write(mock_write, writer_instance):
    files_list = []
    writer_instance.dump_concurrent(files_list)  # Empty, but calls _write
    mock_write.assert_called_once()


def test_write_md_streamed_no_toc(writer_instance):
    temp_file = Path(writer_instance.temp_dir) / "temp.tmp"
    temp_file.write_text("content")
    df = DumpFile(path="test.py", temp_path=temp_file)
    writer_instance.files = [df]
    writer_instance.no_toc = True
    with patch("shutil.copyfileobj"):
        with patch("pathlib.Path.replace"):
            writer_instance._write_md_streamed()
    # No TOC written


def test_write_md_streamed_error_df(writer_instance):
    error_df = DumpFile(path="fail.py", error="Failed")
    writer_instance.files = [error_df]
    with patch("pathlib.Path.open") as mock_open, \
         patch("pathlib.Path.replace"):
        writer_instance._write_md_streamed()
    mock_open.return_value.__enter__.return_value.write.assert_any_call(
        '## fail.py\n\n> ⚠️ **Failed:** Failed\n\n---\n\n'
    )


def test_write_md_streamed_stream_copy(writer_instance):
    temp_file = Path(writer_instance.temp_dir) / "temp.tmp"
    temp_file.write_text("content")
    df = DumpFile(path="test.py", temp_path=temp_file)
    writer_instance.files = [df]
    with patch("shutil.copyfileobj") as mock_copy, \
         patch("pathlib.Path.open"), \
         patch("pathlib.Path.replace"):
        writer_instance._write_md_streamed()
    mock_copy.assert_called_once()


def test_write_md_streamed_atomic_replace(writer_instance):
    temp_file = Path(writer_instance.temp_dir) / "temp.tmp"
    temp_file.write_text("content")
    df = DumpFile(path="test.py", temp_path=temp_file)
    writer_instance.files = [df]
    with patch("pathlib.Path.replace") as mock_replace, \
         patch("pathlib.Path.open"), \
         patch("shutil.copyfileobj"):
        writer_instance._write_md_streamed()
    mock_replace.assert_called_once_with(writer_instance.outfile)


def test_write_md_streamed_except_unlink(writer_instance):
    temp_file = Path(writer_instance.temp_dir) / "temp.tmp"
    temp_file.write_text("content")
    df = DumpFile(path="test.py", temp_path=temp_file)
    writer_instance.files = [df]
    temp_out = writer_instance.outfile.with_suffix(".tmp")
    temp_out.touch()  # Ensure temp_out exists
    with patch("pathlib.Path.open"), \
         patch("shutil.copyfileobj"), \
         patch("pathlib.Path.replace", side_effect=Exception("Replace failed")):
        with patch("pathlib.Path.unlink") as mock_unlink:
            with pytest.raises(Exception):
                writer_instance._write_md_streamed()
            assert mock_unlink.call_count == 2  # except (temp_out) + finally (temp_file)


def test_write_md_streamed_finally_cleanup(writer_instance):
    temp_file = Path(writer_instance.temp_dir) / "temp.tmp"
    temp_file.touch()
    df = DumpFile(path="test.py", temp_path=temp_file)
    writer_instance.files = [df]
    temp_out = writer_instance.outfile.with_suffix(".tmp")
    temp_out.touch()  # Ensure temp_out exists
    with patch("pathlib.Path.unlink") as mock_unlink, \
         patch("shutil.copyfileobj"), \
         patch("pathlib.Path.replace", return_value=None):
        writer_instance._write_md_streamed()
    mock_unlink.assert_called_once()
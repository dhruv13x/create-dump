# tests/test_processor_coverage.py

import pytest
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import anyio
import uuid

from create_dump.processor import FileProcessor, ProcessorMiddleware
from create_dump.core import DumpFile

@pytest.fixture
def mock_temp_dir(tmp_path):
    temp_dir = tmp_path / "temp"
    temp_dir.mkdir()
    return temp_dir

@pytest.mark.anyio
class TestProcessorCoverage:

    async def test_process_file_with_middleware(self, mock_temp_dir):
        # Create dummy file
        src_file = mock_temp_dir / "test.py"
        src_file.write_text("print('hello')")

        # Define middleware
        class MockMiddleware:
            async def process(self, dump_file: DumpFile) -> None:
                dump_file.language = "modified_lang"

        processor = FileProcessor(str(mock_temp_dir), middlewares=[MockMiddleware()])

        result = await processor.process_file(str(src_file))

        assert result.language == "modified_lang"
        assert result.error is None
        assert result.temp_path.exists()
        assert result.temp_path.read_text() == "print('hello')"

    async def test_process_file_middleware_error(self, mock_temp_dir):
        # Create dummy file
        src_file = mock_temp_dir / "test.py"
        src_file.write_text("print('secret')")

        # Define middleware that errors out
        class MockMiddleware:
            async def process(self, dump_file: DumpFile) -> None:
                dump_file.error = "Secret found"

        processor = FileProcessor(str(mock_temp_dir), middlewares=[MockMiddleware()])

        result = await processor.process_file(str(src_file))

        assert result.error == "Secret found"
        # Temp file should still exist as it was created before middleware
        assert result.temp_path.exists()

    async def test_process_file_read_error(self, mock_temp_dir):
        src_file = mock_temp_dir / "test.py"
        # Don't create the file, so open fails

        processor = FileProcessor(str(mock_temp_dir))

        result = await processor.process_file(str(src_file))

        assert result.error is not None
        assert "No such file" in result.error or "not found" in result.error

    async def test_process_file_write_error(self, mock_temp_dir):
        src_file = mock_temp_dir / "test.py"
        src_file.write_text("content")

        processor = FileProcessor(str(mock_temp_dir))

        original_open = anyio.Path.open

        # Use simple recursion protection or check path
        async def side_effect_open(self, mode="r", *args, **kwargs):
            # self is the anyio.Path instance
            if "w" in mode:
                raise OSError("Write failed")
            return await original_open(self, mode, *args, **kwargs)

        with patch("anyio.Path.open", side_effect=side_effect_open):
             result = await processor.process_file(str(src_file))

             assert result.error is not None
             # We don't check specific error message because internal errors might obscure it
             # The goal is to ensure we entered the except block

    async def test_dump_concurrent_timeout(self, mock_temp_dir):
        src_file = mock_temp_dir / "test.py"
        src_file.write_text("content")

        processor = FileProcessor(str(mock_temp_dir))

        # Mock process_file on the instance.
        processor.process_file = AsyncMock(side_effect=TimeoutError("Timeout"))

        results = await processor.dump_concurrent([str(src_file)], progress=False)

        assert len(results) == 1
        assert results[0].error == "Timeout"

    async def test_dump_concurrent_exception(self, mock_temp_dir):
        src_file = mock_temp_dir / "test.py"
        src_file.write_text("content")

        processor = FileProcessor(str(mock_temp_dir))

        processor.process_file = AsyncMock(side_effect=Exception("General Error"))

        results = await processor.dump_concurrent([str(src_file)], progress=False)

        assert len(results) == 1
        assert "Unhandled exception" in results[0].error

    async def test_dump_concurrent_with_progress(self, mock_temp_dir):
        src_file = mock_temp_dir / "test.py"
        src_file.write_text("content")

        processor = FileProcessor(str(mock_temp_dir))

        # Mock HAS_RICH to True
        with patch("create_dump.processor.HAS_RICH", True):
            with patch("create_dump.processor.console", MagicMock()):
                 results = await processor.dump_concurrent([str(src_file)], progress=True)

        assert len(results) == 1
        assert results[0].path == str(src_file)
        assert results[0].error is None

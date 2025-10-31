"""Tests for single dump runner."""

import pytest
from pathlib import Path
from typing import Optional
from unittest.mock import patch, MagicMock, call, ANY
from typer import Exit
from contextlib import nullcontext

from create_dump.single import run_single
from create_dump.core import GitMeta, load_config, Config


@pytest.fixture
def mock_root(tmp_path: Path):
    tmp_path.mkdir(exist_ok=True)
    return tmp_path


class TestRunSingle:
    @pytest.mark.parametrize("max_size", [None, 1024])  # Coverage: 80-82 override
    def test_valid_root_success(self, mock_root: Path, max_size: Optional[int]):
        mock_root.joinpath("test.py").write_text("content")
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single.get_git_meta") as mock_git, \
             patch("create_dump.single._unique_path") as mock_unique, \
             patch("create_dump.single.metrics_server") as mock_server, \
             patch("create_dump.single.DUMP_DURATION") as mock_duration, \
             patch("create_dump.single.MarkdownWriter") as mock_writer, \
             patch("create_dump.single.ChecksumWriter") as mock_checksum, \
             patch("create_dump.single.ArchiveManager") as mock_archive:
            # Use real Config for model_copy override testing
            runner_cfg = Config(max_file_size_kb=100, use_gitignore=True)
            if max_size is not None:
                runner_cfg = runner_cfg.model_copy(update={"max_file_size_kb": max_size})
            mock_load.return_value = Config(max_file_size_kb=100, use_gitignore=True)  # Base; override in-call
            mock_collector.return_value.collect.return_value = ["test.py"]
            mock_git.return_value = GitMeta(branch="main", commit="abc123")
            mock_unique.return_value = mock_root / "dump.md"
            mock_server.return_value.__enter__.return_value = None
            mock_server.return_value.__exit__.return_value = False
            mock_duration.time.return_value.__enter__.return_value = None
            mock_duration.time.return_value.__exit__.return_value = False
            mock_writer.return_value.dump_concurrent.return_value = None
            mock_writer.return_value.files = [MagicMock(error=None)]
            mock_checksum.return_value.write.return_value = "abc123"
            mock_archive.return_value.run.return_value = {'default': Path("archive.zip")}
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=max_size,  # Param for override
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=4,
                archive=True,
                archive_all=False,
                archive_search=False,
                archive_include_current=True,
                archive_no_remove=False,
                archive_keep_latest=True,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=True,
                quiet=False,
            )
            # Assert on updated config in collector call
            collector_call = mock_collector.call_args.args[0]
            assert collector_call.max_file_size_kb == (max_size or 100)
            mock_writer.assert_called_once_with(mock_unique.return_value, False, mock_git.return_value, ANY)
            mock_writer.return_value.dump_concurrent.assert_called_once_with(["test.py"], True, 4)
            mock_checksum.assert_called_once()
            mock_checksum.return_value.write.assert_called_once_with(mock_unique.return_value)
            mock_archive.assert_called_once_with(
                root=mock_root,
                timestamp=ANY,
                keep_latest=True,
                keep_last=None,
                clean_root=False,
                search=False,
                include_current=True,
                no_remove=False,
                dry_run=False,
                yes=True,  # Reuse force for yes
                verbose=True,
                md_pattern=ANY,  # Enforce strict from cfg
                archive_all=False,
            )
            mock_archive.return_value.run.assert_called_once_with(current_outfile=mock_unique.return_value)

    def test_dry_run(self, mock_root: Path):
        mock_root.joinpath("test.py").write_text("content")
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single.styled_print") as mock_print, \
             patch("create_dump.single.MarkdownWriter") as mock_writer:
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)  # Real Config
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            run_single(
                root=mock_root,
                dry_run=True,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=4,
                archive=False,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=True,
                quiet=False,
            )
            mock_collector.assert_called_once_with(mock_config, [], [], True, mock_root)
            mock_print.assert_any_call("[green]✅ Dry run: Would process listed files.[/green]")
            mock_writer.assert_not_called()  # No write on dry-run

    @pytest.mark.parametrize("allow_empty, expected_exit", [(True, None), (False, 1)])  # Coverage: 173-176
    def test_no_files_allow_empty(self, mock_root: Path, allow_empty: bool, expected_exit: Optional[int]):
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single.logger.warning") as mock_warn, \
             patch("create_dump.single.styled_print") as mock_print:
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)  # Real
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = []
            if expected_exit:
                with pytest.raises(Exit) as exc_info:
                    run_single(
                        root=mock_root,
                        dry_run=False,
                        yes=True,
                        no_toc=False,
                        compress=False,
                        exclude="**/*",
                        include="",
                        max_file_size=None,
                        use_gitignore=True,
                        git_meta=True,
                        progress=True,
                        max_workers=4,
                        archive=False,
                        archive_all=False,
                        archive_search=False,
                        archive_include_current=False,
                        archive_no_remove=False,
                        archive_keep_latest=False,
                        archive_keep_last=None,
                        archive_clean_root=False,
                        allow_empty=allow_empty,
                        metrics_port=0,
                        verbose=True,
                        quiet=False,
                    )
                assert exc_info.value.exit_code == expected_exit
            else:
                run_single(
                    root=mock_root,
                    dry_run=False,
                    yes=True,
                    no_toc=False,
                    compress=False,
                    exclude="**/*",
                    include="",
                    max_file_size=None,
                    use_gitignore=True,
                    git_meta=True,
                    progress=True,
                    max_workers=4,
                    archive=False,
                    archive_all=False,
                    archive_search=False,
                    archive_include_current=False,
                    archive_no_remove=False,
                    archive_keep_latest=False,
                    archive_keep_last=None,
                    archive_clean_root=False,
                    allow_empty=allow_empty,
                    metrics_port=0,
                    verbose=True,
                    quiet=False,
                )
            mock_warn.assert_called_once_with("⚠️ No matching files found; skipping dump.")
            if allow_empty:
                mock_print.assert_called_with("[yellow]⚠️ No matching files found; skipping dump.[/yellow]")

    def test_invalid_root(self, mock_root: Path):
        invalid_root = mock_root / "invalid"
        with pytest.raises(ValueError, match="Invalid root"):
            run_single(
                root=invalid_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=4,
                archive=False,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=True,
                quiet=False,
            )

    def test_compress(self, mock_root: Path):
        mock_root.joinpath("test.py").write_text("content")
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single._unique_path") as mock_unique, \
             patch("create_dump.single.gzip") as mock_gzip, \
             patch("create_dump.single.shutil") as mock_shutil, \
             patch("create_dump.single.ChecksumWriter") as mock_checksum:
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)  # Real
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            mock_unique.return_value = mock_root / "dump.md"
            mock_shutil.copyfileobj.return_value = None
            mock_gzip.open.return_value.__enter__.return_value = MagicMock()
            mock_gzip.open.return_value.__exit__.return_value = False
            mock_checksum.return_value.write.return_value = "abc123"
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=True,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=4,
                archive=False,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=True,
                quiet=False,
            )
            mock_gzip.open.assert_called_once_with(mock_unique.return_value.with_suffix(".md.gz"), "wb")
            mock_shutil.copyfileobj.assert_called_once()
            mock_checksum.return_value.write.assert_called_once_with(mock_unique.return_value.with_suffix(".md.gz"))

    def test_archive(self, mock_root: Path):
        mock_root.joinpath("test.py").write_text("content")
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single.get_git_meta") as mock_git, \
             patch("create_dump.single._unique_path") as mock_unique, \
             patch("create_dump.single.ArchiveManager") as mock_archive, \
             patch("create_dump.single.ChecksumWriter") as mock_checksum:
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)  # Real
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            mock_git.return_value = GitMeta(branch="main", commit="abc123")
            mock_unique.return_value = mock_root / "dump.md"
            mock_checksum.return_value.write.return_value = "abc123"
            mock_archive.return_value.run.return_value = {'default': Path("archive.zip")}
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=4,
                archive=True,
                archive_all=False,
                archive_search=False,
                archive_include_current=True,
                archive_no_remove=False,
                archive_keep_latest=True,
                archive_keep_last=3,
                archive_clean_root=True,
                allow_empty=True,
                metrics_port=0,
                verbose=True,
                quiet=False,
            )
            mock_archive.assert_called_once_with(
                root=mock_root,
                timestamp=ANY,
                keep_latest=True,
                keep_last=3,
                clean_root=True,
                search=False,
                include_current=True,
                no_remove=False,
                dry_run=False,
                yes=True,
                verbose=True,
                md_pattern=ANY,
                archive_all=False,
            )
            mock_archive.return_value.run.assert_called_once_with(current_outfile=mock_unique.return_value)

    def test_no_confirm_force(self, mock_root: Path):
        mock_root.joinpath("test.py").write_text("content")
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single.styled_print") as mock_print, \
             patch("create_dump.single.input") as mock_input:
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)  # Real
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            mock_input.return_value = "n"  # Would cancel if not force
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,  # Skips confirm
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=4,
                archive=False,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=True,
                quiet=False,
            )
            mock_input.assert_not_called()  # Skipped due to force
            # Check no confirm prompt
            assert not any("Proceed with dump" in str(c) for c in mock_print.call_args_list)

    def test_max_file_size_override(self, mock_root: Path):
        mock_root.joinpath("test.py").write_text("content")
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector:
            base_config = Config(max_file_size_kb=50)  # Real base
            mock_load.return_value = base_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=100,  # Override to 100
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=4,
                archive=False,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=True,
                quiet=True,
            )
            # Assert on updated config in collector call_args
            updated_config = mock_collector.call_args.args[0]
            assert updated_config.max_file_size_kb == 100

    @pytest.mark.parametrize("include,exclude,expected_inc,expected_exc", [  # Coverage: 99-105 parsing
        ("", ",,,", [], []),
        ("*.py,*.sh,", "*.log, ,test", ["*.py", "*.sh"], ["*.log", "test"]),
    ])
    def test_patterns_exclude_include(self, mock_root: Path, include: str, exclude: str, expected_inc: list, expected_exc: list):
        mock_root.joinpath("test.py").write_text("content")
        mock_root.joinpath("exclude.txt").write_text("exclude")
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector:
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)  # Real
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude=exclude,
                include=include,
                max_file_size=None,
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=4,
                archive=False,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=True,
                quiet=True,
            )
            mock_collector.assert_called_once_with(mock_config, expected_inc, expected_exc, True, mock_root)

    # FIXED: Coverage 105-110: Confirm prompt – Use partial/ANY for dynamic filename
    def test_confirm_prompt(self, mock_root: Path):
        (mock_root / "test.py").touch()
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single.styled_print") as mock_print, \
             patch("builtins.input", return_value="y"):
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            # Mock unique to return predictable branded for prompt assert
            with patch("create_dump.single._unique_path") as mock_unique:
                mock_unique.return_value = Path("project_all_code_dump_20251030_172000.md")  # Static for assert
                run_single(
                    root=mock_root,
                    dry_run=False,
                    yes=False,
                    no_toc=False,
                    compress=False,
                    exclude="",
                    include="",
                    max_file_size=None,
                    use_gitignore=False,
                    git_meta=False,
                    progress=False,
                    max_workers=1,
                    archive=False,
                    archive_all=False,
                    archive_search=False,
                    archive_include_current=False,
                    archive_no_remove=False,
                    archive_keep_latest=False,
                    archive_keep_last=None,
                    archive_clean_root=False,
                    allow_empty=True,
                    metrics_port=0,
                    verbose=False,
                    quiet=False,
                )
            # Partial match: prefix      structure
            prompt_call = next((c for c in mock_print.call_args_list if "Proceed with dump to [blue]" in str(c)), None)
            assert prompt_call is not None
            assert "Proceed with dump to [blue]" in str(prompt_call.args[0])
            assert "[/blue]? [yellow](y/n)[/yellow]" in str(prompt_call.args[0])
            assert prompt_call.kwargs['nl'] == False


    # FIXED: Coverage 126-129: Chdir and log – Correct patch path to utils.logger
    def test_chdir_log(self, mock_root: Path):
        (mock_root / "test.py").touch()
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.utils.logger.info") as mock_info:  # FIXED: Full utils path
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=False,
                git_meta=False,
                progress=False,
                max_workers=1,
                archive=False,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=False,
                quiet=True,
            )
            mock_info.assert_any_call(
                "Collection complete",
                count=1,
                total_size_kb=ANY,  # Float calc
                root=str(mock_root),
            )

    # NEW: Coverage 178-180: Archive results logging
    def test_archive_results_log(self, mock_root: Path):
        (mock_root / "test.py").touch()
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single.ArchiveManager") as mock_archive, \
             patch("create_dump.single.styled_print") as mock_print:
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            mock_archive.return_value.run.return_value = {'src': Path("src.zip"), 'tests': Path("tests.zip")}
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=False,
                git_meta=False,
                progress=False,
                max_workers=1,
                archive=True,
                archive_all=True,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=False,
                quiet=False,
            )
            mock_print.assert_called_with("[green]Archived groups: src, tests[/green]")

    # NEW: Coverage 182-185: No prior dumps msg
    def test_no_prior_dumps_msg(self, mock_root: Path):
        (mock_root / "test.py").touch()
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single.ArchiveManager") as mock_archive, \
             patch("create_dump.single.styled_print") as mock_print:
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            mock_archive.return_value.run.return_value = {}
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=False,
                git_meta=False,
                progress=False,
                max_workers=1,
                archive=True,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=False,
                quiet=False,
            )
            mock_print.assert_called_with("[yellow]ℹ️ No prior dumps found for archiving.[/yellow]")


    def test_dest_resolution(self, mock_root: Path):  # FIXED: Drop max_size param
        dest_dir = mock_root / "custom_dest"
        (mock_root / "test.py").touch()
        with patch("create_dump.single.load_config") as mock_load, \
             patch("create_dump.single.FileCollector") as mock_collector, \
             patch("create_dump.single._unique_path") as mock_unique, \
             patch("create_dump.single.ChecksumWriter") as mock_checksum:  # FIXED: Mock checksum to skip I/O
            mock_config = Config(max_file_size_kb=100, use_gitignore=True)
            mock_load.return_value = mock_config
            mock_collector.return_value.collect.return_value = ["test.py"]
            mock_checksum.return_value.write.return_value = "dummy_checksum"  # FIXED: Dummy for no I/O
            run_single(
                root=mock_root,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude="",
                include="",
                max_file_size=None,
                use_gitignore=False,
                git_meta=False,
                progress=False,
                max_workers=1,
                archive=False,
                archive_all=False,
                archive_search=False,
                archive_include_current=False,
                archive_no_remove=False,
                archive_keep_latest=False,
                archive_keep_last=None,
                archive_clean_root=False,
                allow_empty=True,
                metrics_port=0,
                verbose=False,
                quiet=True,
                dest=dest_dir,
            )
            # FIXED: Assert inside patch scope; call count & prefix
            assert len(mock_unique.call_args_list) == 2  # Prompt      outfile
            branded_prefix = f"{mock_root.name}_all_code_dump_"
            for call_arg in mock_unique.call_args_list:
                arg_path = call_arg.args[0]
                assert arg_path.parent == dest_dir  # Under dest
                assert str(arg_path.name).startswith(branded_prefix)  # Branded      dynamic timestamp
                assert arg_path.is_absolute()  # Resolved path
    
    def test_temp_cleanup_exception(self, mock_root: Path):
         (mock_root / "test.py").touch()
 
         with patch("create_dump.single.load_config") as mock_load, \
              patch("create_dump.single.FileCollector") as mock_collector, \
              patch("create_dump.single.MarkdownWriter") as mock_writer, \
              patch("create_dump.single.TemporaryDirectory") as mock_temp, \
              patch("create_dump.single.get_git_meta", return_value=None), \
              patch("create_dump.single._unique_path", return_value=mock_root / "dump.md"), \
              patch("create_dump.single.ChecksumWriter") as mock_checksum, \
              patch("create_dump.single.metrics_server", return_value=nullcontext()), \
              patch("create_dump.utils.DUMP_DURATION.time", return_value=nullcontext()):
 
             # Mock configuration load
             mock_config = Config(max_file_size_kb=100, use_gitignore=True)
             mock_load.return_value = mock_config
 
             # Mock collector
             mock_collector.return_value.collect.return_value = ["test.py"]
 
             # Mock writer
             mock_writer_instance = MagicMock()
             mock_writer.return_value = mock_writer_instance
             mock_writer_instance.dump_concurrent.side_effect = Exception("Test exception")
 
             # Mock temp_dir
             mock_temp_instance = MagicMock()
             mock_temp.return_value = mock_temp_instance
             mock_temp_instance.name = "/tmp/test_dir"
 
             # Mock cleanup
             mock_cleanup = MagicMock()
             mock_temp_instance.cleanup = mock_cleanup
 
             # Mock checksum
             mock_checksum.return_value.write.return_value = "mock_checksum"
 
             # Expect the simulated MarkdownWriter exception; finally should still call cleanup
             with pytest.raises(Exception, match="Test exception"):
                 run_single(
                     root=mock_root,
                     dry_run=False,
                     yes=True,
                     no_toc=False,
                     compress=False,
                     exclude="",
                     include="",
                     max_file_size=None,
                     use_gitignore=False,
                     git_meta=False,
                     progress=False,
                     max_workers=1,
                     archive=False,
                     archive_all=False,
                     archive_search=False,
                     archive_include_current=False,
                     archive_no_remove=False,
                     archive_keep_latest=False,
                     archive_keep_last=None,
                     archive_clean_root=False,
                     allow_empty=True,
                     metrics_port=0,
                     verbose=False,
                     quiet=True,
                 )
 
             # Assert cleanup called once even on raised exception (via finally)
             mock_cleanup.assert_called_once()
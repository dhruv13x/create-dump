import pytest
import re
from pathlib import Path
from unittest.mock import patch, MagicMock, call, ANY
from datetime import datetime, timezone
from create_dump.orchestrator import run_batch, _centralize_outputs
from create_dump.archiver import ArchiveManager
from create_dump.core import DEFAULT_DUMP_PATTERN


@pytest.fixture
def mock_root(tmp_path: Path):
    tmp_path.mkdir(exist_ok=True)
    return tmp_path


class TestCentralizeOutputs:
    @pytest.mark.parametrize("dump_pattern", [DEFAULT_DUMP_PATTERN])
    def test_no_files(self, mock_root: Path, dump_pattern: str):
        with patch("create_dump.orchestrator.logger.info") as mock_log:
            _centralize_outputs(mock_root, [], compress=False, yes=True, dest=None, dump_pattern=dump_pattern)
            mock_log.assert_called_once_with("No matching dumps found for centralization.")

    @pytest.mark.parametrize("compress", [False, True])
    def test_md_only(self, mock_root: Path, compress: bool):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        suffix = ".gz" if compress else ""
        filename = f"bot_platform_all_code_dump_20251030_133140.md{suffix}"
        md1 = sub1 / filename
        md1.write_text("md1")
        dest_dir = mock_root / "archives"
        target = dest_dir / filename
        with patch("shutil.move") as mock_move, \
             patch("create_dump.orchestrator.logger.info") as mock_log:
            _centralize_outputs(mock_root, [sub1], compress=compress, yes=True, dest=None, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_move.assert_called_once_with(str(md1), str(target))
            mock_log.assert_has_calls([
                call("Moved dump to dest", src=md1, dst=target),
                call("Centralized %d dump files to %s", 1, dest_dir),
            ], any_order=True)

    def test_md_sha(self, mock_root: Path):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        filename = "bot_platform_all_code_dump_20251030_133140.md"
        md1 = sub1 / filename
        md1.write_text("md1")
        sha_filename = "bot_platform_all_code_dump_20251030_133140.sha256"
        sha1 = sub1 / sha_filename
        sha1.write_text("sha1")
        dest_dir = mock_root / "archives"
        target_md = dest_dir / filename
        target_sha = dest_dir / sha_filename
        with patch("shutil.move") as mock_move, \
             patch("create_dump.orchestrator.logger.info") as mock_log:
            _centralize_outputs(mock_root, [sub1], compress=False, yes=True, dest=None, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_move.assert_has_calls([
                call(str(md1), str(target_md)),
                call(str(sha1), str(target_sha)),
            ], any_order=True)
            mock_log.assert_called_with("Centralized %d dump files to %s", 2, dest_dir)

    def test_compress(self, mock_root: Path):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        filename = "bot_platform_all_code_dump_20251030_133140.md.gz"
        md1 = sub1 / filename
        md1.write_text("gz1")
        sha_filename = "bot_platform_all_code_dump_20251030_133140.sha256"
        sha1 = sub1 / sha_filename
        sha1.write_text("sha1")
        dest_dir = mock_root / "archives"
        target_md = dest_dir / filename
        target_sha = dest_dir / sha_filename
        with patch("shutil.move") as mock_move, \
             patch("create_dump.orchestrator.logger.info") as mock_log:
            _centralize_outputs(mock_root, [sub1], compress=True, yes=True, dest=None, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_move.assert_has_calls([
                call(str(md1), str(target_md)),
                call(str(sha1), str(target_sha)),
            ], any_order=True)
            mock_log.assert_called_with("Centralized %d dump files to %s", 2, dest_dir)

    def test_test_unsafe_skip(self, mock_root: Path):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        filename = "bot_platform_all_code_dump_20251030_133140.md"
        md1 = sub1 / filename
        md1.write_text("unsafe")
        with patch("create_dump.orchestrator.safe_is_within") as mock_within, \
             patch("create_dump.orchestrator.logger.warning") as mock_warn, \
             patch("shutil.move") as mock_move, \
             patch("create_dump.orchestrator.logger.info") as mock_log:
            mock_within.return_value = False
            _centralize_outputs(mock_root, [sub1], compress=False, yes=True, dest=None, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_warn.assert_called_once_with("Skipping unsafe dump: %s", md1)
            mock_move.assert_not_called()
            mock_log.assert_called_once_with("No matching dumps found for centralization.")  # 🐞 FIX: Align to code's moved==0 log

    def test_overwrite(self, mock_root: Path):
        archives_dir = mock_root / "archives"
        archives_dir.mkdir()
        filename = "bot_platform_all_code_dump_20251030_133140.md"
        target_md = archives_dir / filename
        target_md.write_text("old")
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        md1 = sub1 / filename
        md1.write_text("new")
        with patch("pathlib.Path.unlink") as mock_unlink, \
             patch("shutil.move") as mock_move, \
             patch("create_dump.orchestrator.logger.info") as mock_log:
            _centralize_outputs(mock_root, [sub1], compress=False, yes=True, dest=None, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_unlink.assert_called_once()
            mock_move.assert_called_once_with(str(md1), str(target_md))
            mock_log.assert_called_with("Centralized %d dump files to %s", 1, mock_root / "archives")


class TestRunBatch:
    def test_no_sub_roots(self, mock_root: Path):
        canonical_pattern = r".*_all_code_dump_.*"
        with patch("create_dump.orchestrator.load_config") as mock_load:
            mock_load.return_value.dump_pattern = canonical_pattern
            with patch("create_dump.orchestrator.logger.warning") as mock_warn:
                run_batch(
                    root=mock_root,
                    subdirs=["nonexistent"],
                    pattern=canonical_pattern,
                    dry_run=False,
                    yes=True,
                    accept_prompts=True,
                    compress=False,
                    max_workers=2,
                    verbose=True,
                    quiet=False,
                )
                mock_warn.assert_called_once_with("No valid subdirs found: %s", ["nonexistent"])

    @pytest.mark.parametrize("pattern,expected_pattern", [
        (r".*dump.*", r".*dump.*"),
        (r".*_all_code_dump_.*", r".*_all_code_dump_.*"),
    ])
    def test_pre_cleanup(self, mock_root: Path, pattern: str, expected_pattern: str):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        old_dump = mock_root / "old_dump.md"
        old_dump.touch()
        with patch("create_dump.orchestrator.find_matching_files") as mock_find, \
             patch("create_dump.orchestrator.confirm") as mock_confirm, \
             patch("create_dump.orchestrator.safe_delete_paths") as mock_delete, \
             patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single:
            mock_find.return_value = [old_dump]
            mock_confirm.return_value = True
            mock_delete.return_value = (1, 0)
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True)
            mock_cfg.dump_pattern = expected_pattern
            mock_load.return_value = mock_cfg
            mock_run_single.return_value = None
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=pattern,
                dry_run=False,
                yes=False,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=True,
            )
            mock_find.assert_called_once_with(mock_root, expected_pattern)
            mock_delete.assert_called_once_with([old_dump], mock_root, dry_run=False, assume_yes=False)

    def test_pre_cleanup_no_confirm(self, mock_root: Path):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        old_dump = mock_root / "old_dump.md"
        old_dump.touch()
        with patch("create_dump.orchestrator.find_matching_files") as mock_find, \
             patch("create_dump.orchestrator.confirm") as mock_confirm, \
             patch("create_dump.orchestrator.safe_delete_paths") as mock_delete, \
             patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single:
            mock_find.return_value = [old_dump]
            mock_confirm.return_value = False
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=r".*dump.*")
            mock_load.return_value = mock_cfg
            mock_run_single.return_value = None
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=r".*dump.*",
                dry_run=False,
                yes=False,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=True,
            )
            mock_delete.assert_not_called()

    @pytest.mark.parametrize("pattern", [r".*nonexistent.*"])
    def test_pre_cleanup_no_matches(self, mock_root: Path, pattern: str):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        with patch("create_dump.orchestrator.find_matching_files") as mock_find, \
             patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single:
            mock_find.return_value = []
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=pattern)
            mock_load.return_value = mock_cfg
            mock_run_single.return_value = None
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=pattern,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=True,
            )
            mock_find.assert_called_once_with(mock_root, pattern)

    def test_pre_cleanup_dry_run(self, mock_root: Path):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        old_dump = mock_root / "old_dump.md"
        old_dump.touch()
        with patch("create_dump.orchestrator.find_matching_files") as mock_find, \
             patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single:
            mock_find.return_value = [old_dump]
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=r".*dump.*")
            mock_load.return_value = mock_cfg
            mock_run_single.return_value = None
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=r".*dump.*",
                dry_run=True,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=True,
            )
            mock_find.assert_called_once_with(mock_root, r".*dump.*")

    @pytest.mark.parametrize("pattern", [r".*", r".*_all_code_dump_.*"])
    def test_success(self, mock_root: Path, pattern: str):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        with patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single, \
             patch("create_dump.orchestrator._centralize_outputs") as mock_centralize, \
             patch("create_dump.orchestrator.DUMP_DURATION.time") as mock_time, \
             patch("create_dump.orchestrator.styled_print") as mock_print, \
             patch("create_dump.orchestrator.logger.info") as mock_info, \
             patch("create_dump.orchestrator.find_matching_files") as mock_find:
            mock_find.return_value = []
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True)
            mock_cfg.dump_pattern = pattern if re.match(r'.*_all_code_dump_', pattern) else pattern
            mock_load.return_value = mock_cfg
            mock_run_single.return_value = None
            mock_time.return_value.__enter__.return_value = None
            mock_time.return_value.__exit__.return_value = False
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=pattern,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=False,
            )
            expected_pattern = pattern if re.match(r'.*_all_code_dump_', pattern) else mock_cfg.dump_pattern
            mock_find.assert_called_once_with(mock_root, expected_pattern)
            mock_run_single.assert_called_once_with(
                root=sub1,
                dry_run=False,
                yes=True,
                no_toc=False,
                compress=False,
                exclude='',
                include='',
                max_file_size=100,
                use_gitignore=True,
                git_meta=True,
                progress=True,
                max_workers=2,
                archive=False,
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
            mock_centralize.assert_called_once_with(mock_root, [sub1], False, True, dest=None, dump_pattern=expected_pattern)
            mock_info.assert_called_with("Batch complete: %d successes, %d failures", 1, 0)
            mock_print.assert_any_call(f"[blue]Dumping {sub1}...[/blue]")
            mock_print.assert_any_call("[green]✅ Batch dump complete (1/1 subdirs).[/green]")

    @pytest.mark.parametrize("pattern", [r".*"])
    def test_failure(self, mock_root: Path, pattern: str):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        with patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single, \
             patch("create_dump.orchestrator.logger.error") as mock_error, \
             patch("create_dump.orchestrator.styled_print") as mock_print, \
             patch("create_dump.orchestrator.find_matching_files") as mock_find:
            mock_find.return_value = []
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_load.return_value = mock_cfg
            mock_run_single.side_effect = Exception("Test fail")
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=pattern,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=False,
            )
            mock_error.assert_called_once_with("Subdir dump failed", subdir=sub1, error="Test fail")
            mock_print.assert_any_call(f"[red]Failed {sub1}: Test fail[/red]")

    def test_no_success_skip_centralize(self, mock_root: Path):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        with patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single, \
             patch("create_dump.orchestrator._centralize_outputs") as mock_centralize, \
             patch("create_dump.orchestrator.logger.info") as mock_info, \
             patch("create_dump.orchestrator.find_matching_files") as mock_find:
            mock_find.return_value = []
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_load.return_value = mock_cfg
            mock_run_single.side_effect = Exception("Fail")
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=DEFAULT_DUMP_PATTERN,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=True,
            )
            mock_centralize.assert_not_called()
            mock_info.assert_called_with("No successful dumps; skipping centralization.")

    @pytest.mark.parametrize("quiet", [True, False])
    def test_quiet_mode(self, mock_root: Path, quiet: bool):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        with patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single, \
             patch("create_dump.orchestrator.styled_print") as mock_print, \
             patch("create_dump.orchestrator.find_matching_files") as mock_find:
            mock_find.return_value = []
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_load.return_value = mock_cfg
            mock_run_single.return_value = None
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=DEFAULT_DUMP_PATTERN,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=quiet,
            )
            if not quiet:
                assert mock_print.call_count > 0
            else:
                mock_print.assert_not_called()

    def test_verbose_failures(self, mock_root: Path):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        sub2 = mock_root / "sub2"
        sub2.mkdir()
        with patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single, \
             patch("create_dump.orchestrator.logger.error") as mock_error, \
             patch("create_dump.orchestrator.find_matching_files") as mock_find:
            mock_find.return_value = []
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_load.return_value = mock_cfg
            mock_run_single.side_effect = [None, Exception("Fail")]
            run_batch(
                root=mock_root,
                subdirs=["sub1", "sub2"],
                pattern=DEFAULT_DUMP_PATTERN,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=True,
            )
            mock_error.assert_has_calls([
                call("Subdir dump failed", subdir=sub2, error="Fail"),
                call("Failure in %s: %s", sub2, "Fail"),
            ], any_order=True)

    @pytest.mark.parametrize("archive_results", [{'default': Path('mock.zip')}, {}])
    def test_archive_integration_with_results(self, mock_root: Path, archive_results: dict):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        with patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single, \
             patch("create_dump.orchestrator._centralize_outputs") as mock_centralize, \
             patch("create_dump.orchestrator.DUMP_DURATION.time") as mock_time, \
             patch("create_dump.orchestrator.styled_print") as mock_print, \
             patch("create_dump.orchestrator.logger.info") as mock_info, \
             patch("create_dump.orchestrator.datetime") as mock_dt, \
             patch("create_dump.orchestrator.ArchiveManager") as mock_class, \
             patch("create_dump.orchestrator.find_matching_files") as mock_find:
            mock_find.return_value = []
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_load.return_value = mock_cfg
            mock_run_single.return_value = None
            mock_time.return_value.__enter__.return_value = None
            mock_time.return_value.__exit__.return_value = False
            mock_dt.now.return_value.strftime.return_value = "20251030_133000"
            mock_manager = MagicMock()
            mock_manager.run.return_value = archive_results
            mock_class.return_value = mock_manager
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=DEFAULT_DUMP_PATTERN,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=False,
                archive=True,
            )
            mock_manager.run.assert_called_once()
            if archive_results:
                groups = ', '.join(k for k, v in archive_results.items() if v)
                mock_info.assert_has_calls([call("Archived groups: %s", groups)], any_order=True)
                mock_print.assert_any_call(f"[green]📦 Batched archived groups: {groups}[/green]")
            else:
                msg = "ℹ️ No prior dumps found for archiving."
                mock_info.assert_any_call(msg)  # 🐞 FIX: Use assert_any_call for multi-log
                mock_print.assert_any_call(f"[yellow]{msg}[/yellow]")

    def test_archive_all_integration(self, mock_root: Path):
        sub1 = mock_root / "sub1"
        sub1.mkdir()
        with patch("create_dump.orchestrator.load_config") as mock_load, \
             patch("create_dump.orchestrator.run_single") as mock_run_single, \
             patch("create_dump.orchestrator._centralize_outputs") as mock_centralize, \
             patch("create_dump.orchestrator.DUMP_DURATION.time") as mock_time, \
             patch("create_dump.orchestrator.styled_print") as mock_print, \
             patch("create_dump.orchestrator.logger.info") as mock_info, \
             patch("create_dump.orchestrator.datetime") as mock_dt, \
             patch("create_dump.orchestrator.find_matching_files") as mock_find, \
             patch("create_dump.orchestrator.ArchiveManager") as mock_class:
            mock_find.return_value = []
            mock_cfg = MagicMock(max_file_size_kb=100, use_gitignore=True, git_meta=True, dump_pattern=DEFAULT_DUMP_PATTERN)
            mock_load.return_value = mock_cfg
            mock_run_single.return_value = None
            mock_time.return_value.__enter__.return_value = None
            mock_time.return_value.__exit__.return_value = False
            mock_dt.now.return_value.strftime.return_value = "20251030_133000"
            mock_manager = MagicMock()
            mock_manager.run.return_value = {'tests': Path('tests.zip'), 'src': Path('src.zip')}
            mock_class.return_value = mock_manager
            run_batch(
                root=mock_root,
                subdirs=["sub1"],
                pattern=DEFAULT_DUMP_PATTERN,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=True,
                quiet=False,
                archive_all=True,
            )
            mock_class.assert_called_once_with(
                root=mock_root,
                timestamp="20251030_133000",
                keep_latest=True,
                keep_last=None,
                clean_root=False,
                search=False,
                include_current=True,
                no_remove=False,
                dry_run=False,
                yes=True,
                verbose=True,
                md_pattern=DEFAULT_DUMP_PATTERN,
                archive_all=True,
            )
            mock_manager.run.assert_called_once()
            mock_info.assert_has_calls([call("Archived groups: %s", "tests, src")], any_order=True)
            mock_print.assert_any_call("[green]📦 Batched archived groups: tests, src[/green]")
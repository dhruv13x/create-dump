<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/create-dump/main/create-dump_logo.png" alt="create-dump logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/create-dump.svg)](https://pypi.org/project/create-dump/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/create-dump.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/create-dump/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/create-dump/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/create-dump/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/create-dump/graph/badge.svg)](https://codecov.io/gh/dhruv13x/create-dump)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/create-dump/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/create-dump.svg)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/create-dump.svg)](https://pypi.org/project/create-dump/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Docs -->
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://your-docs-link)

</div>


# create-dump

**Enterprise-Grade Code Dump Utility for Monorepos**

`create-dump` is a production-ready CLI tool for automated code archival in large-scale monorepos.
It generates branded Markdown dumps with Git metadata, integrity checksums, flexible archiving,
retention policies, path safety, full concurrency, and SRE-grade observability.

Designed for SRE-heavy environments (Telegram bots, microservices, monorepos), it ensures
**reproducible snapshots for debugging, forensics, compliance audits, and CI/CD pipelines**. It also includes a `rollback` command to restore a project from a dump file.

Built for Python 3.11+, leveraging **AnyIO**, Pydantic, Typer, Rich, and Prometheus metrics.

-----

## 🚀 Quick Start

```bash
pip install create-dump

# Create an interactive config file
create-dump --init

# Single dump (current directory)
create-dump single --dest ./dumps/my-snapshot.md

# Batch dump (monorepo)
create-dump batch --root ./monorepo --archive --keep-last 5

# SRE / Git-only dump in watch mode with secret redaction
create-dump single --git-ls-files --watch --scan-secrets --hide-secrets

# Scan for TODOs and get a push notification on completion
create-dump single --scan-todos --notify-topic your_ntfy_topic

# Rollback a dump file to a new directory
create-dump rollback --file ./dumps/my-snapshot.md

# Output example:
# dumps/my-snapshot_all_create_dump_20250101_121045.md
# dumps/my-snapshot_all_create_dump_20250101_121045.md.sha256
# archives/my-snapshot_20250101_121045.zip
```

-----

## ✨ Features

  * **Branded Markdown Generation**
    Auto TOC (list or tree), language-detected code blocks, Git metadata, timestamps.

  * **Async-First & Concurrent**
    Built on `anyio` for high-throughput, non-blocking I/O. Parallel file processing (16+ workers), timeouts, and progress bars (Rich).

  * **Flexible Archiving**
    Automatically archive old dumps into **ZIP, tar.gz, or tar.bz2** formats. Includes integrity validation and retention policies (e.g., "keep last N").

  * **Project Rollback & Restore**
    Includes a `rollback` command to rehydrate a full project structure from a `.md` dump file, with SHA256 integrity verification.

  * **Git-Native Collection**
    Use `git ls-files` for fast, accurate file discovery (`--git-ls-files`) or dump only changed files (`--diff-since <ref>`).

  * **Live Watch Mode**
    Run in a persistent state (`--watch`) that automatically re-runs the dump on any file change, perfect for live development.

  * **Secret Scanning**
    Integrates `detect-secrets` to scan files during processing. Can fail the dump (`--scan-secrets`) or redact secrets in-place (`--hide-secrets`).

  * **Safety & Integrity**
    SHA256 hashing for all dumps, atomic writes, async-safe path guards (prevents traversal & Zip-Slip), and orphan quarantine.

  * **Observability**
    Prometheus metrics (e.g., `create_dump_duration_seconds`, `create_dump_files_total`).

  * **TODO/FIXME Scanning**
    Scan for `TODO` or `FIXME` tags in code and append a summary to the dump (`--scan-todos`).

  * **Push Notifications**
    Get notified on dump completion via `ntfy.sh` push notifications (`--notify-topic <topic>`).

  * **Dump Header Statistics**
    Dump header includes total lines of code and file count for quick context.

| Feature | Single Mode | Batch Mode |
| :--- | :--- | :--- |
| **Scope** | Current dir/files | Recursive subdirs |
| **Archiving** | Optional | Enforced retention |
| **Concurrency** | Up to **16** workers | Parallel subdirs |
| **Git Metadata** | ✔️ | Per-subdir ✔️ |

-----

## 📦 Installation

### PyPI

```bash
pip install create-dump
```

### From Source

```bash
git clone https://github.com/dhruv13x/create-dump.git 
cd create-dump
pip install -e .[dev]
```

### Docker

```dockerfile
FROM python:3.12-slim
RUN pip install create-dump
ENTRYPOINT ["create-dump"]
```

-----

## ⚙️ Configuration

### 🚀 Interactive Setup (`--init`)

The easiest way to configure `create-dump` is to run the built-in interactive wizard:

```bash
create-dump --init
```

This will create a `create_dump.toml` file with your preferences. You can also add this configuration to your `pyproject.toml` file under the `[tool.create-dump]` section.

### Example (pyproject.toml)

```toml
[tool.create-dump]
# Default output destination (CLI --dest overrides)
dest = "/path/to/dumps"

# Enable .gitignore parsing
use_gitignore = true

# Include Git branch/commit in header
git_meta = true

# Max file size in KB (e.g., 5MB)
max_file_size_kb = 5000

# Canonical regex for dump artifacts
dump_pattern = ".*_all_create_dump_\\d{8}_\\d{6}\\.(md(\\.gz)?|sha256)$"

# Default excluded directories
excluded_dirs = ["__pycache__", ".git", ".venv", "node_modules"]

# Prometheus export port
metrics_port = 8000

# --- New v9 Feature Flags ---

# Use 'git ls-files' by default for collection
# git_ls_files = true

# Enable secret scanning by default
# scan_secrets = true

# Redact found secrets (requires scan_secrets=true)
# hide_secrets = true

# Scan for TODOs and append a report
# scan_todos = true

# Default ntfy.sh topic for notifications
# notify_topic = "your_ntfy_topic"
```

Override any setting via CLI flags.

### CLI Arguments

| Argument | Shorthand | Description | Default |
| :--- | :--- | :--- | :--- |
| `--version` | `-V` | Show version and exit. | `false` |
| `--init` | | Run interactive wizard to create `create_dump.toml`. | `false` |
| `--config` | | Path to TOML config file. | `null` |
| `--profile` | | Config profile to merge from `pyproject.toml`. | `null` |
| `--yes` | `-y` | Assume yes for prompts and deletions. | `false` |
| `--dry-run` | `-d` | Simulate without writing files. | `false` |
| `--no-dry-run` | `-nd` | Run for real (disables simulation). | `false` |
| `--verbose` | `-v` | Enable debug logging. | `false` |
| `--quiet` | `-q` | Suppress output (CI mode). | `false` |
| `--dest` | | Destination dir for output. | `.` |
| `--no-toc` | | Omit table of contents. | `false` |
| `--tree-toc` | | Render Table of Contents as a file tree. | `false` |
| `--format` | | Output format (md or json). | `md` |
| `--compress` | `-c` | Gzip the output file. | `false` |
| `--progress` / `--no-progress` | `-p` | Show processing progress. | `true` |
| `--allow-empty` | | Succeed on 0 files. | `false` |
| `--metrics-port` | | Prometheus export port. | `8000` |
| `--exclude` | | Comma-separated exclude patterns. | `""` |
| `--include` | | Comma-separated include patterns. | `""` |
| `--max-file-size` | | Max file size in KB. | `null` |
| `--use-gitignore` / `--no-use-gitignore` | | Incorporate .gitignore excludes. | `true` |
| `--git-meta` / `--no-git-meta` | | Include Git branch/commit. | `true` |
| `--max-workers` | | Concurrency level. | `16` |
| `--watch` | | Run in live-watch mode. | `false` |
| `--git-ls-files` | | Use 'git ls-files' for file collection. | `false` |
| `--diff-since` | | Only dump files changed since a specific git ref. | `null` |
| `--scan-secrets` | | Scan files for secrets. Fails dump if secrets are found. | `false` |
| `--hide-secrets` | | Redact found secrets (requires --scan-secrets). | `false` |
| `--scan-todos` | | Scan files for TODO/FIXME tags and append a summary. | `false` |
| `--notify-topic` | | ntfy.sh topic for push notification on completion. | `null` |
| `--archive` | `-a` | Archive prior dumps into ZIP. | `false` |
| `--archive-all` | | Archive dumps grouped by prefix. | `false` |
| `--archive-search` | | Search project-wide for dumps. | `false` |
| `--archive-include-current` / `--no-archive-include-current` | | Include this run in archive. | `true` |
| `--archive-no-remove` | | Preserve originals post-archiving. | `false` |
| `--archive-keep-latest` / `--no-archive-keep-latest` | | Keep latest dump live or archive all. | `true` |
| `--archive-keep-last` | | Keep last N archives. | `null` |
| `--archive-clean-root` | | Clean root post-archive. | `false` |
| `--archive-format` | | Archive format (zip, tar.gz, tar.bz2). | `zip` |

-----

## 📖 Usage

### Single Mode

```bash
# Dump all files matching .py, include git meta
create-dump single --include "*.py" --git-meta

# Dump only files changed since 'main' branch and watch for new changes
create-dump single --diff-since main --watch

# Dump using git, scan for secrets, and redact them
create-dump single --git-ls-files --scan-secrets --hide-secrets

# Scan for TODOs and send a notification
create-dump single --scan-todos --notify-topic your_ntfy_topic

# Dry run with verbose logging
create-dump single --dry-run --verbose
```

### Batch Mode

```bash
# Run dumps in 'src' and 'tests', then archive old dumps, keeping 10
create-dump batch --root ./monorepo --dirs "src,tests" --keep-last 10 --archive

# Run dumps and create grouped archives (e.g., src.zip, tests.zip)
create-dump batch --root ./monorepo --archive-all --archive-format tar.gz
```

### 🗃️ Rollback & Restore

You can instantly restore a project structure from a dump file using the `rollback` command.
It verifies the file's integrity using the accompanying `.sha256` file and then recreates the
directory and all files in a safe, sandboxed folder.

```bash
# Find the latest dump in the current directory and restore it
create-dump rollback .

# Restore from a specific file
create-dump rollback --file my_project_dump.md

# Do a dry run to see what files would be created
create-dump rollback --dry-run
```

This creates a new directory like `./all_create_dump_rollbacks/my_project_dump/` containing the restored code.

-----

## 🏗️ Architecture Overview

```
┌─────────────────┐
│   CLI (Typer)   │
│ (single, batch, │
│  init, rollback)│
└────────┬────────┘
         │
┌────────▼────────┐
│ Config / Models │
│    (core.py)    │
└─────────────────┘
         │
┌─────────────────┴─────────────────┐
│                                   │
▼                                   ▼
┌─────────────────┐               ┌───────────────────┐
│   DUMP FLOW     │               │   RESTORE FLOW    │
│ (Collect)       │               │   (Verify SHA256) │
│      │          │               │         │         │
│      ▼          │               │         ▼         │
│ (Process/Scan)  │               │   (Parse .md)     │
│      │          │               │         ▼         │
│      ▼          │               │   (Rehydrate Files) │
│ (Write MD/JSON) │               │   (Rehydrate Files) │
│      │          │               │                   │
│      ▼          │               └───────────────────┘
│ (Archive/Prune) │
└─────────────────┘
```

-----

## 🧪 Testing & Development

Run the full test suite using `pytest`. It's recommended to run `pytest` as a module to ensure it uses the correct Python interpreter and dependencies:

```bash
# Install dev dependencies
pip install -e .[dev]

# Run tests with coverage
python -m pytest --cov=create_dump --cov-report=html
```

Run linters and formatters:

```bash
ruff check src/ tests/
black src/ tests/
mypy src/
```

-----

## 🔒 Security & Reliability

  * **Secret Scanning** & Redaction (`detect-secrets`)
  * **Async-Safe Path Guards** (Prevents traversal & Zip-Slip)
  * Archive Integrity + SHA256 Validation (on Dump & Restore)
  * `tenacity` Retries on I/O
  * Prometheus Metrics on `:8000/metrics`
  * Graceful `SIGINT`/`SIGTERM` Cleanup Handlers

### Limitations

  * No remote filesystem support (e.g., S3, GCS)

-----

## 🤝 Contributing

1.  Fork repo → create branch
2.  Follow Conventional Commits
3.  Run full CI suite (`pytest`, `ruff`, `mypy`)
4.  Add/Update any ADRs under `/ADRs`
5.  Follow the Code of Conduct

Security issues → `security@dhruv.io`

-----

## 📄 License

MIT License.
See LICENSE.

-----

## 🙏 Acknowledgments

Powered by Typer, Rich, Pydantic, Prometheus, and AnyIO.

Inspired by tooling from Nx, Bazel, and internal SRE practices.

-----

*Questions or ideas?*
*Open an issue or email `dhruv13x@gmail.com`.*

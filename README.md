---

# create-dump

[![PyPI Version](https://badge.fury.io/py/create-dump.svg)](https://badge.fury.io/py/create-dump)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/dhruv/create-dump/actions/workflows/ci.yml/badge.svg)](https://github.com/dhruv/create-dump/actions)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)](https://codecov.io/gh/dhruv/create-dump)

**Enterprise-Grade Code Dump Utility for Monorepos**

`create-dump` is a robust, production-ready CLI tool designed for automated code archival in large-scale monorepos. It generates branded Markdown dumps with embedded Git metadata, integrity checksums, and configurable archiving (ZIP/GZ) while enforcing retention policies, path safety, and observability. Tailored for SRE-led environments like Telegram bot platforms, it ensures reproducible snapshots for debugging, compliance audits, and CI/CD pipelines—reducing operational toil and data loss risks.

Built with Python 3.11+, it leverages async patterns, Pydantic validation, and Prometheus metrics for scalability and reliability. Supports single-file dumps, batch orchestration across subdirectories, and dry-run modes for safe testing.

## 🚀 Quick Start

Install via pip and generate a dump in seconds:

```bash
# Install from PyPI
pip install create-dump

# Generate a single dump (defaults to current dir)
create-dump single --dest ./dumps/my-snapshot.md

# Batch dump a monorepo with archiving
create-dump batch --root ./monorepo --archive --keep-last 5
```

Output: A self-contained Markdown file (`my-snapshot_all_code_dump_YYYYMMDD_HHMMSS.md`) with TOC, fenced code blocks, and `.sha256` checksum.

## ✨ Features

- **Branded Markdown Generation**: Syntax-highlighted code blocks (via language detection), auto-TOC, Git branch/commit metadata, and UTC timestamps.
- **Concurrent Processing**: Thread-pool parallelism for large repos; configurable workers with timeouts and progress bars (Rich).
- **Integrity & Safety**: SHA256 checksums, atomic writes, path traversal guards (`safe_is_within`), and orphan quarantine.
- **Archiving & Retention**: ZIP packaging with validation/rollback, pruning (keep-latest/N), and grouped subdir handling.
- **Configurability**: TOML-based defaults (gitignore integration, file size limits, patterns); CLI overrides.
- **Observability**: Prometheus metrics (files processed, errors, durations), structured logging (structlog).
- **Testing & CI-Ready**: 93%+ coverage (pytest), Ruff/Black/Mypy enforcement, Hypothesis for fuzzing.
- **SRE Safeguards**: Dry-run, no-remove flags, signal handling (CleanupHandler), and resource limits.

| Feature | Single Mode | Batch Mode |
|---------|-------------|------------|
| **Scope** | Current dir/files | Recursive subdirs |
| **Archiving** | Optional ZIP | Enforced retention |
| **Concurrency** | Up to 8 workers | Parallel subdirs |
| **Git Meta** | Branch/commit | Per-subdir |

## 📦 Installation

### Prerequisites
- Python 3.11+
- Git (for metadata; optional)
- Optional: Redis (for future caching; stubbed)

### Via PyPI (Recommended)
```bash
pip install create-dump
```

### From Source
```bash
git clone https://github.com/dhruv/create-dump.git
cd create-dump
pip install -e .[dev]  # Includes testing tools
```

### Docker (For CI/Prod)
```dockerfile
FROM python:3.12-slim
RUN pip install create-dump
ENTRYPOINT ["create-dump"]
```

## ⚙️ Configuration

Defaults are loaded from `pyproject.toml` [tool.create-dump] section. Override via CLI or env vars.

### TOML Example (`pyproject.toml`)
```toml
[tool.create-dump]
use_gitignore = true
git_meta = true
max_file_size_kb = 5000
dest = "/path/to/dumps"  # Default output dir
dump_pattern = ".*_all_code_dump_\\d{8}_\\d{6}\\.(md(\\.gz)?|sha256)$"
excluded_dirs = ["__pycache__", ".git", ".venv", "node_modules"]
metrics_port = 8000
```

### CLI Overrides
Flags take precedence; see `create-dump --help` for full options.

## 📖 Usage

### Single Mode: Ad-Hoc Dumps
For quick snapshots of current files.

```bash
# Basic dump
create-dump single --files "src/*.py" --no-toc --progress

# With Git meta and dest
create-dump single --dest ./output.md --git-meta --include-current

# Dry-run validation
create-dump single --dry-run --verbose
```

### Batch Mode: Monorepo Orchestration
Automated discovery and archival across subdirs.

```bash
# Full batch with pruning
create-dump batch --root ./monorepo --keep-last 10 --clean-root --archive-all

# Search recursive, exclude patterns
create-dump batch --search --exclude "tests/**" --max-size 10MB

# Grouped archiving (e.g., src/tests)
create-dump batch --archive-all --keep-latest
```

### Archiving Workflow
1. Discover MD/SHA pairs via regex pattern.
2. Group by prefix (e.g., `src_`, `tests_`).
3. ZIP with deflation (text) / store (binaries); validate integrity.
4. Prune historicals (keep N latest); quarantine orphans.
5. Cleanup temps/SHAs (configurable).

**Output Artifacts**:
- `project_all_code_dump_YYYYMMDD_HHMMSS.md`: Main dump.
- `.sha256`: Integrity checksum.
- `archives/project_YYYYMMDD_HHMMSS.zip`: Compressed archive.

## 🏗️ Architecture Overview

Modular design follows hexagonal principles: Core (Config/DumpFile), Ports (Collector/Writer/Archiver), Adapters (CLI/TOML).

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│     CLI (Typer) │───▶│   Orchestrator   │───▶│   Single/Batch  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Config (TOML) │◀──▶│     Core (Pydantic)│◀──▶│   Utils (Logging)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Collector     │───▶│     Writer (MD)  │───▶│   Archiver (ZIP)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                          Prometheus Metrics
```

- **Entry**: `cli.py` → `orchestrator.py` / `single.py`.
- **Flow**: Collect files → Concurrent write temps → Stream MD → Checksum/Archive.
- **Safety**: Atomic replaces, finally cleanups, signal handlers.

For deep dives: See [ADR-001: Unified Archiving](ADRs/001-unified-archiving.md).

## 🧪 Testing & Development

### Running Tests
```bash
pytest --cov=src/create_dump --cov-report=html  # 93%+ threshold
hypothesis pytest tests/  # Property-based fuzzing
```

### Linting & Formatting
```bash
ruff check src/ tests/  # Linting
black src/ tests/       # Formatting
mypy src/               # Type checking
```

### Doctests
Integrated via pytest; run standalone with `PYTHONPATH=src python -m doctest -v src/create_dump/*.py`.

## 🔒 Security & Reliability

- **Path Safety**: `safe_is_within` prevents traversal; zip-slip mitigation in `_safe_arcname`.
- **Integrity**: ZIP `testzip()` + SHA256; rollback on corruption.
- **Resilience**: Tenacity retries, concurrent timeouts, CleanupHandler for SIGINT/TERM.
- **Metrics**: Exposed on `:8000/metrics` (Prometheus); track `FILES_PROCESSED`, `ERRORS_TOTAL`.
- **SLOs**: Target <5s dump latency; error budget via Grafana alerts.

**Known Limitations**: Sync-only (async I/O in v7); no remote FS support.

## 🤝 Contributing

1. Fork & PR to `main` with Conventional Commits.
2. Run full CI: `make test lint docs`.
3. Add ADRs for architectural changes (see `/ADRs`).
4. Sign CLA; follow [CODE_OF_CONDUCT.md].

**Guidelines**:
- 100% test coverage for new features.
- No breaking changes without deprecation.
- Security issues: Report to `security@dhruv.io`.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built on [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), [Pydantic](https://pydantic.dev/).
- Inspired by monorepo tools at scale (e.g., Bazel, Nx).

**Questions?** Open an issue or reach dhruv@dhruv.io.

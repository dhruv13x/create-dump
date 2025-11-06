# create-dump

[![PyPI Version](https://badge.fury.io/py/create-dump.svg)](https://badge.fury.io/py/create-dump)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/dhruv/create-dump/actions/workflows/ci.yml/badge.svg)](https://github.com/dhruv/create-dump/actions)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)](https://codecov.io/gh/dhruv/create-dump)

**Enterprise-Grade Code Dump Utility for Monorepos**

`create-dump` is a production-ready CLI tool for automated code archival in large-scale monorepos.  
It generates branded Markdown dumps with Git metadata, integrity checksums, ZIP/GZ archiving,  
retention policies, path safety, concurrency, and full observability.

Designed for SRE-heavy environments (Telegram bots, microservices, monorepos), it ensures  
**reproducible snapshots for debugging, forensics, compliance audits, and CI/CD pipelines**.

Built for Python 3.11+, leveraging Pydantic, Typer, Rich, and Prometheus metrics.

---

## 🚀 Quick Start

```bash
pip install create-dump

Single dump (current directory):

create-dump single --dest ./dumps/my-snapshot.md

Batch dump (monorepo):

create-dump batch --root ./monorepo --archive --keep-last 5

Output example:

my-snapshot_all_create_dump_20250101_121045.md
my-snapshot_all_create_dump_20250101_121045.md.sha256
archives/my-snapshot_20250101_121045.zip


---

✨ Features

Branded Markdown Generation

Auto TOC, language-detected code blocks, Git metadata, timestamps.


High-Concurrency Processing

Parallel workers, timeouts, progress bars (Rich).


Safety & Integrity

SHA256 hashing, atomic writes, safe path guards, orphan quarantine.


Archiving & Retention

ZIP/GZ archive, integrity validation, prune N oldest dumps.


Configurable

TOML config + CLI overrides.


Observability

Prometheus metrics (FILES_PROCESSED, ERRORS_TOTAL).


SRE-Focused

Dry-run, safe-mode, retries, cleanup handlers.



Feature	Single Mode	Batch Mode

Scope	Current dir/files	Recursive subdirs
Archiving	Optional	Enforced retention
Concurrency	Up to 8 workers	Parallel subdirs
Git Metadata	✔️	Per-subdir ✔️



---

📦 Installation

PyPI

pip install create-dump

From Source

git clone https://github.com/dhruv/create-dump.git
cd create-dump
pip install -e .[dev]

Docker

FROM python:3.12-slim
RUN pip install create-dump
ENTRYPOINT ["create-dump"]


---

⚙️ Configuration

Example (pyproject.toml)

[tool.create-dump]
use_gitignore = true
git_meta = true
max_file_size_kb = 5000
dest = "/path/to/dumps"
dump_pattern = ".*_all_create_dump_\\d{8}_\\d{6}\\.(md(\\.gz)?|sha256)$"
excluded_dirs = ["__pycache__", ".git", ".venv", "node_modules"]
metrics_port = 8000

Override any setting via CLI flags.


---

📖 Usage

Single Mode

create-dump single --files "src/*.py" --include-current --git-meta
create-dump single --dry-run --verbose

Batch Mode

create-dump batch --root ./monorepo --keep-last 10 --archive-all
create-dump batch --search --exclude "tests/**" --max-size 10MB


---

🗃️ Archiving Workflow

1. Detect MD/SHA pairs


2. Group by prefix (src_, tests_)


3. ZIP with verification


4. Prune old dumps


5. Cleanup + SHA generation



Artifacts produced:

project_all_create_dump_YYYYMMDD_HHMMSS.md

.sha256 checksum

archives/project_YYYYMMDD_HHMMSS.zip



---

🏗️ Architecture Overview

┌───────────────┐    ┌─────────────────┐    ┌───────────────────┐
│   CLI (Typer) │──▶ │  Orchestrator   │──▶ │   Single/Batch     │
└───────────────┘    └─────────────────┘    └───────────────────┘
                           │
                           ▼
┌───────────────┐    ┌─────────────────┐    ┌───────────────────┐
│ Config (TOML) │◀──▶ │  Core (Models) │◀──▶ │ Logging/Utils     │
└───────────────┘    └─────────────────┘    └───────────────────┘
                           │
                           ▼
┌───────────────┐    ┌─────────────────┐    ┌───────────────────┐
│   Collector   │──▶ │ Writer (MD/Zip) │──▶ │  Archiver (Zip)    │
└───────────────┘    └─────────────────┘    └───────────────────┘


---

🧪 Testing & Development

pytest --cov=src/create_dump --cov-report=html
ruff check src/ tests/
black src/ tests/
mypy src/

Doctests:

PYTHONPATH=src python -m doctest -v src/create_dump/*.py


---

🔒 Security & Reliability

Safe path guards (safe_is_within)

ZIP integrity + SHA256 validation

Tenacity retries

Prometheus metrics on :8000/metrics

Graceful SIGINT/SIGTERM cleanup handlers


Limitations

Sync-only I/O (async pipeline coming in v7)

No remote filesystem support



---

🤝 Contributing

1. Fork repo → create branch


2. Follow Conventional Commits


3. Run full CI suite


4. Add/Update any ADRs under /ADRs


5. Follow the Code of Conduct



Security issues → security@dhruv.io


---

📄 License

MIT License.
See LICENSE.


---

🙏 Acknowledgments

Powered by Typer, Rich, Pydantic, Prometheus

Inspired by tooling from Nx, Bazel, and internal SRE practices


Questions or ideas?
Open an issue or email dhruv@dhruv.io.

---

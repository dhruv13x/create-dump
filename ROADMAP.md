# 🗺️ The Smart Roadmap

This is a visionary, integration-oriented plan that categorizes features from "Core Essentials" to "God Level" ambition.

---

## Phase 1: Foundation (Q1)

**Focus**: Core functionality, stability, security, and basic usage.

- [x] **Branded Markdown Generation**: Auto TOC (list or tree), language-detected code blocks, Git metadata, timestamps.
- [x] **Async-First & Concurrent**: Built on `anyio` for high-throughput, non-blocking I/O.
- [x] **Flexible Archiving**: Automatically archive old dumps into ZIP, tar.gz, or tar.bz2 formats.
- [x] **Project Rollback & Restore**: Rehydrate a full project structure from a `.md` dump file.
- [x] **Git-Native Collection**: Use `git ls-files` for fast, accurate file discovery.
- [x] **Live Watch Mode**: Automatically re-run the dump on any file change.
- [x] **Secret Scanning**: Integrates `detect-secrets` to scan files during processing.
- [x] **Safety & Integrity**: SHA256 hashing for all dumps and atomic writes.
- [x] **Observability**: Prometheus metrics for monitoring.
- [x] **TODO/FIXME Scanning**: Scan for `TODO` or `FIXME` tags in code.
- [x] **Push Notifications**: Get notified on dump completion via `ntfy.sh`.
- [x] **Per-Project Config Discovery**: Enhance `batch` mode to detect and use project-specific `create_dump.toml` files in a monorepo.
- [x] **Dump Header Statistics**: Add total lines of code and file count to the dump header for quick context.
- [x] **Custom Secret Scanning Rules**: Allow users to define custom regex patterns for secret scanning.
- [ ] **Configuration Profiles**: Solidify logic for merging configuration profiles for different environments (e.g., `local`, `ci`).

---

## Phase 2: The Standard (Q2)

**Focus**: Feature parity with top competitors, user experience improvements, and robust error handling.

- [ ] **"Diff-Only" Dump Format**: Output a `.diff` or `.patch` file instead of the full file content when using `--diff-since`.
- [ ] **File Hashing & Caching**: Implement a cache to avoid reprocessing unchanged files in `--watch` mode.
- [ ] **Database Dump Integration**: Add flags to execute `pg_dump` or `mysqldump` and include the output in the dump.
- [ ] **ChatOps Notifications**: Native integration for sending notifications to Slack, Discord, and Telegram.
- [ ] **Enhanced Error Reporting**: More detailed and user-friendly error messages, especially for configuration and I/O errors.

---

## Phase 3: The Ecosystem (Q3-Q4)

**Focus**: Webhooks, API exposure, 3rd party plugins, SDK generation, and extensibility.

- [ ] **Cloud Storage Uploads**: Add support for automatically uploading dumps to S3, GCS, and Azure Blob Storage.
- [ ] **Persistent Server Mode**: A `create-dump serve` command that launches a lightweight FastAPI server to trigger dumps via webhooks.
- [ ] **Official GitHub Action**: A dedicated GitHub Action to generate dumps for pull requests.
- [ ] **Plugin Architecture**: Allow users to create and share their own plugins for custom collectors, scanners, and writers.
- [ ] **SDK Generation**: A library that allows other Python applications to use `create-dump` programmatically.

---

## Phase 4: The Vision (GOD LEVEL)

**Focus**: "Futuristic" features, AI integration, advanced automation, and industry-disrupting capabilities.

- [ ] **AI-Powered Dump Analysis**: Integrate with LLMs to automatically generate summaries of dumps, identify potential issues, and suggest refactorings.
- [ ] **Interactive TUI Explorer**: A `create-dump explore` command that opens a Terminal UI to browse and search a dump file without extracting it.
- [ ] **Direct-to-Archive Streaming**: A high-performance mode that writes directly to a compressed archive, bypassing intermediate files.
- [ ] **Remote/Centralized Configuration**: Allow SRE teams to enforce a central configuration policy from a remote location (e.g., S3).
- [ ] **GitHub App / PR Commenting Bot**: A GitHub App that automatically runs `create-dump` on pull requests and posts the dump as a comment.

---

## The Sandbox (OUT OF THE BOX / OPTIONAL)

**Focus**: Wild, creative, experimental ideas that set the project apart.

- [ ] **Code Archeology**: Analyze the git history of the dumped files to provide insights into code churn, authorship, and historical context.
- [ ] **Dependency Tree Analysis**: Include a dependency graph (e.g., from `pipdeptree` or `npm ls`) in the dump.
- [ ] **Terraform/IaC Integration**: A specialized mode for dumping infrastructure-as-code configurations with built-in validation and visualization.
- [ ] **Jupyter Notebook Integration**: A magic command for Jupyter notebooks that can dump and restore notebook state.

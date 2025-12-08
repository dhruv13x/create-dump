# 🗺️ Strategic ROADMAP V3.0

This is a living strategic document for **create-dump** (V3.0). It balances **Innovation** (Growth), **Stability** (Trust), and **Debt** (Sustainability).

**Key:**
-   `[Debt]`: Technical Debt / Refactoring
-   `[Feat]`: New Feature
-   `[Bug]`: Bug Fix / Stability
-   `[Risk: L/M/H]`: Risk Assessment (Low, Medium, High)
-   `[Size: S/M/L/XL]`: T-Shirt Size Estimate

---

## 🏁 Phase 0: The Core (Stability & Debt)
**Goal**: Solid foundation. Pay down critical debt and ensure stability before scaling features.

- [ ] `[Debt]` **Critical Coverage Increase**: `caching.py` coverage > 95% (Current: ~20%).
    -   *Risk*: Low
    -   *Size*: S
- [ ] `[Debt]` **Unified Error Handling**: Ensure all errors are human-friendly and suggest fixes.
    -   *Risk*: Low
    -   *Size*: M
- [ ] `[Feat]` **Pre-commit Hooks**: Provide official `.pre-commit-hooks.yaml`.
    -   *Risk*: Low
    -   *Size*: S
- [ ] `[Refactor]` **Type Safety**: strict `mypy` compliance across `src/create_dump`.
    -   *Risk*: Low
    -   *Size*: M

---

## 🚀 Phase 1: The Standard (Feature Parity)
**Goal**: Competitiveness. Polishing the UX and configuration story.
**Dependency**: Requires **Phase 0** stability.

- [ ] `[Feat]` **Enhanced Error Reporting**: Suggest fixes for common permission/config errors.
    -   *Risk*: Low
    -   *Size*: M
- [ ] `[Feat]` **Docker Container Support**: Target a running container ID/name as source.
    -   *Risk*: Medium (Requires `docker` CLI or SDK)
    -   *Size*: L
- [ ] `[Feat]` **PDF Export**: Generate `.pdf` dumps (via `weasyprint` or similar).
    -   *Risk*: Medium (Dependency weight)
    -   *Size*: M
- [ ] `[Feat]` **Interactive TUI**: A basic `create-dump explore` interface.
    -   *Risk*: Low
    -   *Size*: M

---

## 🔌 Phase 2: The Ecosystem (Integration)
**Goal**: Interoperability. Opening the platform for developers.
**Dependency**: Requires **Phase 1** API/UX freeze.

- [ ] `[Feat]` **Plugin Architecture**: Dynamic loading of custom collectors/scanners.
    -   *Risk*: High (Architecture change)
    -   *Size*: XL
- [ ] `[Feat]` **SDK Generation**: Official Python library interface (`import create_dump`).
    -   *Risk*: Medium
    -   *Size*: L
- [ ] `[Feat]` **Persistent Server Mode**: `create-dump serve` for webhook triggers.
    -   *Risk*: Medium
    -   *Size*: L
- [ ] `[Feat]` **Cloud Storage Support**: Direct uploads to S3/GCS/Azure.
    -   *Risk*: Medium
    -   *Size*: M

---

## 🔮 Phase 3: The Vision (Innovation)
**Goal**: Market Leader. AI and "God Mode" features.
**Dependency**: Requires **Phase 2** ecosystem.

- [ ] `[Feat]` **AI-Powered Analysis**: Integrated LLM summaries and code health reports.
    -   *Risk*: High (R&D)
    -   *Size*: XL
- [ ] `[Feat]` **RAG Embeddings**: Generate vector embeddings for immediate RAG usage.
    -   *Risk*: High
    -   *Size*: L
- [ ] `[Feat]` **Centralized Config Policy**: Remote configuration enforcement for Enterprise.
    -   *Risk*: Medium
    -   *Size*: M

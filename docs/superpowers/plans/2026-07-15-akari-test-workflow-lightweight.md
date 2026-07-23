# Akari Test Workflow Lightweight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Shorten Akari's ordinary verification loop while retaining every
asset and PDF release guarantee under an explicit owner.

**Architecture:** Keep cheap contracts in root tests, move actual files and
external tools to integration or release audit commands, and expose explicit
serial gates. Preserve all existing public npm aliases and add focused names
for Daily, integration, and release work.

**Tech Stack:** Python 3, `unittest`, Pillow, PyYAML, Node/npm, Poppler,
Tesseract, ImageMagick, Markdown

## Global Constraints

- Target host has 3 CPU cores and 2 GiB RAM.
- Browser, PDF build, Poppler, and Tesseract work runs serially; Node test-file
  concurrency is fixed at one.
- Existing v1.1, legacy v1.2, and Natural Form workflows remain runnable.
- Existing release PDF and checksum files remain byte-for-byte unchanged.
- Candidate and comparison directories remain local and untracked.
- Existing npm aliases keep their current full-audit meanings.
- No changed-file selector or hard memory threshold is added in this pass.

---

## File Structure

- Modify `tests/test_pdf_contract.py`: retain only pure v1.1 PDF primitives.
- Modify `scripts/audit_pdf.py`: add compatible audit levels.
- Modify `tests/test_akari_v1_2_pdf_audit.py`: prove level ownership.
- Modify `scripts/audit_akari_v1_2_pdf.py`: add compatible audit levels.
- Modify `scripts/audit_assets.py`: separate logical and physical work.
- Modify `tests/test_asset_manifest_contract.py`: use in-memory mutations and
  injected physical readers.
- Modify `tests/test_akari_v1_2_natural_form_package.py`: share YAML fixtures.
- Create `scripts/verify_v1_2_release_pins.py`: enforce immutable v1.2.0 hashes.
- Create `tests/test_verify_v1_2_release_pins.py`: cover match, missing, and
  simultaneous drift.
- Modify `package.json`, `AGENTS.md`, and the D02 plan: publish the named gates.

### Task 1: Move v1.1 Actual PDF Checks to Audit Ownership

**Interfaces:**

- `audit_pdf(pdf: Path, level: str = "full") -> None`
- CLI compatibility: `audit_pdf.py PDF` equals `--level full PDF`.

- [x] Add failing unit tests for accepted levels, invalid levels, and structure
  versus raster primitive call sets.
- [x] Run `uv run python -m unittest tests.test_pdf_contract -v` and confirm the
  new API fails because `level` is unsupported.
- [x] Implement `structure`, `raster`, and `full` orchestration while keeping
  the existing call set for `full`.
- [x] Replace actual-PDF unit cases with synthetic parser/text cases and remove
  subprocess/OCR helpers from the test module.
- [x] Run `uv run python -m unittest tests.test_pdf_contract -v` and
  `npm run audit:v1-1:pdf`.

### Task 2: Share Natural Form YAML Fixtures

**Interfaces:**

- `fixture_fingerprint(*values: object) -> str`
- `ImmutableFixtureTestCase.freeze_fixtures(*names: str) -> None`

- [x] Add a focused test proving fixture mutation changes the fingerprint.
- [x] Run the focused test and confirm the fixture helper is missing.
- [x] Add the fingerprint helper and class teardown guard.
- [x] Change repeated `setUp` YAML loads to `setUpClass`, keeping per-test
  `copy.deepcopy` calls before every mutation.
- [x] Run the complete Natural Form module twice to expose order leakage.

### Task 3: Split Asset Logical and Physical Audits

**Interfaces:**

- `audit_manifest_data(source, asset_manifest, page_manifest,
  generation_requests, palette, root) -> list[str]`
- `verify_manifest_files(source, asset_manifest, generation_requests, root,
  *, file_exists=None, hash_reader=None, metadata_reader=None) -> list[str]`
- `verify_source_files(...) -> None`
- `verify_generated_files(...) -> None`

- [x] Add a failing test showing `audit_manifest_data()` never invokes physical
  readers, plus injected-reader tests for source and generated files.
- [x] Run `uv run python -m unittest tests.test_asset_manifest_contract -v` and
  confirm the new API is missing.
- [x] Split path/manifest validation from file existence, hash, and metadata
  verification; make the CLI call both owners explicitly.
- [x] Replace copied-tree mutation helpers with deep-copied in-memory manifests
  and use injected readers for physical negative cases.
- [x] Run the asset module and `npm run audit:assets`.

### Task 4: Add v1.2 PDF Levels and Immutable Release Pins

**Interfaces:**

- `audit_release(pdf: Path, checksum: Path, level: str = "full") -> None`
- `verify_release_pins(root: Path, pins: dict[str, str]) -> None`
- CLI compatibility: no level means `full`.

- [x] Add failing tests for v1.2 structure/raster/full call sets.
- [x] Add failing pin tests for a matching pair, each single-file drift, both
  files drifting, and missing files.
- [x] Implement audit levels without duplicating checksum work in `full`.
- [x] Implement cwd-independent pin verification with both v1.2.0 SHA-256
  constants and aggregated error reporting.
- [x] Run both focused modules, the structure audit, and the pin verifier.

### Task 5: Publish Explicit Serial Gates and Remeasure

**Interfaces:** npm scripts documented in the design's Named Gates section.

- [x] Add package-script contract assertions before editing `package.json`.
- [x] Add the focused, integration, all, and release scripts while preserving
  existing aliases.
- [x] Update `AGENTS.md` and the D02 final verification step to use the named
  gates and state the 3-core, 2 GiB serial-execution rule.
- [x] Run `npm run gate:edit:d02`, `npm run gate:integration:v1-2`,
  `npm run gate:integration:all`, both full PDF audits, and Markdown lint.
- [x] Time `npm run test:python:root`, compare it with the 82.14-second baseline,
  then run `git diff --check` and inspect `git status --short`.

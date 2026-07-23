# Akari Test Workflow Lightweight Design

**Date:** 2026-07-15
**Status:** Implemented and verified
**Scope:** Root Python contracts, asset verification, Natural Form fixtures,
PDF audit levels, v1.2.0 release pins, and named verification gates

## Objective

Reduce the ordinary Akari development loop on a 3-core, 2 GiB VPS without
removing any release guarantee. The current root Python suite takes about 82
seconds on this host because actual PDF OCR, repeated asset-tree audits, and
repeated Natural Form YAML loads run inside ordinary contract tests.

## Chosen Approach

Separate checks by responsibility and keep every public build and audit alias
compatible.

- Root tests own pure and cheap contract behavior.
- `audit:assets` owns real source-file existence, hash, and metadata checks.
- PDF `structure` audits own qpdf, page geometry, fonts, and searchable text.
- PDF `full` audits additionally own raster, blank-page, and v1.1 OCR checks.
- A separate v1.2.0 pin verifier proves that both the release PDF and checksum
  file remain byte-for-byte unchanged during Daily work.
- Named gates are explicit and serial. They do not use a changed-file selector.

The explicit-gate approach is preferred over a selector in this pass because
the repository intentionally keeps candidate and comparison images untracked.
A selector based on all untracked files would repeatedly classify those local
review artifacts as new work.

## Component Boundaries

### v1.1 PDF contracts

`tests/test_pdf_contract.py` retains parser, font, blank-page, and alpha tests
using synthetic inputs. Actual PDF existence, qpdf, raster, OCR, and text
extraction move exclusively to `scripts/audit_pdf.py`.

`npm run audit:v1-1:pdf` remains the backward-compatible full audit. The new
`npm run audit:v1-1:pdf:structure` skips raster and OCR.

### Asset contracts

`scripts/audit_assets.py` exposes separate `audit_manifest_data()` and
`verify_manifest_files()` functions. Logical mutation tests call only the pure
dictionary API; physical verifier tests inject file, hash, and metadata
readers. The CLI always calls both functions, so `npm run audit:assets`
preserves the current real-file guarantee.

### Natural Form fixtures

Natural Form YAML is loaded once per test class. Tests continue to deep-copy
objects before mutation. Each class fingerprints its shared fixture and fails
at teardown if a test changes the canonical object.

### PDF levels and release pins

Both PDF audit CLIs accept `--level structure|raster|full`; existing invocations
without `--level` mean `full`. A new cwd-independent verifier contains the
immutable v1.2.0 SHA-256 values and reports every missing or changed artifact in
one failure.

### Named gates

- `gate:edit:d02`: Natural Form tests, validator, and v1.2.0 release pins.
- `gate:integration:v1-2`: root contracts, Node tests, Natural Form validator,
  real asset/palette/alpha audits, v1.2 structure audit, pins, and Markdown.
- `gate:integration:all`: the v1.2 integration gate plus legacy tests and the
  v1.1 structure audit.
- `gate:release:v1-2`: common checks followed by one build and one full v1.2
  audit, then fixed pins. It does not run a structure audit before the full
  audit.
- `gate:release:v1-1`: common checks followed by one v1.1 build and one full
  v1.1 audit.

Commands run serially. The Node test runner also fixes file concurrency at one.
Chromium, Poppler, Tesseract, and PDF builds are never launched concurrently
on the constrained VPS.

## Compatibility and Safety

- Existing `test:python`, `audit:v1-1:pdf`, `audit:v1-2:pdf`, `audit:pdf`,
  `release:v1-2`, and `audit` aliases keep their meanings.
- v1.1, legacy v1.2, and all existing release files remain present.
- Candidate and comparison directories remain local and untracked.
- No hard memory cutoff is added until process-tree peak memory is measured.
- Node browser sharing, cache layers, and changed-file selection are deferred
  until the high-cost Python work is remeasured.

## Verification

Each new production boundary is introduced by a failing focused test. After
each component turns green, run its existing full module. Final verification
uses the named integration gates, both full PDF audits, the release pin
verifier, Markdown lint, `git diff --check`, and a fresh root-suite timing.

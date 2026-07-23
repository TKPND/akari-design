# Akari v1.2.0 Release Closure Design

## Goal

Close Akari v1.2.0 as a reproducible Natural Form Core release by publishing
the approved 14-page settings PDF, its SHA-256 checksum, dedicated build and
audit commands, and repository guidance that makes v1.2 the default settings
reference while preserving the complete v1.1 deliverable and workflow.

## Current State

- C01 through C07 and D01 are accepted at their canonical paths.
- Gate 4 has outcome `release` with no unresolved finding.
- `akari-v1.2/README.md` and the Core design already describe Natural Form as
  a Core Release.
- `akari-v1.2/release/` contains only `.gitkeep`; the PDF and checksum named in
  the Core design do not exist yet.
- The generic `build:pdf` and `audit:pdf` commands still target
  `dist/akari-v1.1-settings.pdf`.
- Local candidate and comparison images are intentionally untracked and must
  remain outside the release commit.

## Chosen Approach

Add a dedicated v1.2 document definition and release audit to the existing
Playwright PDF system. Share the stable renderer, theme, local font, and
16:9 page geometry, but keep v1.2 page data, output paths, tests, and audit
contracts separate from v1.1.

This is preferred over a broad renderer rewrite because the existing renderer
already supports multiple document definitions. It is preferred over a
one-time PDF export because a formal release must remain reproducible and
auditable.

## Compatibility and Defaults

The v1.1 PDF remains tracked at `dist/akari-v1.1-settings.pdf`. Its existing
Python exporter, PDF audit, document definition, and tests remain functional.
Explicit aliases expose those workflows as:

- `npm run build:v1-1:previews`
- `npm run build:v1-1:pdf`
- `npm run audit:v1-1:pdf`

After v1.2.0 closes, the unqualified settings commands become v1.2 aliases:

- `npm run build:previews` builds Natural Form previews.
- `npm run build:pdf` builds the Natural Form release PDF and checksum.
- `npm run audit:pdf` audits the Natural Form release PDF and checksum.

The explicit v1.2 commands are:

- `npm run build:v1-2:previews`
- `npm run build:v1-2:pdf`
- `npm run audit:v1-2:pdf`
- `npm run release:v1-2`

`release:v1-2` validates the Natural Form package, builds the PDF and checksum,
and then runs the dedicated PDF audit. Existing non-settings v1.1 documents,
including the Situation Daybook and Tonari No Akari, keep their current paths
and commands.

## Release Artifacts

The release contains these tracked files:

- `akari-v1.2/release/akari-v1.2-core-settings.pdf`
- `akari-v1.2/release/checksums.txt`

`checksums.txt` contains exactly one GNU `sha256sum`-compatible line:

```text
<64 lowercase hexadecimal characters>  akari-v1.2-core-settings.pdf
```

The checksum covers the distributed PDF. Accepted image integrity and
source-to-accepted linkage remain governed by `npm run validate:v1-2` and the
Natural Form manifests. The obsolete `release/.gitkeep` is removed once the
two real release artifacts are tracked.

## PDF Structure

The document is a 14-page, 16:9 landscape PDF using the existing local Inter
font and visual theme. It follows section 28 of the Core design exactly:

1. Cover / Natural Form
2. v1.1 to v1.2 inheritance
3. Identity Lock
4. Natural Front Stance
5. Back and 45-degree Views
6. Weight and Joint Guidelines
7. Floor Sitting Master
8. Floor Sitting Anatomy Notes
9. Indoor Sock Feet
10. Morning Bed Hair
11. Sleepy-to-Soft-Smile Expressions
12. D01 Morning Validation
13. Do / Don't
14. Source Manifest and Review Status

The pages use only accepted Natural Form images and copied, provenance-locked
references already declared by the package. Candidate and comparison paths are
not document inputs. The page data names every displayed source through a
document-local asset-path map so it does not duplicate the lifecycle manifests
or require a new YAML parser in Node.

Page 14 records C01 through C07 and D01 as accepted, Gate 4 as released, and
the release version as v1.2.0. The renderer tests cross-check the document asset
paths against canonical accepted paths so a stale or non-accepted image cannot
silently enter the PDF.

## Renderer Changes

Add `natural-form` to the existing document loader registry. The v1.2 document
definition owns:

- the 14 ordered page records;
- the accepted-image and inherited-reference asset map;
- the v1.2 output PDF path;
- an ignored preview directory and generated HTML path.

The shared source-path resolver first accepts a document-local `assetPaths`
map, then falls back to the existing source and asset manifest behavior. This
keeps every current v1.1 document unchanged while allowing Natural Form to use
its canonical YAML-governed package paths without adding runtime dependencies.

No new generic block type is required. Existing image, guide-line, and note
blocks can express all 14 pages. Layout-specific CSS is added only where the
Natural Form pages need a distinct grid; shared v1.1 selectors and values are
not changed unless a regression test proves the change safe.

## Build and Checksum Flow

The v1.2 PDF exporter runs the shared Node renderer with
`--document natural-form --pdf`. It writes the PDF to the release directory,
computes SHA-256 from the completed file, and atomically replaces
`checksums.txt` with the exact one-line contract.

If rendering or hashing fails, the command exits non-zero. It must not report a
release success or leave a checksum that claims to describe a newly built PDF.
The existing v1.1 exporter remains unchanged and is called by the explicit
v1.1 npm alias.

## Audit Contract

The dedicated v1.2 audit rejects the release unless all of these checks pass:

1. The PDF and `checksums.txt` exist as regular files.
2. `qpdf --check` accepts the PDF.
3. `pdfinfo` reports exactly 14 pages with a 16:9 page ratio.
4. `pdffonts` reports at least one embedded Unicode font.
5. Rendering at 288 DPI produces exactly 14 non-blank 3840 x 2160 PNG pages.
6. Extracted text contains v1.2.0, every required page title, C01 through C07,
   D01, and the Gate 4 release status.
7. `checksums.txt` has the exact one-line format and its digest matches the PDF.

The audit writes rendered pages and extracted text only under ignored build or
working directories. It does not modify the release PDF or checksum.

## Tests

Use test-driven changes around four contracts:

- Node document tests verify the 14-page sequence, accepted-only asset map,
  supported blocks, HTML rendering, image containment, and renderer CLI support
  for `natural-form`.
- Python exporter tests verify the Node invocation, checksum format, digest,
  and failure behavior without requiring a full PDF render in each unit test.
- Python audit tests verify PDF metadata parsing, font validation, required
  text, checksum syntax, checksum mismatch rejection, and missing-file errors.
- Natural Form package tests verify the real release artifacts, npm command
  aliases, v1.2.0 documentation state, and preservation of the v1.1 PDF path and
  explicit v1.1 workflows.

After implementation, run fresh full verification from the final tracked
state:

```bash
npm run release:v1-2
npm run test:node
npm run test:python
npm run audit
git ls-files -z -- '*.md' | xargs -0 ./node_modules/.bin/markdownlint-cli2
git diff --check
```

The v1.1 PDF audit is also run explicitly to prove the preserved artifact and
workflow still pass after the default command switch.

## Documentation Changes

Update the following durable guidance:

- `AGENTS.md`: make the v1.2 release PDF the default artifact and identify the
  v1.1 PDF as preserved inheritance and history material.
- Root `README.md`: present Natural Form v1.2.0 as the primary settings release,
  list both settings PDFs, and document explicit v1.1 commands.
- `akari-v1.2/README.md`: record version v1.2.0, release artifact paths, and
  release, build, audit, and validation commands.
- Core design: replace `Draft 0.2` with `v1.2.0` and state that the release
  artifacts have been published.
- Daily handoff: state that Gate 4 and final Core acceptance are complete, so
  Daily Wave 1 is unblocked without making Daily work part of v1.2.0.

## Scope Boundaries

This release closure does not:

- generate or refine any character image;
- promote a candidate or change an accepted image;
- modify the Natural Form identity, body, state, or rendering contracts;
- include local candidate or comparison images in Git;
- produce Daily Wave 1 scenes;
- delete, rename, or overwrite `dist/akari-v1.1-settings.pdf`;
- refactor unrelated v1.1, Daybook, Tonari, or legacy workflows.

## Completion Criteria

v1.2.0 is closed only when:

- the tracked PDF and checksum exist at the canonical release paths;
- the checksum matches the final PDF;
- v1.2 package validation, release audit, full Node and Python tests, repository
  audits, tracked Markdown lint, and whitespace checks pass freshly;
- the explicit v1.1 PDF build and audit path remains usable;
- repository guidance consistently names v1.2.0 as the default settings
  release; and
- Git status shows only the pre-existing local candidate and comparison
  directories outside the committed release scope.

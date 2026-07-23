# Akari v1.2.0 Release Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish and verify the reproducible Akari Natural Form v1.2.0 settings PDF and make it the default settings artifact without removing the v1.1 PDF or workflow.

**Architecture:** Register a dedicated `natural-form` document with the shared Playwright renderer, add a Python exporter that renders the PDF and atomically writes its SHA-256 checksum, and add an independent PDF/checksum audit. Preserve the current v1.1 implementation behind explicit npm aliases while changing only the unqualified settings aliases and repository guidance to v1.2.

**Tech Stack:** Node.js ES modules, Playwright, Node test runner, Python 3.11+, `unittest`, Pillow, Poppler tools, qpdf, SHA-256, npm scripts, Markdown.

## Global Constraints

- Preserve `dist/akari-v1.1-settings.pdf` and its existing source implementation.
- Keep every local `akari-v1.2/source/candidates/` and `akari-v1.2/comparisons/` directory untracked and unstaged.
- Use only accepted Natural Form images and provenance-locked copied references in the PDF.
- The release PDF is exactly 14 pages in 16:9 landscape format.
- `checksums.txt` contains exactly one GNU `sha256sum`-compatible line for `akari-v1.2-core-settings.pdf`.
- Do not generate, refine, replace, or promote any Akari image.
- Use `apply_patch` for hand edits and existing npm commands for verification.
- Run implementation in an isolated worktree; merge only after fresh final verification.

---

## File Map

### New files

- `tools/pdf/natural-form-document.mjs`: v1.2 page model, asset map, and output paths.
- `tools/pdf/natural-form-document.test.mjs`: v1.2 renderer and page-contract tests.
- `scripts/export_akari_v1_2_pdf.py`: PDF render orchestration and atomic checksum writer.
- `scripts/audit_akari_v1_2_pdf.py`: release PDF and checksum audit.
- `tests/test_export_akari_v1_2_pdf.py`: exporter unit tests.
- `tests/test_akari_v1_2_pdf_audit.py`: audit unit tests.
- `akari-v1.2/release/akari-v1.2-core-settings.pdf`: generated tracked release PDF.
- `akari-v1.2/release/checksums.txt`: generated tracked checksum.

### Modified files

- `tools/pdf/render.mjs`: lazy-load the `natural-form` document.
- `tools/pdf/render-html.mjs`: resolve document-local asset paths before manifest paths.
- `tools/pdf/styles.css`: Natural Form page-grid rules only.
- `package.json`: explicit v1.1/v1.2 commands and new defaults.
- `tests/test_environment_contract.py`: npm command contract.
- `tests/test_akari_v1_2_natural_form_package.py`: release and documentation contract.
- `AGENTS.md`: v1.2 default artifact guidance and v1.1 fallback.
- `README.md`: primary release and both settings deliverables.
- `akari-v1.2/README.md`: v1.2.0 release usage.
- `akari-v1.2/docs/akari-v1.2-core-design.md`: final version and artifact state.
- `akari-v1.2/docs/akari-v1.2-daily-handoff.md`: Daily Wave 1 unblocked state.

### Removed file

- `akari-v1.2/release/.gitkeep`: replaced by actual release artifacts.

---

### Task 1: Natural Form Document and Renderer Registration

**Files:**

- Create: `tools/pdf/natural-form-document.mjs`
- Create: `tools/pdf/natural-form-document.test.mjs`
- Modify: `tools/pdf/render.mjs`
- Modify: `tools/pdf/render-html.mjs`
- Modify: `tools/pdf/styles.css`

**Interfaces:**

- Produces: `naturalFormDocument` with `id`, `title`, `pages`, `assetPaths`, `outputPdf`, `previewDir`, and `siteHtml`.
- Produces: renderer document name `natural-form`.
- Extends: `sourceImagePath(assetId, document)` to accept `document.assetPaths`.

- [ ] **Step 1: Write failing document-contract tests**

Create tests that assert this exact page sequence:

```js
const expectedPages = [
  [1, "cover-natural-form", "Cover / Natural Form"],
  [2, "inheritance", "v1.1 to v1.2 Inheritance"],
  [3, "identity-lock", "Identity Lock"],
  [4, "natural-front-stance", "Natural Front Stance"],
  [5, "back-and-45-views", "Back and 45-degree Views"],
  [6, "weight-and-joints", "Weight and Joint Guidelines"],
  [7, "floor-sitting-master", "Floor Sitting Master"],
  [8, "floor-sitting-anatomy", "Floor Sitting Anatomy Notes"],
  [9, "indoor-sock-feet", "Indoor Sock Feet"],
  [10, "morning-bed-hair", "Morning Bed Hair"],
  [11, "expression-gradient", "Sleepy-to-Soft-Smile Expressions"],
  [12, "d01-morning-validation", "D01 Morning Validation"],
  [13, "do-dont", "Do / Don't"],
  [14, "source-review-status", "Source Manifest and Review Status"],
];
```

Assert the document metadata exactly:

```js
assert.equal(naturalFormDocument.id, "akari-v1.2-natural-form-core");
assert.equal(naturalFormDocument.title, "Akari v1.2.0 Natural Form Core Settings");
assert.equal(
  naturalFormDocument.outputPdf,
  "akari-v1.2/release/akari-v1.2-core-settings.pdf",
);
assert.equal(naturalFormDocument.previewDir, "build/akari-v1.2-page-previews");
assert.equal(naturalFormDocument.siteHtml, "build/akari-v1.2-site/index.html");
```

Assert `assetPaths` includes all 13 accepted PNG paths from `assets.yaml`, that
every page uses supported existing block types, and that no value contains
`source/candidates/` or `comparisons/`. Test `renderHtml(naturalFormDocument)`,
`sourceImagePath("C01", naturalFormDocument)`, and:

```js
assert.deepEqual(
  renderer.parseRenderArgs(["--document", "natural-form", "--previews", "--pdf"]),
  { documentName: "natural-form", commands: ["previews", "pdf"] },
);
```

- [ ] **Step 2: Run the focused Node tests and verify RED**

Run:

```bash
node --test tools/pdf/natural-form-document.test.mjs
```

Expected: FAIL because `natural-form-document.mjs` and renderer registration do
not exist.

- [ ] **Step 3: Implement the document-local asset resolver**

At the start of `sourceImagePath`, add this exact precedence:

```js
export function sourceImagePath(assetId, document = settingsDocument) {
  if (document.assetPaths) {
    if (!Object.hasOwn(document.assetPaths, assetId)) {
      throw new Error(`Unknown source asset id: ${assetId}`);
    }
    return document.assetPaths[assetId];
  }

  const sourceManifest = loadJson(document.sourceManifestPath);
  const assetManifest = loadJson(document.assetManifestPath);
  // Preserve the existing manifest-backed implementation below.
}
```

- [ ] **Step 4: Implement the Natural Form page model**

Define IDs for every accepted variant (`C01`, `C02`, `C03-hairpin`,
`C03-non-hairpin`, `C04`, `C05`, `C06-1` through `C06-4`, `C07-standing`,
`C07-seated`, and `D01`) and map each ID to its canonical tracked PNG.

Use the existing helpers and block shapes:

```js
function imageBlock(images) {
  return { type: "image", images };
}

function notes(title, items, variant = "plain") {
  return { type: "note-list", title, variant, items };
}

function guides(title, rows) {
  return { type: "guide-lines", title, rows };
}
```

Populate all 14 pages in the approved order. Page 14 must contain native text
for `v1.2.0`, `C01` through `C07`, `D01`, `accepted`, `Gate 4`, and `release`.
Page 13 must state the hard rules from the Core design: preserve identity,
natural weight, traceable limbs, stable socks and hair ornament, and no staged
pose, broken anatomy, disconnected feet, or candidate-path input.

- [ ] **Step 5: Register the lazy document loader and usage text**

Add:

```js
"natural-form": async () => {
  const { naturalFormDocument } = await import("./natural-form-document.mjs");
  return naturalFormDocument;
},
```

Update the usage string to list
`settings|daybook|tonari-no-akari|natural-form`.

- [ ] **Step 6: Add scoped Natural Form CSS**

Add selectors beginning with `.layout-natural-form-` only. Use the existing
page variables and image-card styles. Ensure portrait images remain
`object-fit: contain`; use two-, three-, or four-column grids according to the
page's image count, and keep page 14 text inside the body area at screen and
print sizes.

- [ ] **Step 7: Run focused and full Node tests**

Run:

```bash
node --test tools/pdf/natural-form-document.test.mjs
npm run test:node
```

Expected: PASS with zero failing tests.

- [ ] **Step 8: Commit Task 1**

```bash
git add tools/pdf/natural-form-document.mjs \
  tools/pdf/natural-form-document.test.mjs \
  tools/pdf/render.mjs tools/pdf/render-html.mjs tools/pdf/styles.css
git commit -m "feat: add Natural Form PDF document"
```

---

### Task 2: PDF Export and Atomic Checksum

**Files:**

- Create: `scripts/export_akari_v1_2_pdf.py`
- Create: `tests/test_export_akari_v1_2_pdf.py`

**Interfaces:**

- Produces: `sha256_file(path: Path) -> str`.
- Produces: `write_checksum(pdf: Path, checksum_path: Path) -> None`.
- Produces: `main() -> int` that renders the PDF and writes its checksum.

- [ ] **Step 1: Write failing exporter tests**

Test a known byte payload against `hashlib.sha256(payload).hexdigest()`. Verify
`write_checksum` writes exactly this one-line shape with one trailing newline:

```text
<digest>  akari-v1.2-core-settings.pdf
```

Mock `subprocess.run` and assert `main()` invokes:

```python
["node", "tools/pdf/render.mjs", "--document", "natural-form", "--pdf"]
```

with `cwd=ROOT` and `check=True`. Also assert a render exception leaves an
existing checksum unchanged.

- [ ] **Step 2: Run exporter tests and verify RED**

Run:

```bash
uv run python -m unittest tests.test_export_akari_v1_2_pdf -v
```

Expected: FAIL because the exporter does not exist.

- [ ] **Step 3: Implement hashing and atomic checksum replacement**

Use these constants and signatures:

```python
ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "akari-v1.2/release/akari-v1.2-core-settings.pdf"
CHECKSUM = ROOT / "akari-v1.2/release/checksums.txt"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

`write_checksum` creates the release directory, writes a temporary sibling
file with UTF-8 and `\n`, then replaces `checksums.txt` using `Path.replace`.
`main` runs the Node renderer before calculating or writing the checksum.

- [ ] **Step 4: Run exporter tests**

Run:

```bash
uv run python -m unittest tests.test_export_akari_v1_2_pdf -v
```

Expected: PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add scripts/export_akari_v1_2_pdf.py tests/test_export_akari_v1_2_pdf.py
git commit -m "feat: export Natural Form release checksum"
```

---

### Task 3: Dedicated Release Audit

**Files:**

- Create: `scripts/audit_akari_v1_2_pdf.py`
- Create: `tests/test_akari_v1_2_pdf_audit.py`

**Interfaces:**

- Produces: `require_pdfinfo_contract(output: str) -> None`.
- Produces: `require_font_table(output: str) -> None`.
- Produces: `require_searchable_text(text: str) -> None`.
- Produces: `require_checksum_contract(pdf: Path, checksum: Path) -> None`.
- Produces: `audit_release(pdf: Path, checksum: Path) -> None`.

- [ ] **Step 1: Write failing audit unit tests**

Cover 14-page and 16:9 acceptance, wrong count and ratio rejection, embedded
Unicode font acceptance, bad font rows, required text, missing text, correct
checksum, uppercase digest, extra lines, wrong filename, wrong digest, missing
files, and missing trailing newline.

Use this required text tuple:

```python
REQUIRED_TEXT = (
    "Akari v1.2.0 Natural Form Core Settings",
    "Cover / Natural Form",
    "v1.1 to v1.2 Inheritance",
    "Identity Lock",
    "Natural Front Stance",
    "Back and 45-degree Views",
    "Weight and Joint Guidelines",
    "Floor Sitting Master",
    "Floor Sitting Anatomy Notes",
    "Indoor Sock Feet",
    "Morning Bed Hair",
    "Sleepy-to-Soft-Smile Expressions",
    "D01 Morning Validation",
    "Do / Don't",
    "Source Manifest and Review Status",
    "C01", "C02", "C03", "C04", "C05", "C06", "C07", "D01",
    "Gate 4", "release",
)
```

- [ ] **Step 2: Run audit tests and verify RED**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_2_pdf_audit -v
```

Expected: FAIL because the audit module does not exist.

- [ ] **Step 3: Implement metadata, render, text, and checksum audits**

Follow the daybook audit structure with:

```python
EXPECTED_PAGE_COUNT = 14
EXPECTED_RENDER_SIZE = (3840, 2160)
RENDER_DIR = ROOT / "build/akari-v1.2-pdf-rendered-pages"
TEXT_DIR = ROOT / "build/akari-v1.2-pdf-text"
CHECKSUM_RE = re.compile(
    r"^([0-9a-f]{64})  akari-v1\.2-core-settings\.pdf\n$"
)
```

Run `qpdf --check`, `pdfinfo`, `pdffonts`, `pdftoppm -png -r 288`, and
`pdftotext`. Require 14 rendered PNGs, each 3840 x 2160 and above the existing
`0.003` non-background content ratio. Compare the checksum capture with a
fresh SHA-256 over the PDF bytes.

- [ ] **Step 4: Implement the CLI result contract**

With no arguments, audit the canonical PDF and checksum. On success print
`Natural Form pdf audit: ok`. On `AuditError`, print
`Natural Form pdf audit: failed: <message>` to stderr and return 1.

- [ ] **Step 5: Run focused audit tests**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_2_pdf_audit -v
```

Expected: PASS.

- [ ] **Step 6: Commit Task 3**

```bash
git add scripts/audit_akari_v1_2_pdf.py tests/test_akari_v1_2_pdf_audit.py
git commit -m "test: audit Natural Form release PDF"
```

---

### Task 4: npm Defaults, Package Contracts, and Release Guidance

**Files:**

- Modify: `package.json`
- Modify: `tests/test_environment_contract.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `akari-v1.2/README.md`
- Modify: `akari-v1.2/docs/akari-v1.2-core-design.md`
- Modify: `akari-v1.2/docs/akari-v1.2-daily-handoff.md`
- Delete: `akari-v1.2/release/.gitkeep`

**Interfaces:**

- Produces: explicit v1.1 aliases, explicit v1.2 commands, v1.2 default aliases,
  and final v1.2.0 documentation state.

- [ ] **Step 1: Write failing package and command-contract tests**

Assert these exact script values:

```python
expected = {
    "build:v1-1:previews": "uv run python scripts/render_page_previews.py",
    "build:v1-1:pdf": "uv run python scripts/export_pdf.py",
    "audit:v1-1:pdf": (
        "uv run python scripts/audit_pdf.py dist/akari-v1.1-settings.pdf"
    ),
    "build:v1-2:previews": (
        "node tools/pdf/render.mjs --document natural-form --previews"
    ),
    "build:v1-2:pdf": "uv run python scripts/export_akari_v1_2_pdf.py",
    "audit:v1-2:pdf": "uv run python scripts/audit_akari_v1_2_pdf.py",
    "build:previews": "npm run build:v1-2:previews",
    "build:pdf": "npm run build:v1-2:pdf",
    "audit:pdf": "npm run audit:v1-2:pdf",
    "release:v1-2": (
        "npm run validate:v1-2 && npm run build:v1-2:pdf && "
        "npm run audit:v1-2:pdf"
    ),
}
```

Require `audit` to include both PDF audits. Replace `Draft 0.2` with
`**Version:** v1.2.0`. Require the v1.2 README to name both release files and
`release:v1-2`. Require AGENTS to use the v1.2 PDF as default and preserve the
exact v1.1 path. Require `.gitkeep` absent after real release files exist.

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```bash
uv run python -m unittest \
  tests.test_environment_contract \
  tests.test_akari_v1_2_natural_form_package -v
```

Expected: FAIL on missing scripts and final release documentation.

- [ ] **Step 3: Update package scripts**

Add the exact values above. Define:

```json
"audit": "npm run audit:assets && npm run audit:palette && npm run audit:v1-1:pdf && npm run audit:v1-2:pdf && npm run audit:alpha"
```

Do not edit the v1.1 exporter, audit, document definition, or tracked PDF.

- [ ] **Step 4: Update release guidance and version state**

Apply these exact semantic changes:

- Default artifact: `akari-v1.2/release/akari-v1.2-core-settings.pdf`.
- Historical artifact: `dist/akari-v1.1-settings.pdf`.
- Core version: `v1.2.0`.
- Core status: `Natural Form Core Release`.
- Daily state: Gate 4 and final Core acceptance are complete; Wave 1 is
  unblocked but outside v1.2.0 scope.
- Release outputs: PDF and checksum paths plus build/audit/release commands.

- [ ] **Step 5: Run focused tests and Markdown lint**

Run:

```bash
uv run python -m unittest \
  tests.test_environment_contract \
  tests.test_akari_v1_2_natural_form_package -v
npm run lint:md
```

Expected: tests pass. Fix every lint error in changed tracked files. If the
repo-wide command also reports unrelated local/dependency noise, record it and
run tracked Markdown lint as the release gate.

- [ ] **Step 6: Commit Task 4**

```bash
git add package.json tests/test_environment_contract.py \
  tests/test_akari_v1_2_natural_form_package.py AGENTS.md README.md \
  akari-v1.2/README.md akari-v1.2/docs/akari-v1.2-core-design.md \
  akari-v1.2/docs/akari-v1.2-daily-handoff.md \
  akari-v1.2/release/.gitkeep
git commit -m "docs: declare Akari v1.2.0 release"
```

---

### Task 5: Generate, Inspect, and Publish Release Artifacts

**Files:**

- Create: `akari-v1.2/release/akari-v1.2-core-settings.pdf`
- Create: `akari-v1.2/release/checksums.txt`

**Interfaces:**

- Consumes: renderer, exporter, audit, manifests, and accepted PNGs.
- Produces: final tracked v1.2.0 release payload.

- [ ] **Step 1: Validate the source package**

Run `npm run validate:v1-2` and require exit 0.

- [ ] **Step 2: Build previews and release payload**

Run:

```bash
npm run build:v1-2:previews
npm run build:v1-2:pdf
```

Expected: 14 preview PNGs, the release PDF, and one checksum line.

- [ ] **Step 3: Run the release audit**

Run `npm run audit:v1-2:pdf`.

Expected: `Natural Form pdf audit: ok`.

- [ ] **Step 4: Perform visual page review**

Create a temporary contact sheet from the 14 audited pages under `build/`,
inspect it with `view_image`, and inspect dense or suspicious pages at original
resolution. Reject clipping, overlap, unreadable text, wrong assets, stretching,
broken images, and inconsistent page numbers. For a defect, add a failing layout
test, fix scoped CSS or page data, rebuild, and repeat the audit.

- [ ] **Step 5: Verify checksum independently**

From `akari-v1.2/release/`, run:

```bash
sha256sum --check checksums.txt
```

Expected: `akari-v1.2-core-settings.pdf: OK`.

- [ ] **Step 6: Commit release artifacts**

```bash
git add akari-v1.2/release/akari-v1.2-core-settings.pdf \
  akari-v1.2/release/checksums.txt
git commit -m "release: publish Akari v1.2.0 settings"
```

---

### Task 6: Final Verification and Main-Branch Closure

**Files:**

- Verify: all Task 1 through Task 5 files.

**Interfaces:**

- Produces: evidence-backed v1.2.0 closure on `main`.

- [ ] **Step 1: Rebuild from a clean tracked state**

Run:

```bash
npm run release:v1-2
git diff --exit-code -- akari-v1.2/release/akari-v1.2-core-settings.pdf \
  akari-v1.2/release/checksums.txt
```

Expected: release passes and rebuilding produces no tracked artifact diff. If
Chromium adds nondeterministic metadata, remove it in the exporter before
accepting the release.

- [ ] **Step 2: Prove the preserved v1.1 workflow**

Run:

```bash
npm run build:v1-1:pdf
npm run audit:v1-1:pdf
```

Expected: both pass. Confirm the v1.1 path still exists. If the old exporter
changes only nondeterministic PDF metadata, retain the original tracked v1.1
artifact and record that limitation rather than committing a v1.1 binary diff.

- [ ] **Step 3: Run the full verification suite**

Run:

```bash
npm run test:node
npm run test:python
npm run validate:v1-2
npm run audit
git ls-files -z -- '*.md' | xargs -0 ./node_modules/.bin/markdownlint-cli2
git diff --check
```

Expected: every command exits 0.

- [ ] **Step 4: Verify branch scope**

Run:

```bash
git status --short
git diff main...HEAD --stat
git diff main...HEAD --name-only
```

Expected: only planned durable files. No candidate or comparison image is
tracked.

- [ ] **Step 5: Merge the verified branch into main**

Fast-forward from the primary checkout. Do not move or delete the pre-existing
untracked candidate/comparison directories. Remove the worktree and branch only
after merge succeeds.

- [ ] **Step 6: Re-run proof on final main**

Run:

```bash
npm run release:v1-2
npm run test:node
npm run test:python
npm run audit
git ls-files -z -- '*.md' | xargs -0 ./node_modules/.bin/markdownlint-cli2
git diff --check
git status --short --branch
```

Expected: every verification command exits 0. The only untracked paths are the
preserved local candidate and comparison directories.

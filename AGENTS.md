# Agent Guide

This repository builds and audits Akari visual-reference materials.

## Default Artifact

- When the user says "the PDF", "the settings PDF", or asks for a PDF audit
  without naming a file, use
  `akari-v1.2/release/akari-v1.2-core-settings.pdf`.
- Do not ask the user to repeat that path unless they explicitly refer to a
  different artifact.
- The text extraction output for the default PDF lives under
  `build/akari-v1.2-pdf-text/` after audit.
- The preserved v1.1 settings PDF is `dist/akari-v1.1-settings.pdf`; use it for
  inheritance, history, recovery, or an explicitly requested v1.1 audit.

## Akari v1.2

- Unqualified `v1.2` means the Natural Form package under `akari-v1.2/`.
- The previous face-hair, eight-view turnaround, motion, and overhead-room work
  lives under `legacy/akari-v1.2-pre-natural-form/` and uses only
  `legacy:v1-2:*` commands.
- Do not use a legacy working path as a Natural Form generation reference.
  Copy the selected file into `akari-v1.2/references/legacy/` and record its
  role, rationale, and SHA-256 in `akari-v1.2/manifest/inheritance.yaml`.
- Run `npm run validate:v1-2` after changing Natural Form manifests or
  references.
- The Natural Form release PDF is the default settings reference. The v1.1 PDF
  remains a preserved inheritance and history artifact.

## Project Shape

- Source inputs and review metadata live under `source/`.
- Original source images should remain immutable under `source/originals/`.
- Palette data lives in `source/palette/akari-v1.1-palette.json`.
- Page and asset contracts live in `source/manifests/`.
- PDF rendering code lives under `tools/pdf/`.
- Python build and audit scripts live under `scripts/`.
- Generated intermediate output belongs under `build/`, `tmp/`, or another
  ignored working directory unless the user asks to preserve it.

## Common Commands

- Install Node dependencies: `npm ci`
- Install Python dependencies: `uv sync --locked`
- Check required system tools: `uv run python scripts/verify_environment.py`
- Run Node tests: `npm run test:node`
- Run Python tests: `npm run test:python`
- Run the fast D02/Daily edit gate: `npm run gate:edit:d02`
- Run v1.2 integration checks: `npm run gate:integration:v1-2`
- Run broad integration including legacy and v1.1 structure:
  `npm run gate:integration:all`
- Build page previews: `npm run build:previews`
- Build the default PDF: `npm run build:pdf`
- Audit the default PDF: `npm run audit:pdf`
- Build the preserved v1.1 PDF: `npm run build:v1-1:pdf`
- Audit the preserved v1.1 PDF: `npm run audit:v1-1:pdf`
- Validate, build, and audit v1.2.0: `npm run release:v1-2`
- Run the formal v1.2 release gate: `npm run gate:release:v1-2`
- Run the formal v1.1 release gate: `npm run gate:release:v1-1`
- Run all audits: `npm run audit`
- Lint Markdown: `npm run lint:md`

## Working Rules

- Prefer existing npm scripts over ad hoc command lines.
- If a script needs the settings PDF path and the user did not specify one,
  pass `akari-v1.2/release/akari-v1.2-core-settings.pdf`.
- For Akari image selection and refinement, default to quality-first judgment
  unless the user explicitly asks for a conservative or safety-biased pass.
  Do not keep a weaker image merely because it is the most conservative-looking
  option. Prefer the candidate with the strongest expression read, character
  appeal, and finished image quality when it still passes identity, age
  impression, anatomy, composition, and artifact gates. Hard safety/policy
  constraints still apply.
- When generating or refining Akari images, use relevant reference images by
  default. Before calling image generation, open the current selected candidate
  plus the strongest applicable identity, hair, outfit, pose, or expression
  references with `view_image`, describe each reference image's role in the
  prompt, and keep those references visible in the conversation context. Do not
  rely on text-only prompts for identity-sensitive Akari generations unless the
  user explicitly asks for a text-only exploration.
- Before changing rendering, manifests, or audit behavior, identify a concrete
  verification command from the list above.
- After changing Markdown, run `npm run lint:md`.
- Use the smallest named gate that owns the changed behavior. Daily-only work
  starts with `gate:edit:d02`; shared Natural Form work uses
  `gate:integration:v1-2`; legacy, cross-version, or unknown broad work uses
  `gate:integration:all`.
- Full PDF raster/OCR belongs to `gate:release:v1-1` or
  `gate:release:v1-2`. Do not put a full release audit in the ordinary Daily
  edit loop.
- This repository is commonly developed on a 3-core, 2 GiB VPS. Keep named
  gate commands serial; do not overlap Chromium, PDF builds, Poppler, or
  Tesseract.
- Do not select checks from every untracked path. Candidate and comparison
  directories are intentionally local and untracked, so use the explicit
  named gates above.
- When compositing generated variants back onto an existing image to reduce
  diff size, prefer visual continuity over exact pixel alignment. Do not force
  warps, masks, or patch seams that truncate or visually disconnect limbs,
  shoes, hands, hair, or props. If a low-diff composite starts to break anatomy
  or object continuity, keep a larger generated region, regenerate, or document
  the deviation instead of hiding it.
- Keep generated folders out of git unless the user explicitly asks to commit a
  final deliverable.

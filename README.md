# Akari Visual Reference Materials

This repository contains Akari visual-reference materials, source manifests,
audit scripts, and rendered deliverables. Akari v1.2.0 Natural Form is the
primary settings release; Akari v1.1 remains available as inheritance and
history material.

The public repository is maintained as `TKPND/akari-design`.

## Contents

- `source/` contains public source manifests, palette data, and compressed WebP
  image derivatives.
- `akari-v1.2/` contains the Natural Form package, accepted Core images,
  lifecycle manifests, documentation, and release deliverables.
- `akari-v1.4/` contains the in-progress style baseline, reproducibility tests,
  and user-selected G–J authority chain.
- `tools/pdf/` contains the Node/Playwright PDF rendering code.
- `scripts/` contains Python build and audit scripts.
- `dist/` contains prebuilt PDF deliverables and public contact sheets.
- `evidence/` contains review evidence used during the finishing pass.

The raster image assets in this public snapshot are WebP derivatives encoded
with high-quality lossy `cwebp` settings. Private working originals are not
included in this repository history.

## Common Commands

```bash
npm ci
npm run lint:md
npm run test:node
npm run test:python
npm run gate:edit:d02
npm run gate:integration:v1-2
npm run gate:integration:all
npm run release:v1-2
npm run gate:release:v1-2
npm run audit
npm run audit:tonari:pdf
```

The named gates run serially for the repository's 3-core, 2 GiB VPS workflow.
Daily work uses the edit or integration gate; full raster/OCR remains a formal
release responsibility.

## Deliverables

- `akari-v1.2/release/akari-v1.2-core-settings.pdf` — default settings PDF
- `akari-v1.2/release/checksums.txt`
- `dist/akari-v1.1-settings.pdf`
- `dist/akari-v1.1-situation-daybook.pdf`
- `dist/akari-v1.1-tonari-no-akari.pdf`
- `dist/akari-v1.1-tonari-no-hyoujou.md`

## Notes

Inter font files are included under their SIL Open Font License files in
`source/fonts/`.

No general project license is granted unless a top-level license is added.

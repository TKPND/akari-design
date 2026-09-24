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
- `akari-v1.5/` contains the first v1.5 body-balance checkpoint, with the
  user-selected B3 baseline and its labeled comparison sheet.
- `akari-v3.0/` preserves the original black-bob P1/P2/P6 references and
  selected situations.
- [Akari v3.1](akari-v3.1/README.md) uses separate U1 upper-body and L1
  lower-body references, an M2 assembled overview, a silver pin and grey socks.
  Its [soft sock material](akari-v3.1/sock-material-requirement.json) is a MUST
  wherever socks are visible; poses and actions can vary.
  Its [selected A/B/C scenes](akari-v3.1/situations/abc-exploration/README.md)
  preserve 18 everyday illustrations in the user-selected long-sleeve uniform.
  A16 uses the selected E1-1 finish, which subtly groups small clothing shadows.
- [Akari v3.2](akari-v3.2/README.md) preserves the earlier light pop direction: the
  selected B2 face, G1 soda-blue gingham outfit, and four accepted scenes.
  The [weekend walk](akari-v3.2/situations/weekend-walk/README.md) follows a
  small shop, a breezy tree-lined path, and the evening walk home.
  Use its native face and body images with separate reference roles.
- [Akari V4.0](akari-v4.0/README.md) is the current visual direction: the
  selected V11 face and pastel rendering, B06 full-body balance, and four
  outfit/scene examples. Use V11 and B06 as separate native references;
  clothing and scenes can vary.
- `tools/pdf/` contains the Node/Playwright PDF rendering code.
- `scripts/` contains Python build and audit scripts.
- `skills/` preserves reusable Codex skills, including their instructions,
  helper scripts, and tests.
- `dist/` contains prebuilt PDF deliverables and public contact sheets.
- `evidence/` contains review evidence used during the finishing pass.

The older settings-release raster assets are WebP derivatives encoded with
high-quality lossy `cwebp` settings. Their private working originals are not
included. Selected v3.0/v3.1/v3.2/v4.0 working references are preserved as native PNGs.

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

## Reusable Skills

[akari-hires-composite](skills/akari-hires-composite/SKILL.md) provides regional
generation and compositing guidance for high-resolution Akari wallpapers and
portraits, with explicit reference roles and same-coordinate comparisons.
Its helper requires Python 3 and ImageMagick 7.

To install or restore the versioned copy, run from the repository root:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/akari-hires-composite "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 skills/akari-hires-composite/scripts/test_compose.py -q
```

This replaces matching files in the installed skill with the repository copy.
Invoke it with `$akari-hires-composite`. Future changes should be preserved in
this repository as well as the installed copy.

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

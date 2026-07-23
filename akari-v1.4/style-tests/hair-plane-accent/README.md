# Akari v1.4 — E: Localized Hair-Plane Accent Test

## Decision carried into E

- Practical base: D2
- Direction reference: D3
- Goal: transfer only D3's bolder crown and upper light-side hair planes into
  D2 without importing D3's broader color or rendering drift.

## Inputs

- Edit target:
  `../paint-planes-hybrid/akari-v14-d2-hair-clothes-medium.png`
- Direction reference:
  `../paint-planes-hybrid/akari-v14-d3-hair-clothes-strong.png`

Image 1 was the edit target. Image 2 was used only as a direction reference for
the scale and decisiveness of contiguous hair light, midtone, and shadow masses.

## Fixed invariants

- Character identity, apparent age, face shape, expression, pose, and framing
- B1 face rendering and A2 eye highlights
- A3 line-pressure variation, selective broken lines, and sparse redraw lines
- Hair silhouette, strand geometry, bangs below the eyebrow line, flyaways,
  crossed blue pins, and blue bow
- T-shirt, shorts, garment folds, body, hands, skin, and lighting direction
- Bed, curtain, wall, scene palette, and background
- No grain, paper texture, bloom, chromatic aberration, text, watermark, or
  added objects

## Variants

All variants were independently edited from D2.

| Variant | Permitted change | File |
| --- | --- | --- |
| E1 | Minimal consolidation of crown and upper light-side hair planes | `akari-v14-e1-subtle-hair-accent.png` |
| E2 | Balanced consolidation into fewer, larger hand-painted planes | `akari-v14-e2-balanced-hair-accent.png` |
| E3 | Strong upper-bound test with decisive contiguous planes | `akari-v14-e3-strong-hair-accent.png` |

## Comparison and QA

`akari-v14-e-hair-accent-comparison.png` shows D2, E1, E2, and E3 at full-frame
scale and with the same head crop.

All three outputs are 1024 × 1536 sRGB PNG files. Visual QA found no obvious
identity, pose, clothing, accessory, or scene drift. Fine anti-aliasing and
brush-edge micro-variation remain outside the target zone, as expected from a
generative image edit.

## User selection

**E2 is formally accepted** for its balanced crown and upper-hair plane accent.

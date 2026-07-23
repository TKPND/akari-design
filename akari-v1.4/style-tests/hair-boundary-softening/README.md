# Akari v1.4 — F: Hair-Boundary Softening

## Decision carried into F

- Accepted visual base: E2
- Accepted line treatment: A3
- Accepted face rendering: B1
- Accepted eye highlights: A2
- Accepted hair-and-clothing plane treatment: D2 plus the E2 crown accent
- Default grain, paper texture, and bloom: off

Before varying the hair boundary, F0 corrects an accessory drift in E2. E2 had
shifted toward parallel blue bars plus a broad filled cloth bow. The v1.1
identity reference instead uses one compact ornament on character-left
(screen-right in this scene): pale-blue crossed straight pins above a delicate
thin cord/ribbon bow with narrow outlined loops and two slim tails.

## Inputs

- Visual base:
  `../hair-plane-accent/akari-v14-e2-balanced-hair-accent.png`
- Ornament reference:
  the supplied v1.1 sample and
  `../../references/v1.1/v1_1_髪飾り側_45deg.png`
- Common F edit base:
  `akari-v14-f0-canonical-ornament.png`

F0 is a targeted ornament correction only. F1, F2, and F3 were then edited
independently from F0.

## Fixed invariants

- Adult 25-year-old Akari identity, face, age impression, and expression
- B1 face rendering and A2 amber-eye highlights
- A3 line-pressure variation, selective broken lines, and sparse redraw lines
- Hair silhouette, bangs, strand geometry, flyaways, and established large
  light/midtone/shadow planes
- Canonical character-left ornament: crossed pale-blue pins plus a thin
  cord/ribbon bow with narrow loops and two slim tails
- Pose, body, hands, skin, white T-shirt, blue shorts, and clothing folds
- Bed, curtain, wall, background objects, framing, lighting direction, shadow
  placement, and color temperature
- No blur filter, airbrush smoothing, global gradient, grain, paper texture,
  bloom, text, border, watermark, or added objects

## Permitted edit

Only the hard diagonal boundary immediately to screen-right of the crown part,
above the forehead and continuing into the upper ornament-side hair, may
change. The large hair-plane shapes and tonal values must remain readable.

| Variant | Permitted boundary treatment | File |
| --- | --- | --- |
| F0 | Canonical ornament correction; hair boundary unchanged | `akari-v14-f0-canonical-ornament.png` |
| F1 | A few tiny edge interruptions and tonal bridges | `akari-v14-f1-subtle-boundary.png` |
| F2 | Moderately broken hand-painted edge with restrained midtone bridges | `akari-v14-f2-balanced-boundary.png` |
| F3 | Upper-bound test with broader lost-and-found sections and midtone steps | `akari-v14-f3-strong-boundary.png` |

## Comparison and QA

`akari-v14-f-boundary-comparison.png` shows F0, F1, F2, and F3 at full-frame
scale and with the same head crop.

All four source images are 1024 × 1536, 8-bit sRGB PNG files. Visual QA found no
material drift in age, expression, pose, hands, clothing, setting, or lighting.
All variants retain the corrected v1.1 ornament topology and side placement.

Independent style and preservation reviews both ranked the candidates
`F2 > F1 > F3`:

- F1 is safe but too close to F0; the hard boundary remains conspicuous.
- F2 removes the cut-paper hardness while preserving the two large hair planes.
- F3 spreads the transition into a broader tonal ramp and slightly softens
  outer wisps and bang/eye microdetail.

## User selection

**F2 is formally accepted** for removing the cut-paper boundary while retaining
the large hair planes and corrected canonical ornament.

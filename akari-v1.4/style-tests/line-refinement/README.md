# Akari v1.4 — G line-refinement comparison

Date: 2026-07-23

## Purpose

Test whether the roughness accumulated in the accepted F2 image can be reduced
without weakening the accepted paint-plane treatment.

The main defect is not uniformly thick linework. It is the accumulation of
short scratch-like fragments, broken retracing marks, repeated contours, and
interior lines that compete with the outer silhouette and painted plane
boundaries.

## Shared base and reference

- Edit base for every variant:
  `../hair-boundary-softening/akari-v14-f2-balanced-boundary.png`
- Direction reference: the user's re-posted v1.1 sample.
- Reference characteristics used in the prompts:
  - long, thin, deliberate outer strokes;
  - sparse, lower-contrast interior lines;
  - no uniform vector-like smoothing;
  - hand-drawn life retained through selected strokes rather than duplicate
    or broken marks.

The v1.1 attachment was used to define the comparison before generation, but
the image-edit tool could only receive F2 as the direct image input. Its line
characteristics were therefore carried into all three edit prompts as explicit
constraints.

## Shared invariants

Change linework only on:

- hair;
- T-shirt;
- shorts;
- hands;
- foreground bedding.

Keep unchanged:

- identity, face, eyes, expression, anatomy, pose, and proportions;
- hairstyle shape and overall silhouette;
- canonical crossed blue pins plus the thin blue cord bow;
- clothing shapes;
- all accepted paint planes, colors, and lighting;
- composition, wall, curtain, bed, and background texture;
- the balanced F2 hair-plane boundary.

Forbidden:

- global blur, smoothing, or antialiasing passes;
- thick or vector-like outlines;
- repainting or flattening accepted color planes;
- added detail, restyling, grain, or bloom.

## Variants

### G1 — minimal duplicate cleanup

Remove only clearly accidental double contours, tiny scratch-like fragments,
and broken retracing lines. Preserve intentional contour, construction, hair,
and fold lines. This is the continuity-first option.

File: `akari-v14-g1-clean-duplicates.png`

### G2 — balanced line hierarchy

Apply G1 cleanup, reduce interior-line density by about 30%, consolidate
remaining marks into longer single strokes, and keep interior lines quieter
than outer contours. Preserve enough hair and fabric structure to retain form.

File: `akari-v14-g2-balanced-lines.png`

### G3 — strong sparse-line upper bound

Remove most nonessential interior hair, garment, and bedding lines. Keep only
the strongest form-defining strokes as thin, long, low-contrast marks. This is
an upper-bound test rather than a continuity-first candidate.

File: `akari-v14-g3-sparse-lines.png`

## Generation

- Built-in image editing.
- Each variant was generated independently from F2.
- Output: 1024 × 1536 RGB PNG.
- No variant was generated from another G variant.

## Pixel-difference reference

Normalized RMSE against F2 is included only as a drift indicator. It does not
measure artistic quality.

| Variant | Whole image | Background crop | Face crop |
| --- | ---: | ---: | ---: |
| G1 | 0.0324472 | 0.0163968 | 0.0460377 |
| G2 | 0.0425784 | 0.0223587 | 0.0564747 |
| G3 | 0.0507451 | 0.0222323 | 0.0709732 |

G1 is quantitatively closest to F2. G3 has the largest total and facial-region
change, consistent with the stronger re-render required for its sparse-line
upper-bound treatment.

## Review

Two separate reviews were used:

- line-quality fit: `G2 > G1 > G3`;
- preservation safety: `G1 > G2 > G3`.

G1 preserves F2 most closely but leaves some remaining chatter around the
lower hair tips, right shoulder and sleeve, shorts waist, and bedding. G2
removes enough of that chatter to establish a clearer hierarchy while
retaining the hand-drawn character. Its trade-off is mild re-render drift in
the outer hair wisps and micro-variation of adjacent painted areas. G3 removes
too much hair, fabric, hand, and bedding structure and begins to resemble a
partial redesign.

## User selection

**G2 is formally accepted** as the v1.4 authority for line hierarchy, large
paint planes, palette, and clean finish. G1 remains the conservative comparison;
G3 is not promoted.

## Files

- `akari-v14-g1-clean-duplicates.png`
- `akari-v14-g2-balanced-lines.png`
- `akari-v14-g3-sparse-lines.png`
- `akari-v14-g-line-comparison.png`

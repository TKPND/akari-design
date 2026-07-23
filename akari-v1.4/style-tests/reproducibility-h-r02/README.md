# Akari v1.4 — H-r02 composition retry

Date: 2026-07-23

## Purpose

Retry the failed H standing reproducibility test while changing only its
composition control. The G2 references, wardrobe, identity, lighting,
rendering contract, and three-independent-generation method remain unchanged.

The original H test failed systematically because all three samples enlarged
the figure to about 89–91%, crossed the legs, and lifted the rear heel. H-r02
removes the phrases that encouraged one-leg weight and a forward half-step,
then explicitly requires:

- hair top near 12% and both sole lines near 84% of canvas height;
- quiet floor visible below both feet;
- feet laterally separated by about one foot width;
- weight shared between both feet;
- both soles fully flat;
- uncrossed knees and ankles;
- neither foot crossing the body centerline.

The exact shared generation prompt is in `PROMPT.md`.

## Reference authority

1. `../line-refinement/akari-v14-g2-balanced-lines.png`
   controls the v1.4 face, apparent age, amber eyes, short-bob silhouette,
   canonical ornament, large paint planes, line hierarchy, warm skin, and
   grain/bloom-free finish.
2. `../../references/v1.1/v1_1_front_2.png`
   controls full-body proportions, healthy leg volume, joint continuity, and
   neutral standing anatomy only. Its socks, gray shorts, older rendering, and
   near-frame-filling composition are not authoritative.
3. `../../references/v1.1/v1_1_髪飾り側_45deg.png`
   controls the character-left placement and topology of the pale-blue crossed
   pins plus thin cord bow only. Its clothing, shoes, older rendering, and
   composition are not authoritative.

## Generation

- Built-in image generation.
- H-r02-1, H-r02-2, and H-r02-3 were generated independently.
- Every sample used the exact same `PROMPT.md` and the same three references in
  the same order.
- No H or H-r02 output was used as a reference for another output.
- No retry was made inside a sample.
- All outputs are 1024 × 1536, 8-bit RGB/sRGB PNG files.

## Composition, body, and production review

Percentages are estimated from the original-size canvases. FW means the
rendered width of one foot at floor level.

| Gate | H-r02-1 | H-r02-2 | H-r02-3 |
| --- | --- | --- | --- |
| Hair top, target ≈12% | ≈3.9% — Fail | ≈4.2% — Fail | ≈3.7% — Fail |
| Lowest sole line, target ≈84% | ≈96.7% — Fail | ≈96.2% — Fail | ≈95.1% — Fail |
| Figure height, target ≈72% | ≈92.8% — Fail | ≈92.0% — Fail | ≈91.4% — Fail |
| Lateral foot gap, target ≈1 FW | ≈1.2 FW — Pass | ≈0.8 FW — Pass | ≈1.0 FW — Pass |
| Both soles and heels grounded | Pass | Pass | Pass |
| Knees and ankles uncrossed | Pass | Pass | Pass |
| Neither foot crosses centerline | Pass | Pass | Pass |
| Hands and feet complete | Pass | Pass | Pass |
| Ornament-side three-quarter view | Marginal pass | Marginal pass | Marginal pass |
| Forbidden objects absent | Pass | Pass | Pass |
| Dimensions and mode | Pass | Pass | Pass |

The stance repair works: all three samples remove the model-leg crossing,
tiptoe, and weak rear-foot contact seen in H. The framing repair does not work:
all three remain nearly frame-filling and leave too little floor below the
feet.

## Style, identity, ornament, and eye review

Scale: 5 is closest to G2. A clean-finish score of 5 means the sample remains
free of grain and bloom.

| Sample | Paint planes | Line hierarchy | Hair | Fabric | Face/eyes | Clean finish | Adult age | Ornament | Style result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| H-r02-1 | 4 | 4 | 4 | 3 | 4 | 5 | Pass | Pass | Pass |
| H-r02-2 | 4 | 4 | 4 | 3 | 3 | 5 | Pass | Pass | Pass |
| H-r02-3 | 3 | 3 | 4 | 2 | 3 | 5 | Pass, youngest read | Pass | Fail |

Style ranking: **H-r02-1 > H-r02-2 > H-r02-3**.

- H-r02-1 is closest overall to G2. Its eye treatment is a hybrid that leans
  toward H3's clearer shape, while the shorts add a localized high-contrast
  fold burst.
- H-r02-2 gives the strongest mid-20s impression and the calmest overall
  balance. Its softer, narrower eye treatment is closest to the original H2.
- H-r02-3 most clearly reproduces the original H3's more open, sharply defined,
  cute eye shape. Its shirt and shorts also reproduce H3's unwanted angular,
  repeated fold facets, and the face reads younger than the other two.

All three keep the canonical character-left crossed pins and thin cord bow.
The topology is most compressed in H-r02-3 but remains recognizable.

Style-only result: two of three pass.

## User preference note

The preferred overall balance in the original H set is H2, while the preferred
eye shape is H3 because its eyes are clearer and carry more immediate charm.
H-r02 repeats that split: H-r02-2 is the calmer adult balance, while H-r02-3
has the clearest H3-like eyes. The eye preference is recorded for a later
single-axis eye study and is not mixed into the H-r02 composition retry.

## Result

Overall H-r02 result: **fail**.

The test requires at least two of three samples to meet every controlling
gate. Zero of three meet the framing gate, even though all three meet the
repaired stance and grounding gates and two of three meet the scoped G2 style
gate.

## Recommended H-r03 axis

Keep the H-r02 prompt, G2 style authority, identity, wardrobe, lighting, and
neutral-foot rules unchanged. Replace only the near-frame-filling anatomy
reference with a composition-normalized derivative whose figure is scaled to
about 72% and placed from roughly 12% to 84% of a 2:3 canvas.

This recommendation is an inference from the repeated result: the numerical
framing language changed, but the almost full-height v1.1 anatomy reference
did not, and all three outputs continued to reproduce its near-frame-filling
scale. A normalized anatomy reference would test that hypothesis without
altering the accepted visual style.

Do not add the H3-like eye preference to H-r03. Test it separately after the
standing composition passes.

## Files

- `akari-v14-h-r02-1-standing-repro.png`
- `akari-v14-h-r02-2-standing-repro.png`
- `akari-v14-h-r02-3-standing-repro.png`
- `akari-v14-h-r02-comparison.png`
- `akari-v14-h-r02-eye-comparison.png`
- `PROMPT.md`

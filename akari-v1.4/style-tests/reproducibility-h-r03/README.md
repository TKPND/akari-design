# Akari v1.4 — H-r03 normalized-reference retry

Date: 2026-07-23

## Decision carried into H-r03

The user selected **H-r02-1** as the preferred H-r02 result. That preference is
recorded as the visual comparison point, but H-r02-1 is not used as a
generation reference. H-r03 continues to use G2 as the primary visual
authority so that standing outputs do not chain-reference one another.

H-r03 tests one causal hypothesis: the near-frame-filling
`../../references/v1.1/v1_1_front_2.png` anatomy reference overrode the
numerical 72% framing instructions in H-r02.

## Single controlled change

Only Image 2 was replaced.

- H-r02 Image 2:
  `../../references/v1.1/v1_1_front_2.png`, whose detected figure bbox was
  approximately
  `468 × 1456 +278 +39`.
- H-r03 Image 2:
  `references/v1_1_front_2-normalized-72pct.png`.

The derivative was made mechanically without repainting:

1. trim the near-white outer canvas from the source;
2. scale the retained source pixels to `356 × 1106`;
3. place them at `+334 +184` on a white `1024 × 1536` canvas.

The resulting figure bbox is exactly `356 × 1106 +334 +184`: hair top at
12.0%, lowest sole at 84.0%, and figure height 72.0%.

The source file was not modified.

## Fixed conditions

- Prompt: byte-identical copy of the H-r02 `PROMPT.md`
  (`SHA-256 29006f527c4bdb162fa140356b6d01720e21a368a29b84042e5af19eaf79cc44`).
- Image 1:
  `../line-refinement/akari-v14-g2-balanced-lines.png`, controlling face,
  apparent age, amber eyes, short-bob silhouette, canonical ornament, paint
  planes, line hierarchy, warm skin, and clean finish.
- Image 2:
  `references/v1_1_front_2-normalized-72pct.png`, controlling full-body
  proportions, neutral standing anatomy, and the normalized 72% composition.
- Image 3:
  `../../references/v1.1/v1_1_髪飾り側_45deg.png`,
  controlling ornament-side placement and topology.
- White T-shirt, pale-blue lounge shorts, bare legs and feet.
- Warm frame-left daylight, warm-gray wall, pale matte floor.
- Neutral separated stance, both soles flat, no crossed knees or ankles.
- No H3-like eye preference was added.

## Generation

- Built-in image generation.
- H-r03-1, H-r03-2, and H-r03-3 were generated independently.
- Every sample used the exact same `PROMPT.md` and the same three references in
  the same order.
- Each sample used one generation call with no retry.
- No H, H-r02, or H-r03 output was used as a reference for another output.
- All outputs are `1024 × 1536`, 8-bit RGB/sRGB PNG files.

## Composition, body, and production review

Measurements are from the original-size canvases and are estimated within
approximately two pixels. FW means one rendered foot width at floor level.

| Gate | H-r03-1 | H-r03-2 | H-r03-3 |
| --- | --- | --- | --- |
| Hair top, target ≈12% | y≈91 / 5.9% — Fail | y≈75 / 4.9% — Fail | y≈77 / 5.0% — Fail |
| Lowest sole, target ≈84% | y≈1436 / 93.5% — Fail | y≈1468 / 95.6% — Fail | y≈1463 / 95.2% — Fail |
| Figure height, formal gate 68–72% | ≈87.6% — Fail | ≈90.7% — Fail | ≈90.2% — Fail |
| Lateral foot gap, target ≈1 FW | ≈0.9 FW — Pass | ≈1.2 FW — Pass | ≈1.0 FW — Pass |
| Both soles and heels grounded | Pass | Pass | Pass |
| Knees and ankles uncrossed | Pass | Pass | Pass |
| Neither foot crosses centerline | Pass | Pass | Pass |
| Hands and feet complete | Pass | Pass | Pass |
| Ornament-side three-quarter view | Marginal pass | Marginal pass | Marginal pass |
| Forbidden objects absent | Pass | Pass | Pass |
| Dimensions and mode | Pass | Pass | Pass |

The H-r02 stance repair remains stable in all three samples. The normalized
front anatomy reference produces only a modest framing improvement in
H-r03-1; none of the samples reaches the formal framing gate.

## Style, identity, ornament, and eye review

Scale: 5 is closest to G2. A clean-finish score of 5 means no visible grain or
bloom.

| Sample | Paint planes | Line hierarchy | Hair | Fabric | Face/eyes | Clean finish | Adult age | Ornament | Style result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| H-r03-1 | 5 | 5 | 5 | 5 | 4 | 4 | Borderline pass | Pass | Pass |
| H-r03-2 | 3 | 4 | 4 | 3 | 4 | 5 | Marginal, youngest read | Pass | Fail |
| H-r03-3 | 4 | 5 | 4 | 4 | 5 | 5 | Pass | Pass | Pass |

Style ranking: **H-r03-1 > H-r03-3 > H-r03-2**.

- H-r03-1 is closest overall to G2 and is the strongest continuation of the
  user-preferred H-r02-1 direction. Its eyes are slightly clearer than
  H-r02-1, while the hair and folds retain more chatter than H-r03-3.
- H-r03-2 is polished but flatter and more airbrushed in the skin and fabric;
  its face also reads youngest.
- H-r03-3 has the clearest complete ornament, the strongest mid-20s balance,
  and the clearest/cutest H3-like eyes. Its hair and fabric planes are smoother
  than G2.

Style-only result: two of three pass.

## Result

Overall H-r03 result: **fail**.

The test requires at least two of three samples to meet every controlling
gate. Zero of three meet the 68–72% figure-height gate, even though all three
retain the repaired stance and two of three pass the scoped G2 style gate.

## Causal update

Normalizing only the front anatomy reference does not normalize the output
composition. It weakens the claim that Image 2 alone caused the enlargement,
but it does not disprove reference-driven framing.

The unchanged ornament-side Image 3 is itself approximately 89.7% tall, from
about 3.0% to 92.7% of its canvas. That closely matches the H-r03 outputs at
87.6–90.7%. It is also the only unchanged full-body reference that already
shows the requested ornament-side three-quarter view. The model therefore
appears to use its pixel-level framing despite the prompt limiting it to
ornament topology. G2's close, frame-filling composition may reinforce the
same enlargement.

See `akari-v14-h-r03-reference-scale-comparison.png`.

## User selection

**H-r03-1 is formally accepted** as the v1.4 standing and adult-face authority.
Its larger figure presence is accepted as part of this composition. The
proposed H-r04 mechanical reduction was cancelled, so the failed 68–72%
framing gate is retained here as test history rather than a continuing
production requirement.

## Files

- `akari-v14-h-r03-1-standing-repro.png`
- `akari-v14-h-r03-2-standing-repro.png`
- `akari-v14-h-r03-3-standing-repro.png`
- `akari-v14-h-r03-comparison.png`
- `akari-v14-h-r03-reference-scale-comparison.png`
- `references/v1_1_front_2-normalized-72pct.png`
- `PROMPT.md`

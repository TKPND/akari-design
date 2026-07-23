# Akari v1.4 — H reproducibility test

Date: 2026-07-23

## Purpose

Test whether the accepted v1.4 G2 visual baseline can be reproduced in a new
composition without inheriting the original bed pose or relying on iterative
editing of the same image.

H1, H2, and H3 are three independent generations from the same prompt and the
same reference set. They are not generated from one another. The test changes
camera distance and pose while keeping wardrobe, viewpoint, lighting, setting,
and all identity/style requirements fixed.

## Reference authority

1. `../line-refinement/akari-v14-g2-balanced-lines.png`
   controls the v1.4 face, apparent age, amber eyes, short-bob silhouette,
   canonical ornament, large hair and clothing paint planes, line hierarchy,
   warm skin, and grain/bloom-free finish.
2. `../../references/v1.1/v1_1_front_2.png`
   controls full-body proportions, healthy leg volume, joint continuity, and
   the neutral standing body only. Its socks, gray shorts, older rendering,
   and microdetails are not authoritative.
3. `../../references/v1.1/v1_1_髪飾り側_45deg.png`
   controls the anatomical character-left placement and topology of the pale
   blue crossed pins plus the thin cord bow only. Its hoodie, skirt, shoes, and
   older rendering are not authoritative.

## Fixed composition

- Portrait 2:3, exactly 1024 × 1536 PNG.
- Eye-level, three-quarter front view from the ornament side.
- Head-to-toe standing figure at about 68–72% of frame height.
- Relaxed grounded weight on one leg; the other bare foot rests a small
  half-step forward.
- Both arms hang naturally with both hands separated from the torso and
  readable.
- Gaze sits just beside the camera, with a quiet familiar closed-mouth smile.
- Simple apartment interior: one warm-gray wall and a pale matte floor only.
- Warm directional daylight enters from frame-left without a visible window or
  curtain.

## Fixed wardrobe and identity

- One 25-year-old Akari.
- Loose opaque white short-sleeved T-shirt.
- Pale-blue lounge shorts with a restrained drawstring.
- Bare legs and bare feet; no socks or shoes.
- Warm chestnut airy short bob with the G2 silhouette and restrained flyaways.
- One complete character-left ornament: two pale-blue straight pins crossing
  above one delicate thin cord bow with narrow loops and two slim tails.
- Large structured amber eyes with G2 highlights and adult facial balance.

## Rendering contract

- Preserve G2's large, readable light/midtone/shadow paint planes.
- Keep thin, deliberate outer strokes and sparse lower-contrast interior
  strokes.
- Do not restore scratch-like fragments, repeated contours, or equally dark
  internal fold lines.
- Full-body distance may simplify microdetail, but may not flatten the hair,
  eyes, skin, or garment form.
- No grain, paper texture, bloom, chromatic aberration, lens flare, heavy
  bokeh, airbrush haze, or global smoothing.

## Prohibitions

- No bed, sofa, rug-rest pose, table, plant, books, mail, bag, phone, food,
  drink, refrigerator, laundry, charger, shelf reach, rain, umbrella, doorway,
  or visible window/curtain.
- No text, logo, watermark, border, collage, grid, split screen, or additional
  character.
- No long hair, compact v1.2 bob, childlike face/body drift, missing,
  duplicated, mirrored, parallel-only, or broad-cloth ornament.
- No extreme wide angle, low angle, fashion pose, sexualized framing, pinched
  ankles, uniformly thin legs, broken hands, fused fingers, floating feet, or
  cropped head/hands/feet.

## Generation prompt

Use case: style-transfer

Asset type: Akari v1.4 H reproducibility test

Primary request: Create a new full-body illustration of the same 25-year-old
Akari in the fixed neutral standing composition. Do not edit or reproduce the
bed scene. Generate one independent sample from the shared references.

Input images:

- Image 1 is the primary v1.4 visual authority for face, age, hair, eyes,
  ornament, paint planes, line hierarchy, skin, and finish.
- Image 2 is a supporting reference for full-body proportions and grounded
  standing anatomy only.
- Image 3 is a supporting reference for the character-left ornament topology
  and three-quarter anatomical placement only.

Scene/backdrop: A quiet minimal apartment interior containing only one
warm-gray wall and a pale matte floor.

Subject: One adult Akari wearing a loose opaque white short-sleeved T-shirt and
pale-blue lounge shorts with a restrained drawstring, bare legs, and bare
feet.

Style/medium: Polished Japanese character illustration matching Image 1:
soft pastel cel shading organized into large readable planes, warm translucent
skin, structured glossy chestnut hair, jewel-like amber eyes, thin deliberate
outer strokes, and sparse lower-contrast interior strokes.

Composition/framing: Portrait 2:3, exact 1024 × 1536. Eye-level three-quarter
front view from the ornament side. Show the complete head-to-toe figure at
about 68–72% frame height. Relaxed grounded weight on one leg, other bare foot
a small half-step forward, both arms hanging naturally, both hands clear and
separated from the torso.

Expression: Quiet familiar closed-mouth smile, gaze just beside the camera,
adult and relaxed rather than posed or childlike.

Lighting/mood: Warm directional daylight from frame-left, similar in direction
and plane readability to Image 1, with restrained floor bounce. No visible
light source.

Constraints: Preserve the Image 1 short-bob silhouette and G2 rendering. One
complete character-left ornament: two pale-blue straight pins crossing above
one delicate thin cord bow with narrow loops and two slim tails. Preserve
healthy thigh and calf volume, coherent joints, complete hands and feet, and
credible floor contact. Keep line hierarchy quiet and paint planes clear.

Avoid: Every item in the Prohibitions section above. No added objects.

## Acceptance gates

Review H1, H2, and H3 independently in this order:

1. identity and adult age impression;
2. ornament topology and anatomical side;
3. hair silhouette and amber-eye structure;
4. roomwear accuracy;
5. body volume, joint continuity, hands, feet, and floor contact;
6. G2 paint-plane organization;
7. G2 line hierarchy without renewed chatter or vector smoothing;
8. exact dimensions, RGB/sRGB PNG, and forbidden-element absence.

The H test passes only if at least two of three samples meet every controlling
gate without a major identity, ornament, body, or rendering drift.

## Files

- `akari-v14-h1-standing-repro.png`
- `akari-v14-h2-standing-repro.png`
- `akari-v14-h3-standing-repro.png`
- `akari-v14-h-repro-comparison.png`

## Generation

- Built-in image generation using the same three local references for every
  sample.
- H1, H2, and H3 were generated independently from the exact shared prompt.
- No H image was used as a reference for another H image.
- All three outputs are 1024 × 1536, 8-bit RGB/sRGB PNG files.

## Review

### Style fidelity

Scale: 5 is closest to G2. A grain/bloom score of 5 means the image remains
clean.

| Sample | Paint planes | Line hierarchy | Hair | Fabric | Face/eyes | Grain/bloom |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| H1 | 4 | 4 | 4 | 4 | 4 | 5 |
| H2 | 4 | 4 | 4 | 3 | 3 | 5 |
| H3 | 3 | 3 | 4 | 2 | 3 | 5 |

H1 transfers G2 most cleanly. H2 remains inside the accepted line and paint
direction but makes the shorts glossier and simplifies some eye depth. H3
fragments the T-shirt and shorts into busier high-contrast folds and no longer
meets the G2 fabric/line gate. All three keep the clean grain- and bloom-free
finish.

Style-only result: H1 and H2 pass, so the two-of-three style criterion passes
narrowly.

### Identity, body, and production gates

| Gate | H1 | H2 | H3 |
| --- | --- | --- | --- |
| Identity and adult age | Pass | Pass | Pass |
| Canonical character-left ornament | Pass | Pass | Pass |
| Hair silhouette | Pass | Pass | Pass |
| Roomwear | Pass | Pass | Pass |
| Hands and joint continuity | Pass | Pass | Pass |
| Healthy leg volume | Pass | Pass | Pass |
| 68–72% figure height | Fail | Fail | Fail |
| Neutral uncrossed half-step | Fail | Fail | Fail |
| Both feet fully grounded | Fail | Fail | Fail |
| Forbidden objects absent | Pass | Pass | Pass |
| Dimensions and mode | Pass | Pass | Pass |

The repeated failures are systematic:

- all three figures occupy about 89–91% of frame height;
- all three cross the legs into a mild fashion/model stance;
- all three raise or point the rear foot instead of grounding both soles.

Overall H result: **fail**. Zero of three images meet every controlling gate,
even though H1 and H2 demonstrate that the G2 visual treatment itself is
transferable.

## Recommended r02 axis

Keep the H references, wardrobe, identity, lighting, and rendering prompt
unchanged. Change composition control only:

- figure top at roughly 12% of canvas height and sole line at roughly 84%;
- leave visible quiet floor below both feet;
- keep the feet laterally separated by about one foot width;
- both soles fully flat, knees uncrossed, and neither foot placed across the
  body centerline;
- remove the phrase “other bare foot a small half-step forward,” which was
  consistently interpreted as a fashion pose.

Do not change the G2 style prompt in r02. H3's fabric drift is useful variance,
but the style side already produced two passing samples; mixing a style repair
into the composition retry would make the result harder to attribute.

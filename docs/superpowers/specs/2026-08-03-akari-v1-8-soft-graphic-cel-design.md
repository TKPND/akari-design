# Akari v1.8 Soft Graphic Cel Design

Status: approved for implementation planning.

Date: 2026-08-03.

## Outcome

Akari v1.8 begins with one bounded rendering study, `V18-01 Soft Graphic Cel
Strength Study`. It translates the accepted v1.7 Akari into a softer graphic
cel-rendering language without redesigning the character.

The first checkpoint compares three independently generated full-body images
at the same camera, pose, outfit, room, and warm lighting as the accepted
V17-01 front image. The candidates differ only in the strength of the rendering
translation. They remain local review artifacts until the user explicitly
selects one.

This checkpoint is not a new pose, wardrobe, background, turnaround, manifest
workflow, PDF, or release package.

## Approved Decisions

| Decision | Approved direction |
| --- | --- |
| Change scope | Rendering language only |
| Style center | Soft graphic cel |
| First asset | Same-condition full-body comparison |
| Background | Preserve the V17-01 apartment |
| Prototype method | Independent gentle, balanced, and graphic candidates |
| Promotion | Only after explicit user selection |

## Authority and Reference Roles

Reference authority is role-specific. A style reference cannot grant identity,
age, anatomy, hair, ornament, clothing, pose, or room authority.

### Positive Character Authority

- `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`
  - SHA-256:
    `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`;
  - sole generation authority for identity, age-25 reading, face, eye scale,
    amber eye color, hair, ornament, body balance, expression, pose, outfit,
    framing, apartment, and warm light.
- `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
  - SHA-256:
    `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`;
  - body-balance review reference only; it does not replace V17-01 as the
    generation authority.

The accepted v1.7 30-degree and 45-degree images remain angle-continuity
authorities but are not required inputs for this fixed front-view study.

### User-Supplied Style References

The user supplied four JPEG images for visual analysis. They are not committed
project assets in this design pass.

| File | Dimensions | SHA-256 | V18-01 role |
| --- | --- | --- | --- |
| `G6f1r23aIAANle8.jpg` | 1776 x 2624 | `765a3832f8543445ff099b3a0d22052c7860bf03a6f8e0ebca64ebb1cea7c54a` | Primary reference for fine colored linework, soft two-to-three-step cel shading, and polished finish |
| `HOvzZrzboAA3IDA.jpg` | 1536 x 2304 | `526c47317339db5e9fa087ac0d31a796a20e6d386e2881c9197bd05b9628dd14` | Secondary reference for clear contour hierarchy, matte cloth, restrained highlights, and clean shape grouping |
| `G-T4x1na8AAgfbo.jpg` | 1184 x 1752 | `bdbe3085b83989baa62d4f4c50fc980216387c94115e7237f6d4e70f1161d42b` | Context only; its high saturation, dynamic pose, and graphic background are outside the first study |
| `HNYSfB1aMAAkqZG.jpg` | 1472 x 2176 | `83753f1a1575c047620dc295474cc534694b4b4307a4005f985b39cb887170b5` | Context only; its heavy deformation, sticker outline, and manga-symbol treatment are outside the first study |

Only the primary and secondary style references are generation inputs for
V18-01. The other two images clarify the broader visual family and the current
exclusion boundary.

### Historical References

- The v1.4 G2 result may be inspected during review for Akari's established
  line hierarchy and readable paint planes. It does not constrain the new
  translation strongly enough to erase the approved style change.
- No v1.6 image, prompt, proportion, accessory, outfit, palette, or finish has
  positive inheritance authority in v1.8.

## Locked Character and Scene Design

All three candidates preserve:

- an adult age-25 reading and the same-person facial identity;
- the accepted softly rounded cheeks, compact chin, nose, face width, amber eye
  size and construction, brow weight, and restrained expression;
- the short, airy chestnut bob, asymmetric looseness, irregular tips, and the
  complete character-left pale-blue crossed ornament with fine cord detail;
- the V17-01 head-to-body ratio, neck and shoulder construction, upper-body
  volume, subtle waist, healthy thigh and calf volume, limb length, hands,
  feet, and neutral standing balance;
- the white T-shirt, pale-blue lounge shorts, framing, apartment geometry, and
  warm directional domestic light.

Reject black-hair drift, long hair, twin tails, heavy straight bangs, uniform
styling, oversized or rounder eyes, childlike head-to-body proportions, a
sharper V-shaped face, a slimmer anime body, pin-up emphasis, or a different
pose.

## Soft Graphic Cel Rendering Language

### Linework

- Use a thin warm-gray or warm-brown outer contour rather than a hard black
  outline.
- Keep the silhouette clearer than the interior drawing.
- Remove duplicate, sketchy, or texture-only strokes while retaining the airy
  irregularity of the hair and the natural shape of hands, feet, and clothing.

### Shading and Light

- Consolidate small painted transitions into two or three large, readable cel
  planes.
- Preserve the direction and warmth of the existing apartment light.
- Allow a soft edge where skin benefits from warmth, but do not airbrush every
  boundary or reintroduce the current hand-painted microtexture.
- Do not add bloom, film grain, paper texture, chromatic aberration, or global
  smoothing.

### Material Separation

- Skin uses a warm peach base, restrained cheek color, one coherent shadow
  family, and sparse highlights.
- Hair uses large chestnut planes and a limited, slightly crisper highlight
  band while preserving individual silhouette breaks and flyaways.
- The cotton T-shirt and lounge shorts remain matte. Their folds are described
  by broad shadow shapes rather than gloss or dense crease lines.
- Skin, hair, and clothing must not share one plastic-like highlight treatment.

### Room Treatment

Preserve the V17-01 room, floor, wall, light direction, and framing. Simplify
small texture into cleaner shapes without replacing the apartment with a white
graphic background, stars, stickers, borders, text, or decorative geometry.

## Candidate Matrix

Every candidate starts independently from V17-01. No candidate is generated
from or edited through another candidate.

### A - Gentle

- Make the smallest clear rendering change.
- Preserve some hand-painted transitions while organizing the contour and
  consolidating micro-shadows into larger planes.
- Favor maximum identity continuity over a dramatic style shift.

### B - Balanced

- This is the recommended center candidate.
- Use thin colored contours, quiet interior lines, soft two-to-three-step cel
  shading, grouped chestnut hair planes, restrained hair highlights, warm skin,
  and matte clothing.
- Aim for the visual midpoint between the primary and secondary user-supplied
  style references while preserving Akari's intimate warmth.

### C - Graphic

- Make the strongest allowed rendering translation.
- Increase contour hierarchy and flatten color grouping further without
  changing face construction, eye scale, head size, body proportions, or scene.
- Reject the candidate if the stronger simplification makes Akari look younger,
  doll-like, sticker-like, or like a different character.

## Generation and Working Files

Before each generation, open at original detail and assign exact roles to:

1. V17-01 as the sole character and scene authority;
2. v1.5 B3 as body-balance review evidence;
3. `G6f1r23aIAANle8.jpg` as the primary style reference;
4. `HOvzZrzboAA3IDA.jpg` as the secondary style reference.

The prompt must explicitly prevent style references from transferring their
hair color, hairstyle, age, proportions, clothing, pose, props, or background.

Review-stage files belong under the ignored directory:

`build/v1.8-soft-graphic-cel/`

Use these working names:

- `akari-v1.8-v18-01-soft-cel-a-gentle.png`;
- `akari-v1.8-v18-01-soft-cel-b-balanced.png`;
- `akari-v1.8-v18-01-soft-cel-c-graphic.png`;
- `akari-v1.8-v18-01-soft-cel-comparison.png`.

If stable local copies of the attachment inputs are needed during generation,
place them in an ignored subdirectory beneath this working directory and
verify their hashes against this design. Do not commit the supplied JPEGs
without a separate provenance and rights decision.

## Review and Acceptance

Review V17-01 and A/B/C at equal display scale in this order:

1. same-person identity and adult age-25 impression;
2. face, amber eyes, short chestnut bob, and complete hair ornament;
3. body balance, neutral pose, hands, feet, and connected anatomy;
4. immediate readability of the intended gentle, balanced, or graphic strength;
5. distinct skin, hair, and matte-cloth material treatment;
6. apartment, framing, and warm-light continuity;
7. finished image quality and absence of generation artifacts.

Every violation of the `Locked Character and Scene Design` section is a
hard-gate failure. This includes drift in identity, adult age, expression,
eyes, hair, ornament, body, pose, anatomy, outfit, framing, apartment, or light.
Among hard-gate passes, prefer the clearest and most natural preservation of
the fixed V17-01 expression, strongest character appeal, and best finished
image quality. Do not preserve a weaker candidate merely because it looks more
conservative.

The study succeeds when at least one candidate reads immediately as the same
Akari in the approved soft graphic cel language. If no candidate passes, keep
all candidates local, select none, and return to a design decision rather than
promoting the least-bad result.

After presenting the comparison, stop for explicit user selection. Do not run
an automatic correction pass and do not promote a candidate before that choice.

## Promotion Boundary

After explicit selection, a separate promotion step may create:

- `akari-v1.8/accepted/base/akari-v1.8-v18-01-soft-graphic-cel-front.png`;
- `akari-v1.8/README.md`;
- `akari-v1.8/selection.md`.

The accepted PNG must be copied without transformation and verified
byte-identical to the selected review source. The selection record must include
reference roles, source and destination SHA-256 values, generation ID, request
ID when available, immutable prompt hash, dimensions, review verdict, and any
known Minor differences.

Candidate images, comparison sheets, copied attachment inputs, and rejected
outputs remain local and untracked unless the user explicitly asks to preserve
them.

## Verification Scope

The V18-01 image-review pass is limited to:

- confirming each output has a valid PNG signature;
- recording dimensions and SHA-256 values;
- inspecting every candidate at original detail;
- building and inspecting one labeled equal-scale comparison;
- checking Git status so generated review files remain ignored or untracked;
- running Markdown lint only when tracked Markdown changes.

Do not run PDF builds or audits, OCR, Python tests, Node tests, integration
gates, or release gates for this checkpoint. No rendering, manifest, audit, or
application code changes are part of the study.

## Completion Criteria

The first v1.8 checkpoint is complete only when:

- A, B, and C were independently generated from the fixed authority set;
- all three candidates and the equal-scale comparison were inspected;
- the review identifies every hard-gate pass and failure, and no hard-gate
  failure is waived;
- the user explicitly selects one passing candidate, or explicitly records
  that none should be selected;
- any selected candidate is promoted byte-for-byte with its provenance and
  review record;
- generated working material remains outside the durable commit.

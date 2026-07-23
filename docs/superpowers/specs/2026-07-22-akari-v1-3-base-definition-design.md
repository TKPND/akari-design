# Akari v1.3 Base Definition Design

**Version:** 1.0

**Date:** 2026-07-22

**Status:** Approved by user on 2026-07-22

## 1. Summary

Akari v1.3 refreshes the character's face, hair, ornament, and rendering quality
while retaining the natural posture, healthy leg volume, and everyday physical
credibility established by v1.2 Natural Form.

The visual starting point is
`source/references/style-study/akari-v04-a.png`. Its expression, face, airy bob, eye finish,
and soft polished rendering define the preferred direction. The current image
is not itself immediately accepted because its hair ornament is on the wrong
character side. The immutable source image becomes the highest visual
authority for the v1.3 refresh after it is copied into the new package with
recorded provenance and a SHA-256 digest.

The first v1.3 milestone is a six-image Base Definition set. It is deliberately
smaller than the v1.2 Core and does not include a release PDF or broad Daily
scene production.

## 2. Approved Direction

The approved direction combines two ideas:

- Use a visual refresh as the primary change: update the face, hair, eyes,
  ornament finish, and rendering quality.
- Carry forward v1.2's natural body language, everyday intimacy, and relaxed
  expressions as a supporting layer.

The source image remains the visual authority, but v1.3 identity is not locked
from one image alone. A corrected key visual and an independently generated
natural full-body view must depict the same person before expression and
wardrobe variants can be accepted.

## 3. Goals

- Preserve the specific appeal of `akari-v04-a.png` instead of reducing it to
  a text-only prompt.
- Establish a stable v1.3 face and airy-bob identity across close and full-body
  camera distances.
- Correct and refine the hair ornament without degrading the face, smile, hair
  movement, or rendering quality.
- Retain healthy legs, believable weight, and natural body connections from
  v1.2.
- Define relaxed intimacy and a bright open-mouth smile as complementary
  expression anchors.
- Define both the inherited outdoor outfit and the white T-shirt with pale-blue
  shorts as canonical wardrobe anchors.
- Keep provenance, inheritance, review status, and accepted revisions
  machine-checkable.

## 4. Non-Goals

- Do not assign one immutable numerical age to the character.
- Do not make Akari childlike; the lower bound remains a clearly young-adult
  reading.
- Do not reproduce the source image's pose, yellow background, or lighting in
  every v1.3 asset.
- Do not discard or overwrite the v1.2 package, release PDF, manifests, or
  accepted assets.
- Do not treat a v1.2 image as v1.3 identity authority.
- Do not build a v1.3 settings PDF during Base Definition.
- Do not begin broad Daily scene production during Base Definition.
- Do not commit candidate and comparison directories by default.

## 5. Identity Lock

### 5.1 Face and age reading

- Preserve the source image's cute face, large amber jewel-like eyes, softly
  rounded cheeks, small nose, and natural blush.
- Preserve the current eye size and general facial balance rather than making
  the face deliberately more mature.
- Do not bind the design to age 25 or another exact number.
- Require a young-adult reading and reject proportions, expressions, or body
  construction that make the character read as a child.

### 5.2 Hair

- Use a warm chestnut-brown, airy short bob as the new canonical hairstyle.
- Preserve the source image's layered ends, fine flyaways, cheek strands, and
  sense of movement.
- Keep the main hair length clearly above the shoulders.
- Allow scene-dependent movement and mild irregularity without changing the
  underlying silhouette.
- Reject long hair, side ponytails, one-side-up styles, twin tails, or a return
  to the more compact v1.2 bob as the default v1.3 silhouette.

### 5.3 Hair ornament

- Place the complete ornament on character-left, which normally appears on
  image-right in a front-facing view.
- Retain the identity motif of pale-blue crossed pins above a small ribbon.
- Refine the ribbon for v1.3 by making it smaller and giving it shorter tails
  so it complements rather than competes with the airy hair.
- Reject mirrored, duplicated, incomplete, oversized, or hidden ornaments.

### 5.4 Body

- Use a light, graceful upper-body impression.
- Retain healthy leg volume from v1.2 instead of extending the source image
  into a uniformly slender full-body design.
- Preserve believable pelvis, knee, ankle, and foot connections.
- Make weight placement and contact with the floor readable in standing and
  seated work.
- Reject excessive leg length, extreme thinness, pinched ankles, disconnected
  joints, or pose choices that trade anatomy for cuteness.

### 5.5 Rendering

- Use fine line art, soft pastel cel shading, warm translucent skin, glossy but
  structured hair, and jewel-like amber eyes.
- Keep one coherent visual style across the set.
- Scale detail with camera distance: close views retain precise eyes, hair,
  blush, and highlights; full-body views simplify small details while
  preserving the same line, color, and light language.
- Do not turn the full-body assets into a flatter or visibly separate house
  style.

### 5.6 Expression anchors

v1.3 has two complementary emotional anchors:

- **Everyday anchor:** relaxed, familiar, and quietly intimate without becoming
  blank or sleepy by default.
- **Key-visual anchor:** the source image's bright open-mouth smile and outward
  energy without exaggerated or childlike facial construction.

Neither anchor supersedes the other. The everyday expression governs ordinary
scenes, while the bright expression governs key art and overtly cheerful
moments.

## 6. Wardrobe Anchors

v1.3 begins with two equally canonical wardrobe contexts.

### 6.1 Outdoor and setting-check outfit

- White oversized hoodie.
- Gray pleated skirt.
- White socks with two pale-blue stripes.
- White chunky sneakers.
- The implementation plan selects the strongest applicable v1.2 references
  for these fixed garments. Each physical reference must be copied and
  recorded before use.

### 6.2 Everyday roomwear

- Loose white short-sleeved T-shirt.
- Pale-blue lounge shorts with a restrained drawstring.
- Bare legs unless the scene or validation role explicitly requires indoor
  socks.
- Relaxed fabric and fit without sexualized framing.

Changing wardrobe must not change facial identity, age reading, body volume,
or hair silhouette.

## 7. Base Definition Deliverables

The first milestone contains four asset IDs and six accepted images.

### V13-01: Corrected Key Visual

Create a close successor to `akari-v04-a.png` that preserves its composition,
face, hair, expression, palette, and light while moving the hair ornament to
character-left and applying the refined v1.3 ornament proportions.

The source image remains immutable. V13-01 is a new accepted artifact, not an
in-place overwrite.

### V13-02: Natural Full Body

Create a neutral-background, natural front full-body view in the white
T-shirt and pale-blue shorts. It must reproduce the V13-01 face and airy bob at
a longer camera distance while validating the approved upper-body lightness,
healthy legs, and natural weight placement.

### V13-03A and V13-03B: Expression Pair

Use the same chest-up crop, head angle, and lighting for both images.

- **V13-03A:** relaxed and familiar everyday expression.
- **V13-03B:** bright open-mouth key-visual smile.

The expression may change upper eyelid opening, lower-lid tension, brow angle,
mouth shape, cheek compression, and gaze energy. It must not change face width,
eye identity, chin shape, hair volume, or ornament design.

### V13-04A and V13-04B: Wardrobe Pair

Use the same natural standing pose, camera, and expression for both images.

- **V13-04A:** inherited outdoor and setting-check outfit.
- **V13-04B:** white T-shirt and pale-blue lounge shorts.

The pair validates that wardrobe changes do not create a different body or age
impression.

## 8. Package Boundary

The future implementation creates an independent package instead of modifying
v1.2 in place:

```text
akari-v1.3/
├── README.md
├── docs/
│   └── akari-v1.3-base-design.md
├── manifest/
│   ├── assets.yaml
│   ├── inheritance.yaml
│   └── review-log.yaml
├── references/
│   ├── style/
│   │   └── akari-v04-a.png
│   └── v1.2/
├── accepted/
│   └── base/
│       ├── key-visual/
│       ├── full-body/
│       ├── expressions/
│       └── wardrobe/
├── source/
│   └── candidates/
└── comparisons/
```

The directories have these responsibilities:

- `references/style/` contains the immutable source image and no candidates.
- `references/v1.2/` contains only explicitly selected body, weight, or outfit
  references copied across the package boundary.
- `source/candidates/` contains working generations and stays untracked unless
  the user explicitly requests preservation.
- `comparisons/` contains local contact sheets and review aids and stays
  untracked by default.
- `accepted/base/` contains only user-selected durable deliverables.
- `manifest/assets.yaml` owns asset IDs, variants, revisions, dependencies,
  states, and accepted paths.
- `manifest/inheritance.yaml` owns source paths, copied paths, SHA-256 digests,
  controlling roles, reuse rationales, inherited traits, and explicit
  non-inherited traits.
- `manifest/review-log.yaml` owns candidate verdicts, defects, selection notes,
  and promotion history.

The implementation may mirror this design into
`akari-v1.3/docs/akari-v1.3-base-design.md`, but this approved specification in
`docs/superpowers/specs/` remains the planning source until the package exists.

## 9. Reference Authority

Reference authority is role-specific rather than global.

1. `akari-v04-a.png` controls the refreshed face, eye finish, hair silhouette,
   expression energy, and rendering direction.
2. Accepted V13-01 controls v1.3 face, hair, ornament, and close-view rendering
   after promotion.
3. Selected v1.2 references control only body connection, healthy leg volume,
   weight, and inherited outfit facts recorded in `inheritance.yaml`.
4. Accepted V13-02 controls the combined v1.3 face, hair, body, and full-body
   rendering after promotion.
5. V13-03 and V13-04 use accepted V13-01 and V13-02 as their v1.3 identity
   authorities.

A v1.2 reference cannot grant v1.3 face or rendering authority. A key visual
cannot grant full-body anatomy authority until V13-02 passes review.

## 10. Production and Data Flow

```text
approved design
  -> immutable style reference + recorded provenance
  -> selected v1.2 body and wardrobe references + recorded provenance
  -> V13-01 candidates
  -> original-resolution review and user selection
  -> accepted V13-01
  -> V13-02 candidates using V13-01 plus role-limited v1.2 references
  -> cross-distance identity and anatomy review
  -> accepted V13-02 and Base Identity Lock
  -> V13-03 expression pair candidates
  -> V13-04 wardrobe pair candidates
  -> pair reviews and user selections
  -> complete six-image Base Definition set
```

V13-01 and V13-02 form a hard gate. Expression and wardrobe production must
not start until both are accepted as the same person.

Before every identity-sensitive generation, open the current selected
candidate and all role-relevant references. The prompt must state each
reference's role. Do not rely on a text-only recreation of the source image.

## 11. Review Gates

Review candidates in this priority order.

1. **Identity:** face, amber eyes, airy bob, and hair color match the accepted
   v1.3 anchors.
2. **Hair ornament:** one complete refined ornament is on character-left.
3. **Body:** weight, pelvis-to-leg connection, healthy volume, joints, and
   contact are credible.
4. **Expression and appeal:** the requested expression reads immediately and
   retains character appeal.
5. **Rendering quality:** hands, hair, clothing, edges, shading, and highlights
   are coherent and artifact-free.

Use three verdict classes:

- **Pass:** eligible for the stated controlling role.
- **Minor:** usable only for a documented limited role; it cannot silently
  become a broader identity authority.
- **Major:** ineligible for promotion.

Wrong-side or duplicate ornaments, childlike identity drift, different-person
facial drift, broken anatomy, and disconnected body parts are Major defects.
Final Base Definition anchors must be Pass. A measured or qualitative Major
cannot be waived into an accepted anchor.

When candidates all pass hard gates, prefer the image with the strongest
expression read, character appeal, and finished image quality.

## 12. V13-01 Preservation Gate

V13-01 has an additional preservation requirement: the ornament is the only
required design correction. A candidate is not improved merely because its
pixel difference is small.

Reject a candidate if ornament correction weakens any of the following:

- face identity or eye rendering
- open-mouth smile and gaze energy
- airy hair volume and fine strands
- head, hand, torso, or raised-leg anatomy
- soft light, skin color, or clothing finish

If a small patch produces visible seams, truncated hair, or an ornament that
does not follow the hair, retain a larger generated region or regenerate the
image. Visual continuity takes priority over minimizing the changed area.

## 13. Failure Handling

- If local ornament editing repeatedly changes the face or breaks the hair,
  widen the edit region or regenerate a close successor using the immutable
  source as a direct reference.
- If V13-02 looks like a different person, stop the pipeline and revise its
  identity references or generation contract. Do not proceed to V13-03 or
  V13-04.
- If a prompt keeps mirroring the ornament, strengthen character-left and
  image-right spatial language and review the reference orientation. Do not
  fix the manifest to match a wrong image.
- If the full body becomes too slender or long-legged, increase the authority
  of the selected v1.2 body reference without granting it face or rendering
  control.
- If close and full-body rendering look like different styles, adjust detail
  density rather than replacing either asset with a separate style family.
- Preserve rejected and superseded decisions in the review log; do not replace
  history with only the final selection.
- Never promote a Major with a promise to repair it later.

## 14. Validation and Verification

The implementation introduces two explicit commands:

```sh
npm run validate:v1-3
npm run gate:integration:v1-3
```

`validate:v1-3` must verify at least:

- required asset IDs and variant counts
- valid state transitions and exactly one accepted revision per required image
- existing files for every manifest path
- matching SHA-256 digests for every physical reference
- explicit controlling roles and reuse rationales
- no direct runtime dependency on `tmp/style-study/` or v1.2 working paths
- review evidence for ornament side and hard-gate verdicts
- accepted Base Definition anchors have a Pass verdict

`gate:integration:v1-3` runs the manifest validator and focused automated tests
serially. It must not overlap image generation, browser rendering, PDF work, or
OCR on the resource-constrained host.

Visual verification includes:

- original-resolution inspection of every candidate
- side-by-side comparison with the source and accepted anchors
- face and hair comparison between V13-01 and V13-02
- same-condition pair comparison for V13-03 and V13-04
- explicit user selection before promotion
- byte comparison and matching SHA-256 between the selected candidate and the
  promoted accepted file

After Markdown changes, run:

```sh
npm run lint:md
```

Changes to shared Natural Form behavior require the existing
`npm run gate:integration:v1-2`. Legacy, cross-version, or uncertain broad
changes require `npm run gate:integration:all`. Base Definition does not add a
v1.3 release or PDF audit gate.

## 15. Completion Criteria

Base Definition is complete only when all of the following are true:

- V13-01 and V13-02 are accepted as the same Akari.
- V13-03A and V13-03B pass the same-condition expression comparison.
- V13-04A and V13-04B pass the same-condition wardrobe comparison.
- All six accepted images have Pass verdicts for their controlling roles.
- Every reference and accepted image has recorded provenance and a matching
  SHA-256 digest.
- The v1.3 validation and integration commands pass.
- Candidate and comparison scratch data remain outside the durable commit
  unless the user explicitly requests otherwise.
- v1.2 and legacy commands, accepted assets, manifests, and release artifacts
  remain unchanged.

Only after these criteria pass should a later design consider broader v1.3
Daily scenes or a settings PDF.

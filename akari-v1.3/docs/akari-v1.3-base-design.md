# Akari v1.3 Base Design

This package design mirrors the approved Base Definition requirements.

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
- The implementation selects the strongest applicable v1.2 references for
  these fixed garments. Each physical reference is copied and recorded before
  use.

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

This package adds neither broad Daily scenes nor a v1.3 settings PDF.

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

## 15. Completion Criteria

Base Identity Lock: Pass

| Asset | Revision | Accepted path |
| --- | --- | --- |
| V13-01 | r01 | `accepted/base/key-visual/akari-v1.3_v13-01_corrected-key-visual_r01.png` |
| V13-02 | r01 | `accepted/base/full-body/akari-v1.3_v13-02_natural-full-body_r01.png` |
| V13-03A | r01 | `accepted/base/expressions/akari-v1.3_v13-03a_everyday_r01.png` |
| V13-03B | r01 | `accepted/base/expressions/akari-v1.3_v13-03b_bright-smile_r01.png` |
| V13-04A | r01 | `accepted/base/wardrobe/akari-v1.3_v13-04a_outdoor_r01.png` |
| V13-04B | r01 | `accepted/base/wardrobe/akari-v1.3_v13-04b_roomwear_r01.png` |

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

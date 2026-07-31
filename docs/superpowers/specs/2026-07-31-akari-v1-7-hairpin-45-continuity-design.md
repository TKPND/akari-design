# Akari v1.7 Hairpin-Side 45-Degree Continuity Design

Status: approved design.

Date: 2026-07-31.

## Summary

`V17-03` extends the accepted Akari v1.7 hairpin-side camera orbit from 30
degrees to exactly 45 degrees. It shows the same adult woman, same instant,
same neutral full-body stance, and same apartment presentation from one camera
position 15 degrees farther around Akari's character-left, hairpin side.

The pass creates three independent full-body candidates from one identical
two-image reference contract. It tests 45-degree continuity; it does not add a
new pose, redesign Akari, create an opposite-side view, complete a turnaround,
or authorize promotion.

## Generation Authority

Pass exactly two accepted v1.7 images to every image-generation call in this
order.

### Image 1: Hairpin-Side 30-Degree Primary Reference

Path:

`akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`

Required SHA-256:

`22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749`

Image 1 is the primary same-side continuity reference. It controls the
accepted camera-orbit direction, hairpin-side face and skull construction,
complete ornament topology, same-moment spatial arrangement, and coherent
face-to-feet perspective. It does not control underlying body volume,
expression restraint, clothing design, palette, or finish when those differ
from Image 2.

The requested result advances the virtual camera another 15 degrees in the
same direction. Image 1 does not authorize copying or increasing its two
recorded Minor findings: slight near-side bust and waist rendering emphasis,
and slightly stronger eye and facial polish than the accepted front.

### Image 2: Intimate Front Correction Reference

Path:

`akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`

Required SHA-256:

`64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`

Image 2 is the correction reference for the underlying identity and design.
It controls Akari's age-25 impression, face construction, restrained eyes and
blush, quietly pleased closed-mouth expression, short airy chestnut bob,
underlying body volume, garment ease, near-even standing balance, roomwear,
bare feet, warm apartment presentation, palette, line hierarchy, paint planes,
and hand-painted finish.

Image 2 must not pull the result back toward a near-front view. It corrects
identity, body, expression, and finish while Image 1 controls the direction of
the camera orbit.

If the two accepted inputs differ, Image 2 wins for identity, underlying body
volume, expression restraint, and finish; Image 1 wins for the same-moment
world-space arrangement, same-side camera direction, perspective continuity,
and ornament ordering.

Every generation prompt and review must apply this precedence explicitly. A
candidate that misses either the Image 1 orbit role or the Image 2 correction
role fails. No candidate may become the input for another candidate. No v1.6
image, prompt, proportion, accessory, outfit, palette, or manifest has positive
or negative generation authority.

## Human QA References

Open these images at original detail before generation, but do not pass them
to image generation:

1. `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
   - SHA-256:
     `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`;
   - checks the inherited head-to-body ratio, restrained upper-body volume,
     subtle waist, healthy thighs, and quiet full-body balance.
2. `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
   - SHA-256:
     `6757e601d2cfd158c970ab701a876981ace837e669c313dec6d25c0c539ff4d6`;
   - checks adult-face direction, deliberate outer lines, restrained interior
     lines, readable paint planes, quiet palette, and finish.
3. `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png`
   - SHA-256:
     `ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21`;
   - checks only 45-degree cheek width, bob silhouette, and the perspective
     ordering of the crossed pins and cord ornament.
4. `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png`
   - SHA-256:
     `19c8c96113bcbc47f7d1e4cc1d58af466d3a573f0dae40cfcdf9bf456b1a0a9b`;
   - checks only coherent 45-degree alignment through the head, ribcage,
     pelvis, knees, and feet.

The two old 45-degree images are not identity, age, body, expression, stance,
outfit, background, framing, palette, or rendering authorities. Their white
backgrounds, different clothing, and larger figure occupancy must not leak
into the new image. Prior v1.7 work already established that old angle images
can pull generation toward their obsolete framing, so they remain human-QA
references only.

## View Contract

Show Akari from exactly 45 degrees toward her own character-left, hairpin side:

- the virtual camera moves horizontally another 15 degrees from the accepted
  30-degree position while Akari remains still;
- camera height, elevation, orbit radius, subject distance, focal perspective,
  pitch, roll, portrait crop, and character scale remain unchanged; azimuth is
  the only camera variable;
- the complete pale-blue ornament and character-left cheek remain on the near
  side and read in correct perspective;
- face, neckline, shoulders, T-shirt and ribcage, shorts waistband and pelvis,
  knees, ankles, and feet agree with one coherent 45-degree camera position;
- Akari does not turn, twist, or re-pose herself to manufacture the angle;
- only her amber eyes track the lens naturally, preserving familiar eye
  contact without turning the head back toward front;
- both eyes may remain visible with physically credible narrowing of the far
  side, without enlarging it or flattening the face;
- both hands, both legs, and both bare feet remain complete and anatomically
  connected in frame;
- the greater overlap and depth separation expected at 45 degrees are allowed
  when they result from perspective rather than a new pose.

Reject a near-30-degree substitute, a profile or near-profile view, a mirrored
or opposite-side view, or any result whose head, upper body, pelvis, knees, and
feet imply different camera or body angles. Also reject a changed camera
height, elevation, distance, focal perspective, pitch, roll, or figure scale,
even when the azimuth appears correct.

## Same-Moment State Contract

The accepted references show one fixed instant, not merely a reusable outfit
and generic standing pose. Preserve the same world-space state:

- the same head, neck, shoulder, ribcage, pelvis, knee, ankle, and foot
  arrangement, with the eyes alone tracking the new lens position;
- the same relaxed arm, elbow, wrist, hand, and finger placement, allowing only
  perspective-required overlap and visibility changes;
- the same airy hair locks, irregular tips, ornament attachment point, pin
  crossing, cord loops, and tails, without restyling or wind movement;
- the same T-shirt hang, sleeve state, hem relationship, shorts waistband,
  drawstring, and garment ease, allowing folds to reveal different sides but
  not a newly staged garment state;
- the same planted-foot base, near-even load, and relationship to the floor;
- the same apartment geometry, wall and baseboard, floor plane, directional
  light source, and quiet shadow state, allowing only camera parallax.

Reject a candidate that looks like a second take, new pose, restyled hair,
reset clothing, shifted feet, moved room, changed light setup, or camera
reframe rather than the same instant viewed from a new azimuth.

## Locked Character, Body, and Presentation

Preserve the accepted v1.7 identity and emotional beat:

- adult age 25, soft cheek volume, compact chin, accepted nose language,
  restrained blush, subtle lip color, low-contrast amber eyes, and quiet lash
  and brow treatment;
- the small closed-mouth smile of becoming quietly pleased after noticing the
  familiar viewer, without a stronger, broader, teasing, smug, glamorous, or
  seductive expression;
- the short airy chestnut bob, asymmetric looseness, irregular tips, natural
  skull volume, and low-gloss paint-plane treatment;
- exactly one complete character-left ornament: two pale-blue crossed pins
  above a delicate thin cord bow with narrow loops and two slim tails.

Preserve the accepted underlying body and stance as one three-dimensional
form seen from a new camera position:

- retain the v1.5 B3-derived head-to-body ratio, restrained bust, subtle waist,
  stable pelvis and hip volume, healthy thighs, limb lengths, hands, feet, and
  adult anatomy;
- retain the white T-shirt's relaxed ease and the pale-blue lounge shorts'
  accepted fit;
- keep shoulders and pelvis level, the spine quiet and near vertical, knees
  softly unlocked, both soles planted, and weight distributed nearly evenly;
- keep relaxed arms and complete hands without turning the stance into a pose;
- do not add chest projection, bust separation, waist pinching, hip flare,
  stronger bust-to-waist or waist-to-hip contrast, leg elongation, one-leg
  loading, lateral hip shift, contrapposto, an S-curve, walking, or crossed
  legs.

At 45 degrees, a greater near/far foot offset, limb overlap, and visible side
edge can be legitimate perspective. Treat them as perspective only when the
shoulders and pelvis remain level, both feet remain planted, the torso stays
centered over the same base of support, and neither leg reads as the sole
weight-bearing leg.

Preserve the warm minimal apartment, directional domestic light, level floor
and baseboard, portrait dimensions, full-body scale, breathing room, quiet
palette, deliberate outer lines, restrained interior lines, readable paint
planes, and hand-painted finish. Do not introduce a white studio background,
camera roll, wide-angle distortion, photorealistic skin, plastic smoothing,
generic character-sheet polish, text, labels, borders, logos, or watermarks.

## Candidate Contract

Generate exactly three candidates, A, B, and C. Every candidate:

- starts independently from the same ordered Image 1 and Image 2 inputs;
- uses one identical complete prompt;
- targets the same exact hairpin-side 45-degree view;
- has no candidate-specific angle, expression, pose, body, styling, or
  rendering delta;
- represents an independent reproducibility attempt, not a designed variant.

Run the three image-generation calls serially. Save and verify each returned
source before starting the next call. Do not use A as an anchor for B, B as an
anchor for C, or any other sibling chaining.

## Working Files

Keep all review-stage output under the ignored directory:

`build/v1.7-hairpin-45-continuity/`

Use these names:

- `akari-v1.7-v17-03-hairpin-45-r01-a.png`;
- `akari-v1.7-v17-03-hairpin-45-r01-b.png`;
- `akari-v1.7-v17-03-hairpin-45-r01-c.png`;
- `akari-v1.7-v17-03-hairpin-45-r01-comparison.png`.

The comparison shows `Front`, `30°`, `A`, `B`, and `C` at equal character
height without cropping or covering any figure. It is local review evidence,
not a deliverable.

Do not modify either accepted v1.7 input, any human-QA reference, existing
V17-01 or V17-02 review evidence, or any v1.6 material.

## Review and Selection

Inspect every candidate at original detail, then review the equal-height
comparison in this order:

1. same-person identity, adult age-25 impression, and accepted emotional beat;
2. the same fixed instant in hair, ornament, arms, hands, garment state, feet,
   room geometry, and light setup;
3. correct character-left hairpin side, unchanged camera height, distance,
   lens perspective, pitch and roll, and coherent exact 45-degree alignment
   from face through feet;
4. unchanged bust, waist, hip, thigh, garment, and head-to-body volume without
   compounding either accepted V17-02 Minor;
5. level shoulders and pelvis, nearly even weight, planted feet, quiet spine,
   and perspective parallax without contrapposto or a new pose;
6. complete ornament topology, believable cheek width, and airy bob volume;
7. intact hands, feet, clothing, framing, level background, light, palette,
   line hierarchy, paint planes, and absence of artifacts or v1.6 drift.

Reject immediately for any identity, adult-age, accepted-expression,
same-moment state, view, camera, body-volume, stance, ornament, anatomy,
presentation, or artifact failure. A candidate must clear every hard gate
before expression appeal or finish quality can break a tie.

The pass succeeds only if at least one candidate clears every hard gate. Among
passing candidates, prefer the strongest same-person read, natural intimate
eye contact, character appeal, and finished image quality. Do not keep a
weaker passing image merely because it looks more conservative.

The user makes the final selection. Do not promote a reviewer's favorite or
the least-bad candidate automatically. If no candidate passes, preserve all
r01 evidence and return to a new design decision. Do not generate r02, repair
or composite a candidate, relax the 45-degree target, or promote any image
without explicit user approval.

## Verification Scope

Verification for this pass is image-only:

- open both generation inputs and all four human-QA references at original
  detail before generation, state each role, and keep them visible in the
  conversation context;
- verify all six recorded input hashes before the first call;
- record the generation artifact or request identifier and exact returned
  source path for A, B, and C;
- copy each returned PNG without transformation and prove byte identity to its
  exact returned source;
- verify every candidate has PNG signature `89504e470d0a1a0a`, exact format and
  dimensions `PNG 1024x1536`, and a recorded SHA-256;
- inspect every candidate at original detail;
- build and inspect the labeled equal-height comparison;
- confirm every generated file remains ignored and the tracked worktree stays
  clean throughout the generation and review pass.

If a generated image appears in the conversation without a local source PNG,
use the repository's structural rollout-payload recovery procedure. Never copy
a large base64 payload manually from terminal output.

Do not run Node tests, Python tests, PDF builds, OCR, package validation,
integration gates, or release gates. No application, renderer, manifest,
validator, or audit behavior changes in this pass.

## Promotion Boundary

Selection does not authorize promotion. After explicit user selection, define
a separate minimal promotion design that decides the semantic accepted path,
durable selection-history update, byte-identity checks, review requirements,
commit boundary, and integration procedure.

## Non-Goals

- no opposite-side 45-degree, profile, rear, overhead, or paired-view asset;
- no complete turnaround, expression sheet, wardrobe pass, manifest, PDF, or
  release package;
- no change to either accepted v1.7 source image or its recorded authority;
- no old 45-degree or v1.6 image as a generation input;
- no candidate-specific prompt variants or sibling chaining;
- no automatic correction, r02 generation, compositing, selection, promotion,
  push, merge, worktree cleanup, or remote synchronization.

# Akari v1.7 Hairpin-Side 45-Degree Continuity r02 Design

Status: approved design.

Date: 2026-07-31.

## Summary

`V17-03 r02` is a body-only correction pass on the selected r01 candidate A.
r01 A already establishes the correct hairpin-side 45-degree view, same fixed
instant, Akari identity, quietly pleased expression, pose, ornament, camera,
scale, crop, apartment, light, palette, line hierarchy, paint planes, and
finished-image quality. r02 keeps that image as the primary target and canvas.

The correction is deliberately narrow. It removes three connected
chest-to-waist drifts in r01 A: the rounder near-side bust projection, the
newly stronger under-bust definition, and the narrower waist with tighter
T-shirt cling. It restores the accepted front checkpoint's underlying body
volume and relaxed shirt drape without flattening the adult torso, copying a
front-view silhouette, or changing the hips or thighs.

This pass does not revisit the 45-degree design, repair any other r01 A Minor,
redesign Akari, create a new pose, or authorize promotion.

## Generation Authority

Pass exactly two images to every image-generation call in the following order.

### Image 1: r01 A Primary Target and Canvas

The authoritative raw r01 A source is:

`/home/takahiro/.codex/generated_images/019fb8b9-0c2a-7232-adbd-7b48a8c4af53/exec-907b61bc-e92b-4b64-9e81-26e4d0cf9dbf.png`

Required SHA-256:

`701f29a74642ab98a6f948df50d7bf11fc659f0844b25d9636bba8f893ce9965`

Before generation, copy that file byte-for-byte into the new r02 worktree's
ignored input directory. Verify the raw source and worktree-local copy with
`cmp`, SHA-256, PNG signature, format, and dimensions. Supply only the verified
worktree-local copy as Image 1; do not reach into the existing r01 worktree or
use a comparison rendering as a generation input.

Image 1 controls every attribute except the explicitly listed chest-to-waist
correction:

- the exact adult woman, age-25 impression, face construction, eye treatment,
  expression, hair, and ornament;
- the already-correct character-left hairpin-side 45-degree camera position,
  camera height, elevation, orbit radius, distance, focal perspective, pitch,
  roll, portrait crop, character scale, and face-to-feet perspective;
- the same fixed moment, including the head, shoulders, ribcage, pelvis,
  knees, feet, arms, hands, fingers, hair locks, clothing state, planted-foot
  base, room geometry, light, and shadows;
- the complete body outside the narrow chest-to-waist correction, including
  shoulders, arms, hands, pelvis, hips, thighs, knees, lower legs, and feet;
- the white T-shirt design outside its chest-to-waist drape, lounge shorts,
  bare feet, warm apartment, framing, palette, line work, paint planes, and
  hand-painted finish.

r01 A's slightly stronger eye polish and compressed cord are known Minor
findings. The user chose a body-only correction, so those exact details remain
locked for r02. They are not permission to intensify, simplify, or otherwise
change either feature.

### Image 2: Accepted Front Body-Volume Correction Reference

Path:

`akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`

Required SHA-256:

`64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`

Image 2 is a correction authority only for the underlying chest-to-waist body
volume and the relaxed T-shirt drape over that volume. It establishes the
restrained bust, soft rather than newly emphasized under-bust transition,
subtle waist, and relaxed garment ease that must be expressed credibly from
Image 1's fixed 45-degree camera position.

Image 2 has no authority over camera angle, head angle, face, eyes, expression,
hair, ornament, pose, arms, hands, hips, thighs, legs, feet, room, light,
palette, line work, paint planes, finish, crop, or scale. It must not pull the
result toward front, reset the same moment, or replace r01 A's view-dependent
construction with a frontal interpretation.

### Precedence Rule

If the inputs differ inside the underlying chest-to-waist body volume or
relaxed shirt drape, Image 2 wins. Everywhere else, Image 1 wins. Do not average
the two views, broaden Image 2's authority, or treat the accepted front as a
general identity or finish correction in this pass.

Every prompt, executor review, independent review, and tie-break must apply
this narrow precedence. A candidate fails if it preserves r01 A's three body
drifts, changes any out-of-scope r01 A detail, or moves toward the front view.

## Human-QA-Only References

Open these images at original detail before generation, but never pass them to
image generation:

1. `akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`
   - SHA-256:
     `22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749`;
   - checks that the accepted orbit direction and same-moment continuity have
     not been disturbed by the body-only repair.
2. `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
   - SHA-256:
     `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`;
   - checks restrained upper-body volume, subtle waist, healthy thighs,
     head-to-body ratio, and quiet full-body balance.
3. `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
   - SHA-256:
     `6757e601d2cfd158c970ab701a876981ace837e669c313dec6d25c0c539ff4d6`;
   - checks adult-face direction, line hierarchy, paint planes, quiet palette,
     and finish without authorizing an r01 A polish change.
4. `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png`
   - SHA-256:
     `ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21`;
   - checks only 45-degree cheek width, bob silhouette, and perspective
     ordering of the crossed pins and cord ornament.
5. `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png`
   - SHA-256:
     `19c8c96113bcbc47f7d1e4cc1d58af466d3a573f0dae40cfcdf9bf456b1a0a9b`;
   - checks only coherent 45-degree alignment through the head, ribcage,
     pelvis, knees, and feet.

These five images are review controls only. None may dilute Image 1's primary
authority, enlarge Image 2's correction scope, or appear in
`referenced_image_paths`.

## Body-Only Correction Contract

Correct exactly three connected r01 A drifts:

- reduce the near-side bust's newly rounder and more prominent projection to
  the restrained accepted underlying volume, while retaining credible adult
  three-dimensional volume at 45 degrees;
- soften the newly stronger under-bust line, shadow, and separation so the
  transition reads through the relaxed shirt instead of as added definition;
- restore the accepted subtle waist and relaxed chest-to-waist T-shirt fall,
  removing r01 A's narrower waist and tighter shirt cling.

The repair must remain physically coherent. The bust, ribcage, waist, shirt,
and 45-degree perspective must agree as one volume. Do not erase the chest,
flatten the torso unnaturally, paste a frontal silhouette onto the 45-degree
view, create a baggy new shirt, or hide the correction behind blur, shadow, or
cropping.

Do not alter the shoulder width, ribcage position, pelvis, hips, waist-to-hip
relationship outside removal of the narrowed waist drift, thigh volume, leg
lengths, stance, arm placement, hand placement, or any other body feature.
Hips and thighs must remain those of r01 A, not be reshaped to compensate for
the waist correction.

## Locked r01 A State

Everything outside the three correction targets remains fixed:

- same person, adult age 25, same face planes, cheeks, chin, nose, amber eyes,
  gaze, brows, lashes, blush, lips, and quietly pleased closed-mouth smile;
- the same slightly stronger eye polish recorded as an r01 A Minor;
- same airy chestnut bob, individual locks, irregular tips, skull volume, and
  hair-edge treatment;
- exactly the same character-left crossed pins and compressed cord ornament,
  including attachment, ordering, loops, tails, scale, and color;
- exact hairpin-side 45-degree azimuth and the same camera height, elevation,
  radius, distance, focal perspective, pitch, roll, crop, and character scale;
- exact head, neck, shoulders, pelvis, legs, feet, arms, hands, fingers, pose,
  balance, clothing state, shorts, bare feet, apartment, baseboard, floor,
  directional light, shadows, palette, lines, paint planes, and finish.

Reject any candidate that looks like a new take, a wider redesign, a camera
correction, a face or ornament polish pass, or a global regeneration rather
than a localized body-volume correction.

## Candidate and Working-File Contract

Generate exactly three independent candidates, A, B, and C. Every candidate:

- starts from the same ordered Image 1 and Image 2 inputs;
- uses the same immutable prompt byte-for-byte;
- receives no candidate-specific instruction or variation;
- never uses a sibling candidate as input, reference, or instruction source;
- is generated serially and source-verified before the next call begins.

Keep all r02 inputs, recovered sources, candidates, and comparisons under:

`build/v1.7-hairpin-45-continuity-r02/`

Use these names:

- input copy:
  `input/akari-v1.7-v17-03-hairpin-45-r01-a-authoritative-source.png`;
- `akari-v1.7-v17-03-hairpin-45-r02-a.png`;
- `akari-v1.7-v17-03-hairpin-45-r02-b.png`;
- `akari-v1.7-v17-03-hairpin-45-r02-c.png`;
- `akari-v1.7-v17-03-hairpin-45-r02-comparison.png`.

The existing r01 worktree and all r01 evidence remain untouched. Do not
overwrite, delete, move, normalize, or clean them up.

The comparison contains six columns in this exact order: accepted `Front`,
accepted `30°`, authoritative `r01 A`, `r02 A`, `r02 B`, and `r02 C`. All six
1024-by-1536 source frames use one equal display scale. Do not crop, warp,
individually normalize, or conceal scale, pose, framing, or anatomy drift.

## Review Order and Seven Hard Gates

Inspect every candidate at original detail before inspecting the six-column
comparison. Apply all seven gates to every candidate:

1. **Identity and chosen face state:** same adult age-25 person, face, amber
   gaze, quietly pleased expression, and r01 A eye polish without any facial
   correction, front-reference pull, or identity drift.
2. **Fixed 45-degree moment:** exact r01 A hairpin-side 45-degree camera,
   head-to-feet alignment, same pose and world-space arrangement, same crop,
   scale, apartment, light, and shadows.
3. **Required body correction:** restrained near-side bust projection, softened
   new under-bust definition, restored subtle waist, and relaxed
   chest-to-waist shirt drape consistent with the accepted front's underlying
   volume.
4. **Correction restraint and three-dimensionality:** no unnatural flattening,
   frontal silhouette, new shirt design, blur-based concealment, hip or thigh
   change, body redesign, or change outside the chest-to-waist correction.
5. **Pose, anatomy, and clothing continuity:** unchanged shoulders, pelvis,
   hips, thighs, arms, hands, legs, feet, stance, shorts, shirt state outside
   the corrected drape, and complete anatomically connected figure.
6. **Hair and ornament lock:** unchanged airy bob, crossed pins, and compressed
   cord with the same topology, ordering, attachment, loops, tails, and
   perspective; the existing compressed-cord Minor is preserved, not repaired
   or worsened.
7. **Presentation and artifact integrity:** unchanged full-body framing,
   background geometry, palette, line hierarchy, paint planes, hand-painted
   finish, and no seams, malformed anatomy, text, borders, logos, watermarks,
   photorealism, plastic smoothing, or v1.6 drift.

A candidate must pass every gate to be selectable. Record all findings even
after a failure. The existing eye-polish and compressed-cord Minors do not fail
a candidate when they remain materially unchanged from r01 A, but any new or
worsened drift does.

Among hard-gate passers, use quality-first judgment: prefer the strongest
localized correction, same-person read, natural body volume, and finished
image quality. The user makes the final selection. Do not select or promote a
reviewer's favorite automatically.

## Verification and Independent Review

Image-only verification must:

- verify the authoritative raw r01 A source and all six repository reference
  hashes before generation;
- prove the worktree-local Image 1 copy is byte-identical to the raw source and
  has PNG signature `89504e470d0a1a0a` and dimensions `PNG 1024x1536`;
- open both generation inputs and all five human-QA-only references at original
  detail, state each role, and keep them visible before the first call;
- record A, B, and C generation or request identifiers and their exact returned
  source paths;
- prove each saved candidate is byte-identical to its own distinct returned
  source, with recorded SHA-256, PNG signature, and `PNG 1024x1536` dimensions;
- structurally recover any missing PNG payload from the exact correlated
  completed `image_generation_end` item whose `result` begins with `iVBOR`;
  accept legacy `image_generation_call` only when that is the schema actually
  recorded, and never hand-copy base64 or match prompt text alone;
- verify that every completed generation used the immutable prompt by hashing
  the exact recorded `revised_prompt` bytes, including the final newline;
- inspect A, B, and C at original detail and inspect the six-column comparison;
- obtain an independent seven-gate review from a reviewer who did not generate
  the candidates;
- obtain one blind candidate-specific tie-break whenever executor and reviewer
  disagree about that candidate's eligibility;
- confirm all outputs remain ignored and the tracked worktree remains clean.

Do not run Node tests, Python tests, PDF builds, OCR, package validation,
integration gates, or release gates. No renderer, manifest, validator, audit,
application, release, or accepted asset changes in this pass.

## Selection and Promotion Boundary

If at least one candidate passes all seven hard gates, show the comparison and
relevant full-size candidates, report every finding, and ask the user to select
a passing A, B, or C, keep r01 A unchanged, or return to design.

If none pass, preserve all r01 and r02 evidence and return to design. Do not
start r03, repair, composite, promote, commit, push, merge, clean up, or relax
the scope automatically.

Selection does not authorize promotion. Any accepted-path change, durable
selection history, byte-identity promotion, integration, commit, or cleanup
requires a separate approved promotion design.

## Non-Goals

- no new view, camera, pose, expression, hair, ornament, outfit, background,
  light, palette, rendering, or finish design;
- no repair of r01 A's eye-polish or compressed-cord Minors;
- no hip, thigh, leg, stance, face, or ornament correction;
- no candidate-specific prompt, sibling chaining, automatic retry, r03,
  compositing, promotion, commit, push, merge, cleanup, or remote sync;
- no modification or deletion of existing r01 evidence or its worktree.

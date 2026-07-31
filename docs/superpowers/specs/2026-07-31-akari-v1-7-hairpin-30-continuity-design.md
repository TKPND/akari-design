# Akari v1.7 Hairpin-Side 30-Degree Continuity Design

Status: approved design, awaiting written-spec review.

Date: 2026-07-31.

## Summary

`V17-02` is the first angle-expansion checkpoint after promotion of the
Akari v1.7 intimate front baseline. It tests whether the accepted same-person
identity, adult age impression, quietly pleased expression, hair, ornament,
body balance, roomwear, and hand-painted finish survive a modest camera-angle
change.

The pass creates three independent full-body candidates from one identical
30-degree hairpin-side contract. It is a continuity probe, not a complete
45-degree reference, paired-view set, turnaround, or redesign.

## Generation Authority

The sole visual input supplied to image generation is:

`akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`

Its required SHA-256 is:

`64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`

This image controls the current v1.7 identity, age 25, face construction, eye
design, quietly pleased closed-mouth expression, short airy chestnut bob,
pale-blue crossed ornament and cord detail, body proportions, upper-to-lower
volume balance, stance, white T-shirt, pale-blue lounge shorts, bare feet,
warm apartment light, framing scale, palette, line hierarchy, and hand-painted
finish.

No candidate may be used as the input for another candidate. No v1.6 image,
prompt, proportion, accessory, outfit, palette, or manifest has positive
authority.

## Human QA References

Before generation, open these images at original detail alongside the current
v1.7 front authority. They support human judgment only and must not be passed
to image generation:

1. `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
   - SHA-256:
     `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`;
   - checks the inherited head-to-body ratio, upper-body restraint, healthy
     thigh volume, and neutral full-body balance.
2. `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
   - SHA-256:
     `6757e601d2cfd158c970ab701a876981ace837e669c313dec6d25c0c539ff4d6`;
   - checks deliberate outer lines, quiet interior lines, readable paint
     planes, adult-face direction, palette, and finish.
3. `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png`
   - SHA-256:
     `ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21`;
   - checks only the character-left cheek, bob silhouette, and perspective
     ordering of the hairpin-side ornament.

The inherited 45-degree image is not a composition, scale, body, expression,
outfit, palette, or rendering authority. Prior reproducibility work showed
that an old angle reference with a large character occupancy can leak its
framing into a new generation even when supplied only for topology. Keeping it
out of the generation input prevents that known failure mode.

## View Contract

The image shows Akari from exactly 30 degrees toward her character-left,
hairpin side:

- the virtual camera moves around Akari toward her character-left side;
- her ornament-side cheek and the complete pale-blue ornament are nearer the
  camera and more visible than in the accepted front image;
- her head, ribcage, pelvis, knees, and feet share one coherent 30-degree
  orientation;
- her head does not rotate independently back to a frontal face;
- her amber eyes track the camera naturally, preserving familiar eye contact;
- both eyes remain visible without enlarging the farther eye or flattening the
  face back toward front view;
- both hands, both legs, and both bare feet remain complete in frame;
- perspective overlap is natural and does not collapse the farther shoulder,
  hip, thigh, knee, ankle, or foot.

This is a camera-angle continuity test, not a new pose. Preserve the neutral,
nearly even standing balance, relaxed shoulders and arms, unlocked knees, and
quiet full-body presentation. Do not add contrapposto, a fashion-model hip
shift, a walking step, crossed legs, a pin-up posture, or a separate head turn.

## Locked Character and Image Design

All candidates preserve:

- the accepted v1.7 face outline, cheek volume, compact chin, nose language,
  adult age impression, restrained blush, and subtle lip color;
- eye size, opening, tilt, iris scale and density, amber color, highlight
  language, lash weight, brow shape, and low-contrast eye treatment;
- the small closed-mouth smile and the emotional beat of quietly becoming
  pleased after noticing the familiar viewer;
- the short airy chestnut bob, asymmetric looseness, irregular tips, crown
  volume, and low-gloss paint-plane treatment;
- one complete character-left ornament with two pale-blue crossed pins above
  a delicate thin cord bow, narrow loops, and two slim tails;
- v1.5 B3 head-to-body ratio, moderate upper-body volume, subtle waist,
  healthy thigh volume, limb length, hands, feet, and adult anatomy;
- the white T-shirt, pale-blue lounge shorts, and bare feet as comparison
  controls;
- a warm minimal apartment, directional domestic light, portrait dimensions,
  full-body scale, quiet framing, and hand-painted finish.

The angle may cause physically necessary overlap and foreshortening. It must
not become an excuse to reshape the face, narrow the torso, reduce the chest or
thighs, lengthen the legs, shrink the head, or polish the image into a generic
character sheet.

## Candidate Contract

Generate exactly three candidates, A, B, and C. Each candidate:

- starts independently from the accepted v1.7 front image;
- uses the same complete prompt and the same sole visual input;
- targets the same hairpin-side 30-degree view;
- has no candidate-specific expression, pose, styling, or angle delta;
- represents an independent reproducibility attempt, not a designed variant.

Generate serially. Do not overlap image-generation calls and do not use A as
an anchor for B, B as an anchor for C, or any other sibling chaining.

## Rejection Boundary

Reject a candidate for any of the following:

- wrong side, mirrored composition, missing, moved, duplicated, simplified,
  or invented ornament parts;
- a near-front view below the intended angle, a 45-degree or profile view, or
  different head and body angles;
- identity drift, younger or childlike impression, sharp V-line jaw, enlarged
  eyes, rounder or darker eyes, heavier lashes, eyeliner, makeup, or stronger
  blush;
- broad, open-mouth, teasing, smug, seductive, glamorous, or posed expression;
- smooth salon-finished round bob, bright Honey Brown hair, repeated glossy
  highlight bands, parallel-pin substitution, or loss of airy irregular tips;
- reduced upper-body volume, thin thighs, model elongation, exaggerated curves,
  pin-up stance, locked knees, twisted joints, broken hands, or broken feet;
- cropped T-shirt, culottes, smartwatch, socks, sneakers, jewelry, or another
  v1.6 or generic fashionable-girl signal;
- white studio background, cool uniform lighting, photorealistic skin,
  plastic smoothing, excessive detail, text, labels, borders, logos, or
  watermarks.

## Working Files

Keep all review-stage output under the ignored directory:

`build/v1.7-hairpin-30-continuity/`

Use these names:

- `akari-v1.7-v17-02-hairpin-30-r01-a.png`;
- `akari-v1.7-v17-02-hairpin-30-r01-b.png`;
- `akari-v1.7-v17-02-hairpin-30-r01-c.png`;
- `akari-v1.7-v17-02-hairpin-30-r01-comparison.png`.

The comparison contains the accepted v1.7 front authority plus candidates
A/B/C at equal character height. Labels identify `Front`, `A`, `B`, and `C`
without covering the images. It is review evidence, not a deliverable.

Do not modify the accepted front image, v1.5 B3, v1.4 references, ignored
V17-01 output, or any v1.6 material.

## Review and Selection

Inspect every candidate at original detail, then review the comparison in this
order:

1. same-person identity and age-25 impression;
2. correct character-left hairpin side and coherent 30-degree head/body view;
3. complete ornament topology and believable bob volume around the skull;
4. preservation of the accepted quietly pleased, familiar expression;
5. preservation of head-to-body ratio, upper-body volume, waist, thighs,
   limbs, neutral stance, and full-body scale;
6. intact hands, feet, clothing, lighting, background, palette, lines, paint
   planes, and absence of generation artifacts;
7. absence of v1.6, gyaru, generic polished-girl, childlike, glamorous, or
   character-sheet drift.

The pass succeeds only if at least one candidate clears every hard identity,
view, ornament, body, anatomy, and artifact gate. Among passing candidates,
prefer the strongest same-person read and most natural intimate eye contact,
not the most polished or conservative image.

The user makes the final selection. Do not promote the reviewer's favorite or
the least-bad candidate automatically. If no candidate passes, preserve all
r01 evidence and return to a design decision before defining r02. Do not run
an automatic correction generation.

## Verification Scope

Verification for this pass is image-only:

- open and state the role of the front authority and all three QA references
  before generation;
- verify the four recorded input hashes before the first call;
- record the source path or generation identifier for A, B, and C;
- verify every candidate has PNG signature `89504e470d0a1a0a`;
- verify every candidate is a valid portrait PNG and record dimensions and
  SHA-256;
- inspect every candidate at original detail;
- build and inspect the labeled equal-height comparison;
- confirm generated files remain ignored and no tracked file changes during
  the review pass.

If a generated image appears in the conversation without a local source PNG,
use the repository's structural rollout-payload recovery procedure. Never copy
a large base64 payload manually from terminal output.

Do not run Python tests, Node tests, PDF builds, OCR, release gates, or package
validation. No application, rendering, manifest, validator, or audit code is
changed.

## Non-Goals

- no exact 45-degree, profile, rear, opposite-side, or paired-view asset;
- no full turnaround, expression sheet, wardrobe pass, manifest, PDF, or
  release package;
- no change to the accepted v1.7 front image or its selected expression;
- no old angle image as a generation input;
- no promotion before explicit user selection;
- no r02 design or generation unless all r01 candidates fail and the observed
  failure is reviewed first.

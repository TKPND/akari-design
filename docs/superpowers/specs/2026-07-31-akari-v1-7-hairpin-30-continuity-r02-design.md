# Akari v1.7 Hairpin-Side 30-Degree Continuity r02 Design

Status: approved design.

Date: 2026-07-31.

## Summary

`V17-02 r02` repeats the hairpin-side 30-degree continuity probe after all
three r01 candidates failed a hard gate. Candidate A established the intended
camera side and approximate angle, but changed Akari's bust projection, waist
and hip contour, and neutral weight distribution. Candidates B and C kept the
body too frontal while turning the head farther.

r02 keeps the accepted v1.7 front as the only generation input and tightens
the body-volume and neutral-stance contract. It does not edit candidate A,
relax the 30-degree target, redesign Akari, or promote any review output.

## Authority and Reference Roles

The sole visual input supplied to image generation remains:

`akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`

Required SHA-256:

`64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`

It controls identity, adult age, expression, face, hair, ornament, body
volume, stance, outfit, bare feet, environment, framing, palette, lines,
paint planes, and finish.

The same v1.5 B3, v1.4 G2, and inherited hairpin-side 45-degree images from the
r01 design remain human-QA references only. They are opened before generation
but are not passed to image generation.

Candidate A from r01 may be opened only as negative human-QA evidence for the
body and stance failure. It is never supplied to generation, composited,
edited, or treated as a positive angle authority. Candidates B and C are also
not generation inputs.

No v1.6 material has positive or negative generation authority.

## Fixed View and Identity Contract

The requested view remains exactly 30 degrees toward Akari's character-left,
hairpin side. The virtual camera moves around the same standing Akari; Akari
does not turn into a new pose.

- Head, ribcage, pelvis, knees, and feet share one coherent 30-degree
  orientation.
- The character-left cheek and complete pale-blue ornament are nearer the
  camera.
- Both eyes remain visible and naturally track the camera.
- The head does not turn independently toward front.
- The accepted soft cheek volume, compact chin, restrained blush, eye scale,
  lash weight, quiet closed-mouth smile, and age-25 impression remain fixed.
- The short airy chestnut bob and complete crossed-pin plus cord-bow topology
  remain fixed.

Near-front bodies with a separately turned head fail the view gate even if the
face is attractive or strongly resembles the accepted front.

## Strengthened Body-Volume Contract

Treat the accepted front body as locked three-dimensional volume observed
from a new camera position, not as permission to restyle the silhouette.

- Preserve the same restrained bust volume and projection. Do not enlarge,
  lift, separate, emphasize, or add shading that makes the bust fuller.
- Preserve the same subtle waist. Do not pinch the waist, deepen the side
  curve, tighten the shirt around it, or increase the bust-to-waist contrast.
- Preserve the same pelvis and hip volume. Do not flare one hip, create an
  S-curve, or increase waist-to-hip contrast.
- Preserve the v1.5 B3-derived head-to-body ratio, moderate upper-body volume,
  healthy thigh volume, limb lengths, and adult hands and feet.
- Keep the white T-shirt's relaxed fall and the pale-blue lounge shorts as
  neutral comparison controls. Perspective overlap may change visible width,
  but not the underlying body volume or garment fit.

Any visible glamour increase, pin-up shaping, or body-volume change is a hard
failure even when angle, identity, and anatomy otherwise pass.

## Strengthened Neutral-Stance Contract

Preserve the accepted quiet, nearly even standing balance while rotating the
whole figure coherently in view.

- Keep shoulders and pelvis level, the spine quiet and near vertical, and the
  torso centered over the midpoint between both planted feet.
- Keep weight distributed nearly evenly across both legs.
- Keep both knees softly unlocked without advancing one leg into a pose.
- Keep both soles naturally planted and both feet complete.
- Preserve relaxed arms, soft elbows, and complete hands.

Reject contrapposto, lateral hip displacement, one-leg weight bearing,
fashion-model posture, walking, crossed legs, an S-curve, or a staged pin-up
stance. A coherent angle is not allowed to come from twisting body segments
against one another.

## Presentation Contract

Preserve the accepted warm minimal apartment, directional domestic light,
full-body portrait framing, breathing room, quiet palette, deliberate outer
lines, restrained interior lines, readable paint planes, and hand-painted
finish.

Do not increase blush, eyeliner, lashes, glossy eye highlights, lip color,
skin polish, hair gloss, or generic character-sheet finish. Do not introduce
v1.6, gyaru, childlike, glamorous, seductive, photorealistic, or fashion-model
signals.

## Candidate Contract

Generate exactly three independent candidates, A, B, and C:

- each starts from the accepted v1.7 front alone;
- each uses one identical complete r02 prompt;
- each targets the same hairpin-side 30-degree view;
- no candidate is used as an input or instruction source for another;
- calls run serially;
- no candidate-specific angle, body, pose, expression, or styling delta is
  added.

Use these ignored working paths:

- `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png`;
- `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-b.png`;
- `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-c.png`;
- `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-comparison.png`.

r01 evidence remains untouched in the same ignored directory.

## Review Order and Hard Gates

Inspect each full-size image, then the equal-height comparison, in this order:

1. accepted same-person identity and age-25 impression;
2. coherent character-left hairpin-side 30-degree whole-body view;
3. restrained bust, subtle waist, unchanged hip and thigh volume, and no
   glamour increase;
4. level shoulders and pelvis, nearly even weight, planted feet, and no
   contrapposto or S-curve;
5. complete ornament topology and believable airy bob volume;
6. accepted quietly pleased expression, eye treatment, and facial restraint;
7. intact anatomy, clothing, framing, background, light, palette, lines,
   paint planes, and absence of artifacts or v1.6 drift.

Reject immediately for any identity, view, body-volume, stance, ornament,
anatomy, or artifact failure. A candidate must pass every hard gate before
expression appeal or finish quality can break a tie.

The user makes the final selection. If no r02 candidate passes, preserve all
evidence and return to design. Do not generate r03, repair a candidate,
promote an image, or change the angle without a new user decision.

## Verification Scope

Use the same image-only verification procedure as r01: open and state all
reference roles, verify input hashes, record generation identifiers and source
paths, verify PNG signatures and dimensions, record SHA-256 values, inspect
every candidate at original detail, build and inspect the comparison, and
confirm outputs stay ignored with a clean tracked tree.

Do not run Node tests, Python tests, PDF builds, OCR, package validation, or
release gates. No application, renderer, manifest, validator, or audit code is
changed.

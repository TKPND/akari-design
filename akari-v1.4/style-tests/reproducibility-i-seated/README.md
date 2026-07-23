# Akari v1.4 — I seated reproducibility test

Date: 2026-07-23

## Decision carried into I

The user adopted **H-r03-1** at its generated scale. The near-full standing
framing is accepted as a valid composition, and no H-r04 mechanical
normalization retry will be performed.

The next planned reproducibility domain after standing was seated anatomy. I
therefore changes the pose and adds one chair, while retaining the accepted
v1.4 identity, roomwear, finish, lighting direction, and close portrait
presence.

## Selected composition

Akari sits naturally on a simple pale-oak armless chair in a minimal apartment
interior.

- eye-level ornament-side three-quarter view;
- complete head, hands, feet, and chair;
- pelvis visibly supported by the seat;
- one open hand resting on each thigh;
- knees and ankles separated and uncrossed;
- both soles and heels flat on the floor;
- white T-shirt, pale-blue lounge shorts, and bare feet;
- warm frame-left daylight;
- no numerical figure-height target and no mechanical shrinking.

The rejected alternatives were a forward-leaning low stool and floor sitting.
Both would add occlusion or overlap the existing rest-pose family.

See `DESIGN.md` and the exact shared prompt in `PROMPT.md`.

## Reference authority

1. `../line-refinement/akari-v14-g2-balanced-lines.png`
   controls large paint planes, line hierarchy, hair, skin, and clean finish.
2. `../reproducibility-h-r03/akari-v14-h-r03-1-standing-repro.png`
   controls the adopted adult face and eye balance, body volume, roomwear, and
   close portrait presence.
3. `../../references/v1.1/v1_1_髪飾り側_45deg.png`
   controls only character-left ornament topology and its three-quarter
   placement.

## Generation

- Built-in image generation.
- I-1, I-2, and I-3 were generated independently and concurrently.
- Every sample used the same `PROMPT.md`, the same three references, and the
  same reference order.
- Each sample used one generation call with no artistic retry.
- No I output was used as a reference for another I output.
- Shared prompt SHA-256:
  `694200f7867329f6bd207a8d2ed4aa3bb8f8a3acfb103dfb7f0381c58f33312a`.
- All outputs are 1024 × 1536, 8-bit true-color sRGB PNG files.

## Anatomy and composition review

All three samples pass the controlling seated-structure gates.

| Gate | I-1 | I-2 | I-3 |
| --- | --- | --- | --- |
| Complete head, hands, feet, and chair | Pass | Pass | Pass |
| Pelvis visibly seat-supported | Pass | Pass | Pass |
| Coherent hips, thighs, knees, and ankles | Pass | Pass | Pass |
| Both soles and heels grounded | Pass | Pass | Pass |
| Knees and ankles uncrossed | Pass | Pass | Pass |
| Human legs distinct from chair legs | Pass | Pass | Pass |
| Plausible visible hands and fingers | Pass | Marginal pass | Pass |
| Healthy thigh and calf volume | Pass | Pass | Pass |
| No forbidden props | Pass | Pass | Pass |
| Eye-level, non-glamour camera | Pass | Pass | Marginal pass |

Notes:

- I-1 has the cleanest overall prompt staging.
- I-2 has slightly less distinct finger articulation on the viewer-right hand
  and somewhat stiffer knee-to-calf contours, but neither is an anatomy
  failure.
- I-3 is the most frontal result, weakening the requested ornament-side
  three-quarter view without becoming a camera-angle failure.

Independent anatomy ranking:

- anatomy alone: **I-3 > I-1 > I-2**;
- composition and prompt staging: **I-1 > I-2 > I-3**;
- combined structure: **I-1 > I-3 > I-2**.

## Style, identity, and ornament review

All three samples remain viable v1.4 style passes.

| Sample | Paint planes | Line hierarchy | Hair | Fabric | Face/eyes | Clean finish | Adult age | Ornament | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| I-1 | 5 | 5 | 5 | 5 | 5 | 5 | Pass | Pass | Pass |
| I-2 | 4 | 4 | 5 | 4 | 5 | 4 | Pass | Pass | Pass |
| I-3 | 5 | 4 | 5 | 5 | 5 | 5 | Pass | Marginal pass | Pass |

Independent style ranking: **I-1 > I-3 > I-2**.

- I-1 most strongly preserves the large planes and deliberate line hierarchy.
  In the primary review its eyes read slightly cuter and younger than
  H-r03-1, but not enough to fail the adult-age gate.
- I-2 gives the calmest direct continuation of H-r03-1 in the primary review.
  It is slightly softer in the lit skin and shirt planes, with mild warm
  bloom, but identity and the canonical ornament remain intact.
- I-3 has a mature face and clean fabric treatment. It is smoother and more
  front-facing, and the ornament contains extra crossed strokes with a less
  explicit cord loop, so it is the weakest canonical-ornament read of the
  three.

Primary continuity preference: **I-2 > I-1 > I-3**.

The two rankings differ because the independent review prioritizes strict G2
plane and line fidelity, while the primary review prioritizes continuity from
the user-adopted H-r03-1 face, eyes, and calm adult balance.

## Result

The I seated reproducibility test **passes**.

All three samples pass both the seated-structure gate and the scoped v1.4
style gate. This is stronger than the minimum requirement of two passing
samples.

I-1 is the strict prompt/style leader. I-2 best preserves the calm adult face,
eyes, and overall balance carried forward from H-r03-1.

## User selection

The user formally selected **I-2** on 2026-07-23. It is the promoted seated
reference for Akari v1.4. This accepts its slightly softer paint planes and
minor hand-articulation weakness in exchange for the strongest continuity with
the adopted H-r03-1 standing reference.

The remaining planned reproducibility domain is J: one simple everyday action
in progress. I-2 may be used as the accepted seated/continuity authority, while
G2 remains the line-and-paint authority; J must not be generated by repeatedly
editing I-2.

## Files

- `akari-v14-i1-chair-seated-repro.png`
- `akari-v14-i2-chair-seated-repro.png`
- `akari-v14-i3-chair-seated-repro.png`
- `akari-v14-i-seated-comparison.png`
- `DESIGN.md`
- `PROMPT.md`

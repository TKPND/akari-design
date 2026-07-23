# Akari v1.2 Daily.1 D04 Morning Drink Fetch Design

**Date:** 2026-07-15

**Status:** Approved under the user's autonomous-completion delegation

**Scope:** D04 scene contract, independent A/B generation, Akari selection,
accepted-asset linkage, and Natural Form integration

## 1. Intent

Create the fourth Daily Wave 1 scene: Akari has left the curtain and is taking
a slow first walk from the bedroom toward a compact kitchenette to get a
drink. The scene continues the same quiet morning, white T-shirt, gray shorts,
sleepy face, reversible morning hair, and striped indoor socks established by
D02 and D03.

The image is about low-energy ordinary motion. It must not become a posed
walk-cycle plate, a stretching scene, or a drink-holding portrait.

## 2. Scene Boundary

Show a bedroom doorway or short domestic passage opening toward a restrained
kitchenette. The kitchenette is readable through cabinet, counter, or muted
appliance geometry, without an open refrigerator, visible sink routine,
bathroom mirror, or explanatory prop.

Akari does not yet hold a mug, glass, bottle, kettle, or food. Her direction,
sleepy gaze, and the kitchenette threshold communicate the action.

D04 must remain distinct from:

- D03's stationary low curtain touch;
- D05's route toward a washroom;
- D12's refrigerator-opening action.

## 3. Pose and Camera

Use a room-side front-biased three-quarter camera at natural standing height,
wide enough to keep the complete figure and threshold context visible.

Capture one slow, stable walking transfer:

- the leading foot is flat and carries readable weight;
- the trailing foot stays close to the floor with only a natural heel release;
- the pelvis remains supported between both legs;
- the knees do not cross or collapse inward;
- shoulders and arms show a small counter-swing;
- the head drifts slightly forward from morning inertia;
- gaze goes toward the kitchenette, never the viewer.

The stride is short. Do not create tiptoe balance, a long runway stride,
crossed legs, dangling feet, or motion blur that obscures anatomy.

## 4. Identity, State, and Outfit

Preserve the same naturally cute 25-year-old adult Akari:

- adult face and healthy body volume;
- short warm-brown bob with reversible just-awake disturbance;
- complete character-left pale-blue crossed pins and ribbon ornament;
- heavy but open sleepy-neutral eyes;
- relaxed brows, cheeks, and closed almost-neutral mouth;
- loose opaque white short-sleeve T-shirt;
- simple opaque gray shorts-style roomwear;
- warm-white mid-calf socks with exactly two thin pale-blue stripes.

The mood is routine waking inertia, never illness, fear, sadness,
intoxication, sensuality, dissociation, or fashion posing.

## 5. Humanization

Use exactly two primary Humanization elements:

1. the trailing-leg sock sits slightly lower with one light natural slouch;
2. the T-shirt hem and shoulder line shift subtly with the small walking
   counter-swing.

Do not add additional costume disorder or loose props.

## 6. Reference Contract

Use five visible accepted references, the generator maximum, in this order:

1. Accepted D03 controls same-morning room palette, diffused light, white
   T-shirt, gray shorts, reversible morning hair, and narrative continuity. It
   does not control the stationary curtain pose or exact bedroom arrangement.
2. Accepted C01 controls healthy standing volume, pelvis-to-leg support,
   proportion, and grounded weight. It does not control outfit, shoes, or
   turnaround stiffness.
3. Accepted C03 hairpin-side three-quarter controls adult identity, ornament,
   side contour, and three-quarter proportion. It does not control standard
   clothes, shoes, or alert presentation.
4. Accepted C06-1 controls adult face, morning-hair rendering, sleepy-neutral
   eyelids, brows, cheeks, gaze softness, and mouth state. It does not control
   crop, hoodie, pose, or background.
5. Accepted C07 standing controls two-stripe sock construction, ankle and foot
   volume, heel and toe shape, and believable floor contact. It does not
   control outfit or static stance.

No local candidate, comparison board, or legacy working path may be a
generation reference.

## 7. Asset and File Contract

Use asset ID `D04`, revision `r01`, descriptor `morning-drink-fetch`, and phase
`7`.

Durable accepted output:

```text
akari-v1.2/accepted/daily/morning/
akari-v1.2_d04_morning-drink-fetch_r01.png
```

Local review outputs:

```text
akari-v1.2/source/candidates/d04/r01/
akari-v1.2/comparisons/d04-r01/d04-r01-comparison.webp
```

Dependencies are D03, C01, C03, C05, C06, and C07. C05 remains an explicit
lineage dependency through accepted D03 and C06 even though the five-image
generation limit uses C06-1 as the direct face, hair, expression, and rendering
reference.

## 8. Generation and Retry Policy

Generate independent A and B with the same frozen prompt and ordered physical
references. A and B never reference one another.

Akari selects the strongest eligible candidate under the user's delegated
authority. Do not pause for another selection.

Generate C only when neither A nor B is eligible and their unresolved Blocker
or Major findings are either D04-scene failures or distinct candidate-local
generation failures with no shared non-scene controller. Do not generate C if
either A or B is eligible.

If both candidates expose the same non-scene structural controller for
identity, adult age, body, hair, expression, sock, foot, or contact, stop and
trace it to D03, C01, C03, C05, C06, or C07 instead of retrying the scene.
This distinction was activated after A mirrored the ornament while B alone
crossed the gait: separate candidate-local defects are not a Core regression.

Use a 1024 by 1536 target with accepted dimensions of 1020-1028 by 1532-1540.
Never resize, crop, pad, warp, mask, or composite a candidate into eligibility.

## 9. Acceptance Gates

Review original candidates and the comparison in order:

1. Identity;
2. Body;
3. State;
4. Continuity;
5. Rendering;
6. Production.

Hard reject:

- severe identity, adult-age, face, body-volume, or rendering drift;
- missing, fused, duplicated, disconnected, or untraceable limbs or joints;
- broken pelvis support, crossed-leg topology, twisted ankles, pointed toes,
  floating feet, or contradictory contact;
- missing, mirrored, relocated, duplicated, or redesigned ornament;
- wrong hair length, non-reversible hair, extreme bed head, wet hair, or wind;
- closed eyes, viewer focus, broad smile, open mouth, distress, intoxication,
  or sensual posing;
- wrong outfit, underwear exposure, shoes, slippers, bare feet, or wrong sock
  height or stripe count;
- stationary curtain touching, washroom or mirror staging, open refrigerator,
  held drink, long runway stride, high reach, or running;
- crop loss preventing head, hands, pelvis, legs, ankles, heels, toes, or floor
  contact review;
- text, logo, watermark, border, collage, grid, or multiple characters.

## 10. Verification and Completion

Extend the registry-driven Daily validator without changing frozen D01-D03
contracts. Add D04 asset, request, comparison command, edit gate, ordered review
records, accepted-linkage tests, and byte-identical promotion.

D04 is complete only when:

1. A and B were independently generated from the five accepted references;
2. every generated candidate has an ordered original-resolution review;
3. Akari selected exactly one eligible candidate;
4. selected source, recorded SHA-256, and accepted bytes agree;
5. `npm run gate:edit:d04` and `npm run gate:integration:v1-2` pass;
6. main is reverified and candidates/comparison remain local.

## 11. r02 Recovery Amendment

D04 r01 is closed without promotion. Original-resolution review found that A,
B, and C all converged on a crossed fashion-walk silhouette. A also mirrored
the ornament, but B and C preserved the accepted identity and still repeated
the same gait failure. The repeated controller is therefore `D04-scene`, not a
Core asset.

D04 r02 keeps the same five ordered accepted references and forbids every r01
candidate as a generation reference. It replaces the front-biased walking
view with a frame-right, side-profile-biased three-quarter view and a tiny
weight transfer on two visibly separate parallel floor lanes. Projected knees,
ankles, and feet require at least one sock-width of image-plane gap; the step
is less than one foot length; the leading foot is flat; and the trailing foot
stays behind and slightly outward with only a small heel release.

Initial r02 candidates are independent A and B. The durable output revision is
`r02`, local review evidence lives under `source/candidates/d04/r02/` and
`comparisons/d04-r02/`, and the accepted target becomes:

```text
akari-v1.2/accepted/daily/morning/
akari-v1.2_d04_morning-drink-fetch_r02.png
```

The r01 request, candidates, comparison, and rejected reviews remain as audit
history. All other identity, state, continuity, rendering, production, retry,
and delegated-selection rules stay unchanged.

# Akari v1.2 Daily.1 D05 Morning Washroom Route Design

**Date:** 2026-07-16

**Status:** Approved under the user's autonomous-completion delegation

**Scope:** D05 scene contract, independent A/B generation, Akari selection,
accepted-asset linkage, and Wave 1 closure

## 1. Intent

Create the fifth and final Daily Wave 1 scene: Akari is moving through the
short hall from the bedroom toward the washroom. The same quiet morning,
white T-shirt, gray shorts, sleepy-neutral face, reversible morning hair, and
striped indoor socks continue from D04.

The image is about an automatic low-energy route between rooms. It is not a
washroom routine, mirror portrait, grooming action, or second kitchenette
scene.

## 2. Scene Boundary

Show a short domestic hall ending at a closed or barely ajar frosted washroom
door. Cooler neutral threshold tile or restrained frosted glass may identify
the destination, but the washroom interior stays unreadable. Add no mirror,
sink, toilet, toothbrush, cosmetics, towel routine, readable sign, or running
water.

No kitchenette counter, open refrigerator, held drink, curtain contact, bed
edge action, or explanatory prop may carry the scene.

## 3. Pose and Camera

Use a hall-side rear-left three-quarter camera at natural standing height.
Akari moves away from the bedroom and deeper frame-right toward the frosted
door while her sleepy face remains readable in soft side three-quarter.

Capture a momentary slowdown rather than a stride:

- the leading foot is fully flat toward the washroom;
- the trailing foot remains flat or releases its heel only minimally;
- both feet use visibly separate parallel floor lanes;
- knees, ankles, and feet do not overlap or cross in image plane;
- the step is shorter than one foot length;
- pelvis, spine, and shoulders remain quietly supported;
- both arms hang with only a small natural counterbalance;
- gaze goes to the frosted door, never the viewer.

Keep the complete head, ornament, hands, pelvis, both legs, ankles, heels,
socked toes, and floor contact visible.

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

The state is ordinary waking inertia, never distress, illness, intoxication,
fear, sadness, sensuality, or dissociation.

## 5. Humanization

Use exactly two primary Humanization elements:

1. the character-right short-sleeve edge has one small accidental half-fold;
2. the back T-shirt hem sits slightly higher on one side with one shallow
   diagonal walking fold.

Do not add extra costume disorder, sock slouch, or loose props.

## 6. Reference Contract

Use five visible accepted references in this order:

1. Accepted D04 r02 controls the same-morning palette, bedroom-to-hall
   continuity, white T-shirt, gray shorts, socks, quiet light, and current
   movement state. It does not control the kitchenette, exact pose, crop, or
   r02 candidate history.
2. Accepted C02 controls healthy rear body volume, back silhouette, support,
   and adult proportion. It does not control hoodie, skirt, shoes, or rigid
   turnaround presentation.
3. Accepted C03 hairpin-side three-quarter controls adult identity, complete
   character-left ornament, visible side contour, and proportion. It does not
   control standard clothes or alert expression.
4. Accepted C06-1 controls adult face, reversible morning hair,
   sleepy-neutral state, palette, and rendering. It does not control crop,
   hoodie, or background.
5. Accepted C07 standing controls two-stripe socks, ankle and foot volume,
   relaxed toes, heel shape, and believable contact. It does not control
   static stance or outfit.

No local candidate, comparison, generated retry, or legacy path may be a
generation reference.

## 7. Asset and Retry Contract

Use asset ID `D05`, revision `r01`, descriptor `morning-washroom-route`, phase
`8`, and dependencies D04, C02, C03, C05, C06, and C07.

Durable accepted output:

```text
akari-v1.2/accepted/daily/morning/
akari-v1.2_d05_morning-washroom-route_r01.png
```

Local review outputs:

```text
akari-v1.2/source/candidates/d05/r01/
akari-v1.2/comparisons/d05-r01/d05-r01-comparison.webp
```

Generate independent A and B from the same frozen prompt and five accepted
references. Akari selects the strongest eligible candidate without pausing.
Generate C only when neither A nor B is eligible and the unresolved Blocker or
Major findings are scene-only or distinct candidate-local failures with no
shared non-scene controller. A shared D04, C02, C03, C05, C06, or C07 failure
reopens that controller instead of retrying the scene.

## 8. Acceptance and Completion

Review Identity, Body, State, Continuity, Rendering, and Production in that
order. Hard reject severe identity or adult-age drift, broken anatomy or
support, crossed or overlapping leg topology, wrong ornament or outfit,
incorrect sock stripes, closed eyes or viewer focus, washroom-routine props,
kitchenette staging, crop loss, text, logo, watermark, grid, collage, or
multiple characters.

D05 is complete only when one eligible candidate is promoted byte-for-byte,
every generated candidate has an ordered review, the D05 edit and v1.2
integration gates pass, main is reverified, local evidence is preserved, and
the five accepted morning scenes are recorded as `v1.2-Daily.1` Wave 1.

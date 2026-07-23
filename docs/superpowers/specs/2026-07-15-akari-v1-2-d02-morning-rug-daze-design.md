# Akari v1.2 Daily.1 D02 Morning Rug Daze Design

**Date:** 2026-07-15
**Status:** User-approved design
**Scope:** D02 generation contract, candidate production, review, acceptance,
and the reusable Daily scene workflow needed for `v1.2-Daily.1`

## 1. Objective

Create the first new post-Core Daily Wave 1 scene: Akari remains seated on a
rug for a while after waking, looking toward the window before she is ready to
move.

D02 follows D01 in the same morning and bedroom but must not repeat D01's
viewer-directed gaze or side-folded leg pose. The scene should communicate a
quiet, ordinary pause rather than sadness, illness, intoxication, sensuality,
or a posed portrait.

## 2. Decisions and Alternatives

The approved direction is a window-side continuation of D01.

- A bed-side repeat would preserve continuity but overlap too strongly with
  D01's staging.
- A living-room rug would create more novelty but weaken the immediate
  morning continuity.
- The selected window-side rug keeps the same bedroom and outfit while giving
  the gaze, light, pose, and negative space a distinct job.

The approved pose extends both legs loosely forward with one knee slightly
bent. This replaces D01's side-folded legs and keeps the complete support chain
available for review.

## 3. Scene Contract

### 3.1 Character and state

- Akari is the same naturally cute 25-year-old adult established by the
  accepted Natural Form assets.
- Preserve the character-left pale-blue crossed pins and ribbon-like ornament.
- Use the accepted C05 reversible morning hair range.
- Use C06-1 `sleepy-neutral` as the expression controller: heavy but open
  eyelids, relaxed brows and cheeks, a closed almost-neutral mouth, and no
  viewer engagement.
- Retain D01's frame-left window and frame-right bed relationship. Direct the
  gaze toward frame-left with incomplete focus and only a light head turn. It
  must not read as deliberate sightseeing, concern, crying, or dissociation.

### 3.2 Pose and camera

- Seat Akari on a low-contrast rug near the window.
- Extend both legs loosely forward and bend one knee slightly. Do not fold both
  legs to the side as in D01.
- Use a mild posterior pelvic tilt, coordinated back rounding, and dropped
  shoulders.
- Place one hand behind or slightly beside the pelvis as believable support.
  Rest the other hand loosely on a thigh.
- Keep both thigh roots, knees, shins, ankles, heels, and socked toes traceable.
- Use a front-biased three-quarter camera at natural seated viewing height,
  slightly wider than D01.
- Keep the complete head, ornament, both hands, pelvis, both legs, heels, and
  toes visible.

### 3.3 Outfit and humanization

- Continue D01's loose opaque white short-sleeve T-shirt.
- Continue D01's simple opaque gray shorts-style roomwear.
- Use warm-white mid-calf socks with exactly two thin pale-blue stripes.
- Limit the new Humanization elements to two:
  - the sock on the straighter extended leg has one light natural slouch;
  - the T-shirt hem sits slightly unevenly with believable seated wrinkles.
- Do not add sheer fabric, visible underwear, shoes, slippers, bare feet,
  decorative sleepwear, or body-emphasizing styling.

### 3.4 Room and lighting

- Continue D01's bedroom identity without copying its exact composition.
- Make the window-side rug the primary surface and visual anchor.
- Use soft curtain-filtered morning light from the direction of Akari's gaze.
- Retain only a restrained bed edge near a frame boundary to establish
  continuity.
- Do not add a phone, mug, clock, readable book, food, or explanatory prop.
- Keep background detail below the character and contact points in visual
  priority.

## 4. Asset and Storage Contract

Use asset ID `D02`, revision `r01`, and scene slug `morning-rug-daze`.

The tracked generation request is:

```text
akari-v1.2/manifest/generation-requests/d02-r01.yaml
```

Local candidate paths are:

```text
akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-a.png
akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-b.png
```

An optional candidate C, when permitted by the retry policy, uses the same
directory and the `r01-c.png` suffix.

The local comparison path is:

```text
akari-v1.2/comparisons/d02-r01/d02-r01-comparison.webp
```

The selected durable asset is promoted byte-for-byte to:

```text
akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png
```

Candidates and comparison images remain local and untracked. The selected
accepted PNG, request manifest, asset manifest entry, review record, workflow
support, tests, and design records may be tracked.

## 5. Reference Contract

Use five visible references with explicit, non-overlapping roles.

1. Accepted D01 controls only continuity of bedroom, morning light, white
   T-shirt, gray roomwear, and the established just-awake moment. It does not
   control the new pose, gaze, crop, or exact background arrangement.
2. Accepted C04 controls seated weight, pelvis support, coordinated torso
   response, healthy leg volume, traceable joints, and believable hand support.
   Do not copy its side-folded leg arrangement, hoodie, skirt, gaze, or
   background.
3. Accepted C05 controls adult identity, reversible morning hair, ornament,
   cheek shape, bob length, palette, and rendering. It does not control crop,
   hoodie, or expression.
4. Accepted C06-1 controls sleepy-neutral eyelids, brows, cheeks, focus, and
   mouth state. It does not control crop, clothing, pose, or room.
5. Accepted C07 seated controls sock height and stripes, ankle and foot volume,
   relaxed toes, heel placement, and rug contact. It does not control its
   clothing, crop, upper body, or expression.

Precedence is D01 for continuity, C04 for body mechanics, C05 for identity and
hair, C06-1 for facial state, and C07 seated for socks and feet. No local
candidate, comparison image, or legacy working path may be used as a
generation reference.

## 6. Generation and Retry Strategy

Generate independent candidates A and B from the same frozen request and the
same ordered references. A and B must not reference one another.

Do not generate C when A or B is eligible. C is allowed only when both initial
candidates fail for D02-scene staging, background, lighting, or presentation.
It uses the same identity, body, expression, outfit, reference, and production
contract.

If A and B share a structural identity, body, hair, expression, sock, foot, or
contact failure, stop D02 generation and trace the finding to D01, C04, C05,
C06, or C07 as appropriate. Repeated scene generation must not conceal a Core
regression.

The target canvas is 1024 by 1536 pixels. Reuse D01's narrow dimension
tolerance and byte-identical promotion rule rather than resizing, stretching,
padding, or warping an eligible source.

## 7. Acceptance and Hard Rejects

Review each original candidate and the comparison board in this order:

1. Identity;
2. Body;
3. State;
4. Continuity;
5. Rendering;
6. Production.

An eligible candidate has no unresolved Blocker or Major finding. The user
must explicitly select an eligible candidate before promotion.

Hard-reject a candidate for any of these:

- severe identity, adult-age, face, body-volume, or rendering drift;
- fused, missing, duplicated, disconnected, or untraceable limbs or joints;
- floating pelvis, contradictory hand support, or implausible whole-body
  weight;
- thin legs, broken knees, twisted ankles, pointed toes, or contradictory foot
  contact;
- missing, mirrored, relocated, duplicated, or redesigned ornament;
- wrong hair length, extreme bed head, wet hair, wind, or non-reversible hair;
- closed eyes, distress, intoxication, sensual posing, viewer-directed focus,
  broad smile, or emphasized open mouth;
- a repeated D01 side-folded leg pose instead of the approved D02 pose;
- wrong outfit, exposed underwear, shoes, slippers, bare feet, or incorrect
  sock height or stripe count;
- crop or scale that prevents complete support, hand, leg, or foot review;
- readable text, logo, watermark, border, collage, grid, or multiple character.

## 8. Daily Workflow Extension

D01-specific behavior must not be copied into a second isolated stack. Extract
or extend the smallest reusable Daily scene contracts needed for D02 while
preserving D01's frozen behavior.

The reusable boundary should cover:

- loading a declared Daily generation request;
- validating canonical candidate IDs and paths;
- validating A/B and optional C ordering;
- building a manifest-ordered comparison board;
- recording controller-aware findings and user selection;
- promoting one selected candidate byte-for-byte;
- validating source hash, accepted hash, and lifecycle status.

D01 retains `daily-validation` semantics and its existing Gate 4 linkage. D02
belongs to `v1.2-Daily.1` and must not modify the already released v1.2.0 Core
classification or checksum.

## 9. Verification Design

Use test-driven development for workflow changes. Tests must prove:

- the exact D02 asset, request, reference, candidate, and accepted path
  contracts;
- D01 remains valid and frozen after reuse is introduced;
- only A/B or A/B/C ordered candidate prefixes are accepted;
- optional C is blocked unless both A and B have eligible scene-only failure
  records;
- structural failures identify their controlling accepted asset;
- accepted status requires one explicit eligible selection;
- selected source, promoted file, recorded SHA-256, and accepted path agree;
- path traversal and symlink escapes remain rejected;
- v1.2.0 Core release artifacts and classification remain unchanged.

After manifest or workflow changes, run the focused tests and
`npm run validate:v1-2`. After Markdown changes, run `npm run lint:md`. Before
claiming D02 complete, also run the relevant full Node and Python suites, the
Natural Form audits, and `git diff --check` on the final integrated state.

## 10. Completion Contract

D02 is complete only when:

1. The reusable Daily request, comparison, review, promotion, and validation
   path is implemented without changing D01 or v1.2.0 outcomes.
2. A and B are generated independently from the approved visible references.
3. Every generated candidate has a complete ordered review.
4. The user explicitly selects an eligible candidate.
5. The selected source is promoted byte-for-byte and its SHA-256 is recorded.
6. The accepted D02 asset is registered as the first new `v1.2-Daily.1`
   morning scene.
7. The required tests, validators, audits, Markdown checks, and final-state
   checks pass.

No candidate is accepted merely for being the best of a weak set.

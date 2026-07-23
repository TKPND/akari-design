# Akari v1.2 Daily.1 D03 Morning Curtain Pause Design

**Date:** 2026-07-15

**Status:** Approved by the user's autonomous-execution delegation

**Scope:** D03 scene contract, reusable Daily validation extension, candidate
production, Akari quality-first selection, acceptance, and integration

## 1. Objective

Create the third Daily Wave 1 scene: Akari has stood up and reached the closed
curtain, but pauses for one quiet beat before opening it.

D03 continues the same morning and bedroom as D01 and D02 while changing the
body task from sitting to relaxed standing. It must read as ordinary waking
inertia, not sadness, fear, illness, intoxication, sensuality, or a posed
portrait.

## 2. Direction and Alternatives

The selected direction is a room-side three-quarter view of Akari standing at
the closed curtain, lightly touching its edge without pulling it open.

- A back view would emphasize the window but weaken face, expression, and
  ornament review.
- A close upper-body crop would make the hand and curtain readable but would
  lose standing weight, socks, and foot contact.
- The selected full-body three-quarter direction preserves the whole support
  chain while keeping the curtain action and sleepy face readable.

The curtain remains fully closed. D03 captures the hesitation before the
action, leaving the actual opening outside the frame and avoiding overlap with
D04's drink-fetching movement or D05's walk toward the washroom.

## 3. Scene Contract

### 3.1 Character and state

- Akari is the same naturally cute 25-year-old adult established by accepted
  Natural Form assets.
- Preserve the character-left pale-blue crossed pins and ribbon-like ornament.
- Use accepted C05 reversible morning hair.
- Use C06-1 `sleepy-neutral`: heavy but open eyelids, relaxed brows and cheeks,
  a quiet closed almost-neutral mouth, and incomplete focus.
- Direct her gaze toward the curtain edge or the dim light behind it, never at
  the viewer.
- The moment reads as slow waking inertia, not concern, crying, dissociation,
  reluctance caused by danger, or deliberate sightseeing.

### 3.2 Pose and camera

- Stand Akari near the frame-left closed curtain, viewed from inside the room.
- Use a room-side, front-biased three-quarter camera at natural standing height.
- Keep her body mostly upright but relaxed: slight forward head drift, dropped
  shoulders, and a small asymmetry through the hips.
- Place most weight over the leg farther from the curtain. Keep the
  curtain-side knee softly unlocked and that foot slightly behind or outward.
- The curtain-side hand lightly touches or pinches the curtain edge at about
  lower-chest height without pulling it open. The other arm hangs naturally.
- Avoid a high reach, stretched torso, theatrical contrapposto, walking stride,
  crossed legs, tiptoe balance, or leaning body weight into the curtain.
- Keep the complete head, ornament, both hands, pelvis, both legs, ankles,
  heels, and socked toes visible with believable floor contact.

### 3.3 Outfit and humanization

- Continue D01 and D02's loose opaque white short-sleeve T-shirt.
- Continue simple opaque gray shorts-style roomwear.
- Use warm-white mid-calf socks with exactly two thin pale-blue stripes.
- Limit the scene to two Humanization elements:
  - one light natural slouch on the softly unlocked leg's sock;
  - a small curtain-side shoulder and T-shirt hem asymmetry caused by the low,
    relaxed arm lift.
- Do not add sheer fabric, visible underwear, shoes, slippers, bare feet,
  decorative sleepwear, or body-emphasizing styling.

### 3.4 Room and lighting

- Continue D02's bedroom identity and frame-left window location without
  copying D02's seated composition.
- Keep the curtain fully closed with only soft diffused morning light passing
  through it. Do not show a bright open window gap.
- Retain a restrained bed or rug fragment near a frame boundary only as a
  continuity cue.
- Do not add a mug, phone, clock, readable book, food, slippers, or explanatory
  prop.
- Keep background detail below the character, hand-curtain contact, feet, and
  floor contact in visual priority.

## 4. Asset and Storage Contract

Use asset ID `D03`, revision `r01`, and descriptor
`morning-curtain-pause`.

Tracked request:

```text
akari-v1.2/manifest/generation-requests/d03-r01.yaml
```

Local candidates:

```text
akari-v1.2/source/candidates/d03/r01/akari-v1.2_d03_morning-curtain-pause_r01-a.png
akari-v1.2/source/candidates/d03/r01/akari-v1.2_d03_morning-curtain-pause_r01-b.png
```

Optional C, when allowed, uses the same directory and the `r01-c.png` suffix.

Local comparison:

```text
akari-v1.2/comparisons/d03-r01/d03-r01-comparison.webp
```

Accepted destination:

```text
akari-v1.2/accepted/daily/morning/akari-v1.2_d03_morning-curtain-pause_r01.png
```

Candidates and comparison images remain local and untracked. The selected PNG
is promoted byte-for-byte. Durable manifests, tests, docs, and the accepted
asset are tracked.

## 5. Reference Contract

Use five visible accepted references with non-overlapping roles. The image
tool accepts at most five physical references, so C06-1 consolidates the
morning-hair, expression, and rendering roles inherited from accepted C05.

1. Accepted D02 controls bedroom, closed-curtain location, soft morning light,
   white T-shirt, gray roomwear, and same-morning continuity. It does not
   control pose, crop, gaze, or exact room arrangement.
2. Accepted C01 controls healthy standing volume, relaxed full-body support,
   pelvis-to-leg continuity, and floor contact. It does not control shoes,
   hoodie, skirt, or alert expression.
3. Accepted C03 hairpin-side three-quarter controls three-quarter adult
   identity, ornament placement, body proportion, and readable side contour.
   It does not control outdoor shoes, standard outfit, or rigid turnaround
   posture.
4. Accepted C06-1 controls adult identity, reversible morning hair, cheek
   shape, bob length, palette, rendering, sleepy-neutral eyelids, brows,
   cheeks, focus, and mouth state. It does not control crop, clothing, pose,
   or room. Its accepted dependency on C05 preserves the C05 lineage.
5. Accepted C07 standing controls sock height and stripes, ankle and foot
   volume, relaxed toes, heel placement, and floor contact. It does not
   control its outfit, crop, or upper body.

Precedence is D02 for room continuity, C01 for standing mechanics, C03 for
three-quarter identity and proportion, C06-1 for morning hair, expression,
and rendering, and C07 standing for socks and feet. Local candidates,
comparison boards, and legacy working paths are forbidden as references.

## 6. Generation and Retry Strategy

Generate independent candidates A and B from the same frozen request and the
same ordered references. A and B never reference one another.

Akari selects the strongest eligible candidate under the user's explicit
autonomous-execution delegation. No additional user selection pause is
required.

Do not generate C when A or B is eligible. C is allowed only when both initial
candidates fail for D03-scene staging, curtain state, background, lighting, or
presentation. Use the same frozen contract for C.

If A and B share a structural identity, standing-body, hair, expression, sock,
foot, or contact failure, stop D03 generation and trace the finding to D02,
C01, C03, C05, C06, or C07. C05 remains a dependency through the accepted C06
lineage. Repeated scene generation must not conceal a Core
or accepted-Daily regression.

Use a 1024 by 1536 target canvas with accepted dimensions of 1020-1028 by
1532-1540. Never resize, crop, stretch, pad, warp, mask, or composite a source
to force eligibility.

## 7. Acceptance and Hard Rejects

Review each original candidate and the comparison in this order:

1. Identity;
2. Body;
3. State;
4. Continuity and curtain action;
5. Rendering;
6. Production.

An eligible candidate has no unresolved Blocker or Major. Quality-first
selection prioritizes expression read, character appeal, natural standing
weight, hand-curtain clarity, and finished image quality after all hard gates
pass.

Hard-reject:

- severe identity, adult-age, face, body-volume, or rendering drift;
- fused, missing, duplicated, disconnected, or untraceable limbs or joints;
- floating weight, broken pelvis-to-leg support, twisted ankles, pointed toes,
  or contradictory foot contact;
- missing, mirrored, relocated, duplicated, or redesigned ornament;
- wrong hair length, extreme bed head, wet hair, wind, or non-reversible hair;
- closed eyes, distress, sensual posing, intoxication, viewer-directed focus,
  broad smile, or emphasized open mouth;
- curtain visibly opened, a bright open gap, a high reaching stretch, walking
  stride, crossed legs, tiptoe balance, or body weight hanging from the fabric;
- wrong outfit, exposed underwear, shoes, slippers, bare feet, wrong sock
  height, or wrong stripe count;
- crop preventing complete hand, pelvis, leg, ankle, heel, toe, or floor-contact
  review;
- readable text, logo, watermark, border, collage, grid, or multiple character.

## 8. Reusable Daily Workflow Extension

Extend the D02 Daily workflow to register D03 without changing frozen D01 or
D02 outcomes. Keep exact per-scene manifest contracts, but make review
provenance, optional-C eligibility, dimension checks, ordered review prefixes,
and byte-identical promotion operate over every registered Daily asset rather
than a D01/D02-only branch.

The validator must derive each Daily scene controller as `<asset-id>-scene`
and allow controlling sources declared by that asset's dependencies. Existing
D01 compatibility messages and D02 behavior remain frozen.

## 9. Verification Design

Use TDD. Tests prove:

- exact D03 asset, dependency, request, reference order, prompt hash, paths,
  dimensions, candidate policy, gates, and hard rejects;
- D01 and D02 remain valid and unchanged;
- registered Daily scenes share ordered A/B or A/B/C lifecycle rules;
- optional C requires rejected A and B with unresolved scene-only Blocker or
  Major findings;
- structural findings name a declared controlling asset;
- accepted D03 has exactly one eligible selected review;
- selected source, SHA-256, promoted bytes, and accepted path agree;
- the Core PDF and release pins remain unchanged;
- candidates and comparisons remain untracked.

Run focused Daily tests during edits, then `npm run gate:edit:d02` until a D03
named edit gate exists. Before integration, run `npm run gate:integration:v1-2`,
tracked Markdown lint, and `git diff --check` serially.

## 10. Completion Contract

D03 is complete only when:

1. The registered Daily workflow supports D03 without changing D01 or D02.
2. A and B are generated independently from the five visible references.
3. Every generated candidate has an original-resolution ordered review.
4. Akari selects the strongest eligible candidate under delegated authority.
5. The selected PNG is promoted byte-for-byte with matching SHA-256 evidence.
6. D03 is accepted as the third Wave 1 morning scene.
7. Focused and integration gates pass on the integrated branch.

No candidate is accepted merely for being the best of a weak set.

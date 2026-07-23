# Akari v1.2 D01 Morning Validation Design

**Date:** 2026-07-15
**Status:** User-approved design
**Scope:** D01 generation contract, candidate production, review, acceptance,
and the final Natural Form Gate 4 decision

## 1. Objective

Create and accept one D01 morning-bedside illustration that proves the
accepted Natural Form Core assets work together in a daily scene:

- C04 r01 floor-sitting body mechanics;
- C05 r01 reversible morning bed hair;
- C06-2 r01 sleepy-secure expression;
- C07 r01 seated indoor sock-foot construction.

D01 is an integration validation asset, not a wallpaper or a new independent
pose standard. Leg structure, pelvis support, weight, and socked-foot contact
remain more important than background polish, lighting effects, or decorative
props.

## 2. Completion Contract

D01 is complete only when all of the following are true:

1. The exact generation, comparison, review, and lifecycle contracts are
   implemented and validated.
2. Two independent initial candidates, A and B, have been generated from the
   same ordered reference set without using one another as references.
3. Every candidate is reviewed in Identity, Body, State, Rendering, and
   Production order.
4. The user explicitly selects an eligible candidate ID.
5. The selected source is promoted byte-for-byte to the declared accepted
   path and its SHA-256 is recorded.
6. Gate 4 and the final Natural Form release classification are recorded from
   the observed findings.
7. The required tests, validator, audit, and Markdown checks pass on the final
   integrated state.

No candidate may be promoted merely because it is the best of a weak set. An
eligible candidate has no unresolved Blocker or Major finding.

## 3. Approved Scene Design

### 3.1 Character and state

- Akari remains the same naturally cute 25-year-old adult established by the
  accepted Natural Form assets.
- Keep the character-left pale-blue crossed pins and ribbon-like ornament.
  D01 remains a strict Core integration check; hairpin-free morning imagery is
  deferred to post-Gate-4 Daily work.
- Use the C06-2 `sleepy-secure` expression: heavy but not closed eyelids,
  incomplete focus, relaxed brows and cheeks, and a quiet closed mouth without
  a visible smile.
- Use the accepted C05 range of small crown flyaways, asymmetric bang
  separation, slight lower-bob irregularity, and one cheek-side strand. Do not
  turn the reversible morning state into a different or longer hairstyle.

### 3.2 Pose and camera

- Seat Akari on the rug beside the bed in the accepted C04 floor-sitting
  mechanical family.
- Use a front-biased light three-quarter camera at a natural seated viewing
  height.
- Keep the pelvis visibly supported, with a slight posterior tilt, coordinated
  back rounding, dropped shoulders, and one believable supporting hand.
- Keep a traceable front and rear leg from thigh root through knee, shin,
  ankle, heel, and relaxed socked toes.
- Direct the gaze generally toward the viewer while retaining incomplete
  sleepy focus. The pose must read as a moment after waking, not a deliberate
  portrait pose.
- Keep the complete head, ornament, both hands, both legs, heels, and socked
  toes visible.

### 3.3 Outfit

- Loose opaque white short-sleeve T-shirt.
- Simple opaque gray shorts-style roomwear.
- Warm-white mid-calf socks with exactly two thin pale-blue stripes.
- No hoodie, skirt, shoes, slippers, visible underwear, sheer material, or
  decorative sleepwear.
- Clothing must respond to the seated body and gravity without obscuring the
  pelvis-to-leg structure required for review.

### 3.4 Room and lighting

- Use a low-contrast rug as the primary contact surface.
- Show only a restrained edge of the bed and slightly rumpled bedding.
- Use soft morning natural light filtered through an implied or lightly shown
  curtain.
- Keep room information at medium density: clearly a lived-in bedroom, neither
  sterile nor cluttered.
- Do not add a clock, phone, mug, readable book, or other explanatory prop.
  The character, posture, hair, expression, and light must communicate morning
  without a prop.
- Background contrast, edges, and detail must not hide the legs, hands, feet,
  or body support.

## 4. Image Size Policy

The generation target is 1024 by 1536 pixels.

- Widths from 1020 through 1028 pixels are acceptable.
- Heights from 1532 through 1540 pixels are acceptable.
- A candidate inside both ranges must not receive a finding solely for its
  numeric size difference.
- Do not resize, stretch, crop, pad, or warp an otherwise eligible candidate
  merely to force exact target dimensions.
- A size or crop issue becomes a finding only when it materially prevents
  identity, body, state, contact, or composition review.
- The accepted file remains byte-identical to the selected candidate, even
  when the source is within tolerance rather than exactly 1024 by 1536.

This tolerance applies to D01 only and does not silently change existing Core
asset contracts.

## 5. Reference Contract and Precedence

The generation request uses exactly four ordered references.

1. `accepted_c04_floor_sitting_body`
   - Path: accepted C04 r01.
   - Controls pelvis contact, posterior tilt, back response, front/rear leg
     trace, hand support, healthy leg volume, and seated weight.
   - Does not control D01 clothing, face state, hair state, or room.
2. `accepted_c05_morning_hair`
   - Path: accepted C05 r01.
   - Controls adult face identity, reversible morning hair range, ornament
     structure, cheek shape, bob length, palette, and rendering.
   - Does not control its chest-up crop, hoodie, blank background, or exact
     facial expression.
3. `accepted_c06_sleepy_secure_expression`
   - Path: accepted C06-2 r01.
   - Controls coordinated eyelid weight, incomplete focus, relaxed brows and
     cheeks, and closed sleepy-secure mouth state.
   - Does not control crop, hoodie, body, pose, or room.
4. `accepted_c07_seated_sock_feet`
   - Path: accepted C07 seated r01.
   - Controls sock height, exactly two pale-blue stripes, ankle and foot
     volume, relaxed toes, contact, and seated lower-leg construction.
   - Does not control hoodie, skirt, upper body, face, or expression.

When references appear to conflict, use this precedence by concern:

- body mechanics and support: C04;
- morning hair and ornament: C05;
- facial state: C06-2;
- socks, ankles, feet, and floor contact: C07 seated.

No legacy working path is a generation reference. No C04 through C07 local
candidate or comparison image is a generation reference.

## 6. Generation Strategy

### 6.1 Initial candidates

Generate two standalone candidates from the same frozen request:

- `d01-r01-a`;
- `d01-r01-b`.

Each call creates a new D01 scene from the four ordered accepted references.
Candidate A must not become a reference for B, and B must not become a
reference for A. The prompt, reference order, roles, and hard rejects remain
identical between the two calls.

Canonical candidate paths are:

```text
source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-a.png
source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-b.png
```

### 6.2 Optional candidate C

Do not generate C when A or B is eligible.

Candidate C is permitted only when the failure is D01-specific staging,
background, lighting, or presentation and the underlying Core rules remain
valid. C uses the same four accepted references and frozen identity, body,
state, outfit, and size contract. Its canonical ID and path are:

```text
d01-r01-c
source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-c.png
```

If A and B share a structural body, hair, expression, or foot failure, stop
D01 candidate generation and trace the issue to C04, C05, C06, or C07. Do not
use repeated D01 regeneration to conceal a Core failure.

## 7. Prompt Boundaries and Hard Rejects

The frozen shared prompt must state each reference role, the precedence rules,
the approved scene, and the following prohibitions.

Hard-reject a candidate for any of these:

- severe identity, age, face, body-volume, or rendering drift;
- fused, missing, duplicated, disconnected, or untraceable limbs or joints;
- floating pelvis or hand support that contradicts the body's weight;
- thin legs, twisted ankles, pointed ballet toes, or contradictory foot
  contact;
- missing, mirrored, relocated, duplicated, or materially redesigned
  ornament;
- non-reversible hair, wrong hair length, extreme bed head, wet hair, or wind;
- expression outside the C06-2 sleepy-secure range, including closed eyes,
  distress, intoxication, sensual posing, broad smile, or open-mouth emphasis;
- wrong outfit, sheer clothing, exposed underwear, sexualized framing, shoes,
  slippers, bare feet, or incorrect sock stripes;
- crop or scale that prevents review of the complete body support or feet;
- readable text, logo, watermark, border, collage, grid, or multiple character.

## 8. Comparison and Review Workflow

Add a D01-specific comparison command that reads the declared candidates and
renders A and B, or A through C, in manifest order. Reuse the existing grid
renderer rather than creating a new general layout framework.

The builder must enforce:

- candidate IDs and suffixes match;
- canonical D01 source directory and filename order;
- two initial candidates and at most one optional C candidate;
- no absolute paths, parent traversal, directory symlink escape, or file
  symlink escape;
- every source file exists before rendering.

Review each original-resolution source as well as the comparison board. Use
this order and stop on a Blocker:

1. Identity;
2. Body;
3. State;
4. Rendering;
5. Production.

For D01 Body review, inspect pelvis, thigh roots, knees, shins, ankles, heels,
toes, hand support, and whole-body weight in that order. Presentation quality
must not compensate for a structural failure.

Every finding records:

- severity and category;
- observed evidence;
- whether it is resolved;
- controlling source asset: C04, C05, C06, C07, or `D01-scene`;
- recommended next action.

## 9. Review and Acceptance Rules

- `accepted` requires no unresolved Blocker, Major, or Minor finding.
- `accepted-with-notes` is allowed only when C01 through C07 remain strictly
  accepted and D01 has only unresolved D01-scene Minor findings.
- An unresolved Core-derived Minor is not silently reclassified as a scene
  note; it must be traced to its controlling asset and evaluated there.
- Rejected and superseded candidates remain recorded in the review log.
- The user must explicitly select one eligible candidate ID before promotion.
- Promotion copies only the selected PNG to:

```text
accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png
```

- Confirm source-to-accepted equality with `cmp` and matching SHA-256.
- Record the selected candidate ID, source path, source SHA-256, decision, and
  final status in the review log.
- Candidate and comparison outputs remain local-only unless the user asks to
  preserve them in git. The accepted PNG, generation request, validator,
  tests, scripts, manifest updates, and durable design records may be tracked.

## 10. Manifest and Validator Contract

Add `manifest/generation-requests/d01-r01.yaml` and make D01 a first-class
validated generation request.

The validator must enforce:

- exact D01 static asset contract: descriptor, phase, variant, expected path,
  dependencies, and gate;
- exact ordered four-reference contract and accepted paths;
- strict accepted revisions C04 r01, C05 r01, C06 r01, and C07 r01;
- C06 expression reference is specifically C06-2 r01;
- exact shared prompt, size policy, candidate policy, paths, acceptance gates,
  and hard rejects;
- candidate count is A/B or A/B/C in that order;
- review entries match the declared candidate IDs and paths;
- status and revision transitions are valid;
- accepted or accepted-with-notes D01 has exactly one matching accepted review;
- accepted source SHA-256 matches the selected candidate and accepted file;
- accepted-with-notes satisfies the D01-only Minor restriction.

Existing C01 through C07 contracts and local-only evidence must remain
unchanged.

## 11. Test Design

Use test-driven development. Add failing tests before production changes for:

1. exact D01 asset and request contracts;
2. exact dependency revisions and accepted paths;
3. ordered reference roles and C06-2 selection;
4. A/B and optional C candidate declarations;
5. target-size success and each boundary of the plus-or-minus-four-pixel
   tolerance;
6. rejection just outside the tolerance only when the validator is given a
   real candidate file for dimension inspection;
7. lifecycle linkage and review ordering;
8. accepted-with-notes restrictions;
9. canonical comparison paths, suffix binding, traversal, and symlink escape;
10. byte-identical promotion and SHA-256 linkage;
11. D01 rejection when any controlling Core dependency is not strictly
    accepted;
12. regression coverage proving C01 through C07 behavior is unchanged.

Dimension tests must reflect the approved policy: dimensions inside tolerance
pass without a finding. A D01 r01 candidate outside either tolerance range is
not eligible for promotion under this request and must fail the production
dimension check with a clear error.

## 12. Gate 4 and Release Decision

After D01 review, record one of these outcomes:

- **Release:** D01 is accepted and all required gates pass.
- **Conditional Release:** D01 is accepted-with-notes with only allowed
  D01-scene Minor findings and C01 through C07 remain accepted.
- **Hold:** D01 exposes an unresolved Core Blocker or Major, or no eligible D01
  candidate exists.

A Hold must name the controlling Core asset and next action. A Release or
Conditional Release may update the package status from pre-production only
after the validator, audit, and final acceptance checks pass.

## 13. Verification and Integration

Before calling D01 complete, run at least:

```sh
npm run test:node
npm run test:python
npm run validate:v1-2
npm run audit
npm run lint:md
```

Also run the focused D01 comparison, generation-contract, dependency,
lifecycle, and acceptance tests introduced by the implementation plan.

Before integrating, verify:

- the selected candidate and accepted PNG are byte-identical;
- their SHA-256 values match the review record;
- image dimensions fall within the approved D01 tolerance;
- exactly one D01 r01 review is accepted or accepted-with-notes;
- Gate 4 and the release classification agree with the findings;
- C04 through C07 local candidate and comparison evidence is unchanged;
- D01 local candidate and comparison evidence is preserved before any
  worktree cleanup.

Do not push unless the user separately requests it. Final integration and
cleanup occur only after user selection, final review, and verification.

## 14. Non-goals

- Hairpin-free morning Akari.
- Additional morning scenes beyond D01.
- Wallpaper composition or decorative room illustration.
- Reworking accepted C01 through C07 without a traced D01 structural finding.
- Changing existing Core dimensions or accepted-with-notes rules.
- A general comparison-framework rewrite.
- A Natural Form release PDF.
- Pushing branches or main.

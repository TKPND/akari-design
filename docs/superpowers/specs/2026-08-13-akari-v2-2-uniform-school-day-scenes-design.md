# Akari V2.2 Uniform School-Day Scene Set Design

Date: 2026-08-13
Status: approved for execution

## Goal

Create a coherent four-image Akari V2.2 mini-series following one school day,
while keeping one uniform design fixed and changing only the situation,
lighting, action, framing, and expression. Identity stability has priority over
camera variety, so every requested scene stops at a face-readable knee-up crop.

## Approved direction

- Series arc: morning commute, daytime classroom, after-school corridor, and
  evening walk home.
- Camera range: chest-up through knee-up; no full-body image in this first set.
- Uniform: white short-sleeve blouse under a navy jumperskirt dress.
- Standard school prop: a plain navy school bag when the scene calls for it.
- Rendering: one clean, soft Akari V2.2 illustration style with unified light,
  line density, and paint density across person and environment.
- Each scene is generated independently from the canonical portrait. No
  generated face is passed into a later generation call.

## Alternatives considered

1. **Independent generation with two transition gates — selected.** This adds
   the uniform before changing the setting, then changes the setting before
   starting the four-image set. It spends more review steps but makes identity
   drift easier to localize.
2. **Go directly to the station scene.** This is faster, but changes wardrobe
   and setting together, so a failed face gives weaker diagnostic evidence.
3. **Transfer a previously approved generated image as a continuity anchor.**
   This could strengthen clothing continuity, but the previous successful T02
   was not approved for anchor transfer. It is not used in this set.

## Reference and continuity contract

- Sole generation input for the transition gates and four requested scenes:
  `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`.
- The canonical portrait is the sole authority for face, eyes, brows, cheeks,
  mouth, bangs, low side ponytail, blue tie, and exactly one blue capsule
  hairpin on viewer-right.
- The canonical full-body image, previous P00/T01/T02 outputs, accepted daily
  scenes, GPT Pro examples, and local composition images are not generation
  inputs for this route.
- The earlier approved P00 may be reused only as a face-comparison control if
  its recorded file and hash still verify. It never becomes Image C or a
  continuity anchor.
- Wardrobe continuity is expressed by the same short clothing specification in
  each prompt, not by forwarding a face-bearing image.

## Transition gates

The two diagnostics do not count toward the requested four images.

### U00 — wardrobe transition

Keep the successful knee-up, shallow three-quarter kitchen composition,
cheerful expression, gaze, morning light, and simple presenting gesture. Change
only the clothing to the approved white short-sleeve blouse and navy
jumperskirt. Do not add the school bag or another new prop at this stage.
Generate one candidate, build the four-panel identity comparison, and stop for
identity review.

### U01 — scene transition

After U00 identity approval, keep the uniform, face-readable knee-up distance,
head angle, gaze, and cheerful expression. Change only the setting and action:
Akari pauses at a quiet station platform in clear morning light with one hand
resting naturally on her bag strap. Generate one candidate, build the identity
comparison, and stop for identity review.

U00 or U01 stops the route if the candidate is an obvious mismatch, cannot be
compared at its native face detail, or the user rejects or defers identity.
Neither gate candidate is forwarded as a later image input.

## Four-scene composition table

| ID | Time and place | Framing and action | Expression and light |
| --- | --- | --- | --- |
| S01 | Morning station | Knee-up shallow three-quarter; one hand on the navy bag strap | Bright open smile; crisp morning light |
| S02 | Daytime classroom | Seated, waist-up; closing a blank notebook near the window | Gentle task-focused look toward her hands; soft daylight |
| S03 | After-school corridor | Knee-up diagonal view; turning back while walking slowly | Small surprised smile; warm side light and long corridor lines |
| S04 | Evening walk home | Knee-up relaxed walk beside a quiet neighborhood fence | Calm closed-mouth smile; amber late-day backlight |

The four images must not repeat the same mouth shape, direct gaze, pose, or
background geometry. Props remain simple and secondary to the face. Any paper,
notebook, sign, or display contains no readable text.

## Generation workflow

1. Before every generation call, open the canonical portrait and confirm the
   reference role. Use one image and one call per candidate.
2. Keep each prompt short and concept-first: reference role, identity relation,
   fixed wardrobe, one coherent visual concept, then shared rendering and a
   minimal avoid list.
3. Complete U00 and U01 serially with explicit identity approval after each.
4. Generate S01 first. Build a comparison artifact and wait for explicit
   identity approval before continuing.
5. Generate S02 through S04 independently and serially. Stop the remaining set
   immediately if a later candidate fails identity.
6. Do not infer identity approval from scene approval, wardrobe approval, or a
   general request to continue.

## Review and stopping rules

For every transition or scene candidate, inspect identity before composition.
The comparison artifact contains the canonical face crop, the latest approved
comparison face, the current candidate face, and the current full image. The
three face crops use the same displayed size without warping, rotation,
landmark fitting, or face-shape correction.

A candidate is either an obvious identity mismatch or `identity_pending` until
the user decides. After identity passes, review uniform construction, hairpin
count and side, hand and bag contact, anatomy, spatial support, accidental
text, watermarking, and image artifacts. A strong background or outfit cannot
offset a failed face.

The route uses the retry and stop limits in the current
`generating-akari-v2-2-images` skill. Rejected, deferred, or unapproved images
are never edited, reused, cropped into references, summarized into continuity
instructions, or promoted as anchors.

## Outputs and preservation

- Store prompts, generated candidates, and comparison artifacts under one
  Git-ignored `tmp/` review directory.
- Do not copy any candidate into `akari-v2.2/accepted/` without explicit user
  acceptance.
- Do not commit generated images or review artifacts unless the user explicitly
  asks for a final deliverable to be tracked.
- Record generation IDs and local output paths in the ignored run ledger so the
  experiment can be reproduced or diagnosed.

## Success criteria

- U00 and U01 each receive explicit identity approval before the four-scene set
  begins.
- Four independently generated, face-readable scenes use the same documented
  uniform construction while presenting distinct places, actions, light, and
  expressions.
- Every retained image clears identity first, followed by wardrobe, anatomy,
  contact, space, text, and artifact review.
- No generated face is used as a generation reference or continuity anchor.
- Nothing is promoted or Git-tracked without a separate explicit acceptance
  decision.

## Out of scope

- Full-body, extreme-angle, distant-camera, or complex-motion scenes.
- Sailor, blazer, cardigan, winter, or alternate uniform designs.
- Anchor-transfer testing or canonical replacement.
- Batch generation without the required identity stops.
- PDF, manifest, release, or broad repository changes.

# Akari v1.2 Representative Motion Poses Design

## Summary

Complete Phase 2 of the Akari v1.2 reference pack by producing one accepted
full-frame key pose for each of three motions: walking, seated, and turning.
The images should remain useful as character references while adding natural,
appealing movement through weight, clothing, and hair.

The accepted Phase 1 eight-view turnaround is immutable input. Phase 2 does
not reopen angle selection or redesign Akari. Work proceeds one motion at a
time in the order walking, seated, then turning. Each motion begins with three
candidates and ends with exactly one accepted deliverable.

## Source Contract

The source of truth is
`source/manifests/v1-2-motion/phase-2-handoff.json`. Every motion request must
consume its complete accepted turnaround pack and verify the recorded source
manifest hash before generation.

All eight turnaround views remain mandatory identity and construction inputs.
The request builder may emphasize the views most relevant to a motion, but it
must not omit the complete pack from the request contract. The accepted v1.2
face, hair, body, standard outfit, socks, sneakers, palette, and
character-left hair ornament remain locked.

Generation must stop before writing requests if any required accepted asset is
missing, has an unexpected hash, or no longer has a passing final Phase 1
review.

## Goals

- Produce one readable, natural, and appealing walking key pose.
- Produce one readable, natural, and appealing seated key pose.
- Produce one readable, natural, and appealing turning key pose.
- Preserve identity, age impression, proportions, outfit construction,
  palette, footwear, and hair-ornament side across all three deliverables.
- Keep the images useful as generation references through full-body framing,
  a plain light background, and restrained perspective.
- Preserve traceability from each accepted image to its request, source pack,
  candidate, review, and hash.

## Non-Goals

- Do not create animation frames or motion sequences.
- Do not add alternative outfits, props, scenery, text, or other characters.
- Do not revise or replace the accepted eight-view turnaround.
- Do not add the motion images to a v1.2 settings PDF in this phase.
- Do not commit generated candidate folders unless the user explicitly asks
  to preserve them.
- Do not force low-difference composites when they damage anatomy, footwear,
  hair, clothing, or object continuity.

## Creative Direction

The approved direction is **natural and appealing**. The images should show
more life than neutral construction references without becoming action
illustrations. Motion comes from believable weight transfer, limb placement,
small differences in shoulder and hip rotation, and restrained follow-through
in the hoodie, skirt, and hair.

All three poses use the standard white oversized hoodie, gray pleated skirt,
striped crew socks, chunky white-and-blue sneakers, and character-left
pale-blue hair ornament. Expressions remain naturally friendly and do not
become a separate expression-design exercise.

## Motion Specifications

### Walking

Show a readable mid-step with one leg forward and the other behind. The
relationship between the two feet and the ground must remain understandable.
Use a modest arm swing and restrained follow-through in the hoodie, skirt, and
hair. The thighs, knees, calves, socks, and sneakers must remain traceable and
must not be hidden by the skirt or crop.

The three initial candidates vary the exact gait instant, stride length, and
arm position while preserving camera, outfit, and identity constraints.

### Seated

Show a natural seated reference pose on an implied, invisible support plane.
Do not render a chair, backrest, or prop as part of the deliverable. Keep the
pelvis, torso, and feet balanced as though a stable seat is present so the pose
does not look suspended. Offset the knees and feet slightly so both legs remain
readable. Place the hands naturally near the knees or beside the body.

The pose must preserve torso-to-leg proportion, believable hoodie compression
and folds, skirt placement, hand anatomy, socks, and complete footwear. The
three initial candidates vary leg offset, hand placement, and modest torso
inclination without changing the underlying character design.

### Turning

Show a natural over-shoulder or mid-turn moment derived from standing or
walking. Use a believable difference between face, shoulder, and hip rotation
to communicate motion without an extreme spinal twist.

The pose must connect the accepted front, profile, rear-three-quarter, and back
construction. The character-left hair ornament must remain on the correct side
and must not be mirrored. The three initial candidates vary turn completion,
gaze direction, and restrained hair or garment follow-through.

## Framing And Presentation

- Use the Phase 1 portrait canvas size of 1024 by 1536 pixels.
- Keep the complete figure, including hair and both shoes, inside the frame.
- Use a plain light background with no environmental storytelling.
- Avoid strong foreshortening, dramatic lens effects, and camera tilt.
- Do not place labels or review marks on source candidates or finished images.
- Place candidate IDs, motion labels, and decisions outside images in contact
  sheets.

## Production Flow

Production proceeds in this order:

1. Build and validate three walking requests.
2. Generate and review the three walking candidates.
3. Record one accept, with remaining candidates marked hold or reject.
4. Repeat the same flow for seated.
5. Repeat the same flow for turning.
6. Promote exactly one accepted candidate per motion.
7. Build and review the final three-pose contact sheet.

If all three candidates for a motion fail, record explicit rejection reasons
and create a new round only for that motion. The next round must incorporate
the failure observations into its prompt while retaining the locked source
contract. A failed motion does not require regenerating candidates for a
different motion.

## Components

### Generation Request Builder

The builder validates the Phase 2 handoff, accepted source paths, hashes, and
final Phase 1 approval. It emits candidate-specific request records containing
the motion slug, round, candidate number, prompt, reference paths, target path,
acceptance gates, request ID, and batch ID.

The initial manifest contains exactly three active candidates for each of
walking, seated, and turning. Later rounds preserve earlier request and review
history rather than replacing it.

### Review Records

Each generated candidate receives one `accept`, `hold`, or `reject` decision
and observations for identity, age impression, anatomy, pose readability,
outfit, footwear, ornament side, framing, artifacts, image quality, and motion
naturalness. A review must identify the request ID and exact source candidate.

Exactly one candidate may be accepted for a motion. A hold candidate remains a
comparison artifact and cannot be promoted or used as an accepted deliverable.

### Contact Sheet Builder

The builder produces a comparison sheet for each active three-candidate motion
batch and a final sheet containing the three accepted motions. It reads request
and review metadata rather than relying on filename ordering. Missing or
unreadable images produce a clear failure instead of an incomplete sheet.

### Promotion Tool

Promotion accepts only a candidate with a matching `accept` review. It rejects
missing reviews, multiple accepts for one motion, mismatched request IDs,
stale source hashes, and attempts to overwrite a different accepted candidate
without an explicit replacement operation.

Accepted images are converted to high-quality WebP under
`source/finished/v1-2-motion/`. The accepted-selection manifest records the
finished path, source candidate, request and batch IDs, review path, source
pack hash, and hashes for both source and finished assets.

## Paths And Deliverables

- Requests and accepted selection:
  `source/manifests/v1-2-motion/`
- Generated candidates:
  `source/generated/v1-2-motion/`
- Reviews and contact sheets:
  `evidence/v1-2-motion/`
- Accepted deliverables:
  `source/finished/v1-2-motion/`

The completed phase contains exactly three finished images, their accepted
selection manifest, candidate review records, motion-batch contact sheets, and
one final three-pose contact sheet.

## Acceptance Gates

Every promoted candidate must pass all of these gates:

1. Identity matches the accepted v1.2 face and hair lock.
2. Age impression remains consistent with the accepted character reference.
3. Anatomy and pose are coherent and immediately readable.
4. Body proportion remains consistent with the accepted turnaround.
5. Hoodie, skirt, socks, and sneakers retain their construction and palette.
6. The pale-blue ornament remains on the character-left side.
7. The entire figure is framed cleanly without clipped hair, hands, or shoes.
8. No extra limbs, merged anatomy, malformed hands or feet, text, or image
   artifacts are present.
9. Weight, balance, garment response, and hair response make the named motion
   feel natural.
10. The candidate is strong enough to serve as a reusable character reference,
    not merely the safest surviving image.

## Verification

Contract tests verify the three motion slots, three initial candidates per
slot, required eight-view inputs, paths, IDs, prompt invariants, and ornament
constraint. Unit tests cover request building, handoff failures, review
validation, contact-sheet ordering, and promotion success and failure cases.

After implementation, run the focused Phase 2 tests followed by the existing
Node and Python suites and repository audits. Visual verification requires
opening every generated candidate before review, comparing each active batch
on its contact sheet, opening each selected candidate individually, and
reviewing the final three-pose sheet before declaring Phase 2 complete.

## Downstream Handoff

Phase 2 completion makes the v1.2 settings PDF eligible for a separate design
and implementation phase. It does not modify
`dist/akari-v1.1-settings.pdf` or imply that PDF promotion has already passed.

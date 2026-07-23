# Akari v1.1 Tonari No Hyoujou Design

## Summary

Create an expression-focused illustration collection titled `となりの表情`.
The collection should emphasize Akari's small, readable reactions during close
everyday conversation. It is not a printed book project for now; it is a curated
image set that can later become a PDF or gallery if the user wants one.

The first version should target 18 illustrations. The production flow should
draft the full 18-image expression map first, review the overall balance, then
send only selected candidates through the one-image-at-a-time
`akari-v1-1-image-review` workflow.

## Goals

- Make expression richness the main reading experience.
- Keep the tone close, conversational, healthy, and everyday.
- Show clear expression differences without turning Akari into another
  character.
- Use conversation reactions as the visible page concepts.
- Use a softer inner-emotion wave as the ordering logic.
- Keep most images close enough for the face to be readable.
- Preserve room for gestures, shoulders, hands, and posture to carry emotion.
- Review accepted candidates one image at a time with the Akari v1.1 image
  review gates.
- Keep generated images free of readable text, logos, labels, borders, or page
  design.

## Non-Goals

- Do not make a print-ready book in this phase.
- Do not create a rigid facial-expression reference sheet with matching camera
  angle on every page.
- Do not repeat the existing `となりのあかり` collection with a new title only.
- Do not fully finish and humanize each candidate before checking the whole
  18-image expression balance.
- Do not accept identity drift, age drift, broken anatomy, or text artifacts
  just because an expression is interesting.
- Do not repair candidates by local pixel compositing. Failed edits should be
  retried, rejected, or kept as rejected evidence.

## Core Decisions

- Working title: `となりの表情`.
- Format for now: curated image set plus review evidence, not a bound product.
- Target count: 18 illustrations.
- Concept model: conversation reaction first, inner emotion second.
- Expression strength: medium range.
- Distance mix: about 10 close portraits, 5 half-body images, and 3 full-body
  or wider gesture images.
- Review strategy: draft all 18 rough candidates first, then perform strict
  single-image review only on likely accepts.
- Image-review stage choice: use Correction Pass for concrete defects and
  Humanization Pass only after the image is structurally valid.

## Reading Experience

The collection should feel like Akari is reacting from the next seat, across a
small table, or while walking beside the viewer. The viewer should understand
what just happened without needing long captions: she was called, teased,
praised, caught off guard, worried, relieved, or about to answer.

The expression should be readable at a glance, but not theatrical. The sweet
spot is a face that changes clearly while still feeling like Akari is trying to
keep her usual distance and composure.

## Expression Model

Use `conversation reaction` as the prompt surface:

- Called from nearby.
- Eye contact lands a little too directly.
- A compliment arrives before she can prepare.
- A teasing remark makes her push back.
- She starts to answer and hesitates.
- She tries to look fine while feeling otherwise.

Use `inner emotion` as the hidden balancing layer:

- Ease.
- Shyness.
- Fluster.
- Resistance.
- Pride.
- Worry.
- Relief.
- Loneliness.
- Honesty.

The final order should move through a gentle wave:

1. Familiar ease.
2. Awkward eye contact.
3. Shy happiness.
4. Small resistance.
5. Concern and quietness.
6. Honest warmth.
7. Leaving or afterglow.

## Initial 18 Slots

1. `called-turn`
   - Japanese title: `呼ばれて振り向く`.
   - Reaction: she turns toward the viewer after being called.
   - Distance: close or upper body.
   - Emotion: familiar ease.
2. `eye-contact-pause`
   - Japanese title: `目が合って止まる`.
   - Reaction: eye contact lands and she pauses for one beat.
   - Distance: close portrait.
   - Emotion: shyness.
3. `compliment-blush`
   - Japanese title: `褒められて照れる`.
   - Reaction: she is happy but tries not to show too much.
   - Distance: close portrait.
   - Emotion: shy happiness.
4. `teased-pout`
   - Japanese title: `からかわれてむっとする`.
   - Reaction: she makes a small annoyed face after being teased.
   - Distance: close or upper body.
   - Emotion: resistance.
5. `answer-hesitation`
   - Japanese title: `言い返す前`.
   - Reaction: she is about to answer but changes course.
   - Distance: half-body.
   - Emotion: hesitation.
6. `side-glance-sulk`
   - Japanese title: `拗ねた目線`.
   - Reaction: she looks aside while still listening.
   - Distance: close portrait.
   - Emotion: sulking.
7. `failed-straight-face`
   - Japanese title: `でも笑ってしまう`.
   - Reaction: her serious face breaks into a smile.
   - Distance: close portrait.
   - Emotion: warmth.
8. `small-pride`
   - Japanese title: `小さく得意げ`.
   - Reaction: she accepts a tiny win and looks quietly proud.
   - Distance: upper body.
   - Emotion: pride.
9. `sudden-surprise`
   - Japanese title: `不意に驚く`.
   - Reaction: something unexpected catches her off guard.
   - Distance: half-body.
   - Emotion: surprise.
10. `worried-peek`
    - Japanese title: `心配そうに覗く`.
    - Reaction: she leans or peeks in to check on the viewer.
    - Distance: half-body.
    - Emotion: concern.
11. `relief-release`
    - Japanese title: `安心して力が抜ける`.
    - Reaction: tension leaves her face and shoulders.
    - Distance: close or upper body.
    - Emotion: relief.
12. `sleepy-reply`
    - Japanese title: `眠たげに返事する`.
    - Reaction: she answers softly while still sleepy.
    - Distance: close portrait.
    - Emotion: softness.
13. `lonely-quiet`
    - Japanese title: `少し寂しそう`.
    - Reaction: her expression goes quiet for a moment.
    - Distance: close portrait.
    - Emotion: loneliness.
14. `brave-okay-face`
    - Japanese title: `平気な顔をする`.
    - Reaction: she says she is fine before fully meaning it.
    - Distance: upper body.
    - Emotion: brave front.
15. `honest-happy`
    - Japanese title: `素直に嬉しい顔`.
    - Reaction: she lets happiness show plainly.
    - Distance: close portrait.
    - Emotion: honest joy.
16. `near-shy-cover`
    - Japanese title: `近距離の照れ隠し`.
    - Reaction: she covers or deflects a close-distance blush.
    - Distance: half-body.
    - Emotion: fluster.
17. `leaving-turn`
    - Japanese title: `帰り際に振り向く`.
    - Reaction: she turns back just before leaving.
    - Distance: full-body or wider gesture.
    - Emotion: afterglow.
18. `almost-says`
    - Japanese title: `何か言いかけて笑う`.
    - Reaction: she almost says something, then smiles instead.
    - Distance: full-body or wider gesture.
    - Emotion: warm restraint.

## Draft Review Flow

The first pass should prioritize coverage, not final polish:

1. Generate or collect one rough candidate for each of the 18 slots.
2. Build an expression map or contact sheet for the full set.
3. Check for repeated face angle, repeated mouth shape, repeated blush level,
   repeated hand pose, and repeated emotional temperature.
4. Replace weak or duplicated slots before any heavy finishing pass.
5. Pick likely accepts.
6. Run `akari-v1-1-image-review` on one selected image at a time.

For each selected image, decide the review stage before editing:

- Use `Correction Pass` for concrete face, hairpin, hand, foot, shoe, sock,
  bag, outfit, or anatomy defects.
- Use `Humanization Pass` only after the candidate is structurally valid and
  needs subtle natural variation.
- Do not mix correction and humanization in one edit.

## Acceptance Gates

A candidate can only move toward final acceptance when it passes the Akari v1.1
identity gates:

- Adult 25-year-old Akari impression remains intact.
- Face, hair, and pale blue hair ornament stay consistent.
- Body proportion does not become childlike, overly thin, or glamorous.
- Anatomy and composition remain clean.
- Expression is readable without becoming theatrical.
- Generated image contains no intentional readable text, watermark, logo, frame,
  border, or panel layout.
- Candidate is a full-frame generated or edited output, not a mechanical local
  composite.

For Humanization Pass candidates, use the review score gate from
`akari-v1-1-image-review`: identity, face/hairpin, anatomy/composition,
technical naturalness, semantic naturalness, edit minimality, and artifact
regression.

## File Structure Direction

If this collection moves beyond design, use repo-local paths parallel to the
existing collections:

```text
source/generated/tonari-no-hyoujou/
source/finished/tonari-no-hyoujou/
source/manifests/tonari-no-hyoujou/
evidence/finish-pass/contact-sheets/
evidence/finish-pass/reviews/
```

Generated intermediates should stay out of git unless the user explicitly asks
to preserve or publish a final deliverable.

## Verification Plan

For this design-only step:

- Run `npm run lint:md`.

For a future implementation step:

- Validate any new manifest JSON with `python -m json.tool`.
- Run relevant contract tests if new manifests or renderers are added.
- Use the `akari-v1-1-image-review` verification checklist for each finished
  candidate.
- If a PDF or rendered gallery is added later, run the matching build and audit
  commands for that artifact.

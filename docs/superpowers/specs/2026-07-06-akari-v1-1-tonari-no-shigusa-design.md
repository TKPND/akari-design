# Akari v1.1 Tonari No Shigusa Design

## Summary

Create an image-first gesture exploration collection titled `となりのしぐさ`.
This is not a print or PDF project for now. It is a lightweight idea, generation,
and review surface for expanding Akari v1.1 beyond facial expressions into hands,
sleeves, shoulders, posture, body direction, and close everyday distance.

The collection should complement `となりの表情`: where that set is primarily about
face-led reactions, this set should make the body readable. The first version
should build 30 to 40 gesture slots, then generate selected candidates from that
map instead of trying to finish every idea at once.

## Goals

- Explore Akari's positive everyday gestures before committing to a booklet.
- Make body motion, distance, and posture the main reading experience.
- Keep the tone happy, warm, familiar, and healthy.
- Emphasize reassurance, shyness, closeness, small dependence, and quiet joy.
- Preserve Akari v1.1 identity while allowing small scene and posture variation.
- Keep generation lightweight enough to add, replace, and compare ideas quickly.
- Use contact sheets to judge motion strength and set balance before finishing.
- Keep generated images free of readable text, logos, labels, borders, or page
  design.

## Non-Goals

- Do not make a print-ready book, PDF, or final gallery in this phase.
- Do not make another expression collection where the face explains everything.
- Do not lock a final page count before the gesture map has been explored.
- Do not finish every generated candidate through heavy correction or
  humanization.
- Do not accept static cute portraits that lack a readable gesture.
- Do not make the tone gloomy, dramatic, pin-up-like, or childlike.
- Do not repair candidates by hiding broken anatomy with local compositing.

## Core Decisions

- Working title: `となりのしぐさ`.
- Format for now: gesture slot map plus generated candidates and contact sheets.
- Initial idea count: 30 to 40 slots.
- First generated batch: about 12 to 18 `promising` slots.
- Organizing model: distance map first, positive emotional body language second.
- Outfit direction: white hoodie as the main identity anchor.
- Scene range: room, desk, sofa, entrance, window, and walk-home settings.
- Composition mix: varied, with the center of gravity around half-body to
  knee-up images.
- Face close-ups: limited, because this collection should not duplicate
  `となりの表情`.
- Review strategy: draft broadly, judge by contact sheet, then finish only likely
  accepts.

## Reading Experience

The set should feel like Akari is nearby and happy to be there. The reader should
notice what her body is doing before reading a title: tugging a sleeve, leaning
over a desk, turning back from the doorway, relaxing beside the viewer, or
tilting with sleepiness.

The gestures should be small and everyday rather than athletic or theatrical.
The desired mood is positive closeness: comfortable silence, bashful distance,
a little bit of reliance, and light moments of joy. Negative emotions can exist
only as softened contrast, such as a shy retreat or tired looseness, not as the
main flavor.

## Distance Map

Use the distance map as the production backbone. These are internal generation
and review categories, not visible chapters.

1. `beside`
   - Japanese label: `隣にいる`.
   - Scenes: sofa, floor, bench, walk home.
   - Gesture focus: shoulder distance, sleeves, leaning angle, knee direction.
   - Tone: reassurance, closeness, small dependence.
2. `across`
   - Japanese label: `向かいにいる`.
   - Scenes: desk, table, cup, casual work.
   - Gesture focus: chin in hand, sleeve cuffs, reaching, leaning forward.
   - Tone: everyday ease, curiosity, quiet joy.
3. `diagonal`
   - Japanese label: `斜め前にいる`.
   - Scenes: room corner, window, side of a desk, walking beside.
   - Gesture focus: hair adjustment, shoulder turned toward viewer, averted gaze.
   - Tone: shyness, familiarity, soft awareness.
4. `over_shoulder`
   - Japanese label: `背中越し・振り返り`.
   - Scenes: entrance, hallway, window, leaving moment.
   - Gesture focus: back, neck twist, shoulder line, hand lingering by a door.
   - Tone: afterglow, invitation, gentle pause.
5. `one_step_close`
   - Japanese label: `一歩近い`.
   - Scenes: near desk edge, doorway, sofa edge, close standing distance.
   - Gesture focus: sleeve tug, peeking in, hand in foreground, almost speaking.
   - Tone: bashfulness, closeness, small courage.
6. `relaxed`
   - Japanese label: `くつろぎの距離`.
   - Scenes: floor, sofa, chair, desk, warm window light.
   - Gesture focus: holding knees, gripping sleeves, head tilt, loosened
     shoulders.
   - Tone: safety, comfort, sleepiness, contentment.

Each category should contribute roughly five to seven slots. The first generated
batch does not need to cover every category evenly, but the full map should avoid
collapsing into only one kind of closeness.

## Gesture Slot Model

Each gesture idea should be stored as a compact slot that can become a generation
request later. A slot should include:

- `slug`: stable English identifier.
- `japanese_title`: short Japanese title.
- `distance`: one distance-map category.
- `positive_tone`: reassurance, shyness, closeness, small dependence, joy, or
  relaxation.
- `gesture_focus`: sleeve, hand, shoulder, back, knee, hair, posture, or feet.
- `scene`: room, desk, sofa, entrance, window, or walk home.
- `composition`: upper body, half body, knee-up, or wider body.
- `motion`: the small action being caught mid-flow.
- `prompt_note`: short generation description.
- `avoid_note`: known failure risk or prompt constraint.
- `priority`: `seed`, `promising`, or `hold`.

The slot map should support filtering by distance, gesture focus, scene, and
priority. This keeps exploration flexible: sleeve ideas, one-step-close ideas,
or desk ideas can be generated independently.

## Initial Gesture Families

Use these families as the starting shelves for the 30 to 40 slots:

1. `sleeves_and_hands`
   - Sleeve tug.
   - Holding a sleeve cuff.
   - Hiding the mouth with a sleeve edge.
   - Reaching out and stopping short.
   - Fingertips almost touching.
   - Holding a cup with both hands.
2. `shoulders_and_leaning`
   - Leaning slightly closer.
   - Turning only the shoulders toward the viewer.
   - Relaxing beside the viewer.
   - Almost leaning on the viewer without fully doing it.
3. `across_the_desk`
   - Chin in hand.
   - Resting on the desk.
   - Peeking over a cup or notebook.
   - Leaning forward during casual work.
4. `seated_and_relaxed`
   - Holding knees.
   - Pulling feet closer on a sofa.
   - Sitting small on a chair.
   - Head tilting from sleepiness.
5. `hair_neck_and_averted_gaze`
   - Fixing hair with one hand.
   - Tucking hair near the ear.
   - Tilting the neck.
   - Looking away while still clearly happy.
6. `over_shoulder`
   - Turning back while leaving.
   - Stopping with a hand near the door.
   - Listening over the shoulder.
   - Hoodie shoulder and back silhouette.
7. `one_step_close`
   - Tugging a sleeve.
   - Peeking in.
   - Moving closer before saying something.
   - Hand entering the foreground.
   - Smiling quietly from close range.
8. `small_energy`
   - Light wave.
   - Leaning forward from happiness.
   - Walking one step ahead and turning back.
   - Small playful bounce.

These families are not final chapters. They are idea shelves that should be
expanded into concrete slots during implementation.

## Motion Gate

`となりのしぐさ` should fail a candidate when it becomes only a cute still portrait.
Every accepted slot and generated candidate must show a readable small action.

Useful motion verbs:

- `pull`: tugging a sleeve, withdrawing a hand, gently moving back.
- `reach`: extending a hand, leaning across a desk, peeking in.
- `lean`: moving closer, nearly resting on someone, softening into a sofa.
- `twist`: turning back, rotating shoulders, looking over the shoulder.
- `fix`: touching hair, adjusting a hood or sleeve cuff.
- `release`: shoulders dropping, head tilting, body loosening from comfort.
- `bounce`: stepping forward, turning back with light happiness.

Motion acceptance checks:

- The gesture is understandable without reading the title.
- At least one of hand, shoulder, torso, knee, or head angle has a clear change.
- The face is not the only carrier of emotion.
- Upper-body images still show meaningful hand or shoulder motion.
- Static standing, sitting, or bust-up images move to `hold` or regeneration.

## Generation Flow

The first production pass should stay light:

1. Write the 30 to 40 slot map.
2. Mark 12 to 18 slots as `promising`.
3. Create generation requests for the promising slots.
4. Generate one candidate per promising slot.
5. Build a contact sheet for the first batch.
6. Review the contact sheet for motion, variety, identity, and overlap with
   `となりの表情`.
7. Replace weak slots or regenerate weak candidates.
8. Send only likely accepts through `akari-v1-1-image-review` correction or
   humanization.

The first pass should prioritize breadth and motion readability over final
polish. Strong directions can receive additional variations after the contact
sheet review.

## Acceptance Gates

A candidate can move toward final acceptance only when it passes these gates:

- Akari v1.1 adult identity remains intact.
- Face, hair shape, warm amber eyes, and pale-blue hair ornament stay consistent
  when visible.
- Body proportions do not become childlike, overly thin, or glamorous.
- The gesture is readable as body language, not only as a facial expression.
- Hands, shoulders, arms, legs, and clothing continuity are clean enough for the
  gesture to be useful.
- The tone stays happy, warm, and healthy.
- The image contains no intentional readable text, logo, watermark, frame,
  border, or panel layout.
- The candidate is a full-frame generated or edited output, not a mechanical
  local composite.

For finishing candidates, use the existing `akari-v1-1-image-review` gates.
Correction Pass should address concrete defects. Humanization Pass should happen
only after the gesture and anatomy are structurally valid.

## File Structure Direction

If this collection moves beyond design, use repo-local paths parallel to the
existing collections:

```text
source/manifests/tonari-no-shigusa/
  gesture-slots.json
  generation-requests.json

source/generated/tonari-no-shigusa/
source/finished/tonari-no-shigusa/

evidence/tonari-no-shigusa/contact-sheets/
evidence/tonari-no-shigusa/reviews/
```

Generated intermediates should stay out of git unless the user explicitly asks
to preserve or publish a final deliverable.

## Verification Plan

For this design-only step:

- Run `npm run lint:md`.

For a future implementation step:

- Validate new JSON manifests with `python -m json.tool`.
- Add a small structural checker if the slot schema becomes stable.
- Generate contact sheets and review them against the Motion Gate.
- Run relevant contract tests if new renderers or stricter manifest checks are
  added.
- Use `akari-v1-1-image-review` verification for each finished candidate.
- If a PDF or rendered gallery is added later, run the matching build and audit
  commands for that artifact.

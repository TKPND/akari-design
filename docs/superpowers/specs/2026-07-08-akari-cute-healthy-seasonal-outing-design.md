# Akari Cute Healthy Seasonal Outing Design

## Summary

Create a small next batch for `となりのコーデ` that extends the existing
`cute_healthy` direction into seasonal outing clothes. The batch should be
small enough to review carefully before committing to a larger run: eight
images, two per season, focused on cute adult private clothes, knee-up framing,
and the leg quality of the original Akari v1.1 body reference.

The core idea is not an overly sanitized "healthy" constraint. Here,
`cute_healthy` means adult-cute seasonal outfits, natural outfit-appropriate
skin visibility, soft physical charm, and attractive healthy leg rendering.
The design should avoid over-constraining the model in ways that make the
images stiff or lower quality.

## Goals

- Add one focused eight-image batch before attempting a larger coordinate set.
- Keep the direction close to cute private outing clothes, not sportswear or
  roomwear.
- Cover spring, summer, autumn, and winter with two images each.
- Use season-specific clothing as the main seasonal signal.
- Keep backgrounds quiet so the person, outfit, and legs stay primary.
- Preserve Akari's adult 25-year-old identity, face, hair, and pale blue hair
  ornament.
- Treat the original full-body Akari leg rendering as a quality target, not a
  disposable detail.
- Require image generation to use reference images, not prompt text alone.

## Non-Goals

- Do not build a PDF in this phase.
- Do not replace the existing `tonari-no-coordinate` set.
- Do not make a broad 16-image or 24-image batch before this smaller batch is
  reviewed.
- Do not optimize for elaborate backgrounds, props, storefronts, or seasonal
  scenery.
- Do not turn the prompt into a rigid safety checklist that suppresses visual
  appeal.
- Do not create explicit adult content, pin-up framing, or glamour-model
  styling. The target is adult cute outfit appeal.

## Core Decisions

- Working title: `Akari Cute Healthy Seasonal Outing`.
- Collection relationship: an extension batch for `akari-v1.1-tonari-no-coordinate`.
- Candidate count: eight.
- Seasonal balance: spring two, summer two, autumn two, winter two.
- Composition: knee-up portrait as the default.
- Outfit distribution: six skirt, dress, or jumper-skirt looks and two
  shorts or culotte looks.
- Seasonal signal: clothing first, background second.
- Background policy: light seasonal atmosphere only.
- Main acceptance axis: character identity, outfit appeal, and leg quality.

## Visual Direction

The batch should feel like Akari going out in cute seasonal private clothes.
The look can have a little adult charm and natural skin visibility when the
outfit calls for it, but it should not become a pin-up sheet, a model catalog,
or a costume set. The best images should still feel close, everyday, and
characterful.

The preferred framing is knee-up. This keeps outfit shape readable while
leaving enough room to inspect the thighs, knees, and lower-leg continuity.
Full-body framing is intentionally out of scope for the first batch because it
raises footwear, hand, and proportion risk before the outfit direction is
validated.

Backgrounds should be simple and secondary. A spring street, summer light,
autumn color, or winter air is enough. If background detail competes with the
person or makes the model spend quality on signs, props, or scenery, the image
is missing the point of this batch.

## Leg Quality Gate

The leg gate is an appeal and quality gate, not a purity gate. The original
Akari v1.1 front reference has the target feel: soft thigh volume, natural knee
shape, believable calf transition, and an attractive healthy line down to the
ankle when visible.

Reject or regenerate images when:

- Thighs become flat, overly thin, inflated, or disconnected from the knees.
- Knees are missing, over-rendered, twisted, or placed at odd heights.
- Calves and ankles do not connect naturally.
- Legs become mannequin-like, rubbery, or over-smoothed.
- Outfit hems hide the leg quality that the batch is meant to inspect.
- The pose makes the legs visually confusing.

## Reference Image Requirement

Every generation request must carry a reference image pack. Prompt text alone
is not acceptable for this batch because the face, body balance, hair ornament,
and leg quality are all easy to drift.

Use these minimum references for each request:

- `source/references/tonari-no-akari/identity-face-hair.webp`
- `source/references/tonari-no-akari/identity-body-base.webp`
- `source/references/tonari-no-akari/identity-basic-outfit.webp`
- `source/references/tonari-no-akari/identity-side-view.webp`
- `source/originals/v1_1_front_1.webp`

The first four references keep the existing `tonari-no-coordinate` identity
pack connected to the current project workflow. The original front reference is
included specifically to anchor the leg-quality target. If an image-generation
tool can accept weighted or role-labeled references, the implementation should
label them as face/hair identity, body balance, default outfit, side-view
identity, and leg-quality reference.

## Candidate Set

1. `spring-light-cardigan-flare-dress`
   - Japanese title: `春の薄カーデワンピ`
   - Outfit: cream light cardigan over a pale mint flare dress.
   - Role: soft spring outing baseline.
   - Risk: avoid making the dress too plain or hiding the leg line.

2. `spring-denim-short-jacket-skirt`
   - Japanese title: `春のデニム短ジャケット`
   - Outfit: short denim jacket, ivory top, and soft A-line skirt.
   - Role: casual spring outing with a little structure.
   - Risk: avoid drifting into youth-casual streetwear.

3. `summer-puff-sleeve-blouse-skirt`
   - Japanese title: `夏のパフ袖ブラウス`
   - Outfit: light puff-sleeve blouse and pale mint trapeze skirt.
   - Role: clear summer clothing signal without relying on scenery.
   - Risk: keep fabric light but not awkwardly transparent.

4. `summer-collar-blouse-culotte`
   - Japanese title: `夏襟ブラウスとキュロット`
   - Outfit: rounded-collar summer blouse and culottes.
   - Role: one of the two shorts or culotte checks.
   - Risk: avoid school-uniform cues.

5. `autumn-short-knit-check-skirt`
   - Japanese title: `秋の短めニット`
   - Outfit: short soft knit and muted check A-line skirt.
   - Role: autumn color and texture while keeping the silhouette cute.
   - Risk: avoid making the knit tight glamour styling.

6. `autumn-jumper-skirt-thin-turtleneck`
   - Japanese title: `秋のジャンスカ`
   - Outfit: brown jumper skirt over a thin turtleneck.
   - Role: adult cute autumn jumper-skirt look.
   - Risk: avoid childlike proportions or school styling.

7. `winter-knit-onepiece-short-coat`
   - Japanese title: `冬のニットワンピ`
   - Outfit: soft knit one-piece with a short winter coat.
   - Role: winter warmth without hiding the legs completely.
   - Risk: avoid bodycon styling and avoid long-coat leg concealment.

8. `winter-short-duffle-culotte`
   - Japanese title: `冬の短めダッフル`
   - Outfit: adult-cute short duffle or cape-like coat with culottes.
   - Role: second shorts or culotte check, winter version.
   - Risk: avoid school-coat impression.

## Prompt Contract

The implementation should reuse the existing `tonari-no-coordinate` request
style, but it should keep this batch separate enough to review on its own.
The request data should include:

- `id`
- `coordinate_order`
- `slot`
- `japanese_title`
- `season`
- `scene`
- `outfit_family`
- `outfit_notes`
- `charm_notes`
- `leg_quality_notes`
- `composition`
- `tone`
- `risk_note`
- `target_path`
- `reference_pack_inputs`
- `reference_usage`
- `prompt`
- `acceptance`
- `risk_profile`
- `review_plan`

The shared prompt should lock:

- Adult 25-year-old Akari identity.
- Short warm-brown bob, warm amber eyes, and pale blue hair ornament.
- Reference-image usage as a required generation input, not optional context.
- Cute adult private outing clothes.
- Knee-up framing with the outfit and legs readable.
- Natural outfit-appropriate skin visibility.
- Soft healthy leg volume and thigh-knee-calf continuity.
- Background that lightly supports the season without taking focus.
- No readable image text, logos, watermarks, frames, or panel layout.

The shared prompt should avoid excessive negative wording. Use targeted
boundaries instead: no underage drift, no student-uniform drift, no explicit
sexual framing, no brand graphics, no broken anatomy, and no background detail
that steals the image.

## Review Strategy

Review the eight candidates as a contact sheet before selecting anything for
finishing. The first pass should ask:

- Does the image still read as Akari?
- Does the outfit clearly express its season?
- Is the outfit cute enough to belong in the `cute_healthy` line?
- Are the thighs, knees, calves, and visible ankles attractive and coherent?
- Is the background quiet enough?
- Did the prompt avoid becoming stiff or over-sanitized?

Each candidate should receive `accept`, `hold`, or `reject`. A strong
candidate can still be rejected if the leg quality misses the original Akari
standard, because this batch exists partly to preserve that quality.

## Artifact Direction

Suggested committed files for implementation:

```text
source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json
tests/test_tonari_no_coordinate_cute_healthy_seasonal_contract.py
```

Suggested working-only generated files:

```text
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_<slot>_v1.webp
evidence/tonari-no-coordinate/contact-sheets/cute-healthy-seasonal-outing-first-pass.webp
```

The generated images and contact sheets should remain working artifacts unless
the user explicitly chooses final deliverables to preserve.

## Verification Plan

Design-document verification:

```bash
npm run lint:md
```

Later implementation verification should include:

```bash
npm run test:python
npm run build:coordinate:contact-sheet -- \
  --requests source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json \
  --output evidence/tonari-no-coordinate/contact-sheets/cute-healthy-seasonal-outing-first-pass.webp
```

The implementation plan should add or update tests before changing generation
contracts. At minimum, the contract test should prove:

- Exactly eight requests.
- Two requests per season.
- Six skirt, dress, or jumper-skirt requests and two shorts or culotte requests.
- Knee-up composition is the default.
- Every request includes leg-quality language.
- Every request includes the minimum reference image pack and explains how to
  use it.
- Every request keeps backgrounds secondary.
- The prompt boundary avoids overbroad negative wording while still blocking
  age drift, student-uniform drift, explicit framing, text, logos, and anatomy
  defects.

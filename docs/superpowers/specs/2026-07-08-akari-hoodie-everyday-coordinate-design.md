# Akari Hoodie Everyday Coordinate Design

## Summary

Create a replacement direction for the next `となりのコーデ` image batch after
the seasonal `cute_healthy` outing pass read too much like catalog clothes on a
background character. The new direction should extend the original Akari v1.1
hoodie image instead of moving farther into dresses, one-pieces, blouses, or
fashion-forward styling.

The target is not "safe and plain." It is Akari wearing clothes that feel like
her own: casual, soft, slightly oversized, easy to go outside in, and still
visually cute. The body, face, hair, and healthy leg rendering should stay
primary; the outfit should support Akari rather than overpower her.

## Context

The previous eight-image seasonal outing batch had useful execution lessons but
missed the desired character feel. The main issue was not a single broken
prompt. The clothing families themselves pushed the model toward fashion
catalog poses, decorative outfits, and "clothes wearing the character" results.

The original v1.1 hoodie image remains the best anchor for this coordinate line:

- The oversized hoodie makes Akari feel relaxed and approachable.
- The short skirt reads as cute without becoming the whole concept.
- Socks and sneakers keep the outfit casual and healthy.
- The legs remain visible enough to judge soft thigh volume, knees, calves, and
  ankles.
- The image reads as Akari first, outfit second.

## Goals

- Design one eight-image first-pass batch before generating anything larger.
- Make hoodie, sweatshirt, long-T, and casual outerwear the main clothing
  families.
- Preserve the "Akari's own clothes" feeling from the original hoodie image.
- Keep seasonal variation through fabric weight, layering, sleeves, socks,
  shoes, and light accessories.
- Keep the legs visible and high quality in every candidate.
- Use full-body or near full-body standing coordinate framing so outfit balance,
  shoes, socks, and legs can be inspected together.
- Require reference images for generation; prompt-only generation is not
  acceptable.
- Avoid the previous batch's fashion-catalog, dress-up, and background-character
  feel.

## Non-Goals

- Do not generate a larger batch before this eight-image direction is reviewed.
- Do not build or update a PDF in this phase.
- Do not treat the previous seasonal outing batch as accepted style direction.
- Do not center dresses, one-pieces, elegant blouses, jumper skirts, formal
  coats, or model-like styling.
- Do not solve the issue by adding elaborate backgrounds or props.
- Do not make the prompts rigidly wholesome in a way that suppresses image
  quality or adult charm.
- Do not create explicit adult content, pin-up framing, glamour-model posing, or
  underage drift.

## Core Decisions

- Working title: `Akari Hoodie Everyday Coordinate`.
- Relationship: a corrective next batch for `となりのコーデ`, not a replacement for
  the whole collection.
- Candidate count: eight.
- Direction: `hoodie_everyday`, with hoodie and sweatshirt looks as the base and
  light casual outerwear as variation.
- Seasonal balance: spring two, early summer or summer two, autumn two, winter
  two.
- Composition: standing full-body or near full-body coordinate-sheet framing.
- Background policy: plain or lightly seasonal; the person and outfit stay
  dominant.
- Main acceptance axis: Akari identity, lived-in casualness, body/leg quality,
  and whether the clothes feel personally owned.

## Visual Direction

The batch should look like Akari is stepping out for a walk, convenience-store
errand, cafe stop, station meetup, or casual day off. The outfit should be easy
to imagine being worn repeatedly. It can be cute and appealing, but it should
not feel like a magazine outfit, boutique mannequin, school uniform, idol
costume, or formal date look.

The strongest silhouettes should echo the original hoodie reference:

- Slightly oversized top.
- Soft shoulder and sleeve volume.
- Short skirt, culotte, or shorts that remain secondary to the top.
- White or pale socks.
- Sneakers or casual walking shoes.
- Pale blue or mint accent through the hair ornament, socks, sneaker accent,
  bag detail, or small seasonal accessory.

Seasonality should be handled with subtle practical changes:

- Spring: lighter fabric, zip hoodie, denim layer, thin socks.
- Summer: oversized T-shirt, thin hoodie, breathable shorts or culotte.
- Autumn: sweatshirt, checked skirt, coach jacket, layered hoodie.
- Winter: boa hoodie, short puffer, thicker socks, warm but not leg-hiding
  layers.

## Anti-Drift Rules

Reject or regenerate a candidate when it reads as:

- A fashion catalog model wearing a coordinated outfit.
- A generic background character with cute clothes.
- A dress-up concept where the clothes are more memorable than Akari.
- A one-piece, elegant blouse, jumper-skirt, formal coat, or boutique styling
  prompt in disguise.
- A pose chosen to sell the outfit rather than show Akari naturally standing.
- A background scene that consumes detail budget or makes the person secondary.
- A softened prompt result where face, legs, or hair ornament drift away from
  the reference identity.

## Leg Quality Gate

The leg gate remains central. The original Akari v1.1 front reference should be
treated as the quality target for soft thigh volume, natural knee placement,
calf transition, ankle shape, and the appealing healthy line down to socks and
shoes.

Every candidate should keep enough leg visibility to inspect:

- Thigh volume and thigh-to-knee transition.
- Knee shape and height.
- Calf and ankle continuity.
- Sock and shoe placement.
- Natural stance weight, without mannequin stiffness or glamour posing.

Reject candidates with flat, over-thin, inflated, rubbery, disconnected,
over-smoothed, or confusing legs.

## Reference Image Requirement

Every generation request must use a visible reference pack. Prompt-only
generation is not acceptable for this direction because the face, hair, body
balance, hoodie feel, and leg quality drift easily.

Minimum identity and body references:

- `source/references/tonari-no-akari/identity-face-hair.webp`
- `source/references/tonari-no-akari/identity-body-base.webp`
- `source/references/tonari-no-akari/identity-basic-outfit.webp`
- `source/references/tonari-no-akari/identity-side-view.webp`
- `source/originals/v1_1_front_1.webp`

Preferred style anchors:

- Existing successful `cute_healthy` coordinate examples may be shown as style
  references when they preserve anime finish, full-body coordinate framing, and
  casual Akari identity.
- The rejected seasonal outing contact sheet should only be used as failure
  evidence, not as a style reference.

If the generation route accepts role labels, label the references as
face/hair identity, body balance, default hoodie outfit, side-view identity,
leg-quality reference, and successful casual-coordinate style.

## Candidate Set

1. `spring-zip-hoodie-pleated-mini`
   - Japanese title: `春のジップパーカー`
   - Outfit: light zip hoodie over a simple inner top, short pleated skirt,
     pale socks, sneakers.
   - Role: closest spring extension of the original hoodie.
   - Risk: avoid making it a school uniform or simply duplicating the original.

2. `spring-long-tee-denim-layer-shorts`
   - Japanese title: `春のロンTデニム羽織り`
   - Outfit: oversized long-sleeve T-shirt, light denim shirt or jacket layer,
     soft shorts, socks, sneakers.
   - Role: casual spring variation without dress-up styling.
   - Risk: avoid denim jacket overpowering the face and body.

3. `summer-oversized-tee-culotte`
   - Japanese title: `夏の大きめTシャツ`
   - Outfit: oversized summer T-shirt, light culotte, short socks, sneakers.
   - Role: breathable summer everyday look.
   - Risk: avoid logo/text graphics and avoid making the top a plain blank sack.

4. `summer-thin-hoodie-shorts`
   - Japanese title: `夏の薄手フーディ`
   - Outfit: thin light hoodie or rash-guard-like hoodie, simple shorts,
     ankle socks, sneakers.
   - Role: summer hoodie adaptation while keeping leg visibility.
   - Risk: avoid swimwear or sporty beach framing.

5. `autumn-sweatshirt-check-skirt`
   - Japanese title: `秋のスウェット`
   - Outfit: soft sweatshirt, muted check short skirt, ribbed socks, sneakers.
   - Role: autumn color and texture closest to hoodie comfort.
   - Risk: avoid school uniform cues from the checked skirt.

6. `autumn-coach-jacket-hoodie-mini`
   - Japanese title: `秋のコーチジャケット`
   - Outfit: casual coach jacket over a hoodie, short skirt, socks, sneakers.
   - Role: light outerwear variation while preserving hoodie identity.
   - Risk: avoid streetwear model styling or brand-like logos.

7. `winter-boa-hoodie-pleated-skirt`
   - Japanese title: `冬のボアパーカー`
   - Outfit: warm boa or fleece hoodie, short pleated skirt or soft skirt,
     thicker socks, sneakers.
   - Role: winter warmth without hiding the legs.
   - Risk: avoid bulky upper body swallowing Akari's proportions.

8. `winter-short-puffer-sweat-culotte`
   - Japanese title: `冬の短め中綿ジャケット`
   - Outfit: short puffer or padded jacket, sweatshirt, culotte or shorts,
     warm socks, sneakers.
   - Role: winter casual outerwear with leg read intact.
   - Risk: avoid formal coat, long coat, or fashion-editorial styling.

## Prompt Contract

Implementation should create a separate request manifest for this corrective
batch rather than mutating the previous seasonal outing manifest. Each request
should include:

- `id`
- `coordinate_order`
- `slot`
- `japanese_title`
- `season`
- `scene`
- `outfit_family`
- `outfit_notes`
- `casual_identity_notes`
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

The shared prompt should explicitly lock:

- Adult 25-year-old Akari identity.
- Short warm-brown bob, warm amber eyes, and pale blue hair ornament.
- Use of attached/visible references, not prompt-only generation.
- Anime illustration finish, not live-action or fashion photography.
- Standing full-body or near full-body coordinate-sheet framing.
- Slightly oversized casual top as the main silhouette.
- Short skirt, culotte, or shorts as secondary support.
- Socks, sneakers, and healthy visible legs.
- Lived-in everyday outing mood.
- Plain or lightly seasonal background.

The shared prompt should explicitly avoid:

- Dress, one-piece, elegant blouse, jumper skirt, formal coat, and boutique
  outfit styling.
- Fashion catalog, model pose, glamour pose, pin-up framing, and editorial
  lighting.
- Logo graphics, readable text, watermarks, panel layouts, and framed designs.
- Background detail that steals focus from Akari.

## Review Strategy

Review the eight candidates as a contact sheet before selecting anything for
finishing. The review should ask:

- Does this read as Akari first?
- Does the outfit feel like she owns and wears it normally?
- Does it preserve the original hoodie image's casual warmth?
- Is the seasonal difference visible without becoming a costume?
- Are face, hair ornament, body balance, socks, shoes, and legs coherent?
- Did the prompt avoid the previous "clothes wearing the character" problem?

Use `accept`, `hold`, or `reject`. A candidate can be rejected even if the
clothing is cute when the clothes overpower Akari or the legs miss the original
quality target.

## Artifact Direction

Suggested committed files for implementation:

```text
source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json
tests/test_tonari_no_coordinate_hoodie_everyday_contract.py
```

Suggested working-only generated files:

```text
source/generated/tonari-no-coordinate/20260708_hoodie-everyday_<slot>_v1.webp
evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp
```

Generated images and contact sheets should remain ignored working artifacts
unless the user explicitly chooses final deliverables to preserve.

## Spec Self-Review

- Difference minimization: this spec only defines the corrective next batch and
  does not replace the broader `となりのコーデ` design.
- Existing pattern fit: it keeps the previous coordinate manifest, request, and
  contact-sheet workflow but changes the outfit family and review gates.
- Edge-case verification: implementation should add a manifest contract test,
  run the coordinate contact-sheet tests after generation metadata is added, and
  run Markdown lint for this spec.

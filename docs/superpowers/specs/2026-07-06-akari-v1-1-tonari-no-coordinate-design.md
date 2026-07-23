# Akari v1.1 Tonari No Coordinate Design

## Summary

Create a lightweight coordinate exploration collection titled
`となりのコーデ`. The collection expands Akari v1.1 beyond the current hoodie-heavy
portrait direction while keeping her base identity stable.

This is not a PDF project for the first phase. The first phase should create a
36-slot coordinate map, mark 12 slots as promising, generate one candidate per
promising slot, and review the resulting contact sheet before deciding whether
to expand, finish, or later turn the work into a PDF art book.

## Goals

- Reduce hoodie repetition while preserving Akari v1.1 identity.
- Explore daily outfits and slightly special day-off outfits.
- Keep the feeling close, healthy, familiar, and adult.
- Use season, scene, and outfit family together so each coordinate has context.
- Make pale blue or mint accents part of the identity system.
- Start with a broad 36-slot map, not a fixed PDF page plan.
- Generate a lightweight first batch of 12 promising candidates.
- Judge the first batch through a contact sheet before heavy finishing.
- Keep generated images free of readable text, logos, labels, borders, or page
  design.

## Non-Goals

- Do not make a print-ready PDF in the first phase.
- Do not replace the Akari v1.1 settings PDF or existing identity references.
- Do not make fashion-model styling the main personality of the collection.
- Do not rely on exposure or glamour to create adult impression.
- Do not use school-uniform-like, cosplay-like, occupation-uniform-like, swimwear,
  underwear-like, or logo/text-heavy outfits.
- Do not finish every generated candidate before checking the whole coordinate
  balance.
- Do not accept a strong outfit if Akari identity, adult impression, anatomy, or
  tone drifts.

## Core Decisions

- Working title: `となりのコーデ`.
- Document ID if later needed: `akari-v1.1-tonari-no-coordinate`.
- Format for now: coordinate slot map plus generated candidates and contact
  sheets.
- Initial idea count: 36 coordinate slots.
- First generated batch: 12 `promising` slots.
- Future PDF: optional, only after the contact sheet proves the direction.
- Main axis: daily clothes plus slightly special day-off clothes.
- Classification model: mixed axis using season, scene, and outfit family.
- Coordinate attitude: between everyday cute and lightly dressed-up.
- Outfit emphasis: layering and one-piece or skirt looks slightly heavier than
  other categories.
- Hoodie role: a small identity baseline, not the dominant outfit.

## Identity Lock

The outfit may change, but the reader should still immediately read the image as
Akari v1.1.

Fixed identity anchors:

- Face shape and key facial impression.
- Hair shape, length, and warm color direction.
- Pale blue or mint hair ornament.
- 25-year-old adult impression.
- Calm, close, everyday Akari mood.
- Natural body proportion and height impression.

Mint or pale blue should appear in every accepted coordinate. The accent can be
the hair ornament, a small bag charm, socks, cardigan detail, scarf edge, nail
color, cup, umbrella, or another small non-logo item. The accent should support
Akari identity, not become a loud costume mark.

## Styling Boundaries

The collection should be more varied than the current hoodie-heavy direction,
but it should not become conservative to the point of sameness. The adult
impression should come from fabric, silhouette, layering, posture, and small
accessories.

Allowed styling range:

- Light cardigans, shirt layers, short jackets, and thin coats.
- Soft knits, ribbed tops, relaxed sweaters, and winter layers.
- One-piece dresses, long skirts, pleated skirts, and day-off skirt looks.
- Relaxed roomwear, morning clothes, and quiet evening clothes.
- Shirts, blouses, simple pants, and casual work-adjacent looks.
- A small number of hoodie baseline looks.

Avoid:

- School uniform impression.
- Cosplay or occupation uniform impression.
- Strong exposure, swimwear, or underwear direction.
- Readable brand logos, text prints, or graphic slogans.
- Overly glamorous model styling.
- Childlike silhouette, styling, or pose.
- Repeating the same white top, grey skirt, and sneakers structure too often.

## Slot Model

Store the first phase as a compact coordinate slot map. Each slot should be easy
to filter by season, scene, outfit family, composition, and priority.

Example slot shape:

```json
{
  "slug": "spring-cardigan-walk",
  "japanese_title": "春のカーディガン",
  "season": "spring",
  "scene": "walk_home",
  "outfit_family": "layering",
  "outfit_notes": "Light cardigan over a simple top and skirt.",
  "mint_accent": "Hair ornament plus a small mint bag charm.",
  "composition": "half_body",
  "tone": "everyday_cute",
  "priority": "promising",
  "risk_note": "Avoid school uniform impression."
}
```

Expected fields:

- `slug`: stable English identifier.
- `japanese_title`: short Japanese title for review and future page use.
- `season`: `spring`, `summer`, `autumn`, `winter`, `rain`, `night`, or
  `all_season`.
- `scene`: room, window, sofa, desk, walk home, cafe, station, riverside,
  doorway, shopping street, or another everyday setting.
- `outfit_family`: layering, one-piece/skirt, knit/soft material,
  roomwear/relaxed, shirt/blouse/pants, or hoodie baseline.
- `outfit_notes`: concise clothing description.
- `mint_accent`: where the pale blue or mint identity accent appears.
- `composition`: close, upper body, half body, knee-up, or full body.
- `tone`: everyday cute, relaxed, lightly dressed-up, quiet, warm, or fresh.
- `priority`: `promising`, `seed`, or `hold`.
- `risk_note`: known failure mode to avoid in generation and review.

## Initial Slot Distribution

The first 36 slots should use this rough distribution:

- Layering and outer layers: 10 slots.
- One-piece and skirt looks: 9 slots.
- Knit and soft-material looks: 6 slots.
- Roomwear and relaxed looks: 5 slots.
- Shirt, blouse, and pants looks: 4 slots.
- Hoodie baseline looks: 2 slots.

The first 12 generated candidates should be selected from the 36 slots:

- Layering and outer layers: 4 candidates.
- One-piece and skirt looks: 3 candidates.
- Knit and soft-material looks: 2 candidates.
- Roomwear and relaxed looks: 1 candidate.
- Shirt, blouse, and pants looks: 1 candidate.
- Hoodie baseline looks: 1 candidate.

This keeps the first batch light while still showing whether the non-hoodie
direction is working.

## Candidate Families

Use these families as starting shelves for the 36 slots.

1. `layering_and_outer`
   - Spring cardigan on a walk.
   - Linen shirt layer near a window.
   - Autumn short jacket on the way home.
   - Rain-day light coat with a mint umbrella.
   - Evening cardigan over a simple top.
2. `one_piece_and_skirt`
   - Day-off one-piece dress.
   - Long skirt with a soft top.
   - Pleated skirt with a grown-up cardigan.
   - Summer skirt and airy blouse.
   - Shopping-street skirt look.
3. `knit_and_soft`
   - Warm winter knit.
   - Ribbed top and relaxed skirt.
   - Soft sweater at a desk.
   - Knit layer with mint scarf detail.
4. `roomwear_and_relaxed`
   - Morning roomwear.
   - Quiet evening lounge outfit.
   - Sofa cardigan and relaxed pants.
   - Soft indoor skirt look.
5. `shirt_blouse_pants`
   - Clean blouse and simple pants.
   - Casual work-adjacent shirt.
   - Cafe blouse with mint accessory.
   - Summer shirt and cropped pants.
6. `hoodie_baseline`
   - Updated hoodie with non-default bottom styling.
   - Hoodie plus cardigan or small accessory variation.

These are idea shelves, not final chapters. The first map should convert them
into concrete coordinate slots with stable slugs and review notes.

## Generation Flow

The first production pass should stay light:

1. Write the 36 coordinate slots.
2. Mark 12 slots as `promising`.
3. Create generation requests for the 12 promising slots.
4. Generate one candidate per promising slot.
5. Build a contact sheet for the first batch.
6. Review the contact sheet for outfit variety, Akari identity, adult
   impression, season and scene balance, and repeated silhouettes.
7. Move weak slots to `hold`, replace unclear slots, or generate alternatives
   for strong directions.
8. Send only likely accepts through the existing Akari v1.1 image-review flow if
   finishing is needed.

The first pass should prioritize range finding over polish.

## Review Gates

A candidate can move toward acceptance only when it passes these gates:

- Akari v1.1 face, hair, and pale blue or mint hair ornament remain recognizable.
- 25-year-old adult impression remains intact.
- Mint or pale blue accent is present and natural.
- Outfit reads as daily wear or slightly special day-off wear.
- Outfit does not read as school uniform, cosplay, occupation uniform, swimwear,
  underwear, or logo/text clothing.
- Body proportion does not become childlike, overly thin, or glamorous.
- Hands, limbs, clothing continuity, and accessories are clean enough for review.
- The image contains no intentional readable text, watermark, frame, border, or
  panel layout.
- The outfit adds variety without overpowering the close Akari mood.

Set-level review should also reject:

- Too many white tops or pale hoodies.
- Too many similar grey skirts.
- Too many identical camera distances.
- Too many indoor morning-light images.
- Too many skirt lengths, shoe types, or cardigan shapes repeating in sequence.

## File Structure Direction

If this collection moves beyond design, use repo-local paths parallel to the
existing collections:

```text
source/manifests/tonari-no-coordinate/
  coordinate-slots.json
  generation-requests.json

source/generated/tonari-no-coordinate/
source/finished/tonari-no-coordinate/

evidence/tonari-no-coordinate/contact-sheets/
evidence/tonari-no-coordinate/reviews/
```

Generated intermediates should stay out of git unless the user explicitly asks
to preserve or publish a final deliverable.

## Relationship To Existing Collections

`となりのコーデ` should complement the existing Akari v1.1 materials:

- It expands the `服で魅せる` idea from `となりのあかり`.
- It should not duplicate `となりの表情`, where facial reactions are primary.
- It should not duplicate `となりのしぐさ`, where body gesture is primary.
- It can reuse the same identity reference pack strategy from
  `となりのあかり`, but outfit prompts should not over-lock the white hoodie.

The collection should remain image-first and exploratory until the contact sheet
proves that the outfit direction is strong enough for a future booklet.

## Verification Plan

For this design-only step:

- Run `npm run lint:md`.

For a future implementation step:

- Validate new JSON manifests with `python -m json.tool`.
- Add or extend contract tests if coordinate manifests become part of the
  verified public snapshot.
- Build contact sheets before finishing individual images.
- Use the Akari v1.1 image-review gates for any finished candidate.

# Akari Situation Play Design

## Goal

Create lightweight, one-off Akari v1.2 situation illustrations without turning
them into a PDF, artbook, formal collection, or contact-sheet workflow. The
first pilot image depicts a cute, slightly messy post-work nap with a clear
everyday story.

## Scope

- Generate and review one pilot image before expanding to more situations.
- Save every generated pilot iteration under `source/generated/situation-play/`.
- Keep generated outputs out of git unless the user later requests otherwise.
- Do not create PDF assets, page manifests, selection manifests, contact sheets,
  or collection audits for this line.
- Do not modify the existing `v1-2-overhead-room` collection.

## Pilot Scene

Use a portrait canvas with a nearly direct overhead view. Akari lies diagonally
on an ivory rug beneath a low work desk after falling asleep. Her head rests on
a small cushion, one knee is loosely bent, and her arms rest naturally. She has
just begun to wake and returns a sleepy direct gaze with her mouth slightly
open.

Akari wears an oversized white hoodie, clearly constructed pale-gray lounge
shorts, and white socks with pale-blue stripes. The shorts must read as casual
roomwear rather than underwear.

The desk holds an open laptop, illegible notes, and a cooled mug. The floor has
one smartphone, two blue cables, and one closed notebook. These objects explain
the situation without obscuring Akari. Warm late-afternoon window light mixes
with a faint cool monitor fill.

## Reference Roles

- `source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp` controls face,
  adult age impression, amber eyes, warm-brown bob, and the complete two-part
  pale-blue hair ornament on character-left.
- `source/finished/v1-2-overhead-room/supine-direct-gaze.webp` controls body
  proportions, overhead anatomy, and hoodie/shorts/socks construction.
- `/path/to/input/ChatGPT Image 2026年7月13日 17_34_50.png` controls only
  the post-work storytelling, overhead composition, and prop density.
- `/path/to/input/ChatGPT Image 2026年7月13日 17_37_18.png` controls only
  the soft diagonal sunlight and intimate returned gaze.

The downloaded images are not identity, age, anatomy, hair, or wardrobe
references.

## Generation and Review

Use the built-in image generation path with all references loaded explicitly.
Generate one non-destructive pilot output. If the output is weak, change only
one prompt dimension per iteration.

Review in this order:

1. Akari identity and adult 25-year-old age impression.
2. Warm-brown bob, amber eyes, and complete character-left hair ornament.
3. Coherent hands, feet, limbs, and body connections in the overhead pose.
4. Clearly constructed hoodie, lounge shorts, and striped socks.
5. Immediate readability as a post-work nap in a cute, lightly messy room.
6. Akari remains the visual focus despite the props.

Reject outputs with readable text, logos, watermarks, extra characters, extra
digits or limbs, disconnected anatomy, underwear-like shorts, sexualized body
emphasis, or a childlike age impression.

## Output

Save the first output as
`source/generated/situation-play/20260713_work-crash-pilot_v1.png`. Preserve
later iterations as `v2`, `v3`, and so on rather than overwriting earlier
outputs.

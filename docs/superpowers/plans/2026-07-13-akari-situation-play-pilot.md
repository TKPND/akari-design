# Akari Situation Play Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review one lightweight Akari v1.2 post-work-nap situation illustration without adding it to a formal collection.

**Architecture:** Use the built-in image generation tool with four explicitly assigned local references. Save each generated iteration non-destructively under `source/generated/situation-play/`, then inspect the raster and perform a focused visual review before deciding whether one targeted regeneration is needed.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick `identify`, PNG output

## Global Constraints

- Do not modify the existing `v1-2-overhead-room` collection or its manifests.
- Do not create a PDF, page manifest, selection manifest, contact sheet, or collection audit.
- Keep generated outputs out of git unless the user later requests otherwise.
- Preserve Akari's accepted adult 25-year-old identity, warm amber eyes, warm-brown bob, and complete two-part pale-blue ornament on character-left.
- Reject readable text, logos, watermarks, extra characters, extra digits or limbs, disconnected anatomy, underwear-like shorts, sexualized body emphasis, and childlike age impression.

---

### Task 1: Generate and Review the Pilot Image

**Files:**

- Read: `source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp`
- Read: `source/finished/v1-2-overhead-room/supine-direct-gaze.webp`
- Read: `/path/to/input/ChatGPT Image 2026年7月13日 17_34_50.png`
- Read: `/path/to/input/ChatGPT Image 2026年7月13日 17_37_18.png`
- Create: `source/generated/situation-play/20260713_work-crash-pilot_v1.png`
- Create only if a targeted retry is required: `source/generated/situation-play/20260713_work-crash-pilot_v2.png`

**Interfaces:**

- Consumes: four raster references with the exact roles defined below.
- Produces: one reviewed portrait PNG suitable for informal project use.

- [ ] **Step 1: Load every reference and verify its role visually**

Use `view_image` on all four files before generation.

Reference roles:

1. Standard face controls identity, adult age impression, amber eyes, warm-brown bob, and complete character-left hair ornament.
2. Accepted overhead image controls body proportions, overhead anatomy, and hoodie/shorts/socks construction.
3. `17_34_50.png` controls only post-work storytelling, overhead composition, and prop density.
4. `17_37_18.png` controls only soft diagonal sunlight and the intimate returned gaze.

- [ ] **Step 2: Generate one built-in image with the approved prompt**

Use the built-in image generation tool with all four local paths as references and this prompt:

```text
Use case: illustration-story
Asset type: informal Akari v1.2 situation-play illustration
Primary request: Create one finished portrait illustration of adult 25-year-old Akari waking after accidentally falling asleep beneath her work desk.
Input images: Image 1 is the authoritative identity, age, face, eye, hair, and ornament reference. Image 2 is the authoritative body-proportion, overhead-anatomy, and roomwear-construction reference. Image 3 supplies only the post-work storytelling, overhead composition, and prop density. Image 4 supplies only the soft diagonal sunlight and intimate returned gaze. Do not copy identity, anatomy, hair, or wardrobe from Images 3 or 4.
Scene/backdrop: A nearly direct overhead view of an ivory rug beneath a low work desk. On the desk are an open laptop, visually illegible notes, and a cooled mug. On the floor are exactly one smartphone, two blue cables, one closed notebook, and one small head cushion. The room is cute and lightly messy, never chaotic.
Subject: Accepted Akari v1.2 identity, clearly an adult woman aged 25, with warm amber eyes, a warm-brown short bob, and the complete two-part pale-blue hair ornament on character-left. She lies diagonally on the rug with her head on the cushion, one knee loosely bent, arms resting naturally, and a sleepy direct gaze toward the viewer. Her mouth is slightly open as if she has just woken and is about to deny falling asleep.
Wardrobe: Oversized white hoodie, clearly constructed pale-gray lounge shorts that cannot be mistaken for underwear, and white socks with pale-blue stripes.
Style/medium: Polished contemporary anime illustration with natural fabric folds, believable room textures, and restrained detail.
Composition/framing: 1024x1536 portrait, 80-to-90-degree overhead camera, full figure readable from hair ornament to both socks, Akari remains the dominant visual focus.
Lighting/mood: Warm late-afternoon diagonal window light mixed with a faint cool monitor fill; sleepy, familiar, affectionate, and healthy.
Constraints: Preserve adult age impression, official identity, body proportions, complete ornament placement, coherent hands and feet, connected limbs, constructed roomwear, and a non-sexualized everyday mood. Props explain the situation without covering the face or body.
Avoid: readable text or numbers, logos, branding, watermarks, borders, panels, other characters, extra limbs, extra fingers, disconnected anatomy, underwear-like shorts, body-part emphasis, suggestive exposure, childlike proportions, school-age cues, clutter covering Akari.
```

Do not request a destination path from the built-in tool. Generate first, then copy the resulting PNG to the exact `v1` workspace path. If the image appears in the conversation but no PNG is available, structurally extract the current day's `image_generation_call` whose `result` starts with `iVBOR`, verify decoded bytes begin with PNG signature `89504e470d0a1a0a`, and save them to the exact `v1` path.

- [ ] **Step 3: Verify the saved raster mechanically**

Run:

```bash
identify source/generated/situation-play/20260713_work-crash-pilot_v1.png
```

Expected: one readable PNG image with portrait dimensions and no decode errors.

- [ ] **Step 4: Review the generated image visually**

Open the saved PNG with `view_image` and review in this order:

1. Identity and adult 25-year-old age impression.
2. Amber eyes, warm-brown bob, and complete character-left ornament.
3. Hands, feet, limb count, and overhead body connections.
4. Hoodie, lounge shorts, and striped socks construction.
5. Immediate readability as a lightly messy post-work nap.
6. Akari remains the focus and the returned gaze feels close but healthy.

Expected: all six checks pass and none of the global rejection conditions appear.

- [ ] **Step 5: Perform at most one single-dimension retry if required**

If a hard gate fails, generate `v2` while changing only the failed dimension. Repeat the unchanged prompt and append exactly one correction sentence describing the observed failure, such as:

```text
Correction: Preserve the entire scene and composition, but repair the character-left hair ornament so both crossed pins and the tied ribbon with two tails are fully present and clearly separated.
```

If the first image passes, skip this step. Never overwrite `v1`.

- [ ] **Step 6: Report the selected output without committing generated files**

Run:

```bash
git status --short -- source/generated/situation-play
```

Expected: the selected PNG is untracked or ignored and no generated image is staged. Report the selected absolute path, the built-in generation path, the final prompt, and the visual review result.

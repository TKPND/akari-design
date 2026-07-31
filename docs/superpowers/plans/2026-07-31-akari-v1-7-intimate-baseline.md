# Akari v1.7 Intimate Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce and review three tightly bounded Akari v1.7
micro-expression candidates by editing the accepted v1.5 B3 image directly.

**Architecture:** Treat B3 as the only image-generation input and start each
candidate independently from it. Keep all candidates in an ignored v1.7
working directory, verify each PNG and its visual invariants, then compare B3
and A/B/C at equal scale before returning to an explicit user selection gate.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick
`identify` and `magick montage`, `xxd`, SHA-256, and Git read-only checks.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-31-akari-v1-7-intimate-baseline-design.md`.
- Use
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
  as the sole positive visual authority supplied to image generation.
- Expected B3 SHA-256 is
  `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`.
- Candidate A, B, and C each start independently from B3. Never edit one
  candidate into another and never supply a v1.6 image to generation.
- Preserve B3 face construction, eye design, hair, ornament, body, pose,
  outfit, background, lighting, framing, and hand-painted rendering.
- Change only the candidate-specific gaze connection and mouth response.
- Generate serially. Do not overlap image-generation or montage operations.
- Keep all review-stage output under ignored
  `build/v1.7-intimate-baseline/`.
- Do not modify or delete v1.5 sources, v1.6 drafts, or the external v1.5
  Kawaii 1000 gallery.
- Do not promote a candidate or create `akari-v1.7/` before explicit user
  selection.
- Do not run Python tests, Node tests, PDF builds, OCR, or release gates.
- Do not run an automatic correction attempt after A/B/C. If all three fail,
  keep B3 and return to a design decision.

---

### Task 1: Generate and review V17-01 A/B/C

**Files:**

- Read:
  `docs/superpowers/specs/2026-07-31-akari-v1-7-intimate-baseline-design.md`
- Read:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
- Inspect as emotional evidence only:
  `/home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/images/akari_v150_kawaii1000_B001_017_everyday-girly_sleeve-hidden-compliment.png`
- Inspect as emotional evidence only:
  `/home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/images/akari_v150_kawaii1000_B001_020_everyday-girly_curtain-peek-tease.png`
- Inspect as emotional evidence only:
  `/home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/images/akari_v150_kawaii1000_B001_026_hobbies-making_successful-souffle-lift.png`
- Inspect as emotional evidence only:
  `/home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/images/akari_v150_kawaii1000_B001_031_travel-walking_departure-board-turn.png`
- Create:
  `build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-a1.png`
- Create:
  `build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png`
- Create:
  `build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-c1.png`
- Create:
  `build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-comparison-a-c.png`

**Interfaces:**

- Consumes: one exact B3 PNG plus the approved v1.7 design contract.
- Produces: three independent review candidates and one labeled comparison;
  no tracked release asset, manifest mutation, or code change.

- [ ] **Step 1: Verify the source, output boundary, and Git state**

Run:

```bash
sha256sum akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png
identify akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png
git check-ignore -v build/v1.7-intimate-baseline/probe.png
git status --short --branch
mkdir -p build/v1.7-intimate-baseline
```

Expected:

- the B3 digest exactly matches the global constraint;
- `identify` reports a valid portrait PNG;
- `git check-ignore` identifies the `build/` rule;
- there are no unexpected tracked changes;
- the v1.7 output directory exists without touching v1.6.

- [ ] **Step 2: Open the visual authority and emotional evidence**

Use `view_image` with original detail for B3 and the four evidence images
listed under **Files**. Keep them visible in the image-generation context and
state these roles before the first generation:

- B3 is the sole generation input and controls identity, adult age, face,
  eyes, hair, ornament, body balance, pose, comparison outfit, background,
  lighting, framing, and rendering;
- B001-017 demonstrates restrained happiness after being noticed or praised;
- B001-020 demonstrates familiar direct eye contact without a broad smile;
- B001-026 demonstrates quiet happiness after a small success;
- B001-031 demonstrates the instant of noticing something and brightening.

Do not pass any of the four evidence images to `image_gen`. They support human
judgment only and must not blend into B3.

Expected: B3 is readable at original detail and the evidence confirms that
the intended appeal comes from emotional timing rather than new facial
features.

- [ ] **Step 3: Generate candidate A independently from B3**

Use the built-in `image_gen` with only this referenced image path:

```text
/home/takahiro/workspace/akari-design/akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png
```

Use this complete prompt:

```text
Use case: precise localized identity-preserving image edit.
Asset: Akari v1.7 V17-01 candidate A, "Eye Contact".

Image 1 is the SOLE visual authority and the exact edit target. Preserve the
same Akari, age 25, and preserve the complete image outside the smallest
necessary facial edit. Do not use a different interpretation of the
character.

Primary request:
Create a new full-resolution copy of Image 1 in which Akari has just noticed
the familiar viewer and her gaze connects a little more directly. Edit only
the iris/pupil direction needed for natural eye contact. Keep her mouth almost
exactly as in Image 1. Preserve the existing head angle unless an
imperceptibly small adjustment is necessary for coherent eye contact.

Exact invariants:
- Preserve face outline, cheek volume, compact chin, nose, ears, neck, adult
  age impression, and skin tone.
- Preserve eye size, eye opening, eye tilt, eyelids, lashes, line weight,
  iris size, amber color, highlight count, highlight size, and brow shape.
- Do not make the eyes rounder, larger, darker, shinier, wetter, or more
  childlike. Do not add catchlights.
- Preserve the small closed mouth, restrained blush, and subtle lip color.
- Preserve the short airy chestnut bob, asymmetric looseness, irregular hair
  tips, highlight language, and exact pale-blue crossed ornament with its
  fine cord detail.
- Preserve the complete B3 body balance, head-to-body ratio, torso, moderate
  upper-body volume, waist, healthy thighs, limbs, hands, feet, pose, and
  contact with the floor.
- Preserve the white T-shirt, pale-blue shorts, all folds, bare feet, warm
  apartment, directional domestic light, floor, shadow, framing, resolution,
  aspect ratio, and hand-painted rendering.
- No crop, zoom, camera shift, recentering, global relighting, cleanup pass,
  beautification, or restyling.

Avoid:
No broad smile, open mouth, teeth, smugness, seduction, glamour, gyaru styling,
heavy lashes, eyeliner, cosmetic makeup, strong blush, tan drift, oversized
eyes, doll face, sharp V jaw, Honey Brown salon bob, parallel pins, glossy
highlight bands, cropped box T-shirt, culottes, smartwatch, socks, sneakers,
white studio background, generic polished reference-sheet style, child body,
model elongation, exaggerated curves, new accessories, text, label, border,
logo, or watermark.
```

Expected: one candidate that differs from B3 only in the natural connection
of the gaze. Record the exact generated source path or generation result ID.

- [ ] **Step 4: Save and verify candidate A**

Copy the exact source PNG returned by the generation tool to:

```text
build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-a1.png
```

Do not move or delete the generation tool's source file. Then run:

```bash
xxd -p -l 8 build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-a1.png
identify build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-a1.png
sha256sum build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-a1.png
```

Expected: signature `89504e470d0a1a0a`, one valid portrait PNG, and one
SHA-256 digest.

If the image appears in the conversation but no local source PNG is reported,
follow the repository's rollout payload recovery procedure. Parse the exact
current-day rollout JSONL structurally, select an `image_generation_call`
whose `result` begins with `iVBOR`, decode that payload, verify the same PNG
signature before accepting it, and record the generation or request ID used.
Never copy a base64 payload manually from terminal output.

- [ ] **Step 5: Generate candidate B independently from B3**

Use the built-in `image_gen` again with only the original B3 referenced image
path. Do not reference candidate A. Use this complete prompt:

```text
Use case: precise localized identity-preserving image edit.
Asset: Akari v1.7 V17-01 candidate B, "Slightly Happy".

Image 1 is the SOLE visual authority and the exact edit target. Preserve the
same Akari, age 25, and preserve the complete image outside the smallest
necessary facial edit. Do not use a different interpretation of the
character.

Primary request:
Create a new full-resolution copy of Image 1 showing the instant Akari notices
the familiar viewer and becomes quietly, genuinely pleased. Preserve direct,
familiar eye contact. Deepen only the existing small closed-mouth smile by a
very slight amount, as if happiness has just reached the mouth before she
poses. Keep the expression understated and spontaneous.

Exact invariants:
- Preserve face outline, cheek volume, compact chin, nose, ears, neck, adult
  age impression, and skin tone.
- Preserve eye size, eye shape, eye tilt, iris size and density, amber color,
  eyelids, lashes, catchlights, line weight, and brow shape exactly. The eyes
  must not become the mechanism for adding cuteness.
- Keep the mouth closed and small. Change only its restrained curvature and
  the minimum natural cheek response. Do not add teeth, lip gloss, lipstick,
  dimples, or stronger blush.
- Preserve the short airy chestnut bob, asymmetric looseness, irregular hair
  tips, highlight language, and exact pale-blue crossed ornament with its
  fine cord detail.
- Preserve the complete B3 body balance, head-to-body ratio, torso, moderate
  upper-body volume, waist, healthy thighs, limbs, hands, feet, pose, and
  contact with the floor.
- Preserve the white T-shirt, pale-blue shorts, all folds, bare feet, warm
  apartment, directional domestic light, floor, shadow, framing, resolution,
  aspect ratio, and hand-painted rendering.
- No crop, zoom, camera shift, recentering, global relighting, cleanup pass,
  beautification, or restyling.

Avoid:
No broad anime smile, open mouth, teeth, performance, smugness, seduction,
glamour, gyaru styling, heavy lashes, eyeliner, cosmetic makeup, strong blush,
tan drift, oversized eyes, doll face, sharp V jaw, Honey Brown salon bob,
parallel pins, glossy highlight bands, cropped box T-shirt, culottes,
smartwatch, socks, sneakers, white studio background, generic polished
reference-sheet style, child body, model elongation, exaggerated curves, new
accessories, text, label, border, logo, or watermark.
```

Expected: one candidate with a slightly warmer closed-mouth response while
all identity and full-image invariants remain unchanged. Record the exact
generated source path or generation result ID.

- [ ] **Step 6: Save and verify candidate B**

Copy the exact returned source PNG to:

```text
build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png
```

Then run:

```bash
xxd -p -l 8 build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png
identify build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png
sha256sum build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png
```

Expected: signature `89504e470d0a1a0a`, one valid portrait PNG, and one
SHA-256 digest. If no local source exists, use the same structural rollout
recovery procedure from Step 4 and verify the generation or request ID.

- [ ] **Step 7: Generate candidate C independently from B3**

Use the built-in `image_gen` again with only the original B3 referenced image
path. Do not reference candidates A or B. Use this complete prompt:

```text
Use case: precise localized identity-preserving image edit.
Asset: Akari v1.7 V17-01 candidate C, "Cannot Quite Hide It".

Image 1 is the SOLE visual authority and the exact edit target. Preserve the
same Akari, age 25, and preserve the complete image outside the smallest
necessary facial edit. Do not use a different interpretation of the
character.

Primary request:
Create a new full-resolution copy of Image 1 showing the instant Akari notices
the familiar viewer and cannot quite hide that she is pleased. Preserve the
same direct eye contact and keep the mouth closed. Let only the image-left
corner of her mouth, on her unpinned side, rise a fraction earlier than the
image-right corner. The result is a spontaneous trace of happiness, not a
deliberate teasing or knowing expression.

Exact invariants:
- Preserve face outline, cheek volume, compact chin, nose, ears, neck, adult
  age impression, and skin tone.
- Preserve eye size, eye shape, eye tilt, iris size and density, amber color,
  eyelids, lashes, catchlights, line weight, brow height, and brow shape
  exactly.
- Keep the mouth small and closed. Limit change to the minimal image-left
  mouth-corner asymmetry and its physically natural cheek response. Keep the
  image-right mouth corner at the B3 level.
- Preserve the short airy chestnut bob, asymmetric looseness, irregular hair
  tips, highlight language, and exact pale-blue crossed ornament with its
  fine cord detail.
- Preserve the complete B3 body balance, head-to-body ratio, torso, moderate
  upper-body volume, waist, healthy thighs, limbs, hands, feet, pose, and
  contact with the floor.
- Preserve the white T-shirt, pale-blue shorts, all folds, bare feet, warm
  apartment, directional domestic light, floor, shadow, framing, resolution,
  aspect ratio, and hand-painted rendering.
- No crop, zoom, camera shift, recentering, global relighting, cleanup pass,
  beautification, or restyling.

Avoid:
No smirk, smugness, teasing, knowing look, raised brow, narrowed eye, wink,
seduction, broad smile, open mouth, teeth, glamour, gyaru styling, heavy
lashes, eyeliner, cosmetic makeup, strong blush, tan drift, oversized eyes,
doll face, sharp V jaw, Honey Brown salon bob, parallel pins, glossy highlight
bands, cropped box T-shirt, culottes, smartwatch, socks, sneakers, white
studio background, generic polished reference-sheet style, child body, model
elongation, exaggerated curves, new accessories, text, label, border, logo,
or watermark.
```

Expected: one candidate with a minimal image-left mouth-corner lead and no
smug or knowing drift. Record the exact generated source path or generation
result ID.

- [ ] **Step 8: Save and verify candidate C**

Copy the exact returned source PNG to:

```text
build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-c1.png
```

Then run:

```bash
xxd -p -l 8 build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-c1.png
identify build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-c1.png
sha256sum build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-c1.png
```

Expected: signature `89504e470d0a1a0a`, one valid portrait PNG, and one
SHA-256 digest. If no local source exists, use the same structural rollout
recovery procedure from Step 4 and verify the generation or request ID.

- [ ] **Step 9: Inspect all three candidates before making a comparison**

Open A, B, and C individually with `view_image` at original detail. For each
candidate, record `PASS` or the exact failed invariants in this order:

1. same B3 face and adult age impression;
2. unchanged eye construction, lashes, iris density, brows, and makeup level;
3. unchanged airy chestnut bob and crossed ornament with cord detail;
4. unchanged body balance, pose, hands, feet, outfit, and bare-foot state;
5. unchanged apartment, light direction, framing, and hand-painted finish;
6. candidate-specific gaze or mouth response;
7. no v1.6 styling, generic polished-girl drift, anatomy defect, text, or
   watermark.

Expected: every candidate receives an explicit invariant assessment. Do not
request or generate a correction, even if one candidate fails.

- [ ] **Step 10: Build and inspect the equal-scale comparison**

Run:

```bash
magick montage \
  -label 'B3 / Original' \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  -label 'A / Eye Contact' \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-a1.png \
  -label 'B / Slightly Happy' \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png \
  -label 'C / Cannot Quite Hide It' \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-c1.png \
  -thumbnail '640x960>' -tile 2x2 -geometry +20+48 \
  -background '#eaded3' -fill '#4e3b34' -pointsize 28 \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-comparison-a-c.png
```

Then run:

```bash
identify build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-comparison-a-c.png
sha256sum build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-comparison-a-c.png
git status --short --branch
```

Open the comparison at original detail with `view_image`.

Expected:

- B3 and A/B/C appear at equal scale with readable labels;
- expression differences are visible without a composition difference;
- generated output remains ignored and no tracked file changes appear.

- [ ] **Step 11: Return to the explicit user selection gate**

Present the labeled comparison and summarize:

- which candidates pass all hard identity and anti-v1.6 constraints;
- whether any candidate is clearly more emotionally appealing than B3;
- the strongest candidate and the reason for the recommendation;
- any remaining non-blocking redraw differences.

Ask the user to choose exactly one of:

1. select A, B, or C as the working V17-01 baseline;
2. keep B3 unchanged because none improves it;
3. stop and revise the design before any further generation.

Expected: no promotion, manifest change, tracked image, correction generation,
or v1.7 package creation occurs before the user's explicit selection.

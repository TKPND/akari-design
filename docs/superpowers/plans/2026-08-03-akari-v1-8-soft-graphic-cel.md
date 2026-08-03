# Akari v1.8 Soft Graphic Cel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, verify, review, and present three same-condition Akari v1.8
soft graphic cel candidates, then stop at an explicit user selection gate.

**Architecture:** Start A, B, and C independently from one hash-pinned copy of
the accepted V17-01 front image. Supply two user-provided JPEGs only as
role-limited rendering references, keep all generated and review material in
an ignored working directory, and compare the baseline and candidates at equal
scale before asking the user to choose. Promotion is a later task after the
choice and is not part of this plan.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick
`identify` and `magick montage`, `cmp`, `xxd`, SHA-256, Markdown, and Git
read-only checks.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-08-03-akari-v1-8-soft-graphic-cel-design.md`.
- Execute in the isolated worktree
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel`
  on branch `codex/akari-v1-8-soft-graphic-cel`, created at execution time with
  `superpowers:using-git-worktrees`.
- The design commit `937cd1e` must be an ancestor of the execution checkout.
- V17-01 is the sole character and scene authority. Its SHA-256 must be
  `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`.
- v1.5 B3 is body-balance human-QA evidence only. Its SHA-256 must be
  `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`.
- v1.4 G2 is line-and-paint human-QA evidence only. Its SHA-256 must be
  `6757e601d2cfd158c970ab701a876981ace837e669c313dec6d25c0c539ff4d6`.
- `G6f1r23aIAANle8.jpg` is the primary rendering reference. Its SHA-256
  must be
  `765a3832f8543445ff099b3a0d22052c7860bf03a6f8e0ebca64ebb1cea7c54a`.
- `HOvzZrzboAA3IDA.jpg` is the secondary rendering reference. Its SHA-256
  must be
  `526c47317339db5e9fa087ac0d31a796a20e6d386e2881c9197bd05b9628dd14`.
- Pass exactly three images to every generation call, in this order: V17-01,
  the primary rendering reference, then the secondary rendering reference.
  Never pass B3, G2, the other two attachments, a v1.6 image, or a sibling
  candidate to generation.
- A, B, and C each start independently from the same V17-01 input copy. Never
  edit one candidate into another.
- Preserve every item in the design's `Locked Character and Scene Design`
  section. Any drift in identity, adult age, fixed expression, eyes, hair,
  ornament, body, pose, anatomy, outfit, framing, apartment, or light is a
  hard-gate failure.
- Generate serially. Do not overlap image-generation, image-copy, verification,
  montage, or original-detail inspection operations.
- Keep all inputs copied from attachments, exact prompts, generated candidates,
  comparisons, hashes, and review notes under ignored
  `build/v1.8-soft-graphic-cel/`.
- If an expected input or output already exists, do not overwrite it. Verify
  its hash, provenance, signature, dimensions, and completed task state before
  resuming from the first incomplete step.
- Generate exactly one A/B/C set. Do not retry, repair, composite, or generate
  a correction round before the user reviews the comparison.
- Do not promote a candidate or create `akari-v1.8/` in this plan.
- Do not commit the supplied JPEGs, candidates, comparison, prompt copies, or
  review notes.
- Do not run PDF builds or audits, OCR, Python tests, Node tests, integration
  gates, or release gates.

---

### Task 1: Freeze and inspect the V18-01 reference set

**Files:**

- Read:
  `docs/superpowers/specs/2026-08-03-akari-v1-8-soft-graphic-cel-design.md`
- Read and copy:
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`
- Inspect as human-QA evidence only:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
- Inspect as human-QA evidence only:
  `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
- Read and copy from the user attachment:
  `/home/takahiro/.codex/attachments/79d4c195-f0cb-4e26-8f11-f71de3e5c7d2/G6f1r23aIAANle8.jpg`
- Read and copy from the user attachment:
  `/home/takahiro/.codex/attachments/0244f8c6-b867-4bf7-82aa-5ad758a41d0b/HOvzZrzboAA3IDA.jpg`
- Create ignored input copy:
  `build/v1.8-soft-graphic-cel/input/v17-01-authority.png`
- Create ignored input copy:
  `build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg`
- Create ignored input copy:
  `build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg`

**Interfaces:**

- Consumes: one tracked character-and-scene authority, two tracked human-QA
  references, two user-supplied style JPEGs, and the approved design contract.
- Produces: one ignored, hash-pinned, ordered three-image generation input set;
  no tracked asset or code change.

- [ ] **Step 1: Verify checkout, source hashes, tools, and output boundary**

Run from the isolated worktree:

```bash
test "$(pwd -P)" = "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel"
test "$(git branch --show-current)" = "codex/akari-v1-8-soft-graphic-cel"
git merge-base --is-ancestor 937cd1e HEAD
git diff --quiet
git diff --cached --quiet
git status --short --branch
sha256sum \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png \
  /home/takahiro/.codex/attachments/79d4c195-f0cb-4e26-8f11-f71de3e5c7d2/G6f1r23aIAANle8.jpg \
  /home/takahiro/.codex/attachments/0244f8c6-b867-4bf7-82aa-5ad758a41d0b/HOvzZrzboAA3IDA.jpg
identify -format '%f | %m %wx%h\n' \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png \
  /home/takahiro/.codex/attachments/79d4c195-f0cb-4e26-8f11-f71de3e5c7d2/G6f1r23aIAANle8.jpg \
  /home/takahiro/.codex/attachments/0244f8c6-b867-4bf7-82aa-5ad758a41d0b/HOvzZrzboAA3IDA.jpg
command -v identify
command -v magick
command -v cmp
command -v xxd
command -v sha256sum
git check-ignore -v build/v1.8-soft-graphic-cel/probe.png
```

Expected:

- the checkout path, branch, and design ancestry checks pass;
- tracked and staged diffs are empty;
- all five hashes match the global constraints;
- V17-01, B3, and G2 are `PNG 1024x1536`;
- the primary style JPEG is `1776x2624` and the secondary is `1536x2304`;
- all five required commands resolve;
- `git check-ignore` identifies the repository `build/` rule.

- [ ] **Step 2: Create immutable ignored input copies**

Confirm none of the destinations exists, then run:

```bash
mkdir -p \
  build/v1.8-soft-graphic-cel/input \
  build/v1.8-soft-graphic-cel/prompts
test ! -e build/v1.8-soft-graphic-cel/input/v17-01-authority.png
test ! -e build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg
test ! -e build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg
cp --no-clobber \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  build/v1.8-soft-graphic-cel/input/v17-01-authority.png
cp --no-clobber \
  /home/takahiro/.codex/attachments/79d4c195-f0cb-4e26-8f11-f71de3e5c7d2/G6f1r23aIAANle8.jpg \
  build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg
cp --no-clobber \
  /home/takahiro/.codex/attachments/0244f8c6-b867-4bf7-82aa-5ad758a41d0b/HOvzZrzboAA3IDA.jpg \
  build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg
cmp \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  build/v1.8-soft-graphic-cel/input/v17-01-authority.png
cmp \
  /home/takahiro/.codex/attachments/79d4c195-f0cb-4e26-8f11-f71de3e5c7d2/G6f1r23aIAANle8.jpg \
  build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg
cmp \
  /home/takahiro/.codex/attachments/0244f8c6-b867-4bf7-82aa-5ad758a41d0b/HOvzZrzboAA3IDA.jpg \
  build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg
sha256sum build/v1.8-soft-graphic-cel/input/*
```

Expected: all three `cmp` calls exit zero and all three copied hashes match the
corresponding global constraints. If a destination already exists, stop before
`cp`; verify it against both its intended source and expected hash rather than
replacing it.

- [ ] **Step 3: Open every reference at original detail and state its role**

Use `view_image` with original detail for these five images:

1. `build/v1.8-soft-graphic-cel/input/v17-01-authority.png`;
2. `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`;
3. `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`;
4. `build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg`;
5. `build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg`.

Immediately state and keep visible in the generation context:

- Image 1 is the exact edit target and sole authority for Akari's identity,
  age, face, eyes, expression, hair, ornament, body, pose, outfit, framing,
  apartment, and light;
- B3 is post-generation human-QA evidence for restrained upper-body volume,
  subtle waist, healthy thighs and calves, adult limb length, and neutral
  balance; it is not passed to generation;
- G2 is post-generation human-QA evidence for intentional outer contours,
  quieter interior lines, adult-face continuity, and readable paint planes; it
  is not passed to generation;
- Image 2 controls only fine colored linework, soft two-to-three-step cel
  shading, clean material separation, and polished finish;
- Image 3 controls only contour hierarchy, matte cloth, restrained highlights,
  and clean shape grouping.

Expected: each visual role is explicit before generation, and no style image
has authority over character or scene design.

- [ ] **Step 4: Confirm Task 1 leaves the tracked tree unchanged**

Run:

```bash
git status --short --branch
git diff --quiet
git diff --cached --quiet
git check-ignore -v \
  build/v1.8-soft-graphic-cel/input/v17-01-authority.png \
  build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg \
  build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg
```

Expected: the tracked and staged trees remain clean and all copied inputs are
ignored. Do not create a commit for this task; its deliverable is intentionally
local and hash-verified.

---

### Task 2: Generate and verify A, B, and C independently

**Files:**

- Read:
  `build/v1.8-soft-graphic-cel/input/v17-01-authority.png`
- Read:
  `build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg`
- Read:
  `build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg`
- Create ignored immutable prompt:
  `build/v1.8-soft-graphic-cel/prompts/a-gentle.txt`
- Create ignored immutable prompt:
  `build/v1.8-soft-graphic-cel/prompts/b-balanced.txt`
- Create ignored immutable prompt:
  `build/v1.8-soft-graphic-cel/prompts/c-graphic.txt`
- Create:
  `build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png`
- Create:
  `build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png`
- Create:
  `build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png`

**Interfaces:**

- Consumes: the ordered, hash-pinned three-image input set from Task 1 and the
  complete immutable prompt for each candidate below.
- Produces: three immutable ignored prompt copies and their SHA-256 values;
  three independent valid PNG candidates; their generation/request IDs,
  returned source paths, dimensions, and SHA-256 values; no tracked asset.

- [ ] **Step 1: Reopen the ordered inputs and generate A / Gentle**

Open V17-01, B3, G2, the primary style JPEG, and the secondary style JPEG again
at original detail immediately before the call. Restate that V17-01 alone
controls character and scene, that B3 and G2 are human-QA-only, and that the
two JPEGs control only their approved rendering roles. Use `image_gen` with
this exact ordered array:

```javascript
referenced_image_paths: [
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/v17-01-authority.png",
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg",
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg"
]
```

Use this complete prompt:

```text
Use case: full-frame identity-preserving rendering translation.
Asset: Akari v1.8 V18-01 candidate A, "Gentle".

Image 1 is the exact edit target and the SOLE authority for the character and
scene. Preserve the same Akari, age 25, identity, face, expression, hair,
ornament, body, pose, clothing, framing, apartment, and warm directional light.
Images 2 and 3 are STYLE-ONLY references. They have zero authority over
identity, age, anatomy, proportions, hair, ornament, clothing, pose, props,
camera, background, palette, or scene content.

Primary request:
Redraw the complete Image 1 at the same portrait aspect ratio and the same
full-body composition. Change only its rendering language to the GENTLE end of
soft graphic cel illustration. Make the smallest clearly visible style shift:
organize the contours, consolidate painted micro-shadows into larger readable
planes, and keep a little of Image 1's soft hand-painted transition. The result
must read immediately as the exact same adult Akari in the exact same moment,
not as a redesign or a new interpretation.

Rendering target:
- Use thin warm-gray or warm-brown outer contours, never hard black.
- Keep the silhouette clearer than interior lines. Remove duplicate or scratchy
  texture lines, but retain natural hand, foot, garment, and airy-hair structure.
- Use two to three broad cel-shadow families while preserving some soft skin
  and room-light transitions.
- Keep skin warm peach with restrained cheek color, one coherent shadow family,
  and sparse highlights.
- Keep hair chestnut brown, short, airy, asymmetrical, and irregular at the
  tips. Group it into larger planes with only a restrained, slightly crisper
  highlight accent.
- Keep the cotton T-shirt and lounge shorts matte. Explain their existing drape
  with broad shadow shapes rather than gloss or dense crease lines.
- Preserve the apartment geometry and warm light direction while simplifying
  only small painted texture into cleaner shapes.

Exact invariants from Image 1:
- Preserve the softly rounded cheeks, compact chin, nose, ears, face width,
  adult age impression, quiet closed-mouth smile, gaze, brow weight, restrained
  blush, and skin hue.
- Preserve eye size, opening, tilt, iris scale, amber color, catchlights,
  eyelids, lashes, and expression. Do not make the eyes the mechanism for
  increasing cuteness.
- Preserve the complete short chestnut bob and one character-left pale-blue
  crossed-pin ornament with its fine cord loops and two narrow tails.
- Preserve head-to-body ratio, neck, shoulders, upper-body volume, subtle
  waist, pelvis, healthy thighs and calves, limb lengths, hands, feet, neutral
  stance, and floor contact.
- Preserve the white T-shirt and pale-blue lounge shorts: same silhouette,
  neckline, sleeves, hems, waistband, drawstring, fit, and drape logic.
- Preserve camera, crop, full-body scale, placement, floor, wall, light shapes,
  shadow direction, resolution class, and aspect ratio.

Avoid:
No black hair, long hair, twin tails, side ponytail, heavy straight bangs,
school uniform, neck ribbon, scrunchies, new props, stars, geometry, stickers,
border, text, logo, or watermark. No oversized or rounder eyes, child face,
doll face, chibi proportions, sharper V jaw, petite body, model elongation,
slimmer anime legs, stronger bust separation, pinched waist, hip flare, pin-up
pose, makeup, glamour, seduction, broad anime smile, open mouth, or teeth. No
hard black outline, plastic shine shared by skin/hair/cloth, photoreal skin,
paper texture, grain, bloom, chromatic aberration, global smoothing, white
studio background, crop, zoom, recentering, camera shift, or global relighting.
```

Before the tool call, use `apply_patch` to create
`build/v1.8-soft-graphic-cel/prompts/a-gentle.txt` with the exact contents of
the prompt block above, excluding the Markdown fences and including one final
newline. Run:

```bash
sha256sum build/v1.8-soft-graphic-cel/prompts/a-gentle.txt
```

Record the digest, then pass the prompt file's complete text to `image_gen`
without edits. The recorded tool-call prompt must match the prompt file
byte-for-byte.

Record A's outer request/call ID, completed generation ID, exact returned
source path, and whether a local source PNG was returned. Do not start B before
A is saved and verified.

Expected: one full-frame candidate showing the smallest clear soft-cel shift,
with no deliberate character or scene change.

- [ ] **Step 2: Save, verify, and inspect A**

Copy the literal returned source PNG path, without transformation, to:

```text
build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png
```

Use `cp --no-clobber` with the literal returned source path. Do not move,
delete, resize, re-encode, optimize, or overwrite the generation source. Then
run:

```bash
xxd -p -l 8 \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png
identify -format '%f | %m %wx%h\n' \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png
sha256sum \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png
```

Expected: PNG signature `89504e470d0a1a0a`, one valid portrait PNG, one
recorded dimension pair, and one recorded SHA-256. Open A with `view_image` at
original detail and record obvious hard-gate failures without retrying it.

If the image appears in the conversation but no local PNG exists, follow the
repository rollout recovery instructions. Search the current-day rollout JSONL
for `image_generation_call`, parse JSONL structurally, select the completed
item whose `result` begins with `iVBOR`, base64-decode it, verify the PNG
signature before saving it to the exact A path, and record the selected request
or generation ID. Never copy a large payload manually from terminal output.

- [ ] **Step 3: Reopen the ordered inputs and generate B / Balanced**

Open V17-01, B3, G2, the primary style JPEG, and the secondary style JPEG again
at original detail. Restate that V17-01 alone controls character and scene,
that B3 and G2 are human-QA-only, and that the two JPEGs control only their
approved rendering roles. Use `image_gen` with this exact ordered array. Do not
reference A:

```javascript
referenced_image_paths: [
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/v17-01-authority.png",
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg",
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg"
]
```

Use this complete prompt:

```text
Use case: full-frame identity-preserving rendering translation.
Asset: Akari v1.8 V18-01 candidate B, "Balanced".

Image 1 is the exact edit target and the SOLE authority for the character and
scene. Preserve the same Akari, age 25, identity, face, expression, hair,
ornament, body, pose, clothing, framing, apartment, and warm directional light.
Images 2 and 3 are STYLE-ONLY references. They have zero authority over
identity, age, anatomy, proportions, hair, ornament, clothing, pose, props,
camera, background, palette, or scene content.

Primary request:
Redraw the complete Image 1 at the same portrait aspect ratio and the same
full-body composition. Change only its rendering language to a BALANCED soft
graphic cel illustration: a clear midpoint between Image 2's fine colored
linework and soft two-to-three-step shading and Image 3's clean contour
hierarchy, matte cloth, restrained highlights, and grouped shapes. Remove the
current painted microtexture more decisively than the Gentle candidate while
preserving Akari's intimate warmth and every fixed design fact. The result must
read immediately as the exact same adult Akari in the exact same moment, not as
a redesign or a new interpretation.

Rendering target:
- Use thin, deliberate warm-gray or warm-brown outer contours and quieter,
  lower-contrast interior lines, never hard black.
- Organize the figure and room into large, readable shapes with soft
  two-to-three-step cel shading.
- Keep skin warm peach and softly luminous through color choice, not airbrush
  texture: restrained cheek color, one coherent shadow family, and sparse
  highlights.
- Keep hair chestnut brown, short, airy, asymmetrical, and irregular at the
  tips. Use larger grouped hair planes and one limited, slightly crisper
  highlight band without turning it glossy black or salon-smooth.
- Keep the cotton T-shirt and lounge shorts matte. Preserve garment construction
  and drape while translating fine folds into broad, clean shadow shapes.
- Preserve the apartment geometry, floor, wall, framing, and warm light
  direction. Translate painted surface texture into quieter cel-rendered planes.
- Keep skin, hair, and cloth materially distinct. Never apply one plastic shine
  treatment across them.

Exact invariants from Image 1:
- Preserve the softly rounded cheeks, compact chin, nose, ears, face width,
  adult age impression, quiet closed-mouth smile, gaze, brow weight, restrained
  blush, and skin hue.
- Preserve eye size, opening, tilt, iris scale, amber color, catchlights,
  eyelids, lashes, and expression. Do not enlarge, darken, polish, or brighten
  the eyes to increase anime appeal.
- Preserve the complete short chestnut bob and one character-left pale-blue
  crossed-pin ornament with its fine cord loops and two narrow tails.
- Preserve head-to-body ratio, neck, shoulders, upper-body volume, subtle
  waist, pelvis, healthy thighs and calves, limb lengths, hands, feet, neutral
  stance, and floor contact.
- Preserve the white T-shirt and pale-blue lounge shorts: same silhouette,
  neckline, sleeves, hems, waistband, drawstring, fit, and drape logic.
- Preserve camera, crop, full-body scale, placement, floor, wall, light shapes,
  shadow direction, resolution class, and aspect ratio.

Avoid:
No black hair, long hair, twin tails, side ponytail, heavy straight bangs,
school uniform, neck ribbon, scrunchies, new props, stars, geometry, stickers,
border, text, logo, or watermark. No oversized or rounder eyes, child face,
doll face, chibi proportions, sharper V jaw, petite body, model elongation,
slimmer anime legs, stronger bust separation, pinched waist, hip flare, pin-up
pose, makeup, glamour, seduction, broad anime smile, open mouth, or teeth. No
hard black outline, plastic shine shared by skin/hair/cloth, photoreal skin,
paper texture, grain, bloom, chromatic aberration, global smoothing, white
studio background, crop, zoom, recentering, camera shift, or global relighting.
```

Before the tool call, use `apply_patch` to create
`build/v1.8-soft-graphic-cel/prompts/b-balanced.txt` with the exact contents of
the prompt block above, excluding the Markdown fences and including one final
newline. Run:

```bash
sha256sum build/v1.8-soft-graphic-cel/prompts/b-balanced.txt
```

Record the digest, then pass the prompt file's complete text to `image_gen`
without edits. The recorded tool-call prompt must match the prompt file
byte-for-byte.

Record B's outer request/call ID, completed generation ID, exact returned
source path, and whether a local source PNG was returned. Do not start C before
B is saved and verified.

Expected: one full-frame candidate with the approved center-strength soft
graphic cel treatment and no deliberate character or scene change.

- [ ] **Step 4: Save, verify, and inspect B**

Copy the literal returned source PNG path, without transformation, to:

```text
build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png
```

Use `cp --no-clobber`; preserve the source. Then run:

```bash
xxd -p -l 8 \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png
identify -format '%f | %m %wx%h\n' \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png
sha256sum \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png
```

Expected: valid PNG signature, one valid portrait PNG, one recorded dimension
pair, and one recorded SHA-256. Open B at original detail and record obvious
hard-gate failures without retrying it. If no local source PNG exists, search
the current-day rollout JSONL for `image_generation_call`, parse JSONL
structurally, select B's completed item whose `result` begins with `iVBOR`,
base64-decode it, verify the PNG signature before saving it to the exact B
path, and record its request or generation ID. Never copy a large payload
manually from terminal output.

- [ ] **Step 5: Reopen the ordered inputs and generate C / Graphic**

Open V17-01, B3, G2, the primary style JPEG, and the secondary style JPEG again
at original detail. Restate that V17-01 alone controls character and scene,
that B3 and G2 are human-QA-only, and that the two JPEGs control only their
approved rendering roles. Use `image_gen` with this exact ordered array. Do not
reference A or B:

```javascript
referenced_image_paths: [
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/v17-01-authority.png",
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/g6-primary-style.jpg",
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-8-soft-graphic-cel/build/v1.8-soft-graphic-cel/input/hov-secondary-style.jpg"
]
```

Use this complete prompt:

```text
Use case: full-frame identity-preserving rendering translation.
Asset: Akari v1.8 V18-01 candidate C, "Graphic".

Image 1 is the exact edit target and the SOLE authority for the character and
scene. Preserve the same Akari, age 25, identity, face, expression, hair,
ornament, body, pose, clothing, framing, apartment, and warm directional light.
Images 2 and 3 are STYLE-ONLY references. They have zero authority over
identity, age, anatomy, proportions, hair, ornament, clothing, pose, props,
camera, background, palette, or scene content.

Primary request:
Redraw the complete Image 1 at the same portrait aspect ratio and the same
full-body composition. Change only its rendering language to the strongest
allowed GRAPHIC soft-cel translation. Make contour hierarchy, grouped color
shapes, and two-to-three-step cel shadows unmistakable. Remove most painted
microtexture and simplify minor internal rendering more strongly than the
Balanced candidate, while keeping the exact face construction, eye scale, head
size, adult body proportions, quiet expression, outfit, apartment, and light.
The result must remain the exact same adult Akari in the exact same moment; it
must not become chibi, sticker-like, doll-like, youthful, or a new character.

Rendering target:
- Use a clearly readable but still thin warm-gray or warm-brown outer contour,
  with sparse low-contrast interior lines and no hard black.
- Use decisively grouped figure and room shapes with clean two-to-three-step
  cel shadows. Retain only the minimum soft transition needed for warm skin and
  coherent domestic light.
- Keep skin warm peach with restrained cheek color, one compact shadow family,
  and sparse small highlights. Do not flatten facial structure into a childlike
  mask.
- Keep hair chestnut brown, short, airy, asymmetrical, and irregular at the
  tips. Use bold large hair planes and one limited crisp accent without black
  fill, thick glossy bands, or a smooth round salon silhouette.
- Keep the cotton T-shirt and lounge shorts matte and graphic. Preserve their
  construction and drape using fewer, larger shadow shapes rather than changing
  fit or silhouette.
- Preserve the apartment geometry, floor, wall, framing, and warm light
  direction while translating them into quieter, flatter cel-rendered planes.
- Keep skin, hair, and cloth materially distinct. Never apply one plastic shine
  treatment across them.

Exact invariants from Image 1:
- Preserve the softly rounded cheeks, compact chin, nose, ears, face width,
  adult age impression, quiet closed-mouth smile, gaze, brow weight, restrained
  blush, and skin hue.
- Preserve eye size, opening, tilt, iris scale, amber color, catchlights,
  eyelids, lashes, and expression. Do not enlarge, round, darken, polish, or
  brighten the eyes to carry the stronger graphic treatment.
- Preserve the complete short chestnut bob and one character-left pale-blue
  crossed-pin ornament with its fine cord loops and two narrow tails.
- Preserve head-to-body ratio, neck, shoulders, upper-body volume, subtle
  waist, pelvis, healthy thighs and calves, limb lengths, hands, feet, neutral
  stance, and floor contact.
- Preserve the white T-shirt and pale-blue lounge shorts: same silhouette,
  neckline, sleeves, hems, waistband, drawstring, fit, and drape logic.
- Preserve camera, crop, full-body scale, placement, floor, wall, light shapes,
  shadow direction, resolution class, and aspect ratio.

Avoid:
No black hair, long hair, twin tails, side ponytail, heavy straight bangs,
school uniform, neck ribbon, scrunchies, new props, stars, geometry, cyan sticker
outline, stickers, border, text, logo, or watermark. No oversized or rounder
eyes, child face, doll face, chibi proportions, sharper V jaw, petite body,
model elongation, slimmer anime legs, stronger bust separation, pinched waist,
hip flare, pin-up pose, makeup, glamour, seduction, broad anime smile, open
mouth, or teeth. No hard black outline, plastic shine shared by
skin/hair/cloth, photoreal skin, paper texture, grain, bloom, chromatic
aberration, global smoothing, white studio background, crop, zoom, recentering,
camera shift, or global relighting.
```

Before the tool call, use `apply_patch` to create
`build/v1.8-soft-graphic-cel/prompts/c-graphic.txt` with the exact contents of
the prompt block above, excluding the Markdown fences and including one final
newline. Run:

```bash
sha256sum build/v1.8-soft-graphic-cel/prompts/c-graphic.txt
```

Record the digest, then pass the prompt file's complete text to `image_gen`
without edits. The recorded tool-call prompt must match the prompt file
byte-for-byte.

Record C's outer request/call ID, completed generation ID, exact returned
source path, and whether a local source PNG was returned.

Expected: one full-frame candidate with the strongest allowed graphic cel
treatment, without intentional deformation or scene replacement.

- [ ] **Step 6: Save, verify, and inspect C**

Copy the literal returned source PNG path, without transformation, to:

```text
build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png
```

Use `cp --no-clobber`; preserve the source. Then run:

```bash
xxd -p -l 8 \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png
identify -format '%f | %m %wx%h\n' \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png
sha256sum \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png
```

Expected: valid PNG signature, one valid portrait PNG, one recorded dimension
pair, and one recorded SHA-256. Open C at original detail and record obvious
hard-gate failures without retrying it. If no local source PNG exists, search
the current-day rollout JSONL for `image_generation_call`, parse JSONL
structurally, select C's completed item whose `result` begins with `iVBOR`,
base64-decode it, verify the PNG signature before saving it to the exact C
path, and record its request or generation ID. Never copy a large payload
manually from terminal output.

- [ ] **Step 7: Verify the complete independent candidate set**

Run:

```bash
xxd -p -l 8 \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png
xxd -p -l 8 \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png
xxd -p -l 8 \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png
identify -format '%f | %m %wx%h\n' \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png
sha256sum \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png
sha256sum \
  build/v1.8-soft-graphic-cel/prompts/a-gentle.txt \
  build/v1.8-soft-graphic-cel/prompts/b-balanced.txt \
  build/v1.8-soft-graphic-cel/prompts/c-graphic.txt
git status --short --branch
git diff --quiet
git diff --cached --quiet
```

Expected: all signatures are PNG, all candidates are readable portrait images,
all three image hashes are recorded and distinct, all three prompt hashes are
recorded, each candidate has its own generation/request IDs and returned source
path, and the tracked tree remains clean. Do not commit this task; its
deliverables are intentionally ignored.

---

### Task 3: Compare, adjudicate, and stop for explicit selection

**Files:**

- Read:
  `build/v1.8-soft-graphic-cel/input/v17-01-authority.png`
- Read:
  `build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png`
- Read:
  `build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png`
- Read:
  `build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png`
- Create:
  `build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-comparison.png`
- Create:
  `build/v1.8-soft-graphic-cel/review.md`

**Interfaces:**

- Consumes: the exact baseline plus three verified independent candidates and
  their provenance records.
- Produces: one labeled equal-scale comparison, one seven-gate review with
  eligibility and ranking, and one explicit user choice or rejection; no
  promotion and no tracked change.

- [ ] **Step 1: Build and verify the equal-scale comparison**

Run:

```bash
magick montage \
  -background '#f4f1ec' \
  -fill '#302b29' \
  -stroke none \
  -font DejaVu-Sans \
  -pointsize 34 \
  -label 'BASE / V17-01' \
  build/v1.8-soft-graphic-cel/input/v17-01-authority.png \
  -label 'A / Gentle' \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png \
  -label 'B / Balanced' \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png \
  -label 'C / Graphic' \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png \
  -tile 2x2 \
  -geometry 512x768+24+56 \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-comparison.png
xxd -p -l 8 \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-comparison.png
identify -format '%f | %m %wx%h\n' \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-comparison.png
sha256sum \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-comparison.png
```

Expected: one valid labeled 2x2 PNG with equal-size baseline, A, B, and C
panels, PNG signature `89504e470d0a1a0a`, readable labels, and one recorded
SHA-256.

- [ ] **Step 2: Inspect every candidate and the comparison at original detail**

Use `view_image` with original detail, serially, for baseline, A, B, C, and the
comparison. Review each candidate in this exact order:

1. same-person identity and adult age-25 impression;
2. face, amber eyes, short chestnut bob, and complete hair ornament;
3. body balance, fixed pose, hands, feet, and connected anatomy;
4. immediate readability of its intended Gentle, Balanced, or Graphic strength;
5. distinct warm skin, chestnut hair, and matte-cloth materials;
6. apartment, framing, and warm-light continuity;
7. finished image quality and absence of generation artifacts.

Use `apply_patch` to create
`build/v1.8-soft-graphic-cel/review.md` with actual PASS or FAIL results for
every gate. For each candidate, include its image hash, prompt hash, dimensions,
generation/request IDs, returned source path, eligible or ineligible verdict,
observed Minor differences, and concise rationale. Any violation of the locked
character or scene design makes that candidate ineligible.

Expected: the local review separates hard-gate eligibility from quality ranking
and does not waive a failed locked attribute.

- [ ] **Step 3: Run one independent artifact review**

Dispatch one read-only reviewer with the approved design, baseline, A/B/C, and
comparison. Ask it to return:

- PASS or FAIL for each of the same seven gates per candidate;
- every hard-gate failure with concrete visual evidence;
- known Minor differences for passing candidates;
- quality ranking among hard-gate passes only;
- whether at least one candidate is safe to show as eligible for user selection.

Reconcile disagreements by reopening only the affected image at original
detail. Any unresolved hard-gate disagreement makes that candidate ineligible.
Do not generate a repair or break a tie with a new candidate.

Expected: one eligibility set and one ranked list of passing candidates, with
all disagreements resolved or clearly disclosed to the user.

- [ ] **Step 4: Prove the final local-only boundary**

Run:

```bash
git status --short --branch
git diff --quiet
git diff --cached --quiet
git check-ignore -v \
  build/v1.8-soft-graphic-cel/input/v17-01-authority.png \
  build/v1.8-soft-graphic-cel/prompts/a-gentle.txt \
  build/v1.8-soft-graphic-cel/prompts/b-balanced.txt \
  build/v1.8-soft-graphic-cel/prompts/c-graphic.txt \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-a-gentle.png \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-b-balanced.png \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-c-graphic.png \
  build/v1.8-soft-graphic-cel/akari-v1.8-v18-01-soft-cel-comparison.png \
  build/v1.8-soft-graphic-cel/review.md
```

Expected: tracked and staged diffs are empty and every V18-01 working artifact
is ignored. Do not commit generated or review material. A later, separately
reviewed promotion plan owns any accepted v1.8 PNG and tracked package files.

- [ ] **Step 5: Present the comparison and stop at the user selection gate**

Show the comparison and each passing candidate in the Codex app using absolute
image paths. Lead with:

- which candidates passed every hard gate;
- which candidates failed and why;
- the quality ranking among passes;
- a brief description of A/B/C's actual visible rendering difference;
- a recommendation based on same-person continuity, preserved fixed expression,
  character appeal, and finished image quality.

If no candidate passes, report that the set has no eligible selection and stop
at the required return-to-design decision without calling
`request_user_input`. If one or two candidates pass, use `request_user_input`
with only those passing candidates plus `どれも選ばない`. If all three pass,
offer A, B, and C and state that the tool's free-form choice can be used for
`どれも選ばない`.

After the response, record only the explicit selection or explicit rejection
in the conversation. Stop. Do not promote, correct, regenerate, composite, or
create `akari-v1.8/` in this plan.

Expected: the user makes one explicit choice or rejects the set, and no work
crosses the promotion boundary.

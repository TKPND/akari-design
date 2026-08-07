# Akari v2.2 Character-Sheet Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, preserve, and review twelve landscape Akari v2.2
character-sheet candidates, each containing four coordinated depictions made
by Imagegen from one fixed identity contract.

**Architecture:** Treat the supplied close portrait as the primary identity
anchor and the supplied full-body image as outfit-and-proportion support only.
Persist one master prompt, run twelve independent built-in Imagegen calls in
three reviewable groups of four, and copy each returned PNG byte-for-byte into
an ignored run directory. No script or compositor decides the layout inside a
sheet.

**Tech Stack:** built-in `image_gen`, `view_image`, ImageMagick, `sha256sum`,
`xxd`, `cmp`, Git scope checks.

## Global Constraints

- Implement `docs/superpowers/specs/2026-08-07-akari-v2-2-character-sheet-batch-design.md`.
- Generate exactly twelve independent candidates using exactly the same two
  references in the same order and exactly the same master prompt.
- Every candidate is a wide landscape image containing exactly four matching
  depictions: two face-scale views and two full-body views.
- Image 1 controls face, eyes, apparent age, hair, single hairpin, tie, palette,
  and rendering; Image 2 supplies body balance and outfit only.
- Do not transfer Image 2's crossed hairpins or different face construction.
- Do not use one generated candidate as a reference for another candidate.
- Let Imagegen choose placement, scale, whitespace, overlap, and hierarchy; do
  not create a grid, collage, contact sheet, or layout with code.
- Store every input, prompt, output, hash, identifier, and review note under
  ignored `tmp/akari-v2.2-character-sheet/r01/`.
- Do not overwrite, retry, repair, promote, stage, or commit generated review
  material.
- The twelve authorized calls remain the complete selection set even when a
  call fails or an image looks weak; do not silently replace it with a
  thirteenth call.
- Per the user's execution override, do not assign automated or agent visual
  audit results, PASS/FAIL labels, scores, rankings, or a winner. Verify only
  that each returned PNG was preserved correctly, then present all outcomes
  for direct human selection.

---

### Task 1: Freeze Inputs and the Master Prompt

**Files:**

- Create: `tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg`
- Create: `tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg`
- Create: `tmp/akari-v2.2-character-sheet/r01/prompts/master.txt`
- Create: `tmp/akari-v2.2-character-sheet/r01/run.md`
- Verify: `docs/superpowers/specs/2026-08-07-akari-v2-2-character-sheet-batch-design.md`

**Interfaces:**

- Consumes: the two approved attachment paths and the approved generation
  contract.
- Produces: immutable local reference copies, one exact prompt consumed by all
  twelve calls, twelve absent output paths, and a run-record schema.

- [ ] **Step 1: Verify source bytes and dimensions**

Run:

```bash
sha256sum \
  /home/takahiro/.codex/attachments/7d6f1a9a-c761-49e5-971c-cc0902df456a/1239849770.jpeg \
  /home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg
identify -format '%f %m %wx%h %[colorspace]\n' \
  /home/takahiro/.codex/attachments/7d6f1a9a-c761-49e5-971c-cc0902df456a/1239849770.jpeg \
  /home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg
```

Expected:

- `1239849770.jpeg` is JPEG `944x1672` with SHA-256
  `142a765b8bf4c549ea22c3ea357d5d2b45eca4b417041f3907272fe3efcad1b1`;
- `1844477702.jpeg` is JPEG `944x1672` with SHA-256
  `cb6a659ec374f0c113fec58f989cb351130c950d2312892d1de4f7245e97c605`.

- [ ] **Step 2: Establish the ignored, non-overwriting workspace**

Run:

```bash
mkdir -p tmp/akari-v2.2-character-sheet/r01/inputs
mkdir -p tmp/akari-v2.2-character-sheet/r01/prompts
mkdir -p tmp/akari-v2.2-character-sheet/r01/outputs
git check-ignore -q tmp/akari-v2.2-character-sheet/r01/
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-01.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-02.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-03.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-04.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-05.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-06.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-07.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-08.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-09.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-10.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-11.png
test ! -e tmp/akari-v2.2-character-sheet/r01/outputs/candidate-12.png
```

Expected: every command exits `0`; the run directory is ignored and all twelve
output paths are absent.

- [ ] **Step 3: Copy both references without changing bytes**

Run:

```bash
cp --no-clobber \
  /home/takahiro/.codex/attachments/7d6f1a9a-c761-49e5-971c-cc0902df456a/1239849770.jpeg \
  tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg
cp --no-clobber \
  /home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg \
  tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg
cmp --silent \
  /home/takahiro/.codex/attachments/7d6f1a9a-c761-49e5-971c-cc0902df456a/1239849770.jpeg \
  tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg
cmp --silent \
  /home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg \
  tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg
```

Expected: both `cmp` commands exit `0`.

- [ ] **Step 4: Persist the exact master prompt**

Use `apply_patch` to create
`tmp/akari-v2.2-character-sheet/r01/prompts/master.txt` with exactly:

```text
Use case: stylized-concept
Asset type: wide landscape Akari v2.2 anime character reference sheet for visual selection
Input images: Image 1 is the primary identity anchor and controls the face, exact eye construction, apparent age, hair design, single blue hairpin, blue ponytail tie, chestnut palette, and polished anime rendering. Image 2 is supporting reference only for body balance and the white T-shirt, navy utility shorts, white socks, and blue-and-white sneakers; do not copy Image 2's face or crossed hairpins.
Primary request: Generate one complete wide landscape character sheet containing exactly four clearly matching depictions of the same twenty-five-year-old Akari: one face-scale near-front view with a calm softly friendly expression; one face-scale three-quarter view with the warm open smile from Image 1; one natural front-oriented full-body standing view; and one relaxed three-quarter full-body view with light believable movement. All four must be unmistakably the same person in the same outfit and character design.
Layout freedom: Design an elegant organic reference-sheet composition yourself. You may choose placement, relative scale, whitespace, gentle overlap, and visual flow. Keep the canvas unmistakably wider than tall and keep all essential facial and full-body features readable. Do not use a rigid grid, mechanical collage, fixed panel template, or fixed left-to-right order.
Eye identity lock: Copy Image 1's warm brown eye shape and mature-cute adult impression. Keep coordinated gaze, matching iris scale, clean pupils, consistent eye spacing, the same gentle upper-lid weight, fine lashes, and coherent catchlights in every depiction. The eyes must remain clear and attractive at face scale without becoming childlike or doll-like.
Hair identity lock: Preserve Image 1's chestnut asymmetrical bob, longer hair gathered into one low side ponytail on character-left, blue tie, warm highlights, soft flyaways, and exactly one straight slender filled blue capsule hairpin above the character-left temple. Never introduce crossed, doubled, forked, or ghost hairpins.
Outfit: Loose plain white T-shirt, dark navy utility shorts with one pocket, white socks, and blue-and-white sneakers in both full-body depictions.
Style/medium: Polished high-quality anime character illustration matching Image 1's linework, soft cel shading, warm color balance, facial appeal, and finished quality. Clean white to softly warm off-white reference-sheet background.
Constraints: exactly four depictions and no fifth figure; same face, age, eyes, hair, hairpin, outfit, body balance, palette, and finish throughout; plausible hands, feet, limbs, joints, necks, and proportions; overlapping layout elements must not merge anatomy or share limbs; no essential feature cropped away; no title, label, caption, measurement, pseudo-text, logo, watermark, border, or scenery.
Avoid: crossed gaze; mismatched iris sizes; duplicate pupils or irises; fused lashes; wandering highlights; oversized eyes; different faces or ages; crossed or multiple hairpins; extra fingers or limbs; merged bodies; broken joints; truncated hands, feet, hair, or shoes; outfit drift; chibi proportions; sexualized styling; photorealism; 3D rendering; rough sketch finish.
```

- [ ] **Step 5: Create the run record**

Use `apply_patch` to create `tmp/akari-v2.2-character-sheet/r01/run.md`
with the run title, both source attachment paths and roles, both verified hashes,
the exact master-prompt path, and an initially empty candidate table with these
columns: candidate, built-in source path, generation or request identifier,
saved path, dimensions, and SHA-256.

- [ ] **Step 6: Open and label both reference roles**

Open both copied JPEGs with `view_image` at original detail. State that
`identity-anchor.jpeg` is Image 1 and the controlling identity reference, while
`fullbody-support.jpeg` is Image 2 and controls only body balance and outfit.
Do not call image generation until both are visible in the active conversation.

No commit: every Task 1 deliverable is intentionally ignored review material.

### Task 2: Generate and Preserve Candidates 01-04

**Files:**

- Read: `tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg`
- Read: `tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg`
- Read: `tmp/akari-v2.2-character-sheet/r01/prompts/master.txt`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-01.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-02.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-03.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-04.png`
- Modify: `tmp/akari-v2.2-character-sheet/r01/run.md`

**Interfaces:**

- Consumes: the frozen reference pair and exact master prompt from Task 1.
- Produces: four independent byte-preserved PNG candidates and four complete
  run-record rows for final review.

- [ ] **Step 1: Run four independent built-in Imagegen calls**

Call built-in `image_gen` once for each candidate, always with this exact
`referenced_image_paths` order:

1. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg`;
2. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg`.

Use the exact contents of
`tmp/akari-v2.2-character-sheet/r01/prompts/master.txt` as every call's prompt.
Do not include earlier generated outputs. A call failure is recorded as the
result for its assigned candidate number and is not retried.

- [ ] **Step 2: Copy each returned source PNG into its fixed path**

For each successful call, use the absolute source PNG path returned by the
built-in tool as the source of `cp --no-clobber`. Copy in call order to
`candidate-01.png`, `candidate-02.png`, `candidate-03.png`, and
`candidate-04.png`. Do not infer a path or use a destination argument on the
image-generation call.

- [ ] **Step 3: Verify bytes and metadata for candidates 01-04**

For each successful candidate, run `cmp --silent` against its built-in source
path, then run:

```bash
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-01.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-02.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-03.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-04.png
identify -format '%f %m %wx%h %[colorspace]\n' \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-01.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-02.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-03.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-04.png
sha256sum tmp/akari-v2.2-character-sheet/r01/outputs/candidate-0{1,2,3,4}.png
```

Expected: every successful file begins `89504e470d0a1a0a`, is PNG with width
greater than height, and has a recorded SHA-256.

- [ ] **Step 4: Open and record candidates 01-04**

Open each saved PNG with `view_image` for later presentation. Record the actual
source path, returned identifier, saved path, dimensions, and hash in `run.md`.
Do not assign a quality verdict, score, or rank, and do not repair or replace a
candidate.

No commit: the four candidates and run updates are intentionally ignored.

### Task 3: Generate and Preserve Candidates 05-08

**Files:**

- Read: `tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg`
- Read: `tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg`
- Read: `tmp/akari-v2.2-character-sheet/r01/prompts/master.txt`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-05.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-06.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-07.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-08.png`
- Modify: `tmp/akari-v2.2-character-sheet/r01/run.md`

**Interfaces:**

- Consumes: the same frozen reference pair and exact master prompt from Task 1.
- Produces: four additional independent byte-preserved PNG candidates and four
  complete run-record rows.

- [ ] **Step 1: Run four independent built-in Imagegen calls**

Call built-in `image_gen` once for each candidate, always with this exact
`referenced_image_paths` order:

1. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg`;
2. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg`.

Use the exact contents of
`tmp/akari-v2.2-character-sheet/r01/prompts/master.txt` as every call's prompt.
Do not include earlier generated outputs. Assign the four outcomes in call
order to candidate numbers 05, 06, 07, and 08. A call failure is recorded for
its assigned number and is not retried.

- [ ] **Step 2: Copy each returned source PNG into its fixed path**

For each successful call, use `cp --no-clobber` from the exact built-in source
path to `candidate-05.png`, `candidate-06.png`, `candidate-07.png`, or
`candidate-08.png` according to call order.

- [ ] **Step 3: Verify bytes and metadata for candidates 05-08**

Run `cmp --silent` against every successful built-in source path, then run:

```bash
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-05.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-06.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-07.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-08.png
identify -format '%f %m %wx%h %[colorspace]\n' \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-05.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-06.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-07.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-08.png
sha256sum tmp/akari-v2.2-character-sheet/r01/outputs/candidate-0{5,6,7,8}.png
```

Expected: every successful file begins `89504e470d0a1a0a`, is PNG with width
greater than height, and has a recorded SHA-256.

- [ ] **Step 4: Open and record candidates 05-08**

Open each saved PNG for later presentation and add its actual metadata to
`run.md`. Do not assign a quality verdict, score, or rank. Keep failures
unchanged.

No commit: the four candidates and run updates are intentionally ignored.

### Task 4: Generate and Preserve Candidates 09-12

**Files:**

- Read: `tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg`
- Read: `tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg`
- Read: `tmp/akari-v2.2-character-sheet/r01/prompts/master.txt`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-09.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-10.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-11.png`
- Create: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-12.png`
- Modify: `tmp/akari-v2.2-character-sheet/r01/run.md`

**Interfaces:**

- Consumes: the same frozen reference pair and exact master prompt from Task 1.
- Produces: the final four independent byte-preserved PNG candidates and four
  complete run-record rows.

- [ ] **Step 1: Run four independent built-in Imagegen calls**

Call built-in `image_gen` once for each candidate, always with this exact
`referenced_image_paths` order:

1. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-character-sheet/r01/inputs/identity-anchor.jpeg`;
2. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-character-sheet/r01/inputs/fullbody-support.jpeg`.

Use the exact contents of
`tmp/akari-v2.2-character-sheet/r01/prompts/master.txt` as every call's prompt.
Do not include earlier generated outputs. Assign the four outcomes in call
order to candidate numbers 09, 10, 11, and 12. A call failure is recorded for
its assigned number and is not retried.

- [ ] **Step 2: Copy each returned source PNG into its fixed path**

For each successful call, use `cp --no-clobber` from the exact built-in source
path to `candidate-09.png`, `candidate-10.png`, `candidate-11.png`, or
`candidate-12.png` according to call order.

- [ ] **Step 3: Verify bytes and metadata for candidates 09-12**

Run `cmp --silent` against every successful built-in source path, then run:

```bash
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-09.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-10.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-11.png
xxd -p -l 8 tmp/akari-v2.2-character-sheet/r01/outputs/candidate-12.png
identify -format '%f %m %wx%h %[colorspace]\n' \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-09.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-10.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-11.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-12.png
sha256sum \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-09.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-10.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-11.png \
  tmp/akari-v2.2-character-sheet/r01/outputs/candidate-12.png
```

Expected: every successful file begins `89504e470d0a1a0a`, is PNG with width
greater than height, and has a recorded SHA-256.

- [ ] **Step 4: Open and record candidates 09-12**

Open each saved PNG for later presentation and add its actual metadata to
`run.md`. Do not assign a quality verdict, score, or rank. Keep failures
unchanged.

No commit: the four candidates and run updates are intentionally ignored.

### Task 5: Present the Complete Selection Set

**Files:**

- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-01.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-02.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-03.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-04.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-05.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-06.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-07.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-08.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-09.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-10.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-11.png`
- Read: `tmp/akari-v2.2-character-sheet/r01/outputs/candidate-12.png`
- Modify: `tmp/akari-v2.2-character-sheet/r01/run.md`

**Interfaces:**

- Consumes: all twelve generation outcomes and their per-candidate reviews.
- Produces: a complete unranked set for the user's visual decision, plus proof
  that no canonical image changed.

- [ ] **Step 1: Verify the complete output inventory**

Run:

```bash
find tmp/akari-v2.2-character-sheet/r01/outputs \
  -maxdepth 1 -type f -name 'candidate-*.png' -printf '%f\n' | sort
```

Expected: one filename for every successful authorized call, with no filename
outside `candidate-01.png` through `candidate-12.png`. Any failed call must be
listed explicitly in `run.md` instead of being regenerated.

- [ ] **Step 2: Prepare the unranked human-selection list**

Read all twelve rows and add a numeric presentation list to `run.md` in
candidate order. Do not add visual judgments, scores, rankings, a winner, or a
promotion recommendation.

- [ ] **Step 3: Confirm bounded Git scope**

Run:

```bash
git status --short --branch
git diff --name-only
git diff --cached --name-only
git check-ignore -v tmp/akari-v2.2-character-sheet/r01/
```

Expected: the run directory is ignored; no canonical image is changed; no
generated file is staged. Preserve the pre-existing untracked
`docs/superpowers/plans/2026-08-04-akari-v2-0-uniform-batch.md` unchanged.

- [ ] **Step 4: Present all candidates for user selection**

Render each successful saved PNG in candidate-number order. Include the
complete set without review labels and make no selection, correction,
promotion, PDF, or manifest change without the user's next decision.

No commit: final outputs and review notes remain ignored selection material.

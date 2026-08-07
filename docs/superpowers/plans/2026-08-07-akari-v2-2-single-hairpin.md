# Akari v2.2 Single-Hairpin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce one non-destructive single-hairpin edit of each supplied
Akari v2.2 candidate and review both against the approved seven-gate contract.

**Architecture:** Treat the full-figure and close-portrait JPEGs as independent
edit targets. Run one built-in image edit per target with the other v2.2 image
as a supporting cross-scale reference, persist each returned PNG byte-for-byte
under an ignored working directory, then review original detail and one
equal-scale comparison. No canonical or tracked image changes during execution.

**Tech Stack:** built-in `image_gen`, `view_image`, ImageMagick,
`sha256sum`, `xxd`, `cmp`, Git scope checks.

## Global Constraints

- Implement the approved design in
  `docs/superpowers/specs/2026-08-07-akari-v2-2-single-hairpin-design.md`.
- Use exactly one straight, slender, filled capsule-shaped hairpin.
- Place it on character-left/canvas-right above the temple, rising about 35
  degrees from face-front/lower toward crown-back/upper.
- Use a matte, muted medium blue. Exactly one quiet dark edge is permitted only
  when needed for legibility; heavy black border, doubled outline, separate
  line, or internal construction line remain forbidden.
- Change only the hairpin; preserve identity, age, face, hair silhouette,
  expression, pose, crop, body, outfit, palette, and rendering finish.
- Keep full-figure and portrait generation calls independent.
- Store every input copy, prompt, output, comparison, and record under ignored
  `tmp/akari-v2.2-single-hairpin/r01/`.
- Do not overwrite a file, retry a failed edit, composite a repair, promote an
  output, or modify a canonical asset without a new user decision.
- Do not stage or commit generated images or working records.

---

### Task 1: Preflight and Preserve Inputs

**Files:**

- Create: `tmp/akari-v2.2-single-hairpin/r01/inputs/fullbody.jpeg`
- Create: `tmp/akari-v2.2-single-hairpin/r01/inputs/portrait.jpeg`
- Create: `tmp/akari-v2.2-single-hairpin/r01/prompts/fullbody.txt`
- Create: `tmp/akari-v2.2-single-hairpin/r01/prompts/portrait.txt`
- Verify: `docs/superpowers/specs/2026-08-07-akari-v2-2-single-hairpin-design.md`

**Interfaces:**

- Consumes: the two user attachment paths and their approved SHA-256 values.
- Produces: immutable local edit inputs and the exact prompts consumed by Tasks
  2 and 3.

- [ ] **Step 1: Verify source bytes and dimensions**

Run:

```bash
sha256sum \
  /home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg \
  /home/takahiro/.codex/attachments/12b80512-5531-4d4d-97e9-111f5121b087/517254027.jpeg
identify -format '%f %m %wx%h %[colorspace]\n' \
  /home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg \
  /home/takahiro/.codex/attachments/12b80512-5531-4d4d-97e9-111f5121b087/517254027.jpeg
```

Expected:

- `1844477702.jpeg` SHA-256
  `cb6a659ec374f0c113fec58f989cb351130c950d2312892d1de4f7245e97c605`;
- `517254027.jpeg` SHA-256
  `3756e53b3a0a912e61f22a5ce7f339667c7146d3591d0fa54074ef3c585d7a29`;
- both inputs are `JPEG 944x1672 sRGB`.

- [ ] **Step 2: Establish the ignored, non-overwriting workspace**

Run:

```bash
mkdir -p tmp/akari-v2.2-single-hairpin/r01/inputs
mkdir -p tmp/akari-v2.2-single-hairpin/r01/prompts
mkdir -p tmp/akari-v2.2-single-hairpin/r01/outputs
test ! -e tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-fullbody-r01.png
test ! -e tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-portrait-r01.png
git check-ignore -q tmp/akari-v2.2-single-hairpin/r01/
```

Expected: every command exits `0`; both output paths are absent and the working
directory is ignored by Git.

- [ ] **Step 3: Copy the source inputs without changing bytes**

Run:

```bash
cp --no-clobber \
  /home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg \
  tmp/akari-v2.2-single-hairpin/r01/inputs/fullbody.jpeg
cp --no-clobber \
  /home/takahiro/.codex/attachments/12b80512-5531-4d4d-97e9-111f5121b087/517254027.jpeg \
  tmp/akari-v2.2-single-hairpin/r01/inputs/portrait.jpeg
cmp --silent \
  /home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg \
  tmp/akari-v2.2-single-hairpin/r01/inputs/fullbody.jpeg
cmp --silent \
  /home/takahiro/.codex/attachments/12b80512-5531-4d4d-97e9-111f5121b087/517254027.jpeg \
  tmp/akari-v2.2-single-hairpin/r01/inputs/portrait.jpeg
```

Expected: both `cmp` commands exit `0`.

- [ ] **Step 4: Persist the exact full-figure prompt**

Use `apply_patch` to create
`tmp/akari-v2.2-single-hairpin/r01/prompts/fullbody.txt` with exactly:

```text
Use case: precise-object-edit
Asset type: Akari v2.2 full-figure character-design review candidate
Input images: Image 1 is the sole edit target and controls every existing visual decision; Image 2 is a supporting cross-scale identity and hair-continuity reference only and must not replace Image 1's composition, face, body, pose, outfit, or rendering.
Primary request: In Image 1, replace only the crossed blue hairpin above the character-left temple, visible on canvas-right, with exactly one straight slender filled capsule-shaped hairpin. Remove every remnant of the old crossed-pin construction.
Hairpin construction: one continuous solid piece with softly rounded ends; no opening or internal line; length approximately 0.8 of the visible eye width; narrow but thick enough to remain one filled shape at full-figure scale; anchored on the outer hair mass above the character-left temple; rising approximately 35 degrees from face-front/lower toward crown-back/upper along the local hair plane; matte muted medium blue coordinated with the existing blue accents; no black outline and no glossy stripe.
Composition/framing: preserve Image 1's exact full-figure composition, camera, crop, pose, hand gesture, margins, and white background.
Style/medium: preserve Image 1's exact polished anime illustration style, linework, cel shading, color balance, and finish.
Constraints: change only the hairpin; preserve the same person, apparent age, face, eyes, gaze, brows, cheeks, nose, mouth, smile, expression, bangs, hairline, side ponytail, ponytail tie, flyaways, highlights, chestnut hair palette, hair volume, anatomy, proportions, white T-shirt, navy shorts, utility pocket, socks, shoes, and background; do not beautify, polish, repair, redraw, recolor, or restyle any other region; no text, logo, watermark, border, or seam.
Avoid: a second pin; crossed or X-shaped pins; parallel double pins; U-shaped bobby pin; fork; loop; gap; hinge; tooth; bow; ribbon; bead; flower; symbol; decorative tail; ghost lines from the old ornament; extra accessories; any change outside the hairpin.
```

- [ ] **Step 5: Persist the exact portrait prompt**

Use `apply_patch` to create
`tmp/akari-v2.2-single-hairpin/r01/prompts/portrait.txt` with exactly:

```text
Use case: precise-object-edit
Asset type: Akari v2.2 close-portrait character-design review candidate
Input images: Image 1 is the sole edit target and controls every existing visual decision; Image 2 is a supporting cross-scale identity and hair-continuity reference only and must not replace Image 1's composition, face, pose, outfit, or rendering.
Primary request: In Image 1, replace only the crossed blue hairpin above the character-left temple, visible on canvas-right, with exactly one straight slender filled capsule-shaped hairpin. Remove every remnant of the old crossed-pin construction.
Hairpin construction: one continuous solid piece with softly rounded ends; no opening; length approximately 0.8 of the visible eye width; narrow but unmistakably one filled shape at close-portrait scale; anchored on the outer hair mass above the character-left temple; rising approximately 35 degrees from face-front/lower toward crown-back/upper along the local hair plane; matte muted medium blue coordinated with the existing blue accents; exactly one quiet dark edge is permitted only when needed for legibility; heavy black border, doubled outline, separate line, or internal construction line remain forbidden; no glossy stripe.
Composition/framing: preserve Image 1's exact close-portrait composition, camera, crop, head angle, hand gesture, and white background.
Style/medium: preserve Image 1's exact polished anime illustration style, linework, cel shading, color balance, and finish.
Constraints: change only the hairpin; preserve the same person, apparent age, face, eyes, gaze, brows, cheeks, nose, mouth, smile, expression, bangs, hairline, side ponytail, ponytail tie, flyaways, highlights, chestnut hair palette, hair volume, ear, jaw-to-neck connection, visible anatomy, white T-shirt, and background; do not beautify, polish, repair, redraw, recolor, or restyle any other region; no text, logo, watermark, border, or seam.
Avoid: a second pin; crossed or X-shaped pins; parallel double pins; U-shaped bobby pin; fork; loop; gap; hinge; tooth; bow; ribbon; bead; flower; symbol; decorative tail; ghost lines from the old ornament; extra accessories; any change outside the hairpin.
```

- [ ] **Step 6: Open and label both reference roles**

Open both copied inputs with `view_image` at original detail. For the first
edit, state that `fullbody.jpeg` is Image 1 and the edit target while
`portrait.jpeg` is Image 2 and a supporting cross-scale reference only. Do not
call image generation until both are visible in the active conversation.

No commit: every Task 1 deliverable is intentionally ignored review material.

### Task 2: Edit and Verify the Full-Figure Candidate

**Files:**

- Read: `tmp/akari-v2.2-single-hairpin/r01/inputs/fullbody.jpeg`
- Read: `tmp/akari-v2.2-single-hairpin/r01/inputs/portrait.jpeg`
- Read: `tmp/akari-v2.2-single-hairpin/r01/prompts/fullbody.txt`
- Create: `tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-fullbody-r01.png`
- Update: `tmp/akari-v2.2-single-hairpin/r01/run.md`

**Interfaces:**

- Consumes: Image 1 full-figure edit target, Image 2 supporting portrait, and
  the exact Task 1 full-figure prompt.
- Produces: one byte-preserved PNG candidate plus its actual built-in generation
  identifiers and verification evidence.

- [ ] **Step 1: Run exactly one built-in full-figure edit**

Call built-in `image_gen` with:

- `referenced_image_paths` in this exact order:
  1. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-single-hairpin/r01/inputs/fullbody.jpeg`;
  2. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-single-hairpin/r01/inputs/portrait.jpeg`.
- `prompt`: the exact contents of
  `tmp/akari-v2.2-single-hairpin/r01/prompts/fullbody.txt`.
- no `num_last_images_to_include` argument.

Use the built-in tool result's actual generated source path and generation
identifier. Do not invoke a second call if the result is weak or malformed.

- [ ] **Step 2: Copy the generated PNG without overwriting**

Run `cp --no-clobber` from the exact returned built-in generated source path to:

```text
tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-fullbody-r01.png
```

Then run `cmp --silent` between the generated source and copied output.
Expected: `cmp` exits `0`.

- [ ] **Step 3: Record and verify full-figure provenance**

Use `apply_patch` to create or extend
`tmp/akari-v2.2-single-hairpin/r01/run.md` with the actual prompt path,
ordered reference paths and roles, outer request ID if returned, completed
generation ID, generated source path, copied output path, dimensions, PNG
signature, SHA-256, byte-identity result, and generation timestamp.

Run:

```bash
identify -format '%f %m %wx%h %[colorspace]\n' \
  tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-fullbody-r01.png
xxd -p -l 8 \
  tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-fullbody-r01.png
sha256sum \
  tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-fullbody-r01.png
```

Expected: format `PNG`, signature `89504e470d0a1a0a`, and a recorded nonempty
SHA-256.

- [ ] **Step 4: Review full-figure output at original detail**

Open the copied output with `view_image` at original detail. Record pass or
fail for all seven approved review gates in `run.md`. Reject the output if the
pin is not exactly one filled capsule, if any old pin remnant remains, or if
any face, hair, hand, body, clothing, shoe, crop, or rendering drift is visible.

No commit: the candidate and record remain ignored review material.

### Post-Task 2 User Ruling (2026-08-07)

Task 2's full-figure candidate was originally reviewed as `REJECT` under the
historical fullbody prompt's stricter `no black outline` wording. After the
user explicitly ruled `Minorとして許容`, its unchanged PNG is adjudicated `PASS`
under the revised contract: one quiet dark edge is permitted only when needed
for legibility, while heavy black borders, doubled outlines, separate lines,
and internal construction lines remain forbidden. The quiet dark edge and the
`2x3`-pixel dimension delta (`942x1669` vs `944x1672`) are recorded as Minor;
original-detail review found no material visual drift. The historical
fullbody prompt, Task 2 call, source, copied PNG, hash, and byte record remain
immutable provenance and are not rewritten. This ruling does not authorize a
retry, retouch, composite, or pixel change.

### Task 3: Edit and Verify the Close-Portrait Candidate

**Files:**

- Read: `tmp/akari-v2.2-single-hairpin/r01/inputs/portrait.jpeg`
- Read: `tmp/akari-v2.2-single-hairpin/r01/inputs/fullbody.jpeg`
- Read: `tmp/akari-v2.2-single-hairpin/r01/prompts/portrait.txt`
- Create: `tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-portrait-r01.png`
- Update: `tmp/akari-v2.2-single-hairpin/r01/run.md`

**Interfaces:**

- Consumes: Image 1 portrait edit target, Image 2 supporting full figure, and
  the exact Task 1 portrait prompt.
- Produces: one byte-preserved PNG candidate plus its actual built-in generation
  identifiers and verification evidence.

- [ ] **Step 1: Reopen and label references in portrait-first order**

Open `portrait.jpeg` and then `fullbody.jpeg` with `view_image` at original
detail. State that the portrait is Image 1 and the sole edit target while the
full figure is Image 2 and a supporting cross-scale reference only.

- [ ] **Step 2: Run exactly one built-in portrait edit**

Call built-in `image_gen` with:

- `referenced_image_paths` in this exact order:
  1. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-single-hairpin/r01/inputs/portrait.jpeg`;
  2. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-single-hairpin/r01/inputs/fullbody.jpeg`.
- `prompt`: the exact contents of
  `tmp/akari-v2.2-single-hairpin/r01/prompts/portrait.txt`.
- no `num_last_images_to_include` argument.

Use the built-in tool result's actual generated source path and generation
identifier. Do not invoke a second call if the result is weak or malformed.

- [ ] **Step 3: Copy the generated PNG without overwriting**

Run `cp --no-clobber` from the exact returned built-in generated source path to:

```text
tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-portrait-r01.png
```

Then run `cmp --silent` between the generated source and copied output.
Expected: `cmp` exits `0`.

- [ ] **Step 4: Record and verify portrait provenance**

Extend `tmp/akari-v2.2-single-hairpin/r01/run.md` with the actual prompt path,
ordered reference paths and roles, outer request ID if returned, completed
generation ID, generated source path, copied output path, dimensions, PNG
signature, SHA-256, byte-identity result, and generation timestamp.

Run:

```bash
identify -format '%f %m %wx%h %[colorspace]\n' \
  tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-portrait-r01.png
xxd -p -l 8 \
  tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-portrait-r01.png
sha256sum \
  tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-portrait-r01.png
```

Expected: format `PNG`, signature `89504e470d0a1a0a`, and a recorded nonempty
SHA-256.

- [ ] **Step 5: Review portrait output at original detail**

Open the copied output with `view_image` at original detail. Record pass or
fail for all seven approved review gates in `run.md`. Reject the output if the
pin is not exactly one filled capsule, if any old pin remnant remains, or if
any face, hair, ear, jaw-to-neck, hand, T-shirt, crop, or rendering drift is
visible.

No commit: the candidate and record remain ignored review material.

### Task 4: Compare, Adjudicate, and Present

**Files:**

- Read: both original input copies.
- Read: both generated output candidates.
- Create: `tmp/akari-v2.2-single-hairpin/r01/comparison.png`
- Update: `tmp/akari-v2.2-single-hairpin/r01/run.md`

**Interfaces:**

- Consumes: Task 2 and Task 3 outputs and seven-gate reviews.
- Produces: one equal-scale comparison, final per-output verdicts, and a user
  review handoff without promotion.

- [ ] **Step 1: Build an equal-scale two-by-two comparison**

Run:

```bash
montage \
  -background '#f5f2ec' -fill '#222222' -pointsize 18 -label '%f' \
  tmp/akari-v2.2-single-hairpin/r01/inputs/fullbody.jpeg \
  tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-fullbody-r01.png \
  tmp/akari-v2.2-single-hairpin/r01/inputs/portrait.jpeg \
  tmp/akari-v2.2-single-hairpin/r01/outputs/akari-v2.2-single-hairpin-portrait-r01.png \
  -tile 2x2 -geometry '472x836+16+32>' \
  tmp/akari-v2.2-single-hairpin/r01/comparison.png
```

Expected: one readable 2-by-2 comparison containing each original followed by
its single-pin edit at equal maximum cell size.

- [ ] **Step 2: Inspect the equal-scale comparison**

Open `comparison.png` with `view_image` at original detail. Confirm the pin
reads as the same design at portrait and full-figure scale and that comparison
layout does not hide cropping, pose, or proportion drift.

- [ ] **Step 3: Finalize the evidence record**

Record in `run.md`:

- each candidate's seven gate results;
- concrete residual Minor findings, if any;
- the cross-scale consistency result;
- the final verdict for each output as `PASS` or `REJECT`;
- confirmation that no retry, composite, promotion, or canonical change was
  performed.

- [ ] **Step 4: Verify the final bounded scope**

Run:

```bash
git diff --check
git status --short --branch
git check-ignore -q tmp/akari-v2.2-single-hairpin/r01/comparison.png
```

Expected: no tracked execution change; the pre-existing unrelated untracked
`docs/superpowers/plans/2026-08-04-akari-v2-0-uniform-batch.md` may remain and
must not be altered; every generated deliverable remains ignored.

- [ ] **Step 5: Present review outputs and stop at selection**

Show the full-figure edit, portrait edit, and comparison. Report each verdict
and any residual Minor plainly. If either result is rejected, keep the original
and ask whether to attempt a bounded correction round. If both pass, ask which
files, if any, the user wants promoted or otherwise preserved. Do not infer
promotion from approval of the visual result.

No commit: Task 4 closes at explicit user review and selection.

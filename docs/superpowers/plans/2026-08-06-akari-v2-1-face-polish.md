# Akari v2.1 Face Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review three controlled front-face polish candidates that preserve the accepted v2.1 identity while restoring the approved v1-derived hair-ornament topology, then stop for explicit user selection.

**Architecture:** Treat the accepted v2.1 face as the sole identity and rendering authority and the v1 image as an ornament-topology reference only. Keep all prompts, candidates, provenance, comparison output, and review evidence under one ignored `r01` directory; make three independent image-generation calls from the same ordered references, apply the eight approved gates, and leave canonical files untouched. This plan ends at candidate selection and contains no promotion task.

**Tech Stack:** Built-in `image_gen`, `view_image`, Markdown run ledgers, ImageMagick `magick` and `identify`, `xxd`, `sha256sum`, `cmp`, Git ignore checks, and markdownlint-cli2.

## Global Constraints

- The approved design is `docs/superpowers/specs/2026-08-06-akari-v2-1-face-polish-design.md`.
- The sole face, identity, hair, expression, eye, palette, and rendering authority is `akari-v2.1/accepted/base/akari-v2.1-front-face-master.png`, dimensions `1023 x 1537`, SHA-256 `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73`.
- The ornament-topology reference only is `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png`, dimensions `1055 x 1491`, SHA-256 `ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21`.
- The accepted full-body baseline `akari-v2.1/accepted/base/akari-v2.1-front-fullbody.png`, SHA-256 `8acc519847d5e02fc8b1917301d800b600b1738cf56b734c9177fa731b6326e3`, is frozen and must not be opened as a generation reference, modified, regenerated, or promoted in this checkpoint.
- Immediately before every identity-sensitive generation call, open both input authorities with `view_image` at `detail: original`, state their distinct roles, and keep them visible in conversation context.
- Make exactly three independent built-in image-generation calls: A, B, and C. Every call uses the same two ordered local reference paths and no recent-conversation image injection.
- A changes the ornament only; B applies the balanced ornament, light hair cleanup, and minimal chin softening; C uses B's ornament and chin treatment with the strongest permitted hair cleanup that retains natural volume.
- Do not change identity, apparent age, eye geometry, gaze, brows, cheeks, nose, mouth, expression, pose, crop, camera, background, ponytail design, laterality, T-shirt, shoulders, or rendering family.
- Never chain a candidate into another call. Never use A, B, C, a comparison derivative, or the full-body image as an input reference.
- Keep all implementation artifacts under ignored `tmp/akari-v2.1-face-polish/r01/`; do not stage or commit them.
- Preserve each returned PNG byte-for-byte. Do not resize, crop, recompress, retouch, composite, or overwrite a candidate; only comparison derivatives may be resized and labeled.
- If a call or payload recovery fails technically, record the failure and stop without a retry or substitute call. If no candidate passes all eight gates, reject all three and stop without retry, retouch, compositing, or regeneration.
- Candidate selection is not promotion. Do not modify `akari-v2.1/README.md`, `akari-v2.1/selection.md`, either accepted PNG, a manifest, release, or PDF.

---

### Task 1: Pin the run contract and complete preflight

**Files:**

- Create locally: `tmp/akari-v2.1-face-polish/r01/RUN.md`
- Create locally: `tmp/akari-v2.1-face-polish/r01/PROMPTS.md`
- Reuse only for payload recovery: `tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs`
- Read: `docs/superpowers/specs/2026-08-06-akari-v2-1-face-polish-design.md`

**Interfaces:**

- Consumes: the approved design, the two immutable input authorities, the frozen full-body hash, and the empty ignored `r01` target.
- Produces: one preflight ledger and one immutable prompt contract whose shared section and candidate deltas are consumed verbatim by Task 2.

- [ ] **Step 1: Verify immutable inputs, output absence, and Git scope**

Run:

```bash
test "$(sha256sum akari-v2.1/accepted/base/akari-v2.1-front-face-master.png | cut -d' ' -f1)" = \
  fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73
test "$(sha256sum akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png | cut -d' ' -f1)" = \
  ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21
test "$(sha256sum akari-v2.1/accepted/base/akari-v2.1-front-fullbody.png | cut -d' ' -f1)" = \
  8acc519847d5e02fc8b1917301d800b600b1738cf56b734c9177fa731b6326e3
identify -format '%f %wx%h %[channels]\n' \
  akari-v2.1/accepted/base/akari-v2.1-front-face-master.png \
  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png \
  akari-v2.1/accepted/base/akari-v2.1-front-fullbody.png
xxd -p -l 8 \
  akari-v2.1/accepted/base/akari-v2.1-front-face-master.png
xxd -p -l 8 \
  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png
test ! -e tmp/akari-v2.1-face-polish/r01
git check-ignore -q tmp/akari-v2.1-face-polish/r01/probe
git status --short --branch
```

Expected: both input hashes and dimensions match Global Constraints; both PNG signatures are `89504e470d0a1a0a`; the full-body hash is unchanged; `r01` is absent; a future file below it is ignored by `.gitignore:12:tmp/`; and the only unrelated untracked path remains `docs/superpowers/plans/2026-08-04-akari-v2-0-uniform-batch.md`.

- [ ] **Step 2: Create the ignored run structure and preflight ledger**

Create these directories without adding a tracked file:

```bash
mkdir -p \
  tmp/akari-v2.1-face-polish/r01/images \
  tmp/akari-v2.1-face-polish/r01/comparison
```

Use `apply_patch` to create `RUN.md` with:

- status `preflight complete; not generated`;
- the approved design path;
- the three Global Constraints paths, roles, dimensions, and hashes;
- the exact candidate destinations `images/akari-v2.1-face-polish-r01-{a,b,c}.png`;
- the rule that each candidate receives one independent call from the same two ordered references;
- the exact concatenation rule: the effective prompt is the plain text under `Shared Prompt` followed by the matching plain text under `Candidate A`, `Candidate B`, or `Candidate C` in `PROMPTS.md`, separated by one blank line;
- the no-retry, no-overwrite, no-transform, no-promotion, and frozen-full-body boundaries;
- the preflight command results and the starting Git status.

Do not add empty generation-ID, hash, or verdict fields. Append those facts only after they exist.

- [ ] **Step 3: Record the exact shared prompt and three deltas**

Use `apply_patch` to create `PROMPTS.md` with the following effective prompt contract:

```text
# Akari v2.1 Face Polish r01 Prompt Contract

## Shared Prompt

Use case: identity-preserving edit of an accepted anime character face master.
Asset: Akari v2.1 front-face polish, r01.

Reference roles, in order:
Image 1 is the SOLE current v2.1 face, identity, expression, eye, hair,
palette, crop, and rendering authority. Preserve this exact same approachable
18-year-old young woman, same-person face, direct gaze, friendly small open
smile, honey-amber almond eyes, brow and eye spacing, warm skin, compact lower
face, warm chestnut hair, off-center V bangs, character-left low side ponytail,
strict-front composition, T-shirt and shoulders, fine anime linework,
restrained cel shading, and warm off-white presentation.

Image 2 is a HAIR-ORNAMENT TOPOLOGY REFERENCE ONLY. Borrow only the idea of
two slim pale-blue crossed straight pins above one compact thin-cord bow with
two narrow loops and two short subtle tails. Do not borrow its face, apparent
age, eyes, head angle, hair length, bob silhouette, pose, outfit, body, color
rendering, or finish.

Primary request:
Edit Image 1 into one polished, full-resolution strict-front face master at
approximately the same 1023 x 1537 portrait size and identical crop. Keep the
existing person and emotional moment. Replace the current bright, strongly
outlined character-left ornament on canvas-right with one coherent hybrid
ornament: two slim pale gray-blue straight pins crossing cleanly, immediately
above one compact thin-cord bow with two short narrow loops and two subtle
short tails. Connect pins, knot, loops, and tails as one complete ornament.
Make it approximately 80 to 85 percent of the current ornament's visual
footprint, readable but quieter than the eyes, with muted color and a soft
outline integrated naturally into the hair.

Identity and expression locks:
- Keep the exact same approachable 18-year-old young-adult identity and
  same-person face; neither childlike nor older or glamorized.
- Preserve the exact eye geometry, iris scale, pupils, highlight treatment,
  gaze, brows, cheeks, nose, mouth, small open friendly smile, and face spacing.
- Preserve strict-front head position, level relaxed shoulders, direct gaze,
  camera, crop, background, warm skin, and T-shirt construction.

Hair and laterality locks:
- Preserve warm chestnut color, the off-center V bangs, hairline, ear,
  character-left low side ponytail on canvas-right, ponytail attachment,
  accepted silhouette, natural asymmetry, movement, and readable volume.
- Keep exactly one ornament on character-left/canvas-right. It must not be
  mirrored, duplicated, split, hidden, incomplete, or moved.
- Preserve the ponytail, bangs, jaw-to-neck connection, and shoulder overlap.

Rendering locks:
- Preserve Image 1's fine anime linework, restrained cel shading, bright but
  non-neon palette, clean warm off-white background, and finished face-master
  presentation.
- Keep all anatomy and object connections coherent and preserve comfortable
  margins around the complete hair silhouette.

Avoid:
New person, changed eyes, changed gaze, changed expression, closed mouth,
larger smile, altered brows, changed pose, head tilt, crop shift, new lighting,
new outfit, changed shoulders, child face, older face, long face, wide jaw,
generic ribbon, fabric bow, scissors-like loops, long vertical loops, oversized
tails, heavy black edging, neon or saturated blue, duplicate pins, unrelated
pin cluster, wrong-side ornament, missing ornament piece, disconnected
ponytail, flat helmet hair, gray or darker hair, materially shorter hair,
photorealism, malformed anatomy, duplicated feature, seam, border, text, logo,
watermark, or material generation artifact.

## Candidate A

Candidate A, ornament-only: make only the complete hybrid-ornament replacement
and the minimum local integration needed around it. Preserve Image 1's current
hair highlights, flyaways, internal strand lines, chin point, jaw, and lower
face as closely as the model allows. Do not perform general hair cleanup or
chin reshaping.

## Candidate B

Candidate B, balanced and recommended: apply the complete hybrid ornament.
Lightly reduce only the strongest crown and ponytail highlight shapes and
remove only excess high-frequency flyaways or internal strand noise while
preserving main hair masses, natural asymmetry, movement, and volume. Soften
the chin point by the minimum visible amount without widening, lengthening, or
replacing the compact lower-face identity.

## Candidate C

Candidate C, stronger hair cleanup: apply exactly the same complete hybrid
ornament and minimal chin treatment requested for Candidate B. Make the
strongest permitted reduction in the conspicuous crown highlight, ponytail
highlight, excess flyaways, and small internal strand noise, but retain warm
chestnut color, natural asymmetry, movement, separated hair masses, and clear
volume. Do not make the hair flat, helmet-like, uniformly smooth, gray, darker,
or materially shorter.
```

- [ ] **Step 4: Verify and freeze the local prompt contract**

Run:

```bash
sha256sum \
  tmp/akari-v2.1-face-polish/r01/RUN.md \
  tmp/akari-v2.1-face-polish/r01/PROMPTS.md
./node_modules/.bin/markdownlint-cli2 \
  tmp/akari-v2.1-face-polish/r01/RUN.md \
  tmp/akari-v2.1-face-polish/r01/PROMPTS.md
git check-ignore -v \
  tmp/akari-v2.1-face-polish/r01/RUN.md \
  tmp/akari-v2.1-face-polish/r01/PROMPTS.md
```

Expected: both local Markdown files have recorded hashes, lint passes, and both paths are ignored. After recording the prompt hash in `RUN.md`, do not edit `PROMPTS.md` during r01.

### Task 2: Generate and preserve A, B, and C independently

**Required sub-skill:** `imagegen`

**Files:**

- Read: `tmp/akari-v2.1-face-polish/r01/PROMPTS.md`
- Create locally: `tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png`
- Create locally: `tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png`
- Create locally: `tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png`
- Modify locally: `tmp/akari-v2.1-face-polish/r01/RUN.md`
- Reuse only if needed: `tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs`

**Interfaces:**

- Consumes: Task 1's frozen prompt contract, the same two ordered input authorities, and three absent output paths.
- Produces: three independent exact-output PNGs and complete per-call provenance for Task 3.

- [ ] **Step 1: Generate Candidate A from freshly opened authorities**

Immediately before the call, use `view_image` with `detail: original` on:

```text
/home/takahiro/workspace/akari-design/akari-v2.1/accepted/base/akari-v2.1-front-face-master.png
/home/takahiro/workspace/akari-design/akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png
```

State that Image 1 is the sole v2.1 identity, face, eyes, expression, hair, crop, palette, and rendering authority; Image 2 controls only the crossed-pins-plus-compact-cord-bow topology. Call `image_gen` once with the effective A prompt and `referenced_image_paths` set to exactly those two paths in that order. Omit `num_last_images_to_include`.

- [ ] **Step 2: Preserve and verify Candidate A**

When the tool returns a readable local source path, bind `akari_generated_source` to that exact path, then save it without overwrite and verify the bytes:

```bash
: "${akari_generated_source:?set the exact readable local tool source path}"
test -f "$akari_generated_source"
test ! -e tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png
cp --no-clobber -- "$akari_generated_source" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png
cmp --silent -- "$akari_generated_source" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png
```

Use that block only when the tool returns an actual readable local source path, replacing the shown literal with that exact path. If no local source exists, recover only the completed A call payload with:

```bash
akari_session_day="$(TZ=Asia/Tokyo date +%Y/%m/%d)"
: "${akari_candidate_a_call_id:?record the completed Candidate A call ID}"
export akari_session_day akari_candidate_a_call_id
bash -lc 'node tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs \
  "$akari_candidate_a_call_id" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png \
  "$akari_session_day"'
```

The recovery script must find exactly one matching `image_generation_call` or `image_generation_end` payload beginning `iVBOR`, verify PNG signature `89504e470d0a1a0a`, and refuse overwrite. If preservation or recovery fails, append `technical failure after Candidate A; no retry` to `RUN.md` and stop.

Run:

```bash
file tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png
xxd -p -l 8 \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png
sha256sum \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png
```

Append the exact effective prompt components, prompt-contract hash, ordered reference paths, outer request ID, completed call ID, tool-provided source path or rollout recovery path, destination, `cmp` result when copied, dimensions, channels, signature, and SHA-256 to `RUN.md`.

- [ ] **Step 3: Generate and preserve Candidate B independently**

Immediately before the B call, reopen both absolute reference paths from Step 1 with `view_image` at `detail: original`. Restate that Image 1 is the sole v2.1 identity, face, eyes, expression, hair, crop, palette, and rendering authority and Image 2 controls only the approved ornament topology. Call `image_gen` once with the effective B prompt and exactly the same two ordered `referenced_image_paths`; omit `num_last_images_to_include`.

When a readable local source is returned, bind `akari_generated_source` to it and run:

```bash
: "${akari_generated_source:?set the exact readable local tool source path}"
test -f "$akari_generated_source"
test ! -e tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png
cp --no-clobber -- "$akari_generated_source" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png
cmp --silent -- "$akari_generated_source" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png
```

If no local source exists, bind `akari_candidate_b_call_id` to the completed B call ID and run:

```bash
akari_session_day="$(TZ=Asia/Tokyo date +%Y/%m/%d)"
: "${akari_candidate_b_call_id:?record the completed Candidate B call ID}"
export akari_session_day akari_candidate_b_call_id
bash -lc 'node tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs \
  "$akari_candidate_b_call_id" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png \
  "$akari_session_day"'
```

Verify and record B independently:

```bash
file tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png
xxd -p -l 8 \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png
sha256sum \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png
```

Append B's exact effective prompt components, prompt-contract hash, ordered references, outer request ID, completed call ID, source or recovery path, destination, `cmp` result when copied, dimensions, channels, signature, and hash to `RUN.md`. Do not reference Candidate A in the prompt or input list. On technical failure, record `technical failure after Candidate B; no retry` and stop.

- [ ] **Step 4: Generate and preserve Candidate C independently**

Immediately before the C call, reopen both absolute reference paths from Step 1 with `view_image` at `detail: original`. Restate that Image 1 is the sole v2.1 identity, face, eyes, expression, hair, crop, palette, and rendering authority and Image 2 controls only the approved ornament topology. Call `image_gen` once with the effective C prompt and exactly the same two ordered `referenced_image_paths`; omit `num_last_images_to_include`.

When a readable local source is returned, bind `akari_generated_source` to it and run:

```bash
: "${akari_generated_source:?set the exact readable local tool source path}"
test -f "$akari_generated_source"
test ! -e tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png
cp --no-clobber -- "$akari_generated_source" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png
cmp --silent -- "$akari_generated_source" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png
```

If no local source exists, bind `akari_candidate_c_call_id` to the completed C call ID and run:

```bash
akari_session_day="$(TZ=Asia/Tokyo date +%Y/%m/%d)"
: "${akari_candidate_c_call_id:?record the completed Candidate C call ID}"
export akari_session_day akari_candidate_c_call_id
bash -lc 'node tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs \
  "$akari_candidate_c_call_id" \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png \
  "$akari_session_day"'
```

Verify and record C independently:

```bash
file tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png
xxd -p -l 8 \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png
sha256sum \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png
```

Append C's exact effective prompt components, prompt-contract hash, ordered references, outer request ID, completed call ID, source or recovery path, destination, `cmp` result when copied, dimensions, channels, signature, and hash to `RUN.md`. Do not reference Candidate A or B in the prompt or input list. On technical failure, record `technical failure after Candidate C; no retry` and stop.

- [ ] **Step 5: Verify the complete immutable candidate set**

Run:

```bash
test "$(find tmp/akari-v2.1-face-polish/r01/images -maxdepth 1 -type f -name '*.png' | wc -l)" -eq 3
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-face-polish/r01/images/*.png
xxd -p -l 8 \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png
xxd -p -l 8 \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png
xxd -p -l 8 \
  tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png
sha256sum tmp/akari-v2.1-face-polish/r01/images/*.png
git check-ignore -v tmp/akari-v2.1-face-polish/r01/images/*.png
```

Expected: exactly three non-empty readable RGB or RGBA portrait PNGs, three signatures `89504e470d0a1a0a`, three recorded hashes, and all outputs ignored. Update `RUN.md` to `generation complete; review pending`. Do not choose a candidate yet.

### Task 3: Build the equal-scale comparison, apply all gates, and stop

**Files:**

- Create locally: `tmp/akari-v2.1-face-polish/r01/comparison/current-card.png`
- Create locally: `tmp/akari-v2.1-face-polish/r01/comparison/a-card.png`
- Create locally: `tmp/akari-v2.1-face-polish/r01/comparison/b-card.png`
- Create locally: `tmp/akari-v2.1-face-polish/r01/comparison/c-card.png`
- Create locally: `tmp/akari-v2.1-face-polish/r01/akari-v2.1-face-polish-r01-comparison.png`
- Create locally: `tmp/akari-v2.1-face-polish/r01/REVIEW.md`
- Modify locally: `tmp/akari-v2.1-face-polish/r01/RUN.md`

**Interfaces:**

- Consumes: the current accepted face, v1 topology reference, exact A/B/C PNGs, prompt contract, and recorded provenance.
- Produces: one labeled equal-scale control/A/B/C comparison, an eight-gate verdict for every candidate, a quality-first recommendation among eligible candidates, and an explicit selection stop.

- [ ] **Step 1: Create labeled equal-scale comparison derivatives**

Run these commands. They resize only disposable comparison cards and never alter the current authority or candidate PNGs:

```bash
magick akari-v2.1/accepted/base/akari-v2.1-front-face-master.png \
  -auto-orient -resize '720x1080>' -background '#f7f0e8' \
  -gravity center -extent 760x1120 -gravity north -splice 0x72 \
  -font DejaVu-Sans -pointsize 34 -fill '#332b27' \
  -annotate +0+18 'Current v2.1' \
  tmp/akari-v2.1-face-polish/r01/comparison/current-card.png
magick tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-a.png \
  -auto-orient -resize '720x1080>' -background '#f7f0e8' \
  -gravity center -extent 760x1120 -gravity north -splice 0x72 \
  -font DejaVu-Sans -pointsize 34 -fill '#332b27' \
  -annotate +0+18 'A - ornament only' \
  tmp/akari-v2.1-face-polish/r01/comparison/a-card.png
magick tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-b.png \
  -auto-orient -resize '720x1080>' -background '#f7f0e8' \
  -gravity center -extent 760x1120 -gravity north -splice 0x72 \
  -font DejaVu-Sans -pointsize 34 -fill '#332b27' \
  -annotate +0+18 'B - balanced' \
  tmp/akari-v2.1-face-polish/r01/comparison/b-card.png
magick tmp/akari-v2.1-face-polish/r01/images/akari-v2.1-face-polish-r01-c.png \
  -auto-orient -resize '720x1080>' -background '#f7f0e8' \
  -gravity center -extent 760x1120 -gravity north -splice 0x72 \
  -font DejaVu-Sans -pointsize 34 -fill '#332b27' \
  -annotate +0+18 'C - stronger cleanup' \
  tmp/akari-v2.1-face-polish/r01/comparison/c-card.png
magick montage \
  tmp/akari-v2.1-face-polish/r01/comparison/current-card.png \
  tmp/akari-v2.1-face-polish/r01/comparison/a-card.png \
  tmp/akari-v2.1-face-polish/r01/comparison/b-card.png \
  tmp/akari-v2.1-face-polish/r01/comparison/c-card.png \
  -tile 2x2 -geometry +20+20 -background '#e9ddd1' \
  tmp/akari-v2.1-face-polish/r01/akari-v2.1-face-polish-r01-comparison.png
identify -format '%f %wx%h\n' \
  tmp/akari-v2.1-face-polish/r01/comparison/*.png \
  tmp/akari-v2.1-face-polish/r01/akari-v2.1-face-polish-r01-comparison.png
```

Expected: all four cards have identical dimensions and padding, and one readable 2-by-2 comparison contains Current, A, B, and C without changing source bytes. Open the comparison with `view_image`.

- [ ] **Step 2: Inspect every authority and candidate at original detail**

Use `view_image` with `detail: original` on the current v2.1 face, the v1 ornament reference, and A, B, and C individually. Inspect the face, both eyes, ornament construction, chin, hairline, crown, ponytail attachment, ear, jaw-to-neck connection, shoulders, crop, and background. Use the current v2.1 face for all same-person and rendering judgments; use v1 only to judge the approved ornament topology.

- [ ] **Step 3: Write the eight-gate review with concrete evidence**

Use `apply_patch` to create `REVIEW.md`. For A, B, and C, record exactly one `Pass` or `Fail` and concrete visual evidence for every gate:

1. immediately recognizable as the same accepted v2.1 Akari;
2. approachable 18-year-old young-adult read;
3. compatible eyes, gaze, brows, cheeks, nose, mouth, expression, and face spacing;
4. complete hybrid ornament with approved topology, scale, muted color, quiet outline, and character-left/canvas-right placement;
5. accepted hair silhouette, off-center V bangs, connected low ponytail, warm chestnut palette, natural movement, and readable volume;
6. unchanged chin for A or only minimal, identity-compatible chin softening for B/C;
7. visible improvement over Current in ornament treatment without a larger weakness;
8. no malformed anatomy, duplication, disconnected strand or ornament piece, seam, border, text, watermark, or material artifact.

Also record:

- concrete residual Minors for every all-pass candidate;
- every failed gate and disqualifying reason for every failed candidate;
- a quality-first ranking among all-pass candidates using same-person continuity, v1-derived ornament charm, v2.1 finish, natural hair volume, and future reuse;
- one recommendation only if at least one candidate passes all eight gates;
- `reject all three` if none passes all eight gates;
- the boundary that recommendation is not selection and selection is not canonical promotion.

Do not select the least-bad failed image. Do not retouch, composite, regenerate, or change the prompt after review.

- [ ] **Step 4: Run final provenance, canonical-scope, and Markdown checks**

Run:

```bash
test "$(sha256sum akari-v2.1/accepted/base/akari-v2.1-front-face-master.png | cut -d' ' -f1)" = \
  fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73
test "$(sha256sum akari-v2.1/accepted/base/akari-v2.1-front-fullbody.png | cut -d' ' -f1)" = \
  8acc519847d5e02fc8b1917301d800b600b1738cf56b734c9177fa731b6326e3
sha256sum tmp/akari-v2.1-face-polish/r01/images/*.png
./node_modules/.bin/markdownlint-cli2 \
  tmp/akari-v2.1-face-polish/r01/RUN.md \
  tmp/akari-v2.1-face-polish/r01/PROMPTS.md \
  tmp/akari-v2.1-face-polish/r01/REVIEW.md
bash -lc 'npm run lint:md'
git check-ignore -v \
  tmp/akari-v2.1-face-polish/r01/RUN.md \
  tmp/akari-v2.1-face-polish/r01/PROMPTS.md \
  tmp/akari-v2.1-face-polish/r01/REVIEW.md \
  tmp/akari-v2.1-face-polish/r01/images/*.png \
  tmp/akari-v2.1-face-polish/r01/akari-v2.1-face-polish-r01-comparison.png
git diff --check
git status --short -- akari-v2.1
git status --short --branch
```

Expected: both canonical hashes remain fixed; all three candidate hashes match the provenance recorded in `RUN.md`; local and tracked Markdown lint pass; every run artifact is ignored; no path below `akari-v2.1/` changed; no candidate is staged; and the unrelated user-owned v2.0 uniform-batch plan remains untouched.

- [ ] **Step 5: Present the comparison and enforce the selection stop**

Show:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-face-polish/r01/akari-v2.1-face-polish-r01-comparison.png
```

Report A/B/C pass or fail, concrete residual Minors, and the quality-first recommendation in concise Japanese. Ask the user to select `A`, `B`, or `C` only from all-pass candidates, or to reject the set. Stop after the response is received. Do not copy into `akari-v2.1/accepted/`, update documentation, stage, commit, push, or begin another generation round without a separate explicit instruction.

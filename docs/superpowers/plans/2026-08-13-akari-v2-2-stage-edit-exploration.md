# Akari V2.2 Stage Edit Exploration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate three independent, one-variable edits from the identity-approved and wardrobe-selected Candidate 2, then present identity-only comparison artifacts without reusing rejected outputs.

**Architecture:** Use built-in `image_gen.imagegen` in edit mode with exactly two local inputs per candidate: Candidate 2 as the edit target and the canonical portrait as the sole facial authority. Generate candidates A, B, and C independently from the same approved target, save all review artifacts under ignored `tmp/`, and stop after identity comparison.

**Tech Stack:** Built-in `image_gen.imagegen`, local `view_image`, ImageMagick `identify`/`magick`, Git-ignored review files, Markdown run ledger.

## Global Constraints

- Do not restart the failed new-scene or full-body generation route.
- Do not use Candidate 3 or any rejected or unapproved image as an input, edit target, crop source for continuity, anchor, composite source, or prompt-derived continuity description.
- Image A is Candidate 2, the user-approved edit target and wardrobe reference.
- Image B is `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`, the sole facial identity authority.
- Inspect `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp` before generation, but do not pass it to any call.
- Use one built-in call per candidate and change exactly one element in each call.
- Never pass a generated candidate into another candidate's call.
- Save candidates, crops, comparison artifacts, and the run ledger under `tmp/akari-v22-stage-edit-exploration-2026-08-13/`; do not add them to Git.
- Stop after the three identity comparisons. Do not promote an anchor or preserve a formal deliverable without a new explicit user decision.

---

### Task 1: Verify and inspect the approved inputs

**Files:**

- Read: `tmp/akari-v22-identity-recovery-2026-08-12/candidate-2-wardrobe-only.png`
- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp`
- Create: `tmp/akari-v22-stage-edit-exploration-2026-08-13/run-record.txt`

**Interfaces:**

- Consumes: the approved state recorded in `tmp/akari-v22-identity-recovery-2026-08-12/run-record.txt`.
- Produces: three visually inspected, readable local paths and a run ledger that records each image's role.

- [ ] **Step 1: Verify that the three required paths are readable images**

Run:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  tmp/akari-v22-identity-recovery-2026-08-12/candidate-2-wardrobe-only.png \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp
```

Expected: three readable sRGB images. Stop without generating if any image is missing or unreadable.

- [ ] **Step 2: Open all three images at original detail**

Use `view_image` separately for Candidate 2, the canonical portrait, and the canonical full body. Confirm these roles before generation:

- Candidate 2: edit target, accepted identity, selected wardrobe.
- Canonical portrait: sole facial authority.
- Canonical full body: inspection-only body/laterality authority, excluded from calls.

- [ ] **Step 3: Create the ignored run directory and ledger**

Create the directory with `mkdir -p tmp/akari-v22-stage-edit-exploration-2026-08-13/`. Create `run-record.txt` with `apply_patch`; record the date, built-in execution mode, exact input paths, authority roles, and the prohibition on Candidate 3.

- [ ] **Step 4: Verify review output remains ignored**

Run:

```bash
git check-ignore -v tmp/akari-v22-stage-edit-exploration-2026-08-13/
```

Expected: an ignore rule covering `tmp/`.

### Task 2: Generate three independent one-variable edits

**Files:**

- Read: `tmp/akari-v22-identity-recovery-2026-08-12/candidate-2-wardrobe-only.png`
- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Create: `tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-a-closer-framing.png`
- Create: `tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-b-closed-mouth-smile.png`
- Create: `tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-c-morning-light.png`
- Modify: `tmp/akari-v22-stage-edit-exploration-2026-08-13/run-record.txt`

**Interfaces:**

- Consumes: the two verified input paths and roles from Task 1.
- Produces: three local PNG candidates created by separate built-in calls; none is approved or reusable yet.

- [ ] **Step 1: Generate Candidate A with framing as the only change**

Call `image_gen.imagegen` once with the Candidate 2 path first and canonical portrait path second. Use this prompt:

```text
Use case: identity-preserve
Asset type: Akari V2.2 staged edit candidate A

Image A is the user-approved edit target. Preserve its person, seated pose, jumperskirt wardrobe, bright open smile, warm-cream background, neutral daylight, and V2.2 rendering.
Image B is the sole facial identity authority. Preserve its face shape, eye opening and iris scale, eyebrow-to-eye relation, cheek-to-short-chin transition, mouth-to-cheek response, bangs, warm chestnut hair, low side ponytail, blue tie, and exactly one blue capsule hairpin on viewer-right.

Change only the camera framing: move from knee-up to a closer waist-up portrait while keeping the same head angle, gaze, pose, expression, wardrobe, background, and lighting.

Do not redesign the face, narrow or lengthen the eyes, shrink the irises, lengthen the jaw, re-age the face, change the pose, change the wardrobe, add hairpins, or add text.
```

Copy the returned PNG non-destructively to `candidate-a-closer-framing.png`. Do not use the output in later calls.

- [ ] **Step 2: Generate Candidate B with expression as the only change**

Call `image_gen.imagegen` once with the same two input paths. Use this prompt:

```text
Use case: identity-preserve
Asset type: Akari V2.2 staged edit candidate B

Image A is the user-approved edit target. Preserve its person, seated knee-up framing, pose, jumperskirt wardrobe, warm-cream background, neutral daylight, and V2.2 rendering.
Image B is the sole facial identity authority. Preserve its face shape, eye opening and iris scale, eyebrow-to-eye relation, cheek-to-short-chin transition, bangs, warm chestnut hair, low side ponytail, blue tie, and exactly one blue capsule hairpin on viewer-right.

Change only the expression: replace the bright open smile with a natural gentle closed-mouth smile. Keep the cheek response warm and subtle. Keep the same head angle, gaze, pose, framing, wardrobe, background, and lighting.

Do not redesign the face, narrow or lengthen the eyes, shrink the irises, lengthen the jaw, re-age the face, change the pose, change the wardrobe, add hairpins, or add text.
```

Copy the returned PNG non-destructively to `candidate-b-closed-mouth-smile.png`. Do not use the output in later calls.

- [ ] **Step 3: Generate Candidate C with lighting as the only change**

Call `image_gen.imagegen` once with the same two input paths. Use this prompt:

```text
Use case: lighting-weather
Asset type: Akari V2.2 staged edit candidate C

Image A is the user-approved edit target. Preserve its person, seated knee-up framing, pose, bright open smile, jumperskirt wardrobe, warm-cream background, and V2.2 rendering.
Image B is the sole facial identity authority. Preserve its face shape, eye opening and iris scale, eyebrow-to-eye relation, cheek-to-short-chin transition, mouth-to-cheek response, bangs, warm chestnut hair, low side ponytail, blue tie, and exactly one blue capsule hairpin on viewer-right.

Change only the lighting: replace the neutral daylight with soft warm morning side light and a very gentle shadow transition. Keep the same head angle, gaze, pose, expression, framing, wardrobe, and background geometry.

Do not redesign the face, narrow or lengthen the eyes, shrink the irises, lengthen the jaw, re-age the face, change the pose, change the wardrobe, add hairpins, add objects, or add text.
```

Copy the returned PNG non-destructively to `candidate-c-morning-light.png`. Do not use the output in later calls.

- [ ] **Step 4: Validate all three local outputs**

Run:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-a-closer-framing.png \
  tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-b-closed-mouth-smile.png \
  tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-c-morning-light.png
```

Expected: three readable sRGB PNG files. Append each built-in output path, local path, and exact prompt to `run-record.txt`.

### Task 3: Build identity-only review artifacts and stop

**Files:**

- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `tmp/akari-v22-identity-recovery-2026-08-12/candidate-2-wardrobe-only.png`
- Read: the three candidates from Task 2
- Create: `tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-a-identity-comparison.png`
- Create: `tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-b-identity-comparison.png`
- Create: `tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-c-identity-comparison.png`
- Modify: `tmp/akari-v22-stage-edit-exploration-2026-08-13/run-record.txt`

**Interfaces:**

- Consumes: three independent `identity_pending` candidates.
- Produces: three four-panel comparison artifacts and a user-facing identity-only review gate.

- [ ] **Step 1: Inspect each candidate at original detail**

Use `view_image` for all three candidates. Exclude any candidate that clearly changed more than its assigned one element, became full-body, or made the face too small to compare. Record the exclusion reason; do not retry it.

- [ ] **Step 2: Create same-display-scale face crops**

For each candidate, create unwarped rectangular crops of the canonical portrait face, Candidate 2 face, and candidate face. Use ImageMagick crop only: no rotation, geometry alignment, face-shape correction, or distortion. Resize each crop proportionally to the same displayed head scale and record the crop rectangles in `run-record.txt`.

- [ ] **Step 3: Assemble one four-panel artifact per candidate**

For each artifact, place these elements on one canvas in this order:

1. canonical portrait face crop;
2. Candidate 2 approved face crop;
3. current candidate face crop;
4. current candidate full frame, reduced proportionally for framing confirmation only.

Label the panels `Canonical`, `Approved control`, `Candidate`, and `Full frame`. Use a neutral light background. Do not retouch any source.

- [ ] **Step 4: Validate and present the identity gate**

Run:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  tmp/akari-v22-stage-edit-exploration-2026-08-13/candidate-?-identity-comparison.png
git status --short --branch
git check-ignore -v tmp/akari-v22-stage-edit-exploration-2026-08-13/
```

Expected: three readable sRGB comparison PNGs, all review images ignored by Git, and no new tracked image changes. Present the comparison artifacts and ask only whether each candidate preserves Akari's identity. Stop before any anchor promotion, second round, acceptance copy, manifest edit, or retry.

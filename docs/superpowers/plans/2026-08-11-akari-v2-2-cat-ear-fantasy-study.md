# Akari V2.2 Cat-Ear Fantasy Study Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, verify, and present six noncanonical Akari V2.2 cat-ear fantasy candidates based on the approved scene set.

**Architecture:** Three independent workers each own two numbered images and save only to distinct paths in one ignored batch directory. Every built-in generation uses the canonical portrait and full-body authorities plus one relevant local composition reference, then an independent visual reviewer audits the final six before a contact sheet is assembled.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick `montage`/`identify`, Markdown prompt provenance, Git-ignored `tmp/` output.

## Global Constraints

- The design source of truth is `docs/superpowers/specs/2026-08-11-akari-v2-2-cat-ear-fantasy-study-design.md`.
- Use built-in `image_gen`; issue one call per distinct asset.
- Inspect and label the canonical V2.2 portrait and full-body roles before every generation.
- Use the local cute-composition pack only for visual grammar; never copy its identity, ear design, clothing, pose, objects, or graphic decoration.
- Exactly two naturally grown chestnut cat ears, no visible human ears, no tail, no ear headband, and no other animal traits.
- Preserve one canvas-right blue capsule hairpin and one same-side blue-elastic low ponytail.
- Preserve the 25-year-old adult identity, modest adult wardrobe, coherent anatomy, singular prop interactions, and real physical spaces.
- Save final candidates as 1024 x 1536 RGB PNG files below `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/`.
- Keep all candidates untracked and noncanonical until the user explicitly accepts one.

---

### Task 1: Prepare the Batch and Reference Set

**Files:**

- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/`
- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/PROMPTS.md`

**Interfaces:**

- Consumes: the approved design spec and four local reference paths.
- Produces: a unique destination for each numbered image and one prompt-provenance document.

- [ ] **Step 1: Verify all reference files and the local-pack README exist**

Run:

```bash
test -f akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp
test -f akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp
test -f akari-v2.2/accepted/daily/life/akari-v2.2-d07-fan-breeze.png
test -f local-reference-packs/akari-v2.2-cute-composition/README.md
```

Expected: every command exits 0.

- [ ] **Step 2: Create the ignored batch directory**

Run:

```bash
mkdir -p tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01
```

Expected: the directory exists and `git check-ignore` reports it as ignored.

- [ ] **Step 3: Open the portrait, full-body, D07, and selected local composition references at original detail**

Expected: all references are visible before the first image-generation call.

### Task 2: Generate Candidates 01 and 02

**Files:**

- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/01-book-peek.png`
- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/02-arcade-win.png`

**Interfaces:**

- Consumes: shared reference contract and scene definitions 01-02.
- Produces: two final original-size PNGs plus exact prompts and source paths for `PROMPTS.md`.

- [ ] **Step 1: Generate 01 with portrait, full-body, D07, and local reference 03**

Expected: one book, two separate book-corner hand contacts, canonical laterality, two natural cat ears, hidden human ears, and no tail.

- [ ] **Step 2: Generate 02 with portrait, full-body, D07, and local reference 07**

Expected: one joystick, one button, separated hand actions, canonical laterality, two natural cat ears, hidden human ears, and no tail.

- [ ] **Step 3: Inspect both at original detail and use at most one targeted correction per hard failure**

Expected: final saved files have no unresolved hard failure; otherwise the report names the unresolved defect.

### Task 3: Generate Candidates 03 and 04

**Files:**

- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/03-rooftop-lights.png`
- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/04-camera-walk.png`

**Interfaces:**

- Consumes: shared reference contract and scene definitions 03-04.
- Produces: two final original-size PNGs plus exact prompts and source paths for `PROMPTS.md`.

- [ ] **Step 1: Generate 03 with portrait, full-body, D07, and local reference 07**

Expected: one attached bulb cord, one clip, readable railing contact, below-knee dress, canonical lookback laterality, two natural cat ears, hidden human ears, and no tail.

- [ ] **Step 2: Generate 04 with portrait, full-body, D07, and local reference 03**

Expected: one compact camera, one continuous attached strap, two supporting hands, midi skirt, two natural cat ears, hidden human ears, and no tail.

- [ ] **Step 3: Inspect both at original detail and use at most one targeted correction per hard failure**

Expected: final saved files have no unresolved hard failure; otherwise the report names the unresolved defect.

### Task 4: Generate Candidates 05 and 06

**Files:**

- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/05-honest-ears.png`
- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/06-good-key-sound.png`

**Interfaces:**

- Consumes: shared reference contract and scene definitions 05-06.
- Produces: two final original-size PNGs plus exact prompts and source paths for `PROMPTS.md`.

- [ ] **Step 1: Generate 05 with portrait, full-body, D07, and local reference 06**

Expected: adult trouser suit, one jacket-button contact, one plain folio, canonical laterality, two natural cat ears, hidden human ears, and no tail.

- [ ] **Step 2: Generate 06 with portrait, full-body, D07, and local reference 03**

Expected: one keyboard with one coral key, one pressing finger, one supporting hand, canonical laterality, two natural cat ears, hidden human ears, and no tail.

- [ ] **Step 3: Inspect both at original detail and use at most one targeted correction per hard failure**

Expected: final saved files have no unresolved hard failure; otherwise the report names the unresolved defect.

### Task 5: Independent Batch QA and Presentation

**Files:**

- Modify: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/PROMPTS.md`
- Create: `tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/cat-ear-fantasy-contact-sheet.jpg`

**Interfaces:**

- Consumes: all six final candidate files and worker provenance reports.
- Produces: one verified batch summary and one review image for the user.

- [ ] **Step 1: Verify file format, dimensions, and color model**

Run:

```bash
identify -format '%f %wx%h %[colorspace]\n' tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/0*.png
```

Expected: six lines, each reporting `1024x1536` and `sRGB` or `RGB`.

- [ ] **Step 2: Review all six against the shared identity, ear, anatomy, wardrobe, prop, and space gates**

Expected: each candidate receives a PASS, MINOR, or HARD verdict with concrete visual evidence.

- [ ] **Step 3: Write exact final prompts, generation source paths, saved paths, and QA verdicts to `PROMPTS.md`**

Expected: every numbered candidate has a complete provenance section and no incomplete markers.

- [ ] **Step 4: Assemble the six-up contact sheet from the final saved files**

Run:

```bash
montage tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/0*.png -thumbnail 384x576 -tile 3x2 -geometry +12+12 -background '#f3efe9' tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/cat-ear-fantasy-contact-sheet.jpg
```

Expected: a readable 3 x 2 sheet containing each final candidate once in numeric order.

- [ ] **Step 5: Confirm the batch remains ignored and accepted-package files are untouched**

Run:

```bash
git check-ignore tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01/01-book-peek.png
git status --short -- akari-v2.2 tmp/akari-v2.2-cat-ear-fantasy-study-20260811/r01
```

Expected: the candidate is ignored and no tracked `akari-v2.2` file is modified.

# Akari V2.2 Milky-Pop Cat-Ear Study Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate twelve review-ready, noncanonical Akari V2.2 cat-ear
illustrations with three distinct camera lanes, dynamic pop composition, and a
luminous milky-pastel palette.

**Architecture:** Six independent generation workers each own one numbered
pair and one report file under a shared ignored run directory. Every image uses
the same canonical identity inputs plus a scene-specific composition input and
the user mood reference; an independent final reviewer then checks all saved
files together and builds the 4 x 3 review sheet.

**Tech Stack:** Built-in `image_gen`, local `view_image`, PNG files, ImageMagick
`montage`/`identify`, Markdown prompt and QA records.

## Global Constraints

- Design authority:
  `docs/superpowers/specs/2026-08-11-akari-v2-2-milky-pop-cat-ear-study-design.md`.
- Final workspace root:
  `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/`.
- Use built-in `image_gen`; issue one generation call per requested image.
- Before every call, inspect every referenced image with `view_image` at
  original detail and label each input role in the prompt.
- Every call uses at most five referenced paths: canonical portrait, canonical
  full body, user mood reference, one local composition reference, and D07 when
  useful for motion or spatial grounding.
- The accepted portrait wins face, eyes, hair, hairpin, ponytail, and adult-age
  conflicts. The accepted full body wins body balance and laterality conflicts.
- Exactly two natural asymmetric crown cat ears; no visible human ears, tail,
  headband, seams, cap, collar, bell, paw clip, paw gloves, whiskers, or animal
  nose.
- Exactly one filled blue capsule hairpin and one same-side low ponytail tied by
  one blue elastic appear on canvas-right.
- Use modest adult clothing, coherent hands and limbs, coherent prop contact,
  luminous milky pastel color masses, and a genuinely dynamic composition.
- Do not copy any reference identity, outfit, pose, icon field, sticker border,
  or graphic arrangement.
- Save each accepted built-in result unchanged to its assigned workspace path.
  A hard defect permits at most one targeted correction for that image.
- Do not edit tracked V2.2 package files or add the ignored run folder to Git.
- Preserve unrelated `.gitignore` and
  `docs/superpowers/plans/2026-08-04-akari-v2-0-uniform-batch.md` worktree state.

## Shared References

```text
Portrait identity authority:
/home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp

Full-body proportion authority:
/home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp

User pop/asymmetric-ear mood reference:
/home/takahiro/.codex/attachments/d0438499-86a8-413e-84e0-880666d2a706/codex-clipboard-ff414bd0-c8d3-46c1-af14-fc7d05af6159.png

Natural-motion anchor:
/home/takahiro/workspace/akari-design/akari-v2.2/accepted/daily/life/akari-v2.2-d07-fan-breeze.png

Local composition pack:
/home/takahiro/workspace/akari-design/local-reference-packs/akari-v2.2-cute-composition/
```

---

### Task 1: Generate Close-Face 01 and 02

**Files:**

- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/01-cheek-press.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/02-bubble-lens.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/worker-01-02-report.md`

**Interfaces:**

- Consumes: the design specification, the shared portrait/full-body/mood
  references, and local pack image `06-extreme-close-face.jpg`.
- Produces: two final PNGs plus exact prompts, built-in source paths, saved
  paths, iteration notes, dimensions, colorspace, and original-detail QA.

- [ ] **Step 1: Inspect all input roles**

Use `view_image` at original detail for the portrait, full body, user mood
reference, `06-extreme-close-face.jpg`, and D07. Note which visual facts each
input is allowed to control.

- [ ] **Step 2: Generate and save 01 Cheek Press**

Use one built-in call with the five referenced paths. Require the exact scene
from the design, both amber eyes open, one connected index finger pressing one
cheek, asymmetric natural ears, and peach/mint/cream pop diagonals. Copy the
result unchanged to the assigned 01 path.

- [ ] **Step 3: Generate and save 02 Bubble Lens**

Use one separate built-in call with the same five referenced paths. Require one
large coherent iridescent bubble, optical magnification of only part of one
eye, one connected approaching fingertip, and milk-blue/lavender/cream color
separation. Copy the result unchanged to the assigned 02 path.

- [ ] **Step 4: Run pair QA and one-change correction if required**

Inspect both saved PNGs at original detail. Check identity, age, exact ear
count, natural asymmetric construction, hidden human ears, no tail, pin and
ponytail laterality, hand anatomy, scene prop count, pop finish, and dynamic
crop. If a hard defect exists, make only one targeted correction for that file
and reinspect before replacement.

- [ ] **Step 5: Write the worker report**

Record exact final prompts and every source path, including superseded sources.
Verify with:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/01-cheek-press.png \
  tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/02-bubble-lens.png
```

Expected: two readable portrait RGB/sRGB PNGs, targeted at 1024 x 1536.

### Task 2: Generate Close-Face 03 and 04

**Files:**

- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/03-cassette-secret.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/04-sleepy-sleeve.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/worker-03-04-report.md`

**Interfaces:**

- Consumes: the design specification, shared references, and local pack image
  `03-close-face-hand-gesture.jpg`.
- Produces: two final PNGs and a complete prompt/source/QA report.

- [ ] **Step 1: Inspect all input roles**

Open the portrait, full body, user mood reference,
`03-close-face-hand-gesture.jpg`, and D07 at original detail.

- [ ] **Step 2: Generate and save 03 Cassette Secret**

Use one built-in call. Require one unlabeled translucent cassette enlarged in
the foreground, one coherent holding hand, direct adult gaze, opposing face and
prop diagonals, and asymmetric ear attention. Save unchanged to the 03 path.

- [ ] **Step 3: Generate and save 04 Sleepy Sleeve**

Use one separate built-in call. Require one cream knit sleeve supporting the
cheek, one relaxed connected hand emerging from its cuff, half-lidded adult
eyes, butter/lavender/cream slabs, and no paw gesture. Save unchanged to 04.

- [ ] **Step 4: Run pair QA and one-change correction if required**

Inspect original detail for all global gates plus exactly one cassette in 03
and coherent sleeve/hand/cheek contact in 04. Correct a hard defect at most once
per file and preserve all unrelated image content.

- [ ] **Step 5: Write the worker report**

Include exact prompts, source history, saved paths, dimensions, colorspace,
defect verdicts, and whether a correction was used. Run `identify` on both
assigned PNGs.

### Task 3: Generate Foreground-Half 05 and 06

**Files:**

- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/05-sneaker-lace-pull.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/06-paper-plane-catch.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/worker-05-06-report.md`

**Interfaces:**

- Consumes: the design specification, shared references, and local pack image
  `02-kitchen-wide-angle-motion.jpg`.
- Produces: two final PNGs and a complete prompt/source/QA report.

- [ ] **Step 1: Inspect all input roles**

Open the portrait, full body, user mood reference,
`02-kitchen-wide-angle-motion.jpg`, and D07 at original detail.

- [ ] **Step 2: Generate and save 05 Sneaker Lace Pull**

Use one built-in call. Require one mint-and-coral sneaker enlarged in the low
foreground, two connected hands pulling different ends of its one lace, a
grounded second foot, a readable entry bench/floor relationship, and adult
lavender wide-leg trousers. Save unchanged to 05.

- [ ] **Step 3: Generate and save 06 Paper Plane Catch**

Use one separate built-in call. Require exactly one plain paper airplane, one
open receiving hand enlarged by the lens, a separate naturally bracing hand,
and scene-derived air/light bands rather than floating symbols. Save unchanged
to 06.

- [ ] **Step 4: Run pair QA and one-change correction if required**

Check all global gates plus lace continuity, hand separation, shoe/foot/floor
support in 05 and exact plane count, flight direction, palm anatomy, and no
duplicate paper in 06. Correct a hard defect once at most.

- [ ] **Step 5: Write the worker report**

Include exact prompts, complete source history, final QA, `identify` results,
and any unresolved concern.

### Task 4: Generate Foreground-Half 07 and 08

**Files:**

- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/07-clear-umbrella-twirl.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/08-roller-brake.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/worker-07-08-report.md`

**Interfaces:**

- Consumes: the design specification, shared references, and local pack image
  `05-cheer-motion-foreshortening.jpg`.
- Produces: two final PNGs and a complete prompt/source/QA report.

- [ ] **Step 1: Inspect all input roles**

Open the portrait, full body, user mood reference,
`05-cheer-motion-foreshortening.jpg`, and D07 at original detail.

- [ ] **Step 2: Generate and save 07 Clear Umbrella Twirl**

Use one built-in call. Require exactly one transparent canopy, one continuous
shaft and handle, two coherent separated hand contacts, a near curved rim, real
rain/reflections, and a mint/lavender/coral motion diagonal. Save unchanged.

- [ ] **Step 3: Generate and save 08 Roller Brake**

Use one separate built-in call. Require one foreground skate with four
coherent wheels, one grounded second skate, a physically plausible heel brake,
counterbalancing connected arms, and modest adult sportswear. Save unchanged.

- [ ] **Step 4: Run pair QA and one-change correction if required**

Check every global gate plus umbrella geometry/hand contact in 07 and skate
count, wheel count, limb continuity, floor contact, and adult anatomy in 08.
Correct a hard defect once at most per file.

- [ ] **Step 5: Write the worker report**

Record exact prompts, every source, saved paths, original-detail QA,
`identify` output, and unresolved minor issues.

### Task 5: Generate Full-Action 09 and 10

**Files:**

- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/09-picnic-cloth-snap.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/10-bowling-release.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/worker-09-10-report.md`

**Interfaces:**

- Consumes: the design specification, shared references, and local pack image
  `05-cheer-motion-foreshortening.jpg`.
- Produces: two final PNGs and a complete prompt/source/QA report.

- [ ] **Step 1: Inspect all input roles**

Open the portrait, full body, user mood reference,
`05-cheer-motion-foreshortening.jpg`, and D07 at original detail.

- [ ] **Step 2: Generate and save 09 Picnic Cloth Snap**

Use one built-in call. Require one continuous mint/butter/cream cloth held by
two connected hands, a large coherent fabric wave, readable full adult figure,
two grounded feet, and wind-reactive asymmetric ears. Save unchanged.

- [ ] **Step 3: Generate and save 10 Bowling Release**

Use one separate built-in call. Require exactly one foreground lavender ball,
a lane-level camera, a coherent finished bowling release with one planted foot
and one trailing leg, modest adult clothing, and no text or logo. Save unchanged.

- [ ] **Step 4: Run pair QA and one-change correction if required**

Check all global gates plus cloth continuity and hand contact in 09 and ball
count, finger/arm continuity, leg balance, lane grounding, and believable
motion in 10. Correct a hard defect once at most per file.

- [ ] **Step 5: Write the worker report**

Include exact prompts, source histories, saved paths, original-detail QA,
dimensions/colorspace, and unresolved concerns.

### Task 6: Generate Full-Action 11 and 12

**Files:**

- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/11-kite-reel-turn.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/12-jump-rope-cross-step.png`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/worker-11-12-report.md`

**Interfaces:**

- Consumes: the design specification, shared references, and local pack image
  `05-cheer-motion-foreshortening.jpg`.
- Produces: two final PNGs and a complete prompt/source/QA report.

- [ ] **Step 1: Inspect all input roles**

Open the portrait, full body, user mood reference,
`05-cheer-motion-foreshortening.jpg`, and D07 at original detail.

- [ ] **Step 2: Generate and save 11 Kite Reel Turn**

Use one built-in call. Require one coherent reel held by two hands, one
continuous taut string exiting the crop, a readable seaside promenade, coral
windbreaker, knee-covering milk-blue skirt, and full-body wind motion. Save
unchanged.

- [ ] **Step 3: Generate and save 12 Jump-Rope Cross-Step**

Use one separate built-in call. Require one continuous lavender rope, exactly
two handles held separately, a complete arc, coherent cross-step, grounded
adult legs/feet, and knee-covering cream-and-peach athletic clothing. Save
unchanged.

- [ ] **Step 4: Run pair QA and one-change correction if required**

Check every global gate plus reel/string/hand continuity in 11 and rope/handle
count, limb separation, foot placement, and readable action in 12. Correct a
hard defect once at most per file.

- [ ] **Step 5: Write the worker report**

Record exact prompts, all built-in source paths, saved paths, original-detail
QA, dimensions/colorspace, and remaining concerns.

### Task 7: Independent Batch QA and Contact Sheet

**Files:**

- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/independent-qa.md`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/PROMPTS.md`
- Create: `tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/milky-pop-cat-ear-contact-sheet.jpg`

**Interfaces:**

- Consumes: all twelve final PNGs and all six worker reports.
- Produces: one evidence-backed PASS/MINOR/HARD verdict per image, an exact
  consolidated prompt record, and a review sheet built only from final files.

- [ ] **Step 1: Verify the final file set**

Run:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  tmp/akari-v2.2-milky-pop-cat-ear-study-20260811/r01/{01,02,03,04,05,06,07,08,09,10,11,12}-*.png
```

Expected: twelve readable portrait RGB/sRGB PNGs, with any dimension variance
reported rather than silently resized.

- [ ] **Step 2: Inspect all twelve finals independently**

Use `view_image` at original detail on every saved file. For each image, record
identity, adult age, hairpin/ponytail laterality, two natural asymmetric ears,
hidden human ears, no tail, anatomy, action/prop continuity, pop finish,
milky-pastel palette, and dynamic-composition evidence.

- [ ] **Step 3: Consolidate exact prompt provenance**

Merge the six worker reports into `PROMPTS.md` without paraphrasing the final
generation prompts. Keep superseded source history and correction notes under
the relevant numbered image.

- [ ] **Step 4: Build the 4 x 3 contact sheet**

Run ImageMagick from the run directory:

```bash
montage \
  01-cheek-press.png 02-bubble-lens.png 03-cassette-secret.png \
  04-sleepy-sleeve.png 05-sneaker-lace-pull.png 06-paper-plane-catch.png \
  07-clear-umbrella-twirl.png 08-roller-brake.png 09-picnic-cloth-snap.png \
  10-bowling-release.png 11-kite-reel-turn.png 12-jump-rope-cross-step.png \
  -thumbnail 306x459 -background '#fffaf5' -geometry 306x459+0+0 -tile 4x3 \
  milky-pop-cat-ear-contact-sheet.jpg
```

Expected: a 1224 x 1377 four-column, three-row contact sheet containing the
saved finals in numeric order.

- [ ] **Step 5: Final repository-scope verification**

Run:

```bash
git status --short
```

Expected: no tracked or untracked changes from the ignored generation folder;
only the user's pre-existing `.gitignore` modification and untracked V2.0 plan
remain outside already committed design/plan documentation.

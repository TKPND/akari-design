# Akari v2.2 Milky Pastel-Pop Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review six ignored Akari v2.2 milky pastel-pop
daily-life candidates without promoting any candidate to the accepted set.

**Architecture:** Treat each scene as an independent built-in image-generation
unit with an explicit reference-role map and physical-contact guard. Copy each
generated PNG into one ignored run directory, inspect it at original detail,
then assemble a prompt ledger and contact sheet only after all six scene files
exist.

**Tech Stack:** Codex built-in `image_gen`, local `view_image`, ImageMagick
`magick`/`montage`/`identify`, Git, Markdown lint.

## Global Constraints

- The approved design authority is
  `docs/superpowers/specs/2026-08-10-akari-v2-2-milky-pastel-pop-batch-design.md`.
- Use one distinct built-in image-generation call per scene.
- Reopen the canonical portrait, canonical full-body, the most relevant
  accepted pop anchor, and the applicable local composition reference before
  every generation call.
- Use the canonical portrait for face, eyes, hair, single blue hairpin, and low
  side ponytail; use the canonical full-body for adult proportions and
  laterality.
- Local cute-composition images guide framing, diagonal energy, foreground
  scale, clean cel shapes, and color rhythm only; never copy their character,
  face, hairstyle, outfit, mascot, pose, border, sticker outline, symbol field,
  or readable text.
- Keep roughly 75% coherent daily-life scene and 25% flat pop treatment, with
  decorative fields occupying about 12–18% of the frame.
- Use the approved milky palette and reduce background, clothing, prop, and
  shadow saturation about 15–20% relative to D28 and D29 while retaining crisp
  focal contrast.
- Use no stars, hearts, enclosing frames, text, logos, or watermarks.
- Save candidates under
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/`; keep the directory ignored
  and do not promote or commit generated images.

---

### Task 1: Freeze Run Inputs and Ledger Structure

**Files:**

- Create: `tmp/akari-v2.2-pastel-pop-study-20260810/r01/README.md`
- Read:
  `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read:
  `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp`
- Read:
  `akari-v2.2/accepted/daily/life/akari-v2.2-d28-rubber-glove-snap.png`
- Read:
  `akari-v2.2/accepted/daily/life/akari-v2.2-d29-headphone-listen.png`
- Read: `local-reference-packs/akari-v2.2-cute-composition/*.jpg`

**Interfaces:**

- Consumes: the approved design and existing reference images.
- Produces: one run ledger with six numbered scene records containing filename,
  scene intent, exact reference roles, final prompt, generated source path,
  visual review, and correction history.

- [ ] **Step 1: Confirm the run destination is new and ignored**

Run:

```bash
test ! -e tmp/akari-v2.2-pastel-pop-study-20260810/r01
git check-ignore -q tmp/akari-v2.2-pastel-pop-study-20260810/r01
```

Expected: both commands exit `0`; if the first command fails, use the next
unused sibling run number rather than overwriting the existing run.

- [ ] **Step 2: Create the run directory**

Run:

```bash
mkdir -p tmp/akari-v2.2-pastel-pop-study-20260810/r01
```

Expected: the directory exists and remains untracked.

- [ ] **Step 3: Write the ledger skeleton**

Create `README.md` with the approved palette, shared identity rules, numbered
entries `01` through `06`, and these exact output names:

```text
01-glasses-cloth-polish.png
02-ice-tray-twist.png
03-pastel-tape-cut.png
04-phone-case-corner-snap.png
05-hand-crank-pencil-sharpener.png
06-seatbelt-click.png
contact-sheet.png
```

Expected: every numbered entry has fields for reference roles, final prompt,
source path, inspection verdict, and any targeted correction.

### Task 2: Generate Scenes 01 and 02

**Files:**

- Create:
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/01-glasses-cloth-polish.png`
- Create:
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/02-ice-tray-twist.png`
- Modify: `tmp/akari-v2.2-pastel-pop-study-20260810/r01/README.md`

**Interfaces:**

- Consumes: Task 1 reference-role map and shared milky physical-pop rules.
- Produces: two portrait PNGs with readable hand-to-object contact and recorded
  prompts.

- [ ] **Step 1: Reopen the references for Scene 01**

Open with `view_image`: canonical portrait, canonical full-body, D29 for
face-forward close framing, and the selected close-face/hand local reference.

Expected: all four roles are visible before the generation call.

- [ ] **Step 2: Generate Scene 01 with one built-in call**

Use case `illustration-story`. Prompt for Akari polishing one lens of plain
glasses with a cloth while looking through the unobstructed lens. Require both
hands, coherent temples, cloth-to-lens contact, a visible single blue hairpin,
powder-aqua/periwinkle accents, clean two-step cel shading, and the shared
no-copy/no-text constraints.

Expected: one generated portrait image and one local generated source path.

- [ ] **Step 3: Copy and inspect Scene 01**

Copy the generated PNG to its numbered output name, open the copy at original
detail, and record identity, anatomy, glasses geometry, cloth contact, palette,
and artifact verdicts in the ledger.

Expected: the final candidate exists in the run directory; any correction is
limited to one explicit defect.

- [ ] **Step 4: Reopen the references for Scene 02**

Open with `view_image`: canonical portrait, canonical full-body, D28 for
foreground hand/action clarity, and the selected wide-action local reference.

Expected: all four roles are visible before the generation call.

- [ ] **Step 5: Generate, copy, and inspect Scene 02**

Use case `illustration-story`. Prompt for a waist-up kitchen-counter view where
Akari twists opposite ends of one translucent pale-aqua tray and exactly one
ice cube falls into a supported bowl. Require two hands on opposite ends, one
continuous tray, a coherent counter plane, powder-aqua/butter-cream accents,
and the shared identity/rendering constraints.

Expected: `02-ice-tray-twist.png` passes identity, tray continuity, cube path,
bowl support, and pastel-balance review, or receives one targeted correction.

### Task 3: Generate Scenes 03 and 04

**Files:**

- Create:
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/03-pastel-tape-cut.png`
- Create:
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/04-phone-case-corner-snap.png`
- Modify: `tmp/akari-v2.2-pastel-pop-study-20260810/r01/README.md`

**Interfaces:**

- Consumes: Task 1 reference-role map and shared milky physical-pop rules.
- Produces: two portrait PNGs with a single physically continuous action prop.

- [ ] **Step 1: Reopen references and generate Scene 03**

Open canonical portrait, canonical full-body, D28, and the selected tabletop or
foreshortened-hand local reference. Use one built-in call for a low tabletop
close view: one hand stabilizes a plain dispenser while the other pulls one
continuous pale tape strip down onto one cutter. Use blush-coral/warm-white
accents and the shared constraints.

Expected: one roll, one tape strip, one cutter, separate fingers, and no labels
or writing.

- [ ] **Step 2: Copy and inspect Scene 03**

Copy the source PNG to `03-pastel-tape-cut.png`, inspect at original detail,
and record identity, hand anatomy, tape continuity, cutter contact, and palette
verdicts.

Expected: the candidate passes or receives one targeted correction.

- [ ] **Step 3: Reopen references and generate Scene 04**

Open canonical portrait, canonical full-body, D29, and the selected extreme
close-face local reference. Use one built-in call for a face-and-hands close
view: Akari presses the last corner of one plain black-screen phone into one
translucent powder-aqua case. Require three seated corners, one visibly entering
corner, exactly one phone and case, no UI, and blush-coral accents.

Expected: the phone, case, thumb pressure, and final corner are immediately
readable without duplicate devices.

- [ ] **Step 4: Copy and inspect Scene 04**

Copy the source PNG to `04-phone-case-corner-snap.png`, inspect at original
detail, and record identity, hand anatomy, phone/case count, corner seating,
palette, and artifact verdicts.

Expected: the candidate passes or receives one targeted correction.

### Task 4: Generate Scenes 05 and 06

**Files:**

- Create:
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/05-hand-crank-pencil-sharpener.png`
- Create:
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/06-seatbelt-click.png`
- Modify: `tmp/akari-v2.2-pastel-pop-study-20260810/r01/README.md`

**Interfaces:**

- Consumes: Task 1 reference-role map and shared milky physical-pop rules.
- Produces: two portrait PNGs with connected mechanical actions and coherent
  environmental support.

- [ ] **Step 1: Reopen references and generate Scene 05**

Open canonical portrait, canonical full-body, D28, and the selected diagonal
motion local reference. Use one built-in call for a desk-height three-quarter
view: one hand steadies one plain manual sharpener, the other turns its connected
crank, and one thick colored pencil enters the front opening. Use pale
periwinkle/butter-cream accents and the shared constraints.

Expected: pencil, opening, crank shaft, handle, supporting hand, and desk plane
are connected and distinct with no loose duplicate parts.

- [ ] **Step 2: Copy and inspect Scene 05**

Copy the source PNG to `05-hand-crank-pencil-sharpener.png`, inspect at original
detail, and record identity, hand anatomy, mechanism continuity, support,
palette, and artifact verdicts.

Expected: the candidate passes or receives one targeted correction.

- [ ] **Step 3: Reopen references and generate Scene 06**

Open canonical portrait, canonical full-body, D29, and the selected wide-angle
scene local reference. Use one built-in call for a visibly parked car from the
passenger-side dashboard area: Akari guides one metal tongue into one buckle at
her hip, with the belt continuous from shoulder across torso to hip. Use dusty
denim/blush-coral accents and a warm-white cabin.

Expected: one continuous belt, aligned tongue/buckle, supported seated body,
and no road-motion cues, dashboard text, or logos.

- [ ] **Step 4: Copy and inspect Scene 06**

Copy the source PNG to `06-seatbelt-click.png`, inspect at original detail, and
record identity, belt path, buckle alignment, seat/body support, palette, and
artifact verdicts.

Expected: the candidate passes or receives one targeted correction.

### Task 5: Assemble and Verify the Batch

**Files:**

- Create:
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/contact-sheet.png`
- Modify: `tmp/akari-v2.2-pastel-pop-study-20260810/r01/README.md`

**Interfaces:**

- Consumes: all six numbered PNGs and their completed ledger records.
- Produces: a labeled two-column contact sheet and a verified local review
  package ready for explicit user selection.

- [ ] **Step 1: Run independent whole-batch visual review**

Open all six outputs at original detail and score each for canonical identity,
adult impression, anatomy, physical contact, spatial support, pastel balance,
decoration density, reference-copy risk, text/logo/watermark, and artifacts.

Expected: every candidate has an explicit pass/flag verdict in the ledger;
flagged defects are described narrowly rather than hidden.

- [ ] **Step 2: Build the labeled contact sheet**

Use ImageMagick to resize copies only, label each `01` through `06`, and compose
a two-column sheet. Preserve the six source PNGs unchanged.

Expected: `contact-sheet.png` shows all six images in numeric order with labels
large enough to read on mobile.

- [ ] **Step 3: Verify file count, dimensions, and ignore status**

Run:

```bash
identify tmp/akari-v2.2-pastel-pop-study-20260810/r01/0[1-6]-*.png
test "$(find tmp/akari-v2.2-pastel-pop-study-20260810/r01 -maxdepth 1 -name '0[1-6]-*.png' -type f | wc -l)" -eq 6
git check-ignore -q tmp/akari-v2.2-pastel-pop-study-20260810/r01
```

Expected: six readable portrait PNGs are reported and the run directory is
ignored.

- [ ] **Step 4: Verify the ledger and tracked tree**

Run:

```bash
npx markdownlint-cli2 tmp/akari-v2.2-pastel-pop-study-20260810/r01/README.md
git diff --check
git status --short
```

Expected: the ledger has zero Markdown issues, tracked diffs have no whitespace
errors, and no generated candidate or contact-sheet file appears as tracked or
untracked Git content.

- [ ] **Step 5: Present the complete contact sheet**

Render `contact-sheet.png` inline and list the six stable candidate paths. Ask
for explicit selection before changing `akari-v2.2/accepted/`, `README.md`, or
`selection.md`.

Expected: the user can review all six candidates without any implicit
promotion.

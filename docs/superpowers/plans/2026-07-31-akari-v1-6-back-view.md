# Akari v1.6 Back View Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review one canonical straight-back full-body Akari v1.6
reference that closes the approved rear hair, clothing, accessory, and stance
construction.

**Architecture:** Use the approved front and both three-quarter full-body PNGs
as role-labeled image-generation references. Generate one new rear view with
the built-in image tool, save it only in the ignored working directory, and
review it in a four-view comparison. Permit at most one targeted correction
for a hard invariant before returning to a user decision gate.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick `magick
montage`, SHA-256, Git-tracked Markdown design and plan documents.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-31-akari-v1-6-back-view-design.md`.
- Use `build/v1.6-face-drafts/akari-v1.6-fullbody-base-r1.png` as the
  primary body, outfit, scale, rendering, and framing authority.
- Use the accepted pin-side and unpinned-side three-quarter images only as
  rear construction and continuity authorities.
- Generate one exact straight-back full-body view, not a rear three-quarter
  view or a turnaround sheet.
- Keep generated candidates and comparison sheets under the ignored
  `build/v1.6-face-drafts/` directory.
- Do not commit generated PNGs during review.
- Allow at most one targeted correction after the first candidate.
- Keep heavy image operations serial.

---

### Task 1: Generate and review the canonical rear view

**Files:**

- Read:
  `docs/superpowers/specs/2026-07-31-akari-v1-6-back-view-design.md`
- Read:
  `build/v1.6-face-drafts/akari-v1.6-fullbody-base-r1.png`
- Read:
  `build/v1.6-face-drafts/akari-v1.6-fullbody-pin-side-3q-a1.png`
- Read:
  `build/v1.6-face-drafts/akari-v1.6-fullbody-unpinned-side-3q-a2.png`
- Create:
  `build/v1.6-face-drafts/akari-v1.6-fullbody-back-a1.png`
- Create:
  `build/v1.6-face-drafts/akari-v1.6-fullbody-four-view-check-a1.png`
- Create only if a targeted correction is required:
  `build/v1.6-face-drafts/akari-v1.6-fullbody-back-a2.png`
- Create only if a targeted correction is required:
  `build/v1.6-face-drafts/akari-v1.6-fullbody-four-view-check-a2.png`

**Interfaces:**

- Consumes: three approved PNG authorities and the accepted back-view design
  contract.
- Produces: one user-reviewed back-view candidate plus a four-view comparison
  sheet; no tracked release asset or manifest mutation.

- [ ] **Step 1: Verify the exact reference files and working tree**

Run:

```bash
test -f build/v1.6-face-drafts/akari-v1.6-fullbody-base-r1.png
test -f build/v1.6-face-drafts/akari-v1.6-fullbody-pin-side-3q-a1.png
test -f build/v1.6-face-drafts/akari-v1.6-fullbody-unpinned-side-3q-a2.png
sha256sum \
  build/v1.6-face-drafts/akari-v1.6-fullbody-base-r1.png \
  build/v1.6-face-drafts/akari-v1.6-fullbody-pin-side-3q-a1.png \
  build/v1.6-face-drafts/akari-v1.6-fullbody-unpinned-side-3q-a2.png
git status --short --branch
```

Expected: all three files exist; SHA-256 emits one digest per file; the plan
and design commits are present without unrelated tracked changes.

- [ ] **Step 2: Open all three image authorities before generation**

Use `view_image` at original detail for each input. Keep all three visible in
the conversation context and state their roles:

- front r1: body, outfit, scale, rendering, and framing authority;
- pin-side 3/4 A1: pin-side bob tightening and side construction;
- unpinned-side 3/4 A2: unpinned rear volume and cheek-lock continuity.

Expected: the three images are readable, consistent, and not replaced by an
earlier candidate.

- [ ] **Step 3: Generate the first straight-back candidate**

Use built-in `image_gen` with all three local paths supplied as referenced
images and the following prompt:

```text
Use case: identity-preserve
Asset type: Akari v1.6 canonical straight-back full-body reference.

Input images:
- Image 1 is the PRIMARY authority for the approved petite adult body,
  outfit, scale, rendering, full-body framing and standing logic.
- Image 2 supports ONLY pin-side bob construction, the slight pin-side
  tightening, and side-view continuity.
- Image 3 supports ONLY unpinned-side rear volume, cheek-lock continuity, and
  side-view continuity.

Primary request:
Generate one new exact straight-back full-body view of the same approved
Akari v1.6 design. Rotate the complete character to face directly away from
the viewer. This is a rear construction reference, not a new pose, outfit,
expression, rear three-quarter view, or turnaround sheet.

Body and pose:
- Preserve the 152 cm concept, approximately 6.6-head petite 25-year-old adult
  proportions, small gently sloped shoulders, compact ribcage, subtle waist,
  slim base, and modest healthy softness at hips and upper thighs.
- Anatomical right leg bears the weight. Anatomical left leg rests a small
  half-step forward and slightly to its own side.
- Keep knees, lower legs, ankles and shoes separated with visible background
  space. No crossed, pigeon-toed, catwalk, or rigid turnaround stance.
- Let both arms hang naturally so the back construction remains visible.
  Preserve exactly one smartwatch on the anatomical-left wrist.

Rear hair:
- Compact, normally rounded Honey Brown bob with crown flow, broad authored
  highlights, selective internal lines and a gentle inward nape.
- Anatomical-left pin side is only slightly tighter behind the ear and into
  the nape. Anatomical-right unpinned side remains slightly fuller without a
  new long rear strand.
- Show only the outer tips of exactly two short, equal-length, parallel pale
  ice-blue pins at the anatomical-left outer silhouette. Do not relocate the
  pins onto the back of the head.

Rear outfit:
- Ivory matte cotton-jersey cropped box T-shirt, simple back neckline and
  shoulder seams, short wide sleeves, restrained folds, and rear hem almost
  level with the front.
- Only a narrow strip of lower-back skin above the high waistband.
- Mist-blue soft matte culotte shorts, natural high waist, mid-thigh, modest
  A-line, two separate leg openings, shallow fine gathers across the rear
  elastic section, and no rear pockets.
- No belt loops, drawstring, fly emphasis, tailoring crease, logo, print,
  jewelry, bag, or extra accessory.
- Low ivory ankle socks and the same rounded ivory low-top sneakers with thin
  practical soles and restrained mist-blue heel accents.

Composition and finish:
- Vertical complete full body, centered, same scale and generous margins as
  Image 1. Show all hair, both hands, both socks, both shoes and the faint
  contact shadow.
- Warm off-white seamless background with no room or floor line.
- Match the approved warm anime rendering, clean line hierarchy and matte
  practical materials.

Avoid:
No face visibility, head turn, rear three-quarter view, twisted neck or torso,
body redesign, age drift, child/chibi body, model elongation, exaggerated
curves, crossed or overlapping legs/shoes, hidden or malformed hands, missing
watch, watch on the wrong wrist, prominent full pins on the back of the head,
rear pockets, glossy fabric, new ornament, text, labels, border, watermark,
grain, noise or busy background.
```

Expected: one generated PNG with a reported source path under
`/home/takahiro/.codex/generated_images/`.

- [ ] **Step 4: Save the candidate non-destructively and verify its format**

Use the exact absolute PNG path reported by the generation tool as the source
of a normal file copy. Do not delete or move that generated source. Use this
exact destination:

```text
build/v1.6-face-drafts/akari-v1.6-fullbody-back-a1.png
```

Then run:

```bash
identify build/v1.6-face-drafts/akari-v1.6-fullbody-back-a1.png
sha256sum build/v1.6-face-drafts/akari-v1.6-fullbody-back-a1.png
```

Expected: a valid PNG, a complete full-body portrait image, and one SHA-256
digest. Use the source path returned by the tool; do not infer a filename.

- [ ] **Step 5: Inspect the candidate against every hard invariant**

Open `akari-v1.6-fullbody-back-a1.png` at original detail and check:

1. exact straight-back head and torso direction;
2. consistent petite adult scale and body proportions;
3. compact rounded bob, slight anatomical-left tightening, and fuller
   anatomical-right side;
4. only two pin tips at anatomical left;
5. nearly level T-shirt hem and narrow lower-back skin gap;
6. shallow fine rear elastic gathers and no rear pockets;
7. one smartwatch on anatomical left;
8. coherent hands, legs, socks and shoes;
9. separated legs and shoes;
10. matching background, contact shadow and rendering.

Expected: record either `PASS` or one concise list of hard invariant failures.
Do not request a correction for harmless pixel or fold differences.

- [ ] **Step 6: Build and inspect the four-view comparison**

Run:

```bash
magick montage \
  -label 'Pin-side 3/4' \
  build/v1.6-face-drafts/akari-v1.6-fullbody-pin-side-3q-a1.png \
  -label 'Front r1' \
  build/v1.6-face-drafts/akari-v1.6-fullbody-base-r1.png \
  -label 'Unpinned 3/4 A2' \
  build/v1.6-face-drafts/akari-v1.6-fullbody-unpinned-side-3q-a2.png \
  -label 'Back A1' \
  build/v1.6-face-drafts/akari-v1.6-fullbody-back-a1.png \
  -thumbnail 420x900 -tile 4x1 -geometry +16+26 \
  -background '#f7f1ec' -fill '#59463d' -pointsize 22 \
  build/v1.6-face-drafts/akari-v1.6-fullbody-four-view-check-a1.png
```

Open the comparison with `view_image` at original detail.

Expected: all four views read as one character with consistent body scale,
shoulder width, waist, hip/thigh volume, garment length, and footwear.

- [ ] **Step 7: Apply at most one targeted correction if required**

If Step 5 or Step 6 finds a hard failure, open A1 and the strongest applicable
approved authority again, then run one built-in `image_gen` precise edit. The
prompt must name only the failed regions, list every approved region as an
invariant, and forbid global restyling. Save the result as
`akari-v1.6-fullbody-back-a2.png`, rebuild the montage as
`akari-v1.6-fullbody-four-view-check-a2.png`, and repeat the same checks once.

Expected: either A1 passes, A2 passes, or the attempt stops at the user gate
with the remaining failure stated plainly. Do not run a third attempt.

- [ ] **Step 8: Return to the user decision gate**

Present the latest four-view comparison and summarize:

- what passes;
- any remaining deviation;
- the recommended choice.

Ask the user to choose one of: accept the back view, request one explicitly
described design change, or stop without promotion.

Expected: no generated PNG is promoted into a tracked release location or
manifest before explicit user acceptance.

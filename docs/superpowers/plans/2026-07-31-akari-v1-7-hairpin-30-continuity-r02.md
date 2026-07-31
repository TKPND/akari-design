# Akari v1.7 Hairpin-Side 30-Degree Continuity r02 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review three independent r02 hairpin-side 30-degree
candidates while preserving the accepted V17-01 body volume and standing pose
that drifted in r01.

**Architecture:** Supply only the accepted v1.7 front PNG to image generation.
Describe the change as a horizontal camera orbit around the unchanged moment,
then run one immutable r02 prompt three times serially. Keep r01 and r02
  evidence separate in the ignored review directory, validate and inspect every
  PNG, build an equal-display-scale comparison, and return to the user for
  selection.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick
`identify` and `magick montage`, `xxd`, SHA-256, Git read-only checks, and the
repository rollout-payload recovery procedure.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-continuity-r02-design.md`.
- Execute in the existing isolated checkout
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-30-continuity`
  after the controller fast-forwards that worktree branch to the committed r02
  design and plan.
- Before any generation call, read and follow the local `imagegen` skill.
- Supply only
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png` to image
  generation.
- The sole generation input must have SHA-256
  `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`.
- Open the v1.5 B3, v1.4 G2, inherited hairpin-side 45-degree image, and r01 A
  for human QA only. Never include them in `referenced_image_paths`.
- Treat r01 A only as negative evidence for prohibited bust, waist, hip, and
  weight-shift drift. Do not edit, composite, or use any part of it as a
  positive authority.
- Generate r02 A, B, and C independently with the exact same prompt,
  reference, and target view. Never chain candidates or add
  candidate-specific deltas.
- Generate serially. Do not overlap image-generation or comparison work.
- Preserve the accepted identity, age 25, quietly pleased expression, hair,
  ornament, underlying body volume, garment ease, standing pose, bare feet,
  apartment light, framing, and hand-painted finish while changing only the
  camera viewpoint.
- Keep all output under ignored `build/v1.7-hairpin-30-continuity/` and do not
  overwrite or delete r01 evidence.
- Do not modify accepted assets, references, v1.6 material, manifests,
  validators, rendering code, audit code, or release packages.
- Do not promote a candidate or create an accepted angle asset before the
  user's explicit selection.
- If no r02 candidate passes, stop at a design decision. Do not generate r03
  or run an automatic correction loop.
- Do not run Python tests, Node tests, PDF builds, OCR, release gates, or
  package validation.

---

### Task 1: Generate and review V17-02 r02 A/B/C

**Files:**

- Read:
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-continuity-r02-design.md`
- Read and supply to image generation:
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`
- Inspect for human QA only:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
- Inspect for human QA only:
  `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
- Inspect for human QA only:
  `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png`
- Inspect as negative human QA evidence only:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png`
- Create:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png`
- Create:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-b.png`
- Create:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-c.png`
- Create:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-comparison.png`

**Interfaces:**

- Consumes: one hash-pinned accepted v1.7 front authority, three hash-pinned
  positive human-QA references, and one hash-pinned negative r01 example.
- Produces: three independent ignored r02 PNG candidates, one ignored
  comparison, and a review report; no tracked accepted asset or commit.

- [ ] **Step 1: Verify checkout, sources, tools, output boundary, and Git state**

Run:

```bash
test "$(pwd -P)" = \
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-30-continuity"
test -f \
  docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-continuity-r02-design.md
test -f \
  docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-30-continuity-r02.md
mkdir -p build/v1.7-hairpin-30-continuity
if [ ! -f \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png \
]; then
  cp \
    /home/takahiro/.codex/generated_images/019fb844-c2df-7ba3-bcc9-c17d3f224e2f/exec-c4eaeea1-3c84-4bf5-9c62-8c454306c09a.png \
    build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png
fi
cmp --silent \
  /home/takahiro/.codex/generated_images/019fb844-c2df-7ba3-bcc9-c17d3f224e2f/exec-c4eaeea1-3c84-4bf5-9c62-8c454306c09a.png \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png
test "$(sha256sum \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  | cut -d ' ' -f 1)" = \
  "64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8"
test "$(sha256sum \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  | cut -d ' ' -f 1)" = \
  "e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734"
test "$(sha256sum \
  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png \
  | cut -d ' ' -f 1)" = \
  "6757e601d2cfd158c970ab701a876981ace837e669c313dec6d25c0c539ff4d6"
test "$(sha256sum \
  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png \
  | cut -d ' ' -f 1)" = \
  "ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21"
test "$(sha256sum \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png \
  | cut -d ' ' -f 1)" = \
  "2ad81bc807701ae8fe9dc643a4dbe670f87058f10ec559d92b5b0a40c961a1fa"
identify -format '%f | %m %wx%h\n' \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png \
  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png
command -v magick
command -v identify
command -v sha256sum
command -v xxd
git check-ignore -v build/v1.7-hairpin-30-continuity/probe.png
git status --short --branch
git diff --quiet
git diff --cached --quiet
```

Expected: execution is in the named isolated checkout with both committed r02
documents; r01 A exists and is byte-identical to its recorded generation
source; all five hashes match; all images are readable; required tools resolve;
`build/` is ignored; the tracked tree is clean.

- [ ] **Step 2: Open and state every reference role**

Use `view_image` with original detail for the accepted v1.7 front, all three
positive human-QA images, and r01 A. State immediately before generation:

- accepted V17-01 front is the sole generation input and controls all current
  character and presentation attributes;
- v1.5 B3 checks inherited head-to-body ratio, restrained upper-body volume,
  healthy thighs, and quiet full-body balance after generation;
- v1.4 G2 checks line hierarchy, paint planes, adult-face direction, palette,
  and finish after generation;
- inherited hairpin-side 45 degrees checks only cheek, bob, and ornament
  perspective topology after generation;
- r01 A is negative evidence only for added bust projection, pinched waist,
  stronger hip contour, and one-leg weight bias that must not recur.

Keep all five images visible in conversation context. Pass only the accepted
front path to image generation.

- [ ] **Step 3: Generate candidate A from the immutable r02 prompt**

Use built-in `image_gen` with exactly one referenced image path:

```text
/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-30-continuity/akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png
```

Use this complete prompt byte-for-byte for A, B, and C:

```text
Use case: identity-preserving novel-view continuity.
Asset: Akari v1.7 V17-02 hairpin-side 30-degree continuity probe, r02.

Image 1 is the sole visual authority. Preserve the exact same adult woman,
age 25, identity, face, expression, hair, ornament, body proportions, standing
pose, clothing, bare feet, apartment setting, framing, palette, line work,
paint planes, and hand-painted finish. Change only the camera viewpoint.

Create one full-resolution 1024 x 1536 portrait image of the same instant from
a camera horizontally orbited exactly 30 degrees from the source front
position toward Akari's own left, her hairpin side, which is on image-right in
Image 1. Akari remains in the same three-dimensional standing pose. Do not
turn, twist, or re-pose her to manufacture the angle.

The face, neckline, shoulder line, T-shirt and ribcage perspective, shorts
waistband and pelvis, knees, and feet must all agree with this one camera
position. Her character-left cheek and the complete pale-blue ornament are
nearer the camera and more visible. Keep both amber eyes visible; only the
eyes track the lens naturally. Do not leave the body near-front while turning
the head, and do not turn the head farther than the torso.

Preserve Image 1's exact underlying body volume, garment ease, and quiet
near-even balance. Keep the white T-shirt hanging with the same relaxed
looseness and keep the pale-blue lounge shorts at the same fit. Preserve the
same base of support, relaxed shoulders, naturally hanging arms, softly
unlocked knees, and nearly even weight across both planted feet. Do not
beautify or enhance the body contour: no added chest projection, waist
pinching, stronger bust-to-waist or waist-to-hip contrast, lateral hip shift,
one-leg weight bearing, or S-curve. Do not symmetrize or "correct" the source
pose. Allow only the modest overlap and foreshortening physically caused by
the 30-degree camera position; keep both hands, both legs, and both feet
complete and anatomically connected.

Preserve the accepted adult face construction, soft cheek volume, compact
chin, restrained blush, low-contrast amber eyes, and small closed-mouth smile:
quietly pleased after noticing a familiar viewer. Preserve the short airy
chestnut bob, asymmetric looseness, irregular tips, natural skull volume, and
low-gloss paint planes. Preserve exactly one complete character-left
ornament: two pale-blue crossed pins above a delicate thin cord bow with
narrow loops and two slim tails, attached to the same side in correct
perspective.

Preserve the warm minimal apartment, directional domestic light, full-body
scale and breathing room, quiet warm palette, deliberate outer lines,
restrained interior lines, readable paint planes, and hand-painted finish.
Keep the complete figure in frame from hair to toes.

Avoid a mirrored or wrong-side view, near-front body with a separate head
turn, 45-degree or profile view, contrapposto, walking or crossed-leg pose,
fashion-model or pin-up posture, body reshaping, identity or age drift,
stronger smile, blush, makeup or glamour, enlarged eyes, salon-smooth glossy
hair, altered or incomplete ornament, changed clothing or accessories,
cropping, wide-angle distortion, photorealism, plastic smoothing, text,
borders, logos, or watermarks.
```

Record the returned generation or request identifier and exact source path.
Do not generate B until A is saved and verified.

- [ ] **Step 4: Save and verify candidate A**

Copy the exact returned source PNG without transformation to:

```text
build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png
```

Do not move or delete the generation source. Run:

```bash
candidate_a_source='/absolute/path/returned/by/imagegen'
cmp --silent "$candidate_a_source" \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png
test "$(sha256sum "$candidate_a_source" | cut -d ' ' -f 1)" = \
  "$(sha256sum \
    build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png \
    | cut -d ' ' -f 1)"
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png)" = \
  "PNG 1024x1536"
sha256sum \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png
```

Expected: destination byte identity and SHA-256 match the returned source;
signature and exact `PNG 1024x1536` assertion pass; one digest is recorded.

If the image appears in conversation without a local source PNG, parse the
current-day rollout JSONL structurally. Extract the intended
`image_generation_call` item whose `result` begins with `iVBOR`, decode it,
verify its PNG signature, and record its generation or request identifier.
Never hand-copy base64 from terminal output.

- [ ] **Step 5: Generate and verify candidate B independently**

Call `image_gen` again with only the accepted front and the Step 3 prompt,
byte-for-byte unchanged. Do not reference A or add a B-specific instruction.
Save without transformation to:

```text
build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-b.png
```

Repeat Step 4's source/destination `cmp`, matching source/destination SHA-256,
signature, exact `PNG 1024x1536` assertion, source-path, and generation-ID
checks for B. Use a task-specific `candidate_b_source` variable. Do not
generate C until B is saved and verified.

- [ ] **Step 6: Generate and verify candidate C independently**

Call `image_gen` a third time with only the accepted front and exact Step 3
prompt. Do not reference A or B or add a C-specific instruction. Save without
transformation to:

```text
build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-c.png
```

Repeat Step 4's complete verification for C using a task-specific
`candidate_c_source` variable. Do not start another generation after C.

- [ ] **Step 7: Inspect each r02 candidate at original detail**

Open A, B, and C separately with `view_image` at original detail. Record
pass/fail in the r02 design's order:

1. same-person identity and age-25 impression;
2. coherent character-left hairpin-side 30-degree whole-body view;
3. restrained bust, subtle waist, unchanged hip and thigh volume, and no
   glamour increase;
4. level shoulders and pelvis, nearly even weight, planted feet, and no
   contrapposto or S-curve;
5. complete ornament topology and believable airy bob volume;
6. accepted quietly pleased expression, eye treatment, and facial restraint;
7. anatomy, clothing, framing, environment, palette, finish, artifacts, and
   absence of v1.6 drift.

Reject any identity, view, body-volume, stance, ornament, anatomy, or artifact
failure. Record all visible findings even after a hard failure.

- [ ] **Step 8: Build and inspect the labeled r02 comparison**

Run:

```bash
magick montage \
  \( akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
     -set label 'Front / Accepted' \) \
  \( build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png \
     -set label 'r02 A' \) \
  \( build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-b.png \
     -set label 'r02 B' \) \
  \( build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-c.png \
     -set label 'r02 C' \) \
  -tile 2x2 \
  -geometry 720x1080+24+72 \
  -background '#eee8df' \
  -fill '#4d463f' \
  -pointsize 32 \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-comparison.png
identify -format '%f | %m %wx%h\n' \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-comparison.png
sha256sum \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-comparison.png
```

Expected: one readable 2-by-2 PNG with full uncropped figures, clear labels,
equal display scale, and one recorded digest. Preserve any scale drift as
review evidence rather than normalizing it away.

Open the comparison at original detail and repeat all seven hard-gate checks.

- [ ] **Step 9: Return to the explicit user selection gate**

Summarize generation IDs, source paths, dimensions, SHA-256 values, hard-gate
verdicts, the strongest passing candidate if any, Minor findings, and all
review paths. Show the comparison and any candidate needing full-size review.

Ask the user to select a passing candidate, keep only the accepted front, or
return to design. Do not promote, commit, repair, generate r03, or clean up
r01/r02 evidence in this task.

Run:

```bash
git status --short --branch
git diff --quiet
git diff --cached --quiet
git check-ignore -v \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-b.png \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-c.png \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-comparison.png
```

Expected: both tracked diff assertions pass; all review output is ignored; r01
evidence remains intact. This image-review task intentionally creates no
tracked commit.

# Akari v1.7 Hairpin-Side 45-Degree Continuity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review three independent Akari v1.7 hairpin-side
45-degree candidates from the accepted 30-degree and front checkpoints without
changing the accepted character, moment, stance, or presentation.

**Architecture:** Supply the accepted hairpin-side 30-degree PNG first as the
same-moment camera-orbit authority and the accepted front PNG second as the
identity, body-volume, expression, and finish correction authority. Run one
immutable prompt three times serially with no sibling chaining, preserve every
returned PNG byte-for-byte under ignored review output, inspect all candidates
and one five-image comparison, then stop at the explicit user-selection gate.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick
`identify` and `magick montage`, `xxd`, SHA-256, Git read-only checks, and the
repository rollout-payload recovery procedure.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-45-continuity-design.md`.
- At execution time, use `superpowers:using-git-worktrees` to create the
  isolated checkout
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity`
  on branch `codex/akari-v1-7-hairpin-45-continuity` from the commit containing
  this plan.
- Before the first generation call, read and follow the local `imagegen` skill.
- Supply exactly two images to every generation call in this order:
  `akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`, then
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`.
- The accepted 30-degree input must have SHA-256
  `22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749`.
- The accepted front input must have SHA-256
  `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`.
- Image 1 controls the same-moment world-space arrangement, same-side camera
  direction, view-dependent hairpin-side face and skull construction,
  perspective continuity, and ornament ordering. Image 2 controls identity,
  age, underlying face and body design, expression restraint, clothing design,
  palette, and finish whenever the accepted inputs differ.
- Open the v1.5 B3, v1.4 G2, inherited v1.1 hairpin-side 45-degree image, and
  accepted v1.2 C03 hairpin-side 45-degree image for human QA only. Never add
  them to `referenced_image_paths`.
- Generate A, B, and C independently with the exact same prompt, ordered input
  array, and target view. Never chain candidates or add candidate-specific
  instructions.
- The immutable prompt block, including its final newline, must have SHA-256
  `761267fa3b64f916ad3bf0ec2ee57aedd28b0c0480a5eeff7b5874c1455ea6c7`.
- Generate serially. Save and verify one returned source before beginning the
  next call. Do not overlap image-generation or comparison work.
- Change only camera azimuth: advance another 15 degrees from the accepted
  30-degree view to exactly 45 degrees toward Akari's character-left,
  hairpin side.
- Preserve camera height, elevation, orbit radius, subject distance, focal
  perspective, pitch, roll, portrait crop, and character scale.
- Preserve the same fixed instant: body segment arrangement, arms, hands,
  fingers, hair locks, ornament, garment state, feet, room geometry, light,
  and shadow state may change only through camera parallax and visibility.
- Preserve the accepted age-25 identity, quietly pleased closed-mouth
  expression, complete crossed-pin and cord-bow ornament, body volume, garment
  ease, near-even stance, bare feet, warm apartment, palette, line hierarchy,
  paint planes, and hand-painted finish.
- Do not compound V17-02's slight near-side bust/waist emphasis or its slightly
  stronger eye and facial polish.
- Keep all generated and comparison output under ignored
  `build/v1.7-hairpin-45-continuity/`.
- Do not modify accepted assets, human-QA references, V17-01 or V17-02 review
  evidence, v1.6 material, manifests, validators, rendering code, audit code,
  release packages, or PDFs.
- Do not promote a candidate, create an accepted 45-degree asset, or update
  durable selection history before the user's explicit selection.
- If no candidate passes, preserve all r01 evidence and stop at a new design
  decision. Do not generate r02, repair, composite, or relax the angle.
- Do not run Node tests, Python tests, PDF builds, OCR, package validation,
  integration gates, or release gates.
- Do not push, merge, clean up the execution worktree, or synchronize remotes
  in this image-review task.

---

### Task 1: Generate and review V17-03 r01 A/B/C

**Files:**

- Read:
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-45-continuity-design.md`
- Read:
  `docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-45-continuity.md`
- Read and supply first to image generation:
  `akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`
- Read and supply second to image generation:
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`
- Inspect for human QA only:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
- Inspect for human QA only:
  `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
- Inspect for human QA only:
  `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png`
- Inspect for human QA only:
  `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png`
- Create:
  `build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png`
- Create:
  `build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png`
- Create:
  `build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png`
- Create:
  `build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-comparison.png`

**Interfaces:**

- Consumes: two ordered, hash-pinned accepted v1.7 generation inputs and four
  hash-pinned human-QA-only references.
- Produces: three independent ignored 45-degree PNG candidates, one ignored
  comparison, exact generation provenance and visual verdicts in the task
  report, and an explicit user-selection gate; no tracked accepted asset or
  implementation commit.

#### Immutable Generation Prompt

Use this complete prompt byte-for-byte for A, B, and C:

```text
Use case: identity-preserve
Asset: Akari v1.7 V17-03 hairpin-side 45-degree continuity probe, r01.

Image 1 is the accepted V17-02 hairpin-side 30-degree checkpoint. It is the
primary authority for the same fixed moment, world-space arrangement,
same-side camera-orbit direction, view-dependent hairpin-side face and skull
construction, face-to-feet perspective continuity, and complete ornament
ordering. Image 2 is the accepted V17-01 intimate front checkpoint. It is the
correction authority for the exact adult woman, age 25, identity, underlying
face and body design, restrained expression, clothing, palette, line work,
paint planes, and hand-painted finish.

If the accepted inputs differ, Image 1 wins for the same-moment world-space
arrangement, camera direction, view-dependent hairpin-side face and skull
construction, perspective continuity, and ornament ordering. Image 2 wins for
underlying identity, face and body design, age, expression restraint, clothing
design, palette, and finish. Do not average or reverse these roles.

Create one full-resolution 1024 x 1536 portrait image of the same instant from
a camera horizontally orbited another 15 degrees in the same direction as
Image 1, reaching exactly 45 degrees from the front position toward Akari's
own left, her hairpin side. Akari remains fixed in the same three-dimensional
standing state. Change only camera azimuth. Keep camera height, elevation,
orbit radius, subject distance, focal perspective, pitch, roll, portrait crop,
and character scale unchanged.

Preserve Image 1's world-space head, neck, shoulders, ribcage, pelvis, knees,
ankles, feet, relaxed arms, elbows, wrists, hands, fingers, hair locks,
ornament attachment, garment state, planted-foot base, room geometry, light
source, and quiet shadow state. Allow only the overlap, foreshortening, and
visibility changes physically caused by moving the camera. Do not turn, twist,
re-pose, restyle, reset, or stage Akari again.

The face, neckline, shoulder line, T-shirt and ribcage, shorts waistband and
pelvis, knees, ankles, and feet must all agree with one coherent hairpin-side
45-degree camera position. Her character-left cheek and complete pale-blue
ornament are nearer the camera. Only her amber eyes track the lens naturally;
do not turn her head back toward front. Both eyes may remain visible with
physically credible far-eye narrowing. Do not enlarge the far eye or flatten
the face toward a near-front view.

Use Image 2 to preserve the accepted adult age-25 face construction, soft cheek
volume, compact chin, restrained blush, subtle lip color, low-contrast amber
eyes, quiet lash and brow treatment, and the small closed-mouth smile of
becoming quietly pleased after noticing a familiar viewer. Do not increase the
eye contrast or facial polish found as a Minor in Image 1. Preserve the short
airy chestnut bob, asymmetric looseness, irregular tips, natural skull volume,
and low-gloss paint planes.

Preserve exactly one complete character-left ornament: two pale-blue crossed
pins above a delicate thin cord bow with narrow loops and two slim tails. Keep
the same attachment point and correct 45-degree perspective. Do not mirror,
move, duplicate, simplify, replace, or invent any ornament part.

Use Image 2's underlying body volume as the correction authority: keep the
same head-to-body ratio, restrained bust, subtle waist, stable pelvis and hip
volume, healthy thighs, limb lengths, adult hands and feet, relaxed T-shirt
ease, and pale-blue lounge-short fit. Do not copy or increase Image 1's slight
near-side bust and waist emphasis. Do not add chest projection, bust
separation, waist pinching, hip flare, stronger bust-to-waist or waist-to-hip
contrast, leg elongation, or glamour shaping.

Preserve the same quiet near-even standing balance. Keep shoulders and pelvis
level, spine quiet and near vertical, knees softly unlocked, both soles
planted, torso centered over the same base, and weight distributed nearly
evenly. A greater near/far foot offset and limb overlap are valid only as
45-degree parallax. Do not add one-leg loading, lateral hip shift,
contrapposto, an S-curve, walking, crossed legs, or a fashion-model or pin-up
pose. Keep both hands, both legs, and both bare feet complete and anatomically
connected in frame.

Preserve the white T-shirt, pale-blue lounge shorts, bare feet, warm minimal
apartment, wall, level baseboard and floor, directional domestic light,
full-body scale, breathing room, quiet warm palette, deliberate outer lines,
restrained interior lines, readable paint planes, and hand-painted finish.
Keep the complete figure in frame from hair to toes.

Reject a near-30-degree substitute, profile or near-profile view, mirrored or
opposite-side view, independently turned head, mismatched upper- and lower-body
angles, changed camera height or distance, wide-angle distortion, pitch,
camera roll, changed figure scale, a second-take pose, shifted feet, restyled
hair, reset clothing, moved room, changed light setup, identity or age drift,
stronger smile, blush, makeup or glamour, enlarged or polished eyes,
salon-smooth glossy hair, altered ornament, changed clothing or accessories,
cropping, white studio background, photorealism, plastic smoothing, generic
character-sheet polish, v1.6 signals, text, labels, borders, logos, or
watermarks.
```

- [ ] **Step 1: Verify checkout, sources, tools, output boundary, and Git state**

Run:

```bash
test "$(pwd -P)" = \
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity"
git cat-file -e \
  HEAD:docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-45-continuity-design.md
git cat-file -e \
  HEAD:docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-45-continuity.md
test "$(awk '
  /^#### Immutable Generation Prompt$/ { section = 1; next }
  section && /^```text$/ { inside = 1; next }
  inside && /^```$/ { exit }
  inside { print }
' docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-45-continuity.md \
  | sha256sum | cut -d ' ' -f 1)" = \
  "761267fa3b64f916ad3bf0ec2ee57aedd28b0c0480a5eeff7b5874c1455ea6c7"
mkdir -p build/v1.7-hairpin-45-continuity
mkdir -p build/v1.7-hairpin-45-continuity/recovered
test ! -e \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png
test ! -e \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png
test ! -e \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png
test ! -e \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-comparison.png
sha256sum -c <<'EOF'
22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png
e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png
6757e601d2cfd158c970ab701a876981ace837e669c313dec6d25c0c539ff4d6  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png
ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png
19c8c96113bcbc47f7d1e4cc1d58af466d3a573f0dae40cfcdf9bf456b1a0a9b  akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
EOF
identify -format '%f | %m %wx%h\n' \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png \
  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png \
  akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
command -v magick
command -v identify
command -v sha256sum
command -v xxd
git check-ignore -v build/v1.7-hairpin-45-continuity/probe.png
git diff --quiet
git diff --cached --quiet
git status --short --branch
```

Expected: execution is in the named isolated checkout at a commit containing
the approved design and this plan; no r01 output exists to overwrite; all six
hashes match; all inputs are readable; required tools resolve; `build/` is
ignored; tracked and staged diffs are empty.

If an r01 output already exists, do not overwrite it or continue automatically.
Inspect its provenance, signature, dimensions, hash, and task state first, then
resume only from the first incomplete verified step.

- [ ] **Step 2: Open and state every reference role**

Use `view_image` with original detail for all six inputs. Immediately before
generation, state:

- accepted V17-02 30 degrees is Image 1 and controls the same fixed moment,
  world-space arrangement, same-side orbit direction, perspective continuity,
  and ornament ordering;
- accepted V17-01 front is Image 2 and corrects identity, age, underlying body
  volume, restrained expression, clothing, palette, and finish without pulling
  the target back toward front;
- v1.5 B3 checks head-to-body ratio, restrained upper-body volume, subtle
  waist, healthy thighs, and quiet full-body balance after generation;
- v1.4 G2 checks adult-face direction, line hierarchy, paint planes, quiet
  palette, and finish after generation;
- inherited v1.1 hairpin-side 45 degrees checks only cheek width, bob
  silhouette, and ornament perspective ordering after generation;
- accepted v1.2 C03 hairpin-side 45 degrees checks only coherent 45-degree
  alignment through head, ribcage, pelvis, knees, and feet after generation.

Keep all six images visible in conversation context. Pass only Image 1 and
Image 2 to generation, in that order. Never pass a human-QA-only image.

- [ ] **Step 3: Generate candidate A from the immutable prompt**

Use built-in `image_gen` with exactly these `referenced_image_paths`, in this
order:

```text
/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity/akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity/akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png
```

Use the `Immutable Generation Prompt` block exactly as written. Record the
returned generation or request identifier and exact returned source path. Do
not generate B until A is saved and source-verified.

- [ ] **Step 4: Save and verify candidate A byte-for-byte**

In the shell session, bind `candidate_a_source` to the exact absolute PNG path
returned by the completed A call, then run:

```bash
: "${candidate_a_source:?candidate_a_source must be the exact returned A PNG}"
test -f "$candidate_a_source"
cp "$candidate_a_source" \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png
cmp --silent "$candidate_a_source" \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png
test "$(sha256sum "$candidate_a_source" | cut -d ' ' -f 1)" = \
  "$(sha256sum \
    build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png \
    | cut -d ' ' -f 1)"
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png)" = \
  "PNG 1024x1536"
sha256sum \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png
git check-ignore -v \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png
```

Expected: the saved A is byte-identical to its returned source, has matching
source and destination SHA-256 values, valid PNG signature, exact
`PNG 1024x1536` format and dimensions, one recorded digest, and ignored status.

If the completed call displays an image without a local PNG path, follow the
project's `画像生成payload救出` procedure: search the current-day rollout JSONL
for `image_generation_call`, structurally parse the JSONL, and select the exact
A call by its recorded generation or request identifier, not by prompt text
alone. Decode its `iVBOR` result to
`build/v1.7-hairpin-45-continuity/recovered/akari-v1.7-v17-03-hairpin-45-r01-a-source.png`,
verify signature `89504e470d0a1a0a`, and bind `candidate_a_source` to that
recovered source. Never decode directly over the final candidate path or
hand-copy base64 from the terminal.

- [ ] **Step 5: Generate, save, and verify candidate B independently**

Call `image_gen` a second time with the exact ordered two-path array from Step
3 and the exact `Immutable Generation Prompt`. Do not reference A or add a
B-specific instruction. Record B's generation identifier and exact returned
source path. In the shell session, bind `candidate_b_source` to that path, then
run:

```bash
: "${candidate_b_source:?candidate_b_source must be the exact returned B PNG}"
test -f "$candidate_b_source"
cp "$candidate_b_source" \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png
cmp --silent "$candidate_b_source" \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png
test "$(sha256sum "$candidate_b_source" | cut -d ' ' -f 1)" = \
  "$(sha256sum \
    build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png \
    | cut -d ' ' -f 1)"
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png)" = \
  "PNG 1024x1536"
sha256sum \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png
git check-ignore -v \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png
```

Expected: B passes the same byte-identity, source-hash, signature, dimensions,
digest-recording, and ignored-output checks as A. Do not begin C until B is
saved and verified. If the tool exposes no local source path, correlate the
rollout payload with B's recorded generation or request identifier, decode it
to
`build/v1.7-hairpin-45-continuity/recovered/akari-v1.7-v17-03-hairpin-45-r01-b-source.png`,
verify its PNG signature, bind `candidate_b_source` to that recovered source,
and then run the B copy and `cmp` checks above.

- [ ] **Step 6: Generate, save, and verify candidate C independently**

Call `image_gen` a third time with the exact ordered two-path array from Step 3
and the exact `Immutable Generation Prompt`. Do not reference A or B or add a
C-specific instruction. Record C's generation identifier and exact returned
source path. In the shell session, bind `candidate_c_source` to that path, then
run:

```bash
: "${candidate_c_source:?candidate_c_source must be the exact returned C PNG}"
test -f "$candidate_c_source"
cp "$candidate_c_source" \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png
cmp --silent "$candidate_c_source" \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png
test "$(sha256sum "$candidate_c_source" | cut -d ' ' -f 1)" = \
  "$(sha256sum \
    build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png \
    | cut -d ' ' -f 1)"
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png)" = \
  "PNG 1024x1536"
sha256sum \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png
git check-ignore -v \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png
```

Expected: C passes the same byte-identity, source-hash, signature, dimensions,
digest-recording, and ignored-output checks as A and B. Do not start a fourth
generation or a correction call. If the tool exposes no local source path,
correlate the rollout payload with C's recorded generation or request
identifier, decode it to
`build/v1.7-hairpin-45-continuity/recovered/akari-v1.7-v17-03-hairpin-45-r01-c-source.png`,
verify its PNG signature, bind `candidate_c_source` to that recovered source,
and then run the C copy and `cmp` checks above.

- [ ] **Step 7: Inspect every candidate at original detail**

Open A, B, and C separately with `view_image` at original detail. Record a
full verdict for every candidate in this order:

1. same-person identity, adult age-25 impression, and accepted quietly pleased
   emotional beat;
2. the same fixed instant in hair, ornament, arms, hands, garment state, feet,
   room geometry, light, and shadows;
3. correct character-left hairpin side, unchanged camera height, distance,
   focal perspective, pitch, roll and scale, and coherent exact 45-degree
   alignment from face through feet;
4. unchanged bust, waist, hip, thigh, garment, and head-to-body volume without
   compounding either accepted V17-02 Minor;
5. level shoulders and pelvis, nearly even weight, planted feet, quiet spine,
   and perspective parallax without contrapposto or a new pose;
6. complete ornament topology, believable cheek width, and airy bob volume;
7. intact anatomy, clothing, full-body framing, level background, light,
   palette, line hierarchy, paint planes, and absence of artifacts or v1.6
   drift.

Reject immediately for any identity, adult-age, accepted-expression,
same-moment, view, camera, body-volume, stance, ornament, anatomy,
presentation, or artifact failure. Record all visible findings even after a
hard failure. Do not use surface polish to rescue a hard-gate failure.

- [ ] **Step 8: Build and inspect the labeled five-image comparison**

Run:

```bash
magick montage \
  \( akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
     -set label 'Front / accepted' \) \
  \( akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png \
     -set label '30 deg / accepted' \) \
  \( build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png \
     -set label '45 deg / r01 A' \) \
  \( build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png \
     -set label '45 deg / r01 B' \) \
  \( build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png \
     -set label '45 deg / r01 C' \) \
  -tile 5x1 \
  -geometry 480x720+18+64 \
  -background '#eee8df' \
  -fill '#4d463f' \
  -pointsize 24 \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-comparison.png
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-comparison.png)" = \
  "89504e470d0a1a0a"
identify -format '%f | %m %wx%h\n' \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-comparison.png
sha256sum \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-comparison.png
git check-ignore -v \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-comparison.png
```

Expected: one readable five-column PNG with complete, uncropped figures,
clear labels, identical source-frame scaling, and one recorded digest. The
locked camera distance and character scale should make valid candidates read
at equal character height. Preserve any figure-scale drift as review evidence;
do not individually normalize a failing candidate to hide it.

Open the comparison with `view_image` at original detail. Read it left to right
as `Front → 30° → A/B/C`, then repeat all seven hard-gate checks. Use the
full-size candidate views for face, ornament, hands, feet, and artifact calls.

- [ ] **Step 9: Obtain an independent verdict and return to user selection**

Before recommending a candidate, have a reviewer who did not generate the
images apply the exact seven hard gates to all source PNGs and the comparison.
If the executor and reviewer disagree about whether a candidate passes a hard
gate, obtain one blind candidate-specific tie-break against the approved design
before presenting it as selectable.

Summarize for the user:

- A, B, and C generation identifiers and exact returned source paths;
- source/destination byte-identity results;
- each candidate's dimensions and SHA-256;
- all seven hard-gate verdicts and every Minor finding;
- which candidates are eligible for selection, if any;
- the candidate with the strongest same-person read, intimate eye contact,
  character appeal, and finished image quality among hard-gate passers;
- full paths to the comparison and each candidate.

Show the comparison and any candidate needing full-size review. Ask the user to
select a passing A, B, or C, keep only the existing front and 30-degree
checkpoints, or return to design. Do not promote, commit, repair, composite,
generate r02, or clean up review evidence in this task.

Run:

```bash
git diff --quiet
git diff --cached --quiet
git check-ignore -v \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-a.png \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-b.png \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-c.png \
  build/v1.7-hairpin-45-continuity/akari-v1.7-v17-03-hairpin-45-r01-comparison.png
git status --short --branch
```

Expected: both tracked-diff assertions pass, all review output is ignored, and
the execution branch remains tracked-clean. This image-review task
intentionally creates no tracked implementation commit.

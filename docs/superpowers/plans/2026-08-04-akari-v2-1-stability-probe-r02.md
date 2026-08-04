# Akari v2.1 Stability Probe r02 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and audit one corrected noncanonical 30-degree hairpin-side
probe that cleanly tests Candidate C's selected eye geometry without the head
roll and round-eye regression found in r01.

**Architecture:** Preserve r01 as immutable negative evidence, then create a
separate ignored `stability-r02` run with one hash-pinned prompt and exactly one
built-in image-generation call. Generate cleanly from Candidate C and the two
accepted v2.0 supporting authorities, preserve the returned PNG byte-for-byte,
apply six Candidate-C-relative review gates, and stop for explicit user
direction regardless of verdict.

**Tech Stack:** Markdown run ledgers, built-in `image_gen`, local `view_image`,
ImageMagick `identify`, `xxd`, SHA-256, `cmp`, the existing Node rollout-payload
recovery helper, Git ignore checks, and markdownlint-cli2.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-08-04-akari-v2-1-stability-probe-r02-design.md`.
- Execute in the existing checkout `/home/takahiro/workspace/akari-design`; do
  not create or switch to another worktree.
- Before the generation call, read and follow the current `imagegen` skill.
- Candidate C at
  `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png`, SHA-256
  `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73`,
  remains the primary current identity authority byte-for-byte.
- The accepted v2.0 face at
  `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png`, SHA-256
  `34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe`,
  supports only same-person lineage, familiar warmth, hairline logic, and the
  18-year-old read.
- The accepted v2.0 full body at
  `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png`, SHA-256
  `03e7effc6dd13dadb4f1ec394b84ffe8ed9d218e500f0aefa49ebf2b5f0b6d94`,
  supports only laterality, shoulder-crop clothing, compact proportion cues,
  and the rendering family.
- The rejected r01 probe, SHA-256
  `f48b078c23ca33bf1953f6a87d792332cbb38d44dbf368cd9b268d599046807b`,
  is negative review evidence only. Never include it in
  `referenced_image_paths`, edit it, composite from it, or use it as a positive
  identity, angle, or rendering authority.
- Open the three generation references with `view_image` at original detail
  immediately before generation and state their independent roles.
- Make exactly one built-in image-generation call with those three paths and no
  recent-conversation image injection.
- Target one shoulder-up portrait near 1024-by-1536 scale from a horizontal
  approximately 30-degree camera view toward Akari's character-left hairpin
  side, with level head, eye line, and shoulders and no added roll or pitch.
- Preserve Candidate C's low, nearly straight central upper-lid language,
  restrained vertical opening, smooth nearer-eye outer lid, compact chin, and
  softly finished lower face in correct perspective.
- Keep the prompt, ledgers, generated PNG, and review under ignored
  `tmp/akari-v2.1-redesign/stability-r02/` and do not stage them.
- Preserve `tmp/akari-v2-uniform-batch/` byte-for-byte. Its recorded digest is
  `4ac76bd19c478edaf11cf122ed41a35e0658fdf796731d49dcddb323b11382cc`.
- Do not retry, regenerate, retouch, crop, resize, recompress, composite,
  promote, continue to Stage 2, or create package, manifest, release, or PDF
  artifacts.
- Whether r02 passes or fails, show the exact probe, report all six gates, and
  stop for explicit user direction.

---

### Task 1: Pin the r02 run and correction prompt

**Files:**

- Read:
  `docs/superpowers/specs/2026-08-04-akari-v2-1-stability-probe-r02-design.md`
- Modify: `tmp/akari-v2.1-redesign/stability-r01/RUN.md`
- Modify: `tmp/akari-v2.1-redesign/stability-r01/REVIEW.md`
- Create: `tmp/akari-v2.1-redesign/stability-r02/RUN.md`
- Create:
  `tmp/akari-v2.1-redesign/stability-r02/prompts/akari-v2.1-stability-30-r02.md`
- Reuse: `tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs`

**Interfaces:**

- Consumes: the approved r02 design, the explicit user instructions
  `r02に進めよう` and `OK`, three immutable generation authorities, the rejected
  r01 review, and the preserved v2.0 batch digest.
- Produces: an immutable r02 correction boundary, one complete hash-pinned
  prompt, and a preflight ledger consumed by Task 2.

- [ ] **Step 1: Verify the checkout, authorities, rejected probe, and batch**

Run:

```bash
test "$(pwd -P)" = "/home/takahiro/workspace/akari-design"
test -f \
  docs/superpowers/specs/2026-08-04-akari-v2-1-stability-probe-r02-design.md
test -f \
  docs/superpowers/plans/2026-08-04-akari-v2-1-stability-probe-r02.md
sha256sum \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
  akari-v2.0/accepted/base/akari-v2.0-front-face-master.png \
  akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png \
  tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
  akari-v2.0/accepted/base/akari-v2.0-front-face-master.png \
  akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png \
  tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
find tmp/akari-v2-uniform-batch -type f -print0 | sort -z | \
  xargs -0 sha256sum | sha256sum
command -v identify
command -v sha256sum
command -v xxd
command -v cmp
bash -lc 'command -v node; node --version'
git status --short --branch
git diff --quiet
git diff --cached --quiet
```

Expected: all four hashes match the Global Constraints and r01 records; all
four images are readable with their recorded dimensions; the batch digest is
`4ac76bd19c478edaf11cf122ed41a35e0658fdf796731d49dcddb323b11382cc`;
all required tools resolve; tracked and staged trees are clean; the pre-existing
user-owned untracked v2.0 uniform-batch plan remains untouched.

- [ ] **Step 2: Append the bounded r02 continuation to the r01 ledgers**

Use `apply_patch` to append a short `r02 continuation` subsection to both r01
ledgers. Record all of the following facts verbatim in meaning:

- the r01 verdict remains `FAIL` and is not retroactively changed;
- the user explicitly instructed `r02に進めよう` and approved the written r02
  design with `OK` on 2026-08-04;
- the only authorized continuation is one corrected Stage 1.5 probe under
  `../stability-r02/`;
- r01 remains negative review evidence and is not a generation input;
- no r03, Stage 2, promotion, package, manifest, release, or PDF work is
  authorized.

- [ ] **Step 3: Create the r02 prompt exactly**

Use `apply_patch` to create
`tmp/akari-v2.1-redesign/stability-r02/prompts/akari-v2.1-stability-30-r02.md`
with the Markdown title
`# Akari v2.1 30-Degree Stability Probe Prompt — r02`, followed by this complete
prompt body:

```text
Use case: stylized-concept.
Asset: Akari v2.1 noncanonical 30-degree hairpin-side stability probe, r02.

Reference roles:
Image 1 is the PRIMARY current identity authority: the user-selected Akari
v2.1 Candidate C. Preserve this exact same late-teen young woman, age 18,
same-person face, selected low horizontally emphasized eye construction,
friendly small open smile, brow placement, eye spacing, soft cheek character,
compact softly rounded chin, warm chestnut hair, off-center V bangs,
character-left crossed hairpin and low side ponytail, warm palette, soft anime
linework, restrained cel shading, and finished presentation.

Image 2 is the accepted v2.0 face and close-view supporting authority. Use it
only to protect same-person lineage, original hairline and silhouette logic,
familiar warmth, and the 18-year-old read. It must not override Image 1's
selected v2.1 eye geometry, lower-face refinement, bang grouping, or quieter
rendering. In particular, do not regress toward Image 2's rounder eye family.

Image 3 is the accepted v2.0 body, outfit, laterality, and full-figure
supporting authority. Use it only to confirm character-left hairpin and
ponytail placement, the white crew-neck top at the shoulder crop, compact
healthy proportion cues, and the same rendering family. Do not widen this
portrait into a full-body composition.

Primary request:
Create one full-resolution portrait near 1024 x 1536 of the same Akari and the
same emotional moment as Image 1 from one coherent camera view approximately
30 degrees toward Akari's own left, her hairpin side. Move the virtual camera
horizontally from the strict-front position toward the ornament side that is
on image-right in the front references. Her character-left cheek, complete
crossed hairpin, and low character-left ponytail are nearer the camera and
clearly visible. This is a true modest three-quarter camera view, not a
mirrored image, not a near-front substitute, and not an independently turned,
rolled, pitched, or tilted head.

Level-view lock:
Keep the head upright and the eye line and shoulders level relative to the
canvas. Use pure horizontal yaw only: no head roll, no camera roll, no tilted
eye line, no raised near-side shoulder, and no upward or downward head pitch.
The face, neck, shoulders, shirt neckline, and camera viewpoint must agree as
one level 30-degree view.

Selected eye-geometry lock:
Candidate C in Image 1 controls both eyes. Preserve medium-width almond eyes
with low restrained vertical opening. Through the central portion of each
upper lid, keep a low, gently sloped, nearly straight segment that softens only
toward the outer end. Never replace that segment with a high semicircular,
dome-shaped, or round upper-lid arch.

Perspective may make the farther eye horizontally narrower, but do not
compensate by opening it vertically, rounding its aperture, exposing more
iris, enlarging the iris, or raising the upper-lid apex. It must remain a
foreshortened version of Candidate C's selected almond construction, not a
rounder v2.0 or generic anime eye. Keep the nearer upper lid smooth and softly
tapered; do not add a sharp outer spur, hook, lash cluster, drooping corner, or
eyeliner-like point.

Keep both honey-amber eyes visible and naturally tracking the camera. Preserve
medium iris scale, deeper brown rims, subtle pupils, one small principal
highlight per eye, understated lower lids, and compatible binocular gaze.
Keep the iris naturally occluded by the lids rather than fully circular and
floating. Do not use wet gloss, overloaded sparkle, multiple bright
catchlights, heavy lower lashes, or unequal focus.

Identity and lower-face locks:
Keep the exact same approachable 18-year-old young-adult read: naturally cute,
fresh, familiar, and neither childlike nor mid-20s. Preserve Image 1's brow
placement, eye spacing, soft cheeks, small natural nose, friendly small open
smile, compact chin, jaw-to-neck connection, and warm skin treatment in
correct perspective. Do not narrow, lengthen, or sharpen the lower face. Keep
the chin compact and softly rounded rather than pointier than Image 1. Do not
increase glamour, blush, makeup, lip detail, or idol polish.

Hair and laterality locks:
Preserve warm chestnut or cocoa-brown hair, the off-center V-bang structure
with two or three primary groups, restrained crown volume, low-gloss shine,
and restrained internal strand detail. Preserve exactly one complete pale
muted-blue crossed hairpin on character-left in natural 30-degree perspective.
Never mirror, move, duplicate, uncross, merge, simplify, or replace it.
Preserve one connected low side ponytail on character-left, attached behind
the near-side head with natural overlap and light movement at the tips. Do not
hide it completely, detach it, duplicate it, or move it to character-right.

Composition and rendering locks:
Use a shoulder-up portrait crop with direct familiar gaze, relaxed level
shoulders, complete hair silhouette, comfortable margins, and the same plain
warm off-white background as Image 1. Preserve soft anime linework, warm skin,
restrained cel shading, pale muted-blue accents, honey-amber eyes, and bright
but non-neon color. Keep every visible connection coherent: both eyes, brows,
ears as naturally visible, hairline, jaw, neck, shoulders, hairpin, and
ponytail.

Avoid:
No head roll, eye-line roll, shoulder roll, rounder farther eye, vertically
expanded farther eye, sharp nearer-eye outer spur, wrong-side or mirrored view,
exact front, near-front substitute,
45-degree or profile view, separate head turn, hidden or far-side hairpin,
missing ponytail, new person, child face, mid-20s face, sharp V jaw, long or
narrow lower face, oversized round irises, drooping outer corners, heavy
lashes, eyeliner, wet gloss, overloaded sparkle, orange-red hair, neon-blue
hairpin, glossy plastic hair, dense strand noise, fashion styling, glamour,
photorealism, crop through the hair or chin, malformed anatomy, duplicated
feature, seam, border, text, logo, or watermark.
```

Do not add r01 as an image reference. Its documented failure modes are already
expressed as text-only negative constraints.

- [ ] **Step 4: Hash the exact prompt**

Run:

```bash
sha256sum \
  tmp/akari-v2.1-redesign/stability-r02/prompts/akari-v2.1-stability-30-r02.md
```

Expected: one SHA-256 is returned. Preserve it exactly for the preflight ledger
and completed-generation provenance comparison.

- [ ] **Step 5: Create and validate the r02 preflight ledger**

Use `apply_patch` to create
`tmp/akari-v2.1-redesign/stability-r02/RUN.md`. Record:

- status `preflight; not generated`;
- approved design and implementation-plan paths;
- both explicit user instructions and date;
- all three authority paths, roles, dimensions, and hashes;
- rejected r01 path, hash, and negative-evidence-only role;
- prompt path and the SHA-256 computed in Step 4;
- target output
  `images/akari-v2.1-stability-30-r02.png`;
- one-call, no-retry, no-retouch, no-promotion, and stop boundaries;
- preserved v2.0 batch digest.

Run:

```bash
bash -lc './node_modules/.bin/markdownlint-cli2 \
  :tmp/akari-v2.1-redesign/stability-r01/RUN.md \
  :tmp/akari-v2.1-redesign/stability-r01/REVIEW.md \
  :tmp/akari-v2.1-redesign/stability-r02/RUN.md \
  :tmp/akari-v2.1-redesign/stability-r02/prompts/akari-v2.1-stability-30-r02.md \
  --no-globs'
git check-ignore -v \
  tmp/akari-v2.1-redesign/stability-r01/RUN.md \
  tmp/akari-v2.1-redesign/stability-r02/RUN.md \
  tmp/akari-v2.1-redesign/stability-r02/prompts/akari-v2.1-stability-30-r02.md
```

Expected: one prompt hash is copied into `RUN.md`; markdownlint reports four
linted files and zero issues; every ledger and prompt is ignored.

### Task 2: Generate and preserve the single r02 probe

**Files:**

- Read:
  `tmp/akari-v2.1-redesign/stability-r02/prompts/akari-v2.1-stability-30-r02.md`
- Create:
  `tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png`
- Modify: `tmp/akari-v2.1-redesign/stability-r02/RUN.md`

**Interfaces:**

- Consumes: one exact prompt and the three immutable reference paths pinned by
  Task 1.
- Produces: one exact first-call PNG plus its request IDs, source provenance,
  dimensions, signature, hash, and original-detail inspection record for
  Task 3.

- [ ] **Step 1: Reverify and open all generation references**

Re-run the three authority `sha256sum` checks from Task 1. Then use `view_image`
with `detail: original` on Candidate C, the v2.0 face master, and the v2.0 full
body. State immediately before generation:

1. Candidate C is the primary current identity authority and controls the
   selected eye construction, expression, face geometry, hair, palette,
   linework, and finish.
2. The v2.0 face supports only same-person lineage, familiar warmth, hairline
   logic, and the 18-year-old read; it must not override Candidate C's eyes.
3. The v2.0 full body supports only laterality, shoulder-crop clothing, compact
   proportion cues, and rendering family.

Keep all three images visible in conversation context. Do not open the rejected
r01 probe in the same immediate pre-generation reference set.

- [ ] **Step 2: Make exactly one built-in generation call**

Call built-in `image_gen` once with the complete prompt from Task 1 and exactly
these `referenced_image_paths`:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-face-master.png
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
```

Omit `num_last_images_to_include`. Do not include A, B, r01 probe, any v1 image,
or any v2.0 batch image. Record the outer request ID, completed generation or
call ID, tool-provided source path, and any completed-event revised prompt.
Never make a second generation call in this run.

- [ ] **Step 3: Preserve the exact returned PNG without transformation**

Create the destination directory, then copy the readable tool-provided source
with `cp --no-clobber` to:

```text
tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png
```

Use the literal source path returned by the tool as the copy source. Do not move
or delete the generated source. Run `cmp --silent` between that literal source
and the destination.

If and only if the tool displays the image but no readable source PNG exists,
run the existing recovery helper through `bash -lc` with the literal completed
call ID, the exact destination above, and the current Asia/Tokyo session day in
`YYYY/MM/DD` form:

```text
tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs
```

The helper must structurally parse current-day rollouts, match the exact call
ID, require one unique `iVBOR` payload, verify PNG signature
`89504e470d0a1a0a`, and refuse overwrite. If recovery fails, record
`technical failure` and stop without another image-generation call.

- [ ] **Step 4: Verify and inspect the exact saved output**

Run:

```bash
file \
  tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png
sha256sum \
  tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png
```

Expected: one readable non-empty RGB portrait PNG near 1024-by-1536, signature
`89504e470d0a1a0a`, and one recorded SHA-256. Confirm source-to-destination byte
identity with `cmp`. Use `view_image` at original detail on the saved output and
Candidate C. If the ignored workspace path fails to render while the
byte-identical generated source renders, inspect the source and record the
renderer discrepancy without altering the PNG.

- [ ] **Step 5: Complete the generation ledger**

Update `RUN.md` with `apply_patch`. Record the exact source path, outer request
ID, completed call ID, call count, prompt and revised-prompt hashes when
available, save method, recovery use or non-use, dimensions, channels, PNG
signature, SHA-256, `cmp` result, and original-detail inspection result. Set the
status to `generated once; preserved; awaiting six-gate review`.

### Task 3: Audit r02 and stop at the result gate

**Files:**

- Create: `tmp/akari-v2.1-redesign/stability-r02/REVIEW.md`
- Modify: `tmp/akari-v2.1-redesign/stability-r02/RUN.md`

**Interfaces:**

- Consumes: the exact first-call r02 PNG, Candidate C, both v2.0 supporting
  authorities, the rejected r01 negative evidence, and the approved r02 design.
- Produces: one evidence-backed `PASS` or `FAIL`, concrete residual findings,
  and an explicit stop for user direction; no canonical asset or tracked
  promotion.

- [ ] **Step 1: Open the complete review set at original detail**

Use `view_image` with `detail: original` on:

1. Candidate C as the positive identity and eye-geometry authority;
2. the exact r02 probe as the review target;
3. the v2.0 face for supporting lineage and age only;
4. the v2.0 full body for supporting laterality and rendering only;
5. the rejected r01 probe as negative evidence for round-eye drift, outer-lid
   spur, pointier chin, and head or eye-line roll only.

Do not treat r01 as a positive target. Keep Candidate C and r02 visible together
for every eye-shape conclusion.

- [ ] **Step 2: Apply all six Candidate-C-relative gates**

Create `REVIEW.md` and record one `Pass` or `Fail` plus concrete visual evidence
for each gate:

1. same-person face read against selected Candidate C;
2. both eyes preserve Candidate C's low, nearly straight central upper-lid
   language, restrained opening, medium iris scale, restrained highlights, and
   compatible gaze after reasonable perspective foreshortening;
3. head, eye line, and shoulders remain level in one coherent approximately
   30-degree character-left hairpin-side camera view, with no roll, pitch,
   mirror, near-front substitute, or independent head turn;
4. hairline, V bangs, pale muted-blue crossed hairpin, attached low ponytail,
   and character-left laterality remain coherent;
5. approachable 18-year-old young-adult read, soft cheeks, compact softly
   rounded chin, and non-glamorous presentation remain stable;
6. no malformed geometry, disconnection, duplication, seam, border, crop,
   text, logo, watermark, or material-rendering artifact is present.

For Gate 2, normal horizontal near/far foreshortening is allowed. Fail if the
farther eye becomes dome-shaped or vertically compensated, the nearer eye gains
a sharp outer spur, either eye regresses toward the rounder v2.0 family, or head
roll makes the comparison ambiguous. Do not pass the gate merely because the
eyes are attractive, coherent, amber, or non-glossy.

The final verdict is `PASS` only if all six gates pass. When evidence remains
visually disputed, record `FAIL`; do not choose a least-bad result. List every
residual Minor for a passing result and every failed gate and stop reason for a
failing result.

- [ ] **Step 3: Record the noncanonical boundary and final status**

State in both `REVIEW.md` and `RUN.md` that r02 is ignored evidence only and is
not a v2.1 authority or promotion candidate. Set `RUN.md` to
`reviewed; PASS; awaiting explicit probe approval` or
`reviewed; FAIL; stopped before Stage 2`. Record that no retry, r03, Stage 2,
face promotion, package, manifest, release, or PDF work occurred.

- [ ] **Step 4: Run the final verification set**

Run serially:

```bash
bash -lc './node_modules/.bin/markdownlint-cli2 \
  :tmp/akari-v2.1-redesign/stability-r01/RUN.md \
  :tmp/akari-v2.1-redesign/stability-r01/REVIEW.md \
  :tmp/akari-v2.1-redesign/stability-r02/RUN.md \
  :tmp/akari-v2.1-redesign/stability-r02/REVIEW.md \
  :tmp/akari-v2.1-redesign/stability-r02/prompts/akari-v2.1-stability-30-r02.md \
  --no-globs'
bash -lc 'npm run lint:md'
find tmp/akari-v2-uniform-batch -type f -print0 | sort -z | \
  xargs -0 sha256sum | sha256sum
git check-ignore -v \
  tmp/akari-v2.1-redesign/stability-r02/RUN.md \
  tmp/akari-v2.1-redesign/stability-r02/REVIEW.md \
  tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png
git status --short -- tmp/akari-v2.1-redesign
git diff --check
git diff --quiet
git diff --cached --quiet
git status --short --branch
```

Expected: five local Markdown files are linted with zero issues; tracked
Markdown lint passes; the preserved batch digest remains
`4ac76bd19c478edaf11cf122ed41a35e0658fdf796731d49dcddb323b11382cc`;
all r02 artifacts are ignored; tracked and staged trees are clean after this
plan's commit; the pre-existing user-owned untracked v2.0 plan remains untouched.

- [ ] **Step 5: Show r02 and enforce the stop**

Show:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png
```

Report the six-gate verdict and every residual Minor or failure. Stop for
explicit approval or rejection. Do not infer approval from a `PASS` verdict and
do not continue to Stage 2 automatically.

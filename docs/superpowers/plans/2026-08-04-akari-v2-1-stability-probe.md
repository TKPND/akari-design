# Akari v2.1 30-Degree Stability Probe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix user-selected Candidate C as the byte-identical working v2.1 face authority, generate one noncanonical 30-degree hairpin-side portrait, review identity stability, and stop at the explicit probe-result gate.

**Architecture:** Preserve Stage 1 review history while appending the explicit C selection and Stage 1.5 authorization to its ignored ledgers. Build a separate ignored `stability-r01` run with one pinned prompt, exactly one built-in image-generation call, exact-output preservation, and a six-gate review. The probe is evidence only; no promotion, correction round, Stage 2 generation, or package work is included.

**Tech Stack:** Markdown run ledgers, built-in `image_gen`, `view_image`, ImageMagick `identify`, `xxd`, `sha256sum`, `cmp`, Git ignore checks, markdownlint-cli2.

## Global Constraints

- Candidate C at `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png`, SHA-256 `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73`, is the selected working v2.1 face authority byte-for-byte.
- The v2.0 face authority remains `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png`, SHA-256 `34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe`.
- The v2.0 body, outfit, laterality, and full-figure authority remains `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png`, SHA-256 `03e7effc6dd13dadb4f1ec394b84ffe8ed9d218e500f0aefa49ebf2b5f0b6d94`.
- Open all three references with `view_image` at original detail immediately before generation and state their independent roles.
- Make exactly one built-in image-generation call with those three paths and no recent-conversation image injection.
- The target is one approximately 30-degree view toward Akari's character-left hairpin side at approximately 1024-by-1536 portrait scale.
- Do not regenerate, retouch, composite, crop, resize, recompress, promote, or use a failed probe to continue.
- Keep the probe, prompt, ledgers, and recovery evidence under ignored `tmp/akari-v2.1-redesign/stability-r01/`.
- Preserve `tmp/akari-v2-uniform-batch/` byte-for-byte and do not stage ignored artifacts.
- Whether the probe passes or fails, show the result and stop for explicit user direction before Stage 2.

---

### Task 1: Record the selected authority and pin the probe run

**Files:**

- Modify: `tmp/akari-v2.1-redesign/r01/RUN.md`
- Modify: `tmp/akari-v2.1-redesign/r01/REVIEW.md`
- Create: `tmp/akari-v2.1-redesign/stability-r01/RUN.md`
- Create: `tmp/akari-v2.1-redesign/stability-r01/prompts/akari-v2.1-stability-30-r01.md`
- Reuse: `tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs`

**Interfaces:**

- Consumes: the user's explicit Candidate C selection and subsequent Stage 1.5 authorization on 2026-08-04.
- Produces: an immutable selected-face record, a preflight ledger, and one hashed full prompt consumed by Task 2.

- [ ] **Step 1: Reverify the immutable inputs and preserved batch**

Run:

```bash
sha256sum \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
  akari-v2.0/accepted/base/akari-v2.0-front-face-master.png \
  akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
  akari-v2.0/accepted/base/akari-v2.0-front-face-master.png \
  akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
find tmp/akari-v2-uniform-batch -type f -print0 | sort -z | \
  xargs -0 sha256sum | sha256sum
```

Expected: all three hashes match Global Constraints, all files are readable RGB PNGs, and the batch digest is `4ac76bd19c478edaf11cf122ed41a35e0658fdf796731d49dcddb323b11382cc`.

- [ ] **Step 2: Append the explicit decisions without rewriting Stage 1 review evidence**

Use `apply_patch` to:

- change the Stage 1 `RUN.md` status to `Candidate C explicitly selected; Stage 1.5 explicitly authorized`;
- add a dated selection section naming C, its source path, dimensions, and hash;
- append a post-review decision section to `REVIEW.md` stating that the historical review itself selected nothing, the user subsequently selected C, C is now the byte-identical working v2.1 face authority, and it has not been promoted or retouched;
- record that the later instruction `進んで良いわよ` authorizes only the Stage 1.5 probe defined by the approved design.

- [ ] **Step 3: Create the Stage 1.5 ledger and exact prompt**

Create the run directory and record this full prompt verbatim at the named prompt path:

```text
Use case: identity-preserving novel-view character continuity generation.
Asset: Akari v2.1 noncanonical 30-degree hairpin-side stability probe, r01.

Reference roles:
Image 1 is the PRIMARY current identity authority: the user-selected Akari
v2.1 Candidate C. Preserve this exact same late-teen young woman, age 18,
same-person face, redesigned eye geometry, friendly small open smile, brow and
eye spacing, soft cheek character, compact chin, warm chestnut hair, off-center
V bangs, character-left crossed hairpin and low side ponytail, warm palette,
soft anime linework, restrained cel shading, and finished presentation.

Image 2 is the accepted v2.0 face and close-view identity authority. Use it only
to protect same-person lineage, original hairline and silhouette logic, familiar
warmth, and the 18-year-old read. It must not override Image 1's selected v2.1
eye redesign, lower-face refinement, bang grouping, or quieter rendering.

Image 3 is the accepted v2.0 body, outfit, laterality, and full-figure authority.
Use it only to confirm character-left hairpin and ponytail placement, the white
crew-neck top at the shoulder crop, compact healthy proportion cues, and the
same rendering family. Do not widen this portrait into a full-body composition.

Primary request:
Create one full-resolution portrait at approximately 1024 x 1536 of the same
Akari and same emotional moment as Image 1 from a coherent camera view about 30
degrees toward Akari's own left, her hairpin side. The virtual camera has moved
horizontally from the strict-front position toward the ornament side that is on
image-right in the front references. Her character-left cheek, complete crossed
hairpin, and low character-left ponytail are nearer the camera and clearly
visible. This is a true modest three-quarter camera view, not a mirrored image,
not a near-front substitute, and not an independently turned head.

Identity and expression locks:
- Keep the exact same 18-year-old young-adult read: naturally cute, fresh,
  familiar, and approachable; neither childlike nor mid-20s.
- Preserve Image 1's soft compact face and friendly small open smile without
  increasing glamour, blush, makeup, lip detail, or idol polish.
- Keep both honey-amber eyes visible and naturally tracking the camera. Preserve
  the selected medium-width almond geometry, restrained vertical opening,
  medium iris scale, deeper brown rim, subtle pupil, one small principal
  highlight, understated lower lid, and compatible binocular gaze.
- Preserve brow placement, eye spacing, cheek character, nose language, compact
  chin, jaw-to-neck connection, and warm skin treatment in correct perspective.

Hair and laterality locks:
- Preserve the warm chestnut or cocoa-brown hair, off-center V-bang structure
  with two or three primary groups, slightly quiet crown volume, low-gloss shine,
  and restrained internal strand detail.
- Preserve exactly one complete pale muted-blue crossed hairpin on
  character-left in natural 30-degree perspective. Never mirror, move,
  duplicate, uncross, merge, simplify, or replace it.
- Preserve one connected low side ponytail on character-left, attached behind
  the near-side head with natural overlap and light movement at the tips. Do not
  hide it completely, detach it, duplicate it, or move it to character-right.

Composition and rendering locks:
- Shoulder-up portrait crop, level head, direct familiar gaze, relaxed level
  shoulders, complete hair silhouette, comfortable margins, and the same plain
  warm off-white background as Image 1.
- Preserve soft anime linework, warm skin, restrained cel shading, pale muted
  blue accents, warm honey-amber eyes, and bright but non-neon color.
- Keep all visible anatomy and connections coherent: both eyes, brows, ears as
  naturally visible, hairline, jaw, neck, shoulders, hairpin, and ponytail.

Avoid:
No wrong-side or mirrored view, exact front, near-front substitute, 45-degree or
profile view, separate head turn, hidden or far-side hairpin, missing ponytail,
new person, child face, mid-20s face, sharp V jaw, long lower face, enlarged or
rounder eyes, drooping outer corners, heavy lashes, eyeliner, wet gloss,
overloaded sparkle, multiple bright catchlights, orange-red hair, neon-blue
hairpin, glossy plastic hair, dense strand noise, fashion styling, glamour,
photorealism, crop through the hair or chin, malformed anatomy, duplicated
feature, seam, border, text, logo, or watermark.
```

In `RUN.md`, record the approved design path, selected C path/hash, both v2.0 reference roles/hashes, preserved batch digest, one-call/no-retry rule, output path, and status `preflight; not generated`.

- [ ] **Step 4: Verify the pinned records**

Run:

```bash
sha256sum \
  tmp/akari-v2.1-redesign/stability-r01/prompts/akari-v2.1-stability-30-r01.md
./node_modules/.bin/markdownlint-cli2 \
  tmp/akari-v2.1-redesign/r01/RUN.md \
  tmp/akari-v2.1-redesign/r01/REVIEW.md \
  tmp/akari-v2.1-redesign/stability-r01/RUN.md \
  tmp/akari-v2.1-redesign/stability-r01/prompts/akari-v2.1-stability-30-r01.md
git check-ignore -v \
  tmp/akari-v2.1-redesign/r01/RUN.md \
  tmp/akari-v2.1-redesign/stability-r01/RUN.md
```

Expected: one prompt hash is recorded, lint passes, and both ledgers are ignored.

### Task 2: Generate and preserve the single stability probe

**Files:**

- Read: `tmp/akari-v2.1-redesign/stability-r01/prompts/akari-v2.1-stability-30-r01.md`
- Create: `tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png`
- Modify: `tmp/akari-v2.1-redesign/stability-r01/RUN.md`

**Interfaces:**

- Consumes: the exact prompt and three immutable reference paths from Task 1.
- Produces: one exact first-call PNG plus its request IDs, source provenance, dimensions, signature, hash, and original-detail inspection record.

- [ ] **Step 1: Open all identity-sensitive references at original detail**

Use `view_image` with `detail: original` on Candidate C, the v2.0 front-face master, and the v2.0 front full-body. State their three roles exactly as recorded in the prompt and keep them visible in conversation context.

- [ ] **Step 2: Make exactly one built-in generation call**

Call built-in `image_gen` once with the complete prompt from Task 1 and exactly these local paths:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-face-master.png
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
```

Do not include A, B, v1 images, v2.0 batch images, or recent conversation images. Record the outer request ID and completed call/generation ID.

- [ ] **Step 3: Preserve the exact returned PNG without transformation**

Copy the readable tool-provided source without overwriting to:

```text
tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
```

Run `cmp --silent` between source and destination. If the local source is absent, invoke `recover-image-payload.mjs` with the literal completed call ID, destination, and actual session day. Recovery must parse the matching current-day rollout structurally, require an `iVBOR` payload and PNG signature `89504e470d0a1a0a`, reject ambiguity, and refuse overwrite. If recovery fails, record `technical failure` and stop without another call.

- [ ] **Step 4: Verify and inspect the exact saved output**

Run:

```bash
file tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
sha256sum \
  tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
```

Expected: one readable non-empty RGB portrait PNG near 1024x1536, signature `89504e470d0a1a0a`, and one SHA-256. Use `view_image` at original detail on the saved output and re-open Candidate C at original detail for the same-person comparison. Record all provenance and inspection facts in `RUN.md`; do not retouch or retry.

### Task 3: Review the probe and stop at the result gate

**Files:**

- Create: `tmp/akari-v2.1-redesign/stability-r01/REVIEW.md`
- Modify: `tmp/akari-v2.1-redesign/stability-r01/RUN.md`

**Interfaces:**

- Consumes: the exact first-call probe PNG, Candidate C, both v2.0 supporting authorities, and the approved design's Stage 1.5 test list.
- Produces: one evidence-backed `PASS` or `FAIL`, concrete residual Minors or failure reasons, and an explicit user-direction stop.

- [ ] **Step 1: Apply all six probe gates at original detail**

Record one `Pass` or `Fail` plus concrete evidence for each:

1. same-person face read against selected Candidate C;
2. stable selected eye shape, iris scale, highlight restraint, and compatible gaze;
3. coherent hairline, off-center V bangs, crossed hairpin, and attached low ponytail;
4. correct character-left hairpin-side 30-degree view and laterality, with no mirror or independent head turn;
5. preserved approachable 18-year-old young-adult read;
6. no malformed geometry, disconnection, duplication, seam, border, text, watermark, or material rendering artifact.

The final verdict is `PASS` only if all six pass. List concrete residual Minors for a passing result. For a failing result, name every failed gate and stop condition.

- [ ] **Step 2: Record the noncanonical boundary**

State that the probe is evidence only, remains ignored, and is not a v2.1 authority or promotion candidate. Update `RUN.md` to `reviewed; PASS; awaiting explicit probe approval` or `reviewed; FAIL; stopped before Stage 2`. State that no retry, Stage 2 generation, face promotion, package, manifest, or PDF work occurred.

- [ ] **Step 3: Run the final verification set**

Run:

```bash
./node_modules/.bin/markdownlint-cli2 \
  tmp/akari-v2.1-redesign/r01/RUN.md \
  tmp/akari-v2.1-redesign/r01/REVIEW.md \
  tmp/akari-v2.1-redesign/stability-r01/RUN.md \
  tmp/akari-v2.1-redesign/stability-r01/REVIEW.md \
  tmp/akari-v2.1-redesign/stability-r01/prompts/akari-v2.1-stability-30-r01.md
bash -lc 'npm run lint:md'
find tmp/akari-v2-uniform-batch -type f -print0 | sort -z | \
  xargs -0 sha256sum | sha256sum
git check-ignore -v \
  tmp/akari-v2.1-redesign/stability-r01/RUN.md \
  tmp/akari-v2.1-redesign/stability-r01/REVIEW.md \
  tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
git status --short -- tmp/akari-v2.1-redesign
git diff --check
git diff --quiet
git diff --cached --quiet
git status --short --branch
```

Expected: local records lint, tracked Markdown lint passes, the preserved batch digest is unchanged, all Stage 1.5 artifacts are ignored, the tracked and staged trees remain clean after the plan commit, and the pre-existing user-owned untracked v2.0 plan remains untouched.

- [ ] **Step 4: Show the probe and enforce the stop**

Show:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png
```

Report the six-gate verdict and residual Minors or failures. Stop for explicit approval or rejection. Do not infer approval from a passing review and do not continue to Stage 2 automatically.

# Akari v2.2 Cozy-Reach Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, preserve, review, and present exactly one noncanonical
Akari v2.2 cozy-reach prototype without changing a canonical image or silently
retrying a weak result.

**Architecture:** Freeze three ordered reference copies and one verbatim master
prompt in an ignored run directory. Make one built-in Imagegen call, preserve
its PNG byte-for-byte or recover the call-ID-bound rollout payload, then record
provenance and review the unchanged candidate against seven visual gates. The
workflow ends at user review; it has no promotion path.

**Tech Stack:** built-in `image_gen`, `view_image`, ImageMagick `identify`,
`sha256sum`, `xxd`, `stat`, `cmp`, `file`, Git scope checks,
`markdownlint-cli2`, and the existing structured Node payload-recovery helper.

## Global Constraints

- Implement the approved design in
  `docs/superpowers/specs/2026-08-07-akari-v2-2-cozy-reach-design.md`.
- Execute from `/home/takahiro/workspace/akari-design`; the approved absolute
  reference paths and ignored output root name this canonical checkout.
- Generate exactly one new image with exactly one built-in Imagegen call.
- Use the exact frozen master prompt and exactly three reference copies in the
  approved order. Omit `num_last_images_to_include`.
- Image 1 controls face, identity, apparent age, eyes, hair, one-piece hairpin,
  palette, and close rendering. Image 2 controls body balance, outfit, and
  laterality. Image 3 controls only sofa composition, reaching-hand
  foreshortening, viewer interaction, and warm domestic mood.
- Preserve the user-ratified 18-year-old young-adult read from the v2.0/v2.1
  lineage. Do not import the separate character-sheet batch's 25-year-old
  wording.
- Preserve exactly one filled blue capsule hairpin on
  character-left/canvas-right at approximately 45–60 degrees and 0.8–1.0
  visible eye width. One quiet dark edge is allowed only for legibility.
- Keep the canonical white T-shirt, blue denim skirt, and gray socks where
  visible. Do not import a sailor uniform, school bag, black hair, gray eyes,
  or the composition reference's person.
- Store every execution input, prompt, output, and ledger update under ignored
  `tmp/akari-v2.2-cozy-reach/r01/`.
- Do not overwrite, retry, regenerate, repair, composite, rank, promote, stage,
  commit, push, or publish any execution artifact.
- Present the single candidate even when a review gate fails. A weak or failed
  candidate is still the one authorized outcome.
- Preserve the pre-existing unrelated untracked
  `docs/superpowers/plans/2026-08-04-akari-v2-0-uniform-batch.md` unchanged.
- Use `bash -lc` for the Node recovery helper so the configured fnm Node path is
  available. Never print or hand-copy a PNG base64 payload.
- If a generated source path and an unambiguous call/request ID are both
  unavailable, perform the bounded structural rollout scan below. Stop as a
  technical failure if it does not identify exactly one completed PNG call.
- Tokens beginning `ACTUAL_` in Task 2 are runtime substitutions, not values to
  guess or execute literally. Each one is defined by the immediately preceding
  timestamp or Imagegen-result step and must be replaced with that recorded
  value.

## File Map

- Read only:
  `docs/superpowers/specs/2026-08-07-akari-v2-2-cozy-reach-design.md` — approved
  visual contract, prompt, review gates, and non-goals.
- Read only:
  `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp` — canonical
  face, hair, hairpin, and rendering authority.
- Read only:
  `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp` — canonical
  body, outfit, and laterality authority.
- Read only:
  `/home/takahiro/.codex/attachments/fa016a44-2698-4939-aaa5-607832e76ac7/HFfjnyCbQAA19tl.jpg`
  — composition and mood reference only.
- Create:
  `tmp/akari-v2.2-cozy-reach/r01/inputs/portrait-authority.webp` — byte-identical
  run copy of Image 1.
- Create:
  `tmp/akari-v2.2-cozy-reach/r01/inputs/fullbody-authority.webp` — byte-identical
  run copy of Image 2.
- Create:
  `tmp/akari-v2.2-cozy-reach/r01/inputs/composition-reference.jpg` —
  byte-identical run copy of Image 3.
- Create: `tmp/akari-v2.2-cozy-reach/r01/prompts/master.txt` — the sole prompt
  supplied to Imagegen.
- Create: `tmp/akari-v2.2-cozy-reach/r01/tools/recover-image-payload.mjs` —
  byte-identical run-local copy of the structured recovery helper.
- Create: `tmp/akari-v2.2-cozy-reach/r01/run.md` — immutable input facts,
  runtime provenance, seven-gate evidence, and final scope result.
- Create: `tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png`
  — the sole review candidate.

---

### Task 1: Freeze Inputs, Prompt, and Run Record

**Files:**

- Create: `tmp/akari-v2.2-cozy-reach/r01/inputs/portrait-authority.webp`
- Create: `tmp/akari-v2.2-cozy-reach/r01/inputs/fullbody-authority.webp`
- Create: `tmp/akari-v2.2-cozy-reach/r01/inputs/composition-reference.jpg`
- Create: `tmp/akari-v2.2-cozy-reach/r01/prompts/master.txt`
- Create: `tmp/akari-v2.2-cozy-reach/r01/tools/recover-image-payload.mjs`
- Create: `tmp/akari-v2.2-cozy-reach/r01/run.md`
- Verify: `docs/superpowers/specs/2026-08-07-akari-v2-2-cozy-reach-design.md`

**Interfaces:**

- Consumes: the three approved sources, their exact dimensions and SHA-256
  values, and the approved master prompt.
- Produces: three byte-identical run copies, one prompt with SHA-256
  `4eae9128b2fbcbf6dbf814e95f7f8bc2f1488be6744b386137c241cc035cf7cb`,
  one byte-identical run-local recovery helper, one initialized ledger, and one
  absent output path consumed by Task 2.

- [ ] **Step 1: Verify the clean tracked baseline and source identities**

Run:

```bash
git diff --quiet
git diff --cached --quiet
git status --short --branch
sha256sum \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp \
  /home/takahiro/.codex/attachments/fa016a44-2698-4939-aaa5-607832e76ac7/HFfjnyCbQAA19tl.jpg
identify -format '%f %m %wx%h %[colorspace]\n' \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp \
  /home/takahiro/.codex/attachments/fa016a44-2698-4939-aaa5-607832e76ac7/HFfjnyCbQAA19tl.jpg
sha256sum tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs
bash -lc 'command -v node; command -v npm; node --version; npm --version'
```

Expected:

- both Git diff commands exit `0`;
- the unrelated untracked v2.0 uniform plan may appear in status and remains
  untouched;
- portrait authority: WebP `1888x3344` sRGB, SHA-256
  `b076afd95be49c4ed9c5a4ddfb4083c9ead8328313b4d5fa0555a374dd10543c`;
- full-body authority: WebP `1888x3344` sRGB, SHA-256
  `d93307fe219de81c6fb501e9472725a0ad8f3d242a0ddc741bf53d156f8d7688`;
- composition reference: JPEG `1480x2184` sRGB, SHA-256
  `13523b51df5999a93ab934ecf563a4b7c5631e79d5c76583ed6ee028903db191`;
- recovery helper SHA-256:
  `ebec00fd125481cecd4ba47fea838f0b39a87d3fd05b298f2ac54abd109744fa`;
- login-shell Node resolves successfully. The verified planning-time versions
  were Node `v26.6.0` and npm `11.18.0`; execution records any later version
  drift but requires both commands to exist.

- [ ] **Step 2: Establish the ignored non-overwriting run directory**

Run:

```bash
test ! -e tmp/akari-v2.2-cozy-reach/r01/
mkdir -p tmp/akari-v2.2-cozy-reach/r01/inputs
mkdir -p tmp/akari-v2.2-cozy-reach/r01/prompts
mkdir -p tmp/akari-v2.2-cozy-reach/r01/outputs
mkdir -p tmp/akari-v2.2-cozy-reach/r01/tools
git check-ignore -v tmp/akari-v2.2-cozy-reach/r01/
test ! -e tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
```

Expected: every command exits `0`; `.gitignore` owns the run directory and the
sole output path is absent. If the run directory already exists, stop rather
than reuse or delete it.

- [ ] **Step 3: Copy the references and recovery helper without changing bytes**

Run:

```bash
cp --no-clobber \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  tmp/akari-v2.2-cozy-reach/r01/inputs/portrait-authority.webp
cp --no-clobber \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp \
  tmp/akari-v2.2-cozy-reach/r01/inputs/fullbody-authority.webp
cp --no-clobber \
  /home/takahiro/.codex/attachments/fa016a44-2698-4939-aaa5-607832e76ac7/HFfjnyCbQAA19tl.jpg \
  tmp/akari-v2.2-cozy-reach/r01/inputs/composition-reference.jpg
cmp --silent \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  tmp/akari-v2.2-cozy-reach/r01/inputs/portrait-authority.webp
cmp --silent \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp \
  tmp/akari-v2.2-cozy-reach/r01/inputs/fullbody-authority.webp
cmp --silent \
  /home/takahiro/.codex/attachments/fa016a44-2698-4939-aaa5-607832e76ac7/HFfjnyCbQAA19tl.jpg \
  tmp/akari-v2.2-cozy-reach/r01/inputs/composition-reference.jpg
cp --no-clobber \
  tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs \
  tmp/akari-v2.2-cozy-reach/r01/tools/recover-image-payload.mjs
cmp --silent \
  tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs \
  tmp/akari-v2.2-cozy-reach/r01/tools/recover-image-payload.mjs
```

Expected: all four `cmp` commands exit `0`.

- [ ] **Step 4: Persist the exact approved master prompt**

Use `apply_patch` to create
`tmp/akari-v2.2-cozy-reach/r01/prompts/master.txt` with exactly:

```text
Use case: illustration-story
Asset type: one review-only Akari v2.2 prototype illustration

Input images:
- Image 1 is the PRIMARY face, identity, eye, apparent-age, hair, single-hairpin, palette, and close-rendering authority.
- Image 2 is the BODY BALANCE, canonical casual outfit, laterality, and full-figure support authority.
- Image 3 is a COMPOSITION AND MOOD REFERENCE ONLY. Borrow only its intimate first-person sofa viewpoint, diagonal body flow, foreground reaching-hand foreshortening, direct viewer interaction, and warm domestic atmosphere. Do not copy its person, face, hair, eyes, sailor uniform, school bag, speech bubbles, room layout, or character identity.

Primary request: Create one polished vertical portrait anime illustration of the same Akari from Images 1 and 2 in an intimate everyday sofa moment. She is the same 18-year-old young adult established by the v2.0-to-v2.2 lineage: fresh and naturally cute, clearly not a child and not a mid-twenties reinterpretation.

Scene/backdrop: A quiet warm living room with a beige sofa. Akari is settled naturally on the sofa, supporting herself with one arm while looking directly toward the viewer. Include one blue cushion as a restrained accent. Optionally include one small unframed coral annoyance mark floating above a distant cushion; it must contain no text or enclosing bubble.

Composition/framing: Vertical portrait composition. Place her face large and near the visual center. Let her body follow a relaxed diagonal into the depth of the frame. One open hand reaches toward the lens from the lower foreground and becomes noticeably larger through natural wide-angle foreshortening, but remains secondary to the face and does not block both eyes. Her other forearm rests comfortably near or beneath her cheek. Her legs may recede into the background with lightly bent knees and gray-socked feet where visible. Keep natural clothing coverage and do not direct attention toward the skirt.

Expression/emotional read: Affectionate exasperation rather than anger. Preserve Image 1's exact facial construction beneath a changed scene expression: coordinated direct gaze, soft blush across both cheeks, relaxed brows with a slight protesting lift or pinch, and a small open mouth or restrained half-smile that reads as “hey, stop filming.” She feels familiar and engaged, as if the viewer is a close childhood friend just beyond the camera.

Identity locks: Preserve Image 1's warm amber-brown eyes, eye spacing, brows, soft cheeks, compact rounded chin, small nose, warm chestnut hair, soft off-center bangs, and polished soft-cel rendering family. Preserve one low side ponytail on character-left/canvas-right with the same blue tie. Preserve exactly one straight slender filled blue capsule hairpin above the character-left temple, visible on canvas-right, rising toward crown-back at approximately 45–60 degrees and approximately 0.8–1.0 visible eye width. One quiet dark edge is allowed only for legibility. Preserve Image 2's plain white short-sleeve T-shirt, blue denim skirt, gray socks where visible, healthy body balance, and laterality. The approved sofa pose and reaching gesture replace the literal standing V-sign pose in Image 2 without changing her underlying body identity.

Style/medium: Polished anime illustration with thin warm-brown to neutral-gray colored linework, clean controlled cel-shadow shapes, soft blending mainly on cheeks and skin transitions, and restrained warm hair highlights. Let the close camera make the head and eyes feel slightly more prominent without changing the canonical face or turning her into a chibi figure.

Color palette: Warm chestnut, white, denim blue, warm beige, skin peach, and a small coral accent. Keep the background quieter than the face, eyes, reaching hand, hairpin, and clothing edges.

Anatomy and coverage: Construct the reaching hand as one palm, one thumb, and four fingers with plausible knuckles and a coherent wrist-to-forearm connection. Natural finger overlap or partial occlusion is allowed, but no extra or structurally missing digit. Keep both arms, shoulders, neck, torso, and every visible part of the hips, legs, and feet anatomically connected, with plausible off-frame continuation. Keep the T-shirt and denim skirt naturally fitted and fully covering for the pose.

Avoid: childlike age drift, mid-twenties age drift, doll-like giant eyes, chibi proportions, black hair, gray eyes, copied face from Image 3, sailor uniform, school bag, crossed hairpins, second hairpin, doubled pin outline, internal pin line, loop, ornament attachment, unrelated wardrobe decoration, neutral model pose, glamour expression, aggressive anger, extra person, merged limbs, duplicate fingers, extra hands, fused feet, broken joints, disconnected hair, sofa intersections, underwear view, cleavage emphasis, transparent fabric, voyeuristic or fetish framing, text, pseudo-text, speech bubble, logo, watermark, border, seam, or material generation artifact.
```

Run:

```bash
sha256sum tmp/akari-v2.2-cozy-reach/r01/prompts/master.txt
```

Expected: SHA-256
`4eae9128b2fbcbf6dbf814e95f7f8bc2f1488be6744b386137c241cc035cf7cb`.

- [ ] **Step 5: Initialize the run ledger with known facts only**

Use `apply_patch` to create `tmp/akari-v2.2-cozy-reach/r01/run.md` with exactly:

```markdown
# Akari v2.2 Cozy-Reach r01 Run

Status: prepared; zero image-generation calls made.

## Approved Inputs

| Order | Role | Run copy | Dimensions | SHA-256 |
| ---: | --- | --- | --- | --- |
| 1 | Primary face, identity, apparent-age, hair, single-hairpin, palette, and close-rendering authority | `inputs/portrait-authority.webp` | `1888 x 3344` | `b076afd95be49c4ed9c5a4ddfb4083c9ead8328313b4d5fa0555a374dd10543c` |
| 2 | Body balance, canonical casual outfit, laterality, and full-figure support authority | `inputs/fullbody-authority.webp` | `1888 x 3344` | `d93307fe219de81c6fb501e9472725a0ad8f3d242a0ddc741bf53d156f8d7688` |
| 3 | Composition and mood reference only | `inputs/composition-reference.jpg` | `1480 x 2184` | `13523b51df5999a93ab934ecf563a4b7c5631e79d5c76583ed6ee028903db191` |

All three run copies are byte-identical to their approved sources under `cmp`.

## Master Prompt

- Path: `prompts/master.txt`
- SHA-256: `4eae9128b2fbcbf6dbf814e95f7f8bc2f1488be6744b386137c241cc035cf7cb`
- Built-in call budget: exactly one.
- Generated outputs may not be used as references or silently replaced.
```

- [ ] **Step 6: Lint the ledger and open all references at original detail**

Run:

```bash
./node_modules/.bin/markdownlint-cli2 \
  tmp/akari-v2.2-cozy-reach/r01/run.md
```

Expected: `0 issues`.

Open all three run copies with `view_image` at `detail: original`. State before
generation that Image 1 is the controlling v2.2 face/hair/hairpin authority,
Image 2 controls body/outfit/laterality beneath the new pose, and Image 3
controls only the approved sofa POV and reaching-hand composition. Keep all
three visible in the active conversation.

No commit: every Task 1 deliverable is intentionally ignored review material.

### Task 2: Generate and Preserve the Sole Candidate

**Files:**

- Read: `tmp/akari-v2.2-cozy-reach/r01/inputs/portrait-authority.webp`
- Read: `tmp/akari-v2.2-cozy-reach/r01/inputs/fullbody-authority.webp`
- Read: `tmp/akari-v2.2-cozy-reach/r01/inputs/composition-reference.jpg`
- Read: `tmp/akari-v2.2-cozy-reach/r01/prompts/master.txt`
- Create: `tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png`
- Modify: `tmp/akari-v2.2-cozy-reach/r01/run.md`

**Interfaces:**

- Consumes: the three frozen Task 1 references in order, the prompt whose hash
  is `4eae9128b2fbcbf6dbf814e95f7f8bc2f1488be6744b386137c241cc035cf7cb`,
  and one unused call budget.
- Produces: exactly one preserved PNG or one recorded technical failure, plus
  actual call-boundary and provenance evidence for Task 3.

- [ ] **Step 1: Record the call boundary and recheck the output absence**

Run immediately before the call:

```bash
date -u +%Y-%m-%dT%H:%M:%S.%3NZ
date +%Y/%m/%d
test ! -e tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
```

Use `apply_patch` to add the returned UTC invocation timestamp and Asia/Tokyo
session day to a new `## Generation Call` section in `run.md`. Do not add an
identifier or source path until Imagegen actually returns one.

- [ ] **Step 2: Make exactly one built-in Imagegen call**

Call built-in `image_gen` once with:

- `referenced_image_paths` in this exact order:
  1. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-cozy-reach/r01/inputs/portrait-authority.webp`;
  2. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-cozy-reach/r01/inputs/fullbody-authority.webp`;
  3. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-cozy-reach/r01/inputs/composition-reference.jpg`.
- `prompt`: the exact complete contents of
  `tmp/akari-v2.2-cozy-reach/r01/prompts/master.txt`.
- no `num_last_images_to_include` argument.

Do not pass a destination path. Capture the tool's returned source path,
output hint, outer request ID, completed call/generation ID, and visible image.
Do not invoke the tool again for any reason during this run.

- [ ] **Step 3: Record completion time and actual returned metadata**

Run immediately after the call completes:

```bash
date -u +%Y-%m-%dT%H:%M:%S.%3NZ
```

Use `apply_patch` to extend `## Generation Call` with the returned completion
timestamp, tool mode `built-in image_gen`, source path or `not returned`, outer
request ID or `not returned`, and completed call/generation ID or
`not returned`. Record unavailable fields literally as `not returned`; never
invent a value.

- [ ] **Step 4: Preserve the returned PNG without overwrite**

If the tool returned a local source PNG path, run:

```bash
cp --no-clobber -- "ACTUAL_BUILT_IN_SOURCE_PATH" \
  tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
cmp --silent -- "ACTUAL_BUILT_IN_SOURCE_PATH" \
  tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
```

`ACTUAL_BUILT_IN_SOURCE_PATH` means the exact path returned by this one tool
call, not an inferred `$CODEX_HOME/generated_images` path. Expected: `cmp`
exits `0`.

If the image is visible but no source path was returned, use the exact
completed call ID from Step 3 with the existing structural helper:

```bash
bash -lc 'node "$1" "$2" "$3" "$4"' _ \
  tmp/akari-v2.2-cozy-reach/r01/tools/recover-image-payload.mjs \
  ACTUAL_COMPLETED_CALL_ID \
  tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png \
  ACTUAL_ASIA_TOKYO_SESSION_DAY
```

Use the extensionless `exec-...` call ID; strip a trailing `.png` only if a
filename form was returned. `ACTUAL_ASIA_TOKYO_SESSION_DAY` is the exact
`YYYY/MM/DD` value recorded before the call. The helper requires that value to
still be the current Asia/Tokyo day, requires exactly one unique completed PNG
for the call ID, validates signature `89504e470d0a1a0a`, and refuses overwrite.

If neither path nor call ID was returned, structurally scan only the recorded
UTC call interval without printing payload data:

```bash
jq -rc \
  --arg after ACTUAL_INVOCATION_UTC \
  --arg before ACTUAL_COMPLETION_UTC '
    . as $event
    | select($event.timestamp >= $after and $event.timestamp <= $before)
    | ($event | .. | objects
       | select(
           (.type? == "image_generation_call" or
            .type? == "image_generation_end") and
           ((.result? // "") | type == "string") and
           ((.result? // "") | startswith("iVBOR"))
         ))
    | (.call_id // .generation_id // .id)
    | select(. != null)
  ' /home/takahiro/.codex/sessions/ACTUAL_ASIA_TOKYO_SESSION_DAY/rollout-*.jsonl \
  | sort -u
```

Use the actual recorded timestamps and session-day path components. `sort -u`
deduplicates the reported call IDs. Proceed with the helper only if exactly one
non-null extensionless call ID remains; otherwise record `technical failure:
ambiguous or absent rollout payload` and stop without a second Imagegen call.
Never emit `.result` or the base64 payload to the terminal.

- [ ] **Step 5: Verify and record the preserved file**

Run:

```bash
file tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
xxd -p -l 8 \
  tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
identify -format '%f %m %wx%h %[colorspace]\n' \
  tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
stat -c '%n %s bytes' \
  tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
sha256sum \
  tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
```

Expected:

- the file is PNG;
- the first eight bytes are `89504e470d0a1a0a`;
- height is greater than width, matching the requested vertical portrait;
- dimensions, colorspace, byte size, and SHA-256 are concrete and recorded.

Use `apply_patch` to add a `## Preserved Output` section to `run.md` containing
the exact saved path, format, dimensions, colorspace, byte size, signature,
SHA-256, preservation method (`returned source copy` or `rollout recovery`),
source-path `cmp` result when applicable, and the helper's rollout path when
recovery was used.

No commit: the sole candidate and all Task 2 evidence are intentionally
ignored review material.

### Task 3: Review, Verify Scope, and Present

**Files:**

- Read: `tmp/akari-v2.2-cozy-reach/r01/inputs/portrait-authority.webp`
- Read: `tmp/akari-v2.2-cozy-reach/r01/inputs/fullbody-authority.webp`
- Read: `tmp/akari-v2.2-cozy-reach/r01/inputs/composition-reference.jpg`
- Read: `tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png`
- Modify: `tmp/akari-v2.2-cozy-reach/r01/run.md`

**Interfaces:**

- Consumes: the one unchanged preserved Task 2 PNG, the three frozen
  references, and the seven approved review gates.
- Produces: one evidence-backed seven-gate verdict, one verified ignored-only
  Git scope, and one user-visible candidate handoff with no further mutation.

- [ ] **Step 1: Inspect the candidate at original and reduced detail**

Open the candidate with `view_image` at `detail: original`, then open it again
at `detail: high` for reduced-scale readability. Reopen Image 1 at original
detail as the face/hair/hairpin comparison and Image 2 at original detail as
the body/outfit/laterality comparison. Use Image 3 only to judge the approved
composition and mood; do not treat its person as an identity target.

- [ ] **Step 2: Record all seven visual gates with concrete evidence**

Use `apply_patch` to add `## Seven-Gate Review` to `run.md`. Record each gate as
`PASS` or `FAIL`, followed by one or more visible facts and any residual Minor:

1. **Identity and age:** same v2.2 face and an 18-year-old young-adult read,
   neither childlike nor mid-twenties.
2. **Emotional success:** direct gaze, blush, mouth, reach, and proximity read
   as an affectionate softly protesting “hey, stop” moment.
3. **Hair continuity:** chestnut hair, bangs, low side ponytail, blue tie, and
   exactly one correctly lateralized filled blue capsule hairpin at the
   approved angle and relative length.
4. **Anatomy:** the foreshortened hand, implied one-thumb/four-finger
   construction, wrist, arms, neck, and every visible leg/foot part are
   plausible; off-frame continuation is coherent.
5. **Outfit and coverage:** white T-shirt, denim skirt, and gray socks where
   visible are scene-coherent, naturally covered, and free of Image 3 wardrobe
   transfer.
6. **Composition and finish:** face remains primary, the diagonal sofa POV is
   readable, hand foreshortening supports intimacy without dominating, palette
   is restrained, and rendering is polished.
7. **Artifact safety:** no extra person, duplicate feature, disconnected prop,
   pseudo-text, text, speech bubble, logo, watermark, border, seam, or material
   artifact.

Do not adjust pixels, replace the candidate, or make another Imagegen call in
response to a `FAIL`.

- [ ] **Step 3: Lint the final ledger and verify bounded Git scope**

Run:

```bash
./node_modules/.bin/markdownlint-cli2 \
  tmp/akari-v2.2-cozy-reach/r01/run.md
git check-ignore -v tmp/akari-v2.2-cozy-reach/r01/
git check-ignore -v \
  tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
git diff --quiet
git diff --cached --quiet
git status --short --branch
```

Expected:

- the ledger reports `0 issues`;
- both ignored-path checks resolve to `.gitignore`;
- both Git diff commands exit `0`;
- no canonical or tracked image changed;
- the pre-existing unrelated untracked v2.0 uniform plan remains unchanged;
- ignored run material does not appear in status.

Use `apply_patch` to append the exact scope result and final candidate verdict
to `run.md`, then rerun the explicit ledger lint once.

- [ ] **Step 4: Present the single candidate and stop**

Render the saved image inline from the absolute path:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.2-cozy-reach/r01/outputs/akari-v2.2-cozy-reach-r01.png
```

Report:

- that exactly one built-in Imagegen call was made;
- the final saved path, dimensions, byte size, and SHA-256;
- the exact prompt path and its SHA-256;
- the ordered reference roles;
- each seven-gate `PASS` or `FAIL` and every residual Minor;
- that the candidate is ignored, noncanonical, and not promoted.

Ask the user whether to keep the prototype, request a separately authorized
correction round, or leave it as an experiment. Do not infer that selection
authorizes promotion, another call, a batch, a manifest, a PDF, a push, or any
other package expansion.

No commit: Task 3 only finalizes ignored evidence and hands the unchanged
prototype to the user.

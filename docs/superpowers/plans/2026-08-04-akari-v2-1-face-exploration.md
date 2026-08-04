# Akari v2.1 Stage 1 Face Exploration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review exactly three controlled Akari v2.1 strict-front
face candidates, present one equal-scale comparison, and stop for an explicit
user selection.

**Architecture:** Keep the two accepted v2.0 PNGs immutable and use them with
fixed, role-separated authority in three independent serial image edits. Store
assembled prompts, exact PNG outputs, generation provenance, hard-gate review,
and the comparison only under ignored `tmp/akari-v2.1-redesign/r01/`. The final
action is to request an explicit selection and stop; selection recording, the
30-degree probe, full-body generation, promotion, retry rounds, and package
expansion require later authorization.

**Tech Stack:** Built-in `image_gen`, `view_image`, the `imagegen` skill, PNG,
ImageMagick, Node.js for deterministic prompt assembly and payload recovery,
SHA-256, and Markdown working records.

## Global Constraints

- The approved design is
  `docs/superpowers/specs/2026-08-04-akari-v2-1-redesign-design.md`.
- Design approval authorizes Stage 1 only: three candidates, their review, and
  an explicit face-selection gate.
- Do not generate the 30-degree stability probe or strict-front full-body image
  under this plan.
- Do not promote an asset or create `akari-v2.1/` under this plan.
- Do not generate `r02`, retouch, composite, resize, crop, recompress, or color
  adjust a candidate.
- If a generation call yields no usable or recoverable PNG, record that
  technical failure and continue the remaining first calls. A replacement call
  requires explicit user authorization.
- If no candidate passes all hard gates, reject all three and stop. Do not pick
  the least-bad result.
- Preserve every existing file under `tmp/akari-v2-uniform-batch/` without
  deletion, modification, renaming, or use as a v2.1 reference.
- Store every new working artifact under ignored
  `tmp/akari-v2.1-redesign/r01/`; do not stage or commit it.
- The sole v2.0 face and close-view identity authority is
  `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png`, SHA-256
  `34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe`.
- The v2.0 body, outfit, laterality, and full-figure authority is
  `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png`, SHA-256
  `03e7effc6dd13dadb4f1ec394b84ffe8ed9d218e500f0aefa49ebf2b5f0b6d94`.
- Open both authority images at original detail with `view_image` before every
  image-generation call and state each image's role in the prompt.
- Every candidate must be edited independently from those same two v2.0
  authorities. Do not provide A as a reference for B or C, or B as a reference
  for C.
- "V1 naturalness" is a qualitative goal only. Do not use a v1 image or a
  paused v2.0 candidate as positive identity authority.
- Use `referenced_image_paths` with the two repository paths. Do not use
  `num_last_images_to_include` because all required references have local paths.
- Keep strict-front face direction, level head, direct gaze, the same small open
  friendly smile, shoulder-up crop, warm off-white background, portrait
  orientation, and approximately `1024 x 1536` output scale fixed.
- Keep soft anime linework, warm skin treatment, restrained cel shading, and a
  warm polished finish fixed. Avoid glossy skin, plastic hair, heavy gradients,
  hyper-detailed pupils, and high-frequency strand noise.
- Akari must read as the same approachable 18-year-old young adult as v2.0,
  neither childlike nor mid-20s, glamorous, doll-like, cold, sleepy, or generic
  moe.
- Lock warm chestnut hair, off-center V bangs, low side ponytail, pale muted blue
  crossed hairpin, soft cheeks, compact chin, honey-amber eyes, and the visible
  clothing and neckline from the face master.
- Keep the ponytail and hairpin on character-left, which is canvas-right in the
  strict-front image.
- Only eye implementation, minimal lower-face refinement, bang grouping, hair
  shine, and accent saturation may differ across A, B, and C.
- The common eye lock is medium-width almond geometry with horizontal emphasis,
  restrained vertical opening, a slightly straighter central upper lid, a soft
  inner corner and outer end, no strong droop, medium honey-amber irises with a
  deeper brown rim, a subtle pupil, one small main highlight, at most one faint
  secondary highlight, and an understated lower lid.
- Candidate A is conservative: maximum v2.0 continuity, slightly smaller irises,
  one principal highlight, simplified lid rendering, and minimal face cleanup.
- Candidate B is balanced: horizontally emphasized almond eyes, a slightly
  straighter central upper lid, medium irises, one principal highlight, and
  minimal cheek and chin cleanup.
- Candidate C is refined: the strongest allowed refinement, slightly more
  restrained vertical eye opening, and clearer bang and lower-face grouping
  while retaining the same age and person.
- Use quality-first judgment among passing candidates: same-person continuity,
  late-teen freshness, less stock-AI eye treatment, natural appeal, finish, and
  future reusability. Conservatism alone is not a tie-break.
- Do not build or audit a PDF, run Python tests, run a release gate, add a
  manifest, or create a turnaround, expression sheet, wardrobe sheet, or batch.

## Stage 1 Hard Gates

A candidate passes only when all eight checks are true:

1. It is recognizably the same Akari lineage as the accepted v2.0 face.
2. It reads as an 18-year-old young adult, neither childlike nor mid-20s.
3. Its eyes follow the approved shape, iris, highlight, and lid design.
4. Both eyes align coherently and share compatible gaze, iris scale, and focus.
5. Brows, hairline, ears, jaw-to-neck connection, bangs, hairpin, and ponytail
   connect coherently.
6. Hairpin and ponytail remain on character-left, appearing on canvas-right.
7. It is less glossy and stock-AI-looking without becoming generic v1-style
   prettiness.
8. It has no malformed anatomy, duplicated feature, seam, border, text,
   watermark, or material generation artifact.

## File Map

All created files are ignored working artifacts unless explicitly noted.

- Read only:
  `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png` — sole face and
  close-view identity authority.
- Read only:
  `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png` — body, laterality,
  and full-figure supporting authority.
- Create: `tmp/akari-v2.1-redesign/r01/RUN.md` — authority hashes, prompt hashes,
  output provenance, dimensions, PNG signatures, and run state.
- Create: `tmp/akari-v2.1-redesign/r01/REVIEW.md` — per-candidate hard-gate
  evidence, pass/fail decision, residual Minors, and quality ordering.
- Create: `tmp/akari-v2.1-redesign/r01/prompts/shared.md` — conditions shared
  byte-for-byte by A, B, and C.
- Create: `tmp/akari-v2.1-redesign/r01/prompts/delta-a.md` — conservative delta.
- Create: `tmp/akari-v2.1-redesign/r01/prompts/delta-b.md` — balanced delta.
- Create: `tmp/akari-v2.1-redesign/r01/prompts/delta-c.md` — refined delta.
- Create: `tmp/akari-v2.1-redesign/r01/prompts/assemble-prompts.mjs` — builds
  three immutable full prompt files from the common prompt and one delta.
- Create: `tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-a.md`.
- Create: `tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-b.md`.
- Create: `tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-c.md`.
- Create: `tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs` — structurally
  recovers the exact completed PNG payload when a preview exists without a
  usable local file.
- Create: `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png`.
- Create: `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png`.
- Create: `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png`.
- Create: `tmp/akari-v2.1-redesign/r01/comparison/a-card.png` — local comparison
  intermediate.
- Create: `tmp/akari-v2.1-redesign/r01/comparison/b-card.png` — local comparison
  intermediate.
- Create: `tmp/akari-v2.1-redesign/r01/comparison/c-card.png` — local comparison
  intermediate.
- Create: `tmp/akari-v2.1-redesign/r01/akari-v2.1-face-r01-comparison.png` —
  required equal-scale labeled comparison.

---

### Task 1: Prepare and pin the ignored Stage 1 run

**Files:**

- Create: `tmp/akari-v2.1-redesign/r01/RUN.md`
- Create: `tmp/akari-v2.1-redesign/r01/prompts/shared.md`
- Create: `tmp/akari-v2.1-redesign/r01/prompts/delta-a.md`
- Create: `tmp/akari-v2.1-redesign/r01/prompts/delta-b.md`
- Create: `tmp/akari-v2.1-redesign/r01/prompts/delta-c.md`
- Create: `tmp/akari-v2.1-redesign/r01/prompts/assemble-prompts.mjs`
- Create: `tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs`
- Read only: `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png`
- Read only: `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png`

**Interfaces:**

- Consumes: the approved design and two hash-pinned v2.0 authorities.
- Produces: three full prompts whose shared portion is identical, a run ledger,
  and a safe payload-recovery helper used by Tasks 2 through 4.

- [ ] **Step 1: Confirm the repository and ignore boundary**

Run:

```bash
git status --short --branch
git check-ignore -v tmp/akari-v2.1-redesign/r01/.sentinel
git status --short -- tmp/akari-v2-uniform-batch
find tmp/akari-v2-uniform-batch -type f -print0 | sort -z | \
  xargs -0 sha256sum | sha256sum
```

Expected: `tmp/akari-v2.1-redesign/r01/` is covered by `.gitignore`'s `tmp/`
rule. The v2.0 batch command prints no tracked or untracked status because the
preserved batch remains ignored. Record the final tree digest in `RUN.md`; the
same command must produce the same digest at the end. Do not clean or alter any
existing status item.

- [ ] **Step 2: Verify the two immutable authorities**

Run:

```bash
printf '%s  %s\n' \
  '34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe' \
  'akari-v2.0/accepted/base/akari-v2.0-front-face-master.png' | sha256sum --check -
printf '%s  %s\n' \
  '03e7effc6dd13dadb4f1ec394b84ffe8ed9d218e500f0aefa49ebf2b5f0b6d94' \
  'akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png' | sha256sum --check -
file akari-v2.0/accepted/base/akari-v2.0-front-face-master.png
file akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
identify -format '%f %wx%h %[channels]\n' \
  akari-v2.0/accepted/base/akari-v2.0-front-face-master.png \
  akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
xxd -p -l 8 akari-v2.0/accepted/base/akari-v2.0-front-face-master.png
xxd -p -l 8 akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
```

Expected: both hash checks are `OK`; both are RGB PNGs; dimensions are
`1023x1537` and `941x1672`; both signatures are `89504e470d0a1a0a`.

- [ ] **Step 3: Create the run directories**

Create exactly these ignored directories:

```text
tmp/akari-v2.1-redesign/r01/prompts/
tmp/akari-v2.1-redesign/r01/images/
tmp/akari-v2.1-redesign/r01/comparison/
```

- [ ] **Step 4: Write the shared prompt**

Use `apply_patch` to create `prompts/shared.md` with this exact content:

```text
Use case: character-design-edit
Asset type: local noncanonical Akari v2.1 Stage 1 face candidate
Primary request: Create one polished strict-front shoulder-up portrait of the same Akari as the input authorities. This is one independent candidate, not a comparison sheet.
Input image roles:
- Image 1 is the sole v2.0 face and close-view identity authority. Preserve the same-person lineage, brow placement, eye spacing, cheek character, compact chin, expression warmth, hairline, off-center V bangs, low side ponytail, crossed hairpin, visible clothing and neckline, and warm close-view rendering.
- Image 2 is supporting authority only for body balance, full-figure rendering family, and laterality. Preserve the character-left placement of the ponytail and hairpin, which appears on canvas-right in this strict-front view. Do not import its drawcord or organizer into the portrait.
Subject: one original approachable 18-year-old young adult Akari, clearly neither childlike nor mid-20s. She is naturally cute, familiar, fresh, and warm rather than glamorous, doll-like, cold, sleepy, highly fashionable, or generically moe.
Composition: strict-front face; level head; direct gaze; the same small open friendly smile as the face authority; shoulder-up portrait crop; both shoulders and the complete hair silhouette visible; portrait orientation at approximately 1024 by 1536; plain warm off-white background; no props.
Face lock: soft rounded face, soft cheeks, compact chin, small delicate nose with faint readable structure, stable friendly mouth corners, no detailed lips, no synthetic idol smile. Remove only excess lower-face puffiness; do not lengthen or sharpen the lower face.
Hair lock: warm chestnut or cocoa-brown hair; off-center V bangs formed by two or three primary groups with only enough smaller strands for natural asymmetry; slightly reduced crown puffiness and internal strand noise; readable connected low side ponytail on character-left; pale muted blue complete crossed hairpin on character-left; light movement only at the tips.
Eye design: medium-width honey-amber almond eyes with horizontal emphasis and restrained vertical opening; a slightly straighter central upper lid that softens toward the outer end; soft inner corners; no strongly drooping outer corners; deeper restrained brown iris rim; readable subtle pupil; one small main highlight and at most one faint secondary highlight; understated lower lid; compatible gaze, iris scale, and focus in both eyes.
Rendering lock: soft anime linework, warm skin, restrained cel shading, warm polished finish, bright fresh muted palette. Avoid glossy skin, plastic hair, heavy gradients, hyper-detailed pupils, wet-gloss eyes, oversized round irises, heavy eyeliner, lower-lash emphasis, lash clusters, and high-frequency hair strands.
Fixed comparison conditions: keep pose, head angle, gaze, expression, crop, visible clothing, background, lighting, line treatment, skin treatment, shading, and finish fixed. Change only the candidate-specific eye implementation, minimal lower-face refinement, bang grouping, hair shine, and accent saturation described below.
Text verbatim: ""
Hard constraints: one person only; same Akari lineage; coherent eyes, brows, hairline, ears, jaw-to-neck connection, bangs, hairpin, and ponytail; correct character-left laterality; no malformed anatomy, duplicated feature, disconnected hair, seam, border, text, logo, watermark, or generation artifact.
Avoid: new person, child face, mid-20s face, generic v1-style prettiness, glossy stock-AI anime finish, glamour makeup, fashion styling, altered outfit, tilted head, oblique camera, closed mouth, broad idol grin, cropped hair, extra accessories, extra characters, multi-panel layout, neon blue, orange-red hair, loud yellow eyes, and competing cute accent colors.
```

- [ ] **Step 5: Write the three candidate deltas**

Use `apply_patch` to create the three delta files with these exact contents.

`prompts/delta-a.md`:

```text
Candidate direction: A / conservative.
Use maximum v2.0 continuity. Make the irises only slightly smaller than the face authority, use one principal highlight with no visible sparkle cluster, and simplify the lid rendering without changing the familiar eye spacing or warmth. Apply only the minimum lower-face cleanup needed for a finished result. Keep the original cheek and chin character dominant. Simplify internal hair shine and bang noise only enough to remove the stock-AI gloss impression.
```

`prompts/delta-b.md`:

```text
Candidate direction: B / balanced.
Use the recommended center refinement. Make the almond eyes more horizontally emphasized with a slightly straighter central upper lid, medium honey-amber irises, one principal highlight, a subtle pupil, and an understated lower lid. Apply minimal cheek and chin cleanup while preserving the same short compact lower-face identity. Group the bangs more clearly and mute hair and blue-accent saturation slightly without making the palette gray.
```

`prompts/delta-c.md`:

```text
Candidate direction: C / refined.
Use the strongest refinement allowed by the design while keeping the same person and age. Restrain the vertical eye opening slightly more than B, retain horizontal almond emphasis, medium honey-amber irises, one principal highlight, a subtle pupil, and a quiet lower lid. Clarify the two-or-three-group bang structure and lower-face finish slightly more than B, but keep soft cheeks, the compact chin, the familiar smile, and late-teen warmth. Reduce synthetic shine and accent saturation only to the approved muted-bright endpoint.
```

- [ ] **Step 6: Add deterministic prompt assembly**

Use `apply_patch` to create `prompts/assemble-prompts.mjs`:

```javascript
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const shared = readFileSync(join(root, "shared.md"), "utf8").trim();

for (const variant of ["a", "b", "c"]) {
  const delta = readFileSync(join(root, `delta-${variant}.md`), "utf8").trim();
  const output = `${shared}\n\n${delta}\n`;
  writeFileSync(
    join(root, `akari-v2.1-face-r01-${variant}.md`),
    output,
    { encoding: "utf8", flag: "wx" },
  );
}
```

Run:

```bash
bash -lc 'node tmp/akari-v2.1-redesign/r01/prompts/assemble-prompts.mjs'
sha256sum tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-a.md
sha256sum tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-b.md
sha256sum tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-c.md
```

Expected: exactly three full prompts are created. Record their literal hashes in
`RUN.md`. A second assembly attempt must fail instead of overwriting them.

- [ ] **Step 7: Add structural PNG payload recovery**

Use `apply_patch` to create `recover-image-payload.mjs`:

```javascript
import { createHash } from "node:crypto";
import {
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";

const [callId, destination, sessionDay] = process.argv.slice(2);

if (!callId || !destination || !sessionDay) {
  throw new Error(
    "usage: node recover-image-payload.mjs CALL_ID DESTINATION YYYY/MM/DD",
  );
}

const codexRoot = process.env.CODEX_HOME ?? "/home/takahiro/.codex";
const rolloutRoot = resolve(codexRoot, "sessions", sessionDay);
const payloads = new Map();

function visit(value, rolloutPath) {
  if (Array.isArray(value)) {
    for (const item of value) visit(item, rolloutPath);
    return;
  }
  if (!value || typeof value !== "object") return;

  const type = value.type;
  const result = value.result;
  const recordedCallId = value.call_id ?? value.generation_id ?? value.id;
  const eligibleType =
    type === "image_generation_call" || type === "image_generation_end";

  if (
    eligibleType &&
    recordedCallId === callId &&
    typeof result === "string" &&
    result.startsWith("iVBOR")
  ) {
    const bytes = Buffer.from(result, "base64");
    const signature = bytes.subarray(0, 8).toString("hex");
    if (signature !== "89504e470d0a1a0a") {
      throw new Error(`invalid PNG signature for ${callId}: ${signature}`);
    }
    const sha256 = createHash("sha256").update(bytes).digest("hex");
    payloads.set(sha256, { bytes, rolloutPath, sha256, signature, type });
  }

  for (const child of Object.values(value)) visit(child, rolloutPath);
}

for (const name of readdirSync(rolloutRoot)) {
  if (!name.startsWith("rollout-") || !name.endsWith(".jsonl")) continue;
  const rolloutPath = join(rolloutRoot, name);
  const lines = readFileSync(rolloutPath, "utf8").split("\n");
  for (const line of lines) {
    if (!line) continue;
    visit(JSON.parse(line), rolloutPath);
  }
}

if (payloads.size !== 1) {
  throw new Error(
    `expected one unique completed PNG for ${callId}, found ${payloads.size}`,
  );
}

const recovered = [...payloads.values()][0];
mkdirSync(dirname(destination), { recursive: true });
writeFileSync(destination, recovered.bytes, { flag: "wx" });
process.stdout.write(
  `${JSON.stringify({
    callId,
    destination,
    rolloutPath: recovered.rolloutPath,
    sha256: recovered.sha256,
    signature: recovered.signature,
    sourceType: recovered.type,
  })}\n`,
);
```

Run:

```bash
bash -lc 'node --check tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs'
```

Expected: syntax check passes. Use the helper only when the image is visible but
the tool-provided local PNG is absent or unreadable. It must match the exact
returned call ID, parse the current-day rollout structurally, accept only an
`iVBOR` payload, verify `89504e470d0a1a0a`, refuse an ambiguous match, and never
overwrite an existing candidate.

- [ ] **Step 8: Create the run ledger**

Use `apply_patch` to create `RUN.md` with:

- status `prepared; no generation call issued`;
- the approved design path and approval date `2026-08-04`;
- both authority paths, roles, dimensions, hashes, and PNG signatures;
- all three full prompt paths and their computed SHA-256 values;
- one row per candidate with initial state `not generated`;
- columns for outer request ID, completed generation/call ID, authoritative
  generated path or rollout path, saved candidate path, dimensions, signature,
  candidate SHA-256, original-detail inspection, and technical notes;
- the statement that A, B, and C each receive exactly one independent first
  call and that payload rescue is recovery, not regeneration;
- the statement that no working file is eligible for Git staging.

Run:

```bash
git status --short -- tmp/akari-v2.1-redesign/r01
```

Expected: no output because the entire run is ignored.

### Task 2: Generate, preserve, and inspect candidate A

**Files:**

- Read: `tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-a.md`
- Create: `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png`
- Modify: `tmp/akari-v2.1-redesign/r01/RUN.md`
- Read only: both accepted v2.0 authority PNGs.

**Interfaces:**

- Consumes: the immutable A prompt and the two role-separated v2.0 references.
- Produces: candidate A's exact first-call PNG and complete provenance, or one
  recorded unrecoverable technical failure. It never produces a retry.

- [ ] **Step 1: Load the required image-generation instructions**

Read `/home/takahiro/.codex/skills/.system/imagegen/SKILL.md` completely and
announce that the `imagegen` skill is being used before taking image-generation
action. Do not call image generation until this is complete.

- [ ] **Step 2: Re-open both authorities at original detail**

Use `view_image` with `detail: "original"` on:

```text
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-face-master.png
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
```

Keep both visible in the conversation. State that the face master controls
identity and close-view rendering, while the full-body image supports body
family and character-left laterality only.

- [ ] **Step 3: Issue candidate A's one independent edit call**

Read the full A prompt verbatim and call `image_gen` once with:

```json
{
  "prompt": "the complete UTF-8 contents of akari-v2.1-face-r01-a.md",
  "referenced_image_paths": [
    "/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-face-master.png",
    "/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png"
  ]
}
```

Do not include B, C, any v1 image, any v2.0 uniform-batch image, or a recent
conversation image. Record the outer request ID and completed call/generation
ID before any file operation.

- [ ] **Step 4: Preserve the exact returned A PNG**

If the tool returns a readable local source path, copy that exact file to:

```text
tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png
```

Use a no-clobber copy and do not transform it. If no local PNG exists, run the
recovery helper with the exact completed call ID and the actual current session
day. For a run on the design date, the command shape is:

```bash
cp --no-clobber -- "$AKARI_V21_SOURCE_PATH" \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png
cmp --silent -- "$AKARI_V21_SOURCE_PATH" \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png
rg -l '"type":"image_generation_call"|"result":"iVBOR' \
  /home/takahiro/.codex/sessions/2026/08/04/rollout-*.jsonl
bash -lc 'node tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs "$AKARI_V21_CALL_ID" tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png 2026/08/04'
```

Set `AKARI_V21_SOURCE_PATH` to the literal readable source path and
`AKARI_V21_CALL_ID` to the literal completed ID returned by candidate A's tool
call. Use only the copy and `cmp` lines for a readable local source; use only the
search and recovery lines when it is absent. Record whether the source was a
generated path or a structurally parsed rollout payload. If neither source is
usable, mark A `technical failure` and do not issue another call.

- [ ] **Step 5: Verify and inspect A**

For a saved PNG, run:

```bash
file tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png
sha256sum \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png
```

Expected: readable non-empty RGB PNG, portrait dimensions near `1024 x 1536`,
signature `89504e470d0a1a0a`, and one recorded SHA-256. Use `view_image` at
original detail and record concrete preliminary findings for all eight gates.
A failed visual gate does not authorize correction and does not prevent the
first B and C calls.

### Task 3: Generate, preserve, and inspect candidate B

**Files:**

- Read: `tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-b.md`
- Create: `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png`
- Modify: `tmp/akari-v2.1-redesign/r01/RUN.md`
- Read only: both accepted v2.0 authority PNGs.

**Interfaces:**

- Consumes: the immutable B prompt and the original two v2.0 references, never
  candidate A.
- Produces: candidate B's exact first-call PNG and complete provenance, or one
  recorded unrecoverable technical failure. It never produces a retry.

- [ ] **Step 1: Load the required image-generation instructions**

Read `/home/takahiro/.codex/skills/.system/imagegen/SKILL.md` completely and
announce that the `imagegen` skill is being used before taking B's generation
action.

- [ ] **Step 2: Re-open both original authorities**

Use `view_image` with `detail: "original"` on:

```text
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-face-master.png
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
```

Keep them visible and state that the face master controls identity and
close-view rendering, while the full-body image supports body family and
character-left laterality only. Do not open A as an input reference for B.

- [ ] **Step 3: Issue candidate B's one independent edit call**

Read the full B prompt verbatim and call `image_gen` once with:

```json
{
  "prompt": "the complete UTF-8 contents of akari-v2.1-face-r01-b.md",
  "referenced_image_paths": [
    "/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-face-master.png",
    "/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png"
  ]
}
```

Record the outer request ID and completed call/generation ID. Do not include A,
C, any v1 image, any v2.0 batch image, or recent conversation images.

- [ ] **Step 4: Preserve the exact returned B PNG**

Copy a readable tool-provided source without transformation and without
overwriting to:

```text
tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png
```

If the local source is absent, invoke the recovery helper with B's literal
completed call ID, destination, and actual session day. Record the source path
or rollout path and recovery type. If recovery also fails, mark B
`technical failure` and do not call again.

Set `AKARI_V21_SOURCE_PATH` to B's literal readable source path and
`AKARI_V21_CALL_ID` to B's literal completed ID. Run:

```bash
cp --no-clobber -- "$AKARI_V21_SOURCE_PATH" \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png
cmp --silent -- "$AKARI_V21_SOURCE_PATH" \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png
rg -l '"type":"image_generation_call"|"result":"iVBOR' \
  /home/takahiro/.codex/sessions/2026/08/04/rollout-*.jsonl
bash -lc 'node tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs "$AKARI_V21_CALL_ID" tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png 2026/08/04'
```

Use only the copy and `cmp` lines for a readable local source; use only the
search and recovery lines when it is absent. Record byte identity for a copied
source or payload provenance for a recovered source.

- [ ] **Step 5: Verify and inspect B**

For a saved PNG, run:

```bash
file tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png
sha256sum \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png
```

Expected: readable non-empty RGB PNG, portrait dimensions near `1024 x 1536`,
signature `89504e470d0a1a0a`, and one recorded SHA-256. Use `view_image` at
original detail. Record preliminary evidence for all eight hard gates,
including whether B actually occupies the balanced center rather than drifting
toward A or C. Do not retouch or retry.

### Task 4: Generate, preserve, and inspect candidate C

**Files:**

- Read: `tmp/akari-v2.1-redesign/r01/prompts/akari-v2.1-face-r01-c.md`
- Create: `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png`
- Modify: `tmp/akari-v2.1-redesign/r01/RUN.md`
- Read only: both accepted v2.0 authority PNGs.

**Interfaces:**

- Consumes: the immutable C prompt and the original two v2.0 references, never
  candidates A or B.
- Produces: candidate C's exact first-call PNG and complete provenance, or one
  recorded unrecoverable technical failure. It never produces a retry.

- [ ] **Step 1: Load the required image-generation instructions**

Read `/home/takahiro/.codex/skills/.system/imagegen/SKILL.md` completely and
announce that the `imagegen` skill is being used before taking C's generation
action.

- [ ] **Step 2: Re-open both original authorities**

Use `view_image` with `detail: "original"` on:

```text
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-face-master.png
/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
```

Keep them visible and state that the face master controls identity and
close-view rendering, while the full-body image supports body family and
character-left laterality only. Do not open A or B as an input reference for C.

- [ ] **Step 3: Issue candidate C's one independent edit call**

Read the full C prompt verbatim and call `image_gen` once with:

```json
{
  "prompt": "the complete UTF-8 contents of akari-v2.1-face-r01-c.md",
  "referenced_image_paths": [
    "/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-face-master.png",
    "/home/takahiro/workspace/akari-design/akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png"
  ]
}
```

Record the outer request ID and completed call/generation ID. Do not include A,
B, any v1 image, any v2.0 batch image, or recent conversation images.

- [ ] **Step 4: Preserve the exact returned C PNG**

Copy a readable tool-provided source without transformation and without
overwriting to:

```text
tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
```

If the local source is absent, invoke the recovery helper with C's literal
completed call ID, destination, and actual session day. Record the source path
or rollout path and recovery type. If recovery also fails, mark C
`technical failure` and do not call again.

Set `AKARI_V21_SOURCE_PATH` to C's literal readable source path and
`AKARI_V21_CALL_ID` to C's literal completed ID. Run:

```bash
cp --no-clobber -- "$AKARI_V21_SOURCE_PATH" \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
cmp --silent -- "$AKARI_V21_SOURCE_PATH" \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
rg -l '"type":"image_generation_call"|"result":"iVBOR' \
  /home/takahiro/.codex/sessions/2026/08/04/rollout-*.jsonl
bash -lc 'node tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs "$AKARI_V21_CALL_ID" tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png 2026/08/04'
```

Use only the copy and `cmp` lines for a readable local source; use only the
search and recovery lines when it is absent. Record byte identity for a copied
source or payload provenance for a recovered source.

- [ ] **Step 5: Verify and inspect C**

For a saved PNG, run:

```bash
file tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
sha256sum \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
```

Expected: readable non-empty RGB PNG, portrait dimensions near `1024 x 1536`,
signature `89504e470d0a1a0a`, and one recorded SHA-256. Use `view_image` at
original detail. Record preliminary evidence for all eight hard gates,
including whether C stays inside the approved refinement ceiling and preserves
the same age and person. Do not retouch or retry.

### Task 5: Build the equal-scale comparison and make the hard-gate review

**Files:**

- Read: all three candidate PNGs.
- Create: `tmp/akari-v2.1-redesign/r01/comparison/a-card.png`
- Create: `tmp/akari-v2.1-redesign/r01/comparison/b-card.png`
- Create: `tmp/akari-v2.1-redesign/r01/comparison/c-card.png`
- Create: `tmp/akari-v2.1-redesign/r01/akari-v2.1-face-r01-comparison.png`
- Create: `tmp/akari-v2.1-redesign/r01/REVIEW.md`
- Modify: `tmp/akari-v2.1-redesign/r01/RUN.md`

**Interfaces:**

- Consumes: exactly one preserved first-call PNG for A, B, and C.
- Produces: one uncropped equal-scale comparison, an eight-gate verdict for each
  candidate, and either an all-reject stop or an explicit user-selection gate.

- [ ] **Step 1: Require all three exact files before comparison**

Run:

```bash
test -s tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png
test -s tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png
test -s tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
```

If any command fails, do not make a misleading three-way comparison. Report
the available candidates and recorded technical failure, then stop. A missing
candidate's replacement call requires explicit authorization.

- [ ] **Step 2: Build three fixed-size uncropped cards**

Run:

```bash
magick \
  \( tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png \
     -auto-orient -resize '600x900' -background '#f3f0ec' \
     -gravity center -extent 600x900 \) \
  \( -size 600x72 xc:'#ffffff' -font DejaVu-Sans -pointsize 30 \
     -fill '#2b2927' -gravity center -annotate +0+0 'A - conservative' \) \
  -append tmp/akari-v2.1-redesign/r01/comparison/a-card.png
magick \
  \( tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png \
     -auto-orient -resize '600x900' -background '#f3f0ec' \
     -gravity center -extent 600x900 \) \
  \( -size 600x72 xc:'#ffffff' -font DejaVu-Sans -pointsize 30 \
     -fill '#2b2927' -gravity center -annotate +0+0 'B - balanced' \) \
  -append tmp/akari-v2.1-redesign/r01/comparison/b-card.png
magick \
  \( tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
     -auto-orient -resize '600x900' -background '#f3f0ec' \
     -gravity center -extent 600x900 \) \
  \( -size 600x72 xc:'#ffffff' -font DejaVu-Sans -pointsize 30 \
     -fill '#2b2927' -gravity center -annotate +0+0 'C - refined' \) \
  -append tmp/akari-v2.1-redesign/r01/comparison/c-card.png
```

Each candidate is contained within the same `600 x 900` image area without
cropping, centered on the same background, and labeled in a separate `600 x
72` strip.

- [ ] **Step 3: Join and verify the required comparison**

Run:

```bash
magick \
  tmp/akari-v2.1-redesign/r01/comparison/a-card.png \
  tmp/akari-v2.1-redesign/r01/comparison/b-card.png \
  tmp/akari-v2.1-redesign/r01/comparison/c-card.png \
  +append tmp/akari-v2.1-redesign/r01/akari-v2.1-face-r01-comparison.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/r01/akari-v2.1-face-r01-comparison.png
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/r01/akari-v2.1-face-r01-comparison.png
sha256sum \
  tmp/akari-v2.1-redesign/r01/akari-v2.1-face-r01-comparison.png
```

Expected: one `1800 x 972` RGB PNG, signature `89504e470d0a1a0a`, and one
recorded SHA-256. Use `view_image` at original detail on the comparison and all
three individual PNGs. Re-open the v2.0 face master at original detail for the
same-person gate. The comparison is review evidence only and does not replace
original-detail inspection.

- [ ] **Step 4: Record the complete review matrix**

Use `apply_patch` to create `REVIEW.md` with:

- review date and the approved design path;
- all three prompt hashes, candidate hashes, dimensions, and call IDs;
- one row for each of the eight hard gates and one `Pass` or `Fail` cell for A,
  B, and C;
- concrete evidence for every failed gate, not only a summary label;
- concrete residual Minors for each passing candidate;
- a final eligibility line for each candidate: `PASS` only if all eight gates
  pass, otherwise `FAIL`;
- a quality-first ordering of passing candidates based on same-person
  continuity, 18-year-old freshness, eye naturalness, appeal, finish, and reuse;
- an explicit statement that no candidate has been selected, regenerated,
  promoted, or used as authority yet.

Update `RUN.md` to status `reviewed; awaiting explicit face selection` when at
least one candidate passes, or `reviewed; zero passing candidates; stopped`
when none passes.

- [ ] **Step 5: Verify the final boundary before asking for selection**

Run:

```bash
./node_modules/.bin/markdownlint-cli2 \
  tmp/akari-v2.1-redesign/r01/RUN.md \
  tmp/akari-v2.1-redesign/r01/REVIEW.md
bash -lc 'npm run lint:md'
find tmp/akari-v2-uniform-batch -type f -print0 | sort -z | \
  xargs -0 sha256sum | sha256sum
git check-ignore -v \
  tmp/akari-v2.1-redesign/r01/RUN.md \
  tmp/akari-v2.1-redesign/r01/REVIEW.md \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-a.png \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-b.png \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
  tmp/akari-v2.1-redesign/r01/akari-v2.1-face-r01-comparison.png
git status --short -- tmp/akari-v2.1-redesign/r01
git diff --check
git diff --quiet
git diff --cached --quiet
git status --short --branch
```

Expected: all Stage 1 artifacts remain ignored, no Stage 1 artifact appears in
Git status, the v2.0 batch tree digest matches the value captured in Task 1, no
tracked or staged file was changed by execution, targeted and tracked Markdown
lint pass, and the pre-existing user-owned untracked v2.0 plan remains
untouched. Do not stage or commit the ignored run. Show the review result and
stop for explicit selection.

- [ ] **Step 6: Enforce the correct stop**

If zero candidates pass, show the comparison and concrete rejection reasons,
state that `r02` requires a new explicit instruction, and stop.

If one or more candidates pass, show the comparison at:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/r01/akari-v2.1-face-r01-comparison.png
```

Report A, B, and C pass/fail status, residual Minors, and the quality-first
recommendation. Use `request_user_input` without `autoResolutionMs` so the gate
cannot resolve automatically. Offer only passing candidates and an explicit
reject path. When all three pass, use A/B/C as the three choices and explain
that the automatically available free-form choice can reject the set. Mark the
quality-first recommendation as recommended without preselecting it.

Do not infer selection from the recommendation. This plan ends at the explicit
input gate; it does not record or act on the answer.

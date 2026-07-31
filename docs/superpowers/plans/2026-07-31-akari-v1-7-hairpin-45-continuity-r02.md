# Akari v1.7 Hairpin-Side 45-Degree Continuity r02 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review three independent body-only r02 corrections of
V17-03 r01 A while preserving its already-correct 45-degree moment and every
out-of-scope visual detail.

**Architecture:** Byte-copy the authoritative raw r01 A PNG into the new
worktree's ignored r02 input area and supply that verified copy first as the
primary target and canvas. Supply the accepted V17-01 front second, with
authority limited to the underlying chest-to-waist volume and relaxed T-shirt
drape. Run one immutable prompt three times serially with no sibling chaining,
verify each returned source and rollout request, review all three at original
detail and in one six-column comparison, obtain independent review, then stop
at the explicit user-selection gate.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick
`identify` and `magick montage`, `cmp`, `xxd`, SHA-256, structured JSONL
parsing, Git read-only checks, and the repository rollout-payload recovery
procedure.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-45-continuity-r02-design.md`.
- At execution time, use `superpowers:using-git-worktrees` to create the
  isolated checkout
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02`
  on branch `codex/akari-v1-7-hairpin-45-continuity-r02` from the commit
  containing this design and plan.
- Before the first generation call, read and follow the local `imagegen` skill.
- The official image-generation use case is exactly `identity-preserve`.
- Supply exactly two images to every generation call, in this order:
  1. the verified worktree-local byte-copy of authoritative raw r01 A;
  2. `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`.
- The authoritative raw r01 A source is
  `/home/takahiro/.codex/generated_images/019fb8b9-0c2a-7232-adbd-7b48a8c4af53/exec-907b61bc-e92b-4b64-9e81-26e4d0cf9dbf.png`
  with SHA-256
  `701f29a74642ab98a6f948df50d7bf11fc659f0844b25d9636bba8f893ce9965`.
- The accepted front input must have SHA-256
  `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`.
- Image 1 controls the exact r01 A identity, face, expression, eye polish,
  hair, compressed-cord ornament, 45-degree camera, same moment, pose, hips,
  thighs, framing, background, light, palette, lines, paint planes, and finish.
- Image 2 wins only for the underlying chest-to-waist body volume and relaxed
  T-shirt drape. It must not pull the output toward front or change any other
  Image 1 detail.
- Correct only r01 A's rounder near-side bust projection, newly stronger
  under-bust definition, and narrower waist with tighter shirt cling. Retain
  natural adult three-dimensional volume; do not flatten the torso.
- Do not alter hips or thighs. Do not repair r01 A's eye-polish or
  compressed-cord Minors; the user explicitly locked this pass to body only.
- Open the accepted V17-02 30-degree image, v1.5 B3, v1.4 G2, inherited v1.1
  hairpin-side 45-degree image, and accepted v1.2 C03 hairpin-side 45-degree
  image for human QA only. Never add them to `referenced_image_paths`.
- Generate A, B, and C independently with the same ordered input array and
  exact immutable prompt. Never chain candidates or add candidate-specific
  deltas.
- The immutable prompt block, including its final newline, must have SHA-256
  `19459cdff592ecb59a32dbce7f082f233e96e66e5a74a1383ef678773e9c572c`.
- Run generation calls serially. Save and source-verify one candidate before
  beginning the next call.
- Record each completed generation artifact ID, outer rollout request call ID,
  exact returned source path, source/destination byte identity, SHA-256, PNG
  signature, and dimensions.
- Keep all r02 inputs, recovered payloads, candidates, and comparison output
  under ignored `build/v1.7-hairpin-45-continuity-r02/`.
- Preserve all r01 evidence in its existing worktree. Do not read from it for
  generation, overwrite it, delete it, move it, or clean it up.
- Do not modify accepted assets, human-QA references, v1.6 material,
  manifests, validators, rendering code, audit code, release packages, or PDFs.
- If no r02 candidate clears all seven gates, preserve the evidence and return
  to design. Do not generate r03, repair, composite, or relax the scope.
- Do not promote, commit an implementation artifact, push, merge, clean up the
  execution worktree, synchronize remotes, or update selection history.
- Do not run Node tests, Python tests, PDF builds, OCR, package validation,
  integration gates, or release gates.

---

### Task 1: Generate and review V17-03 r02 A/B/C

**Files:**

- Read:
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-45-continuity-r02-design.md`
- Read:
  `docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-45-continuity-r02.md`
- Read as the authoritative raw r01 A source:
  `/home/takahiro/.codex/generated_images/019fb8b9-0c2a-7232-adbd-7b48a8c4af53/exec-907b61bc-e92b-4b64-9e81-26e4d0cf9dbf.png`
- Create and supply first to image generation:
  `build/v1.7-hairpin-45-continuity-r02/input/akari-v1.7-v17-03-hairpin-45-r01-a-authoritative-source.png`
- Read and supply second to image generation:
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`
- Inspect for human QA only:
  `akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`
- Inspect for human QA only:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
- Inspect for human QA only:
  `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
- Inspect for human QA only:
  `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png`
- Inspect for human QA only:
  `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png`
- Create:
  `build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png`
- Create:
  `build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png`
- Create:
  `build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png`
- Create:
  `build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png`

**Interfaces:**

- Consumes: one byte-verified raw r01 A target copied into the worktree, one
  hash-pinned accepted front correction reference, and five hash-pinned
  human-QA-only references.
- Produces: three independent ignored body-only correction candidates, one
  ignored six-column comparison, exact request/source provenance, executor and
  independent seven-gate verdicts, and an explicit user-selection gate; no
  tracked accepted asset or implementation commit.

#### Immutable Generation Prompt

Use this complete prompt byte-for-byte for A, B, and C:

```text
Use case: identity-preserve
Asset: Akari v1.7 V17-03 hairpin-side 45-degree continuity body correction, r02.

Image 1 is the authoritative raw r01 A image and the primary target and canvas.
It already has the correct adult woman, age 25, identity, quietly pleased
closed-mouth expression, hairpin-side 45-degree view, same fixed instant, pose,
ornament, camera, scale, crop, apartment, light, palette, line work, paint
planes, and hand-painted finish. Preserve every Image 1 detail except the three
connected chest-to-waist corrections explicitly requested below.

Image 2 is the accepted V17-01 front checkpoint. It is a correction authority
only for the underlying chest-to-waist body volume and relaxed white T-shirt
drape. If the inputs differ within that narrow scope, Image 2 wins. Everywhere
else Image 1 wins. Do not average or reverse these roles, broaden Image 2's
authority, or pull the result toward a front view.

Create one full-resolution 1024 x 1536 portrait image by making only this
localized body correction to Image 1:

1. Reduce Image 1's newly rounder and more prominent near-side bust projection
   to the restrained accepted underlying volume shown by Image 2, expressed
   naturally from Image 1's fixed 45-degree camera position.
2. Soften Image 1's newly stronger under-bust line, shadow, and separation so
   the transition reads through a relaxed T-shirt rather than as added bust
   definition.
3. Restore Image 2's subtle underlying waist and relaxed chest-to-waist T-shirt
   fall, removing Image 1's narrower waist and tighter shirt cling.

Keep the corrected bust, ribcage, waist, and T-shirt physically coherent as one
adult three-dimensional form at 45 degrees. Do not erase or unnaturally flatten
the chest, paste a frontal silhouette into the angled view, make the shirt
newly baggy, move the ribcage, or conceal the correction with blur, shadow,
cropping, or a pose change. Do not alter the pelvis, hips, thighs, waist-to-hip
relationship beyond removing the narrowed-waist drift, leg lengths, or any
other body region.

Keep Image 1's exact character-left hairpin-side 45-degree azimuth, camera
height, elevation, orbit radius, subject distance, focal perspective, pitch,
roll, portrait crop, and character scale. Keep the exact head, neck, shoulders,
ribcage position, pelvis, knees, ankles, feet, arms, elbows, wrists, hands,
fingers, planted-foot base, quiet near-even balance, room geometry, light
source, and shadows. Do not turn, twist, re-pose, reframe, rescale, or stage the
moment again, and do not move the result toward front.

Preserve Image 1's exact face construction, soft cheek volume, compact chin,
nose, low-contrast amber gaze, brows, lashes, restrained blush, lips, and small
closed-mouth smile. Preserve its existing slightly stronger eye polish exactly;
the user chose body-only scope, so do not correct, reduce, or intensify it.

Preserve Image 1's exact short airy chestnut bob, asymmetric locks, irregular
tips, skull volume, and hair-edge finish. Preserve exactly its character-left
ornament: two pale-blue crossed pins and the same compressed thin cord bow,
including attachment point, ordering, loops, tails, scale, color, and
45-degree perspective. The compressed cord is an accepted r01 A Minor for this
body-only pass; do not expand, repair, simplify, or otherwise change it.

Preserve Image 1's shoulders, arms, hands, pelvis, hips, thighs, knees, lower
legs, bare feet, pale-blue lounge shorts, shirt design outside the corrected
chest-to-waist drape, warm minimal apartment, wall, level baseboard and floor,
directional domestic light, full-body breathing room, quiet warm palette,
deliberate outer lines, restrained interior lines, readable paint planes, and
hand-painted finish. Keep the complete figure in frame from hair to toes.

Reject any changed identity, age, expression, eye treatment, hair, ornament,
camera angle, head angle, pose, balance, hands, hips, thighs, legs, feet,
shorts, room, light, shadow, palette, line hierarchy, paint planes, finish,
crop, or scale. Reject front-view pull, a new take, global redraw, body glamour,
bust enlargement or flattening, strong under-bust definition, waist pinching,
shirt cling, hip reshaping, anatomy defects, seams, blur, wide-angle distortion,
photorealism, plastic smoothing, v1.6 signals, text, labels, borders, logos, or
watermarks. Make no correction beyond the three connected chest-to-waist
targets.
```

- [ ] **Step 1: Verify checkout, prompt, sources, local input copy, tools, and
  output boundary**

Run:

```bash
set -euo pipefail

test "$(pwd -P)" = \
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02"
git cat-file -e \
  HEAD:docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-45-continuity-r02-design.md
git cat-file -e \
  HEAD:docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-45-continuity-r02.md
test "$(awk '
  /^#### Immutable Generation Prompt$/ { section = 1; next }
  section && /^```text$/ { inside = 1; next }
  inside && /^```$/ { exit }
  inside { print }
' docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-45-continuity-r02.md \
  | sha256sum | cut -d ' ' -f 1)" = \
  "19459cdff592ecb59a32dbce7f082f233e96e66e5a74a1383ef678773e9c572c"

raw_r01_a='/home/takahiro/.codex/generated_images/019fb8b9-0c2a-7232-adbd-7b48a8c4af53/exec-907b61bc-e92b-4b64-9e81-26e4d0cf9dbf.png'
local_r01_a='build/v1.7-hairpin-45-continuity-r02/input/akari-v1.7-v17-03-hairpin-45-r01-a-authoritative-source.png'
mkdir -p build/v1.7-hairpin-45-continuity-r02/input
mkdir -p build/v1.7-hairpin-45-continuity-r02/recovered
test -f "$raw_r01_a"
if [ -e "$local_r01_a" ]; then
  cmp --silent "$raw_r01_a" "$local_r01_a"
else
  cp -- "$raw_r01_a" "$local_r01_a"
fi
cmp --silent "$raw_r01_a" "$local_r01_a"
test "$(sha256sum "$raw_r01_a" | cut -d ' ' -f 1)" = \
  "701f29a74642ab98a6f948df50d7bf11fc659f0844b25d9636bba8f893ce9965"
test "$(sha256sum "$local_r01_a" | cut -d ' ' -f 1)" = \
  "701f29a74642ab98a6f948df50d7bf11fc659f0844b25d9636bba8f893ce9965"
test "$(xxd -p -l 8 "$local_r01_a")" = "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' "$local_r01_a")" = \
  "PNG 1024x1536"

test ! -e \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png
test ! -e \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png
test ! -e \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png
test ! -e \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png

sha256sum -c <<'EOF'
64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png
22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png
6757e601d2cfd158c970ab701a876981ace837e669c313dec6d25c0c539ff4d6  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png
ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png
19c8c96113bcbc47f7d1e4cc1d58af466d3a573f0dae40cfcdf9bf456b1a0a9b  akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
EOF
identify -format '%f | %m %wx%h\n' \
  "$local_r01_a" \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png \
  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png \
  akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
command -v magick
command -v identify
command -v sha256sum
command -v xxd
command -v python3
git check-ignore -v build/v1.7-hairpin-45-continuity-r02/probe.png
git diff --quiet
git diff --cached --quiet
git status --short --branch
```

Expected: execution is in the named isolated checkout at a commit containing
both r02 documents; the plan prompt hash matches; the local Image 1 input is a
byte-identical copy of the hash-pinned raw source with valid PNG signature and
exact `PNG 1024x1536` dimensions; all six repository hashes match; all seven
images are readable; tools resolve; `build/` is ignored; no r02 candidate is
overwritten; and tracked and staged diffs are empty.

If a local input or output already exists, do not overwrite it or continue
automatically. Verify its provenance, byte identity, hash, signature,
dimensions, and task state, then resume only from the first incomplete verified
step. Never inspect, copy from, or clean the existing r01 worktree.

- [ ] **Step 2: Open and state all generation and human-QA roles**

Use `view_image` with original detail for the worktree-local r01 A input, the
accepted front, and all five human-QA-only images. Immediately before the first
generation call, state:

- worktree-local r01 A is Image 1, the primary target and canvas, and controls
  every attribute except the narrow chest-to-waist correction;
- accepted V17-01 front is Image 2 and corrects only underlying chest-to-waist
  volume and relaxed T-shirt drape, without pulling the output toward front;
- accepted V17-02 30 degrees checks only same-moment orbit continuity after
  generation;
- v1.5 B3 checks restrained upper-body volume, subtle waist, healthy thighs,
  head-to-body ratio, and quiet full-body balance after generation;
- v1.4 G2 checks adult-face direction, line hierarchy, paint planes, quiet
  palette, and finish after generation;
- inherited v1.1 45 degrees checks only cheek width, bob silhouette, and
  ornament perspective ordering after generation;
- accepted v1.2 C03 45 degrees checks only coherent face-to-feet 45-degree
  alignment after generation.

Keep all seven images visible in conversation context. Pass only Image 1 and
Image 2 to image generation, in that exact order. Never pass a human-QA-only
image.

- [ ] **Step 3: Generate candidate A from the immutable prompt**

Use built-in `image_gen` with the following exact inline array. It must appear
directly in the recorded generation wrapper as valid JSON-compatible syntax:
double-quoted literal absolute strings, no trailing comma, and no variable or
template indirection.

```javascript
referenced_image_paths: [
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/build/v1.7-hairpin-45-continuity-r02/input/akari-v1.7-v17-03-hairpin-45-r01-a-authoritative-source.png",
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png"
]
```

Use the `Immutable Generation Prompt` block exactly, including its final
newline. Keep both paths as literal absolute strings in the request's recorded
two-element `referenced_image_paths` array; do not construct them indirectly.
Record A's outer rollout `custom_tool_call.call_id`, completed generation
artifact ID, and exact returned source path. Do not generate B until A is saved
and source-verified.

- [ ] **Step 4: Save and verify candidate A byte-for-byte**

For the normal saved-path case, bind `candidate_a_source` to the usable exact
returned PNG, `candidate_a_event_saved_path` to the exact `saved_path` recorded
by the completed event, and `candidate_a_generation_id` to that event's exact
`call_id`. Normally the first two paths are identical. Then run:

```bash
set -euo pipefail

: "${candidate_a_source:?set candidate_a_source to candidate A exact returned PNG}"
: "${candidate_a_event_saved_path:?record candidate A exact event saved_path}"
: "${candidate_a_generation_id:?record candidate A completed event call_id}"
test -f "$candidate_a_source"
cp -- "$candidate_a_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png
cmp --silent "$candidate_a_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png
test "$(sha256sum "$candidate_a_source" | cut -d ' ' -f 1)" = \
  "$(sha256sum \
    build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png \
    | cut -d ' ' -f 1)"
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png)" = \
  "PNG 1024x1536"
sha256sum "$candidate_a_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png
git check-ignore -v \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png
```

Expected: saved A is byte-identical to its exact returned source; source and
destination hashes match; signature is valid; dimensions are exactly
`PNG 1024x1536`; provenance and digest are recorded; and the output is ignored.

If the completed call displays an image but exposes no local source PNG, bind
`rollout_path`, `candidate_a_generation_id`, and `recovered_path` to the exact
current-day rollout, A generation artifact ID, and the following unused
recovery path:

`build/v1.7-hairpin-45-continuity-r02/recovered/akari-v1.7-v17-03-hairpin-45-r02-a-source.png`

Then run this structural recovery procedure:

```bash
set -euo pipefail

: "${rollout_path:?set rollout_path to the exact current-day rollout JSONL}"
: "${candidate_a_generation_id:?set candidate A completed artifact ID}"
: "${recovered_path:?set candidate A unused recovered-source PNG path}"
test ! -e "$recovered_path"
python3 - "$rollout_path" "$candidate_a_generation_id" \
  "$recovered_path" <<'PY'
import base64
import json
import pathlib
import sys

rollout = pathlib.Path(sys.argv[1])
generation_id = sys.argv[2]
destination = pathlib.Path(sys.argv[3])

def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)
    elif isinstance(value, str) and value[:1] in "[{" and len(value) < 20000000:
        try:
            decoded = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return
        yield from walk(decoded)

matches = []
with rollout.open("r", encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        for item in walk(event):
            result = item.get("result")
            if item.get("type") not in {
                "image_generation_call",
                "image_generation_end",
            }:
                continue
            if not isinstance(result, str) or not result.startswith("iVBOR"):
                continue
            metadata = {key: value for key, value in item.items() if key != "result"}
            if generation_id in json.dumps(metadata, sort_keys=True):
                matches.append((line_number, item))

if len(matches) != 1:
    raise SystemExit(f"expected one correlated payload, found {len(matches)}")

line_number, selected = matches[0]
payload = base64.b64decode(selected["result"], validate=True)
if payload[:8].hex() != "89504e470d0a1a0a":
    raise SystemExit("recovered payload does not have a PNG signature")
destination.parent.mkdir(parents=True, exist_ok=True)
with destination.open("xb") as output:
    output.write(payload)
print(
    f"recovered line={line_number} generation={generation_id} "
    f"event_saved_path={selected.get('saved_path')} bytes={len(payload)} "
    f"path={destination}"
)
PY
test "$(xxd -p -l 8 "$recovered_path")" = "89504e470d0a1a0a"
```

Bind `candidate_a_source` to that recovered source and
`candidate_a_event_saved_path` to the event's recorded `saved_path`, even when
that returned path is absent locally. Run the complete A copy, `cmp`, hash,
signature, and dimension block above. Step 7 proves the recovered bytes match
the correlated event payload instead of requiring the recovery path to equal
the event's `saved_path`. Never decode directly over the final candidate,
select by prompt text alone, or hand-copy base64.

- [ ] **Step 5: Generate, save, and verify candidate B independently**

Call `image_gen` a second time with the exact literal two-path array from Step 3
and the exact immutable prompt. Do not reference A or add a B-specific
instruction. Record B's outer rollout request call ID, completed generation
artifact ID, and exact returned source path. Bind the required shell values,
then run:

```bash
set -euo pipefail

: "${candidate_b_source:?set candidate_b_source to candidate B exact returned PNG}"
: "${candidate_b_event_saved_path:?record candidate B exact event saved_path}"
: "${candidate_b_generation_id:?record candidate B completed event call_id}"
test -f "$candidate_b_source"
cp -- "$candidate_b_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png
cmp --silent "$candidate_b_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png
test "$(sha256sum "$candidate_b_source" | cut -d ' ' -f 1)" = \
  "$(sha256sum \
    build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png \
    | cut -d ' ' -f 1)"
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png)" = \
  "PNG 1024x1536"
sha256sum "$candidate_b_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png
git check-ignore -v \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png
```

Expected: B passes the same byte-identity, source/destination hash, signature,
dimensions, provenance-recording, and ignored-output checks as A. Do not begin
C until B is saved and verified.

If no local B source exists, run Step 4's structural procedure with B's exact
generation artifact ID and this unused path:

`build/v1.7-hairpin-45-continuity-r02/recovered/akari-v1.7-v17-03-hairpin-45-r02-b-source.png`

Bind `candidate_b_source` to the verified recovered PNG and
`candidate_b_event_saved_path` to B's event-recorded path, then run the complete
B block. Do not reuse A's payload, source path, identifier, or recovered file.

- [ ] **Step 6: Generate, save, and verify candidate C independently**

Call `image_gen` a third time with the exact literal two-path array from Step 3
and the exact immutable prompt. Do not reference A or B or add a C-specific
instruction. Record C's outer rollout request call ID, completed generation
artifact ID, and exact returned source path. Bind the required shell values,
then run:

```bash
set -euo pipefail

: "${candidate_c_source:?set candidate_c_source to candidate C exact returned PNG}"
: "${candidate_c_event_saved_path:?record candidate C exact event saved_path}"
: "${candidate_c_generation_id:?record candidate C completed event call_id}"
test -f "$candidate_c_source"
cp -- "$candidate_c_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png
cmp --silent "$candidate_c_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png
test "$(sha256sum "$candidate_c_source" | cut -d ' ' -f 1)" = \
  "$(sha256sum \
    build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
    | cut -d ' ' -f 1)"
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png)" = \
  "PNG 1024x1536"
sha256sum "$candidate_c_source" \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png
git check-ignore -v \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png
```

Expected: C passes the same byte-identity, source/destination hash, signature,
dimensions, provenance-recording, and ignored-output checks as A and B. Do not
start a fourth generation or a correction call.

If no local C source exists, run Step 4's structural procedure with C's exact
generation artifact ID and this unused path:

`build/v1.7-hairpin-45-continuity-r02/recovered/akari-v1.7-v17-03-hairpin-45-r02-c-source.png`

Bind `candidate_c_source` to the verified recovered PNG and
`candidate_c_event_saved_path` to C's event-recorded path, then run the complete
C block. Do not reuse A's or B's payload, source path, identifier, or recovered
file.

- [ ] **Step 7: Verify distinct calls, generation/source correlation, ordered
  inputs, and rollout prompt hashes**

Keep the candidate source and generation variables from Steps 4 through 6.
Bind `rollout_path` to the exact JSONL that recorded the three calls and bind
each request variable to its outer `custom_tool_call.call_id`, not its item ID.
The generation variables identify the completed `image_generation_end` events.
Run:

```bash
set -euo pipefail

: "${candidate_a_source:?A source must remain recorded}"
: "${candidate_b_source:?B source must remain recorded}"
: "${candidate_c_source:?C source must remain recorded}"
: "${candidate_a_event_saved_path:?A event saved_path must remain recorded}"
: "${candidate_b_event_saved_path:?B event saved_path must remain recorded}"
: "${candidate_c_event_saved_path:?C event saved_path must remain recorded}"
: "${candidate_a_generation_id:?A generation ID must remain recorded}"
: "${candidate_b_generation_id:?B generation ID must remain recorded}"
: "${candidate_c_generation_id:?C generation ID must remain recorded}"
: "${candidate_a_request_call_id:?A outer rollout request call ID is required}"
: "${candidate_b_request_call_id:?B outer rollout request call ID is required}"
: "${candidate_c_request_call_id:?C outer rollout request call ID is required}"
: "${rollout_path:?the exact rollout JSONL is required}"
test "$candidate_a_source" != "$candidate_b_source"
test "$candidate_a_source" != "$candidate_c_source"
test "$candidate_b_source" != "$candidate_c_source"
test "$candidate_a_event_saved_path" != "$candidate_b_event_saved_path"
test "$candidate_a_event_saved_path" != "$candidate_c_event_saved_path"
test "$candidate_b_event_saved_path" != "$candidate_c_event_saved_path"
test "$candidate_a_generation_id" != "$candidate_b_generation_id"
test "$candidate_a_generation_id" != "$candidate_c_generation_id"
test "$candidate_b_generation_id" != "$candidate_c_generation_id"
test "$candidate_a_request_call_id" != "$candidate_b_request_call_id"
test "$candidate_a_request_call_id" != "$candidate_c_request_call_id"
test "$candidate_b_request_call_id" != "$candidate_c_request_call_id"

expected_prompt_sha='19459cdff592ecb59a32dbce7f082f233e96e66e5a74a1383ef678773e9c572c'
expected_image_1='/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/build/v1.7-hairpin-45-continuity-r02/input/akari-v1.7-v17-03-hairpin-45-r01-a-authoritative-source.png'
expected_image_2='/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png'
python3 - "$rollout_path" "$expected_prompt_sha" "$expected_image_1" \
  "$expected_image_2" "$candidate_a_request_call_id" \
  "$candidate_b_request_call_id" "$candidate_c_request_call_id" \
  "$candidate_a_generation_id" "$candidate_b_generation_id" \
  "$candidate_c_generation_id" "$candidate_a_event_saved_path" \
  "$candidate_b_event_saved_path" "$candidate_c_event_saved_path" \
  "$candidate_a_source" "$candidate_b_source" \
  "$candidate_c_source" <<'PY'
import base64
import hashlib
import json
import pathlib
import sys

rollout = pathlib.Path(sys.argv[1])
expected_hash = sys.argv[2]
expected_paths = sys.argv[3:5]
request_ids = sys.argv[5:8]
generation_ids = sys.argv[8:11]
event_saved_paths = sys.argv[11:14]
local_source_paths = sys.argv[14:17]

events = []
with rollout.open("r", encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        events.append((line_number, json.loads(line)))

request_lines = {}
for request_id in request_ids:
    requests = []
    for line_number, event in events:
        if event.get("type") != "response_item":
            continue
        payload = event.get("payload", {})
        if payload.get("type") != "custom_tool_call":
            continue
        if payload.get("call_id") != request_id:
            continue
        request_input = payload.get("input")
        if isinstance(request_input, str):
            requests.append((line_number, request_input))
    if len(requests) != 1:
        raise SystemExit(f"{request_id}: expected one request, found {len(requests)}")
    line_number, request_input = requests[0]
    request_lines[request_id] = line_number
    marker = "referenced_image_paths"
    marker_index = request_input.index(marker)
    array_start = request_input.index("[", marker_index)
    array_end = request_input.index("]", array_start) + 1
    paths = json.loads(request_input[array_start:array_end])
    if paths != expected_paths:
        raise SystemExit(f"{request_id}: ordered inputs differ: {paths!r}")
    print(f"verified request={request_id} line={line_number} paths={paths!r}")

ordered_request_lines = [request_lines[request_id] for request_id in request_ids]
if ordered_request_lines != sorted(ordered_request_lines):
    raise SystemExit(f"request calls are not serial A/B/C: {ordered_request_lines}")

generation_lines = {}
for generation_id, event_saved_path, local_source_path in zip(
    generation_ids,
    event_saved_paths,
    local_source_paths,
):
    completed = []
    for line_number, event in events:
        if event.get("type") != "event_msg":
            continue
        payload = event.get("payload", {})
        if payload.get("type") != "image_generation_end":
            continue
        if payload.get("call_id") == generation_id:
            completed.append((line_number, payload))
    if len(completed) != 1:
        raise SystemExit(
            f"{generation_id}: expected one completion, found {len(completed)}"
        )
    line_number, payload = completed[0]
    generation_lines[generation_id] = line_number
    if payload.get("status") != "completed":
        raise SystemExit(f"{generation_id}: status is not completed")
    if payload.get("saved_path") != event_saved_path:
        raise SystemExit(
            f"{generation_id}: saved_path {payload.get('saved_path')!r} "
            f"!= {event_saved_path!r}"
        )
    result = payload.get("result")
    if not isinstance(result, str) or not result.startswith("iVBOR"):
        raise SystemExit(f"{generation_id}: missing PNG payload")
    payload_bytes = base64.b64decode(result, validate=True)
    if payload_bytes[:8].hex() != "89504e470d0a1a0a":
        raise SystemExit(f"{generation_id}: payload signature is not PNG")
    local_bytes = pathlib.Path(local_source_path).read_bytes()
    if hashlib.sha256(local_bytes).digest() != hashlib.sha256(payload_bytes).digest():
        raise SystemExit(
            f"{generation_id}: local source does not match correlated payload"
        )
    prompt = payload.get("revised_prompt")
    if not isinstance(prompt, str):
        raise SystemExit(f"{generation_id}: missing revised_prompt")
    actual_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if actual_hash != expected_hash:
        raise SystemExit(
            f"{generation_id}: prompt hash {actual_hash} != {expected_hash}"
        )
    print(
        f"verified generation={generation_id} line={line_number} "
        f"saved_path={event_saved_path} local_source={local_source_path} "
        f"prompt_sha256={actual_hash}"
    )

final_boundary = events[-1][0] + 1
for index, (request_id, generation_id) in enumerate(
    zip(request_ids, generation_ids)
):
    request_line = request_lines[request_id]
    next_request_line = (
        request_lines[request_ids[index + 1]]
        if index + 1 < len(request_ids)
        else final_boundary
    )
    generation_line = generation_lines[generation_id]
    if not request_line < generation_line < next_request_line:
        raise SystemExit(
            f"{request_id}: generation {generation_id} is outside its serial "
            f"request window {request_line}..{next_request_line}"
        )
    window_completions = []
    for line_number, event in events:
        if not request_line < line_number < next_request_line:
            continue
        if event.get("type") != "event_msg":
            continue
        payload = event.get("payload", {})
        if payload.get("type") != "image_generation_end":
            continue
        if payload.get("status") == "completed":
            window_completions.append(payload.get("call_id"))
    if window_completions != [generation_id]:
        raise SystemExit(
            f"{request_id}: completed events in serial window are "
            f"{window_completions!r}, expected [{generation_id!r}]"
        )
    print(
        f"correlated request={request_id} generation={generation_id} "
        f"window={request_line}<{generation_line}<{next_request_line}"
    )
PY
```

Expected: A, B, and C have pairwise-distinct request IDs, generation IDs,
event paths, and usable source paths. Each outer request resolves to one
literal ordered two-path array. Each serial request window contains exactly one
matching completed `image_generation_end`; its `saved_path` matches the
recorded event path, its decoded payload is byte-identical to the usable local
source even after recovery, and its `revised_prompt` SHA-256 matches the
immutable plan prompt.

If the installed rollout schema names the completed structural event
`image_generation_call` instead, or nests request arguments under a named
field, adapt only those structural field paths and record the exact JSON paths
in the task report. Retain the same one-request-per-call, one-completion-per-ID,
source-correlation, PNG-payload, prompt-hash, and ordered-path assertions. Do
not fall back to regex, prompt-text matching, or terminal-copy evidence.

- [ ] **Step 8: Inspect every candidate at original detail**

Open A, B, and C separately with `view_image` at original detail. Record a
complete verdict for every candidate in this exact order:

1. same adult age-25 person, face, amber gaze, quietly pleased expression, and
   preserved r01 A eye polish without front-reference pull;
2. exact r01 A hairpin-side 45-degree camera, same fixed moment, pose, crop,
   scale, apartment, light, and shadows;
3. corrected restrained near-side bust projection, softened new under-bust
   definition, subtle waist, and relaxed chest-to-waist shirt drape;
4. natural adult three-dimensionality without flattening, frontal silhouette,
   new shirt design, concealment, hip or thigh change, or wider body redesign;
5. unchanged shoulders, pelvis, hips, thighs, arms, hands, legs, feet, stance,
   shorts, and anatomically connected full figure;
6. unchanged airy bob, crossed pins, and the same compressed cord topology,
   ordering, attachment, loops, tails, color, and perspective;
7. unchanged framing, background, palette, line hierarchy, paint planes,
   hand-painted finish, and absence of artifacts or v1.6 drift.

Every gate is hard. Record all visible findings even after a failure. r01 A's
eye-polish and compressed-cord Minors are not failures when materially
unchanged, but any repair, worsening, or other change to them fails scope.
Surface polish cannot rescue a body-correction, front-pull, scope, anatomy, or
artifact failure.

- [ ] **Step 9: Build and inspect the labeled six-column comparison**

Run:

```bash
set -euo pipefail

magick montage \
  \( akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
     -set label 'Front / accepted' \) \
  \( akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png \
     -set label '30 deg / accepted' \) \
  \( build/v1.7-hairpin-45-continuity-r02/input/akari-v1.7-v17-03-hairpin-45-r01-a-authoritative-source.png \
     -set label '45 deg / r01 A' \) \
  \( build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png \
     -set label '45 deg / r02 A' \) \
  \( build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png \
     -set label '45 deg / r02 B' \) \
  \( build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
     -set label '45 deg / r02 C' \) \
  -tile 6x1 \
  -geometry 400x600+15+60 \
  -background '#eee8df' \
  -fill '#4d463f' \
  -pointsize 22 \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png)" = \
  "89504e470d0a1a0a"
identify -format '%f | %m %wx%h\n' \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png
sha256sum \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png
git check-ignore -v \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png
```

Expected: one readable PNG in the exact order `Front → 30° → r01 A →
r02 A → r02 B → r02 C`, with complete uncropped figures, clear labels,
and the same display geometry applied to all six equal-size source frames.
There is no individual normalization, crop, warp, or scale correction. Any
framing, pose, or character-scale drift remains visible as review evidence.

Open the comparison with `view_image` at original detail. Repeat all seven hard
gates left to right. Use the full-size candidates for face, ornament, shirt,
hands, feet, seams, and artifact calls.

- [ ] **Step 10: Obtain independent review and stop at user selection**

Have a reviewer who did not generate the images open the following at original
detail before issuing a verdict:

- worktree-local r01 A and accepted V17-01 front;
- accepted V17-02 30 degrees, v1.5 B3, v1.4 G2, inherited v1.1 45 degrees,
  and accepted v1.2 C03 45 degrees as the five human-QA-only controls;
- r02 A, B, and C separately;
- the six-column comparison.

The reviewer applies the exact seven gates independently and reports candidate
eligibility without seeing the executor's recommendation first.

Only if executor and reviewer disagree about a candidate's overall eligibility,
obtain one candidate-specific blind tie-break against the approved r02 design.
The tie-break resolves the disputed hard-gate findings that caused the
eligibility disagreement. Do not trigger a tie-break when both reviewers already
agree the candidate is ineligible, use a general favorite vote, or compare
finish before eligibility is resolved.

Before showing images or asking the blocking user-selection question, run:

```bash
set -euo pipefail

git diff --quiet
git diff --cached --quiet
git check-ignore -v \
  build/v1.7-hairpin-45-continuity-r02/input/akari-v1.7-v17-03-hairpin-45-r01-a-authoritative-source.png \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-a.png \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-b.png \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png
git status --short --branch
```

Expected: both tracked-diff assertions pass; the verified input copy and all
r02 review output are ignored; the execution branch remains tracked-clean; and
all r01 evidence remains untouched. This image-review task intentionally
creates no tracked implementation commit.

After those assertions pass, summarize for the user:

- A, B, and C completed generation artifact IDs, outer rollout request call
  IDs, event-recorded paths, and exact distinct usable source paths;
- source/destination byte-identity results, dimensions, signatures, and
  SHA-256 values;
- successful immutable-prompt and ordered-input verification for all calls;
- executor, independent-reviewer, and any eligibility tie-break verdict for all
  seven gates with every Minor finding;
- selectable candidates, if any, and the strongest localized correction,
  same-person read, natural body volume, and finish among passers;
- absolute paths to the comparison and every candidate.

Show the comparison and any candidate needing full-size review. Ask the user to
select a passing A, B, or C, keep r01 A unchanged, or return to design. If none
passes, preserve all evidence and return to design.

Do not promote, repair, composite, generate r03, commit, push, merge, clean up,
or modify selection history in this task, even after the user selects a
candidate.

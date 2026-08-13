# Akari V2.2 Uniform School-Day Scenes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review a coherent four-image Akari V2.2 school-day mini-series in one fixed jumperskirt uniform, after two identity-gated diagnostic transitions.

**Architecture:** Every candidate is a separate built-in `image_gen.imagegen` call whose sole image input is the canonical portrait. The route advances serially through U00, U01, S01, S02, S03, and S04; each output is copied into one ignored review directory, compared against the canonical portrait and latest approved face, and held at `identity_pending` until the user explicitly approves identity.

**Tech Stack:** Built-in `image_gen.imagegen`, local `view_image`, ImageMagick 7 (`identify`, `magick`, `montage`), Bash, Git-ignored PNG and Markdown review artifacts.

## Global Constraints

- Sole generation input: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`.
- Do not pass the canonical full-body image, P00, U00/U01, S01-S04, accepted daily scenes, GPT Pro examples, or local composition images into any generation call.
- Use `referenced_image_paths` with exactly the canonical portrait path; do not use `num_last_images_to_include`.
- Generate exactly one image per call and never forward a generated face into a later call.
- Fixed uniform: a white short-sleeve blouse under a navy jumperskirt dress; use a plain navy school bag only when the scene calls for it.
- Camera range: chest-up through knee-up; no full-body, extreme angle, distant camera, or complex motion.
- Preserve warm chestnut hair, bangs, a low side ponytail with blue tie, and exactly one blue capsule hairpin on viewer-right.
- The face remains the largest, clearest focal point, with one shared light direction and consistent line and paint density across character and environment.
- Stop after each candidate for identity-only review. Scene, wardrobe, or general approval does not imply identity approval.
- A rejected, deferred, unreadable, or unapproved output may be used only for diagnosis and its own comparison artifact; never use it as an image input, edit target, anchor, composite source, crop source for continuity, or prompt-derived continuity description.
- Save all prompts, candidates, crops, comparison artifacts, and state under `tmp/akari-v22-uniform-school-day-2026-08-13/`; do not add them to Git.
- Do not copy a candidate into `akari-v2.2/accepted/`, edit manifests, or commit generated images without a separate explicit user acceptance decision.

---

### Task 1: Verify authorities and initialize the ignored review run

**Files:**

- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `/home/takahiro/.codex/generated_images/019ff88d-af00-7812-9198-d5cad1f65503/exec-eb77b3ca-e653-4fd2-b113-19fb04a3e04b.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/run-record.md`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/build-identity-comparison.sh`

**Interfaces:**

- Consumes: the repository canonical portrait and the previously identity-approved P00 comparison control.
- Produces: verified authority hashes, an ignored run ledger, and a reusable comparison builder that never modifies its source images.

- [ ] **Step 1: Verify the canonical portrait and P00 control**

Run:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  /home/takahiro/.codex/generated_images/019ff88d-af00-7812-9198-d5cad1f65503/exec-eb77b3ca-e653-4fd2-b113-19fb04a3e04b.png
sha256sum \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  /home/takahiro/.codex/generated_images/019ff88d-af00-7812-9198-d5cad1f65503/exec-eb77b3ca-e653-4fd2-b113-19fb04a3e04b.png
```

Expected:

- Canonical portrait: readable `1888x3344` sRGB image with SHA-256 `b076afd95be49c4ed9c5a4ddfb4083c9ead8328313b4d5fa0555a374dd10543c`.
- P00: readable `942x1669` image with SHA-256 `df013000f147b84ee834940cff8fe331b2df825c1fed9d33be3b624d70923dfb`.
- Stop before generation if either path or hash does not match.

- [ ] **Step 2: Open both identity references at original detail**

Use `view_image` separately for the canonical portrait and P00. Confirm these roles:

- Canonical portrait: sole generation input and sole identity authority.
- P00: identity-approved comparison control only; never a generation input or continuity anchor.

- [ ] **Step 3: Create the run directory and initial ledger**

Run `mkdir -p tmp/akari-v22-uniform-school-day-2026-08-13/`. Create `run-record.md` with `apply_patch` and record:

- date and route name;
- canonical and P00 paths, dimensions, hashes, and roles;
- built-in route using one local reference path per call;
- initial states `U00: not_generated`, `U01: blocked_by_U00`, `S01: blocked_by_U01`, `S02: blocked_by_S01`, `S03: blocked_by_S02`, and `S04: blocked_by_S03`;
- the prohibition on using any generated candidate as a later input.

- [ ] **Step 4: Create the comparison builder**

Create `build-identity-comparison.sh` with `apply_patch`. It must accept seven arguments in this order: canonical path, approved-control path, candidate path, output path, canonical crop geometry, control crop geometry, and candidate crop geometry. For each face source, it must crop without rotation or distortion, resize the manually selected square crop to `700x700`, add a `64`-pixel label band, contain the full candidate within `700x700`, and assemble a neutral `2x2` montage labelled `Canonical`, `Approved control`, `Candidate`, and `Full frame`.

Use this implementation:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 7 ]]; then
  echo "usage: $0 CANONICAL CONTROL CANDIDATE OUTPUT CANON_GEOM CONTROL_GEOM CAND_GEOM" >&2
  exit 2
fi

canonical=$1
control=$2
candidate=$3
output=$4
canon_geom=$5
control_geom=$6
cand_geom=$7
review_tmp=$(mktemp -d)
trap 'rm -rf "$review_tmp"' EXIT

make_face_panel() {
  local source_path=$1
  local geometry=$2
  local label=$3
  local stem=$4
  magick "$source_path" -crop "$geometry" +repage -resize 700x700 \
    "$review_tmp/$stem-crop.png"
  magick "$review_tmp/$stem-crop.png" -background '#f7f2ec' -gravity north \
    -splice 0x64 -fill '#2f2925' -font DejaVu-Sans -pointsize 28 \
    -annotate +0+17 "$label" "$review_tmp/$stem-panel.png"
}

make_face_panel "$canonical" "$canon_geom" "Canonical" canonical
make_face_panel "$control" "$control_geom" "Approved control" control
make_face_panel "$candidate" "$cand_geom" "Candidate" candidate

magick "$candidate" -resize 700x700 -background '#f7f2ec' -gravity center \
  -extent 700x700 "$review_tmp/full-base.png"
magick "$review_tmp/full-base.png" -background '#f7f2ec' -gravity north \
  -splice 0x64 -fill '#2f2925' -font DejaVu-Sans -pointsize 28 \
  -annotate +0+17 'Full frame' "$review_tmp/full-panel.png"

magick montage \
  "$review_tmp/canonical-panel.png" \
  "$review_tmp/control-panel.png" \
  "$review_tmp/candidate-panel.png" \
  "$review_tmp/full-panel.png" \
  -tile 2x2 -geometry +16+16 -background '#ddd3c9' "$output"
```

- [ ] **Step 5: Verify the helper and ignored boundary**

Run:

```bash
bash -n tmp/akari-v22-uniform-school-day-2026-08-13/build-identity-comparison.sh
git check-ignore -v tmp/akari-v22-uniform-school-day-2026-08-13/
git status --short --branch
```

Expected: Bash syntax passes, `tmp/` is ignored, and no generated/review file appears in Git status.

### Task 2: Generate and review U00 wardrobe transition

**Files:**

- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `/home/takahiro/.codex/generated_images/019ff88d-af00-7812-9198-d5cad1f65503/exec-eb77b3ca-e653-4fd2-b113-19fb04a3e04b.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/u00-wardrobe-transition.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/u00-identity-comparison.png`
- Modify: `tmp/akari-v22-uniform-school-day-2026-08-13/run-record.md`

**Interfaces:**

- Consumes: verified canonical portrait and identity-approved P00 comparison control from Task 1.
- Produces: one independent U00 candidate and one identity-only comparison artifact; U01 remains blocked until explicit user identity approval.

- [ ] **Step 1: Re-open the sole generation input immediately before the call**

Use `view_image` at original detail on the canonical portrait. Confirm that it is Image A and the only path to be supplied to `referenced_image_paths`.

- [ ] **Step 2: Generate exactly one U00 candidate**

Call `image_gen.imagegen` once with `referenced_image_paths` containing only the canonical portrait and this prompt:

```text
Image A is the sole authority for Akari V2.2's face and hair.

Create the same Akari shown in Image A, preserving the relationships among her face, eyes, brows, cheeks, and mouth, plus her bangs, low side ponytail with blue tie, and exactly one blue capsule hairpin on viewer-right.

She wears a crisp white short-sleeve blouse under a simple navy jumperskirt dress. Do not add a school bag, apron, cardigan, blazer, neck ribbon, or alternate uniform layer.

In a warm morning kitchen, show her knee-up at a gentle three-quarter angle, looking toward the viewer with the same bright open smile and a simple open-palm presenting gesture. A plate of omurice rests flat on the counter as a small secondary element. Use soft window light, navy-and-white color echoes, and counter lines to return attention to her large, clearly readable face.

Render Akari and the kitchen as one clean, soft V2.2 illustration with a shared light direction and consistent line and paint density. Avoid facial redesign or re-aging, left-right reversal, broken hand or object contact, readable text, and watermarks.
```

Do not include P00, the full-body authority, T01/T02, or any other image. Forward the generated image in the conversation, record the returned generation ID and source output path, and copy the PNG non-destructively to `u00-wardrobe-transition.png`.

- [ ] **Step 3: Validate and inspect U00**

Run:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  tmp/akari-v22-uniform-school-day-2026-08-13/u00-wardrobe-transition.png
sha256sum tmp/akari-v22-uniform-school-day-2026-08-13/u00-wardrobe-transition.png
```

Open the local PNG with `view_image` at original detail. Stop the route as an obvious mismatch if the face is not plausibly Akari, the face is too small to compare, the image is full-body, or the output misses the requested camera range. Otherwise record `U00: identity_pending`.

- [ ] **Step 4: Build U00's four-panel comparison**

Use original-detail inspection to select three square crop rectangles that contain the top of the hair, both eyes, cheeks, chin, and a small margin while keeping the displayed head scale equal. Record the exact `WIDTHxHEIGHT+X+Y` rectangles in the ledger. Do not rotate, align landmarks, warp, retouch, or compensate for face shape.

Run the comparison builder with:

- canonical portrait as `Canonical`;
- P00 as `Approved control`;
- U00 as `Candidate` and `Full frame`;
- output `u00-identity-comparison.png`.

Then run:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  tmp/akari-v22-uniform-school-day-2026-08-13/u00-identity-comparison.png
```

- [ ] **Step 5: Present identity only and stop**

Show the comparison artifact and ask only whether U00 preserves Akari's identity. Do not ask about wardrobe selection, scene quality, acceptance, or anchor transfer in the same question. Stop until the user explicitly says identity passes.

### Task 3: Generate and review U01 scene transition

**Files:**

- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/u00-wardrobe-transition.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/u01-station-transition.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/u01-identity-comparison.png`
- Modify: `tmp/akari-v22-uniform-school-day-2026-08-13/run-record.md`

**Interfaces:**

- Consumes: explicit U00 identity approval; U00 is comparison-only and is never passed to the generator.
- Produces: one independent U01 candidate and identity comparison; S01 remains blocked until explicit U01 identity approval.

- [ ] **Step 1: Record the U00 decision and re-open the canonical portrait**

Change `U00` to `identity_approved` only when the user's response explicitly concerns identity. Set `U01: identity_pending`, then use `view_image` on the canonical portrait immediately before generation.

- [ ] **Step 2: Generate exactly one U01 candidate**

Call `image_gen.imagegen` once with only the canonical portrait path and this prompt:

```text
Image A is the sole authority for Akari V2.2's face and hair.

Create the same Akari shown in Image A, preserving the relationships among her face, eyes, brows, cheeks, and mouth, plus her bangs, low side ponytail with blue tie, and exactly one blue capsule hairpin on viewer-right.

She wears the same crisp white short-sleeve blouse under a simple navy jumperskirt dress and carries a plain navy school bag.

In clear morning light, show her paused on a quiet Japanese station platform, knee-up at a gentle three-quarter angle, looking toward the viewer with a bright open smile. One hand rests naturally on the bag strap. Use the platform edge and canopy lines, restrained blue-and-white echoes, and open background space to guide attention back to her large, clearly readable face.

Render Akari and the station as one clean, soft V2.2 illustration with a shared light direction and consistent line and paint density. Avoid facial redesign or re-aging, left-right reversal, broken hand or bag contact, readable signs or text, and watermarks.
```

Copy the returned PNG to `u01-station-transition.png`, record generation ID, source path, dimensions, hash, prompt, and `U01: identity_pending`.

- [ ] **Step 3: Inspect, compare, and stop**

Open U01 at original detail. Stop on obvious mismatch, unreadable face, full-body framing, or broken bag contact. Otherwise build `u01-identity-comparison.png` using canonical portrait, identity-approved U00 as the approved comparison control, and U01 as candidate/full frame. Record exact crops, validate the artifact with `identify`, show it, and ask only whether U01 preserves Akari's identity. Do not generate S01 before explicit approval.

### Task 4: Generate and review S01 morning station

**Files:**

- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/u01-station-transition.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/s01-morning-station.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/s01-identity-comparison.png`
- Modify: `tmp/akari-v22-uniform-school-day-2026-08-13/run-record.md`

**Interfaces:**

- Consumes: explicit U01 identity approval; U01 remains comparison-only.
- Produces: the first requested scene, held at `identity_pending` until explicit approval.

- [ ] **Step 1: Record U01 approval and generate S01 independently**

Re-open the canonical portrait, then call `image_gen.imagegen` once with only that path and this prompt:

```text
Image A is the sole authority for Akari V2.2's face and hair.

Create the same Akari shown in Image A, preserving the relationships among her face, eyes, brows, cheeks, and mouth, plus her bangs, low side ponytail with blue tie, and exactly one blue capsule hairpin on viewer-right.

She wears a crisp white short-sleeve blouse under a simple navy jumperskirt dress and carries a plain navy school bag.

Make a finished morning-commute illustration on a quiet Japanese station platform. Frame her knee-up in a shallow three-quarter view, with one hand resting naturally on the bag strap and a bright open smile toward the viewer. Crisp morning light, repeating navy and sky-blue accents, and receding platform lines should make her large, readable face the unmistakable focal point.

Render Akari and the station as one clean, soft V2.2 illustration with a shared light direction and consistent line and paint density. Avoid facial redesign or re-aging, left-right reversal, broken hand or bag contact, readable signs or text, and watermarks.
```

Copy and validate the PNG as `s01-morning-station.png`; record generation metadata, prompt, hash, and `S01: identity_pending`.

- [ ] **Step 2: Inspect, compare, and stop**

Open S01 at original detail. Stop for any obvious identity mismatch, unreadable face, out-of-range framing, or major contact failure. Otherwise build `s01-identity-comparison.png` with canonical portrait, identity-approved U01 control, and S01 candidate/full frame. Record exact crops, validate and show the artifact, and ask only whether S01 preserves Akari's identity. Do not generate S02 before explicit approval.

### Task 5: Generate and review S02 daytime classroom

**Files:**

- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/s01-morning-station.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/s02-daytime-classroom.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/s02-identity-comparison.png`
- Modify: `tmp/akari-v22-uniform-school-day-2026-08-13/run-record.md`

**Interfaces:**

- Consumes: explicit S01 identity approval; S01 is comparison-only.
- Produces: the second requested scene, held at `identity_pending` until explicit approval.

- [ ] **Step 1: Record S01 approval and generate S02 independently**

Re-open the canonical portrait, then call `image_gen.imagegen` once with only that path and this prompt:

```text
Image A is the sole authority for Akari V2.2's face and hair.

Create the same Akari shown in Image A, preserving the relationships among her face, eyes, brows, cheeks, and mouth, plus her bangs, low side ponytail with blue tie, and exactly one blue capsule hairpin on viewer-right.

She wears the same crisp white short-sleeve blouse under a simple navy jumperskirt dress. The school bag is not visible in this classroom view.

In a quiet daytime classroom near a window, show her seated waist-up while gently closing a blank notebook. Her gaze follows her hands with a soft, task-focused expression rather than looking at the viewer. Diffuse window daylight, pale desk planes, and restrained navy accents should frame and return attention to her clearly readable face without crowding it.

Render Akari and the classroom as one clean, soft V2.2 illustration with a shared light direction and consistent line and paint density. Avoid facial redesign or re-aging, left-right reversal, broken hand or notebook contact, readable writing or text, and watermarks.
```

Copy and validate the PNG as `s02-daytime-classroom.png`; record generation metadata, prompt, hash, and `S02: identity_pending`.

- [ ] **Step 2: Inspect, compare, and stop**

Open S02 at original detail. Stop for any obvious identity mismatch, unreadable face, repeated direct gaze/open-smile expression, or broken notebook contact. Otherwise build `s02-identity-comparison.png` with canonical portrait, identity-approved S01 control, and S02 candidate/full frame. Record exact crops, validate and show the artifact, and ask only whether S02 preserves Akari's identity. Do not generate S03 before explicit approval.

### Task 6: Generate and review S03 after-school corridor

**Files:**

- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/s02-daytime-classroom.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/s03-after-school-corridor.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/s03-identity-comparison.png`
- Modify: `tmp/akari-v22-uniform-school-day-2026-08-13/run-record.md`

**Interfaces:**

- Consumes: explicit S02 identity approval; S02 is comparison-only.
- Produces: the third requested scene, held at `identity_pending` until explicit approval.

- [ ] **Step 1: Record S02 approval and generate S03 independently**

Re-open the canonical portrait, then call `image_gen.imagegen` once with only that path and this prompt:

```text
Image A is the sole authority for Akari V2.2's face and hair.

Create the same Akari shown in Image A, preserving the relationships among her face, eyes, brows, cheeks, and mouth, plus her bangs, low side ponytail with blue tie, and exactly one blue capsule hairpin on viewer-right.

She wears the same crisp white short-sleeve blouse under a simple navy jumperskirt dress and carries a plain navy school bag.

In an after-school corridor, show her knee-up from a gentle diagonal view as she walks slowly and turns her head back toward the viewer. Give her a small, lightly surprised smile rather than the broad morning smile. Warm side light and long corridor lines should catch the hair and uniform edges while leading attention back to her large, readable face.

Render Akari and the corridor as one clean, soft V2.2 illustration with a shared light direction and consistent line and paint density. Avoid facial redesign or re-aging, left-right reversal, broken walking anatomy or bag contact, readable signs or text, and watermarks.
```

Copy and validate the PNG as `s03-after-school-corridor.png`; record generation metadata, prompt, hash, and `S03: identity_pending`.

- [ ] **Step 2: Inspect, compare, and stop**

Open S03 at original detail. Stop for any obvious identity mismatch, unreadable face, complex or broken motion, repeated classroom pose, or major bag-contact failure. Otherwise build `s03-identity-comparison.png` with canonical portrait, identity-approved S02 control, and S03 candidate/full frame. Record exact crops, validate and show the artifact, and ask only whether S03 preserves Akari's identity. Do not generate S04 before explicit approval.

### Task 7: Generate and review S04 evening walk home

**Files:**

- Read: `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/s03-after-school-corridor.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/s04-evening-walk-home.png`
- Create: `tmp/akari-v22-uniform-school-day-2026-08-13/s04-identity-comparison.png`
- Modify: `tmp/akari-v22-uniform-school-day-2026-08-13/run-record.md`

**Interfaces:**

- Consumes: explicit S03 identity approval; S03 is comparison-only.
- Produces: the fourth requested scene, held at `identity_pending` until explicit approval.

- [ ] **Step 1: Record S03 approval and generate S04 independently**

Re-open the canonical portrait, then call `image_gen.imagegen` once with only that path and this prompt:

```text
Image A is the sole authority for Akari V2.2's face and hair.

Create the same Akari shown in Image A, preserving the relationships among her face, eyes, brows, cheeks, and mouth, plus her bangs, low side ponytail with blue tie, and exactly one blue capsule hairpin on viewer-right.

She wears the same crisp white short-sleeve blouse under a simple navy jumperskirt dress and carries a plain navy school bag.

Show a quiet evening walk home beside a simple neighborhood fence, framed knee-up in a relaxed walking moment. Her gaze is slightly off-camera with a calm closed-mouth smile. Amber late-day backlight should rim her hair and shoulders, while the fence rhythm and cool navy uniform balance the warm sky and return attention to her large, readable face.

Render Akari and the neighborhood as one clean, soft V2.2 illustration with a shared light direction and consistent line and paint density. Avoid facial redesign or re-aging, left-right reversal, broken walking anatomy or bag contact, readable signs or text, and watermarks.
```

Copy and validate the PNG as `s04-evening-walk-home.png`; record generation metadata, prompt, hash, and `S04: identity_pending`.

- [ ] **Step 2: Inspect, compare, and stop**

Open S04 at original detail. Stop for any obvious identity mismatch, unreadable face, repeated direct gaze/open smile, complex or broken motion, or major bag-contact failure. Otherwise build `s04-identity-comparison.png` with canonical portrait, identity-approved S03 control, and S04 candidate/full frame. Record exact crops, validate and show the artifact, and ask only whether S04 preserves Akari's identity.

### Task 8: Audit the approved four-scene set and hold preservation boundary

**Files:**

- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/s01-morning-station.png`
- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/s02-daytime-classroom.png`
- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/s03-after-school-corridor.png`
- Read: `tmp/akari-v22-uniform-school-day-2026-08-13/s04-evening-walk-home.png`
- Modify: `tmp/akari-v22-uniform-school-day-2026-08-13/run-record.md`

**Interfaces:**

- Consumes: explicit identity approval for S01, S02, S03, and S04.
- Produces: a locally retained, technically reviewed four-image set and a separate user acceptance gate; it does not promote or track files.

- [ ] **Step 1: Record S04 identity approval and inspect the set together**

Open all four full frames. Review identity first as already approved, then check the fixed uniform construction, one viewer-right hairpin, hand and bag/notebook contact, anatomy, spatial support, accidental text, watermarks, and image artifacts.

- [ ] **Step 2: Verify deliberate scene variation**

Confirm that the four outputs do not repeat the same mouth shape, direct gaze, pose, or background geometry, and that each scene matches its requested time, place, crop, action, and light. Record each technical check as `pass` or a concrete failure in the ledger; do not let background or outfit quality compensate for an identity failure.

- [ ] **Step 3: Verify files and Git boundary**

Run:

```bash
identify -format '%f %wx%h %[colorspace]\n' \
  tmp/akari-v22-uniform-school-day-2026-08-13/s01-morning-station.png \
  tmp/akari-v22-uniform-school-day-2026-08-13/s02-daytime-classroom.png \
  tmp/akari-v22-uniform-school-day-2026-08-13/s03-after-school-corridor.png \
  tmp/akari-v22-uniform-school-day-2026-08-13/s04-evening-walk-home.png
git check-ignore -v tmp/akari-v22-uniform-school-day-2026-08-13/
git status --short --branch
```

Expected: four readable sRGB images, all run artifacts ignored, and no newly tracked generated images.

- [ ] **Step 4: Present the set and ask for a separate acceptance decision**

Show the four full images together with the concise technical audit. Ask whether the set should be accepted or whether a specific scene should be rejected. Do not copy, promote, edit manifests, or commit images until the user explicitly requests preservation.

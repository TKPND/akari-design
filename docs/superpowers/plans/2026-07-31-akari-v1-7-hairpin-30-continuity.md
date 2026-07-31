# Akari v1.7 Hairpin-Side 30-Degree Continuity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and review three independent Akari v1.7 hairpin-side
30-degree full-body candidates without weakening the accepted V17-01 front
identity or promoting an unselected image.

**Architecture:** Supply only the accepted v1.7 front PNG to image generation
and run one immutable prompt three times serially. Keep all outputs in an
ignored review directory, validate and inspect every PNG, build one labeled
equal-scale comparison, and return to the user for explicit selection.

**Tech Stack:** Built-in `image_gen`, local `view_image`, ImageMagick
`identify` and `magick montage`, `xxd`, SHA-256, Git read-only checks, and the
repository rollout-payload recovery procedure.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-continuity-design.md`.
- Before any generation call, read and follow the local `imagegen` skill.
- Supply only
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png` to image
  generation.
- The sole generation input must have SHA-256
  `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`.
- Open the v1.5 B3, v1.4 G2, and inherited hairpin-side 45-degree images for
  human QA only. Do not pass them to image generation.
- Generate A, B, and C independently with the exact same prompt, reference,
  and target view. Never chain candidates or add candidate-specific deltas.
- Generate serially. Do not overlap image-generation or comparison work.
- Preserve the accepted identity, age 25, quietly pleased expression, hair,
  ornament, body balance, roomwear, bare feet, apartment light, framing, and
  hand-painted finish while changing only the coherent camera viewpoint.
- Keep all review output under ignored
  `build/v1.7-hairpin-30-continuity/`.
- Do not modify accepted assets, references, v1.6 material, manifests,
  validators, rendering code, audit code, or release packages.
- Do not promote a candidate or create an accepted angle asset before the
  user's explicit selection.
- If no r01 candidate passes, stop at a design decision. Do not generate r02
  or run an automatic correction loop.
- Do not run Python tests, Node tests, PDF builds, OCR, release gates, or
  package validation.

---

### Task 1: Generate and review V17-02 r01 A/B/C

**Files:**

- Read:
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-continuity-design.md`
- Read and supply to image generation:
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`
- Inspect for human QA only:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
- Inspect for human QA only:
  `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
- Inspect for human QA only:
  `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png`
- Create:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png`
- Create:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-b.png`
- Create:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-c.png`
- Create:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-comparison.png`

**Interfaces:**

- Consumes: one hash-pinned accepted v1.7 front authority plus three
  hash-pinned human-only QA images.
- Produces: three independent ignored PNG candidates, one ignored comparison,
  and a review report with a recommendation; no tracked asset or commit.

- [ ] **Step 1: Verify sources, tools, output boundary, and Git state**

Run:

```bash
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
identify -format '%f | %m %wx%h\n' \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png \
  akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png
command -v magick
command -v identify
command -v sha256sum
command -v xxd
git check-ignore -v build/v1.7-hairpin-30-continuity/probe.png
git status --short --branch
mkdir -p build/v1.7-hairpin-30-continuity
```

Expected:

- all four hashes match the global constraints and design specification;
- all four visual inputs are readable images;
- required local tools resolve;
- `build/` is confirmed ignored;
- the tracked tree is clean before review output is created.

- [ ] **Step 2: Open and state every reference role**

Use `view_image` with original detail for the accepted v1.7 front authority
and all three human QA images. State these roles immediately before the first
generation call:

- v1.7 V17-01 accepted front is the sole generation input and controls the
  current identity, adult age, expression, face, eyes, hair, ornament, body,
  stance, outfit, bare feet, background, light, framing, palette, lines, and
  finish;
- v1.5 B3 checks inherited head-to-body ratio, restrained upper-body volume,
  healthy thighs, and full-body balance after generation;
- v1.4 G2 checks line hierarchy, paint planes, adult-face direction, palette,
  and finish after generation;
- inherited hairpin-side 45 degrees checks only cheek, bob, and ornament
  perspective topology after generation.

Keep the images visible in the conversation context. Do not include the three
QA-only paths in `referenced_image_paths`.

- [ ] **Step 3: Generate candidate A from the immutable prompt**

Use the built-in `image_gen` with exactly one referenced image path:

```text
/home/takahiro/workspace/akari-design/akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png
```

Use this complete prompt as the immutable prompt constant for A, B, and C:

```text
Use case: identity-preserving novel-view character continuity generation.
Asset: Akari v1.7 V17-02 hairpin-side 30-degree continuity probe, r01.

Image 1 is the SOLE visual authority. It is the accepted current Akari v1.7
front baseline and controls the same woman, age 25, identity, face design,
quietly pleased expression, hair, ornament, body balance, outfit, bare feet,
warm apartment presentation, palette, line hierarchy, paint planes, and
hand-painted finish. Do not blend another character interpretation into her.

Primary request:
Create a new full-resolution 1024 x 1536 portrait image of the same Akari as
Image 1 from a coherent 30-degree view toward her character-left, hairpin
side. The virtual camera has moved from the accepted front position around
toward Akari's own left side, which is the ornament side shown on image-right
in the front reference. Her character-left cheek and complete pale-blue
ornament are nearer the camera and more visible. This is a true modest
three-quarter camera view, not a mirrored image and not a frontal body with an
independent head turn.

View and expression:
- Keep head, ribcage, pelvis, knees, and feet aligned in one coherent
  hairpin-side 30-degree orientation.
- Do not rotate the head independently back to a frontal face.
- Keep both amber eyes visible and let them track the camera naturally for
  familiar direct eye contact.
- Preserve the exact emotional beat from Image 1: a small closed-mouth smile,
  quietly and genuinely pleased after noticing the familiar viewer.
- Do not increase the smile, eye size, catchlights, blush, makeup, or glamour.

Exact character invariants:
- Preserve the adult age-25 face, soft cheek volume, compact chin, nose
  language, restrained blush, subtle lip color, and same-person read.
- Preserve eye size, opening, tilt, iris scale and density, amber color,
  highlight language, eyelids, lashes, line weight, and low-contrast brows.
- Preserve the short airy chestnut bob, asymmetric looseness, irregular tips,
  crown volume, low-gloss paint planes, and natural skull volume.
- Preserve one complete character-left ornament: two pale-blue crossed pins
  above a delicate thin cord bow with narrow loops and two slim tails. Keep it
  attached to the correct side in natural perspective; never mirror, move,
  duplicate, simplify, or replace it.
- Preserve the v1.5 B3-derived head-to-body ratio, moderate upper-body volume,
  subtle waist, healthy thigh volume, limb lengths, adult hands and feet, and
  neutral nearly even standing balance.
- Keep relaxed shoulders and arms, soft elbows, unlocked knees, both hands,
  both legs, and both bare feet complete and anatomically connected.

Exact image invariants:
- Preserve the same simple white T-shirt and pale-blue lounge shorts as
  comparison controls. Do not crop or redesign them.
- Preserve a warm minimal apartment, directional domestic light, quiet wall
  and floor, portrait framing, full-body scale, breathing room, warm palette,
  deliberate outer lines, quiet interior lines, readable paint planes, and
  hand-painted finish.
- Keep the full figure in frame from complete hair to complete toes. No crop,
  zoom, extreme foreshortening, camera tilt, wide-angle distortion, or
  dramatic perspective.
- Natural overlap from the 30-degree view is required, but do not collapse,
  thin, hide, or disconnect the farther shoulder, hip, thigh, knee, ankle, or
  foot.

Avoid:
No wrong-side view, mirrored composition, near-front substitute, exact
45-degree view, profile, separate head turn, contrapposto, fashion-model hip
shift, walking step, crossed legs, pin-up pose, broad smile, open mouth,
teeth, teasing, smugness, seduction, gyaru styling, oversized or rounder eyes,
heavy lashes, eyeliner, cosmetic makeup, strong blush, tan drift, childlike
face or body, sharp V jaw, smooth salon-finished round bob, bright Honey Brown
hair, repeated glossy highlight bands, parallel-pin substitution, reduced
upper-body volume, thin thighs, model elongation, exaggerated curves, cropped
T-shirt, culottes, smartwatch, jewelry, socks, sneakers, white studio
background, cool uniform lighting, generic polished character sheet,
photorealistic skin, plastic smoothing, text, label, border, logo, or
watermark.
```

Record the returned generation or request identifier and exact source path.
Do not generate candidate B until A is saved and verified.

- [ ] **Step 4: Save and verify candidate A**

Copy the exact returned source PNG without transformation to:

```text
build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png
```

Do not move or delete the generation tool's source. Run:

```bash
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png)" = \
  "89504e470d0a1a0a"
identify -format '%f | %m %wx%h\n' \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png
sha256sum \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png
```

Expected: signature check exits zero, `identify` reports `PNG 1024x1536`, and
SHA-256 prints one digest. A different size is a failed candidate for this
equal-scale comparison pass.

If the generated image is visible but no local source PNG is available, parse
the exact current-day rollout JSONL structurally. Extract the intended
`image_generation_call` item whose `result` begins with `iVBOR`, decode it,
verify the PNG signature before accepting it, and record the generation or
request identifier used. Never hand-copy base64 from terminal output.

- [ ] **Step 5: Generate and verify candidate B independently**

Call `image_gen` again with only the accepted v1.7 front path from Step 3 and
the exact immutable prompt constant from Step 3, byte-for-byte unchanged. Do
not reference candidate A or add a B-specific instruction.

Copy the exact returned source PNG without transformation to:

```text
build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-b.png
```

Run the same signature, `identify`, and SHA-256 checks from Step 4 against the
B path. Record B's generation or request identifier, exact source path,
dimensions, and digest. Use structural rollout recovery only if needed. Do
not generate C until B is saved and verified.

- [ ] **Step 6: Generate and verify candidate C independently**

Call `image_gen` a third time with only the accepted v1.7 front path from Step
3 and the exact immutable prompt constant from Step 3, byte-for-byte
unchanged. Do not reference A or B or add a C-specific instruction.

Copy the exact returned source PNG without transformation to:

```text
build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-c.png
```

Run the same signature, `identify`, and SHA-256 checks from Step 4 against the
C path. Record C's generation or request identifier, exact source path,
dimensions, and digest. Use structural rollout recovery only if needed. Do
not start another generation after C.

- [ ] **Step 7: Inspect each candidate at original detail**

Open A, B, and C separately with `view_image` at original detail. For every
candidate, record pass/fail findings in the specification's review order:

1. identity and adult age;
2. correct character-left hairpin side and coherent 30-degree head/body view;
3. ornament topology and bob volume;
4. accepted quietly pleased expression and familiar eye contact;
5. head-to-body ratio, upper-body volume, waist, thighs, limbs, stance, and
   full-body scale;
6. hands, feet, clothing, background, light, palette, lines, paint planes,
   and artifacts;
7. absence of v1.6, gyaru, polished-girl, childlike, glamorous, or generic
   character-sheet drift.

Reject a candidate immediately for any hard identity, view, ornament, body,
anatomy, or artifact failure, but still record all visible findings so a
failed round can inform a later design decision.

- [ ] **Step 8: Build and inspect the labeled comparison**

Run:

```bash
magick montage \
  \( akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
     -set label 'Front / Accepted' \) \
  \( build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png \
     -set label 'A' \) \
  \( build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-b.png \
     -set label 'B' \) \
  \( build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-c.png \
     -set label 'C' \) \
  -tile 2x2 \
  -geometry 720x1080+24+72 \
  -background '#eee8df' \
  -fill '#4d463f' \
  -pointsize 32 \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-comparison.png
identify -format '%f | %m %wx%h\n' \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-comparison.png
sha256sum \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-comparison.png
```

Expected: one readable 2-by-2 PNG comparison with full uncropped figures,
clear labels, equal display scale, and one recorded digest. If a candidate's
figure scale differs from the accepted front despite equal image display,
preserve that difference as review evidence rather than normalizing it away.

Open the comparison with `view_image` at original detail and re-evaluate the
same seven review dimensions across all four panels.

- [ ] **Step 9: Return to the explicit user selection gate**

Summarize:

- source or request identifiers, dimensions, and SHA-256 for A/B/C;
- hard-gate pass/fail for each candidate;
- the strongest passing candidate, if any, and why;
- any Minor findings on passing candidates;
- the comparison path and all individual candidate paths;
- confirmation that no tracked files changed and no prohibited test or
  release command ran.

Show the comparison and any candidate that needs full-size inspection. Ask
the user to select a passing candidate, keep the accepted front without an
angle, or return to design. Do not promote, commit, generate r02, or clean up
the r01 evidence as part of this task.

Run:

```bash
git status --short --branch
git check-ignore -v \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-a.png \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-b.png \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-c.png \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r01-comparison.png
```

Expected: the tracked tree remains clean and every review output is ignored.
This image-review task intentionally creates no commit.

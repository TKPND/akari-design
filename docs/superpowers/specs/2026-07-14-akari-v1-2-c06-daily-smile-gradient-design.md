# Akari v1.2 C06 Daily Smile Gradient Design

**Date:** 2026-07-14

**Scope:** C06-1 through C06-4 expression-gradient generation, comparison,
review, repair, and accepted-asset promotion for the Natural Form package

## Goal

Create and accept one four-image C06 expression set that carries the same
just-awake Akari from a sleepy neutral face through a soft everyday smile. The
four images must preserve the accepted C05 composition, morning hair, outfit,
lighting, backdrop, and identity closely enough that expression is the only
meaningful change when the images are viewed in sequence.

C06 is complete only when all four ordered stages have no unresolved Blocker
or Major, the user explicitly selects the complete set, all four accepted PNGs
are promoted byte-for-byte from their reviewed sources, and the Natural Form
validator confirms the complete lifecycle. Individual C06 stages cannot be
accepted or released separately.

## Fixed Decisions

- Use accepted C05 as the common edit source for every C06 image.
- Edit each stage directly from C05. Never feed C06-1 into C06-2 or otherwise
  chain generated C06 outputs.
- Use a 1024 x 1536 portrait canvas for every image.
- Lock composition, camera, crop, head angle, morning hair, ornament, hoodie,
  lighting, backdrop, and rendering across all four stages.
- Treat four-image continuity as more important than maximizing the isolated
  impact of any one image.
- Generate two complete initial candidate families, A and B, for eight initial
  outputs.
- Review and select complete ordered sets. Do not promote a partial set.
- Permit one targeted C-stage replacement only under the repair rules below.
- If drift affects multiple stages or global invariants, generate a complete C
  family rather than combining several isolated repairs.
- Keep candidates and comparisons local-only. Commit only durable contracts,
  tests, reference snapshots, review metadata, and the four selected PNGs.
- Do not push during the C06 workflow unless the user requests it separately.

## Accepted Deliverables

The accepted set has these four ordered paths:

```text
akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-1_sleepy-neutral_r01.png
akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png
akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-3_loosened-mouth_r01.png
akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-4_soft-smile_r01.png
```

Each file is one standalone portrait. A generated grid, expression sheet,
collage, multi-panel image, or multiple-character image cannot be promoted as
a C06 stage.

## Reference Snapshot

Copy the immutable source expression sheet byte-for-byte from:

```text
source/originals/v1_1_front_3.webp
```

to this canonical Natural Form reference path:

```text
akari-v1.2/references/v1.1/expression-grid.webp
```

The required SHA-256 digest is:

```text
2b70c639b320275cde6787263bd6fe0f88ad59068154e4c2439ae69502e6f919
```

Record the snapshot in `akari-v1.2/manifest/inheritance.yaml` with role
`v1.1-expression-range`, `inheritance_class: reference-only`, the exact source
and copied paths, the digest above, and a rationale limiting it to neutral,
relaxed-mouth, and soft-smile expression mechanics. Its open-mouth, laughing,
surprised, worried, pouting, yawning, and closed-eye examples are outside the
C06 target range and grant no authority over identity, crop, rendering, hair,
outfit, or background.

No legacy working path may be used directly. The existing C05-only sleepy and
morning-hair supporting images are intentionally excluded because accepted C05
already contains the state they established. Reintroducing them would add
conflicting hands, backgrounds, crops, lighting, or hair-strength signals.

## Ordered Reference Contract

Before every generation call, open the exact current versions of all four
references with `view_image`, keep them visible in context, and state every role
in the prompt in this order.

1. `accepted_c05_edit_source`
   - `akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png`
   - Primary edit target and controlling reference for composition, crop,
     camera, head angle, morning-hair state, ornament placement, hoodie,
     lighting, backdrop, rendering, and the sleepy-neutral starting state.
2. `accepted_c01_identity_crosscheck`
   - `akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png`
   - Controlling cross-check for the 25-year-old adult identity, healthy face
     width, rounded cheeks, compact chin, base eye construction, warm amber
     eyes, palette, and white oversized hoodie. It does not replace C05's crop,
     camera, or state.
3. `accepted_c03_hairpin_three_quarter`
   - `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png`
   - Controlling cross-check for the character-left pale-blue crossed pins and
     ribbon-like ornament, cheek silhouette, and short-bob side construction.
     It does not replace C05's crop or morning-hair irregularity.
4. `v1_1_expression_range`
   - `akari-v1.2/references/v1.1/expression-grid.webp`
   - Non-controlling reference for the progression from neutral lips through a
     relaxed mouth to a closed-mouth soft smile. Do not copy its grid layout,
     panel-specific face geometry, open-mouth expressions, extreme emotions,
     crop, or rendering.

Accepted C05 controls whenever another reference conflicts with the current
composition or state. C01 and C03 prevent the slightly narrow face and chin
recorded as a C05 Minor from becoming narrower or sharper in C06. The expression
grid controls no identity or scene property.

Keep the lifecycle declaration `depends_on: [C05]`. C01 and C03 are generation
cross-checks, not new lifecycle dependencies. The generation request still
requires their exact accepted paths so older or legacy identity images cannot
be substituted silently.

## Generation Request Contract

Add one request manifest:

```text
akari-v1.2/manifest/generation-requests/c06-r01.yaml
```

Use `asset_id: C06`, `revision: r01`, and
`variation_axis: expression_gradient_family_attempt`. The request declares:

- the four ordered reference roles above
- the accepted C05 path as the edit source for every call
- the ordered stages `sleepy-neutral`, `sleepy-secure`, `loosened-mouth`, and
  `soft-smile`
- complete initial A and B entries under `candidates`
- an inactive `repair_lane` that may become one targeted C stage or one
  complete C family, but not several unrelated stage repairs
- explicit `review_sets` that map each review ID to four ordered literal source
  paths independently of the generated-candidate grouping
- one shared invariant prompt plus exactly one stage-specific expression delta
- exact 1024 x 1536 output and production checks
- `acceptance_gates: [identity, state, rendering]`, with exact dimensions and
  path integrity enforced separately as production requirements
- the hard rejects in this design

Manifest `target_path` and review-log `source_paths` values are package-relative
and must use these canonical initial paths:

```text
source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-a.png
source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-a.png
source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-a.png
source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-a.png
source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-b.png
source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-b.png
source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-b.png
source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-b.png
```

On disk from the repository root, these files live below
`akari-v1.2/source/candidates/c06/r01/`. Never place the `akari-v1.2/` package
prefix inside manifest `target_path` or review-log `source_paths` values.

The initial request uses `repair_lane.mode: inactive`. Before any C generation
call, update, validate, and commit the request with exactly one of these modes:

- `targeted-stage`: declare base family A or B, one stage, its exact `-c.png`
  target path, and one assembled four-source `review_sets` entry
- `full-family`: append complete family C under `candidates` and add its exact
  four-source `review_sets` entry

The existing A and B review sets remain declared in either mode. The lifecycle
validator matches C06 reviews to `review_sets`, not directly to `candidates`.
Other asset types retain the current one-candidate-to-one-review behavior.
Declaring or activating the repair lane does not authorize hidden extra
attempts. Every returned image must occupy one declared path and remain
available for review.

Complete-family review IDs are `c06-r01-a`, `c06-r01-b`, and, when generated,
`c06-r01-c`. A targeted repair set uses the canonical ID
`c06-r01-<base>-repair-c06-<stage>`, such as
`c06-r01-a-repair-c06-3`. Its declared four-source mapping contains three
members of the named base family and the one matching C-stage path.

## Shared Image Invariants

All eight initial candidates must preserve these C05 properties:

- one naturally cute 25-year-old Akari
- near-eye-level, front-biased light three-quarter camera
- complete crown, outer short-bob silhouette, face outline, chin, shoulders,
  hoodie neckline, and upper chest
- both eyes and the complete character-left ornament
- the same one or two small crown lifts, lightly separated bangs, partial nape
  flick, lower-bob irregularity, and cheek-side strand
- the same short-bob length, warm-brown color, part direction, and side volume
- the same white oversized hoodie, shoulder volume, and neckline
- nearly plain warm off-white or pale neutral backdrop
- soft diffuse near-neutral light with no visible source, hard shadow, dramatic
  rim light, or room context
- about 70 px of advisory space above the hair and about 60 px beside it
- face placement in the vertical upper-middle

Do not add hands, props, furniture, a bed, window, room scene, text, logo,
watermark, border, grid, or another character. Do not alter hairstyle length,
ornament construction, outfit, crop, lens, body pose, head tilt, palette, blush,
or rendering strength to make one stage more expressive.

Face width, cheek volume, chin construction, base eye shape, iris size, nose,
ear placement, and age impression are identity invariants. Preserve C05's face
width consistently throughout each set and never make it narrower, sharper,
younger, or more doll-like as the smile grows. C01 and C03 are rejection
cross-checks for further drift; they do not authorize intentional face reshaping
that would differ between stages.

## Expression Stage Contract

Only upper-eyelid opening, lower-eyelid roundness, pupil focus, brow height and
angle, mouth corners, and cheek relaxation may vary across the sequence.

### C06-1: Sleepy Neutral

- Stay closest to C05's incompletely awake baseline.
- Use slightly heavy upper eyelids without materially shrinking the eyes.
- Keep the viewer-directed gaze softly unfocused.
- Keep brows relaxed and lips closed in a neutral line.
- Show no smile, sadness, distress, pout, yawn, or sensual emphasis.

### C06-2: Sleepy Secure

- Preserve nearly the same eyelid weight and low-energy gaze as C06-1.
- Soften the brow angle, lower eyelid, and cheek tension enough to read as safe
  and comfortable rather than blank.
- Keep the mouth closed and almost neutral; do not use a visible smile as the
  primary difference.
- The change from C06-1 must be readable at enlarged review without becoming a
  jump in alertness.

### C06-3: Loosened Mouth

- Preserve the secure, sleepy eyes and relaxed brows established by C06-2.
- Let the closed mouth relax and lift only minimally at the corners.
- Add slight cheek relaxation without narrowing the face or raising the cheeks
  into a full smile.
- It must read as the beginning of warmth, not yet as the final soft smile.

### C06-4: Soft Smile

- Use a clearly readable but small closed-mouth everyday smile.
- Coordinate both mouth corners, lower eyelids, brows, and cheeks without
  turning the expression into a grin.
- Retain some just-awake softness; do not become fully alert or performative.
- No teeth, open mouth, closed eyes, laughing face, strong blush, head tilt, or
  extra pose is allowed.

Across the four columns, comfort and mouth warmth must increase monotonically.
Eye opening may change only subtly and must not become the sole carrier of the
progression. No stage may reverse toward distress, blankness, or stronger
sleepiness after a later stage has become warmer.

## Prompt Architecture

Every generation call is an identity-preserving edit of accepted C05. The
prompt must name C05 as the edit target and describe the other three images as
cross-checks with the limited roles above.

Use one shared invariant prompt for all calls and one stage delta for each
column. Family A and family B receive identical prompts for the same stage; the
family letter represents only an independent generation attempt. Do not give A
and B different creative directions, smile strengths, lighting, framing, or
quality targets.

The stage delta may mention only the allowed expression controls. It must not
request redrawing the hair, ornament, outfit, crop, background, or pose. Do not
use any C06 output as a reference for another C06 output.

## Generation Order and Attempt Limits

Run the eight initial calls in this order:

1. A C06-1
2. A C06-2
3. A C06-3
4. A C06-4
5. B C06-1
6. B C06-2
7. B C06-3
8. B C06-4

Stop the initial round after eight successfully returned standalone images.
Each returned full image counts as an attempt even when it later fails visual
review.

A technical call that produces no image and no recoverable payload may be
retried once for the same declared target. If an image appears in the interface
but no local PNG exists, parse the current-date rollout structurally for an
`image_generation_call` result beginning with `iVBOR`, verify the decoded PNG
signature `89504e470d0a1a0a`, and save it to the declared path. Do not move a
large base64 payload through terminal output.

Check file type and exact dimensions immediately after every saved output. A
wrong-size or corrupt output is preserved locally and receives a production
Major; the same stage may use the declared C repair path instead of overwriting
the failed source.

## Repair Policy

Prefer a complete A or B family. A targeted C replacement is allowed only when:

- one leading family's other three members pass identity, invariants,
  rendering, and production gates
- exactly one stage has an expression-strength, expression-order, technical,
  or dimension problem
- the problem can be corrected by editing C05 directly with the unchanged
  shared prompt and that stage's existing delta
- no other stage needs a repair

Generate only that one C stage, assemble it with the three retained members of
the leading family, and review the resulting four-image set from the beginning.
The final review records the four literal source paths and hashes; it never
pretends the replacement came from A or B.

The targeted-repair and complete-C branches become mutually exclusive after a
C image is successfully returned. If the assembled targeted-repair set still
has an unresolved Blocker or Major, close r01 and design r02; do not overwrite
the C source, add another isolated C repair, or reinterpret it as a complete C
family.

If more than one stage fails, or if any failure involves identity, face
geometry, crop, hair, ornament, outfit, lighting, backdrop, or rendering drift
that could affect family comparability, generate a complete four-member C
family. Do not perform multiple isolated C repairs. If complete A, B, and C
families all fail, close r01 as rejected and design r02 from the observed
failure pattern.

Do not patch, mask, warp, blend, mirror, resize, or mechanically composite a
generated expression onto C05 or another candidate to rescue continuity.

## Candidate Comparison

Add a review-only artifact:

```text
akari-v1.2/comparisons/c06-r01/c06-r01-comparison.webp
```

The initial board is two rows by four columns:

- rows: family A, family B
- columns: C06-1, C06-2, C06-3, C06-4

Show every image at equal scale with consistent crop treatment. Label row,
stage number, and stage name outside the image area. Do not favor a family by
size, placement, or background. The board supports sequence review; the source
candidates remain standalone 1024 x 1536 PNGs.

Add a repository command named:

```text
build:v1-2:c06-comparison
```

Reuse existing image-loading, scaling, labeling, and WebP-writing patterns. A
thin C06 four-column layout is appropriate; do not redesign the C03/C07 paired
comparison behavior or introduce a general visual-layout framework.

If a targeted C repair is activated, rebuild the board with one additional
assembled-set row containing the three retained images and the literal C
replacement. If a complete C family is activated, add it as an ordinary third
family row.

## Review and Acceptance

Review each complete set in this order:

1. Identity: adult age, face width, cheeks, chin, base eye construction, bob,
   ornament, palette, and hoodie.
2. Invariants: crop, camera, head angle, hair state, outfit, backdrop, lighting,
   and rendering remain stable across all four images.
3. Stage clarity: each image satisfies its named expression contract.
4. Gradient continuity: warmth increases without reversal or a sudden jump,
   and sleepiness is not expressed only by eye closure.
5. Rendering: face, eyes, mouth, hair, ornament, hoodie, background, and image
   surface contain no artifacts.
6. Production: exact dimensions, standalone composition, canonical paths,
   SHA-256 values, and manifest linkage.

Persist findings with the existing review-log category vocabulary. Face and
character-construction drift use `identity`; both per-stage expression clarity
and four-stage gradient continuity use `state`; drawing and surface artifacts
use `rendering`; dimensions, crop readability, paths, hashes, and file integrity
use `production`. Outfit or hair construction drift uses `identity` when it
changes the character and `rendering` when it is a local drawing defect. Do not
add `expression-sequence`, `invariants`, or `gradient-continuity` as new stored
category values.

Blocker or immediate-reject conditions include:

- severe identity, age, face-shape, chin, or base-eye drift
- corrupted, asymmetric, duplicated, or disconnected facial features
- missing, mirrored, relocated, duplicated, or redesigned ornament
- multiple characters, collage output, readable text, logo, or watermark

Major conditions include:

- material crop, head-angle, hairstyle, outfit, backdrop, lighting, palette,
  or rendering change between stages
- progressively narrower face, sharper chin, younger age, or larger doll-like
  eyes as the smile grows
- an expression stage that is indistinguishable from both neighbors
- a reversed or abrupt expression progression
- sleepiness shown mainly through closed or substantially shrunken eyes
- sadness, distress, pout, intoxication, illness, sensuality, strong blush,
  yawn, teeth, open mouth, laughter, or a performative grin
- wrong dimensions, corrupt file, or crop that prevents complete face-and-hair
  comparison

Minor findings may remain only when they do not compromise identity,
expression-stage clarity, monotonic continuity, production eligibility, or use
as D01 expression evidence. A strong isolated image never compensates for a
set-level identity or continuity failure.

The user makes the final set selection. Do not promote an assistant-only
ranking. The accepted review contains exactly four ordered source paths and
four lowercase SHA-256 digests matching C06-1 through C06-4. Record every
non-selected reviewed set as rejected. A repaired set records its literal mixed
variant mapping.

Promote the selected four source files byte-for-byte to the accepted paths.
Confirm every pair with `cmp` and matching SHA-256. Change the C06 asset to
`accepted` r01 only after all four files and the single accepted set review are
present and free of unresolved Blocker or Major findings.

## Validation Contract

Extend the Natural Form validator and focused tests to enforce:

- C06 depends on the exact accepted C05 r01 path declared in assets
- the request ID, asset ID, revision, and variation axis are canonical
- the exact ordered four-reference contract and C05 edit-source role
- the expression-grid snapshot source, copied path, role, rationale, byte
  identity, and SHA-256
- the exact ordered four stage names and accepted descriptors
- complete A and B families with one canonical output per stage
- explicit A and B `review_sets` with canonical IDs and exact four-path mappings
- identical shared invariants and identical same-stage prompts across A and B
- stage deltas change only allowed expression controls
- every stage edits accepted C05 directly and no C06 output is chained
- the inactive, targeted, and full-family C repair states are mutually valid
  and cannot authorize several isolated repairs
- comparison row and column order follows declared sets and stages
- reviews contain exactly four ordered stage sources and hashes
- complete-family and targeted-repair candidate IDs follow the canonical forms
  and resolve to their exact declared four-source mappings
- a repaired accepted review contains at most one C source unless C is a
  complete family
- accepted paths match the selected review digests in stage order
- an accepted C06 has exactly one accepted set review and all other reviewed
  sets are rejected
- an accepted review has no unresolved Blocker or Major
- request acceptance gates remain exactly `identity`, `state`, and `rendering`,
  with stage clarity and sequence continuity persisted under `state`
- candidate C06 retains empty `accepted_paths` before promotion
- D01 cannot become accepted before complete accepted C06 evidence exists

The validator may report advisory framing differences, but framing coordinates
alone cannot reject a candidate unless crop or scale prevents complete
face-and-hair sequence review. Exact file dimensions remain a production gate,
not advisory framing.

## Verification

Use red-green-refactor for the request contract, validator, lifecycle linkage,
and comparison builder. During implementation, run focused tests before broad
suites. Before calling C06 complete, run:

```sh
npm run test:node
npm run test:python
npm run validate:v1-2
npm run lint:md
npm run audit
git diff --check
```

Also confirm:

- all four accepted files are real 1024 x 1536 PNGs
- each accepted file is byte-identical to its selected source candidate
- selected-source and accepted SHA-256 values match in C06-1 through C06-4
  order
- exactly one C06 r01 complete-set review is accepted
- no accepted finding contains an unresolved Blocker or Major
- all non-selected reviewed sets are rejected
- the expression-grid snapshot matches its recorded source and digest
- candidate and comparison outputs remain local-only
- existing local-only C04, C05, and C07 review artifacts remain untouched
- no unintended generated artifact is staged or committed

## Out of Scope

- Reworking accepted C01 through C05 or C07 assets
- Changing C05 morning-hair strength, crop, outfit, lighting, or backdrop
- Open-mouth smiles, laughter, yawns, closed-eye smiles, or strong emotional
  expressions
- Hair-ornament-free Daily variants
- D01 room-scene generation or acceptance
- Pushing `main` or the C06 feature branch

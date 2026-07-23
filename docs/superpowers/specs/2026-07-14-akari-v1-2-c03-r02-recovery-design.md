# Akari v1.2 C03 r02 Framing Recovery Design

**Date:** 2026-07-14

**Scope:** Close the failed C03 r01 round, regenerate all three C03 pairs at
r02 with a deterministic framing contract, and accept at most one complete
r02 pair

## Relationship to the C03 Design

This document is the recovery addendum to
`2026-07-14-akari-v1-2-c03-paired-45-views-design.md`. The original design
still controls C03 identity, paired generation, visual review, byte-identical
promotion, and lifecycle rules. This addendum controls the r01 closure and r02
framing recovery. Where the two documents differ, this addendum takes
precedence for r02.

No r01 image is promotable. C03 remains `candidate` at `r00` until one complete
r02 pair passes every machine and visual gate and the user selects it.

## Goal

Create a fresh A/B/C round of three matched C03 pairs and give each pair a
bounded opportunity to match the accepted C01 and C02 vertical framing before
visual review begins. Each A/B/C pair is an independent retry and freeze unit;
the six canonical members do not need to originate from one simultaneous
batch. Stop a variant after the user-agreed retry cap instead of generating
indefinitely.
Then review and, only after an explicit user selection, promote one complete
r02 pair.

The recovery is complete only when:

- r01 A/B/C have durable rejected review records with exact source hashes and
  measured landmark failures;
- r02 has one committed request manifest with an exact framing contract;
- every r02 pair is either frozen with two automatic-audit passes or closed as
  rejected after reaching the retry cap;
- at least one complete r02 pair passes the automatic head-top and sole audit;
- one complete r02 pair passes the original C03 visual gates and is selected by
  the user;
- both selected sources are promoted byte-for-byte as r02;
- the final manifests and validator represent both request revisions without
  hiding or replacing r01 history.

## Why r01 Failed

The controlling canvas is 1024 x 1536. Measurements use ImageMagick 7 with a
6% fuzz trim bounding box:

```sh
magick identify -fuzz 6% -format '%@' IMAGE
```

For geometry `WIDTHxHEIGHT+X+Y`:

```text
head_top_y = Y
sole_y = Y + HEIGHT - 1
```

Accepted anchors measure as follows:

| Anchor | Geometry | Head top | Sole |
| --- | --- | ---: | ---: |
| C01 r01 | `423x1386+300+65` | 65 | 1450 |
| C02 r01 | `418x1399+299+65` | 65 | 1463 |

The 2% tolerance is 30.72 px. Because landmark coordinates are integers, a
displacement of 30 px passes and 31 px fails. Every C03 image must pass against
both anchors, not merely the nearer anchor.

| r01 member | Head top | Sole | Sole delta from C01 / C02 | Result |
| --- | ---: | ---: | --- | --- |
| A hairpin | 67 | 1422 | 28 (1.82%) / 41 (2.67%) | Major |
| A non-hairpin | 91 | 1434 | 16 (1.04%) / 29 (1.89%) | Pass |
| B hairpin | 52 | 1410 | 40 (2.60%) / 53 (3.45%) | Major |
| B non-hairpin | 56 | 1411 | 39 (2.54%) / 52 (3.39%) | Major |
| C hairpin | 68 | 1424 | 26 (1.69%) / 39 (2.54%) | Major |
| C non-hairpin | 52 | 1427 | 23 (1.50%) / 36 (2.34%) | Major |

Each pair contains at least one unresolved Major, so all three pairs fail. The
earlier provisional preference for B does not override this hard gate. No r01
accepted files were written.

## Chosen Recovery Approach

Use a derived C01/C02 framing board, an exact numeric framing contract in the
r02 request, and an automatic pre-review audit.

This approach is selected because the accepted images remain the controlling
visual evidence while the machine gate removes ambiguity about the 2%
threshold. The prompt and framing reference reinforce each other, but only the
measurement audit decides whether an output is review-ready.

### Pair-Atomic Retry Amendment

Two full-round attempts plus a third-round first-member failure showed that
vertical placement varies independently between image-generation calls.
Replacing every passing pair whenever an unrelated pair fails makes the
probability of completing C03 worse without improving pair consistency.
Therefore A, B, and C are independent retry and freeze units for r02.

- Generate and evaluate both members of one variant as a complete pair.
- If the hairpin-side member fails the automatic landmark gate, retire that
  partial attempt without generating its non-hairpin member.
- If the non-hairpin member fails, retire both members from that pair attempt.
- If both members pass, keep that complete pair at its canonical variant paths,
  freeze it, hash it, and never overwrite it.
- Retry only variants that do not yet have a frozen complete pair.
- After the user imposes a three-attempt cap, stop that variant when its third
  pair attempt fails. Keep the final failed pair as local review evidence and
  record its exact hashes and unresolved Major in the durable review log.
- Once the cap is reached, continue to visual selection when at least one
  complete pair is frozen. A capped failed pair is ineligible and cannot block
  selection of a different passing pair.
- Never combine members from different attempts, variants, or revisions.
- Never shift, scale, warp, patch, or composite a generated member into
  compliance.

The threshold remains unchanged: every frozen member must be 1024 x 1536 and
within 30 px of both C01 and C02 for head-top and sole landmarks. The exact
shared and view prompts also remain unchanged across all attempts.

The second full-round attempt already produced a valid B pair from one matched
attempt: hairpin-side measures head 62 / sole 1467 and non-hairpin-side measures
head 73 / sole 1450. That pair may be restored byte-for-byte from the local
failed-draft history and frozen as canonical B. A and C must be retried as
complete pairs subject to the user-agreed cap. A frozen passing pair remains
valid; C is closed as rejected when its capped final attempt fails.

Two alternatives are rejected:

1. **Numeric prompt only.** This is the smallest change, but r01 showed that
   prompt wording alone does not reliably control full-figure scale.
2. **Shift or composite generated figures after generation.** This can make the
   bounding box pass while introducing seams, clipped hair or shoes, false
   pixel provenance, or disconnected anatomy. C03 must be regenerated rather
   than repaired through post-positioning.

## Close r01 Durably

Keep `manifest/generation-requests/c03-r01.yaml` unchanged. Append exactly
three r01 C03 reviews to `manifest/review-log.yaml` in A/B/C request order. All
three reviews use `status: rejected`, two ordered `source_paths`, and two
ordered `source_sha256s`.

The source hashes are fixed as follows:

```text
c03-r01-a
  hairpin-side-45
    3fdf1dc9e5d15f438f512fc2750e05b9830f4f2fb5cad32a2afbcf20fe24d8e8
  non-hairpin-side-45
    c681bff18d3dccc17f3edabbb45e4cd6356a66e3ac186581354b7d8586b2a61f

c03-r01-b
  hairpin-side-45
    5aa985aaeccac830aaa9c53819905aea02596a0e0cf2ff768ac348e5d7969374
  non-hairpin-side-45
    98f1a3578f5056294610010f2116f2ae798da7cfaaa49ccabbda0703a6d0d4f8

c03-r01-c
  hairpin-side-45
    33d89602f14ed2f73dc6eac5c95ac7798c5d740fa909e7251546d0c50299fa47
  non-hairpin-side-45
    7fc375236ca9ffe1c69d95e537af19745233bd153d60bfbab27277f4487e1d9a
```

Each failing member produces an unresolved finding with `severity: major` and
`category: body`, including its displacement from C01 and C02. Every decision
states that the complete pair is rejected. B's decision also records that the
strict landmark re-audit invalidated the provisional selection before
promotion.

r01 candidates and comparisons remain local review artifacts. The review log
preserves their provenance after a clean checkout; the candidate PNGs do not
become tracked inputs to r02.

## r02 Request Contract

Add one request:

```text
akari-v1.2/manifest/generation-requests/c03-r02.yaml
```

Its identity is:

```yaml
request_id: akari-v1.2-c03-r02
asset_id: C03
revision: r02
variation_axis: paired_generation_attempt
```

The request retains the same five ordered logical reference roles as r01:

1. accepted C01 front stance;
2. accepted C02 back stance;
3. v1.1 hairpin-side identity;
4. v1.1 non-hairpin-side identity;
5. v1.1 shoe construction.

No r01 C03 candidate, comparison, or crop may appear in `references`, the
framing board, or an image-generation call. The only generated supporting
reference is the r02 hairpin member of the same pair while creating its
non-hairpin member.

The six canonical targets are:

```text
source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-a.png
source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-a.png
source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-b.png
source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-b.png
source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-c.png
source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-c.png
```

Use one byte-identical shared prompt template for A, B, and C and one
byte-identical view delta per view. Candidate-specific corrective wording is
forbidden because it would change the comparison axis. The shared prompt adds
the exact target coordinates and states that the output must be one standalone
image, never the framing board, a split screen, a collage, or a marked-up
reference.

Within each pair, generate hairpin-side first and non-hairpin-side second. The
second member uses the first only as a supporting continuity reference. C01,
C02, and the v1.1 images remain controlling.

## Framing Contract

The r02 manifest adds a required `framing_contract` mapping. Its semantic
content is exact:

```yaml
framing_contract:
  canvas:
    width: 1024
    height: 1536
  measurement:
    tool: imagemagick
    fuzz_percent: 6
    geometry_format: "%@"
    head_top_formula: y
    sole_formula: y_plus_height_minus_1
  anchors:
    - asset_id: C01
      revision: r01
      head_top_y: 65
      sole_y: 1450
    - asset_id: C02
      revision: r01
      head_top_y: 65
      sole_y: 1463
  maximum_displacement:
    percent_of_canvas_height: 2
    integer_pixels: 30
  required_intersection:
    head_top_y: [35, 95]
    sole_y: [1433, 1480]
  prompt_target:
    head_top_y: 65
    sole_y: 1456
    bottom_margin_pixels: 79
```

`required_intersection` is derived from the maximum displacement around both
anchors. It is a hard machine gate. `prompt_target` guides generation but does
not replace anchor comparison.

Shoulders, visual waist, and knees retain the original 3% visual review gate.
They are not inferred from the trim bounding box and are not added to this
automatic audit.

## Derived Framing Board

Create the board locally under `tmp/`; do not commit it or record it as a new
canonical reference. The board is 2112 x 1536:

- immutable accepted C01 occupies the left 1024 px;
- a 64 px center gutter uses solid `#f1f2f1`;
- immutable accepted C02 occupies the right 1024 px;
- the gutter contains two 48 x 3 px `#6b7280` horizontal ticks, spanning
  x=1032 through x=1079 and centered on y=65 and y=1456;
- the ticks remain entirely inside the gutter;
- there are no labels, captions, borders, scaling operations, or overlays on
  either accepted image.

The prompt describes this board as geometry-only evidence. It explicitly says
not to reproduce the side-by-side layout, gutter, ticks, or any other board
structure in the standalone output.

The board also keeps image-generation calls within the five-file reference
limit while preserving all five logical roles:

- hairpin generation uses the board plus the three v1.1 references: four
  physical files representing five logical references;
- non-hairpin generation adds the same pair's r02 hairpin candidate: five
  physical files.

Before each call, open the board and every applicable identity, hair, outfit,
shoe, or paired reference and state each file's role. Generate with the built-in
image generation tool; do not substitute a text-only identity exploration.

## Automatic Landmark Audit

Add:

```text
scripts/audit_v1_2_c03_landmarks.py
```

The command-line interface is exact:

```sh
uv run python scripts/audit_v1_2_c03_landmarks.py \
  --request akari-v1.2/manifest/generation-requests/c03-r02.yaml \
  --package-root akari-v1.2
```

The script loads the exact `framing_contract`, resolves C01 and C02 from the
first two request references, and remeasures both anchors before processing any
candidate. Their canvas, head-top, and sole values must exactly match the
contract. It then audits the six declared outputs in request order. For each
file it:

1. requires a readable 1024 x 1536 image;
2. obtains the 6%-fuzz geometry through ImageMagick;
3. parses the geometry and calculates `head_top_y` and `sole_y`;
4. reports both coordinates and their deltas from C01 and C02;
5. requires every head and sole delta to be at most 30 px;
6. exits nonzero for a missing tool, missing file, malformed geometry, wrong
   canvas, or any failed landmark.

The output must name every failed file and anchor instead of returning only a
summary. A zero exit means all six files pass; partial success is a nonzero
exit.

All six canonical r02 members must pass before comparison sheets or visual
review are considered review-ready. Draft outputs that fail this preflight are
not frozen as canonical A/B/C candidates and receive no review records. Retire
the failed pair attempt together, regenerate only that variant with the same
request and prompts, and rerun the audit after all three variants are frozen.
Each frozen complete pair is hashed and never overwritten.

## Comparison and Visual Review

Reuse the existing generic C03 comparison builder with the r02 request. Add
explicit r02 package commands that produce:

```text
akari-v1.2/comparisons/c03-r02/c03-r02-pair-comparison.webp
akari-v1.2/comparisons/c03-r02/c03-r02-alignment-comparison.webp
```

Keep the existing r01 commands and artifacts available for historical review.
Add these exact package commands so none can silently target r01:

```text
audit:v1-2:c03-r02-landmarks
build:v1-2:c03-r02-comparison
build:v1-2:c03-r02-alignment-comparison
```

After the machine gate passes, apply every visual gate from the original C03
design. Review in this order:

1. exact side and 45-degree direction;
2. identity and 25-year-old age impression;
3. shoulders, waist, and knees against the 3% gate;
4. pair consistency in face, body width, pelvis, leg volume, outfit, socks,
   shoes, perspective, palette, and rendering;
5. anatomy, crop, accessories, background, artifacts, text, logos, and
   watermarks.

If either member has an unresolved Blocker or Major, reject the whole pair.
Never mix r02 pair members or combine r01 and r02. The user selects from the
eligible complete pairs after seeing both r02 comparison artifacts and the
review recommendation.

## Manifest and Lifecycle Result

Before r02 selection, durable state contains:

- four generation requests in `(asset_id, revision)` order: C01 r01, C02 r01,
  C03 r01, C03 r02;
- 12 candidate groups and 18 generated outputs;
- nine reviews: the existing six C01/C02 reviews plus three rejected C03 r01
  reviews;
- C03 still at `candidate`, `r00`, with no accepted paths.

After selection, append exactly three C03 r02 pair reviews in A/B/C request
order. Exactly one is `accepted`; the other two are `rejected`. The final
review count is 12.

Set C03 to `accepted`, revision `r02`, with these ordered paths:

```text
accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png
```

Copy both selected sources byte-for-byte. Prove each source/destination pair
with `cmp` and matching SHA-256. The accepted r02 review stores both source
hashes in view order, and the validator recomputes both accepted-file hashes.

All three r01 reviews remain rejected. No accepted r01 review or accepted r01
C03 file may exist.

## Validator Changes

Add an exact `("C03", "r02")` request contract. It validates the same ordered
references, pair policy, views, A/B/C structure, and comparison anchors as r01,
but requires r02 target paths and the exact `framing_contract` above.

`validate_generation_dependencies()` must validate every request revision. It
must not reduce the collection to one request per `asset_id`, because doing so
allows C03 r02 to hide C03 r01 or vice versa. Group or iterate requests by
`(asset_id, revision)` and enforce the accepted C01/C02 anchors for both C03
requests.

Lifecycle lookup remains keyed by `(asset_id, revision)`. The accepted C03 r02
asset must link only to the three declared r02 reviews. The r01 rejected
reviews remain valid history but cannot satisfy, reorder, or replace the r02
lifecycle.

Add negative coverage for:

- a missing, changed, reordered, or extra r02 framing field;
- a 31 px displacement and an intersection endpoint violation;
- a request collection where one C03 revision has a substituted anchor;
- a validator that checks only the latest C03 request;
- r01 reviews used as r02 lifecycle records;
- mixed-revision source or accepted paths;
- missing, duplicated, reordered, or replaced r02 reviews;
- an accepted member whose SHA-256 differs from its selected source hash.

The validator summary must report four requests, 12 candidate groups, 18
generated outputs, and the current review count.

## Test Contract

Follow red-green-refactor for validator and audit behavior. Focused tests cover:

- parsing ImageMagick geometry and the `Y + HEIGHT - 1` sole formula;
- the integer boundary: 30 px passes and 31 px fails;
- synthetic temporary images for pass, wrong canvas, missing foreground, and
  out-of-range cases;
- the committed C01 and C02 anchors measuring exactly `(65, 1450)` and
  `(65, 1463)` under the declared 6% fuzz method;
- all six r02 request paths audited in A/B/C and view order;
- nonzero audit exit when any one of six files fails;
- exact r01/r02 request collection order and work counts;
- dependency validation across both C03 revisions;
- package commands targeting r02 request and output paths;
- final r02 review and accepted-asset linkage.

## Local Artifact Policy

Keep these paths local and untracked:

```text
akari-v1.2/source/candidates/c03/r02/
akari-v1.2/comparisons/c03-r02/
tmp/akari-v1.2/c03-r02/
```

The existing C03 candidate-directory exclusion covers r02 sources. Add an
explicit exclusion for `comparisons/c03-r02/`. Only the request, review
metadata, validator, audit script, tests, package commands, selected accepted
PNGs, and design/plan documents are durable git payload.

## Failure Handling

- If any canonical member fails the automatic audit, do not begin visual review
  or promote a pair. Retire and regenerate that member's complete variant pair
  under the unchanged contract; do not disturb frozen passing variants.
- If a frozen all-pass r02 batch has no pair that passes visual gates, record
  all three r02 reviews as rejected and stop without promotion. A later retry
  must use r03 and three fresh complete pairs.
- If a user-preferred pair fails a hard gate, report the measurement and keep
  it rejected. Preference cannot override a Blocker or Major.
- If ImageMagick is unavailable or its measured anchor coordinates differ from
  the committed contract, stop. Do not guess coordinates or weaken the gate.
- If only one member of a pair fails, retire the complete pair attempt. Never
  retain the other member or combine it with a later attempt.

## Verification

During implementation, run focused tests after each behavior change. Before
r02 visual review, run:

```sh
npm run audit:v1-2:c03-r02-landmarks
npm run build:v1-2:c03-r02-comparison
npm run build:v1-2:c03-r02-alignment-comparison
```

Before committing the accepted result, run:

```sh
npm run test:python
npm run validate:v1-2
npm run lint:md
npm run audit
git diff --check
```

Completion evidence must also show:

- six frozen r02 sources pass the machine audit;
- all six frozen source hashes are present in the three ordered r02 review
  records;
- both accepted files are byte-identical to the selected sources;
- exactly one r02 pair review is accepted;
- all r01 reviews and the other two r02 reviews are rejected;
- no unresolved Blocker or Major exists on the accepted pair;
- no candidate, comparison, or framing-board artifact is staged.

## Out of Scope

- Promoting, patching, shifting, or compositing any r01 C03 image
- Replacing or editing accepted C01 or C02
- Automating shoulder, waist, or knee detection
- A generic landmark framework for assets other than C03
- C04, C05, C06, C07, D01, or Natural Form release-PDF work

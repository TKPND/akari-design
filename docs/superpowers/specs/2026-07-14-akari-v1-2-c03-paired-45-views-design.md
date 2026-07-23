# Akari v1.2 C03 Paired 45-Degree Views Design

**Date:** 2026-07-14
**Scope:** C03 hairpin-side and non-hairpin-side natural-standing 45-degree
views, from generation contract through paired acceptance

## Goal

Create and accept one matched C03 pair that completes the two 45-degree
standing views in Akari v1.2 Natural Form Phase 1. The pair must preserve the
accepted C01 and C02 body, stance, landmark heights, rendering treatment, and
v1.1 identity while representing the hairpin and non-hairpin sides as separate
standalone images.

C03 is complete only when both images in one A/B/C pair have no unresolved
Blocker or Major findings, the user selects that pair, both images are promoted
byte-for-byte under the same revision, and the package validator confirms the
complete paired lifecycle.

## Global Constraints

- Generate three matched candidate pairs, A/B/C, for six standalone images.
- Select and accept a complete pair. Never combine images from different pairs.
- Generate each view as a separate 1024 x 1536 portrait image.
- Do not generate a collage, grid, split screen, contact sheet, or image that
  must be cropped into separate deliverables.
- Do not mirror one view to create the other view.
- Keep C01 and C02 images and their review decisions unchanged.
- Keep candidate and comparison output out of git. Only accepted deliverables
  and their durable contracts and review metadata are committed.
- C03 Core assets must use `accepted`, not `accepted-with-notes`, for release.

## Generation Approach

Use one request manifest:

```text
akari-v1.2/manifest/generation-requests/c03-r01.yaml
```

The request represents A/B/C as paired generation attempts. Each candidate has
two ordered outputs:

1. `hairpin-side-45`
2. `non-hairpin-side-45`

The canonical candidate paths are:

```text
akari-v1.2/source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-a.png
akari-v1.2/source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-a.png
akari-v1.2/source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-b.png
akari-v1.2/source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-b.png
akari-v1.2/source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-c.png
akari-v1.2/source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-c.png
```

Use `variation_axis: paired_generation_attempt`. The request schema contains a
shared prompt, two view-specific prompt deltas, the ordered candidates and
outputs, the pair-generation policy, comparison anchors, acceptance gates, and
hard rejects.

## Reference Contract

Every first-view generation uses these five references in this exact order:

1. `accepted_c01_front_stance`
   - `akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png`
   - Controls front identity, proportions, natural stance, landmark heights,
     crop, palette, and rendering treatment.
2. `accepted_c02_back_stance`
   - `akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png`
   - Controls rear identity, rear hair and outfit construction, landmark
     heights, leg volume, and rendering treatment.
3. `hairpin_side_identity`
   - `akari-v1.2/references/v1.1/hairpin-side-45.webp`
   - Controls the hairpin-side face, cheek, bob silhouette, and placement of
     the character-left parallel pins and pale-blue ribbon.
4. `non_hairpin_side_identity`
   - `akari-v1.2/references/v1.1/non-hairpin-side-45.webp`
   - Controls the opposite face, cheek, and bob silhouette without inventing
     mirrored accessories.
5. `shoe_construction`
   - `akari-v1.2/references/v1.1/shoes.webp`
   - Controls distinct left and right chunky sneaker construction.

Within each pair, generate the hairpin-side view first. Generate the
non-hairpin-side view with the same five controlling references plus the newly
generated hairpin-side member as a sixth `paired_candidate_anchor` reference.
The prompt states that C01, C02, and the v1.1 snapshots remain controlling; the
candidate anchor only improves within-pair rendering and proportion continuity
and must not propagate an error.

Use the same generation order for A, B, and C so the only comparison axis is
the independent paired attempt.

## Image Contract

Both views show the same 25-year-old Akari in the same physical natural stance
as accepted C01 and C02:

- compact anime proportions and stable head-to-body ratio
- sturdy, healthy legs without thin-leg drift
- nearly even weight distribution with subtle natural asymmetry
- unlocked knees, relaxed shoulders, soft elbows, and neutral lumbar curve
- level or nearly level pelvis without a fashion-model hip shift
- white oversized hoodie, gray pleated skirt, two-line white socks, and white
  chunky sneakers
- complete hair and shoes in frame with quiet breathing room
- plain low-contrast background and stable D65-like palette
- soft polished anime rendering consistent with accepted C01 and C02

The hairpin-side view must show the character-left parallel pins and small
pale-blue ribbon in the correct perspective. The non-hairpin-side view must
preserve the opposite bob silhouette without moving, duplicating, or inventing
the accessories.

The two views must use matching perspective conditions. Face width, cheek
roundness, ribcage direction, pelvis direction, leg thickness, skirt and hoodie
overlap, sock height, and shoe construction must read as one person and one
standing reference set.

Do not introduce a head turn independent of the body, strong contrapposto,
locked knees, twisted ankles, mirrored shoes, elongated proportions, long hair,
adult-glamorous facial drift, toddler-like proportions, photorealistic skin,
dramatic lighting, props, logos, readable text, or watermarks.

## Landmark Alignment

Measure each C03 image against accepted C01 and C02 on the 1536 px canvas:

- head-top and sole displacement: at most 2% of canvas height
- shoulder, visual-waist, and knee displacement: at most 3% of canvas height

Review pair-to-pair symmetry as well as anchor alignment. A view that passes an
individual threshold can still fail if the two C03 members clearly depict
different body widths, leg volumes, perspective conditions, or identity.

The accepted C01 character-left knee-to-foot inward Minor and the accepted C02
sock-top height Minor are comparison warnings, not target features to amplify.

## Candidate Comparison Artifacts

Build two review-only WebP artifacts:

```text
akari-v1.2/comparisons/c03-r01/c03-r01-pair-comparison.webp
akari-v1.2/comparisons/c03-r01/c03-r01-alignment-comparison.webp
```

The pair comparison uses three rows and two columns. Rows are A/B/C; columns
are hairpin-side and non-hairpin-side. It is the primary view for comparing
within-pair face, body, perspective, outfit, and rendering consistency.

The alignment comparison uses one row per candidate pair and shows accepted
C01, the pair's hairpin-side image, accepted C02, and the pair's
non-hairpin-side image in that order. It supports four-direction identity and
landmark review without converting the generated source images into panels.

Add these repository commands:

```text
build:v1-2:c03-comparison
build:v1-2:c03-alignment-comparison
```

Use a focused C03 comparison builder. Reuse stable card rendering primitives
from the current comparison code where practical, but do not complicate the
single-output C01/C02 request behavior with paired-only branching.

## Review and Selection

Review every candidate pair in this order:

1. Confirm exact 45-degree view direction and correct accessory side.
2. Confirm v1.1 identity and age impression across C01, C02, and both C03 views.
3. Confirm the 2% and 3% landmark tolerances.
4. Compare face width, cheeks, ribcage, pelvis, leg volume, skirt, hoodie, socks,
   shoes, and perspective between both members.
5. Check crop, background, palette, rendering continuity, anatomy, artifacts,
   text, logos, and watermarks.

A wrong view, mirrored substitute, identity drift, severe proportion mismatch,
wrong-side or missing accessories, disconnected or twisted anatomy, thin-leg
drift, or unusable crop is a Blocker. Clear landmark failure, locked knees,
perspective mismatch, mismatched pair identity or body construction, mirrored
shoes, or material outfit construction errors are Major findings.

Minor findings may remain only when neither member compromises the paired
turnaround contract. If either member has an unresolved Blocker or Major, the
whole pair is rejected. The user makes the final pair selection after seeing
both comparison artifacts and the review recommendation.

## Failure Handling

Do not mix the strong side of one pair with the strong side of another pair.
Do not accept a weak pair to preserve schedule.

If no r01 pair passes, incorporate the observed failures into a revised shared
prompt and generate a complete r02 round with three new pairs. Do not patch only
one r01 member or retain the other r01 member in the new accepted pair. This
keeps revision identity and paired generation history unambiguous.

## Manifest Schema Migration

Replace the single-value `accepted_path` field with an ordered
`accepted_paths` list for every asset in `manifest/assets.yaml`:

- accepted single-variant assets contain one path
- accepted multi-variant assets contain one path per variant in variant order
- non-accepted assets contain an empty list

Migrate C01 and C02 mechanically without changing their images, revisions,
statuses, reviews, or decisions. C03 depends on both accepted C01 and accepted
C02 because both are controlling generation anchors.

Replace the single-value `source_path` field with an ordered `source_paths`
list for every review in `manifest/review-log.yaml`. Existing C01 and C02
reviews contain one path. Each C03 review represents one A/B/C pair and contains
the two source paths in view order. C03 therefore adds three review records,
not six.

Add an ordered `source_sha256s` list to every review, with one lowercase
SHA-256 digest per `source_paths` entry. Candidate PNGs remain local working
artifacts, so these digests are the durable provenance after a clean checkout.
At promotion time, compare each selected source and accepted destination
directly with `cmp` and record the source digest. In later validation, compare
each accepted PNG with the corresponding digest from the accepted review; do
not require ignored candidate files to remain present.

The accepted C03 asset contains both accepted paths under the same revision:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_rNN.png
akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_rNN.png
```

Promote both selected sources byte-for-byte and record one accepted pair review.
The other two pair reviews remain rejected with findings and decisions.

## Validation Contract

Extend the Natural Form validator and tests to enforce:

- `accepted_paths` exists for every asset and matches variant order and count
- candidate assets have an empty `accepted_paths` list
- accepted files exist at every recorded path
- C03 requires accepted C01 r01 and C02 r01 at the exact declared anchors
- the C03 request has the exact ordered five-reference base contract
- `variation_axis` is `paired_generation_attempt`
- candidates are exactly A/B/C with exactly two ordered outputs each
- every output uses the canonical descriptor, revision, and variant suffix
- comparison anchors and pair-generation policy match the declared contract
- C03 reviews match the three declared candidate pairs in order
- each C03 review has exactly the two declared `source_paths` in view order
- every review has one valid `source_sha256s` digest per source path
- an accepted C03 asset has exactly one accepted pair review
- accepted paths match both digests in the selected review
- an accepted pair has no unresolved Blocker or Major finding
- no accepted review exists without a matching accepted asset
- C01 and C02 lifecycle validation remains unchanged after the list migration
- legacy runtime paths, substituted references, duplicates, missing files,
  reordered references or outputs, and mixed-pair paths are rejected

The validator's summary reports both candidate-pair count and generated-output
count so a C03 request cannot be mistaken for only three images.

## Verification

Add focused tests for the request schema, manifest migration, generation
dependencies, lifecycle linkage, byte identity, comparison order, missing
inputs, and package commands. Follow red-green-refactor for all validator and
builder behavior changes.

Run focused tests during implementation, then run:

```sh
npm run test:python
npm run validate:v1-2
npm run lint:md
npm run audit
```

Before declaring C03 complete, also confirm:

- both accepted PNGs exist at the recorded paths
- both accepted PNGs are byte-for-byte identical to the selected pair sources
- exactly one C03 pair review is accepted
- neither accepted member has an unresolved Blocker or Major
- the two non-selected pair reviews are recorded as rejected
- the working tree contains no unintended generated artifacts

## Out of Scope

- Reworking or replacing accepted C01 or C02 images
- C04, C05, C06, C07, or D01 generation and acceptance
- A general-purpose multi-panel layout framework
- Correction Pass infrastructure for retaining one member of a failed pair
- Direct runtime use of legacy pre-Natural Form assets
- A Natural Form release PDF

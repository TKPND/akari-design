# Akari v1.2 C02 Natural Back Stance Design

**Date:** 2026-07-13
**Status:** Approved for written review
**Scope:** C02 natural back stance, from first candidates through acceptance

## Objective

Create and accept the C02 rear full-body asset as the paired back view of the
accepted C01 Natural Form stance. C02 must preserve Akari v1.1 rear identity,
outfit construction, compact proportions, healthy leg volume, and rendering
language while matching C01's physical stance and landmark heights.

C02 is complete only when one candidate has no unresolved Blocker or Major
review findings, the user has selected it, the accepted file and review record
are linked to a declared candidate, and the Natural Form package validator
passes.

## Production approach

Generate three standalone first-round candidates from one shared prompt and
one exact ordered reference set. Candidates A, B, and C are independent
generation attempts, not different pose or styling experiments. Select between
them only on identity, front-to-back consistency, anatomy, rear construction,
and finished image quality.

This approach keeps the comparison fair. It avoids mixing a bob experiment,
garment experiment, or stance experiment into the same batch, and it provides
more useful selection coverage than refining a single first attempt.

## Reference contract

Open and inspect every selected reference before generation. Use these five
references in this order:

1. `akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png`
   is the primary head-to-body ratio, body width, landmark-height, leg-volume,
   stance, framing, and rendering anchor.
2. `akari-v1.2/references/v1.1/back.webp` is the primary rear bob, hood,
   hoodie-back, skirt, sock, and rear-silhouette identity reference.
3. `akari-v1.2/references/v1.1/hairpin-side-45.webp` confirms the
   character-left hair-accessory construction and adjacent bob silhouette.
4. `akari-v1.2/references/v1.1/non-hairpin-side-45.webp` confirms the opposite
   bob and cheek-side silhouette without moving the accessory.
5. `akari-v1.2/references/v1.1/shoes.webp` defines the inherited rear sneaker
   construction and the intentional differences between left and right shoes.

Use `akari-v1.2/references/v1.1/akari-v1.1-palette.json` as the D65 color
contract during review. Do not use pre-Natural Form legacy images as generation
references. Open `akari-v1.2/references/legacy/back.webp` only after generation
as a comparison for rear construction and body consistency; resemblance to it
does not grant acceptance.

## Shared image contract

All three candidates depict one standalone, exact rear-facing, full-body view
of the same Akari and the same physical stance as accepted C01. Use the same
1024 x 1536 portrait canvas as C01. Keep complete hair and shoes in frame with
comparable breathing room on a plain, low-contrast background.

Lock these elements across the batch:

- On the equal-size canvas, keep head-top and sole-height displacement within
  2% of canvas height relative to C01. Keep shoulder, visual waist, and knee
  displacement within 3%. Measure the visual waist at the torso-to-pelvis
  transition implied by the hoodie and skirt silhouette.
- Preserve C01's compact anime proportions, body width, sturdy thighs, soft
  calves, and approximately even weight loading.
- Keep the knees visibly unlocked, the shoulders relaxed, the elbows soft,
  the pelvis nearly level, and the lumbar curve neutral.
- Reproduce C01's small natural foot-angle difference without deliberately
  copying or amplifying its recorded character-left knee-to-foot inward Minor.
- Preserve the rounded rear bob and show the parallel pins and small ribbon on
  character-left, which appears on image-left in the exact rear view. Keep the
  accessory visible but less prominent than in the front view.
- Preserve the white hoodie, gray pleated skirt, two-line socks, and white
  chunky sneakers. Keep the hoodie back from ballooning and match the skirt
  length to C01.
- Construct the left and right shoes as a believable pair with natural small
  differences; do not mirror-copy one shoe.
- Preserve soft anime rendering, pale shading, restrained outlines, and
  D65-stable object colors.

Reject three-quarter rotation, head turning, fashion-model posing, strong hip
shift, locked knees, twisted ankles, elongated proportions, thin legs,
mirrored or missing hair accessories, overinflated hoodie volume, mirrored
shoes, dramatic lighting, photorealistic skin, incomplete crop, props, logos,
readable text, watermarks, collage, grid, split screen, or contact sheet.

## Generation request and working files

Define the round in:

```text
akari-v1.2/manifest/generation-requests/c02-r01.yaml
```

The request uses `variation_axis: generation_attempt` and declares candidates
`a`, `b`, and `c` with the same visual contract. Store generated files under:

```text
akari-v1.2/source/candidates/c02/r01/
  akari-v1.2_c02_back-natural-stance_r01-a.png
  akari-v1.2_c02_back-natural-stance_r01-b.png
  akari-v1.2_c02_back-natural-stance_r01-c.png
```

Each candidate is one complete generation. Do not blend candidates or use
low-diff compositing to hide anatomy, hair, clothing, or shoe failures.

## Comparison artifacts

Create two local working comparisons:

```text
akari-v1.2/comparisons/c02-r01/c02-r01-comparison.webp
akari-v1.2/comparisons/c02-r01/c02-r01-alignment-comparison.webp
```

The first is a labeled A/B/C selection sheet in request order. The second puts
accepted C01 first, followed by A/B/C, so head top, shoulder, waist, knee, and
sole alignment can be judged in one view. Comparison sheets are review aids,
not accepted sources.

Generalize the existing C01-only comparison code only as far as needed to
build both C01 and C02 comparisons from manifest data. Preserve the existing
C01 command behavior while adding a C02 command. Generated candidates and
comparison artifacts remain uncommitted unless the user explicitly asks to
preserve or publish them.

## Review and selection flow

Review candidates in this order:

1. **C01 pairing:** exact rear view, head-to-body ratio, framing, landmark
   heights, body width, leg volume, stance, and visible weight balance.
2. **Rear identity:** rounded bob, character-left accessory placement, age
   impression, and stable hair color.
3. **Body and outfit:** unlocked knees, pelvis-to-knee-to-ankle continuity,
   hoodie-back volume, skirt length and pleats, sock height, and leg thickness.
4. **Shoes and rendering:** distinct left and right rear construction, sole
   contact, D65 color stability, crop, background, artifacts, text, and
   watermark absence.

Treat a wrong view, identity drift, severe proportion mismatch, wrong-side or
missing accessory, disconnected or twisted anatomy, thin-leg drift, or
unusable crop as a Blocker. Treat clear locked knees, landmark displacement
beyond the stated 2% or 3% tolerance, overinflated hoodie volume, mirrored
shoes, or construction errors as a Major. Minor findings may remain only when
they do not compromise the paired turnaround contract.

The user makes the final selection after seeing both comparison artifacts and
the review recommendation.

## Correction and failure handling

If one candidate is clearly strongest but has a correctable Major, edit that
exact candidate with the same five references and a narrowly scoped correction
prompt. Do not broaden the correction into a new pose, outfit, or rendering
direction.

If all three candidates fail identity, stance, or anatomy, revise the shared
prompt and generate a complete `r02` round. Do not promote a weaker candidate
to preserve schedule, and do not accumulate patches on a failed base.

The recorded C01 character-left knee-to-foot inward Minor is a comparison
warning, not a feature to reproduce. C02 may resolve that ambiguity while
remaining visibly paired with C01.

## Acceptance and lifecycle updates

Promote the selected candidate byte-for-byte to:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_rNN.png
```

Then update `akari-v1.2/manifest/assets.yaml` with the accepted revision and
path, and append all candidate decisions and findings to
`akari-v1.2/manifest/review-log.yaml`. Do not mark C03 or later assets accepted
as part of this scope.

Extend the package validator to load every declared generation-request
manifest, validate C01 and C02 against their exact asset-specific reference and
candidate-path contracts, and verify that every accepted review links to one
declared candidate and one matching accepted asset. C02 validation must also
require C01 to remain accepted at the exact path declared by C02. The validator
must reject legacy generation references, substituted references, duplicate
references, arbitrary candidate IDs, arbitrary source paths, revision
mismatches, multiple accepted reviews for one asset revision, and accepted
reviews without accepted assets.

## Verification

Add or update tests for:

- The exact ordered five-reference C02 generation contract.
- Three same-contract C02 candidates and canonical target paths.
- C02 dependency on accepted C01.
- C01 and C02 lifecycle linkage across multiple generation requests.
- Rejection of legacy, substituted, duplicated, missing, or reordered C02
  references.
- Rejection of undeclared C02 candidates, source paths, and revision links.
- A/B/C comparison order and missing-candidate errors.
- C01/A/B/C alignment comparison order and missing-anchor errors.
- Preservation of existing C01 comparison command behavior.

After code, manifest, review-log, or documentation changes, run:

```sh
npm run test:python
npm run validate:v1-2
npm run lint:md
npm run audit
```

Before declaring C02 complete, also verify that the accepted PNG exists at the
recorded path, is byte-for-byte identical to the selected source candidate, has
exactly one accepted review with no unresolved Blocker or Major, and the git
working tree contains no unintended generated artifacts.

## Out of scope

- C03 or later asset generation and acceptance.
- Reworking accepted C01.
- Redesigning the hoodie, skirt, socks, shoes, hair, or hair accessories.
- Promoting the legacy rear image or using it as a generation source.
- Committing working candidates or comparison artifacts by default.

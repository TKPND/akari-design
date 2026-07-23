# Akari v1.2 C07 Indoor Sock Feet Design

**Date:** 2026-07-14

**Scope:** Generate, compare, review, and accept the paired C07 standing and
seated indoor sock-foot references for the Natural Form package.

## Goal

Create one accepted C07 r01 pair that defines how Akari's socked feet behave
while standing and while floor-sitting. The pair must preserve the same sock
design, leg volume, ankle construction, and rendering while showing
pose-appropriate loading, contact, lift, and compression.

C07 completes Phase 2 together with accepted C04 and becomes body-reference
evidence for D01.

## Deliverables

The accepted pair consists of:

- `accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-standing_r01.png`
- `accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png`

Each output uses a 1024 x 1536 portrait canvas and one foot-focused
composition. The standing image shows both legs from at least mid-thigh to
the complete socked toes. The seated image shows the pelvis and skirt hem,
both thigh roots, and both legs through the complete socked toes.

## Fixed Decisions

- Generate exactly three ordered candidate pairs: A, B, and C.
- Every candidate is an indivisible `standing` plus `seated` pair.
- Generate the standing member first.
- Generate the seated member second, using the same candidate's standing
  member as a supporting consistency reference.
- Never mix a standing member from one candidate with a seated member from
  another candidate.
- Use the accepted C04 floor-sitting mechanical family for the seated member.
- Use foot-focused crops rather than full-body compositions.
- Treat framing coordinates as advisory. A numeric miss alone cannot reject a
  candidate.
- Stop after three pairs. If no pair is eligible, close r01 and design r02
  separately.
- Promote only the user-selected pair, byte-for-byte.
- Keep candidates, comparisons, and review crops local-only.

## Reference Roles

The generation request declares references in this order:

1. Accepted C01 front natural stance
   - Controls healthy leg volume, standing knee state, natural loading,
     palette, outfit edge, and rendering.
   - Does not authorize copying its sneakers.
2. Accepted C04 floor sitting
   - Controls seated pelvis mechanics, front/rear leg trace, relaxed ankles,
     floor contact, outfit compression, and rendering.
   - The C07 seated member belongs to the same mechanical family but is not a
     pixel copy of C04.
3. v1.1 standard foot set
   - Controls white sock material, two pale-blue stripes, sock height, ankle
     volume, and readable foot construction.
   - Its shoes, labels, borders, panels, and layout are non-controlling.
4. Same-candidate standing member
   - Added only while generating the seated member.
   - Supports pair consistency for sock height, stripe count and placement,
     line width, ankle volume, foot proportions, palette, and rendering.
   - Does not override accepted C04's seated anatomy.

Before each generation call, open every reference used by that call with
`view_image` and state its role in the prompt.

## Generation Architecture

Add `manifest/generation-requests/c07-r01.yaml` with:

- `asset_id: C07`
- `revision: r01`
- `variation_axis: paired_generation_attempt`
- ordered views `[standing, seated]`
- ordered candidates `[a, b, c]`
- one output path for each view in each candidate
- a pair-generation policy with standing first and seated second
- the same-candidate standing output as the seated-only supporting reference
- body and rendering acceptance gates
- advisory framing guidance for both views

Generation runs in this exact order:

1. A standing
2. A seated, with A standing added as a supporting reference
3. B standing
4. B seated, with B standing added as a supporting reference
5. C standing
6. C seated, with C standing added as a supporting reference

Each call produces one standalone image. Do not generate a collage, comparison
board, multi-panel image, or both views in one file. Do not patch, mask, warp,
blend, mirror, or mechanically composite outputs.

## Visual Contract

### Standing

- Use a front-biased light three-quarter view at a natural standing height.
- Show both legs from at least mid-thigh through the complete toes.
- Keep the feet at a natural hip-width spacing without a symbolically
  symmetrical stance.
- Keep both knees unlocked and both ankles structurally connected.
- Let the primary load foot contact through heel, outer edge, forefoot, and
  toes.
- Let the secondary foot read slightly lighter through pressure or angle, not
  through a dramatic pose or raised leg.
- Preserve sturdy, healthy lower-leg and ankle volume.

### Seated

- Use the accepted C04 floor-sitting mechanical family and viewing direction.
- Show the pelvis, skirt hem, both thigh roots, knees, shins, ankles, heels,
  and complete toes.
- Keep a clearly traceable front leg and rear leg.
- Coordinate pelvis contact, knee direction, ankle angle, and foot contact.
- Show mild compression where a socked foot contacts the rug and relaxation
  where a foot is lifted or lightly resting.
- Do not use a chair, bench, bed, or straight-down seated lower legs.

### Pair Consistency

- Socks are opaque warm white with exactly two thin pale-blue stripes.
- Both socks use the same initial height with no intentional left/right drift.
- Stripe count, order, spacing, line width, hue, and vertical placement match
  within each pair.
- Sock ribbing, ankle volume, foot length, toe roundness, and rendering match
  within each pair.
- Large slouching, heavy folds, and mismatched sock heights are excluded from
  the Core reference. Those variations remain Daily-only possibilities.
- The fixed outfit edge remains the white oversized hoodie and gray pleated
  skirt. No footwear is present.

## Advisory Framing

Both views use a 1024 x 1536 canvas. Record these comparison targets as
advisory guidance:

- complete toes remain visible
- intended bottom breathing room: 46 to 150 px
- intended lateral breathing room: at least 48 px
- standing upper crop: both legs visible from at least mid-thigh
- seated upper crop: pelvis, skirt hem, and both thigh roots visible

The validator must require `enforcement: advisory` and
`reject_on_numeric_miss_alone: false`. A candidate receives a Major framing
finding only when crop or scale prevents review of a required joint chain,
sock construction, loading, contact, lift, or compression.

## Review and Acceptance

Review the six images as three fixed pair rows in this order:

1. A standing / A seated
2. B standing / B seated
3. C standing / C seated

Review order:

1. Pair identity: correct two-line sock design and consistent rendering
2. Leg topology: thigh to knee to shin to ankle to toe remains traceable
3. Standing loading and foot contact
4. Seated pelvis, knee, ankle, and rug-contact coordination
5. Pair consistency in sock height, stripes, ankle volume, and foot length
6. Production artifacts and crop readability

An eligible pair has no unresolved Blocker or Major. Minor findings may be
recorded. The user selects one eligible literal pair A, B, or C before any
accepted C07 state changes.

The complete review batch contains exactly three ordered reviews with exactly
one accepted decision. The accepted review records both source paths and both
SHA-256 values. The lifecycle validator proves that the two accepted files
match those recorded values.

## Hard Rejects

- bare feet, shoes, slippers, or any other footwear
- anything other than two pale-blue stripes on each white sock
- mismatched sock height or materially inconsistent stripe placement
- fused, missing, duplicated, disconnected, or untraceable legs, ankles, or
  feet
- twisted ankle mechanics or a ballet-like pointed-toe pose
- standing contact that contradicts the visible loading
- seated contact that contradicts pelvis, knee, or ankle mechanics
- severe lower-leg, ankle, or foot-volume drift between pair members
- crop or scale that prevents structural foot and contact review
- copied reference text, logo, watermark, border, grid, collage, or multiple
  compositions
- unresolved Blocker or Major in either member of the pair

## Comparison Output

Add a C07 comparison command that reuses the existing paired grid renderer.
The output is a three-row by two-column WebP with A/B/C in rows and
`standing`/`seated` in columns. No new visual layout framework is required.

The comparison output lives under `akari-v1.2/comparisons/c07-r01/` and stays
untracked. Review crops, if needed, live under `tmp/` and are never promoted.

## Validation and Tests

Use test-driven development in this order:

1. Exact C07 generation-request contract
2. Accepted C01 r01 and C04 r01 dependency enforcement
3. Ordered pair-generation policy and output paths
4. Advisory framing semantics and rejection of hard pixel enforcement
5. Three-row by two-column comparison builder behavior
6. Final asset, review, candidate, source-path, and SHA-256 lifecycle linkage

The validator must reject missing, changed, extra, or reordered reference and
candidate data. It must reject reordered pair members and a seated member that
references the wrong standing candidate.

After selection, copy only the chosen pair to accepted paths and prove byte
identity with `cmp` and SHA-256. Run focused tests, the complete Node and Python
suites, `npm run validate:v1-2`, repository audits, Markdown lint, file-type
inspection, and `git diff --check` before completion.

## Repository Hygiene

Durable changes may include the C07 request, validator and tests, comparison
command or thin builder support, accepted pair, asset state, and review log.
Candidate PNGs, comparison WebPs, and review crops remain local-only unless
the user explicitly requests otherwise.

Do not modify or remove the existing local-only C04 candidate and comparison
artifacts while producing C07.

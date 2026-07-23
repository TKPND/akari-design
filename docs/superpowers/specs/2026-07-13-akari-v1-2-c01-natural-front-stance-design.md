# Akari v1.2 C01 Natural Front Stance Design

**Date:** 2026-07-13
**Status:** Approved for planning
**Scope:** C01 natural front stance, from first candidates through acceptance

## Objective

Create and accept the C01 front full-body asset that anchors Akari v1.2 Natural
Form. C01 must preserve the v1.1 identity, outfit, proportions, and rendering
language while adding believable standing weight balance and small signs of
physical relaxation.

C01 is completed only when one candidate has no unresolved Blocker or Major
review findings, is recorded as `accepted`, and passes the Natural Form package
validator.

## Production approach

Generate three standalone first-round candidates from the same reference set
and the same identity, outfit, rendering, framing, and background constraints.
Vary only posture relaxation and weight distribution.

This parallel three-candidate approach is preferred over single-image iteration
because it provides a useful posture comparison without mixing identity,
proportion, style, and pose experiments. It is preferred over a larger batch
because C01 needs focused review rather than broad exploration.

## Reference contract

Open and inspect every selected reference before generation. Use these v1.1
references for generation:

- `akari-v1.2/references/v1.1/front.webp`: primary face, body, outfit, and
  frontal silhouette lock.
- `akari-v1.2/references/v1.1/hairpin-side-45.webp`: character-left hair
  accessory and cheek silhouette support.
- `akari-v1.2/references/v1.1/non-hairpin-side-45.webp`: opposite cheek and bob
  silhouette support.
- `akari-v1.2/references/v1.1/shoes.webp`: inherited white sneaker
  construction.

Use `akari-v1.2/references/v1.1/akari-v1.1-palette.json` as the D65 color
contract during review. Do not use pre-Natural Form legacy images as generation
references. They may be opened only after generation for comparison and must
not grant acceptance by resemblance alone.

## Shared image contract

All three candidates must depict one standalone, front-facing, full-body image
on a plain low-contrast background. The complete hair, shoes, and surrounding
breathing room must remain in frame.

Lock these elements across the batch:

- Akari v1.1 identity and 25-year-old age impression.
- Short warm-brown bob and hair accessories on character-left.
- Warm-brown eyes and normal neutral expression.
- Compact anime proportions and unchanged basic head-to-body ratio.
- Sturdy healthy legs with fuller thighs and soft calves.
- White hoodie, gray pleated skirt, two-line socks, and white chunky sneakers.
- Soft anime rendering, pale shading, restrained outlines, and D65-stable
  object colors.
- Arms resting naturally without props, logos, text, or watermarks.

Reject fashion-model posing, strongly shifted hips, locked knees, twisted
ankles, elongated proportions, thin legs, mirrored accessories, glamorous or
childlike age drift, dramatic lighting, and photorealistic skin.

## Candidate posture variants

### Candidate A: conservative relaxation

Stay closest to the v1.1 frontal stance. Keep weight nearly even, pelvis nearly
level, feet almost parallel with a slight outward angle, and introduce only
small softness in the knees, shoulders, and elbows.

### Candidate B: standard Natural Form

Use approximately even loading with visibly unlocked knees, relaxed shoulders,
soft elbows, and a neutral lumbar curve. This is the default recommendation and
the center of the permitted C01 range.

### Candidate C: softer asymmetry

Use a subtle weight difference, never beyond 55:45, with small corresponding
differences in shoulder and arm height. Keep the pelvis nearly horizontal and
avoid turning the result into a model pose.

## Files and comparison

Store first-round working images under
`akari-v1.2/source/candidates/c01/r01/` with explicit variant suffixes:

```text
akari-v1.2_c01_front-natural-stance_r01-a.png
akari-v1.2_c01_front-natural-stance_r01-b.png
akari-v1.2_c01_front-natural-stance_r01-c.png
```

Create a labeled comparison artifact under `akari-v1.2/comparisons/c01-r01/`
without treating the comparison sheet as an accepted source image. Generated
working folders remain uncommitted unless the user explicitly asks to preserve
or publish the final deliverable.

## Review and selection flow

Review candidates in this order:

1. Identity: face, age, bob, accessory side, head-to-body ratio, and v1.1 read.
2. Body: leg thickness, knee state, ankle connection, foot orientation, pelvis,
   and visible weight balance.
3. Rendering: outfit construction, D65 color stability, crop, background,
   artifacts, text, and watermark absence.

Reject a candidate immediately for an identity or anatomy Blocker. Select the
strongest candidate only when it has no Blocker. A Major finding requires a
Correction Pass before acceptance; Minor findings may be recorded if they do
not compromise the C01 contract.

The user makes the final selection after seeing the three candidates and the
review recommendation.

## Correction and failure handling

If one candidate is clearly strongest but has a correctable Major issue, edit
that exact candidate with the same references and a narrowly scoped correction
prompt. Do not blend candidates or use low-diff compositing when it risks
breaking anatomy, clothes, hair, or shoe continuity.

If all three candidates fail identity or anatomy, revise the common prompt and
generate a new complete round. Do not accumulate local patches on a failed
base. If pose differences also cause identity or style drift, reduce the next
round to the conservative A posture before widening the range again.

## Acceptance and package updates

Promote the accepted image to:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_rNN.png
```

Then update `akari-v1.2/manifest/assets.yaml` with the accepted revision and
path, and append the candidate decision and findings to
`akari-v1.2/manifest/review-log.yaml`. Do not mark C02 or C03 accepted as part
of this scope.

## Verification

After manifest, review-log, or reference changes, run:

```sh
npm run validate:v1-2
npm run lint:md
```

Before declaring C01 complete, also verify that the accepted PNG exists at the
recorded path, the review log has no unresolved Blocker or Major finding for the
accepted revision, and the git working tree contains no unintended generated
artifacts.

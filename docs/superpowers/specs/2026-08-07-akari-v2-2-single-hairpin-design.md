# Akari v2.2 Single-Hairpin Design

Status: approved by the user; ready for implementation.

Date: 2026-08-07.

## Goal

Replace only the unstable crossed hairpin in the two user-provided Akari v2.2
candidates with one simple, repeatable blue hairpin. Preserve each candidate's
existing identity, age impression, hair silhouette, expression, pose, crop,
body, outfit, palette, and rendering finish.

The change succeeds when both the close portrait and full-figure composition
show the same clearly readable one-piece ornament without duplicate lines,
crossings, fragments, or unrelated visual drift.

## Input Candidates

The two JPEGs are edit targets, not general style references.

| Role | Source | Dimensions | SHA-256 |
| --- | --- | --- | --- |
| Full-figure composition edit target | `/home/takahiro/.codex/attachments/fe844d5e-28a7-4e61-942b-8787a90a7ee6/1844477702.jpeg` | `944 x 1672` | `cb6a659ec374f0c113fec58f989cb351130c950d2312892d1de4f7245e97c605` |
| Close-portrait edit target | `/home/takahiro/.codex/attachments/12b80512-5531-4d4d-97e9-111f5121b087/517254027.jpeg` | `944 x 1672` | `3756e53b3a0a912e61f22a5ce7f339667c7146d3591d0fa54074ef3c585d7a29` |

Immediately before each edit, open the edit target at original detail. Also
open the other v2.2 candidate as a supporting cross-scale identity and hair
continuity reference. The edit target controls all existing pixels and visual
decisions outside the ornament.

## Considered Approaches

1. **One filled capsule pin, selected:** one solid silhouette avoids the line
   counting, endpoint, and overlap failures visible in the current crossed
   construction while keeping Akari's blue accent and side marker.
2. **One U-shaped bobby pin:** recognizable as a conventional pin, but its two
   parallel edges and joined endpoint preserve much of the current generation
   ambiguity.
3. **No hairpin:** maximizes stability, but removes a useful face-side identity
   accent and laterality cue.

## Approved Hairpin Contract

Use exactly one straight, slender, filled capsule-shaped hairpin:

- one continuous solid piece with softly rounded ends;
- placed on character-left, which appears on canvas-right in both supplied
  views;
- anchored above the character-left temple on the outer hair mass;
- rising approximately 35 degrees from face-front/lower toward
  crown-back/upper, following the local hair plane rather than the page edge;
- approximately 0.8 of the visible eye width in length;
- narrow enough to read as a hairpin, but thick enough to remain one filled
  shape at full-figure scale;
- matte, muted medium blue, coordinated with the existing blue accents but not
  electric, neon, or glossy;
- no black outline, internal line, opening, hinge, tooth, highlight stripe, or
  separate clasp detail.

Do not add a second pin, crossing, bow, ribbon, loop, bead, flower, symbol, or
decorative tail. Remove every visible remnant of the original crossed-pin
construction.

## Locked Image Content

Change only the hairpin. In each candidate, preserve:

- the same face identity, apparent age, eye geometry, gaze, brows, cheeks,
  nose, mouth, smile, and expression;
- the same bangs, hairline, side ponytail, ponytail tie, flyaways, highlights,
  chestnut palette, and overall hair volume;
- the same head angle, camera, framing, crop, pose, hand gesture, anatomy,
  proportions, and background;
- the same white T-shirt, navy shorts, utility pocket, socks, shoes, linework,
  shading, and finish wherever visible.

Do not use the edit as an opportunity to polish the face, reshape the hair,
repair anatomy, change clothing, alter saturation, or restyle the rendering.

## Execution Boundary

Create one non-destructive edited candidate from each supplied image using the
same ornament contract. Keep the two image-generation calls independent so a
failure in one scale does not contaminate the other target.

Use the built-in image-edit path. Store preview candidates and their prompt,
generation identifiers, hashes, dimensions, and review notes under:

```text
tmp/akari-v2.2-single-hairpin/r01/
```

Suggested filenames:

- `akari-v2.2-single-hairpin-fullbody-r01.png`;
- `akari-v2.2-single-hairpin-portrait-r01.png`.

The directory remains ignored and untracked. The edits are review candidates,
not canonical assets, and do not replace or promote any existing image.

## Review Gates

Each output passes only when all of the following are true:

1. Exactly one complete blue hairpin is visible.
2. It follows the approved filled-capsule shape, scale, color, angle, and
   character-left/canvas-right placement.
3. No second line, crossing, fork, loop, gap, fragment, or ghost of the old
   ornament remains.
4. The character remains immediately recognizable as the same supplied v2.2
   candidate at the same age, expression, pose, crop, and finish.
5. Hair silhouette, bangs, ponytail, ear, jaw-to-neck connection, hands, body,
   clothing, shoes, and background remain coherent and materially unchanged.
6. The pin reads as the same design at original detail and at reduced
   full-figure viewing scale.
7. There is no seam, patch boundary, duplicated feature, malformed anatomy,
   text, logo, watermark, border, or new generation artifact.

If an output fails any gate, reject that output and preserve its original edit
target unchanged. Do not silently accept the least-bad result, promote it,
composite it, or start an additional correction round without a new user
decision.

## Verification

Before editing:

- verify the two input hashes and dimensions above;
- confirm the working output names do not overwrite an existing file;
- open both supplied images at original detail and state their distinct roles.

After editing:

- inspect both outputs at original detail and at equal reduced scale;
- record the exact prompt, generated source, generation identifiers, copied
  output path, dimensions, PNG signature, and SHA-256 for each output;
- verify copied files byte-for-byte against their generated sources;
- confirm no canonical image changed and inspect the bounded Git scope.

## Non-Goals

This checkpoint does not redesign or polish the face, eyes, hair, ponytail,
body, outfit, pose, or rendering style. It does not create additional views,
expressions, wardrobes, a turnaround, manifest-backed package, release, PDF,
promotion, staging, push, or replacement of a canonical authority.

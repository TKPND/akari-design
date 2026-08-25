# Akari v2.3 Selection History

Promotion date: 2026-08-25.

## Promoted Decision

- The user supplied `20260819_219844051.jpeg` and explicitly directed that it be
  committed as Akari v2.3.
- This instruction promotes the previously documented V2.3 face-anchor
  candidate to the formal V2.3 canonical face authority.
- The exact incoming JPEG is preserved without resizing, cropping,
  recompression, compositing, retouching, or color adjustment.

## Authority and Provenance

- Accepted destination:
  `accepted/base/akari-v2.3-face-anchor.jpeg`.
- Original attachment name: `20260819_219844051.jpeg`.
- The image and SHA-256 were previously recorded in
  `akari-v3.0/docs/akari-v3.0-style-research-checkpoint.md` as the first of
  three external-model V2.3 identity-study images.
- The later six-sample reproducibility run scored five of six generated faces
  as matching. That result remains useful evidence, but the user's explicit
  promotion decision is the authority for this package.

## Review Result

Original-detail inspection found coherent near-front facial anatomy, a direct
coordinated gaze, consistent warm brown and honey-amber iris construction,
rounded cheeks, a compact chin, a small nose, blush hatching, and a short
closed-mouth smile. The chestnut bob, grouped bangs, low side ponytail, blue
tie, and single blue hairpin are complete and readable.

The image contains no visible text, logo, watermark, decorative frame, duplicate
feature, seam, or material image artifact. The lower torso and arms leave the
canvas as part of the intended close-portrait composition; the image is not a
full-body or complete-outfit authority.

## File Hash

| Role | Dimensions | Color | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| v2.3 accepted face anchor | `1024 x 1536` | 8-bit sRGB JPEG | `2720040` | `9cdee2f3df4adf99a1d3aeeacbca1e17633ae4f8a99c835a727d68343f758024` |

## Promotion Verification

The accepted JPEG must remain byte-identical to the supplied attachment under
`cmp`. Its JFIF signature, dimensions, color space, byte size, and SHA-256 must
match the values above. Promotion verification also includes original-detail
inspection, Markdown lint, `git diff --check`, and exact Git-scope inspection.

Promotion scope is the accepted image, this package's `README.md` and
`selection.md`, and the documentation updates that replace the external
candidate path with the committed authority. No push, PDF work, full-body
promotion, or generated-sample promotion is authorized.

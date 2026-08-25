# Akari v2.3 Portrait Baseline

Status: close-portrait face anchor promoted.

Date: 2026-08-25.

Akari v2.3 is a compact one-image identity checkpoint. It formalizes the
user-selected portrait that was previously evaluated as the V2.3 face-anchor
candidate and preserves that exact JPEG as the canonical source.

## Canonical Authority

- `accepted/base/akari-v2.3-face-anchor.jpeg` is the sole authority for face
  identity, eye construction, cheeks, chin, expression, hair, the blue hairpin
  and tie, apparent adult age, and close-view rendering.

The portrait is not a full-body, pose, or complete-wardrobe authority. Its white
T-shirt and upper-torso crop are presentation context only. Body proportions,
lower garments, footwear, and complete-figure composition require a separately
approved supporting reference.

## Locked Design

- Approachable adult impression with rounded cheeks and a small, softly tapered
  chin.
- Large but noncircular warm brown eyes, darker upper irises, honey-amber lower
  irises, restrained reflections, and a direct coordinated gaze.
- Small understated nose, blush hatching, and a short low closed-mouth smile.
- Warm chestnut asymmetrical bob with grouped bangs and one low side ponytail on
  character-left/canvas-right.
- Exactly one straight slender blue hairpin above the character-left temple and
  one blue ponytail tie.
- Clean anime linework, restrained cel shading, warm off-white background, and
  no text, logo, watermark, or decorative frame.

## Generation Use

Open this canonical image before identity-sensitive V2.3 generation and use it
as the primary identity reference. A task-local face crop may be derived from
this exact image when more facial detail is required, but the crop does not
replace the committed JPEG as the canonical source. Do not let a body, pose,
outfit, or scene reference override this portrait's face, eyes, hair, accessory,
or adult impression.

## Scope Boundary

This is a minimal one-image identity package. It is not a full-body baseline,
turnaround, angle set, expression sheet, wardrobe set, manifest-backed release,
or PDF. Reproducibility samples, holdouts, comparisons, prompts, and unselected
working outputs remain noncanonical unless separately promoted.

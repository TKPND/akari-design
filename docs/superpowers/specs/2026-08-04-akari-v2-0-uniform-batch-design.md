# Akari v2.0 Uniform Batch Generation Design

Status: approved for pilot specification review.

Date: 2026-08-04.

## Goal

Create a local exploration batch of approximately 300 Akari v2.0 images focused
on school uniforms. The batch must vary uniforms, scenes, framing, camera
angle, and expression without losing the approved v2.0 character identity.

The work is split into a 30-image pilot and a 270-image expansion. The pilot
is reviewed before the expansion axes are frozen.

## Authority and Scope

- `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png` is the primary
  identity reference for face, eyes, cheeks, chin, smile, hair, ornament,
  ponytail, skin treatment, and close-view rendering.
- `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png` is the secondary
  authority for body balance, laterality, limbs, and general figure treatment.
- The nine user-provided JPGs are supporting references for uniform design,
  school-life scenes, lighting, and composition only. They do not override the
  v2.0 identity authorities.
- The existing white T-shirt and navy shorts remain the current v2.0 baseline,
  but the uniform batch may vary the clothing broadly as explicitly requested.
- No generated candidate becomes a new canonical v2.0 asset during this batch.

## Character and Safety Lock

- Akari reads as an 18-year-old young adult in ordinary school life.
- Keep the warm chestnut hair, amber eyes, pale-blue crossed ornament, and low
  side ponytail on character-left; in front views these appear on canvas-right.
- Preserve the compact healthy body and approachable childhood-friend presence.
- Expressions are scene-driven and may vary: happy, sleepy, thoughtful,
  surprised, shy, focused, calm, or similar everyday emotions.
- Keep the images non-sexual and natural. Avoid underwear exposure, transparent
  clothing, fetish framing, readable logos or signs, watermarks, and invented
  text.
- Keep the v2.0 soft cel-shaded anime rendering and warm, polished finish.

## Pilot Matrix

The first 30 images use six uniform families crossed with five composition
families.

### Uniform families

1. Summer white-and-navy sailor uniform.
2. Dark winter sailor uniform with a restrained accent ribbon.
3. Navy blazer with a plaid skirt.
4. Shirt with a knit vest and pleated skirt.
5. Cardigan with a blouse and pleated skirt.
6. A calm long-skirt school uniform variation.

### Composition families

1. Full-body walking or commuting view.
2. Knee-up gesture or conversation view.
3. Chest-up or close facial expression view.
4. High-angle or overhead view using stairs, a desk, or a corridor.
5. Rear or rear three-quarter view with a natural look-back.

Each combination receives a distinct everyday situation such as arrival,
classroom pause, station waiting, rain clearing, reading, or after-school
departure. The framing need not show the complete body. High-angle views must
serve environmental storytelling and gesture clarity, not invasive emphasis.

## Generation Workflow

Use the built-in `image_gen` tool in generate mode. The word batch does not
authorize CLI fallback. Issue one call per distinct image, with the face master
and full-body baseline named by role in the prompt. Add only the relevant
supporting JPG references for the current uniform or composition.

Save pilot outputs and a prompt/index record under the ignored working path:

```text
tmp/akari-v2-uniform-batch/pilot-30/
```

The index records the stable ordinal, uniform family, composition family,
scene, expression, reference roles, generation ID, and saved output path. It is
working metadata, not a release manifest.

After visual review, select the strongest uniform families, composition types,
and expression patterns. Expand only those choices into approximately 270
additional images in several small blocks. Keep candidates local and do not
promote or commit them without a separate explicit selection decision.

## Review Gate

Review every pilot image for:

1. Same-person identity against the face master.
2. Correct hair, ornament, ponytail side, and age impression.
3. Coherent anatomy, hands, feet, clothing construction, and camera geometry.
4. Clear school-uniform read without logos, text, or accidental modern branding.
5. Useful composition and readable scene-specific expression.
6. No visible watermark, border, seam, or generation artifact.

The pilot review result controls the 270-image expansion. A weak uniform family
or composition may be removed rather than repeated for quota.

## Verification and Explicit Non-Goals

Use visual inspection plus lightweight PNG existence, dimensions, and file
checks as needed. Do not build or audit a PDF. Do not run Python tests. Do not
run a broad release gate. Do not alter the existing v2.0 canonical images.

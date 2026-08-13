# Akari V2.2 concept-first transition success

## Outcome

- On 2026-08-13, Codex built-in `image_gen.imagegen` produced a three-step
  Akari V2.2 sequence whose identity was explicitly approved by the user at
  every step: P00 preflight, T01 scene transition, and T02 wardrobe transition.
- T02 was also separately selected for its wardrobe. Record its state as
  `identity_approved` plus `wardrobe_selected`, not
  `anchor_transfer_approved`.
- This is positive evidence for this exact route and staged transition. It does
  not retroactively change the rejected status of r01-r06 and is not a
  controlled proof that any single prompt change caused the improvement.
- Rollout/thread id: `019ff88d-af00-7812-9198-d5cad1f65503`.
- Rollout path:
  `/home/takahiro/.codex/sessions/2026/08/13/rollout-2026-08-13T09-37-42-019ff88d-af00-7812-9198-d5cad1f65503.jsonl`.

## Exact successful execution pattern

1. Use the repository canonical portrait as the sole image input for every
   generation call:
   `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`.
   Each call used `referenced_image_paths` with exactly this one path.
2. Do not pass the canonical full-body image, P00, T01, GPT Pro examples, or
   local cute-composition images into the image tool for this route. Earlier
   generated images were comparison controls only, never generation inputs or
   continuity anchors. Composition observations were expressed in text.
3. Generate exactly one image per call. Stop after P00 and each transition,
   present an identity comparison, and wait for explicit user approval before
   adding the next major change.
4. Keep the prompt short and concept-first, in this order:
   reference role; identity relationship; wardrobe; one coherent visual
   concept; shared rendering plus a short avoid list.
5. Make the face the largest and clearest focal point. Tie camera, action,
   light, palette repetition, props, and background lines into one composition
   that returns attention to the face instead of listing unrelated details.
6. Preserve the same cheerful expression, gaze, and head angle during the
   transition test, and change only one major dimension at a time.

## Successful transition ladder

- P00: canonical portrait only; retain close portrait framing, three-quarter
  head angle, viewer gaze, bright open smile, and plain white T-shirt; simple
  warm off-white background. User status: `identity_approved`.
- T01: canonical portrait only; keep white T-shirt and add one major change,
  from close portrait to a knee-up three-quarter morning-kitchen scene. Place
  omurice flat on the counter and use one open-palm introduction gesture. Keep
  the plate secondary and guide attention back to the face with window light
  and counter lines. User status: `identity_approved`.
- T02: canonical portrait only; keep the textual T01 camera, kitchen, action,
  light, and focal hierarchy, then change only the wardrobe to a pale-blue
  short-sleeve blouse, simple blue skirt, and soft-pink bib apron. User status:
  `identity_approved` plus `wardrobe_selected`.

## Prompt characteristics that should be reused

- Start with: `Image A is the sole authority for Akari V2.2's face and hair.`
- Request the same person by preserving relationships among face, eyes, brows,
  cheeks, and mouth, plus bangs, low side ponytail with blue tie, and exactly
  one viewer-right blue capsule hairpin. Avoid numeric face redesign and
  repeated synonyms.
- Describe clothing structure and major colors in one short paragraph.
- Describe scene, light, camera, palette echo, negative space/background
  guidance, and one main action together as a visual concept.
- End by asking for one shared light direction and consistent line and paint
  density across character and environment. Keep the avoid list to facial
  redesign/re-aging, left-right reversal, major hand/object-contact breakage,
  and text/watermarks.

## Identity review pattern

- For T01, compare canonical face, approved P00 face, current candidate face,
  and current full image in one artifact. For T02, compare canonical face,
  approved T01 face, current candidate face, and current full image.
- Keep the three face crops unwarped and at the same displayed size. Ask about
  identity first; do not combine that question with wardrobe selection or
  anchor-transfer approval.
- The user, not Codex, is the final identity judge. Codex only filters obvious
  mismatches before requesting approval.

## Reproduction record

| Step | Generation id | Dimensions | SHA-256 |
| --- | --- | --- | --- |
| P00 | `exec-eb77b3ca-e653-4fd2-b113-19fb04a3e04b` | 942x1669 | `df013000f147b84ee834940cff8fe331b2df825c1fed9d33be3b624d70923dfb` |
| T01 | `exec-8125d4ef-e454-431b-9158-21eea021550f` | 943x1668 | `bf22890830b45242bf1580b6c36e83f1e6ee780b313dd298e6beae891ed9c98d` |
| T02 | `exec-e76e69a4-82f6-4eef-89a1-b0696c52b117` | 1087x1447 | `a7a3740cfdeeaf207459478e4647bba0c6904d76026517c2b233b27a88ccab3f` |

## Boundaries and next reuse

- The result supports canonical-portrait-only, face-readable, staged changes
  across this close-portrait to knee-up kitchen and wardrobe path. It does not
  yet prove large pose or angle changes, full-body distance, complex motion,
  different expressions, multi-image batch continuity, or general superiority
  over GPT Pro.
- T02 must not be used automatically as Image C. If the user wants a
  face-included continuity transfer, first get explicit permission for one
  downstream transfer trial, generate only that one image, create the identity
  comparison, and wait for explicit approval before recording
  `anchor_transfer_approved` or generating the rest of the set.
- Until that transfer test is approved, reuse T02's selected wardrobe as text,
  while continuing to generate independently from the canonical portrait.
- The three generated files and comparison artifacts remain local review
  outputs. They were not formally copied into the repository or Git-tracked in
  this run.

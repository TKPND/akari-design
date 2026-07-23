# Akari v1.1 Humanization Pass Plan

**Goal:** Apply a one-image-at-a-time finishing pass to accepted `となりのあかり` candidate images before final PDF work. The pass must reduce over-polished AI smoothness without changing Akari's identity, composition, outfit, pose, or page intent.

**Source instruction:** external finishing workflow prompt, not included in this repository.

## Scope

- Work only in the Tonari No Akari feature worktree.
- Process one image per review loop.
- Do not update the Tonari PDF, run PDF OCR audits, or replace original generated candidates during this pass.
- Save finish candidates under `source/finished/tonari-no-akari/`.
- Save comparison evidence under `evidence/finish-pass/`.
- Track finish status in `source/manifests/tonari-no-akari/finish-pass-manifest.json`.

## First Image

Start with `window-breath` because the source instruction includes specific H05 guidance for that page and the current candidate has low footwear risk.

- Source: `source/generated/tonari-no-akari/20260701_window-breath_v1.webp`
- Output: `source/finished/tonari-no-akari/20260701_window-breath_v1_finish_h05_v1.webp`
- Stage: `humanization`
- Strength: `H05`

## Prompt Template

```text
TASK: Subtle finishing edit / humanization pass for one existing illustration.

Use the provided input image as the primary source. Preserve the same composition, crop, camera angle, pose, background layout, outfit design, and character identity. Do not create a new scene. Do not make a collage. Do not create side-by-side panels. Output one full-frame image only.

Character identity lock:
Akari is a 25-year-old Japanese woman with a naturally cute adult impression, not glamorous and not childlike. Keep her short fluffy light-brown bob, airy uneven hair ends, soft side bangs, warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth, and pale blue crossed hairpins / ribbon-like hair clips on the visible side. Keep her body proportions and page-specific outfit exactly consistent with the input image.

Goal:
Make the illustration feel slightly less AI-polished and slightly more like a finished human-drawn everyday anime illustration. Keep the quality high. This is a 5% finishing adjustment, not a redraw.

Allowed micro-edits:
- Add a few subtle flyaway hairs and tiny irregularities in the bangs and hair tips.
- Add very small natural fabric wrinkles, sleeve looseness, cloth weight, and lived-in folds.
- Slightly reduce airbrushed skin and overly glossy highlights.
- Add very subtle natural asymmetry to the expression without changing the face structure.
- Add slight line-weight variation and uneven hand-drawn edge softness.
- Make the lighting feel a little more like natural everyday room/street light, not perfectly staged.

Window-breath page addendum:
Preserve the quiet morning indoor mood and the hand near the curtain. Add only subtle hair-end looseness, a few flyaway hairs, tiny wrinkles on the white cardigan and roomwear, and slightly less perfect airbrushed highlights. Keep the face and expression nearly identical. Do not change the hand pose or curtain composition.

Do not change:
Face structure, eye shape, eye color, nose, mouth, jaw, hairstyle silhouette, hair length, hair ornament, age impression, body proportions, outfit design, pose, hands, feet, shoes, background layout, time of day, or aspect ratio.

Negative constraints:
No anatomy errors, no extra fingers, no fused fingers, no distorted hands, no distorted feet, no shoe drift, no missing hairpins, no changed clothing, no added text, no logos, no watermarks, no frame, no border, no panel layout, no collage, no heavy sketch filter, no low-quality noise, no over-sexualization, no childlike presentation.

Output:
One edited image only, same composition and aspect ratio as the input, with subtle human-drawn irregularities while preserving Akari's identity.
```

## Review And Evidence

For each finish candidate:

- Verify the output is a single PNG with the same dimensions and aspect ratio as the source.
- Verify the original source image was not overwritten.
- Create a normal A/B contact sheet and a blind A/B contact sheet.
- Keep the blind mapping in JSON for review after the first impression pass.
- Stop after one image and wait for human selection before moving to the next candidate.

## Acceptance Gate

Accept a finish candidate only if human review keeps these scores at or above the threshold:

- `identity_preservation >= 4`
- `face_consistency >= 4`
- `hair_and_hairpin_consistency >= 4`
- `anatomy_integrity >= 4`
- `composition_preservation >= 4`
- `ai_polish_reduction >= 3`

Use the original image if the finish candidate weakens the face, age impression, hair silhouette, hair ornament, hands, composition, or everyday tone.

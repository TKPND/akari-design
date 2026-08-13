# Akari V2.2 Face-Angle Preservation and Routing Design

Date: 2026-08-13
Status: approved direction; written-spec review pending

## Decision

Preserve the user-approved F00, F01-r02, and F02 images as a small supporting
face-angle authority pack. Keep the existing canonical portrait and full-body
images unchanged. The face-angle pack supplements the canonical portrait for
one intended head direction at a time; it does not replace the portrait or
become a three-image face blend.

## Accepted Files

Copy the reviewed PNG bytes without resizing, cropping, recompression, color
conversion, or retouching into:

- `akari-v2.2/accepted/base/face-angles/akari-v2.2-face-near-front-f00.png`
  - SHA-256:
    `8ff5e5369b9877225b2c2bbc87ea92b6cb0e60309e846cb9250fc2a366cae957`
- `akari-v2.2/accepted/base/face-angles/akari-v2.2-face-hairpin-side-f01-r02.png`
  - SHA-256:
    `a8d1574fd1edb071be5ddf111768aa1e5c8fa38a02d5f7aac76b5023823e6902`
- `akari-v2.2/accepted/base/face-angles/akari-v2.2-face-opposite-side-f02.png`
  - SHA-256:
    `338568d22fc150b5b965b259a731de1d30d33c41d0d1238e3c28c044cb7734ad`

F01-r01 remains comparison history only and is never copied into the accepted
pack or used as a generation input.

## Authority Hierarchy

1. The canonical portrait remains the primary authority for Akari's base face
   identity, eye construction, cheeks and chin, bangs, hairpin, side ponytail,
   age impression, line weight, and close-view paint density.
2. The canonical full-body image remains the primary authority for body balance,
   baseline outfit construction, pose, laterality, and complete-figure
   presentation.
3. Exactly one face-angle image may supplement the portrait for the intended
   head direction and the perspective relationship among the eyes, cheeks,
   jaw, ear, bangs, hairpin, and ponytail.

If an angle image conflicts with the canonical portrait's base identity, the
canonical portrait wins. If face and body references compete, the portrait wins
for the face and the full-body image wins only for body and outfit information.

## Angle Routing

Choose the support image from Akari's intended head direction before composing
the tool call:

| Intended head direction | Supporting image | Role |
| --- | --- | --- |
| Near-front or shallow three-quarter, with both eyes similarly readable | F00 | Neutral closed-mouth near-front face relationship |
| About 30 degrees toward Akari's hairpin side, with the hairpin side nearer and more visible | F01-r02 | Hairpin-side eye, cheek, jaw, ear, hairpin, and ponytail perspective |
| About 30 degrees toward the side opposite the hairpin, with the hairpin naturally less visible | F02 | Opposite-side eye, cheek, jaw, ear, bangs, and ponytail perspective |

Interpret the direction from Akari's character anatomy, not from a later canvas
flip. These references do not define strict profile, rear, overhead, or extreme
foreshortened views. For an angle outside the pack, do not pretend the closest
image is an exact authority; use the canonical portrait and a task-specific
transition gate.

## Reference Budget

Keep the existing maximum of three input images, but treat it as a ceiling:

- Always include the canonical portrait for a new identity-sensitive scene.
- Add exactly one matching face-angle image when its angle information is
  needed.
- Add the canonical full-body image only when the call needs body balance,
  laterality, or baseline outfit construction.
- If a separate wardrobe or approved continuity reference is essential, remove
  an unnecessary full-body or angle reference rather than adding a fourth
  image.
- Never pass F00, F01-r02, and F02 together. Never use one face-angle image to
  generate or reinterpret another.

The prompt must identify the canonical portrait as the base face authority and
the selected angle image only as head-direction support. These labels describe
intent; they do not guarantee model weighting or a face lock.

## First Downstream Use

Updating the generation skill changes the input conditions, so the next
built-in image-generation session still begins with its existing canonical
portrait-only environment preflight. The first scene that uses one of the new
angle images is then generated alone as a task-representative transfer gate.
Create the normal same-scale identity comparison artifact and stop for the
user's identity decision before using that angle image for more outputs.

Approval of one routed downstream image validates that angle image only for the
same environment and workflow. It does not turn the generated scene into a new
identity authority or validate the other two angles automatically.

## Repository and Skill Updates

- Add the three exact PNGs under `akari-v2.2/accepted/base/face-angles/`.
- Record their acceptance, roles, source labels, dimensions, and hashes in
  `akari-v2.2/selection.md`.
- Update `akari-v2.2/README.md` with the authority hierarchy and routing table.
- Update the global `generating-akari-v2-2-images` skill to resolve and route
  the accepted pack while preserving its three-reference limit, user identity
  gate, and retry stops.
- Keep manual review comparisons, rejected revisions, prompts, and temporary
  GPT Pro packaging out of Git.

## Verification

- Verify each accepted PNG is byte-identical to the approved working copy.
- Confirm the three accepted dimensions are `1086x1448`, `1086x1448`, and
  `1024x1536` respectively.
- Scan the repository and skill text for all three routed paths and the
  one-angle-only rule.
- Validate the global skill with its standard `quick_validate.py` command and
  lint all changed Markdown.
- Confirm no rejected or comparison-only image became tracked or referenced as
  an input.

## Out of Scope

This step does not generate S03 or any other scene, replace either canonical
image, promote a generated downstream scene, or commit unrelated local work.

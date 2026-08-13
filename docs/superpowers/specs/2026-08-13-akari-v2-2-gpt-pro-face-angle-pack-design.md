# Akari V2.2 GPT Pro Face-Angle Pack Design

Date: 2026-08-13
Status: approach approved; written-spec review pending

## Decision

Pause the uniform school-day scene run after the rejected S02-r02 candidate.
Build three close, simple face references with GPT Pro before resuming scene
generation. Generate and review one image at a time. Do not create a multi-face
contact sheet.

The approved route uses one pack-local relay anchor:

1. `F00`: near-front neutral master, matching the canonical portrait's shallow
   three-quarter head angle, with a gentle closed-mouth smile.
2. `F01`: hairpin-side 30-degree view, derived only after F00 passes.
3. `F02`: opposite-side 30-degree view, derived only after F01 passes.

The three outputs remain provisional review material until the user explicitly
accepts every face and separately approves preservation and downstream use.

## Purpose

The current canonical portrait provides a strong close face but only one shallow
angle and one open-mouth expression. Wider scene generation repeatedly replaces
the eye opening and face relationships with a generic face, including vertically
elongated eyes. The face-angle pack supplies large, readable references for the
small set of angles used most often in later scenes.

This is an identity-calibration task, not a scene, outfit, pose, or expression
batch.

## Authority and Input Roles

### F00

- Sole image input: the accepted canonical V2.2 portrait.
- Authority: face silhouette, cheeks and chin, eye opening and placement, iris
  size, brows, nose and mouth placement, bangs, hair, one blue hairpin, low side
  ponytail, age impression, line weight, and paint density.
- Requested changes: remove the hand and scene-like gesture, use a plain warm
  off-white background, keep a white T-shirt, and close the mouth into a small
  relaxed smile.

### F01 and F02

- Image A: the accepted canonical V2.2 portrait, retaining base identity
  authority.
- Image B: F00 only after the user explicitly approves both its identity and its
  use as the pack-local relay anchor.
- Image B supplies the closed-mouth expression, simplified face-reference
  framing, and pack continuity. It does not replace the canonical portrait.
- F01 and F02 are generated independently from Image A plus F00. F01 is never
  forwarded into F02, preventing cumulative drift.

### Excluded Inputs

Do not provide GPT Pro with:

- S02-r01, S02-r02, or any other rejected or pending candidate;
- the canonical full-body image;
- composition-pack images, scene images, or outfit references;
- old-version angle references;
- the lower-resolution R02 eye-rendering calibration image.

The accepted R02 eye-rendering direction may inform review terminology, but the
image itself is excluded to avoid averaging two face inputs before F00 exists.

## Image Contract

Each output is one character in one finished image:

- close head-and-shoulders or tight bust-up framing;
- large, unobstructed face;
- plain warm off-white background;
- plain white T-shirt;
- relaxed direct gaze;
- gentle closed-mouth smile with no visible teeth or tongue;
- warm chestnut hair, canonical bangs, low side ponytail with blue tie;
- one blue capsule hairpin in its canonical location, never mirrored or
  duplicated;
- no hands, props, text, labels, borders, inset panels, or decorative symbols.

For F01, turn the head about 30 degrees toward the hairpin side while keeping
that side readable. For F02, turn the head about 30 degrees toward the opposite
side. Natural occlusion of the hairpin is allowed in F02; relocation, mirroring,
or a second hairpin is not.

Prompts stay short. They identify the input roles, the single angle change, the
simple presentation, and only the most important prohibitions. They do not
numerically redesign the face or prescribe a new eye shape.

## Serial Gates

1. Ask GPT Pro for exactly one F00 image and stop.
2. Present a same-scale comparison of the canonical face and F00. The user
   decides identity; Codex may only reject an obvious mismatch.
3. If F00 passes, ask separately whether it may become the pack-local relay
   anchor. Identity acceptance alone does not grant anchor use.
4. After anchor approval, ask GPT Pro for exactly one F01 image and stop.
5. If F01 passes, ask GPT Pro for exactly one F02 image and stop.
6. Any rejection stops the route. A retry requires a new explicit user request
   and may change only one observed variable.

Rejected, pending, or comparison-only images are never inputs, edit targets,
anchors, crops for continuity, composites, or prompt-derived continuity
references.

## Identity Review

Review the face before hair, clothing, or presentation quality. Compare at the
same display scale without warping or landmark fitting.

The user checks:

- the eyes have not become vertically elongated or symmetrically generic;
- eye opening, iris size, white-space balance, and brow-to-eye spacing remain
  consistent with the canonical identity at the requested angle;
- cheeks, jaw transition, chin length, nose and mouth placement, and age
  impression still read as Akari;
- the closed mouth works with the cheeks rather than flattening the expression;
- bangs, face-framing locks, ponytail, hairpin side, line weight, and paint
  density remain coherent.

Background, clothing, and rendering polish cannot compensate for an identity
failure.

## Working Package

After written-spec approval, create an ignored manual-upload bundle under:

`tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/`

The bundle contains:

- `PROMPT.md`: scope, serial workflow, input roles, and review gates;
- `reference/01-canonical-portrait.webp`: the sole F00 image input;
- `prompts/F00.txt`, `prompts/F01.txt`, and `prompts/F02.txt`: short prompts,
  with F01 and F02 clearly blocked until their preceding gates pass;
- `DECISIONS.md`: pending, approved, rejected, and anchor-use states;
- `tree.txt` and a sanitized archive for manual GPT Pro upload.

Creating the package does not generate an image. GPT Pro generation remains a
manual external step, one image at a time.

## Preservation and Downstream Use

Even after all three faces pass, do not automatically:

- copy them into `akari-v2.2/accepted/`;
- change the global V2.2 image-generation skill;
- make them canonical authorities;
- resume S03 or any other scene generation;
- commit generated image files.

Those actions require a separate user decision. If preservation is approved,
the follow-up design must define which single angle reference is selected for a
given scene so later generation does not average the whole face pack.

## Success Criteria

- F00, F01, and F02 are generated serially and reviewed independently.
- Every accepted image reads as the same Akari to the user.
- No rejected or pending image is reused.
- Eye height does not drift toward the rejected generic-face pattern.
- The result is a small, practical face-angle reference set rather than a large
  expression or turnaround project.
- Promotion, skill changes, and scene resumption remain explicit later gates.

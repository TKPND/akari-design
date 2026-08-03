# Akari v2.0 Front Master Full-Body Design

Status: approved for GPT Pro generation.

Date: 2026-08-03.

## Goal

Promote Akari v2.0 around one stable front-view identity. Preserve the approved
FRONT MASTER as the sole face authority, extend it into one practical full-body
front reference with GPT Pro, and commit those two canonical images as the
minimal v2.0 package.

## Canonical Assets

The package will contain exactly two canonical images:

1. The existing FRONT MASTER, retained byte-for-byte as the face, eye, hair,
   skin, and expression authority.
2. One GPT Pro full-body front image derived from the FRONT MASTER.

Oblique, rear-three-quarter, rear, daily-pose, and outfit-variation images are
not canonical v2.0 assets. They may remain local generation aids because the
image-generation workflow can infer those views from the two front authorities.

## Character Lock

- Age impression: 18-year-old young adult.
- Read: cute, approachable childhood-friend familiarity rather than idol or
  fashion-model posing.
- Face: preserve the FRONT MASTER's eye shapes, iris sizes, amber color,
  eyebrows, cheek width, rounded lower face, compact chin, nose, open smile,
  and skin treatment. Do not redraw or reinterpret the face.
- Hair: warm chestnut, off-center V bangs, low side ponytail on character-left,
  and pale-blue crossed ornament on character-left.
- Body: compact and healthy, with moderate shoulders and torso, restrained
  bust, subtle waist, natural arms, and full thighs and calves.

## Full-Body Image Contract

- Camera: strict front view at approximately zero degrees.
- Framing: vertical, complete figure from hair to shoe soles, with comfortable
  margins and no cropped limbs.
- Pose: relaxed neutral standing pose, level shoulders and pelvis, both feet
  planted, arms resting naturally, no gesture pose.
- Base outfit: plain white T-shirt, navy A-line mid-thigh shorts, white socks,
  and generic blue-and-white sneakers.
- Waist details: exactly two short drawcord ends and no bow.
- Organizer: one slim vertical navy organizer on character-left, which appears
  on canvas-right in the front view, with one tiny warm-metal zipper pull.
- Background: plain warm off-white with only a restrained grounding shadow.
- Rendering: match the FRONT MASTER's anime line quality, soft cel shading,
  warm palette, and finish.

## GPT Pro Generation Method

Use the FRONT MASTER as the primary image and extend it downward. Preserve its
existing head, face, hair, neck, visible shoulders, and visible white T-shirt
as closely as the tool permits. Use the prior white-T full-body image only as a
secondary guide for body balance, shorts, organizer, socks, and shoes; its face
is not an identity reference.

Generate one final PNG, not a contact sheet or multiple variants. Do not add
labels, measurements, text, decorative graphics, props, or a jacket.

## Acceptance Gates

The returned full-body image is eligible only when all of these pass:

1. Same-person face read against the FRONT MASTER at enlarged scale.
2. No drift in eye shape, iris size, cheek width, chin length, mouth, hairline,
   ponytail side, or ornament side.
3. Complete, anatomically coherent full body with the approved compact healthy
   proportions.
4. Correct white-T outfit, exactly two drawcord ends, one organizer on
   character-left/canvas-right, socks, and generic sneakers.
5. Strict front-view neutral pose and uncluttered presentation.
6. Clean PNG with no visible edit seam, border, text, watermark, or generation
   artifact.

## Promotion Contract

After explicit user approval, copy both canonical PNGs without transformation
under `akari-v2.0/accepted/base/`. Record their roles, source lineage, dimensions,
SHA-256 hashes, and selection decision in a concise `README.md` and
`selection.md`. Keep generated candidates and comparisons untracked. Run only
the relevant lightweight image, scope, and Markdown checks; PDF audit and
Python tests are explicitly out of scope.

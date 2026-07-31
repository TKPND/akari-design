# Akari v1.6 Back View Design

Status: approved design, awaiting implementation planning.

Date: 2026-07-31.

## Summary

This design adds one canonical straight-back full-body view to the approved
Akari v1.6 character baseline. It closes the rear construction of the bob,
cropped box T-shirt, soft culotte shorts, smartwatch, socks, and sneakers
without reopening any approved front or three-quarter decisions.

The back view is a character-reference image on the same warm off-white
seamless background as the approved front baseline. It is not a new pose,
outfit variant, expression study, or turnaround sheet.

## Approved Inputs

The implementation uses these untracked working authorities:

1. `build/v1.6-face-drafts/akari-v1.6-fullbody-base-r1.png`
   - primary authority for body proportions, outfit, standing logic, palette,
     rendering, framing, and scale;
2. `build/v1.6-face-drafts/akari-v1.6-fullbody-pin-side-3q-a1.png`
   - supporting authority for pin-side bob volume, side construction, and
     outfit continuity;
3. `build/v1.6-face-drafts/akari-v1.6-fullbody-unpinned-side-3q-a2.png`
   - supporting authority for unpinned-side bob volume, cheek-lock continuity,
     and outfit continuity.

The accepted views define one character. Earlier candidates, rejected crossed
leg variants, and v1.3 or v1.5 bodies are not generation authorities.

## Composition and Pose

- Use one exact straight-back, complete full-body reference view.
- Keep the 152 cm concept and approximately 6.6-head petite adult ratio.
- Preserve the approved small, gently sloped shoulders, compact ribcage,
  subtle waist, and modest healthy softness at the hips and upper thighs.
- Translate the approved standing logic coherently to the rear: anatomical
  right leg bears the weight; anatomical left leg rests a small half-step
  forward and slightly to its own side.
- Keep knees, lower legs, ankles, and shoes separated. Do not use a crossed,
  pigeon-toed, catwalk, or rigid turnaround stance.
- Let both arms hang naturally enough to read the rear clothing construction.
  Keep the single smartwatch on the anatomical-left wrist.
- Show all hair, both hands, both shoes, and the faint contact shadow with
  comfortable margins.

## Rear Hair Construction

- Keep a compact, normally rounded Honey Brown bob with a gentle inward nape.
- Preserve the established crown flow, selective internal-line economy, and
  broad authored highlight planes.
- Make the anatomical-left pin side only slightly tighter from behind the ear
  into the nape.
- Keep the anatomical-right unpinned side slightly fuller so it connects to
  the approved front cheek-lock construction without creating a new long rear
  strand.
- Show only the outer tips of the two short, equal-length, parallel pale
  ice-blue pins at the anatomical-left silhouette.
- Do not move the pins onto the back of the head, enlarge them, cross them, or
  add another ornament.

## Rear Outfit Construction

### T-shirt

- Preserve the ivory matte cotton-jersey cropped box T-shirt.
- Keep the back neckline, shoulder seams, short wide sleeves, and restrained
  fabric folds simple and practical.
- Keep the rear hem almost level with the front hem.
- Show only a narrow strip of lower-back skin above the high waistband.

### Culotte shorts

- Preserve the mist-blue soft matte woven fabric, natural high waist,
  mid-thigh length, and modest A-line volume.
- Use shallow, fine gathers across the rear elastic section. The gathering
  must explain movement without reading as lounge shorts.
- Add no rear pockets, welt openings, patch pockets, belt loops, drawstring,
  fly emphasis, or tailoring crease.
- Preserve two clearly separate leg openings. Do not turn the garment into a
  skirt, tight shorts, gym shorts, or stiff tailored shorts.

### Accessories and footwear

- Keep one slim smartwatch on the anatomical-left wrist with a small dark
  face and mist-blue band.
- Keep low ivory ankle socks.
- Keep the approved rounded ivory low-top sneakers, thin practical soles, and
  restrained mist-blue accents. The heel view may reveal a small mist-blue
  accent but no new logo or decorative panel.

## Rendering and Background

- Match the approved warm anime character-reference rendering and clean line
  hierarchy.
- Use a warm off-white seamless background with no room, floor line, prop, or
  text.
- Use only a faint, soft contact shadow beneath the separated shoes.
- Keep skin, cotton jersey, woven culotte fabric, socks, and shoes matte and
  practical. Avoid glossy sportswear or global relighting.

## Non-Goals

- Do not redesign the approved face, hair, body, outfit, or palette.
- Do not create a rear three-quarter view in this pass.
- Do not add an expression, gesture, prop, bag, jewelry, logo, print, or text.
- Do not create a front-and-back sheet, annotations, measurements, or a PDF.
- Do not promote generated working candidates into Git during review.

## Acceptance Criteria

The back-view candidate passes when all of the following are true:

- it reads as the same petite 25-year-old adult character as the accepted
  front and side views;
- body scale, shoulder width, waist, hips, thighs, and limb lengths remain
  consistent with the approved baseline;
- the bob is compact and rounded, with only a slight pin-side tightening;
- only the outer tips of two parallel pins are visible at anatomical left;
- the T-shirt hem is nearly level and the rear skin gap stays narrow;
- the culotte has fine restrained rear gathers and no rear pockets;
- the smartwatch remains on anatomical left;
- both arms, legs, hands, socks, and shoes are anatomically coherent and fully
  visible;
- the legs and shoes do not cross or overlap;
- the background, lighting, rendering, and full-body framing match the
  accepted reference family;
- there is no text, watermark, extra ornament, or unapproved redesign.

## Verification and Review

The first generated back view is saved under the ignored
`build/v1.6-face-drafts/` working directory. It is reviewed beside the approved
front and both three-quarter full-body views. A failed hard invariant receives
at most one targeted correction before the design returns to a user decision
gate.

Generated candidates and comparison sheets remain untracked unless the user
later approves a durable release destination.

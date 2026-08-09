# Akari v2.2 Milky Pastel-Pop Batch Design

Date: 2026-08-10
Status: direction approved; written-spec review pending

## Goal

Create six new portrait-format Akari v2.2 daily-life candidates that keep the
clear face-to-hand-to-object reading of the accepted pop scenes while reducing
the previous batch's saturation. The images should feel softly pastel rather
than washed out, and physically readable rather than like graphic collages.

The six outputs remain ignored working candidates until the user explicitly
selects any image for formal preservation.

## Visual Direction

Use a **milky physical-pop** balance:

- roughly 75% coherent daily-life scene and 25% flat pop treatment;
- decorative color fields occupy about 12–18% of the frame;
- one main pastel color, one supporting pastel color, and the canonical blue
  hairpin act as the primary color hierarchy in each image;
- background, clothing, props, and shadows are about 15–20% softer and less
  saturated than the preceding pop-study batch;
- hair, amber-brown eyes, lashes, expression, hand-to-object contact, and the
  blue hairpin retain enough contrast to preserve identity and action clarity.

Do not solve the pastel request by applying a uniform white haze. Whites remain
warm, skin remains healthy, and the focal face and contact point remain crisp.

## Identity and Reference Roles

- `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp` is the
  authority for face, eyes, hair, hairpin, and low side ponytail.
- `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp` is the
  authority for body proportions, adult impression, and laterality.
- D28 rubber-glove snap and D29 headphone listen are the closest accepted
  anchors for face-forward pop composition and sparse nonfigurative accents.
- The local cute-composition references may inform close framing, diagonal
  energy, clean cel shapes, foreground scale, and color rhythm only.

Do not copy a reference character, face, hairstyle, outfit, mascot, pose,
decorative layout, poster border, sticker outline, symbol field, or readable
text.

## Palette and Rendering

Core palette:

- warm white: `#FFF9F4`;
- powder aqua: `#CBE6E7`;
- blush coral: `#F2B8B0`;
- butter cream: `#F2DEAA`;
- pale periwinkle: `#C9CDE8`;
- dusty denim: `#7894AA`;
- cocoa hair: `#6B4338`;
- dark cocoa line: `#4D3D3A`.

Rendering rules:

- retain clean two-step cel shading;
- use shallow cool lavender or blue-gray shadows;
- use dark cocoa rather than pure black for most outlines;
- keep inner lines lighter and thinner than the outer contour;
- simplify copper hair highlights into one soft chestnut band;
- reserve the strongest contrast for the eyes, lashes, expression, and the
  hand-to-object contact point;
- use at most one large pale rounded field plus two to four small dots, arcs,
  or scene-derived marks;
- no stars, hearts, enclosing frames, text, logos, or watermarks.

## Six Scenes

### 01 — Glasses Cloth Polish

- Extreme close view at a slight diagonal.
- Akari holds the temple of plain glasses with one hand and wipes one lens with
  a soft cloth in the other, looking through the unobstructed lens.
- Use powder aqua and pale periwinkle accents.
- Keep both hands connected, the cloth visibly touching one lens, both temples
  coherent, the single blue hairpin visible, and the glasses free of text or
  branding.

### 02 — Ice Tray Twist

- Waist-up kitchen-counter view with the translucent tray large in the
  foreground.
- Akari twists opposite ends of one pale-aqua ice tray so one cube falls into a
  bowl directly below.
- Use powder aqua and butter cream accents.
- Keep two hands on opposite tray ends, one continuous tray, one falling cube,
  a supported bowl, and a simple coherent counter plane.

### 03 — Pastel Tape Cut

- Low tabletop close view, with the tape strip leading toward Akari's focused
  smile.
- One hand stabilizes a plain desktop dispenser while the other draws a single
  strip of pale tape down onto the cutter.
- Use blush coral and warm white accents.
- Keep one roll, one continuous tape strip, one cutter edge, and separate
  readable fingers. Do not add labels or writing.

### 04 — Phone Case Corner Snap

- Face-and-hands close view with the last phone corner nearest the camera.
- Akari presses one corner of a plain black-screen phone into a translucent
  powder-aqua case with her thumb.
- Use powder aqua and blush coral accents.
- Show exactly one phone and one case, with three corners already seated and
  the final corner visibly entering the case. No UI, text, logo, or extra
  device.

### 05 — Hand-Crank Pencil Sharpener

- Desk-height three-quarter view with the crank forming a small diagonal.
- One hand steadies a plain manual sharpener while the other turns its connected
  handle; one thick colored pencil enters the front opening.
- Use pale periwinkle and butter cream accents.
- Keep the pencil, opening, crank shaft, handle, and supporting hand physically
  connected and distinct. Avoid brand marks and loose duplicate parts.

### 06 — Seatbelt Click

- Stopped-car waist-up view from the passenger-side dashboard area.
- Akari guides one metal tongue into the buckle at her hip while smiling toward
  the viewer.
- Use dusty denim and blush coral accents with a warm-white cabin.
- Keep the belt continuous from shoulder across torso to hip, the tongue aligned
  with one buckle, her body supported by the seat, and the car visibly parked.
  No dashboard text, logo, or moving-road cues.

## Output and Review Loop

- Use the built-in image-generation path, one distinct call per scene.
- Before each call, visibly reopen the canonical portrait and full-body
  authorities, the most relevant accepted pop anchor, and the strongest
  applicable local composition reference.
- Save all six final candidates under
  `tmp/akari-v2.2-pastel-pop-study-20260810/r01/` with numbered descriptive
  filenames, a prompt ledger, and a labeled contact sheet.
- Review each output for identity, adult impression, anatomy, prop contact,
  spatial support, pastel balance, decoration density, reference-copy risk,
  text, logo, watermark, and image artifacts.
- Correct only narrow defects. Preserve successful composition and identity
  during any refinement.
- Present the complete contact sheet for selection. Promote nothing until the
  user explicitly accepts it.

## Success Criteria

The batch succeeds when all six requested scenes exist, Akari remains clearly
the same v2.2 adult character, each action target is physically readable at a
glance, and the palette is visibly softer than D28/D29 without losing facial or
gesture clarity. Pop decoration must support the composition and never become
the subject.

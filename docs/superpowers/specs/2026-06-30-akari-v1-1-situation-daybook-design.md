# Akari v1.1 Situation Daybook Design

## Summary

Create a separate 10-12 page 16:9 landscape PDF that expands the accepted
lakeside bench image into a small situation daybook. This document is not a
replacement for `dist/akari-v1.1-settings.pdf`; it is a companion booklet for
scene mood, visual direction, and lightweight generation notes.

The strongest anchor is the accepted summer image: Akari sitting on a shaded
bench near water, wearing a simple white T-shirt outfit, holding a bottle, and
lit by clear natural daylight. The daybook should preserve that calm summer
distance while adding a small number of light, weather, and time-of-day
variations.

## Goals

- Build a viewing-first companion PDF that still helps future image generation.
- Preserve the accepted image's mood: summer daytime, water, tree shade, white
  T-shirt, simple gray bottom, pale blue accents, and close everyday distance.
- Keep the page text short: a title, one atmosphere note, and three generation
  notes per scene.
- Keep all text deterministic and outside generated image binaries.
- Reuse the existing PDF pipeline patterns where practical without changing the
  primary settings PDF contract.
- Keep generated assets traceable through manifests, accepted/rejected status,
  and source paths.

## Non-Goals

- Do not turn this into a full character settings document.
- Do not replace or rename the existing settings PDF.
- Do not make a prompt archive page that overwhelms the visual daybook.
- Do not create text-heavy lore pages.
- Do not force low-diff image compositing when it breaks anatomy, props, or
  object continuity.
- Do not embed captions, titles, labels, prompt text, or notes inside generated
  image pixels.

## Core Decisions

- Working title: `Akari v1.1 Situation Daybook`.
- Output PDF path: `dist/akari-v1.1-situation-daybook.pdf`.
- Format: 16:9 landscape, matching the settings PDF page geometry.
- Length: target 10-12 pages.
- Role: visual scene booklet plus lightweight generation notes.
- Anchor image role: cover and mood standard.
- Visual direction: `Summer Daybook with Light Notes`.
- Language: English for PDF titles, captions, and notes.
- Text strategy: all readable text is rendered as PDF-native text or stored in
  non-binary sidecar files.

## Text And Binary Image Rules

Generated scene images must be illustration-only. They must not contain
intentional readable text, page labels, captions, prompt notes, watermarks,
logos, or typography. If a scene would naturally include signage, vending
machine panels, packaging, or shop fronts, the generation prompt should keep
that text abstract, blurred, cropped, or visually unreadable.

The PDF renderer owns all reader-facing text:

- Page titles.
- Atmosphere notes.
- Generation notes.
- Source chips.
- Review labels.
- Rejection or warning labels.

Sidecar manifests own production metadata:

- Source asset IDs.
- Prompt summaries.
- Accepted/rejected review state.
- Generation IDs.
- Candidate paths.
- Deviation notes.

This keeps text searchable, editable, auditable, and independent from the image
binary.

## Visual Anchor

The accepted anchor image is a 1280x720 sRGB scene showing Akari on a lakeside
bench in summer daylight. During implementation it should be imported into the
project under a stable source asset ID, for example
`situation-daybook-lakeside-bench-cover`, with its original file kept immutable.

Anchor qualities to preserve:

- Warm brown short bob and gentle Akari expression.
- Simple white T-shirt outfit with gray bottom.
- White socks with pale blue stripes and white/pale-blue sneakers.
- Small pale bag and bottle as everyday props.
- Tree shade over the bench, bright open water, and blue sky.
- Wide 16:9 breathing room to the right of the character.
- Relaxed seated posture with complete, connected limbs and shoes.

## Page Model

Each scene page should use one large image and a small notes area. The notes
area should not compete with the image.

Required text per scene:

- Scene title.
- One sentence atmosphere note.
- Three short generation notes, normally covering light, composition, and
  outfit/props.

Optional metadata should remain in manifests, not on the page.

## Initial Page List

1. Cover: `Lakeside Bench`
   - Uses the accepted anchor image.
   - Establishes the visual standard for the daybook.
2. `Shade Break`
   - Bench and tree shade, shortly before or after drinking water.
   - Notes: leaf-shadow edges, relaxed hands, bottle scale.
3. `Convenience Walk`
   - Summer walk after a convenience-store stop.
   - Notes: small bag or bottle, no readable package text, bright pavement.
4. `Riverside Path`
   - Akari walking or pausing on a water-side path.
   - Notes: wide right-side negative space, rail or path perspective, clear sky.
5. `Park Steps`
   - Sitting on low steps or a stone edge in the same summer outfit family.
   - Notes: stable seated anatomy, complete shoes, grounded shadow.
6. `Window Seat`
   - Indoor summer afternoon by a window.
   - Notes: soft side light, simple room props, white T-shirt still central.
7. `Rain-Cooled Street`
   - Rain-afterglow street with damp pavement.
   - Notes: readable text avoided, reflection control, optional light cardigan.
8. `Station After Sun`
   - Late afternoon near a small station or transit stop.
   - Notes: warm rim light, simple thin outer layer, no station text dependency.
9. `Vending Machine Night`
   - Evening or night scene with cool practical light.
   - Notes: unreadable vending details, color temperature contrast, calm face.
10. `Golden Hour Return`
    - Return path at sunset.
    - Notes: warm backlight, long shadows, keep outfit silhouette readable.
11. `Generation Notes`
    - A compact page summarizing what to preserve and avoid.
    - Uses PDF-native text and optional small thumbnails only.
12. `Candidate Contact Sheet`
    - Optional page for accepted candidate thumbnails.
    - Uses PDF-native labels only.

Pages 11 and 12 may be omitted if the first pass is stronger as a 10-page
visual booklet.

## Scene Generation Guidance

Prompts should be written to preserve the anchor mood rather than maximize
novelty. A good prompt keeps the scene simple, readable, and grounded.

Stable elements:

- Akari identity from the settings PDF.
- White T-shirt as the outfit anchor.
- Gray or muted neutral bottom.
- Pale blue accents in socks, shoes, or small accessories.
- Everyday props such as bottle, small bag, or light outer layer.
- 16:9 composition with enough breathing room for PDF layout.

Allowed variation:

- Light: clear midday, shade, golden hour, window light, rain-afterglow, night
  practical light.
- Setting: water-side park, path, steps, small station, quiet street, indoor
  window seat.
- Outfit detail: thin cardigan, small hat, bag, bottle, or seasonal prop.

Avoid:

- Heavy fashion redesigns.
- Text/logos/signage in the image.
- Crops that cut off feet, hands, or hair.
- Low-diff composites that visually disconnect limbs or props.
- Excessive story text or lore on the page.
- Dramatic action poses that break the quiet daybook mood.

## Asset And Manifest Strategy

The daybook should have separate document data from the settings PDF. It may
reuse renderer utilities and styles, but should keep its own page list, asset
IDs, and output paths so the settings PDF remains stable.

Recommended sidecar data:

- Daybook page manifest for page order and text.
- Daybook asset manifest for accepted scene images.
- Generation request records for new scene candidates.
- Review notes for identity, composition, text-in-image, and continuity checks.

Image imports should preserve originals. Generated candidates should live under
`source/generated/` until accepted. Build intermediates belong under `build/`.

## Acceptance Criteria

- The daybook renders as a 16:9 PDF separate from the settings PDF.
- The accepted lakeside bench image is used as the cover or first visual page.
- Every reader-facing title, note, and label is PDF-native text, not baked into
  generated image pixels.
- Generated scene images contain no intentional readable text, labels,
  captions, logos, or watermarks.
- Each scene has a title, one atmosphere note, and three generation notes.
- Scene images preserve Akari identity, outfit anchor, full limb continuity, and
  everyday summer mood.
- The implementation can build previews and the PDF through npm scripts.
- Markdown, manifest, and PDF audits can verify the document without changing
  the primary settings PDF.

## Verification Plan

Minimum verification after editing this design:

- `npm run lint:md`

Expected implementation verification:

- Node tests for the separate daybook document model.
- Python manifest tests for daybook asset/page contracts.
- Preview rendering for every daybook page.
- PDF audit for page size, page count, non-blank rendering, and searchable text.
- Manual visual review for text-in-image violations and anatomy continuity.

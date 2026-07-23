# Akari v1.1 Palette-Anchored Master PDF Design

## Summary

Create a polished, multi-page Akari v1.1 settings PDF that works as both a presentation document and a practical production reference. The document will use a D65/6500K sRGB palette page as the color source of truth, then regenerate or color-correct major assets against that palette.

The final document is a 12-page, 16:9 landscape, English-labeled PDF. It should preserve Akari's identity while producing a cleaner, more consistent reference set than the current loose image collection.

## Goals

- Produce a usable character settings PDF for Akari v1.1, not just a collage of existing images.
- Use D65/6500K sRGB color assumptions so the character, outfit, shoes, and bag read consistently.
- Avoid resolution loss from image-generation compositing. When aspect ratio, layout, or image framing is wrong, regenerate an asset or page component at the intended format instead of gluing smaller images together.
- Preserve the existing strongest materials as references, especially the expression sheet, footwear boards, and bag board.
- Keep source files, generated assets, corrected assets, previews, manifests, and final PDF outputs traceable.
- Lock identity, proportions, left/right rules, and PDF layout enough that future Akari variants can be checked against v1.1.

## Non-Goals

- Do not build an 18+ page exhaustive production bible in the first pass.
- Do not edit original source PNGs destructively.
- Do not rely on Japanese text inside generated images. The final PDF labels and body copy are English.
- Do not treat D65 as a substitute for physical display calibration. This design defines a consistent sRGB/D65 document target.
- Do not treat embedded text in existing bitmap boards as final PDF text.

## Existing Source Inventory

Current source images in the workspace:

- `v1_1_front_1.webp`: hoodie full-body front, 1024x1536.
- `v1_1_front_2.webp`: base/body front, 1024x1536.
- `v1_1_front_3.webp`: expression sheet, 1254x1254.
- `v1_1_back.webp`: hoodie full-body back, 1055x1491.
- `v1_1_真横.webp`: side view, 1055x1491.
- `v1_1_髪飾り側_45deg.webp`: hairpin-side 45 degree view, 1055x1491.
- `v1_1_非髪飾り側45deg.webp`: non-hairpin-side 45 degree view, 1055x1491.
- `v1_1_standard_foot_set.webp`: footwear and sock reference board, 1448x1086.
- `v1_1_shoes.webp`: sneaker reference board, 1491x1055.
- `v1_1_bag.webp`: bag/accessory reference board, 1448x1086.

Original PNG files are treated as source evidence. They are copied into `source/originals/` during implementation and then referenced by hash from manifests.

## Core Decisions

- Approach: Palette-Anchored Master PDF.
- Target format: 12 pages, 16:9 landscape.
- PDF page size: fixed 16:9 MediaBox, recommended 13.333 x 7.5 in.
- Target render size: 3840x2160 page previews, with the PDF preserving the same 16:9 aspect ratio.
- Target language: English.
- Color strategy: build a D65/6500K sRGB palette board and a machine-readable palette manifest before final regeneration.
- Regeneration strategy: prioritize consistency over preserving every existing render.
- Identity master: expression sheet.
- Secondary full-body/outfit master: hoodie front full-body image.
- Text strategy: final labels, notes, callouts, and captions are deterministic PDF text, not generated bitmap text.
- Directory convention: use singular `source/` for source and manifest folders.

## Akari Identity And Proportion Lock

This lock is the acceptance contract for every generated, corrected, or relaid-out asset. A visual may be attractive and still be rejected if it drifts from these rules.

### Identity Anchors

- Primary face and hair anchor: `v1_1_front_3.webp`.
- Secondary full-body and outfit anchor: `v1_1_front_1.webp`.
- Base outfit/body anchor: `v1_1_front_2.webp`.
- Turnaround anchors: `v1_1_back.webp`, `v1_1_真横.webp`, `v1_1_髪飾り側_45deg.webp`, and `v1_1_非髪飾り側45deg.webp`.
- Detail anchors: `v1_1_standard_foot_set.webp`, `v1_1_shoes.webp`, and `v1_1_bag.webp`.

### Proportion And Silhouette Rules

- Every full-body production view aligns to shared guide lines: ground, top of head, eye line, chin, shoulder, hoodie hem, skirt hem, knee, ankle, and shoe sole.
- Front, back, side, and 45-degree views must be normalized to the same top-of-head and ground line before comparison.
- The head is slightly large and rounded, but not chibi. Preserve the existing youthful anime proportion instead of moving toward adult fashion illustration or super-deformed proportions.
- Hair volume is a soft short bob around the jaw and neck. Do not lengthen into shoulder-length hair or flatten the side volume.
- The hoodie is oversized with dropped shoulders, soft sleeve volume, visible drawstrings, kangaroo pocket, ribbed cuffs, and a ribbed hem sitting above the skirt.
- The pleated skirt remains gray, short, and visible below the hoodie hem. Do not hide it completely under the hoodie or lengthen it into a knee-length skirt.
- Socks are white crew socks with two pale blue horizontal stripes near the top.
- Sneakers are chunky white sneakers with pale blue accents and rounded volume. Avoid thin running shoes, high heels, boots, or brand-like logo marks.
- Bag scale must be checked against Akari's torso and hip height when shown on-body.

### Left And Right Rules

- Use `character left/right` for design facts and `viewer left/right` only for page layout instructions.
- The hair ornament is on Akari's character-left side, which appears on viewer-right in a straight front view.
- The implementation manifest must record each mirrored or rotated image with its orientation state.
- Do not mirror an accepted Akari view unless the page explicitly labels it as mirrored for comparison.
- Hair ornament, bag strap position, shoe asymmetry, and callout arrows must be checked after every crop, rotation, or regeneration.

### Identity Acceptance Checklist

An asset can be accepted only when these conditions pass visual review:

- Face: warm brown eyes, soft eye shape, small mouth, subtle cheek blush, rounded chin, and gentle expression range.
- Hair: brown short bob, airy bangs with strand separation, soft outward tips, neck-length side/back hair, and no long-hair drift.
- Hair ornament: thin pale blue pins on character-left side, correct count and position, no side flip.
- Outfit: white oversized hoodie, gray pleated skirt, visible hoodie drawstrings and pocket, restrained detail density.
- Shoes and socks: two pale blue sock stripes, chunky white sneakers, pale blue shoe accents, no logo-like marks.
- Bag and accessories: keep scale, strap thickness, metal accents, and pale neutral palette aligned with the bag source.
- Rejection triggers: long hair, changed eye color, large mouth style change, missing hair ornament, flipped ornament, changed skirt length, added brand logos, excessive outfit decoration, or a different overall age/proportion read.

### Expression Set

The expression page should label the nine expressions in English and give a short use note for each. Initial labels:

- Neutral
- Soft Smile
- Open Smile
- Laughing
- Surprised
- Anxious
- Pout
- Sleepy
- Wink

Expression rules: keep eyes soft, avoid extreme sharp anger, keep mouth shapes modest, preserve subtle blush, and avoid making worried expressions read too young or exaggerated.

## Page Structure

1. Cover / Key Visual
   - Clean Akari v1.1 hero page with title and version.
   - Regenerate at the final 16:9 composition.
   - Must pass the identity checklist before use.

2. D65 Color Palette
   - Source-of-truth palette for hair, skin, eyes, hoodie, skirt, socks, shoes, bag, and metal accents.
   - Include named color roles, swatches, base/shadow/highlight ramps where needed, and palette version.
   - Swatches are drawn from `source/palette/akari-v1.1-palette.json`.

3. Character Summary + Proportion / Silhouette Guide
   - Presentation-style summary of Akari's silhouette, personality impression, and core design notes.
   - Include guide lines for ground, top of head, eye line, chin, shoulder, hoodie hem, skirt hem, knee, ankle, and shoe sole.
   - Include short notes for hair volume, hoodie volume, skirt length, sock line, sneaker volume, and bag scale.
   - Use a regenerated or corrected key image only after it passes the identity checklist.

4. Front / Back
   - Production sheet with matched front and back scale, posture, crop, and white balance.
   - Align top-of-head, eye line, hoodie hem, skirt hem, ankle, and ground lines.
   - Regenerate if matching cannot be achieved cleanly.

5. Angle Turnaround
   - Side and 45-degree views focused on hair volume, hoodie shape, skirt, and shoes.
   - Regenerate for consistent scale and D65 color.
   - Label hairpin-side and non-hairpin-side with character-left/right orientation.

6. Expressions
   - Face/hair identity master page.
   - Prefer keeping the existing expression sheet with color correction and clean labels unless audit shows it cannot meet document quality.
   - Add deterministic PDF labels and one-line use notes for the nine expression states.

7. Hair / Face Details
   - Close-up details for hairpin side, bangs, eye color, cheek tone, face proportions, and back/side hair volume.
   - New detail board generated from identity anchors.
   - Use callouts for no-drift face and hair rules.

8. Outfit Rules
   - Hoodie, skirt, base T-shirt/shorts relationship, socks, and silhouette rules.
   - New layout, with callouts for details that should not drift.
   - Clarify which base outfit details are official v1.1 layers and which are only construction reference.

9. Shoes / Socks
   - Footwear detail board with sneaker construction, sock stripe placement, and pose examples.
   - Use existing footwear assets as visual sources, then recreate labels, notes, dimensions, and color chips as PDF text/vector elements.
   - Do not paste the existing board as an unreadable bitmap page.

10. Bag / Accessories
    - Bag board adapted to 16:9 with specs, scale on Akari, material notes, and detail views.
    - Use existing bag views as visual sources, then recreate labels, notes, dimensions, and color chips as PDF text/vector elements.
    - Include on-body scale guidance when possible.

11. Do / Don't
    - Production-facing rules: features to preserve and common mistakes to avoid.
    - Prefer approved assets with redline annotations, comparison frames, and deterministic PDF labels.
    - If a rejected generated example is necessary, label it clearly as `Rejected / Do Not Use` and make it visually secondary to approved examples.

12. Production Notes / Source Manifest
    - Compact traceability page with version, palette version, accepted source asset IDs, major correction notes, review date, and a warning not to use unapproved generated variants.
    - Detailed prompt logs, rejected variants, hashes, and review notes live in sidecar manifest files, not crowded into the PDF page.

## Color And Regeneration Workflow

1. Build the D65 palette board and palette manifest.
   - Define named color roles before final page generation.
   - Store palette data in `source/palette/akari-v1.1-palette.json`.
   - Initial roles: hair, skin, eyes, hoodie white, hoodie shadow, skirt gray, sock white, sock stripe blue, sneaker white, sneaker accent blue, bag body, bag strap, and metal.
   - Hair, skin, hoodie, sneakers, and bag should use base/shadow/highlight ramps rather than a single flat color where shading matters.

2. Lock identity anchors.
   - Use the expression sheet as the primary face/hair identity reference.
   - Use the hoodie full-body front as the secondary body/outfit reference.
   - Record character-left/right orientation and reference hashes in `source/manifests/source-assets.json`.

3. Generate or regenerate key visual assets.
   - Use image generation for missing or inconsistent visual material.
   - Generate at the target page/component aspect ratio when layout or crop matters.
   - Do not use image generation to merge multiple low-resolution references into a finished page.
   - Every generated asset enters the manifest as `needs_review` before it can become `accepted`.

4. Correct existing strong boards.
   - Footwear, sneaker, bag, and expression pages can be retained as sources if color, crop, and legibility pass audit.
   - Final labels, notes, dimensions, and color chips are reconstructed in the PDF layout.
   - Corrected derivatives must be stored separately from originals.

5. Compose the PDF deterministically.
   - Use a layout/export pipeline for text, labels, spacing, page size, and final PDF output.
   - Generated bitmap assets are inputs, not the whole document engine.
   - PDF text must remain searchable unless a specific rendering limitation is documented.

## Palette Manifest Contract

`source/palette/akari-v1.1-palette.json` should be machine-readable and versioned. Each role should include:

- `name`: stable role name.
- `hex`: canonical sRGB hex value.
- `rgb`: canonical sRGB triplet.
- `usage`: where the color is allowed.
- `ramp`: optional `base`, `shadow`, and `highlight` entries for shaded materials.
- `sample_area`: manual or scripted sample guidance.
- `tolerance`: audit tolerance for generated/corrected assets.
- `exception_policy`: when and where deviations may be recorded.

Palette swatches in the PDF must match this file. Existing PNGs without embedded ICC or gamma metadata are treated as assumed-sRGB RGB sources, not as proof of explicit embedded sRGB profiles.

## Generated Asset Acceptance Contract

Each generated or corrected asset gets a manifest entry under `source/manifests/asset-manifest.json` with:

- `id`
- `status`: `needs_review`, `accepted`, `rejected`, or `needs_correction`
- `source_inputs`
- `prompt_summary`
- `model_or_tool`
- `seed_or_generation_id` when available
- `palette_version`
- `orientation_state`
- `identity_check`
- `color_check`
- `layout_check`
- `reviewer`
- `accepted_reason` or `rejected_reason`

Only `accepted` assets can be used in final PDF pages. Rejected assets may appear only on the Do / Don't page when clearly marked as rejected.

## Image Generation Policy

- Use the built-in `image_gen` path for normal generated assets.
- Save project-bound generated assets into the workspace; do not leave final assets only under the default generated image location.
- Use one generation per distinct asset or page component.
- Prompt with exact English labels only when text must appear in the generated image; prefer deterministic PDF text for labels and annotations.
- Avoid white-background chroma key for Akari assets because the hoodie, socks, shoes, and bag contain white or pale colors.
- If transparency is needed, prefer generation with transparent or non-white solid background, then use manual mask/segmentation if needed.
- Chroma key is a last resort and must not be used on white clothing, white shoes, pale socks, or pale bag areas without explicit alpha-edge QA.
- Validate alpha edges around hoodie sleeves, shoelaces, hair tips, and bag corners before using a cutout.
- Ask before switching to CLI fallback or true native transparency.

## PDF Layout Contract

- Page aspect: 16:9 landscape.
- Recommended MediaBox: 13.333 x 7.5 in.
- Preview render: 3840x2160 px.
- Safe margin: at least 160 px at 3840x2160 preview scale.
- Minimum body text size: 30 px at preview scale.
- Minimum caption/callout text size: 24 px at preview scale.
- Text, arrows, guide lines, and callout boxes must not cover the face, hair ornament, shoe details, or bag detail views unless the page is explicitly an annotated detail page.
- Use consistent title, section, callout, and caption styles across all pages.
- Dense pages such as Shoes / Socks and Bag / Accessories must keep image crops large enough for normal PDF viewing and avoid bitmap-embedded labels.

## Deliverables

Recommended structure for implementation:

```text
source/originals/
source/anchors/
source/palette/
source/manifests/
build/assets/generated/
build/assets/corrected/
build/page-previews/
build/pdf-rendered-pages/
dist/akari-v1.1-settings.pdf
dist/akari-v1.1-settings-pages/
docs/superpowers/specs/2026-06-29-akari-v1-1-palette-anchored-master-pdf-design.md
```

Original images stay unchanged. Generated and corrected files are derived artifacts. Page previews and PDF-rendered pages are kept so visual QA can happen without opening the PDF repeatedly.

## Verification Plan

Before implementing final PDF output, prepare verification that can catch the most likely failures:

- Asset audit:
  - Every original PNG copied to `source/originals/` has a SHA256 hash in `source/manifests/source-assets.json`.
  - Original PNGs remain unchanged.
  - Every PDF page has listed source inputs, generated/corrected outputs, accepted assets, and a page role.
  - No `rejected`, `needs_review`, or `needs_correction` asset is used in final production pages, except clearly marked rejected examples on Page 11.

- Color audit:
  - Palette swatches in the PDF match `source/palette/akari-v1.1-palette.json`.
  - Strict palette swatches match canonical hex values exactly, or record an implementation-specific rendering tolerance.
  - Generated/corrected asset base colors are sampled from recorded sample areas and compared against palette roles.
  - Default tolerance for flat base samples is median RGB channel delta <= 12 unless the role defines another tolerance.
  - Shaded areas are reviewed by hue drift, lightness range, and visual check instead of median RGB alone.
  - Flag any page whose white hoodie, skin, hair, or blue accent visibly drifts from the palette.
  - PDF output confirms no unintended color conversion from the sRGB/D65 target.

- Layout audit:
  - Render each page as a 3840x2160 preview image.
  - Confirm no text, labels, guide lines, callouts, or character details are clipped.
  - Confirm safe margin, minimum font size, and no-overlap rules.
  - Confirm dense boards such as shoes and bag remain readable.
  - Confirm full-body production views align to top-of-head, ground, eye, hoodie hem, skirt hem, ankle, and shoe sole guide lines.

- PDF audit:
  - Export the final PDF.
  - Render the PDF back to page images under `build/pdf-rendered-pages/`.
  - Confirm page count is 12.
  - Confirm PDF page aspect ratio is 16:9.
  - Confirm rendered pages are readable at normal viewing size.
  - Confirm PDF text is searchable and fonts are embedded or otherwise reproducibly rendered.
  - Confirm placed image effective resolution and scaling are acceptable for the final MediaBox.

- Alpha and cutout audit:
  - If transparent assets are used, inspect hoodie sleeves, shoelaces, hair tips, and bag corners at high zoom.
  - Reject visible white halos, missing white clothing edges, broken shoelaces, or damaged hair tips.

Default verification command interfaces:

```bash
identify -format '%f %wx%h\n' source/originals/*.png
python scripts/audit_assets.py
python scripts/audit_palette.py
python scripts/render_page_previews.py
python scripts/export_pdf.py
python scripts/audit_pdf.py dist/akari-v1.1-settings.pdf
python scripts/audit_alpha_edges.py
```

Implementation must provide these command interfaces unless the implementation plan explicitly replaces them with equivalent commands that cover the same checks.

## Risks And Mitigations

- Risk: regenerated images drift from Akari's face, proportion, or personality.
  - Mitigation: the expression sheet is the identity master; every generated or corrected asset must pass the identity acceptance checklist before use.

- Risk: full-body views look clean individually but fail as a production turnaround.
  - Mitigation: Page 3, Page 4, and Page 5 use shared proportion guide lines and alignment checks.

- Risk: D65 color consistency becomes false precision.
  - Mitigation: palette swatches are strict, but shaded illustration areas use role-specific sample areas, hue drift checks, lightness range checks, and visual review.

- Risk: generated text is inaccurate.
  - Mitigation: use generated images mainly for visuals; render labels and explanatory text in the PDF layout.

- Risk: white-background extraction damages white clothing, socks, shoes, or bag elements.
  - Mitigation: avoid white chroma key by default; prefer transparent or non-white generation and validate alpha edges before use.

- Risk: existing bag and footwear boards become unreadable when moved into 16:9.
  - Mitigation: use the existing boards as visual sources, then reconstruct labels, notes, dimensions, and color chips as deterministic PDF text/vector elements.

- Risk: Do / Don't rejected examples become attractive alternate references.
  - Mitigation: prefer redline annotations over new bad-example generation; any rejected examples must be clearly labeled and visually secondary.

- Risk: final PDF looks polished but is hard to revise.
  - Mitigation: keep source, generated assets, corrected assets, palette data, manifests, previews, PDF-rendered pages, and production notes separate.

## Approval State

Approved during brainstorming:

- Hybrid master document.
- D65/6500K palette board first.
- 12-page standard edition.
- 16:9 landscape fixed format.
- English main labels and text.
- Consistency-first regeneration for major pages.
- Expression sheet as identity master.
- Page architecture, color/regeneration workflow, deliverables, and verification design.

External review intake:

- No P0 blockers found in the design direction.
- Required pre-implementation clarifications were incorporated for proportion lock, color manifests, generated asset acceptance, white-background cutout risk, existing board relayout, verification thresholds, directory naming, expression labels, Do / Don't handling, and PDF layout contract.

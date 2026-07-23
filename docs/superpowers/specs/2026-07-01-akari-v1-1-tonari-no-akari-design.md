# Akari v1.1 Tonari No Akari Design

## Summary

Create a separate A4 portrait PDF art book titled `となりのあかり`.
Unlike the situation daybook, this booklet focuses on Akari's expressions,
poses, clothing variation, and near-everyday presence. It is a viewing-first
portrait collection, not a replacement for `dist/akari-v1.1-settings.pdf` or
`dist/akari-v1.1-situation-daybook.pdf`.

The booklet should contain about 24 artwork pages. Every page is a finished
portrait page: no cover, no chapter-divider pages, and no prompt-archive pages.
Each page presents one large portrait image with a Japanese title and a short
Japanese line rendered as PDF-native text below the image.

## Goals

- Build a viewing-first A4 portrait art book centered on Akari.
- Maximize useful variation across expression, pose, clothing, distance, and
  mood while keeping Akari identity stable.
- Use one generated portrait image per page.
- Keep all reader-facing text as PDF-native text, not baked into images.
- Preserve a healthy but slightly sweet tone.
- Use a lightweight review loop while generating and selecting images.
- Run heavy PDF/OCR-style auditing only at the final assembly stage.
- Keep the settings PDF and situation daybook contracts stable.
- Reuse existing manifest and PDF-rendering patterns where practical.

## Non-Goals

- Do not turn this into another settings/reference PDF.
- Do not include cover, chapter-divider, prompt-log, or contact-sheet pages in
  the first version.
- Do not place readable titles, captions, signs, logos, watermarks, or labels
  inside generated image pixels.
- Do not require a full PDF/OCR audit after every individual generated image.
- Do not lock every detail through references; the booklet needs visual freedom.
- Do not accept images with unstable Akari identity, broken anatomy, or tone
  drift just because they add variation.

## Core Decisions

- Working title: `となりのあかり`.
- Document ID: `akari-v1.1-tonari-no-akari`.
- Output PDF path: `dist/akari-v1.1-tonari-no-akari.pdf`.
- Format: A4 portrait.
- Length: target about 24 pages.
- Page role: every page is an artwork page.
- Layout: one portrait image with generous margins and a title plus short line
  beneath it.
- Language: Japanese for visible page title and short line.
- Tone: healthy, slightly sweet, close, and everyday.
- Selection model: internal range-based candidate selection.
- Reference model: minimum identity reference pack.

## Audience And Reading Experience

The desired feeling is that Akari is close enough to feel familiar, but the
booklet remains tasteful and natural. The reader should come away with a broad
sense of Akari's expressions, posture, clothing, and presence.

Variation is the highest-priority reading goal. Individual pages should still be
strong, but the final book should avoid repeating the same face angle, pose,
clothing silhouette, distance, or mood for too long.

## Text And Binary Image Rules

Generated portrait images must be illustration-only. They must not contain
intentional readable text, titles, labels, captions, watermarks, logos, shop
signs, package text, posters, or typographic decorations.

The PDF renderer owns all reader-facing text:

- Japanese page title.
- One short Japanese line per page.
- Any future source or review labels if needed.

Sidecar manifests own production metadata:

- Page IDs.
- Internal range.
- Prompt summary.
- Reference pack version.
- Candidate path.
- Accepted or rejected state.
- Selection reason.
- Rejection reason.
- Known deviations.

This keeps visible text searchable, editable, and auditable without depending on
image binaries.

## Reference Pack Strategy

The booklet should use newly generated images for the final pages. Generation
should use a small shared reference pack to preserve Akari identity without
over-constraining the artwork.

The minimum identity reference pack should anchor:

- Face shape and key facial impression.
- Hair shape, length, and color direction.
- Body proportions and height impression.
- Basic outfit direction.
- Broad color impression.

The reference pack should not rigidly lock:

- Shoes.
- Small props.
- Chapter-specific clothing.
- Exact poses.
- Exact lighting.
- Camera distance.

This keeps Akari recognizable while leaving room for page-level variation.

## Internal Range Model

The PDF should not show chapter-divider pages, but production should use
internal ranges to keep the 24-page selection balanced.

Initial internal ranges:

1. `いつもの距離`
   - Smile, talking, turning back, walking beside the viewer.
2. `少し甘め`
   - Shy expression, close distance, relaxed eye contact, gentle sweetness.
3. `元気な一瞬`
   - Small run, stretch, peace sign, lively body language.
4. `静かな余韻`
   - Side profile, window light, seated stillness, sleepy or thoughtful mood.
5. `服で魅せる`
   - Everyday clothing, roomwear, outing clothes, slightly special outfit.
6. `全身ポーズ`
   - Standing, sitting, crouching, walking, looking back.

These are production ranges, not visible chapters. A page can belong to a
primary range and optionally carry secondary tags. Page order should be adjusted
so similar images do not cluster.

## Selection Rules

Akari identity is a hard gate. A candidate cannot be accepted if the face, hair,
body impression, or overall character identity drifts too far from Akari.

After passing the identity gate, selection should balance:

- Expression and pose variation.
- Strength as a finished illustration.
- Slight sweetness and "next to you" feeling.
- Clothing and distance variation.
- A4 portrait fit.

Reject candidates that show:

- Broken hands, feet, limbs, face, or hair continuity.
- Accidental readable text or logo-like marks.
- Unwanted or tonally awkward exposure.
- Overly dramatic action that breaks the everyday tone.
- Too much similarity to already accepted pages.
- Composition that cannot fit the A4 portrait layout gracefully.

## Page Model

Each final page should contain:

- One generated portrait image.
- One Japanese title.
- One short Japanese line.

The text should stay visually quiet. It should support the portrait rather than
turn the page into a reference sheet.

Image composition can vary:

- Face and upper-body portraits.
- Half-body portraits.
- Full-body standing or walking poses.
- Sitting or crouching poses.
- Looking back or side-profile compositions.

The final collection should aim for a roughly even split between close
expression pages and full-body or pose-driven pages.

## Layout Direction

The page should feel like a simple portrait plate:

- A4 portrait page.
- Generous outer margin.
- One large image area.
- Title and short line below the image.
- No visible chapter labels.
- No dense notes.
- No decorative card-heavy layout.

The layout should support both close portraits and full-body images. Full-body
images may need more vertical breathing room, while close portraits can use a
slightly larger image crop, but the overall page system should stay consistent.

## Data And File Structure

Expected project additions:

```text
source/manifests/tonari-no-akari/
  source-assets.json
  asset-manifest.json
  page-manifest.json
  generation-requests.json

source/generated/tonari-no-akari/
source/references/tonari-no-akari/
tools/pdf/tonari-no-akari-document.mjs
scripts/audit_tonari_no_akari_pdf.py
dist/akari-v1.1-tonari-no-akari.pdf
```

The curated reference pack should live under
`source/references/tonari-no-akari/`. If a reference image is copied from an
existing immutable original, its source path and hash should be recorded in the
Tonari No Akari source manifest.

## Rendering Architecture

The existing renderer should remain the entry point. Add a document loader for
`tonari-no-akari`, following the daybook separation pattern:

- A dedicated document module reads the Tonari No Akari page manifest.
- The module validates document ID, page count, and page fields.
- The shared renderer writes previews and the final PDF.
- Settings PDF and situation daybook behavior remain unchanged.

The document model should expose:

- Document ID.
- Title.
- Pages.
- Source manifest path.
- Asset manifest path.
- Output PDF path.
- Preview directory.
- Site HTML path.

## Candidate Workflow

1. Build or select the minimum identity reference pack.
2. Define internal ranges and candidate prompts.
3. Generate candidates range by range.
4. Apply lightweight human review to each candidate.
5. Record accepted and rejected candidates in manifests.
6. Select about 24 final images with range balance.
7. Write Japanese titles and short lines.
8. Build preview pages at meaningful milestones.
9. Assemble final PDF.
10. Run full final verification.

The workflow should not require heavy PDF or OCR audit per candidate image.

## Verification Strategy

Use different checks at different stages.

Lightweight candidate-stage checks:

- Human review for Akari identity.
- Human review for anatomy and tone.
- Human review for accidental text, logos, labels, or watermarks.
- Manifest checks for required fields.
- File existence checks.
- Image dimension and orientation checks.
- Occasional preview generation when layout risk is high.

Final-stage verification:

- Node tests for the document model and renderer integration.
- Python tests for manifests and audit contracts.
- PDF build.
- PDF audit for page count, page size, non-blank rendering, embedded fonts, and
  searchable text.
- Final visual review for image-internal text and anatomy issues.

OCR or similarly expensive image-text checks should be reserved for final
assembly or explicit review checkpoints, not every single image iteration.

## Acceptance Criteria

- The booklet renders as an A4 portrait PDF separate from the settings PDF and
  situation daybook.
- The PDF contains about 24 artwork pages and no cover or chapter-divider pages.
- Each page has one large generated portrait image.
- Each page has a Japanese title and one short Japanese line as PDF-native text.
- Generated images contain no intentional readable text, logos, labels,
  captions, or watermarks.
- Final pages preserve Akari identity through the minimum reference pack.
- Final selection balances close expression pages and pose/full-body pages.
- Internal ranges are recorded in manifests but not shown as chapter pages.
- Candidate-stage workflow avoids repeated heavy PDF/OCR audits.
- Final verification includes the full document-level tests and audits.

## Risks And Mitigations

- Risk: 24 new generated images may drift in identity.
  - Mitigation: use the minimum identity reference pack and make identity a hard
    acceptance gate.
- Risk: page variety may collapse into many similar close portraits.
  - Mitigation: track internal ranges, camera distance, pose type, and clothing
    silhouette in manifests.
- Risk: accidental text appears in generated images.
  - Mitigation: prompt against text, reject obvious cases during lightweight
    review, and reserve heavier checks for final assembly.
- Risk: A4 portrait layout exposes weak full-body anatomy.
  - Mitigation: reject unstable full-body candidates and preserve enough page
    margin to avoid awkward crops.
- Risk: verification becomes too slow during image iteration.
  - Mitigation: separate cheap candidate checks from final PDF/OCR audits.

## Implementation Planning Choices

These choices should be resolved during implementation planning:

- How much shared helper code to extract after adding the first dedicated
  `audit_tonari_no_akari_pdf.py` script.
- How many candidates to generate per internal range before first selection.
- Whether preview generation should happen after every accepted batch or only
  after the full 24-page draft exists.

## Required Design Verification

After editing this design document:

```sh
npm run lint:md
```

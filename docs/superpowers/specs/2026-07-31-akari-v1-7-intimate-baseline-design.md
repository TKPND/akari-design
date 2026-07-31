# Akari v1.7 Intimate Baseline Design

Status: complete.

Date: 2026-07-31.

## Outcome

- The design was approved and candidate B / Slightly Happy was explicitly
  selected as the V17-01 working baseline.
- The final independent review returned `READY` with zero Critical and zero
  Important findings.
- The selected PNG was promoted byte-for-byte to
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`.

## Summary

Akari v1.7 restarts the character direction from the accepted v1.5 B3
body-balance image. The first checkpoint, `V17-01`, does not redesign Akari's
face, eyes, hair, body, clothing, or rendering. It tests whether a smaller,
more intimate emotional beat can restore the childhood-friend appeal that was
lost when v1.6 accumulated brighter, cleaner, and more fashionable design
signals.

The first pass directly adjusts the B3 image into three tightly bounded
micro-expression candidates. It is not a new full-body generation, a face
redesign, a wardrobe pass, or a turnaround.

## Lineage and Authority

The sole positive visual authority supplied to the first v1.7 image edit is:

- `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
  - SHA-256:
    `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`;
  - controls the rendered identity visible in the v1.5 checkpoint, the B3
    upper-to-lower body balance, adult anatomy, composition, comparison
    outfit, room lighting, and hand-painted finish for this pass.

The B3 checkpoint continues the established age-25 identity, chestnut bob,
amber eyes, pale-blue ornament, healthy thigh volume, and hand-painted
direction inherited by v1.5. This pass does not reopen those traits.

Previously selected v1.5 Kawaii 1000 favorites may be inspected as evidence
for emotional timing, especially reactions such as a restrained smile after a
small success or the moment of noticing someone familiar. They are not image
generation authorities and must not replace or blend the B3 identity.

No v1.6 image, prompt, proportion, accessory, outfit, or palette has positive
inheritance authority in v1.7. Existing v1.6 files remain preserved as
historical working material and may be used only to identify rejected drift.

## Emotional Direction

The v1.7 baseline is built around **intimate childhood-friend familiarity**.
The intended moment is: Akari notices the viewer, their eyes meet, and a small
amount of happiness reaches her expression before it becomes a posed smile.

The appeal must come from emotional timing and familiar distance, not from:

- enlarging or brightening the eyes;
- adding makeup, lashes, gloss, or stronger blush;
- making the face younger or more doll-like;
- making the pose flirtier, more glamorous, or more performative;
- changing the clothing or body silhouette.

## Locked Visual Design

All three candidates preserve the following B3 traits:

- face outline, cheek volume, compact chin, nose, and adult age impression;
- eye size, eye shape, iris scale and density, eyelash weight, and amber color;
- low-contrast brows and restrained cheek and lip color;
- short airy chestnut bob, asymmetric looseness, irregular tips, and overall
  hair volume;
- the established pale-blue crossed ornament and fine cord detail;
- B3 head-to-body ratio, moderate upper-body volume, subtle waist, healthy
  thigh volume, limb length, hands, feet, and neutral standing balance;
- white T-shirt and pale-blue shorts as comparison controls;
- warm apartment background, directional domestic light, framing, and
  hand-painted rendering language.

Small incidental redraw differences outside the face are not design changes.
A candidate is rejected if such differences noticeably alter any locked
trait.

## Candidate Matrix

Each candidate starts independently from B3. Candidates must not be generated
sequentially from one another.

### A — Eye Contact

- Preserve the B3 mouth almost exactly.
- Make the gaze feel newly connected to the viewer without changing eye
  construction or adding catchlights.
- Preserve the existing head angle unless a nearly imperceptible adjustment
  is required for natural eye contact.

### B — Slightly Happy

- This is the recommended center candidate.
- Preserve direct, familiar eye contact.
- Deepen the small closed-mouth smile only enough to read as quiet happiness.
- Keep the expression unposed and below the threshold of a broad anime smile.

### C — Cannot Quite Hide It

- Preserve the same direct eye contact and closed mouth.
- Let one mouth corner respond a fraction earlier than the other.
- The asymmetry must read as a spontaneous reaction, not smugness, teasing,
  seduction, or a deliberate wink-like performance.

The three candidates differ only in gaze connection and restrained mouth
response. They do not form different personalities or new design variants.

## Explicit v1.6 Rejection Boundary

Reject any candidate that introduces or strengthens the following:

- oversized, rounder, darker, or more reflective eyes;
- heavy upper lashes, dark eyeliner, strong lower-lid definition, or dense
  cosmetic blush;
- bright Honey Brown hair, a smooth salon-finished round bob, repeated glossy
  highlight bands, or two simple parallel pins;
- highly symmetrical front-facing presentation or generic polished character
  sheet styling;
- cropped box T-shirt, high-waisted culottes, smartwatch, ankle socks, or
  low-top sneakers;
- a clean white studio background or a cool, uniform reference-sheet finish;
- petite-number targets, body reshaping, model elongation, or childlike drift.

Also reject sharp V-line facial drift, exaggerated curves, pin-up posing,
tan-skin drift, jewelry, extra accessories, text, labels, borders, or
watermarks.

## Working Files and Promotion Boundary

Review-stage output belongs only under the ignored directory:

`build/v1.7-intimate-baseline/`

Use these working names:

- `akari-v1.7-v17-01-intimate-a1.png`;
- `akari-v1.7-v17-01-intimate-b1.png`;
- `akari-v1.7-v17-01-intimate-c1.png`;
- `akari-v1.7-v17-01-intimate-comparison-a-c.png`.

Do not modify or remove `build/v1.6-face-drafts/`, the v1.5 B3 source, or the
external v1.5 Kawaii 1000 gallery. Do not create a durable `akari-v1.7/`
package or promote a candidate before explicit user selection.

After selection, a later promotion pass may create a hash-pinned `V17-01`
accepted asset and record its v1.5 lineage. That promotion is outside this
first review pass.

## Review and Acceptance

Review B3 and A/B/C at equal display scale. Judge in this order:

1. same-person identity and adult age impression;
2. absence of v1.6 or generic polished-girl drift;
3. immediate intimate childhood-friend feeling;
4. natural emotional timing rather than a posed expression;
5. preservation of B3 hair, body, outfit, composition, and rendering;
6. clean anatomy and absence of generation artifacts.

The pass succeeds when at least one candidate is clearly more emotionally
appealing than B3 while remaining visibly the same design. If none improves
on B3, keep B3 unchanged and return to a design decision; do not select the
least-bad candidate.

## Verification Scope

This is an image-review pass. Verification is limited to:

- opening B3 before editing and assigning its exact reference role;
- confirming each output is a valid PNG and recording SHA-256;
- inspecting every candidate at original detail;
- building and inspecting one labeled, equal-scale comparison;
- checking Git status to ensure generated files remain untracked or ignored.

Do not run Python tests, Node tests, PDF builds, OCR, or release gates for this
pass. No rendering, manifest, audit, or application code is changed.

## Non-Goals

- no new hairstyle, hair color, ornament, body ratio, or age design;
- no wardrobe, accessory, footwear, pose, background, or palette redesign;
- no face-only lock followed by full-body reintegration;
- no angle study, expression sheet, turnaround, PDF, or release package;
- no reuse or promotion of a v1.6 candidate;
- no automatic correction loop after the first three candidates.

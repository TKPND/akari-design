# Akari v1.2 Face And Hair Design

## Summary

Create the first Akari v1.2 exploration as a focused face-and-hair
brush-up. This phase does not replace the Akari v1.1 settings PDF, update the
full-body design, or expand the existing portrait collections. It defines how
to compare a small set of bust-up candidates and choose the visual direction
for Akari v1.2's standard face.

The desired change is subtle but meaningful: preserve the v1.1 softness,
familiarity, and innocent character appeal while making the eyes feel more
settled, attractive, and stable as the center of the design. The result should
feel like the same Akari with a cleaner v1.2 face-and-hair read, not a new
character.

## Goals

- Explore a v1.2 standard face direction without disturbing the v1.1 body,
  outfit, palette documents, or existing PDFs.
- Keep Akari's creative-character innocence and softness. Do not push the
  design toward literal real-world age realism.
- Make the eyes the primary refinement axis.
- Keep the short bob, bangs, and pale blue hair ornament recognizably connected
  to Akari v1.1.
- Generate an initial set of eight bust-up candidates under matched conditions.
- Select by both character appeal and identity continuity.
- Record selection notes that can become v1.2 face-and-hair rules later.

## Non-Goals

- Do not update `dist/akari-v1.1-settings.pdf` in this phase.
- Do not redesign Akari's full-body proportions, hoodie, skirt, shoes, bag, or
  wider outfit system.
- Do not create a new expression collection, coordinate collection, or PDF book.
- Do not make the design more realistic just because Akari is an adult
  character.
- Do not accept a candidate that is attractive but no longer reads as Akari.
- Do not commit generated candidates or contact sheets unless the user chooses
  to preserve a final deliverable later.

## Core Decisions

- Working title: `Akari v1.2 Face And Hair`.
- Phase type: comparison and selection material, not a final PDF product.
- Primary visual target: bust-up face-and-hair candidates.
- Initial candidate count: eight.
- Main variation axis: eyes.
- Secondary review axis: organized v1.1 short bob.
- Hair ornament: keep the character-left pale blue pin identity mark.
- Selection priority: character appeal and v1.1 identity continuity together.
- First deliverable: comparison sheet, candidate notes, and draft v1.2
  face-and-hair rules.

## Scope Boundary

This phase is intentionally narrow. It should answer one question: what should
Akari v1.2's standard face and hair feel like?

In scope:

- Eye shape, softness, and horizontal balance.
- Eyelids, eyebrows, catchlights, and gaze direction.
- Mouth restraint only as needed to support the eye read.
- Face roundness only as needed to avoid unwanted drift.
- Bangs, side hair, bob volume, and hair-tip organization.
- Hair ornament position, visibility, and pale blue identity color.

Out of scope:

- Full-body silhouette.
- Hoodie volume and skirt balance.
- Shoes, socks, bag, and accessory redesign.
- Palette remastering.
- PDF layout changes.
- Productionizing all v1.2 assets.

## Face Direction

The face should be slightly more refined than v1.1, but not colder, sharper, or
more realistic. The accepted direction should keep a soft, approachable,
somewhat innocent character impression. "Adult" here means avoiding unwanted
childlike drift, not pursuing realism or fashion-illustration maturity.

The preferred eye direction is soft and gentle, with enough horizontal balance
to feel settled. The eyes may become a little less round than some v1.1 images,
but they must not become sharp, severe, sleepy-only, or emotionally distant.
The viewer should still read warmth and closeness first.

## Hair Direction

The hair should keep the v1.1 short bob identity. This phase should organize
the existing design rather than invent a new hairstyle.

Preferred hair traits:

- Short bob around the jaw and neck.
- Soft bangs with readable strand groups.
- Side volume that frames the face without becoming heavy.
- Rounded back-of-head shape.
- Natural hair-tip movement.
- Warm brown color direction consistent with v1.1.

Avoid:

- Shoulder-length drift.
- Flattened or helmet-like hair.
- Excessively airy hair that changes the silhouette.
- Hair so heavy that the face loses softness.
- Missing, flipped, or overdesigned hair ornament.

## Candidate Set

Create eight matched bust-up candidates. They should use the same general
composition, similar clothing context, and no readable text in the image. The
point of the set is to compare face-and-hair design, not background, outfit, or
pose variation.

The eight candidates should mostly vary the eyes:

1. Softer horizontal eyes with calm direct gaze.
2. Slightly rounder eyes with strong innocence.
3. Gentle eyes with lowered eyelid weight.
4. Warm eyes with brighter catchlights.
5. Mildly narrower eyes with stable expression.
6. Soft eyes with slightly shy gaze.
7. v1.1-near eyes with cleaner rendering.
8. Balanced hybrid candidate based on the strongest prior traits.

Hair differences should remain subtle. A candidate may vary bang grouping,
side-hair volume, or hair-tip organization, but should not change the base bob
design.

## Reference-Locked Pilot

The first text-only generation batch did not preserve Akari's v1.1 identity
well enough. It should be treated as rejected exploration evidence, not as a
candidate set for selection.

Before regenerating all eight candidates, run one reference-locked pilot image.
Use `source/originals/v1_1_front_3.webp` as the primary face reference and
`source/originals/v1_1_front_1.webp` plus `source/originals/v1_1_front_2.webp`
as auxiliary references. The pilot should keep the same face, hair mass, eye
color, mouth scale, and soft v1.1 character impression first, then apply only a
small eye refinement.

If the pilot still reads as a different character, stop broad generation and
tighten the reference strategy before producing another eight-image set.

The first reference-locked pilot still drifted too far toward a darker-haired,
older-looking alternate character with a flower-like hair accessory. The next
pilot must add `source/originals/v1_1_髪飾り側_45deg.webp` as a strict
hair-ornament and side-hair reference. It must explicitly reject flower
accessories, darker generic bob hair, sharper mature facial proportions, and
large glossy mouth rendering. The target is Akari v1.1's lighter copper-brown
hair, rounder cheeks, small mouth, warm amber eyes, soft innocent expression,
and pale-blue crossed hairpins or ribbon-like clips.

If the original-reference pilots remain too generic, use existing
`tonari-no-hyoujou` bust-up images as the face identity anchor. The first
Hyoujou-based pilot should use
`source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp` as the main
standard-face reference, with
`source/generated/tonari-no-hyoujou/20260703_eye-contact-pause_v1.webp` for
innocence and
`source/generated/tonari-no-hyoujou/20260706_extra-02_prank-smug_v5.webp` for
appeal. This pilot should inherit the Hyoujou face family instead of inventing
a new face from the older v1.1 reference sheets.

## Selection Gates

A candidate can only become a v1.2 direction candidate when it passes both
appeal and identity gates.

Appeal gate:

- The face has immediate character charm.
- The eyes feel soft, close, and memorable.
- The expression feels warm rather than blank.
- The hair supports the face instead of distracting from it.

Identity gate:

- The image still reads as Akari v1.1 evolving into v1.2.
- Warm brown eyes and hair direction remain intact.
- Short bob silhouette remains intact.
- Pale blue hair ornament remains on Akari's character-left side.
- Face shape, mouth scale, and overall mood do not become another character.

Reject candidates for:

- Long-hair drift.
- Missing or flipped hair ornament.
- Eye color drift.
- Eyes that are too sharp, cold, or generic.
- Extreme roundness that makes the character read too young.
- Realistic rendering that weakens the character design.
- Large mouth style changes.
- Overly flirtatious or pin-up-like expression.
- Strong outfit, background, or lighting choices that hide the face decision.

## Review Notes

Review should capture both whole-candidate judgment and reusable design
ingredients. The winning direction may combine observations from multiple
candidates, such as:

- Candidate A has the best eye softness.
- Candidate C has the best bang organization.
- Candidate E has the strongest v1.1 continuity.
- Candidate G has the best hair ornament placement.

Each reviewed candidate should receive:

- Candidate ID.
- One-line visual summary.
- Appeal notes.
- Identity notes.
- Rejection reason, if rejected.
- Reusable traits, if any.
- Overall state: `accept`, `hold`, or `reject`.

## Artifact Direction

The implementation plan should keep generated exploration materials separate
from committed design documentation unless the user explicitly chooses to
preserve them.

Suggested working paths:

```text
source/generated/v1-2-face-hair/
evidence/v1-2-face-hair/
source/manifests/v1-2-face-hair/
```

Possible artifacts:

- Eight generated candidate images.
- One contact sheet for side-by-side review.
- A lightweight candidate review manifest.
- A short Markdown selection note.
- Draft v1.2 face-and-hair rules extracted from the review.

The first formal committed artifact in this brainstorming phase is this design
document only.

## Current Selection

The current v1.2 standard-face axis is the Hyoujou-reference free generation
path, not the initial text-only batch. The selected base direction is
`source/generated/v1-2-face-hair/free-reference-batch/20260708_free-ref-05.png`.

After review, the standard-face hold candidate moved to
`source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png`.
This candidate keeps the 05-axis gentleness but shifts the age impression away
from an older-sister read toward an early-20s, university-age young adult.

This does not mean making Akari underage or childlike. The intended adjustment
is softer cheeks, lighter eye contact, and less mature composure while keeping
the familiar Akari face family, white hoodie context, short warm-brown bob, and
pale blue hair ornament.

## Verification Plan

Design-document verification:

```bash
npm run lint:md
```

Later implementation verification should include:

- Confirm the eight candidates use matched bust-up conditions.
- Confirm no generated image contains readable text, logo marks, labels,
  watermarks, or page-design elements.
- Confirm the contact sheet preserves enough resolution to compare eyes and
  hair.
- Confirm the reference-locked pilot still reads as Akari v1.1 before any
  second eight-image batch is generated.
- Confirm review notes identify appeal, identity continuity, and rejection
  reasons.
- Confirm generated working outputs are not committed unless the user chooses a
  final deliverable.

## Approval State

Approved brainstorming decisions:

- Scope: face and hair only.
- Change level: subtle refinement, not redesign.
- Primary axis: eyes.
- Eye direction: soft and gentle, chosen through visual comparison.
- Hair direction: organize the v1.1 short bob.
- Hair ornament: keep the pale blue character-left pin.
- Initial comparison shape: eight matched bust-up candidates.
- Selection priority: character appeal and v1.1 identity continuity.
- Phase deliverable: comparison and selection material, not a PDF update.
- Mid-run amendment: text-only generation was not similar enough; next
  generation must start with a one-image `v1_1_front_3.webp` reference-locked
  pilot before regenerating the full set.
- Pilot amendment: the first reference-locked pilot was still too dissimilar,
  so the next pilot must use the hair-ornament-side 45-degree reference and
  hard-ban flower accessory drift.
- Hyoujou amendment: if original-reference pilots remain too generic, use the
  accepted `tonari-no-hyoujou` bust-up expression images as the next reference
  family, starting with `called-turn_v2`.
- Selection amendment: select the 05-axis free-reference candidate as the base,
  then hold the `younger-01` adjustment as the current v1.2 standard-face
  direction. Age impression should be early-20s / university-age, less
  older-sister-like, but still not underage.

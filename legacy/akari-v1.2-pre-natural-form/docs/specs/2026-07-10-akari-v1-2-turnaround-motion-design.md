# Akari v1.2 Canonical Turnaround And Motion Design

## Summary

Create a new AI-generation-first reference pack that makes Akari v1.2 stable
across full-body viewing angles. The pack will not overwrite the Akari v1.1
settings material. It will first establish one canonical eight-view turnaround
in the standard hoodie outfit, then derive three representative motion poses
from the accepted turnaround.

The production method is sequential rather than eight independent generations.
One approved front master becomes the anchor for both left and right branches.
Each accepted neighboring angle becomes a mandatory reference for the next
angle. The two branches converge at the back view, where contradictions must be
resolved before the pack can proceed to motion poses.

## Existing Context

The repository already has strong coverage in several separate collections:

- The 14-page Akari v1.1 settings PDF accounts for 15 accepted identity,
  turnaround, palette, footwear, and accessory assets.
- The Situation Daybook contains ten environmental scenes.
- `となりのあかり` contains 24 portrait and everyday-distance illustrations.
- `となりの表情` contains 26 expression concepts, including 18 core expressions
  and eight additions.
- Local ignored coordinate work contains 52 outfit candidates.
- The `codex/tonari-no-shigusa` worktree contains gesture candidates.
- The `codex/akari-v1-2-face-hair` worktree contains the in-progress Akari v1.2
  face-and-hair selection work.

The current settings pack does not provide one corrected-proportion character
across a complete turnaround. The accepted proportion correction is a front
view, while the current back, side, and 45-degree references come from older
sources. There is one true profile, no opposite true profile, and no rear
three-quarter views. The new pack addresses this specific reproducibility gap.

## Goals

- Make full-body Akari v1.2 reproducible in AI image generation across eight
  canonical viewing angles.
- Preserve one face, body proportion, outfit construction, hair silhouette,
  hair-ornament side, sock design, and sneaker design across all views.
- Remove the need for a generator to invent the opposite profile or rear
  three-quarter construction.
- Make angle drift traceable by deriving each new angle from approved adjacent
  references.
- Produce clean individual reference images first, with contact sheets and a
  manifest supporting review and reuse.
- Derive one walking, one seated, and one turning key pose only after the
  eight-view pack passes its final gate.

## Non-Goals

- Do not modify or replace `dist/akari-v1.1-settings.pdf`.
- Do not redesign Akari's body, standard outfit, footwear, or palette in this
  phase.
- Do not independently regenerate eight attractive but inconsistent views.
- Do not introduce a 3D modeling pipeline.
- Do not create an animation sequence. Each motion deliverable is one
  representative key pose.
- Do not finish or publish every candidate. Generated candidates and review
  sheets remain working artifacts until explicitly accepted.
- Do not use mirroring, aggressive warping, or seam-producing local composites
  to hide an angle mismatch.

## Approved Decisions

- Primary consumer: AI image generation.
- First drift target: full-body proportion and angle consistency.
- Version anchor: the accepted Akari v1.2 face-and-hair direction.
- Turnaround scope: eight canonical directions.
- Motion scope: walking, seated, and turning representative key poses.
- Delivery sequence: two phases, with the turnaround completed before motion.
- Standard outfit: white oversized hoodie, gray pleated skirt, striped crew
  socks, chunky white-and-blue sneakers, and the character-left pale-blue hair
  ornament.
- Acceptance priority: cross-view identity consistency before isolated image
  appeal.
- Production approach: front master followed by sequential adjacent-angle
  derivation.

## Prerequisite

The Akari v1.2 face-and-hair selection must be explicitly accepted before this
turnaround starts. The accepted face image and its recorded rules become the
only v1.2 face-and-hair lock for this pack. Exploratory or rejected v1.2 face
candidates must not be mixed into turnaround generation.

This prerequisite is a gate, not part of the turnaround implementation. The
turnaround plan may define its manifests and verification tooling in advance,
but it must not generate the front master until the face-and-hair selection is
recorded as accepted.

## Phase 1: Canonical Eight-View Turnaround

The eight required views are:

1. Front.
2. Character-left front three-quarter.
3. Character-left true profile.
4. Character-left rear three-quarter.
5. Back.
6. Character-right rear three-quarter.
7. Character-right true profile.
8. Character-right front three-quarter.

All views use a neutral standing pose, matched camera height, matched framing,
a 1024-by-1536 portrait canvas, and the standard outfit. Left and right labels
always use the character's perspective, not the viewer's. The shoulder bag is
excluded because it would obscure the body and hoodie silhouette. It remains a
separate accessory reference from the v1.1 pack.

### Front Master

The front master combines four accepted inputs:

- The accepted Akari v1.2 face-and-hair lock.
- The accepted corrected body proportion.
- The standard hoodie outfit construction.
- The accepted footwear, sock, and hair-ornament details.

The front master is reviewed and accepted independently. No other v1.2
turnaround candidate may be generated from an unaccepted front master.

### Sequential Angle Flow

The accepted front master seeds both left and right branches:

1. Generate two or three candidates for each front three-quarter view using
   the front master and the relevant existing side reference.
2. Accept one candidate on each side before generating the true profiles.
3. Generate each true profile from the front master and its accepted front
   three-quarter neighbor.
4. Generate each rear three-quarter from its accepted profile and front
   three-quarter references.
5. Generate the back view from both accepted rear three-quarter views and the
   existing v1.1 back reference.
6. Review the complete eight-view sheet before any motion work begins.

An angle may only consume accepted upstream references. `hold` and `reject`
candidates never become generation inputs.

## Phase 2: Representative Motion Poses

Phase 2 begins only after the complete eight-view contact sheet passes review.
It produces one full-frame key pose for each motion:

- Walking: a readable mid-step pose that preserves thigh, knee, calf, sock, and
  sneaker continuity while showing natural hoodie, skirt, and hair movement.
- Seated: a natural seated pose that preserves torso-to-leg proportion and
  shows believable hoodie folds, skirt placement, hands, socks, and footwear.
- Turning: an over-shoulder or mid-turn pose that connects front, profile, rear
  three-quarter, and back construction without flipping the hair ornament.

Each key pose uses the accepted eight-view pack as its mandatory reference set.
This phase does not add animation frames, alternative outfits, props, or scene
design.

## Components And Responsibilities

### Identity Lock Manifest

Records the accepted v1.2 face-and-hair asset and the existing body, outfit,
footwear, sock, and ornament references. It answers which files are permitted
as identity sources and what each source controls.

### Turnaround Slot Manifest

Defines the eight angle slots, their order, side, Japanese and English labels,
target paths, expected hair-ornament visibility, matched camera contract, and
required upstream references. It is the stable source of truth for generation
requests and contact-sheet ordering.

### Generation Requests

Produces candidate-specific prompts from the slot manifest. A request includes
the angle target, required image references, standard outfit description,
anti-drift rules, candidate target path, and acceptance gates. It must reject a
request when its required upstream angle is not accepted.

### Review Records

Store one `accept`, `hold`, or `reject` result per candidate with explicit
identity, geometry, outfit, anatomy, and image-quality observations. Accepted
records identify the exact image that may feed the next angle.

### Contact Sheets

Provide stage-level and final visual review. Stage sheets compare two or three
candidates for one paired angle step. The final sheet presents all eight views
in canonical order with alignment guides and labels outside the image area.

### PDF Promotion

The clean images, manifests, review records, and contact sheet are the primary
deliverables. A new v1.2 settings PDF is a later promotion step after both
phases pass. It must use a new output path and must not replace the v1.1 PDF.

## Data Flow

```text
accepted v1.2 face-and-hair lock
        + corrected body and standard outfit references
        + footwear, sock, and ornament references
                              |
                              v
                    accepted front master
                    /                   \
        left front 45                    right front 45
              |                                |
        left profile                       right profile
              |                                |
        left rear 45                     right rear 45
                    \                   /
                     accepted back view
                              |
                   final eight-view gate
                              |
             walking / seated / turning key poses
```

## Acceptance Gates

### Identity Gate

- Use only the accepted v1.2 face-and-hair direction.
- Preserve warm-brown eyes, short bob silhouette, face shape, and adult age
  impression.
- Keep the pale-blue hair ornament on character-left. Its visibility may change
  through occlusion, but its physical side may not flip.

### Geometry Gate

- Normalize every standing view to the same canvas, camera height, and sole
  baseline.
- Compare crown, chin, shoulder, hoodie hem, skirt hem, knee, ankle, and sole
  landmarks on the contact sheet.
- Measure landmark offsets as a percentage of normalized crown-to-sole standing
  height. Keep corresponding major landmark ratios within 2 percent for
  left/right counterpart views and within 3 percent across the full eight-view
  set.
- Reject perspective or pose changes that make these normalized comparisons
  invalid.

### Outfit Gate

- Preserve hoodie length, shoulder drop, sleeve volume, pocket placement, and
  back hood volume.
- Preserve skirt reveal, pleat scale, and hem height.
- Preserve sock height and two pale-blue stripes.
- Preserve sneaker toe shape, sole mass, tongue visibility, laces, and blue
  accent placement.
- Keep the standard outfit free of logos or readable text.

### Quality Gate

- Preserve clean anatomy and believable hand, arm, leg, and clothing
  continuity.
- Preserve the accepted healthy leg volume and knee-to-calf transition.
- Reject text, logos, watermarks, borders, frames, and panel layouts inside
  clean reference images.
- Prefer cross-view consistency over the isolated charm of one candidate.

### Motion Gate

- The action must be readable without a caption.
- Clothing, hair, and leg deformation must remain traceable to the accepted
  turnaround.
- Hands and feet must be structurally usable as references.
- A motion pose fails if it changes body proportion or identity to make the
  action easier.

## Failure Handling

- If one angle drifts, regenerate that angle from the last accepted neighbor.
  Do not restart unrelated accepted branches.
- If the back view exposes a contradiction, trace the mismatch backward to the
  earliest inconsistent rear three-quarter or profile and return that candidate
  to `hold`.
- Reject mirrored hair ornaments and mirrored clothing asymmetries rather than
  flipping the image locally.
- Use a Correction Pass only for a localized defect on an otherwise coherent
  full image. Regenerate the full frame when anatomy, silhouette, or angle
  continuity is structurally wrong.
- Do not use warps, masks, or partial composites that create disconnected hair,
  hands, sleeves, legs, shoes, or garment seams.
- A candidate that is appealing but inconsistent remains `hold` or `reject`; it
  does not become a reference input.

## File Structure Direction

```text
source/manifests/v1-2-turnaround/
  identity-lock.json
  angle-slots.json
  generation-requests.json

source/generated/v1-2-turnaround/
source/finished/v1-2-turnaround/

evidence/v1-2-turnaround/
  contact-sheets/
  reviews/

dist/
  akari-v1.2-settings.pdf
```

Generated candidates and working contact sheets remain ignored. A finished
image or PDF becomes tracked only after explicit acceptance and a manifest
records its provenance.

## Verification Plan

Implementation must provide a failing contract test before adding the new
manifests or builders. The contract should verify:

- Exactly eight unique angle slots in canonical order.
- Valid side and expected hair-ornament visibility for every slot.
- Required upstream references for every non-front slot.
- No generation request consumes an unaccepted reference.
- Stable target paths, matched canvas contract, and standard outfit fields.
- Exactly three motion slots, each dependent on an accepted eight-view set.
- Review states restricted to `accept`, `hold`, and `reject`.

Run at least:

```bash
python -m json.tool source/manifests/v1-2-turnaround/angle-slots.json
python -m json.tool source/manifests/v1-2-turnaround/generation-requests.json
npm run test:python
```

The final visual verification is the aligned eight-view contact sheet. If a
v1.2 PDF is later implemented, add dedicated build and audit commands rather
than extending the v1.1-only audit implicitly.

## Acceptance Criteria

- The v1.2 face-and-hair prerequisite is explicitly accepted and referenced by
  exact path.
- Eight clean full-body images exist in canonical angle order.
- Every image passes identity, geometry, outfit, and quality gates.
- The two angle branches agree at the accepted back view.
- The final contact sheet passes landmark and hair-ornament review.
- Review records explain every accepted, held, and rejected candidate.
- Walking, seated, and turning key poses each pass the motion gate.
- No v1.1 artifact is overwritten.
- No generated working output is committed without explicit acceptance.

## Risks And Mitigations

- **Face direction changes after turnaround work starts:** enforce the v1.2
  face-and-hair prerequisite before front-master generation.
- **Sequential drift accumulates:** retain the front master as a mandatory
  reference at every stage, not only the immediate neighbor.
- **One branch becomes stronger than the other:** review left and right
  counterparts together before advancing.
- **The back view hides earlier contradictions:** make it a convergence gate and
  trace mismatches backward instead of averaging them away.
- **The standard hoodie hides body structure:** use the accepted corrected body
  reference as a mandatory input and verify normalized landmarks on every view.
- **Motion scope expands into animation:** limit each motion to one canonical
  key pose in this design.

## Approval State

Approved during brainstorming on 2026-07-10:

- AI-generation-first use.
- Full-body and angle drift as the first target.
- Akari v1.2 face-and-hair lock as a prerequisite.
- Eight canonical views plus three representative motion poses.
- Two-phase delivery.
- Standard hoodie outfit.
- Consistency-first acceptance.
- Sequential adjacent-angle production from an accepted front master.
- The scope, production flow, and acceptance gates in this document.

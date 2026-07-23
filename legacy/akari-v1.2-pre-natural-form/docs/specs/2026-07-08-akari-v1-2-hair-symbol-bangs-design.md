# Akari v1.2 Hair Symbol And Bangs Design

## Summary

Continue the Akari v1.2 face-and-hair exploration from the current Y1
standard-face hold candidate. The next adjustment should not reopen the whole
face design. It should keep the Y1 face, early-20s university-age impression,
white hoodie context, and gentle expression, then strengthen Akari v1.1
continuity through the hair ornament and bangs.

The adjustment target is small but important: make the current Y1 image read
less like a polished new portrait and more like Akari v1.1 evolving naturally
into v1.2. The strongest lever is the character-left pale blue hair symbol,
followed by the front bang grouping and face-framing bob softness.

## Goals

- Keep the selected Y1 face direction as the current v1.2 standard-face axis.
- Restore the complete two-part pale blue v1.1 identity ornament, including its
  crossed upper pins and compact lower loop with trailing strands.
- Make the bangs slightly less salon-polished and more consistent with Akari
  v1.1's short-bob strand groups.
- Preserve the early-20s / university-age young adult read without making Akari
  underage or older-sister-like.
- Produce a small comparison set that isolates hair-symbol and bang changes.
- Record the chosen direction as a follow-up selection note before any PDF or
  final asset update.

## Non-Goals

- Do not redesign the eyes, mouth, face shape, body, outfit, pose, or setting.
- Do not re-run a broad eight-image face exploration.
- Do not update `dist/akari-v1.1-settings.pdf` in this step.
- Do not commit generated candidate images unless the user later chooses a
  final deliverable to preserve.
- Do not accept a technically cleaner image if it weakens Akari identity.

## Starting Point

The current held standard-face candidate is:

```text
source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png
```

This candidate should be treated as the face lock. Its age impression, gentle
eye read, small mouth scale, and soft white-hoodie mood are already close
enough. The next work should protect those traits while adjusting only the hair
identity layer.

Useful reference anchors:

```text
source/originals/v1_1_front_3.webp
source/originals/v1_1_髪飾り側_45deg.webp
source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp
```

The hair-ornament-side original is the strict source for the pale blue
character-left symbol. The Hyoujou reference is secondary and should only help
preserve the accepted face family.

## 2026-07-10 Contract Correction

The v1.1 ornament is one compact, two-part identity mark on Akari's
character-left side:

- Upper: small pale-blue crossed X-shaped hairpins.
- Lower: a compact pale-blue ribbon-like loop immediately below, with two thin
  trailing strands.

Both parts are required and must read together as one ornament. The first
generation contract incorrectly allowed the crossed pins to stand alone and
broadly rejected bows/ribbons. Those X-only candidates fail identity because
they omit the canonical lower loop and strands. The compact lower ribbon-like
loop is required; only an oversized fashion bow or large dangling ribbon is
ornament drift.

Every corrected prompt must also preserve the exact same crop, pose,
background layout, and aspect ratio as the Y1 primary source. These are hard
comparison locks, not variation axes.

## Adjustment Axes

### 1. Hair Ornament Shape

The ornament must preserve both canonical parts: small pale-blue crossed
X-shaped hairpins above, plus a compact pale-blue ribbon-like loop immediately
below with two thin trailing strands. Both stay on Akari's character-left side
and read together as one compact v1.1 identity ornament.

Reject a missing upper or lower component, wrong-side placement,
flower/petal/flower-center drift, jewel/gemstone drift, an oversized fashion
bow, or a large dangling ribbon. Do not flatten the entire ornament into an
X-only pin symbol, and do not reject the required compact lower loop merely
because its geometry is ribbon-like.

This is the highest-priority correction because it gives the face an immediate
Akari continuity cue without disturbing the expression.

### 2. Bang Grouping

The current Y1 bangs are attractive but slightly too polished. The next
variants should restore more v1.1-like readable strand groups: soft uneven
front pieces, natural short-bob movement, and a lighter handmade feel around
the forehead.

The bangs should not become messy, heavy, or face-obscuring. The goal is
familiarity, not disorder.

### 3. Side-Hair Softness

The face-framing side hair can add a little of the v1.1 approachable roundness
back into Y1. Small cheek-adjacent strands and softer jawline framing are
allowed, but the bob length and silhouette must remain short.

Avoid shoulder-length drift, generic airy bob drift, or changes that make the
head shape feel older and more fashion-portrait-like.

## Candidate Set

Create four matched bust-up variants from the Y1 axis:

1. `ornament-lock`: preserve the Y1 face and focus almost entirely on the
   complete two-part pale blue v1.1 hair ornament.
2. `bang-texture`: keep both ornament parts intact and adjust the bangs toward
   v1.1-like uneven strand grouping.
3. `side-frame-softness`: keep the face and complete ornament stable while
   adding subtle cheek-side bob softness.
4. `balanced-symbol-bangs`: combine the best small changes from the first
   three directions without adding a new face design.

All four should use matched composition and lighting. The comparison should be
about hair-symbol identity and bangs, not pose, outfit, background, or face
redesign. Crop, pose, background layout, and aspect ratio must match the Y1
primary source exactly.

## Selection Gates

Accept a candidate only if:

- It still reads as the selected Y1 face direction.
- Crop, pose, background layout, and aspect ratio exactly match the Y1 primary
  source.
- The upper crossed X-shaped hairpins and lower compact ribbon-like loop with
  two thin trailing strands are all present, pale blue, and character-left.
- Bangs feel a little more Akari-like without hiding the eyes.
- The short bob remains warm brown, soft, and close to the existing silhouette.
- Age impression remains early-20s / university-age young adult.

Reject a candidate if:

- The face, eyes, mouth, or age impression noticeably changes.
- Crop, pose, background layout, or aspect ratio differs from the Y1 primary
  source.
- Either the upper crossed pins or lower loop/strands are missing.
- The ornament flips to the wrong character side.
- The ornament drifts into a flower, petal, flower center, jewel, gemstone,
  oversized fashion bow, or large dangling ribbon.
- The bangs become too heavy, too fashionable, or too messy.
- The bob becomes longer, colder, darker, or generic.
- The image looks like a new portrait family rather than a Y1 refinement.

## Expected Artifacts

Implementation should keep generated outputs ignored by git unless the user
later asks to preserve a final deliverable.

Suggested working paths:

```text
source/generated/v1-2-face-hair/hair-symbol-bangs-y1/
evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-v2.webp
```

Tracked artifacts should be limited to prompt contracts, selection notes, and
tests. The existing v1.2 manifest can be extended, or a small sibling manifest
can be added, as long as the selection record is machine-checkable.

## Verification Plan

Design-document verification:

```bash
npm run lint:md
```

Implementation verification should include:

- A contract test that records Y1 as the locked source axis.
- A contract test for the four named follow-up slots.
- A contract test requiring both ornament components and forbidding missing
  parts, wrong-side placement, flower/petal/flower-center drift,
  jewel/gemstone drift, oversized fashion bows, large dangling ribbons, and
  face redesign.
- A contract test requiring the exact Y1 crop, pose, background layout, and
  aspect-ratio lock in both live and documented prompts.
- PNG validation that fails when any corrected candidate dimensions differ
  from the Y1 source dimensions.
- Contact sheet generation for the four variants.
- Manual visual review against Y1 and the v1.1 hair-ornament reference.
- Confirmation that generated candidates and evidence remain ignored unless
  explicitly promoted.

## Approval State

Approved direction:

- Next adjustment axis: hair ornament and bangs.
- Source lock: the current Y1 standard-face hold candidate.
- Primary correction: restore the v1.1 pale blue hair identity symbol.
- Secondary correction: make bangs slightly more v1.1-like and less polished.
- Scope limit: do not reopen face, age, outfit, pose, or PDF work.

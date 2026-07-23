# Akari v1.2 C05 Morning Bed Hair Design

**Date:** 2026-07-14

**Scope:** C05 morning bed hair and sleepiness reference, from generation
contract through user selection and accepted-asset promotion

## Goal

Create and accept one C05 chest-up identity plate that establishes Akari v1.2
Natural Form's reversible just-awake hair state and incomplete wakefulness. The
image must preserve the accepted C01 identity and C03 hair-ornament construction
while making the hair changes, eyelids, brows, gaze, and neutral mouth easy to
inspect.

C05 is complete only when one independently generated A/B/C candidate has no
unresolved Blocker or Major, the user explicitly selects it, the selected PNG is
promoted byte-for-byte, and the Natural Form validator confirms its complete
lifecycle. C06 begins only after C05 is accepted.

## Global Constraints

- Generate three independent candidates, A/B/C, as standalone images.
- Give all three candidates the same prompt, references, state strength, crop,
  camera direction, outfit, backdrop, and lighting contract.
- Use a 1024 x 1536 portrait canvas with one character and one composition.
- Frame Akari from the chest upward in a front-biased light three-quarter view.
- Keep the complete head, outer hair silhouette, ornament, shoulders, hoodie
  neckline, and upper chest visible.
- Do not include hands, props, furniture, a bed, a window, or a room scene.
- Keep candidate and comparison artifacts local-only. Commit only durable
  contracts, tests, reference snapshots, review metadata, and the selected
  accepted PNG.
- C05 must use `accepted`, not `accepted-with-notes`, for release.
- Do not mechanically composite generated and original pixels to rescue a
  candidate.
- Stop the r01 round after three successfully returned images. If all fail,
  design a complete r02 round from the observed failures.

## Chosen Generation Approach

Use one new-generation request manifest:

```text
akari-v1.2/manifest/generation-requests/c05-r01.yaml
```

Use `variation_axis: independent_generation_attempt`. Candidates A, B, and C
all receive the same prompt contract and ordered reference set. The variation
axis is the independent generation attempt, not deliberate differences in hair
disorder, sleepiness, expression, camera, outfit, or lighting.

Canonical candidate paths are:

```text
akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-a.png
akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-b.png
akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-c.png
```

Use the built-in image-generation path for three separate calls. This is a new
standalone asset, not an edit of C01 or C03. Reframing a full-body accepted image
into a chest-up plate would require a broad redraw and would not provide a
cleaner identity-preservation contract than reference-guided generation.

## Reference Contract

Before every generation, open all four current reference snapshots with
`view_image` and state each role in the image-generation prompt. Use the exact
ordered set below.

1. `accepted_c01_front_identity`
   - `akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png`
   - Primary and controlling reference for the 25-year-old adult identity,
     face proportions, warm amber eyes, healthy impression, white hoodie,
     palette, and Natural Form rendering.
2. `accepted_c03_hairpin_three_quarter`
   - `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png`
   - Controlling reference for the character-left ornament, cheek silhouette,
     bob side volume, and three-quarter construction. It does not force C05 to
     copy the full-body pose or exact camera angle.
3. `supporting_sleepy_expression`
   - `akari-v1.2/references/supporting/sleepy-reply-v3.webp`
   - Non-controlling reference for the coordinated upper-eyelid weight, lower
     gaze energy, and incomplete visual focus only. Do not copy its cheek-rest
     hand, open mouth, blush, background, crop, or more rendered finish.
4. `supporting_morning_hair`
   - `akari-v1.2/references/supporting/morning-glance-h05.png`
   - Non-controlling reference for small crown flyaways, a cheek-side strand,
     and slight end irregularity only. Do not copy its doorway, room, strong
     window light, hand, pose, or alert expression.

The two supporting files are immutable package snapshots copied byte-for-byte
from:

```text
source/generated/tonari-no-hyoujou/20260705_sleepy-reply_v3.webp
source/finished/tonari-no-akari/20260701_morning-glance_v1_finish_h05_v1.png
```

Their required SHA-256 digests are:

- `sleepy-reply-v3.webp`:
  `a0b4dc00d8b32a0232c6579f3c28f792f49f5ede8f1d3527969c367cc3a9d6b2`
- `morning-glance-h05.png`:
  `282379918dd6ff553305bf07e7d7aa47693fcd7edc19908ea94e1a0c5771ba7b`

Record both snapshots in `akari-v1.2/manifest/inheritance.yaml` with
`inheritance_class: reference-only`, their source and copied paths, explicit
reuse rationales, and matching SHA-256 digests. The sleepy-expression source is
a high-priority draft that still needs strict review in its original collection;
its use here grants no identity or acceptance authority. C01 and C03 control
whenever a supporting image conflicts with them.

Keep the lifecycle declaration `depends_on: [C01]` unchanged. Accepted C03 is a
controlling generation reference for ornament construction, but it is not a new
C05 lifecycle dependency. The request contract still requires its exact accepted
path so an older or legacy hair-ornament image cannot be substituted silently.

## Image Contract

Show the same naturally cute 25-year-old Akari against a nearly plain warm
off-white or pale neutral backdrop. Use soft diffuse, near-neutral light without
a visible source, dramatic rim light, hard shadow, or room context.

The camera is near eye level and front-biased, with only a light three-quarter
turn. Both eyes, the complete face outline, and the complete character-left
ornament must remain easy to compare with C01 and C03. The output must not use a
profile, top-down angle, strong tilt, or exaggerated perspective.

The fixed visible outfit is the accepted white oversized hoodie. Keep the
hoodie neckline and shoulder volume consistent with C01. The gray skirt, socks,
and shoes are outside the chest-up crop and must not be invented into frame.

Apply only reversible morning-state hair changes:

- one or two small lifts or flyaways near the crown
- a light, asymmetric separation in the bangs
- a partial outward flick near the nape with small lower-bob end irregularity
- one soft strand falling toward a cheek

Preserve the normal short-bob length, overall outer contour, warm-brown color,
part direction, face visibility, and character-left ornament. The result must
read as hair that can return to the normal C01 state with ordinary grooming, not
as a haircut, longer hairstyle, wind effect, wet hair, or extreme bed head.

Build sleepiness from coordinated micro-signals:

- slightly heavy upper eyelids without substantially shrinking the eyes
- subtly lower or softer brows without sadness or distress
- a gaze directed generally toward the viewer but not fully focused
- a relaxed neutral mouth with closed lips and no smile
- relaxed facial tension without intoxication, illness, or sensual posing

Do not use closed eyes, a wink, a yawn, a smile gradient, strong blush, parted
lip emphasis, a cheek-rest hand, or a tilted sleep-crash pose. C05 establishes
the base just-awake state; C06 owns the later expression progression.

## Framing Guidance and Tolerance

Use advisory framing rather than strict pixel landmarks. The complete hair
silhouette and enough hoodie shoulder structure for identity comparison matter
more than exact placement.

On the 1024 x 1536 canvas, aim for:

- complete head and hair with at least about 70 px of breathing room above
- chest-up crop ending below the hoodie neckline and upper chest
- at least about 60 px of lateral breathing room outside the hair
- face centered near the vertical upper-middle rather than filling the canvas

A small numerical miss is not a defect by itself. Framing becomes Major when
the crop hides the crown, cheek-side strands, lower bob ends, ornament, chin,
shoulders, or hoodie neckline, or when extreme scale prevents comparison across
the complete state plate.

## Prompt Contract

The shared prompt must explicitly identify all four input-image roles and state
that C01 and C03 are controlling. It must ask for one standalone chest-up
illustration rather than a collage, edit sheet, character board, or scene.

The prompt must include:

- the accepted adult identity and fixed white hoodie
- the exact camera, crop, backdrop, and lighting contract
- the four reversible hair changes
- coordinated eyelid, brow, gaze, and neutral-mouth sleepiness
- the complete character-left crossed pins and ribbon-like ornament
- the prohibition on borrowing hands, props, backgrounds, poses, blush, or
  rendering drift from supporting references
- the prohibition on C06 smile progression and D01 room-scene content
- no readable text, logo, watermark, border, grid, or multiple character

The prompt must not assign different state strengths or creative directions to
A, B, and C.

## Candidate Comparison

Build one review-only artifact:

```text
akari-v1.2/comparisons/c05-r01/c05-r01-comparison.webp
```

The comparison shows A, B, and C at equal scale with no candidate favored by
layout. It supports a whole-image first impression followed by enlarged review
of the crown, bangs, cheek strand, lower bob ends, ornament, eyelids, brows,
irises, mouth, chin, and hoodie neckline. The source candidates remain
standalone PNGs.

Add a repository command named:

```text
build:v1-2:c05-comparison
```

Reuse the existing single-output A/B/C comparison builder. Do not create a new
general layout framework or modify paired C03/C07 comparison behavior merely to
support C05.

## Review and Acceptance

Review each candidate in this order:

1. Identity: adult age, face width, rounded cheeks, compact chin, eye
   construction, bob, ornament, palette, and hoodie.
2. State: reversible bed hair, coordinated eyelids and brows, incompletely
   focused gaze, neutral mouth, and no C06 expression progression.
3. Rendering: hair and ornament integrity, facial artifacts, background,
   lighting, text, logos, noise, and unwanted scene elements.
4. Production: dimensions, standalone composition, filename, SHA-256, and
   manifest linkage.

Blocker or immediate reject conditions include:

- severe identity, age, face-shape, or eye-construction drift
- missing, mirrored, relocated, duplicated, or materially redesigned ornament
- corrupted face, eyes, hair, or hoodie construction
- multiple characters, collage output, readable text, logo, or watermark

Major conditions include:

- bed hair that reads as a different, longer, windblown, or wet hairstyle
- sleepiness expressed only by closing or shrinking the eyes
- sultry, intoxicated, ill, distressed, childlike, or strongly blushing drift
- a smile, open-mouth emphasis, cheek-rest hand, prop, or room-scene leak
- material crop, palette, backdrop, lighting, or rendering drift
- framing that prevents complete face-and-hair state review

Minor findings may remain only when they do not compromise identity, the
reversible hair read, sleepy-state clarity, ornament integrity, or future use as
C06 dependency evidence. Presentation polish never compensates for an Identity
or State failure.

The user makes the final A/B/C selection. Do not promote any candidate from an
assistant-only ranking. Promote the selected source byte-for-byte to:

```text
akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
```

Record all three reviews in declared A/B/C order, exactly one as `accepted` and
the other two as `rejected`. Record source paths and lowercase SHA-256 digests.
Confirm the promoted file with `cmp` and a matching SHA-256.

## Failure and Output Recovery

Each successfully returned full image counts as one r01 attempt, even when it
fails review. A technical call that produces no image and no recoverable payload
does not consume one of the three visual candidates and may be retried once for
the same declared target path.

If a generated image appears in the interface but no local PNG exists, search
the current-date Codex rollout for an `image_generation_call` result beginning
with `iVBOR`. Parse the JSONL structurally, verify that the decoded PNG signature
is `89504e470d0a1a0a`, and save it to the declared candidate path. Do not copy a
large base64 payload through terminal output.

Reject unrelated drift rather than hiding it with masking, patching, warping,
or local pixel compositing. If all three candidates contain unresolved Blocker
or Major findings, close r01 as rejected and create a separate r02 design using
the observed failure pattern. Do not add hidden fourth or fifth r01 candidates.

## Validation Contract

Extend the Natural Form validator and focused tests to enforce:

- C05 depends on the exact accepted C01 r01 path declared in assets
- the request ID, asset ID, revision, and variation axis are canonical
- candidate paths use the assets manifest's `morning-bedhair` descriptor
- the request uses the exact ordered four-reference contract
- both supporting snapshots are recorded, byte-identical, and hash-valid
- candidates are exactly A/B/C with one canonical output each
- outputs use the C05 descriptor, r01 revision, and variant suffix
- all candidates share one prompt without per-candidate state deltas
- framing guidance, acceptance gates, and hard rejects match the request
- C05 reviews match the declared A/B/C sources in order
- every review contains one valid source SHA-256
- an accepted C05 asset has exactly one accepted review
- the accepted path matches the selected review digest
- an accepted review has no unresolved Blocker or Major
- candidate assets retain an empty `accepted_paths` list before promotion
- C06 cannot become accepted before C05 is accepted

The validator may report C05 framing measurements, but it must not reject a
candidate solely for a small advisory framing miss.

## Verification

Follow red-green-refactor for validator and comparison behavior. During
implementation, run focused Python tests before the main suites. Before calling
C05 complete, run:

```sh
npm run test:node
npm run test:python
npm run validate:v1-2
npm run lint:md
npm run audit
git diff --check
```

Also confirm:

- the accepted PNG is a real 1024 x 1536 PNG
- it is byte-identical to the selected source candidate
- exactly one C05 r01 review is accepted
- no accepted finding contains an unresolved Blocker or Major
- the two non-selected reviews are rejected
- both supporting reference snapshots match their recorded source SHA-256
- candidate and comparison outputs remain local-only
- no unintended generated artifact is staged or committed

## Out of Scope

- Reworking accepted C01, C02, C03, C04, or C07 assets
- C06-1 through C06-4 generation or acceptance
- D01 generation or acceptance
- Hair-ornament-free Daily morning variants
- Humanization or Correction Passes on a failed C05 candidate
- Candidate-to-candidate compositing or local patch repair
- A reusable arbitrary comparison-layout framework
- A Natural Form release PDF

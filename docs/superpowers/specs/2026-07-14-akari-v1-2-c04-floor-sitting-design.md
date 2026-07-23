# Akari v1.2 C04 Floor-Sitting Design

**Date:** 2026-07-14

**Scope:** C04 floor-sitting reference, from generation contract through user
selection and accepted-asset promotion

## Goal

Create and accept one C04 reference that establishes Akari v1.2 Natural Form's
canonical relaxed floor-sitting body construction. The image must preserve the
accepted C01-C03 identity, healthy body volume, outfit, and rendering while
making the pelvis, both legs, support hand, and whole-body weight balance easy
to inspect.

C04 is complete only when one independently generated A/B/C candidate has no
unresolved Blocker or Major, the user explicitly selects it, the selected PNG
is promoted byte-for-byte, and the package validator confirms its complete
lifecycle.

## Global Constraints

- Generate three independent candidates, A/B/C, as standalone images.
- Use a 1024 x 1536 portrait canvas with one character and one composition.
- Use a front-biased light three-quarter camera view.
- Keep the full head, hair, hands, socks, and toes visible.
- Keep candidate and comparison artifacts local-only. Commit only durable
  contracts, tests, review metadata, and the selected accepted PNG.
- C04 must use `accepted`, not `accepted-with-notes`, for release.
- Do not mechanically composite generated and original pixels to rescue a
  candidate.
- Stop the r01 round after three candidates. If all fail, design a complete r02
  round from the observed failures.

## Chosen Generation Approach

Use one new-generation request manifest:

```text
akari-v1.2/manifest/generation-requests/c04-r01.yaml
```

Use `variation_axis: independent_generation_attempt`. Candidates A, B, and C
all receive the same prompt contract and references. The variation axis is the
independent generation attempt, not a deliberate pose, camera, expression, or
outfit change.

Canonical candidate paths are:

```text
akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-a.png
akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-b.png
akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-c.png
```

Do not edit the legacy seated image into C04. That image depicts bench sitting,
straight lower legs, and sneakers, so using it as the primary scene source
would preserve the wrong body mechanics.

## Reference Contract

Before every generation, open the current references with `view_image` and
state each role in the image-generation prompt. Use these four references:

1. `accepted_c01_front_identity`
   - `akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png`
   - Controls adult identity, front face, healthy body volume, outfit, palette,
     and rendering.
2. `accepted_c03_hairpin_three_quarter`
   - `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png`
   - Controls the approved three-quarter face, bob, hairpin-side accessories,
     perspective, and rendering continuity.
3. `v1_1_indoor_foot_construction`
   - `akari-v1.2/references/v1.1/standard-foot-set.webp`
   - Controls white socks, two pale-blue stripes, ankle volume, and relaxed
     socked-foot construction. Any text or panel layout in the reference must
     not appear in the output.
4. `legacy_seated_anatomy_warning`
   - `akari-v1.2/references/legacy/seated.webp`
   - Provides comparison evidence for pelvis, leg volume, and garment
     compression only. It is non-controlling and must not supply the bench,
     straight-down legs, shoes, hand placement, scene, or exact pose.

The accepted references control whenever the legacy comparison conflicts with
them. C02 and the non-hairpin C03 view remain accepted dependency evidence but
need not be passed to the generation tool because C04 shows the hairpin-side
three-quarter view and excessive references add conflicting scene signals.

## Image Contract

Show the same naturally cute 25-year-old Akari on a nearly plain,
low-contrast rug. The camera is a front-biased light three-quarter view at a
natural seated viewing height, without dramatic foreshortening or a top-down
look.

The fixed outfit is:

- white oversized hoodie
- gray pleated skirt
- white socks with two pale-blue stripes
- no sneakers or other footwear

The pose is relaxed floor sitting:

- both legs flow loosely from the front toward one side
- the knees are visibly offset rather than symmetrically aligned
- the front and rear leg remain identifiable from thigh root through toe
- the pelvis is grounded and slightly posteriorly tilted
- the back rounds in coordination with the pelvis
- shoulders drop naturally
- ankles and toes remain relaxed and are not arranged into a cute symbol pose
- one hand provides the minimum believable support for the body
- the other hand rests naturally on a knee or the rug
- thigh and skirt forms respond visibly but modestly to gravity and contact

Use a small calm, secure expression. Do not introduce C05 morning bed hair or
the C06 expression gradient. Preserve compact anime proportions, warm amber
eyes, rounded cheeks, a compact chin, short fluffy light-brown bob, and the
character-left pale-blue crossed pins and ribbon-like ornament.

Do not introduce a chair, bench, bed, room scene, props, shoes, exposed
underwear, sexualized posing, excessive glamour, childlike age drift, thin-leg
drift, dramatic lighting, photorealistic skin, readable text, logo, watermark,
border, collage, grid, or multiple character.

## Framing Guidance and Tolerance

Pixel measurements guide composition but do not independently decide review.
Floor-sitting candidates naturally have different exterior bounds as the legs
relax, so C04 must not inherit C03's strict plus-or-minus 30 px alignment gate.

Prompt and measure these broad target ranges on the 1024 x 1536 canvas:

- head top: `y=70..160`
- lowest visible socked toe: `y=1360..1490`
- intended lateral breathing room: about 48 px or more on both sides

A small range miss is acceptable when the complete body remains visible and
the pelvis-to-toe structure is readable. Record measurements as comparison
evidence. Do not assign Major or reject solely from a numerical miss.

A framing issue becomes Major only when clipping, extreme subject scale, or
insufficient rug context prevents identity, anatomy, support, or contact from
being reviewed. A small margin is not a defect by itself.

## Candidate Comparison

Build one review-only artifact:

```text
akari-v1.2/comparisons/c04-r01/c04-r01-comparison.webp
```

The comparison shows A, B, and C at equal scale with no candidate favored by
layout. It supports a whole-image first impression followed by enlarged review
of pelvis, thighs, knees, shins, ankles, toes, hands, and garment compression.
The source candidates remain standalone PNGs.

Add a repository command named:

```text
build:v1-2:c04-comparison
```

Prefer extending the existing single-output comparison builder when its
current contract already fits C04. Do not create a general layout framework or
modify paired C03 behavior merely to support one three-candidate comparison.

## Review and Acceptance

Review each candidate in this order:

1. Identity: adult age, face, bob, accessories, healthy body volume.
2. Body: pelvis contact, thigh roots, knees, shins, ankles, toes, then overall
   weight balance.
3. Outfit: hoodie volume, skirt compression, sock construction, no shoes.
4. Rendering: hands and feet, artifacts, background, text, logos, noise.
5. Production: dimensions, standalone composition, filename, SHA-256, and
   manifest linkage.

Blocker or immediate reject conditions include:

- fused, missing, duplicated, disconnected, or untraceable legs or joints
- floating pelvis or support-hand placement that contradicts the center of mass
- severe identity or age drift
- explicit sexualization or exposed underwear
- multiple characters, collage output, readable text, logo, or watermark

Major conditions include:

- unclear front-versus-rear leg construction
- incompatible pelvis, back, and shoulder mechanics
- overly symmetrical symbolic sitting or artificially aligned toes
- material hand, foot, sock, skirt, or hairpin defects
- thin-leg, elongated-proportion, or outfit drift
- framing that prevents structural review

Minor findings may remain only when they do not compromise identity, anatomy,
contact, garment behavior, or future use as C07 and D01 dependency evidence.
Presentation polish never compensates for a Body failure.

The user makes the final A/B/C selection. Do not promote any candidate from an
assistant-only ranking. Promote the selected source byte-for-byte to:

```text
akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
```

Record all three reviews in declared A/B/C order, exactly one as `accepted`
and the other two as `rejected`. Record source paths and lowercase SHA-256
digests. Confirm the promoted file with `cmp` and a matching SHA-256.

## Failure and Output Recovery

If a generated image appears in the interface but no local PNG exists, search
the current-date Codex rollout for an `image_generation_call` result beginning
with `iVBOR`. Parse the JSONL structurally, verify the decoded PNG signature is
`89504e470d0a1a0a`, and save it to the declared candidate path. Do not copy a
large base64 payload through terminal output.

Reject unrelated drift rather than hiding it with masking, patching, warping,
or local pixel compositing. If all three candidates contain unresolved Blocker
or Major findings, close r01 as rejected and create a separate r02 design using
the observed failure pattern. Do not exceed three r01 generation attempts.

## Validation Contract

Extend the Natural Form validator and focused tests to enforce:

- C04 depends on accepted C01, C02, and C03 revisions declared in assets
- the request uses the exact ordered four-reference contract
- `variation_axis` is `independent_generation_attempt`
- candidates are exactly A/B/C with one canonical output each
- outputs use the C04 descriptor, r01 revision, and variant suffix
- comparison configuration and acceptance gates match the request
- C04 reviews match the declared A/B/C sources in order
- every review contains one valid source SHA-256
- an accepted C04 asset has exactly one accepted review
- the accepted path matches the selected review digest
- an accepted review has no unresolved Blocker or Major
- candidate assets retain an empty `accepted_paths` list before promotion
- legacy paths cannot be substituted for accepted Natural Form dependencies
- strict C03 landmark limits are not applied to C04

The validator may report the recorded C04 framing measurements, but it must not
reject a candidate solely for missing a broad numerical target range.

## Verification

Follow red-green-refactor for validator and comparison behavior. During
implementation, run focused Python tests before the main suites. Before calling
C04 complete, run:

```sh
npm run test:python
npm run validate:v1-2
npm run lint:md
npm run audit
git diff --check
```

Also confirm:

- the accepted PNG is a real 1024 x 1536 PNG
- it is byte-identical to the selected source candidate
- exactly one C04 r01 review is accepted
- no accepted finding contains an unresolved Blocker or Major
- the two non-selected reviews are rejected
- candidate and comparison outputs remain local-only
- no unintended generated artifact is staged or committed

## Out of Scope

- Reworking accepted C01, C02, or C03 assets
- C07 standing or seated indoor-foot references
- C05, C06, or D01 generation
- Humanization or Correction Passes on a failed C04 candidate
- A reusable arbitrary comparison-layout framework
- A Natural Form release PDF

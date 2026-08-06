# Akari v2.1 Face Polish Design

Status: approved by the user; ready for implementation planning.

Date: 2026-08-06.

## Goal

Create one bounded polish pass for the accepted Akari v2.1 front-face master.
Preserve the existing person, age, expression, eye design, face character, and
side-ponytail silhouette while restoring the softer charm of the v1 hair
ornament in a quieter v2.1 treatment.

The pass may also reduce conspicuous hair highlights and excess fine flyaways
and may soften the chin point by a minimal amount. It is successful only when
the result is recognizably the same accepted v2.1 Akari and is visibly more
finished than the current authority.

## Decision Basis

The accepted v2.1 face already passes its identity, age, eye, anatomy,
laterality, and artifact gates. Its remaining visible Minors are a bright,
strongly outlined ornament, moderately busy hair highlights and small strands,
and a slightly narrow chin.

The v1 ornament has the more appealing topology: two pale-blue crossed pins
above a compact thin-cord bow. The current v2.1 ornament inherits that idea,
but its long vertical loops, strong blue, and dark outline can read as a hard
symbol rather than a soft character detail. This checkpoint restores the v1
topology without reverting the v2.1 face, hair design, rendering style, or
character age.

## Scope

This checkpoint contains three review steps:

1. Generate three controlled front-face candidates from the accepted v2.1 face
   using the v1 image only as an ornament-topology reference.
2. Review the candidates at equal scale and original detail against the fixed
   identity, ornament, hair, chin, laterality, and artifact gates.
3. Stop for explicit user selection. Promotion, if desired, requires a later
   and separate user approval.

No candidate replaces a canonical file during this checkpoint.

## Input Authorities

Open both images at original detail immediately before every
identity-sensitive generation and state their separate roles.

| Role | Repository path | Dimensions | SHA-256 |
| --- | --- | --- | --- |
| Sole v2.1 face, identity, hair, expression, eye, palette, and rendering authority | `akari-v2.1/accepted/base/akari-v2.1-front-face-master.png` | `1023 x 1537` | `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73` |
| Hair-ornament topology reference only | `akari-v1.4/references/v1.1/v1_1_髪飾り側_45deg.png` | `1055 x 1491` | `ff7f350a7dff1957ad7caabea49cff905dde1aa2e742efd10d0799f8cc3f5e21` |

The v1 image controls only the construction and soft character of the complete
ornament. It must not influence face identity, apparent age, eye shape, hair
length, bob silhouette, pose, outfit, body, color rendering, or finish.

## Locked v2.1 Design

Keep all of the following unchanged across candidates:

- the same approachable 18-year-old young-adult identity;
- strict-front head position, direct gaze, crop, camera, background, and
  small open friendly smile;
- honey-amber almond-eye geometry, iris scale, highlight treatment, gaze,
  brows, cheeks, nose, and mouth;
- warm chestnut off-center V bangs and the character-left low side ponytail;
- hairpin and ponytail on character-left, appearing on canvas-right;
- warm skin, fine anime linework, restrained cel shading, and warm off-white
  presentation;
- T-shirt construction and all visible body or shoulder content.

Do not use eye, mouth, expression, pose, crop, lighting, or outfit changes to
make a candidate look more attractive.

## Hybrid Ornament Contract

Use one complete character-left ornament composed of:

- two slim pale gray-blue straight pins crossing cleanly;
- one compact thin-cord bow immediately below the crossed pins;
- two short narrow loops and two subtle short tails;
- a quieter outline than the current saturated blue-and-dark-edge treatment.

The ornament should occupy approximately 80 to 85 percent of the current
v2.1 ornament's overall visual footprint. This is a visual scale target, not a
pixel-exact crop ratio. It must remain readable at face-master scale without
competing with the eyes or becoming a generic ribbon, fabric bow, scissors,
double ornament, or cluster of unrelated pins.

The crossed pins, bow knot, loops, and tails must connect as one coherent
ornament. Reject long vertical loops, heavy black edging, neon or saturated
blue, oversized tails, duplicate pins, hidden pieces, mirrored placement, or
an incomplete topology.

## Allowed Polish

The following changes are allowed and no others:

- reduce the strongest crown and ponytail highlight shapes;
- remove only excess high-frequency flyaways or internal strand lines while
  preserving the main hair masses, natural asymmetry, and movement;
- soften the chin point minimally without lengthening, widening, or replacing
  the compact lower-face identity;
- integrate the new ornament naturally into the existing hair.

The hair must not become flat, helmet-like, uniformly smooth, gray, darker, or
materially shorter. The ponytail, bangs, hairline, ear, jaw-to-neck connection,
and shoulder overlap must remain coherent.

## Candidate Set

Generate all three candidates independently from the same two ordered input
images and the same shared composition and rendering prompt. Only the deltas
below may differ.

- **A, ornament-only:** replace and integrate the ornament. Preserve the current
  hair highlights, flyaways, and chin as closely as the model allows.
- **B, balanced, recommended:** apply the hybrid ornament, lightly simplify the
  strongest hair highlights and excess flyaways, and soften the chin point by
  the minimum visible amount.
- **C, stronger hair cleanup:** apply the same ornament and chin treatment as B
  while making the strongest permitted reduction in crown, ponytail, and
  small-strand visual noise. Do not flatten the hair.

Suggested working filenames:

- `akari-v2.1-face-polish-r01-a.png`;
- `akari-v2.1-face-polish-r01-b.png`;
- `akari-v2.1-face-polish-r01-c.png`.

Store candidates, prompts, generation identifiers, source paths, hashes,
review notes, and one required equal-scale labeled comparison under:

```text
tmp/akari-v2.1-face-polish/r01/
```

The directory remains ignored and untracked unless the user later authorizes
a durable deliverable.

## Review Gates

A candidate passes only when all of these are true:

1. It is immediately recognizable as the same accepted v2.1 Akari.
2. It retains the approachable 18-year-old young-adult read.
3. The eyes, gaze, brows, cheeks, nose, mouth, expression, and face spacing
   remain compatible with the current v2.1 authority.
4. The complete hybrid ornament has the approved topology, soft scale, muted
   color, quiet outline, and correct character-left/canvas-right placement.
5. The hair keeps its accepted silhouette, off-center V bangs, connected low
   ponytail, warm chestnut palette, natural movement, and readable volume.
6. Any chin change is minimal and softer without creating a different jaw,
   longer face, older read, or childlike roundness.
7. The candidate is visibly more polished than the current face in at least
   the ornament treatment and does not introduce a larger visual weakness.
8. There is no malformed anatomy, duplicated feature, disconnected strand or
   ornament piece, seam, border, text, watermark, or material generation
   artifact.

Review the face, eyes, ornament, chin, hairline, crown, ponytail connection,
ear, jaw-to-neck connection, and shoulders at original detail. Also compare all
three candidates at equal scale so crop, scale, or presentation cannot bias the
selection.

If no candidate passes all eight gates, reject all three and keep the current
canonical face unchanged. Do not select the least-bad option and do not retry,
retouch, composite, or regenerate without a new user instruction.

If more than one candidate passes, recommend the image with the strongest
balance of same-person continuity, v1-derived ornament charm, v2.1 finish,
natural hair volume, and future reuse. Recommendation is not selection.

## Selection and Promotion Boundary

After review, show the equal-scale comparison, report pass or fail and concrete
residual Minors for each candidate, and wait for an explicit user selection.
Selection makes that PNG the working face-polish choice byte-for-byte. It does
not authorize canonical promotion, replacement of the current face master,
manifest changes, staging, commit, or push.

Any later promotion must preserve the selected bytes exactly and must verify
the selected source and destination with `cmp`, PNG signature, dimensions, and
SHA-256 before updating the package documentation.

## Verification

Before generation:

- verify both input hashes and dimensions;
- confirm the candidate directory is ignored and does not already contain a
  target filename;
- open both authorities at original detail and state their distinct roles.

After generation and review:

- record the exact prompt, generation identifiers, generated source path,
  candidate path, dimensions, PNG signature, and SHA-256 for every call;
- verify any copied candidate byte-for-byte against its generated source;
- run the repository's tracked Markdown lint if review Markdown is made
  durable;
- inspect Git scope and confirm no canonical image changed.

## Non-Goals

This checkpoint does not:

- modify or regenerate the accepted v2.1 full-body baseline;
- create an angle, stability, turnaround, expression, pose, or wardrobe set;
- redesign the eyes, face, expression, ponytail, outfit, body, or age;
- promote a candidate automatically;
- create a manifest-backed package, release, PDF, or settings document;
- resume or modify the paused v2.0 uniform batch;
- modify prior v2.1 candidates, probes, comparisons, prompts, or run ledgers.

# Akari v2.1 Stability Probe r03 Design

Status: approved by the user; ready for implementation planning.

Date: 2026-08-05.

## Goal

Run one final, bounded Stage 1.5 experiment that tests whether selected Akari
v2.1 Candidate C can reproduce its approved eye language in a clean,
approximately 30-degree hairpin-side portrait when the generation reference
architecture supplies the missing view geometry explicitly.

r03 is not another prompt-only correction. It changes the generation inputs:
Candidate C becomes the sole identity and rendering authority, while a new
neutral structural guide becomes the sole geometry authority. The accepted
v2.0 images move to review-only roles for this probe.

A passing r03 is only **one successful guide-assisted realization with the
exact approved inputs**. One call does not establish statistical
reproducibility, and it does not prove that Candidate C alone is an unambiguous
rotation authority.

## Decision Basis

The exact single-call r02 output failed gates 2 and 3. Its farther eye retained
too much vertical opening and a dome-shaped upper lid, its nearer eye retained
a sharp outer-lid taper, and the eye, brow, and mouth axes remained visibly
inclined. The recorded 6,076-character r02 prompt was byte-identical to the
completed call's revised prompt, so another retry with the same three image
references and more negative wording would not test a materially new cause.

The leading, but not proven, cause hypothesis is a combination of:

- Candidate C being a polished front portrait rather than an explicit rotation
  construction sheet;
- the rounder v2.0 eye family re-entering through the two supporting generation
  references;
- model preference for retaining a readable circular iris under yaw;
- the absence of a visual horizontal and canthus-level geometry authority.

r03 changes those variables once. If the same failure mode survives this
change, the prompt-based stability track ends.

## Scope

This checkpoint contains three separately gated phases:

1. deterministically construct and review one neutral 30-degree structural
   guide without calling an image-generation model;
2. only after explicit user approval of the exact guide PNG, make one built-in
   `image_gen` call using Candidate C and that approved guide;
3. review the exact returned PNG against the six existing Stage 1.5 quality
   gates, report the result, and stop for explicit user direction.

The guide may be revised before approval because it is a deterministic local
diagram, not a generated candidate. Once approved, its bytes and SHA-256 are
pinned. Any later guide change invalidates approval and requires a new guide
review before generation.

## Non-Goals

r03 does not:

- retry with the r02 reference set;
- use r01 or r02 as positive geometry, identity, style, or composition input;
- create a 15-degree or 20-degree bridge probe;
- redesign or reselect Candidate C;
- claim Candidate C-alone rotation stability;
- authorize more than one image-generation call;
- promote Candidate C or any probe;
- continue automatically to Stage 2;
- create a turnaround, canonical angle set, package, manifest, release, or PDF;
- resume or modify the paused v2.0 uniform batch.

## Limited Contract Override

For r03 generation only, this design supersedes the Stage 1.5 sentence in the
approved bounded-redesign design that assigns the two v2.0 images supporting
generation-reference roles. It also replaces the r02 design's Generation
Approach, Input Authorities, Composition and Pose Contract, Eye Stability
Contract, and Review Gates only where this document defines the new two-input
architecture, neutral guide, axis measurement, and r03-specific gates. The v2.0
images remain accepted authorities and are used during review, but they are not
passed to `image_gen` for r03.

This override does not change the Stage 1 face selection, Candidate C's
byte-for-byte working-authority status, the Stage 2 full-body reference
contract, or any canonical v2.0 asset. It does not revise the historical r01 or
r02 `FAIL` verdicts, their negative-evidence-only status, or their run and review
records. The completed r02 implementation plan remains history and must not be
re-run. Its statements that r03 was not authorized describe the old stop point
and remain unedited; the user's 2026-08-05 instruction authorizes this new
design continuation without retroactively changing those records.

## Authority Architecture

### Generation inputs

Exactly two images may be passed to the r03 generation call.

| Input | Role | Contract |
| --- | --- | --- |
| `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png` | Sole identity and rendering authority | Preserve the same person, approachable 18-year-old read, expression, selected eye language, face character, hair silhouette and laterality, palette, linework, and restrained cel finish. The file remains byte-identical with SHA-256 `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73`. |
| `tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png` | Sole projection and placement authority | Follow only its yaw, vertical head axis, level facial axes, projected canthus positions, relative near/far scale, iris occlusion, nose projection, jaw projection, neck, and quiet shoulder placement. Do not copy or replace identity-bearing eyelid character, facial proportions, age, color, texture, hair, expression, or rendering style. Its dimensions and SHA-256 must be recorded and approved before generation. |

Immediately before generation, open both approved inputs at original detail and
state their distinct roles. No third image may be supplied.

Candidate C controls every identity-bearing shape, including the characteristic
lid curve and taper, nose character, cheek character, jaw, and chin. The guide
controls how those shapes are projected, positioned, foreshortened, aligned,
and occluded at the target view. Reject the guide before approval if it
contradicts Candidate C's identity-bearing morphology. During output review,
inability to satisfy both Candidate C's morphology and the guide's spatial
construction is a failure, not permission for either authority to override the
other.

### Review-only images

The following images may be opened during guide or output review, but none may
be passed to the r03 generation call:

| Image | Review-only role |
| --- | --- |
| `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png` | Same-person lineage, familiar warmth, and 18-year-old-read cross-check |
| `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png` | Character-left laterality and rendering-family cross-check |
| `tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png` | Negative evidence for round-eye drift, outer-lid spur, pointier chin, and roll |
| `tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png` | Negative evidence for repeated farther-eye dome, nearer-eye taper, and residual roll |
| Existing r01/r02 comparisons | Review context only; never a positive target |

## Neutral Structural Guide Contract

### Construction method

Construct the guide deterministically as a simple vector diagram and rasterize
it to an exact 1024-by-1536 portrait PNG. Derive its eye
language only from the approved Candidate C contract; do not trace or transfer
geometry from either failed probe. Do not use `image_gen` or another generative
model to make the guide.

Base the pose on a neutral parametric head-and-landmark scaffold with yaw set to
30 degrees and roll and pitch set to zero, then weak-perspective project it to
the canvas. Record those rotation parameters and the projected source
coordinates; do not infer or advertise 30 degrees solely from a hand-drawn
eye-width ratio. Candidate C supplies the approved lid language after
projection, while the neutral scaffold supplies only spatial construction.

The generation-input PNG must contain only quiet monochrome or neutral-gray
geometry on a plain light field. It must not contain labels, measurements,
color coding, hair, hairpin, ponytail, clothing detail, skin treatment, texture,
shading, catchlights, decorative lashes, or a recognizable character style.
Keep any annotated measurement overlay as a separate review file that is never
passed to generation.

### Required geometry

The guide must show:

- an approximately 30-degree view from Akari's character-left hairpin side,
  with the near side on canvas-right;
- a vertical head axis with no roll or pitch;
- level eye-center, brow, and mouth axes;
- the near and far inner and outer canthi;
- low central upper-lid segments and quiet lower lids;
- natural horizontal foreshortening of the farther eye;
- a farther iris no larger or more exposed than the nearer iris, including
  natural nasal-side and upper-lid occlusion;
- a near upper lid that terminates softly at the outer canthus without an
  independent spur, hook, lash cluster, or eyeliner point;
- a compact, softly rounded jaw and chin rather than a narrow V;
- a coherent nose, neck, and quiet level shoulder base for orientation.

### Guide review and approval

Before approval, show the clean guide PNG and a separate annotated review view.
Record its source method, dimensions, SHA-256, landmark coordinates, and the
measurements below in the r03 run ledger.

The hard guide checks are morphological and positional:

1. the facial axes are level and the head axis is vertical;
2. the farther upper lid retains the low central construction rather than a
   dome;
3. the farther iris is not more exposed than the nearer iris;
4. the nearer upper lid retains Candidate C's connected soft taper without a
   separate extension;
5. the jaw remains compact and soft;
6. the view orientation and near side are unambiguous.

Construct the guide at a documented 30-degree yaw. The accepted output band is
approximately 25 to 35 degrees. Judge the band from the whole construction: the
projected face centerline and nose, near and far cheek widths, ear visibility,
canthus placement, eye foreshortening, and a normalized overlay against the
approved guide must agree. A near-front view below the band, a 45-degree or
deeper view above it, a profile, or a face/neck/shoulder perspective mismatch
fails Gate 3. Neither an eye-width ratio nor a single landmark establishes yaw
by itself. If the guide-relative band remains reasonably disputed, it fails.

The guide targets zero-degree roll and pitch. Its level facial axes target
canvas horizontal and its construction head axis targets canvas vertical. For
the generated output, the unified hard roll tolerance is an absolute signed
angle difference of at most 3 degrees from each corresponding projected guide
axis, not an assumption that every perspective landmark must be exactly zero
degrees on canvas. Candidate C's observed approximately 7-to-8-degree eye and
mouth incline is normalized rather than inherited because r03 is explicitly a
clean level-yaw test. There is no separate 3-to-5-degree gray zone.

Record `W_far / W_near` and `H_far / H_near` as diagnostic sanity checks. The
expected neighborhoods are approximately 0.75 to 0.88 and 0.85 to 1.00,
respectively, but neither range is an automatic PASS or FAIL criterion. A guide
passes only through the hard morphology and axis checks above plus explicit
user approval of the exact PNG.

### Landmark and measurement method

Use the center of each drawn stroke when placing a landmark. Define eye width
`W` as the Euclidean distance between the inner and outer canthi. Define eye
height `H` as the maximum aperture measured perpendicular to that canthus
chord. Define each eye center as the chord midpoint; the eye-center axis joins
those two midpoints. Define each brow center as the midpoint along its visible
arc, the mouth axis as the line between mouth corners, and the shoulder axis as
the line between the two visible acromion landmarks. In the guide, define the
head axis as the explicit vertical construction axis through the cranial volume.
Do not derive a separate output head-axis number from the same three facial
axes, and do not use the nose-to-chin facial midline as a roll measure, because
yaw naturally shifts that projected line. Record each output-to-guide facial
axis delta independently; all three must pass the same 3-degree tolerance.

The shoulder angle is a diagnostic corroboration rather than a numeric hard
gate because perspective can project equal-height shoulder landmarks at
slightly different canvas heights. It still fails qualitatively if the output
adds an obvious compensating body lean or cute shoulder tilt.

For the guide-relative output overlay, uniformly scale by the chin-to-crown head
height and translate the midpoint between the two eye centers to the guide
midpoint. Do not rotate, skew, or warp either image. Compare the face centerline,
nose tip, four canthi, near and far cheek contours, chin, and visible ear against
the approved guide. The overlay supports the 25-to-35-degree human band
judgment; it does not turn any single pixel-distance ratio into an angle meter.

Pitch is a qualitative guide-relative check rather than a second inferred angle
from the roll landmarks. Compare crown-plane, brow, nose, ear, mouth, chin, and
visible nostril or under-chin relationships in the unrotated overlay. An obvious
upward or downward camera view, increased crown or under-chin plane, or a
reasonably disputed pitch match fails Gate 3.

For upper-lid shape, record the maximum rise above the canthus chord within the
central 50 percent of each eye. For each iris, fit its apparent ellipse from the
visible contour, record the fitted vertical diameter `D`, the visible vertical
span `V`, and normalized exposure `E = V / D`. Record apparent iris scale and
exposure separately; the farther iris must be no larger and no more exposed
than the nearer iris, subject to the visual-dispute rule.

Define the anatomical outer canthus independently as the junction of the fitted
upper- and lower-lid centerlines before any decorative continuation. Record the
near upper-lid continuation length `L` from that junction along the lid tangent
and normalize it as `L / W_near`. Before guide approval, measure the same ratio
on Candidate C's hairpin-side eye. The r03 guide and output may not exceed that
Candidate C baseline by more than the measurement uncertainty, defined as the
greater of two canvas pixels normalized by `W_near` or the spread between the
two independent landmark placements. This numeric check accompanies the
controlling morphology rule: a short connected soft taper is allowed, but an
independently readable spur, hook, lash cluster, or eyeliner point fails.

Record coordinates in canvas pixels and derived angles to one decimal degree.
Repeat the measurements once after hiding the first annotations. If stroke
thickness, hair occlusion, crop, or landmark disagreement can move a hard axis
from one side of the 3-degree boundary to the other, the evidence is disputed
and the gate fails rather than being rounded into a pass.

## Generation Contract

### Composition and identity

- Produce one tight head-and-shoulders portrait near 1024-by-1536 portrait
  scale, with the chin-to-crown head mass occupying approximately 55 to 65
  percent of output height.
- Follow the guide's approximately 30-degree hairpin-side yaw and keep the near
  character-left side on canvas-right.
- Keep the head upright and the eye, brow, mouth, and shoulder axes level.
- Preserve Candidate C's same small open friendly smile and familiar
  camera-directed gaze, while allowing natural partial iris occlusion.
- Preserve Candidate C's warm off-white background, warm chestnut hair,
  off-center V bangs, pale muted-blue crossed hairpin, one connected low side
  ponytail, white crew-neck top, palette, linework, and restrained finish.
- Keep the complete hair silhouette and compact softly rounded lower face
  within comfortable margins.

### Eye construction

- Use Candidate C for the selected low, horizontally emphasized eye language
  and use the guide for its 30-degree placement and occlusion.
- Let the farther eye become naturally narrower without lifting its central
  upper lid into a dome.
- Let the farther iris appear smaller and more hidden; a fully readable circular
  iris or complete catchlight is not required.
- Do not increase farther-eye iris exposure or open either eye to preserve iris
  readability.
- End the nearer upper lid at the outer canthus in one soft taper without a
  separate hook, spur, lash extension, or eyeliner point.
- Keep compatible camera-directed gaze, honey-amber irises, restrained pupils,
  one small principal highlight where naturally visible, and quiet lower lids.

### Prompt discipline

The prompt must state the two reference roles first, describe observable
positive geometry before prohibitions, and use one short negative block limited
to test-breaking failures. It must not restate the same lock in multiple forms,
include pixel ratios as generation commands, or claim that text can assign
numeric image-reference weights.

The complete prompt must contain at most 3,500 Unicode characters, including
line breaks, as measured from the exact prompt file. At minimum, the short
negative block excludes head or camera roll, a dome-shaped farther upper lid,
increased farther-eye iris exposure, a nearer-eye outer spur, a narrow V-shaped
chin, mirrored laterality, malformed or duplicated anatomy, text, and
watermarks.

## Execution and Provenance

Store all local r03 material under:

```text
tmp/akari-v2.1-redesign/stability-r03/
```

Use these working paths:

```text
guides/akari-v2.1-stability-30-r03-structure.svg
guides/akari-v2.1-stability-30-r03-structure.png
guides/akari-v2.1-stability-30-r03-structure-review.png
prompts/akari-v2.1-stability-30-r03.md
images/akari-v2.1-stability-30-r03.png
RUN.md
REVIEW.md
```

After the exact guide PNG is approved and pinned, use one built-in `image_gen`
call and preserve the first returned image exactly. Do not retry, retouch, crop,
resize, recompress, composite, or silently replace it. A technical recovery of
the completed call's exact current-day rollout payload is allowed when needed;
recovery is not regeneration.

The ledger must record the two generation inputs and their roles, dimensions,
and hashes; the final prompt and hash; guide construction and approval evidence;
call and request identifiers; completed-event evidence; source and saved image
paths; PNG metadata and signature; byte comparison; and the final six-gate
review.

## Six Review Gates

Review the exact r03 output at original detail against Candidate C and the
approved guide. Use the accepted v2.0 images only for their review roles and
r01/r02 only as negative evidence. Record one `Pass` or `Fail` with concrete
evidence for each gate:

1. **Same-person identity:** the face, expression, selected v2.1 rendering, and
   familiar warmth remain Candidate C's Akari rather than the neutral guide or a
   generic character.
2. **Selected eye morphology:** the farther eye retains a low central upper lid
   without extra iris exposure, the nearer lid retains Candidate C's connected
   soft taper without a separate spur, both irises and highlights remain
   restrained, and gaze remains compatible.
3. **View and axes:** the result is a coherent approximately 30-degree
   character-left hairpin-side view; the eye, brow, and mouth axes each remain
   within the unified 3-degree difference from the approved guide, while the
   shoulders remain a quiet perspective-aware corroboration without obvious
   body lean; the qualitative guide-relative pitch check also passes.
4. **Hair and laterality:** the hairline, off-center V bangs, complete crossed
   hairpin, ear, and one attached low ponytail remain coherent on
   character-left, near on canvas-right, without mirroring or duplication.
5. **Age and lower face:** the result preserves the approachable 18-year-old
   young-adult read, compact soft cheeks and chin, and non-glamorous
   presentation without narrowing into a V-shaped lower face.
6. **Anatomy and artifacts:** no malformed geometry, disconnection,
   duplication, seam, border, accidental crop, text, logo, watermark, or
   material-rendering artifact is present.

Record the same eye-width and eye-height ratios used for guide diagnostics, but
do not use `H/W`, `W_far / W_near`, or `H_far / H_near` alone to pass or fail the
output. Upper-lid curvature, iris occlusion, canthus termination, axis level,
and direct visual comparison to Candidate C remain controlling.

The final verdict is `PASS` only if all six gates pass. Any reasonable dispute
about selected eye morphology or any axis outside the unified tolerance is a
`FAIL`; do not choose a least-bad interpretation.

## Result Meaning and Stop Boundary

Whether r03 passes or fails, show the exact probe, report all six findings, and
stop for explicit user direction. The guide and probe remain ignored, local,
noncanonical evidence and never become v2.1 authorities or promotion
candidates in this checkpoint.

If r03 passes, it records one successful guide-assisted realization with these
exact inputs only. Stage 2 and promotion remain blocked pending a separate user
decision.

Any r03 failure stops the run without a correction call. If Gate 2 repeats the
farther-eye dome or exposure or nearer-eye spur, or Gate 3 repeats excess roll
despite the approved guide, end the prompt-based 30-degree probe track and ask
the user to choose between:

- redesigning the front master with explicit level and rotation-ready eye
  structure; or
- retaining Candidate C as a front-only design constraint.

A failure confined to identity, age, lower face, laterality, crop, anatomy, or
a material artifact still stops r03, but it does not by itself prove the eye or
axis hypothesis failed. Report it for separate diagnosis and wait for explicit
user direction without assuming the front-redesign/front-only decision.

No result authorizes an automatic r04.

## Verification

Before guide work, verify Candidate C's hash and confirm the paused v2.0 uniform
batch digest is unchanged. Before generation, verify the exact approved guide
hash, dimensions, axis and landmark record, Candidate C hash, prompt length and
hash, two-input-only reference set, and explicit guide approval.

After generation and review, run focused Markdown lint for the local ledger,
review, and prompt; tracked Markdown lint; PNG signature and metadata checks;
source-to-saved `cmp`; Git ignore checks; the paused-batch digest check;
`git diff --check`; and clean tracked and staged-tree checks.

# Akari v2.1 Stability Probe r02 Design

Status: approved by the user; ready for implementation planning.

Date: 2026-08-04.

## Goal

Generate one corrected, noncanonical 30-degree hairpin-side stability probe from
the user-selected Akari v2.1 Candidate C. The r02 probe must provide clean
evidence that Candidate C's low, horizontally emphasized eye construction
survives a modest yaw without the rounder eye regression or head roll observed
in the rejected r01 probe.

This is a bounded Stage 1.5 retry. It does not reopen Candidate C selection or
authorize Stage 2, promotion, packaging, manifest work, or PDF work.

## Prior Failure and Correction Boundary

The rejected r01 probe preserved Akari's general identity, age, hair, laterality,
and artifact-free rendering, but it failed the selected-eye stability gate after
independent audit. The farther eye became rounder and relatively more open, the
near eye acquired a sharper outer upper-lid spur, and added eye-line and head
roll confounded the intended pure 30-degree comparison. Its chin was also
slightly narrower and pointier than Candidate C.

r02 corrects only these evidence defects:

- restore Candidate C's low, slightly straighter central upper-lid language;
- keep restrained vertical eye opening under perspective;
- prevent a round or dome-shaped farther-eye opening;
- prevent a sharp outer upper-lid spur on the nearer eye;
- remove added head, eye-line, and shoulder roll;
- keep Candidate C's compact, softly finished lower face and chin.

All other approved v2.1 design locks remain unchanged.

## Generation Approach

Generate r02 cleanly from Candidate C and the two accepted v2.0 supporting
authorities. Do not edit the rejected r01 probe and do not include it as an
image-generation input. This avoids anchoring the retry to the exact morphology
and roll that caused the failure.

Use one built-in `image_gen` call and preserve the first returned image exactly.
Do not retry, retouch, crop, resize, recompress, composite, or silently replace
the result. A technical failure may use structural current-day rollout payload
recovery for the completed call, but recovery is not regeneration.

Store all prompts, ledgers, provenance, the generated image, and review notes
under the ignored working directory:

```text
tmp/akari-v2.1-redesign/stability-r02/
```

## Input Authorities

Open all three images at original detail immediately before generation and
state their independent roles.

| Role | Repository path | SHA-256 |
| --- | --- | --- |
| Primary current identity authority: selected v2.1 face, eye design, expression, face geometry, hair, palette, and finish | `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png` | `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73` |
| Supporting v2.0 face authority: same-person lineage, familiar warmth, hairline logic, and 18-year-old read only | `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png` | `34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe` |
| Supporting v2.0 body authority: laterality, shoulder-crop clothing, compact proportion cues, and rendering family only | `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png` | `03e7effc6dd13dadb4f1ec394b84ffe8ed9d218e500f0aefa49ebf2b5f0b6d94` |

The rejected r01 probe is review evidence only. It must not become a positive
identity, composition, angle, or rendering reference for r02.

## Composition and Pose Contract

- Produce one shoulder-up portrait near 1024-by-1536 portrait scale.
- Move the virtual camera horizontally about 30 degrees toward Akari's own left,
  the hairpin side.
- Keep the head, eye line, and shoulders level with no added roll or pitch.
- Keep the face, neck, and shoulders in one coherent camera view; do not create
  an independently turned or tilted head.
- Keep the same small open friendly smile, direct familiar gaze, warm off-white
  background, complete hair silhouette, and comfortable margins as Candidate C.
- Preserve the crossed hairpin and attached low side ponytail on character-left,
  nearer and clearly visible on the hairpin-side view.

## Eye Stability Contract

Candidate C's eye geometry is the controlling visual authority. Perspective may
foreshorten the farther eye horizontally, but it must not replace the selected
construction with a rounder v2.0 or generic anime-eye solution.

- Keep medium-width almond eyes with low, restrained vertical opening.
- Keep the central portion of each upper lid low and nearly straight before it
  softens toward the outer end; do not turn it into a high semicircular arch.
- Foreshorten the farther eye horizontally without compensating through extra
  vertical opening, a dome-shaped upper lid, or enlarged visible iris area.
- Keep the nearer upper lid smooth and softly tapered, without a sharp outer
  spur, hook, lash cluster, or eyeliner-like point.
- Preserve medium honey-amber irises, a deeper brown rim, subtle pupils, one
  small principal highlight, quiet lower lids, and compatible binocular gaze.
- Avoid oversized round irises, wet gloss, overloaded sparkle, heavy lower
  lashes, drooping outer corners, and unequal focus.

## Identity and Rendering Locks

- Preserve the same approachable 18-year-old young-adult read, neither
  childlike nor mid-20s.
- Preserve Candidate C's brow placement, eye spacing, soft cheeks, compact chin,
  small natural nose, smile, jaw-to-neck connection, and familiar warmth.
- Do not narrow, lengthen, or sharpen the lower face. Keep the chin compact and
  softly rounded in correct perspective.
- Preserve warm chestnut hair, off-center V bangs, restrained crown volume,
  pale muted-blue crossed hairpin, and one connected low side ponytail.
- Preserve soft anime linework, warm skin, restrained cel shading, low-gloss
  hair, restrained internal strand detail, and bright but non-neon color.
- Avoid glamour, makeup, idol polish, fashion styling, photorealism, malformed
  anatomy, duplicated features, seams, borders, text, logos, and watermarks.

## Review Gates

Review the exact r02 output at original detail against Candidate C and the two
supporting authorities. Use the rejected r01 only as negative comparison
evidence. Record one `Pass` or `Fail` with concrete evidence for each gate:

1. same-person face read against selected Candidate C;
2. stable Candidate C eye construction, iris scale, highlight restraint, and
   compatible gaze under perspective;
3. level head, eye line, and shoulders in a coherent approximately 30-degree
   hairpin-side camera view;
4. coherent hairline, V bangs, crossed hairpin, attached ponytail, and correct
   character-left laterality;
5. preserved approachable 18-year-old young-adult read and compact lower face;
6. no malformed geometry, disconnection, duplication, seam, border, text,
   watermark, or material-rendering artifact.

Gate 2 is relative to Candidate C, not an absolute judgment that the eyes are
merely attractive or non-glossy. It passes only when both eyes retain the
selected low central upper-lid language and restrained opening after reasonable
perspective foreshortening. If that evidence remains visually disputed or is
confounded by head roll, r02 fails.

The final verdict is `PASS` only if all six gates pass. Do not select a least-bad
result.

## Stop Boundary

Whether r02 passes or fails, show the exact probe, report all six gate findings,
and stop for explicit user direction. The probe remains ignored, local,
noncanonical evidence and never becomes a v2.1 authority or promotion candidate
in this checkpoint.

Do not automatically generate another retry, continue to Stage 2, promote
Candidate C, or create package, manifest, release, or PDF artifacts.

## Verification

Before generation, verify the three authority hashes and confirm that the paused
v2.0 uniform batch digest is unchanged. After recording r02, run focused
Markdown lint for the local ledgers and prompt, tracked Markdown lint, PNG
signature and metadata checks, source-to-saved `cmp`, Git ignore checks, batch
digest verification, `git diff --check`, and clean tracked/staged-tree checks.

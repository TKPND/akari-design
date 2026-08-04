# Akari v2.1 Bounded Redesign Design

Status: approved by the user; Stage 1 execution awaits implementation-plan choice.

Date: 2026-08-04.

## Goal

Create a bounded Akari v2.1 redesign derived from the accepted v2.0 character.
Preserve the same-person lineage and the distinctive v2.0 identifiers while
making the face more polished, the eye construction less fragile across
generation scales and angles, and the overall result less like a generic
AI-anime character.

The redesign keeps Akari clearly readable as an approachable 18-year-old young
adult. It moves the main source of identity away from busy eye rendering and
toward the hair silhouette, off-center V bangs, low side ponytail, pale muted
blue crossed hairpin, soft youthful face, warm chestnut and honey-amber palette,
and natural signature-casual silhouette.

## Current Work Boundary

The existing v2.0 school-uniform batch is paused while v2.1 is designed. Preserve
all existing local outputs without deletion or modification:

- 30 pilot images;
- 50 completed expansion images out of the planned 270;
- prompt, selection, index, comparison, and provenance records under
  `tmp/akari-v2-uniform-batch/`.

The paused v2.0 candidates remain v2.0 exploration material. They do not become
v2.1 references or canonical assets.

## Scope

The first v2.1 checkpoint contains three review stages:

1. Generate and compare three tightly controlled front-face candidates.
2. After explicit user selection, generate one untracked 30-degree identity
   stability probe.
3. After the probe passes, generate and review one strict-front full-body
   baseline.

The only canonical outputs eligible for promotion are one selected face master
and one accepted front full-body baseline. The 30-degree probe is evidence only.

## Non-Goals

This checkpoint does not create:

- a turnaround or canonical angle set;
- expression or wardrobe sheets;
- a uniform batch;
- a manifest-backed release package;
- a PDF or settings release;
- fashion, idol, glamorous, model, or costume-led redesigns;
- a younger childlike or older mid-20s interpretation;
- automatic correction rounds after a failed review.

## Input Authorities

Open both images at original detail before every identity-sensitive generation.
Use their roles independently.

| Role | Repository path | SHA-256 |
| --- | --- | --- |
| Sole v2.0 face and close-view identity authority | `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png` | `34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe` |
| v2.0 body, outfit, laterality, and full-figure authority | `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png` | `03e7effc6dd13dadb4f1ec394b84ffe8ed9d218e500f0aefa49ebf2b5f0b6d94` |

The phrase "V1 naturalness" is a qualitative design goal only. No v1 image is a
positive identity authority for v2.1, and no generic v1-era facial solution may
override the two v2.0 authorities.

## Inheritance and Intentional Change

| Area | Treatment |
| --- | --- |
| Same-person lineage, 18-year-old read, approachable warmth | Lock |
| Warm chestnut hair, off-center V bangs, low side ponytail, crossed hairpin | Lock |
| Ponytail and hairpin on character-left; canvas-right in a front view | Lock |
| Compact healthy body and restrained, non-model proportions | Inherit from v2.0 full-body |
| Eye geometry, iris scale, highlight count, and lid rendering | Intentional redesign |
| Excess lower-face puffiness and chin finish | Minimal intentional refinement |
| Bang grouping, internal hair noise, crown volume, and shine | Minimal intentional refinement |
| Hair, amber-eye, and blue-accent saturation | Muted refinement without grayness |
| Base bottom and utility construction | Intentional v2.1 redesign |

Changing the eyes does not authorize a new person. Brow placement, eye spacing,
cheek character, compact chin, expression warmth, hairline, silhouette, hair
laterality, and overall age read remain continuity gates.

## Character and Rendering Lock

Akari must read as a late-teen young adult: clearly not a child and not a
mid-20s adult. She is naturally cute, familiar, fresh, and approachable rather
than glamorous, doll-like, cold, sleepy, highly fashionable, or generically
moe.

Keep a soft rounded face, soft cheeks, and compact chin. Remove only the excess
roundness that creates an unrefined impression. Do not lengthen or sharpen the
lower face.

Keep the nose small and delicate while giving it a faint readable structure
rather than reducing it to an arbitrary symbol. Keep the mouth friendly and
natural, with stable corners and no detailed lips or synthetic idol smile.

Keep the v2.0 soft anime linework, warm skin treatment, restrained cel shading,
and warm off-white presentation. Avoid glossy skin, plastic hair, heavy gradient
rendering, hyper-detailed pupils, and high-frequency strand noise.

## Hair and Color Lock

Keep the off-center V-bang structure with two or three primary bang groups and
only enough smaller strands to preserve natural asymmetry. Slightly reduce crown
puffiness and internal strand noise. Preserve the readable low side-ponytail
silhouette with light movement at the tips and no disconnected or duplicate
hair mass.

Use warm chestnut or cocoa-brown hair, honey-amber eyes with a deeper brown rim,
pale muted blue for the crossed hairpin and related accents, and white and navy
for the base clothing. Keep the palette bright and fresh while reducing the
toy-like saturation of v2.0. Avoid neon blue, orange-red hair, loud yellow eyes,
or multiple competing cute accent colors.

## Eye Redesign Lock

Use medium-width almond eyes with horizontal emphasis and restrained vertical
opening. The upper lid is slightly straighter through the center and softens
toward the outer end. Inner corners remain soft and outer corners do not become
strongly drooping.

Use medium honey-amber irises with a slightly deeper brown rim, a readable but
subtle pupil, one small main highlight, and at most one faint secondary
highlight. Keep the lower lid understated. Do not use wet gloss, overloaded
sparkle, oversized round irises, heavy eyeliner, lower lash emphasis, or lash
clusters.

## Stage 1: Controlled Face Exploration

### Shared generation contract

Generate all three candidates independently from the same v2.0 face master.
Keep these conditions fixed:

- strict-front face;
- level head;
- direct gaze;
- the same small open friendly smile;
- shoulder-up portrait crop;
- the same warm off-white background;
- the same reference set and reference roles;
- the same output orientation and approximately 1024-by-1536 portrait scale;
- the same line, skin, shading, and finish direction.

Only the eye implementation, very small lower-face refinement, bang grouping,
hair shine, and accent saturation may vary. Do not alter pose, expression,
camera, crop, outfit, or lighting to make one option look more attractive.

### Candidate deltas

- **A, conservative:** maximum v2.0 continuity; slightly smaller irises, one
  principal highlight, and simplified lid rendering with minimal face cleanup.
- **B, balanced:** the recommended center; horizontally emphasized almond eyes,
  a slightly straighter central upper lid, medium irises, one principal
  highlight, and minimal cheek and chin cleanup.
- **C, refined:** the strongest allowed refinement; slightly more restrained
  vertical eye opening and clearer bang and lower-face grouping while retaining
  the same age and person.

Suggested working filenames:

- `akari-v2.1-face-r01-a.png`;
- `akari-v2.1-face-r01-b.png`;
- `akari-v2.1-face-r01-c.png`.

Store candidates, prompts, generation identifiers, review notes, and a required
equal-scale labeled comparison under:

```text
tmp/akari-v2.1-redesign/r01/
```

### Face hard gates

A candidate passes only when all of these are true:

1. It is recognizably the same Akari lineage as the accepted v2.0 face.
2. It reads as an 18-year-old young adult, neither childlike nor mid-20s.
3. The eyes follow the approved shape, iris, highlight, and lid design.
4. Both eyes align coherently and share compatible gaze, iris scale, and focus.
5. Brows, hairline, ears, jaw-to-neck connection, bangs, hairpin, and ponytail
   connect coherently.
6. Hairpin and ponytail remain on character-left, appearing on canvas-right in
   the front view.
7. The result is less glossy and less stock-AI-looking without becoming generic
   v1-style prettiness.
8. There is no malformed anatomy, duplicated feature, seam, border, text,
   watermark, or material generation artifact.

If no candidate passes, reject all three and stop. Do not select the least bad
option. A bounded `r02` is allowed only after explicit user instruction.

After review, show the equal-scale comparison, report pass/fail and concrete
residual Minors for each candidate, and wait for an explicit user selection.
Selection does not authorize automatic generation of the next stage.

If multiple candidates pass, prefer the one with the strongest balance of
same-person continuity, 18-year-old freshness, reduced stock-AI eye treatment,
natural appeal, finish quality, and future reusability. Do not choose a candidate
only because it is the safest-looking or the most dramatic.

The selected candidate becomes the working v2.1 face authority byte-for-byte.
Do not regenerate or silently retouch it before later promotion.

## Stage 1.5: Noncanonical 30-Degree Stability Probe

After explicit authorization following face selection, generate one
approximately 30-degree hairpin-side portrait with character-left identifiers
visible. Use the selected face as primary identity authority and the v2.0
references only in their original supporting roles.

The probe tests:

- same-person face read away from front;
- stable eye shape, iris scale, and highlight restraint;
- hairline, V-bang, hairpin, and ponytail continuity;
- correct character-left laterality;
- preserved 18-year-old read;
- absence of geometry or rendering artifacts.

The probe remains under the ignored working directory and never becomes a
canonical v2.1 asset in this checkpoint. If it fails, stop before full-body
generation. Whether it passes or fails, show the finding and stop for explicit
user direction. Do not regenerate automatically, proceed automatically, or
promote the selected face.

## Stage 2: Strict-Front Full-Body Baseline

Use the selected v2.1 face as the primary face authority. Use the v2.0
full-body image for body balance, laterality, and full-figure presentation.

### Composition and anatomy

- strict front view at approximately zero degrees;
- level head, shoulders, and pelvis;
- direct gaze and the same approachable expression family;
- relaxed neutral standing pose with separated arms and legs;
- complete figure from hair to shoe soles with comfortable top and bottom
  margins;
- coherent shoulders, elbows, wrists, hands, fingers, pelvis, knees, ankles,
  feet, and shoe construction;
- both feet grounded with a restrained contact shadow;
- plain warm off-white background without props or clutter.

### Body and outfit

- compact healthy body with moderate shoulders and torso;
- restrained bust, slight waist definition, and healthy thighs and calves;
- clean white compact-fit cotton T-shirt with a crew neck and no print;
- navy soft A-line mid-thigh shorts, slightly high-waisted;
- no drawcord;
- one slim vertical utility pocket integrated into the shorts on
  character-left, appearing on canvas-right in the front view;
- minimal warm-metal zipper detail only;
- white short-to-medium-short socks;
- rounded everyday blue-and-white sneakers without technical styling.

Avoid skort ambiguity, gym-short styling, a detached pouch, military or gadget
detail, logos, text, loud color blocking, and fashion-heavy decoration.

### Full-body hard gates

The full-body image passes only when all of these are true:

1. The face has a clear same-person read against the selected v2.1 face at
   enlarged scale.
2. The eyes preserve the selected geometry at full-body drawing scale.
3. Age, body balance, and non-sexual everyday presentation remain correct.
4. Hairpin, ponytail, and integrated pocket laterality are correct.
5. Clothing construction matches the fixed v2.1 baseline without skort,
   drawcord, or detached-pouch drift.
6. Visible limbs, joints, hands, fingers, feet, shoes, and their connections are
   anatomically coherent.
7. The strict-front neutral composition, margins, grounding, and background are
   clean.
8. There is no crop, seam, border, text, watermark, or generation artifact.

If the image fails, stop and report the failure. A targeted correction or `r02`
requires explicit user instruction.

## User Gates and Stop Conditions

Pause for explicit user input at each of these gates:

1. selection of one passing face candidate;
2. approval or rejection of the 30-degree stability-probe result;
3. approval or rejection of the front full-body result;
4. authorization to promote the two final assets;
5. authorization for any later angle, expression, wardrobe, batch, release, or
   PDF work.

An approved design document authorizes Stage 1 generation only. It does not
authorize Codex to choose a face, continue through later stages, retry failed
outputs, or expand the package without a new explicit gate.

## Promotion Contract

After explicit promotion approval, create the lightweight checkpoint package:

```text
akari-v2.1/
  README.md
  selection.md
  accepted/base/
    akari-v2.1-front-face-master.png
    akari-v2.1-front-fullbody.png
```

Promote the selected face and accepted full-body PNGs without resizing,
cropping, recompression, compositing, or color adjustment. Record in
`selection.md`:

- explicit user decisions and dates;
- source and destination paths;
- generation and request identifiers when available;
- input authority roles and hashes;
- dimensions and SHA-256 hashes;
- per-gate findings and accepted residual Minors;
- PNG signature verification;
- byte-identity verification with `cmp`;
- original-detail inspection results;
- exact tracked promotion scope.

Keep all rejected candidates, comparisons, prompts, transfer files, and the
30-degree probe untracked. The package is not a manifest-backed release or PDF.

## Missing-Output Recovery

If an image appears in the conversation but no local PNG is available, inspect
the current-date Codex rollout structurally for an `image_generation_call`
whose `result` begins with `iVBOR`. Decode only after confirming that the bytes
start with the PNG signature `89504e470d0a1a0a`. Save the recovered exact PNG
under the working run directory and record its generation or request identifier,
rollout source, output path, dimensions, and hash. Do not copy a large base64
payload manually from terminal output.

## Verification

Before asking for written-spec approval, run targeted Markdown lint on this
file, `git diff --check`, and a bounded scope inspection. After the document is
tracked, run the repository Markdown lint command. No image generation, Python
test, PDF audit, or release gate belongs to the design-document step.

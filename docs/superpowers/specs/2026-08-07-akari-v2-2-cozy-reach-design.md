# Akari v2.2 Cozy-Reach Illustration Design

Status: approved by the user; ready for implementation.

Date: 2026-08-07.

## Goal

Generate one review-only Akari v2.2 illustration that translates the supplied
examples' shared cute construction into an intimate everyday sofa moment. The
result should feel cute because of viewer proximity, a readable emotional
reaction, playful perspective, and a controlled color rhythm—not because Akari
has been made younger or redesigned.

The first output is one prototype. It does not replace, expand, or promote the
canonical v2.2 package.

## Approved Direction

- Emotional direction: intimate everyday cuteness.
- Scene: Akari reaches one hand toward the camera from a sofa.
- Expression: a blushing, softly exasperated “hey, stop filming” reaction.
- Outfit: the canonical v2.2 casual white T-shirt and blue denim skirt, with
  gray socks where the lower legs are visible.
- Reference strategy: balance identity and composition by using the two
  canonical v2.2 authorities first and one supplied composition reference
  third.
- Output boundary: exactly one built-in Imagegen call and one untracked review
  candidate.

## Age and Lineage

The user explicitly re-ratified during this design discussion that v2.2
continues v2.0's 18-year-old age contract. Preserve the **18-year-old
young-adult** impression carried through the v2.0 and v2.1 same-person lineage:
fresh and naturally cute, clearly not a child and not a mid-twenties
reinterpretation.

For this prototype, that explicit user ruling is the age authority. The
separate v2.2 character-sheet batch's conflicting “twenty-five-year-old”
wording is outside this task and must not enter this prompt or review criteria.
This design does not amend, repair, or reinterpret that separate batch.

## Input References

The generation uses exactly three ordered image references.

| Order | Role | Source | Dimensions | SHA-256 |
| ---: | --- | --- | --- | --- |
| 1 | Primary face, identity, eye, expression, hair, single-hairpin, and rendering authority | `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp` | `1888 x 3344` | `b076afd95be49c4ed9c5a4ddfb4083c9ead8328313b4d5fa0555a374dd10543c` |
| 2 | Body balance, casual outfit, laterality, and full-figure support | `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp` | `1888 x 3344` | `d93307fe219de81c6fb501e9472725a0ad8f3d242a0ddc741bf53d156f8d7688` |
| 3 | Composition and mood reference only | `/home/takahiro/.codex/attachments/fa016a44-2698-4939-aaa5-607832e76ac7/HFfjnyCbQAA19tl.jpg` | `1480 x 2184` | `13523b51df5999a93ab934ecf563a4b7c5631e79d5c76583ed6ee028903db191` |

Reference 1 wins every conflict involving face identity, apparent age, eyes,
cheeks, chin, bangs, hair palette, ponytail, hairpin, and close-view finish.
Reference 2 wins body, outfit, and scene-appropriate clothing construction.
Reference 3 contributes only the intimate first-person viewpoint, diagonal
body flow, foreground reaching-hand perspective, direct viewer interaction,
and warm sofa atmosphere.

The approved scene intentionally changes the literal smile and V-sign standing
pose shown by References 1 and 2. This design's softly exasperated expression,
reaching gesture, sofa pose, and portrait composition therefore control those
four scene-specific decisions. Reference 1 still controls the facial
construction beneath the changed expression, and Reference 2 still controls
body balance, outfit construction, and laterality beneath the changed pose.

Do not transfer Reference 3's black hair, gray eyes, face, sailor uniform,
school bag, speech bubbles, room layout, or character identity. The other two
supplied inspiration images informed the general technique analysis but are
not generation inputs.

## Scene and Composition

Create a vertical portrait illustration in a warm, quiet living room. Akari is
settled naturally on a beige sofa, supporting herself with one arm while
looking directly toward the viewer. Her body follows a relaxed diagonal into
the depth of the frame.

Place her face large and near the visual center. One open hand reaches toward
the lens from the lower foreground and becomes noticeably larger through
foreshortening. Keep the hand secondary to the face: it creates intimacy and
depth without blocking both eyes or dominating the image.

Her other forearm rests comfortably near or beneath her cheek. Her legs may
recede into the background with lightly bent knees and gray-socked feet, but
the pose and crop must preserve natural clothing coverage and avoid directing
attention toward the skirt. Shoes may remain outside the scene because she is
on the sofa.

Use only a few supporting accents: a blue cushion that echoes the hairpin and
denim, plus one optional small coral annoyance mark floating freely above a
distant sofa cushion. If present, the mark has no enclosing bubble, border,
word, letter, or character. Render no speech bubbles, captions, decorative
pseudo-text, logo, or watermark.

## Expression and Emotional Read

The image should read as affectionate exasperation rather than anger:

- direct, coordinated eye contact;
- a soft blush across both cheeks;
- relaxed brows with only a slight protesting lift or pinch;
- a small open mouth or restrained half-smile that suggests “hey, stop”;
- an engaged, familiar presence, as if the viewer is a close childhood
  friend standing just beyond the camera.

Do not use a neutral model pose, a glamorous expression, a distressed face, an
aggressive gesture, or a pout that makes her look substantially younger.

## Cute-Rendering Technique

Use a polished anime illustration finish with:

- thin warm-brown to neutral-gray colored linework rather than uniformly heavy
  black outlines;
- clean, controlled cel-shadow shapes;
- soft blending reserved mainly for cheeks, skin transitions, and restrained
  hair highlights;
- a compact palette of warm chestnut, white, denim blue, warm beige, skin
  peach, and a small coral accent;
- detail concentrated around the face, eyes, hand, hairpin, and clothing
  edges, with a quieter background.

Allow the close camera to make the head and eyes feel slightly more prominent,
but keep the canonical facial construction and 18-year-old young-adult read.
Do not inflate the eyes into a doll-like style, shorten the lower face into a
child's proportions, or turn the body into a chibi figure.

## Locked V2.2 Identity

Preserve:

- the same warm amber-brown eyes, eye spacing, coordinated gaze, brows, soft
  cheeks, compact rounded chin, small nose, and familiar smile construction;
- warm chestnut hair with soft off-center bangs and one low side ponytail on
  character-left/canvas-right, secured by the same blue tie;
- exactly one straight, slender, filled blue capsule hairpin above the
  character-left temple, visible on canvas-right, rising toward crown-back at
  approximately 45–60 degrees and approximately 0.8–1.0 visible eye width;
- one quiet dark hairpin legibility edge only when needed;
- the plain white short-sleeve T-shirt, blue denim skirt, and gray socks where
  visible;
- the same approachable same-person palette and polished soft-cel rendering
  family.

Forbid a second pin, crossing, doubled outline, internal pin line, loop,
ornament attachment, black-hair drift, gray-eye drift, uniform transfer, and
unrelated wardrobe decoration.

## Anatomy and Framing Constraints

- The reaching hand is constructed as one palm, one thumb, and four fingers
  with plausible knuckles and a coherent wrist-to-forearm connection. Natural
  finger overlap or partial occlusion is allowed, but the hand must not imply
  an extra or structurally missing digit.
- Both arms, shoulders, neck, torso, and every visible part of the hips, legs,
  and feet remain anatomically connected and compatible with the camera
  perspective. Off-frame anatomy must have a plausible continuation.
- No merged limbs, duplicate fingers, extra hands, fused feet, broken joints,
  disconnected hair, or sofa intersections.
- Keep the T-shirt and skirt naturally fitted for the pose. No underwear view,
  cleavage emphasis, transparent fabric, voyeuristic angle, or fetish framing.
- Do not crop through the eyes, primary reaching hand, or another essential
  feature.

## Considered Approaches

1. **Balanced three-reference generation, selected.** The two canonical v2.2
   images lock the person and outfit; the sofa image contributes only
   perspective and emotional staging. This offers the best balance of identity
   continuity and the requested cute effect.
2. **Identity-first two-reference generation.** Using only the canonical v2.2
   pair would reduce style contamination, but the intimate POV and foreground
   hand would be less strongly demonstrated to the model.
3. **Atmosphere-first five-reference generation.** Using all three supplied
   inspiration images would intensify the general cute vocabulary but create
   avoidable pressure toward black hair, uniforms, costume details, and a more
   childlike face.

## Approved Master Prompt

Persist the following prompt verbatim as `prompts/master.txt` and use it as the
complete prompt for the single built-in Imagegen call. Do not silently add,
remove, or reorder creative requirements.

```text
Use case: illustration-story
Asset type: one review-only Akari v2.2 prototype illustration

Input images:
- Image 1 is the PRIMARY face, identity, eye, apparent-age, hair, single-hairpin, palette, and close-rendering authority.
- Image 2 is the BODY BALANCE, canonical casual outfit, laterality, and full-figure support authority.
- Image 3 is a COMPOSITION AND MOOD REFERENCE ONLY. Borrow only its intimate first-person sofa viewpoint, diagonal body flow, foreground reaching-hand foreshortening, direct viewer interaction, and warm domestic atmosphere. Do not copy its person, face, hair, eyes, sailor uniform, school bag, speech bubbles, room layout, or character identity.

Primary request: Create one polished vertical portrait anime illustration of the same Akari from Images 1 and 2 in an intimate everyday sofa moment. She is the same 18-year-old young adult established by the v2.0-to-v2.2 lineage: fresh and naturally cute, clearly not a child and not a mid-twenties reinterpretation.

Scene/backdrop: A quiet warm living room with a beige sofa. Akari is settled naturally on the sofa, supporting herself with one arm while looking directly toward the viewer. Include one blue cushion as a restrained accent. Optionally include one small unframed coral annoyance mark floating above a distant cushion; it must contain no text or enclosing bubble.

Composition/framing: Vertical portrait composition. Place her face large and near the visual center. Let her body follow a relaxed diagonal into the depth of the frame. One open hand reaches toward the lens from the lower foreground and becomes noticeably larger through natural wide-angle foreshortening, but remains secondary to the face and does not block both eyes. Her other forearm rests comfortably near or beneath her cheek. Her legs may recede into the background with lightly bent knees and gray-socked feet where visible. Keep natural clothing coverage and do not direct attention toward the skirt.

Expression/emotional read: Affectionate exasperation rather than anger. Preserve Image 1's exact facial construction beneath a changed scene expression: coordinated direct gaze, soft blush across both cheeks, relaxed brows with a slight protesting lift or pinch, and a small open mouth or restrained half-smile that reads as “hey, stop filming.” She feels familiar and engaged, as if the viewer is a close childhood friend just beyond the camera.

Identity locks: Preserve Image 1's warm amber-brown eyes, eye spacing, brows, soft cheeks, compact rounded chin, small nose, warm chestnut hair, soft off-center bangs, and polished soft-cel rendering family. Preserve one low side ponytail on character-left/canvas-right with the same blue tie. Preserve exactly one straight slender filled blue capsule hairpin above the character-left temple, visible on canvas-right, rising toward crown-back at approximately 45–60 degrees and approximately 0.8–1.0 visible eye width. One quiet dark edge is allowed only for legibility. Preserve Image 2's plain white short-sleeve T-shirt, blue denim skirt, gray socks where visible, healthy body balance, and laterality. The approved sofa pose and reaching gesture replace the literal standing V-sign pose in Image 2 without changing her underlying body identity.

Style/medium: Polished anime illustration with thin warm-brown to neutral-gray colored linework, clean controlled cel-shadow shapes, soft blending mainly on cheeks and skin transitions, and restrained warm hair highlights. Let the close camera make the head and eyes feel slightly more prominent without changing the canonical face or turning her into a chibi figure.

Color palette: Warm chestnut, white, denim blue, warm beige, skin peach, and a small coral accent. Keep the background quieter than the face, eyes, reaching hand, hairpin, and clothing edges.

Anatomy and coverage: Construct the reaching hand as one palm, one thumb, and four fingers with plausible knuckles and a coherent wrist-to-forearm connection. Natural finger overlap or partial occlusion is allowed, but no extra or structurally missing digit. Keep both arms, shoulders, neck, torso, and every visible part of the hips, legs, and feet anatomically connected, with plausible off-frame continuation. Keep the T-shirt and denim skirt naturally fitted and fully covering for the pose.

Avoid: childlike age drift, mid-twenties age drift, doll-like giant eyes, chibi proportions, black hair, gray eyes, copied face from Image 3, sailor uniform, school bag, crossed hairpins, second hairpin, doubled pin outline, internal pin line, loop, ornament attachment, unrelated wardrobe decoration, neutral model pose, glamour expression, aggressive anger, extra person, merged limbs, duplicate fingers, extra hands, fused feet, broken joints, disconnected hair, sofa intersections, underwear view, cleavage emphasis, transparent fabric, voyeuristic or fetish framing, text, pseudo-text, speech bubble, logo, watermark, border, seam, or material generation artifact.
```

## Execution Boundary

Use the built-in Imagegen path for one new image-generation call. Do not use a
previous generated candidate as an input and do not make an automatic retry.

Keep all execution material under the ignored directory:

```text
tmp/akari-v2.2-cozy-reach/r01/
  inputs/
    portrait-authority.webp
    fullbody-authority.webp
    composition-reference.jpg
  prompts/
    master.txt
  outputs/
    akari-v2.2-cozy-reach-r01.png
  run.md
```

Before generation:

- verify all three hashes and dimensions;
- confirm the run directory is ignored and the exact destinations do not
  exist;
- copy each reference without overwrite and verify it byte-for-byte with
  `cmp`;
- persist the approved master prompt above verbatim before the call and record
  its SHA-256;
- open all three references at original detail and state their distinct roles.

Call Imagegen with `referenced_image_paths` set to exactly these verified
run-directory copies in this order:

1. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-cozy-reach/r01/inputs/portrait-authority.webp`
2. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-cozy-reach/r01/inputs/fullbody-authority.webp`
3. `/home/takahiro/workspace/akari-design/tmp/akari-v2.2-cozy-reach/r01/inputs/composition-reference.jpg`

Omit `num_last_images_to_include` so unrelated conversation images do not
enter the generation.

After generation:

- copy the built-in result into the assigned output path without overwrite;
- record the built-in result path, generation/call/request identifier when
  returned, dimensions, format, colorspace, bytes, PNG signature, SHA-256, and
  `cmp` result when a source path is available; record an unavailable metadata
  field explicitly as `not returned` rather than inventing a value;
- inspect the saved output at original detail and at reduced scale;
- run the bounded Git-scope checks and confirm no canonical or tracked image
  changed.

If the built-in image is visible but no local PNG can be found, recover only
the PNG payload matching the returned generation/call/request identifier. If
the tool returned no identifier, inspect only the current rollout interval
between this call's invocation and completion and require exactly one PNG
payload beginning `iVBOR`; stop as ambiguous if zero or multiple payloads
match. Use the repository's structured `image_generation_call` recovery
procedure, verify the `89504e470d0a1a0a` signature before saving, and refuse to
overwrite any file.

## Review Gates

The prototype review records evidence for all seven gates:

1. **Identity and age:** immediately recognizable as the same v2.2 Akari and
   reads as an 18-year-old young adult, neither childlike nor mid-twenties.
2. **Emotional success:** the direct gaze, blush, mouth, reaching gesture, and
   proximity clearly communicate a cute, softly protesting “hey, stop” moment.
3. **Hair continuity:** chestnut hair, bangs, side ponytail, blue tie, and the
   exact one-piece blue hairpin remain coherent and correctly lateralized.
4. **Anatomy:** the foreshortened hand, fingers, wrist, arms, neck, and all
   visible parts of the legs and feet are plausible and unmerged; off-frame
   parts have a coherent implied continuation.
5. **Outfit and coverage:** white T-shirt, denim skirt, and gray socks remain
   scene-coherent, naturally covered, and free of reference-three wardrobe
   transfer.
6. **Composition and finish:** the face stays primary, the diagonal sofa scene
   reads clearly, the restrained palette and soft-cel rendering feel polished,
   and the background does not become cluttered.
7. **Artifact safety:** no extra person, duplicate feature, disconnected prop,
   text, pseudo-text, logo, watermark, border, seam, or material generation
   artifact.

Present the single generated candidate and the review findings to the user even
if a gate fails. Do not hide a weak output, replace it with a second call, start
a correction round, or promote it without a new explicit decision.

## Non-Goals

This prototype does not create a batch, alternate expression, turnaround,
character sheet, wardrobe set, mechanical comparison, release package,
manifest, PDF, or canonical promotion. It does not modify the existing v2.2
authorities or repair the separate character-sheet batch. User acceptance of
the displayed prototype does not itself authorize promotion or another image
generation call.

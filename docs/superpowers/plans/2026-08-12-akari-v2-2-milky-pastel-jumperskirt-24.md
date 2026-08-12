# Akari V2.2 Milky-Pastel Jumperskirt 24-Scene Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate one approved jumperskirt-uniform anchor and exactly
twenty-four review-ready Akari V2.2 portrait scenes in four luminous
milky-pastel chapters.

**Architecture:** Run one identity preflight, then a gated three-uniform study,
then four sequential six-image scene waves. Every generation is one built-in
image call with the minimum approved local references; every result is checked
against the canonical portrait before the next call, and all output remains in
one ignored run directory until the user explicitly requests preservation.

**Tech Stack:** Built-in image_gen, local view_image, PNG/WebP references,
ImageMagick identify and montage, Markdown prompt and review ledgers.

## Global Constraints

- Design authority:
  docs/superpowers/specs/2026-08-12-akari-v2-2-milky-pastel-jumperskirt-24-design.md.
- Run root:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/.
- Use the repository canonical portrait as the sole face, eye, hair, hairpin,
  apparent-adult-age, and close-rendering authority:
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp.
- Use the repository canonical full body only for body proportion, balance,
  laterality, and complete-figure construction:
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp.
- Open both canonical files at original detail before the first call. Reopen
  every path that will be passed immediately before each later call.
- Use built-in image_gen with exactly one output image per call. Use
  referenced_image_paths for local references and never combine it with
  num_last_images_to_include.
- Pass no more than three images. The local cute-composition pack is inspected
  for camera grammar only and is never passed to image_gen.
- Every final candidate is a 2:3 portrait targeted at 1024 x 1536 or larger.
- The set contains human Akari only: no cat ears, animal traits, fantasy
  anatomy, readable text, logos, watermarks, speech balloons, comic
  punctuation, decorative symbol fields, poster borders, or sticker outlines.
- Preserve warm chestnut hair, amber-brown eyes, one blue ponytail tie, a low
  side ponytail, and exactly one blue capsule hairpin on canvas-right.
- Identity preflight gets one call and no retry. A clear Codex identity failure
  or user rejection stops the built-in new-scene path.
- U-A is the first production image. It may receive at most one identity retry
  that changes exactly one recorded variable. A second failure stops the path.
- U-B, U-C, and all twenty-four scenes receive no automatic retry. Any clear
  identity failure stops all ungenerated work. A non-identity technical defect
  is held for user review instead of being silently edited.
- Only the user can approve identity. An unapproved or failed image must never
  become an input, edit target, continuity anchor, compositing source, or
  textual source of face-continuity details.
- The selected uniform study becomes Image C or the second input only after
  the user both selects it and explicitly approves that saved local file for
  identity and wardrobe continuity.
- Generate scenes in Cream, Mint, Coral, and Lavender order. Stop after every
  six-image contact sheet for user review before beginning the next chapter.
- Keep all generated images, prompts, reviews, and contact sheets under the
  ignored run root. Do not change akari-v2.2/accepted/, manifests, release
  files, PDFs, or the existing D40-D80 run.
- Do not add a Git commit step to runtime tasks: committing ignored candidates
  would violate the approved boundary. Only this tracked plan and the approved
  status update are committed before execution.

---

## Runtime File Map

The implementation creates only ignored runtime material:

    tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/
    ├── PROMPTS.md
    ├── REVIEW.md
    ├── preflight/
    │   └── identity-preflight.png
    ├── uniform/
    │   ├── u-a-classic-navy-r01.png
    │   ├── u-a-classic-navy-r02.png
    │   ├── u-b-milky-blue-retro-r01.png
    │   ├── u-c-tailored-deep-teal-r01.png
    │   ├── uniform-contact-sheet.jpg
    │   └── selection.md
    ├── chapters/
    │   ├── cream/
    │   │   ├── c01-collar-adjustment.png
    │   │   ├── c02-mug-offer.png
    │   │   ├── c03-sun-shade-palm.png
    │   │   ├── c04-sleeve-thread.png
    │   │   ├── c05-door-push.png
    │   │   └── c06-corridor-turn.png
    │   ├── mint/
    │   │   ├── m01-strawberry-offer.png
    │   │   ├── m02-hat-brim-peek.png
    │   │   ├── m03-pinwheel-breeze.png
    │   │   ├── m04-bag-strap-pull.png
    │   │   ├── m05-sleeve-roll.png
    │   │   └── m06-curb-step.png
    │   ├── coral/
    │   │   ├── r01-sorbet-spoon.png
    │   │   ├── r02-single-flower.png
    │   │   ├── r03-scarf-catch.png
    │   │   ├── r04-baguette-carry.png
    │   │   ├── r05-cardigan-turn.png
    │   │   └── r06-stair-turn.png
    │   └── lavender/
    │       ├── l01-round-light.png
    │       ├── l02-cuff-button.png
    │       ├── l03-desk-arm-rest.png
    │       ├── l04-yawn-stretch.png
    │       ├── l05-book-close.png
    │       └── l06-hallway-light-turn.png
    └── contact-sheets/
        ├── cream.jpg
        ├── mint.jpg
        ├── coral.jpg
        ├── lavender.jpg
        └── all-24.jpg

The U-A r02 file is created only when the single allowed identity retry is
actually used. PROMPTS.md records exact prompts, ordered input paths, tool
source paths, saved paths, and whether recovery from a rollout payload was
needed. REVIEW.md records the pre-existing repository status, per-image QA,
user decisions, stop state, and chapter checkpoint results.

## Exact Prompt Assembly Contract

### Identity preflight prompt

Pass only the canonical portrait as referenced_image_paths Image A:

    Image A is the sole facial identity authority for Akari V2.2.

    Create one diagnostic portrait illustration of the exact same Akari shown
    in Image A. Keep the same head angle, gaze direction, bright expression,
    facial geometry, eye opening and iris scale, brows, cheeks, jaw, mouth and
    cheek relationship, bangs, warm chestnut hair, low side ponytail, one blue
    ponytail tie, and exactly one blue capsule hairpin on viewer-right. Dress
    her in a plain white T-shirt.

    Use a close face-first 2:3 portrait with a simple warm-cream indoor
    background, soft neutral daylight, both eyes clearly readable, no handheld
    prop, and no main action. Preserve the clean, soft Akari V2.2 line and
    rendering density.

    Do not redesign the face, narrow or lengthen the eyes, change iris scale,
    re-age her, change the ponytail or hairpin side, add hairpins, add animal
    traits, or add readable text, logos, watermarks, or graphic decoration.

### Uniform study prompts

For all three studies, pass the canonical portrait as Image A and canonical
full body as Image B. Never pass an earlier study.

U-A prompt:

    Image A is the sole facial identity authority for Akari V2.2. Image B
    controls adult body proportion, balance, laterality, and complete-figure
    construction only; it is not a face authority.

    Create a new illustration of the exact same Akari V2.2 person shown in
    Image A. Preserve her facial geometry, rounded-almond eye opening and iris
    scale, brows, cheeks, jaw, mouth and cheek relationship, warm chestnut
    hair, bangs, low side ponytail, blue ponytail tie, and exactly one blue
    capsule hairpin on viewer-right.

    Dress her in a plain classic jumperskirt uniform: a white short-sleeve
    blouse under a deep navy square-neck jumperskirt with a slightly high waist
    seam, broad box pleats, a below-knee hem, simple charcoal socks, and brown
    loafers. No crest, badge, lettering, school name, sailor collar, blazer,
    tie clutter, mini hem, cleavage, or fashion hardware.

    Use a shallow three-quarter full-body pose with both eyes visible, relaxed
    connected arms and hands, both feet readable, and no handheld prop. Keep
    the camera quiet and matched for wardrobe comparison. Use a simple
    warm-cream background, neutral soft light, and a 2:3 portrait composition.

    Preserve clean soft Akari V2.2 rendering. Do not redesign the face, narrow
    or lengthen the eyes, change iris scale, re-age her, change the ponytail or
    hairpin side, add hairpins, break limb continuity, or add readable text,
    logos, watermarks, animal traits, or graphic decoration.

U-B prompt:

    Image A is the sole facial identity authority for Akari V2.2. Image B
    controls adult body proportion, balance, laterality, and complete-figure
    construction only; it is not a face authority.

    Create a new illustration of the exact same Akari V2.2 person shown in
    Image A. Preserve her facial geometry, rounded-almond eye opening and iris
    scale, brows, cheeks, jaw, mouth and cheek relationship, warm chestnut
    hair, bangs, low side ponytail, blue ponytail tie, and exactly one blue
    capsule hairpin on viewer-right.

    Dress her in a plain milky-blue retro jumperskirt uniform: a cream blouse
    with a restrained rounded collar under a clean milk-blue V-neck
    jumperskirt, one centered inverted pleat, an upper-calf hem, simple
    gray-blue socks, and brown loafers. Keep the blue clear and luminous rather
    than gray or chalky. No crest, badge, lettering, school name, sailor
    collar, blazer, tie clutter, mini hem, cleavage, or fashion hardware.

    Use a shallow three-quarter full-body pose with both eyes visible, relaxed
    connected arms and hands, both feet readable, and no handheld prop. Match
    U-A's quiet camera, warm-cream background, neutral soft light, and 2:3
    portrait composition.

    Preserve clean soft Akari V2.2 rendering. Do not redesign the face, narrow
    or lengthen the eyes, change iris scale, re-age her, change the ponytail or
    hairpin side, add hairpins, break limb continuity, or add readable text,
    logos, watermarks, animal traits, or graphic decoration.

U-C prompt:

    Image A is the sole facial identity authority for Akari V2.2. Image B
    controls adult body proportion, balance, laterality, and complete-figure
    construction only; it is not a face authority.

    Create a new illustration of the exact same Akari V2.2 person shown in
    Image A. Preserve her facial geometry, rounded-almond eye opening and iris
    scale, brows, cheeks, jaw, mouth and cheek relationship, warm chestnut
    hair, bangs, low side ponytail, blue ponytail tie, and exactly one blue
    capsule hairpin on viewer-right.

    Dress her in a plain tailored jumperskirt uniform: an ivory blouse with a
    simple collar under a deep blue-green shallow-U-neck jumperskirt with
    restrained vertical seam construction, a modest A-line silhouette, a
    below-knee hem, simple dark socks, and loafers. No crest, badge, lettering,
    school name, sailor collar, blazer, tie clutter, mini hem, cleavage, or
    fashion hardware.

    Use a shallow three-quarter full-body pose with both eyes visible, relaxed
    connected arms and hands, both feet readable, and no handheld prop. Match
    U-A's quiet camera, warm-cream background, neutral soft light, and 2:3
    portrait composition.

    Preserve clean soft Akari V2.2 rendering. Do not redesign the face, narrow
    or lengthen the eyes, change iris scale, re-age her, change the ponytail or
    hairpin side, add hairpins, break limb continuity, or add readable text,
    logos, watermarks, animal traits, or graphic decoration.

### Scene input-role blocks

For every close or half-body scene, pass exactly two ordered paths: canonical
portrait as Image A, then the user-approved uniform anchor as Image B. Begin
the prompt with:

    Image A is the sole facial identity authority for Akari V2.2. Image B is a
    user-approved same-character wardrobe and set-continuity anchor; use only
    its selected jumperskirt construction and color continuity. Image B never
    overrides Image A's face, eyes, hair, hairpin, apparent adult age, or close
    rendering.

For every full-body scene, pass exactly three ordered paths: canonical portrait
as Image A, canonical full body as Image B, then the user-approved uniform
anchor as Image C. Begin the prompt with:

    Image A is the sole facial identity authority for Akari V2.2. Image B
    controls adult body proportion, balance, laterality, and complete-figure
    construction only; it is not a face authority. Image C is a user-approved
    same-character wardrobe and set-continuity anchor; use only its selected
    jumperskirt construction and color continuity. Images B and C never
    override Image A's face, eyes, hair, hairpin, apparent adult age, or close
    rendering.

### Shared scene identity block

Append this exact block after the input-role block:

    Create a new illustration of the exact Akari V2.2 person shown in Image A.
    Preserve her facial geometry, rounded-almond eye opening and iris scale,
    brows, cheeks, jaw, mouth and cheek relationship, warm chestnut hair,
    bangs, low side ponytail, one blue ponytail tie, and exactly one blue
    capsule hairpin on viewer-right. Keep both eyes readable unless the scene
    naturally crops one edge of the face; never hide identity behind the prop.

### Selected-uniform blocks

selection.md must contain exactly one saved anchor path and exactly one of
these blocks. Append the selected block without mixing alternatives.

U-A block:

    Keep the approved classic uniform unchanged: white blouse, deep navy
    square-neck jumperskirt, slightly high waist seam, broad box pleats,
    below-knee hem, charcoal socks when visible, and brown loafers when
    visible.

U-B block:

    Keep the approved retro uniform unchanged: cream restrained rounded-collar
    blouse, clear milk-blue V-neck jumperskirt, one centered inverted pleat,
    upper-calf hem, gray-blue socks when visible, and brown loafers when
    visible.

U-C block:

    Keep the approved tailored uniform unchanged: ivory simple-collar blouse,
    deep blue-green shallow-U-neck jumperskirt, restrained vertical seams,
    modest A-line silhouette, below-knee hem, dark socks when visible, and
    loafers when visible.

### Chapter wardrobe and palette blocks

Cream:

    Use the basic blouse with no outer layer. Light the scene with luminous
    warm cream, shell peach, butter yellow, and a restrained powder-blue
    accent. Keep large clean color planes; do not gray or wash out skin, hair,
    eyes, or the dark uniform structure.

Mint:

    Use the basic blouse with no outer layer. Light the scene with luminous
    milk blue, clear mint, pale aqua, and soft young green over warm-cream
    neutrals. Keep large clean color planes; do not turn the palette chalky.

Coral:

    Add one soft-coral cardigan worn open enough to keep the approved neckline,
    waist, and skirt construction readable. Use luminous soft coral, apricot,
    rose milk, and light lilac over warm-cream neutrals.

Lavender:

    Add one pale-lavender knit layer worn open enough to keep the approved
    neckline, waist, and skirt construction readable. Use luminous lavender,
    periwinkle, moon white, and restrained blue-green with gentle evening
    depth, not gray desaturation.

### Shared scene rendering and negative block

Append this exact block after the scene-specific block:

    Render one 2:3 portrait targeted at 1024 x 1536 or larger in clean, soft
    Akari V2.2 anime illustration. Spend detail on the face, hair, connected
    hands and body, and uniform construction. Use at most the one named main
    prop and only one or two simple physical space cues. Keep the rest as broad
    warm-white and pastel surfaces with natural light falloff.

    Do not redesign the face, narrow or lengthen the eyes, change iris scale,
    re-age her, change the ponytail or hairpin side, add hairpins, break hand or
    limb continuity, copy another character identity, or add readable text,
    logos, watermarks, animal traits, speech balloons, comic marks, decorative
    symbol fields, poster borders, or sticker outlines.

## Scene Prompt Catalog

The relevant local-pack image is opened for visual analysis only. Its camera
grammar is already encoded in the exact scene block and it is never included
in referenced_image_paths.

| ID | Output slug | Frame | Local-pack image | Exact scene-specific prompt block |
| --- | --- | --- | --- | --- |
| C01 | c01-collar-adjustment | close | 03-close-face-hand-gesture.jpg | Scene: with a composed small smile, Akari adjusts her blouse collar. Use an extreme close crop: one connected hand and the collar enlarge across the lower foreground while her off-center face sits on the opposite diagonal. Both eyes and the selected neckline remain readable. |
| C02 | c02-mug-offer | close | 04-cafe-wide-angle-scene.jpg | Scene: Akari offers one plain cream mug with a warm open-eyed welcome. Let the mug fill one lower corner while she leans in from the opposite upper corner. Use wide-angle foreground scale and a bold off-center crop; show only a simple table or window cue. |
| C03 | c03-sun-shade-palm | close | 07-double-v-diagonal.jpg | Scene: Akari raises one connected palm near the top of the lens to shade soft backlight, smiling as if lightly dazzled. Place her face off-center beside the enlarged palm on a counter-diagonal. Keep both eyes readable and do not let the hand cover the face. |
| C04 | c04-sleeve-thread | half | 02-kitchen-wide-angle-motion.jpg | Scene: with focused soft amusement, Akari threads one arm into or straightens the blouse sleeve. Use a wide-angle half-body crop: the sleeve and connected hand approach the camera while her torso twists away on a strong diagonal. Use one plain wall or window edge only. |
| C05 | c05-door-push | half | 02-kitchen-wide-angle-motion.jpg | Scene: Akari pushes one plain door and looks back over her shoulder with a small curious expression. Let the connected pushing hand and one door edge dominate the foreground while the torso and face recede on an opposing diagonal. Keep the doorway physically coherent. |
| C06 | c06-corridor-turn | full | 05-cheer-motion-foreshortening.jpg | Scene: Akari rounds one plain corridor corner with a bright relaxed smile. Use a floor-level full-body camera: one coherent near foot, turning body, and readable face form one rising diagonal. Show both connected legs and a simple floor-wall junction. |
| M01 | m01-strawberry-offer | close | 03-close-face-hand-gesture.jpg | Scene: Akari offers exactly one strawberry close to the lens with playful anticipation. Enlarge the berry and one connected holding hand in the foreground while her face approaches from the opposite side on a diagonal. Keep both eyes unobstructed. |
| M02 | m02-hat-brim-peek | close | 06-extreme-close-face.jpg | Scene: Akari peeks from below one plain pale hat brim with a shy closed-mouth smile. Let the broad brim cut diagonally across the near foreground and use an asymmetrical extreme close crop. The brim frames rather than covers both readable eyes. |
| M03 | m03-pinwheel-breeze | close | 01-close-diagonal-plush.jpg | Scene: one unlettered pastel pinwheel turns in the near foreground as a light breeze moves Akari's hair behind it; she shows small open-eyed surprise. Balance the enlarged pinwheel against her off-center face on a strong diagonal without covering her eyes or hairpin. |
| M04 | m04-bag-strap-pull | half | 02-kitchen-wide-angle-motion.jpg | Scene: with ready-to-go focus, Akari pulls one plain shoulder-bag strap toward the lens. Use a wide-angle half-body view: the connected hand and strap enlarge in the foreground while her torso counter-rotates along a diagonal. Show only a plain wall or door cue. |
| M05 | m05-sleeve-roll | half | 02-kitchen-wide-angle-motion.jpg | Scene: Akari calmly rolls one blouse sleeve. A foreshortened connected elbow enters the foreground and leads through the rolling hand to her side-turned face. Use a strong diagonal and a bold half-body crop with a minimal warm interior cue. |
| M06 | m06-curb-step | full | 05-cheer-motion-foreshortening.jpg | Scene: Akari steps down one simple curb with a carefree smile. Use a low full-body camera: one coherent stepping foot approaches the foreground while her balanced adult body recedes along a clean diagonal. Show the second foot, curb edge, and ground contact clearly. |
| R01 | r01-sorbet-spoon | close | 04-cafe-wide-angle-scene.jpg | Scene: Akari presents one plain spoon holding one small pastel sorbet scoop, looking delighted in anticipation. Enlarge the spoon and connected hand in one foreground corner and place her off-center face on the opposite diagonal. Show one simple tabletop cue only. |
| R02 | r02-single-flower | close | 03-close-face-hand-gesture.jpg | Scene: Akari holds exactly one pale flower beside her cheek with a soft attentive smile. Bring the flower and connected fingers slightly forward while cropping her face off-center on a counter-diagonal. Keep both eyes and the single hairpin readable. |
| R03 | r03-scarf-catch | close | 07-double-v-diagonal.jpg | Scene: Akari catches one windblown scarf end with a surprised grin. Let the scarf end and connected catching hand sweep through the foreground opposite the diagonal of her face and shoulders. Keep the cloth away from both eyes and preserve coherent hand-to-cloth contact. |
| R04 | r04-baguette-carry | half | 02-kitchen-wide-angle-motion.jpg | Scene: Akari carries exactly one baguette in a blank unlabelled paper sleeve and gives a pleased side glance. Use a wide-angle half-body view: the baguette crosses the lower foreground while she leans over it on the opposing diagonal. Keep both hands and the paper sleeve coherent. |
| R05 | r05-cardigan-turn | half | 02-kitchen-wide-angle-motion.jpg | Scene: Akari turns with an amused half-smile while settling the soft-coral cardigan. One connected cardigan sleeve creates a simple enlarged foreground arc while her off-center upper body rotates on the opposing diagonal in a bold half-body crop. Preserve the selected neckline and waist beneath the open cardigan. |
| R06 | r06-stair-turn | full | 05-cheer-motion-foreshortening.jpg | Scene: Akari turns on one simple stair flight and looks back with a warm smile. Use a low full-body camera: one descending step, her balanced torso, and readable face form a clear S-curve. Show coherent feet, stair contact, railing or wall edge, and no dense background. |
| L01 | l01-round-light | close | 06-extreme-close-face.jpg | Scene: Akari holds exactly one small opaque milky round light near her cheek with quiet contentment. Use a bold asymmetrical close crop and form a diagonal pair between the light and her off-center face against a minimal dark-lavender field. The light must not obscure or overexpose her eyes or facial geometry. |
| L02 | l02-cuff-button | close | 03-close-face-hand-gesture.jpg | Scene: with gentle concentration, Akari fastens one blouse cuff. Use an extreme close crop: the connected fastening hand and cuff occupy the near foreground while her unobstructed face remains behind them on a diagonal. Keep the cuff, fingers, and wrist connection clear. |
| L03 | l03-desk-arm-rest | close | 01-close-diagonal-plush.jpg | Scene: Akari rests above folded forearms at a minimal desk with a tired but warm gaze. Enlarge the connected forearms across the lower foreground and tilt her off-center face just above them on a gentle diagonal. Keep both eyes visible and show only one desk edge. |
| L04 | l04-yawn-stretch | half | 07-double-v-diagonal.jpg | Scene: Akari gives a natural sleepy yawn while stretching. Use a wide-angle half-body crop: both connected sleeved arms rise on opposing diagonals and frame rather than cover her face. Keep shoulders, elbows, hands, and the open cardigan or knit layer anatomically continuous. |
| L05 | l05-book-close | half | 02-kitchen-wide-angle-motion.jpg | Scene: Akari leans across one minimal desk and closes exactly one blank unlettered book with a foreground palm, looking calmly finished for now. Make the connected hand, book, and off-center face form a clear triangle with mild wide-angle depth. |
| L06 | l06-hallway-light-turn | full | 05-cheer-motion-foreshortening.jpg | Scene: Akari turns in a simple hallway with a gentle backward glance while exactly one opaque round light provides a spatial cue. Use a floor-level full-body view: coherent feet, the light, and her readable turning face align along a long diagonal. Keep the floor-wall relationship simple and physical. |

## Per-Image QA Contract

Immediately after every call, save the built-in output unchanged, run identify,
and open the saved image plus the canonical portrait at original detail. Record
the following in REVIEW.md before any next call:

1. exact ID, tool source path, saved path, ordered reference paths, and prompt
   entry in PROMPTS.md;
2. dimensions, 2:3 orientation, decode success, and colorspace;
3. identity verdict using only clear failure or user confirmation pending;
4. comparable-scale face findings: cheeks-to-jaw shape, eye opening and iris
   scale, brows-to-eyes relationship, nose and mouth placement, mouth-to-cheek
   response, bangs, adult impression, line weight, and rendering density;
5. warm chestnut hair, low side ponytail, blue tie, exactly one blue capsule
   hairpin on canvas-right, and both eyes where required;
6. connected hands, limbs, balance, foreshortening, and body support;
7. selected neckline, waist, pleats, hem, and chapter layer;
8. prop count, hand-to-prop contact, foreground separation, and one or two
   coherent space cues;
9. luminous chapter palette without chalky grayness or washed-out identity;
10. no text, logos, watermarks, copied identity, graphic fields, animal traits,
    or other artifacts.

If a local PNG is missing after the image appears in conversation, follow the
repository AGENTS.md payload-recovery procedure: inspect the current day's
rollout JSONL structurally, select the matching image_generation_call whose
result begins iVBOR, verify the decoded signature is 89504e470d0a1a0a, and
write only that payload to the assigned run path. Never hand-copy base64.

---

### Task 1: Validate Authorities and Run the Identity Preflight

**Files:**

- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/PROMPTS.md
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/REVIEW.md
- Create:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/preflight/identity-preflight.png

**Interfaces:**

- Consumes: approved design specification, current V2.2 generation skill,
  repository canonical portrait/full-body pair, and composition-pack README.
- Produces: a verified run workspace, exact preflight provenance, one
  diagnostic PNG, and either an explicit user identity approval or a stopped
  run.

- [ ] **Step 1: Re-read the execution authorities**

Read the complete current files:

    /home/takahiro/.agents/skills/generating-akari-v2-2-images/SKILL.md
    /home/takahiro/workspace/akari-design/docs/superpowers/specs/2026-08-12-akari-v2-2-milky-pastel-jumperskirt-24-design.md
    /home/takahiro/workspace/akari-design/local-reference-packs/akari-v2.2-cute-composition/README.md

Expected: the skill still permits the requested built-in new-scene path and
retains the one-call preflight, maximum-three-reference, and stopping rules.

- [ ] **Step 2: Verify the canonical pair and ignored workspace**

Run:

    test -r /home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp
    test -r /home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp
    identify -format '%f %wx%h %[colorspace]\n' /home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp /home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp
    mkdir -p /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/{preflight,uniform,chapters/{cream,mint,coral,lavender},contact-sheets}
    git check-ignore -v /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812

Expected: both authorities decode, the directory exists, and git check-ignore
reports an ignore rule. If either authority cannot be opened, stop without an
image call and report its absolute path.

- [ ] **Step 3: Initialize the ledgers and record baseline state**

Use apply_patch to create PROMPTS.md and REVIEW.md. Record the current
git status --short output, especially every pre-existing path under
akari-v2.2/accepted/, so the final audit can distinguish the run from unrelated
work. Add a preflight row with output path, exact prompt from this plan, and
the sole ordered reference path.

- [ ] **Step 4: Inspect the canonical pair at original detail**

Open both canonical files with view_image at original detail. Use the portrait
for the comparable-scale identity criteria and the full body only to confirm
the active same-location pair. Do not pass the full body to preflight.

- [ ] **Step 5: Generate and save the one allowed preflight**

Call built-in image_gen once with the exact Identity preflight prompt and:

    referenced_image_paths:
      - /home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp

Do not set num_last_images_to_include. Save the displayed result unchanged as
preflight/identity-preflight.png, using structural payload recovery only if the
built-in output has no accessible local PNG.

- [ ] **Step 6: Apply identity QA and stop for the user**

Run identify on the saved PNG, then inspect it and the canonical portrait at
original detail. Complete every Per-Image QA field. If identity is a clear
failure, mark the run STOPPED, show the reason, and make no retry. Otherwise
mark it user confirmation pending, show the diagnostic image, and wait for the
user to explicitly approve Akari's identity before Task 2.

### Task 2: Generate and Approve U-A as the First Production Candidate

**Files:**

- Create:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-a-classic-navy-r01.png
- Create only after an allowed retry:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-a-classic-navy-r02.png
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/PROMPTS.md
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/REVIEW.md

**Interfaces:**

- Consumes: explicit user approval of the preflight and the canonical pair.
- Produces: one user-approved U-A identity candidate, or a stopped run after
  no more than two U-A calls.

- [ ] **Step 1: Verify the preflight approval gate**

Record the user's exact identity-approval decision in REVIEW.md. Confirm that
the saved preflight is not being used as an input or continuity anchor.

- [ ] **Step 2: Reopen both canonical authorities**

Open the canonical portrait and full body at original detail immediately
before the call. No preflight or composition-pack image is passed.

- [ ] **Step 3: Generate U-A r01**

Call built-in image_gen once with the exact U-A prompt and exactly these
ordered referenced_image_paths:

    - /home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp
    - /home/takahiro/workspace/akari-design/akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp

Save unchanged as uniform/u-a-classic-navy-r01.png and write exact provenance
to PROMPTS.md.

- [ ] **Step 4: Inspect U-A and classify its first identity gate**

Apply the Per-Image QA Contract. If U-A r01 is not a clear identity failure,
present it for user identity review before retrying. If Codex finds a clear
identity failure, record the observed cause and choose exactly one of these
single-variable corrections:

- remove Image B while leaving the prompt unchanged when the low-detail
  full-body face appears to compete with Image A;
- shorten only the first identity paragraph to “Create the exact Akari V2.2
  identity shown in Image A without changing her facial design” when verbose
  identity wording appears to trigger redesign; or
- change only the head instruction from shallow three-quarter to the canonical
  portrait head angle while preserving the full-body comparison pose.

Reopen every retained reference, call image_gen once, and save the result as
uniform/u-a-classic-navy-r02.png. Never overwrite r01. If r02 is also a clear
identity failure, mark the run STOPPED and do not generate U-B or U-C.

- [ ] **Step 5: Present the surviving U-A for explicit identity approval**

Mark the surviving U-A user confirmation pending and show it at useful scale.
If the user rejects r01 for identity and the retry has not been used, record
the feedback, choose one applicable single-variable correction from Step 4,
reopen every retained reference, generate r02 once, run full QA, and present
r02. A user rejection of r02, or of r01 after the retry has already been used,
marks the run STOPPED. Wait for explicit user identity approval. U-A approval
at this gate permits matched studies but does not yet authorize using U-A as
the set anchor.

### Task 3: Generate U-B and U-C, Then Lock One Approved Uniform Anchor

**Files:**

- Create:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-b-milky-blue-retro-r01.png
- Create:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-c-tailored-deep-teal-r01.png
- Create:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/uniform-contact-sheet.jpg
- Create:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/selection.md
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/PROMPTS.md
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/REVIEW.md

**Interfaces:**

- Consumes: explicit U-A identity approval and the canonical pair.
- Produces: three comparable studies plus one user-selected, explicitly
  identity-and-wardrobe-approved local anchor path and its exact uniform block.

- [ ] **Step 1: Generate and inspect U-B independently**

Reopen the canonical portrait and full body. Call image_gen once with the exact
U-B prompt and the same ordered canonical pair used for U-A r01. Save unchanged
as uniform/u-b-milky-blue-retro-r01.png and apply the full QA contract. If it
is a clear identity failure, mark STOPPED and do not generate U-C.

- [ ] **Step 2: Generate and inspect U-C independently**

Reopen the canonical portrait and full body. Call image_gen once with the exact
U-C prompt and the same ordered canonical pair. Save unchanged as
uniform/u-c-tailored-deep-teal-r01.png and apply the full QA contract. A clear
identity failure marks STOPPED; do not continue to scene generation.

- [ ] **Step 3: Build the matched three-study contact sheet**

Use the surviving U-A file, then U-B, then U-C:

    if test -r /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-a-classic-navy-r02.png; then magick montage /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-a-classic-navy-r02.png /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-b-milky-blue-retro-r01.png /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-c-tailored-deep-teal-r01.png -thumbnail '306x459>' -background '#fffaf5' -fill '#4c4056' -pointsize 22 -set label '%t' -geometry '306x459+12+30' -tile 3x1 /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/uniform-contact-sheet.jpg; else magick montage /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-a-classic-navy-r01.png /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-b-milky-blue-retro-r01.png /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/u-c-tailored-deep-teal-r01.png -thumbnail '306x459>' -background '#fffaf5' -fill '#4c4056' -pointsize 22 -set label '%t' -geometry '306x459+12+30' -tile 3x1 /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/uniform/uniform-contact-sheet.jpg; fi

Expected: one row in U-A, U-B, U-C order with readable file labels.

- [ ] **Step 4: Obtain selection and separate anchor approval**

Show the contact sheet and individual studies. Ask the user to choose U-A,
U-B, or U-C and explicitly confirm that the exact saved image is approved for
both Akari identity and wardrobe/set continuity. A mere style preference does
not unlock scene generation. If the user rejects U-B or U-C for identity,
mark the built-in new-scene path STOPPED and do not start a chapter, even if
the user prefers a different study.

- [ ] **Step 5: Write the immutable runtime selection**

Use apply_patch to create selection.md with:

- selected ID and absolute saved image path;
- the user's exact approval wording;
- identity approved: yes;
- wardrobe continuity approved: yes;
- exactly one corresponding Selected-uniform block from this plan;
- statement that the image is a run-local anchor, not a canonical promotion.

Open the selected saved file and both canonical authorities at original detail
once more. Task 4 is blocked unless all three local paths are readable.

### Task 4: Generate and Review the Cream Chapter

**Files:**

- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/cream/c01-collar-adjustment.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/cream/c02-mug-offer.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/cream/c03-sun-shade-palm.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/cream/c04-sleeve-thread.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/cream/c05-door-push.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/cream/c06-corridor-turn.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/cream.jpg
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/PROMPTS.md
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/REVIEW.md

**Interfaces:**

- Consumes: readable canonical pair, readable approved uniform anchor, selected
  U-A/U-B/U-C block, Cream chapter block, and C01-C06 catalog rows.
- Produces: six sequential Cream PNGs and one user-reviewed contact sheet.

- [ ] **Step 1: Generate C01-C05 sequentially with two references**

For each ID in C01, C02, C03, C04, C05 order: open the exact local-pack image
named in its catalog row for camera analysis, then reopen the canonical
portrait and approved uniform anchor. Assemble the prompt as close/half role
block + shared identity block + selected uniform block + Cream block + the
exact catalog scene block + shared rendering block. Call image_gen once with
portrait then anchor in referenced_image_paths, save to the catalog output
path, and complete QA before moving to the next ID. Never pass the local-pack
image.

- [ ] **Step 2: Generate C06 with three references**

Open 05-cheer-motion-foreshortening.jpg for camera analysis, then reopen the
canonical portrait, canonical full body, and approved uniform anchor. Assemble
the prompt with the full-body role block and C06 catalog row. Call once with
portrait, full body, then anchor; save unchanged as c06-corridor-turn.png and
complete QA.

- [ ] **Step 3: Enforce the stop rule after every result**

If any Cream image is a clear identity failure, write STOPPED with the exact
ID, leave all remaining images ungenerated, and do not use the failed image in
any later call. If a hand, prop, uniform, space, or artifact issue occurs
without clear identity failure, mark it held for user review and continue only
under the approved one-call-per-scene slate.

- [ ] **Step 4: Build and inspect the Cream contact sheet**

Run:

    magick montage /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/cream/{c01-collar-adjustment,c02-mug-offer,c03-sun-shade-palm,c04-sleeve-thread,c05-door-push,c06-corridor-turn}.png -thumbnail '256x384>' -background '#fffaf5' -fill '#4c4056' -pointsize 20 -set label '%t' -geometry '256x384+10+28' -tile 3x2 /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/cream.jpg

Open the sheet and all six originals. Confirm three close, two half, one full;
all required camera devices; expression/gaze variety; selected uniform
continuity; and luminous Cream color.

- [ ] **Step 5: Present the six-image checkpoint**

Show cream.jpg plus concise ID-level holds. Mark every surviving image user
confirmation pending unless the user explicitly approves it. Wait for user
authorization before Task 5. If the user rejects any Cream image for identity,
mark the built-in new-scene path STOPPED. Any requested retry or alternate
path requires a new decision and is outside this automatic sequence.

### Task 5: Generate and Review the Mint Chapter

**Files:**

- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/mint/m01-strawberry-offer.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/mint/m02-hat-brim-peek.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/mint/m03-pinwheel-breeze.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/mint/m04-bag-strap-pull.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/mint/m05-sleeve-roll.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/mint/m06-curb-step.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/mint.jpg
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/PROMPTS.md
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/REVIEW.md

**Interfaces:**

- Consumes: user authorization after Cream, canonical pair, approved uniform
  anchor, selected block, Mint block, and M01-M06 catalog rows.
- Produces: six sequential Mint PNGs and one user-reviewed contact sheet.

- [ ] **Step 1: Generate M01-M05 sequentially with two references**

For M01 through M05 in order, use the same exact per-call procedure as the
global contract: inspect only the row's local-pack image for camera grammar,
reopen portrait and approved anchor, concatenate the close/half role block,
identity block, selected uniform block, Mint block, exact row block, and
rendering block, then call once and QA before advancing.

- [ ] **Step 2: Generate M06 with three references**

Inspect 05-cheer-motion-foreshortening.jpg, reopen portrait, full body, and
approved anchor, assemble the full-body prompt with M06, call once, save as
m06-curb-step.png, and complete QA.

- [ ] **Step 3: Apply the identity and technical stop classifications**

A clear identity failure stops all ungenerated work with no retry. Record a
non-identity issue as held for user review and never edit from the unapproved
candidate without a new explicit decision.

- [ ] **Step 4: Build and inspect the Mint contact sheet**

Run:

    magick montage /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/mint/{m01-strawberry-offer,m02-hat-brim-peek,m03-pinwheel-breeze,m04-bag-strap-pull,m05-sleeve-roll,m06-curb-step}.png -thumbnail '256x384>' -background '#f5fffb' -fill '#36544f' -pointsize 20 -set label '%t' -geometry '256x384+10+28' -tile 3x2 /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/mint.jpg

Open the sheet and originals. Confirm the 3/2/1 framing mix, camera devices,
gaze/expression change from Cream, uniform continuity, and clear luminous Mint.

- [ ] **Step 5: Present the six-image checkpoint**

Show mint.jpg and concise ID-level holds, keep surviving images user
confirmation pending, and wait for authorization before Task 6. If the user
rejects any Mint image for identity, mark the built-in new-scene path STOPPED.

### Task 6: Generate and Review the Coral Chapter

**Files:**

- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/coral/r01-sorbet-spoon.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/coral/r02-single-flower.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/coral/r03-scarf-catch.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/coral/r04-baguette-carry.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/coral/r05-cardigan-turn.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/coral/r06-stair-turn.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/coral.jpg
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/PROMPTS.md
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/REVIEW.md

**Interfaces:**

- Consumes: user authorization after Mint, canonical pair, approved uniform
  anchor, selected block, Coral block, and R01-R06 catalog rows.
- Produces: six sequential Coral PNGs and one user-reviewed contact sheet.

- [ ] **Step 1: Generate R01-R05 sequentially with two references**

For R01 through R05 in order, inspect the catalog's one local-pack image,
reopen portrait and approved anchor, assemble the exact close/half prompt with
the Coral layer/palette block and row-specific scene, call once, save to its
declared path, and finish QA before the next call.

- [ ] **Step 2: Generate R06 with three references**

Inspect 05-cheer-motion-foreshortening.jpg, reopen portrait, full body, and
approved anchor, assemble the full-body prompt with R06, call once, save as
r06-stair-turn.png, and complete QA.

- [ ] **Step 3: Enforce stop classifications**

Stop permanently on a clear identity failure and leave all later IDs absent.
Hold non-identity technical issues for user review without automatic repair.

- [ ] **Step 4: Build and inspect the Coral contact sheet**

Run:

    magick montage /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/coral/{r01-sorbet-spoon,r02-single-flower,r03-scarf-catch,r04-baguette-carry,r05-cardigan-turn,r06-stair-turn}.png -thumbnail '256x384>' -background '#fff7f4' -fill '#634541' -pointsize 20 -set label '%t' -geometry '256x384+10+28' -tile 3x2 /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/coral.jpg

Open the sheet and originals. Confirm the 3/2/1 mix, selected uniform visible
under the open cardigan, expression and diagonal variety, and luminous Coral.

- [ ] **Step 5: Present the six-image checkpoint**

Show coral.jpg with ID-level holds, keep survivors user confirmation pending,
and wait for authorization before Task 7. If the user rejects any Coral image
for identity, mark the built-in new-scene path STOPPED.

### Task 7: Generate and Review the Lavender Chapter

**Files:**

- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/lavender/l01-round-light.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/lavender/l02-cuff-button.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/lavender/l03-desk-arm-rest.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/lavender/l04-yawn-stretch.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/lavender/l05-book-close.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/lavender/l06-hallway-light-turn.png
- Create: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/lavender.jpg
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/PROMPTS.md
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/REVIEW.md

**Interfaces:**

- Consumes: user authorization after Coral, canonical pair, approved uniform
  anchor, selected block, Lavender block, and L01-L06 catalog rows.
- Produces: six sequential Lavender PNGs and one user-reviewed contact sheet.

- [ ] **Step 1: Generate L01-L05 sequentially with two references**

For L01 through L05 in order, inspect the row's one local-pack image, reopen
portrait and approved anchor, assemble the exact close/half prompt with the
Lavender block and row scene, call once, save to the declared path, and finish
QA before the next call.

- [ ] **Step 2: Generate L06 with three references**

Inspect 05-cheer-motion-foreshortening.jpg, reopen portrait, full body, and
approved anchor, assemble the full-body prompt with L06, call once, save as
l06-hallway-light-turn.png, and complete QA.

- [ ] **Step 3: Enforce stop classifications**

Stop permanently on a clear identity failure. Hold any other technical issue
for explicit user review and do not edit or anchor from that unapproved image.

- [ ] **Step 4: Build and inspect the Lavender contact sheet**

Run:

    magick montage /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/lavender/{l01-round-light,l02-cuff-button,l03-desk-arm-rest,l04-yawn-stretch,l05-book-close,l06-hallway-light-turn}.png -thumbnail '256x384>' -background '#faf7ff' -fill '#4c4666' -pointsize 20 -set label '%t' -geometry '256x384+10+28' -tile 3x2 /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/lavender.jpg

Open the sheet and originals. Confirm the 3/2/1 mix, readable knit-over-uniform
construction, restrained evening depth, expression variety, and no
overexposure from either round-light scene.

- [ ] **Step 5: Present the six-image checkpoint**

Show lavender.jpg with ID-level holds and record the user's chapter review.
Do not describe any surviving image as accepted unless the user explicitly
accepts it. If the user rejects any Lavender image for identity, mark the
built-in new-scene path STOPPED and do not claim a successful complete set.

### Task 8: Audit the Complete Candidate Set and Present Final Review

**Files:**

- Create:
  tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/all-24.jpg
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/PROMPTS.md
- Modify: tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/REVIEW.md

**Interfaces:**

- Consumes: all four completed six-image chapters, prompt provenance, QA
  records, and chapter reviews.
- Produces: an evidence-backed 24-image review package with no promotion or
  tracked generated artifacts.

- [ ] **Step 1: Verify exact file count, decoding, dimensions, and colorspace**

Run:

    rg --files /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters | rg '/[cmrl][0-9]{2}-.*\.png$'
    identify -format '%f %wx%h %[colorspace]\n' /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/{cream,mint,coral,lavender}/*.png

Expected: exactly twenty-four readable portrait PNGs, six in each chapter,
targeted at 1024 x 1536 or larger. Report any dimension variance; do not resize
or crop a final silently.

- [ ] **Step 2: Re-audit set-level distribution**

Open all four chapter sheets and spot-check every original at original detail.
Record evidence for exactly twelve close, eight half, and four full views;
three/two/one per chapter; at least two required camera devices per image; no
centered front-facing standing portrait; no consecutive repeated
expression/gaze silhouette; and one recognizable selected uniform throughout.

- [ ] **Step 3: Build the ordered all-24 contact sheet**

Run one montage command with the twenty-four files explicitly ordered C01-C06,
M01-M06, R01-R06, L01-L06. Use:

    magick montage /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/cream/{c01-collar-adjustment,c02-mug-offer,c03-sun-shade-palm,c04-sleeve-thread,c05-door-push,c06-corridor-turn}.png /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/mint/{m01-strawberry-offer,m02-hat-brim-peek,m03-pinwheel-breeze,m04-bag-strap-pull,m05-sleeve-roll,m06-curb-step}.png /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/coral/{r01-sorbet-spoon,r02-single-flower,r03-scarf-catch,r04-baguette-carry,r05-cardigan-turn,r06-stair-turn}.png /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/chapters/lavender/{l01-round-light,l02-cuff-button,l03-desk-arm-rest,l04-yawn-stretch,l05-book-close,l06-hallway-light-turn}.png -thumbnail '204x306>' -background '#fffaf8' -fill '#4c4056' -pointsize 16 -set label '%t' -geometry '204x306+8+24' -tile 6x4 /home/takahiro/workspace/akari-design/tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/contact-sheets/all-24.jpg

Expected: four chapter rows in Cream, Mint, Coral, Lavender order.

- [ ] **Step 4: Reconcile generation provenance and stop state**

PROMPTS.md must contain one preflight, three uniform studies, and twenty-four
scene entries, plus one extra U-A entry only if its allowed retry was used.
REVIEW.md must contain every QA field, every user gate, all held technical
issues, and no claim that user-confirmation-pending images are accepted.

- [ ] **Step 5: Verify repository boundaries**

Run:

    git status --short
    git diff --check
    bash -lc 'npm run lint:md'

Compare the final status with the baseline recorded in Task 1. Expected: no
new tracked or untracked generated file outside the ignored run root, no
change caused by this run under akari-v2.2/accepted/, Markdown lint passes,
and unrelated pre-existing work remains untouched.

- [ ] **Step 6: Present final review without promotion**

Show all-24.jpg and the four chapter sheets with concise ID-level findings.
State the exact count and any held concern. Every image remains user
confirmation pending unless explicitly accepted. Do not copy, stage, commit,
or promote any generated image until the user gives a separate preservation
request naming the accepted scope.

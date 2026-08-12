# Akari V2.2 Milky-Pastel Jumperskirt 24-Scene Design

Date: 2026-08-12
Status: approved in conversation and written-spec review on 2026-08-12

## Goal

Create a separate set of twenty-four Akari V2.2 portrait illustrations that
combine luminous milky-pastel color with aggressive, character-first camera
placement. The set explores one selected jumperskirt uniform through close
wide-angle framing, diagonals, foreground foreshortening, and bold crops while
preserving the canonical adult Akari identity.

This is a new series. It does not replace, recolor, edit, promote, or otherwise
change the existing D40-D80 candidate batch.

## Deliverables and boundaries

- The final candidate set contains exactly twenty-four 2:3 portrait images,
  targeted at 1024 x 1536 or larger.
- One identity preflight and three uniform-comparison images are generated
  before the twenty-four scenes and do not count toward the final set.
- A normal successful run therefore uses at least twenty-eight independent
  image-generation calls: one preflight, three uniform studies, and twenty-four
  scene calls.
- All preflight, study, scene, prompt, review, and contact-sheet artifacts stay
  under the ignored working directory
  `tmp/akari-v2.2-milky-pastel-jumperskirt-24-20260812/`.
- No generated image enters `akari-v2.2/accepted/` or Git without a later,
  explicit user acceptance and preservation request.
- The set depicts human Akari only. It contains no cat ears, animal traits,
  fantasy anatomy, readable text, logos, watermarks, speech balloons, comic
  punctuation, decorative symbol fields, poster borders, or sticker outlines.
- Release PDFs, manifest changes, package refactors, and changes to the existing
  D40-D80 run are out of scope.

## Canonical identity contract

The repository's accepted V2.2 pair remains authoritative:

1. `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp` is the
   sole authority for face identity, facial geometry, eyes, brows, cheeks,
   mouth, apparent adult age, warm chestnut hair, bangs, low side ponytail,
   exactly one blue capsule hairpin on canvas-right, and close rendering.
2. `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-fullbody.webp` controls
   body proportions, balance, laterality, connected anatomy, and full-figure
   construction. It is not a face authority.
3. After explicit user approval, the selected uniform-study image may be used
   as a wardrobe and set-continuity anchor. It never overrides either canonical
   authority.

Akari remains the same 25-year-old adult. The jumperskirt uniform is an
intentional wardrobe study and must not re-age her, redesign her face, shorten
her proportions, or introduce childlike styling.

The canonical chestnut hair, amber-brown eyes, blue hairpin, and blue ponytail
tie keep their accepted color and contrast. The pastel treatment applies to
light, clothing, props, and background surfaces; it must not wash out the
identity features or overexpose the skin.

## Composition-reference contract

Before a scene is generated, inspect the one most relevant image from
`local-reference-packs/akari-v2.2-cute-composition/` and translate only its
camera grammar into text:

- close camera placement;
- an off-center face;
- strong diagonal body flow;
- gentle wide-angle foreshortening;
- one enlarged hand, sleeve, or ordinary prop in the foreground;
- a bold but coherent crop; and
- a few broad, clean color masses.

The pack contains other characters, so its images are not passed to the image
generator. Do not copy their character identity, face, hair, clothing, animal
traits, mascots, gestures as a literal pose trace, text, stars, geometric
decoration, borders, or sticker treatment.

Every final scene must use at least two of these five camera devices:

1. bold crop;
2. strong diagonal;
3. enlarged foreground hand, sleeve, or single prop;
4. wide-angle foreshortening; or
5. low-angle or high-angle placement.

A conventional centered, front-facing standing portrait is not allowed in the
twenty-four-scene set.

## Character-first rendering budget

The image should spend visual complexity on Akari's face, hair, hands, connected
body, and uniform construction.

- Use at most one main prop per scene.
- Show only one or two spatial cues, such as a floor, window, door, desk, or
  stair edge.
- Keep the remainder as broad warm-white and pastel surfaces with natural
  light falloff.
- Do not place the face behind glass, mirrors, refraction, water, dense cloth,
  or other effects that compete with identity rendering.
- Do not use complex splashes, transparent umbrellas, mirrored faces, detailed
  crowds, dense rooms, or elaborate graphic backgrounds.
- Generate dynamism through Akari's placement, body twist, connected limbs,
  foreground scale, and crop rather than environmental detail.

## Milky-pastel system

The palette is luminous rather than gray, chalky, or uniformly desaturated.
Warm cream is the shared neutral. Four six-image chapters rotate the accents:

- **Cream:** warm cream, shell peach, butter yellow, and powder blue;
- **Mint:** milk blue, clear mint, pale aqua, and soft young green;
- **Coral:** soft coral, apricot, rose milk, and light lilac;
- **Lavender:** lavender, periwinkle, moon white, and restrained blue-green.

The chapters are color-and-mood groups, not a literal morning-to-night story.
Pastel depth comes from large clothing and background planes, soft natural
light, hair movement, and simple physical props. Decorative stars, icons, and
floating graphic marks do not supply the color rhythm.

## Uniform study

Generate the three wardrobe candidates under matched conditions: the same
simple warm-cream background, neutral light, shallow three-quarter full-body
pose, both eyes visible, and no handheld prop. This comparison deliberately
uses a quieter camera than the final scenes so silhouette, neckline, waist,
hem, and pleat structure are easy to judge.

### U-A — Classic navy

- white short-sleeve blouse;
- deep navy square-neck jumperskirt;
- slightly high waist seam;
- broad box pleats;
- below-knee hem;
- simple charcoal socks and brown loafers.

This is the recommended option because the dark silhouette remains clear
against milky backgrounds and supports the widest range of dynamic crops.

### U-B — Milky-blue retro

- cream blouse with a restrained rounded collar;
- clean milk-blue V-neck jumperskirt without gray or chalky desaturation;
- one centered inverted pleat;
- upper-calf hem;
- simple gray-blue socks and brown loafers.

This option has the strongest pastel unity but may read more like an ordinary
pinafore dress than a school-uniform study.

### U-C — Tailored deep teal

- ivory blouse with a simple collar;
- deep blue-green shallow-U-neck jumperskirt;
- restrained vertical seam construction;
- modest A-line silhouette;
- below-knee hem;
- simple dark socks and loafers.

This option has the most adult impression and freshest color, but it is less
immediately traditional than U-A.

All three are plain and modest. They contain no crest, badge, lettering,
school name, sailor collar, blazer conversion, tie clutter, mini hem, cleavage,
or fashion-heavy hardware.

After the user selects one study, its jumperskirt structure and main color stay
fixed through all twenty-four scenes. Chapter variation may adjust blouse
sleeves and add one light cardigan: no outer layer in Cream, the basic blouse
in Mint, a soft-coral cardigan in Coral, and a pale-lavender knit layer in
Lavender. These layers must not obscure the selected neckline, waist, or skirt
silhouette in every image.

## Framing allocation

Each chapter contains the same framing mix:

- three face-first extreme or close views;
- two wide-angle half-body views; and
- one low-angle or high-angle full-body view.

Across the complete set this yields twelve close views, eight half-body views,
and four full-body views. Face position, gaze target, mouth shape, hand entry,
and diagonal direction must vary within each chapter. Do not repeat the same
open-mouth smile, direct gaze, or silhouette for consecutive scenes.

## Twenty-four-scene slate

### Cream chapter

| ID | Scene | Frame and camera design | Expression |
| --- | --- | --- | --- |
| C01 | Collar adjustment | Extreme close view; one hand and the blouse collar enlarge across the lower foreground while the face sits on the opposite diagonal | composed small smile |
| C02 | Mug offer | A plain cream mug fills one lower corner while Akari leans in from the opposite upper corner | warm open-eyed welcome |
| C03 | Sun-shade palm | One palm approaches the top of the lens and the off-center face appears beside it in soft backlight; both eyes remain readable | lightly dazzled smile |
| C04 | Sleeve thread | Half-body wide angle; one blouse sleeve comes toward the camera while the torso twists away | focused, softly amused |
| C05 | Door push | The pushing hand and a single door edge dominate the foreground; Akari looks back over her shoulder | small curious look |
| C06 | Corridor turn | Floor-level full-body view; a coherent near foot, turning body, and face form one rising diagonal as she rounds a plain corridor corner | bright relaxed smile |

### Mint chapter

| ID | Scene | Frame and camera design | Expression |
| --- | --- | --- | --- |
| M01 | Strawberry offer | One strawberry is held close to the lens while Akari's face approaches from the opposite side | playful anticipation |
| M02 | Hat-brim peek | The broad brim of one plain pale hat cuts diagonally across the foreground and the face peeks from below it | shy closed-mouth smile |
| M03 | Pinwheel breeze | One unlettered pastel pinwheel occupies the near foreground; wind moves the hair behind it without covering the face | small open-eyed surprise |
| M04 | Bag-strap pull | Half-body wide angle; one plain shoulder-bag strap and hand pull toward the lens while the torso counter-rotates | ready-to-go focus |
| M05 | Sleeve roll | A foreshortened elbow enters the foreground and leads through the rolling hand to a side-turned face | calm concentration |
| M06 | Curb step | Low full-body camera; one coherent stepping foot approaches the foreground while the rest of the body recedes along a clean diagonal | carefree smile |

### Coral chapter

| ID | Scene | Frame and camera design | Expression |
| --- | --- | --- | --- |
| R01 | Sorbet spoon | One plain spoon with a small pastel sorbet scoop enlarges in the foreground; the face waits on the opposite diagonal | delighted anticipation |
| R02 | Single flower | One pale flower comes forward from beside the cheek while the face is cropped off-center | soft attentive smile |
| R03 | Scarf catch | One scarf end and the catching hand sweep through the foreground in the opposite direction from the face and shoulders | surprised grin |
| R04 | Baguette carry | Half-body wide angle; one baguette in an unlabelled paper sleeve crosses the lower frame as Akari leans over it | pleased side glance |
| R05 | Cardigan turn | One cardigan sleeve creates a simple foreground arc while the upper body rotates in the other direction | amused half-turn |
| R06 | Stair turn | Low full-body view; one descending step, the torso, and a backward glance create a readable S-curve | warm backward smile |

### Lavender chapter

| ID | Scene | Frame and camera design | Expression |
| --- | --- | --- | --- |
| L01 | Round light | One small opaque milky round light sits near the cheek, forming a diagonal pair with the face against a minimal dark-lavender field | quiet contentment |
| L02 | Cuff button | Extreme close view; the fastening hand and blouse cuff occupy the near foreground while the unobstructed face stays behind them | gentle concentration |
| L03 | Desk-arm rest | Folded forearms enlarge across the lower foreground and Akari's tilted face rests just above them | tired but warm gaze |
| L04 | Yawn stretch | Half-body wide angle; both sleeved arms rise on opposing diagonals and frame rather than cover the face | natural sleepy yawn |
| L05 | Book close | Akari leans across a minimal desk and closes one blank, unlettered book with a foreground palm; hand, book, and face form a triangle | calm finished-for-now look |
| L06 | Hallway light turn | Floor-level full-body view; feet, one opaque round light, and a turning face align along a long diagonal in a simple corridor | gentle backward glance |

## Expression and identity distribution

- Keep both eyes readable in most scenes and in all identity-critical early
  candidates.
- Distribute bright smiles, small closed-mouth smiles, concentration, mild
  surprise, sleepy warmth, and a few transitional expressions.
- Do not use repeated winks, repeated closed eyes, generic symmetrical smiles,
  long horizontally narrowed eyes, tiny irises, or an adolescent face design.
- A challenging expression never excuses facial-geometry drift. Face identity
  is reviewed before costume, pose, background, or prop quality.

## Generation workflow

### Phase 0 — identity preflight

1. Open the accepted canonical portrait at original detail.
2. Generate one diagnostic image using the portrait alone: close face, matching
   head angle and gaze, bright expression, white T-shirt, simple background,
   no prop, and no main action.
3. If Codex finds a clear identity mismatch, stop this built-in new-scene path.
4. Otherwise present it as `user confirmation pending`. Do not generate a
   uniform study until the user explicitly approves identity.
5. The preflight receives no retry.

### Phase 1 — matched uniform comparison

1. Open the canonical portrait and full-body authorities immediately before
   each call.
2. Generate U-A first using only the canonical pair. It is the first production
   candidate and may receive at most one identity-related retry that changes
   one suspected variable.
3. Present U-A for explicit identity approval. If approved, generate U-B and
   U-C independently from the same canonical pair and matched comparison
   conditions.
4. Inspect every study for face identity first, then adult proportion,
   laterality, neckline, waist, pleats, hem, hands, feet, and artifacts.
5. If a later study clearly fails identity, stop the ungenerated remainder in
   accordance with the V2.2 skill; do not use or summarize the failed face as
   an anchor.
6. Ask the user to choose one uniform and separately approve that saved image
   as the wardrobe and set-continuity anchor.

### Phase 2 — four six-scene waves

Generate the final scenes sequentially as Cream, Mint, Coral, and Lavender
waves. Each scene uses one image-generation call.

- Close and half-body scenes normally use the canonical portrait plus the
  user-approved uniform anchor.
- Full-body scenes add the canonical full-body authority, reaching the maximum
  of three inputs.
- Omit the full-body authority from face-first scenes unless its proportion or
  laterality information is genuinely necessary.
- Never mix `referenced_image_paths` with `num_last_images_to_include`.
- Never use an unapproved or identity-failed candidate as an input, editing
  target, continuity anchor, compositing source, or textual face description.
- Inspect each result before making the next call. A clear identity failure
  stops all ungenerated scenes.
- Present a six-image contact sheet after each completed chapter. The user
  selected chapter-sized review rather than one-image or all-at-once review.

## Prompt structure

Each scene prompt has five blocks:

1. input roles and authority boundaries;
2. concise canonical identity preservation;
3. selected uniform structure and current chapter layer;
4. one action plus exact crop, camera position, foreground element, body flow,
   gaze, and expression; and
5. clean V2.2 rendering, minimal physical background, and the chapter palette.

Negative instructions stay limited to identity and scene-critical failures:
face redesign, narrowed eyes or changed irises, age drift, changed ponytail or
hairpin side, extra hairpins, broken hand or limb continuity, copied reference
identity, readable text, and graphic-decoration fields.

## Review and stopping rules

Review every candidate at original detail in this order:

1. face identity against the canonical portrait at comparable display scale;
2. apparent adult age, hair, ponytail, hairpin count and side, and eye design;
3. connected hands, arms, legs, body balance, and foreshortening;
4. selected uniform neckline, waist, pleats, hem, and chapter layer;
5. hand-to-prop contact and foreground-to-background separation;
6. minimal but coherent floor, furniture, door, desk, or stair relationships;
7. milky-pastel clarity without chalky grayness or washed-out identity;
8. text, logos, watermarks, copied graphic elements, and image artifacts.

Codex may only classify identity as `clear failure` or `user confirmation
pending`; it does not make the final identity acceptance. A clear preflight
failure stops immediately. The first production study may receive one
single-variable retry. A second failure or any later clear identity failure
stops the built-in new-scene path and leaves all remaining images ungenerated.

Non-identity technical failures remain held for user review. They are not
silently edited from an unapproved candidate. Any later retry or alternate
path requires a new explicit decision consistent with the V2.2 skill.

## Success criteria

- The user has explicitly approved the identity preflight.
- The user has selected one of U-A, U-B, and U-C and explicitly approved its
  saved image for identity and wardrobe continuity.
- Exactly twenty-four readable 2:3 scene candidates exist, arranged as four
  six-image chapters with the 12/8/4 framing allocation.
- Every image preserves adult Akari's canonical face, hair, eyes, single blue
  hairpin, low side ponytail, and body balance.
- Every image uses at least two required camera devices and avoids a generic
  centered standing portrait.
- The selected jumperskirt structure remains recognizable in every scene.
- Backgrounds remain minimal and physically coherent, with no copied character
  identity or graphic decoration.
- Every surviving candidate is still marked for user confirmation unless the
  user has explicitly accepted it.
- No unapproved generated image is promoted, tracked, or used as a later
  anchor.

# Akari v1.5 Kawaii 1000 B001 Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Define, generate, durably save, validate, and review the first fifty production images, B001, without changing the gallery application or generating any B002 image.

**Architecture:** A tracked, fully specified request matrix is compiled into fifty deterministic prompts and one pending production manifest. Built-in `image_gen` is called independently once per intended image; small Python tools validate and install each PNG into the external data root, derive its WebP thumbnail, and reconcile per-image receipts into the batch manifest and novelty ledger so interruption and retry are safe. The existing Node gallery performs review; after all fifty B001 reviews are complete, their summary becomes the input to a separate B002 implementation plan.

**Tech Stack:** Built-in `image_gen`, Codex `view_image`, Python 3.11+, Pillow, JSON, `unittest`, Node.js 26 ESM manifest validation, existing plain-JavaScript review gallery, `systemd --user`, Tailscale.

## Global Constraints

- Canonical design:
  `docs/superpowers/specs/2026-07-29-akari-v1-5-kawaii-1000-generation-gallery-design.md`.
- Foundation plan:
  `docs/superpowers/plans/2026-07-29-akari-v1-5-kawaii-1000-gallery-foundation.md`.
- This plan generates B001 only: exactly fifty technically valid PNG files,
  IDs `B001-001` through `B001-050`.
- Use one independent built-in `image_gen` call per intended image. Never use
  one broad call, an `n` variants request, a browser generation button, or a
  CLI image-generation fallback.
- Before every `image_gen` call, open with `view_image` the current selected
  v1.5 B3 candidate, the permanent v1.4 G2 rendering authority, and every
  conditional reference named by that matrix row. The B3 image satisfies both
  “current selected candidate” and permanent identity/body authority; do not
  send a byte-identical second B3 copy.
- Pass the same opened paths through `referenced_image_paths` in the built-in
  call. Two references are the minimum; four are the maximum.
- Every prompt is printed by the tested compiler and passed verbatim to
  `image_gen`. Do not rewrite it interactively.
- Generated PNGs, thumbnails, receipts, attempts, manifests, reviews, staging
  files, and novelty state live only under
  `/home/takahiro/workspace/akari_generated/v1.5-1000/`.
- Never commit generated images or external state. Never overwrite an existing
  final PNG, thumbnail, receipt, manifest with a different matrix fingerprint,
  or reference snapshot.
- A technically valid, byte-distinct PNG counts even when its later human
  review is `reject`. Do not silently regenerate a visually weak but
  technically valid image.
- A missing result, invalid PNG signature, damaged PNG, failed immutable copy,
  or byte-identical duplicate does not count. Record the failure, then retry
  the same ID with the same compiled intent.
- When a built-in result is visible but no local PNG is available, structurally
  parse the current Codex rollout for `type == "image_generation_call"` and a
  base64 `result` beginning with `iVBOR`; require decoded signature
  `89504e470d0a1a0a` before recovery.
- The production manifest has exactly five entries per lane, ten
  `textureFocus: true` entries, five `subculture: true` entries, thirty-five
  solo entries, ten viewer-POV/two-person entries, five group entries, forty
  `action-reaction` entries, and ten `quiet-posed` entries.
- The first three lanes provide B001’s fifteen uniform images. Across the
  twenty-batch project those lanes reach the approved 300-image uniform total.
- B001 texture allocation is five `over-knee-socks`, two
  `tights-stockings`, one `knee-high-socks`, one `crew-ankle-socks`, and one
  `bare-contact`.
- The five `subculture-wildcard` rows are the only B001 rows with
  `subculture: true`.
- All visible skin follows the approved soft semi-realistic, warm
  hand-painted treatment. Texture rows keep Akari’s full outfit, expression,
  and gesture as the subject; no isolated leg crop is allowed.
- The permanent B3 identity/body and G2 rendering/skin references are present
  in every manifest entry. Conditional references supplement, never replace,
  those authorities.
- Do not use an earlier B001 output or any generated sibling as an identity
  reference.
- Do not build a new application, edit gallery behavior, trigger generation
  from the browser, produce a PDF, or run PDF/OCR release gates.
- Run named gates serially on the 3-core, 2 GiB host.

## Live Handoff Facts

- Data root:
  `/home/takahiro/workspace/akari_generated/v1.5-1000`.
- Gallery URL: `http://100.125.117.75:8787`.
- The Task 10 worktree service is active, Tailscale-only, and must be
  reinstalled from canonical `/home/takahiro/workspace/akari-design` after
  the foundation branch is integrated.
- B000 contains 50/50 reviews. A live identical write to B000-001 returned
  HTTP 200, advanced revision 1 to 2, and survived service restart.
- B000’s live API and both PNG/WebP media routes pass. Chrome desktop/mobile
  fixtures pass. Actual live desktop/mobile visual appearance remains a manual
  check because this CLI surface exposed no in-app Browser tab.
- Reference manifest:
  `/home/takahiro/workspace/akari_generated/v1.5-1000/references/manifest.json`.
- Permanent identity/body snapshot:
  `references/akari-v1.5-b3-body-balance.png`,
  SHA-256
  `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`.
- Permanent rendering/skin snapshot:
  `references/akari-v1.4-g2-balanced-lines.png`,
  SHA-256
  `6757e601d2cfd158c970ab701a876981ace837e669c313dec6d25c0c539ff4d6`.
- Seated continuity snapshot:
  `references/akari-v1.4-i2-seated.png`,
  SHA-256
  `0871f903bbbf408174285a8f2c7404aaec51449de5fe32202e51512a8a5b05d0`.
- Hand/object continuity snapshot:
  `references/akari-v1.4-j1-action.png`,
  SHA-256
  `130642eb7a2db7d29f26fb7101a1f0049fe4214c839d8a8ab5520d756b7f276a`.
- Hosiery-pressure snapshot:
  `references/neesocks-pressure-study.jpeg`,
  SHA-256
  `d8185d8f453dbca9a22bbbae676d8f1c9634b4f2f8a2fecd2a8e675a990047d7`.

## File Structure

Tracked source and tests created by Tasks 1 through 3:

```text
akari-v1.5/generation/
└── b001-request-matrix.json

scripts/
├── akari_v1_5_b001_contract.py
├── akari_v1_5_b001_state.py
├── manage_akari_v1_5_b001.py
└── recover_akari_imagegen_payload.py

tests/
├── test_akari_v1_5_b001_contract.py
├── test_akari_v1_5_b001_state.py
└── test_recover_akari_imagegen_payload.py
```

External runtime layout created by Task 4:

```text
/home/takahiro/workspace/akari_generated/v1.5-1000/
├── references/
├── state/
│   ├── novelty-ledger.json
│   └── prior-coverage.json
└── batches/B001/
    ├── attempts/
    ├── images/
    ├── receipts/
    ├── staging/
    ├── thumbs/
    ├── manifest.json
    └── reviews.json
```

Responsibility boundaries:

- `b001-request-matrix.json` owns the fifty creative decisions and contains no
  generated output metadata.
- `akari_v1_5_b001_contract.py` owns matrix validation, prompt compilation,
  reference resolution, filenames, and pending-manifest construction.
- `akari_v1_5_b001_state.py` owns exclusive media installation, attempt and
  success receipts, manifest/ledger reconciliation, resume status, and review
  summary. It also snapshots names and available manifest metadata from the
  pre-existing generated archive as prior coverage without using archive
  pixels as references.
- `manage_akari_v1_5_b001.py` is a thin CLI with `prepare`, `prompt`,
  `status`, `record-success`, `record-failure`, `reconcile`, and
  `review-summary` subcommands.
- `recover_akari_imagegen_payload.py` owns JSONL parsing and PNG payload
  recovery only.
- Existing `scripts/build_akari_review_thumbnail.py` remains the sole PNG
  inspection and WebP derivation implementation.
- Existing `tools/review-gallery/manifest.mjs` remains the canonical final
  manifest validator.

## Exact B001 Creative Matrix

The matrix file must contain these IDs in this order. Every row also receives
the two permanent references. Conditional reference IDs use
`v1.4-seated`, `v1.4-action`, and `neesocks-pressure-study`.

### Lane 1: `classic-school-uniform`

- **B001-001 — Courtyard schedule dash**
  - `filenameScene=courtyard-schedule-dash`;
    `wardrobeFamily=navy-blazer-burgundy-ribbon`;
    wardrobe is a navy adult-academy blazer, ivory rounded-collar blouse,
    burgundy ribbon, charcoal knee-length pleated skirt, and brown loafers.
  - `setting=adult-academy-courtyard`;
    `action=jogs-with-windblown-schedule`;
    `cuteBeat=leans forward with sudden happiness after finding the right room`.
  - `sceneMode=action-reaction`;
    `composition=full-body-forward-motion`;
    `camera=eye-level-front-three-quarter-50mm`;
    pose/hands/gaze: one hand secures the schedule, the other balances her
    stride, gaze toward the doorway.
  - `lighting=clear-morning-open-shade`; `cast=solo`;
    `dominantColor=navy-burgundy-ivory`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: fashion-catalog stillness and copied B3 apartment.

- **B001-002 — Library ribbon adjustment**
  - `filenameScene=library-ribbon-adjustment`;
    `wardrobeFamily=cream-cardigan-sailor-collar`;
    wardrobe is a cream cardigan, navy sailor collar, muted blue pleated
    skirt, dark over-knee socks, and oxford shoes.
  - `setting=quiet-library-corridor`;
    `action=reties-loosened-ribbon`;
    `cuteBeat=becomes visibly embarrassed when she notices the crooked bow`.
  - `sceneMode=action-reaction`;
    `composition=knee-up-intimate-gesture`;
    `camera=slightly-high-left-three-quarter-65mm`;
    pose/hands/gaze: both hands lightly retie the bow, knees relaxed, gaze
    briefly down and aside.
  - `lighting=soft-window-afternoon`; `cast=solo`;
    `dominantColor=cream-navy-dusty-blue`;
    `textureType=over-knee-socks`; conditional references:
    `v1.4-action`, `neesocks-pressure-study`;
    targeted avoid: uniform rubber-ring compression and isolated leg framing.

- **B001-003 — Classroom tab sorting**
  - `filenameScene=classroom-tab-sorting`;
    `wardrobeFamily=moss-knit-vest-pinstripe`;
    wardrobe is a moss knit vest, blue pinstripe blouse, long brown plaid
    pleated skirt, cream tights, and leather flats.
  - `setting=sunlit-seminar-classroom`;
    `action=sorts-colored-index-tabs`;
    `cuteBeat=narrows her eyes in absorbed curiosity while choosing one tab`.
  - `sceneMode=action-reaction`;
    `composition=waist-up-table-context`;
    `camera=high-oblique-right-45mm`;
    pose/hands/gaze: fingertips separate small tabs on a notebook, shoulders
    slightly forward, gaze fixed on the colors.
  - `lighting=late-morning-window-bounce`; `cast=solo`;
    `dominantColor=moss-blue-walnut`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: illegible written text and extra fingers.

- **B001-004 — Platform lanyard catch**
  - `filenameScene=platform-lanyard-catch`;
    `wardrobeFamily=camel-blazer-checked-culottes`;
    wardrobe is a camel cropped blazer, pale-pink bow blouse, brown checked
    culottes, ribbed knee socks, and tassel loafers.
  - `setting=covered-adult-academy-platform`;
    `action=catches-falling-id-lanyard`;
    `cuteBeat=freezes in small surprise as the lanyard slips`.
  - `sceneMode=action-reaction`;
    `composition=full-body-diagonal-catch`;
    `camera=low-right-three-quarter-35mm`;
    pose/hands/gaze: one foot checks forward momentum, one hand catches the
    lanyard, gaze follows it.
  - `lighting=overcast-platform-fill`; `cast=solo`;
    `dominantColor=camel-pink-chocolate`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: train logos and airborne anatomy distortion.

- **B001-005 — Rooftop notebook relief**
  - `filenameScene=rooftop-notebook-relief`;
    `wardrobeFamily=lilac-cardigan-tea-pleat`;
    wardrobe is a lilac cardigan, white scalloped-collar blouse, ink-blue
    tea-length pleated skirt, and cream ankle-strap shoes.
  - `setting=adult-academy-rooftop-garden`;
    `action=closes-finished-notebook`;
    `cuteBeat=lets out a tiny relieved smile after finishing her notes`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-standing-environment`;
    `camera=eye-level-side-three-quarter-70mm`;
    pose/hands/gaze: notebook held closed to her chest, weight settles onto
    one leg, gaze toward the sunset plants.
  - `lighting=warm-sunset-rim`; `cast=solo`;
    `dominantColor=lilac-ink-gold`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: cold model pose and excessive lens flare.

### Lane 2: `professional-service-uniform`

- **B001-006 — Bakery madeleine presentation**
  - `filenameScene=bakery-madeleine-presentation`;
    `wardrobeFamily=rose-bakery-apron-dress`;
    wardrobe is a rose service dress, ivory bib apron, narrow neck ribbon,
    warm brown sheer tights, and low leather pumps.
  - `setting=small-bakery-open-kitchen`;
    `action=presents-fresh-madeleine-tray`;
    `cuteBeat=leans forward with proud visible excitement at a successful bake`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-tray-foreground`;
    `camera=counter-height-front-three-quarter-50mm`;
    pose/hands/gaze: both hands level the tray, elbows natural, gaze toward the
    viewer.
  - `lighting=warm-oven-and-window-mix`; `cast=solo`;
    `dominantColor=rose-ivory-caramel`;
    `textureType=tights-stockings`; conditional references:
    `v1.4-action`, `neesocks-pressure-study`;
    targeted avoid: food logos, painted-on tights, and duplicated pastries.

- **B001-007 — Florist bouquet untangle**
  - `filenameScene=florist-bouquet-untangle`;
    `wardrobeFamily=sage-florist-apron`;
    wardrobe is a sage cross-back apron over a puff-sleeve cream dress, a
    narrow coral waist ribbon, and tan lace-up shoes.
  - `setting=corner-flower-shop`;
    `action=untangles-ribbon-from-bouquet`;
    `cuteBeat=smiles with shy embarrassment after catching her own sleeve`.
  - `sceneMode=action-reaction`;
    `composition=knee-up-bouquet-interaction`;
    `camera=eye-level-left-three-quarter-55mm`;
    pose/hands/gaze: one hand steadies stems, the other frees the ribbon, gaze
    follows the knot.
  - `lighting=diffused-shopfront-daylight`; `cast=solo`;
    `dominantColor=sage-coral-cream`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: fused fingers and flowers replacing the hair ornament.

- **B001-008 — Bookstore bookplate stamp**
  - `filenameScene=bookstore-bookplate-stamp`;
    `wardrobeFamily=plum-bookstore-waistcoat`;
    wardrobe is a plum waistcoat, ivory pintuck blouse, dark green midi skirt,
    patterned neck scarf, and black flats.
  - `setting=independent-bookstore-counter`;
    `action=stamps-bookplate-carefully`;
    `cuteBeat=shows quiet concentration with the tip of her tongue almost
    visible`.
  - `sceneMode=action-reaction`;
    `composition=waist-up-counter-detail`;
    `camera=slightly-high-front-60mm`;
    pose/hands/gaze: one palm steadies the book, the other presses the stamp,
    gaze centered on the plate.
  - `lighting=amber-pendant-soft-fill`; `cast=solo`;
    `dominantColor=plum-forest-ivory`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: readable copyrighted text and impossible stamp grip.

- **B001-009 — Hotel key-tag stop**
  - `filenameScene=hotel-key-tag-stop`;
    `wardrobeFamily=teal-concierge-jacket`;
    wardrobe is a teal concierge jacket, pearl blouse, charcoal midi skirt,
    small neck bow, and polished pumps.
  - `setting=boutique-hotel-lobby`;
    `action=stops-rolling-key-tag`;
    `cuteBeat=widens her eyes in a tiny mistake reaction before recovering`.
  - `sceneMode=action-reaction`;
    `composition=full-body-reaching-step`;
    `camera=low-front-three-quarter-40mm`;
    pose/hands/gaze: one foot blocks the rolling tag, one hand reaches without
    overbalancing, gaze down.
  - `lighting=soft-lobby-chandelier`; `cast=solo`;
    `dominantColor=teal-pearl-charcoal`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: hotel branding and broken ankle perspective.

- **B001-010 — Workshop shaving brush-off**
  - `filenameScene=workshop-shaving-brushoff`;
    `wardrobeFamily=indigo-workshop-dress`;
    wardrobe is an indigo tailored workshop dress with rolled sleeves, a sand
    utility apron, rust neckerchief, and sturdy brown boots.
  - `setting=bright-woodcraft-workshop`;
    `action=brushes-wood-shavings-from-apron`;
    `cuteBeat=gives a calm playful smile at the stubborn last shaving`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-standing-bench-context`;
    `camera=eye-level-right-three-quarter-50mm`;
    pose/hands/gaze: one hand brushes the apron, the other rests safely on the
    bench edge, gaze at the shaving.
  - `lighting=north-window-worklight`; `cast=solo`;
    `dominantColor=indigo-sand-rust`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: active power tools and heavy industrial grime.

### Lane 3: `sports-ceremony-fictional-uniform`

- **B001-011 — Boathouse pennant lift**
  - `filenameScene=boathouse-pennant-lift`;
    `wardrobeFamily=rowing-club-cardigan`;
    wardrobe is a white rowing-club cardigan with plain navy piping, a
    sky-blue blouse, navy pleated skort, ribbed knee-high socks, and deck shoes.
  - `setting=river-boathouse-terrace`;
    `action=raises-small-team-pennant`;
    `cuteBeat=beams with open happiness after her team is called`.
  - `sceneMode=action-reaction`;
    `composition=full-body-upward-gesture`;
    `camera=slightly-low-left-three-quarter-45mm`;
    pose/hands/gaze: pennant raised in one hand, the other at her chest, gaze
    toward teammates outside frame.
  - `lighting=crisp-river-morning`; `cast=solo`;
    `dominantColor=white-navy-sky`;
    `textureType=knee-high-socks`; conditional references:
    `neesocks-pressure-study`;
    targeted avoid: logos, school-child drift, and uniform band grooves.

- **B001-012 — Fencing glove hesitation**
  - `filenameScene=fencing-glove-hesitation`;
    `wardrobeFamily=plum-fencing-warmup`;
    wardrobe is a plum warm-up jacket over an ivory athletic blouse, a black
    wrap skort, opaque tights, and clean court shoes.
  - `setting=adult-fencing-club-anteroom`;
    `action=checks-glove-strap-twice`;
    `cuteBeat=hesitates with an embarrassed half-smile before entering`.
  - `sceneMode=action-reaction`;
    `composition=knee-up-preparation`;
    `camera=eye-level-front-65mm`;
    pose/hands/gaze: unarmed hands adjust the glove strap, shoulders slightly
    drawn in, gaze toward the doorway.
  - `lighting=cool-gym-window-warm-bounce`; `cast=solo`;
    `dominantColor=plum-ivory-black`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: weapon emphasis and child competition styling.

- **B001-013 — Star-map alignment**
  - `filenameScene=star-map-alignment`;
    `wardrobeFamily=planetarium-guide-uniform`;
    wardrobe is a midnight-blue guide tunic, silver waist tab, soft gray
    pleated trousers, and navy ankle boots.
  - `setting=planetarium-control-gallery`;
    `action=aligns-transparent-star-map`;
    `cuteBeat=leans closer in absorbed curiosity when two stars finally match`.
  - `sceneMode=action-reaction`;
    `composition=waist-up-map-layer`;
    `camera=over-console-right-three-quarter-50mm`;
    pose/hands/gaze: both hands hold opposite map corners, gaze through the
    transparent layer.
  - `lighting=dim-blue-console-glow`; `cast=solo`;
    `dominantColor=midnight-silver-blue`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: readable interface text and transparent extra fingers.

- **B001-014 — Choir folio catch**
  - `filenameScene=choir-folio-catch`;
    `wardrobeFamily=modern-civic-choir`;
    wardrobe is a wine-red modern choir overdress over a cream blouse, narrow
    gold sash, black midi skirt, and low heels.
  - `setting=civic-hall-side-stage`;
    `action=catches-slipping-music-folio`;
    `cuteBeat=reacts with a small surprised inhale without losing composure`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-side-stage`;
    `camera=eye-level-left-profile-three-quarter-70mm`;
    pose/hands/gaze: forearm catches the closed folio while the other hand
    steadies it, gaze down.
  - `lighting=warm-stage-spill`; `cast=solo`;
    `dominantColor=wine-cream-gold`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: readable sheet music and duplicated arms.

- **B001-015 — Glasshouse field-pouch relief**
  - `filenameScene=glasshouse-fieldpouch-relief`;
    `wardrobeFamily=botanical-expedition-uniform`;
    wardrobe is a moss expedition vest over a pale-yellow shirt dress, khaki
    belt pouch, cream leggings, and brown walking boots.
  - `setting=research-glasshouse-balcony`;
    `action=zips-secured-field-pouch`;
    `cuteBeat=relaxes into a satisfied smile after finding the missing sample`.
  - `sceneMode=action-reaction`;
    `composition=full-body-railing-context`;
    `camera=eye-level-rear-three-quarter-turn-55mm`;
    pose/hands/gaze: both hands finish the zipper, torso turns back toward the
    plants, gaze soft.
  - `lighting=humid-greenhouse-diffusion`; `cast=solo`;
    `dominantColor=moss-yellow-khaki`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: military insignia and tactical posing.

### Lane 4: `everyday-girly`

- **B001-016 — Strawberry basket turn**
  - `filenameScene=strawberry-basket-turn`;
    `wardrobeFamily=gingham-blouse-denim-midi`;
    wardrobe is a red gingham puff-sleeve blouse, indigo A-line denim midi
    skirt, cream belt, and red flats.
  - `setting=apartment-kitchen-window`;
    `action=turns-with-strawberry-basket`;
    `cuteBeat=lights up with happiness when she notices one perfect berry`.
  - `sceneMode=action-reaction`;
    `composition=full-body-turning-arc`;
    `camera=eye-level-left-three-quarter-45mm`;
    pose/hands/gaze: basket supported by both forearms, skirt follows the turn,
    gaze at the berry.
  - `lighting=bright-spring-window`; `cast=solo`;
    `dominantColor=red-indigo-cream`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: copied B3 lounge outfit and duplicated fruit.

- **B001-017 — Sleeve-hidden compliment**
  - `filenameScene=sleeve-hidden-compliment`;
    `wardrobeFamily=rose-knit-dress`;
    wardrobe is a rose rib-knit dress with a modest flared skirt, oatmeal
    cardigan, charcoal over-knee socks, and brown Mary Jane shoes.
  - `setting=cozy-living-room-sofa-side`;
    `action=hides-fingertips-in-sleeves`;
    `cuteBeat=looks away with warm embarrassment after an off-frame compliment`.
  - `sceneMode=action-reaction`;
    `composition=knee-up-soft-posture`;
    `camera=slightly-high-front-three-quarter-70mm`;
    pose/hands/gaze: sleeves meet lightly near her chin, knees and hips remain
    natural, gaze aside.
  - `lighting=cloudy-window-warm-lamp`; `cast=solo`;
    `dominantColor=rose-oatmeal-charcoal`;
    `textureType=over-knee-socks`; conditional references:
    `neesocks-pressure-study`;
    targeted avoid: pin-up framing and uniform compression rings.

- **B001-018 — Needle threading focus**
  - `filenameScene=needle-threading-focus`;
    `wardrobeFamily=mint-cardigan-linen-trouser`;
    wardrobe is a mint cropped cardigan, ivory camisole blouse, high-waisted
    sand linen trousers, and soft house flats.
  - `setting=window-desk-sewing-corner`;
    `action=threads-needle-under-window`;
    `cuteBeat=holds her breath in tiny concentrated curiosity`.
  - `sceneMode=action-reaction`;
    `composition=waist-up-hand-detail`;
    `camera=eye-level-right-three-quarter-85mm`;
    pose/hands/gaze: needle and thread held with believable fine grip, elbows
    supported, gaze fixed on the eye.
  - `lighting=neutral-north-window`; `cast=solo`;
    `dominantColor=mint-ivory-sand`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: macro-only crop, extra fingers, and oversized needle.

- **B001-019 — Entryway scarf catch**
  - `filenameScene=entryway-scarf-catch`;
    `wardrobeFamily=blue-wrap-blouse-cream-skirt`;
    wardrobe is a cornflower wrap blouse, cream box-pleat skirt, gray tights,
    and navy ankle boots.
  - `setting=apartment-entryway`;
    `action=catches-tumbling-scarf`;
    `cuteBeat=blinks in surprise when the scarf slides from the hook`.
  - `sceneMode=action-reaction`;
    `composition=full-body-reach-across`;
    `camera=low-eye-level-front-three-quarter-40mm`;
    pose/hands/gaze: one hand catches the scarf mid-fall, the other keeps her
    bag from slipping, gaze tracks fabric.
  - `lighting=soft-entryway-evening`; `cast=solo`;
    `dominantColor=cornflower-cream-gray`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: impossible scarf physics and bent doorway geometry.

- **B001-020 — Curtain-peek tease**
  - `filenameScene=curtain-peek-tease`;
    `wardrobeFamily=peach-sweater-check-lounge-skirt`;
    wardrobe is an oversized peach sweater, brown checked lounge skirt, cream
    leggings, and plush slippers.
  - `setting=bedroom-window-curtain`;
    `action=peeks-around-curtain`;
    `cuteBeat=gives a calm teasing smile after hiding for one second`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-vertical-frame`;
    `camera=eye-level-front-55mm`;
    pose/hands/gaze: one hand holds the curtain edge, other behind her back,
    gaze directly to viewer.
  - `lighting=golden-hour-through-curtain`; `cast=solo`;
    `dominantColor=peach-brown-cream`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: voyeuristic framing and copied bedroom composition.

### Lane 5: `outings-special-days`

- **B001-021 — Parfait arrival lean**
  - `filenameScene=parfait-arrival-lean`;
    `wardrobeFamily=powderblue-tea-dress`;
    wardrobe is a powder-blue tea dress with an ivory collar, narrow navy
    belt, pearl-gray cardigan, and blue pumps.
  - `setting=botanical-cafe-table`;
    `action=leans-toward-arriving-parfait`;
    `cuteBeat=shows unguarded happiness at the tiny seasonal decoration`.
  - `sceneMode=action-reaction`;
    `composition=seated-three-quarter-table`;
    `camera=table-height-front-three-quarter-60mm`;
    pose/hands/gaze: hands remain near her lap and cup, torso leans naturally,
    gaze at the dessert.
  - `lighting=leaf-filtered-noon`; `cast=solo`;
    `dominantColor=powderblue-ivory-green`;
    `textureType=none`; conditional references: `v1.4-seated`;
    targeted avoid: duplicated utensils and commercial food text.

- **B001-022 — Reversed cinema ticket**
  - `filenameScene=reversed-cinema-ticket`;
    `wardrobeFamily=burgundy-capelet-ivory-dress`;
    wardrobe is a burgundy capelet, ivory fit-and-flare dress, charcoal ankle
    socks, and oxblood strap shoes.
  - `setting=restored-cinema-queue`;
    `action=flips-reversed-ticket`;
    `cuteBeat=flushes with embarrassment when she notices she held it upside
    down`.
  - `sceneMode=action-reaction`;
    `composition=knee-up-queue-context`;
    `camera=eye-level-left-three-quarter-65mm`;
    pose/hands/gaze: ticket pinched by two corners, shoulders soften, gaze on
    the blank ticket face.
  - `lighting=marquee-dusk-fill`; `cast=solo`;
    `dominantColor=burgundy-ivory-oxblood`;
    `textureType=crew-ankle-socks`; conditional references:
    `v1.4-action`, `neesocks-pressure-study`;
    targeted avoid: readable ticket text and exaggerated sock indentation.

- **B001-023 — Record sleeve comparison**
  - `filenameScene=record-sleeve-comparison`;
    `wardrobeFamily=emerald-bow-black-midi`;
    wardrobe is an emerald bow blouse, black paneled midi skirt, camel short
    coat, and black loafers.
  - `setting=independent-record-shop`;
    `action=compares-two-record-sleeves`;
    `cuteBeat=tilts her head in focused curiosity over the difficult choice`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-aisle`;
    `camera=slightly-high-right-three-quarter-50mm`;
    pose/hands/gaze: one sleeve in each hand with plausible grip, gaze moves
    between abstract covers.
  - `lighting=warm-shop-tracklights`; `cast=solo`;
    `dominantColor=emerald-black-camel`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: album logos, readable titles, and duplicate sleeves.

- **B001-024 — Gallery umbrella pop**
  - `filenameScene=gallery-umbrella-pop`;
    `wardrobeFamily=champagne-blouse-plum-skirt`;
    wardrobe is a champagne satin blouse, plum midi skirt, soft gray trench
    carried over one arm, and taupe heels.
  - `setting=art-gallery-foyer`;
    `action=contains-opening-umbrella`;
    `cuteBeat=reacts in surprised apology when the damp umbrella starts to
    open`.
  - `sceneMode=action-reaction`;
    `composition=full-body-diagonal-object`;
    `camera=eye-level-front-three-quarter-45mm`;
    pose/hands/gaze: both hands safely contain the umbrella, step moves away
    from displays, gaze at the latch.
  - `lighting=cool-gallery-softbox`; `cast=solo`;
    `dominantColor=champagne-plum-gray`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: artwork replication and umbrella intersecting limbs.

- **B001-025 — Winter bridge cocoa**
  - `filenameScene=winter-bridge-cocoa`;
    `wardrobeFamily=ivory-coatdress-lavender-scarf`;
    wardrobe is an ivory coat dress, lavender scarf, slate tights, and dark
    mauve ankle boots.
  - `setting=winter-light-pedestrian-bridge`;
    `action=warms-hands-around-cocoa`;
    `cuteBeat=settles into a calm relieved smile beneath the lights`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-environmental-portrait`;
    `camera=eye-level-side-three-quarter-75mm`;
    pose/hands/gaze: both hands around a plain cup, shoulders relaxed, gaze at
    distant lights.
  - `lighting=blue-hour-fairy-lights`; `cast=solo`;
    `dominantColor=ivory-lavender-slate`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: logos, excessive bokeh, and glamour-model posture.

### Lane 6: `hobbies-making`

- **B001-026 — Successful soufflé lift**
  - `filenameScene=successful-souffle-lift`;
    `wardrobeFamily=navy-dress-gingham-apron`;
    wardrobe is a navy puff-sleeve dress, red gingham apron, cream
    over-knee socks, and brown kitchen clogs.
  - `setting=community-cooking-studio`;
    `action=lifts-successful-souffle`;
    `cuteBeat=shows a small proud grin at the evenly risen top`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-oven-to-counter`;
    `camera=counter-height-left-three-quarter-50mm`;
    pose/hands/gaze: oven-mitted hands support the dish evenly, gaze at the
    soufflé, stance stable.
  - `lighting=warm-kitchen-tasklight`; `cast=solo`;
    `dominantColor=navy-red-cream`;
    `textureType=over-knee-socks`; conditional references:
    `v1.4-action`, `neesocks-pressure-study`;
    targeted avoid: unsafe bare-hand heat contact and hard sock-ring grooves.

- **B001-027 — Escaping thread spool**
  - `filenameScene=escaping-thread-spool`;
    `wardrobeFamily=blue-sewing-smock-floral-skirt`;
    wardrobe is a dusty-blue sewing smock, ivory blouse, small floral midi
    skirt, and tan flats.
  - `setting=shared-sewing-room`;
    `action=stops-rolling-thread-spool`;
    `cuteBeat=laughs with embarrassed hesitation at her own small mistake`.
  - `sceneMode=action-reaction`;
    `composition=full-body-crouching-reach`;
    `camera=slightly-low-right-three-quarter-45mm`;
    pose/hands/gaze: one knee bends without collapse, fingertips stop the
    spool, gaze down.
  - `lighting=bright-overcast-studio`; `cast=solo`;
    `dominantColor=dustyblue-floral-tan`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: broken crouch anatomy and tangled extra thread.

- **B001-028 — Camera focus ring**
  - `filenameScene=camera-focus-ring`;
    `wardrobeFamily=olive-utility-blouse-beige-culottes`;
    wardrobe is an olive utility blouse, beige wide culottes, rust belt, and
    dark brown lace shoes.
  - `setting=analog-photography-worktable`;
    `action=adjusts-camera-focus-ring`;
    `cuteBeat=concentrates with bright curiosity as the image sharpens`.
  - `sceneMode=action-reaction`;
    `composition=waist-up-camera-object`;
    `camera=eye-level-front-three-quarter-70mm`;
    pose/hands/gaze: left hand supports the lens, right hand turns the ring,
    gaze through the viewfinder.
  - `lighting=single-window-reflector`; `cast=solo`;
    `dominantColor=olive-beige-rust`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: impossible camera controls and brand marks.

- **B001-029 — Piano folio elbow save**
  - `filenameScene=piano-folio-elbow-save`;
    `wardrobeFamily=coral-cardigan-piano-dress`;
    wardrobe is a coral cardigan over a simple black piano dress, gray tights,
    and black strap shoes.
  - `setting=small-music-practice-room`;
    `action=steadies-slipping-folio-with-elbow`;
    `cuteBeat=blinks in surprise while keeping both hands near the keyboard`.
  - `sceneMode=action-reaction`;
    `composition=seated-side-three-quarter`;
    `camera=keyboard-height-left-three-quarter-55mm`;
    pose/hands/gaze: forearm and elbow catch the closed folio naturally, back
    stays aligned, gaze to the side.
  - `lighting=late-afternoon-practice-room`; `cast=solo`;
    `dominantColor=coral-black-gray`;
    `textureType=none`; conditional references:
    `v1.4-seated`, `v1.4-action`;
    targeted avoid: extra hands and readable sheet music.

- **B001-030 — Soil-smudge relief**
  - `filenameScene=soil-smudge-relief`;
    `wardrobeFamily=garden-overalls-puff-blouse`;
    wardrobe is sage garden overalls over a cream puff-sleeve blouse, a coral
    hair-safe scarf at the neck, and brown garden shoes.
  - `setting=apartment-balcony-garden`;
    `action=wipes-soil-smudge-from-cheek`;
    `cuteBeat=smiles in relief after the repotted plant stands straight`.
  - `sceneMode=action-reaction`;
    `composition=knee-up-planter-context`;
    `camera=eye-level-right-three-quarter-60mm`;
    pose/hands/gaze: clean wrist touches cheek while the other hand rests on
    the planter rim, gaze at the plant.
  - `lighting=soft-late-day-balcony`; `cast=solo`;
    `dominantColor=sage-cream-terracotta`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: facial mud masking identity and gardening-tool clutter.

### Lane 7: `travel-walking`

- **B001-031 — Departure-board turn**
  - `filenameScene=departure-board-turn`;
    `wardrobeFamily=red-trench-plaid-skirt`;
    wardrobe is a red short trench, cream cable knit, forest plaid midi skirt,
    black tights, and oxblood boots.
  - `setting=regional-rail-concourse`;
    `action=turns-toward-departure-board`;
    `cuteBeat=brightens with happiness when her platform appears`.
  - `sceneMode=action-reaction`;
    `composition=full-body-turn-suitcase`;
    `camera=eye-level-rear-three-quarter-45mm`;
    pose/hands/gaze: one hand holds the suitcase handle, coat follows the turn,
    gaze upward.
  - `lighting=high-station-skylight`; `cast=solo`;
    `dominantColor=red-cream-forest`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: readable station text and copied travel archive scene.

- **B001-032 — Ferry hat-ribbon hold**
  - `filenameScene=ferry-hatribbon-hold`;
    `wardrobeFamily=mustard-duffle-corduroy-skirt`;
    wardrobe is a mustard duffle coat, ivory ribbon blouse, brown corduroy
    skirt, navy tights, and tan boots.
  - `setting=ferry-upper-deck`;
    `action=secures-windblown-hat-ribbon`;
    `cuteBeat=smiles with embarrassed hesitation at the sudden gust`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-wind-motion`;
    `camera=eye-level-left-three-quarter-50mm`;
    pose/hands/gaze: one hand secures the plain beret and ribbon, other holds
    the rail lightly, gaze toward shore.
  - `lighting=bright-sea-overcast`; `cast=solo`;
    `dominantColor=mustard-brown-navy`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: unsafe railing lean and excessive wind distortion.

- **B001-033 — Train route tracing**
  - `filenameScene=train-route-tracing`;
    `wardrobeFamily=blue-travel-cardigan-soft-shorts`;
    wardrobe is a blue travel cardigan, ivory bow blouse, tailored tan
    mid-thigh shorts, and brown ankle boots.
  - `setting=regional-train-window-seat`;
    `action=traces-route-on-folded-map`;
    `cuteBeat=leans in with focused curiosity while counting one final stop`.
  - `sceneMode=action-reaction`;
    `composition=seated-full-figure-window-context`;
    `camera=aisle-eye-level-three-quarter-55mm`;
    pose/hands/gaze: thighs contact the seat naturally, one finger traces an
    abstract route, map rests across both hands.
  - `lighting=moving-soft-window-daylight`; `cast=solo`;
    `dominantColor=blue-ivory-tan`;
    `textureType=bare-contact`; conditional references:
    `v1.4-seated`, `v1.4-action`;
    targeted avoid: pin-up leg framing, readable map text, and hard seat
    indentation.

- **B001-034 — Coastal splash sidestep**
  - `filenameScene=coastal-splash-sidestep`;
    `wardrobeFamily=white-raincoat-teal-dress`;
    wardrobe is a white cropped raincoat over a teal gathered dress, gray
    leggings, and yellow rain boots.
  - `setting=covered-coastal-shopping-arcade`;
    `action=sidesteps-sudden-rain-splash`;
    `cuteBeat=opens her eyes in amused surprise as the water misses`.
  - `sceneMode=action-reaction`;
    `composition=full-body-lateral-motion`;
    `camera=low-front-three-quarter-35mm`;
    pose/hands/gaze: side step stays balanced, one hand lifts the coat hem
    safely, gaze at the splash.
  - `lighting=rainy-day-reflection`; `cast=solo`;
    `dominantColor=white-teal-yellow`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: transparent wet clothing and impossible splash anatomy.

- **B001-035 — Observation-deck arrival**
  - `filenameScene=observationdeck-arrival`;
    `wardrobeFamily=plum-knitcoat-gray-dress`;
    wardrobe is a plum knit coat over a dove-gray dress, cream scarf, charcoal
    tights, and black ankle boots.
  - `setting=airport-observation-deck`;
    `action=rests-hand-on-suitcase-after-arrival`;
    `cuteBeat=exhales with quiet relief while watching one distant plane`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-standing-railing-distance`;
    `camera=eye-level-side-three-quarter-75mm`;
    pose/hands/gaze: one hand rests on suitcase handle, other holds scarf,
    weight settles naturally, gaze outward.
  - `lighting=cool-dusk-runway-glow`; `cast=solo`;
    `dominantColor=plum-dove-charcoal`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: airline logos and cinematic loneliness drift.

### Lane 8: `retro-storybook`

- **B001-036 — Found postcard offer**
  - `filenameScene=found-postcard-offer`;
    `wardrobeFamily=taisho-hakama-daywear`;
    wardrobe is an adult Taisho-inspired ivory blouse, rust hakama-style long
    skirt, moss short cape, and brown lace boots.
  - `setting=old-bookshop-back-aisle`;
    `action=offers-found-postcard-to-viewer`;
    `cuteBeat=shares visible happiness at the delicate discovery`.
  - `sceneMode=action-reaction`;
    `composition=three-quarter-viewer-pov-offer`;
    `camera=viewer-eye-level-front-55mm`;
    pose/hands/gaze: one hand offers a blank vintage postcard, other holds an
    open book, gaze to viewer.
  - `lighting=dusty-window-gold`; `cast=viewer-pov`;
    `dominantColor=rust-moss-ivory`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: readable postcard text and period-child styling.

- **B001-037 — Shared float straw bump**
  - `filenameScene=shared-float-straw-bump`;
    `wardrobeFamily=fifties-polkadot-dress`;
    wardrobe is a cherry 1950s-inspired polka-dot day dress, cream cardigan,
    sheer warm-gray stockings, and red pumps.
  - `setting=gentle-retro-soda-parlor`;
    `action=steadies-shared-float`;
    `cuteBeat=flushes with embarrassment when two straws bump`.
  - `sceneMode=action-reaction`;
    `composition=seated-two-person-table`;
    `camera=table-height-side-three-quarter-65mm`;
    pose/hands/gaze: one hand steadies the glass base, the companion is only
    partially visible, gaze shifts from straws to companion.
  - `lighting=soft-neon-and-window`; `cast=two-person`;
    `dominantColor=cherry-cream-aqua`;
    `textureType=tights-stockings`; conditional references:
    `v1.4-seated`, `neesocks-pressure-study`;
    targeted avoid: romantic age drift, duplicated glassware, and plastic
    stockings.

- **B001-038 — Conservatory cipher**
  - `filenameScene=conservatory-cipher`;
    `wardrobeFamily=edwardian-pinafore-daywear`;
    wardrobe is an adult Edwardian-inspired high-neck ivory blouse, sage
    pinafore midi skirt, plum ribbon belt, and brown boots.
  - `setting=storybook-glass-conservatory`;
    `action=deciphers-symbol-note-with-friend`;
    `cuteBeat=shows intent curiosity when one symbol finally makes sense`.
  - `sceneMode=action-reaction`;
    `composition=two-person-waist-up-note`;
    `camera=slightly-high-front-three-quarter-60mm`;
    pose/hands/gaze: Akari points to an abstract symbol while a friend holds
    the note, both gazes meet the paper.
  - `lighting=greenhouse-morning-haze`; `cast=two-person`;
    `dominantColor=sage-plum-ivory`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: readable language and merged hands.

- **B001-039 — Theater lantern flicker**
  - `filenameScene=theater-lantern-flicker`;
    `wardrobeFamily=showa-cinema-usher`;
    wardrobe is a Showa-inspired navy usher jacket, peach blouse, burgundy
    midi skirt, and navy low heels.
  - `setting=restored-neighborhood-theater`;
    `action=looks-up-at-flickering-lantern`;
    `cuteBeat=shares a startled glance with her coworker`.
  - `sceneMode=action-reaction`;
    `composition=two-person-full-figure-aisle`;
    `camera=low-aisle-left-three-quarter-45mm`;
    pose/hands/gaze: flashlight remains pointed safely down, free hand pauses
    near chest, both gazes upward.
  - `lighting=amber-lantern-flicker`; `cast=two-person`;
    `dominantColor=navy-peach-burgundy`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: horror tone, readable posters, and theatrical logos.

- **B001-040 — Tiny music-box reveal**
  - `filenameScene=tiny-musicbox-reveal`;
    `wardrobeFamily=storybook-cape-dress`;
    wardrobe is a teal storybook cape dress, cream pintuck blouse, brown
    corset-style waist panel without tight-lacing, and ankle boots.
  - `setting=cobbled-western-retro-street`;
    `action=reveals-tiny-music-box`;
    `cuteBeat=gives the viewer a playful relieved smile after fixing it`.
  - `sceneMode=action-reaction`;
    `composition=viewer-pov-knee-up-reveal`;
    `camera=viewer-eye-level-front-60mm`;
    pose/hands/gaze: both palms present the closed music box safely, gaze to
    viewer.
  - `lighting=late-afternoon-shopfront`; `cast=viewer-pov`;
    `dominantColor=teal-cream-walnut`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: readable engraving and fantasy-corset exaggeration.

### Lane 9: `magic-fantasy-sf`

- **B001-041 — Orbiting star cradle**
  - `filenameScene=orbiting-star-cradle`;
    `wardrobeFamily=apprentice-mage-capelet`;
    wardrobe is a midnight apprentice capelet over a lavender layered dress,
    charcoal over-knee socks, and silver ankle boots.
  - `setting=moonlit-magic-observatory`;
    `action=cradles-orbiting-star-light`;
    `cuteBeat=holds a small happy smile as the light settles between her
    hands`.
  - `sceneMode=quiet-posed`;
    `composition=viewer-pov-full-figure-outfit`;
    `camera=viewer-eye-level-front-65mm`;
    pose/hands/gaze: cupped hands remain anatomically clear below her face,
    relaxed stance, gaze to the floating light.
  - `lighting=moonlight-and-warm-star-glow`; `cast=viewer-pov`;
    `dominantColor=midnight-lavender-silver`;
    `textureType=over-knee-socks`; conditional references:
    `v1.4-action`, `neesocks-pressure-study`;
    targeted avoid: magical light hiding fingers and hard sock-band grooves.

- **B001-042 — Orbital cuff greeting**
  - `filenameScene=orbital-cuff-greeting`;
    `wardrobeFamily=space-station-host-uniform`;
    wardrobe is a pearl-white host jacket, sky-blue asymmetric midi dress,
    silver belt tab, gray tights, and white ankle boots.
  - `setting=orbital-lounge-window`;
    `action=smooths-glowing-cuff-before-greeting`;
    `cuteBeat=shows gentle embarrassment after noticing the cuff is crooked`.
  - `sceneMode=quiet-posed`;
    `composition=viewer-pov-three-quarter-outfit`;
    `camera=viewer-eye-level-left-three-quarter-70mm`;
    pose/hands/gaze: one hand smooths the opposite cuff, posture welcoming,
    gaze returns to viewer.
  - `lighting=earthlight-soft-interior`; `cast=viewer-pov`;
    `dominantColor=pearl-sky-silver`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: logos, helmet, and sterile catalog posture.

- **B001-043 — Luminous seed inspection**
  - `filenameScene=luminous-seed-inspection`;
    `wardrobeFamily=botanical-alchemist-coatdress`;
    wardrobe is a moss alchemist coat dress, ivory gathered blouse, amber belt
    bottles, and brown boots.
  - `setting=luminous-fantasy-greenhouse`;
    `action=studies-glowing-seed-vial`;
    `cuteBeat=shares concentrated curiosity with an assistant`.
  - `sceneMode=quiet-posed`;
    `composition=two-person-waist-up-vial`;
    `camera=eye-level-right-three-quarter-75mm`;
    pose/hands/gaze: Akari holds the vial by its base while assistant indicates
    one seed, both gazes on the object.
  - `lighting=green-bioluminescent-warm-fill`; `cast=two-person`;
    `dominantColor=moss-amber-ivory`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: vial transparency erasing fingers and laboratory logos.

- **B001-044 — Holographic pet landing**
  - `filenameScene=holographic-pet-landing`;
    `wardrobeFamily=future-rain-dress`;
    wardrobe is a translucent-looking but opaque teal rain jacket over a plum
    future-city dress, charcoal leggings, and silver rain boots.
  - `setting=future-city-transit-platform`;
    `action=receives-holographic-pet-on-sleeve`;
    `cuteBeat=raises her brows in delighted surprise at the unexpected landing`.
  - `sceneMode=quiet-posed`;
    `composition=viewer-pov-three-quarter-sleeve-focus`;
    `camera=viewer-eye-level-front-three-quarter-60mm`;
    pose/hands/gaze: forearm held level, other hand relaxed near chest, gaze at
    the tiny light creature.
  - `lighting=rainy-neon-reflected-softly`; `cast=viewer-pov`;
    `dominantColor=teal-plum-silver`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: transparent clothing, cyberpunk grime, and hidden ornament.

- **B001-045 — Floating-door compass**
  - `filenameScene=floatingdoor-compass`;
    `wardrobeFamily=dream-navigator-gown`;
    wardrobe is a silver-blue navigator gown with a short structured jacket,
    cream layered skirt, navy sash, and soft boots.
  - `setting=strange-room-floating-doors`;
    `action=holds-compass-beside-companion`;
    `cuteBeat=settles into calm relief when the compass points to one door`.
  - `sceneMode=quiet-posed`;
    `composition=two-person-full-figure-environment`;
    `camera=eye-level-wide-three-quarter-50mm`;
    pose/hands/gaze: compass rests in both hands at waist height, companion
    stands behind one shoulder, both gaze to the chosen door.
  - `lighting=soft-shadowless-dreamlight`; `cast=two-person`;
    `dominantColor=silverblue-cream-navy`;
    `textureType=none`; conditional references: `v1.4-action`;
    targeted avoid: liminal horror, duplicated doors, and floating anatomy.

### Lane 10: `subculture-wildcard`

- **B001-046 — Dessert-studio cake share**
  - `filenameScene=dessertstudio-cake-share`;
    `wardrobeFamily=soft-gothic-plum-dress`;
    wardrobe is a plum soft-gothic dress with an ivory high collar, restrained
    black lace trim, black tights, and plum strap shoes.
  - `setting=sunlit-dessert-studio`;
    `action=shares-first-cake-slice-with-friends`;
    `cuteBeat=smiles openly with happiness as everyone leans in`.
  - `sceneMode=quiet-posed`;
    `composition=small-group-seated-table`;
    `camera=table-height-front-three-quarter-55mm`;
    pose/hands/gaze: Akari supports the serving plate while a friend receives
    it; three friends remain secondary.
  - `lighting=high-key-window-daylight`; `cast=group`;
    `dominantColor=plum-ivory-black`;
    `textureType=none`; `subculture=true`;
    conditional references: `v1.4-action`;
    targeted avoid: dark horror makeup and duplicated cake utensils.

- **B001-047 — Backward band badge**
  - `filenameScene=backward-band-badge`;
    `wardrobeFamily=pastel-punk-cardigan-pleat`;
    wardrobe is a mint-and-black pastel-punk cardigan, white blouse, charcoal
    pleated mini skirt over safe shorts, black over-knee socks, and platform
    sneakers with moderate soles.
  - `setting=bright-band-rehearsal-lounge`;
    `action=turns-backward-badge-rightside-up`;
    `cuteBeat=flushes with embarrassment when her bandmates point it out`.
  - `sceneMode=quiet-posed`;
    `composition=small-group-three-quarter`;
    `camera=eye-level-left-three-quarter-60mm`;
    pose/hands/gaze: fingers rotate the plain badge at her chest, friends react
    lightly behind, gaze down.
  - `lighting=soft-rehearsal-window`; `cast=group`;
    `dominantColor=mint-black-white`;
    `textureType=over-knee-socks`; `subculture=true`;
    conditional references: `v1.4-action`, `neesocks-pressure-study`;
    targeted avoid: logos, fetish framing, and excessive platform height.

- **B001-048 — One-charm selection**
  - `filenameScene=onecharm-selection`;
    `wardrobeFamily=decora-lite-layered-dress`;
    wardrobe is a coral decora-lite cardigan over a sky-blue layered dress,
    cream leggings, restrained colorful hair clips that do not replace the
    canonical ornament, and white sneakers.
  - `setting=art-school-sticker-workshop`;
    `action=selects-one-charm-from-tray`;
    `cuteBeat=shows intense concentration while friends wait for the choice`.
  - `sceneMode=quiet-posed`;
    `composition=small-group-waist-up-worktable`;
    `camera=slightly-high-front-three-quarter-55mm`;
    pose/hands/gaze: one fingertip indicates a single abstract charm, friends’
    hands remain separate, gaze on the tray.
  - `lighting=clean-studio-daylight`; `cast=group`;
    `dominantColor=coral-sky-cream`;
    `textureType=none`; `subculture=true`;
    conditional references: `v1.4-action`;
    targeted avoid: ornament replacement, brand characters, and cluttered face.

- **B001-049 — Laundromat bubble surprise**
  - `filenameScene=laundromat-bubble-surprise`;
    `wardrobeFamily=cyber-girly-reflective-jacket`;
    wardrobe is a silver reflective cropped jacket over a violet modest knit
    top, teal tulle midi skirt, black leggings, and silver sneakers.
  - `setting=clean-neon-laundromat`;
    `action=reacts-to-bubble-release`;
    `cuteBeat=widens her eyes in playful surprise as friends laugh`.
  - `sceneMode=quiet-posed`;
    `composition=small-group-full-figure`;
    `camera=low-eye-level-front-three-quarter-45mm`;
    pose/hands/gaze: hands lift slightly without flailing, friends remain clear
    behind, gaze at bubbles.
  - `lighting=soft-cyan-magenta-practicals`; `cast=group`;
    `dominantColor=silver-violet-teal`;
    `textureType=none`; `subculture=true`;
    conditional references: `v1.4-action`;
    targeted avoid: public-brand machines, wet clothing, and harsh cyberpunk.

- **B001-050 — Dawn rooftop cleanup**
  - `filenameScene=dawn-rooftop-cleanup`;
    `wardrobeFamily=angelcore-knit-sheerlayer-skirt`;
    wardrobe is an ivory angelcore knit, pale-blue long skirt with an opaque
    lining and soft sheer outer layer, gray tights, and ivory flats.
  - `setting=rooftop-picnic-at-dawn`;
    `action=rests-after-folding-picnic-cloth`;
    `cuteBeat=shares a calm relieved smile with friends after cleanup`.
  - `sceneMode=quiet-posed`;
    `composition=small-group-seated-wide`;
    `camera=eye-level-side-three-quarter-65mm`;
    pose/hands/gaze: Akari sits with natural weight on a bench, folded cloth in
    lap, friends nearby, gaze toward sunrise.
  - `lighting=pale-dawn-backlight`; `cast=group`;
    `dominantColor=ivory-paleblue-gray`;
    `textureType=none`; `subculture=true`;
    conditional references: `v1.4-seated`;
    targeted avoid: translucent underwear, angel wings, and religious symbols.

---

### Task 1: B001 Request Matrix and Prompt Compiler

**Files:**

- Create: `akari-v1.5/generation/b001-request-matrix.json`
- Create: `scripts/akari_v1_5_b001_contract.py`
- Create: `tests/test_akari_v1_5_b001_contract.py`

**Interfaces:**

- Consumes: the exact creative matrix above and
  `<dataRoot>/references/manifest.json`.
- Produces:
  `load_matrix(path: Path) -> dict[str, object]`,
  `validate_matrix(matrix: dict[str, object]) -> None`,
  `compile_prompt(entry: dict[str, object], references: dict[str, object]) -> str`,
  `reference_records(entry, reference_manifest) -> list[dict[str, object]]`,
  and `build_pending_manifest(matrix, reference_manifest) -> dict[str, object]`.

- [ ] **Step 1: Write failing contract tests**

Create tests that load the real matrix and assert:

```python
self.assertEqual(
    [f"B001-{ordinal:03d}" for ordinal in range(1, 51)],
    [entry["id"] for entry in matrix["entries"]],
)
self.assertEqual(
    {lane: 5 for lane in EXPECTED_LANES},
    Counter(entry["lane"] for entry in matrix["entries"]),
)
self.assertEqual(10, sum(item["textureFocus"] for item in entries))
self.assertEqual(
    {
        "over-knee-socks": 5,
        "tights-stockings": 2,
        "knee-high-socks": 1,
        "crew-ankle-socks": 1,
        "bare-contact": 1,
        "none": 40,
    },
    Counter(entry["textureType"] for entry in entries),
)
self.assertEqual(
    {"solo": 35, "viewer-pov": 5, "two-person": 5, "group": 5},
    Counter(entry["cast"] for entry in entries),
)
self.assertEqual(
    {"action-reaction": 40, "quiet-posed": 10},
    Counter(entry["sceneMode"] for entry in entries),
)
```

Also assert five `subculture` rows, exact sequential filenames, at most two
uses of one `wardrobeFamily`, at most three uses of one `setting`, at most two
uses of one `action`, unique existing `noveltyKey` field tuples, and no string
matching case-insensitive
the case-insensitive unresolved-marker expression assembled in the test from
`("T" + "BD", "TO" + "DO", "fill" + " in", "place" + "holder",
"appro" + "priate", "similar" + " to")`.

- [ ] **Step 2: Verify RED**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_5_b001_contract -v
```

Expected: FAIL because the matrix and compiler do not exist.

- [ ] **Step 3: Create the explicit matrix schema and all fifty rows**

The root is:

```json
{
  "schemaVersion": 1,
  "batchId": "B001",
  "title": "Akari v1.5 Kawaii 1000 B001",
  "promptContractVersion": 1,
  "entries": []
}
```

Each entry has exactly these matrix-owned properties:

```json
{
  "id": "B001-002",
  "filenameScene": "library-ribbon-adjustment",
  "lane": "classic-school-uniform",
  "conceptTitle": "Library ribbon adjustment",
  "scene": "In a quiet library corridor, ...",
  "cuteBeat": "She becomes visibly embarrassed ...",
  "wardrobeFamily": "cream-cardigan-sailor-collar",
  "wardrobe": "Cream cardigan, navy sailor collar, ...",
  "setting": "quiet-library-corridor",
  "action": "reties-loosened-ribbon",
  "sceneMode": "action-reaction",
  "composition": "knee-up-intimate-gesture",
  "camera": "slightly-high-left-three-quarter-65mm",
  "lighting": "soft-window-afternoon",
  "cast": "solo",
  "dominantColor": "cream-navy-dusty-blue",
  "textureFocus": true,
  "textureType": "over-knee-socks",
  "subculture": false,
  "poseHandsGaze": "Both hands lightly retie the bow ...",
  "material": "Dark over-knee knit remains distinct from warm skin ...",
  "conditionalReferenceIds": [
    "v1.4-action",
    "neesocks-pressure-study"
  ],
  "targetedAvoid": [
    "uniform rubber-ring compression",
    "isolated leg framing"
  ]
}
```

Transcribe every decision in “Exact B001 Creative Matrix” without weakening
specific nouns into generic labels. `scene`, `cuteBeat`, `wardrobe`,
`poseHandsGaze`, and `material` are complete English prompt clauses, not tags.
For `textureType=none`, `material` names the row’s most important garment
fabric plus the global skin direction. Construct
`filenameStem` in code as:

```python
f"akari_v150_kawaii1000_{entry['id'].replace('-', '_')}_"
f"{entry['lane']}_{entry['filenameScene']}"
```

- [ ] **Step 4: Implement validation and deterministic prompt compilation**

Validate exact property names, types, allowed enums, quotas, ordered IDs,
filename slug syntax, string non-emptiness, uniqueness, and reference count.
The compiler emits exactly nine paragraphs in the design’s order:

1. `scene` plus `conceptTitle`;
2. `cuteBeat`;
3. `wardrobe`;
4. `poseHandsGaze`;
5. expanded `composition` and `camera`;
6. expanded `lighting` and `dominantColor`;
7. `material` plus the global soft-skin paragraph;
8. explicit role and exclusion sentence for every active reference;
9. only `targetedAvoid` plus the global output invariants.

The fixed identity/output sentence is:

```text
One full-frame illustration of young adult Akari in her early twenties:
short airy chestnut bob, clear amber eyes, and one complete character-left
pale-blue crossed-pin and thin-cord ornament. Preserve v1.5 body balance and
healthy thigh volume, soft hand-painted planes, deliberate line hierarchy,
and a clean grain-free finish. No text, logos, watermarks, borders, collages,
or split panels.
```

The fixed skin sentence is:

```text
Visible skin has subtle warm variation at cheeks, ears, knees, and fingertips,
restrained highlights, firmer front and outer thigh planes, softer inner and
rear tissue, warm reflected shadow, no pore-level photorealism, oily gloss,
plastic smoothing, or hard muscle definition.
```

Reference roles come from the live reference manifest and must preserve its
exact `role`, `snapshotPath`, SHA-256, and `exclusions`. Active references are
always `v1.5-body-balance`, `v1.4-rendering`, then the row’s conditional IDs.
Reject more than four references.

Use this compilation structure:

```python
def _reference_sentence(reference: dict[str, object]) -> str:
    exclusions = ", ".join(reference["exclusions"])
    return (
        f"{reference['snapshotPath']} is used only as "
        f"{reference['role']}; exclude {exclusions}. "
        f"Expected SHA-256: {reference['sha256']}."
    )


def compile_prompt(
    entry: dict[str, object],
    references: list[dict[str, object]],
) -> str:
    reference_text = " ".join(
        _reference_sentence(reference) for reference in references
    )
    avoid_text = "; ".join(entry["targetedAvoid"])
    paragraphs = (
        f"{entry['scene']} Concept: {entry['conceptTitle']}.",
        str(entry["cuteBeat"]),
        str(entry["wardrobe"]),
        str(entry["poseHandsGaze"]),
        (
            f"Composition: {entry['composition']}. "
            f"Camera: {entry['camera']}."
        ),
        (
            f"Lighting: {entry['lighting']}. "
            f"Dominant colors: {entry['dominantColor']}."
        ),
        f"{entry['material']} {FIXED_SKIN_SENTENCE}",
        reference_text,
        f"{FIXED_IDENTITY_OUTPUT_SENTENCE} Targeted avoids: {avoid_text}.",
    )
    return "\n\n".join(paragraphs)
```

- [ ] **Step 5: Build pending manifest entries**

Map the matrix into the existing `validateBatchManifest` shape. The prompt is
the compiled prompt. Artifact paths are:

```text
batches/B001/images/<filenameStem>.png
batches/B001/thumbs/<filenameStem>.webp
```

Pending generation metadata is:

```json
{
  "toolMode": "built-in-imagegen",
  "generationId": null,
  "requestId": null,
  "sourcePath": null,
  "technicalStatus": "pending",
  "failureReason": null
}
```

Pending artifact metadata has null SHA-256, width, and height. Add tests that
write the manifest to a temporary data root and call:

```bash
node --input-type=module -e \
  'import {readFileSync} from "node:fs";
   import {validateBatchManifest} from "./tools/review-gallery/manifest.mjs";
   validateBatchManifest(JSON.parse(readFileSync(process.argv[1], "utf8")));' \
  <temporary-manifest>
```

- [ ] **Step 6: Verify GREEN and commit**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_5_b001_contract -v
node --test --test-concurrency=1 tools/review-gallery/manifest.test.mjs
```

Expected: PASS.

Commit:

```bash
git add akari-v1.5/generation/b001-request-matrix.json \
  scripts/akari_v1_5_b001_contract.py \
  tests/test_akari_v1_5_b001_contract.py
git commit -m "Add Akari B001 request matrix"
```

### Task 2: Resume-Safe B001 State and CLI

**Files:**

- Create: `scripts/akari_v1_5_b001_state.py`
- Create: `scripts/manage_akari_v1_5_b001.py`
- Create: `tests/test_akari_v1_5_b001_state.py`

**Interfaces:**

- Consumes: matrix path, data root, image ID, optional generated source PNG,
  generation ID, request ID, and failure reason.
- Produces:
  `prepare_b001(matrix_path, data_root, archive_root) -> Path`,
  `record_success(...) -> dict[str, object]`,
  `record_failure(...) -> Path`,
  `reconcile_b001(...) -> dict[str, object]`,
  `b001_status(...) -> dict[str, object]`, and
  `summarize_b001_reviews(...) -> dict[str, object]`.

- [ ] **Step 1: Write failing persistence tests**

Test these behaviors with real Pillow PNGs:

- `prepare_b001` creates the external directory structure, pending
  `manifest.json`, and fifty revision-zero `reviews.json` entries.
- Re-running prepare with the same matrix fingerprint is byte-idempotent.
- A changed matrix fingerprint is rejected before mutation.
- `record_success` rejects a non-PNG, a damaged PNG, an unknown ID, and a
  SHA-256 already present in the ledger.
- A valid result creates one immutable PNG, one WebP, and one receipt; updates
  exactly that manifest entry to `valid`; and increments
  `acceptedProductionImages` exactly once.
- Re-recording the same ID/source is idempotent; a different source for the
  completed ID is rejected without overwrite.
- A simulated crash after PNG install, after thumbnail install, and after
  receipt write is repaired by `reconcile_b001`.
- A failure attempt increments `technicalFailures` but leaves the intended ID
  pending or failed and eligible for the same prompt retry.
- Reconcile preserves ledger entries belonging to batches other than B001.
- Prior-coverage indexing scans the pre-existing generated archive while
  excluding the active `v1.5-1000` data root, records relative filenames and
  any available novelty metadata, never changes archive files, and is
  idempotent.
- Review summary rejects any `unreviewed` record and, once complete, returns
  counts, reason totals, favorite IDs, keep IDs, reject IDs, and notes.

- [ ] **Step 2: Verify RED**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_5_b001_state -v
```

Expected: FAIL because the state module does not exist.

- [ ] **Step 3: Implement durable preparation**

Calculate `matrixFingerprint` as SHA-256 of canonical compact JSON with sorted
keys. `prepare_b001` verifies reference hashes, then creates directories with
mode-safe ordinary directory operations and refuses symlinks at `batches`,
`B001`, and every owned child. It accepts
`archive_root=/home/takahiro/workspace/akari_generated`, excludes the resolved
active data root, and atomically writes `state/prior-coverage.json` with source
root, scan time, sorted relative PNG names, and normalized novelty metadata
found in adjacent manifests. It rejects any full novelty key already present
in the production ledger or prior-coverage metadata. Archive images are never
returned as generation references.

Write JSON through a same-directory temporary file, flush, `os.fsync`, then
`os.replace`. After replacement, fsync the parent directory. The initial
manifest is the Task 1 pending manifest plus top-level
`matrixFingerprint`. Because the existing Node validator ignores additional
top-level metadata, its contract remains valid.

Use this durable JSON primitive for manifest, ledger, review, and receipt
documents:

```python
def _atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(
        f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
    )
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
```

The initial review document is:

```json
{
  "schemaVersion": 1,
  "batchId": "B001",
  "reviews": {
    "B001-001": {
      "status": "unreviewed",
      "reasons": [],
      "note": "",
      "revision": 0,
      "updatedAt": null
    }
  }
}
```

Never replace an existing non-empty review document during prepare or
reconcile.

- [ ] **Step 4: Implement attempts, immutable media, and receipts**

One failed attempt is an immutable JSON file in
`attempts/<imageId>/<six-digit-attempt>.json`:

```json
{
  "schemaVersion": 1,
  "batchId": "B001",
  "imageId": "B001-002",
  "promptSha256": "<compiled prompt hash>",
  "generationId": null,
  "requestId": null,
  "failureReason": "missing local PNG and no recoverable payload",
  "recordedAt": "<UTC ISO timestamp>"
}
```

One success receipt is:

```json
{
  "schemaVersion": 1,
  "batchId": "B001",
  "imageId": "B001-002",
  "matrixFingerprint": "<matrix hash>",
  "promptSha256": "<compiled prompt hash>",
  "generationId": "<string or null>",
  "requestId": "<string or null>",
  "sourcePath": "<absolute original generated location>",
  "imagePath": "batches/B001/images/<filenameStem>.png",
  "thumbnailPath": "batches/B001/thumbs/<filenameStem>.webp",
  "sha256": "<PNG hash>",
  "width": 1024,
  "height": 1536,
  "recordedAt": "<UTC ISO timestamp>"
}
```

For `record_success`:

1. run existing `inspect_png(source)`;
2. reject a hash already recorded for another production image;
3. install bytes with `os.open(..., O_CREAT | O_EXCL | O_WRONLY)`, flush, and
   fsync;
4. re-run `inspect_png` on the installed final;
5. build the thumbnail to a unique staging path, verify `RIFF....WEBP`, then
   install without overwrite;
6. atomically write the receipt as the commit point;
7. call `reconcile_b001`;
8. return the final valid manifest entry.

If a matching final PNG exists without a receipt, verify it against the source
or its own immutable metadata, finish the missing thumbnail/receipt, and
reconcile. Never unlink or rewrite a mismatched final.

The immutable install primitive is:

```python
def _install_exclusive(contents: bytes, destination: Path) -> None:
    descriptor = os.open(
        destination,
        os.O_CREAT | os.O_EXCL | os.O_WRONLY,
        0o644,
    )
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
```

- [ ] **Step 5: Implement deterministic reconciliation**

Receipts are authoritative for successful results. Rebuild each B001 manifest
entry from the matrix, then apply its receipt to generation/artifact metadata.
If the newest failure has no later success, use `technicalStatus: "failed"` and
its reason; the same ID remains the next retry target.

Rebuild only B001’s ledger entries, preserving all other batches. A ledger
success entry contains batch ID, image ID, novelty key, prompt hash, PNG hash,
artifact path, and reference hashes. Set `acceptedProductionImages` to the
number of unique successful production entries across the full ledger and
`technicalFailures` to the number of immutable failure receipts. Atomically
write manifest, then ledger; every CLI entry point starts with reconciliation,
so a crash between those writes converges on the next invocation.

The reconciliation loop has this shape:

```python
manifest = build_pending_manifest(matrix, reference_manifest)
manifest["matrixFingerprint"] = matrix_fingerprint(matrix)
b001_ledger_entries = []
for entry in manifest["entries"]:
    receipt = _read_valid_receipt(receipts_dir, entry["id"])
    failure = _latest_valid_failure(attempts_dir, entry["id"])
    if receipt is not None:
        _verify_receipt_media(data_root, entry, receipt)
        entry["generation"].update({
            "generationId": receipt["generationId"],
            "requestId": receipt["requestId"],
            "sourcePath": receipt["sourcePath"],
            "technicalStatus": "valid",
            "failureReason": None,
        })
        entry["artifact"].update({
            "sha256": receipt["sha256"],
            "width": receipt["width"],
            "height": receipt["height"],
        })
        b001_ledger_entries.append(_ledger_entry(entry, receipt))
    elif failure is not None:
        entry["generation"]["technicalStatus"] = "failed"
        entry["generation"]["failureReason"] = failure["failureReason"]

ledger["entries"] = [
    item for item in ledger["entries"] if item["batchId"] != "B001"
] + b001_ledger_entries
ledger["acceptedProductionImages"] = len(ledger["entries"])
ledger["technicalFailures"] = _count_failure_receipts(data_root)
_atomic_json(manifest_path, manifest)
_atomic_json(ledger_path, ledger)
```

Status output is stable JSON:

```json
{
  "batchId": "B001",
  "valid": 0,
  "failedAttempts": 0,
  "remaining": 50,
  "nextImageId": "B001-001",
  "complete": false
}
```

- [ ] **Step 6: Implement the thin CLI**

Exact examples:

```bash
uv run python scripts/manage_akari_v1_5_b001.py prepare \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --archive-root /home/takahiro/workspace/akari_generated

uv run python scripts/manage_akari_v1_5_b001.py prompt \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --image-id B001-001

uv run python scripts/manage_akari_v1_5_b001.py record-success \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --image-id B001-001 \
  --source /absolute/generated/result.png \
  --generation-id '<if exposed>' \
  --request-id '<if exposed>'

uv run python scripts/manage_akari_v1_5_b001.py record-failure \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --image-id B001-001 \
  --reason 'missing local PNG and no recoverable payload'
```

`prompt` prints JSON with `imageId`, `prompt`, `promptSha256`,
`referencedImagePaths`, `roles`, and `targetPath`. The first referenced path is
the B3 snapshot and is labeled current selected plus permanent identity/body
authority.

- [ ] **Step 7: Verify GREEN and commit**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_5_b001_state -v
uv run python -m unittest \
  tests.test_akari_v1_5_b001_contract \
  tests.test_akari_v1_5_b001_state -v
```

Expected: PASS.

Commit:

```bash
git add scripts/akari_v1_5_b001_state.py \
  scripts/manage_akari_v1_5_b001.py \
  tests/test_akari_v1_5_b001_state.py
git commit -m "Add resume-safe Akari B001 state"
```

### Task 3: Rollout Recovery and B001 Gate

**Files:**

- Create: `scripts/recover_akari_imagegen_payload.py`
- Create: `tests/test_recover_akari_imagegen_payload.py`
- Modify: `package.json`
- Modify: `tests/test_workflow_gate_contract.py`

**Interfaces:**

- Consumes: one rollout JSONL, one image-generation call ID or ordinal, and an
  external staging output path.
- Produces:
  `recover_png(rollout_path, output_path, call_id=None, ordinal=None) -> Path`
  and npm script `gate:v1-5:b001`.

- [ ] **Step 1: Write failing structural-recovery tests**

Use synthetic JSONL containing unrelated assistant events, one invalid
`image_generation_call`, and two valid PNG base64 payloads. Assert explicit
call-ID selection, explicit ordinal selection, rejection of ambiguous default
selection, PNG signature verification, exclusive output creation, and refusal
to overwrite an existing staging file.

- [ ] **Step 2: Verify RED**

Run:

```bash
uv run python -m unittest tests.test_recover_akari_imagegen_payload -v
```

Expected: FAIL because the recovery module does not exist.

- [ ] **Step 3: Implement structural JSONL recovery**

Parse each line with `json.loads`; recursively inspect JSON objects but select
only objects whose `type` equals `image_generation_call` and whose `result`
starts with `iVBOR`. Decode with strict base64 validation, require PNG
signature `89504e470d0a1a0a`, and write with exclusive creation under the
caller-supplied external `staging/` path. Never print the payload.

Use an iterative structural walk so large payloads are never copied into
terminal text:

```python
def _walk(value: object):
    stack = [value]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            yield current
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)


def _payloads(rollout_path: Path):
    with rollout_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            value = json.loads(line)
            for item in _walk(value):
                result = item.get("result")
                if (
                    item.get("type") == "image_generation_call"
                    and isinstance(result, str)
                    and result.startswith("iVBOR")
                ):
                    yield line_number, item, result
```

CLI:

```bash
uv run python scripts/recover_akari_imagegen_payload.py \
  --rollout "$CODEX_HOME/sessions/YYYY/MM/DD/rollout-....jsonl" \
  --call-id '<image generation call id>' \
  --output /home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/staging/B001-001-recovered.png
```

- [ ] **Step 4: Add the focused B001 gate**

Set:

```json
{
  "test:python:b001": "uv run python -m unittest tests.test_akari_v1_5_b001_contract tests.test_akari_v1_5_b001_state tests.test_recover_akari_imagegen_payload -v",
  "gate:v1-5:b001": "npm run test:python:b001 && node --test --test-concurrency=1 tools/review-gallery/manifest.test.mjs tools/review-gallery/server.test.mjs && npm run lint:md"
}
```

Extend the workflow contract test with those exact values and assert the B001
gate contains no PDF, OCR, Poppler, Tesseract, image-generation, or public-bind
command.

- [ ] **Step 5: Verify GREEN and commit**

Run:

```bash
uv run python -m unittest tests.test_recover_akari_imagegen_payload -v
uv run python -m unittest tests.test_workflow_gate_contract -v
bash -lc 'npm run gate:v1-5:b001'
```

Expected: PASS.

Commit:

```bash
git add scripts/recover_akari_imagegen_payload.py \
  tests/test_recover_akari_imagegen_payload.py \
  package.json tests/test_workflow_gate_contract.py
git commit -m "Add Akari B001 generation gate"
```

### Task 4: Real B001 Preflight Without Generation

**Files:**

- External only:
  `/home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/`

**Interfaces:**

- Consumes: Tasks 1 through 3 and the live immutable reference snapshot.
- Produces: one structurally valid pending B001 manifest and empty review state.

- [ ] **Step 1: Reinstall the live service from canonical integrated code**

If the service still references a feature worktree, stop here until the
foundation branch is integrated. Then run the existing installer with:

```bash
uv run python scripts/install_akari_review_gallery_service.py \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --host 100.125.117.75 \
  --port 8787 \
  --install
```

Assert the unit `ExecStart` contains no `.worktrees/`.

- [ ] **Step 2: Run the B001 gate**

Run:

```bash
bash -lc 'npm run gate:v1-5:b001'
```

Expected: PASS before any generation call.

- [ ] **Step 3: Prepare B001**

Run the `prepare` CLI from Task 2. Expected status is exactly:

```json
{
  "batchId": "B001",
  "valid": 0,
  "failedAttempts": 0,
  "remaining": 50,
  "nextImageId": "B001-001",
  "complete": false
}
```

- [ ] **Step 4: Validate the pending manifest and gallery**

Run:

```bash
node --input-type=module -e \
  'import {readFileSync} from "node:fs";
   import {validateBatchManifest} from "./tools/review-gallery/manifest.mjs";
   const path="/home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/manifest.json";
   const value=validateBatchManifest(JSON.parse(readFileSync(path,"utf8")));
   console.log(value.batchId, value.entries.length);'

curl --fail --silent http://100.125.117.75:8787/api/batches \
  | jq '.data.batches[] | select(.batchId=="B001")'
```

Expected: B001 has fifty pending entries, 0/50 reviewed, and is not ready.
No media exists yet and no image-generation call has occurred.

## Mandatory Per-Image Generation Protocol

Every ID in Tasks 5 through 14 executes these steps in order. Do not batch
tool calls or skip the per-image checks.

The reference-role/exclusion contract for every call is:

- `v1.5-body-balance`: current selected candidate and permanent v1.5 identity,
  face, hair, ornament, and body-balance authority; exclude its outfit, pose,
  and background.
- `v1.4-rendering`: permanent eyes, skin, hair-plane, line-hierarchy, palette,
  and clean-finish authority; exclude its body balance, pose, and background.
- `v1.4-action`: hands and action continuity only; exclude identity, outfit,
  and background.
- `v1.4-seated`: seated anatomy and weight distribution only; exclude
  identity, outfit, and background.
- `neesocks-pressure-study`: anatomy and hosiery pressure only; exclude
  identity, composition, underwear, outfit, and color.

1. Run `status`; its `nextImageId` must equal the intended ID.
2. Run `prompt --image-id <ID>` and retain its exact JSON.
3. Open every `referencedImagePaths` item with `view_image`. Describe each
   role to the built-in call exactly as compiled. The B3 snapshot is the
   current selected candidate plus identity/body authority; G2 is the
   rendering/skin authority; conditional roles and exclusions come from the
   reference manifest.
4. Call `image_gen` once for that ID with the compiled prompt verbatim and the
   exact opened paths in `referenced_image_paths`.
5. If a local PNG path is returned, pass it to `record-success`. If no local
   path exists, use Task 3 rollout recovery, then pass the recovered PNG.
   If neither path works, call `record-failure` and retry the same ID with the
   same prompt; do not advance.
6. Assert the returned entry is `technicalStatus: valid`, the PNG and WebP
   exist, `inspect_png` succeeds, the receipt hash matches the immutable PNG,
   and the status advances by one.
7. Open the saved PNG for technical inspection only. A valid image is not
   regenerated for subjective weakness; identity, cuteness, garment, anatomy,
   and material judgments belong to the gallery human-review gate.

### Task 5: Generate Lane 1 — Classic School Uniform

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-001` through
`B001-005`.

- [ ] Generate `B001-001` — Courtyard schedule dash — with the mandatory protocol.
- [ ] Generate `B001-002` — Library ribbon adjustment — with the mandatory protocol.
- [ ] Generate `B001-003` — Classroom tab sorting — with the mandatory protocol.
- [ ] Generate `B001-004` — Platform lanyard catch — with the mandatory protocol.
- [ ] Generate `B001-005` — Rooftop notebook relief — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 5`, `nextImageId: B001-006`, and validate the manifest structurally.

### Task 6: Generate Lane 2 — Professional and Service Uniform

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-006` through
`B001-010`.

- [ ] Generate `B001-006` — Bakery madeleine presentation — with the mandatory protocol.
- [ ] Generate `B001-007` — Florist bouquet untangle — with the mandatory protocol.
- [ ] Generate `B001-008` — Bookstore bookplate stamp — with the mandatory protocol.
- [ ] Generate `B001-009` — Hotel key-tag stop — with the mandatory protocol.
- [ ] Generate `B001-010` — Workshop shaving brush-off — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 10`, `nextImageId: B001-011`, and validate the manifest structurally.

### Task 7: Generate Lane 3 — Sports, Ceremony, and Fictional Uniform

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-011` through
`B001-015`.

- [ ] Generate `B001-011` — Boathouse pennant lift — with the mandatory protocol.
- [ ] Generate `B001-012` — Fencing glove hesitation — with the mandatory protocol.
- [ ] Generate `B001-013` — Star-map alignment — with the mandatory protocol.
- [ ] Generate `B001-014` — Choir folio catch — with the mandatory protocol.
- [ ] Generate `B001-015` — Glasshouse field-pouch relief — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 15`, `nextImageId: B001-016`, and validate the manifest structurally.

### Task 8: Generate Lane 4 — Everyday Girly

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-016` through
`B001-020`.

- [ ] Generate `B001-016` — Strawberry basket turn — with the mandatory protocol.
- [ ] Generate `B001-017` — Sleeve-hidden compliment — with the mandatory protocol.
- [ ] Generate `B001-018` — Needle threading focus — with the mandatory protocol.
- [ ] Generate `B001-019` — Entryway scarf catch — with the mandatory protocol.
- [ ] Generate `B001-020` — Curtain-peek tease — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 20`, `nextImageId: B001-021`, and validate the manifest structurally.

### Task 9: Generate Lane 5 — Outings and Special Days

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-021` through
`B001-025`.

- [ ] Generate `B001-021` — Parfait arrival lean — with the mandatory protocol.
- [ ] Generate `B001-022` — Reversed cinema ticket — with the mandatory protocol.
- [ ] Generate `B001-023` — Record sleeve comparison — with the mandatory protocol.
- [ ] Generate `B001-024` — Gallery umbrella pop — with the mandatory protocol.
- [ ] Generate `B001-025` — Winter bridge cocoa — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 25`, `nextImageId: B001-026`, and validate the manifest structurally.

### Task 10: Generate Lane 6 — Hobbies and Making

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-026` through
`B001-030`.

- [ ] Generate `B001-026` — Successful soufflé lift — with the mandatory protocol.
- [ ] Generate `B001-027` — Escaping thread spool — with the mandatory protocol.
- [ ] Generate `B001-028` — Camera focus ring — with the mandatory protocol.
- [ ] Generate `B001-029` — Piano folio elbow save — with the mandatory protocol.
- [ ] Generate `B001-030` — Soil-smudge relief — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 30`, `nextImageId: B001-031`, and validate the manifest structurally.

### Task 11: Generate Lane 7 — Travel and Walking

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-031` through
`B001-035`.

- [ ] Generate `B001-031` — Departure-board turn — with the mandatory protocol.
- [ ] Generate `B001-032` — Ferry hat-ribbon hold — with the mandatory protocol.
- [ ] Generate `B001-033` — Train route tracing — with the mandatory protocol.
- [ ] Generate `B001-034` — Coastal splash sidestep — with the mandatory protocol.
- [ ] Generate `B001-035` — Observation-deck arrival — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 35`, `nextImageId: B001-036`, and validate the manifest structurally.

### Task 12: Generate Lane 8 — Retro and Storybook

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-036` through
`B001-040`.

- [ ] Generate `B001-036` — Found postcard offer — with the mandatory protocol.
- [ ] Generate `B001-037` — Shared float straw bump — with the mandatory protocol.
- [ ] Generate `B001-038` — Conservatory cipher — with the mandatory protocol.
- [ ] Generate `B001-039` — Theater lantern flicker — with the mandatory protocol.
- [ ] Generate `B001-040` — Tiny music-box reveal — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 40`, `nextImageId: B001-041`, and validate the manifest structurally.

### Task 13: Generate Lane 9 — Magic, Fantasy, and Science Fiction

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-041` through
`B001-045`.

- [ ] Generate `B001-041` — Orbiting star cradle — with the mandatory protocol.
- [ ] Generate `B001-042` — Orbital cuff greeting — with the mandatory protocol.
- [ ] Generate `B001-043` — Luminous seed inspection — with the mandatory protocol.
- [ ] Generate `B001-044` — Holographic pet landing — with the mandatory protocol.
- [ ] Generate `B001-045` — Floating-door compass — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 45`, `nextImageId: B001-046`, and validate the manifest structurally.

### Task 14: Generate Lane 10 — Subculture and Wildcards

**Files:** External B001 runtime only.

**Interfaces:** Produces valid receipts/media for `B001-046` through
`B001-050`.

- [ ] Generate `B001-046` — Dessert-studio cake share — with the mandatory protocol.
- [ ] Generate `B001-047` — Backward band badge — with the mandatory protocol.
- [ ] Generate `B001-048` — One-charm selection — with the mandatory protocol.
- [ ] Generate `B001-049` — Laundromat bubble surprise — with the mandatory protocol.
- [ ] Generate `B001-050` — Dawn rooftop cleanup — with the mandatory protocol.
- [ ] Run `reconcile`, assert `valid: 50`, `remaining: 0`, `nextImageId: null`, and `complete: true`.

### Task 15: Final Technical Batch Gate

**Files:** External B001 runtime only.

**Interfaces:** Consumes all fifty receipts and produces a technically complete
B001 visible in the existing gallery.

- [ ] **Step 1: Reconcile and validate every declared file**

Run:

```bash
uv run python scripts/manage_akari_v1_5_b001.py reconcile \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000

node --input-type=module -e \
  'import {readFileSync} from "node:fs";
   import {validateBatchManifest} from "./tools/review-gallery/manifest.mjs";
   const root="/home/takahiro/workspace/akari_generated/v1.5-1000";
   const path=`${root}/batches/B001/manifest.json`;
   const value=validateBatchManifest(
     JSON.parse(readFileSync(path,"utf8")),
     {dataRoot:root,checkFiles:true},
   );
   console.log(JSON.stringify({batchId:value.batchId,entries:value.entries.length}));'
```

Expected: `{"batchId":"B001","entries":50}`.

- [ ] **Step 2: Prove count, uniqueness, quotas, and immutability**

Use the management status and manifest to assert:

- fifty receipts, PNGs, and WebPs;
- fifty distinct PNG SHA-256 values;
- no receipt or artifact path outside B001;
- `acceptedProductionImages` increased by exactly fifty from its pre-B001
  value;
- technical failure receipts do not increase the accepted count;
- five rows per lane;
- texture distribution 5/2/1/1/1;
- five subculture rows;
- cast distribution 35/5/5/5;
- scene distribution 40/10;
- all compiled prompt hashes and reference hashes match receipts.

- [ ] **Step 3: Exercise live gallery media**

Run:

```bash
curl --fail --silent http://100.125.117.75:8787/api/batches \
  | jq '.data.batches[] | select(.batchId=="B001")'
curl --fail --silent --output /dev/null \
  http://100.125.117.75:8787/media/B001/B001-001/thumb
curl --fail --silent --output /dev/null \
  http://100.125.117.75:8787/media/B001/B001-050/image
```

Expected: B001 is enabled, 0/50 reviewed, not ready, and both media requests
return 200.

- [ ] **Step 4: Run serial gates**

Run:

```bash
bash -lc 'npm run gate:v1-5:b001'
bash -lc 'npm run gate:integration:all'
git diff --check
git status --short --branch
```

Expected: PASS; external generated data is absent from Git.

### Task 16: Human Review and B002 Planning Handoff

**Files:**

- External review state:
  `/home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/reviews.json`
- Create after review:
  `docs/superpowers/plans/<execution-date>-akari-v1-5-b002-generation.md`

**Interfaces:**

- Consumes: technically complete B001, existing gallery, and all fifty human
  review records.
- Produces: complete B001 review evidence and a separate, feedback-controlled
  B002 implementation plan. Produces no B002 image.

- [ ] **Step 1: Review all fifty images in the existing gallery**

Open `http://100.125.117.75:8787` on desktop and a mobile tailnet device.
Rate every B001 image `reject`, `keep`, or `favorite`; apply only the existing
reject reasons and optional notes. Verify full outfit readability, Akari
identity and adult impression, cute beat, anatomy/hands, composition,
garment/material behavior, and the ten texture rows’ pressure/tissue behavior.

Do not replace rejected but technically valid images. The technical count
remains fifty.

- [ ] **Step 2: Verify review persistence and readiness**

Before and after:

```bash
sha256sum \
  /home/takahiro/workspace/akari_generated/v1.5-1000/batches/B001/reviews.json
systemctl --user restart akari-review-gallery.service
curl --retry 5 --retry-connrefused --retry-delay 1 --fail --silent \
  http://100.125.117.75:8787/api/batches/B001/reviews
```

Expected: every record remains rated at its latest monotonic revision and the
batch summary is `reviewed: 50`, `total: 50`, `ready: true`.

- [ ] **Step 3: Produce the deterministic feedback summary**

Run:

```bash
uv run python scripts/manage_akari_v1_5_b001.py review-summary \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000
```

Expected: JSON with 50 reviewed entries, status totals, reason totals,
favorites, keeps, rejects, notes, and lane/texture cross-tabs. The command
must fail if any record is unreviewed.

- [ ] **Step 4: Write the separate B002 implementation plan**

Invoke `superpowers:writing-plans`. The B002 plan must:

- preserve five rows per lane and the same batch quotas;
- use one winning element from a favorite at most once per new request;
- change at least three of outfit, setting, action, and camera for every
  favorite-derived request;
- strengthen identity/age wording only in lanes with those reject reasons;
- strengthen anatomy/material wording or conditional references only for the
  affected concepts;
- ban novelty combinations rejected as duplicate;
- reduce combinations associated with `not-cute`;
- define a new explicit B002 fifty-row request matrix before generation;
- reuse the tested persistence/generation protocol without creating a new
  gallery or browser generation feature;
- stop after planning and generate no B002 image.

- [ ] **Step 5: Validate and commit only the B002 plan**

Run:

```bash
npm run lint:md
rg -ni 'T''BD|TO''DO|fill'' in|place''holder|appro''priate|similar'' to' \
  docs/superpowers/plans/<execution-date>-akari-v1-5-b002-generation.md
git diff --check
```

Expected: Markdown PASS and the unresolved-marker scan returns no matches. Commit only
the tracked B002 plan; the external review/generated tree remains untracked.

## Plan Self-Review Checklist

- Spec coverage: matrix, references, prompt order, independent calls,
  technical counting, recovery, review persistence, feedback control, and B002
  planning each map to a named task.
- Creative completeness: every B001 ID has a concrete scene, wardrobe,
  setting, action, cute beat, pose/hands/gaze, camera, lighting, cast, palette,
  material direction, texture allocation, conditional reference set, and
  targeted avoid list.
- Quota consistency: 50 total; 5 per lane; 10 texture; 5 subculture; 35 solo,
  5 viewer-POV, 5 two-person, 5 group; 40 action/reaction and 10 quiet posed.
- Type consistency: the matrix properties, compiler outputs, pending manifest,
  receipt fields, ledger fields, CLI subcommands, and final Node manifest shape
  use the same names throughout.
- Scope: no new application, browser generation feature, PDF, B002 image, or
  generated Git asset is introduced.
- Unresolved-marker scan: no implementation instruction relies on an executor
  inventing a concept or filling an unspecified field.

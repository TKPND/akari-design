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
- Generated PNGs, thumbnails, receipts, attempts, manifests, reviews, recovery
  staging, prepared metadata, same-directory prepared files, and novelty state
  live only under
  `/home/takahiro/workspace/akari_generated/v1.5-1000/`.
- Never commit generated images or external state. Never overwrite an existing
  final PNG, thumbnail, receipt, manifest with a different batch-intent
  fingerprint, or reference snapshot.
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
└── batches/
    ├── B001.lock
    ├── B001.boundary.json
    └── B001/
        ├── attempts/
        ├── images/
        ├── receipts/
        ├── staging/  # Rollout-recovery sources only
        ├── thumbs/
        ├── intent-lock.json
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
- `OwnedBatchFs` in `akari_v1_5_b001_state.py` pins every owned directory and
  file operation to no-follow directory descriptors for one CLI invocation;
  no owned runtime mutation re-resolves an absolute `Path`.
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
  `reference_records(entry: dict[str, object], reference_manifest:
  dict[str, object]) -> list[dict[str, object]]`,
  `resolve_reference_paths(references_dir_fd: int, data_root_display: Path,
  references: list[dict[str, object]]) -> list[PinnedReference]`,
  `compile_prompt(entry: dict[str, object], references:
  list[dict[str, object]]) -> str`,
  `build_batch_intent(matrix: dict[str, object], reference_manifest:
  dict[str, object]) -> dict[str, object]`, and
  `build_pending_manifest(batch_intent: dict[str, object]) ->
  dict[str, object]`.

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
uses of one `action`, unique existing `noveltyKey` field tuples, no ASCII or
Unicode ellipsis in any creative string, every required prose field non-empty,
and no string matching the case-insensitive unresolved-marker expression
assembled in the test from
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

The “Exact B001 Creative Matrix” section in this plan is the authority for all
fifty final rows. The executor mechanically copies its exact wardrobe,
cute-beat, pose/hands/gaze, targeted-avoid prose and exact novelty-axis values
into JSON. For `wardrobe`, copy the words after `wardrobe is`; for `cuteBeat`,
copy the text inside its code span after the equals sign; for
`poseHandsGaze`, copy the words after `pose/hands/gaze:`. Collapse Markdown
line wrapping to one space and omit only terminal sentence punctuation
outside a code span. Preserve word choice, case, and order. The executor must
not invent, summarize, localize, capitalize, add a subject to, or paraphrase a
creative clause.

Each entry has exactly these matrix-owned properties. These three fully
concrete rows demonstrate the literal transcription for an action row, a
texture row, and a quiet group row:

```json
[
  {
    "id": "B001-001",
    "filenameScene": "courtyard-schedule-dash",
    "lane": "classic-school-uniform",
    "conceptTitle": "Courtyard schedule dash",
    "cuteBeat": "leans forward with sudden happiness after finding the right room",
    "wardrobeFamily": "navy-blazer-burgundy-ribbon",
    "wardrobe": "a navy adult-academy blazer, ivory rounded-collar blouse, burgundy ribbon, charcoal knee-length pleated skirt, and brown loafers",
    "setting": "adult-academy-courtyard",
    "action": "jogs-with-windblown-schedule",
    "sceneMode": "action-reaction",
    "composition": "full-body-forward-motion",
    "camera": "eye-level-front-three-quarter-50mm",
    "lighting": "clear-morning-open-shade",
    "cast": "solo",
    "dominantColor": "navy-burgundy-ivory",
    "textureFocus": false,
    "textureType": "none",
    "subculture": false,
    "poseHandsGaze": "one hand secures the schedule, the other balances her stride, gaze toward the doorway",
    "conditionalReferenceIds": ["v1.4-action"],
    "targetedAvoid": [
      "fashion-catalog stillness",
      "copied B3 apartment"
    ]
  },
  {
    "id": "B001-002",
    "filenameScene": "library-ribbon-adjustment",
    "lane": "classic-school-uniform",
    "conceptTitle": "Library ribbon adjustment",
    "cuteBeat": "becomes visibly embarrassed when she notices the crooked bow",
    "wardrobeFamily": "cream-cardigan-sailor-collar",
    "wardrobe": "a cream cardigan, navy sailor collar, muted blue pleated skirt, dark over-knee socks, and oxford shoes",
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
    "poseHandsGaze": "both hands lightly retie the bow, knees relaxed, gaze briefly down and aside",
    "conditionalReferenceIds": [
      "v1.4-action",
      "neesocks-pressure-study"
    ],
    "targetedAvoid": [
      "uniform rubber-ring compression",
      "isolated leg framing"
    ]
  },
  {
    "id": "B001-050",
    "filenameScene": "dawn-rooftop-cleanup",
    "lane": "subculture-wildcard",
    "conceptTitle": "Dawn rooftop cleanup",
    "cuteBeat": "shares a calm relieved smile with friends after cleanup",
    "wardrobeFamily": "angelcore-knit-sheerlayer-skirt",
    "wardrobe": "an ivory angelcore knit, pale-blue long skirt with an opaque lining and soft sheer outer layer, gray tights, and ivory flats",
    "setting": "rooftop-picnic-at-dawn",
    "action": "rests-after-folding-picnic-cloth",
    "sceneMode": "quiet-posed",
    "composition": "small-group-seated-wide",
    "camera": "eye-level-side-three-quarter-65mm",
    "lighting": "pale-dawn-backlight",
    "cast": "group",
    "dominantColor": "ivory-paleblue-gray",
    "textureFocus": false,
    "textureType": "none",
    "subculture": true,
    "poseHandsGaze": "Akari sits with natural weight on a bench, folded cloth in her lap, friends nearby, gaze toward sunrise",
    "conditionalReferenceIds": ["v1.4-seated"],
    "targetedAvoid": [
      "translucent underwear",
      "angel wings",
      "religious symbols"
    ]
  }
]
```

Transcribe every decision in “Exact B001 Creative Matrix” without weakening
specific nouns into generic labels. `cuteBeat`, `wardrobe`, and
`poseHandsGaze` are exact English prompt fragments, not tags or invitations
for rewriting. The contract test embeds and compares the normalized literal
values for all fifty rows, not only the three representative rows above.
Settings, actions, composition, camera, lighting, and colors retain the exact
canonical slugs in the plan; the compiler humanizes a slug only by replacing
hyphens with spaces. Construct
`filenameStem` in code as:

```python
f"akari_v150_kawaii1000_{entry['id'].replace('-', '_')}_"
f"{entry['lane']}_{entry['filenameScene']}"
```

- [ ] **Step 4: Implement validation and deterministic prompt compilation**

Validate exact property names, types, allowed enums, quotas, ordered IDs,
filename slug syntax, string non-emptiness, uniqueness, no ASCII `\u002e`
repeated three times, no Unicode `\u2026`, and reference count. Require the
matrix, reference manifest, batch-intent, and pending-manifest schema versions
to equal their declared module constants.
The compiler emits exactly nine paragraphs in the design’s order:

1. a fixed scene sentence from humanized `setting` and `action`, plus
   `conceptTitle`;
2. `cuteBeat`;
3. `wardrobe`;
4. `poseHandsGaze`;
5. expanded `composition` and `camera`;
6. expanded `lighting` and `dominantColor`;
7. fixed material text selected by `textureType`, plus the global soft-skin
   paragraph;
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

The exact compiler fields and material constants are:

```python
PROMPT_TEMPLATE_FIELDS = (
    "scene-action-concept",
    "cuteBeat",
    "wardrobe",
    "poseHandsGaze",
    "composition-camera",
    "lighting-dominantColor",
    "material-skin",
    "reference-contract",
    "identity-output-avoids",
)

MATERIAL_BY_TEXTURE = {
    "none": (
        "Render every named garment material with distinct weave, weight, "
        "fold scale, edge response, and restrained highlights; avoid one "
        "generic plastic fabric treatment."
    ),
    "over-knee-socks": (
        "Over-knee knit stays visibly separate from skin, carries plausible "
        "vertical and circumferential tension, and its band sinks unevenly "
        "into soft tissue with a small rounded transition above it, never a "
        "uniform rubber-ring groove."
    ),
    "tights-stockings": (
        "Tights or stockings read as a thin continuous textile layer with "
        "subtle tension and value shift over form, never painted-on color or "
        "plastic gloss."
    ),
    "knee-high-socks": (
        "Knee-high rib knit shows believable stretch, fold recovery, and a "
        "soft nonuniform band transition without cutting a hard groove."
    ),
    "crew-ankle-socks": (
        "Crew or ankle sock ribbing, cuff pressure, and shoe contact remain "
        "locally readable without becoming the composition focus."
    ),
    "bare-contact": (
        "Bare-skin contact with seat or clothing shows gentle flattening, "
        "warm occlusion, and continuous anatomy without hard dents."
    ),
}
```

Reference roles come from the live reference manifest and must preserve its
exact `role`, `snapshotPath`, SHA-256, and `exclusions`. Active references are
always `v1.5-body-balance`, `v1.4-rendering`, then the row’s conditional IDs.
Reject more than four references.

Define `BATCH_INTENT_SCHEMA_VERSION = 1`,
`PENDING_MANIFEST_SCHEMA_VERSION = 1`,
`REFERENCE_MANIFEST_SCHEMA_VERSION = 1`,
`PROMPT_CONTRACT_VERSION = 1`,
`PROMPT_TEMPLATE_FIELDS`, `FIXED_IDENTITY_OUTPUT_SENTENCE`,
`FIXED_SKIN_SENTENCE`, and all `MATERIAL_BY_TEXTURE` strings as module
constants. Their exact canonical JSON representation is part of the batch
intent in Task 2. There is no runtime prose rewriting.

`reference_records` returns ordered manifest records with relative paths only:

```json
{
  "id": "v1.5-body-balance",
  "snapshotPath": "references/akari-v1.5-b3-body-balance.png",
  "role": "v1.5 identity and body balance",
  "exclusions": ["outfit", "pose", "background"],
  "sha256": "e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734"
}
```

The pinned result type is:

```python
@dataclass(frozen=True)
class PinnedReference:
    display_path: Path
    fd: int
    sha256: str
```

The caller closes every returned descriptor in `finally`.
`resolve_reference_paths` is the only relative-to-absolute display boundary.
It receives the already pinned `<dataRoot>/references` descriptor from
`OwnedBatchFs`. For every ordered record it must:

1. reject an absolute, empty, dot, parent, Windows-rooted, or backslash path;
2. require the first lexical segment to be exactly `references`;
3. open every remaining directory component relative to the prior descriptor
   with `O_DIRECTORY | O_NOFOLLOW`, then the final name with
   `O_RDONLY | O_NOFOLLOW`;
4. require the pinned final descriptor to be a regular file, hash bytes from
   that descriptor, compare SHA-256 with the record, and preserve input order;
5. construct `display_path` only after descriptor verification, without using
   that path for validation or an owned mutation;
6. retain all final file descriptors until prompt JSON is emitted or intent
   compilation completes, and require two through four results.

The batch intent, prepared records, and final receipts store only the relative
`snapshotPath`. Manifest references store the same relative value under the
existing validator’s `path` key. The `prompt` command alone adds
`referencedImagePaths`, containing normalized absolute display strings from
the pinned results. It keeps reference and intent descriptors open until the
JSON has been completely written, then closes them in `finally`.

Add tests for absolute paths, lexical traversal, a symlinked file, a symlinked
parent, a directory in place of a file, missing files, a hash mismatch, wrong
order, one reference, five references, descriptor lifetime, a swap after
pinning, root containment, and the exact relative-versus-absolute output
split. The swap test proves hashing continues on the pinned inode and no
replacement path is opened.

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
    human_setting = str(entry["setting"]).replace("-", " ")
    human_action = str(entry["action"]).replace("-", " ")
    reference_text = " ".join(
        _reference_sentence(reference) for reference in references
    )
    avoid_text = "; ".join(entry["targetedAvoid"])
    paragraphs = (
        (
            f"Scene: {human_setting}. Current action: {human_action}. "
            f"Concept: {entry['conceptTitle']}."
        ),
        f"Cute beat: Akari {entry['cuteBeat']}.",
        f"Wardrobe: Akari wears {entry['wardrobe']}.",
        f"Pose, hands, and gaze: {entry['poseHandsGaze']}.",
        (
            f"Composition: {entry['composition']}. "
            f"Camera: {entry['camera']}."
        ),
        (
            f"Lighting: {entry['lighting']}. "
            f"Dominant colors: {entry['dominantColor']}."
        ),
        f"{MATERIAL_BY_TEXTURE[entry['textureType']]} {FIXED_SKIN_SENTENCE}",
        reference_text,
        f"{FIXED_IDENTITY_OUTPUT_SENTENCE} Targeted avoids: {avoid_text}.",
    )
    return "\n\n".join(paragraphs)
```

- [ ] **Step 5: Build the canonical batch intent and pending manifest**

`build_batch_intent` canonicalizes everything that may change a generated
result:

```python
intent_entries = []
for matrix_entry in matrix["entries"]:
    references = reference_records(matrix_entry, reference_manifest)
    compiled_prompt = compile_prompt(matrix_entry, references)
    filename_stem = filename_stem_for(matrix_entry)
    intent_entries.append({
        "id": matrix_entry["id"],
        "compiledPrompt": compiled_prompt,
        "promptSha256": hashlib.sha256(
            compiled_prompt.encode("utf-8")
        ).hexdigest(),
        "references": references,
        "imagePath": f"batches/B001/images/{filename_stem}.png",
        "thumbnailPath": f"batches/B001/thumbs/{filename_stem}.webp",
    })

batch_intent = {
    "schemaVersion": BATCH_INTENT_SCHEMA_VERSION,
    "batchId": "B001",
    "schemaContract": {
        "intentSchemaVersion": BATCH_INTENT_SCHEMA_VERSION,
        "matrixSchemaVersion": matrix["schemaVersion"],
        "pendingManifestSchemaVersion": PENDING_MANIFEST_SCHEMA_VERSION,
        "referenceManifestSchemaVersion": REFERENCE_MANIFEST_SCHEMA_VERSION,
    },
    "matrixContract": matrix,
    "compilerContract": {
        "promptContractVersion": PROMPT_CONTRACT_VERSION,
        "templateFields": list(PROMPT_TEMPLATE_FIELDS),
        "fixedIdentityOutputSentence": FIXED_IDENTITY_OUTPUT_SENTENCE,
        "fixedSkinSentence": FIXED_SKIN_SENTENCE,
        "materialByTexture": MATERIAL_BY_TEXTURE,
    },
    "entries": intent_entries,
}
```

Serialize this payload as UTF-8 canonical compact JSON with sorted object keys
and list order preserved. Its SHA-256 is `batchIntentFingerprint`. Tests assert
exactly fifty compiled prompts, fifty prompt hashes, two through four resolved
reference records per row, and one fingerprint change when an intent, matrix,
pending-manifest, or reference-manifest schema version, any matrix field,
compiler constant, template field, reference role, exclusion, relative path,
order, or SHA changes.

Map the matrix into the existing `validateBatchManifest` shape. The prompt is
the compiled prompt. The manifest uses `batchType: "production"` and copies
every novelty-axis property without renaming it. Its reference objects use the
validator’s `path` key, mechanically mapped from each locked record’s
`snapshotPath`; `role`, `exclusions`, and `sha256` remain byte-for-byte equal.
The batch intent and prepared/final receipts retain the canonical
`snapshotPath` name, while CLI prompt JSON exposes those same canonical
records as `referenceRecords`. Tests assert this deliberate boundary and reject
`snapshotPath` in a manifest reference or `path` in an intent/receipt
reference. Artifact paths are:

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

- Modify: `scripts/build_akari_review_thumbnail.py`
- Modify: `tests/test_build_akari_review_thumbnail.py`
- Create: `scripts/akari_v1_5_b001_state.py`
- Create: `scripts/manage_akari_v1_5_b001.py`
- Create: `tests/test_akari_v1_5_b001_state.py`

**Interfaces:**

- Consumes: matrix path, data root, image ID, optional generated source PNG,
  generation ID, request ID, and failure reason.
- Produces:
  `render_thumbnail_bytes(source: Path, max_edge: int = 512) -> bytes`,
  `render_thumbnail_bytes_from_fd(source_fd: int, max_edge: int = 512) ->
  bytes`,
  `OwnedBatchFs.pin_root(data_root: Path) -> OwnedBatchFs`,
  `OwnedBatchFs.pin_batch(mode: Literal["prepare", "mutate", "read"],
  batch_intent_fingerprint: str, intent_lock: dict[str, object] | None = None)
  -> None`,
  `OwnedBatchFs.write_staging_exclusive(name: str, contents: bytes) -> None`,
  `OwnedBatchFs.close() -> None`,
  `prepare_b001(matrix_path, data_root, archive_root) -> Path`,
  `record_success(matrix_path: Path, data_root: Path, image_id: str,
  source_path: Path | None, staging_name: str | None, generation_id: str |
  None, request_id: str | None) -> dict[str, object]`,
  `record_failure(matrix_path: Path, data_root: Path, image_id: str,
  failure_reason: str, generation_id: str | None, request_id: str | None) ->
  Path`,
  `reconcile_b001(matrix_path: Path, data_root: Path) ->
  dict[str, object]`,
  `b001_status(matrix_path: Path, data_root: Path) ->
  dict[str, object]`, and
  `summarize_b001_reviews(matrix_path: Path, data_root: Path) ->
  dict[str, object]`.

- [ ] **Step 1: Write failing persistence tests**

Test these behaviors with real Pillow PNGs:

- `prepare_b001` creates the external directory structure, pending
  `B001.lock`, `B001.boundary.json`, `intent-lock.json`, `manifest.json`, and
  fifty revision-zero `reviews.json` entries.
- Re-running prepare with the same batch intent is byte-idempotent, including
  `prior-coverage.json`.
- Changing the matrix, any of the four schema-version contracts,
  prompt-contract version, compiler constant, template order, reference role,
  exclusion, relative path, SHA, or reference order changes
  `batchIntentFingerprint` and is rejected before mutation.
- A receipt or prepared record from another fingerprint is rejected; a run
  cannot mix prompt or reference contracts.
- `record_success` rejects a non-PNG, a damaged PNG, an unknown ID, and a
  SHA-256 already present in the ledger.
- `record_success` rejects an absolute source whose opened descriptor resolves
  beneath the pinned data root, accepts a validated staging basename only
  through `staging_fd`, and rejects simultaneous external/staging/resume
  source modes.
- A valid result creates same-directory prepared PNG/WebP files, durably
  writes prepared metadata, commits each final with an atomic no-replace link,
  writes one final receipt, updates exactly that manifest entry to `valid`,
  and increments `acceptedProductionImages` exactly once.
- `render_thumbnail_bytes` returns a verified `RIFF`/`WEBP` payload without
  opening any destination; `build_thumbnail` delegates to it so thumbnail
  derivation remains owned by the existing module. The existing thumbnail
  tests assert the byte API has the same size bounds and decoded RGB result as
  the path API, and rejects the same invalid PNG inputs.
- `render_thumbnail_bytes_from_fd` reads a duplicated pinned descriptor,
  leaves the caller’s descriptor open, and returns the identical deterministic
  payload; the B001 state layer never reopens prepared media by absolute path.
- Re-recording the same ID/source is idempotent; a different source for the
  completed ID is rejected without overwrite.
- Inject crashes at `after_prepared_image_file_fsync`,
  `after_prepared_image_dir_fsync`, `after_prepared_thumb_file_fsync`,
  `after_prepared_thumb_dir_fsync`, and `after_prepared_record_fsync`.
  At every boundary before the prepared receipt is durable, restart safely
  removes only same-intent regular orphan stages and requires the source. At
  `after_prepared_record_fsync`, restart with `source_path=None` finishes from
  the durable receipt and prepared or already-linked media.
- Also inject crashes after image link plus directory fsync, thumbnail link
  plus directory fsync, final-receipt fsync, JSON temporary unlink before its
  directory fsync, and reconcile before prepared cleanup. Startup/reconcile
  removes only validated same-intent debris and converges to one receipt and
  count.
- Crash before the final link leaves no final file. Crash after a final link
  but before a final receipt recovers without the source. A mismatched
  pre-existing final, symbolic link, directory, or wrong hash is rejected
  without replacement.
- Thumbnail commit has the same no-overwrite, regular-file, non-symlink,
  prepared-hash, atomic-link, and directory-fsync assertions as the PNG.
- Every mutation test records an external sentinel directory and file hash.
  After pinning, replace the data root, `references`, `state`, `batches`,
  `batches/B001`, and each owned child in turn by a symlink or by renaming the
  pinned directory and installing an ordinary replacement. Inject the swap
  before each write/link/unlink/replace/list family; the operation must remain
  on the pinned inode or reject, and every external sentinel hash and directory
  listing must remain unchanged.
- On a fresh entry point after a completed prepare, a replaced ordinary B001
  directory fails the pinned `B001.boundary.json` device/inode check before
  mutation. A replaced `B001.lock`, missing boundary record, symlinked
  component, or malformed intent lock also fails closed.
- Parse the state, management CLI, and recovery modules with `ast`. Except for
  the single lexical `/` anchor and declared external read-only inputs, reject
  owned `Path.open`, `Path.mkdir`, `Path.unlink`, `Path.replace`, globbing, or
  any `os.open/stat/mkdir/link/unlink/replace` call missing its required
  `dir_fd`, `src_dir_fd`, or `dst_dir_fd` keyword. Assert every public
  mutation entry point constructs exactly one fresh `OwnedBatchFs`.
- Run two same-intent `prepare` processes against one pinned batches
  directory. Both fsync their private intent-lock temporary before attempting
  the no-replace link; exactly one creates `intent-lock.json`, the loser reads
  it through its pinned B001 descriptor, verifies canonical byte equality, and
  returns idempotent success. Repeat with different and malformed existing
  lock bytes and assert the loser rejects without changing either file.
- A failure attempt increments `technicalFailures` but leaves the intended ID
  pending or failed and eligible for the same prompt retry.
- Reconcile preserves ledger entries belonging to batches other than B001.
- Prior-coverage indexing scans the pre-existing generated archive while
  excluding the active `v1.5-1000` data root, records relative filenames and
  any available novelty metadata, never changes archive files, and is
  byte-idempotent; operational scan time is absent from authoritative JSON.
- Review summary rejects any `unreviewed` record and, once complete, returns
  counts, reason totals, favorite IDs, keep IDs, reject IDs, notes, exact
  per-lane status cross-tabs, and exact per-texture-type status cross-tabs.

For the cross-tab test, rate offset 0 in every lane `favorite`, offsets 1 and
2 `keep`, and offsets 3 and 4 `reject`, then assert:

```python
self.assertTrue(all(
    counts == {"favorite": 1, "keep": 2, "reject": 2}
    for counts in summary["byLane"].values()
))
self.assertEqual(
    {
        "over-knee-socks": {"favorite": 2, "keep": 3, "reject": 0},
        "tights-stockings": {"favorite": 1, "keep": 1, "reject": 0},
        "knee-high-socks": {"favorite": 1, "keep": 0, "reject": 0},
        "crew-ankle-socks": {"favorite": 0, "keep": 1, "reject": 0},
        "bare-contact": {"favorite": 0, "keep": 1, "reject": 0},
        "none": {"favorite": 6, "keep": 14, "reject": 20},
    },
    summary["byTextureType"],
)
```

- [ ] **Step 2: Verify RED**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_5_b001_state -v
```

Expected: FAIL because the state module does not exist.

- [ ] **Step 3: Implement durable preparation**

Every CLI invocation begins with a fresh `OwnedBatchFs.pin_root(data_root)`.
It requires an absolute lexical data-root path with no dot or parent
components, opens `/`, and walks each component with
`os.open(name, O_RDONLY | O_DIRECTORY | O_NOFOLLOW, dir_fd=parent_fd)`.
Intermediate descriptors close only after the next component is pinned. It
then pins `references`, `state`, and `batches` the same way. Absolute paths are
display/provenance values only after this point.

The caller reads `references/manifest.json` relative to the pinned
`references_fd`, resolves and hashes reference records through pinned file
descriptors, builds the complete Task 1 batch intent, and calculates
`batchIntentFingerprint` before any owned write. It then calls
`pin_batch`:

- `prepare` opens or exclusively creates regular `B001.lock` relative to
  `batches_fd`, takes `fcntl.flock(lock_fd, LOCK_EX)`, then creates or opens
  `B001` and its five child directories only through pinned parent
  descriptors;
- `mutate` requires the lock, B001, and all children to exist, takes
  `LOCK_EX`, creates nothing while pinning, and is used by `status` because it
  reconciles first;
- `read` requires the existing boundary and takes `LOCK_SH`; `prompt` and
  `review-summary` hold both this boundary and the reference descriptors until
  their output is complete.

The five child descriptors are `images_fd`, `thumbs_fd`, `receipts_fd`,
`attempts_fd`, and `staging_fd`. The context also retains `root_fd`,
`references_fd`, `state_fd`, `batches_fd`, `lock_fd`, and `batch_fd`.
Every open uses `O_NOFOLLOW`; directory opens also use `O_DIRECTORY`.
`fstat` must confirm regular files and directories. All descriptors remain
open until the entire public operation finishes and close in reverse order in
`finally`, including every exception path.

The abstraction has this concrete shape:

```python
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
OWNED_CHILDREN = ("images", "thumbs", "receipts", "attempts", "staging")


def _open_directory_at(parent_fd: int, name: str) -> int:
    descriptor = os.open(name, DIRECTORY_FLAGS, dir_fd=parent_fd)
    if not stat.S_ISDIR(os.fstat(descriptor).st_mode):
        os.close(descriptor)
        raise ValueError(f"not a directory: {name}")
    return descriptor


def _create_directory_at(parent_fd: int, name: str) -> int:
    try:
        os.mkdir(name, 0o755, dir_fd=parent_fd)
        os.fsync(parent_fd)
    except FileExistsError:
        pass
    return _open_directory_at(parent_fd, name)


def _open_batch_lock_at(batches_fd: int, create: bool) -> int:
    flags = os.O_RDWR | os.O_NOFOLLOW
    if not create:
        return os.open("B001.lock", flags, dir_fd=batches_fd)
    try:
        descriptor = os.open(
            "B001.lock",
            flags | os.O_CREAT | os.O_EXCL,
            0o600,
            dir_fd=batches_fd,
        )
        try:
            os.fsync(batches_fd)
            return descriptor
        except BaseException:
            os.close(descriptor)
            raise
    except FileExistsError:
        return os.open("B001.lock", flags, dir_fd=batches_fd)


@dataclass
class OwnedBatchFs:
    display_root: Path
    descriptors: list[int]
    root_fd: int
    references_fd: int
    state_fd: int
    batches_fd: int
    lock_fd: int | None = None
    batch_fd: int | None = None
    images_fd: int | None = None
    thumbs_fd: int | None = None
    receipts_fd: int | None = None
    attempts_fd: int | None = None
    staging_fd: int | None = None

    @classmethod
    def pin_root(cls, data_root: Path) -> "OwnedBatchFs":
        _require_safe_absolute_components(data_root)
        current_fd = os.open("/", DIRECTORY_FLAGS)
        retained = []
        try:
            for component in data_root.parts[1:]:
                next_fd = _open_directory_at(current_fd, component)
                os.close(current_fd)
                current_fd = next_fd
            root_fd = current_fd
            retained.append(root_fd)
            references_fd = _open_directory_at(root_fd, "references")
            retained.append(references_fd)
            state_fd = _open_directory_at(root_fd, "state")
            retained.append(state_fd)
            batches_fd = _open_directory_at(root_fd, "batches")
            retained.append(batches_fd)
            return cls(
                data_root,
                retained,
                root_fd,
                references_fd,
                state_fd,
                batches_fd,
            )
        except BaseException:
            if retained:
                while retained:
                    os.close(retained.pop())
            else:
                os.close(current_fd)
            raise

    def pin_batch(
        self,
        mode: Literal["prepare", "mutate", "read"],
        batch_intent_fingerprint: str,
        intent_lock: dict[str, object] | None = None,
    ) -> None:
        self.lock_fd = _open_batch_lock_at(
            self.batches_fd,
            create=mode == "prepare",
        )
        self.descriptors.append(self.lock_fd)
        if not stat.S_ISREG(os.fstat(self.lock_fd).st_mode):
            raise ValueError("B001.lock is not a regular file")
        fcntl.flock(
            self.lock_fd,
            fcntl.LOCK_SH if mode == "read" else fcntl.LOCK_EX,
        )
        batch_created = False
        try:
            self.batch_fd = _open_directory_at(self.batches_fd, "B001")
        except FileNotFoundError:
            if mode != "prepare":
                raise
            self.batch_fd = _create_directory_at(self.batches_fd, "B001")
            batch_created = True
        self.descriptors.append(self.batch_fd)
        if mode == "prepare":
            if intent_lock is None:
                raise ValueError("prepare requires candidate intent lock")
            _verify_prepare_boundary_or_recovery_at(
                self.batches_fd,
                self.lock_fd,
                self.batch_fd,
                intent_lock,
                batch_intent_fingerprint,
                batch_created,
            )
            _create_or_verify_intent_lock_at(
                self.batch_fd,
                intent_lock,
                batch_intent_fingerprint,
            )
            _create_or_verify_boundary_at(
                self.batches_fd,
                self.lock_fd,
                self.batch_fd,
                batch_intent_fingerprint,
                batch_created,
            )
        else:
            _verify_existing_boundary_at(
                self.batches_fd,
                self.lock_fd,
                self.batch_fd,
                batch_intent_fingerprint,
            )
        child_descriptors = []
        for name in OWNED_CHILDREN:
            child_fd = (
                _create_directory_at(self.batch_fd, name)
                if mode == "prepare"
                else _open_directory_at(self.batch_fd, name)
            )
            child_descriptors.append(child_fd)
            self.descriptors.append(child_fd)
        (
            self.images_fd,
            self.thumbs_fd,
            self.receipts_fd,
            self.attempts_fd,
            self.staging_fd,
        ) = child_descriptors

    def write_staging_exclusive(
        self,
        name: str,
        contents: bytes,
    ) -> None:
        if self.staging_fd is None:
            raise RuntimeError("batch tree is not pinned")
        _require_recovery_basename(name)
        _write_bytes_exclusive_at(self.staging_fd, name, contents)
        os.fsync(self.staging_fd)

    def close(self) -> None:
        while self.descriptors:
            os.close(self.descriptors.pop())

    def __enter__(self) -> "OwnedBatchFs":
        return self

    def __exit__(self, *_error: object) -> None:
        self.close()
```

Production code wraps descriptor acquisition in one outer `try` so that a
failure after any intermediate child open still closes every retained
descriptor; tests inject one failure after each open and assert the process
has no leaked descriptors.

The pinned boundary record is created at `batches/B001.boundary.json` only
after the intent lock is durable:

```json
{
  "schemaVersion": 1,
  "batchId": "B001",
  "batchIntentFingerprint": "<64 lowercase hex characters>",
  "lockDevice": 123,
  "lockInode": 456,
  "batchDevice": 123,
  "batchInode": 789
}
```

On every later entry point, read this file relative to `batches_fd` and
require its fingerprint, lock pair, and batch pair to equal the candidate
intent, `os.fstat(lock_fd)`, and `os.fstat(batch_fd)`. A missing boundary is
allowed only during
`prepare`: either this invocation created B001, or an exact durable intent
lock already exists from a crash before boundary-record creation. An existing
unmarked B001 with no exact lock is rejected rather than initialized.

After pinning, all owned-tree reads and mutations use a single relative name
plus the correct retained directory descriptor. This includes
`os.open`, `os.stat(name, dir_fd=directory_fd, follow_symlinks=False)`,
`os.listdir`,
`os.mkdir`, `os.link`, `os.unlink`, and `os.replace`. Nested attempt
directories are opened component by component below `attempts_fd` and retained
until the attempt write finishes. No helper accepts an owned absolute `Path`.
External generated source PNGs and archive scanning remain read-only `Path`
inputs.

`prepare_b001` accepts
`archive_root=/home/takahiro/workspace/akari_generated`, excludes the pinned
active data-root inode, and computes deterministic
`state/prior-coverage.json` content with schema version, normalized source
root, sorted relative PNG names, and normalized novelty metadata found in
adjacent manifests. The authoritative document contains no clock value. If
the pinned state file exists with equal canonical bytes, do not rewrite it; if
it differs, reject with an explicit prior-coverage drift error. Reject any
full novelty key already present in the pinned production ledger or
prior-coverage metadata. Archive images are never returned as generation
references.

The create-once intent lock is:

```python
intent_lock = {
    "schemaVersion": 1,
    "batchId": "B001",
    "batchIntentFingerprint": batch_intent_fingerprint,
    "batchIntent": batch_intent,
}
```

Preparation uses this ordering:

```python
with OwnedBatchFs.pin_root(data_root) as owned_fs:
    batch_intent = _build_candidate_intent_from_pinned_references(
        matrix_path,
        owned_fs,
    )
    fingerprint = _fingerprint(batch_intent)
    intent_lock = _intent_lock(batch_intent, fingerprint)
    owned_fs.pin_batch("prepare", fingerprint, intent_lock)
    _cleanup_same_intent_debris_at(owned_fs, intent_lock)
    _prepare_prior_coverage_at(
        owned_fs.state_fd,
        archive_root,
        owned_fs.root_fd,
        fingerprint,
    )
    _prepare_manifest_and_reviews_at(owned_fs, intent_lock)
```

Create `intent-lock.json` relative to pinned `batch_fd` without replacement,
flush and fsync the file, then fsync `batch_fd`. If the no-replace hard link
loses to another creator, remove and durably forget the private temporary,
re-open the winner with `O_RDONLY | O_NOFOLLOW` relative to the same pinned
descriptor, and compare exact canonical bytes. Equal bytes are idempotent
success; different or malformed bytes are a hard rejection.
Every `prepare`, `prompt`, `status`,
`record-success`, `record-failure`, `reconcile`, and `review-summary`
invocation must, before any mutation:

1. rebuild candidate intent from current matrix, compiler constants/template,
   and current full relative reference records;
2. verify its fingerprint equals the stored fingerprint;
3. verify the canonical stored payload itself hashes to that fingerprint;
4. reject any drift, corrupt lock, or mixed receipt/prepared fingerprint.

Write replaceable JSON through a same-directory relative temporary, flush,
`os.fsync`, then call `os.replace` with both source and destination directory
descriptors. After replacement, fsync that retained descriptor. The initial
manifest is the Task 1 pending manifest plus top-level
`batchIntentFingerprint`. Because the existing Node validator ignores
additional top-level metadata, its contract remains valid.

Use only descriptor-relative JSON primitives for manifest, ledger, review,
intent, attempt, and receipt documents:

```python
def _write_bytes_exclusive_at(
    directory_fd: int,
    name: str,
    contents: bytes,
) -> None:
    descriptor = os.open(
        name,
        os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW,
        0o600,
        dir_fd=directory_fd,
    )
    try:
        _write_all(descriptor, contents)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_json_at(
    directory_fd: int,
    target_name: str,
    value: object,
    fingerprint: str,
) -> None:
    temporary_name = _temporary_name(target_name, fingerprint, "tmp")
    _write_bytes_exclusive_at(
        directory_fd,
        temporary_name,
        _canonical_document_bytes(value),
    )
    os.replace(
        temporary_name,
        target_name,
        src_dir_fd=directory_fd,
        dst_dir_fd=directory_fd,
    )
    os.fsync(directory_fd)


def _json_no_replace_at(
    directory_fd: int,
    target_name: str,
    value: object,
    fingerprint: str,
) -> None:
    temporary_name = _temporary_name(target_name, fingerprint, "prepared")
    _write_bytes_exclusive_at(
        directory_fd,
        temporary_name,
        _canonical_document_bytes(value),
    )
    try:
        os.link(
            temporary_name,
            target_name,
            src_dir_fd=directory_fd,
            dst_dir_fd=directory_fd,
            follow_symlinks=False,
        )
        os.fsync(directory_fd)
    finally:
        os.unlink(temporary_name, dir_fd=directory_fd)
        os.fsync(directory_fd)


def _create_or_verify_intent_lock_at(
    batch_fd: int,
    intent_lock: dict[str, object],
    fingerprint: str,
) -> None:
    expected = _canonical_document_bytes(intent_lock)
    try:
        _json_no_replace_at(
            batch_fd,
            "intent-lock.json",
            intent_lock,
            fingerprint,
        )
    except FileExistsError:
        actual = _read_regular_bytes_at(batch_fd, "intent-lock.json")
        if actual != expected:
            raise ValueError("intent lock create race mismatch")
```

`_temporary_name` accepts a validated basename only, rejects every slash,
backslash, dot component, control character, and non-allowlisted target, and
returns `.<target>.<full-fingerprint>.<uuid>.<kind>`. The reader helpers use
`os.open(name, O_RDONLY | O_NOFOLLOW, dir_fd=directory_fd)`, require a regular
`fstat`, and read from the descriptor. Boundary-record creation uses the same
create-or-verify rule and additionally compares the pinned device/inode pair.

The contract test scans the state module to reject `path.parent`, absolute
owned mutations, or a `_json_no_replace_at` implementation that omits the
post-unlink directory fsync.

At startup and before reconciliation, list each pinned owned descriptor with
`os.listdir(directory_fd)`. Temporary names encode the exact target and full
64-character intent fingerprint. Remove a regular non-symlink JSON temporary
only when its name targets a known document and its fingerprint is current.
Remove deterministic prepared PNG/WebP stages without a prepared receipt only
when both final media names and the final receipt are absent; these pre-receipt
orphans are non-authoritative and the retry still requires its source.
When a prepared or final receipt exists, validate its full intent and hashes
before removing any stage. Unknown names, another fingerprint, a symlink,
directory, unexpected final, or inconsistent pair rejects cleanup without
unlinking. `staging_fd` separately allowlists regular
`B001-NNN-recovered.png` sources and retains them; they are never interpreted
as prepared media. Every successful unlink is followed by `os.fsync` on its
pinned parent descriptor, so a crash before that fsync safely repeats cleanup.

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
  "batchIntentFingerprint": "<64 lowercase hex characters>",
  "promptSha256": "<compiled prompt hash>",
  "references": [
    {
      "id": "v1.5-body-balance",
      "snapshotPath": "references/akari-v1.5-b3-body-balance.png",
      "role": "v1.5 identity and body balance",
      "exclusions": ["outfit", "pose", "background"],
      "sha256": "e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734"
    }
  ],
  "generationId": null,
  "requestId": null,
  "failureReason": "missing local PNG and no recoverable payload",
  "recordedAt": "<UTC ISO timestamp>"
}
```

A durable prepared record is
`receipts/<imageId>.prepared.json`. It is written before either final media
path exists:

```json
{
  "schemaVersion": 1,
  "batchId": "B001",
  "imageId": "B001-002",
  "batchIntentFingerprint": "<64 lowercase hex characters>",
  "promptSha256": "<compiled prompt hash>",
  "references": [
    {
      "id": "v1.5-body-balance",
      "snapshotPath": "references/akari-v1.5-b3-body-balance.png",
      "role": "v1.5 identity and body balance",
      "exclusions": ["outfit", "pose", "background"],
      "sha256": "e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734"
    }
  ],
  "generationId": "<string or null>",
  "requestId": "<string or null>",
  "sourcePath": "<absolute original generated location>",
  "preparedImagePath": "batches/B001/images/.B001-002-<intent-fingerprint>.prepared.png",
  "imagePath": "batches/B001/images/<filenameStem>.png",
  "preparedThumbnailPath": "batches/B001/thumbs/.B001-002-<intent-fingerprint>.prepared.webp",
  "thumbnailPath": "batches/B001/thumbs/<filenameStem>.webp",
  "sha256": "<PNG hash>",
  "thumbnailSha256": "<WebP hash>",
  "width": 1024,
  "height": 1536,
  "recordedAt": "<UTC ISO timestamp>"
}
```

A final success receipt `receipts/<imageId>.json` contains the same intent,
prompt, ordered references, generation provenance, final relative paths,
hashes, dimensions, and `recordedAt`, but omits prepared paths. Validate every
field against the intent lock before reconciliation.

Refactor the existing thumbnail module without changing its output settings:
`render_thumbnail_bytes` runs `inspect_png`, converts to RGB, bounds the long
edge at 512 with LANCZOS, saves to `io.BytesIO` as WebP with quality 82 and
method 6, validates the two WebP header spans, and returns immutable bytes.
`render_thumbnail_bytes_from_fd` duplicates the supplied descriptor, seeks the
duplicate to zero, performs the same verification/conversion, and closes only
the duplicate. `render_thumbnail_bytes` and `build_thumbnail` delegate to that
descriptor implementation and preserve their current path APIs for external
callers. The B001 state layer calls only the descriptor API and owns exclusive
persistence.

For `record_success`:

1. enter fresh pinned root and full exclusive B001 contexts, verify the current
   candidate batch intent, boundary record, and `intent-lock.json`;
2. require exactly one of an external `source_path`, a validated
   `staging_name`, or resume-without-source mode. Open an external source once
   with `O_RDONLY | O_NOFOLLOW`, compare the Linux
   `/proc/self/fd/<descriptor>` target against the retained root-descriptor
   target, reject a source beneath the owned data root, and inspect bytes from
   that descriptor. Open a staging source only by basename relative to
   `staging_fd`. Reject a hash already recorded for another production image;
3. write PNG bytes by basename only through `_write_prepared_file` with
   `fs.images_fd`, `prepared_image_name`, the contents, and the two exact
   failpoint callbacks; this exclusively creates and fsyncs the file, then
   fsyncs `images_fd`;
4. re-open the PNG relative to `images_fd` with `O_NOFOLLOW`, verify its hash
   and dimensions from the descriptor, and call
   `render_thumbnail_bytes_from_fd`;
5. verify WebP bytes 0–3 are `RIFF` and bytes 8–11 are `WEBP`, then write them
   by basename only through `_write_prepared_file` with `fs.thumbs_fd`,
   `prepared_thumb_name`, the contents, and the two exact failpoint callbacks;
   re-open and verify through `thumbs_fd`;
6. only after both prepared directory fsyncs return, create
   `receipts/<imageId>.prepared.json` with `_json_no_replace_at`, including
   full intent fingerprint, prompt hash, ordered full relative reference
   records, provenance, prepared/final paths, hashes, and dimensions;
7. commit PNG with `_commit_no_replace_at(fs.images_fd,
   prepared_image_name, final_image_name, sha256)`, then fsync `images_fd`;
8. commit WebP with `_commit_no_replace_at(fs.thumbs_fd,
   prepared_thumb_name, final_thumb_name, thumbnail_sha256)`, then fsync
   `thumbs_fd`;
9. create the final receipt with `_json_no_replace_at` on `fs.receipts_fd`,
   call internal reconciliation with the same pinned context, then unlink
   prepared basenames and metadata relative to their retained descriptors and
   fsync each descriptor after its unlink;
10. return the final valid manifest entry.

If a final path already exists, require a regular non-symlink file and verify
its bytes against the prepared record. A match means its no-replace link
already completed; continue. Any mismatch is a hard rejection without
unlinking or rewriting the final.

Before the prepared record and its receipts-directory entry are durable,
retry may clean matching regular same-intent orphan prepared names and
requires the source again. Once `_json_no_replace_at` has fsynced
`receipts_fd`, `record_success(source_path=None)` verifies the prepared record,
prepared media or matching committed final media, full intent, prompt, and
references, then completes thumbnail/final links, receipt, and reconciliation
without reading the original source location.

Use these primitives; never open a final media path for writing:

```python
def _write_prepared_file(
    directory_fd: int,
    prepared_name: str,
    contents: bytes,
    after_file_fsync: Callable[[], None],
    after_directory_fsync: Callable[[], None],
) -> None:
    descriptor = os.open(
        prepared_name,
        os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW,
        0o644,
        dir_fd=directory_fd,
    )
    try:
        _write_all(descriptor, contents)
        os.fsync(descriptor)
        after_file_fsync()
    finally:
        os.close(descriptor)
    os.fsync(directory_fd)
    after_directory_fsync()


def _require_regular_nonsymlink_hash_at(
    directory_fd: int,
    name: str,
    expected_sha256: str,
) -> None:
    descriptor = os.open(
        name,
        os.O_RDONLY | os.O_NOFOLLOW,
        dir_fd=directory_fd,
    )
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError(f"not a regular non-symlink file: {name}")
        digest = hashlib.sha256()
        while chunk := os.read(descriptor, 1024 * 1024):
            digest.update(chunk)
        actual_sha256 = digest.hexdigest()
    finally:
        os.close(descriptor)
    if actual_sha256 != expected_sha256:
        raise ValueError(f"immutable file hash mismatch: {name}")


def _commit_no_replace_at(
    directory_fd: int,
    prepared_name: str,
    final_name: str,
    expected_sha256: str,
) -> None:
    try:
        _require_regular_nonsymlink_hash_at(
            directory_fd,
            final_name,
            expected_sha256,
        )
        return
    except FileNotFoundError:
        pass
    _require_regular_nonsymlink_hash_at(
        directory_fd,
        prepared_name,
        expected_sha256,
    )
    try:
        os.link(
            prepared_name,
            final_name,
            src_dir_fd=directory_fd,
            dst_dir_fd=directory_fd,
            follow_symlinks=False,
        )
    except FileExistsError:
        _require_regular_nonsymlink_hash_at(
            directory_fd,
            final_name,
            expected_sha256,
        )
        return
    os.fsync(directory_fd)
    _require_regular_nonsymlink_hash_at(
        directory_fd,
        final_name,
        expected_sha256,
    )
```

Inject failures at named boundaries
`after_prepared_image_file_fsync`, `after_prepared_image_dir_fsync`,
`after_prepared_thumb_file_fsync`, `after_prepared_thumb_dir_fsync`,
`after_prepared_record_fsync`, `after_image_link_fsync`,
`after_thumbnail_link_fsync`, `after_final_receipt_fsync`, and
`after_reconcile_before_cleanup`. For each boundary, tests assert exact
expected files, restart with the source requirement described above, finish to
one receipt/count, and prove no existing final was overwritten.

- [ ] **Step 5: Implement deterministic reconciliation**

After verifying the current candidate intent lock, reconciliation first
finishes every valid prepared record using the source-free no-replace protocol.
Final receipts are then authoritative for successful results. Rebuild each
B001 manifest entry from the locked batch intent, then apply its strictly
matching receipt to generation/artifact metadata. If the newest matching
failure has no later success, use `technicalStatus: "failed"` and its reason;
the same ID remains the next retry target.

Rebuild only B001’s ledger entries, preserving all other batches. A ledger
success entry contains batch ID, image ID, batch-intent fingerprint, novelty
key, prompt hash, PNG hash, artifact path, and ordered full relative reference
records. Set `acceptedProductionImages` to the number of unique successful
production entries across the full ledger and `technicalFailures` to the
number of immutable matching failure receipts. Atomically write manifest, then
ledger; every CLI entry point starts with intent verification and
reconciliation, so a crash between those writes converges on the next
invocation.

The reconciliation loop has this shape:

```python
with OwnedBatchFs.pin_root(data_root) as owned_fs:
    candidate_intent = _build_candidate_intent_from_pinned_references(
        matrix_path,
        owned_fs,
    )
    fingerprint = _fingerprint(candidate_intent)
    owned_fs.pin_batch("mutate", fingerprint)
    intent_lock = _load_and_verify_intent_at(
        owned_fs.batch_fd,
        candidate_intent,
        fingerprint,
    )
    _cleanup_same_intent_debris_at(owned_fs, intent_lock)
    _resume_prepared_records_at(owned_fs, intent_lock)
    batch_intent = intent_lock["batchIntent"]
    manifest = build_pending_manifest(batch_intent)
    manifest["batchIntentFingerprint"] = fingerprint
    b001_ledger_entries = []
    for entry in manifest["entries"]:
        receipt = _read_valid_receipt_at(
            owned_fs.receipts_fd,
            entry["id"],
        )
        failure = _latest_valid_failure_at(
            owned_fs.attempts_fd,
            entry["id"],
        )
        if receipt is not None:
            _require_receipt_matches_intent(
                receipt,
                batch_intent,
                fingerprint,
            )
            _verify_receipt_media_at(owned_fs, entry, receipt)
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
            _require_failure_matches_intent(
                failure,
                batch_intent,
                fingerprint,
            )
            entry["generation"]["technicalStatus"] = "failed"
            entry["generation"]["failureReason"] = failure["failureReason"]

    ledger = _read_ledger_at(owned_fs.state_fd)
    ledger["entries"] = [
        item for item in ledger["entries"] if item["batchId"] != "B001"
    ] + b001_ledger_entries
    ledger["acceptedProductionImages"] = len(ledger["entries"])
    ledger["technicalFailures"] = _count_failure_receipts_at(
        owned_fs.attempts_fd,
    )
    _atomic_json_at(
        owned_fs.batch_fd,
        "manifest.json",
        manifest,
        fingerprint,
    )
    _atomic_json_at(
        owned_fs.state_fd,
        "novelty-ledger.json",
        ledger,
        fingerprint,
    )
```

The public function owns the context above. Calls from `record_success`,
`record_failure`, `prepare`, or status use an internal pinned variant and pass
the same `OwnedBatchFs`; they never reopen the tree or recursively acquire the
batch lock.

`_load_and_verify_intent_at` is read-only: it loads the intent lock relative
to pinned `batch_fd`,
rebuilds the complete candidate batch intent, verifies both candidate and
stored canonical hashes against the locked fingerprint, and returns the lock
only on an exact payload match. `_require_receipt_matches_intent` and
`_require_failure_matches_intent` compare the fingerprint, prompt hash, and
entire ordered relative reference-record list with the locked entry, rejecting
extra, missing, reordered, or changed reference fields. They also require the
exact document key set and types shown above, exact locked final paths, valid
provenance nullability, lowercase hashes, positive dimensions, and a parseable
UTC `recordedAt`; prepared receipts additionally require the exact
fingerprint-derived prepared paths. `_resume_prepared_records_at` processes
prepared records in image-ID order through an internal no-replace finalizer;
it does not recursively invoke reconciliation. It accepts no source path and
advances only records that exactly match the locked entry and whose prepared
or already-linked final media match every recorded hash.

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

uv run python scripts/manage_akari_v1_5_b001.py record-success \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --image-id B001-001 \
  --staging-name B001-001-recovered.png

uv run python scripts/manage_akari_v1_5_b001.py record-success \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --image-id B001-001 \
  --resume-prepared

uv run python scripts/manage_akari_v1_5_b001.py record-failure \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --image-id B001-001 \
  --reason 'missing local PNG and no recoverable payload'
```

`prompt` prints JSON with `imageId`, `prompt`, `promptSha256`,
`batchIntentFingerprint`, ordered `referenceRecords`,
`referencedImagePaths`, and `targetPath`. `referenceRecords` contain only
relative manifest paths and the full role/exclusion/SHA contract.
`referencedImagePaths` contain only safely resolved normalized absolute paths
for `view_image` and `image_gen`. The first record/path is the B3 snapshot and
is labeled current selected plus permanent identity/body authority.
`targetPath` is an operator display value only; no persistence helper accepts
it.

Each CLI call creates and closes one fresh `OwnedBatchFs`. `prompt` and
`review-summary` take the shared read mode and perform no reconciliation.
`prepare`, `record-success`, `record-failure`, `reconcile`, and `status` take
the exclusive full-tree mode because `status` first converges any durable
receipt. All mutation subcommands reuse one pinned context through return and
never call a public entry point from another public entry point.

- [ ] **Step 7: Verify GREEN and commit**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_5_b001_state -v
uv run python -m unittest \
  tests.test_build_akari_review_thumbnail \
  tests.test_akari_v1_5_b001_contract \
  tests.test_akari_v1_5_b001_state -v
```

Expected: PASS.

Commit:

```bash
git add scripts/build_akari_review_thumbnail.py \
  scripts/akari_v1_5_b001_state.py \
  scripts/manage_akari_v1_5_b001.py \
  tests/test_build_akari_review_thumbnail.py \
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

- Consumes: one read-only rollout JSONL, one image-generation call ID or
  ordinal, a fully pinned and intent-verified `OwnedBatchFs`, and one safe
  staging basename.
- Produces:
  `recover_png(rollout_path: Path, owned_fs: OwnedBatchFs, output_name: str,
  call_id: str | None = None, ordinal: int | None = None) -> str`
  and npm script `gate:v1-5:b001`.

- [ ] **Step 1: Write failing structural-recovery tests**

Use synthetic JSONL containing unrelated assistant events, one invalid
`image_generation_call`, and two valid PNG base64 payloads. Assert explicit
call-ID selection, explicit ordinal selection, rejection of ambiguous default
selection, PNG signature verification, exclusive descriptor-relative output
creation, file and staging-directory fsync, and refusal to overwrite an
existing staging name. Reject a slash, backslash, dot component, absolute
name, non-B001 name, or non-PNG suffix. Swap the staging path for an external
symlink and ordinary sentinel directory after pinning; recovery writes only
through the retained `staging_fd` and leaves both sentinels unchanged.

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
signature `89504e470d0a1a0a`, and call
`owned_fs.write_staging_exclusive(output_name, decoded_bytes)`. That method
validates one basename, opens it with
`O_CREAT | O_EXCL | O_WRONLY | O_NOFOLLOW` relative to retained
`staging_fd`, fsyncs the file, closes it, then fsyncs `staging_fd`. Never
accept an output path or print the payload.

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
  --rollout "$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<rollout-id>.jsonl" \
  --call-id '<image generation call id>' \
  --matrix akari-v1.5/generation/b001-request-matrix.json \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --output-name B001-001-recovered.png
```

The recovery CLI fresh-pins root, references, state, batches, B001, and every
owned child, takes the exclusive batch lock, verifies the candidate intent and
boundary, and only then decodes and writes. It returns the staging basename;
the absolute display path is assembled for the operator only after the pinned
write and both fsyncs complete.

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
   path exists, use Task 3 rollout recovery, then pass its returned basename
   through `record-success --staging-name`. If neither source works, call
   `record-failure` and retry the same ID with the same prompt; do not advance.
   If `record-success` stops after durable prepared metadata, resume with
   `record-success --image-id <ID> --resume-prepared`; do not require or
   reopen the original generated path.
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
- `intent-lock.json` contains the complete batch intent and its canonical
  payload hashes to the stored `batchIntentFingerprint`;
- `B001.boundary.json` matches the pinned lock and batch device/inode pairs,
  and a fresh read-mode pin opens root, references, state, batches, B001, and
  all five owned children without following a symlink;
- every receipt has that exact fingerprint, its locked prompt hash, and its
  full ordered relative reference records with exact role, exclusions,
  snapshot path, and SHA-256;
- every manifest reference `path` and receipt reference `snapshotPath` is
  relative beneath `references/`, while only transient `prompt` output
  contains absolute `referencedImagePaths`;
- no receipt document, final image path, or final thumbnail path escapes B001;
  relative reference snapshots deliberately resolve under `references/`, and
  the receipt’s `sourcePath` is absolute generation provenance only;
- no prepared metadata, hidden prepared PNG/WebP, JSON temporary, symbolic
  link, directory in place of media, or unrecorded final remains; every
  descriptor-relative debris scan returns only allowlisted final names and
  explicitly retained rollout-recovery sources;
- `acceptedProductionImages` increased by exactly fifty from its pre-B001
  value;
- technical failure receipts do not increase the accepted count;
- five rows per lane;
- texture distribution 5/2/1/1/1;
- five subculture rows;
- cast distribution 35/5/5/5;
- scene distribution 40/10;
- all fifty compiled prompt hashes and all reference hashes match receipts;
- rebuilding the candidate intent from the tracked matrix, compiler constants,
  template order, schema versions, and current reference manifest yields the
  locked fingerprint before any final-gate mutation.

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
- Filesystem consistency: every owned runtime read, write, list, stat, link,
  unlink, replace, and directory creation receives a retained directory
  descriptor plus one validated relative name; only external read-only inputs
  and operator display output use absolute paths.
- Durability order: prepared file fsync precedes its parent-directory fsync;
  both media directory fsyncs precede the prepared receipt; JSON temporary
  unlink precedes a final parent-directory fsync.
- Scope: no new application, browser generation feature, PDF, B002 image, or
  generated Git asset is introduced.
- Unresolved-marker scan: no implementation instruction relies on an executor
  inventing a concept or filling an unspecified field.

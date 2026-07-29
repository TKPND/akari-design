# Akari v1.5 Kawaii 1000 Generation and Review Gallery Design

Status: approved design, awaiting implementation planning.

Date: 2026-07-29.

## Summary

This project will generate 1,000 independent Akari illustrations in twenty
batches of fifty. The collection focuses on classic girly cuteness, natural
expressions and gestures, varied uniforms, and carefully rendered skin and
fabric texture. It uses the current Akari v1.5 B3 body-balance baseline and the
accepted v1.4 rendering authorities to preserve identity.

Each completed batch will be reviewed through a lightweight browser gallery
served only over Tailscale. Review results will control the contents of the
next batch without automatically regenerating rejected images. Generated
images, thumbnails, manifests, and review state will live outside the Git
repository under `/home/takahiro/workspace/akari_generated/v1.5-1000/`.

The project produces images and review data only. It does not produce a PDF.

## Goals

- Produce 1,000 successfully saved PNG generation results.
- Keep every image recognizable as the same Akari defined by v1.5.
- Center the collection on classic girly cuteness rather than repeating the
  previous subculture-heavy direction.
- Make expression and gesture the primary source of cuteness.
- Include 300 uniform images across school-inspired, professional, sports,
  ceremonial, fantasy, and science-fiction families.
- Give all visible skin a soft semi-realistic finish while preserving the
  accepted hand-painted anime direction.
- Give 200 images an explicit skin, hosiery, or fabric-pressure focus.
- Prevent repeated combinations of outfit, setting, action, camera, mood, and
  cast structure.
- Support fast PC and mobile review without downloading individual images.
- Keep the gallery reachable only through the host's Tailscale address.
- Preserve complete generation and review provenance for every image.

## Non-Goals

- Do not build, render, or audit a PDF.
- Do not commit generated images, thumbnails, or working review data to Git.
- Do not expose the gallery on a public interface.
- Do not trigger image generation from the browser.
- Do not turn the gallery into a general asset manager or prompt editor.
- Do not use previously generated siblings as character identity references.
- Do not automatically replace a visually weak but technically valid result.
- Do not emphasize a numeric age repeatedly in prompts.
- Do not make isolated leg crops or hosiery-focused pin-up sheets the visual
  center of the collection.

## Existing Context

The live repository state on 2026-07-29 defines
`akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png` as the initial v1.5
body-balance authority. It keeps the v1.4 face, hair, ornament, rendering, and
healthy thigh direction while changing the upper-to-lower-body balance.

The collected archive under `/home/takahiro/workspace/akari_generated`
contained 277 PNG files at design time. Its major groups already covered:

- forty-eight unusual camera-angle studies;
- forty-eight summer angle and moment studies;
- approximately sixty companion scenes;
- sixty seasonal scenes.

Those images frequently used French girly, himekaji, angelcore, pale
subculture, active-cute, short bottoms, socks, and sneakers. The new collection
will index that archive as already-used territory and will not treat it as a
character reference pack.

## Core Creative Concept

Working concept: **Akari's 1,000 Kawaii Moments**.

The guiding sentence is:

> Clothing creates the opportunity; expression and gesture create the
> cuteness.

The collection uses the following direction:

- 90% classic girly and 10% subculture or wildcard styling;
- a young-adult visual impression roughly equivalent to the early twenties;
- clear adult identity without repeatedly calling attention to a number;
- classic uniforms, cardigans, blouses, ribbons, pleats, knitwear, and dresses;
- broader footwear and hem choices than the previous shorts-and-sneakers lock;
- natural, healthy body volume and warm skin;
- soft hand-painted anime rendering with controlled semi-realistic material
  detail;
- readable but secondary backgrounds;
- no cold fashion-catalog posing as the default;
- no explicit pin-up framing or glamour-model drift.

Each image must define one clear cute beat. Examples include:

- leaning forward from sudden happiness;
- adjusting a ribbon while becoming slightly embarrassed;
- freezing after noticing a small mistake;
- concentrating while choosing a small object;
- hiding fingertips inside warm sleeves;
- turning after being called;
- showing a small, proud expression after succeeding;
- rubbing sleepy eyes;
- giving a playful, teasing smile;
- taking one nervous step forward.

## Collection Lanes

The 1,000 images are divided into ten lanes of 100 images each.

| Lane | Count | Direction |
| --- | ---: | --- |
| Classic school-inspired uniforms | 100 | Blazers, sailor collars, cardigans, knit vests, and pleats |
| Professional and service uniforms | 100 | Cafes, florists, bookstores, hotels, workshops, research, and transport |
| Sports, ceremony, and fictional uniforms | 100 | Teams, stages, ceremonies, adult academies, and science-fiction groups |
| Everyday girly | 100 | Blouses, knitwear, dresses, and roomwear |
| Outings and special days | 100 | Date outfits, dresses, concerts, tea rooms, and evening scenes |
| Hobbies and making | 100 | Cooking, sewing, photography, music, gardening, computers, and crafts |
| Travel and walking | 100 | Rail, boats, airports, shopping streets, coasts, and regional cities |
| Retro and storybook worlds | 100 | Taisho- and Showa-inspired looks, Western retro, and gentle storybook scenes |
| Magic, fantasy, and science fiction | 100 | Magic, space, future cities, and strange rooms |
| Subculture and wildcards | 100 | A limited continuation of prior styling plus genuinely new experiments |

The first three lanes make up the 300-image uniform allocation.

## Batch Contract

There are twenty batches, `B001` through `B020`. Each batch contains fifty
successfully saved PNG files.

Every batch contains:

- five images from each of the ten collection lanes;
- forty action- or reaction-in-progress images;
- ten quieter outfit-presenting compositions;
- thirty-five solo images;
- ten two-person or viewer-point-of-view images;
- five images with friends, coworkers, or background groups;
- ten explicit skin or fabric texture-focus images;
- five subculture or wildcard images.

Within each lane's five images, the planned emotional distribution is:

1. happiness or visible excitement;
2. embarrassment or hesitation;
3. concentration or curiosity;
4. a small mistake or surprise;
5. calm, playfulness, or relief.

The exact scene does not repeat solely because the emotional label differs.

## Novelty Contract

Every request records the following primary novelty axes:

- lane;
- wardrobe family;
- setting and world;
- action;
- composition and subject distance;
- camera height, direction, and lens treatment;
- time, weather, and light;
- emotional beat;
- cast structure;
- dominant color family;
- texture focus.

No request may reuse an existing combination of all primary axes. The first
implementation pass will also index names and available metadata from the
existing generated archive as prior coverage.

Within one batch:

- one wardrobe family appears at most twice;
- one background class appears at most three times;
- one specific action verb appears at most twice;
- the same outfit, setting, action, and camera combination is forbidden;
- the white T-shirt and pale-blue lounge shorts in the v1.5 authority are not
  copied unless a request explicitly calls for them;
- a favorite from the previous batch may contribute only one inherited
  creative element;
- a favorite-derived request must change at least three of outfit, setting,
  action, and camera.

Previous generated outputs are not used as identity references for later
siblings. Their metadata can influence future concepts without their pixels
becoming a new character authority.

## Skin and Material Direction

All images with visible skin use a soft semi-realistic treatment inside the
accepted hand-painted anime rendering:

- subtle natural color variation at cheeks, ears, knees, and fingertips;
- soft reflected light and restrained highlights;
- readable body planes without hard muscle definition;
- firmer front and outer thigh planes;
- softer inner and rear thigh tissue;
- warm shadow color instead of gray plastic shading;
- no pore-level photorealism;
- no oily gloss, airbrushed plastic skin, or global smoothing.

Two hundred images make skin, hosiery, or contact pressure an explicit
secondary visual feature.

| Texture focus | Count |
| --- | ---: |
| Over-knee socks | 100 |
| Tights and stockings | 35 |
| Knee-high socks | 30 |
| Crew and ankle socks | 20 |
| Bare skin with natural clothing or seat contact | 15 |

The source at `/home/takahiro/neesocks.jpeg` is used only as an anatomy and
pressure reference. Before generation begins, implementation will copy it
non-destructively into the untracked project reference snapshot under
`/home/takahiro/workspace/akari_generated/v1.5-1000/references/` and record its
source SHA-256:

`d8185d8f453dbca9a22bbbae676d8f1c9634b4f2f8a2fecd2a8e675a990047d7`.

Its role is limited to these principles:

- the front and outer thigh show more structural tension;
- the inner and rear thigh show softer tissue;
- a sock band sinks unevenly into soft tissue;
- a small rounded transition appears above the band;
- the band does not create a harsh, uniform rubber-ring groove;
- sock fabric remains visibly separate from skin and carries plausible tension.

The line-art composition, underwear, identity, outfit, and colors are excluded
from the reference role.

Texture-focused images still present Akari, her expression, her gesture, and
the complete outfit as the main subject. Isolated leg studies are out of
scope.

## Reference Pack

### Permanent authorities

Every generation call uses:

1. `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
   - primary v1.5 face, hair, ornament, and body-balance authority;
   - its white T-shirt, lounge shorts, standing pose, and apartment are not
     composition or wardrobe references.
2. `akari-v1.4/style-tests/line-refinement/akari-v14-g2-balanced-lines.png`
   - primary authority for eyes, skin, hair planes, line hierarchy, palette,
     and clean grain-free finish;
   - body balance is superseded by v1.5 B3.

### Conditional authorities

The request may add the strongest relevant contextual reference:

- seated anatomy and continuity:
  `akari-v1.4/style-tests/reproducibility-i-seated/akari-v14-i2-chair-seated-repro.png`;
- hand and object interaction:
  `akari-v1.4/style-tests/reproducibility-j-action/akari-v14-j1-mandarin-action-repro.png`;
- hosiery pressure:
  the snapshotted `neesocks.jpeg`;
- one specific outfit, pose, or expression reference when one is available and
  materially useful.

The preferred maximum is four input images per call. Each prompt explicitly
states the role and excluded traits of every input. Before each built-in
`image_gen` call, the active references are opened with `view_image` so their
roles remain visible in the conversation context.

## Prompt Contract

Every distinct asset uses one independent built-in `image_gen` call. A batch is
not implemented with one broad prompt or as multiple `n` variants of a shared
prompt.

Prompts use this concise order:

1. scene and current situation;
2. Akari's cute beat;
3. complete wardrobe and material description;
4. pose, hands, gaze, and object contact;
5. composition, framing, and camera;
6. lighting and palette;
7. skin, fabric, and pressure behavior;
8. reference-image roles and invariants;
9. only the targeted avoid conditions relevant to that request.

Age wording appears once and stays equivalent to `young adult Akari in her
early twenties`. Prompts prevent childlike face or body drift without
repeatedly emphasizing age.

Prompts do not become exhaustive negative checklists. Each request preserves:

- short airy chestnut bob;
- clear amber eyes;
- one complete character-left pale-blue crossed-pin and thin-cord ornament;
- v1.5 body balance and healthy thigh volume;
- soft hand-painted planes and deliberate line hierarchy;
- one full-frame illustration;
- no text, logos, watermarks, borders, collages, or split panels.

## Generation and Persistence

Built-in `image_gen` is the default and required path unless the user later
explicitly requests the CLI fallback.

Built-in results are copied from the Codex generated-image location into:

```text
/home/takahiro/workspace/akari_generated/v1.5-1000/
├── references/
├── state/
│   └── novelty-ledger.json
└── batches/
    └── B001/
        ├── images/
        ├── thumbs/
        ├── manifest.json
        └── reviews.json
```

Generated files are never left only under `$CODEX_HOME/generated_images/`.
Existing files are not overwritten. Stable filenames use:

```text
akari_v150_kawaii1000_B001_001_<lane>_<short-scene>.png
```

Each manifest entry records:

- stable ID and batch ID;
- lane and all novelty axes;
- cute beat;
- full final prompt;
- reference paths, roles, exclusions, and SHA-256 values;
- generation ID and request ID when exposed;
- built-in tool mode;
- generated-image source path;
- final saved path;
- PNG dimensions and SHA-256;
- technical validation status;
- thumbnail path;
- whether the image is a texture-focus or subculture slot.

Original PNG files are immutable after successful validation. Thumbnails are
derived cache files and may be rebuilt.

## Review Gallery Architecture

Repository-owned gallery code lives under `tools/review-gallery/`. The design
prefers a small Node HTTP service and plain responsive HTML, CSS, and
JavaScript over a large application framework.

The gallery:

- reads only the configured `v1.5-1000` data root;
- serves only files declared in a validated batch manifest;
- provides cached WebP thumbnails for the grid;
- loads the original PNG only when the image is enlarged;
- supports batch, lane, status, texture, and reason filters;
- shows reviewed and unreviewed counts;
- writes only review state, never source PNG files;
- marks a batch `Ready for next batch` after all fifty images are rated.

The browser does not start generation, edit prompts, delete files, or promote
images into the Git repository.

### Review states

Each image has one state:

- `favorite`;
- `keep`;
- `reject`;
- `unreviewed`.

Reject reasons are optional and include:

- `identity-drift`;
- `age-drift`;
- `not-cute`;
- `duplicate`;
- `anatomy`;
- `hands`;
- `composition`;
- `garment`;
- `artifact`;
- `skin-flat`;
- `skin-plastic`;
- `compression-missing`;
- `compression-excessive`;
- `sock-painted-on`;
- `tissue-anatomy`;
- `fabric-texture-weak`.

Review records contain status, reasons, an optional note, update time, and a
monotonic revision.

### Interaction

The default view is a fifty-image grid. Selecting one image opens a large
detail view.

PC controls:

- arrow keys move between images;
- `1`, `2`, and `3` assign reject, keep, and favorite;
- reason tags are available without blocking fast rating.

Mobile controls:

- responsive one- or two-column grid;
- large touch targets;
- swipe or buttons for previous and next;
- the same three review states and optional reasons.

Every review action is persisted immediately. The server serializes writes and
uses write-to-temporary-file plus atomic rename. A rolling backup supports
recovery from damaged review JSON.

## Feedback Control

After all fifty images are reviewed, Codex reads `reviews.json` and adjusts the
next batch.

- A favorite contributes one winning element, but the next request changes at
  least three major visual axes.
- A keep is recorded as a successful direction without automatically producing
  a close sibling.
- `identity-drift` or `age-drift` strengthens the reference-role and identity
  wording for the affected lane.
- anatomy and material reasons strengthen only the relevant targeted prompt
  section or contextual reference.
- `duplicate` bans the conflicting axis combination.
- `not-cute` reduces similar outfit, palette, and expression combinations.

The fixed five-images-per-lane allocation remains in force. Feedback changes
the contents of each lane rather than allowing a popular lane to consume the
collection.

## Counting and Retry Rules

- A technically valid, successfully saved PNG counts toward 1,000 even when it
  is later rejected for visual quality.
- A network failure, missing result, absent PNG, invalid PNG signature, or
  failed final copy does not count.
- A technically failed ID is retried with the same intent.
- Before regenerating a missing built-in result, recovery checks the current
  Codex rollout for an `image_generation_call` PNG base64 payload.
- Recovered payloads must begin with PNG signature
  `89504e470d0a1a0a`.
- A byte-identical SHA-256 duplicate is a technical duplicate and does not
  count.
- A semantically similar but byte-distinct result counts and is reviewed in
  the browser.
- A visual reject is not silently replaced.
- Replacements beyond the 1,000-result contract require an explicit later
  decision.

## Tailscale-Only Service

The live host exposed Tailscale IPv4 `100.125.117.75` at design time. The
default gallery URL is:

`http://100.125.117.75:8787`

The implementation installs a `systemd --user` service with these behaviors:

- bind only to the configured Tailscale IPv4;
- never fall back to `0.0.0.0`;
- fail safely when the Tailscale address is unavailable;
- use `Restart=on-failure`;
- use absolute paths for Node, the repository, and the data root;
- log through the user journal;
- optionally enable user lingering so the service can start before an
  interactive login.

The service rejects path traversal and never serves a path that is absent from
a validated manifest. Public firewall exposure is not added. Application-level
authentication is out of scope for the first version because the service is
limited to the existing tailnet; it can be added later if tailnet membership
becomes broader.

## Error Handling

- A busy port produces a clear startup error and identifies the configured
  port.
- A missing image appears as a disabled error card without blocking the rest of
  the batch.
- A failed review write remains visibly failed in the browser.
- Review writes are serialized across PC and mobile clients.
- A corrupt review file can be restored from the latest valid backup.
- A missing or corrupt thumbnail is regenerated from the immutable PNG.
- A corrupt source PNG is not served as valid media and does not count.
- A manifest validation error blocks only the affected batch.
- Service restart does not change review state or generated files.

## Verification Strategy

Implementation will add a focused named gallery gate and use existing
repository checks in proportion to the changed scope.

### Manifest and generation tests

- exactly fifty requests per batch;
- exactly five requests per lane;
- exactly ten texture-focus requests;
- exactly five subculture or wildcard requests;
- unique stable IDs and primary novelty combinations;
- no more than four references per request;
- reference existence and SHA-256 verification;
- prompt and reference-role presence;
- PNG signature, dimensions, and SHA-256 verification;
- deterministic thumbnail path generation.

### Server and persistence tests

- Tailscale-only binding and refusal to bind publicly;
- manifest allowlisting and path-traversal rejection;
- valid review-state transitions;
- reason-tag validation;
- atomic review writes;
- serialized concurrent updates;
- backup recovery;
- missing-image and corrupt-thumbnail behavior;
- `Ready for next batch` only after fifty rated images.

### Browser tests

- fifty-card grid rendering;
- lazy thumbnail and detail-image loading;
- keyboard navigation and `1`/`2`/`3` rating;
- filters and progress counters;
- desktop and mobile viewport behavior;
- touch-sized controls and mobile previous/next navigation;
- visible save-error reporting.

### Live verification

- start and enable the user service;
- confirm the listener is the Tailscale IPv4 only;
- open the gallery from a second tailnet device;
- rate sample images from PC and mobile;
- restart the service and confirm state persistence;
- confirm no public listener or generated-image Git changes;
- run Markdown lint after documentation changes;
- run the focused gallery gate and the smallest existing integration gate that
  covers shared repository behavior.

No PDF, Chromium PDF render, Poppler, OCR, or release audit belongs in the
ordinary generation and review loop.

## Acceptance Criteria

The implementation is ready for the first batch when:

1. The structured data root and reference snapshot exist outside Git.
2. The manifest validator accepts one fifty-request dry-run batch.
3. Every request has explicit reference roles and a unique novelty signature.
4. The gallery serves only through the configured Tailscale IPv4.
5. PC and mobile review flows persist favorite, keep, reject, reasons, and
   notes.
6. Review data survives service restart and has a valid backup.
7. The gallery cannot serve undeclared local files.
8. The first batch can be generated one image at a time with built-in
   `image_gen` and saved into its final batch directory.
9. Technical failures can be retried without changing the intended ID.
10. The browser never triggers image generation or deletes source data.

The first fifty-image generation batch begins only after the implementation
plan is approved and the gallery and manifest dry run pass.

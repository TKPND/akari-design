# Akari v2.1 Selection History

Promotion date: 2026-08-05.

## Promoted Decisions

- On 2026-08-04, the user explicitly selected front-face Candidate C as the
  working v2.1 face authority.
- On 2026-08-05, after four same-condition full-body candidates were shown, the
  user delegated the choice with `おすすめでいいよ`. Candidate A was
  recommended for face continuity, compact healthy body balance, and overall
  full-figure stability, and was selected on that basis.
- On 2026-08-05, the user explicitly authorized promotion with `昇格OK`.

The two selected PNGs are promoted without resizing, cropping, recompression,
compositing, retouching, or color adjustment.

## Authority and Lineage

- Accepted face destination:
  `accepted/base/akari-v2.1-front-face-master.png`.
- Face promotion source:
  `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png`.
- Face generation call ID:
  `exec-52706d4e-2e58-41dd-ab44-8497e96c1755`.
- Face outer request ID: `call_1i5CEfRlm51t95kOlcXftWOL`.
- Accepted full-body destination:
  `accepted/base/akari-v2.1-front-fullbody.png`.
- Full-body promotion source:
  `tmp/akari-v2.1-redesign/fullbody-r01/selected/akari-v2.1-front-fullbody-r01.png`.
- Full-body built-in generated source ID:
  `exec-66dd2bef-9e26-49b3-9271-e338d40b6fab`.
- Approved design SHA-256:
  `085b07b97fa0672b966bfbe06876ed79f15ba1aef5404604ed13137e0b9ed189`.

The selected v2.1 face is the sole authority for facial identity, eyes, cheeks,
chin, expression, hair, and close-view rendering. The accepted v2.0 full-body
image was used only as a supporting body, outfit, laterality, and full-figure
reference during v2.1 full-body generation.

## Input Authorities

| Role | Source | SHA-256 |
| --- | --- | --- |
| Original v2.0 face and identity authority | `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png` | `34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe` |
| v2.0 body, outfit, laterality, and full-figure authority | `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png` | `03e7effc6dd13dadb4f1ec394b84ffe8ed9d218e500f0aefa49ebf2b5f0b6d94` |
| Selected v2.1 face authority used for full-body generation | `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png` | `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73` |

## Review Result

Original-detail inspection found the face master coherent and recognizably in
the accepted Akari lineage. It preserves the approachable late-teen read,
honey-amber almond eyes, compatible gaze, soft compact lower face, open smile,
off-center V bangs, complete crossed hairpin, connected low side ponytail, and
correct character-left/canvas-right laterality. The remaining bright hairpin
and moderately polished hair highlights are accepted Minors.

Original-detail inspection found the full-body baseline centered, uncropped,
grounded, and close to strict front. The figure preserves the selected face
family at full-body drawing scale, compact healthy proportions, separated
limbs, coherent simplified hands and fingers, complete legs and shoes, the
white T-shirt, navy no-drawcord A-line shorts, character-left/canvas-right
utility pocket, white socks, and blue-and-white sneakers. The pocket remains
more externally outlined than the quietest integrated-pocket target, and fine
hand and face details are simplified by scale; these are explicitly accepted
Minors under the user-directed human-selection workflow.

No visible crop, duplicate feature, disconnected limb, text, logo, watermark,
border, seam, or material generation artifact was found in either promoted
image.

## File Hashes

| Role | Dimensions | Color | SHA-256 |
| --- | --- | --- | --- |
| v2.1 accepted face master | `1023 x 1537` | 8-bit sRGB | `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73` |
| v2.1 accepted front full-body | `941 x 1672` | 8-bit sRGB | `8acc519847d5e02fc8b1917301d800b600b1738cf56b734c9177fa731b6326e3` |

## Promotion Verification

Both accepted PNGs must be byte-identical to their selected working sources
under `cmp`. Both must have PNG signature `89504e470d0a1a0a`, and their
dimensions and SHA-256 hashes must match the values above. Promotion
verification also includes original-detail inspection, Markdown lint,
`git diff --check`, and bounded Git-scope inspection.

The 30-degree probe, rejected candidates, comparison sheets, prompts, and run
ledgers remain ignored and noncanonical. No package expansion, manifest-backed
release, PDF work, staging, commit, or push is authorized by this promotion.

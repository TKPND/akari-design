# Akari v2.0 Selection History

Selection date: 2026-08-03.

## Promoted Decision

**The GPT Pro strict-front white-T full-body result is the accepted Akari v2.0
front full-body baseline.**

After directing that the FRONT MASTER be expanded into a full-body image and
committed as v2.0, the user reviewed the returned PNG and explicitly endorsed
it as `いい感じになった`. That exact PNG is promoted without transformation.
The existing FRONT MASTER is promoted beside it, also without transformation,
as the sole high-detail face authority.

## Authority and Lineage

- Accepted face destination:
  `accepted/base/akari-v2.0-front-face-master.png`.
- Face promotion source:
  `/home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-cc663046-4420-4290-a975-1a7d7bf09a59.png`.
- Accepted full-body destination:
  `accepted/base/akari-v2.0-front-fullbody.png`.
- Full-body promotion source:
  `/home/takahiro/.codex/attachments/bf3cd5cb-6575-4edd-b7bc-91c0ac7943ad/ChatGPT Image 2026年8月3日 21_48_22.png`.
- GPT Pro prompt SHA-256:
  `e884ad9cafdbba512145b32345618483042497e29c531bba245ce642dd78a977`.
- GPT Pro transfer archive SHA-256:
  `9e73d9b3af67c8757f4b59d241a4b21b8ad5094e1be68a72bcbec56d1a9354bd`.
- Approved design SHA-256:
  `b8d7b194e36a11c6f2eb097b19f4eda8ec42f4de947a50b7a2fdd9ca1c1b8855`.

The GPT Pro package assigned the FRONT MASTER sole authority over the face,
eyes, cheeks, chin, expression, hair, and skin. The earlier white-T full-body
candidate was included only as a secondary body and outfit guide. The returned
image therefore does not grant that secondary candidate any v2.0 identity
authority.

## Review Result

The full-body return passed both independent promotion gates.

The face gate found no same-person blocker. It preserves the horizontal almond
eye construction, amber irises, soft cheeks, short chin, open smile, age read,
off-center V bangs, crossed ornament, and low side ponytail. At full-body
drawing scale, the eye openings and mouth read slightly smaller and the lower
cheeks and chin slightly tighter than in the close master. These are accepted
scale-related Minor differences; further regeneration carries more identity
drift risk than retaining the approved image.

The full-body gate found a strict-front neutral stance, coherent compact
healthy proportions, complete hands and shoes, the white T-shirt, navy A-line
shorts, exactly two drawcord ends without a bow, one organizer on
character-left/canvas-right, correct ornament and ponytail laterality, white
socks, and generic blue-and-white sneakers. It found no text, watermark,
visible seam, or material generation artifact.

The only presentation Minor is the approximately one-pixel margin beneath the
shoe soles. The shoes are complete and uncropped, so the user-approved image
remains eligible as the front full-body baseline.

## File Hashes

| Role | Dimensions | SHA-256 |
| --- | --- | --- |
| v2.0 accepted face master | `1023 x 1537` | `34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe` |
| v2.0 accepted front full-body | `941 x 1672` | `03e7effc6dd13dadb4f1ec394b84ffe8ed9d218e500f0aefa49ebf2b5f0b6d94` |

## Promotion Verification

Both accepted PNGs were copied without resizing, cropping, recompression, or
color adjustment. Each destination was verified byte-identical to its source
with `cmp`. Both files have the PNG signature `89504e470d0a1a0a`; dimensions
and SHA-256 hashes match the values above. Original-detail inspection covered
the face, hair, ornament, ponytail, whole figure, hands, drawcords, organizer,
legs, socks, shoes, background, and image edges.

Targeted and repository Markdown lint, `git diff --check`, bounded Git-scope
inspection, and post-commit byte-identity checks are the promotion gates. PDF
audit and Python tests are explicitly out of scope.

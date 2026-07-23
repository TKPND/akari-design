# Akari v1.4 — J action-in-progress reproducibility test

Date: 2026-07-23

## Decision carried into J

The accepted v1.4 authorities are:

- **G2** for large paint planes, line hierarchy, hair, skin, palette, and the
  grain/bloom-free finish;
- **H-r03-1** for the adopted standing and adult-face direction;
- **I-2** for the adopted seated and continuity direction.

J is the last planned reproducibility domain: one simple everyday action in
progress.

The user had already approved `V13-D01: Table-side mandarin peel` in the first
Daily production ticket and promoted its v1.3 candidate B. J reuses that
approved action design with the v1.4 authorities. The old Daily output is not
used as a generation reference.

## Selected composition

Akari sits at a small dining table and looks down while peeling exactly one
mandarin.

- eye-level ornament-side three-quarter view from across the table;
- portrait 2:3, exact 1024 × 1536;
- crown-to-below-knees seated framing at about 65% figure presence;
- both forearms, wrists, and hands visible above the tabletop;
- one hand supports the fruit while the other lifts one continuous peel
  section;
- exactly one small plain cream dish and no other prop;
- loose opaque white T-shirt, pale-blue lounge shorts, and bare legs;
- soft warm frame-left morning light without a visible source or sunbeam.

See `DESIGN.md` and the exact shared prompt in `PROMPT.md`.

## Reference authority

1. `../line-refinement/akari-v14-g2-balanced-lines.png`
   controls the v1.4 rendering.
2. `../reproducibility-i-seated/akari-v14-i2-chair-seated-repro.png`
   controls the accepted adult face, eye balance, body volume, roomwear,
   seated continuity, and close portrait presence.
3. `../../references/v1.1/v1_1_髪飾り側_45deg.png`
   controls only canonical character-left ornament topology and placement.

## Generation

- Built-in image generation.
- J-1, J-2, and J-3 were generated independently and concurrently.
- Every sample used the same `PROMPT.md`, the same three references, and the
  same reference order.
- Each sample used one generation call with no artistic retry.
- No J output was used as a reference for another J output.
- Shared prompt SHA-256:
  `53584990ddf5482540544e5b4337097ce585be522239445f2b229241f98fed2a`.
- All three outputs are 1024 × 1536, 8-bit true-color sRGB PNG files.

## Action and composition review

The action itself is reproducible. All three samples pass the controlling
two-hand interaction gates.

| Gate | J-1 | J-2 | J-3 |
| --- | --- | --- | --- |
| Crown-to-below-knees seated framing | Pass | Pass | Marginal pass |
| Both wrists and hands fully visible | Pass | Pass | Pass |
| Plausible supporting hand | Pass | Pass | Pass |
| Plausible peeling hand | Pass | Pass | Marginal pass |
| Peel attached to or contacting fruit | Marginal pass | Pass | Pass |
| Fingers separate and not merged into fruit | Pass | Pass | Marginal pass |
| Gaze directed at fruit | Pass | Pass | Pass |
| Exactly one mandarin and one dish | Pass | Pass | Pass |
| Coherent seated joints | Pass | Pass | Marginal pass |
| No food-ad pose | Pass | Marginal pass | Pass |

Action/composition ranking: **J-2 > J-1 > J-3**.

- **J-1:** Quiet and coherent. The peel connection is visible but has the least
  sharply defined attachment seam.
- **J-2:** Clearest separation of supporting and peeling hands and the most
  readable continuous peel. The high peel arc approaches a display gesture
  but remains action-focused because the fruit stays inward and the gaze is
  lowered.
- **J-3:** The action remains valid, but the peeling fingertips form the
  tightest cluster. The central table leg also bisects the lower body and
  weakens hip-to-knee readability.

Action reproducibility result: **3/3 pass**.

## Style, identity, and ornament review

Scale: 5 is closest to the accepted authority. A clean-finish score of 5 means
no visible grain or bloom.

| Sample | Paint planes | Line hierarchy | Hair | Fabric | Face/eyes | Clean finish | Adult age | Roomwear | Ornament |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| J-1 | 4 | 4 | 4 | 4 | 4 | 4 | Pass | Pass | Pass |
| J-2 | 4 | 4 | 4 | 3 | 4 | 4 | Pass | Pass | Pass |
| J-3 | 3 | 3 | 3 | 3 | 3 | 3 | Marginal | Pass | Pass |

Style/identity ranking: **J-1 > J-2 > J-3**.

- **J-1** best preserves I-2's adult eye restraint and the separation between
  firm silhouette lines and quiet interior marks. Extra halo strands and
  somewhat busy shorts folds are the main drift.
- **J-2** remains close, but the face is slightly softer and rounder, while
  narrow shorts creases and small shirt-shadow wedges make the fabric busier.
- **J-3** has the roundest, largest eyes and softest lower face. Repeated long
  hair contours and sharper garment creases weaken G2's large-plane
  hierarchy.

All three retain the accepted roomwear and a readable canonical ornament: two
crossed pale-blue pins above one thin cord bow with two narrow loops and two
slim tails.

Scoped style/identity result: **2/3 pass**.

## Production and forbidden-element review

| Gate | J-1 | J-2 | J-3 |
| --- | --- | --- | --- |
| No extra food, utensil, drink, packaging, or second fruit | Pass | Pass | Pass |
| No direct gaze or fruit-to-viewer food-ad staging | Pass | Pass | Pass |
| No detached floating spiral peel | Pass | Pass | Pass |
| No visible window or curtain | Pass | Pass | Pass |
| No visible sunbeam or hard shaped light band | Pass | **Fail** | **Fail** |
| No text, logo, watermark, collage, or extra character | Pass | Pass | Pass |
| No clear grain, bloom, haze, or scratch artifact | Pass | Pass | Pass |
| Full production result | **Pass** | **Fail** | **Fail** |

- J-2 contains a conspicuous diagonal sunbeam on the frame-left wall and a
  matching hard diagonal light/shadow division across the tabletop.
- J-3 contains a softer but still distinct diagonal sunbeam on the frame-left
  wall.
- J-1 keeps the frame-left light diffuse and is the only full production pass.

## Result

The action-in-progress objective succeeds: all three samples show a coherent
two-hand mandarin-peeling action.

The full J test nevertheless **fails** its formal two-of-three requirement.
Only J-1 passes every controlling gate. J-2 and J-3 fail the explicit
no-sunbeam condition, and J-3 also carries the weakest style and adult-age
continuity.

**J-1 is the recommended selection and the only strict full pass.**

## User selection

**J-1 is formally accepted for the Akari v1.4 action-in-progress domain.**

The selection preserves I-2's calm adult-face continuity while adding a
coherent two-hand everyday action. Its marginally soft peel-attachment seam,
extra halo strands, and busier lounge-shorts folds are accepted.

The accepted v1.4 authority chain is now:

- **G2** — line hierarchy, large paint planes, palette, and finish;
- **H-r03-1** — standing composition and adult-face direction;
- **I-2** — seated composition and face continuity;
- **J-1** — everyday action in progress.

## File hashes

| File | SHA-256 |
| --- | --- |
| `akari-v14-j1-mandarin-action-repro.png` | `130642eb7a2db7d29f26fb7101a1f0049fe4214c839d8a8ab5520d756b7f276a` |
| `akari-v14-j2-mandarin-action-repro.png` | `7b31ba7290c5f64f3373fd4e006768ca254f5b46475828371c6c0a1795b3b460` |
| `akari-v14-j3-mandarin-action-repro.png` | `f7197272d20adfef0c37f5327c780c24821fdef8f725acfd703fda40b7fa7d94` |
| `akari-v14-j-action-comparison.png` | `bbb7bf43098ae565744cc7c04e9b9f16da9c1c95a8c86a460b9414b276e95aa5` |

## Files

- `akari-v14-j1-mandarin-action-repro.png`
- `akari-v14-j2-mandarin-action-repro.png`
- `akari-v14-j3-mandarin-action-repro.png`
- `akari-v14-j-action-comparison.png`
- `akari-v14-j-action-selection.md`
- `DESIGN.md`
- `PROMPT.md`
- `PLAN.md`

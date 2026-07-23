# Akari v1.2 Daily.2 D08 r02 Sock-Adjust Retry Design

**Date:** 2026-07-16

**Status:** Approved under the user's autonomous-completion delegation

## 1. Why r01 Closed

D08 r01 produced three ineligible candidates. A separated the sock mouth into
a strap-like artifact. B adjusted the character-left sock despite an explicit
character-right target. C used the correct side but pulled that sock above the
other one, contradicting the required same-evening lower-right-sock state.

The repeated height inversion exposed a scene-contract conflict: asking the
model to pull the already-lower sock upward while also requiring it to remain
lower. Core and D07 controllers passed and remain frozen.

## 2. r02 Correction

Keep the same bedroom, camera family, supported bed-edge hinge, outfit, state,
and five accepted references. Change only the working side:

- both hands smooth the top of the character-left sock;
- the character-left sock has normal mid-calf height and two complete stripes;
- the untouched character-right sock stays slightly lower with two complete
  stripes;
- both feet remain grounded on separate lanes;
- the character-right hoodie cuff remains pushed up one thumb width;
- no sock mouth is stretched into a detached band.

The gaze follows the character-left working sock. This preserves D07
continuity while making the adjustment action and final sock heights mutually
compatible.

## 3. Retry Contract

Use revision `r02` with the same D08 descriptor, dependencies, references, and
production gate. Generate independent A/B from the corrected frozen prompt.
Do not use r01 A, B, or C as references. Optional C remains available only for
distinct r02 candidate-local Blocker/Major failures.

Local evidence uses `source/candidates/d08/r02/` and
`comparisons/d08-r02/d08-r02-comparison.webp`. Promotion uses the canonical
`accepted/daily/evening/akari-v1.2_d08_evening-bed-edge-sock-adjust_r02.png`.

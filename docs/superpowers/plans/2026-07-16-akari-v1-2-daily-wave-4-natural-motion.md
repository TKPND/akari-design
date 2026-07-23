# Akari v1.2 Daily Wave 4 Natural Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, generate, review, promote, and release D16-D20 as a five-image Natural Motion wave that expands Akari v1.2 from seated household life into progressively harder standing movement.

**Architecture:** Extend the existing data-driven Daily lifecycle without changing Core. Each asset receives one static asset contract, one ordered review policy, one r01 generation request, one A/B comparison command, and one lifecycle test class. Generate and accept each asset sequentially; Wave 4 closes only after D16-D20 have accepted bytes, ordered review evidence, SHA linkage, clean-clone coverage, and a separate release register.

**Tech Stack:** Python 3 with `unittest`, PyYAML, Pillow, existing Daily validator helpers; npm scripts as command aliases; Markdown and YAML manifests; built-in image generation for independent A/B candidates; Git for per-asset checkpoints.

## Global Constraints

- Preserve Akari v1.2 Accepted Core identity, body, palette, files, and image bytes.
- Use a 1024 by 1536 PNG portrait canvas with the existing 1020-1028 by 1532-1540 tolerance; forced exact resize is forbidden.
- Use one standalone image, one scene, and one composition; collage, grid, split screen, multi-panel, text, logo, and watermark are forbidden.
- Use the same outfit in D16-D20: loose opaque white short-sleeve T-shirt, clearly constructed opaque gray lounge shorts, and white socks with exactly two pale-blue stripes; no shoes.
- Keep the complete head, character-left ornament, both hands, pelvis, both knees, both ankles, both heels, and both toes structurally reviewable.
- Use one or two Humanization details per scene.
- Generate D16-D20 sequentially and accept one asset before generating the next.
- Never reference a D16-D20 candidate or accepted image from another D16-D20 request; every scene re-anchors independently to Accepted Core and established pre-Wave-4 Daily references.
- Initial variants are `a` and `b`; optional `c` is allowed only after both A/B attempts have scene-local or distinct candidate-local Blocker/Major findings.
- Local candidates and comparisons remain evidence outside the tracked release; accepted PNG bytes and manifests are tracked.
- D16-D20 use `accepted/daily/motion/`; Waves 1-3 and their release registers remain unchanged.
- Core promotion is forbidden.

---

## File Map

**Create:**

- `akari-v1.2/manifest/generation-requests/d16-r01.yaml` — doorway-turn generation contract.
- `akari-v1.2/manifest/generation-requests/d17-r01.yaml` — upper-shelf-reach generation contract.
- `akari-v1.2/manifest/generation-requests/d18-r01.yaml` — lower-cabinet-retrieve generation contract.
- `akari-v1.2/manifest/generation-requests/d19-r01.yaml` — cable-step-over generation contract.
- `akari-v1.2/manifest/generation-requests/d20-r01.yaml` — fitted-sheet-pull generation contract.
- `akari-v1.2/accepted/daily/motion/akari-v1.2_d16_motion-doorway-turn_r01.png` — selected D16 bytes at the accepted revision.
- `akari-v1.2/accepted/daily/motion/akari-v1.2_d17_motion-upper-shelf-reach_r01.png` — selected D17 bytes.
- `akari-v1.2/accepted/daily/motion/akari-v1.2_d18_motion-lower-cabinet-retrieve_r01.png` — selected D18 bytes.
- `akari-v1.2/accepted/daily/motion/akari-v1.2_d19_motion-cable-step-over_r01.png` — selected D19 bytes.
- `akari-v1.2/accepted/daily/motion/akari-v1.2_d20_motion-fitted-sheet-pull_r01.png` — selected D20 bytes.
- `akari-v1.2/docs/akari-v1.2-daily-wave-4.md` — Wave 4 release register.

**Modify:**

- `scripts/akari_v1_2_daily.py` — D16-D20 review policies.
- `scripts/validate_akari_v1_2_natural_form.py` — asset IDs plus static and generation contracts.
- `tests/test_akari_v1_2_daily.py` — policy, contract, dependency, and lifecycle coverage.
- `akari-v1.2/manifest/assets.yaml` — candidate then accepted asset state.
- `akari-v1.2/manifest/review-log.yaml` — ordered A/B reviews and selected-source SHA linkage.
- `akari-v1.2/docs/akari-v1.2-daily-handoff.md` — Wave 4 completion state.
- `package.json` — D16-D20 comparison and focused gate aliases.

**Local evidence only:**

- `akari-v1.2/source/candidates/dNN/rNN/*.png`
- `akari-v1.2/comparisons/dNN-rNN/dNN-rNN-comparison.webp`

---

### Task 1: Add the Wave 4 validation skeleton

**Files:**

- Modify: `scripts/akari_v1_2_daily.py`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_daily.py`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `package.json`

**Interfaces:**

- Consumes: existing `DailyReviewPolicy`, `validate_daily_generation_request()`, `validate_assets()`, `validate_generation_dependencies()`, and `build_v1_2_daily_comparison.py`.
- Produces: validator-recognized IDs D16-D20, review controllers `D16-scene` through `D20-scene`, candidate asset rows, and comparison/gate commands.

- [ ] **Step 1: Record the Wave 4 baseline and write failing policy and asset-registration tests**

Run `git rev-parse HEAD > /tmp/akari-wave4-base` before editing tracked files.

Append a table-driven test before adding production mappings:

```python
WAVE4_ASSETS = {
    "D16": {
        "descriptor": "motion-doorway-turn",
        "phase": 19,
        "depends_on": ["D01", "D05", "C01", "C03", "C07"],
    },
    "D17": {
        "descriptor": "motion-upper-shelf-reach",
        "phase": 20,
        "depends_on": ["D01", "D05", "C01", "C03", "C07"],
    },
    "D18": {
        "descriptor": "motion-lower-cabinet-retrieve",
        "phase": 21,
        "depends_on": ["D01", "D12", "C01", "C03", "C07"],
    },
    "D19": {
        "descriptor": "motion-cable-step-over",
        "phase": 22,
        "depends_on": ["D01", "D13", "C01", "C03", "C07"],
    },
    "D20": {
        "descriptor": "motion-fitted-sheet-pull",
        "phase": 23,
        "depends_on": ["D01", "D08", "C01", "C03", "C07"],
    },
}


class Wave4RegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )

    def test_wave4_review_policies_are_ordered(self):
        self.assertEqual(
            tuple(DAILY_REVIEW_POLICIES)[-5:],
            ("D16", "D17", "D18", "D19", "D20"),
        )
        for asset_id in WAVE4_ASSETS:
            with self.subTest(asset_id=asset_id):
                self.assertEqual(
                    daily_review_policy(asset_id).scene_controller,
                    f"{asset_id}-scene",
                )

    def test_wave4_assets_start_as_candidates(self):
        assets = {item["asset_id"]: item for item in self.assets["assets"]}
        for asset_id, expected in WAVE4_ASSETS.items():
            with self.subTest(asset_id=asset_id):
                asset = assets[asset_id]
                self.assertEqual(asset["descriptor"], expected["descriptor"])
                self.assertEqual(asset["phase"], expected["phase"])
                self.assertEqual(asset["depends_on"], expected["depends_on"])
                self.assertEqual(asset["status"], "candidate")
                self.assertEqual(asset["revision"], "r00")
                self.assertEqual(asset["accepted_paths"], [])
```

Update the existing exact policy-order assertion so its expected tuple ends with D16-D20.

- [ ] **Step 2: Run the focused tests and verify failure**

Run:

```bash
uv run python -m unittest   tests.test_akari_v1_2_daily.DailyPrimitiveTests   tests.test_akari_v1_2_daily.Wave4RegistrationTests -v
```

Expected: FAIL because D16-D20 are not recognized and their asset rows do not exist.

- [ ] **Step 3: Add review policies and validator IDs**

Add these policies after D15:

```python
    "D16": DailyReviewPolicy(
        frozenset({"D01", "D05", "C01", "C03", "C07", "D16-scene"}),
        "D16-scene", frozenset({"blocker", "major"}), True,
    ),
    "D17": DailyReviewPolicy(
        frozenset({"D01", "D05", "C01", "C03", "C07", "D17-scene"}),
        "D17-scene", frozenset({"blocker", "major"}), True,
    ),
    "D18": DailyReviewPolicy(
        frozenset({"D01", "D12", "C01", "C03", "C07", "D18-scene"}),
        "D18-scene", frozenset({"blocker", "major"}), True,
    ),
    "D19": DailyReviewPolicy(
        frozenset({"D01", "D13", "C01", "C03", "C07", "D19-scene"}),
        "D19-scene", frozenset({"blocker", "major"}), True,
    ),
    "D20": DailyReviewPolicy(
        frozenset({"D01", "D08", "C01", "C03", "C07", "D20-scene"}),
        "D20-scene", frozenset({"blocker", "major"}), True,
    ),
```

Append `"D16"` through `"D20"` to `ASSET_IDS` in `validate_akari_v1_2_natural_form.py`.

- [ ] **Step 4: Register candidate asset rows**

Append five rows to `assets.yaml`. Use this exact shape for each ID:

```yaml
  - asset_id: D16
    descriptor: motion-doorway-turn
    phase: 19
    variants: [default]
    expected_paths:
      - accepted/daily/motion/akari-v1.2_d16_motion-doorway-turn_r01.png
    depends_on: [D01, D05, C01, C03, C07]
    gate: daily
    status: candidate
    revision: r00
    accepted_paths: []
```

Repeat with:

```text
D17 / motion-upper-shelf-reach / phase 20 / [D01, D05, C01, C03, C07]
D18 / motion-lower-cabinet-retrieve / phase 21 / [D01, D12, C01, C03, C07]
D19 / motion-cable-step-over / phase 22 / [D01, D13, C01, C03, C07]
D20 / motion-fitted-sheet-pull / phase 23 / [D01, D08, C01, C03, C07]
```

- [ ] **Step 5: Add comparison and focused gate aliases**

Add:

```json
"build:v1-2:d16-comparison": "uv run python scripts/build_v1_2_daily_comparison.py --request akari-v1.2/manifest/generation-requests/d16-r01.yaml --output akari-v1.2/comparisons/d16-r01/d16-r01-comparison.webp --asset-id D16",
"build:v1-2:d17-comparison": "uv run python scripts/build_v1_2_daily_comparison.py --request akari-v1.2/manifest/generation-requests/d17-r01.yaml --output akari-v1.2/comparisons/d17-r01/d17-r01-comparison.webp --asset-id D17",
"build:v1-2:d18-comparison": "uv run python scripts/build_v1_2_daily_comparison.py --request akari-v1.2/manifest/generation-requests/d18-r01.yaml --output akari-v1.2/comparisons/d18-r01/d18-r01-comparison.webp --asset-id D18",
"build:v1-2:d19-comparison": "uv run python scripts/build_v1_2_daily_comparison.py --request akari-v1.2/manifest/generation-requests/d19-r01.yaml --output akari-v1.2/comparisons/d19-r01/d19-r01-comparison.webp --asset-id D19",
"build:v1-2:d20-comparison": "uv run python scripts/build_v1_2_daily_comparison.py --request akari-v1.2/manifest/generation-requests/d20-r01.yaml --output akari-v1.2/comparisons/d20-r01/d20-r01-comparison.webp --asset-id D20",
"gate:edit:d16": "npm run test:python:daily && npm run test:python:natural-form && npm run validate:v1-2 && npm run verify:v1-2:release-pins",
"gate:edit:d17": "npm run test:python:daily && npm run test:python:natural-form && npm run validate:v1-2 && npm run verify:v1-2:release-pins",
"gate:edit:d18": "npm run test:python:daily && npm run test:python:natural-form && npm run validate:v1-2 && npm run verify:v1-2:release-pins",
"gate:edit:d19": "npm run test:python:daily && npm run test:python:natural-form && npm run validate:v1-2 && npm run verify:v1-2:release-pins",
"gate:edit:d20": "npm run test:python:daily && npm run test:python:natural-form && npm run validate:v1-2 && npm run verify:v1-2:release-pins"
```

- [ ] **Step 6: Run tests and commit the skeleton**

Run:

```bash
npm run test:python:daily
npm run validate:v1-2
npm run verify:v1-2:release-pins
```

Expected: all commands PASS while D16-D20 remain candidate r00.

Commit:

```bash
git add scripts/akari_v1_2_daily.py   scripts/validate_akari_v1_2_natural_form.py   tests/test_akari_v1_2_daily.py   akari-v1.2/manifest/assets.yaml package.json
git commit -m "feat: register Daily Wave 4 motion skeleton"
```

---

### Task 2: Implement and accept D16 doorway turn

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/d16-r01.yaml`
- Create: `akari-v1.2/accepted/daily/motion/akari-v1.2_d16_motion-doorway-turn_r01.png`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_daily.py`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`

**Interfaces:**

- Consumes: D01 roomwear identity, D05 hallway scale, C01 standing body, C03 hairpin-side three-quarter identity, C07 standing sock feet.
- Produces: accepted D16 r01 plus immutable source SHA linkage.

- [ ] **Step 1: Write failing D16 contract tests**

Create `D16ContractTests` using the D15 class shape and assert:

```python
self.assertEqual(self.d16["descriptor"], "motion-doorway-turn")
self.assertEqual(self.d16["phase"], 19)
self.assertEqual(
    self.d16["depends_on"], ["D01", "D05", "C01", "C03", "C07"]
)
self.assertEqual(
    [item["variant"] for item in self.request["candidates"]], ["a", "b"]
)
self.assertEqual(
    self.request["scene_contract"]["action"],
    "stopped-mid-route-soft-bedroom-doorway-turn",
)
for phrase in (
    "called from another room",
    "both feet fully grounded",
    "head chest and pelvis",
    "not a fashion pose",
):
    self.assertIn(phrase, self.request["shared_prompt"])
validate_generation_request(self.request)
validate_generation_dependencies(self.assets, self.requests)
```

- [ ] **Step 2: Run D16 tests and verify failure**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_2_daily.D16ContractTests -v
```

Expected: FAIL because the request and static validator contract do not exist.

- [ ] **Step 3: Add the D16 static and generation contracts**

Use:

```python
D16_STATIC_ASSET_CONTRACT = {
    "descriptor": "motion-doorway-turn",
    "phase": 19,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/motion/akari-v1.2_d16_motion-doorway-turn_r01.png"
    ],
    "depends_on": ["D01", "D05", "C01", "C03", "C07"],
    "gate": "daily",
}
D16_R01_SCENE_CONTRACT = {
    "camera": "eye-level-bedroom-side-three-quarter-portrait-full-body",
    "location": "plain-bedroom-doorway-to-hall",
    "support": "bilateral-grounded-staggered-feet-with-readable-floor-contact",
    "action": "stopped-mid-route-soft-bedroom-doorway-turn",
    "continuity": "white-t-shirt-gray-lounge-shorts-two-stripe-socks",
    "lighting": "soft-neutral-indoor-daylight",
    "gaze": "soft-responsive-gaze-toward-off-frame-call",
    "pose": "linked-head-chest-pelvis-turn-with-one-foot-slightly-forward",
    "humanization": [
        "one-small-turn-driven-t-shirt-side-fold",
        "one-subtle-sock-height-difference",
    ],
    "outfit": {
        "top": "loose-opaque-white-short-sleeve-t-shirt",
        "bottom": "clearly-constructed-opaque-gray-lounge-shorts",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-soft-responsive-face",
        "both-natural-five-finger-hands",
        "linked-neck-chest-pelvis-turn",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-grounded-striped-socks-ankles-heels-and-toes",
        "one-coherent-doorway-and-floor-plane",
    ],
    "forbidden_props": ["mirror", "phone", "bag", "footwear", "readable-text"],
}
```

References are ordered exactly:

```text
accepted_d01_roomwear_identity -> accepted D01 PNG
accepted_d05_hallway_scale -> accepted D05 PNG
accepted_c01_standing_body -> accepted C01 PNG
accepted_c03_hairpin_three_quarter -> accepted C03 hairpin-side PNG
accepted_c07_standing_sock_feet -> accepted C07 standing PNG
```

The shared prompt must implement every D16 section of the approved design and include the four test phrases verbatim. Hash the final UTF-8 prompt and store the digest as `D16_R01_SHARED_PROMPT_SHA256`.

- [ ] **Step 4: Register and validate the D16 r01 request**

Create YAML with the existing exact Daily top-level order and:

```yaml
request_id: akari-v1.2-d16-r01
asset_id: D16
revision: r01
variation_axis: independent_scene_attempt
candidate_policy:
  initial_variants: [a, b]
  optional_variant: c
  optional_c_only_for: d16-scene-or-distinct-independent-candidate-local-major-failures
  stop_for_shared_failure: [D01, D05, C01, C03, C07]
  cross_candidate_references: forbidden
candidates:
  - variant: a
    title: independent-scene-a
    target_path: source/candidates/d16/r01/akari-v1.2_d16_motion-doorway-turn_r01-a.png
  - variant: b
    title: independent-scene-b
    target_path: source/candidates/d16/r01/akari-v1.2_d16_motion-doorway-turn_r01-b.png
comparison_anchors: []
acceptance_gates: [identity, body, state, continuity, rendering, production]
```

Use the approved common blockers plus D16-specific rejects: head-only twist, incompatible pelvis/feet, fashion pose, hidden critical anatomy, or non-grounded feet.

Run:

```bash
npm run gate:edit:d16
git add akari-v1.2/manifest/generation-requests/d16-r01.yaml   scripts/validate_akari_v1_2_natural_form.py   tests/test_akari_v1_2_daily.py
git commit -m "feat: register D16 doorway turn"
```

Expected: focused gate PASS with D16 still candidate r00.

- [ ] **Step 5: Generate, compare, review, and promote D16**

Open the five accepted references at original resolution. Generate independent A and B; do not include A while generating B. Save them to the declared local candidate paths.

Run:

```bash
npm run build:v1-2:d16-comparison
```

Review A then B in Identity, Body, State, Continuity, Rendering, Production order. Record both reviews in `review-log.yaml`. If one candidate passes with no unresolved Blocker/Major, copy its exact bytes to:

```text
akari-v1.2/accepted/daily/motion/akari-v1.2_d16_motion-doorway-turn_r01.png
```

Set D16 to `status: accepted`, `revision: r01`, and the accepted path. Record `source_paths` and the candidate SHA-256; assert the accepted PNG SHA matches.

- [ ] **Step 6: Add D16 lifecycle coverage and commit acceptance**

Copy the D15 lifecycle class shape, changing constants to D16 and deriving the selected candidate ID and SHA from the recorded review. Preserve the test proving validation succeeds when all local D16 candidates are absent.

Run:

```bash
npm run gate:edit:d16
git add akari-v1.2/accepted/daily/motion/akari-v1.2_d16_motion-doorway-turn_r01.png   akari-v1.2/manifest/assets.yaml akari-v1.2/manifest/review-log.yaml   tests/test_akari_v1_2_daily.py
git commit -m "feat: accept D16 doorway turn"
```

Expected: PASS and exact accepted/source SHA equality.

---

### Task 3: Implement and accept D17 upper-shelf reach

Execute this complete D17 checklist with the following exact identifiers:

```text
asset: D17
descriptor: motion-upper-shelf-reach
phase: 20
dependencies/controllers: D01, D05, C01, C03, C07, D17-scene
action: small-hall-closet-upper-shelf-reach
accepted path: accepted/daily/motion/akari-v1.2_d17_motion-upper-shelf-reach_r01.png
required prompt phrases: upper shelf / slight heel lift / asymmetric shoulders / never ballet tiptoe
```

The scene contract must specify a waist-height hallway three-quarter side camera, one planted foot, only one slight heel lift, one-sided torso extension, both hands visible, and fingertips through both feet in frame. Reject bilateral tiptoe, elongated waist, disconnected reaching shoulder, or performance posing.

- [ ] Write and run failing `D17ContractTests`.
- [ ] Add `D17_STATIC_ASSET_CONTRACT`, D17 r01 references, scene contract, production requirements, candidate policy, hard rejects, and prompt SHA.
- [ ] Create `d17-r01.yaml` with independent A/B paths and no cross-candidate references.
- [ ] Run `npm run gate:edit:d17`; commit `feat: register D17 upper shelf reach`.
- [ ] Generate independent A/B, run `npm run build:v1-2:d17-comparison`, and record ordered original-resolution reviews.
- [ ] Promote the selected exact bytes and add the candidate-absent lifecycle test.
- [ ] Run `npm run gate:edit:d17`; commit `feat: accept D17 upper shelf reach`.

References remain D01, D05, C01, C03, C07. D16 is forbidden as a generation reference.

---

### Task 4: Implement and accept D18 lower-cabinet retrieve

Use:

```text
asset: D18
descriptor: motion-lower-cabinet-retrieve
phase: 21
dependencies/controllers: D01, D12, C01, C03, C07, D18-scene
action: calm-kitchen-lower-cabinet-container-retrieve
accepted path: accepted/daily/motion/akari-v1.2_d18_motion-lower-cabinet-retrieve_r01.png
required prompt phrases: lower cabinet / movement begins at the hips / knees and toes / do not hide the joint chain
```

References are D01 roomwear identity, D12 kitchen structure only, C01 body volume, C03 identity/ornament, and C07 standing socks/feet. The camera is a lightly elevated opposite-counter three-quarter view. Reject waist-only collapse, rigid legs, inward knee/ankle rotation, deep unrelated squat, or cabinet-obscured pelvis/knees/feet.

- [ ] Write and run failing `D18ContractTests`.
- [ ] Add exact D18 static/generation constants and prompt SHA.
- [ ] Create `d18-r01.yaml` with A/B and D18-specific rejects.
- [ ] Run the pending-state focused gate and commit `feat: register D18 lower cabinet retrieve`.
- [ ] Generate independent A/B, build comparison, and review in declared order.
- [ ] Promote exact selected bytes, record SHA linkage, and add candidate-absent lifecycle coverage.
- [ ] Run `npm run gate:edit:d18`; commit `feat: accept D18 lower cabinet retrieve`.

D16 and D17 are forbidden as generation references.

---

### Task 5: Implement and accept D19 cable step-over

Use:

```text
asset: D19
descriptor: motion-cable-step-over
phase: 22
dependencies/controllers: D01, D13, C01, C03, C07, D19-scene
action: cautious-living-room-charging-cable-step-over
accepted path: accepted/daily/motion/akari-v1.2_d19_motion-cable-step-over_r01.png
required prompt phrases: charging cable / planted leg visibly carries the body / not running or jumping / both feet are never airborne
```

References are D01 roomwear identity, D13 cable construction and compact-room scale only, C01 standing body, C03 identity/ornament, and C07 standing socks/feet. Use a side-biased camera slightly above floor level; no carried prop. Reject airborne feet, support-knee hyperextension, ballet-like lifted foot, cable/ankle merge, running, jumping, or dance read.

- [ ] Write and run failing `D19ContractTests`.
- [ ] Add exact D19 static/generation constants and prompt SHA.
- [ ] Create `d19-r01.yaml` with A/B and D19-specific support/cable blockers.
- [ ] Run the pending-state focused gate and commit `feat: register D19 cable step over`.
- [ ] Generate independent A/B, build comparison, and review support foot before lifted foot.
- [ ] Promote exact selected bytes, record SHA linkage, and add candidate-absent lifecycle coverage.
- [ ] Run `npm run gate:edit:d19`; commit `feat: accept D19 cable step over`.

D16-D18 are forbidden as generation references.

---

### Task 6: Implement and accept D20 fitted-sheet pull

Use:

```text
asset: D20
descriptor: motion-fitted-sheet-pull
phase: 23
dependencies/controllers: D01, D08, C01, C03, C07, D20-scene
action: ordinary-bedroom-fitted-sheet-corner-pull
accepted path: accepted/daily/motion/akari-v1.2_d20_motion-fitted-sheet-pull_r01.png
required prompt phrases: fitted-sheet corner / force travels from the planted feet / staggered stance / not an extreme lunge
```

References are D01 roomwear identity, D08 bedroom/bed scale only, C01 standing body, C03 identity/ornament, and C07 standing socks/feet. Use a lightly elevated bed-corner three-quarter side camera. Keep both hands, inclined torso, pelvis, both knees, and both feet visible along a diagonal. Reject arms-only force, unrelated foot directions, extreme lunge/split, bed-obscured joints, glamour, athletic display, or theatrical strain.

- [ ] Write and run failing `D20ContractTests`.
- [ ] Add exact D20 static/generation constants and prompt SHA.
- [ ] Create `d20-r01.yaml` with A/B and D20-specific force-path blockers.
- [ ] Run the pending-state focused gate and commit `feat: register D20 fitted sheet pull`.
- [ ] Generate independent A/B, build comparison, and review the feet-to-hands force path.
- [ ] Promote exact selected bytes, record SHA linkage, and add candidate-absent lifecycle coverage.
- [ ] Run `npm run gate:edit:d20`; commit `feat: accept D20 fitted sheet pull`.

D16-D19 are forbidden as generation references.

---

### Task 7: Close and release Daily Wave 4

**Files:**

- Create: `akari-v1.2/docs/akari-v1.2-daily-wave-4.md`
- Modify: `akari-v1.2/docs/akari-v1.2-daily-handoff.md`
- Modify: `tests/test_akari_v1_2_daily.py`

**Interfaces:**

- Consumes: accepted D16-D20 assets, revisions, candidate IDs, review log, accepted/source hashes, and the Core tree/hash baseline.
- Produces: complete Wave 4 release register and final handoff.

- [ ] **Step 1: Write failing closeout tests**

Add assertions that:

```python
wave4 = ROOT / "akari-v1.2/docs/akari-v1.2-daily-wave-4.md"
handoff = ROOT / "akari-v1.2/docs/akari-v1.2-daily-handoff.md"
self.assertTrue(wave4.is_file())
self.assertIn("**Status:** Wave 4 Complete", wave4.read_text(encoding="utf-8"))
for asset_id in ("D16", "D17", "D18", "D19", "D20"):
    self.assertIn(f"| {asset_id} |", wave4.read_text(encoding="utf-8"))
self.assertIn("D01-D20 accepted", handoff.read_text(encoding="utf-8"))
```

Also assert all five assets are accepted, each selected review source SHA equals the accepted PNG SHA, and validation succeeds with all local D16-D20 candidate directories absent.

- [ ] **Step 2: Run closeout tests and verify failure**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_2_daily.Wave4ReleaseTests -v
```

Expected: FAIL because the release register and completed handoff do not yet exist.

- [ ] **Step 3: Write the Wave 4 release register**

Build the table from the accepted manifests and accepted reviews so no hand-entered revision or candidate identifier can drift:

```python
from pathlib import Path
import yaml

root = Path("akari-v1.2")
assets = yaml.safe_load((root / "manifest/assets.yaml").read_text())
reviews = yaml.safe_load((root / "manifest/review-log.yaml").read_text())
wave_ids = ("D16", "D17", "D18", "D19", "D20")
asset_by_id = {item["asset_id"]: item for item in assets["assets"]}

lines = [
    "# Akari v1.2 Daily.4 Release Register",
    "",
    "**Status:** Wave 4 Complete",
    "",
    "Daily.4 records the accepted Natural Motion sequence from D16 through D20.",
    "",
    "| Asset | Revision | Selected candidate | Accepted path |",
    "| --- | --- | --- | --- |",
]
for asset_id in wave_ids:
    asset = asset_by_id[asset_id]
    selected = next(
        item for item in reviews["reviews"]
        if item["asset_id"] == asset_id
        and item["revision"] == asset["revision"]
        and item["status"] == "accepted"
    )
    assert asset["status"] == "accepted"
    assert len(asset["accepted_paths"]) == 1
    lines.append(
        f"| {asset_id} | {asset['revision']} | {selected['candidate_id']} | "
        f"`{asset['accepted_paths'][0]}` |"
    )

(root / "docs/akari-v1.2-daily-wave-4.md").write_text(
    "\n".join(lines) + "\n", encoding="utf-8"
)
```

After generating the table, append a Core-unchanged paragraph containing the exact baseline commit read from `/tmp/akari-wave4-base` and the successful Core-path diff result.

- [ ] **Step 4: Update the Daily handoff**

State:

```text
Daily.4 / Wave 4 is complete.
D01-D20 accepted.
Wave 4 closes the five Natural Motion scenes: doorway turn, upper-shelf reach,
lower-cabinet retrieve, cable step-over, and fitted-sheet pull.
A future Daily wave requires a new explicit design contract.
```

Keep the Wave 1-3 release register links and append the Wave 4 link.

- [ ] **Step 5: Run focused, integration, and release verification**

Run:

```bash
npm run gate:edit:d20
npm run gate:integration:v1-2
npm run gate:release:v1-2
git diff --exit-code "$(cat /tmp/akari-wave4-base)" -- akari-v1.2/accepted/core
```

Expected:

- all gates PASS
- no accepted Core image-byte change
- D16-D20 lifecycle tests pass without local candidates
- release PDF and release pins remain valid

Task 1 must first run `git rev-parse HEAD > /tmp/akari-wave4-base`; the diff command above then uses that exact recorded baseline.

- [ ] **Step 6: Commit Wave 4 closure**

```bash
git add akari-v1.2/docs/akari-v1.2-daily-wave-4.md   akari-v1.2/docs/akari-v1.2-daily-handoff.md   tests/test_akari_v1_2_daily.py
git commit -m "feat: close Daily Wave 4 natural motion"
```

Run `git status --short`. Expected: only intentionally untracked local candidate/comparison evidence, or a clean tracked worktree.

---

## Execution Checkpoints

After each asset:

1. Preserve the generated A/B originals locally.
2. Record ordered reviews before promotion.
3. Confirm accepted bytes equal the selected source SHA.
4. Run the asset-focused gate.
5. Commit the accepted asset and evidence before beginning the next scene.

Stop the wave and fix the controlling reference or prompt contract when A and B share the same identity, anatomy, outfit, or support failure. Do not spend optional C on a shared failure.

## Final Verification Matrix

| Requirement | Proof |
| --- | --- |
| Same Akari identity | per-candidate Identity review and Accepted Core references |
| Same roomwear outfit | request contracts and original-resolution review |
| Progressive motion load | D16-D20 scene action assertions |
| Full-body structural visibility | scene contracts and Production review |
| Independent generation | no Wave 4 cross-reference paths in any request |
| Ordered A/B review | review-log order and lifecycle validator |
| Exact source promotion | accepted/source SHA equality tests |
| Clean-clone validity | candidate-absent lifecycle tests |
| Core unchanged | Core path diff against Wave 4 base |
| Separate Wave release | `akari-v1.2-daily-wave-4.md` and updated handoff |

# Akari v1.2 C04 Floor-Sitting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, review, and accept one C04 floor-sitting reference that becomes the body-construction dependency for C07 and D01.

**Architecture:** Add an exact single-output C04 r01 generation contract to the existing manifest-driven validator, including broad advisory framing guidance that is never a pixel-only rejection gate. Reuse the existing three-card comparison builder, generate three independent full-frame candidates from four role-locked references, stop for explicit user selection, then promote only the selected PNG byte-for-byte and close the full A/B/C review lifecycle.

**Tech Stack:** Python 3.12+, PyYAML, Pillow, `unittest`, Node/npm scripts, built-in `image_gen`, PNG and WebP assets, Git

## Global Constraints

- Use a 1024 x 1536 portrait canvas and one standalone character per output.
- Use a front-biased light three-quarter camera view at a natural seated viewing height.
- Generate exactly three independent candidates, A/B/C, from one byte-identical prompt and ordered reference contract.
- Open all four references with `view_image` before generation and state every role in the prompt.
- Use accepted C01 for front identity, body volume, outfit, palette, and rendering.
- Use accepted hairpin-side C03 r02 for the three-quarter face, bob, accessories, perspective, and rendering continuity.
- Use the v1.1 standard-foot set for white socks, two pale-blue stripes, ankle volume, and relaxed socked feet.
- Use the legacy seated image as non-controlling anatomy-warning evidence only; never copy its bench, straight-down lower legs, sneakers, exact pose, hands, or scene.
- Keep the fixed white oversized hoodie, gray pleated skirt, two-line socks, and no footwear.
- Keep the pelvis grounded, both legs traceable from thigh root through toe, knees offset, back and pelvis mechanics coordinated, one believable support hand, and relaxed ankles and toes.
- Treat `head_top_y: [70, 160]`, `lowest_toe_y: [1360, 1490]`, and 48 px intended lateral breathing room as advisory comparison evidence only.
- Never reject solely for a broad framing-range miss; reject framing only when crop or scale prevents identity, anatomy, support, or contact review.
- Reject fused or untraceable legs, floating pelvis, contradictory support, explicit sexualization, exposed underwear, severe identity or age drift, material hand or foot defects, shoes, text, logo, watermark, collage, or multiple characters.
- Do not patch, mask, warp, blend, or mechanically composite a candidate into compliance.
- Stop r01 after three candidates. If all three retain a Blocker or Major, close r01 as rejected and design r02 separately.
- Keep `akari-v1.2/source/candidates/c04/r01/` and `akari-v1.2/comparisons/c04-r01/` local-only.
- Stop for explicit user selection before modifying accepted C04 state.
- Run Node/npm commands through `bash -lc` so the repository's fnm-managed Node is available.

---

## File Map

### Durable files created

- `akari-v1.2/manifest/generation-requests/c04-r01.yaml` — exact references, prompt, advisory framing guidance, A/B/C outputs, and review gates.
- `akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png` — user-selected source promoted byte-for-byte.

### Durable files modified

- `scripts/validate_akari_v1_2_natural_form.py` — C04 request, framing-guidance, and dependency validation.
- `tests/test_akari_v1_2_natural_form_package.py` — request, collection, dependency, command, lifecycle, and accepted-state tests.
- `package.json` — `build:v1-2:c04-comparison`.
- `akari-v1.2/manifest/assets.yaml` — C04 changes from candidate r00 to accepted r01 only after user selection.
- `akari-v1.2/manifest/review-log.yaml` — complete A/B/C decisions after user selection.

### Existing code reused unchanged unless a failing test proves otherwise

- `scripts/build_v1_2_candidate_comparison.py` — manifest-driven A/B/C sheet builder.
- `tests/test_build_v1_2_candidate_comparison.py` — generic ordering, dimensions, and missing-input coverage.

### Local-only files

- `akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-a.png`
- `akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-b.png`
- `akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-c.png`
- `akari-v1.2/comparisons/c04-r01/c04-r01-comparison.webp`

---

### Task 1: Add the exact C04 request and advisory framing contract

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/c04-r01.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: `GENERATION_REQUEST_CONTRACTS`, `validate_generation_request(data: dict) -> None`, and `load_generation_requests(request_root: Path) -> list[dict]`.
- Produces: exact contract key `("C04", "r01")` and an ordered `framing_guidance` mapping whose `enforcement` value is `advisory`.

- [ ] **Step 1: Load C04 in the request-test fixture and write failing contract tests**

Add to `NaturalFormGenerationRequestTests.setUp`:

```python
self.c04 = load_yaml(
    PACKAGE_ROOT / "manifest/generation-requests/c04-r01.yaml"
)
```

Add these tests:

```python
def test_c04_request_has_exact_single_output_contract(self):
    validate_generation_request(self.c04)
    self.assertEqual(self.c04["asset_id"], "C04")
    self.assertEqual(self.c04["revision"], "r01")
    self.assertEqual(
        self.c04["variation_axis"], "independent_generation_attempt"
    )
    self.assertEqual(
        [candidate["variant"] for candidate in self.c04["candidates"]],
        ["a", "b", "c"],
    )

def test_c04_framing_guidance_is_advisory_and_broad(self):
    framing = self.c04["framing_guidance"]
    self.assertEqual(framing["enforcement"], "advisory")
    self.assertEqual(framing["head_top_y"], [70, 160])
    self.assertEqual(framing["lowest_toe_y"], [1360, 1490])
    self.assertEqual(framing["intended_lateral_margin_pixels"], 48)
    self.assertFalse(framing["reject_on_numeric_miss_alone"])

def test_c04_rejects_strict_pixel_enforcement(self):
    invalid = copy.deepcopy(self.c04)
    invalid["framing_guidance"]["enforcement"] = "hard"
    with self.assertRaisesRegex(
        ValidationError, "exact framing guidance required"
    ):
        validate_generation_request(invalid)

def test_c04_rejects_reordered_references(self):
    invalid = copy.deepcopy(self.c04)
    invalid["references"][0], invalid["references"][1] = (
        invalid["references"][1], invalid["references"][0]
    )
    with self.assertRaisesRegex(
        ValidationError, "exact reference contract"
    ):
        validate_generation_request(invalid)

def test_c04_rejects_noncanonical_candidate_path(self):
    invalid = copy.deepcopy(self.c04)
    invalid["candidates"][0]["target_path"] = "source/candidates/c04/a.png"
    with self.assertRaisesRegex(
        ValidationError, "candidate target path"
    ):
        validate_generation_request(invalid)
```

- [ ] **Step 2: Run the focused tests and verify red**

Run:

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
```

Expected: ERROR because `c04-r01.yaml` does not exist.

- [ ] **Step 3: Create the exact request manifest**

Create `c04-r01.yaml` with this content:

```yaml
schema_version: 1
request_id: akari-v1.2-c04-r01
asset_id: C04
revision: r01
variation_axis: independent_generation_attempt
references:
  - role: accepted_c01_front_identity
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
  - role: accepted_c03_hairpin_three_quarter
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
  - role: v1_1_indoor_foot_construction
    path: akari-v1.2/references/v1.1/standard-foot-set.webp
  - role: legacy_seated_anatomy_warning
    path: akari-v1.2/references/legacy/seated.webp
shared_prompt: >-
  Use the four visible images only in their declared roles. Create one
  standalone full-body floor-sitting reference of the same naturally cute
  25-year-old Akari on a 1024 x 1536 nearly plain low-contrast rug canvas.
  Use a front-biased light three-quarter view at a natural seated viewing
  height. C01 controls adult identity, healthy body volume, fixed white
  oversized hoodie and gray pleated skirt, palette, and rendering. Accepted
  hairpin-side C03 r02 controls the three-quarter face, short fluffy
  light-brown bob, warm amber eyes, rounded cheeks, compact chin, and correct
  character-left pale-blue crossed pins and ribbon-like ornament. The v1.1
  foot reference controls white socks with two pale-blue stripes, ankle volume,
  and relaxed socked feet; do not reproduce its text or panel layout. The
  legacy seated image is non-controlling anatomy-warning evidence for pelvis,
  leg volume, and garment compression only. Do not copy its bench,
  straight-down lower legs, shoes, hand placement, scene, or exact pose. Seat
  the pelvis visibly on the rug with a slight posterior tilt and coordinated
  natural rounding through the back and dropped shoulders. Flow both legs
  loosely from the front toward one side, offset the knees, and keep a clearly
  traceable front leg and rear leg from thigh root through relaxed socked toes.
  Use one hand for the minimum believable body support and rest the other on a
  knee or the rug. Show modest gravity and contact response in thighs, hoodie,
  and skirt. Keep the complete head, hair, hands, socks, and toes visible. Aim
  broadly for head top y=70..160, lowest toe y=1360..1490, and about 48 px or
  more lateral breathing room, but preserve believable anatomy and pose over
  exact pixel placement. Use a small calm secure expression without C05 bed
  hair or the C06 expression gradient. No chair, bench, bed, room scene,
  props, shoes, exposed underwear, sexualized pose, symmetrical symbol pose,
  artificially aligned toes, fused or untraceable limbs, floating pelvis,
  contradictory support, thin legs, elongated proportions, childlike or
  glamorous drift, dramatic lighting, photorealistic skin, readable text,
  logo, watermark, border, collage, grid, or multiple character.
framing_guidance:
  canvas: {width: 1024, height: 1536}
  enforcement: advisory
  head_top_y: [70, 160]
  lowest_toe_y: [1360, 1490]
  intended_lateral_margin_pixels: 48
  reject_on_numeric_miss_alone: false
  major_only_when: crop-or-scale-prevents-structural-review
candidates:
  - variant: a
    title: independent-attempt-a
    target_path: source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-a.png
  - variant: b
    title: independent-attempt-b
    target_path: source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-b.png
  - variant: c
    title: independent-attempt-c
    target_path: source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-c.png
comparison_anchors: []
acceptance_gates: [identity, body, rendering]
hard_rejects:
  - fused missing duplicated disconnected or untraceable limbs or joints
  - floating pelvis or support placement that contradicts body weight
  - severe identity or age drift
  - exposed underwear or explicit sexualization
  - material hand foot sock skirt or hairpin defect
  - shoes or wrong fixed outfit
  - unreadable anatomy caused by crop or extreme subject scale
  - readable text logo watermark collage or multiple character
```

- [ ] **Step 4: Add the exact validator contract**

Add this constant beside `C03_R02_FRAMING_CONTRACT`:

```python
C04_R01_FRAMING_GUIDANCE = {
    "canvas": {"width": 1024, "height": 1536},
    "enforcement": "advisory",
    "head_top_y": [70, 160],
    "lowest_toe_y": [1360, 1490],
    "intended_lateral_margin_pixels": 48,
    "reject_on_numeric_miss_alone": False,
    "major_only_when": "crop-or-scale-prevents-structural-review",
}
```

Add `("C04", "r01")` to `GENERATION_REQUEST_CONTRACTS`:

```python
("C04", "r01"): {
    "variation_axis": "independent_generation_attempt",
    "references": (
        (
            "accepted_c01_front_identity",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
        ),
        (
            "accepted_c03_hairpin_three_quarter",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c03_hairpin-side-45_r02.png",
        ),
        (
            "v1_1_indoor_foot_construction",
            "akari-v1.2/references/v1.1/standard-foot-set.webp",
        ),
        (
            "legacy_seated_anatomy_warning",
            "akari-v1.2/references/legacy/seated.webp",
        ),
    ),
    "candidate_prefix": "source/candidates/c04/r01/",
    "candidate_stem": "akari-v1.2_c04_floor-sitting_r01",
    "candidate_detail": None,
    "output_specs": None,
    "comparison_anchors": (),
    "framing_contract": None,
    "framing_guidance": C04_R01_FRAMING_GUIDANCE,
},
```

Add `"framing_guidance": None` to every existing request contract. After the
existing `framing_contract` validation, add:

```python
expected_guidance = contract["framing_guidance"]
actual_guidance = data.get("framing_guidance")
if expected_guidance is None:
    if "framing_guidance" in data:
        raise ValidationError(
            "generation request: unexpected framing guidance"
        )
elif ordered_value(actual_guidance) != ordered_value(expected_guidance):
    raise ValidationError(
        "generation request: exact framing guidance required"
    )
```

- [ ] **Step 5: Update request collection expectations and verify green**

Change the exact request-order expectation to:

```python
[
    ("C01", "r01"),
    ("C02", "r01"),
    ("C03", "r01"),
    ("C03", "r02"),
    ("C04", "r01"),
]
```

Change the generation-count expectation to `(15, 21)`, then run:

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests -v
```

Expected: PASS.

- [ ] **Step 6: Commit the request contract**

```sh
git add akari-v1.2/manifest/generation-requests/c04-r01.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: define Natural Form C04 generation contract"
```

---

### Task 2: Enforce accepted C04 generation dependencies

**Files:**

- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: accepted asset records for C01 r01, C02 r01, and C03 r02.
- Produces: `validate_generation_dependencies(assets: dict, requests: list[dict]) -> None` enforcement for every C04 request revision.

- [ ] **Step 1: Write failing C04 dependency tests**

Add:

```python
def test_c04_declares_all_standing_dependencies(self):
    c04 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C04"
    )
    self.assertEqual(c04["depends_on"], ["C01", "C02", "C03"])

def test_c04_requires_accepted_c01_c02_and_c03(self):
    for asset_id in ("C01", "C02", "C03"):
        with self.subTest(asset_id=asset_id):
            invalid = copy.deepcopy(self.assets)
            asset = next(
                item for item in invalid["assets"]
                if item["asset_id"] == asset_id
            )
            asset.update(status="candidate", revision="r00", accepted_paths=[])
            with self.assertRaisesRegex(
                ValidationError,
                "C04 requires accepted C01 r01, C02 r01, and C03 r02",
            ):
                validate_generation_dependencies(invalid, self.requests)

def test_c04_requires_exact_accepted_reference_paths(self):
    invalid = copy.deepcopy(self.requests)
    c04 = next(item for item in invalid if item["asset_id"] == "C04")
    c04["references"][1]["path"] = (
        "akari-v1.2/accepted/core/standing/substituted-c03.png"
    )
    with self.assertRaisesRegex(
        ValidationError,
        "C04 requires accepted C01 r01, C02 r01, and C03 r02",
    ):
        validate_generation_dependencies(self.assets, invalid)
```

- [ ] **Step 2: Run the focused tests and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests -v
```

Expected: FAIL because dependency validation has no C04 branch.

- [ ] **Step 3: Implement C04 dependency validation**

In `validate_generation_dependencies`, bind `c03 = assets_by_id["C03"]` and
add:

```python
c04_requests = [item for item in requests if item["asset_id"] == "C04"]
expected_c01 = (
    "akari-v1.2/accepted/core/standing/"
    "akari-v1.2_c01_front-natural-stance_r01.png"
)
expected_c03 = (
    "akari-v1.2/accepted/core/standing/"
    "akari-v1.2_c03_hairpin-side-45_r02.png"
)
for request in c04_requests:
    if (
        (c01["status"], c01["revision"]) != ("accepted", "r01")
        or (c02["status"], c02["revision"]) != ("accepted", "r01")
        or (c03["status"], c03["revision"]) != ("accepted", "r02")
        or request["references"][0]["path"] != expected_c01
        or request["references"][1]["path"] != expected_c03
    ):
        raise ValidationError(
            "C04 requires accepted C01 r01, C02 r01, and C03 r02 "
            "at its declared anchors"
        )
```

This deliberately checks C02 as accepted dependency state without adding a
fifth image-generation reference.

- [ ] **Step 4: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests -v
uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v
git add scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "test: enforce Natural Form C04 dependencies"
```

---

### Task 3: Add the C04 comparison command without new layout code

**Files:**

- Modify: `package.json`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`
- Verify unchanged: `scripts/build_v1_2_candidate_comparison.py`
- Verify unchanged: `tests/test_build_v1_2_candidate_comparison.py`

**Interfaces:**

- Consumes: `build_comparison(request_path: Path, package_root: Path, output_path: Path, anchor_path: Path | None = None) -> Path`.
- Produces: npm command `build:v1-2:c04-comparison` and `akari-v1.2/comparisons/c04-r01/c04-r01-comparison.webp`.

- [ ] **Step 1: Add the failing package-command expectation**

Add to `natural_form_commands` in `NaturalFormIsolationTests`:

```python
"build:v1-2:c04-comparison": (
    "uv run python scripts/build_v1_2_candidate_comparison.py "
    "--request akari-v1.2/manifest/generation-requests/c04-r01.yaml "
    "--output akari-v1.2/comparisons/c04-r01/"
    "c04-r01-comparison.webp"
),
```

- [ ] **Step 2: Verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests.test_package_command_reserves_unqualified_v1_2_for_natural_form -v
```

Expected: FAIL because the command is absent.

- [ ] **Step 3: Add the exact package command**

Add to `package.json` beside the C03 commands:

```json
"build:v1-2:c04-comparison": "uv run python scripts/build_v1_2_candidate_comparison.py --request akari-v1.2/manifest/generation-requests/c04-r01.yaml --output akari-v1.2/comparisons/c04-r01/c04-r01-comparison.webp"
```

- [ ] **Step 4: Prove the reused builder still fits C04**

```sh
uv run python -m unittest tests.test_build_v1_2_candidate_comparison -v
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests -v
```

Expected: PASS. Do not modify the builder when these tests remain green.

- [ ] **Step 5: Commit**

```sh
git add package.json tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: add Natural Form C04 comparison command"
```

---

### Task 4: Generate and freeze three local C04 candidates

**Files:**

- Create local-only: `akari-v1.2/source/candidates/c04/r01/*.png`
- Do not modify durable manifests or accepted assets.

**Interfaces:**

- Consumes: the four ordered references and byte-identical `shared_prompt` from `c04-r01.yaml`.
- Produces: exactly three full-frame PNGs at the declared A/B/C paths.

- [ ] **Step 1: Validate the durable contract before generation**

```sh
bash -lc 'npm run validate:v1-2'
```

Expected: PASS with C04 still `candidate` r00 and without C04 reviews.

- [ ] **Step 2: Open and inspect every reference**

Use `view_image` with `detail: original` for, in order:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
akari-v1.2/references/v1.1/standard-foot-set.webp
akari-v1.2/references/legacy/seated.webp
```

Reconfirm that the legacy image is bench sitting with shoes and therefore
non-controlling.

- [ ] **Step 3: Generate A with the exact prompt and declared roles**

Call built-in `image_gen` with the four absolute reference paths and the exact
`shared_prompt`. Add only this role header before the prompt:

```text
Use case: stylized-concept
Asset type: Akari v1.2 canonical character reference
Input images: Image 1 controls accepted front identity/body/outfit/rendering;
Image 2 controls accepted hairpin-side three-quarter identity/perspective;
Image 3 controls sock and relaxed indoor-foot construction only; Image 4 is a
non-controlling warning for pelvis/leg/garment compression and must not supply
its bench, shoes, scene, hands, straight-down legs, or exact pose.
```

Save the returned full-frame PNG as the declared A path. Do not edit it.

- [ ] **Step 4: Repeat independently for B and C**

Reopen the same four references before each call. Use the same role header and
byte-identical `shared_prompt`; do not use A as a reference for B or C. Save
each result directly to its declared path without overwriting earlier output.

- [ ] **Step 5: Recover any missing local payload structurally**

If an image appeared in the interface but the PNG is missing, search the
current-date rollout for `image_generation_call`, parse JSONL records, decode
only a `result` beginning with `iVBOR`, verify the decoded signature is
`89504e470d0a1a0a`, and save it to the matching candidate path. Never print or
copy the base64 payload through terminal output.

- [ ] **Step 6: Verify and freeze all three candidates**

```sh
file akari-v1.2/source/candidates/c04/r01/*.png
identify -format '%f %wx%h\n' akari-v1.2/source/candidates/c04/r01/*.png
sha256sum akari-v1.2/source/candidates/c04/r01/*.png
git status --short
```

Expected: exactly three real 1024 x 1536 PNGs, three unique SHA-256 values, and
no candidate staged or tracked. If a tool returns a different dimension, keep
the original local output for evidence and treat that candidate as ineligible;
do not resize it into compliance.

---

### Task 5: Build the comparison, review A/B/C, and stop for user selection

**Files:**

- Create local-only: `akari-v1.2/comparisons/c04-r01/c04-r01-comparison.webp`
- Do not modify accepted state.

**Interfaces:**

- Consumes: the three frozen candidate PNGs in manifest order.
- Produces: one equal-scale comparison and a written A/B/C review recommendation.

- [ ] **Step 1: Build the comparison**

```sh
bash -lc 'npm run build:v1-2:c04-comparison'
```

Expected: prints `akari-v1.2/comparisons/c04-r01/c04-r01-comparison.webp`.

- [ ] **Step 2: Verify the review artifact**

```sh
file akari-v1.2/comparisons/c04-r01/c04-r01-comparison.webp
identify akari-v1.2/comparisons/c04-r01/c04-r01-comparison.webp
git status --short
```

Expected: a readable WebP with three cards in A/B/C order and no tracked
comparison change.

- [ ] **Step 3: Review candidates in the required order**

Open the comparison and each full-resolution candidate. For each image record:

1. identity and adult age
2. pelvis contact and posterior tilt
3. thigh roots and identifiable front/rear leg
4. knees, shins, ankles, and relaxed toes
5. support hand and whole-body center of mass
6. hoodie, skirt compression, two-line socks, and no shoes
7. hairpin, hands, artifacts, text, logos, and crop
8. advisory head-top, lowest-toe, and lateral-margin observations

Do not assign Major from advisory pixels alone. Stop reviewing a candidate when
a Blocker is found.

- [ ] **Step 4: Present the comparison and stop**

Give the user the A/B/C comparison, concise findings, and a quality-first
recommendation. Ask for an explicit `A`, `B`, or `C` selection. Do not promote,
edit manifests, or generate more candidates in this task.

---

### Task 6: Promote exactly the user-selected C04 candidate

**Files:**

- Create: `akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: explicit user selection, the three frozen paths, SHA-256 values,
  and completed findings from Task 5.
- Produces: one accepted C04 r01 asset and one complete ordered review batch
  with exactly one accepted decision.

- [ ] **Step 1: Reconfirm the selection and candidate hashes**

Map the user's literal selection to exactly one declared source path. Run:

```sh
sha256sum akari-v1.2/source/candidates/c04/r01/*.png
```

Record those exact three outputs before editing YAML. Stop if any digest differs
from Task 4.

- [ ] **Step 2: Write failing final-state tests using the selected variant and observed digest**

Add tests with the literal selected candidate ID, source path, and SHA-256 from
Step 1:

```python
def test_c04_acceptance_links_asset_review_and_declared_candidate(self):
    c04 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C04"
    )
    self.assertEqual(c04["status"], "accepted")
    self.assertEqual(c04["revision"], "r01")
    self.assertEqual(
        c04["accepted_paths"],
        [
            "accepted/core/sitting/"
            "akari-v1.2_c04_floor-sitting_r01.png"
        ],
    )
    reviews = [
        review for review in self.review_log["reviews"]
        if (review["asset_id"], review["revision"]) == ("C04", "r01")
    ]
    self.assertEqual(
        [review["candidate_id"] for review in reviews],
        ["c04-r01-a", "c04-r01-b", "c04-r01-c"],
    )
    self.assertEqual(
        len([review for review in reviews if review["status"] == "accepted"]),
        1,
    )
    validate_assets(self.assets, PACKAGE_ROOT)
    validate_review_log(self.review_log)
    validate_lifecycle_linkage(
        self.assets,
        self.generation_requests,
        self.review_log,
        PACKAGE_ROOT,
    )
```

The existing lifecycle validator supplies the exact source-path and digest
assertions: the accepted review must match one declared A/B/C source, and the
promoted accepted PNG must match that review's recorded SHA-256.

- [ ] **Step 3: Verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
```

Expected: FAIL because C04 is still candidate r00 and has no review batch.

- [ ] **Step 4: Promote the exact selected source byte-for-byte**

Use exactly one of these byte-preserving copies according to the user's
literal selection:

```sh
# Run only for selection A
cp akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-a.png \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png

# Run only for selection B
cp akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-b.png \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png

# Run only for selection C
cp akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-c.png \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
```

The destination is:

```text
akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
```

Prove identity with exactly one corresponding command:

```sh
# Run only for selection A
cmp --silent \
  akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-a.png \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png

# Run only for selection B
cmp --silent \
  akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-b.png \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png

# Run only for selection C
cmp --silent \
  akari-v1.2/source/candidates/c04/r01/akari-v1.2_c04_floor-sitting_r01-c.png \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png

sha256sum akari-v1.2/source/candidates/c04/r01/*.png \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
```

The accepted digest must equal the digest of the one selected source.

- [ ] **Step 5: Update the C04 asset and append the exact A/B/C reviews**

Change only the C04 record in `assets.yaml` to:

```yaml
    status: accepted
    revision: r01
    accepted_paths:
      - accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
```

Append three C04 r01 reviews in A/B/C order. Each review must use its literal
source path and observed digest, its actual Task 5 findings, and a decision that
states whether it was selected or why it was rejected. The selected review must
have `status: accepted`, `findings: []` or only resolved/minor findings, and no
unresolved Blocker or Major. The other two must have `status: rejected`.

- [ ] **Step 6: Verify lifecycle green and byte identity**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
sha256sum akari-v1.2/source/candidates/c04/r01/*.png \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
```

Expected: PASS, with the accepted digest matching exactly one candidate: the
user-selected source. Re-run the corresponding `cmp --silent` command from
Step 4 and require exit code 0.

- [ ] **Step 7: Commit durable acceptance only**

```sh
git add akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  tests/test_akari_v1_2_natural_form_package.py
git status --short
git commit -m "feat: accept Natural Form C04 r01"
```

Before committing, confirm no candidate PNG or comparison WebP is staged.

---

### Task 7: Run final merged-state verification

**Files:**

- Verify only; do not change scope to fix unrelated failures.

**Interfaces:**

- Consumes: final C04 request, command, reviews, asset, and accepted PNG.
- Produces: fresh completion evidence on the final branch state.

- [ ] **Step 1: Run focused and full test suites**

```sh
uv run python -m unittest tests.test_build_v1_2_candidate_comparison -v
bash -lc 'npm run test:node'
bash -lc 'npm run test:python'
bash -lc 'npm run validate:v1-2'
```

Expected: PASS.

- [ ] **Step 2: Run audits and Markdown lint**

```sh
bash -lc 'npm run audit'
bash -lc 'npm run lint:md'
```

Expected: PASS and zero Markdown errors.

- [ ] **Step 3: Prove final artifact and repository hygiene**

```sh
file akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
identify -format '%f %wx%h\n' \
  akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
git diff --check
git status --short --branch
```

Expected: a real 1024 x 1536 PNG, no whitespace errors, no staged or tracked
candidate/comparison output, and a clean durable working tree. Report any
local-only candidates and comparison sheet separately from tracked status.

---

## Execution Stop Conditions

- Stop before Task 4 if contract or dependency validation is red.
- Stop a candidate immediately for a Blocker; do not spend review effort on its polish.
- Stop after Task 5 until the user explicitly selects A, B, or C.
- Stop before promotion if the selected candidate has an unresolved Blocker or Major.
- Stop r01 after three candidates; do not silently generate a fourth attempt.
- Stop completion claims until all Task 7 commands have fresh passing output.

# Akari v1.2 D01 Morning Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, review, explicitly select, and byte-identically accept one
D01 r01 morning-bedside image that proves C04, C05, C06-2, and C07 seated work
together, then record the Gate 4 Natural Form release decision.

**Architecture:** Add one exact D01 generation request and specialized validator
contract beside the existing C06 specialization, plus a thin D01 comparison
builder that reuses the established grid renderer. Candidate image dimensions
are inspected only when local files exist and accept 1020-1028 by 1532-1540;
review findings carry their controlling Core asset, while one top-level Gate 4
record links the selected review to Release, Conditional Release, or Hold.

**Tech Stack:** Python 3.13, PyYAML, Pillow, `unittest`, npm scripts, built-in
`image_gen`, the Akari image-review workflow, SHA-256, Git.

## Global Constraints

- Work only in `/path/to/akari-design/.worktrees/codex-d01-morning-validation`
  on branch `codex/d01-morning-validation`, based on local `main` commit
  `5b1975e`.
- Treat
  `docs/superpowers/specs/2026-07-15-akari-v1-2-d01-morning-validation-design.md`
  as authoritative.
- D01 is an integration validation asset, not a wallpaper and not a new Core
  pose standard.
- Use exactly four visible accepted references in this order: C04 r01 floor
  sitting, C05 r01 morning hair, C06-2 r01 sleepy-secure expression, and C07
  r01 seated sock feet.
- Reopen all four accepted references at original detail immediately before
  every image-generation call and state each reference role in the prompt.
- Never use legacy paths, local Core candidates, comparison boards, D01 A, D01
  B, or D01 C as a generation reference.
- Keep the character-left pale-blue crossed pins and ribbon-like ornament.
- Use a loose opaque white short-sleeve T-shirt, opaque gray shorts-style
  roomwear, and warm-white mid-calf socks with exactly two thin pale-blue
  stripes.
- Seat Akari on a low-contrast rug beside a restrained bed edge, using a
  front-biased light three-quarter camera at natural seated viewing height.
- Keep the complete head, ornament, both hands, both legs, heels, and socked
  toes visible.
- Keep the room medium-density and prop-free: no clock, phone, mug, readable
  book, explanatory object, logo, or text.
- Generate independent A and B candidates first from the same frozen request.
  Do not generate C when either A or B is eligible.
- Permit C only for D01-scene staging, room, light, or presentation failures.
  Shared body, hair, expression, or foot failures stop D01 and reopen the
  controlling Core asset.
- Target 1024 x 1536. Accept width 1020-1028 and height 1532-1540. Do not resize,
  crop, pad, stretch, warp, patch, mask, or composite an eligible candidate to
  force exact dimensions.
- Review in Identity, Body, State, Rendering, Production order and stop on a
  Blocker. Within Body, inspect pelvis, thigh roots, knees, shins, ankles,
  heels, toes, hand support, then whole-body weight.
- `accepted` permits no unresolved finding. `accepted-with-notes` permits only
  unresolved D01-scene Minor findings while C01-C07 remain strictly accepted.
- Promote only after the user returns one exact eligible candidate ID.
- Prove the accepted PNG is byte-identical to the selected candidate with
  `cmp` and the same lowercase SHA-256.
- Keep candidate PNGs, comparison WebPs, and review crops local-only. Stage
  durable paths explicitly; never use `git add -A`.
- Preserve the main workspace's local C04-C07 candidate and comparison evidence
  and preserve D01 local evidence before removing the worktree.
- Follow red-green-refactor and commit after every independently testable task.
- Do not push the feature branch or `main`.

---

## File Map

### Durable files created

- `akari-v1.2/manifest/generation-requests/d01-r01.yaml` - frozen D01 request,
  A/B declarations, optional-C policy, dimensions, and review gates.
- `scripts/build_v1_2_d01_comparison.py` - canonical A/B or A/B/C comparison
  builder with traversal and symlink protection.
- `tests/test_build_v1_2_d01_comparison.py` - comparison ordering and boundary
  tests.
- `akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png`
  - selected candidate after explicit user approval.

### Durable files modified

- `scripts/validate_akari_v1_2_natural_form.py` - D01 static request,
  dependency, dimensions, review, lifecycle, and Gate 4 contracts.
- `tests/test_akari_v1_2_natural_form_package.py` - exact D01 contracts,
  tolerance, review provenance, acceptance, release, and regressions.
- `package.json` - `build:v1-2:d01-comparison` command.
- `akari-v1.2/manifest/assets.yaml` - D01 accepted r01 state after selection.
- `akari-v1.2/manifest/review-log.yaml` - A/B or A/B/C reviews and final Gate 4
  record.
- `akari-v1.2/README.md` - release classification after Gate 4 passes.
- `akari-v1.2/docs/akari-v1.2-core-design.md` - matching final package status.

### Local-only files

- `akari-v1.2/source/candidates/d01/r01/*.png`
- `akari-v1.2/comparisons/d01-r01/d01-r01-comparison.webp`
- `tmp/d01-review/` if original-scale inspection crops are needed.

---

### Task 1: Add the exact D01 generation request and static contract

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/d01-r01.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py:20-230,430-858,997-1082`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:69-125,438-1110`

**Interfaces:**

- Consumes: `validate_generation_request(data: dict) -> None`,
  `validate_assets(data: dict, package_root: Path | None = None) -> None`.
- Produces: `D01_STATIC_ASSET_CONTRACT`, `D01_R01_SIZE_POLICY`,
  `validate_d01_generation_request(data: dict, contract: dict) -> None`, and a
  ninth validated generation request with two initial candidate outputs.

- [ ] **Step 1: Write failing exact-contract tests**

Add `self.d01` loading to `NaturalFormGenerationRequestTests.setUp`, then add
tests which call `validate_generation_request` after independently mutating the
request ID, variation axis, each ordered reference role/path, shared prompt,
scene contract, production requirements, candidate policy, A/B order, candidate
path, acceptance gates, and hard rejects. Each mutation must raise the named
D01 contract error, while the untouched request must pass.

Use this mutation-test body after loading `self.d01`:

```python
def test_d01_request_matches_frozen_contract(self):
    validate_generation_request(self.d01)


def test_d01_rejects_frozen_contract_mutations(self):
    cases = (
        (
            "request id",
            lambda data: data.__setitem__("request_id", "akari-v1.2-d01-r02"),
            "request_id mismatch",
        ),
        (
            "variation axis",
            lambda data: data.__setitem__("variation_axis", "scene_style"),
            "invalid variation axis",
        ),
        (
            "reference role",
            lambda data: data["references"][0].__setitem__("role", "body"),
            "exact reference contract required",
        ),
        (
            "reference path",
            lambda data: data["references"][2].__setitem__(
                "path",
                "akari-v1.2/accepted/core/face-hair/"
                "akari-v1.2_c06-1_sleepy-neutral_r01.png",
            ),
            "exact reference contract required",
        ),
        (
            "prompt",
            lambda data: data.__setitem__(
                "shared_prompt", data["shared_prompt"] + " altered"
            ),
            "D01 exact shared prompt contract mismatch",
        ),
        (
            "scene",
            lambda data: data["scene_contract"].__setitem__(
                "room_density", "cluttered"
            ),
            "D01 scene contract mismatch",
        ),
        (
            "production",
            lambda data: data["production_requirements"][
                "accepted_width"
            ].__setitem__("minimum", 1019),
            "D01 production contract mismatch",
        ),
        (
            "policy",
            lambda data: data["candidate_policy"].__setitem__(
                "cross_candidate_references", "allowed"
            ),
            "D01 candidate policy mismatch",
        ),
        (
            "candidate order",
            lambda data: data["candidates"].reverse(),
            "D01 candidate contract mismatch",
        ),
        (
            "candidate path",
            lambda data: data["candidates"][0].__setitem__(
                "target_path", "source/candidates/d01/r01/substitute.png"
            ),
            "D01 candidate contract mismatch",
        ),
        (
            "gates",
            lambda data: data.__setitem__(
                "acceptance_gates", ["identity", "body"]
            ),
            "D01 acceptance gates mismatch",
        ),
        (
            "hard rejects",
            lambda data: data["hard_rejects"].pop(),
            "D01 exact hard rejects required",
        ),
    )
    for name, mutate, message in cases:
        with self.subTest(name=name):
            invalid = copy.deepcopy(self.d01)
            mutate(invalid)
            with self.assertRaisesRegex(ValidationError, message):
                validate_generation_request(invalid)
```

Add this exact static asset assertion to `NaturalFormManifestTests`:

```python
def test_d01_has_exact_static_asset_contract(self):
    d01 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "D01"
    )
    self.assertEqual(
        {key: d01[key] for key in (
            "descriptor", "phase", "variants", "expected_paths",
            "depends_on", "gate",
        )},
        {
            "descriptor": "morning-bedside",
            "phase": 4,
            "variants": ["default"],
            "expected_paths": [
                "accepted/daily-validation/"
                "akari-v1.2_d01_morning-bedside_rNN.png"
            ],
            "depends_on": ["C04", "C05", "C06", "C07"],
            "gate": "daily",
        },
    )
```

- [ ] **Step 2: Run the focused tests and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests.test_d01_has_exact_static_asset_contract \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
```

Expected: the static assertion passes, while D01 request loading or validation
fails because `d01-r01.yaml` and its specialized validator do not exist.

- [ ] **Step 3: Create the frozen request**

Create `akari-v1.2/manifest/generation-requests/d01-r01.yaml` with this exact
structure and wording:

```yaml
schema_version: 1
request_id: akari-v1.2-d01-r01
asset_id: D01
revision: r01
variation_axis: independent_scene_attempt
references:
  - role: accepted_c04_floor_sitting_body
    path: akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
  - role: accepted_c05_morning_hair
    path: akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
  - role: accepted_c06_sleepy_secure_expression
    path: akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png
  - role: accepted_c07_seated_sock_feet
    path: akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png
shared_prompt: >-
  Use the four visible accepted images only in their declared roles to create
  one standalone morning-bedside illustration of the same naturally cute
  25-year-old Akari. Image 1 controls the C04 floor-sitting mechanical family:
  visible pelvis support, slight posterior tilt, coordinated back rounding,
  dropped shoulders, one believable supporting hand, healthy leg volume, and
  traceable front and rear legs. Image 2 controls adult identity, reversible
  C05 morning hair, complete character-left pale-blue crossed pins and
  ribbon-like ornament, cheek shape, short-bob length, palette, and rendering;
  do not copy its chest-up crop or hoodie. Image 3 controls only the C06-2
  sleepy-secure expression: heavy but open eyelids, incomplete viewer-directed
  focus, relaxed brows and cheeks, and a quiet closed almost-neutral mouth.
  Image 4 controls C07 seated warm-white mid-calf socks with exactly two thin
  pale-blue stripes, ankle and foot volume, relaxed toes, heel placement, and
  floor contact; do not copy its hoodie, skirt, or upper-body crop. Seat Akari
  on a low-contrast rug beside a restrained bed edge with slightly rumpled
  bedding. Use a front-biased light three-quarter camera at natural seated
  viewing height and soft morning natural light filtered through an implied or
  lightly shown curtain. Dress her in a loose opaque white short-sleeve T-shirt
  and simple opaque gray shorts-style roomwear. Keep the complete head,
  ornament, both hands, both legs, heels, and socked toes visible. Keep the room
  lived-in at medium density but add no clock, phone, mug, readable book, or
  explanatory prop. The moment must feel just after waking rather than a posed
  portrait. When references conflict, C04 controls body mechanics and support,
  C05 controls morning hair and ornament, C06-2 controls facial state, and C07
  seated controls socks, ankles, feet, and contact. Do not copy any reference
  background, crop, disallowed outfit, or non-controlling expression.
scene_contract:
  camera: front-biased-light-three-quarter-at-natural-seated-viewing-height
  surface: low-contrast-rug-beside-restrained-bed-edge
  lighting: soft-curtain-filtered-morning-natural-light
  room_density: medium-lived-in-not-cluttered
  gaze: viewer-directed-with-incomplete-sleepy-focus
  outfit:
    top: loose-opaque-white-short-sleeve-t-shirt
    bottom: simple-opaque-gray-shorts-style-roomwear
    socks: warm-white-mid-calf-exactly-two-thin-pale-blue-stripes
  required_visible_features:
    - complete-head-and-ornament
    - both-hands-including-one-believable-supporting-hand
    - pelvis-support-and-both-thigh-roots
    - both-knees-shins-ankles-heels-and-socked-toes
  forbidden_props: [clock, phone, mug, readable-book, explanatory-prop]
production_requirements:
  file_format: png
  target_canvas: {width: 1024, height: 1536}
  accepted_width: {minimum: 1020, maximum: 1028}
  accepted_height: {minimum: 1532, maximum: 1540}
  standalone_composition: true
  generated_grid: forbidden
  force_exact_resize: forbidden
candidate_policy:
  initial_variants: [a, b]
  optional_variant: c
  optional_c_only_for: d01-scene-staging-background-lighting-or-presentation
  stop_for_shared_core_failure: [C04, C05, C06, C07]
  cross_candidate_references: forbidden
candidates:
  - variant: a
    title: independent-scene-a
    target_path: source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-a.png
  - variant: b
    title: independent-scene-b
    target_path: source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-b.png
comparison_anchors: []
acceptance_gates: [identity, body, state, rendering, production]
hard_rejects:
  - severe identity age face body-volume or rendering drift
  - fused missing duplicated disconnected or untraceable limbs or joints
  - floating pelvis or hand support that contradicts body weight
  - thin legs twisted ankles pointed ballet toes or contradictory foot contact
  - missing mirrored relocated duplicated or materially redesigned ornament
  - non-reversible hair wrong hair length extreme bed head wet hair or wind
  - closed eyes distress intoxication sensual posing broad smile or open mouth
  - wrong outfit sheer clothing exposed underwear shoes slippers or bare feet
  - incorrect sock height stripe count ankle volume toe relaxation or contact
  - crop or scale that prevents complete body support or feet review
  - readable text logo watermark border collage grid or multiple character
```

- [ ] **Step 4: Add exact constants and specialized validation**

Add `D01_STATIC_ASSET_CONTRACT`, `D01_R01_SIZE_POLICY`, the exact reference
tuple, scene contract, candidate policy, gates, hard rejects, and SHA-256 of the
literal shared prompt beside the C06 constants. Add `("D01", "r01")` to
`GENERATION_REQUEST_CONTRACTS` and dispatch it before the generic candidate
path in `validate_generation_request`:

```python
D01_R01_SHARED_PROMPT_SHA256 = (
    "ad9c1e9f86e18cb912ed32eed624d03bd0e05b9bfd0c09071e344b2076ca5232"
)
```

```python
if key == ("D01", "r01"):
    validate_d01_generation_request(data, contract)
    return
```

Implement `validate_d01_generation_request` so the only accepted candidate
lists are A/B and A/B/C, with titles and paths derived exactly as follows:

```python
def d01_candidate_path(variant: str) -> str:
    return (
        "source/candidates/d01/r01/"
        f"akari-v1.2_d01_morning-bedside_r01-{variant}.png"
    )


def validate_d01_generation_request(data: dict, contract: dict) -> None:
    candidates = data.get("candidates")
    variants = [item.get("variant") for item in candidates or []]
    if variants not in (["a", "b"], ["a", "b", "c"]):
        raise ValidationError("D01 candidate contract mismatch")
    expected_candidates = [
        {
            "variant": variant,
            "title": f"independent-scene-{variant}",
            "target_path": d01_candidate_path(variant),
        }
        for variant in variants
    ]
    if candidates != expected_candidates:
        raise ValidationError("D01 candidate contract mismatch")
    if ordered_value(data.get("scene_contract")) != ordered_value(
        contract["scene_contract"]
    ):
        raise ValidationError("D01 scene contract mismatch")
    if data.get("production_requirements") != contract["production_requirements"]:
        raise ValidationError("D01 production contract mismatch")
    if data.get("candidate_policy") != contract["candidate_policy"]:
        raise ValidationError("D01 candidate policy mismatch")
    if data.get("comparison_anchors") != []:
        raise ValidationError("D01 comparison anchors mismatch")
    prompt = data.get("shared_prompt")
    if not isinstance(prompt, str) or hashlib.sha256(
        prompt.encode("utf-8")
    ).hexdigest() != contract["shared_prompt_sha256"]:
        raise ValidationError("D01 exact shared prompt contract mismatch")
    if data.get("acceptance_gates") != list(contract["acceptance_gates"]):
        raise ValidationError("D01 acceptance gates mismatch")
    if data.get("hard_rejects") != list(contract["hard_rejects"]):
        raise ValidationError("D01 exact hard rejects required")
```

Pin D01 static asset fields in `validate_assets` before generic validation,
using error `D01: static asset contract mismatch`.

- [ ] **Step 5: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
bash -lc 'npm run validate:v1-2'
git add \
  akari-v1.2/manifest/generation-requests/d01-r01.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: add Natural Form D01 generation contract"
```

Expected: focused tests pass; validator reports nine generation requests,
twenty-four candidate groups, and thirty-eight generated outputs.

---

### Task 2: Enforce exact D01 Core dependencies

**Files:**

- Modify: `scripts/validate_akari_v1_2_natural_form.py:859-996`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:1279-1540`

**Interfaces:**

- Consumes: `validate_generation_dependencies(assets: dict, requests: list[dict]) -> None`
  and the Task 1 D01 ordered references.
- Produces: strict D01 linkage to accepted C04 r01, C05 r01, C06 r01 with the
  C06-2 file, and C07 r01 with the seated file.

- [ ] **Step 1: Add dependency mutation tests**

Add one passing live-D01 test and parameterized failures that independently set
C04, C05, C06, or C07 to `candidate/r00`, change any one dependency revision,
replace any one accepted path, select C06-1 instead of C06-2, or select C07
standing instead of seated. Require:

```text
D01 requires strict accepted C04 r01, C05 r01, C06 r01 C06-2, and C07 r01 seated
```

Use this test for asset-state mutations; add the reference-path cases in the
same loop with the four exact Task 1 paths:

```python
def test_d01_requires_all_strict_accepted_core_dependencies(self):
    d01_requests = [
        copy.deepcopy(item)
        for item in self.requests
        if item["asset_id"] == "D01"
    ]
    validate_generation_dependencies(self.assets, d01_requests)
    for asset_id in ("C04", "C05", "C06", "C07"):
        with self.subTest(asset_id=asset_id):
            invalid = copy.deepcopy(self.assets)
            asset = next(
                item for item in invalid["assets"]
                if item["asset_id"] == asset_id
            )
            asset.update(status="candidate", revision="r00", accepted_paths=[])
            with self.assertRaisesRegex(
                ValidationError,
                "D01 requires strict accepted C04 r01, C05 r01, "
                "C06 r01 C06-2, and C07 r01 seated",
            ):
                validate_generation_dependencies(invalid, d01_requests)


def test_d01_requires_exact_c06_2_and_c07_seated_paths(self):
    replacements = {
        2: (
            "akari-v1.2/accepted/core/face-hair/"
            "akari-v1.2_c06-1_sleepy-neutral_r01.png"
        ),
        3: (
            "akari-v1.2/accepted/core/indoor-feet/"
            "akari-v1.2_c07_indoor-socks-standing_r01.png"
        ),
    }
    for index, path in replacements.items():
        with self.subTest(index=index):
            requests = [
                copy.deepcopy(item)
                for item in self.requests
                if item["asset_id"] == "D01"
            ]
            requests[0]["references"][index]["path"] = path
            with self.assertRaisesRegex(
                ValidationError,
                "D01 requires strict accepted C04 r01, C05 r01, "
                "C06 r01 C06-2, and C07 r01 seated",
            ):
                validate_generation_dependencies(self.assets, requests)
```

- [ ] **Step 2: Run the focused dependency class and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests -v
```

Expected: the new D01 mutation cases fail because D01 dependencies are not yet
checked.

- [ ] **Step 3: Implement strict dependency comparison**

In `validate_generation_dependencies`, derive the exact live accepted paths
from C04-C07 and compare both the four asset states and the four request paths:

```python
d01_requests = [item for item in requests if item["asset_id"] == "D01"]
expected_d01_paths = [
    "akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png",
    "akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png",
    "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png",
    "akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png",
]
for request in d01_requests:
    if (
        [(asset["status"], asset["revision"]) for asset in (c04, c05, c06, c07)]
        != [("accepted", "r01")] * 4
        or [item["path"] for item in request["references"]]
        != expected_d01_paths
    ):
        raise ValidationError(
            "D01 requires strict accepted C04 r01, C05 r01, C06 r01 "
            "C06-2, and C07 r01 seated"
        )
```

- [ ] **Step 4: Verify dependency green and all prior requests unchanged**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests -v
bash -lc 'npm run validate:v1-2'
git diff --check
git add scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: enforce Natural Form D01 dependencies"
```

Expected: dependency tests and validator pass without changing C01-C07 data.

---

### Task 3: Add the D01 comparison builder

**Files:**

- Create: `scripts/build_v1_2_d01_comparison.py`
- Create: `tests/test_build_v1_2_d01_comparison.py`
- Modify: `package.json:15-30`

**Interfaces:**

- Consumes: Task 1 `candidates` in manifest order and
  `scripts.build_v1_2_c03_comparisons.render_grid(rows, output_path) -> Path`.
- Produces:
  `build_d01_comparison(request_path: Path, package_root: Path, output_path: Path) -> Path`
  and npm command `build:v1-2:d01-comparison`.

- [ ] **Step 1: Write failing renderer and source-boundary tests**

Create `tests/test_build_v1_2_d01_comparison.py` with temporary 300 x 480 solid
PNG candidates. Assert A/B produces one row with two cards in manifest order;
A/B/C produces one row with three cards. Add failures for reordered variants,
ID-to-suffix mismatch, absolute paths, `..`, noncanonical directories, missing
files, a symlinked candidate directory outside the package root, and a
canonical candidate filename symlinked outside its directory.

Use these helpers so labels and paths are exact:

```python
def candidate_path(variant: str) -> Path:
    return Path("source/candidates/d01/r01") / (
        f"akari-v1.2_d01_morning-bedside_r01-{variant}.png"
    )


def make_request(root: Path, variants=("a", "b")) -> Path:
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump(
            {
                "asset_id": "D01",
                "revision": "r01",
                "candidates": [
                    {
                        "variant": variant,
                        "title": f"independent-scene-{variant}",
                        "target_path": candidate_path(variant).as_posix(),
                    }
                    for variant in variants
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return request
```

Use these complete core tests. Each success test creates its source PNGs
explicitly; the missing-source test intentionally creates none. Keep the
directory-symlink and file-symlink tests separate so either escape reports the
canonical-source error:

```python
def test_builds_ab_in_declared_order(self):
    with TemporaryDirectory() as directory:
        root = Path(directory)
        for variant, color in (("a", "red"), ("b", "blue")):
            path = root / candidate_path(variant)
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (300, 480), color).save(path)
        output = root / "comparison.webp"
        build_d01_comparison(make_request(root), root, output)
        with Image.open(output) as image:
            self.assertEqual(image.size, (660, 566))
            self.assertGreater(image.getpixel((170, 260))[0], 180)
            self.assertGreater(image.getpixel((490, 260))[2], 120)


def test_builds_abc_in_declared_order(self):
    with TemporaryDirectory() as directory:
        root = Path(directory)
        for variant, color in (("a", "red"), ("b", "blue"), ("c", "green")):
            path = root / candidate_path(variant)
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (300, 480), color).save(path)
        output = root / "comparison.webp"
        build_d01_comparison(
            make_request(root, ("a", "b", "c")), root, output
        )
        with Image.open(output) as image:
            self.assertEqual(image.size, (980, 566))


def test_rejects_variant_order_and_suffix_mismatch(self):
    for variants in (("b", "a"), ("a", "c")):
        with self.subTest(variants=variants), TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root, variants)
            with self.assertRaisesRegex(
                ValueError, "expected D01 A/B or A/B/C candidates"
            ):
                build_d01_comparison(request, root, root / "out.webp")


def test_rejects_absolute_parent_and_noncanonical_sources(self):
    replacements = (
        "/tmp/d01.png",
        "source/candidates/d01/r01/../d01.png",
        "source/candidates/d01/other/akari-v1.2_d01_morning-bedside_r01-a.png",
        "source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-b.png",
    )
    for replacement in replacements:
        with self.subTest(replacement=replacement), TemporaryDirectory() as directory:
            root = Path(directory)
            for variant in ("a", "b"):
                path = root / candidate_path(variant)
                path.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (300, 480), "gray").save(path)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["candidates"][0]["target_path"] = replacement
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "D01 candidate sources must remain canonical"
            ):
                build_d01_comparison(request, root, root / "out.webp")


def test_rejects_missing_source(self):
    with TemporaryDirectory() as directory:
        root = Path(directory)
        request = make_request(root)
        with self.assertRaisesRegex(ValueError, "missing .*r01-a.png"):
            build_d01_comparison(request, root, root / "out.webp")


def test_rejects_candidate_directory_symlink_escape(self):
    with TemporaryDirectory() as directory, TemporaryDirectory() as outside:
        root = Path(directory)
        candidate_dir = root / "source/candidates/d01/r01"
        candidate_dir.parent.mkdir(parents=True)
        candidate_dir.symlink_to(Path(outside), target_is_directory=True)
        request = make_request(root)
        with self.assertRaisesRegex(
            ValueError, "D01 candidate sources must remain canonical"
        ):
            build_d01_comparison(request, root, root / "out.webp")


def test_rejects_candidate_file_symlink_escape(self):
    with TemporaryDirectory() as directory, TemporaryDirectory() as outside:
        root = Path(directory)
        candidate_dir = root / "source/candidates/d01/r01"
        candidate_dir.mkdir(parents=True)
        escaped = Path(outside) / "escaped.png"
        Image.new("RGB", (300, 480), "red").save(escaped)
        (root / candidate_path("a")).symlink_to(escaped)
        Image.new("RGB", (300, 480), "blue").save(
            root / candidate_path("b")
        )
        request = make_request(root)
        with self.assertRaisesRegex(
            ValueError, "D01 candidate sources must remain canonical"
        ):
            build_d01_comparison(request, root, root / "out.webp")
```

- [ ] **Step 2: Run the new module and verify red**

```sh
uv run python -m unittest tests.test_build_v1_2_d01_comparison -v
```

Expected: import failure because `build_v1_2_d01_comparison.py` is absent.

- [ ] **Step 3: Implement the thin canonical builder**

Create `scripts/build_v1_2_d01_comparison.py` with `ROOT`, `PACKAGE_ROOT`, CLI
argument handling matching the C06 builder, and this core implementation:

```python
SOURCE_DIRECTORY = Path("source/candidates/d01/r01")


def expected_candidate_path(variant: str) -> Path:
    return SOURCE_DIRECTORY / (
        f"akari-v1.2_d01_morning-bedside_r01-{variant}.png"
    )


def build_d01_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    if (request.get("asset_id"), request.get("revision")) != ("D01", "r01"):
        raise ValueError("expected D01 r01 request")
    candidates = request.get("candidates")
    variants = [item.get("variant") for item in candidates or []]
    if variants not in (["a", "b"], ["a", "b", "c"]):
        raise ValueError("expected D01 A/B or A/B/C candidates")

    anchored = package_root.resolve(strict=False) / SOURCE_DIRECTORY
    actual_directory = (package_root / SOURCE_DIRECTORY).resolve(strict=False)
    if actual_directory != anchored:
        raise ValueError("D01 candidate sources must remain canonical")

    row = []
    for candidate, variant in zip(candidates, variants):
        source = Path(candidate.get("target_path", ""))
        expected = expected_candidate_path(variant)
        resolved = (package_root / source).resolve(strict=False)
        if (
            source.is_absolute()
            or source != expected
            or resolved.parent != anchored
        ):
            raise ValueError("D01 candidate sources must remain canonical")
        if not (package_root / source).is_file():
            raise ValueError(f"missing {source.name}")
        row.append((f"{variant.upper()}  D01 morning bedside", package_root / source))
    return render_grid([row], output_path)
```

- [ ] **Step 4: Add the package command**

Add exactly:

```json
"build:v1-2:d01-comparison": "uv run python scripts/build_v1_2_d01_comparison.py --request akari-v1.2/manifest/generation-requests/d01-r01.yaml --output akari-v1.2/comparisons/d01-r01/d01-r01-comparison.webp"
```

- [ ] **Step 5: Verify green, isolation, and commit**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_d01_comparison \
  tests.test_build_v1_2_c06_comparison -v
git diff --check
git add scripts/build_v1_2_d01_comparison.py \
  tests/test_build_v1_2_d01_comparison.py package.json
git commit -m "feat: add Natural Form D01 comparison"
```

Expected: D01 and C06 comparison suites pass; no existing comparison script is
modified.

---

### Task 4: Validate D01 dimensions, findings, lifecycle, and Gate 4

**Files:**

- Modify: `scripts/validate_akari_v1_2_natural_form.py:1084-1282,1345-1375`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:1542-2364`

**Interfaces:**

- Consumes: D01 candidates from Task 1, `validate_review_log`,
  `validate_lifecycle_linkage`, and optional local candidate files.
- Produces:
  `validate_d01_png_dimensions(source: Path) -> None`,
  `validate_d01_candidate_dimensions(request: dict, package_root: Path) -> None`
  and `validate_gate4(assets: dict, review_log: dict) -> None`.

- [ ] **Step 1: Add failing dimension-boundary tests**

Using temporary package roots and real Pillow PNGs, prove that 1024 x 1536,
1020 x 1532, and 1028 x 1540 pass. Prove 1019 x 1536, 1029 x 1536,
1024 x 1531, and 1024 x 1541 raise:

```text
D01 r01: candidate dimensions outside 1020-1028 x 1532-1540
```

Also prove missing candidate files do not fail generation-contract validation,
because A/B do not exist before image generation.

Add `from tempfile import TemporaryDirectory`,
`validate_d01_candidate_dimensions`, and `validate_d01_png_dimensions` to the
test imports and use this exact test class:

```python
class NaturalFormD01DimensionTests(unittest.TestCase):
    def setUp(self):
        self.request = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml"
        )

    def test_accepts_target_and_all_tolerance_corners(self):
        sizes = (
            (1024, 1536),
            (1020, 1532),
            (1020, 1540),
            (1028, 1532),
            (1028, 1540),
        )
        for size in sizes:
            with self.subTest(size=size), TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / self.request["candidates"][0]["target_path"]
                source.parent.mkdir(parents=True)
                Image.new("RGB", size, "white").save(source)
                validate_d01_candidate_dimensions(self.request, root)

    def test_rejects_each_just_outside_dimension(self):
        sizes = ((1019, 1536), (1029, 1536), (1024, 1531), (1024, 1541))
        for size in sizes:
            with self.subTest(size=size), TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / self.request["candidates"][0]["target_path"]
                source.parent.mkdir(parents=True)
                Image.new("RGB", size, "white").save(source)
                with self.assertRaisesRegex(
                    ValidationError,
                    "D01 r01: candidate dimensions outside "
                    "1020-1028 x 1532-1540",
                ):
                    validate_d01_candidate_dimensions(self.request, root)

    def test_allows_declared_candidates_to_be_absent_before_generation(self):
        with TemporaryDirectory() as directory:
            validate_d01_candidate_dimensions(self.request, Path(directory))

    def test_rejects_outside_tolerance_promoted_png(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "accepted.png"
            Image.new("RGB", (1019, 1536), "white").save(source)
            with self.assertRaisesRegex(
                ValidationError,
                "D01 r01: candidate dimensions outside "
                "1020-1028 x 1532-1540",
            ):
                validate_d01_png_dimensions(source)
```

- [ ] **Step 2: Add failing D01 review and Gate 4 tests**

Build synthetic A/B reviews and assert:

- D01 findings require exactly `severity`, `category`, `note`, `resolved`,
  `controlling_source_asset`, and `recommended_next_action`;
- controlling source is one of C04, C05, C06, C07, or `D01-scene`;
- accepted D01 has no unresolved finding;
- accepted-with-notes has at least one unresolved finding and every unresolved
  finding is a D01-scene Minor;
- all Core assets are strictly accepted for either accepted D01 status;
- D01 reviews match declared A/B or A/B/C candidates in order;
- before acceptance, D01 reviews may be only an ordered prefix while the next
  declared candidate is not generated; acceptance requires the full list;
- declaring C requires completed rejected A and B reviews whose unresolved
  findings are exclusively controlled by D01-scene;
- exactly one accepted or accepted-with-notes review matches accepted D01;
- `release` requires accepted D01, `conditional-release` requires
  accepted-with-notes D01, and `hold` requires no accepted D01 review;
- Gate 4 selected ID matches the accepted review, or is null on Hold.

Use this exact release-record shape:

```yaml
gate_4:
  asset_id: D01
  revision: r01
  outcome: release
  selected_candidate_id: d01-r01-a
  controlling_source_asset: D01-scene
  decision: D01 passed all five review gates with no unresolved finding.
```

Add `validate_gate4` to the test imports. Use this helper and focused tests;
the existing lifecycle tests continue to exercise candidate ordering and exact
one-review linkage:

```python
def d01_review(status="review", findings=None, candidate_id="d01-r01-a"):
    variant = candidate_id[-1]
    return {
        "asset_id": "D01",
        "revision": "r01",
        "candidate_id": candidate_id,
        "status": status,
        "source_paths": [
            "source/candidates/d01/r01/"
            f"akari-v1.2_d01_morning-bedside_r01-{variant}.png"
        ],
        "source_sha256s": [f"{1 if variant == 'a' else 2:064x}"],
        "findings": [] if findings is None else findings,
        "decision": f"Synthetic D01 {candidate_id} decision.",
    }


def d01_finding(
    severity="minor", controller="D01-scene", resolved=False
):
    return {
        "severity": severity,
        "category": "production",
        "note": "Synthetic original-resolution evidence.",
        "resolved": resolved,
        "controlling_source_asset": controller,
        "recommended_next_action": "Preserve or regenerate the scene.",
    }


def test_d01_findings_require_controller_and_next_action(self):
    for missing in ("controlling_source_asset", "recommended_next_action"):
        with self.subTest(missing=missing):
            log = copy.deepcopy(self.review_log)
            finding = d01_finding()
            finding.pop(missing)
            log["reviews"].append(d01_review(findings=[finding]))
            with self.assertRaisesRegex(
                ValidationError, "D01: exact finding provenance required"
            ):
                validate_review_log(log)


def test_d01_accepted_rejects_every_unresolved_finding(self):
    log = copy.deepcopy(self.review_log)
    log["reviews"].append(
        d01_review(status="accepted", findings=[d01_finding()])
    )
    with self.assertRaisesRegex(
        ValidationError, "D01: accepted requires no unresolved finding"
    ):
        validate_review_log(log)


def test_d01_accepted_with_notes_allows_only_scene_minor(self):
    allowed = copy.deepcopy(self.review_log)
    allowed["reviews"].append(
        d01_review(status="accepted-with-notes", findings=[d01_finding()])
    )
    validate_review_log(allowed)
    for severity, controller in (("major", "D01-scene"), ("minor", "C04")):
        with self.subTest(severity=severity, controller=controller):
            invalid = copy.deepcopy(self.review_log)
            invalid["reviews"].append(
                d01_review(
                    status="accepted-with-notes",
                    findings=[d01_finding(severity, controller)],
                )
            )
            with self.assertRaisesRegex(
                ValidationError,
                "D01: accepted-with-notes requires D01-scene Minor only",
            ):
                validate_review_log(invalid)


def test_gate4_outcome_matches_d01_status_and_selection(self):
    cases = (
        ("accepted", "release", "d01-r01-a"),
        ("accepted-with-notes", "conditional-release", "d01-r01-a"),
        ("candidate", "hold", None),
    )
    for status, outcome, selected in cases:
        with self.subTest(status=status):
            assets = copy.deepcopy(self.assets)
            d01 = next(
                item for item in assets["assets"] if item["asset_id"] == "D01"
            )
            d01.update(
                status=status,
                revision="r01" if status != "candidate" else "r00",
                accepted_paths=(
                    [
                        "accepted/daily-validation/"
                        "akari-v1.2_d01_morning-bedside_r01.png"
                    ]
                    if status != "candidate" else []
                ),
            )
            log = copy.deepcopy(self.review_log)
            if selected is not None:
                findings = (
                    [d01_finding()]
                    if status == "accepted-with-notes" else None
                )
                log["reviews"].append(
                    d01_review(status=status, findings=findings)
                )
            log["gate_4"] = {
                "asset_id": "D01",
                "revision": "r01",
                "outcome": outcome,
                "selected_candidate_id": selected,
                "controlling_source_asset": "D01-scene",
                "decision": "Synthetic Gate 4 decision.",
            }
            validate_gate4(assets, log)


def test_d01_optional_c_allows_only_rejected_scene_only_ab_prefix(self):
    request = next(
        copy.deepcopy(item)
        for item in self.generation_requests
        if (item["asset_id"], item["revision"]) == ("D01", "r01")
    )
    request["candidates"].append(
        {
            "variant": "c",
            "title": "independent-scene-c",
            "target_path": (
                "source/candidates/d01/r01/"
                "akari-v1.2_d01_morning-bedside_r01-c.png"
            ),
        }
    )
    requests = [
        request
        if (item["asset_id"], item["revision"]) == ("D01", "r01")
        else copy.deepcopy(item)
        for item in self.generation_requests
    ]
    reviews = copy.deepcopy(self.review_log)
    reviews["reviews"].extend(
        [
            d01_review(
                status="rejected",
                findings=[d01_finding()],
                candidate_id=f"d01-r01-{variant}",
            )
            for variant in ("a", "b")
        ]
    )
    validate_lifecycle_linkage(self.assets, requests, reviews)
    invalid = copy.deepcopy(reviews)
    invalid["reviews"][-1]["findings"][0][
        "controlling_source_asset"
    ] = "C04"
    with self.assertRaisesRegex(
        ValidationError,
        "D01 r01: optional C requires rejected scene-only A/B",
    ):
        validate_lifecycle_linkage(self.assets, requests, invalid)
```

- [ ] **Step 3: Run the focused tests and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormD01DimensionTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormReviewLogTests -v
```

Expected: new tolerance, finding-provenance, and Gate 4 cases fail before the
specialized validators exist.

- [ ] **Step 4: Implement conditional file-dimension inspection**

```python
def validate_d01_png_dimensions(source: Path) -> None:
    try:
        with Image.open(source) as image:
            width, height = image.size
            image.verify()
    except (OSError, SyntaxError) as error:
        raise ValidationError("D01 r01: unreadable candidate PNG") from error
    if not (1020 <= width <= 1028 and 1532 <= height <= 1540):
        raise ValidationError(
            "D01 r01: candidate dimensions outside "
            "1020-1028 x 1532-1540"
        )


def validate_d01_candidate_dimensions(request: dict, package_root: Path) -> None:
    for candidate in request["candidates"]:
        source = package_root / candidate["target_path"]
        if source.is_file():
            validate_d01_png_dimensions(source)
```

Import Pillow's `Image`, call this function from `main` only for D01 after
request validation, and call it directly in the boundary tests.

- [ ] **Step 5: Implement D01 review provenance and acceptance restrictions**

In `validate_review_log`, require the two additional finding fields only when
`asset_id == "D01"`. Reject accepted D01 if any finding is unresolved. Permit
accepted-with-notes only when at least one finding is unresolved and every
unresolved finding is Minor and controlled by `D01-scene`.

Extend `validate_assets` so D01 accepted or accepted-with-notes requires C04,
C05, C06, and C07 each at strict `accepted/r01`, not merely C06 accepted. When
`package_root` is provided and D01 is accepted, also call
`validate_d01_png_dimensions` on its one accepted path so a clean clone does
not depend on local candidate evidence for the dimension gate.

In `validate_lifecycle_linkage`, specialize only D01 r01 review matching. When
D01 is not accepted, allow `actual == declared[:len(actual)]`; when D01 is
accepted or accepted-with-notes, require `actual == declared`. If C is declared,
require the A and B prefix to exist, both statuses to be `rejected`, each to
have at least one unresolved finding, and every unresolved finding controller
to be `D01-scene`. Raise `D01 r01: optional C requires rejected scene-only A/B`
for any violation. All C01-C07 matching behavior remains exact and unchanged.

- [ ] **Step 6: Implement Gate 4 linkage**

Add `validate_gate4(assets, review_log)` with these exact transitions:

```python
def validate_gate4(assets: dict, review_log: dict) -> None:
    d01 = next(item for item in assets["assets"] if item["asset_id"] == "D01")
    record = review_log.get("gate_4")
    if record is None:
        if d01["status"] in {"accepted", "accepted-with-notes"}:
            raise ValidationError("Gate 4 record required for accepted D01")
        return
    if set(record) != {
        "asset_id", "revision", "outcome", "selected_candidate_id",
        "controlling_source_asset", "decision",
    } or (record["asset_id"], record["revision"]) != ("D01", "r01"):
        raise ValidationError("Gate 4 record contract mismatch")
    matching = [
        review for review in review_log["reviews"]
        if (review["asset_id"], review["revision"]) == ("D01", "r01")
        and review["status"] in {"accepted", "accepted-with-notes"}
    ]
    expected = {
        "accepted": "release",
        "accepted-with-notes": "conditional-release",
    }.get(d01["status"], "hold")
    if record["outcome"] != expected:
        raise ValidationError("Gate 4 outcome does not match D01 status")
    expected_id = matching[0]["candidate_id"] if len(matching) == 1 else None
    if record["selected_candidate_id"] != expected_id:
        raise ValidationError("Gate 4 selection does not match D01 review")
    if record["controlling_source_asset"] not in {
        "C04", "C05", "C06", "C07", "D01-scene"
    } or not isinstance(record["decision"], str) or not record["decision"].strip():
        raise ValidationError("Gate 4 decision contract mismatch")
```

Call it after `validate_lifecycle_linkage` in `main`.

- [ ] **Step 7: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormD01DimensionTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormReviewLogTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
git diff --check
git add scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: validate Natural Form D01 lifecycle"
```

Expected: focused tests pass and the current candidate/r00 D01 state remains
valid without a Gate 4 record.

---

### Task 5: Generate independent D01 A and B candidates

**Files:**

- Create locally: `akari-v1.2/source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-a.png`
- Create locally: `akari-v1.2/source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-b.png`

**Interfaces:**

- Consumes: Task 1 frozen prompt and the four accepted references.
- Produces: two standalone local PNGs with no cross-candidate reference use.

- [ ] **Step 1: Read required generation and review skills completely**

Read the current `imagegen` and `akari-v1-1-image-review` skill files before
opening references or invoking image generation. Follow any stricter current
instruction when it does not conflict with the approved D01 design.

- [ ] **Step 2: Open and assign the four references for candidate A**

Open at original detail, in order:

```text
akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png
akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png
```

State that Image 1 controls body mechanics, Image 2 controls identity/hair and
ornament, Image 3 controls sleepy-secure facial state, and Image 4 controls
socks/ankles/feet/contact. Use the literal shared prompt from the request.

- [ ] **Step 3: Generate and persist candidate A**

Invoke image generation once. Treat the returned image as the end of that
agent turn. On continuation, save it to the declared A path; if the image was
shown but no file exists, use the repository's rollout payload-recovery
procedure and verify the PNG signature before decoding.

- [ ] **Step 4: Verify candidate A before generating B**

```sh
file akari-v1.2/source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-a.png
identify -format '%m %w %h %[colorspace]\n' \
  akari-v1.2/source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-a.png
sha256sum \
  akari-v1.2/source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-a.png
bash -lc 'npm run validate:v1-2'
```

Expected: real readable PNG, sRGB-compatible color, dimensions inside the D01
tolerance, and validator pass. Preserve but do not promote a wrong-size result.

- [ ] **Step 5: Reopen accepted references and generate B independently**

Open the same four accepted references again in the same order. Do not open A
as a generation reference. Repeat the exact prompt and role statement, invoke
one new generation, and save to the declared B path on continuation.

- [ ] **Step 6: Verify both candidates and record hashes outside git**

```sh
identify -format '%f %m %w %h %[colorspace]\n' \
  akari-v1.2/source/candidates/d01/r01/*.png
sha256sum akari-v1.2/source/candidates/d01/r01/*.png
bash -lc 'npm run validate:v1-2'
git status --short
```

Expected: exactly A and B local PNGs, each inside tolerance; neither is staged
or committed.

---

### Task 6: Build the board and review A/B at original resolution

**Files:**

- Create locally: `akari-v1.2/comparisons/d01-r01/d01-r01-comparison.webp`
- Modify: `akari-v1.2/manifest/review-log.yaml`

**Interfaces:**

- Consumes: Task 5 PNGs and Task 3 builder.
- Produces: one local comparison board, full A/B review records, eligibility
  decision, and either a user-selection request, optional-C justification, or
  Core Hold.

- [ ] **Step 1: Build and inspect the comparison**

```sh
bash -lc 'npm run build:v1-2:d01-comparison'
identify akari-v1.2/comparisons/d01-r01/d01-r01-comparison.webp
```

Open the board and both source PNGs at original detail.

- [ ] **Step 2: Review in the mandatory order**

For each candidate, inspect Identity, then Body, State, Rendering, and
Production. Stop that candidate's review on a Blocker. For every finding,
record all six exact fields:

```yaml
- severity: minor
  category: production
  note: The observed evidence in the original-resolution source.
  resolved: false
  controlling_source_asset: D01-scene
  recommended_next_action: Keep the source unchanged or regenerate D01 staging.
```

Use an empty `findings: []` when no finding exists. Set a structurally invalid
candidate to `rejected`; set an eligible candidate to `review` until the user
selects it.

- [ ] **Step 3: Append A/B records in declared order**

Each record must use the real SHA-256 from Task 5 and this exact shape:

```yaml
- asset_id: D01
  revision: r01
  candidate_id: d01-r01-a
  status: review
  source_paths:
    - source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-a.png
  source_sha256s:
    - 64-character lowercase digest copied exactly from the Task 5 A sha256sum output
  findings: []
  decision: Eligible after original-resolution Identity, Body, State, Rendering, and Production review; awaiting explicit user selection.
```

Write B immediately after A using `d01-r01-b`, the B path, B digest, observed
findings, and evidence-specific decision.

- [ ] **Step 4: Validate the review branch and commit durable metadata**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_d01_comparison \
  tests.test_akari_v1_2_natural_form_package.NaturalFormReviewLogTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
git add akari-v1.2/manifest/review-log.yaml
git diff --cached --check
git commit -m "docs: record Natural Form D01 candidate review"
```

- [ ] **Step 5: Follow exactly one observed branch**

- If A or B is eligible, show the comparison, recommend the strongest eligible
  candidate, and require the user to return its literal ID. Do not promote yet.
- If neither is eligible and every failure is D01-scene-only, execute Task 7.
- If A and B share a C04, C05, C06, or C07 structural failure, add a Hold Gate
  4 record naming that asset and next action, validate it, commit it, and stop
  D01 without Task 7 or promotion.

---

### Task 7: Generate optional D01 C only when scene repair is justified

**Files:**

- Modify conditionally: `akari-v1.2/manifest/generation-requests/d01-r01.yaml`
- Create locally conditionally:
  `akari-v1.2/source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-c.png`
- Modify conditionally: `akari-v1.2/manifest/review-log.yaml`

**Interfaces:**

- Consumes: Task 6 evidence proving no A/B candidate is eligible and failures
  are exclusively controlled by `D01-scene`.
- Produces: validated A/B/C request, one independent C image, rebuilt board,
  and a third review record.

- [ ] **Step 1: Skip this task when A or B is eligible**

Record `Task 7 skipped: eligible A/B candidate exists` in the execution
progress log and proceed directly to Task 8 after explicit selection.

- [ ] **Step 2: Add C to the request and verify the contract before generation**

Append exactly:

```yaml
  - variant: c
    title: independent-scene-c
    target_path: source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-c.png
```

Then run:

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_build_v1_2_d01_comparison -v
bash -lc 'npm run validate:v1-2'
git add akari-v1.2/manifest/generation-requests/d01-r01.yaml
git commit -m "feat: activate Natural Form D01 scene repair"
```

- [ ] **Step 3: Generate C from the same four accepted references**

Read the generation skill again if a context reset occurred. Open only the four
accepted references at original detail, state the same roles, and use the same
frozen prompt. Do not use A or B as a reference. Generate once and persist C by
the same save-or-payload-recovery procedure.

- [ ] **Step 4: Verify, rebuild, review, and record C**

```sh
identify -format '%f %m %w %h %[colorspace]\n' \
  akari-v1.2/source/candidates/d01/r01/*.png
sha256sum akari-v1.2/source/candidates/d01/r01/*.png
bash -lc 'npm run validate:v1-2'
bash -lc 'npm run build:v1-2:d01-comparison'
```

Review C in the same five-gate order, append `d01-r01-c` after B with its real
hash and findings, validate, and commit only the review log. If C is eligible,
show the rebuilt board and require its exact candidate ID before promotion. If
C is ineligible, record Hold with `D01-scene` and stop.

---

### Task 8: Promote the explicit selection and record Gate 4

**Files:**

- Create: `akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Modify: `akari-v1.2/README.md`
- Modify: `akari-v1.2/docs/akari-v1.2-core-design.md`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: literal user-selected `d01-r01-a`, `d01-r01-b`, or `d01-r01-c`,
  its eligible review, local PNG, and SHA-256.
- Produces: one byte-identical accepted r01 PNG, one selected accepted review,
  rejected nonselected reviews, and a matching Gate 4 release classification.

- [ ] **Step 1: Write the final-state test before promotion**

Add a live test asserting D01 is r01, has exactly one accepted path, D01 reviews
remain in request order, exactly one accepted status matches the user's literal
ID, the selected source SHA equals the accepted file SHA, and Gate 4 matches
the selected review. The test must fail while D01 remains candidate/r00.

Use this exact test, replacing only the `expected_selected_id` literal with the
ID the user actually returned before running the RED step:

```python
def test_d01_acceptance_links_selected_source_and_gate4(self):
    expected_selected_id = "d01-r01-a"
    d01 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "D01"
    )
    self.assertIn(d01["status"], {"accepted", "accepted-with-notes"})
    self.assertEqual(d01["revision"], "r01")
    self.assertEqual(
        d01["accepted_paths"],
        [
            "accepted/daily-validation/"
            "akari-v1.2_d01_morning-bedside_r01.png"
        ],
    )
    request = next(
        item for item in self.generation_requests
        if (item["asset_id"], item["revision"]) == ("D01", "r01")
    )
    reviews = [
        item for item in self.review_log["reviews"]
        if (item["asset_id"], item["revision"]) == ("D01", "r01")
    ]
    self.assertEqual(
        [item["candidate_id"] for item in reviews],
        [f"d01-r01-{item['variant']}" for item in request["candidates"]],
    )
    selected = [
        item for item in reviews
        if item["status"] in {"accepted", "accepted-with-notes"}
    ]
    self.assertEqual(len(selected), 1)
    self.assertEqual(selected[0]["candidate_id"], expected_selected_id)
    self.assertEqual(selected[0]["status"], d01["status"])
    self.assertEqual(
        selected[0]["source_sha256s"],
        [sha256_file(PACKAGE_ROOT / d01["accepted_paths"][0])],
    )
    self.assertEqual(
        self.review_log["gate_4"]["selected_candidate_id"],
        expected_selected_id,
    )
    self.assertEqual(
        self.review_log["gate_4"]["outcome"],
        "release" if d01["status"] == "accepted" else "conditional-release",
    )
```

Add `sha256_file` to the validator imports in the test module.

- [ ] **Step 2: Run the focused test and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests.test_d01_acceptance_links_selected_source_and_gate4 -v
```

Expected: FAIL because D01 is not yet accepted.

- [ ] **Step 3: Copy only the literal selected PNG and prove equality**

Map the user-selected ID to its declared source path, then copy it without
transformation:

```sh
cp -- "$SELECTED_D01_SOURCE" \
  akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png
cmp --silent -- "$SELECTED_D01_SOURCE" \
  akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png
sha256sum "$SELECTED_D01_SOURCE" \
  akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png
```

Expected: `cmp` exits 0 and both printed digests equal the selected review's
recorded SHA-256.

- [ ] **Step 4: Update asset, reviews, Gate 4, and package status**

Set D01 in `assets.yaml` to:

```yaml
    status: accepted
    revision: r01
    accepted_paths:
      - accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png
```

Use `accepted-with-notes` instead only when every unresolved finding is a
D01-scene Minor. Set the selected review to the identical status and every
nonselected D01 review to `rejected`.

For clean acceptance, add:

```yaml
gate_4:
  asset_id: D01
  revision: r01
  outcome: release
  selected_candidate_id: d01-r01-a
  controlling_source_asset: D01-scene
  decision: D01 passed all five review gates with no unresolved finding; Natural Form Gate 4 is released.
```

The example uses A. If the user's literal response is `d01-r01-b` or
`d01-r01-c`, write that exact returned ID instead; do not infer it from the
assistant's recommendation.

For accepted-with-notes, use `outcome: conditional-release` and a decision that
names each observed D01-scene Minor. Update both package status lines to
`Natural Form Core Release` or `Natural Form Core Conditional Release`. Hold
leaves both documents at `Design Approved / Pre-production` and creates no
accepted PNG.

Replace the pre-production assertion in `test_core_design_is_the_approved_draft`
with the exact status reached by Gate 4. For clean acceptance the assertion is:

```python
self.assertIn("**Status:** Natural Form Core Release", text)
self.assertIn(
    "Status: Natural Form Core Release.",
    (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8"),
)
```

For conditional release, both literals include `Conditional Release`. Hold
retains the existing pre-production assertion.

- [ ] **Step 5: Verify final-state green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormReviewLogTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
cmp --silent -- "$SELECTED_D01_SOURCE" \
  akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png
git add \
  akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  akari-v1.2/README.md \
  akari-v1.2/docs/akari-v1.2-core-design.md \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: accept Natural Form D01 morning validation"
```

Expected: selected ID, status, source hash, accepted hash, Gate 4 outcome, and
package status all agree.

---

### Task 9: Run final review, verification, integration, and cleanup

**Files:**

- Verify: all durable Task 1-8 files.
- Preserve locally: D01 candidates and comparison plus existing C04-C07 local
  evidence.
- Integrate: feature branch into local `main` without push.

**Interfaces:**

- Consumes: completed D01 branch with explicit user selection and Gate 4.
- Produces: reviewed, verified local `main`, preserved local evidence, and no
  remaining feature worktree or branch.

- [ ] **Step 1: Run the complete focused and repository suites**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_d01_comparison \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormD01DimensionTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormReviewLogTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run test:node'
bash -lc 'npm run test:python'
bash -lc 'npm run validate:v1-2'
bash -lc 'npm run audit'
bash -lc 'npm run lint:md'
```

Expected: every command exits 0. If repo-wide Markdown lint sees ignored
working material, also run tracked Markdown explicitly and require zero errors:

```sh
git ls-files -z -- '*.md' | xargs -0 ./node_modules/.bin/markdownlint-cli2
```

- [ ] **Step 2: Verify selected bytes, dimensions, and evidence manifests**

Re-run `cmp`, SHA-256, and dimension inspection for selected source and accepted
PNG. Record path and SHA-256 manifests for all D01 local candidate/comparison
files and all existing C04-C07 local evidence before cleanup.

- [ ] **Step 3: Request independent branch review**

Use `superpowers:requesting-code-review` against base `5b1975e`. Review exact
request pinning, tolerance boundaries, dependency states, path/symlink
protection, accepted-with-notes restrictions, Gate 4 transitions, selected
hash linkage, and C01-C07 regressions. Reproduce every finding before changing
code; use `superpowers:receiving-code-review` and TDD for valid fixes.

- [ ] **Step 4: Re-run the entire verification set on the final feature HEAD**

After any review fix, repeat Step 1 and Step 2 from the final commit. Do not use
earlier passing output as completion evidence.

- [ ] **Step 5: Preserve local evidence and fast-forward local main**

Copy D01 candidate PNGs and comparison WebP to the same untracked paths in the
main workspace, then prove their hashes match the worktree copies. Prove the
pre-existing C04-C07 evidence hashes are unchanged. Fast-forward local `main`
only; do not push.

- [ ] **Step 6: Verify merged main before cleanup**

On merged `main`, repeat Node, Python plus legacy, Natural Form validator,
audit, tracked Markdown lint, selected-source-to-accepted equality, accepted
SHA-256, D01 evidence hashes, and C04-C07 evidence hashes.

- [ ] **Step 7: Remove the feature worktree and branch**

Use `superpowers:finishing-a-development-branch` with the already selected
local-main integration outcome. Remove the clean D01 worktree and feature
branch only after merged-main verification and evidence preservation pass.

Expected final state: D01 and Gate 4 are durably recorded on local `main`, the
accepted PNG is byte-identical to the explicit selection, candidate/comparison
evidence remains untracked locally, C04-C07 evidence is unchanged, and no push
has occurred.

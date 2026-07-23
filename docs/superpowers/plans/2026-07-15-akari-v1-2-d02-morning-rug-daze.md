# Akari v1.2 Daily.1 D02 Morning Rug Daze Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the reusable Daily scene workflow, generate and review D02, and
accept one morning rug scene without changing D01 or the v1.2.0 Core release.

**Architecture:** Extract the Daily request, image, review, and lifecycle rules
from current D01 special cases into a small data-driven module. Keep the
Natural Form validator as package orchestrator, register D02 as a candidate,
and use one generic Daily comparison builder with a D01 compatibility wrapper.
Generated candidates and comparisons stay local; only the selected PNG and
durable contracts are tracked.

**Tech Stack:** Python 3.12, `unittest`, PyYAML, Pillow, Node/npm scripts,
Markdown, image generation with visible local references

## Global Constraints

- D02 is asset `D02`, revision `r01`, descriptor `morning-rug-daze`, and the
  first new `v1.2-Daily.1` morning scene.
- The target canvas is 1024 by 1536 pixels; accepted width is 1020 through
  1028 and accepted height is 1532 through 1540.
- Promote the selected PNG byte-for-byte. Do not resize, stretch, crop, pad,
  or warp it to force exact dimensions.
- Initial candidates are independent A and B. Candidate C is allowed only
  when both fail for scene-only staging, background, lighting, or presentation.
- D01 controls continuity, C04 body mechanics, C05 identity and morning hair,
  C06-1 sleepy-neutral state, and C07 seated socks and feet.
- No local candidate, comparison image, or legacy working path may be used as
  a generation reference.
- Candidate and comparison outputs remain local and untracked. Existing local
  review artifacts must remain untouched.
- The accepted path is
  `akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png`.
- D01 Gate 4 and v1.2.0 release metadata remain unchanged.
- The Core PDF SHA-256 remains
  `a3904369ed20875e4d18e7a28eb2cce81e7f2da4e8cfb846cae7395bbab0e673`.
- The release checksum file SHA-256 remains
  `e8ead253ec1dbdf19e7c179c4f848f4c2839038a7704a373c6754ba38a28dd17`.

---

## File Structure

- Create `scripts/akari_v1_2_daily.py`: reusable Daily request, dimension,
  finding, and lifecycle primitives.
- Modify `scripts/validate_akari_v1_2_natural_form.py`: register D02 and call
  the Daily primitives while retaining D01 Gate 4 behavior.
- Create `scripts/build_v1_2_daily_comparison.py`: render a declared Daily A/B
  or A/B/C request after canonical-path checks.
- Modify `scripts/build_v1_2_d01_comparison.py`: compatibility wrapper over the
  generic Daily builder.
- Create `tests/test_akari_v1_2_daily.py`: focused D01 compatibility and D02
  contract tests.
- Create `tests/test_build_v1_2_daily_comparison.py`: generic comparison and
  path-containment tests.
- Modify `tests/test_build_v1_2_d01_comparison.py`: retain frozen D01 behavior.
- Modify `akari-v1.2/manifest/assets.yaml`: append D02 as candidate, then
  promote it only after selection.
- Create `akari-v1.2/manifest/generation-requests/d02-r01.yaml`: frozen request.
- Modify `akari-v1.2/manifest/review-log.yaml`: append final ordered D02 review
  records after user selection.
- Create `akari-v1.2/accepted/daily/morning/.gitkeep`: reserve the destination.
- Modify `package.json`: add the D02 comparison command.
- Local only: `akari-v1.2/source/candidates/d02/r01/*.png` and
  `akari-v1.2/comparisons/d02-r01/d02-r01-comparison.webp`.

### Task 1: Extract Reusable Daily Validation Primitives

**Files:**

- Create: `scripts/akari_v1_2_daily.py`
- Create: `tests/test_akari_v1_2_daily.py`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`

**Interfaces:**

- Consumes: generation-request mappings and package-root `Path` values.
- Produces: `ValidationError`, `daily_candidate_path()`,
  `validate_daily_generation_request()`, `validate_daily_png_dimensions()`,
  and `validate_daily_candidate_dimensions()`.

- [ ] **Step 1: Write failing helper and D01 compatibility tests**

Create `tests/test_akari_v1_2_daily.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image
import yaml

from scripts.akari_v1_2_daily import (
    ValidationError,
    daily_candidate_path,
    validate_daily_candidate_dimensions,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"


class DailyPrimitiveTests(unittest.TestCase):
    def test_candidate_path_is_derived_from_declared_scene(self):
        self.assertEqual(
            daily_candidate_path("D02", "r01", "morning-rug-daze", "a"),
            "source/candidates/d02/r01/"
            "akari-v1.2_d02_morning-rug-daze_r01-a.png",
        )

    def test_d01_live_request_keeps_dimension_tolerance(self):
        request = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml")
            .read_text(encoding="utf-8")
        )
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / request["candidates"][0]["target_path"]
            source.parent.mkdir(parents=True)
            Image.new("RGB", (1028, 1540), "white").save(source)
            validate_daily_candidate_dimensions(request, root)
            Image.new("RGB", (1029, 1540), "white").save(source)
            with self.assertRaisesRegex(
                ValidationError, "D01 r01: candidate dimensions outside"
            ):
                validate_daily_candidate_dimensions(request, root)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify the import fails**

Run:

```bash
uv run python -m unittest tests.test_akari_v1_2_daily -v
```

Expected: `ERROR` with `No module named 'scripts.akari_v1_2_daily'`.

- [ ] **Step 3: Add the minimal reusable module**

Create `scripts/akari_v1_2_daily.py` with the following behavior:

```python
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image


class ValidationError(ValueError):
    pass


DAILY_TOP_LEVEL_KEYS = {
    "schema_version", "request_id", "asset_id", "revision",
    "variation_axis", "references", "shared_prompt", "scene_contract",
    "production_requirements", "candidate_policy", "candidates",
    "comparison_anchors", "acceptance_gates", "hard_rejects",
}


def daily_candidate_path(
    asset_id: str, revision: str, descriptor: str, variant: str
) -> str:
    lower_id = asset_id.lower()
    return (
        f"source/candidates/{lower_id}/{revision}/"
        f"akari-v1.2_{lower_id}_{descriptor}_{revision}-{variant}.png"
    )


def validate_daily_generation_request(data: dict, contract: dict) -> None:
    asset_id = data["asset_id"]
    if set(data) != DAILY_TOP_LEVEL_KEYS:
        raise ValidationError(f"{asset_id} exact top-level contract required")
    if any(set(item) != {"role", "path"} for item in data["references"]):
        raise ValidationError(f"{asset_id} exact reference contract required")
    candidates = data.get("candidates")
    variants = [item.get("variant") for item in candidates or []]
    if variants not in (["a", "b"], ["a", "b", "c"]):
        raise ValidationError(f"{asset_id} candidate contract mismatch")
    expected = [
        {
            "variant": variant,
            "title": f"independent-scene-{variant}",
            "target_path": daily_candidate_path(
                asset_id, data["revision"], contract["descriptor"], variant
            ),
        }
        for variant in variants
    ]
    if candidates != expected:
        raise ValidationError(f"{asset_id} candidate contract mismatch")
    for key in ("scene_contract", "production_requirements", "candidate_policy"):
        if data.get(key) != contract[key]:
            raise ValidationError(f"{asset_id} {key} mismatch")
    if data.get("comparison_anchors") != []:
        raise ValidationError(f"{asset_id} comparison anchors mismatch")
    prompt = data.get("shared_prompt")
    if not isinstance(prompt, str):
        raise ValidationError(f"{asset_id} shared prompt required")
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if digest != contract["shared_prompt_sha256"]:
        raise ValidationError(f"{asset_id} exact shared prompt contract mismatch")
    if data.get("acceptance_gates") != list(contract["acceptance_gates"]):
        raise ValidationError(f"{asset_id} acceptance gates mismatch")
    if data.get("hard_rejects") != list(contract["hard_rejects"]):
        raise ValidationError(f"{asset_id} exact hard rejects required")


def validate_daily_png_dimensions(
    source: Path, asset_id: str, revision: str, requirements: dict
) -> None:
    try:
        with Image.open(source) as image:
            image_format = image.format
            width, height = image.size
            image.verify()
    except (OSError, SyntaxError) as error:
        raise ValidationError(
            f"{asset_id} {revision}: unreadable candidate PNG"
        ) from error
    if image_format != "PNG":
        raise ValidationError(f"{asset_id} {revision}: candidate must be PNG")
    width_gate = requirements["accepted_width"]
    height_gate = requirements["accepted_height"]
    if not (
        width_gate["minimum"] <= width <= width_gate["maximum"]
        and height_gate["minimum"] <= height <= height_gate["maximum"]
    ):
        raise ValidationError(
            f"{asset_id} {revision}: candidate dimensions outside "
            f"{width_gate['minimum']}-{width_gate['maximum']} x "
            f"{height_gate['minimum']}-{height_gate['maximum']}"
        )


def validate_daily_candidate_dimensions(request: dict, package_root: Path) -> None:
    for candidate in request["candidates"]:
        source = package_root / candidate["target_path"]
        if source.is_file():
            validate_daily_png_dimensions(
                source,
                request["asset_id"],
                request["revision"],
                request["production_requirements"],
            )
```

- [ ] **Step 4: Replace D01 helper duplication without behavior changes**

Import the five public names into the Natural Form validator. Remove its local
`ValidationError`, D01 top-level key set, D01 candidate-path helper, D01
request validator, and D01 dimension functions. Add
`"descriptor": "morning-bedside"` to the D01 contract and dispatch D01
through the new request and dimension functions. Keep the imported
`ValidationError` name exported so existing imports remain valid.

- [ ] **Step 5: Run compatibility tests**

```bash
uv run python -m unittest tests.test_akari_v1_2_daily \
  tests.test_akari_v1_2_natural_form_package -v
```

Expected: all existing Natural Form tests and both new primitive tests pass.

- [ ] **Step 6: Commit the reusable primitives**

```bash
git add scripts/akari_v1_2_daily.py \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_daily.py
git commit -m "refactor: add reusable Daily validation helpers"
```

### Task 2: Register the Frozen D02 Asset and Generation Request

**Files:**

- Modify: `akari-v1.2/manifest/assets.yaml`
- Create: `akari-v1.2/manifest/generation-requests/d02-r01.yaml`
- Create: `akari-v1.2/accepted/daily/morning/.gitkeep`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_daily.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: Task 1 Daily validators.
- Produces: exact D02 asset and request contracts in candidate state.

- [ ] **Step 1: Add failing live D02 tests**

Add `D02ContractTests` that load the live D02 request and assert
`validate_assets()`, `validate_generation_request()`, and
`validate_generation_dependencies()` pass. Assert the ordered reference roles
are `accepted_d01_morning_continuity`, `accepted_c04_floor_sitting_body`,
`accepted_c05_morning_hair`, `accepted_c06_sleepy_neutral_expression`, and
`accepted_c07_seated_sock_feet`.

- [ ] **Step 2: Verify the missing request failure**

```bash
uv run python -m unittest tests.test_akari_v1_2_daily.D02ContractTests -v
```

Expected: `ERROR` because `d02-r01.yaml` does not exist.

- [ ] **Step 3: Add the candidate asset and destination**

Append this exact asset after D01 and add the `.gitkeep`:

```yaml
  - asset_id: D02
    descriptor: morning-rug-daze
    phase: 5
    variants: [default]
    expected_paths:
      - accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_rNN.png
    depends_on: [D01, C04, C05, C06, C07]
    gate: daily
    status: candidate
    revision: r00
    accepted_paths: []
```

- [ ] **Step 4: Create the exact D02 request**

Use schema version 1, request ID `akari-v1.2-d02-r01`, revision `r01`, and
variation axis `independent_scene_attempt`. Declare these references in order:

```yaml
references:
  - role: accepted_d01_morning_continuity
    path: akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png
  - role: accepted_c04_floor_sitting_body
    path: akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
  - role: accepted_c05_morning_hair
    path: akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
  - role: accepted_c06_sleepy_neutral_expression
    path: akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-1_sleepy-neutral_r01.png
  - role: accepted_c07_seated_sock_feet
    path: akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png
```

After the references, add this exact request body:

```yaml
shared_prompt: >-
  Use the five visible accepted images only in their declared roles to create
  one standalone morning continuation of the same naturally cute 25-year-old
  Akari. Image 1 controls only D01 bedroom, soft morning light, loose opaque
  white short-sleeve T-shirt, simple opaque gray shorts-style roomwear, and
  just-awake continuity; do not copy its viewer gaze, side-folded legs, crop,
  or exact background arrangement. Image 2 controls C04 seated weight, visible
  pelvis support, slight posterior tilt, coordinated back rounding, dropped
  shoulders, one believable supporting hand, healthy leg volume, and traceable
  joints; do not copy its hoodie, skirt, side-folded legs, smile, or blank
  background. Image 3 controls adult identity, reversible C05 morning hair,
  complete character-left pale-blue crossed pins and ribbon-like ornament,
  cheek shape, short-bob length, palette, and rendering; do not copy its
  chest-up crop, hoodie, or exact expression. Image 4 controls only the C06-1
  sleepy-neutral state: heavy but open eyelids, relaxed brows and cheeks,
  incomplete frame-left focus, and a quiet closed almost-neutral mouth; do not
  copy its crop or hoodie. Image 5 controls C07 warm-white mid-calf socks with
  exactly two thin pale-blue stripes, ankle and foot volume, relaxed toes, heel
  placement, and rug contact; do not copy its hoodie, skirt, or crop. Seat
  Akari on the frame-left window-side area of a low-contrast bedroom rug, with
  the restrained bed edge at frame-right. Extend both legs loosely forward,
  keep one knee slightly bent, place one hand behind or beside the pelvis as
  support, and rest the other hand loosely on a thigh. Turn her head only
  lightly and direct an unfocused gaze toward the frame-left window. Use soft
  curtain-filtered morning light and a front-biased three-quarter camera at
  natural seated viewing height, slightly wider than D01. Keep the complete
  head, ornament, both hands, pelvis, both thigh roots, both knees, shins,
  ankles, heels, and socked toes visible. Add exactly two Humanization
  elements: one light natural sock slouch on the straighter extended leg and a
  slightly uneven T-shirt hem with believable seated wrinkles. Add no phone,
  mug, clock, readable book, food, or explanatory prop. The moment must read as
  still not ready to move, never sadness, illness, intoxication, sensuality,
  dissociation, or a posed portrait. When references conflict, D01 controls
  continuity, C04 body mechanics, C05 identity and hair, C06-1 facial state,
  and C07 socks and feet. Do not create closed eyes, viewer-directed focus, a
  broad smile, an open mouth, thin legs, broken joints, twisted ankles, pointed
  toes, contradictory support or contact, wrong ornament, wrong hair length,
  wrong outfit, incorrect sock stripes, crop loss, text, logo, watermark,
  border, collage, grid, multiple characters, or any severe identity,
  adult-age, anatomy, or rendering drift.
scene_contract:
  camera: front-biased-three-quarter-natural-seated-height-wider-than-d01
  surface: frame-left-window-side-low-contrast-bedroom-rug
  continuity: d01-same-morning-bedroom-outfit-and-hair
  lighting: soft-frame-left-curtain-filtered-morning-light
  gaze: frame-left-window-directed-with-incomplete-focus
  pose: both-legs-forward-one-knee-slightly-bent-one-supporting-hand
  humanization:
    - straighter-leg-sock-light-natural-slouch
    - slightly-uneven-t-shirt-hem-with-seated-wrinkles
  outfit:
    top: loose-opaque-white-short-sleeve-t-shirt
    bottom: simple-opaque-gray-shorts-style-roomwear
    socks: warm-white-mid-calf-exactly-two-thin-pale-blue-stripes
  required_visible_features:
    - complete-head-and-ornament
    - both-hands-including-one-believable-supporting-hand
    - pelvis-support-and-both-thigh-roots
    - both-knees-shins-ankles-heels-and-socked-toes
  forbidden_props: [phone, mug, clock, readable-book, food, explanatory-prop]
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
  optional_c_only_for: d02-scene-staging-background-lighting-or-presentation
  stop_for_shared_failure: [D01, C04, C05, C06, C07]
  cross_candidate_references: forbidden
candidates:
  - variant: a
    title: independent-scene-a
    target_path: source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-a.png
  - variant: b
    title: independent-scene-b
    target_path: source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-b.png
comparison_anchors: []
acceptance_gates: [identity, body, state, continuity, rendering, production]
hard_rejects:
  - severe identity adult-age face body-volume or rendering drift
  - fused missing duplicated disconnected or untraceable limbs or joints
  - floating pelvis contradictory hand support or implausible whole-body weight
  - thin legs broken knees twisted ankles pointed toes or contradictory foot contact
  - missing mirrored relocated duplicated or materially redesigned ornament
  - non-reversible hair wrong hair length extreme bed head wet hair or wind
  - closed eyes distress intoxication sensual posing viewer-directed focus broad smile or open mouth
  - repeated d01 side-folded leg pose instead of approved d02 forward-leg pose
  - wrong outfit exposed underwear shoes slippers bare feet or incorrect sock height or stripes
  - crop or scale preventing complete support hand leg or foot review
  - readable text logo watermark border collage grid or multiple character
```

Freeze the prompt digest with the following command and require the output to
equal `fe97dbb86b527379a60c5ff4732781adbda0b2501cf3bcedde94ad9ba40e1f38`:

```bash
uv run python -c 'import hashlib,yaml,pathlib; p=pathlib.Path("akari-v1.2/manifest/generation-requests/d02-r01.yaml"); d=yaml.safe_load(p.read_text()); print(hashlib.sha256(d["shared_prompt"].encode()).hexdigest())'
```

- [ ] **Step 5: Register exact D02 constants and dependencies**

Append `D02` to `ASSET_IDS` and `continuity` to `REVIEW_CATEGORIES`. Add the
exact static asset, references, scene, production, candidate, gate, reject, and
prompt-digest constants. Register `("D02", "r01")` with descriptor
`morning-rug-daze`. Dispatch D01 and D02 through the Daily helpers. Require
accepted D01 r01, C04 r01, C05 r01, C06 r01, and C07 r01 at the five exact
reference paths.

- [ ] **Step 6: Run focused validation**

```bash
uv run python -m unittest tests.test_akari_v1_2_daily -v
npm run validate:v1-2
```

Expected: D02 is a valid ungenerated candidate; the validator reports 9 assets
and 10 generation requests.

- [ ] **Step 7: Commit the request contract**

```bash
git add akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/generation-requests/d02-r01.yaml \
  akari-v1.2/accepted/daily/morning/.gitkeep \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_daily.py \
  tests/test_akari_v1_2_natural_form_package.py \
  docs/superpowers/plans/2026-07-15-akari-v1-2-d02-morning-rug-daze.md
git commit -m "feat: register D02 morning rug request"
```

### Task 3: Generalize Daily Review and Lifecycle Validation

**Files:**

- Modify: `scripts/akari_v1_2_daily.py`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_daily.py`

**Interfaces:**

- Consumes: Daily candidates, reviews, asset state, and local file existence.
- Produces: controller-aware findings, ordered prefixes, optional-C gating,
  explicit selection enforcement, and source/accepted hash linkage.

- [ ] **Step 1: Add failing lifecycle tests**

Use these exact fixture shapes:

```python
def d02_review(variant: str, status: str = "review", findings=None) -> dict:
    source = (
        "source/candidates/d02/r01/"
        f"akari-v1.2_d02_morning-rug-daze_r01-{variant}.png"
    )
    return {
        "asset_id": "D02",
        "revision": "r01",
        "candidate_id": f"d02-r01-{variant}",
        "status": status,
        "source_paths": [source],
        "source_sha256s": ["0" * 64],
        "findings": [] if findings is None else findings,
        "decision": "Original-resolution ordered review recorded.",
    }


def d02_finding(controller: str = "D02-scene") -> dict:
    return {
        "severity": "major",
        "category": "continuity",
        "note": "The room no longer reads as the D01 morning bedroom.",
        "resolved": False,
        "controlling_source_asset": controller,
        "recommended_next_action": "Reject this scene attempt.",
    }
```

Test all allowed D02 controllers, rejection of unknown controllers, ordered
review prefixes while candidate, optional C only after scene-only rejected A/B,
exactly one accepted selection after promotion, selected-source and accepted
hash equality, and unchanged D01 Gate 4.

- [ ] **Step 2: Run tests and verify D02 lifecycle failures**

```bash
uv run python -m unittest tests.test_akari_v1_2_daily -v
```

Expected: failures show missing D02 finding provenance and pending handling.

- [ ] **Step 3: Add data-driven controller maps**

```python
DAILY_CONTROLLERS = {
    "D01": {"C04", "C05", "C06", "C07", "D01-scene"},
    "D02": {"D01", "C04", "C05", "C06", "C07", "D02-scene"},
}
DAILY_SCENE_CONTROLLER = {"D01": "D01-scene", "D02": "D02-scene"}
DAILY_FINDING_FIELDS = {
    "severity",
    "category",
    "note",
    "resolved",
    "controlling_source_asset",
    "recommended_next_action",
}


def validate_daily_finding(asset_id: str, finding: dict) -> None:
    if (
        set(finding) != DAILY_FINDING_FIELDS
        or finding.get("controlling_source_asset")
        not in DAILY_CONTROLLERS[asset_id]
        or not isinstance(finding.get("recommended_next_action"), str)
        or not finding["recommended_next_action"].strip()
    ):
        raise ValidationError(
            f"{asset_id}: exact finding provenance required"
        )


def validate_daily_review_status(
    asset_id: str,
    status: str,
    findings: list[dict],
) -> None:
    unresolved = [item for item in findings if not item["resolved"]]
    if status == "accepted" and unresolved:
        raise ValidationError(
            f"{asset_id}: accepted requires no unresolved finding"
        )
    if status == "accepted-with-notes" and (
        not unresolved
        or any(
            item["severity"] != "minor"
            or item["controlling_source_asset"]
            != DAILY_SCENE_CONTROLLER[asset_id]
            for item in unresolved
        )
    ):
        raise ValidationError(
            f"{asset_id}: accepted-with-notes requires "
            f"{DAILY_SCENE_CONTROLLER[asset_id]} Minor only"
        )
```

Call `validate_daily_finding()` after the validator has checked the shared
severity, category, note, and boolean-resolution types. Call
`validate_daily_review_status()` after all findings in one review are valid.

- [ ] **Step 4: Replace D01-only lifecycle branches with Daily-key logic**

Use the helpers for D01 and D02 in `validate_review_log()`. In lifecycle
linkage, derive Daily keys from `DAILY_CONTROLLERS` and treat generated files
and reviews as independent ordered prefixes while pending. Reviews may lag the
locally generated prefix, including zero reviews before explicit selection,
but must not outpace the local generated prefix when the package root is
available. Enforce the A/B rule before C and verify source and accepted hashes
after promotion. Keep
`validate_gate4()` D01-only.

- [ ] **Step 5: Run regression tests**

```bash
uv run python -m unittest tests.test_akari_v1_2_daily \
  tests.test_akari_v1_2_natural_form_package -v
npm run validate:v1-2
```

Expected: all tests pass with no D01 lifecycle or Gate 4 change.

- [ ] **Step 6: Commit lifecycle reuse**

```bash
git add scripts/akari_v1_2_daily.py \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_daily.py
git commit -m "feat: validate Daily scene lifecycle"
```

### Task 4: Add the Generic Daily Comparison Builder

**Files:**

- Create: `scripts/build_v1_2_daily_comparison.py`
- Modify: `scripts/build_v1_2_d01_comparison.py`
- Create: `tests/test_build_v1_2_daily_comparison.py`
- Modify: `tests/test_build_v1_2_d01_comparison.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`
- Modify: `package.json`
- Modify: `docs/superpowers/plans/2026-07-15-akari-v1-2-d02-morning-rug-daze.md`

**Interfaces:**

- Consumes: a Daily request, package root, output path, and optional expected
  asset ID.
- Produces: `build_daily_comparison(request_path: Path, package_root: Path,
  output_path: Path, expected_asset_id: str | None = None) -> Path` and
  `build_d01_comparison(request_path: Path, package_root: Path,
  output_path: Path) -> Path`.

- [ ] **Step 1: Write failing generic builder tests**

Create D02 red/blue/green fixtures in
`tests/test_build_v1_2_daily_comparison.py` and call:

```python
build_daily_comparison(request, root, output, expected_asset_id="D02")
```

Assert A/B and A/B/C manifest order. Add explicit rejection tests for reversed
or skipped variants, absolute paths, parent traversal, wrong descriptor or
suffix, directory symlink escape, file symlink escape, and missing sources.

- [ ] **Step 2: Run the test and verify the missing import**

```bash
uv run python -m unittest tests.test_build_v1_2_daily_comparison -v
```

Expected: `ERROR` because `scripts.build_v1_2_daily_comparison` is absent.

- [ ] **Step 3: Implement the generic builder**

Expose this exact interface:

```python
import re

import yaml

if __package__:
    from scripts.build_v1_2_c03_comparisons import render_grid
else:
    from build_v1_2_c03_comparisons import render_grid


def build_daily_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
    expected_asset_id: str | None = None,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    asset_id = request.get("asset_id")
    revision = request.get("revision")
    if (
        not isinstance(asset_id, str)
        or re.fullmatch(r"D\d{2}", asset_id) is None
        or revision != "r01"
        or (
            expected_asset_id is not None
            and asset_id != expected_asset_id
        )
    ):
        raise ValueError("expected declared Daily r01 request")
    candidates = request.get("candidates")
    variants = [item.get("variant") for item in candidates or []]
    if variants not in (["a", "b"], ["a", "b", "c"]):
        raise ValueError("expected Daily A/B or A/B/C candidates")

    lower_id = asset_id.lower()
    source_directory = Path(f"source/candidates/{lower_id}/r01")
    canonical_directory = package_root.resolve(strict=False) / source_directory
    actual_directory = (package_root / source_directory).resolve(strict=False)
    if actual_directory != canonical_directory:
        raise ValueError("Daily candidate sources must remain canonical")

    pattern = re.compile(
        rf"^source/candidates/{lower_id}/r01/"
        rf"akari-v1\.2_{lower_id}_([a-z0-9-]+)_r01-([abc])\.png$"
    )
    descriptor = None
    row = []
    for candidate, variant in zip(candidates, variants):
        source = Path(candidate.get("target_path", ""))
        match = pattern.fullmatch(source.as_posix())
        resolved = (package_root / source).resolve(strict=False)
        if (
            source.is_absolute()
            or match is None
            or match.group(2) != variant
            or resolved.parent != canonical_directory
        ):
            raise ValueError("Daily candidate sources must remain canonical")
        current_descriptor = match.group(1)
        if descriptor is None:
            descriptor = current_descriptor
        elif current_descriptor != descriptor:
            raise ValueError("Daily candidate descriptor mismatch")
        if not (package_root / source).is_file():
            raise ValueError(f"missing {source.name}")
        row.append(
            (
                f"{variant.upper()}  {asset_id} "
                f"{current_descriptor.replace('-', ' ')}",
                package_root / source,
            )
        )
    return render_grid([row], output_path)
```

Add the existing `resolve_from()` and CLI pattern with required `--request`,
`--output`, and `--asset-id` arguments. The CLI passes `--asset-id` to
`expected_asset_id` and prints the output path relative to the repository root.

Keep the D01 builder as a thin compatibility wrapper:

```python
if __package__:
    from scripts.build_v1_2_daily_comparison import build_daily_comparison
else:
    from build_v1_2_daily_comparison import build_daily_comparison


def build_d01_comparison(request_path, package_root, output_path):
    return build_daily_comparison(
        request_path,
        package_root,
        output_path,
        expected_asset_id="D01",
    )
```

Retain its existing CLI arguments and printed relative path.

- [ ] **Step 4: Add the D02 npm command and expand the Daily test gate**

Add exactly:

```json
"build:v1-2:d02-comparison": "uv run python scripts/build_v1_2_daily_comparison.py --request akari-v1.2/manifest/generation-requests/d02-r01.yaml --output akari-v1.2/comparisons/d02-r01/d02-r01-comparison.webp --asset-id D02",
"test:python:daily": "uv run python -m unittest tests.test_akari_v1_2_daily tests.test_build_v1_2_daily_comparison tests.test_build_v1_2_d01_comparison -v"
```

- [ ] **Step 5: Run builder and script-contract tests**

```bash
uv run python -m unittest tests.test_build_v1_2_daily_comparison \
  tests.test_build_v1_2_d01_comparison \
  tests.test_akari_v1_2_natural_form_package -v
```

Expected: generic D02 tests and all frozen D01 wrapper tests pass.

- [ ] **Step 6: Commit comparison reuse**

```bash
git add scripts/build_v1_2_daily_comparison.py \
  scripts/build_v1_2_d01_comparison.py \
  tests/test_build_v1_2_daily_comparison.py \
  tests/test_build_v1_2_d01_comparison.py \
  tests/test_akari_v1_2_natural_form_package.py package.json \
  docs/superpowers/plans/2026-07-15-akari-v1-2-d02-morning-rug-daze.md
git commit -m "feat: add Daily scene comparison builder"
```

### Task 5: Generate and Review Independent D02 Candidates

**Files:**

- Local create: `akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-a.png`
- Local create: `akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-b.png`
- Local create: `akari-v1.2/comparisons/d02-r01/d02-r01-comparison.webp`

**Interfaces:**

- Consumes: frozen D02 request and five accepted references.
- Produces: two independent candidates, a comparison, and evidence-backed
  findings for explicit user selection.

- [ ] **Step 1: Invoke image generation and inspect all references**

Read `imagegen/SKILL.md`. Open these files with `view_image` and keep them
visible:

```text
akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png
akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-1_sleepy-neutral_r01.png
akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png
```

State every declared role in the prompt. Do not substitute a candidate,
comparison, or legacy path.

- [ ] **Step 2: Generate candidate A**

Call image generation once with all five references and the frozen
`shared_prompt`. Save the standalone PNG at the declared A path. If the image
appears in the UI without a local file, structurally extract the current-day
`image_generation_call` whose result starts with `iVBOR`, verify signature
`89504e470d0a1a0a`, and decode it to that path.

- [ ] **Step 3: Generate candidate B independently**

Call image generation again with the same prompt and five accepted references.
Do not include A in the call or prompt. Save B at its declared path, using the
same payload recovery only if necessary.

- [ ] **Step 4: Validate files and build the board**

```bash
file akari-v1.2/source/candidates/d02/r01/*.png
sha256sum akari-v1.2/source/candidates/d02/r01/*.png
npm run validate:v1-2
npm run build:v1-2:d02-comparison
```

Expected: both are readable PNGs inside the declared dimension gate, hashes
differ, package validation passes with zero D02 review records before explicit
selection, and the comparison WebP exists.

- [ ] **Step 5: Review originals before the comparison**

Open A and B individually at original detail. Review Identity, Body, State,
Continuity, Rendering, and Production in order. Inspect pelvis and support
hand, thigh roots, knees, shins, ankles, heels, toes, sock stripes and slouch,
ornament, C06-1 expression, frame-left gaze, D01 outfit and room continuity,
full-body crop, and artifacts. Then open the comparison board for overall read.

- [ ] **Step 6: Stop for explicit user selection**

Report eligibility and every finding with severity, controller, evidence, and
next action. Recommend the strongest eligible candidate but do not promote it.
Ask for literal A or B selection.

If neither is eligible, generate C only when both failures are scene-only and
controlled by `D02-scene`. Otherwise stop and trace the shared structural issue
to D01, C04, C05, C06, or C07.

### Task 6: Record Selection, Promote D02, and Verify Final State

**Files:**

- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Create: `akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png`
- Modify: `tests/test_akari_v1_2_daily.py`

**Interfaces:**

- Consumes: explicit user selection, completed reviews, and source hashes.
- Produces: accepted D02 r01 with one matching accepted review and unchanged
  Core release evidence.

- [ ] **Step 1: Write the failing live accepted-linkage test**

Load the live manifests and call:

```python
validate_assets(assets, PACKAGE_ROOT)
validate_review_log(review_log)
validate_lifecycle_linkage(
    assets, generation_requests, review_log, PACKAGE_ROOT
)
validate_gate4(assets, review_log)
```

Assert D02 is accepted at r01, has the one declared accepted path, and has one
accepted review whose candidate ID matches the explicit selection and whose
hash equals the local source and promoted PNG.

- [ ] **Step 2: Verify the candidate-state failure**

```bash
uv run python -m unittest tests.test_akari_v1_2_daily -v
```

Expected: FAIL because D02 is candidate r00 with no accepted review.

- [ ] **Step 3: Promote exactly the selected source**

If the user selects A, run exactly:

```bash
cp akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-a.png \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png
cmp --silent \
  akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-a.png \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png
sha256sum \
  akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-a.png \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png
```

If the user selects B, run exactly:

```bash
cp akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-b.png \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png
cmp --silent \
  akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-b.png \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png
sha256sum \
  akari-v1.2/source/candidates/d02/r01/akari-v1.2_d02_morning-rug-daze_r01-b.png \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d02_morning-rug-daze_r01.png
```

Do not choose a branch until the explicit Task 5 response is received.

- [ ] **Step 4: Finalize asset and ordered reviews**

Change D02 to `status: accepted`, `revision: r01`, and its declared accepted
path. Append D02 reviews in declared candidate order. The selected entry is
accepted with its observed hash and no unresolved finding; non-selected entries
are rejected with observed findings and controller provenance. Do not modify
`gate_4`.

- [ ] **Step 5: Run focused tests until green**

```bash
npm run gate:edit:d02
```

Expected: all Daily and Natural Form tests pass, the package validates with D02
r01 accepted, and the closed v1.2.0 release pins remain unchanged.

- [ ] **Step 6: Run full final-state verification**

```bash
npm run gate:integration:v1-2
git diff --check
```

Expected: all v1.2 integration checks pass; Markdown reports zero errors; the
structure audit passes; and the PDF and checksum file match the fixed release
pins. D02 does not run v1.1, legacy, or full raster/OCR release checks.

- [ ] **Step 7: Commit only durable D02 outputs**

```bash
git add akari-v1.2/accepted/daily/morning/ \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  tests/test_akari_v1_2_daily.py
git commit -m "feat: accept D02 morning rug scene"
```

Confirm `git status --short` shows only intentionally preserved untracked
candidate and comparison directories, including D02 local review artifacts.

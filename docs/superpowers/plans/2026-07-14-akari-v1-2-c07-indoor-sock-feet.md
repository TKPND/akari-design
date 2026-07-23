# Akari v1.2 C07 Indoor Sock Feet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, review, and accept one matched C07 r01 pair that defines Akari's standing and floor-seated indoor sock-foot construction.

**Architecture:** Add one exact paired-generation request with standing-first sequencing and a same-candidate standing consistency anchor for the seated member. Reuse the existing paired comparison grid, generate three indivisible A/B/C pairs, stop for literal user selection, and promote only the selected two PNGs byte-for-byte.

**Tech Stack:** Python 3.12+, PyYAML, Pillow, `unittest`, Node/npm scripts, built-in `image_gen`, PNG and WebP assets, Git

## Global Constraints

- Use a 1024 x 1536 portrait canvas for every C07 output.
- Generate exactly three ordered candidate pairs: A, B, and C.
- Every candidate is an indivisible `standing` plus `seated` pair.
- Generate each standing member before its seated member.
- Add only the same candidate's standing member as the seated member's supporting consistency reference.
- Never mix outputs from different candidate pairs.
- Use foot-focused crops: standing from at least mid-thigh through complete toes; seated from pelvis and both thigh roots through complete toes.
- Use accepted C01 r01 for standing leg volume, knee state, loading, palette, outfit edge, and rendering.
- Use accepted C04 r01 for seated pelvis mechanics, leg trace, relaxed ankles, contact, outfit compression, and rendering.
- Use the v1.1 standard-foot set only for white sock material, two pale-blue stripes, sock height, ankle volume, and readable foot construction.
- Do not copy sneakers, reference labels, borders, panels, grids, or layouts.
- Keep socks fully opaque, equal in initial height, and free of large slouching or heavy folds.
- Keep knees unlocked, ankles connected, toes relaxed, and standing/seated contact mechanically believable.
- Treat bottom and lateral framing guidance as advisory; a numeric miss alone cannot reject a candidate.
- Reject framing only when crop or scale prevents joint-chain, sock, loading, contact, lift, or compression review.
- Do not patch, mask, warp, blend, mirror, or mechanically composite candidates.
- Stop after three pairs. If all three retain a Blocker or Major, close r01 and design r02 separately.
- Keep `akari-v1.2/source/candidates/c07/r01/`, `akari-v1.2/comparisons/c07-r01/`, and review crops local-only.
- Stop for explicit user selection before changing accepted C07 state.
- Preserve the existing local-only C04 candidates and comparison sheet.
- Run Node/npm commands through `bash -lc`.

---

## File Map

### Durable files created

- `akari-v1.2/manifest/generation-requests/c07-r01.yaml` — exact references, prompts, pair policy, advisory framing, outputs, and review gates.
- `scripts/build_v1_2_paired_candidate_comparison.py` — thin generic two-view wrapper around the existing paired grid renderer.
- `tests/test_build_v1_2_paired_candidate_comparison.py` — candidate ordering, view ordering, dimensions, and missing-file coverage.
- `akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-standing_r01.png` — selected standing source copied byte-for-byte.
- `akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png` — selected seated source copied byte-for-byte.

### Durable files modified

- `scripts/validate_akari_v1_2_natural_form.py` — C07 contract, per-request acceptance gates, and dependency validation.
- `tests/test_akari_v1_2_natural_form_package.py` — request, dependency, command, lifecycle, and accepted-state tests.
- `package.json` — `build:v1-2:c07-comparison`.
- `akari-v1.2/manifest/assets.yaml` — C07 changes from candidate r00 to accepted r01 only after selection.
- `akari-v1.2/manifest/review-log.yaml` — complete A/B/C pair decisions after selection.

### Existing code reused

- `scripts/build_v1_2_c03_comparisons.py::render_grid` — existing pair-grid renderer.
- `scripts/validate_akari_v1_2_natural_form.py::validate_lifecycle_linkage` — exact accepted-file SHA-256 linkage.

### Local-only files

- `akari-v1.2/source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-standing_r01-{a,b,c}.png`
- `akari-v1.2/source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-seated_r01-{a,b,c}.png`
- `akari-v1.2/comparisons/c07-r01/c07-r01-pair-comparison.webp`

---

### Task 1: Add the exact C07 paired-generation contract

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/c07-r01.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: `GENERATION_REQUEST_CONTRACTS`, `validate_generation_request(data: dict) -> None`, and `load_yaml(path: Path) -> dict`.
- Produces: exact key `("C07", "r01")`, ordered views `("standing", "seated")`, request-specific acceptance gates, and advisory two-view framing guidance.

- [ ] **Step 1: Load C07 in the generation-request fixture and write failing tests**

Add to `NaturalFormGenerationRequestTests.setUp`:

```python
self.c07 = load_yaml(
    PACKAGE_ROOT / "manifest/generation-requests/c07-r01.yaml"
)
```

Add:

```python
def test_c07_request_has_exact_ordered_pair_contract(self):
    validate_generation_request(self.c07)
    self.assertEqual(self.c07["asset_id"], "C07")
    self.assertEqual(self.c07["revision"], "r01")
    self.assertEqual(
        self.c07["variation_axis"], "paired_generation_attempt"
    )
    self.assertEqual(
        [candidate["variant"] for candidate in self.c07["candidates"]],
        ["a", "b", "c"],
    )
    for candidate in self.c07["candidates"]:
        self.assertEqual(
            [output["view"] for output in candidate["outputs"]],
            ["standing", "seated"],
        )
    self.assertEqual(self.c07["acceptance_gates"], ["body", "rendering"])

def test_c07_framing_guidance_is_advisory(self):
    framing = self.c07["framing_guidance"]
    self.assertEqual(framing["canvas"], {"width": 1024, "height": 1536})
    self.assertEqual(framing["enforcement"], "advisory")
    self.assertEqual(
        framing["views"],
        {
            "standing": {
                "upper_crop": "both-legs-visible-from-at-least-mid-thigh",
                "intended_bottom_margin_pixels": [46, 150],
                "intended_lateral_margin_pixels": 48,
            },
            "seated": {
                "upper_crop": "pelvis-skirt-hem-and-both-thigh-roots-visible",
                "intended_bottom_margin_pixels": [46, 150],
                "intended_lateral_margin_pixels": 48,
            },
        },
    )
    self.assertFalse(framing["reject_on_numeric_miss_alone"])

def test_c07_rejects_strict_pixel_enforcement(self):
    invalid = copy.deepcopy(self.c07)
    invalid["framing_guidance"]["enforcement"] = "hard"
    with self.assertRaisesRegex(
        ValidationError, "exact framing guidance required"
    ):
        validate_generation_request(invalid)

def test_c07_rejects_reordered_references(self):
    invalid = copy.deepcopy(self.c07)
    invalid["references"].reverse()
    with self.assertRaisesRegex(
        ValidationError, "exact reference contract required"
    ):
        validate_generation_request(invalid)

def test_c07_rejects_reordered_pair_outputs(self):
    invalid = copy.deepcopy(self.c07)
    invalid["candidates"][0]["outputs"].reverse()
    with self.assertRaisesRegex(
        ValidationError, "ordered paired outputs required"
    ):
        validate_generation_request(invalid)

def test_c07_requires_same_candidate_standing_anchor_policy(self):
    invalid = copy.deepcopy(self.c07)
    invalid["pair_generation_policy"][
        "second_view_additional_reference"
    ]["source_view"] = "seated"
    with self.assertRaisesRegex(
        ValidationError, "pair generation policy mismatch"
    ):
        validate_generation_request(invalid)
```

Update the collection expectations:

```python
def test_requests_load_in_asset_revision_order(self):
    self.assertEqual(
        [(item["asset_id"], item["revision"]) for item in self.requests],
        [
            ("C01", "r01"),
            ("C02", "r01"),
            ("C03", "r01"),
            ("C03", "r02"),
            ("C04", "r01"),
            ("C07", "r01"),
        ],
    )

def test_generation_counts_distinguish_groups_from_outputs(self):
    self.assertEqual(count_generation_work(self.requests), (18, 27))
```

- [ ] **Step 2: Run the focused tests and verify red**

Run:

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
```

Expected: ERROR because `c07-r01.yaml` does not exist.

- [ ] **Step 3: Create the exact request manifest**

Create `akari-v1.2/manifest/generation-requests/c07-r01.yaml`:

```yaml
schema_version: 1
request_id: akari-v1.2-c07-r01
asset_id: C07
revision: r01
variation_axis: paired_generation_attempt
references:
  - role: accepted_c01_standing_body
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
  - role: accepted_c04_seated_body
    path: akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
  - role: v1_1_indoor_sock_construction
    path: akari-v1.2/references/v1.1/standard-foot-set.webp
shared_prompt: >-
  Use the visible images only in their declared roles. Create one standalone
  technical lower-body footwear reference of the same healthy 25-year-old
  Akari on a 1024 x 1536 nearly plain warm-white or low-contrast rug canvas.
  Keep the fixed white oversized hoodie edge and gray pleated skirt, with no
  footwear. Keep all clothing fully opaque and securely arranged. Show warm
  white mid-calf socks with exactly two thin pale-blue stripes at equal
  initial height, consistent ribbing, sturdy natural ankles, rounded relaxed
  toes, and believable pose-specific contact. C01 controls standing upper-leg
  and lower-leg volume, unlocked knees, natural loading, palette, outfit edge,
  and rendering; do not copy its sneakers. Accepted C04 controls seated pelvis
  mechanics, front/rear leg trace, relaxed ankles, rug contact, garment
  compression, and rendering. The v1.1 foot board controls sock material,
  stripe count and placement, sock height, ankle volume, and readable foot
  construction only; do not reproduce its shoes, labels, panels, borders, or
  layout. Use a front-biased light three-quarter view. Preserve structural
  anatomy and pose readability over exact pixel placement. No bare feet,
  shoes, slippers, pointed ballet toes, locked knees, thin legs, twisted or
  fused ankles, mismatched sock height, extra stripes, heavy sock slouching,
  dramatic lighting, photorealistic skin, readable text, logo, watermark,
  border, collage, grid, or multiple composition.
view_prompts:
  standing: >-
    Show both legs from at least mid-thigh through the complete socked toes.
    Use a natural hip-width stance with both knees unlocked. Keep the primary
    load foot grounded through heel, outer edge, forefoot, and toes, while the
    secondary foot reads only slightly lighter through pressure or angle.
    Keep both complete feet visible with broadly 46 to 150 px bottom breathing
    room and at least 48 px lateral breathing room.
  seated: >-
    Show the pelvis, skirt hem, both upper-leg roots, knees, shins, ankles,
    heels, and complete socked toes in the accepted C04 floor-sitting
    mechanical family. Keep a traceable front leg and rear leg. Coordinate
    pelvis contact, knee direction, ankle angle, rug compression, and relaxed
    lift. Match the same candidate's standing member for sock height, stripe
    design, ankle volume, foot proportions, palette, and rendering without
    copying its standing pose. Keep broadly 46 to 150 px bottom breathing room
    and at least 48 px lateral breathing room.
pair_generation_policy:
  first_view: standing
  second_view: seated
  second_view_additional_reference:
    role: paired_standing_sock_anchor
    source_view: standing
    priority: supporting
framing_guidance:
  canvas: {width: 1024, height: 1536}
  enforcement: advisory
  views:
    standing:
      upper_crop: both-legs-visible-from-at-least-mid-thigh
      intended_bottom_margin_pixels: [46, 150]
      intended_lateral_margin_pixels: 48
    seated:
      upper_crop: pelvis-skirt-hem-and-both-thigh-roots-visible
      intended_bottom_margin_pixels: [46, 150]
      intended_lateral_margin_pixels: 48
  reject_on_numeric_miss_alone: false
  major_only_when: crop-or-scale-prevents-structural-foot-review
candidates:
  - variant: a
    title: paired-attempt-a
    outputs:
      - view: standing
        target_path: source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-standing_r01-a.png
      - view: seated
        target_path: source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-seated_r01-a.png
  - variant: b
    title: paired-attempt-b
    outputs:
      - view: standing
        target_path: source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-standing_r01-b.png
      - view: seated
        target_path: source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-seated_r01-b.png
  - variant: c
    title: paired-attempt-c
    outputs:
      - view: standing
        target_path: source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-standing_r01-c.png
      - view: seated
        target_path: source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-seated_r01-c.png
comparison_anchors: []
acceptance_gates: [body, rendering]
hard_rejects:
  - bare feet shoes slippers or any footwear
  - wrong stripe count color order spacing or materially inconsistent placement
  - mismatched sock height or severe pair construction drift
  - fused missing duplicated disconnected or untraceable legs ankles or feet
  - twisted ankles ballet-like pointed toes or contradictory loading
  - seated contact that contradicts pelvis knee or ankle mechanics
  - unreadable foot construction caused by crop or extreme scale
  - readable text logo watermark border collage grid or multiple composition
```

- [ ] **Step 4: Add the validator constants and exact contract**

Add beside `C04_R01_FRAMING_GUIDANCE`:

```python
C07_R01_FRAMING_GUIDANCE = {
    "canvas": {"width": 1024, "height": 1536},
    "enforcement": "advisory",
    "views": {
        "standing": {
            "upper_crop": "both-legs-visible-from-at-least-mid-thigh",
            "intended_bottom_margin_pixels": [46, 150],
            "intended_lateral_margin_pixels": 48,
        },
        "seated": {
            "upper_crop": "pelvis-skirt-hem-and-both-thigh-roots-visible",
            "intended_bottom_margin_pixels": [46, 150],
            "intended_lateral_margin_pixels": 48,
        },
    },
    "reject_on_numeric_miss_alone": False,
    "major_only_when": "crop-or-scale-prevents-structural-foot-review",
}
```

Add `"acceptance_gates": ("identity", "body", "rendering")` to each existing
request contract. Add:

```python
("C07", "r01"): {
    "variation_axis": "paired_generation_attempt",
    "references": (
        (
            "accepted_c01_standing_body",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
        ),
        (
            "accepted_c04_seated_body",
            "akari-v1.2/accepted/core/sitting/"
            "akari-v1.2_c04_floor-sitting_r01.png",
        ),
        (
            "v1_1_indoor_sock_construction",
            "akari-v1.2/references/v1.1/standard-foot-set.webp",
        ),
    ),
    "candidate_prefix": "source/candidates/c07/r01/",
    "candidate_detail": None,
    "output_specs": (
        ("standing", "akari-v1.2_c07_indoor-socks-standing_r01"),
        ("seated", "akari-v1.2_c07_indoor-socks-seated_r01"),
    ),
    "comparison_anchors": (),
    "pair_generation_policy": {
        "first_view": "standing",
        "second_view": "seated",
        "second_view_additional_reference": {
            "role": "paired_standing_sock_anchor",
            "source_view": "standing",
            "priority": "supporting",
        },
    },
    "view_names": ("standing", "seated"),
    "framing_contract": None,
    "framing_guidance": C07_R01_FRAMING_GUIDANCE,
    "acceptance_gates": ("body", "rendering"),
},
```

Replace the hard-coded gate check with:

```python
if data.get("acceptance_gates") != list(contract["acceptance_gates"]):
    raise ValidationError("generation request: acceptance gates mismatch")
```

- [ ] **Step 5: Run focused request tests and package validation**

Run:

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
bash -lc 'npm run validate:v1-2'
```

Expected: PASS and validation reports six generation requests, eighteen
candidate groups, and twenty-seven declared outputs.

- [ ] **Step 6: Commit the request contract**

```sh
git add akari-v1.2/manifest/generation-requests/c07-r01.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: define Natural Form C07 generation contract"
```

---

### Task 2: Enforce accepted C07 dependencies

**Files:**

- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: accepted C01 r01 and accepted C04 r01 asset records plus the first two C07 references.
- Produces: `validate_generation_dependencies(assets: dict, requests: list[dict]) -> None` enforcement for every C07 request.

- [ ] **Step 1: Write failing dependency tests**

Add to `NaturalFormGenerationDependencyTests`:

```python
def test_c07_declares_c01_and_c04_dependencies(self):
    c07 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C07"
    )
    self.assertEqual(c07["depends_on"], ["C01", "C04"])

def test_c07_requires_accepted_c01_and_c04(self):
    c07_requests = [
        item for item in self.requests if item["asset_id"] == "C07"
    ]
    for asset_id in ("C01", "C04"):
        with self.subTest(asset_id=asset_id):
            invalid = copy.deepcopy(self.assets)
            asset = next(
                item for item in invalid["assets"]
                if item["asset_id"] == asset_id
            )
            asset.update(status="candidate", revision="r00", accepted_paths=[])
            with self.assertRaisesRegex(
                ValidationError,
                "C07 requires accepted C01 r01 and C04 r01",
            ):
                validate_generation_dependencies(invalid, c07_requests)

def test_c07_requires_exact_accepted_reference_paths(self):
    c07_requests = [
        copy.deepcopy(item)
        for item in self.requests
        if item["asset_id"] == "C07"
    ]
    c07_requests[0]["references"][1]["path"] = (
        "akari-v1.2/accepted/core/sitting/substituted-c04.png"
    )
    with self.assertRaisesRegex(
        ValidationError,
        "C07 requires accepted C01 r01 and C04 r01",
    ):
        validate_generation_dependencies(self.assets, c07_requests)
```

- [ ] **Step 2: Run the dependency tests and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests -v
```

Expected: FAIL because dependency validation has no C07 branch.

- [ ] **Step 3: Add minimal C07 dependency validation**

Add `c04 = assets_by_id["C04"]` near the existing asset bindings, then append:

```python
c07_requests = [item for item in requests if item["asset_id"] == "C07"]
expected_c07_anchors = [
    "akari-v1.2/accepted/core/standing/"
    "akari-v1.2_c01_front-natural-stance_r01.png",
    "akari-v1.2/accepted/core/sitting/"
    "akari-v1.2_c04_floor-sitting_r01.png",
]
for request in c07_requests:
    if (
        (c01["status"], c01["revision"]) != ("accepted", "r01")
        or (c04["status"], c04["revision"]) != ("accepted", "r01")
        or [reference["path"] for reference in request["references"][:2]]
        != expected_c07_anchors
    ):
        raise ValidationError(
            "C07 requires accepted C01 r01 and C04 r01 "
            "at its declared anchors"
        )
```

- [ ] **Step 4: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests -v
bash -lc 'npm run validate:v1-2'
git add scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "test: enforce Natural Form C07 dependencies"
```

Expected: PASS.

---

### Task 3: Add the C07 paired comparison command

**Files:**

- Create: `scripts/build_v1_2_paired_candidate_comparison.py`
- Create: `tests/test_build_v1_2_paired_candidate_comparison.py`
- Modify: `package.json`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: an exact two-view paired request and `render_grid(rows, output_path) -> Path`.
- Produces: `build_paired_comparison(request_path: Path, package_root: Path, output_path: Path) -> Path` and `build:v1-2:c07-comparison`.

- [ ] **Step 1: Write failing builder tests**

Create `tests/test_build_v1_2_paired_candidate_comparison.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageColor
import yaml

from scripts.build_v1_2_paired_candidate_comparison import (
    build_paired_comparison,
)


PAIR_COLORS = (
    ("red", "green"),
    ("blue", "yellow"),
    ("magenta", "cyan"),
)


def make_request(root: Path) -> Path:
    candidates = []
    for variant, colors in zip(("a", "b", "c"), PAIR_COLORS):
        outputs = []
        for view, color in zip(("standing", "seated"), colors):
            target = Path("candidates") / f"{variant}-{view}.png"
            path = root / target
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (300, 480), color).save(path)
            outputs.append({"view": view, "target_path": target.as_posix()})
        candidates.append(
            {
                "variant": variant,
                "title": f"paired-attempt-{variant}",
                "outputs": outputs,
            }
        )
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump(
            {
                "view_prompts": {
                    "standing": "Standing view.",
                    "seated": "Seated view.",
                },
                "candidates": candidates,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return request


def assert_color_close(testcase, actual, expected_name):
    expected = ImageColor.getrgb(expected_name)
    testcase.assertTrue(
        all(abs(left - right) <= 20 for left, right in zip(actual, expected)),
        (actual, expected),
    )


class PairedCandidateComparisonTests(unittest.TestCase):
    def test_builds_three_pair_rows_in_request_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            output = root / "pair.webp"
            build_paired_comparison(request, root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (660, 1658))
                expected = (
                    ((170, 260), "red"),
                    ((490, 260), "green"),
                    ((170, 806), "blue"),
                    ((490, 806), "yellow"),
                    ((170, 1352), "magenta"),
                    ((490, 1352), "cyan"),
                )
                for point, color in expected:
                    assert_color_close(self, image.getpixel(point), color)

    def test_rejects_reordered_pair_views(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["candidates"][0]["outputs"].reverse()
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "expected paired view order"):
                build_paired_comparison(request, root, root / "pair.webp")

    def test_rejects_missing_pair_member(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            (root / "candidates/b-seated.png").unlink()
            with self.assertRaisesRegex(ValueError, "missing b-seated.png"):
                build_paired_comparison(request, root, root / "pair.webp")


if __name__ == "__main__":
    unittest.main()
```

Also extend `NaturalFormIsolationTests` so `natural_form_commands` includes:

```python
"build:v1-2:c07-comparison": (
    "uv run python scripts/build_v1_2_paired_candidate_comparison.py "
    "--request akari-v1.2/manifest/generation-requests/c07-r01.yaml "
    "--output akari-v1.2/comparisons/c07-r01/"
    "c07-r01-pair-comparison.webp"
),
```

- [ ] **Step 2: Run focused tests and verify red**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_paired_candidate_comparison \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests -v
```

Expected: ERROR because the builder module and package command do not exist.

- [ ] **Step 3: Implement the thin paired builder**

Create `scripts/build_v1_2_paired_candidate_comparison.py`:

```python
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

if __package__:
    from scripts.build_v1_2_c03_comparisons import render_grid
else:
    from build_v1_2_c03_comparisons import render_grid


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"


def build_paired_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    candidates = request["candidates"]
    if [candidate.get("variant") for candidate in candidates] != ["a", "b", "c"]:
        raise ValueError("expected candidates a, b, c")
    view_order = list(request.get("view_prompts", {}))
    if len(view_order) != 2:
        raise ValueError("expected exactly two paired views")
    rows = []
    for candidate in candidates:
        outputs = candidate.get("outputs")
        if not isinstance(outputs, list) or [
            output.get("view") for output in outputs
        ] != view_order:
            raise ValueError("expected paired view order")
        rows.append(
            [
                (
                    f"{candidate['variant'].upper()}  {output['view']}",
                    package_root / output["target_path"],
                )
                for output in outputs
            ]
        )
    return render_grid(rows, output_path)


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_paired_comparison(
        resolve_from(ROOT, args.request),
        PACKAGE_ROOT,
        resolve_from(ROOT, args.output),
    )
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
```

Add to `package.json` scripts:

```json
"build:v1-2:c07-comparison": "uv run python scripts/build_v1_2_paired_candidate_comparison.py --request akari-v1.2/manifest/generation-requests/c07-r01.yaml --output akari-v1.2/comparisons/c07-r01/c07-r01-pair-comparison.webp"
```

- [ ] **Step 4: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_paired_candidate_comparison \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests -v
git add scripts/build_v1_2_paired_candidate_comparison.py \
  tests/test_build_v1_2_paired_candidate_comparison.py \
  tests/test_akari_v1_2_natural_form_package.py package.json
git diff --cached --check
git commit -m "feat: add Natural Form C07 comparison command"
```

---

### Task 4: Generate and freeze three local C07 pairs

**Files:**

- Create locally: six candidate PNGs declared by `c07-r01.yaml`.
- Verify only: accepted C01, accepted C04, and the v1.1 standard-foot set.

**Interfaces:**

- Consumes: the exact request, three visible controlling references, and each same-candidate standing output for its seated call.
- Produces: six real 1024 x 1536 RGB PNGs and six frozen SHA-256 values.

- [ ] **Step 1: Run the pre-generation gate**

```sh
bash -lc 'npm run validate:v1-2'
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests -v
```

Expected: PASS with C07 still `candidate` r00 and no C07 reviews.

- [ ] **Step 2: Open and describe the three fixed references**

Open with `view_image`:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png
akari-v1.2/references/v1.1/standard-foot-set.webp
```

State these roles before generation:

- C01 controls standing body volume, knee state, loading, palette, outfit edge, and rendering; its shoes are excluded.
- C04 controls seated pelvis/leg/contact mechanics, outfit compression, and rendering.
- The foot set controls sock material, two pale-blue stripes, sock height, ankle volume, and foot readability only; its shoes and board layout are excluded.

- [ ] **Step 3: Generate A standing**

Call `image_gen` once with the three fixed references, the exact shared prompt,
and the exact `standing` view prompt. Save the returned PNG to:

```text
akari-v1.2/source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-standing_r01-a.png
```

- [ ] **Step 4: Generate A seated with A standing visible**

Open A standing with `view_image`. Call `image_gen` once with C01, C04, the
foot set, and A standing visible. State that A standing is a supporting sock
consistency anchor and cannot override C04 anatomy. Use the exact shared and
`seated` prompts. Save to:

```text
akari-v1.2/source/candidates/c07/r01/akari-v1.2_c07_indoor-socks-seated_r01-a.png
```

- [ ] **Step 5: Generate B and C in the same fixed sequence**

Repeat Steps 3 and 4 independently for B, then C. Before each call reopen all
references used by that call. Do not use A while generating B or C, and do not
use B while generating C.

Save to the exact four remaining declared paths.

- [ ] **Step 6: Recover a rendered image only if no local PNG exists**

If `image_gen` rendered an image but no file is available, follow the repository
rollout recovery rule: parse the current day's rollout JSONL, select the
`image_generation_call` whose `result` starts with `iVBOR`, verify decoded PNG
signature `89504e470d0a1a0a`, and write only the matching declared candidate
path. Never hand-copy base64 from terminal output.

- [ ] **Step 7: Freeze dimensions, format, and hashes**

```sh
file akari-v1.2/source/candidates/c07/r01/*.png
identify -format '%f %wx%h %[colorspace]\n' \
  akari-v1.2/source/candidates/c07/r01/*.png
sha256sum akari-v1.2/source/candidates/c07/r01/*.png
```

Expected: six distinct real PNGs, each 1024 x 1536 and RGB/sRGB. Record all
six exact hashes for Task 6.

---

### Task 5: Compare and review A/B/C pairs

**Files:**

- Create locally: `akari-v1.2/comparisons/c07-r01/c07-r01-pair-comparison.webp`.
- Create locally if needed: `tmp/c07-review/` crops.

**Interfaces:**

- Consumes: six frozen candidate PNGs and the C07 review gates.
- Produces: one pair comparison, findings for every pair, and an explicit literal user selection.

- [ ] **Step 1: Build the pair sheet**

```sh
bash -lc 'npm run build:v1-2:c07-comparison'
file akari-v1.2/comparisons/c07-r01/c07-r01-pair-comparison.webp
identify -format '%f %wx%h\n' \
  akari-v1.2/comparisons/c07-r01/c07-r01-pair-comparison.webp
```

Expected: a real 660 x 1658 WebP with A/B/C rows and standing/seated columns.

- [ ] **Step 2: Review at pair and original resolution**

Open the comparison sheet and all six originals with `view_image`. Use
`akari-v1-1-image-review` for the quality-first review. Inspect in this order:

1. exactly two pale-blue stripes and pair rendering consistency
2. upper leg to knee to shin to ankle to toe trace
3. standing loading and foot contact
4. seated pelvis/knee/ankle/contact coordination
5. pair sock height, stripe placement, ankle volume, and foot length
6. production artifacts and crop readability

Treat a numeric framing miss as advisory evidence only. Assign a framing Major
only if structural foot or contact review is prevented.

- [ ] **Step 3: Stop for literal user selection**

Present pair-level A/B/C findings, identify every unresolved Blocker/Major,
state which pairs remain selectable, and recommend the strongest eligible
pair. Ask the user to select exactly `A`, `B`, or `C`.

Do not modify `assets.yaml`, `review-log.yaml`, or accepted C07 files before the
literal selection.

---

### Task 6: Promote exactly the user-selected C07 pair

**Files:**

- Create: both accepted C07 r01 PNGs.
- Modify: `akari-v1.2/manifest/assets.yaml`.
- Modify: `akari-v1.2/manifest/review-log.yaml`.
- Modify: `tests/test_akari_v1_2_natural_form_package.py`.

**Interfaces:**

- Consumes: literal pair selection, six frozen paths and hashes, and pair findings.
- Produces: one accepted C07 r01 asset with two accepted paths and one complete ordered review batch.

- [ ] **Step 1: Reconfirm all six hashes**

```sh
sha256sum akari-v1.2/source/candidates/c07/r01/*.png
```

Stop if any hash differs from Task 4.

- [ ] **Step 2: Write the failing final-state lifecycle test**

Add to `NaturalFormLifecycleTests`:

```python
def test_c07_acceptance_links_asset_review_and_declared_pair(self):
    c07 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C07"
    )
    self.assertEqual(c07["status"], "accepted")
    self.assertEqual(c07["revision"], "r01")
    self.assertEqual(
        c07["accepted_paths"],
        [
            "accepted/core/indoor-feet/"
            "akari-v1.2_c07_indoor-socks-standing_r01.png",
            "accepted/core/indoor-feet/"
            "akari-v1.2_c07_indoor-socks-seated_r01.png",
        ],
    )
    reviews = [
        review for review in self.review_log["reviews"]
        if (review["asset_id"], review["revision"]) == ("C07", "r01")
    ]
    self.assertEqual(
        [review["candidate_id"] for review in reviews],
        ["c07-r01-a", "c07-r01-b", "c07-r01-c"],
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

- [ ] **Step 3: Run the lifecycle test and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests.test_c07_acceptance_links_asset_review_and_declared_pair -v
```

Expected: FAIL because C07 is candidate r00 and has no review batch.

- [ ] **Step 4: Copy only the selected pair byte-for-byte**

Map the literal selection to the matching suffix `a`, `b`, or `c`. Copy the
standing and seated source with that same suffix to:

```text
akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-standing_r01.png
akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png
```

Use `cp`; do not resize or edit. Run `cmp --silent` from each selected source
to its accepted destination and require exit code 0.

- [ ] **Step 5: Update the C07 asset and append exact reviews**

Change only C07 in `assets.yaml`:

```yaml
    status: accepted
    revision: r01
    accepted_paths:
      - accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-standing_r01.png
      - accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png
```

Append three C07 r01 reviews in A/B/C order. Each review uses candidate ID
`c07-r01-{variant}`, both literal source paths in standing/seated order, both
observed SHA-256 values in the same order, the actual Task 5 findings, and a
pair-level decision. Mark only the selected pair `accepted`; mark the other
two `rejected`. The selected review has no unresolved Blocker or Major.

- [ ] **Step 6: Verify lifecycle and byte identity**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
sha256sum akari-v1.2/source/candidates/c07/r01/*.png \
  akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_*.png
```

Expected: PASS; both accepted hashes equal the corresponding two selected
sources.

- [ ] **Step 7: Commit durable acceptance only**

```sh
git add akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-standing_r01.png \
  akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --name-only
git diff --cached --check
git commit -m "feat: accept Natural Form C07 r01 pair"
```

Before committing, confirm no C07 candidate PNG, comparison WebP, C04 local
artifact, or review crop is staged.

---

### Task 7: Run final branch-state verification

**Files:**

- Verify only; do not broaden scope to unrelated changes.

**Interfaces:**

- Consumes: final C07 request, command, reviews, asset record, and accepted pair.
- Produces: fresh completion evidence on the final branch state.

- [ ] **Step 1: Run focused and full test suites**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_paired_candidate_comparison -v
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

- [ ] **Step 3: Prove final artifacts and repository hygiene**

```sh
file akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_*.png
identify -format '%f %wx%h %[colorspace]\n' \
  akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_*.png
git diff --check
git status --short --branch
```

Expected: two real 1024 x 1536 RGB/sRGB PNGs, no whitespace errors, no staged
or tracked candidates/comparisons, and only expected local-only C04/C07 review
artifacts shown separately.

---

## Execution Stop Conditions

- Stop before generation if contract or dependency validation is red.
- Stop a pair immediately when either member has a Blocker; never reuse its other member in another pair.
- Stop after three pairs; do not silently generate a fourth.
- Stop after review until the user explicitly selects A, B, or C.
- Stop before promotion if the selected pair has an unresolved Blocker or Major.
- Stop completion claims until every Task 7 command has fresh passing output.

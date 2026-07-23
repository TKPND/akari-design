# Akari v1.2 C01 Natural Front Stance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, review, and accept one C01 Natural Form front-standing image from a controlled three-candidate posture comparison.

**Architecture:** Add a durable C01 generation-request contract and extend the Natural Form validator from pre-production-only checks to real revision and review lifecycle checks. Generate three local candidates from the same v1.1 references, build a reproducible comparison sheet, stop for user selection, then promote only the selected revision and record its review decision.

**Tech Stack:** Python 3.11+, PyYAML, Pillow, `unittest`, npm scripts, Codex `image_gen`, PNG assets

## Global Constraints

- Preserve the Akari v1.1 identity, 25-year-old age impression, face, head-to-body ratio, short warm-brown bob, character-left hair accessories, warm-brown eyes, sturdy healthy legs, and standard outfit.
- Use `akari-v1.2/references/v1.1/front.webp`, both v1.1 45-degree references, and `akari-v1.2/references/v1.1/shoes.webp` as generation references after opening each one with `view_image`.
- Do not use pre-Natural Form legacy images as generation references; use them only after generation for comparison.
- Generate exactly three standalone front full-body candidates; vary only posture relaxation and weight distribution.
- Candidate A is conservative, B is the standard Natural Form target, and C uses subtle asymmetry capped at 55:45 loading.
- Keep the background plain and low contrast. Keep the complete hair and shoes in frame. No text, logo, watermark, collage, grid, split screen, or contact sheet in generated source images.
- Do not blend candidates or hide anatomy failures with low-diff compositing.
- Stop for explicit user selection before promotion to `accepted/core/standing/`.
- Keep working candidates and comparison artifacts uncommitted. Commit only durable code, manifests, review metadata, and the user-approved accepted asset.
- C02 through D01 remain unchanged in this plan.

---

## File map

- `akari-v1.2/manifest/generation-requests/c01-r01.yaml`: exact reference roles, shared prompt, candidate posture deltas, target paths, and acceptance gates for the first C01 round.
- `scripts/validate_akari_v1_2_natural_form.py`: validates generation requests, live asset revisions, accepted paths, and non-empty review records.
- `tests/test_akari_v1_2_natural_form_package.py`: regression coverage for generation-request and lifecycle validation.
- `scripts/build_v1_2_c01_comparison.py`: builds the labeled three-column review sheet from the request contract and generated candidate files.
- `tests/test_build_v1_2_c01_comparison.py`: verifies request order, missing-file behavior, and comparison dimensions.
- `akari-v1.2/source/candidates/c01/r01/*.png`: uncommitted first-round candidate images.
- `akari-v1.2/comparisons/c01-r01/c01-r01-comparison.webp`: uncommitted review artifact.
- `akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_rNN.png`: selected accepted asset.
- `akari-v1.2/manifest/assets.yaml`: C01 revision, status, and accepted path.
- `akari-v1.2/manifest/review-log.yaml`: candidate outcomes, findings, and final C01 decision.

---

### Task 1: Make the Natural Form manifests production-capable

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/c01-r01.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: existing `load_yaml(path: Path) -> dict`, asset IDs, statuses, severities, gates, and canonical package root.
- Produces: `validate_generation_request(data: dict) -> None`, production-capable `validate_assets(data: dict, package_root: Path | None = None) -> None`, and `validate_review_log(data: dict) -> None`.

- [ ] **Step 1: Add failing lifecycle and generation-request tests**

Add `re`-safe lifecycle cases and generation request coverage to
`tests/test_akari_v1_2_natural_form_package.py`:

```python
from scripts.validate_akari_v1_2_natural_form import (  # noqa: E402
    ValidationError,
    load_yaml,
    validate_assets,
    validate_generation_request,
    validate_inheritance,
    validate_review_log,
)


class NaturalFormGenerationRequestTests(unittest.TestCase):
    def setUp(self):
        self.data = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c01-r01.yaml"
        )

    def test_c01_r01_has_three_posture_only_candidates(self):
        validate_generation_request(self.data)
        self.assertEqual(self.data["asset_id"], "C01")
        self.assertEqual(
            [candidate["variant"] for candidate in self.data["candidates"]],
            ["a", "b", "c"],
        )
        self.assertEqual(self.data["variation_axis"], "posture_relaxation")

    def test_generation_request_rejects_legacy_reference(self):
        invalid = copy.deepcopy(self.data)
        invalid["references"][0]["path"] = (
            "legacy/akari-v1.2-pre-natural-form/front.webp"
        )
        with self.assertRaisesRegex(ValidationError, "canonical v1.1 reference"):
            validate_generation_request(invalid)


def accepted_c01_assets(assets: dict) -> dict:
    updated = copy.deepcopy(assets)
    c01 = updated["assets"][0]
    c01["status"] = "accepted"
    c01["revision"] = "r01"
    c01["accepted_path"] = (
        "accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r01.png"
    )
    return updated


class NaturalFormLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.assets = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        self.review_log = load_yaml(PACKAGE_ROOT / "manifest/review-log.yaml")

    def test_assets_accept_a_canonical_nonzero_revision(self):
        validate_assets(accepted_c01_assets(self.assets))

    def test_assets_reject_revision_path_mismatch(self):
        invalid = accepted_c01_assets(self.assets)
        invalid["assets"][0]["accepted_path"] = (
            "accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r02.png"
        )
        with self.assertRaisesRegex(ValidationError, "revision mismatch"):
            validate_assets(invalid)

    def test_review_log_accepts_resolved_c01_decisions(self):
        data = copy.deepcopy(self.review_log)
        data["reviews"] = [
            {
                "asset_id": "C01",
                "revision": "r01",
                "candidate_id": "c01-r01-b",
                "status": "accepted",
                "source_path": (
                    "source/candidates/c01/r01/"
                    "akari-v1.2_c01_front-natural-stance_r01-b.png"
                ),
                "findings": [],
                "decision": "Selected after three-candidate posture review.",
            }
        ]
        validate_review_log(data)

    def test_accepted_review_rejects_unresolved_major(self):
        data = copy.deepcopy(self.review_log)
        data["reviews"] = [
            {
                "asset_id": "C01",
                "revision": "r01",
                "candidate_id": "c01-r01-b",
                "status": "accepted",
                "source_path": (
                    "source/candidates/c01/r01/"
                    "akari-v1.2_c01_front-natural-stance_r01-b.png"
                ),
                "findings": [
                    {
                        "severity": "major",
                        "category": "body",
                        "note": "Right ankle connection is unclear.",
                        "resolved": False,
                    }
                ],
                "decision": "Accepted incorrectly.",
            }
        ]
        with self.assertRaisesRegex(ValidationError, "unresolved major"):
            validate_review_log(data)
```

- [ ] **Step 2: Run the focused tests and verify failure**

Run:

```sh
uv run python -m unittest tests.test_akari_v1_2_natural_form_package
```

Expected: FAIL because `c01-r01.yaml` and `validate_generation_request` do not
exist, and the current validator requires `r00` plus an empty review list.

- [ ] **Step 3: Create the exact C01 generation-request contract**

Create `akari-v1.2/manifest/generation-requests/c01-r01.yaml`:

```yaml
schema_version: 1
request_id: akari-v1.2-c01-r01
asset_id: C01
revision: r01
variation_axis: posture_relaxation
references:
  - role: primary_front_identity
    path: akari-v1.2/references/v1.1/front.webp
  - role: hairpin_side_identity
    path: akari-v1.2/references/v1.1/hairpin-side-45.webp
  - role: non_hairpin_side_identity
    path: akari-v1.2/references/v1.1/non-hairpin-side-45.webp
  - role: shoe_construction
    path: akari-v1.2/references/v1.1/shoes.webp
shared_prompt: >-
  Use the visible v1.1 images as strict identity, face, short-bob,
  character-left pale-blue hair-accessory, body-proportion, standard-outfit,
  and white-sneaker references for Akari. Create one standalone front-facing
  full-body character reference image of the same 25-year-old Akari on a plain
  low-contrast background. Preserve her warm-brown eyes, compact anime
  proportions, sturdy healthy legs with fuller thighs and soft calves, white
  hoodie, gray pleated skirt, two-line socks, and white chunky sneakers. Keep
  her normal neutral expression and soft anime rendering with pale shading and
  restrained outlines. Show believable natural joints and standing weight
  balance. Keep complete hair and shoes in frame with breathing room. No props,
  logos, readable text, watermark, collage, grid, split screen, multi-panel, or
  contact sheet. Avoid thin legs, elongated proportions, fashion-model pose,
  locked knees, twisted ankles, mirrored hair accessories, age drift, dramatic
  lighting, and photorealistic skin.
candidates:
  - variant: a
    title: conservative-relaxation
    posture_delta: >-
      Stay closest to the v1.1 frontal stance: nearly even loading, pelvis
      nearly level, feet almost parallel with a slight outward angle, and only
      small softness in knees, shoulders, and elbows.
    target_path: source/candidates/c01/r01/akari-v1.2_c01_front-natural-stance_r01-a.png
  - variant: b
    title: standard-natural-form
    posture_delta: >-
      Use approximately even loading with visibly unlocked knees, relaxed
      shoulders, soft elbows, neutral lumbar curve, and no staged pose.
    target_path: source/candidates/c01/r01/akari-v1.2_c01_front-natural-stance_r01-b.png
  - variant: c
    title: softer-asymmetry
    posture_delta: >-
      Use subtle loading asymmetry no greater than 55:45 with small matching
      shoulder and arm-height differences, while keeping the pelvis nearly
      horizontal and avoiding a model pose.
    target_path: source/candidates/c01/r01/akari-v1.2_c01_front-natural-stance_r01-c.png
acceptance_gates: [identity, body, rendering]
hard_rejects:
  - identity drift
  - age drift
  - elongated proportions
  - overly thin legs
  - locked knees
  - twisted or disconnected ankles
  - mirrored or missing hair accessories
  - incomplete full-body crop
  - readable text, logo, or watermark
```

- [ ] **Step 4: Implement production validation**

In `scripts/validate_akari_v1_2_natural_form.py`, import `re`, add the shared
revision expression, and replace the pre-production-only checks:

```python
import re

REVISION_RE = re.compile(r"^r\d{2}$")
REVIEW_CATEGORIES = ("identity", "body", "state", "rendering", "production")


def validate_generation_request(data: dict) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("generation request: schema_version must be 1")
    if data.get("asset_id") != "C01" or data.get("revision") != "r01":
        raise ValidationError("generation request: expected C01 r01")
    if data.get("variation_axis") != "posture_relaxation":
        raise ValidationError("generation request: invalid variation axis")
    references = data.get("references")
    if not isinstance(references, list) or len(references) != 4:
        raise ValidationError("generation request: expected four references")
    for reference in references:
        path = reference.get("path")
        if (
            not isinstance(path, str)
            or not path.startswith("akari-v1.2/references/v1.1/")
            or ".." in PurePosixPath(path).parts
        ):
            raise ValidationError("generation request: canonical v1.1 reference required")
        if not reference.get("role"):
            raise ValidationError("generation request: reference role required")
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or [c.get("variant") for c in candidates] != [
        "a",
        "b",
        "c",
    ]:
        raise ValidationError("generation request: expected candidates a, b, c")
    for candidate in candidates:
        expected = (
            "source/candidates/c01/r01/"
            f"akari-v1.2_c01_front-natural-stance_r01-{candidate['variant']}.png"
        )
        if candidate.get("target_path") != expected:
            raise ValidationError("generation request: invalid candidate target path")
        if not candidate.get("posture_delta") or not candidate.get("title"):
            raise ValidationError("generation request: candidate details required")
    if not data.get("shared_prompt"):
        raise ValidationError("generation request: shared prompt required")
    if data.get("acceptance_gates") != ["identity", "body", "rendering"]:
        raise ValidationError("generation request: acceptance gates mismatch")
    if not data.get("hard_rejects"):
        raise ValidationError("generation request: hard rejects required")
```

Replace `validate_assets` with this production-capable implementation:

```python
def validate_assets(data: dict, package_root: Path | None = None) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("assets: schema_version must be 1")
    assets = data.get("assets")
    if not isinstance(assets, list):
        raise ValidationError("assets: assets must be a list")
    ids = [item.get("asset_id") for item in assets]
    if ids != list(ASSET_IDS):
        raise ValidationError(f"assets: expected IDs {ASSET_IDS}, got {ids}")
    known = set(ids)
    for item in assets:
        asset_id = item["asset_id"]
        variants = item.get("variants")
        if (
            not isinstance(variants, list)
            or not variants
            or len(variants) != len(set(variants))
        ):
            raise ValidationError(f"{asset_id}: variants must be unique and non-empty")
        expected_paths = item.get("expected_paths")
        if not isinstance(expected_paths, list) or len(expected_paths) != len(variants):
            raise ValidationError(f"{asset_id}: expected_paths must match variants")
        for expected_path in expected_paths:
            parts = PurePosixPath(expected_path).parts
            if not parts or parts[0] != "accepted" or ".." in parts:
                raise ValidationError(f"{asset_id}: invalid expected_paths entry")
        status = item.get("status")
        if status not in STATUSES:
            raise ValidationError(f"{asset_id}: invalid status")
        if item.get("gate") not in GATES:
            raise ValidationError(f"{asset_id}: invalid gate")
        revision = item.get("revision")
        if not isinstance(revision, str) or not REVISION_RE.fullmatch(revision):
            raise ValidationError(f"{asset_id}: invalid revision")
        if revision == "r00" and status in {"accepted", "accepted-with-notes"}:
            raise ValidationError(f"{asset_id}: r00 cannot be accepted")
        dependencies = item.get("depends_on")
        if not isinstance(dependencies, list):
            raise ValidationError(f"{asset_id}: depends_on must be a list")
        unknown = set(dependencies) - known
        if unknown:
            raise ValidationError(f"{asset_id}: unknown dependency {sorted(unknown)}")
        accepted_path = item.get("accepted_path")
        if status in {"accepted", "accepted-with-notes"}:
            if not isinstance(accepted_path, str):
                raise ValidationError(f"{asset_id}: accepted_path is required")
            revision_paths = [
                expected_path.replace("rNN", revision)
                for expected_path in expected_paths
            ]
            if accepted_path not in revision_paths:
                raise ValidationError(f"{asset_id}: accepted_path revision mismatch")
            if package_root is not None and not (package_root / accepted_path).is_file():
                raise ValidationError(f"{asset_id}: accepted file does not exist")
        elif accepted_path is not None:
            raise ValidationError(f"{asset_id}: accepted_path must be null")
```

Replace `validate_review_log` with this implementation:

```python
def validate_review_log(data: dict) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("review-log: schema_version must be 1")
    if tuple(data.get("allowed_statuses", ())) != STATUSES:
        raise ValidationError("review-log: allowed_statuses mismatch")
    if tuple(data.get("allowed_severities", ())) != SEVERITIES:
        raise ValidationError("review-log: allowed_severities mismatch")
    reviews = data.get("reviews")
    if not isinstance(reviews, list):
        raise ValidationError("review-log: reviews must be a list")
    for review in reviews:
        asset_id = review.get("asset_id")
        if asset_id not in ASSET_IDS:
            raise ValidationError("review-log: unknown asset_id")
        revision = review.get("revision")
        if not isinstance(revision, str) or not REVISION_RE.fullmatch(revision):
            raise ValidationError(f"{asset_id}: invalid review revision")
        candidate_id = review.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            raise ValidationError(f"{asset_id}: candidate_id is required")
        source_path = review.get("source_path")
        if not isinstance(source_path, str):
            raise ValidationError(f"{asset_id}: source_path is required")
        source_parts = PurePosixPath(source_path).parts
        if source_parts[:2] != ("source", "candidates") or ".." in source_parts:
            raise ValidationError(f"{asset_id}: canonical candidate source required")
        status = review.get("status")
        if status not in STATUSES:
            raise ValidationError(f"{asset_id}: invalid review status")
        if not isinstance(review.get("decision"), str) or not review["decision"].strip():
            raise ValidationError(f"{asset_id}: decision is required")
        findings = review.get("findings")
        if not isinstance(findings, list):
            raise ValidationError(f"{asset_id}: findings must be a list")
        for finding in findings:
            severity = finding.get("severity")
            category = finding.get("category")
            if severity not in SEVERITIES:
                raise ValidationError(f"{asset_id}: invalid finding severity")
            if category not in REVIEW_CATEGORIES:
                raise ValidationError(f"{asset_id}: invalid finding category")
            if not isinstance(finding.get("note"), str) or not finding["note"].strip():
                raise ValidationError(f"{asset_id}: finding note is required")
            if not isinstance(finding.get("resolved"), bool):
                raise ValidationError(f"{asset_id}: finding resolution must be boolean")
            if (
                status in {"accepted", "accepted-with-notes"}
                and severity in {"blocker", "major"}
                and not finding["resolved"]
            ):
                raise ValidationError(f"{asset_id}: unresolved {severity}")
```

In `main()`, load and validate the request and pass the package root into asset
validation:

```python
generation_request = load_yaml(
    manifest_root / "generation-requests/c01-r01.yaml"
)
validate_assets(assets, args.package_root)
validate_generation_request(generation_request)
validate_inheritance(inheritance, ROOT, args.package_root)
validate_review_log(review_log)
print(
    f"validated {len(assets['assets'])} assets, "
    f"{len(inheritance['references'])} references, "
    f"{len(generation_request['candidates'])} C01 requests, and "
    f"{len(review_log['reviews'])} reviews"
)
```

- [ ] **Step 5: Run tests and package validation**

Run:

```sh
uv run python -m unittest tests.test_akari_v1_2_natural_form_package
npm run validate:v1-2
npm run lint:md
```

Expected: all Natural Form package tests pass; validator reports 8 assets, 13
references, 3 C01 requests, and 0 reviews; Markdown reports 0 errors.

- [ ] **Step 6: Commit the production contract**

```sh
git add akari-v1.2/manifest/generation-requests/c01-r01.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: define Natural Form C01 generation contract"
```

---

### Task 2: Build a reproducible C01 comparison sheet

**Files:**

- Create: `scripts/build_v1_2_c01_comparison.py`
- Create: `tests/test_build_v1_2_c01_comparison.py`
- Modify: `package.json`

**Interfaces:**

- Consumes: `c01-r01.yaml` candidate order and target paths plus three generated PNG files.
- Produces: `build_comparison(request_path: Path, repository_root: Path, output_path: Path) -> Path` and npm command `build:v1-2:c01-comparison`.

- [ ] **Step 1: Write failing comparison-builder tests**

Create `tests/test_build_v1_2_c01_comparison.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image
import yaml

from scripts.build_v1_2_c01_comparison import build_comparison


class C01ComparisonTests(unittest.TestCase):
    def make_request(self, root: Path) -> Path:
        candidates = []
        for variant, color in zip(("a", "b", "c"), ("red", "green", "blue")):
            target = Path("candidates") / f"candidate-{variant}.png"
            path = root / target
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (200, 300), color).save(path)
            candidates.append(
                {
                    "variant": variant,
                    "title": f"variant-{variant}",
                    "target_path": target.as_posix(),
                }
            )
        request = root / "request.yaml"
        request.write_text(
            yaml.safe_dump({"candidates": candidates}, sort_keys=False),
            encoding="utf-8",
        )
        return request

    def test_builds_three_column_sheet_in_request_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "comparison.webp"
            result = build_comparison(self.make_request(root), root, output)
            self.assertEqual(result, output)
            with Image.open(result) as image:
                self.assertEqual(image.size, (980, 566))

    def test_rejects_a_missing_candidate(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = self.make_request(root)
            (root / "candidates/candidate-b.png").unlink()
            with self.assertRaisesRegex(ValueError, "missing candidate-b.png"):
                build_comparison(request, root, root / "comparison.webp")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify failure**

Run:

```sh
uv run python -m unittest tests.test_build_v1_2_c01_comparison
```

Expected: FAIL because `scripts.build_v1_2_c01_comparison` does not exist.

- [ ] **Step 3: Implement the comparison builder**

Create `scripts/build_v1_2_c01_comparison.py` with these constants and behavior:

```python
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "akari-v1.2/manifest/generation-requests/c01-r01.yaml"
OUTPUT = ROOT / "akari-v1.2/comparisons/c01-r01/c01-r01-comparison.webp"
CARD_SIZE = (300, 480)
GAP = 20
LABEL_HEIGHT = 46
BACKGROUND = "#f3f0ec"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2927"


def load_font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def build_comparison(
    request_path: Path, repository_root: Path, output_path: Path
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    candidates = request["candidates"]
    if [candidate["variant"] for candidate in candidates] != ["a", "b", "c"]:
        raise ValueError("expected candidates a, b, c")
    width = GAP * 4 + CARD_SIZE[0] * 3
    height = GAP * 2 + CARD_SIZE[1] + LABEL_HEIGHT
    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    for index, candidate in enumerate(candidates):
        source = repository_root / candidate["target_path"]
        if not source.is_file():
            raise ValueError(f"missing {source.name}")
        x = GAP + index * (CARD_SIZE[0] + GAP)
        y = GAP
        draw.rectangle(
            (x, y, x + CARD_SIZE[0], y + CARD_SIZE[1] + LABEL_HEIGHT),
            fill=CARD_BACKGROUND,
        )
        with Image.open(source) as image:
            fitted = ImageOps.contain(image.convert("RGB"), CARD_SIZE)
        image_x = x + (CARD_SIZE[0] - fitted.width) // 2
        image_y = y + (CARD_SIZE[1] - fitted.height) // 2
        sheet.paste(fitted, (image_x, image_y))
        label = f"{candidate['variant'].upper()}  {candidate['title']}"
        draw.text((x + 10, y + CARD_SIZE[1] + 13), label, fill=TEXT, font=font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=94)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, default=REQUEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_comparison(args.request, ROOT, args.output)
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Add the npm command**

Add to `package.json` scripts:

```json
"build:v1-2:c01-comparison": "uv run python scripts/build_v1_2_c01_comparison.py"
```

- [ ] **Step 5: Run focused and regression tests**

Run:

```sh
uv run python -m unittest tests.test_build_v1_2_c01_comparison
npm run test:python
npm run lint:md
```

Expected: 2 comparison tests pass, both root and legacy Python suites pass, and
Markdown reports 0 errors.

- [ ] **Step 6: Commit the comparison builder**

```sh
git add scripts/build_v1_2_c01_comparison.py \
  tests/test_build_v1_2_c01_comparison.py package.json
git commit -m "feat: build Natural Form C01 comparisons"
```

---

### Task 3: Generate and review the three C01 candidates

**Files:**

- Create locally: `akari-v1.2/source/candidates/c01/r01/akari-v1.2_c01_front-natural-stance_r01-a.png`
- Create locally: `akari-v1.2/source/candidates/c01/r01/akari-v1.2_c01_front-natural-stance_r01-b.png`
- Create locally: `akari-v1.2/source/candidates/c01/r01/akari-v1.2_c01_front-natural-stance_r01-c.png`
- Create locally: `akari-v1.2/comparisons/c01-r01/c01-r01-comparison.webp`

**Interfaces:**

- Consumes: the four reference images and the shared plus per-candidate prompts from `c01-r01.yaml`.
- Produces: three valid PNG candidates, one comparison WEBP, and a user-facing review recommendation. No committed files are produced before user selection.

- [ ] **Step 1: Verify baseline and open all references**

Run:

```sh
npm run validate:v1-2
git status --short
```

Expected: validation passes and the tree is clean. Open each of the four
reference paths with `view_image`. In the generation prompt, explicitly assign
the role recorded in `c01-r01.yaml` to each visible reference.

- [ ] **Step 2: Generate candidate A**

Use `image_gen` with the four inspected reference paths and the exact
`shared_prompt` followed by candidate A's `posture_delta`. Save the result to
the A target path. Do not include B or C in the same source image.

Verify its file signature:

```sh
xxd -l 8 -p akari-v1.2/source/candidates/c01/r01/akari-v1.2_c01_front-natural-stance_r01-a.png
```

Expected: `89504e470d0a1a0a`.

- [ ] **Step 3: Generate candidates B and C independently**

Repeat Step 2 with the same references and `shared_prompt`, changing only to B
and C's respective `posture_delta`. Verify both PNG signatures with `xxd`.

If an image is visible in the conversation but its local PNG is missing, use
the repository AGENTS.md rollout-payload recovery procedure. Parse the JSONL
structurally, verify the decoded PNG signature, and save it only to the target
candidate path.

- [ ] **Step 4: Build and inspect the comparison**

Run:

```sh
npm run build:v1-2:c01-comparison
```

Expected: writes
`akari-v1.2/comparisons/c01-r01/c01-r01-comparison.webp`. Open each candidate at
original detail and then open the comparison sheet.

- [ ] **Step 5: Review in gate order**

For A, B, and C, record findings in working notes using this exact review order:

```text
Identity: face, age, bob, accessory side, head-to-body ratio, v1.1 read
Body: leg thickness, knee state, ankle connection, foot direction, pelvis, loading
Rendering: outfit, D65 stability, crop, background, artifacts, text/watermark
```

Open `akari-v1.2/references/legacy/front.webp` only after this first review and
use it as a comparison check, not a generation source or acceptance authority.

- [ ] **Step 6: Stop for user selection**

Show the three candidates, concise findings, and a quality-first recommendation.
Ask the user to select A, B, C, or request a new complete round. Do not promote,
edit, or commit any generated image before this answer.

---

### Task 4: Correct if needed, promote the selected C01, and verify

**Files:**

- Optional local create: `akari-v1.2/source/candidates/c01/r02/akari-v1.2_c01_front-natural-stance_r02-<variant>.png`
- Create: `akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_rNN.png`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`

**Interfaces:**

- Consumes: explicit user selection plus candidate review findings.
- Produces: one accepted C01 PNG, a matching C01 asset record, review history for all reviewed candidates, and a passing package validation.

- [ ] **Step 1: Apply the correction rule**

If the selected candidate has an unresolved Major, use `image_gen` to edit that
exact candidate with the same four references and one narrowly scoped change.
Store the result as `r02` with the same variant suffix and repeat the complete
Identity, Body, Rendering review. If it has no unresolved Blocker or Major,
keep `r01`. Never accept a Blocker.

- [ ] **Step 2: Promote the approved image**

Copy the approved source image without resampling or recompression to:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
```

Use `r02` in the filename instead when a Correction Pass was required. Verify
that source and accepted SHA-256 hashes are identical.

- [ ] **Step 3: Update the C01 asset record**

In `akari-v1.2/manifest/assets.yaml`, change only C01:

```yaml
status: accepted
revision: r01
accepted_path: accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
```

Use `r02` consistently in all three fields when a Correction Pass was accepted.

- [ ] **Step 4: Record review history**

Append one record per reviewed candidate to
`akari-v1.2/manifest/review-log.yaml`. Use `rejected` for non-selected
candidates, `accepted` for the selected candidate, exact candidate source
paths, concrete findings, and the user's selection in `decision`. Every finding
must include `severity`, `category`, `note`, and `resolved`; accepted records
must have no unresolved Blocker or Major.

- [ ] **Step 5: Run the final verification suite**

Run:

```sh
npm run validate:v1-2
npm run test:python
npm run test:node
npm run audit
npm run lint:md
git diff --check
git status --short
```

Expected: all commands pass. The only intended generated file staged for commit
is the accepted C01 PNG; candidate and comparison files remain untracked and
unstaged.

- [ ] **Step 6: Commit C01 acceptance**

Stage the accepted PNG, both updated manifests, and any correction-specific
durable metadata. Do not stage `source/candidates/` or `comparisons/c01-r01/`.

```sh
git add akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml
git commit -m "feat: accept Natural Form C01 stance"
```

When accepting `r02`, replace `r01` in the staged accepted path. Confirm the
resulting commit with `git show --stat --oneline HEAD` and report the selected
variant, accepted revision, review findings, and verification evidence.

# Akari v1.2 C02 Natural Back Stance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, review, and accept one C02 Natural Form rear-standing image as the paired back view of accepted C01.

**Architecture:** Add an exact C02 generation request and generalize the Natural Form validator from one hard-coded C01 request to an ordered collection of asset-specific requests. Extract a manifest-driven comparison builder that preserves the C01 command and adds C02 A/B/C plus C01-alignment sheets. Generate three independent attempts from one locked reference and prompt contract, stop for user selection, then promote only the selected source byte-for-byte.

**Tech Stack:** Python 3.11+, PyYAML, Pillow, `unittest`, npm scripts, Codex `image_gen`, PNG and WebP assets

## Global Constraints

- Treat accepted C01 as the primary stance, body-proportion, landmark-height, framing, and rendering anchor.
- Use exactly five generation references in this order: accepted C01, v1.1 back, hairpin-side 45, non-hairpin-side 45, and shoes.
- Open and inspect all five references with `view_image` before every generation round and state each reference's role in the prompt.
- Do not use `akari-v1.2/references/legacy/back.webp` as a generation reference; open it only after generation for comparison.
- Generate exactly three standalone exact-rear full-body candidates from the same prompt and references. A, B, and C are independent attempts, not pose or style variants.
- Use a 1024 x 1536 portrait canvas. Keep head-top and sole displacement within 2% of canvas height relative to C01, and shoulder, visual-waist, and knee displacement within 3%.
- Show the character-left parallel pins and small ribbon on image-left in the rear view, visible but less prominent than in the front view.
- Preserve compact proportions, healthy sturdy legs, unlocked knees, relaxed shoulders and elbows, nearly level pelvis, white hoodie, gray pleated skirt, two-line socks, and white chunky sneakers.
- Do not intentionally copy or amplify C01's recorded character-left knee-to-foot inward Minor.
- Reject three-quarter rotation, head turning, thin legs, locked knees, twisted anatomy, overinflated hoodie volume, mirrored shoes, wrong-side or missing accessories, incomplete crop, text, logo, watermark, collage, grid, or contact sheet.
- Do not blend candidates or use low-diff compositing to hide failures.
- Keep generated candidates and comparisons uncommitted. Commit durable code, manifests, review metadata, and only the selected accepted asset.
- Stop for explicit user selection before promotion to `accepted/core/standing/`.
- C03 through D01 remain unchanged.

---

## File map

- `akari-v1.2/manifest/generation-requests/c02-r01.yaml`: exact C02 generation contract.
- `scripts/validate_akari_v1_2_natural_form.py`: asset-specific request, dependency, and lifecycle validation.
- `tests/test_akari_v1_2_natural_form_package.py`: validator and npm-command coverage.
- `scripts/build_v1_2_candidate_comparison.py`: generic three-candidate builder with optional anchor.
- `tests/test_build_v1_2_candidate_comparison.py`: rendered order, size, and missing-file coverage.
- `scripts/build_v1_2_c01_comparison.py`: compatibility wrapper for the existing command.
- `tests/test_build_v1_2_c01_comparison.py`: wrapper regression coverage.
- `package.json`: C02 comparison commands.
- `akari-v1.2/source/candidates/c02/r01/*.png`: local candidate outputs.
- `akari-v1.2/comparisons/c02-r01/*.webp`: local review sheets.
- `akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_rNN.png`: selected asset.
- `akari-v1.2/manifest/assets.yaml`: accepted C02 state.
- `akari-v1.2/manifest/review-log.yaml`: A/B/C decisions.

---

### Task 1: Add the exact C02 request contract

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/c02-r01.yaml`
- Modify: `akari-v1.2/manifest/generation-requests/c01-r01.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: `load_yaml(path: Path) -> dict` and `ValidationError`.
- Produces: `GENERATION_REQUEST_CONTRACTS: dict[tuple[str, str], dict]` and `validate_generation_request(data: dict) -> None` for C01 r01 and C02 r01.

- [ ] **Step 1: Write failing C02 request tests**

Change the request test fixture to load `self.c01` and `self.c02`, then add:

```python
def test_c01_and_c02_requests_have_exact_contracts(self):
    validate_generation_request(self.c01)
    validate_generation_request(self.c02)
    self.assertEqual(self.c02["asset_id"], "C02")
    self.assertEqual(self.c02["revision"], "r01")
    self.assertEqual(self.c02["variation_axis"], "generation_attempt")
    self.assertEqual(
        [candidate["variant"] for candidate in self.c02["candidates"]],
        ["a", "b", "c"],
    )

def test_c02_rejects_reordered_references(self):
    invalid = copy.deepcopy(self.c02)
    invalid["references"][0], invalid["references"][1] = (
        invalid["references"][1], invalid["references"][0]
    )
    with self.assertRaisesRegex(ValidationError, "exact reference contract"):
        validate_generation_request(invalid)

def test_c02_rejects_legacy_reference(self):
    invalid = copy.deepcopy(self.c02)
    invalid["references"][1]["path"] = "akari-v1.2/references/legacy/back.webp"
    with self.assertRaisesRegex(ValidationError, "exact reference contract"):
        validate_generation_request(invalid)

def test_c02_rejects_substituted_anchor(self):
    invalid = copy.deepcopy(self.c02)
    invalid["references"][0]["path"] = (
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r99.png"
    )
    with self.assertRaisesRegex(ValidationError, "exact reference contract"):
        validate_generation_request(invalid)

def test_c02_rejects_noncanonical_candidate_path(self):
    invalid = copy.deepcopy(self.c02)
    invalid["candidates"][0]["target_path"] = "source/candidates/c02/a.png"
    with self.assertRaisesRegex(ValidationError, "candidate target path"):
        validate_generation_request(invalid)
```

- [ ] **Step 2: Verify the tests fail**

Run:

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
```

Expected: ERROR because `c02-r01.yaml` is absent and the validator only permits C01.

- [ ] **Step 3: Create `c02-r01.yaml`**

```yaml
schema_version: 1
request_id: akari-v1.2-c02-r01
asset_id: C02
revision: r01
variation_axis: generation_attempt
references:
  - role: accepted_c01_stance
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
  - role: primary_back_identity
    path: akari-v1.2/references/v1.1/back.webp
  - role: hairpin_side_identity
    path: akari-v1.2/references/v1.1/hairpin-side-45.webp
  - role: non_hairpin_side_identity
    path: akari-v1.2/references/v1.1/non-hairpin-side-45.webp
  - role: shoe_construction
    path: akari-v1.2/references/v1.1/shoes.webp
shared_prompt: >-
  Use the five visible images in their declared roles as strict references for
  the accepted C01 stance and framing, v1.1 rear hair and outfit construction,
  character-left hair accessories, opposite bob silhouette, and rear sneaker
  construction. Create one standalone exact rear-facing full-body reference
  image of the same 25-year-old Akari and the same physical stance as accepted
  C01 on a 1024 x 1536 plain low-contrast portrait canvas. Match C01's compact
  proportions, body width, landmark heights, sturdy healthy legs, nearly even
  loading, unlocked knees, relaxed shoulders, soft elbows, nearly level pelvis,
  and neutral lumbar curve. Preserve the rounded warm-brown rear bob and show
  the parallel pins and small pale-blue ribbon on character-left, image-left in
  the rear view, visible but understated. Preserve the white hoodie without
  excess back inflation, gray pleated skirt at C01 length, two-line socks, and
  white chunky sneakers with believable non-mirrored left and right rear
  construction. Keep complete hair and shoes in frame with breathing room.
  No head turn, three-quarter rotation, props, logos, readable text, watermark,
  collage, grid, split screen, multi-panel, or contact sheet. Avoid thin legs,
  elongated proportions, locked knees, twisted ankles, strong hip shift,
  fashion-model pose, mirrored shoes, wrong-side or missing accessories, age
  drift, dramatic lighting, and photorealistic skin. Do not amplify C01's
  recorded mild character-left knee-to-foot inward direction.
candidates:
  - variant: a
    title: independent-attempt-a
    target_path: source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-a.png
  - variant: b
    title: independent-attempt-b
    target_path: source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-b.png
  - variant: c
    title: independent-attempt-c
    target_path: source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-c.png
comparison_anchor: accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
acceptance_gates: [identity, body, rendering]
hard_rejects:
  - wrong rear view or head turn
  - identity or age drift
  - elongated proportions or thin legs
  - locked knees or twisted anatomy
  - wrong-side or missing hair accessories
  - overinflated hoodie back
  - mirrored shoes
  - incomplete full-body crop
  - readable text, logo, or watermark
```

Add `comparison_anchor: null` to `c01-r01.yaml`.

- [ ] **Step 4: Implement exact asset-specific validation**

Replace the single reference constant with `GENERATION_REQUEST_CONTRACTS`. Each contract contains `variation_axis`, exact ordered `references`, `candidate_prefix`, `candidate_stem`, optional `candidate_detail`, and `comparison_anchor`. Use the following generic body:

```python
GENERATION_REQUEST_CONTRACTS = {
    ("C01", "r01"): {
        "variation_axis": "posture_relaxation",
        "references": (
            ("primary_front_identity", "akari-v1.2/references/v1.1/front.webp"),
            (
                "hairpin_side_identity",
                "akari-v1.2/references/v1.1/hairpin-side-45.webp",
            ),
            (
                "non_hairpin_side_identity",
                "akari-v1.2/references/v1.1/non-hairpin-side-45.webp",
            ),
            ("shoe_construction", "akari-v1.2/references/v1.1/shoes.webp"),
        ),
        "candidate_prefix": "source/candidates/c01/r01/",
        "candidate_stem": "akari-v1.2_c01_front-natural-stance_r01",
        "candidate_detail": "posture_delta",
        "comparison_anchor": None,
    },
    ("C02", "r01"): {
        "variation_axis": "generation_attempt",
        "references": (
            (
                "accepted_c01_stance",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
            ),
            ("primary_back_identity", "akari-v1.2/references/v1.1/back.webp"),
            (
                "hairpin_side_identity",
                "akari-v1.2/references/v1.1/hairpin-side-45.webp",
            ),
            (
                "non_hairpin_side_identity",
                "akari-v1.2/references/v1.1/non-hairpin-side-45.webp",
            ),
            ("shoe_construction", "akari-v1.2/references/v1.1/shoes.webp"),
        ),
        "candidate_prefix": "source/candidates/c02/r01/",
        "candidate_stem": "akari-v1.2_c02_back-natural-stance_r01",
        "candidate_detail": None,
        "comparison_anchor": (
            "accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png"
        ),
    },
}
```

Then use the following generic body:

```python
def validate_generation_request(data: dict) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("generation request: schema_version must be 1")
    key = (data.get("asset_id"), data.get("revision"))
    contract = GENERATION_REQUEST_CONTRACTS.get(key)
    if contract is None:
        raise ValidationError(f"generation request: unsupported request {key}")
    if data.get("request_id") != f"akari-v1.2-{key[0].lower()}-{key[1]}":
        raise ValidationError("generation request: request_id mismatch")
    if data.get("variation_axis") != contract["variation_axis"]:
        raise ValidationError("generation request: invalid variation axis")
    references = data.get("references")
    actual = tuple(
        (item.get("role"), item.get("path"))
        for item in references or ()
        if isinstance(item, dict)
    )
    if actual != contract["references"]:
        raise ValidationError("generation request: exact reference contract required")
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or [
        item.get("variant") for item in candidates
    ] != ["a", "b", "c"]:
        raise ValidationError("generation request: expected candidates a, b, c")
    for candidate in candidates:
        variant = candidate["variant"]
        expected = (
            f"{contract['candidate_prefix']}"
            f"{contract['candidate_stem']}-{variant}.png"
        )
        if candidate.get("target_path") != expected:
            raise ValidationError("generation request: invalid candidate target path")
        if not candidate.get("title"):
            raise ValidationError("generation request: candidate title required")
        detail = contract["candidate_detail"]
        if detail is not None and not candidate.get(detail):
            raise ValidationError(f"generation request: {detail} required")
    if data.get("comparison_anchor") != contract["comparison_anchor"]:
        raise ValidationError("generation request: comparison anchor mismatch")
    if not data.get("shared_prompt"):
        raise ValidationError("generation request: shared prompt required")
    if data.get("acceptance_gates") != ["identity", "body", "rendering"]:
        raise ValidationError("generation request: acceptance gates mismatch")
    if not data.get("hard_rejects"):
        raise ValidationError("generation request: hard rejects required")
```

The C01 contract retains its current four references and `posture_delta`; the C02 contract uses the five paths above and no candidate detail field.

- [ ] **Step 5: Verify green and commit**

Run:

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v
```

Expected: PASS.

```sh
git add akari-v1.2/manifest/generation-requests scripts/validate_akari_v1_2_natural_form.py tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: define Natural Form C02 generation contract"
```

---

### Task 2: Validate multiple lifecycles and the C01 dependency

**Files:**

- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Produces: `load_generation_requests(request_root: Path) -> list[dict]`, `validate_generation_dependencies(assets: dict, requests: list[dict]) -> None`, and `validate_lifecycle_linkage(assets: dict, generation_requests: list[dict], review_log: dict) -> None`.

- [ ] **Step 1: Write failing collection and dependency tests**

```python
class NaturalFormGenerationCollectionTests(unittest.TestCase):
    def setUp(self):
        self.assets = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        self.requests = load_generation_requests(
            PACKAGE_ROOT / "manifest/generation-requests"
        )

    def test_requests_load_in_asset_revision_order(self):
        self.assertEqual(
            [(item["asset_id"], item["revision"]) for item in self.requests],
            [("C01", "r01"), ("C02", "r01")],
        )

    def test_c02_requires_the_accepted_c01_anchor(self):
        validate_generation_dependencies(self.assets, self.requests)

    def test_c02_rejects_a_nonaccepted_c01_dependency(self):
        invalid = copy.deepcopy(self.assets)
        c01 = next(item for item in invalid["assets"] if item["asset_id"] == "C01")
        c01.update(status="candidate", revision="r00", accepted_path=None)
        with self.assertRaisesRegex(ValidationError, "C02 requires accepted C01"):
            validate_generation_dependencies(invalid, self.requests)
```

Update all lifecycle tests to pass `self.generation_requests`, loaded with `load_generation_requests(...)`, and add:

```python
def test_c02_accepted_review_must_match_declared_candidate(self):
    assets = copy.deepcopy(self.assets)
    c02 = next(item for item in assets["assets"] if item["asset_id"] == "C02")
    c02.update(
        status="accepted",
        revision="r01",
        accepted_path=(
            "accepted/core/standing/"
            "akari-v1.2_c02_back-natural-stance_r01.png"
        ),
    )
    reviews = copy.deepcopy(self.review_log)
    reviews["reviews"].append(
        {
            "asset_id": "C02",
            "revision": "r01",
            "candidate_id": "c02-r01-arbitrary",
            "status": "accepted",
            "source_path": "source/candidates/c02/r01/arbitrary.png",
            "findings": [],
            "decision": "Invalid undeclared candidate.",
        }
    )
    with self.assertRaisesRegex(ValidationError, "declared C02 candidate"):
        validate_lifecycle_linkage(
            assets, self.generation_requests, reviews
        )
```

- [ ] **Step 2: Verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
```

Expected: FAIL because collection and dependency interfaces do not exist.

- [ ] **Step 3: Implement deterministic loading and dependency validation**

```python
def load_generation_requests(request_root: Path) -> list[dict]:
    requests = [load_yaml(path) for path in sorted(request_root.glob("*.yaml"))]
    keys = [(item.get("asset_id"), item.get("revision")) for item in requests]
    if len(keys) != len(set(keys)):
        raise ValidationError("generation requests: duplicate asset revision")
    return sorted(requests, key=lambda item: (item["asset_id"], item["revision"]))


def validate_generation_dependencies(assets: dict, requests: list[dict]) -> None:
    assets_by_id = {item["asset_id"]: item for item in assets["assets"]}
    requests_by_id = {item["asset_id"]: item for item in requests}
    if "C02" not in requests_by_id:
        return
    c01 = assets_by_id["C01"]
    anchor = requests_by_id["C02"]["references"][0]["path"]
    expected = (
        f"akari-v1.2/{c01['accepted_path']}"
        if isinstance(c01.get("accepted_path"), str)
        else None
    )
    if (
        c01.get("status") not in {"accepted", "accepted-with-notes"}
        or c01.get("revision") != "r01"
        or anchor != expected
    ):
        raise ValidationError("C02 requires accepted C01 r01 at its declared anchor")
```

- [ ] **Step 4: Generalize accepted-review linkage**

Replace the current function with:

```python
def validate_lifecycle_linkage(
    assets: dict, generation_requests: list[dict], review_log: dict
) -> None:
    accepted_statuses = {"accepted", "accepted-with-notes"}
    requests_by_key = {
        (request["asset_id"], request["revision"]): request
        for request in generation_requests
    }
    accepted_assets = {
        (asset["asset_id"], asset["revision"]): asset
        for asset in assets["assets"]
        if asset["status"] in accepted_statuses
    }
    accepted_reviews = [
        review
        for review in review_log["reviews"]
        if review["status"] in accepted_statuses
    ]
    for asset_key in accepted_assets:
        matching = [
            review
            for review in accepted_reviews
            if (review["asset_id"], review["revision"]) == asset_key
        ]
        if len(matching) != 1:
            asset_id, revision = asset_key
            raise ValidationError(
                f"{asset_id} {revision}: expected exactly one accepted review"
            )
    for review in accepted_reviews:
        key = (review["asset_id"], review["revision"])
        if key not in accepted_assets:
            raise ValidationError(
                f"{review['asset_id']} {review['revision']}: "
                "accepted review requires a matching accepted asset"
            )
        request = requests_by_key.get(key)
        if request is None:
            raise ValidationError(
                f"{review['asset_id']} accepted review requires a generation request"
            )
        declared = {
            (
                f"{request['asset_id'].lower()}-"
                f"{request['revision']}-{candidate['variant']}",
                candidate["target_path"],
            )
            for candidate in request["candidates"]
        }
        if (review["candidate_id"], review["source_path"]) not in declared:
            raise ValidationError(
                f"{review['asset_id']} accepted review must match one declared "
                f"{review['asset_id']} candidate"
            )
```

- [ ] **Step 5: Update `main()` and verify**

Replace the single request block in `main()` with:

```python
generation_requests = load_generation_requests(
    manifest_root / "generation-requests"
)
validate_assets(assets, args.package_root)
for request in generation_requests:
    validate_generation_request(request)
validate_generation_dependencies(assets, generation_requests)
validate_inheritance(inheritance, ROOT, args.package_root)
validate_review_log(review_log)
validate_lifecycle_linkage(assets, generation_requests, review_log)
candidate_count = sum(
    len(request["candidates"]) for request in generation_requests
)
print(
    f"validated {len(assets['assets'])} assets, "
    f"{len(inheritance['references'])} references, "
    f"{len(generation_requests)} generation requests with "
    f"{candidate_count} candidates, and "
    f"{len(review_log['reviews'])} reviews"
)
```

```sh
uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v
npm run validate:v1-2
```

Expected: PASS and `2 generation requests with 6 candidates` in validator output.

- [ ] **Step 6: Commit**

```sh
git add scripts/validate_akari_v1_2_natural_form.py tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: validate Natural Form generation lifecycles"
```

---

### Task 3: Build reusable C02 comparisons

**Files:**

- Create: `scripts/build_v1_2_candidate_comparison.py`
- Create: `tests/test_build_v1_2_candidate_comparison.py`
- Modify: `scripts/build_v1_2_c01_comparison.py`
- Modify: `tests/test_build_v1_2_c01_comparison.py`
- Modify: `package.json`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Produces: `build_comparison(request_path: Path, package_root: Path, output_path: Path, anchor_path: Path | None = None) -> Path`.
- Preserves: `npm run build:v1-2:c01-comparison`.
- Adds: `npm run build:v1-2:c02-comparison` and `npm run build:v1-2:c02-alignment-comparison`.

- [ ] **Step 1: Write failing generic builder tests**

Create a fixture that writes red, green, and blue candidates in A/B/C order. Add tests for a 980 x 566 three-card sheet and a 1300 x 566 sheet with a yellow anchor followed by A/B/C:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageColor
import yaml

from scripts.build_v1_2_candidate_comparison import build_comparison


def make_request(root: Path) -> Path:
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


def assert_color_close(testcase, actual, expected_name):
    expected = ImageColor.getrgb(expected_name)
    testcase.assertTrue(
        all(abs(left - right) <= 20 for left, right in zip(actual, expected)),
        (actual, expected),
    )


class CandidateComparisonTests(unittest.TestCase):
    def test_builds_three_cards_in_request_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "selection.webp"
            build_comparison(make_request(root), root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (980, 566))
                for x, color in zip((170, 490, 810), ("red", "green", "blue")):
                    assert_color_close(self, image.getpixel((x, 200)), color)

    def test_builds_anchor_then_three_candidates(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            anchor = root / "anchor.png"
            Image.new("RGB", (200, 300), "yellow").save(anchor)
            output = root / "alignment.webp"
            build_comparison(make_request(root), root, output, anchor)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 566))
                expected = ("yellow", "red", "green", "blue")
                for index, color in enumerate(expected):
                    assert_color_close(
                        self, image.getpixel((170 + index * 320, 200)), color
                    )

    def test_rejects_a_missing_candidate(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            (root / "candidates/candidate-b.png").unlink()
            with self.assertRaisesRegex(ValueError, "missing candidate-b.png"):
                build_comparison(request, root, root / "comparison.webp")

    def test_rejects_a_missing_anchor(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "missing anchor.png"):
                build_comparison(
                    make_request(root), root, root / "out.webp", root / "anchor.png"
                )
```

- [ ] **Step 2: Verify red**

```sh
uv run python -m unittest tests.test_build_v1_2_candidate_comparison -v
```

Expected: ERROR because the generic module does not exist.

- [ ] **Step 3: Extract the generic renderer**

Move the drawing constants and `load_font` from the C01 builder. Implement:

```python
def build_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
    anchor_path: Path | None = None,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    candidates = request["candidates"]
    if [item["variant"] for item in candidates] != ["a", "b", "c"]:
        raise ValueError("expected candidates a, b, c")
    cards: list[tuple[str, Path]] = []
    if anchor_path is not None:
        if not anchor_path.is_file():
            raise ValueError(f"missing {anchor_path.name}")
        cards.append(("C01  accepted anchor", anchor_path))
    for candidate in candidates:
        source = package_root / candidate["target_path"]
        if not source.is_file():
            raise ValueError(f"missing {source.name}")
        cards.append(
            (f"{candidate['variant'].upper()}  {candidate['title']}", source)
        )
    width = GAP * (len(cards) + 1) + CARD_SIZE[0] * len(cards)
    height = GAP * 2 + CARD_SIZE[1] + LABEL_HEIGHT
    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    for index, (label, source) in enumerate(cards):
        x = GAP + index * (CARD_SIZE[0] + GAP)
        y = GAP
        draw.rectangle(
            (x, y, x + CARD_SIZE[0], y + CARD_SIZE[1] + LABEL_HEIGHT),
            fill=CARD_BACKGROUND,
        )
        with Image.open(source) as image:
            fitted = ImageOps.contain(image.convert("RGB"), CARD_SIZE)
        sheet.paste(
            fitted,
            (
                x + (CARD_SIZE[0] - fitted.width) // 2,
                y + (CARD_SIZE[1] - fitted.height) // 2,
            ),
        )
        draw.text((x + 10, y + CARD_SIZE[1] + 13), label, fill=TEXT, font=font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=94)
    return output_path
```

Add this CLI so request/output resolve from the repository and the optional anchor resolves from the Natural Form package:

```python
ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--anchor", type=Path)
    args = parser.parse_args()
    request = resolve_from(ROOT, args.request)
    output = resolve_from(ROOT, args.output)
    anchor = (
        resolve_from(PACKAGE_ROOT, args.anchor)
        if args.anchor is not None
        else None
    )
    result = build_comparison(request, PACKAGE_ROOT, output, anchor)
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Preserve the C01 wrapper**

Keep `ROOT`, `REQUEST`, `OUTPUT`, and `main()` in `build_v1_2_c01_comparison.py`; import the generic function and call:

```python
result = build_comparison(args.request, ROOT / "akari-v1.2", args.output)
```

Update the existing mock assertion so the old default command remains covered.

- [ ] **Step 5: Add C02 npm commands**

```json
"build:v1-2:c02-comparison": "uv run python scripts/build_v1_2_candidate_comparison.py --request akari-v1.2/manifest/generation-requests/c02-r01.yaml --output akari-v1.2/comparisons/c02-r01/c02-r01-comparison.webp",
"build:v1-2:c02-alignment-comparison": "uv run python scripts/build_v1_2_candidate_comparison.py --request akari-v1.2/manifest/generation-requests/c02-r01.yaml --output akari-v1.2/comparisons/c02-r01/c02-r01-alignment-comparison.webp --anchor accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png"
```

Extend `NaturalFormIsolationTests` so C01 plus these two C02 commands are the permitted unqualified Natural Form `build:v1-2*` commands.

- [ ] **Step 6: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_candidate_comparison \
  tests.test_build_v1_2_c01_comparison \
  tests.test_akari_v1_2_natural_form_package -v
```

Expected: PASS, including pixel-order assertions.

```sh
git add scripts/build_v1_2_candidate_comparison.py scripts/build_v1_2_c01_comparison.py tests/test_build_v1_2_candidate_comparison.py tests/test_build_v1_2_c01_comparison.py tests/test_akari_v1_2_natural_form_package.py package.json
git commit -m "feat: build Natural Form C02 comparisons"
```

---

### Task 4: Generate the three locked candidates

**Files:**

- Create locally: `akari-v1.2/source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-a.png`
- Create locally: `akari-v1.2/source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-b.png`
- Create locally: `akari-v1.2/source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-c.png`
- Create locally: `akari-v1.2/comparisons/c02-r01/c02-r01-comparison.webp`
- Create locally: `akari-v1.2/comparisons/c02-r01/c02-r01-alignment-comparison.webp`

**Interfaces:**

- Consumes: exact five references and `shared_prompt` in `c02-r01.yaml`.
- Produces: three independent 1024 x 1536 PNGs and two review sheets.

- [ ] **Step 1: Open all five references**

Use `view_image` at original detail for accepted C01, v1.1 back, both v1.1 45-degree views, and shoes. State that C01 controls stance/proportions/framing; back controls rear bob/outfit; 45-degree views control accessory side and bob edges; shoes controls distinct rear construction.

- [ ] **Step 2: Generate A, B, and C separately**

Call `image_gen` three separate times. Every call uses the unchanged five reference paths and exact `shared_prompt`; add no candidate-specific pose or style delta. Save each PNG to its declared target. Never request a grid or multiple images in one source.

- [ ] **Step 3: Rescue payload only if needed**

If a generated image is displayed but no PNG exists, follow AGENTS.md: structurally parse the current day's rollout JSONL, select the matching `image_generation_call` result beginning `iVBOR`, verify PNG signature `89504e470d0a1a0a`, and decode only that payload to the declared path.

- [ ] **Step 4: Verify files and build comparisons**

```sh
identify akari-v1.2/source/candidates/c02/r01/*.png
npm run build:v1-2:c02-comparison
npm run build:v1-2:c02-alignment-comparison
```

Expected: exactly three 1024 x 1536, 8-bit sRGB PNGs and both WebP outputs.

- [ ] **Step 5: Keep generated work local**

Run `git status --short`. If generated folders appear, add local-only entries to `.git/info/exclude`; do not stage candidates or comparisons and do not change committed `.gitignore` for this run.

No commit for this task.

---

### Task 5: Review and stop for user selection

**Files:**

- Inspect: accepted C01, A/B/C, both comparisons, and `akari-v1.2/references/legacy/back.webp`.
- Do not modify: `akari-v1.2/manifest/assets.yaml` or `review-log.yaml` before selection.

**Interfaces:**

- Produces: candidate findings, one recommendation, and an explicit selection gate.

- [ ] **Step 1: Open the complete review set**

Open both WebPs, all three full-resolution PNGs, and legacy back. Legacy is comparison-only and cannot grant acceptance.

- [ ] **Step 2: Review C01 pairing**

For each candidate record exact-rear view, canvas, proportions, head/sole 2% tolerance, shoulder/visual-waist/knee 3% tolerance, width, leg volume, knee state, and weight balance. A tolerance failure is Major; wrong view, severe drift, or unusable anatomy is Blocker.

- [ ] **Step 3: Review rear construction and quality**

Record bob, accessory side, hoodie volume, skirt length, socks, pelvis-knee-ankle continuity, non-mirrored shoes, floor contact, D65 color stability, crop, artifacts, text, logo, and watermark.

- [ ] **Step 4: Recommend and stop**

Reject Blockers. Require a Correction Pass for unresolved Major. Recommend the strongest eligible candidate by identity, anatomy, C01 pairing, and finished quality. Show clickable comparison paths and ask the user to choose A/B/C, request correction, or reject the round. Do not promote yet.

- [ ] **Step 5: Handle a requested Correction Pass without losing the source**

If the user requests a narrow correction for one candidate, copy its original PNG to `akari-v1.2/source/superseded/c02/r01/` with suffix `-pre-correction.png`. Open the selected candidate plus the same five controlling references, then call `image_gen` as an edit with those six images and a prompt limited to the recorded Major. Write the corrected full PNG back to the candidate's declared A, B, or C target path, rebuild both comparison sheets, and repeat Steps 1 through 4. Do not accept until the Major is resolved; record it later with `resolved: true`.

If all three candidates fail identity, stance, or anatomy, stop this plan before Task 6. Preserve the local files, report the shared failure pattern, and create a new r02 design/plan with an explicitly revised common prompt and three new target paths. Do not silently invent an r02 contract or patch a failed base during this plan.

No commit for this task.

---

### Task 6: Promote the selected source and close the lifecycle

**Files:**

- Create: `akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: explicit user selection and Task 5 findings.
- Produces: byte-identical accepted PNG, accepted asset state, A/B/C review records, and validated lifecycle.

- [ ] **Step 1: Write the failing accepted-state test**

```python
def test_c02_acceptance_links_asset_review_and_declared_candidate(self):
    c02 = next(item for item in self.assets["assets"] if item["asset_id"] == "C02")
    self.assertEqual(c02["status"], "accepted")
    self.assertEqual(c02["revision"], "r01")
    self.assertEqual(
        c02["accepted_path"],
        "accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png",
    )
    validate_assets(self.assets, PACKAGE_ROOT)
    validate_review_log(self.review_log)
    validate_lifecycle_linkage(
        self.assets, self.generation_requests, self.review_log
    )
```

- [ ] **Step 2: Verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
```

Expected: FAIL because C02 remains `candidate`, `r00`.

- [ ] **Step 3: Promote the exact selected source**

Choose exactly one source assignment after the user's reply:

```sh
# User chose A
source=akari-v1.2/source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-a.png

# User chose B
source=akari-v1.2/source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-b.png

# User chose C
source=akari-v1.2/source/candidates/c02/r01/akari-v1.2_c02_back-natural-stance_r01-c.png
```

Run only the matching assignment, then:

```sh
accepted=akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png
cp "$source" "$accepted"
cmp "$source" "$accepted"
sha256sum "$source" "$accepted"
```

Expected: `cmp` exits 0 and hashes match.

- [ ] **Step 4: Update manifests**

Set C02 to `status: accepted`, `revision: r01`, and `accepted_path: accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png`. Append A/B/C reviews in order with exact candidate IDs and paths, actual findings, and exactly one accepted status. The accepted candidate has no unresolved Blocker or Major.

- [ ] **Step 5: Run focused and full verification**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
npm run test:python
npm run validate:v1-2
npm run lint:md
npm run audit
git diff --check
```

Expected: all commands PASS; validator reports two requests and six candidates; Markdown has 0 errors.

- [ ] **Step 6: Verify scope and commit**

Re-run `cmp` and `sha256sum`, then inspect `git status --short`, `git diff --stat`, and the two manifest diffs. Candidates and comparisons stay unstaged.

```sh
git add akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png akari-v1.2/manifest/assets.yaml akari-v1.2/manifest/review-log.yaml tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: accept Natural Form C02 stance"
```

- [ ] **Step 7: Post-commit verification**

```sh
npm run validate:v1-2
npm run test:python
npm run lint:md
git status --short --branch
```

Expected: validation and tests remain green; the branch is clean apart from locally excluded C02 working artifacts.

# Akari v1.2 C03 r02 Framing Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close C03 r01 as rejected history, generate a machine-gated C03 r02 A/B/C pair round, and promote exactly one user-selected complete pair byte-for-byte.

**Architecture:** Keep both C03 request revisions as immutable manifest history keyed by `(asset_id, revision)`. Add an exact ordered r02 framing contract to the package validator, then use a focused ImageMagick audit as the hard pre-review gate for all six outputs. Treat A, B, and C as independent pair-atomic retry and freeze units while forbidding member mixing. Candidate images, comparison sheets, and the framing board stay local; only the selected pair and durable lifecycle metadata enter git.

**Tech Stack:** Python 3.12+, PyYAML, Pillow, ImageMagick 7, `unittest`, Node/npm scripts, built-in `imagegen`, Git

## Global Constraints

- Work only in `/path/to/akari-design/.worktrees/c03-paired-views` on branch `feat/akari-v1-2-c03-paired-views`.
- Preserve `akari-v1.2/manifest/generation-requests/c03-r01.yaml` byte-for-byte.
- Never use an r01 C03 candidate, crop, or comparison as an r02 generation reference.
- Keep the five ordered logical reference roles from r01; use a derived C01/C02 board only to stay within the five-file image-generation limit.
- Use one byte-identical shared prompt and one byte-identical view delta across A, B, and C.
- Require every r02 image to be exactly 1024 x 1536 and within 30 px of both C01 and C02 for head-top and sole landmarks.
- Treat 31 px as failure; user preference cannot override an unresolved Blocker or Major.
- Freeze each variant only when both members from the same attempt pass the automatic audit; never overwrite a frozen pair.
- Never mix members across variants or revisions, and never shift, warp, patch, or composite a generated figure into compliance.
- Never mix members across attempts. If either member fails, retire that complete pair attempt and retry only that variant.
- Stop a variant after three pair attempts once the user-agreed cap applies. A
  capped failed variant remains ineligible but does not block selection from a
  different frozen passing pair.
- Keep `akari-v1.2/source/candidates/c03/r02/`, `akari-v1.2/comparisons/c03-r02/`, and `tmp/akari-v1.2/c03-r02/` untracked.
- Use the built-in image-generation tool after opening and assigning a role to every applicable visual reference.
- Run Node/npm commands through `bash -lc`; use `UV_CACHE_DIR=/tmp/akari-uv-cache` when the sandbox cannot write the default uv cache.
- Use `apply_patch` for source and manifest edits; binary promotion may use a byte-preserving file copy.
- Stop for an explicit user selection after both r02 comparison sheets and the visual recommendation are ready.

---

## File Map

### Durable files created

- `akari-v1.2/manifest/generation-requests/c03-r02.yaml` — exact r02 references, prompt, paired outputs, and framing contract.
- `scripts/audit_v1_2_c03_landmarks.py` — ImageMagick measurement and six-file pre-review gate.
- `tests/test_audit_v1_2_c03_landmarks.py` — geometry, boundary, synthetic-image, anchor, and CLI coverage.
- `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png` — selected hairpin-side member.
- `akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png` — selected non-hairpin-side member.

### Durable files modified

- `akari-v1.2/manifest/review-log.yaml` — three rejected r01 records, then three ordered r02 records after selection.
- `akari-v1.2/manifest/assets.yaml` — C03 changes from candidate r00 to accepted r02 only after selection.
- `scripts/validate_akari_v1_2_natural_form.py` — exact r02 contract, ordered mapping comparison, all-revision dependency validation, and review-batch lifecycle validation.
- `tests/test_akari_v1_2_natural_form_package.py` — request, collection, dependency, lifecycle, package-command, and final-state tests.
- `package.json` — explicit r02 audit and comparison commands while retaining r01 commands.

### Local-only files

- `tmp/akari-v1.2/c03-r02/c01-c02-framing-board.png` — geometry-only C01/C02 board.
- `akari-v1.2/source/candidates/c03/r02/*.png` — six frozen r02 candidates.
- `akari-v1.2/comparisons/c03-r02/*.webp` — pair and alignment comparison sheets.
- `.git/info/exclude` — local exclusions for r02 comparisons and temporary work.

---

### Task 1: Close C03 r01 with exact rejected review history

**Files:**

- Modify: `tests/test_akari_v1_2_natural_form_package.py`
- Modify: `akari-v1.2/manifest/review-log.yaml`

**Interfaces:**

- Consumes: unchanged `c03-r01.yaml` candidate order and the six fixed r01 SHA-256 values.
- Produces: one complete rejected review batch keyed by `("C03", "r01")` in A/B/C order.

- [ ] **Step 1: Write the failing r01 history test**

Add this method to `NaturalFormManifestTests`:

```python
def test_c03_r01_reviews_close_all_three_pairs_as_rejected(self):
    reviews = [
        review
        for review in self.review_log["reviews"]
        if (review["asset_id"], review["revision"]) == ("C03", "r01")
    ]
    self.assertEqual(
        [review["candidate_id"] for review in reviews],
        ["c03-r01-a", "c03-r01-b", "c03-r01-c"],
    )
    self.assertEqual([review["status"] for review in reviews], ["rejected"] * 3)
    self.assertEqual(
        [review["source_sha256s"] for review in reviews],
        [
            [
                "3fdf1dc9e5d15f438f512fc2750e05b9830f4f2fb5cad32a2afbcf20fe24d8e8",
                "c681bff18d3dccc17f3edabbb45e4cd6356a66e3ac186581354b7d8586b2a61f",
            ],
            [
                "5aa985aaeccac830aaa9c53819905aea02596a0e0cf2ff768ac348e5d7969374",
                "98f1a3578f5056294610010f2116f2ae798da7cfaaa49ccabbda0703a6d0d4f8",
            ],
            [
                "33d89602f14ed2f73dc6eac5c95ac7798c5d740fa909e7251546d0c50299fa47",
                "7fc375236ca9ffe1c69d95e537af19745233bd153d60bfbab27277f4487e1d9a",
            ],
        ],
    )
    self.assertTrue(
        all(
            finding["resolved"] is False
            for review in reviews
            for finding in review["findings"]
            if finding["severity"] == "major"
        )
    )
    self.assertFalse(
        list(
            (PACKAGE_ROOT / "accepted/core/standing").glob(
                "akari-v1.2_c03_*_r01.png"
            )
        )
    )
```

- [ ] **Step 2: Run the focused test and verify red**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests.test_c03_r01_reviews_close_all_three_pairs_as_rejected -v
```

Expected: FAIL because no C03 reviews exist yet.

- [ ] **Step 3: Reconfirm the local r01 hashes before recording them**

Run:

```sh
sha256sum akari-v1.2/source/candidates/c03/r01/*.png
```

Expected: the six values match the test in Step 1 exactly. Stop if any value differs; do not rewrite history around a mismatched local file.

Also prove the request itself remains unchanged from the recovery-design commit:

```sh
git diff --exit-code 4609eb0 -- \
  akari-v1.2/manifest/generation-requests/c03-r01.yaml
```

Expected: no output and exit code 0.

- [ ] **Step 4: Append the three rejected r01 records**

Append these records to `akari-v1.2/manifest/review-log.yaml` without changing the existing C01/C02 records:

```yaml
  - asset_id: C03
    revision: r01
    candidate_id: c03-r01-a
    status: rejected
    source_paths:
      - source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-a.png
      - source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-a.png
    source_sha256s:
      - 3fdf1dc9e5d15f438f512fc2750e05b9830f4f2fb5cad32a2afbcf20fe24d8e8
      - c681bff18d3dccc17f3edabbb45e4cd6356a66e3ac186581354b7d8586b2a61f
    findings:
      - severity: major
        category: body
        note: >-
          The hairpin-side sole is y=1422, differing from accepted C01 by
          28 px (1.82%) and accepted C02 by 41 px (2.67%); the C02 delta
          exceeds the 30 px hard limit.
        resolved: false
    decision: >-
      Rejected as a complete pair because the hairpin-side member has an
      unresolved sole-height Major. The non-hairpin member passes the measured
      head-top and sole gate but cannot be retained independently.
  - asset_id: C03
    revision: r01
    candidate_id: c03-r01-b
    status: rejected
    source_paths:
      - source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-b.png
      - source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-b.png
    source_sha256s:
      - 5aa985aaeccac830aaa9c53819905aea02596a0e0cf2ff768ac348e5d7969374
      - 98f1a3578f5056294610010f2116f2ae798da7cfaaa49ccabbda0703a6d0d4f8
    findings:
      - severity: major
        category: body
        note: >-
          The hairpin-side sole is y=1410, differing from accepted C01 by
          40 px (2.60%) and accepted C02 by 53 px (3.45%); both deltas exceed
          the 30 px hard limit.
        resolved: false
      - severity: major
        category: body
        note: >-
          The non-hairpin-side sole is y=1411, differing from accepted C01 by
          39 px (2.54%) and accepted C02 by 52 px (3.39%); both deltas exceed
          the 30 px hard limit.
        resolved: false
    decision: >-
      Rejected as a complete pair. The strict landmark re-audit invalidated
      the provisional preference for B before promotion; both members retain
      unresolved sole-height Majors.
  - asset_id: C03
    revision: r01
    candidate_id: c03-r01-c
    status: rejected
    source_paths:
      - source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-c.png
      - source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-c.png
    source_sha256s:
      - 33d89602f14ed2f73dc6eac5c95ac7798c5d740fa909e7251546d0c50299fa47
      - 7fc375236ca9ffe1c69d95e537af19745233bd153d60bfbab27277f4487e1d9a
    findings:
      - severity: major
        category: body
        note: >-
          The hairpin-side sole is y=1424, differing from accepted C01 by
          26 px (1.69%) and accepted C02 by 39 px (2.54%); the C02 delta
          exceeds the 30 px hard limit.
        resolved: false
      - severity: major
        category: body
        note: >-
          The non-hairpin-side sole is y=1427, differing from accepted C01 by
          23 px (1.50%) and accepted C02 by 36 px (2.34%); the C02 delta
          exceeds the 30 px hard limit.
        resolved: false
    decision: >-
      Rejected as a complete pair because both members have unresolved
      sole-height Majors against accepted C02.
```

- [ ] **Step 5: Verify the durable r01 state and commit**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests -v
UV_CACHE_DIR=/tmp/akari-uv-cache npm run validate:v1-2
```

Expected: PASS, with the package summary ending in `9 reviews`.

Commit:

```sh
git add akari-v1.2/manifest/review-log.yaml \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "docs: close Natural Form C03 r01 review"
```

---

### Task 2: Add the exact r02 request and validate every C03 revision

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/c03-r02.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Produces: `C03_R02_FRAMING_CONTRACT: dict` and `ordered_value(value) -> object`.
- Extends: `GENERATION_REQUEST_CONTRACTS` with exact key `("C03", "r02")`.
- Changes: `validate_generation_dependencies()` iterates every C03 request instead of collapsing by asset ID.
- Changes: `validate_lifecycle_linkage()` validates a complete declared batch whenever any reviews exist for a request revision.

- [ ] **Step 1: Add r02 request and framing-contract tests**

Load `self.c03_r01` and `self.c03_r02` separately in `NaturalFormGenerationRequestTests`, then add:

```python
def test_c03_r02_has_exact_framing_contract(self):
    validate_generation_request(self.c03_r02)
    self.assertEqual(
        self.c03_r02["framing_contract"],
        {
            "canvas": {"width": 1024, "height": 1536},
            "measurement": {
                "tool": "imagemagick",
                "fuzz_percent": 6,
                "geometry_format": "%@",
                "head_top_formula": "y",
                "sole_formula": "y_plus_height_minus_1",
            },
            "anchors": [
                {
                    "asset_id": "C01",
                    "revision": "r01",
                    "head_top_y": 65,
                    "sole_y": 1450,
                },
                {
                    "asset_id": "C02",
                    "revision": "r01",
                    "head_top_y": 65,
                    "sole_y": 1463,
                },
            ],
            "maximum_displacement": {
                "percent_of_canvas_height": 2,
                "integer_pixels": 30,
            },
            "required_intersection": {
                "head_top_y": [35, 95],
                "sole_y": [1433, 1480],
            },
            "prompt_target": {
                "head_top_y": 65,
                "sole_y": 1456,
                "bottom_margin_pixels": 79,
            },
        },
    )

def test_c03_r02_rejects_missing_changed_reordered_and_extra_framing_data(self):
    invalid_cases = []

    missing = copy.deepcopy(self.c03_r02)
    del missing["framing_contract"]["prompt_target"]["bottom_margin_pixels"]
    invalid_cases.append(missing)

    changed = copy.deepcopy(self.c03_r02)
    changed["framing_contract"]["maximum_displacement"]["integer_pixels"] = 31
    invalid_cases.append(changed)

    reordered = copy.deepcopy(self.c03_r02)
    framing = reordered["framing_contract"]
    reordered["framing_contract"] = {
        "measurement": framing["measurement"],
        "canvas": framing["canvas"],
        **{key: value for key, value in framing.items() if key not in {"canvas", "measurement"}},
    }
    invalid_cases.append(reordered)

    extra = copy.deepcopy(self.c03_r02)
    extra["framing_contract"]["prompt_target"]["tolerance"] = 1
    invalid_cases.append(extra)

    for invalid in invalid_cases:
        with self.subTest(contract=invalid["framing_contract"]):
            with self.assertRaisesRegex(ValidationError, "framing contract"):
                validate_generation_request(invalid)

def test_c03_r02_prompt_binds_standalone_target_coordinates(self):
    prompt = self.c03_r02["shared_prompt"]
    self.assertIn("head top at y=65", prompt)
    self.assertIn("soles at y=1456", prompt)
    self.assertIn("79 px bottom margin", prompt)
    self.assertIn("never reproduce the board", prompt)
```

- [ ] **Step 2: Add collection, dependency, and pre-selection lifecycle tests**

Change the exact collection assertions to four requests, 12 groups, and 18 outputs. Add these tests:

```python
def test_requests_load_in_asset_revision_order(self):
    self.assertEqual(
        [(item["asset_id"], item["revision"]) for item in self.requests],
        [
            ("C01", "r01"),
            ("C02", "r01"),
            ("C03", "r01"),
            ("C03", "r02"),
        ],
    )

def test_generation_counts_distinguish_groups_from_outputs(self):
    self.assertEqual(count_generation_work(self.requests), (12, 18))

def test_dependency_validation_checks_both_c03_revisions(self):
    for revision in ("r01", "r02"):
        invalid = copy.deepcopy(self.requests)
        request = next(
            item
            for item in invalid
            if (item["asset_id"], item["revision"]) == ("C03", revision)
        )
        request["references"][0]["path"] = (
            "akari-v1.2/accepted/core/standing/substituted-c01.png"
        )
        with self.subTest(revision=revision):
            with self.assertRaisesRegex(
                ValidationError, "C03 requires accepted C01 and C02"
            ):
                validate_generation_dependencies(self.assets, invalid)

def test_rejected_c03_r01_review_batch_must_still_be_complete(self):
    invalid = copy.deepcopy(self.review_log)
    invalid["reviews"] = [
        review
        for review in invalid["reviews"]
        if review["candidate_id"] != "c03-r01-b"
    ]
    with self.assertRaisesRegex(ValidationError, "reviews must match declared"):
        validate_lifecycle_linkage(self.assets, self.generation_requests, invalid)
```

Place the dependency tests in `NaturalFormGenerationCollectionTests` and the
review-batch test in `NaturalFormLifecycleTests`.

Replace `accepted_c03_lifecycle()` so existing synthetic pair tests use r02,
retain the durable r01 history, and remain stable after the real r02 records
are added later:

```python
def accepted_c03_lifecycle(
    assets: dict, generation_requests: list[dict], review_log: dict
) -> tuple[dict, dict]:
    updated_assets = copy.deepcopy(assets)
    c03 = next(
        item for item in updated_assets["assets"] if item["asset_id"] == "C03"
    )
    c03.update(
        status="accepted",
        revision="r02",
        accepted_paths=[
            "accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png",
            "accepted/core/standing/"
            "akari-v1.2_c03_non-hairpin-side-45_r02.png",
        ],
    )
    c03_request = next(
        request
        for request in generation_requests
        if (request["asset_id"], request["revision"]) == ("C03", "r02")
    )
    updated_reviews = copy.deepcopy(review_log)
    updated_reviews["reviews"] = [
        review
        for review in updated_reviews["reviews"]
        if (review["asset_id"], review["revision"]) != ("C03", "r02")
    ]
    for index, candidate in enumerate(c03_request["candidates"]):
        updated_reviews["reviews"].append(
            {
                "asset_id": "C03",
                "revision": "r02",
                "candidate_id": f"c03-r02-{candidate['variant']}",
                "status": "accepted" if candidate["variant"] == "b" else "rejected",
                "source_paths": candidate_source_paths(candidate),
                "source_sha256s": [f"{index + 1:064x}"] * 2,
                "findings": [],
                "decision": f"Synthetic paired decision {candidate['variant']}.",
            }
        )
    return updated_assets, updated_reviews
```

Update the three existing synthetic C03 lookups from `c03-r01-a/b/c` to
`c03-r02-a/b/c`. Change the accepted-review revision-mismatch test's expected
message to `reviews require a matching generation request`, because the new
all-batch validator rejects the unknown revision before accepted-asset lookup.

Import `candidate_source_paths` and `count_generation_work` directly at the
top of the test module rather than using `getattr`.

- [ ] **Step 3: Run the focused tests and verify red**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
```

Expected: ERROR for missing `c03-r02.yaml`, then FAIL for the old three-request counts and asset-ID-collapsing dependency behavior.

- [ ] **Step 4: Create the complete r02 request manifest**

Create `akari-v1.2/manifest/generation-requests/c03-r02.yaml` with this content:

```yaml
schema_version: 1
request_id: akari-v1.2-c03-r02
asset_id: C03
revision: r02
variation_axis: paired_generation_attempt
references:
  - role: accepted_c01_front_stance
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
  - role: accepted_c02_back_stance
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png
  - role: hairpin_side_identity
    path: akari-v1.2/references/v1.1/hairpin-side-45.webp
  - role: non_hairpin_side_identity
    path: akari-v1.2/references/v1.1/non-hairpin-side-45.webp
  - role: shoe_construction
    path: akari-v1.2/references/v1.1/shoes.webp
shared_prompt: >-
  Use the visible images in their declared roles as strict references. Create
  one standalone full-body 45-degree natural-standing reference image of the
  same 25-year-old Akari and the same physical stance as accepted C01 and C02
  on a 1024 x 1536 plain #f1f2f1 portrait canvas. Preserve compact anime
  proportions, stable face and age impression, sturdy healthy legs, nearly
  even loading, unlocked knees, relaxed shoulders, soft elbows, nearly level
  pelvis, neutral lumbar curve, white oversized hoodie, gray pleated skirt,
  two-line white socks, and distinct white chunky left and right sneakers.
  Keep complete hair and shoes in frame. Place the head top at y=65 and the
  soles at y=1456, leaving a 79 px bottom margin. Every head-top and sole
  landmark must remain within 30 px of both accepted anchors; shoulders,
  visual waist, and knees must remain within 3% of canvas height. Treat the
  C01/C02 framing board only as geometry evidence: output one character and
  never reproduce the board, split layout, gutter, ticks, captions, borders,
  collage, grid, split screen, multi-panel, or contact sheet. Use one coherent
  45-degree perspective for face, ribcage, pelvis, legs, skirt, hoodie, socks,
  and shoes. No head-only turn, strong hip shift, fashion pose, locked knees,
  twisted anatomy, thin legs, elongated proportions, mirrored shoes,
  wrong-side or invented accessories, age drift, dramatic lighting,
  photorealistic skin, props, readable text, logo, or watermark. Do not
  amplify the recorded C01 knee-to-foot or C02 sock-height Minor findings.
view_prompts:
  hairpin-side-45: >-
    Show the character-left hairpin side at an exact natural 45-degree view.
    Follow the v1.1 hairpin-side reference for face width, cheek roundness, bob
    silhouette, and correct perspective placement of the parallel pins and
    small pale-blue ribbon. Do not move the accessories to the opposite side.
  non-hairpin-side-45: >-
    Show the opposite non-hairpin side at the matching exact natural
    45-degree view. Preserve the v1.1 opposite cheek and bob silhouette. Keep
    the character-left accessories on their true side; do not mirror,
    duplicate, relocate, or invent them. Match the same pair's hairpin member
    only when it agrees with the controlling C01, C02, and v1.1 references.
pair_generation_policy:
  first_view: hairpin-side-45
  second_view: non-hairpin-side-45
  second_view_additional_reference:
    role: paired_candidate_anchor
    source_view: hairpin-side-45
    priority: supporting
framing_contract:
  canvas:
    width: 1024
    height: 1536
  measurement:
    tool: imagemagick
    fuzz_percent: 6
    geometry_format: "%@"
    head_top_formula: y
    sole_formula: y_plus_height_minus_1
  anchors:
    - asset_id: C01
      revision: r01
      head_top_y: 65
      sole_y: 1450
    - asset_id: C02
      revision: r01
      head_top_y: 65
      sole_y: 1463
  maximum_displacement:
    percent_of_canvas_height: 2
    integer_pixels: 30
  required_intersection:
    head_top_y: [35, 95]
    sole_y: [1433, 1480]
  prompt_target:
    head_top_y: 65
    sole_y: 1456
    bottom_margin_pixels: 79
candidates:
  - variant: a
    title: paired-attempt-a
    outputs:
      - view: hairpin-side-45
        target_path: source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-a.png
      - view: non-hairpin-side-45
        target_path: source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-a.png
  - variant: b
    title: paired-attempt-b
    outputs:
      - view: hairpin-side-45
        target_path: source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-b.png
      - view: non-hairpin-side-45
        target_path: source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-b.png
  - variant: c
    title: paired-attempt-c
    outputs:
      - view: hairpin-side-45
        target_path: source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-c.png
      - view: non-hairpin-side-45
        target_path: source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-c.png
comparison_anchors:
  - accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
  - accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png
acceptance_gates: [identity, body, rendering]
hard_rejects:
  - wrong 45-degree view or head-only turn
  - mirrored substitute or mixed candidate pair
  - identity or age drift
  - elongated proportions or thin legs
  - locked knees, twisted anatomy, or mismatched pair construction
  - wrong-side, missing, duplicated, or invented hair accessories
  - mirrored shoes or incomplete full-body crop
  - readable text, logo, or watermark
```

- [ ] **Step 5: Add ordered contract validation**

Add the exact framing constant before `GENERATION_REQUEST_CONTRACTS`:

```python
C03_R02_FRAMING_CONTRACT = {
    "canvas": {"width": 1024, "height": 1536},
    "measurement": {
        "tool": "imagemagick",
        "fuzz_percent": 6,
        "geometry_format": "%@",
        "head_top_formula": "y",
        "sole_formula": "y_plus_height_minus_1",
    },
    "anchors": [
        {"asset_id": "C01", "revision": "r01", "head_top_y": 65, "sole_y": 1450},
        {"asset_id": "C02", "revision": "r01", "head_top_y": 65, "sole_y": 1463},
    ],
    "maximum_displacement": {
        "percent_of_canvas_height": 2,
        "integer_pixels": 30,
    },
    "required_intersection": {
        "head_top_y": [35, 95],
        "sole_y": [1433, 1480],
    },
    "prompt_target": {
        "head_top_y": 65,
        "sole_y": 1456,
        "bottom_margin_pixels": 79,
    },
}


def ordered_value(value):
    if isinstance(value, dict):
        return tuple((key, ordered_value(item)) for key, item in value.items())
    if isinstance(value, list):
        return tuple(ordered_value(item) for item in value)
    return value
```

Add this complete `("C03", "r02")` contract:

```python
("C03", "r02"): {
    "variation_axis": "paired_generation_attempt",
    "references": (
        (
            "accepted_c01_front_stance",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
        ),
        (
            "accepted_c02_back_stance",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c02_back-natural-stance_r01.png",
        ),
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
    "candidate_prefix": "source/candidates/c03/r02/",
    "candidate_detail": None,
    "output_specs": (
        ("hairpin-side-45", "akari-v1.2_c03_hairpin-side-45_r02"),
        ("non-hairpin-side-45", "akari-v1.2_c03_non-hairpin-side-45_r02"),
    ),
    "comparison_anchors": (
        "accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png",
        "accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png",
    ),
    "pair_generation_policy": {
        "first_view": "hairpin-side-45",
        "second_view": "non-hairpin-side-45",
        "second_view_additional_reference": {
            "role": "paired_candidate_anchor",
            "source_view": "hairpin-side-45",
            "priority": "supporting",
        },
    },
    "view_names": ("hairpin-side-45", "non-hairpin-side-45"),
    "framing_contract": C03_R02_FRAMING_CONTRACT,
},
```

Set `"framing_contract": None` on the three existing request contracts. In `validate_generation_request()`, after pair-policy validation, add:

```python
expected_framing = contract["framing_contract"]
actual_framing = data.get("framing_contract")
if expected_framing is None:
    if "framing_contract" in data:
        raise ValidationError("generation request: unexpected framing contract")
elif ordered_value(actual_framing) != ordered_value(expected_framing):
    raise ValidationError("generation request: exact framing contract required")
```

- [ ] **Step 6: Validate dependencies across every revision**

Replace the asset-ID dictionary in `validate_generation_dependencies()` with request lists and check each C03 request:

```python
def validate_generation_dependencies(assets: dict, requests: list[dict]) -> None:
    assets_by_id = {item["asset_id"]: item for item in assets["assets"]}
    c01 = assets_by_id["C01"]
    c02 = assets_by_id["C02"]

    c02_requests = [item for item in requests if item["asset_id"] == "C02"]
    for request in c02_requests:
        paths = c01.get("accepted_paths")
        expected = (
            f"akari-v1.2/{paths[0]}"
            if isinstance(paths, list) and len(paths) == 1
            else None
        )
        if (
            c01.get("status") not in {"accepted", "accepted-with-notes"}
            or c01.get("revision") != "r01"
            or request["references"][0]["path"] != expected
        ):
            raise ValidationError(
                "C02 requires accepted C01 r01 at its declared anchor"
            )

    c03_requests = [item for item in requests if item["asset_id"] == "C03"]
    expected_anchors = []
    for asset in (c01, c02):
        paths = asset.get("accepted_paths")
        expected_anchors.append(
            f"akari-v1.2/{paths[0]}"
            if isinstance(paths, list) and len(paths) == 1
            else None
        )
    for request in c03_requests:
        if (
            any(
                asset.get("status") not in {"accepted", "accepted-with-notes"}
                or asset.get("revision") != "r01"
                for asset in (c01, c02)
            )
            or [reference["path"] for reference in request["references"][:2]]
            != expected_anchors
        ):
            raise ValidationError(
                "C03 requires accepted C01 and C02 r01 at its declared anchors"
            )
```

- [ ] **Step 7: Validate complete review batches even when all are rejected**

At the start of `validate_lifecycle_linkage()`, group reviews by `(asset_id, revision)`. Before checking accepted assets, require every non-empty batch to match the corresponding request exactly:

```python
reviews_by_key: dict[tuple[str, str], list[dict]] = {}
for review in review_log["reviews"]:
    key = (review["asset_id"], review["revision"])
    reviews_by_key.setdefault(key, []).append(review)

for key, matching in reviews_by_key.items():
    request = requests_by_key.get(key)
    if request is None:
        raise ValidationError(
            f"{key[0]} {key[1]}: reviews require a matching generation request"
        )
    declared = [
        (
            f"{request['asset_id'].lower()}-"
            f"{request['revision']}-{candidate['variant']}",
            candidate_source_paths(candidate),
        )
        for candidate in request["candidates"]
    ]
    actual = [
        (review["candidate_id"], review["source_paths"])
        for review in matching
    ]
    if actual != declared:
        raise ValidationError(
            f"{key[0]} {key[1]}: reviews must match declared "
            f"{key[0]} candidates in order before expected exactly one "
            "accepted review"
        )
```

Then fetch accepted-asset matches with `matching = reviews_by_key.get(asset_key, [])`. Retain exactly-one-accepted enforcement, accepted-file hash verification, and the final accepted-review-to-accepted-asset check.

- [ ] **Step 8: Verify green and commit the r02 contract**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package -v
UV_CACHE_DIR=/tmp/akari-uv-cache npm run validate:v1-2
```

Expected: PASS and summary `4 generation requests with 12 candidate groups and 18 generated outputs, and 9 reviews`.

Commit:

```sh
git add akari-v1.2/manifest/generation-requests/c03-r02.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: define Natural Form C03 r02 framing contract"
```

---

### Task 3: Implement the deterministic C03 landmark audit and r02 commands

**Files:**

- Create: `scripts/audit_v1_2_c03_landmarks.py`
- Create: `tests/test_audit_v1_2_c03_landmarks.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`
- Modify: `package.json`

**Interfaces:**

- Produces: `TrimGeometry`, `Measurement`, `parse_geometry()`, `measure_image()`, `measurement_errors()`, `audit_request()`, and `main()`.
- Consumes: exact `C03_R02_FRAMING_CONTRACT` and ordered r02 outputs.
- Adds npm commands: `audit:v1-2:c03-r02-landmarks`, `build:v1-2:c03-r02-comparison`, and `build:v1-2:c03-r02-alignment-comparison`.

- [ ] **Step 1: Write geometry and boundary tests**

Create `tests/test_audit_v1_2_c03_landmarks.py` starting with:

```python
import copy
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageDraw
import yaml

from scripts.audit_v1_2_c03_landmarks import (
    AuditError,
    Measurement,
    TrimGeometry,
    audit_request,
    main,
    measure_image,
    measurement_errors,
    parse_geometry,
)
from scripts.validate_akari_v1_2_natural_form import C03_R02_FRAMING_CONTRACT


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
BACKGROUND = "#f1f2f1"


def make_figure(path: Path, head: int, sole: int, size=(1024, 1536)) -> None:
    image = Image.new("RGB", size, BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rectangle((320, head, 703, sole), fill="#202124")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


class C03GeometryTests(unittest.TestCase):
    def test_parse_geometry_uses_y_plus_height_minus_one_for_sole(self):
        geometry = parse_geometry("423x1386+300+65")
        self.assertEqual(
            geometry,
            TrimGeometry(width=423, height=1386, x=300, y=65),
        )
        self.assertEqual(geometry.y + geometry.height - 1, 1450)

    def test_30_pixels_passes_and_31_pixels_fails(self):
        contract = copy.deepcopy(C03_R02_FRAMING_CONTRACT)
        anchors = contract["anchors"]
        at_limit = Measurement(1024, 1536, TrimGeometry(400, 1362, 300, 95))
        over_limit = Measurement(1024, 1536, TrimGeometry(400, 1361, 300, 96))
        self.assertEqual(measurement_errors(at_limit, contract, anchors), [])
        self.assertTrue(
            any("31 px" in message for message in measurement_errors(over_limit, contract, anchors))
        )

    def test_intersection_endpoints_are_inclusive(self):
        contract = copy.deepcopy(C03_R02_FRAMING_CONTRACT)
        anchors = contract["anchors"]
        lower = Measurement(1024, 1536, TrimGeometry(400, 1399, 300, 35))
        self.assertEqual(lower.head_top_y, 35)
        self.assertEqual(lower.sole_y, 1433)
        self.assertEqual(measurement_errors(lower, contract, anchors), [])
        outside = Measurement(1024, 1536, TrimGeometry(400, 1399, 300, 34))
        self.assertTrue(
            any("required intersection" in message for message in measurement_errors(outside, contract, anchors))
        )
```

- [ ] **Step 2: Add synthetic request, anchor, and CLI tests**

In the same test file, add a helper that writes exact synthetic anchors and six candidates:

```python
def make_request(root: Path) -> Path:
    make_figure(root / "anchors/c01.png", 65, 1450)
    make_figure(root / "anchors/c02.png", 65, 1463)
    candidates = []
    for variant in ("a", "b", "c"):
        outputs = []
        for view in ("hairpin-side-45", "non-hairpin-side-45"):
            target = Path("candidates") / f"{variant}-{view}.png"
            make_figure(root / target, 65, 1456)
            outputs.append({"view": view, "target_path": target.as_posix()})
        candidates.append({"variant": variant, "outputs": outputs})
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump(
            {
                "references": [
                    {"role": "accepted_c01_front_stance", "path": "anchors/c01.png"},
                    {"role": "accepted_c02_back_stance", "path": "anchors/c02.png"},
                ],
                "framing_contract": copy.deepcopy(C03_R02_FRAMING_CONTRACT),
                "candidates": candidates,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return request


class C03LandmarkAuditTests(unittest.TestCase):
    def test_committed_anchors_match_the_contract(self):
        c01 = measure_image(
            PACKAGE_ROOT
            / "accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png",
            6,
        )
        c02 = measure_image(
            PACKAGE_ROOT
            / "accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png",
            6,
        )
        self.assertEqual((c01.head_top_y, c01.sole_y), (65, 1450))
        self.assertEqual((c02.head_top_y, c02.sole_y), (65, 1463))

    def test_audit_reports_all_six_candidates_in_request_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            lines = audit_request(make_request(root), root)
            candidate_lines = [line for line in lines if line.startswith("PASS candidates/")]
            self.assertEqual(
                [line.split(":", 1)[0].removeprefix("PASS ") for line in candidate_lines],
                [
                    f"candidates/{variant}-{view}.png"
                    for variant in ("a", "b", "c")
                    for view in ("hairpin-side-45", "non-hairpin-side-45")
                ],
            )

    def test_one_out_of_range_member_makes_cli_nonzero_and_names_the_file(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            make_figure(root / "candidates/b-non-hairpin-side-45.png", 96, 1456)
            stderr = StringIO()
            with redirect_stderr(stderr):
                status = main(["--request", str(request), "--package-root", str(root)])
            self.assertEqual(status, 1)
            self.assertIn("b-non-hairpin-side-45.png", stderr.getvalue())
            self.assertIn("31 px", stderr.getvalue())

    def test_wrong_canvas_and_missing_foreground_fail(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            make_figure(root / "candidates/a-hairpin-side-45.png", 65, 1456, (1000, 1536))
            Image.new("RGB", (1024, 1536), BACKGROUND).save(
                root / "candidates/c-non-hairpin-side-45.png"
            )
            with self.assertRaises(AuditError) as caught:
                audit_request(request, root)
            message = str(caught.exception)
            self.assertIn("expected 1024x1536", message)
            self.assertIn("missing foreground", message)
```

- [ ] **Step 3: Run the new module and verify red**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache uv run python -m unittest \
  tests.test_audit_v1_2_c03_landmarks -v
```

Expected: ERROR because `scripts.audit_v1_2_c03_landmarks` does not exist.

- [ ] **Step 4: Implement measurement primitives**

Create `scripts/audit_v1_2_c03_landmarks.py` with these public types and functions:

```python
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

import yaml

if __package__:
    from scripts.validate_akari_v1_2_natural_form import (
        C03_R02_FRAMING_CONTRACT,
        ordered_value,
    )
else:
    from validate_akari_v1_2_natural_form import (
        C03_R02_FRAMING_CONTRACT,
        ordered_value,
    )


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
GEOMETRY_RE = re.compile(
    r"^(?P<width>\d+)x(?P<height>\d+)(?P<x>[+-]\d+)(?P<y>[+-]\d+)$"
)


class AuditError(RuntimeError):
    pass


@dataclass(frozen=True)
class TrimGeometry:
    width: int
    height: int
    x: int
    y: int


@dataclass(frozen=True)
class Measurement:
    canvas_width: int
    canvas_height: int
    trim: TrimGeometry

    @property
    def head_top_y(self) -> int:
        return self.trim.y

    @property
    def sole_y(self) -> int:
        return self.trim.y + self.trim.height - 1


def parse_geometry(value: str) -> TrimGeometry:
    match = GEOMETRY_RE.fullmatch(value.strip())
    if match is None:
        raise AuditError(f"malformed ImageMagick geometry: {value!r}")
    geometry = TrimGeometry(**{key: int(item) for key, item in match.groupdict().items()})
    if geometry.width <= 0 or geometry.height <= 0:
        raise AuditError(f"missing foreground in geometry: {value}")
    return geometry


def measure_image(path: Path, fuzz_percent: int) -> Measurement:
    if not path.is_file():
        raise AuditError(f"missing file: {path}")
    command = [
        "magick",
        "identify",
        "-fuzz",
        f"{fuzz_percent}%",
        "-format",
        "%w %h %@",
        str(path),
    ]
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise AuditError("ImageMagick 'magick' is unavailable") from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip() or "identify failed"
        raise AuditError(f"{path}: {detail}") from error
    parts = completed.stdout.strip().split(maxsplit=2)
    if len(parts) != 3:
        raise AuditError(f"{path}: malformed identify output {completed.stdout!r}")
    try:
        canvas_width, canvas_height = (int(parts[0]), int(parts[1]))
    except ValueError as error:
        raise AuditError(f"{path}: malformed canvas size {parts[:2]!r}") from error
    return Measurement(canvas_width, canvas_height, parse_geometry(parts[2]))
```

- [ ] **Step 5: Implement candidate and anchor audit behavior**

Continue the same file with:

```python
def resolve_package_path(package_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == package_root.name:
        return package_root.parent / path
    return package_root / path


def measurement_errors(
    measurement: Measurement,
    contract: dict,
    anchors: list[dict],
) -> list[str]:
    errors = []
    canvas = contract["canvas"]
    if (measurement.canvas_width, measurement.canvas_height) != (
        canvas["width"],
        canvas["height"],
    ):
        errors.append(
            f"expected {canvas['width']}x{canvas['height']}, got "
            f"{measurement.canvas_width}x{measurement.canvas_height}"
        )
    limit = contract["maximum_displacement"]["integer_pixels"]
    for name, actual, anchor_field in (
        ("head_top_y", measurement.head_top_y, "head_top_y"),
        ("sole_y", measurement.sole_y, "sole_y"),
    ):
        for anchor in anchors:
            delta = abs(actual - anchor[anchor_field])
            if delta > limit:
                errors.append(
                    f"{name}={actual} differs from {anchor['asset_id']} "
                    f"{anchor[anchor_field]} by {delta} px; maximum is {limit} px"
                )
        lower, upper = contract["required_intersection"][name]
        if not lower <= actual <= upper:
            errors.append(
                f"{name}={actual} is outside required intersection [{lower}, {upper}]"
            )
    return errors


def describe(measurement: Measurement, anchors: list[dict]) -> str:
    deltas = ", ".join(
        f"{anchor['asset_id']} head={abs(measurement.head_top_y - anchor['head_top_y'])} "
        f"sole={abs(measurement.sole_y - anchor['sole_y'])}"
        for anchor in anchors
    )
    return (
        f"canvas={measurement.canvas_width}x{measurement.canvas_height} "
        f"head_top_y={measurement.head_top_y} sole_y={measurement.sole_y}; {deltas}"
    )


def audit_request(request_path: Path, package_root: Path) -> list[str]:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise AuditError(f"{request_path}: expected mapping")
    contract = request.get("framing_contract")
    if ordered_value(contract) != ordered_value(C03_R02_FRAMING_CONTRACT):
        raise AuditError("request does not contain the exact C03 r02 framing contract")

    references = request.get("references")
    if not isinstance(references, list) or len(references) < 2:
        raise AuditError("request requires C01 and C02 references first")
    anchor_specs = contract["anchors"]
    fuzz_percent = contract["measurement"]["fuzz_percent"]
    anchor_measurements = []
    anchor_errors = []
    lines = []
    for spec, reference in zip(anchor_specs, references[:2]):
        label = f"anchor {spec['asset_id']} {spec['revision']}"
        path = resolve_package_path(package_root, reference["path"])
        try:
            measurement = measure_image(path, fuzz_percent)
        except AuditError as error:
            anchor_errors.append(f"FAIL {label}: {error}")
            continue
        anchor_measurements.append(measurement)
        expected_canvas = contract["canvas"]
        errors = []
        if (measurement.canvas_width, measurement.canvas_height) != (
            expected_canvas["width"],
            expected_canvas["height"],
        ):
            errors.append(
                f"expected {expected_canvas['width']}x{expected_canvas['height']}, got "
                f"{measurement.canvas_width}x{measurement.canvas_height}"
            )
        if measurement.head_top_y != spec["head_top_y"]:
            errors.append(
                f"head_top_y expected {spec['head_top_y']}, got {measurement.head_top_y}"
            )
        if measurement.sole_y != spec["sole_y"]:
            errors.append(f"sole_y expected {spec['sole_y']}, got {measurement.sole_y}")
        if errors:
            anchor_errors.append(f"FAIL {label}: " + "; ".join(errors))
        else:
            lines.append(f"PASS {label}: {describe(measurement, anchor_specs)}")
    if anchor_errors:
        raise AuditError("\n".join(anchor_errors))

    candidates = request.get("candidates")
    if not isinstance(candidates, list) or [item.get("variant") for item in candidates] != ["a", "b", "c"]:
        raise AuditError("request requires candidates a, b, c in order")
    failures = []
    for candidate in candidates:
        outputs = candidate.get("outputs")
        if not isinstance(outputs, list) or [item.get("view") for item in outputs] != [
            "hairpin-side-45",
            "non-hairpin-side-45",
        ]:
            raise AuditError(f"candidate {candidate.get('variant')} has invalid view order")
        for output in outputs:
            relative = output["target_path"]
            path = resolve_package_path(package_root, relative)
            try:
                measurement = measure_image(path, fuzz_percent)
                errors = measurement_errors(measurement, contract, anchor_specs)
            except AuditError as error:
                failures.append(f"FAIL {relative}: {error}")
                continue
            if errors:
                failures.append(
                    f"FAIL {relative}: {describe(measurement, anchor_specs)}; "
                    + "; ".join(errors)
                )
            else:
                lines.append(f"PASS {relative}: {describe(measurement, anchor_specs)}")
    if failures:
        raise AuditError("\n".join(failures))
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT)
    args = parser.parse_args(argv)
    request = args.request if args.request.is_absolute() else ROOT / args.request
    package_root = (
        args.package_root
        if args.package_root.is_absolute()
        else ROOT / args.package_root
    )
    try:
        lines = audit_request(request, package_root)
    except (AuditError, OSError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Add exact package commands and their contract test**

Add these scripts to `package.json`, retaining both r01 C03 commands unchanged:

```json
"audit:v1-2:c03-r02-landmarks": "uv run python scripts/audit_v1_2_c03_landmarks.py --request akari-v1.2/manifest/generation-requests/c03-r02.yaml --package-root akari-v1.2",
"build:v1-2:c03-r02-comparison": "uv run python scripts/build_v1_2_c03_comparisons.py --request akari-v1.2/manifest/generation-requests/c03-r02.yaml --output akari-v1.2/comparisons/c03-r02/c03-r02-pair-comparison.webp",
"build:v1-2:c03-r02-alignment-comparison": "uv run python scripts/build_v1_2_c03_comparisons.py --request akari-v1.2/manifest/generation-requests/c03-r02.yaml --output akari-v1.2/comparisons/c03-r02/c03-r02-alignment-comparison.webp --alignment"
```

Extend `NaturalFormIsolationTests.test_package_command_reserves_unqualified_v1_2_for_natural_form` with these exact key/value pairs, and include all three names in the `natural_form_commands` allowlist used by `old_unqualified`.

- [ ] **Step 7: Run focused and package verification, then commit**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache uv run python -m unittest \
  tests.test_audit_v1_2_c03_landmarks \
  tests.test_build_v1_2_c03_comparisons \
  tests.test_akari_v1_2_natural_form_package -v
UV_CACHE_DIR=/tmp/akari-uv-cache npm run validate:v1-2
```

Expected: all tests PASS; the production audit command is not expected to pass until all six r02 files exist.

Commit:

```sh
git add package.json scripts/audit_v1_2_c03_landmarks.py \
  tests/test_audit_v1_2_c03_landmarks.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: audit Natural Form C03 r02 framing"
```

---

### Task 4: Build the local framing board and freeze three all-pass r02 pairs

**Files:**

- Modify locally: `.git/info/exclude`
- Create locally: `tmp/akari-v1.2/c03-r02/c01-c02-framing-board.png`
- Create locally: `akari-v1.2/source/candidates/c03/r02/*.png`

**Interfaces:**

- Consumes: immutable accepted C01/C02, three v1.1 visual references, and the exact r02 prompt.
- Produces: three frozen complete pairs for which `npm run audit:v1-2:c03-r02-landmarks` exits zero.

- [ ] **Step 1: Add local exclusions and prove they apply**

Using `apply_patch`, ensure `.git/info/exclude` contains these non-duplicated lines:

```gitignore
akari-v1.2/source/candidates/c03/
akari-v1.2/comparisons/c03-r02/
tmp/akari-v1.2/c03-r02/
```

Run:

```sh
git check-ignore -v akari-v1.2/source/candidates/c03/r02/probe.png
git check-ignore -v akari-v1.2/comparisons/c03-r02/probe.webp
git check-ignore -v tmp/akari-v1.2/c03-r02/probe.png
```

Expected: every path is ignored by `.git/info/exclude` or an existing broader local rule.

- [ ] **Step 2: Build the exact geometry-only framing board**

Run:

```sh
mkdir -p tmp/akari-v1.2/c03-r02
magick \
  akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png \
  \( -size 64x1536 canvas:'#f1f2f1' \
  -fill '#6b7280' \
  -draw 'rectangle 8,64 55,66 rectangle 8,1455 55,1457' \) \
  akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png \
  +append tmp/akari-v1.2/c03-r02/c01-c02-framing-board.png
magick identify -format '%w %h\n' \
  tmp/akari-v1.2/c03-r02/c01-c02-framing-board.png
```

Expected: `2112 1536`.

Crop the left and right accepted-image regions and prove zero changed pixels:

```sh
magick tmp/akari-v1.2/c03-r02/c01-c02-framing-board.png \
  -crop 1024x1536+0+0 +repage tmp/akari-v1.2/c03-r02/board-left.png
magick tmp/akari-v1.2/c03-r02/c01-c02-framing-board.png \
  -crop 1024x1536+1088+0 +repage tmp/akari-v1.2/c03-r02/board-right.png
magick compare -metric AE \
  akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png \
  tmp/akari-v1.2/c03-r02/board-left.png null:
magick compare -metric AE \
  akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png \
  tmp/akari-v1.2/c03-r02/board-right.png null:
```

Expected: both `compare` metrics are `0`.

- [ ] **Step 3: Open and assign roles to the hairpin-call references**

Use `view_image` on these four physical files immediately before each A/B/C hairpin call:

```text
tmp/akari-v1.2/c03-r02/c01-c02-framing-board.png
akari-v1.2/references/v1.1/hairpin-side-45.webp
akari-v1.2/references/v1.1/non-hairpin-side-45.webp
akari-v1.2/references/v1.1/shoes.webp
```

State their roles in the generation prompt:

- board: controlling C01/C02 body scale, outfit, rendering, head y=65, target sole y=1456;
- hairpin view: controlling face, bob, parallel pins, and blue ribbon for the requested side;
- non-hairpin view: opposite-side identity and anti-mirroring evidence;
- shoes: controlling distinct left/right chunky sneaker construction.

- [ ] **Step 4: Restore and freeze the already passing B pair**

Copy the matched B pair from the second local full-round attempt without
re-encoding:

```sh
cp tmp/akari-v1.2/c03-r02/failed-draft-02/akari-v1.2_c03_hairpin-side-45_r02-b.png \
  akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-b.png
cp tmp/akari-v1.2/c03-r02/failed-draft-02/akari-v1.2_c03_non-hairpin-side-45_r02-b.png \
  akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-b.png
```

Measure both files. Expected coordinates are hairpin head 62 / sole 1467 and
non-hairpin head 73 / sole 1450. Stop if either file differs.

- [ ] **Step 5: Generate and gate one complete A pair attempt**

Invoke built-in `imagegen` for the A hairpin output using the exact manifest `shared_prompt` followed by the exact `hairpin-side-45` view prompt. Save the returned PNG as:

```text
akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-a.png
```

Measure the A hairpin output immediately. If it fails, move it into a numbered
local `failed-pair-a-*` directory and restart Step 5 without generating the
non-hairpin member.

If it passes, open that result plus the four files from Step 3. Invoke
`imagegen` for A non-hairpin using the unchanged shared prompt followed by the
exact `non-hairpin-side-45` view prompt. Treat the A hairpin image as supporting
same-pair continuity only and save as:

```text
akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-a.png
```

Measure the non-hairpin output immediately. If it fails, move both A members
into the same numbered `failed-pair-a-*` directory and restart Step 5. If both
pass, freeze both canonical A paths and never overwrite them.

- [ ] **Step 6: Generate and gate one complete C pair attempt**

Repeat Step 5 for C. Do not add variant labels, corrective phrases, seeds, or
candidate-specific wording. A failed C attempt retires both C members together;
it never changes frozen A or B.

If a generated image is visible in Codex but no local PNG is available, structurally parse the current-day rollout for an `image_generation_call` whose `result` starts with `iVBOR`, decode only after verifying PNG signature `89504e470d0a1a0a`, and save the payload to its declared target path. Do not copy a base64 payload through terminal output.

- [ ] **Step 7: Run the six-file hard gate**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache npm run audit:v1-2:c03-r02-landmarks
```

Before the cap, the target is eight PASS lines and exit code 0. After a variant
reaches the cap, a nonzero result is expected only for that final failed pair;
all other frozen pairs must still report PASS at their recorded coordinates.

If it fails, identify the failing variant. Retry only that complete pair while
it remains below the three-attempt cap and never disturb a frozen passing pair.
At the cap, stop generation, keep the final failed pair as local evidence, and
mark that variant ineligible. Continue only if at least one other pair passes.
Compute and retain all six final hashes, including the capped failure:

```sh
sha256sum akari-v1.2/source/candidates/c03/r02/*.png
```

From this point onward, do not overwrite any of the six files.

---

### Task 5: Build comparisons, complete visual review, and obtain selection

**Files:**

- Create locally: `akari-v1.2/comparisons/c03-r02/c03-r02-pair-comparison.webp`
- Create locally: `akari-v1.2/comparisons/c03-r02/c03-r02-alignment-comparison.webp`

**Interfaces:**

- Consumes: frozen passing pairs plus any capped final failed pair.
- Produces: an A/B/C pair verdict table, a recommendation among eligible pairs, and an explicit user selection.

- [ ] **Step 1: Build both comparison sheets through package commands**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache npm run build:v1-2:c03-r02-comparison
UV_CACHE_DIR=/tmp/akari-uv-cache npm run build:v1-2:c03-r02-alignment-comparison
```

Expected outputs:

```text
akari-v1.2/comparisons/c03-r02/c03-r02-pair-comparison.webp
akari-v1.2/comparisons/c03-r02/c03-r02-alignment-comparison.webp
```

- [ ] **Step 2: Review both sheets and all six originals**

Open both comparison sheets and each source PNG. Evaluate every pair in this fixed order:

1. exact side and natural 45-degree direction;
2. identity and 25-year-old age impression;
3. shoulders, visual waist, and knees within 3% of the canvas against C01/C02;
4. within-pair face, body width, pelvis, leg volume, outfit, socks, shoes, perspective, palette, and rendering;
5. anatomy, crop, accessory side, background, artifacts, text, logos, and watermarks.

Record each observed issue with severity, category, affected member, and whether it is resolved. A pair is eligible only when neither member has an unresolved Blocker or Major. A capped machine-gate failure is always ineligible and receives an unresolved Major.

- [ ] **Step 3: Present the evidence and pause for the user**

Show both comparison sheets, the machine-audit measurements, a concise A/B/C
verdict table, and the strongest eligible recommendation. For each comparison
artifact, also provide a copy command in the exact form
`scp conoha:{absolute_image_path} .` so the user can inspect it locally. Ask
for one explicit selection: A, B, or C. If no pair is eligible, record all
three as rejected r02 reviews and stop without promotion; the next generation
request must be r03.

For that no-eligible-pair branch, append the same three ordered r02 records
specified in Task 6 Step 3 with all statuses set to `rejected`, leave C03 at
candidate r00 with no accepted paths, run `npm run validate:v1-2`, and commit
only `review-log.yaml` with message
`docs: reject Natural Form C03 r02 review`. Do not create either accepted r02
file.

---

### Task 6: Promote the selected complete pair and seal r02 lifecycle history

**Files:**

- Create: two selected `akari-v1.2/accepted/core/standing/*_r02.png` files.
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: the explicit user selection, six frozen hashes, and the Task 5 verdicts.
- Produces: exactly one accepted r02 review, two rejected r02 reviews, and two byte-identical accepted files.

- [ ] **Step 1: Copy only the selected pair byte-for-byte**

Use exactly one row from this mapping:

| User choice | Hairpin source | Non-hairpin source |
| --- | --- | --- |
| A | `akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-a.png` | `akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-a.png` |
| B | `akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-b.png` | `akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-b.png` |
| C | `akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_hairpin-side-45_r02-c.png` | `akari-v1.2/source/candidates/c03/r02/akari-v1.2_c03_non-hairpin-side-45_r02-c.png` |

Copy to these fixed destinations without image re-encoding:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png
```

- [ ] **Step 2: Update the C03 asset state**

Change only these fields in the C03 entry of `assets.yaml`:

```yaml
    status: accepted
    revision: r02
    accepted_paths:
      - accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
      - accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png
```

- [ ] **Step 3: Append all three r02 review records in request order**

Use `apply_patch` to append A, B, and C. Copy each pair's two SHA-256 values
directly from the frozen `sha256sum` output in hairpin/non-hairpin order, and
copy its findings and decision directly from the completed Task 5 verdict.
The paths are fixed by this table:

| Candidate | Candidate ID | Ordered source suffixes |
| --- | --- | --- |
| A | `c03-r02-a` | `hairpin-side-45_r02-a.png`, `non-hairpin-side-45_r02-a.png` |
| B | `c03-r02-b` | `hairpin-side-45_r02-b.png`, `non-hairpin-side-45_r02-b.png` |
| C | `c03-r02-c` | `hairpin-side-45_r02-c.png`, `non-hairpin-side-45_r02-c.png` |

Set statuses from exactly one row of this selection table:

| User choice | A status | B status | C status |
| --- | --- | --- | --- |
| A | `accepted` | `rejected` | `rejected` |
| B | `rejected` | `accepted` | `rejected` |
| C | `rejected` | `rejected` | `accepted` |

Every record has `asset_id: C03`, `revision: r02`, two canonical
`source_paths`, two matching lowercase SHA-256 values, a findings list, and a
non-empty decision. The accepted record contains no unresolved Blocker or
Major. Keep all three r01 records unchanged and rejected. Immediately validate
the edit with:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests -v
```

- [ ] **Step 4: Add final-state and negative lifecycle tests**

Add these manifest-backed assertions to `NaturalFormLifecycleTests`:

```python
def test_c03_r02_final_lifecycle_has_one_complete_accepted_pair(self):
    c03 = next(item for item in self.assets["assets"] if item["asset_id"] == "C03")
    self.assertEqual(c03["status"], "accepted")
    self.assertEqual(c03["revision"], "r02")
    self.assertEqual(
        c03["accepted_paths"],
        [
            "accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png",
            "accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png",
        ],
    )
    reviews = [
        review
        for review in self.review_log["reviews"]
        if (review["asset_id"], review["revision"]) == ("C03", "r02")
    ]
    self.assertEqual(
        [review["candidate_id"] for review in reviews],
        ["c03-r02-a", "c03-r02-b", "c03-r02-c"],
    )
    self.assertEqual(
        sum(review["status"] in {"accepted", "accepted-with-notes"} for review in reviews),
        1,
    )
    validate_lifecycle_linkage(
        self.assets,
        self.generation_requests,
        self.review_log,
        PACKAGE_ROOT,
    )
```

Add the complete negative cases:

```python
def test_lifecycle_rejects_corrupted_c03_r02_review_batches(self):
    cases = {}

    missing = copy.deepcopy(self.review_log)
    missing["reviews"] = [
        review
        for review in missing["reviews"]
        if review["candidate_id"] != "c03-r02-b"
    ]
    cases["missing"] = missing

    duplicated = copy.deepcopy(self.review_log)
    duplicate_b = copy.deepcopy(
        next(
            review
            for review in duplicated["reviews"]
            if review["candidate_id"] == "c03-r02-b"
        )
    )
    c_index = next(
        index
        for index, review in enumerate(duplicated["reviews"])
        if review["candidate_id"] == "c03-r02-c"
    )
    duplicated["reviews"][c_index] = duplicate_b
    cases["duplicated"] = duplicated

    reordered = copy.deepcopy(self.review_log)
    b_index = next(
        index
        for index, review in enumerate(reordered["reviews"])
        if review["candidate_id"] == "c03-r02-b"
    )
    c_index = next(
        index
        for index, review in enumerate(reordered["reviews"])
        if review["candidate_id"] == "c03-r02-c"
    )
    reordered["reviews"][b_index], reordered["reviews"][c_index] = (
        reordered["reviews"][c_index],
        reordered["reviews"][b_index],
    )
    cases["reordered"] = reordered

    replaced = copy.deepcopy(self.review_log)
    replaced_a = next(
        review
        for review in replaced["reviews"]
        if review["candidate_id"] == "c03-r02-a"
    )
    replaced_a["candidate_id"] = "c03-r02-arbitrary"
    cases["replaced"] = replaced

    mixed_source = copy.deepcopy(self.review_log)
    mixed_a = next(
        review
        for review in mixed_source["reviews"]
        if review["candidate_id"] == "c03-r02-a"
    )
    mixed_a["source_paths"][0] = (
        "source/candidates/c03/r01/"
        "akari-v1.2_c03_hairpin-side-45_r01-a.png"
    )
    cases["mixed source revision"] = mixed_source

    for name, reviews in cases.items():
        with self.subTest(name=name):
            with self.assertRaisesRegex(
                ValidationError, "reviews must match declared"
            ):
                validate_lifecycle_linkage(
                    self.assets,
                    self.generation_requests,
                    reviews,
                )

def test_lifecycle_rejects_r01_reviews_rekeyed_as_r02(self):
    invalid = copy.deepcopy(self.review_log)
    for review in invalid["reviews"]:
        if (review["asset_id"], review["revision"]) == ("C03", "r01"):
            review["revision"] = "r02"
    with self.assertRaisesRegex(ValidationError, "reviews must match declared"):
        validate_lifecycle_linkage(
            self.assets,
            self.generation_requests,
            invalid,
        )

def test_assets_reject_mixed_revision_c03_accepted_paths(self):
    invalid = copy.deepcopy(self.assets)
    c03 = next(item for item in invalid["assets"] if item["asset_id"] == "C03")
    c03["accepted_paths"][0] = (
        "accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r01.png"
    )
    with self.assertRaisesRegex(ValidationError, "variants and revision"):
        validate_assets(invalid)

def test_lifecycle_rejects_c03_accepted_member_hash_mismatch(self):
    invalid = copy.deepcopy(self.review_log)
    accepted = next(
        review
        for review in invalid["reviews"]
        if (review["asset_id"], review["revision"])
        == ("C03", "r02")
        and review["status"] == "accepted"
    )
    accepted["source_sha256s"][0] = "0" * 64
    with self.assertRaisesRegex(ValidationError, "accepted file SHA-256"):
        validate_lifecycle_linkage(
            self.assets,
            self.generation_requests,
            invalid,
            PACKAGE_ROOT,
        )
```

- [ ] **Step 5: Prove byte identity and run focused validation**

For the selected mapping row, run `cmp` for both source/destination pairs, then run:

```sh
sha256sum \
  akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png \
  akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png
UV_CACHE_DIR=/tmp/akari-uv-cache uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
UV_CACHE_DIR=/tmp/akari-uv-cache npm run validate:v1-2
```

Expected: both `cmp` commands exit 0; the accepted hashes equal the selected review hashes; tests PASS; summary reports 12 reviews.

- [ ] **Step 6: Commit the accepted r02 result**

Before staging, confirm ignored candidates and comparisons do not appear in `git status --short`. Then commit only the durable payload:

```sh
git add akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png \
  akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: accept Natural Form C03 r02 pair"
```

---

### Task 7: Run final branch verification and inspect the durable diff

**Files:**

- Verify: all branch changes from `60418e1` through the final C03 r02 commit.

**Interfaces:**

- Consumes: completed branch and local review artifacts.
- Produces: fresh completion evidence with no staged local artifacts and no unresolved Major in the accepted pair.

- [ ] **Step 1: Reconfirm the selected pair and the capped failure**

Run:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache npm run audit:v1-2:c03-r02-landmarks
```

Expected for this round: A and B retain their recorded passing coordinates;
C non-hairpin fails with head 58 / sole 1356 and remains rejected. Separately
measure both selected A files and require hairpin head 60 / sole 1436 and
non-hairpin head 61 / sole 1440 before checking byte identity.

- [ ] **Step 2: Run the full required verification suite**

Run each command separately so a failure is attributable:

```sh
UV_CACHE_DIR=/tmp/akari-uv-cache npm run test:python
UV_CACHE_DIR=/tmp/akari-uv-cache npm run validate:v1-2
bash -lc 'npm run lint:md'
UV_CACHE_DIR=/tmp/akari-uv-cache npm run audit
git diff --check
```

Expected: every command exits 0. If repo-wide Markdown lint scans unrelated ignored material, also run tracked Markdown lint and report both results rather than hiding the first failure:

```sh
git ls-files -z -- '*.md' | xargs -0 ./node_modules/.bin/markdownlint-cli2
```

- [ ] **Step 3: Inspect lifecycle and artifact invariants**

Run:

```sh
git status --short --branch
git diff --stat 60418e1..HEAD
git diff --name-status 60418e1..HEAD
git log --oneline --decorate 60418e1..HEAD
```

Confirm all of the following from current files, not earlier output:

- four requests, 12 candidate groups, 18 outputs, and 12 reviews;
- three rejected r01 C03 reviews and three ordered r02 reviews;
- exactly one accepted r02 review;
- two accepted r02 files whose hashes match that review;
- no unresolved Blocker or Major in the accepted review;
- no candidate PNG, comparison WebP, board PNG, or failed draft staged or committed;
- clean working tree apart from intentionally retained ignored local review artifacts.

- [ ] **Step 4: Review the complete branch diff inline**

Read every durable diff hunk from `60418e1..HEAD`, focusing on contract ordering, all-revision dependency traversal, lifecycle keying, boundary math, subprocess failures, source/destination hash order, and accidental local-artifact inclusion. Fix any Important or higher finding with a focused regression test, rerun the affected suite, and commit the fix before reporting completion.

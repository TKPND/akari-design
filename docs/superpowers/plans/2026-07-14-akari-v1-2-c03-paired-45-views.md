# Akari v1.2 C03 Paired 45-Degree Views Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, review, and accept one matched pair of C03 Natural Form
45-degree standing views that completes Phase 1.

**Architecture:** Normalize accepted and review paths to ordered lists, add
durable source hashes, then extend the request validator with one paired C03
contract while preserving the C01/C02 single-output contracts. Add a focused
two-layout C03 comparison builder. Generate A/B/C as three independent pairs,
stop for explicit user selection, and promote only one complete pair
byte-for-byte under one revision.

**Tech Stack:** Python 3.11+, PyYAML, Pillow, `unittest`, npm scripts, Codex
`image_gen`, PNG and WebP assets

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-14-akari-v1-2-c03-paired-45-views-design.md`.
- Generate A/B/C as three complete pairs: hairpin-side first, then
  non-hairpin-side with the first member as a supporting sixth reference.
- Use accepted C01, accepted C02, both v1.1 45-degree references, and the v1.1
  shoes reference in that exact order for every first member.
- Open every applicable reference with `view_image` at original detail before
  each generation call and state its role in the prompt.
- Produce six separate 1024 x 1536 PNGs. Never generate a grid, contact sheet,
  split screen, or source image that needs cropping.
- Never mirror one side, mix members from different pairs, or retain one r01
  member in a later r02 pair.
- Treat a Blocker or unresolved Major on either member as rejection of the
  complete pair.
- Keep candidates and comparison WebPs local and uncommitted. Commit durable
  code, manifests, review metadata, and the two selected accepted PNGs only.
- Stop for explicit user selection before promotion.
- Do not change the accepted C01/C02 PNGs or their review decisions.
- Follow red-green-refactor for validator and comparison behavior.

---

## File Map

- `akari-v1.2/manifest/assets.yaml`: ordered accepted paths and C03 dependency.
- `akari-v1.2/manifest/review-log.yaml`: ordered source paths and SHA-256s.
- `akari-v1.2/manifest/generation-requests/c01-r01.yaml`: empty comparison
  anchor list.
- `akari-v1.2/manifest/generation-requests/c02-r01.yaml`: one comparison
  anchor in list form.
- `akari-v1.2/manifest/generation-requests/c03-r01.yaml`: exact paired request.
- `scripts/validate_akari_v1_2_natural_form.py`: schemas, dependencies,
  lifecycle linkage, and durable hash validation.
- `tests/test_akari_v1_2_natural_form_package.py`: request and lifecycle tests.
- `scripts/build_v1_2_c03_comparisons.py`: pair and alignment grids.
- `tests/test_build_v1_2_c03_comparisons.py`: grid order and missing inputs.
- `package.json`: two C03 comparison commands.
- `akari-v1.2/source/candidates/c03/r01/*.png`: six local candidate outputs.
- `akari-v1.2/comparisons/c03-r01/*.webp`: two local review sheets.
- `akari-v1.2/accepted/core/standing/akari-v1.2_c03_*_r01.png`: selected pair.

---

### Task 1: Normalize durable asset and review provenance

**Files:**

- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Replaces: asset `accepted_path: str | None` with
  `accepted_paths: list[str]`.
- Replaces: review `source_path: str` with `source_paths: list[str]`.
- Adds: review `source_sha256s: list[str]` in source-path order.
- Extends: `validate_lifecycle_linkage(assets: dict, generation_requests:
  list[dict], review_log: dict, package_root: Path | None = None) -> None`.

- [ ] **Step 1: Write failing list-schema tests**

Update existing fixtures from scalar path fields to list fields, then add:

```python
def test_assets_use_ordered_accepted_paths(self):
    validate_assets(self.assets, PACKAGE_ROOT)
    for asset in self.assets["assets"]:
        self.assertIsInstance(asset["accepted_paths"], list)
        self.assertNotIn("accepted_path", asset)

def test_assets_reject_accepted_path_count_mismatch(self):
    invalid = copy.deepcopy(self.assets)
    c01 = next(item for item in invalid["assets"] if item["asset_id"] == "C01")
    c01["accepted_paths"] = []
    with self.assertRaisesRegex(ValidationError, "accepted_paths must match"):
        validate_assets(invalid)

def test_reviews_use_ordered_paths_and_hashes(self):
    validate_review_log(self.review_log)
    for review in self.review_log["reviews"]:
        self.assertEqual(len(review["source_paths"]), len(review["source_sha256s"]))
        self.assertNotIn("source_path", review)

def test_review_rejects_invalid_source_hash(self):
    invalid = copy.deepcopy(self.review_log)
    invalid["reviews"][0]["source_sha256s"] = ["not-a-sha256"]
    with self.assertRaisesRegex(ValidationError, "source SHA-256"):
        validate_review_log(invalid)
```

- [ ] **Step 2: Verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
```

Expected: FAIL because manifests and validators still use scalar paths.

- [ ] **Step 3: Migrate `assets.yaml`**

For C01 and C02, replace the scalar field with one-item lists containing the
unchanged paths. For C03 through D01, replace `accepted_path: null` with
`accepted_paths: []`. Keep every status and revision unchanged.

Set the accepted entries exactly as follows:

```yaml
accepted_paths:
  - accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
```

```yaml
accepted_paths:
  - accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png
```

- [ ] **Step 4: Migrate `review-log.yaml` with durable hashes**

Replace every `source_path` with a one-item `source_paths` list and add the
matching one-item `source_sha256s` list. Use these exact existing hashes in
review order:

```text
c01-r01-a 92d669f2c6a965bb091923ca2e68154bb81b23d6741b9317c05962adfc078398
c01-r01-b a977f2798d15f3da9ef0d7720d6f9fc41bd2f84f54f4c8a69908a482596a75c5
c01-r01-c a99ad5f6f1cfe8c8510b3f137ade78705761407c60a10a400461d3bc375aaaef
c02-r01-a f17b3be3550c2089d90d84501052026d8bb905ee5a94280933c749115d1de208
c02-r01-b 53b029befd925f0cc185c150817e2067d588dafea9a5e4b388c876f95b31d098
c02-r01-c db509093d8d58d97e43e42c13572d2c7f7681c7db502feadce200d0b9876d88c
```

Do not change findings, statuses, or decisions.

- [ ] **Step 5: Implement ordered path validation**

Add:

```python
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
```

In `validate_assets`, replace scalar handling with:

```python
accepted_paths = item.get("accepted_paths")
if not isinstance(accepted_paths, list) or not all(
    isinstance(path, str) for path in accepted_paths
):
    raise ValidationError(f"{asset_id}: accepted_paths must be a list")
revision_paths = [
    expected_path.replace("rNN", revision) for expected_path in expected_paths
]
if status in {"accepted", "accepted-with-notes"}:
    if accepted_paths != revision_paths:
        raise ValidationError(
            f"{asset_id}: accepted_paths must match variants and revision"
        )
    if package_root is not None:
        for accepted_path in accepted_paths:
            if not (package_root / accepted_path).is_file():
                raise ValidationError(f"{asset_id}: accepted file does not exist")
elif accepted_paths:
    raise ValidationError(f"{asset_id}: candidate accepted_paths must be empty")
```

In `validate_review_log`, validate each list with:

```python
source_paths = review.get("source_paths")
source_sha256s = review.get("source_sha256s")
if not isinstance(source_paths, list) or not source_paths:
    raise ValidationError(f"{asset_id}: source_paths are required")
if not isinstance(source_sha256s, list) or len(source_sha256s) != len(source_paths):
    raise ValidationError(f"{asset_id}: source SHA-256 count mismatch")
for source_path, source_sha256 in zip(source_paths, source_sha256s):
    parts = PurePosixPath(source_path).parts
    if parts[:2] != ("source", "candidates") or ".." in parts:
        raise ValidationError(f"{asset_id}: canonical candidate source required")
    if not isinstance(source_sha256, str) or not SHA256_RE.fullmatch(source_sha256):
        raise ValidationError(f"{asset_id}: invalid source SHA-256")
```

- [ ] **Step 6: Update lifecycle linkage and hash verification**

Use one list even for current single-output requests:

```python
def candidate_source_paths(candidate: dict) -> list[str]:
    if "outputs" in candidate:
        return [output["target_path"] for output in candidate["outputs"]]
    return [candidate["target_path"]]
```

Build declared review tuples as
`(candidate_id, candidate_source_paths(candidate))`. Compare them with
`(review["candidate_id"], review["source_paths"])`.

Extend the lifecycle signature with `package_root: Path | None = None`. Insert
the following block immediately after verifying that `accepted_matching`
contains exactly one review:

```python
if package_root is not None:
    accepted_review = accepted_matching[0]
    accepted_paths = accepted_assets[asset_key]["accepted_paths"]
    if len(accepted_paths) != len(accepted_review["source_sha256s"]):
        raise ValidationError(f"{asset_id} {revision}: accepted hash count mismatch")
    for accepted_path, expected_hash in zip(
        accepted_paths, accepted_review["source_sha256s"]
    ):
        if sha256_file(package_root / accepted_path) != expected_hash:
            raise ValidationError(
                f"{asset_id} {revision}: accepted file SHA-256 mismatch"
            )
```

Pass `args.package_root` from `main()`. Update all tests and helpers to the list
schema, including arbitrary-path, revision-mismatch, and accepted-review cases.

- [ ] **Step 7: Verify green and commit**

```sh
uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v
npm run validate:v1-2
```

Expected: PASS. The accepted C01/C02 hashes must match their recorded selected
source hashes without requiring ignored candidate files.

```sh
git add akari-v1.2/manifest/assets.yaml akari-v1.2/manifest/review-log.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "refactor: normalize Natural Form asset provenance"
```

---

### Task 2: Add and validate the exact paired C03 request

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/c03-r01.yaml`
- Modify: `akari-v1.2/manifest/generation-requests/c01-r01.yaml`
- Modify: `akari-v1.2/manifest/generation-requests/c02-r01.yaml`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Adds: `GENERATION_REQUEST_CONTRACTS[("C03", "r01")]`.
- Adds: paired `candidate["outputs"]` in fixed view order.
- Normalizes: `comparison_anchors: list[str]` for C01, C02, and C03.
- Requires: accepted C01 r01 and C02 r01 for C03 generation.

- [ ] **Step 1: Write failing paired-request tests**

Load `self.c03` in `NaturalFormGenerationRequestTests`, then add:

```python
def test_c03_request_has_three_ordered_pairs(self):
    validate_generation_request(self.c03)
    self.assertEqual(self.c03["variation_axis"], "paired_generation_attempt")
    self.assertEqual(
        [candidate["variant"] for candidate in self.c03["candidates"]],
        ["a", "b", "c"],
    )
    for candidate in self.c03["candidates"]:
        self.assertEqual(
            [output["view"] for output in candidate["outputs"]],
            ["hairpin-side-45", "non-hairpin-side-45"],
        )

def test_c03_rejects_reordered_outputs(self):
    invalid = copy.deepcopy(self.c03)
    invalid["candidates"][0]["outputs"].reverse()
    with self.assertRaisesRegex(ValidationError, "ordered paired outputs"):
        validate_generation_request(invalid)

def test_c03_rejects_substituted_anchor(self):
    invalid = copy.deepcopy(self.c03)
    invalid["references"][1]["path"] = invalid["references"][0]["path"]
    with self.assertRaisesRegex(ValidationError, "exact reference contract"):
        validate_generation_request(invalid)

def test_c03_requires_accepted_c01_and_c02(self):
    validate_generation_dependencies(self.assets, self.requests)
    invalid = copy.deepcopy(self.assets)
    c02 = next(item for item in invalid["assets"] if item["asset_id"] == "C02")
    c02.update(status="candidate", revision="r00", accepted_paths=[])
    with self.assertRaisesRegex(ValidationError, "C03 requires accepted C01 and C02"):
        validate_generation_dependencies(invalid, self.requests)
```

- [ ] **Step 2: Verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests -v
```

Expected: ERROR because `c03-r01.yaml` and its contract do not exist.

- [ ] **Step 3: Normalize comparison anchor fields**

Replace `comparison_anchor` in the existing requests with:

```yaml
# c01-r01.yaml
comparison_anchors: []
```

```yaml
# c02-r01.yaml
comparison_anchors:
  - accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
```

Update the C01/C02 contract tests before implementing the validator change.

- [ ] **Step 4: Create `c03-r01.yaml`**

```yaml
schema_version: 1
request_id: akari-v1.2-c03-r01
asset_id: C03
revision: r01
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
  on a 1024 x 1536 plain low-contrast portrait canvas. Preserve compact anime
  proportions, stable face and age impression, sturdy healthy legs, nearly
  even loading, unlocked knees, relaxed shoulders, soft elbows, nearly level
  pelvis, neutral lumbar curve, white oversized hoodie, gray pleated skirt,
  two-line white socks, and distinct white chunky left and right sneakers.
  Keep complete hair and shoes in frame. Match C01 and C02 rendering, body
  width, and landmark heights: head top and soles within 2% of canvas height,
  and shoulders, visual waist, and knees within 3%. Use one coherent 45-degree
  perspective for face, ribcage, pelvis, legs, skirt, hoodie, socks, and shoes.
  No head-only turn, strong hip shift, fashion pose, locked knees, twisted
  anatomy, thin legs, elongated proportions, mirrored shoes, wrong-side or
  invented accessories, age drift, dramatic lighting, photorealistic skin,
  props, readable text, logo, watermark, collage, grid, split screen,
  multi-panel, or contact sheet. Do not amplify the recorded C01 knee-to-foot
  or C02 sock-height Minor findings.
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
    duplicate, relocate, or invent them. Match the paired candidate anchor
    only when it agrees with the controlling C01, C02, and v1.1 references.
pair_generation_policy:
  first_view: hairpin-side-45
  second_view: non-hairpin-side-45
  second_view_additional_reference:
    role: paired_candidate_anchor
    source_view: hairpin-side-45
    priority: supporting
candidates:
  - variant: a
    title: paired-attempt-a
    outputs:
      - view: hairpin-side-45
        target_path: source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-a.png
      - view: non-hairpin-side-45
        target_path: source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-a.png
  - variant: b
    title: paired-attempt-b
    outputs:
      - view: hairpin-side-45
        target_path: source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-b.png
      - view: non-hairpin-side-45
        target_path: source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-b.png
  - variant: c
    title: paired-attempt-c
    outputs:
      - view: hairpin-side-45
        target_path: source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-c.png
      - view: non-hairpin-side-45
        target_path: source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-c.png
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

- [ ] **Step 5: Implement the paired contract**

Add C03 to `GENERATION_REQUEST_CONTRACTS` with exact references,
`comparison_anchors`, the exact `pair_generation_policy`, and these output
specifications:

```python
"output_specs": (
    (
        "hairpin-side-45",
        "akari-v1.2_c03_hairpin-side-45_r01",
    ),
    (
        "non-hairpin-side-45",
        "akari-v1.2_c03_non-hairpin-side-45_r01",
    ),
),
```

Set `output_specs: None` on C01/C02. In `validate_generation_request`, retain
the existing `target_path` branch when specs are `None`; otherwise require:

```python
outputs = candidate.get("outputs")
if not isinstance(outputs, list) or [
    output.get("view") for output in outputs
] != [view for view, _ in contract["output_specs"]]:
    raise ValidationError("generation request: ordered paired outputs required")
for output, (view, stem) in zip(outputs, contract["output_specs"]):
    expected = f"source/candidates/c03/r01/{stem}-{variant}.png"
    if output.get("target_path") != expected:
        raise ValidationError("generation request: invalid paired output path")
```

Validate `view_prompts`, `pair_generation_policy`, and
`comparison_anchors == list(contract["comparison_anchors"])` exactly. Require
non-empty strings for both view prompts.

- [ ] **Step 6: Bind C03 to accepted C01 and C02**

Change C03 in `assets.yaml` to `depends_on: [C01, C02]`. Extend dependency
validation so the first two C03 references equal the first accepted path of
C01 and C02 and both assets are `accepted` or `accepted-with-notes` at r01.
Raise:

```text
C03 requires accepted C01 and C02 r01 at its declared anchors
```

- [ ] **Step 7: Add synthetic paired lifecycle tests**

Use a copied asset manifest, request collection, and review log. Mark C03
accepted with two accepted paths and append three C03 pair reviews. Test that:

- three exact pair records pass when one is accepted
- a mixed A/B source list fails
- one source path instead of two fails
- two accepted pair reviews fail
- an unresolved Major in the accepted pair fails
- an accepted-file hash mismatch fails when a temporary package root is used

Use `candidate_source_paths()` so C01/C02 and C03 share lifecycle matching.

- [ ] **Step 8: Verify green and commit**

```sh
uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v
npm run validate:v1-2
```

Expected: PASS and summary text reporting `3 generation requests`, `9 candidate
groups`, and `12 generated outputs`.

Update summary counting so each single candidate contributes one output and
each paired candidate contributes two:

```python
candidate_count = sum(len(request["candidates"]) for request in generation_requests)
output_count = sum(
    len(candidate.get("outputs", [candidate]))
    for request in generation_requests
    for candidate in request["candidates"]
)
```

```sh
git add akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/generation-requests \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: define Natural Form C03 paired contract"
```

---

### Task 3: Build paired and four-direction comparison sheets

**Files:**

- Create: `scripts/build_v1_2_c03_comparisons.py`
- Create: `tests/test_build_v1_2_c03_comparisons.py`
- Modify: `package.json`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Produces: `build_c03_comparison(request_path, package_root, output_path,
  alignment=False) -> Path`.
- Reuses: rendering constants and `load_font` from
  `scripts.build_v1_2_candidate_comparison`.
- Adds: `build:v1-2:c03-comparison` and
  `build:v1-2:c03-alignment-comparison`.

- [ ] **Step 1: Write failing grid tests**

Create a temporary request with A/B/C paired outputs. Use red/green for A,
blue/yellow for B, and magenta/cyan for C. Use black for C01 and white for C02.
Assert:

```python
def test_pair_grid_is_three_rows_by_two_columns(self):
    output = self.root / "pair.webp"
    build_c03_comparison(self.request, self.root, output)
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

def test_alignment_grid_repeats_c01_pair_c02_pair_order(self):
    output = self.root / "alignment.webp"
    build_c03_comparison(self.request, self.root, output, alignment=True)
    with Image.open(output) as image:
        self.assertEqual(image.size, (1300, 1658))
        expected_first_row = ("black", "red", "white", "green")
        for x, color in zip((170, 490, 810, 1130), expected_first_row):
            assert_color_close(self, image.getpixel((x, 260)), color)
```

Add failures for a missing paired output, missing C01 anchor, missing C02
anchor, reordered candidate variants, and reordered view names.

- [ ] **Step 2: Verify red**

```sh
uv run python -m unittest tests.test_build_v1_2_c03_comparisons -v
```

Expected: ERROR because the builder module does not exist.

- [ ] **Step 3: Implement the focused builder**

Use `CARD_SIZE = (300, 480)`, `GAP = 20`, and `LABEL_HEIGHT = 46` from the
existing comparison module. Validate A/B/C and both ordered view names before
opening files.

Implement a private renderer:

```python
def render_grid(rows: list[list[tuple[str, Path]]], output_path: Path) -> Path:
    column_count = len(rows[0])
    row_height = CARD_SIZE[1] + LABEL_HEIGHT
    width = GAP * (column_count + 1) + CARD_SIZE[0] * column_count
    height = GAP * (len(rows) + 1) + row_height * len(rows)
    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    for row_index, row in enumerate(rows):
        for column_index, (label, source) in enumerate(row):
            if not source.is_file():
                raise ValueError(f"missing {source.name}")
            x = GAP + column_index * (CARD_SIZE[0] + GAP)
            y = GAP + row_index * (row_height + GAP)
            draw.rectangle(
                (x, y, x + CARD_SIZE[0], y + row_height),
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
            draw.text(
                (x + 10, y + CARD_SIZE[1] + 13), label, fill=TEXT, font=font
            )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=94)
    return output_path
```

For pair mode, rows contain the two candidate output paths. For alignment
mode, each row is C01 anchor, hairpin output, C02 anchor, non-hairpin output.
Resolve anchors from `request["comparison_anchors"]` under `package_root`.

Add CLI arguments `--request`, `--output`, and `--alignment`. Resolve request
and output from repository root and package paths from `akari-v1.2/`.

- [ ] **Step 4: Add npm commands and isolation assertions**

```json
"build:v1-2:c03-comparison": "uv run python scripts/build_v1_2_c03_comparisons.py --request akari-v1.2/manifest/generation-requests/c03-r01.yaml --output akari-v1.2/comparisons/c03-r01/c03-r01-pair-comparison.webp",
"build:v1-2:c03-alignment-comparison": "uv run python scripts/build_v1_2_c03_comparisons.py --request akari-v1.2/manifest/generation-requests/c03-r01.yaml --output akari-v1.2/comparisons/c03-r01/c03-r01-alignment-comparison.webp --alignment"
```

Add both exact strings to `NaturalFormIsolationTests.natural_form_commands`.

- [ ] **Step 5: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_c03_comparisons \
  tests.test_build_v1_2_candidate_comparison \
  tests.test_build_v1_2_c01_comparison \
  tests.test_akari_v1_2_natural_form_package -v
```

Expected: PASS, including exact grid size and pixel-order tests.

```sh
git add scripts/build_v1_2_c03_comparisons.py \
  tests/test_build_v1_2_c03_comparisons.py \
  tests/test_akari_v1_2_natural_form_package.py package.json
git commit -m "feat: build Natural Form C03 comparisons"
```

---

### Task 4: Verify the generation-ready C03 foundation

**Files:**

- Inspect only: all durable files changed in Tasks 1 through 3.

**Interfaces:**

- Produces: a clean, generation-ready checkpoint before live image calls.

- [ ] **Step 1: Run full verification**

```sh
npm run test:python
npm run validate:v1-2
npm run lint:md
npm run audit
git diff --check
```

Expected: all commands PASS. The validator reports three requests, nine
candidate groups, twelve generated outputs, and six existing reviews.

- [ ] **Step 2: Check repository scope**

```sh
git status --short --branch
git log -4 --oneline
```

Expected: no uncommitted durable changes and the schema, request, and builder
commits are present.

No commit for this task.

---

### Task 5: Generate the three locked C03 pairs

**Files:**

- Create locally: `akari-v1.2/source/candidates/c03/r01/*.png` (six files)
- Create locally: `akari-v1.2/comparisons/c03-r01/*.webp` (two files)

**Interfaces:**

- Consumes: exact request manifest, five base references, and one dynamic
  within-pair supporting reference for each second member.
- Produces: A/B/C paired PNGs and both review sheets.

- [ ] **Step 1: Invoke and follow the `imagegen` skill**

Use built-in image generation. Do not use the CLI fallback. Treat each PNG as
a project-bound identity-preserving generated asset and persist it to its exact
declared target path.

- [ ] **Step 2: Open and label the five base references**

Use `view_image` at original detail for:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png
akari-v1.2/references/v1.1/hairpin-side-45.webp
akari-v1.2/references/v1.1/non-hairpin-side-45.webp
akari-v1.2/references/v1.1/shoes.webp
```

State the exact roles from the request manifest. Keep all five visible in the
conversation context.

- [ ] **Step 3: Generate pair A**

Call `image_gen` once for A hairpin-side using the five base reference paths,
the exact shared prompt, and the exact hairpin-side view prompt. Save to the
declared A hairpin path and inspect it at original detail.

Open that saved A hairpin candidate plus the five base references. Call
`image_gen` once for A non-hairpin-side using all six paths, the same shared
prompt, and the exact non-hairpin-side view prompt. Explicitly label the A
hairpin image as `paired_candidate_anchor` with supporting priority. Save to the
declared A non-hairpin path and inspect it.

- [ ] **Step 4: Generate pairs B and C identically**

Repeat Step 3 with the B target paths and then the C target paths. Do not add a
candidate-specific pose, style, expression, palette, or quality variation.
Only the independent model attempt differs.

- [ ] **Step 5: Rescue a missing local PNG only when necessary**

If an image appears in the UI but no local PNG exists, structurally parse the
current day's rollout JSONL. Select the matching `image_generation_call` whose
`result` starts with `iVBOR`, base64-decode it, verify the decoded bytes begin
with PNG signature `89504e470d0a1a0a`, and write only that payload to the
declared target. Never copy a large payload through terminal output.

- [ ] **Step 6: Verify all six sources and build comparisons**

```sh
identify akari-v1.2/source/candidates/c03/r01/*.png
npm run build:v1-2:c03-comparison
npm run build:v1-2:c03-alignment-comparison
identify akari-v1.2/comparisons/c03-r01/*.webp
```

Expected: exactly six 1024 x 1536 PNGs, one 660 x 1658 pair WebP, and one
1300 x 1658 alignment WebP.

- [ ] **Step 7: Keep generated work local**

Run `git status --short`. If C03 generated paths appear, add only these
local exclusions to `.git/info/exclude`:

```text
/akari-v1.2/source/candidates/c03/
/akari-v1.2/comparisons/c03-r01/
```

Do not change committed `.gitignore` and do not commit this task.

---

### Task 6: Review all pairs and stop for user selection

**Files:**

- Inspect: six candidates, both comparisons, C01, C02, and both v1.1 45 views.
- Do not modify: `assets.yaml` or `review-log.yaml` before selection.

**Interfaces:**

- Produces: concrete findings for A/B/C, one recommendation, six SHA-256s, and
  an explicit user selection gate.

- [ ] **Step 1: Open both review sheets and all six full-resolution PNGs**

Use `view_image` at original detail for individual anatomy and accessory checks.
Use the two WebPs for within-pair and four-direction comparison.

- [ ] **Step 2: Review in the fixed order**

For each pair, record:

1. exact view direction and true accessory side
2. C01/C02/v1.1 identity and age impression
3. head/sole 2% and shoulder/waist/knee 3% tolerances
4. face width, cheeks, ribcage, pelvis, leg volume, skirt, hoodie, socks, shoes,
   and perspective consistency
5. crop, palette, rendering, anatomy, artifacts, text, logo, and watermark

Reject a complete pair when either member has a Blocker or unresolved Major.

- [ ] **Step 3: Record concrete hashes**

```sh
sha256sum akari-v1.2/source/candidates/c03/r01/*.png
```

Keep the six exact lowercase digests with the review findings. They become the
three ordered `source_sha256s` pairs in Task 7.

- [ ] **Step 4: Recommend and stop**

Recommend the strongest eligible pair by identity, cross-view consistency,
anatomy, and finished quality. Show clickable paths to both WebPs. Ask the user
to select A/B/C or reject the round. Do not promote or edit manifests yet.

If no pair is eligible, stop this plan. Preserve local files, report the shared
failure pattern, and create an r02 design and plan with a revised shared prompt.
Do not patch one r01 member or retain the other member.

No commit for this task.

---

### Task 7: Promote the selected pair and close the C03 lifecycle

**Files:**

- Create: `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r01.png`
- Create: `akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r01.png`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: explicit A/B/C selection, Task 6 findings, and six source hashes.
- Produces: two byte-identical accepted PNGs, three pair reviews, and a closed
  paired lifecycle.

- [ ] **Step 1: Write the failing accepted-state test**

```python
def test_c03_acceptance_links_both_assets_to_one_pair_review(self):
    c03 = next(item for item in self.assets["assets"] if item["asset_id"] == "C03")
    self.assertEqual(c03["status"], "accepted")
    self.assertEqual(c03["revision"], "r01")
    self.assertEqual(
        c03["accepted_paths"],
        [
            "accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r01.png",
            "accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r01.png",
        ],
    )
    accepted = [
        review
        for review in self.review_log["reviews"]
        if review["asset_id"] == "C03" and review["status"] == "accepted"
    ]
    self.assertEqual(len(accepted), 1)
    self.assertEqual(len(accepted[0]["source_paths"]), 2)
    self.assertEqual(len(accepted[0]["source_sha256s"]), 2)
    validate_lifecycle_linkage(
        self.assets,
        self.generation_requests,
        self.review_log,
        PACKAGE_ROOT,
    )
```

- [ ] **Step 2: Verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
```

Expected: FAIL because C03 remains `candidate`, r00, with no review records.

- [ ] **Step 3: Promote exactly the selected pair**

Set `variant` to the user's exact lowercase selection (`a`, `b`, or `c`), then:

```sh
hairpin_source="akari-v1.2/source/candidates/c03/r01/akari-v1.2_c03_hairpin-side-45_r01-${variant}.png"
non_hairpin_source="akari-v1.2/source/candidates/c03/r01/akari-v1.2_c03_non-hairpin-side-45_r01-${variant}.png"
hairpin_accepted="akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r01.png"
non_hairpin_accepted="akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r01.png"
cp "$hairpin_source" "$hairpin_accepted"
cp "$non_hairpin_source" "$non_hairpin_accepted"
cmp "$hairpin_source" "$hairpin_accepted"
cmp "$non_hairpin_source" "$non_hairpin_accepted"
sha256sum "$hairpin_source" "$hairpin_accepted" \
  "$non_hairpin_source" "$non_hairpin_accepted"
```

Expected: both `cmp` commands exit 0 and each source/destination hash pair
matches.

- [ ] **Step 4: Update the asset and all three pair reviews**

Set C03 to:

```yaml
status: accepted
revision: r01
accepted_paths:
  - accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r01.png
  - accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r01.png
```

Append C03 A/B/C reviews in request order. Every record uses one pair candidate
ID, the exact two declared source paths, the exact two Task 6 hashes, concrete
observed findings, and a concrete decision. Mark only the user-selected pair
`accepted`; mark both unselected pairs `rejected`. The accepted record must have
no unresolved Blocker or Major.

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

Expected: all commands PASS. The validator reports three requests, nine
candidate groups, twelve generated outputs, and nine reviews.

- [ ] **Step 6: Verify scope and commit**

Re-run both `cmp` commands and inspect the manifest diffs. Confirm candidates
and comparisons remain unstaged.

```sh
git status --short
git diff --stat
git diff -- akari-v1.2/manifest/assets.yaml akari-v1.2/manifest/review-log.yaml
git add \
  akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r01.png \
  akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r01.png \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: accept Natural Form C03 paired views"
```

- [ ] **Step 7: Post-commit verification**

```sh
npm run validate:v1-2
npm run test:python
npm run lint:md
git status --short --branch
```

Expected: validation and tests remain green; the branch is clean apart from
locally excluded C03 candidates and comparisons. C03 is accepted at r01 and
C04 is the next blocked asset that has now become eligible for planning.

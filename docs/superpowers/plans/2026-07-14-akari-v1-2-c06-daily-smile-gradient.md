# Akari v1.2 C06 Daily Smile Gradient Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, generate, review, and accept one four-image C06 r01 set that
moves the same just-awake Akari from sleepy neutral to a soft closed-mouth smile
without changing identity, composition, hair, outfit, lighting, or backdrop.

**Architecture:** Add one immutable v1.1 expression-range snapshot, one C06
generation request with two generated candidate families and explicit
four-source `review_sets`, and one thin four-column comparison builder. C06
request validation is specialized for inactive, targeted-stage, and full-family
repair modes, while lifecycle validation reads C06 `review_sets` and leaves all
other assets on their existing candidate-based path. Every C06 image is a
direct identity-preserving edit of accepted C05; no C06 output feeds another.

**Tech Stack:** Python 3.13, PyYAML, Pillow, `unittest`, npm scripts, built-in
`image_gen`, ImageMagick inspection, Git.

## Global Constraints

- Work only in `/path/to/akari-design/.worktrees/codex-c06-expression-gradient`
  on branch `codex/c06-expression-gradient`, based on local `main` commit
  `740c390`.
- Treat the approved design at
  `docs/superpowers/specs/2026-07-14-akari-v1-2-c06-daily-smile-gradient-design.md`
  as authoritative.
- Use accepted C05 as the direct edit source for every C06 call. Never use a
  generated C06 image as another stage's input.
- Use exactly four visible references in this order: accepted C05 edit source,
  accepted C01 identity cross-check, accepted C03 hairpin-side cross-check, and
  the canonical v1.1 expression-range snapshot.
- Reopen all four references at original detail immediately before every image
  generation call and state each role in the prompt.
- Preserve C05 composition, crop, head angle, bed hair, ornament, white hoodie,
  backdrop, lighting, rendering, face width, cheeks, chin, base eye shape, and
  adult age impression.
- Allow changes only to upper-eyelid opening, lower-eyelid roundness, pupil
  focus, brow height and angle, mouth corners, and cheek relaxation.
- Generate complete A and B families first: four standalone images per family,
  eight initial calls total, each on an exact 1024 x 1536 canvas.
- Treat each `image_gen` result as the end of that agent turn. Emit no prose or
  follow-up tool call after the generated image; on the next user continuation,
  verify the saved file before opening references for the next declared slot.
- Treat exact dimensions as a production gate. Preserve a wrong-size output as
  local review evidence; never resize it into compliance.
- Keep `repair_lane.mode: inactive` until A/B review proves that targeted-stage
  or full-family C is required. Validate and commit the activated contract
  before any C call.
- Permit at most one targeted C stage. If multiple stages or global invariants
  fail, generate a complete C family. Never perform several isolated repairs.
- Review and accept a complete ordered four-image set only. Never partially
  accept C06.
- Persist stage clarity and gradient continuity findings under existing review
  category `state`; do not add new review category enum values.
- Promote only after an explicit user selection. The assistant's ranking is not
  authorization to copy accepted files.
- Prove each accepted PNG is byte-identical to its selected source with `cmp`
  and matching lowercase SHA-256.
- Keep candidate PNGs, comparison WebPs, and review crops local-only. Stage
  durable paths explicitly; never use `git add -A`.
- Preserve the main workspace's existing local-only C04, C05, and C07 review
  artifacts. Do not reference, modify, stage, or delete them.
- Do not use direct paths under `legacy/akari-v1.2-pre-natural-form/`.
- Follow red-green-refactor for request, dependency, lifecycle, and comparison
  behavior. Commit after each independently testable task.
- Do not patch, mask, warp, blend, mirror, resize, or mechanically composite
  generated candidates.
- Do not push `main` or the feature branch.

---

## File Map

### Durable files created

- `akari-v1.2/references/v1.1/expression-grid.webp` — immutable expression-range
  reference snapshot.
- `akari-v1.2/manifest/generation-requests/c06-r01.yaml` — C06 generation,
  repair, candidate, and review-set contract.
- `scripts/build_v1_2_c06_comparison.py` — two- or three-row by four-column
  review builder.
- `tests/test_build_v1_2_c06_comparison.py` — comparison order and failure
  tests.
- Four selected PNGs under `akari-v1.2/accepted/core/face-hair/` after user
  selection.

### Durable files modified

- `akari-v1.2/manifest/inheritance.yaml` — expression snapshot provenance and
  SHA-256.
- `akari-v1.2/manifest/assets.yaml` — C06 accepted r01 state after selection.
- `akari-v1.2/manifest/review-log.yaml` — complete ordered C06 set reviews after
  selection or round closure.
- `scripts/validate_akari_v1_2_natural_form.py` — request, repair, dependency,
  lifecycle, D01 gate, and inheritance contracts.
- `tests/test_akari_v1_2_natural_form_package.py` — request, dependency,
  lifecycle, provenance, final-state, and package-command tests.
- `package.json` — `build:v1-2:c06-comparison` command.

### Local-only files

- `akari-v1.2/source/candidates/c06/r01/*.png`
- `akari-v1.2/comparisons/c06-r01/c06-r01-comparison.webp`
- `tmp/c06-review/` if enlarged review crops are needed

---

### Task 1: Add the immutable C06 expression-range snapshot

**Files:**

- Create: `akari-v1.2/references/v1.1/expression-grid.webp`
- Modify: `akari-v1.2/manifest/inheritance.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py:938-986`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:1765-1821`

**Interfaces:**

- Consumes: immutable `source/originals/v1_1_front_3.webp` and
  `validate_inheritance(data, repository_root, package_root) -> None`.
- Produces: one byte-identical `reference-only` snapshot with role
  `v1.1-expression-range`, exact digest, and a validated total of sixteen
  Natural Form references.

- [ ] **Step 1: Write the failing exact-provenance test**

Add to `NaturalFormInheritanceTests`:

```python
def test_c06_expression_grid_has_exact_provenance_and_hash(self):
    records = {record["role"]: record for record in self.data["references"]}
    self.assertEqual(
        records.get("v1.1-expression-range"),
        {
            "role": "v1.1-expression-range",
            "inheritance_class": "reference-only",
            "source_path": "source/originals/v1_1_front_3.webp",
            "copied_path": (
                "akari-v1.2/references/v1.1/expression-grid.webp"
            ),
            "source_collection": "v1.1",
            "reuse_rationale": (
                "C06 neutral relaxed-mouth and closed-mouth soft-smile "
                "mechanics only; open-mouth laughing surprised worried "
                "pouting yawning and closed-eye examples are excluded and "
                "grant no identity crop rendering hair outfit or background "
                "authority"
            ),
            "sha256": (
                "2b70c639b320275cde6787263bd6fe0f88ad59068154e4c2439ae"
                "69502e6f919"
            ),
        },
    )
```

- [ ] **Step 2: Run the focused test and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormInheritanceTests.test_c06_expression_grid_has_exact_provenance_and_hash -v
```

Expected: FAIL because role `v1.1-expression-range` is absent.

- [ ] **Step 3: Copy the snapshot byte-for-byte**

```sh
cp -- \
  source/originals/v1_1_front_3.webp \
  akari-v1.2/references/v1.1/expression-grid.webp
cmp --silent -- \
  source/originals/v1_1_front_3.webp \
  akari-v1.2/references/v1.1/expression-grid.webp
sha256sum \
  source/originals/v1_1_front_3.webp \
  akari-v1.2/references/v1.1/expression-grid.webp
```

Expected: `cmp` exits 0 and both digests are
`2b70c639b320275cde6787263bd6fe0f88ad59068154e4c2439ae69502e6f919`.

- [ ] **Step 4: Append the exact provenance record**

Append to `akari-v1.2/manifest/inheritance.yaml`:

```yaml
  - role: v1.1-expression-range
    inheritance_class: reference-only
    source_path: source/originals/v1_1_front_3.webp
    copied_path: akari-v1.2/references/v1.1/expression-grid.webp
    source_collection: v1.1
    reuse_rationale: C06 neutral relaxed-mouth and closed-mouth soft-smile mechanics only; open-mouth laughing surprised worried pouting yawning and closed-eye examples are excluded and grant no identity crop rendering hair outfit or background authority
    sha256: 2b70c639b320275cde6787263bd6fe0f88ad59068154e4c2439ae69502e6f919
```

- [ ] **Step 5: Raise the exact inheritance count**

Change the start of `validate_inheritance` to:

```python
references = data.get("references")
if not isinstance(references, list) or len(references) != 16:
    raise ValidationError("inheritance: expected 16 references")
```

- [ ] **Step 6: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormInheritanceTests -v
bash -lc 'npm run validate:v1-2'
git add \
  akari-v1.2/references/v1.1/expression-grid.webp \
  akari-v1.2/manifest/inheritance.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: add Natural Form C06 expression reference"
```

Expected: inheritance tests and validator pass with sixteen references.

---

### Task 2: Add the exact C06 generation and repair contract

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/c06-r01.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py:27-416,432-554`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:284-818,819-857`

**Interfaces:**

- Consumes: the ordered four-reference contract, C06 stage descriptors, and
  existing `candidate_source_paths(candidate: dict) -> list[str]`.
- Produces: `validate_c06_generation_request(data: dict, contract: dict) -> None`,
  exact inactive/targeted/full repair states, two initial families, explicit
  `review_sets`, and repair-aware generation counts.

- [ ] **Step 1: Add failing request fixtures and tests**

Add the live request and a canonical inactive synthetic fixture to
`NaturalFormGenerationRequestTests.setUp`:

```python
self.c06 = load_yaml(
    PACKAGE_ROOT / "manifest/generation-requests/c06-r01.yaml"
)
self.c06_inactive = inactive_c06_request(self.c06)
```

Add these reusable helpers above `NaturalFormGenerationRequestTests`:

```python
C06_STAGE_PAIRS = (
    ("c06-1", "sleepy-neutral"),
    ("c06-2", "sleepy-secure"),
    ("c06-3", "loosened-mouth"),
    ("c06-4", "soft-smile"),
)


def c06_candidate_path(stage_index: int, variant: str) -> str:
    stage, descriptor = C06_STAGE_PAIRS[stage_index]
    return (
        "source/candidates/c06/r01/"
        f"akari-v1.2_{stage}_{descriptor}_r01-{variant}.png"
    )


def make_c06_family(variant: str) -> dict:
    return {
        "variant": variant,
        "title": f"complete-family-{variant}",
        "outputs": [
            {
                "stage": stage,
                "descriptor": descriptor,
                "edit_source_role": "accepted_c05_edit_source",
                "target_path": c06_candidate_path(index, variant),
            }
            for index, (stage, descriptor) in enumerate(C06_STAGE_PAIRS)
        ],
    }


def inactive_c06_request(request: dict) -> dict:
    updated = copy.deepcopy(request)
    updated["candidates"] = updated["candidates"][:2]
    updated["repair_lane"] = {"mode": "inactive"}
    updated["review_sets"] = updated["review_sets"][:2]
    return updated


def targeted_c06_request(request: dict, base: str, stage_index: int) -> dict:
    updated = inactive_c06_request(request)
    stage, _ = C06_STAGE_PAIRS[stage_index]
    target = c06_candidate_path(stage_index, "c")
    updated["repair_lane"] = {
        "mode": "targeted-stage",
        "base_family": base,
        "stage": stage,
        "target_path": target,
    }
    family = next(
        candidate for candidate in updated["candidates"]
        if candidate["variant"] == base
    )
    sources = candidate_source_paths(family)
    sources[stage_index] = target
    updated["review_sets"].append(
        {
            "candidate_id": f"c06-r01-{base}-repair-{stage}",
            "source_paths": sources,
        }
    )
    return updated


def full_family_c06_request(request: dict) -> dict:
    updated = inactive_c06_request(request)
    updated["repair_lane"] = {"mode": "full-family"}
    family = make_c06_family("c")
    updated["candidates"].append(family)
    updated["review_sets"].append(
        {
            "candidate_id": "c06-r01-c",
            "source_paths": candidate_source_paths(family),
        }
    )
    return updated
```

Add request tests:

```python
def test_c06_live_request_is_valid_in_its_committed_repair_mode(self):
    validate_generation_request(self.c06)


def test_c06_inactive_contract_declares_exact_families_and_review_sets(self):
    validate_generation_request(self.c06_inactive)
    self.assertEqual(
        [
            candidate["variant"]
            for candidate in self.c06_inactive["candidates"]
        ],
        ["a", "b"],
    )
    self.assertEqual(
        self.c06_inactive["repair_lane"], {"mode": "inactive"}
    )
    self.assertEqual(
        [item["candidate_id"] for item in self.c06_inactive["review_sets"]],
        ["c06-r01-a", "c06-r01-b"],
    )
    for candidate, review_set in zip(
        self.c06_inactive["candidates"],
        self.c06_inactive["review_sets"],
    ):
        self.assertEqual(
            [output["stage"] for output in candidate["outputs"]],
            [stage for stage, _ in C06_STAGE_PAIRS],
        )
        self.assertEqual(
            [output["descriptor"] for output in candidate["outputs"]],
            [descriptor for _, descriptor in C06_STAGE_PAIRS],
        )
        self.assertEqual(
            review_set["source_paths"],
            candidate_source_paths(candidate),
        )
    self.assertEqual(
        self.c06_inactive["acceptance_gates"],
        ["identity", "state", "rendering"],
    )


def test_c06_targeted_stage_repair_is_one_literal_mixed_set(self):
    request = targeted_c06_request(
        self.c06_inactive, base="a", stage_index=2
    )
    validate_generation_request(request)
    repaired = request["review_sets"][-1]
    self.assertEqual(
        repaired["candidate_id"], "c06-r01-a-repair-c06-3"
    )
    self.assertEqual(
        [path.rsplit("-", 1)[-1] for path in repaired["source_paths"]],
        ["a.png", "a.png", "c.png", "a.png"],
    )


def test_c06_full_family_repair_declares_complete_c(self):
    request = full_family_c06_request(self.c06_inactive)
    validate_generation_request(request)
    self.assertEqual(
        [candidate["variant"] for candidate in request["candidates"]],
        ["a", "b", "c"],
    )
    self.assertEqual(
        [item["candidate_id"] for item in request["review_sets"]],
        ["c06-r01-a", "c06-r01-b", "c06-r01-c"],
    )


def test_c06_repair_modes_reject_undeclared_or_mixed_attempts(self):
    cases = {}

    inactive_with_c = copy.deepcopy(self.c06_inactive)
    inactive_with_c["candidates"].append(make_c06_family("c"))
    cases["inactive with C family"] = inactive_with_c

    targeted_plus_full = targeted_c06_request(
        self.c06_inactive, base="a", stage_index=2
    )
    targeted_plus_full["candidates"].append(make_c06_family("c"))
    cases["targeted plus full C"] = targeted_plus_full

    two_c_sources = targeted_c06_request(
        self.c06_inactive, base="a", stage_index=2
    )
    two_c_sources["review_sets"][-1]["source_paths"][1] = (
        c06_candidate_path(1, "c")
    )
    cases["two targeted C sources"] = two_c_sources

    partial_c = full_family_c06_request(self.c06_inactive)
    partial_c["candidates"][-1]["outputs"].pop()
    cases["partial C family"] = partial_c

    reordered_sets = copy.deepcopy(self.c06_inactive)
    reordered_sets["review_sets"].reverse()
    cases["reordered review sets"] = reordered_sets

    for name, invalid in cases.items():
        with self.subTest(name=name):
            with self.assertRaisesRegex(
                ValidationError, "C06 .*contract|C06 .*repair"
            ):
                validate_generation_request(invalid)


def test_c06_rejects_changed_shared_or_stage_prompt(self):
    cases = {}
    changed_shared = copy.deepcopy(self.c06_inactive)
    changed_shared["shared_prompt"] += " Redesign the hair."
    cases["shared"] = changed_shared

    changed_stage = copy.deepcopy(self.c06_inactive)
    changed_stage["stages"][2]["prompt_delta"] += " Change the outfit."
    cases["stage"] = changed_stage

    for name, invalid in cases.items():
        with self.subTest(name=name):
            with self.assertRaisesRegex(
                ValidationError, "C06 exact .* prompt contract"
            ):
                validate_generation_request(invalid)
```

Update `NaturalFormGenerationCollectionTests` request-order expectation to
include `("C06", "r01")` between C05 and C07. Replace the fixed count assertion
with a live-mode-aware assertion, then add the synthetic repair count test:

```python
def test_generation_counts_distinguish_groups_from_outputs(self):
    c06 = next(
        item
        for item in self.requests
        if (item["asset_id"], item["revision"]) == ("C06", "r01")
    )
    expected_by_mode = {
        "inactive": (22, 36),
        "targeted-stage": (22, 37),
        "full-family": (23, 40),
    }
    self.assertEqual(
        count_generation_work(self.requests),
        expected_by_mode[c06["repair_lane"]["mode"]],
    )


def test_c06_repair_modes_have_exact_generation_counts(self):
    live_c06 = next(
        item
        for item in self.requests
        if (item["asset_id"], item["revision"]) == ("C06", "r01")
    )
    c06 = inactive_c06_request(live_c06)
    cases = (
        (targeted_c06_request(c06, base="a", stage_index=2), (22, 37)),
        (full_family_c06_request(c06), (23, 40)),
    )
    for replacement, expected in cases:
        requests = [
            replacement
            if (item["asset_id"], item["revision"]) == ("C06", "r01")
            else item
            for item in self.requests
        ]
        with self.subTest(mode=replacement["repair_lane"]["mode"]):
            self.assertEqual(count_generation_work(requests), expected)
```

- [ ] **Step 2: Run request tests and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests -v
```

Expected: ERROR for missing `c06-r01.yaml`, then FAIL for unsupported C06 until
the validator contract is added.

- [ ] **Step 3: Create the exact initial request**

Create `akari-v1.2/manifest/generation-requests/c06-r01.yaml`:

```yaml
schema_version: 1
request_id: akari-v1.2-c06-r01
asset_id: C06
revision: r01
variation_axis: expression_gradient_family_attempt
references:
  - role: accepted_c05_edit_source
    path: akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
  - role: accepted_c01_identity_crosscheck
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
  - role: accepted_c03_hairpin_three_quarter
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
  - role: v1_1_expression_range
    path: akari-v1.2/references/v1.1/expression-grid.webp
edit_policy:
  source_role: accepted_c05_edit_source
  mode: direct-from-source-per-stage
  chained_c06_outputs: forbidden
shared_prompt: >-
  Use the four visible images only in their declared roles. Edit Image 1
  directly to create one standalone chest-up 1024 x 1536 portrait of the same
  naturally cute 25-year-old Akari. Image 1 is the controlling accepted C05
  edit source for composition, crop, near-eye-level front-biased light
  three-quarter camera, head angle, reversible morning hair, complete
  character-left ornament, white oversized hoodie, warm off-white backdrop,
  soft diffuse near-neutral lighting, rendering, and sleepy-neutral baseline.
  Image 2 is a controlling rejection cross-check for adult identity, healthy
  face width, rounded cheeks, compact chin, base eye construction, warm amber
  eyes, palette, and hoodie only; do not copy its full-body pose or intentionally
  reshape the C05 face. Image 3 is a controlling rejection cross-check for the
  ornament, cheek silhouette, and short-bob side construction only; do not copy
  its full-body pose or replace C05 morning-hair irregularity. Image 4 is a
  non-controlling expression-range reference for neutral lips, relaxed mouth,
  and a small closed-mouth soft smile only; do not copy its grid, panel-specific
  face geometry, open-mouth expressions, extreme emotions, crop, or rendering.
  Preserve the exact C05 crown lifts, lightly separated bangs, partial nape
  flick, lower-bob irregularity, cheek-side strand, short-bob length, part,
  color, side volume, ornament placement, shoulders, neckline, upper chest,
  crop, backdrop, lighting, and rendering. Preserve C05 face width, cheek
  volume, chin, nose, ear placement, iris size, base eye shape, and adult age;
  C01 and C03 reject further narrowing or sharpening but do not authorize a
  face redesign. Change only upper-eyelid opening, lower-eyelid roundness, pupil
  focus, brow height and angle, mouth corners, and cheek relaxation according
  to the one supplied stage delta. No hands, props, furniture, bed, window,
  room scene, head tilt, outfit change, stronger blush, text, logo, watermark,
  border, grid, collage, multiple composition, or multiple character.
stages:
  - stage: c06-1
    descriptor: sleepy-neutral
    prompt_delta: >-
      Stay closest to accepted C05. Keep slightly heavy upper eyelids without
      materially shrinking the eyes, a softly unfocused viewer-directed gaze,
      relaxed brows, and closed lips in a neutral line. Show no smile, sadness,
      distress, pout, yawn, or sensual emphasis. Change no non-expression
      property.
  - stage: c06-2
    descriptor: sleepy-secure
    prompt_delta: >-
      Preserve nearly the same eyelid weight and low-energy gaze as C06-1.
      Soften only the brow angle, lower eyelids, and cheek tension enough to read
      as safe and comfortable rather than blank. Keep the mouth closed and
      almost neutral; do not use a visible smile as the primary difference or
      jump to alertness. Change no non-expression property.
  - stage: c06-3
    descriptor: loosened-mouth
    prompt_delta: >-
      Preserve the secure sleepy eyes and relaxed brows of C06-2. Let the closed
      mouth relax and lift only minimally at both corners, with slight cheek
      relaxation that does not narrow the face or become a full smile. Read as
      the beginning of warmth, not the final smile. Change no non-expression
      property.
  - stage: c06-4
    descriptor: soft-smile
    prompt_delta: >-
      Make a clearly readable but small closed-mouth everyday smile, coordinating
      both mouth corners, lower eyelids, brows, and cheeks while retaining
      just-awake softness. No teeth, open mouth, closed eyes, laughter, strong
      blush, grin, head tilt, extra pose, or full-alert performance. Change no
      non-expression property.
framing_guidance:
  canvas: {width: 1024, height: 1536}
  enforcement: advisory
  crop: chest-up-below-hoodie-neckline-and-upper-chest
  intended_top_breathing_room_pixels: 70
  intended_lateral_hair_margin_pixels: 60
  face_placement: vertical-upper-middle
  required_visible_features:
    - complete-crown-and-outer-hair-silhouette
    - complete-character-left-ornament
    - both-eyes-face-outline-cheek-strand-and-lower-bob-ends
    - shoulders-hoodie-neckline-and-upper-chest
  reject_on_numeric_miss_alone: false
  major_only_when: crop-or-scale-prevents-complete-face-hair-sequence-review
production_requirements:
  file_format: png
  canvas: {width: 1024, height: 1536}
  standalone_composition: true
  generated_grid: forbidden
candidates:
  - variant: a
    title: complete-family-a
    outputs:
      - stage: c06-1
        descriptor: sleepy-neutral
        edit_source_role: accepted_c05_edit_source
        target_path: source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-a.png
      - stage: c06-2
        descriptor: sleepy-secure
        edit_source_role: accepted_c05_edit_source
        target_path: source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-a.png
      - stage: c06-3
        descriptor: loosened-mouth
        edit_source_role: accepted_c05_edit_source
        target_path: source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-a.png
      - stage: c06-4
        descriptor: soft-smile
        edit_source_role: accepted_c05_edit_source
        target_path: source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-a.png
  - variant: b
    title: complete-family-b
    outputs:
      - stage: c06-1
        descriptor: sleepy-neutral
        edit_source_role: accepted_c05_edit_source
        target_path: source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-b.png
      - stage: c06-2
        descriptor: sleepy-secure
        edit_source_role: accepted_c05_edit_source
        target_path: source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-b.png
      - stage: c06-3
        descriptor: loosened-mouth
        edit_source_role: accepted_c05_edit_source
        target_path: source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-b.png
      - stage: c06-4
        descriptor: soft-smile
        edit_source_role: accepted_c05_edit_source
        target_path: source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-b.png
repair_lane:
  mode: inactive
review_sets:
  - candidate_id: c06-r01-a
    source_paths:
      - source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-a.png
      - source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-a.png
      - source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-a.png
      - source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-a.png
  - candidate_id: c06-r01-b
    source_paths:
      - source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-b.png
      - source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-b.png
      - source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-b.png
      - source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-b.png
comparison_anchors: []
acceptance_gates: [identity, state, rendering]
hard_rejects:
  - severe identity age face-shape chin or base-eye drift
  - progressively narrower face sharper chin younger age or larger doll-like eyes
  - corrupted asymmetric duplicated or disconnected facial features
  - missing mirrored relocated duplicated or redesigned ornament
  - material crop head-angle hairstyle outfit backdrop lighting palette or rendering drift
  - indistinguishable reversed or abrupt expression-stage progression
  - sleepiness shown mainly through closed or substantially shrunken eyes
  - sadness distress pout intoxication illness sensuality or strong-blush drift
  - yawn teeth open mouth laughter performative grin or extra pose
  - wrong dimensions corrupt file or unreadable complete face-and-hair crop
  - readable text logo watermark border grid collage or multiple character
```

- [ ] **Step 4: Add the specialized validator contract**

Add constants near the existing framing contracts:

```python
C06_R01_STAGE_PAIRS = (
    ("c06-1", "sleepy-neutral"),
    ("c06-2", "sleepy-secure"),
    ("c06-3", "loosened-mouth"),
    ("c06-4", "soft-smile"),
)
C06_R01_EDIT_POLICY = {
    "source_role": "accepted_c05_edit_source",
    "mode": "direct-from-source-per-stage",
    "chained_c06_outputs": "forbidden",
}
C06_R01_PRODUCTION_REQUIREMENTS = {
    "file_format": "png",
    "canvas": {"width": 1024, "height": 1536},
    "standalone_composition": True,
    "generated_grid": "forbidden",
}
C06_R01_FRAMING_GUIDANCE = {
    "canvas": {"width": 1024, "height": 1536},
    "enforcement": "advisory",
    "crop": "chest-up-below-hoodie-neckline-and-upper-chest",
    "intended_top_breathing_room_pixels": 70,
    "intended_lateral_hair_margin_pixels": 60,
    "face_placement": "vertical-upper-middle",
    "required_visible_features": [
        "complete-crown-and-outer-hair-silhouette",
        "complete-character-left-ornament",
        "both-eyes-face-outline-cheek-strand-and-lower-bob-ends",
        "shoulders-hoodie-neckline-and-upper-chest",
    ],
    "reject_on_numeric_miss_alone": False,
    "major_only_when": (
        "crop-or-scale-prevents-complete-face-hair-sequence-review"
    ),
}
C06_R01_STAGE_REQUIRED_PHRASES = {
    "c06-1": ("closest to accepted C05", "closed lips in a neutral line"),
    "c06-2": ("safe and comfortable rather than blank", "almost neutral"),
    "c06-3": ("lift only minimally", "beginning of warmth"),
    "c06-4": ("small closed-mouth everyday smile", "No teeth, open mouth"),
}
C06_R01_EXACT_PROMPT_SHA256 = {
    "shared": "1d5ede16c4593085ec749f759c0fde8fc721eacc6665e1e1a8c80a2f9dc72fb1",
    "c06-1": "fa7829f275839abd49986d7d0011f66dafede5364144a99915d742eadccd951f",
    "c06-2": "c5c4c8a29038c9a5d98bcafe3512bc6c95f6610545934a0fa5df29cf6d731c29",
    "c06-3": "160b4e1a3cb4299273bf3f1f96a9be1154dd38f50bad203ae20909814d33b282",
    "c06-4": "3498b3310cf0cd2ff48918bbf8b47780107667414ccb78e204a7f001fed0dd12",
}
```

Add `("C06", "r01")` to `GENERATION_REQUEST_CONTRACTS` with the exact four
references, framing, gates, prompt phrases, and hard rejects from the YAML:

```python
("C06", "r01"): {
    "variation_axis": "expression_gradient_family_attempt",
    "references": (
        (
            "accepted_c05_edit_source",
            "akari-v1.2/accepted/core/face-hair/"
            "akari-v1.2_c05_morning-bedhair_r01.png",
        ),
        (
            "accepted_c01_identity_crosscheck",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
        ),
        (
            "accepted_c03_hairpin_three_quarter",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c03_hairpin-side-45_r02.png",
        ),
        (
            "v1_1_expression_range",
            "akari-v1.2/references/v1.1/expression-grid.webp",
        ),
    ),
    "comparison_anchors": (),
    "framing_contract": None,
    "framing_guidance": C06_R01_FRAMING_GUIDANCE,
    "acceptance_gates": ("identity", "state", "rendering"),
    "required_prompt_phrases": (
        "Edit Image 1 directly",
        "Image 1 is the controlling accepted C05 edit source",
        "do not intentionally reshape the C05 face",
        "non-controlling expression-range reference",
        "Preserve C05 face width",
        "Change only upper-eyelid opening",
        "No hands, props, furniture, bed, window, room scene",
    ),
    "hard_rejects": (
        "severe identity age face-shape chin or base-eye drift",
        "progressively narrower face sharper chin younger age or larger doll-like eyes",
        "corrupted asymmetric duplicated or disconnected facial features",
        "missing mirrored relocated duplicated or redesigned ornament",
        "material crop head-angle hairstyle outfit backdrop lighting palette or rendering drift",
        "indistinguishable reversed or abrupt expression-stage progression",
        "sleepiness shown mainly through closed or substantially shrunken eyes",
        "sadness distress pout intoxication illness sensuality or strong-blush drift",
        "yawn teeth open mouth laughter performative grin or extra pose",
        "wrong dimensions corrupt file or unreadable complete face-and-hair crop",
        "readable text logo watermark border grid collage or multiple character",
    ),
},
```

Add the dedicated validator before `validate_generation_request`:

```python
def c06_candidate_path(stage: str, descriptor: str, variant: str) -> str:
    return (
        "source/candidates/c06/r01/"
        f"akari-v1.2_{stage}_{descriptor}_r01-{variant}.png"
    )


def validate_c06_generation_request(data: dict, contract: dict) -> None:
    stages = data.get("stages")
    if not isinstance(stages, list) or [
        (item.get("stage"), item.get("descriptor")) for item in stages
    ] != list(C06_R01_STAGE_PAIRS):
        raise ValidationError("C06 stage contract mismatch")
    if any(
        set(item) != {"stage", "descriptor", "prompt_delta"}
        or not isinstance(item["prompt_delta"], str)
        or not all(
            phrase in item["prompt_delta"]
            for phrase in C06_R01_STAGE_REQUIRED_PHRASES[item["stage"]]
        )
        for item in stages
    ):
        raise ValidationError("C06 stage prompt contract mismatch")
    actual_stage_hashes = {
        item["stage"]: hashlib.sha256(
            item["prompt_delta"].encode("utf-8")
        ).hexdigest()
        for item in stages
    }
    if actual_stage_hashes != {
        stage: C06_R01_EXACT_PROMPT_SHA256[stage]
        for stage, _ in C06_R01_STAGE_PAIRS
    }:
        raise ValidationError("C06 exact stage prompt contract mismatch")
    if data.get("edit_policy") != C06_R01_EDIT_POLICY:
        raise ValidationError("C06 edit policy contract mismatch")
    if data.get("production_requirements") != C06_R01_PRODUCTION_REQUIREMENTS:
        raise ValidationError("C06 production contract mismatch")

    repair = data.get("repair_lane")
    if not isinstance(repair, dict):
        raise ValidationError("C06 repair contract mismatch")
    mode = repair.get("mode")
    expected_variants = ["a", "b", "c"] if mode == "full-family" else ["a", "b"]
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or [
        candidate.get("variant") for candidate in candidates
    ] != expected_variants:
        raise ValidationError("C06 candidate family contract mismatch")

    expected_sets = []
    sources_by_variant = {}
    for variant, candidate in zip(expected_variants, candidates):
        if set(candidate) != {"variant", "title", "outputs"}:
            raise ValidationError("C06 candidate family contract mismatch")
        if candidate.get("title") != f"complete-family-{variant}":
            raise ValidationError("C06 candidate family contract mismatch")
        expected_outputs = [
            {
                "stage": stage,
                "descriptor": descriptor,
                "edit_source_role": "accepted_c05_edit_source",
                "target_path": c06_candidate_path(stage, descriptor, variant),
            }
            for stage, descriptor in C06_R01_STAGE_PAIRS
        ]
        if candidate.get("outputs") != expected_outputs:
            raise ValidationError("C06 candidate output contract mismatch")
        sources_by_variant[variant] = [
            output["target_path"] for output in expected_outputs
        ]
        if variant in {"a", "b"}:
            expected_sets.append(
                {
                    "candidate_id": f"c06-r01-{variant}",
                    "source_paths": sources_by_variant[variant],
                }
            )

    if mode == "inactive":
        if repair != {"mode": "inactive"}:
            raise ValidationError("C06 inactive repair contract mismatch")
    elif mode == "targeted-stage":
        base = repair.get("base_family")
        stage = repair.get("stage")
        if base not in {"a", "b"} or stage not in {
            item[0] for item in C06_R01_STAGE_PAIRS
        }:
            raise ValidationError("C06 targeted repair contract mismatch")
        stage_index = [item[0] for item in C06_R01_STAGE_PAIRS].index(stage)
        descriptor = C06_R01_STAGE_PAIRS[stage_index][1]
        target = c06_candidate_path(stage, descriptor, "c")
        if repair != {
            "mode": "targeted-stage",
            "base_family": base,
            "stage": stage,
            "target_path": target,
        }:
            raise ValidationError("C06 targeted repair contract mismatch")
        mixed = list(sources_by_variant[base])
        mixed[stage_index] = target
        expected_sets.append(
            {
                "candidate_id": f"c06-r01-{base}-repair-{stage}",
                "source_paths": mixed,
            }
        )
    elif mode == "full-family":
        if repair != {"mode": "full-family"}:
            raise ValidationError("C06 full repair contract mismatch")
        expected_sets.append(
            {
                "candidate_id": "c06-r01-c",
                "source_paths": sources_by_variant["c"],
            }
        )
    else:
        raise ValidationError("C06 repair contract mismatch")

    if data.get("review_sets") != expected_sets:
        raise ValidationError("C06 review set contract mismatch")

    if data.get("comparison_anchors") != []:
        raise ValidationError("C06 comparison anchors mismatch")
    if "framing_contract" in data:
        raise ValidationError("C06 unexpected framing contract")
    if ordered_value(data.get("framing_guidance")) != ordered_value(
        contract["framing_guidance"]
    ):
        raise ValidationError("C06 exact framing guidance required")
    shared_prompt = data.get("shared_prompt")
    if not isinstance(shared_prompt, str) or not shared_prompt.strip():
        raise ValidationError("C06 shared prompt required")
    if any(
        phrase not in shared_prompt
        for phrase in contract["required_prompt_phrases"]
    ):
        raise ValidationError("C06 required prompt phrase missing")
    if hashlib.sha256(shared_prompt.encode("utf-8")).hexdigest() != (
        C06_R01_EXACT_PROMPT_SHA256["shared"]
    ):
        raise ValidationError("C06 exact shared prompt contract mismatch")
    if data.get("acceptance_gates") != list(contract["acceptance_gates"]):
        raise ValidationError("C06 acceptance gates mismatch")
    if data.get("hard_rejects") != list(contract["hard_rejects"]):
        raise ValidationError("C06 exact hard rejects required")
```

In `validate_generation_request`, insert this branch immediately after the
exact-reference equality check and before the existing `candidates =
data.get("candidates")` line:

```python
if key == ("C06", "r01"):
    validate_c06_generation_request(data, contract)
    return
```

The early return is valid because the dedicated helper performs C06's complete
candidate, review-set, comparison-anchor, framing, shared-prompt,
acceptance-gate, and hard-reject validation. Keep the existing standard
candidate/view and common-field validation literally in place for every
non-C06 request.

- [ ] **Step 5: Make generation counts repair-aware**

Replace `count_generation_work` with:

```python
def count_generation_work(requests: list[dict]) -> tuple[int, int]:
    candidate_count = sum(len(request["candidates"]) for request in requests)
    output_count = sum(
        len(candidate.get("outputs", [candidate]))
        for request in requests
        for candidate in request["candidates"]
    )
    for request in requests:
        repair = request.get("repair_lane")
        if isinstance(repair, dict) and repair.get("mode") == "targeted-stage":
            output_count += 1
    return candidate_count, output_count
```

Initial C06 reports `(22, 36)`, targeted repair reports `(22, 37)`, and full C
reports `(23, 40)`.

- [ ] **Step 6: Run focused and package validation tests**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests -v
bash -lc 'npm run validate:v1-2'
```

Expected: request and collection tests pass; validator reports eight assets,
sixteen references, eight generation requests, twenty-two candidate groups,
thirty-six generated outputs, and the current twenty reviews.

- [ ] **Step 7: Commit the request contract**

```sh
git add \
  akari-v1.2/manifest/generation-requests/c06-r01.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: add Natural Form C06 generation contract"
```

---

### Task 3: Enforce C05 dependency and C06 review-set lifecycle

**Files:**

- Modify: `scripts/validate_akari_v1_2_natural_form.py:556-748,818-929`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:81-185,941-1118,1119-1764`

**Interfaces:**

- Consumes: C06 `review_sets`, accepted C05 r01, existing assets/reviews, and
  `candidate_source_paths(candidate) -> list[str]`.
- Produces: `declared_review_pairs(request: dict) -> list[tuple[str,
  list[str]]]`, strict C05 dependency checks, strict C06 release status, D01
  C06 gate, and lifecycle linkage for complete or mixed four-image sets.

- [ ] **Step 1: Write failing dependency and release tests**

Add to `NaturalFormGenerationDependencyTests`:

```python
def test_c06_declares_only_c05_dependency(self):
    c06 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C06"
    )
    self.assertEqual(c06["depends_on"], ["C05"])


def test_c06_requires_strict_accepted_c05_r01_at_exact_edit_source(self):
    for mutation in ("status", "revision", "path", "dependency"):
        with self.subTest(mutation=mutation):
            assets = copy.deepcopy(self.assets)
            requests = copy.deepcopy(self.requests)
            c05 = next(
                item for item in assets["assets"]
                if item["asset_id"] == "C05"
            )
            c06 = next(
                item for item in requests if item["asset_id"] == "C06"
            )
            c06_asset = next(
                item for item in assets["assets"]
                if item["asset_id"] == "C06"
            )
            if mutation == "status":
                c05["status"] = "accepted-with-notes"
            elif mutation == "revision":
                c05["revision"] = "r02"
            elif mutation == "path":
                c06["references"][0]["path"] = (
                    "akari-v1.2/accepted/substitute.png"
                )
            else:
                c06_asset["depends_on"] = ["C01", "C05"]
            with self.assertRaisesRegex(
                ValidationError, "C06 requires accepted C05 r01"
            ):
                validate_generation_dependencies(assets, requests)
```

Add to `NaturalFormManifestTests`:

```python
def test_c06_rejects_accepted_with_notes(self):
    invalid = copy.deepcopy(self.assets)
    c06 = next(
        item for item in invalid["assets"] if item["asset_id"] == "C06"
    )
    c06.update(
        status="accepted-with-notes",
        revision="r01",
        accepted_paths=[
            path.replace("rNN", "r01") for path in c06["expected_paths"]
        ],
    )
    with self.assertRaisesRegex(
        ValidationError, "C06: accepted-with-notes is not allowed"
    ):
        validate_assets(invalid)


def test_d01_acceptance_requires_complete_accepted_c06(self):
    invalid = copy.deepcopy(self.assets)
    d01 = next(
        item for item in invalid["assets"] if item["asset_id"] == "D01"
    )
    d01.update(
        status="accepted",
        revision="r01",
        accepted_paths=[
            path.replace("rNN", "r01") for path in d01["expected_paths"]
        ],
    )
    with self.assertRaisesRegex(
        ValidationError, "D01 acceptance requires accepted C06"
    ):
        validate_assets(invalid)
```

Replace the existing
`test_c06_accepted_statuses_require_strict_c05_acceptance` method with the
singular accepted-state case below. The new dedicated
`test_c06_rejects_accepted_with_notes` owns the rejected status path, so the
earlier C05-dependency assertion cannot mask the stricter C06 status error:

```python
def test_c06_acceptance_requires_strict_c05_acceptance(self):
    invalid = copy.deepcopy(self.assets)
    c05 = next(
        item for item in invalid["assets"] if item["asset_id"] == "C05"
    )
    c05.update(status="candidate", revision="r00", accepted_paths=[])
    c06 = next(
        item for item in invalid["assets"] if item["asset_id"] == "C06"
    )
    c06.update(
        status="accepted",
        revision="r01",
        accepted_paths=[
            path.replace("rNN", "r01") for path in c06["expected_paths"]
        ],
    )
    with self.assertRaisesRegex(
        ValidationError, "C06 acceptance requires accepted C05"
    ):
        validate_assets(invalid)
```

- [ ] **Step 2: Add the failing synthetic lifecycle helper and tests**

Add above `NaturalFormLifecycleTests`:

```python
def accepted_c06_lifecycle(
    assets: dict,
    generation_requests: list[dict],
    review_log: dict,
    request: dict,
    accepted_id: str,
):
    updated_assets = copy.deepcopy(assets)
    c06 = next(
        item for item in updated_assets["assets"]
        if item["asset_id"] == "C06"
    )
    c06.update(
        status="accepted",
        revision="r01",
        accepted_paths=[
            path.replace("rNN", "r01") for path in c06["expected_paths"]
        ],
    )
    updated_requests = [
        copy.deepcopy(request)
        if (item["asset_id"], item["revision"]) == ("C06", "r01")
        else copy.deepcopy(item)
        for item in generation_requests
    ]
    updated_reviews = copy.deepcopy(review_log)
    updated_reviews["reviews"] = [
        review for review in updated_reviews["reviews"]
        if (review["asset_id"], review["revision"]) != ("C06", "r01")
    ]
    for index, review_set in enumerate(request["review_sets"], start=1):
        updated_reviews["reviews"].append(
            {
                "asset_id": "C06",
                "revision": "r01",
                "candidate_id": review_set["candidate_id"],
                "status": (
                    "accepted"
                    if review_set["candidate_id"] == accepted_id
                    else "rejected"
                ),
                "source_paths": copy.deepcopy(review_set["source_paths"]),
                "source_sha256s": [f"{index:064x}"] * 4,
                "findings": [],
                "decision": f"Synthetic C06 set decision {index}.",
            }
        )
    return updated_assets, updated_requests, updated_reviews
```

In `NaturalFormLifecycleTests.setUp`, load the live request and derive the same
canonical inactive synthetic fixture:

```python
self.c06 = next(
    item
    for item in self.generation_requests
    if (item["asset_id"], item["revision"]) == ("C06", "r01")
)
self.c06_inactive = inactive_c06_request(self.c06)
```

Then add:

```python
def test_c06_lifecycle_accepts_initial_review_sets(self):
    assets, requests, reviews = accepted_c06_lifecycle(
        self.assets,
        self.generation_requests,
        self.review_log,
        self.c06_inactive,
        "c06-r01-a",
    )
    validate_review_log(reviews)
    validate_lifecycle_linkage(assets, requests, reviews)


def test_c06_targeted_repair_matches_review_sets_not_candidates(self):
    request = targeted_c06_request(
        self.c06_inactive, base="a", stage_index=2
    )
    assets, requests, reviews = accepted_c06_lifecycle(
        self.assets,
        self.generation_requests,
        self.review_log,
        request,
        "c06-r01-a-repair-c06-3",
    )
    validate_review_log(reviews)
    validate_lifecycle_linkage(assets, requests, reviews)


def test_c06_lifecycle_accepts_complete_c_family(self):
    request = full_family_c06_request(self.c06_inactive)
    assets, requests, reviews = accepted_c06_lifecycle(
        self.assets,
        self.generation_requests,
        self.review_log,
        request,
        "c06-r01-c",
    )
    validate_review_log(reviews)
    validate_lifecycle_linkage(assets, requests, reviews)


def test_c06_lifecycle_rejects_changed_review_sets(self):
    cases = {}
    request = targeted_c06_request(
        self.c06_inactive, base="a", stage_index=2
    )
    assets, requests, reviews = accepted_c06_lifecycle(
        self.assets,
        self.generation_requests,
        self.review_log,
        request,
        "c06-r01-a-repair-c06-3",
    )

    missing = copy.deepcopy(reviews)
    missing["reviews"] = [
        item for item in missing["reviews"]
        if item["candidate_id"] != "c06-r01-b"
    ]
    cases["missing"] = missing

    reordered = copy.deepcopy(reviews)
    c06_reviews = [
        index for index, item in enumerate(reordered["reviews"])
        if item["asset_id"] == "C06"
    ]
    left, right = c06_reviews[0], c06_reviews[1]
    reordered["reviews"][left], reordered["reviews"][right] = (
        reordered["reviews"][right], reordered["reviews"][left]
    )
    cases["reordered"] = reordered

    replaced = copy.deepcopy(reviews)
    selected = next(
        item for item in replaced["reviews"]
        if item["candidate_id"] == "c06-r01-a-repair-c06-3"
    )
    selected["source_paths"][2] = c06_candidate_path(2, "b")
    cases["replaced path"] = replaced

    for name, invalid in cases.items():
        with self.subTest(name=name):
            with self.assertRaisesRegex(
                ValidationError,
                "reviews must match declared C06 review sets in order",
            ):
                validate_lifecycle_linkage(assets, requests, invalid)
```

- [ ] **Step 3: Run the focused classes and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
```

Expected: dependency, accepted-with-notes, and D01-gate tests fail; the targeted
lifecycle test fails because current linkage still derives reviews from
`candidates`.

- [ ] **Step 4: Enforce the strict C05 dependency**

In `validate_generation_dependencies`, define `c06 = assets_by_id["C06"]` and
add:

```python
c06_requests = [item for item in requests if item["asset_id"] == "C06"]
c05_paths = c05.get("accepted_paths")
expected_c06_source = (
    f"akari-v1.2/{c05_paths[0]}"
    if isinstance(c05_paths, list) and len(c05_paths) == 1
    else None
)
for request in c06_requests:
    if (
        c06.get("depends_on") != ["C05"]
        or (c05.get("status"), c05.get("revision")) != ("accepted", "r01")
        or request["references"][0]["path"] != expected_c06_source
    ):
        raise ValidationError(
            "C06 requires accepted C05 r01 at its declared edit source"
        )
```

- [ ] **Step 5: Add C06 review-set linkage without changing other assets**

Add beside `candidate_source_paths`:

```python
def declared_review_pairs(request: dict) -> list[tuple[str, list[str]]]:
    if (request["asset_id"], request["revision"]) == ("C06", "r01"):
        return [
            (item["candidate_id"], item["source_paths"])
            for item in request["review_sets"]
        ]
    return [
        (
            f"{request['asset_id'].lower()}-"
            f"{request['revision']}-{candidate['variant']}",
            candidate_source_paths(candidate),
        )
        for candidate in request["candidates"]
    ]
```

Replace the existing local list comprehension assigned to `declared` in
`validate_lifecycle_linkage` with:

```python
declared = declared_review_pairs(request)
actual = [
    (review["candidate_id"], review["source_paths"])
    for review in matching
]
if actual != declared:
    noun = "review sets" if key == ("C06", "r01") else "candidates"
    raise ValidationError(
        f"{key[0]} {key[1]}: reviews must match declared "
        f"{key[0]} {noun} in order before expected exactly one "
        "accepted review"
    )
```

- [ ] **Step 6: Enforce strict C06 and D01 status gates**

In `validate_assets`, replace the C05-only status check with:

```python
if asset_id in {"C05", "C06"} and status == "accepted-with-notes":
    raise ValidationError(
        f"{asset_id}: accepted-with-notes is not allowed"
    )
```

After building `assets_by_id`, retain the existing C06/C05 gate and add:

```python
if (
    assets_by_id["D01"]["status"] in {"accepted", "accepted-with-notes"}
    and assets_by_id["C06"]["status"] != "accepted"
):
    raise ValidationError("D01 acceptance requires accepted C06")
```

- [ ] **Step 7: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
git add \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: validate Natural Form C06 lifecycle"
```

Expected: focused tests pass; all pre-existing non-C06 lifecycle tests remain
green without changing their declared candidate behavior.

---

### Task 4: Add the C06 four-stage comparison command

**Files:**

- Create: `scripts/build_v1_2_c06_comparison.py`
- Create: `tests/test_build_v1_2_c06_comparison.py`
- Modify: `package.json:19-21`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:1843-1944`
- Reuse unchanged: `scripts/build_v1_2_c03_comparisons.py::render_grid`

**Interfaces:**

- Consumes: ordered `stages`, literal `review_sets[].source_paths`, and
  `render_grid(rows: list[list[tuple[str, Path]]], output_path: Path) -> Path`.
- Produces: `build_c06_comparison(request_path: Path, package_root: Path,
  output_path: Path) -> Path` and npm command `build:v1-2:c06-comparison`.

- [ ] **Step 1: Write the failing builder tests**

Create `tests/test_build_v1_2_c06_comparison.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import copy
import unittest

from PIL import Image, ImageColor
import yaml

from scripts.build_v1_2_c06_comparison import build_c06_comparison


STAGES = (
    ("c06-1", "sleepy-neutral"),
    ("c06-2", "sleepy-secure"),
    ("c06-3", "loosened-mouth"),
    ("c06-4", "soft-smile"),
)
COLORS = {
    "a": ("red", "green", "blue", "yellow"),
    "b": ("magenta", "cyan", "orange", "purple"),
    "c": ("brown", "pink", "lime", "navy"),
}


def source_path(variant: str, stage_index: int) -> Path:
    stage, descriptor = STAGES[stage_index]
    return Path("source/candidates/c06/r01") / (
        f"akari-v1.2_{stage}_{descriptor}_r01-{variant}.png"
    )


def make_request(root: Path) -> Path:
    for variant, colors in COLORS.items():
        for index, color in enumerate(colors):
            path = root / source_path(variant, index)
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (300, 480), color).save(path)
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump(
            {
                "stages": [
                    {
                        "stage": stage,
                        "descriptor": descriptor,
                        "prompt_delta": f"{stage} prompt",
                    }
                    for stage, descriptor in STAGES
                ],
                "review_sets": [
                    {
                        "candidate_id": f"c06-r01-{variant}",
                        "source_paths": [
                            source_path(variant, index).as_posix()
                            for index in range(4)
                        ],
                    }
                    for variant in ("a", "b")
                ],
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


class C06ComparisonTests(unittest.TestCase):
    def test_builds_initial_two_by_four_board_in_review_set_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "comparison.webp"
            build_c06_comparison(make_request(root), root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 1112))
                for row, variant in enumerate(("a", "b")):
                    for column, color in enumerate(COLORS[variant]):
                        assert_color_close(
                            self,
                            image.getpixel(
                                (170 + column * 320, 260 + row * 546)
                            ),
                            color,
                        )

    def test_builds_literal_targeted_repair_row(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            sources = copy.deepcopy(data["review_sets"][0]["source_paths"])
            sources[2] = source_path("c", 2).as_posix()
            data["review_sets"].append(
                {
                    "candidate_id": "c06-r01-a-repair-c06-3",
                    "source_paths": sources,
                }
            )
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            output = root / "repair.webp"
            build_c06_comparison(request, root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 1658))
                expected = ("red", "green", "lime", "yellow")
                for column, color in enumerate(expected):
                    assert_color_close(
                        self,
                        image.getpixel((170 + column * 320, 1352)),
                        color,
                    )

    def test_builds_complete_c_family_row(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["review_sets"].append(
                {
                    "candidate_id": "c06-r01-c",
                    "source_paths": [
                        source_path("c", index).as_posix()
                        for index in range(4)
                    ],
                }
            )
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            output = root / "complete-c.webp"
            build_c06_comparison(request, root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 1658))
                for column, color in enumerate(COLORS["c"]):
                    assert_color_close(
                        self,
                        image.getpixel((170 + column * 320, 1352)),
                        color,
                    )

    def test_rejects_reordered_stages(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["stages"].reverse()
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "expected C06 stage order"):
                build_c06_comparison(request, root, root / "out.webp")

    def test_rejects_reordered_or_incomplete_review_sets(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))

            reordered = copy.deepcopy(data)
            reordered["review_sets"].reverse()
            request.write_text(
                yaml.safe_dump(reordered, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "expected C06 A and B review sets first"
            ):
                build_c06_comparison(request, root, root / "reordered.webp")

            incomplete = copy.deepcopy(data)
            incomplete["review_sets"][0]["source_paths"].pop()
            request.write_text(
                yaml.safe_dump(incomplete, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "expected four ordered C06 sources"
            ):
                build_c06_comparison(request, root, root / "incomplete.webp")

    def test_rejects_a_missing_source(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            (root / source_path("b", 1)).unlink()
            with self.assertRaisesRegex(ValueError, "missing"):
                build_c06_comparison(request, root, root / "missing.webp")


if __name__ == "__main__":
    unittest.main()
```

Add this exact entry to `natural_form_commands` in
`NaturalFormIsolationTests`:

```python
"build:v1-2:c06-comparison": (
    "uv run python scripts/build_v1_2_c06_comparison.py "
    "--request akari-v1.2/manifest/generation-requests/c06-r01.yaml "
    "--output akari-v1.2/comparisons/c06-r01/"
    "c06-r01-comparison.webp"
),
```

- [ ] **Step 2: Run focused tests and verify red**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_c06_comparison \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests -v
```

Expected: ERROR because `build_v1_2_c06_comparison.py` and its npm command do
not exist.

- [ ] **Step 3: Implement the thin dedicated builder**

Create `scripts/build_v1_2_c06_comparison.py`:

```python
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

if __package__:
    from scripts.build_v1_2_c03_comparisons import render_grid
else:
    from build_v1_2_c03_comparisons import render_grid


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
STAGE_ORDER = (
    ("c06-1", "sleepy-neutral"),
    ("c06-2", "sleepy-secure"),
    ("c06-3", "loosened-mouth"),
    ("c06-4", "soft-smile"),
)


def review_set_label(candidate_id: str) -> str:
    complete = {
        "c06-r01-a": "A",
        "c06-r01-b": "B",
        "c06-r01-c": "C",
    }
    if candidate_id in complete:
        return complete[candidate_id]
    match = re.fullmatch(
        r"c06-r01-([ab])-repair-c06-([1-4])", candidate_id
    )
    if match:
        return f"{match.group(1).upper()}+C{match.group(2)}"
    raise ValueError("invalid C06 review set ID")


def build_c06_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    actual_stages = [
        (item.get("stage"), item.get("descriptor"))
        for item in request.get("stages", [])
    ]
    if actual_stages != list(STAGE_ORDER):
        raise ValueError("expected C06 stage order")

    review_sets = request.get("review_sets")
    if not isinstance(review_sets, list) or len(review_sets) not in (2, 3):
        raise ValueError("expected two or three C06 review sets")
    candidate_ids = [item.get("candidate_id") for item in review_sets]
    if candidate_ids[:2] != ["c06-r01-a", "c06-r01-b"]:
        raise ValueError("expected C06 A and B review sets first")

    rows = []
    for review_set in review_sets:
        label = review_set_label(review_set["candidate_id"])
        source_paths = review_set.get("source_paths")
        if not isinstance(source_paths, list) or len(source_paths) != 4:
            raise ValueError("expected four ordered C06 sources")
        row = []
        for (stage, descriptor), source_value in zip(
            STAGE_ORDER, source_paths
        ):
            source = Path(source_value)
            expected_name = re.compile(
                rf"akari-v1\.2_{stage}_{descriptor}_r01-[abc]\.png"
            )
            if (
                source.is_absolute()
                or source.parts[:4]
                != ("source", "candidates", "c06", "r01")
                or expected_name.fullmatch(source.name) is None
            ):
                raise ValueError(
                    "review set sources must match C06 stage order"
                )
            row.append(
                (
                    f"{label}  {stage.upper()}  {descriptor}",
                    package_root / source,
                )
            )
        rows.append(row)
    return render_grid(rows, output_path)


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_c06_comparison(
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
"build:v1-2:c06-comparison": "uv run python scripts/build_v1_2_c06_comparison.py --request akari-v1.2/manifest/generation-requests/c06-r01.yaml --output akari-v1.2/comparisons/c06-r01/c06-r01-comparison.webp"
```

- [ ] **Step 4: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_build_v1_2_c06_comparison \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests -v
git add \
  scripts/build_v1_2_c06_comparison.py \
  tests/test_build_v1_2_c06_comparison.py \
  tests/test_akari_v1_2_natural_form_package.py \
  package.json
git diff --cached --check
git commit -m "feat: add Natural Form C06 comparison command"
```

Expected: six comparison tests pass and existing C03/C07 comparison code is
unchanged.

---

### Task 5: Generate and freeze the local A/B families

**Files:**

- Create local-only: eight declared PNGs under
  `akari-v1.2/source/candidates/c06/r01/`.
- Do not modify accepted assets, review log, or repair mode.

**Interfaces:**

- Consumes: the exact four references, `shared_prompt`, and each ordered stage
  `prompt_delta` from `c06-r01.yaml`.
- Produces: complete A and B families, each containing four independent direct
  edits of accepted C05 with frozen format, dimensions, and SHA-256 values.

- [ ] **Step 1: Invoke image generation and run the pre-generation gate**

Invoke `imagegen`, read its current `SKILL.md`, and follow its built-in edit
workflow. Then run:

```sh
bash -lc 'npm run validate:v1-2'
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests -v
git status --short --branch
mkdir -p akari-v1.2/source/candidates/c06/r01
```

Expected: PASS with C06 still `candidate` r00, `repair_lane.mode: inactive`, no
C06 reviews, and `(22, 36)` generation work.

- [ ] **Step 2: Open all four references at original detail**

Use `view_image` with `detail: original` in this order:

```text
akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
akari-v1.2/references/v1.1/expression-grid.webp
```

State these roles before every call:

```text
Image 1 is the controlling accepted C05 edit target for composition, crop,
camera, morning hair, ornament placement, hoodie, light, backdrop, rendering,
and sleepy-neutral baseline. Image 2 is the adult-identity and face-geometry
rejection cross-check only. Image 3 is the ornament, cheek-silhouette, and bob
construction rejection cross-check only. Image 4 is a non-controlling neutral
through closed-mouth-soft-smile mechanics reference only. Image 1 controls the
current visual state; Images 2 and 3 reject further drift; Image 4 controls no
identity, crop, hair, outfit, background, or rendering property.
```

Repeat this four-image opening immediately before each of the eight calls.

- [ ] **Step 3: Generate family A in stage order**

For C06-1, C06-2, C06-3, and C06-4, call built-in `image_gen` once per image as
an identity-preserving edit. Pass the same four absolute reference paths with
C05 first. Use the role text above, the byte-identical `shared_prompt`, and only
that stage's `prompt_delta`. Do not mention family A in the visual prompt.

Save the returned full images without editing to the four declared `-a.png`
paths. At the start of each following continuation, run the complete matching
block below in its own shell before opening references for the next call.

After A C06-1:

```sh
set -euo pipefail
path='akari-v1.2/source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-a.png'
file -- "$path"
identify -format '%f %wx%h %[colorspace]\n' "$path"
sha256sum -- "$path"
```

After A C06-2:

```sh
set -euo pipefail
path='akari-v1.2/source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-a.png'
file -- "$path"
identify -format '%f %wx%h %[colorspace]\n' "$path"
sha256sum -- "$path"
```

After A C06-3:

```sh
set -euo pipefail
path='akari-v1.2/source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-a.png'
file -- "$path"
identify -format '%f %wx%h %[colorspace]\n' "$path"
sha256sum -- "$path"
```

After A C06-4:

```sh
set -euo pipefail
path='akari-v1.2/source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-a.png'
file -- "$path"
identify -format '%f %wx%h %[colorspace]\n' "$path"
sha256sum -- "$path"
```

Expected for every block: a real 1024 x 1536 RGB/sRGB PNG. If dimensions
differ, preserve it at that path and record a production Major; do not resize
or overwrite it.

Because `image_gen` ends its agent turn, each matching verifier runs at the
start of the next continuation, before any references are reopened for the next
slot. After A C06-4, verify it at the start of the continuation that begins B
C06-1.

- [ ] **Step 4: Generate family B independently**

Repeat Step 3 for C06-1 through C06-4 at the four declared `-b.png` paths.
Reopen the fixed references before every call. Use the same prompt for the same
stage and never show an A output while generating B. As with A, run each whole
block at the start of the following continuation.

After B C06-1:

```sh
set -euo pipefail
path='akari-v1.2/source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-b.png'
file -- "$path"
identify -format '%f %wx%h %[colorspace]\n' "$path"
sha256sum -- "$path"
```

After B C06-2:

```sh
set -euo pipefail
path='akari-v1.2/source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-b.png'
file -- "$path"
identify -format '%f %wx%h %[colorspace]\n' "$path"
sha256sum -- "$path"
```

After B C06-3:

```sh
set -euo pipefail
path='akari-v1.2/source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-b.png'
file -- "$path"
identify -format '%f %wx%h %[colorspace]\n' "$path"
sha256sum -- "$path"
```

After B C06-4:

```sh
set -euo pipefail
path='akari-v1.2/source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-b.png'
file -- "$path"
identify -format '%f %wx%h %[colorspace]\n' "$path"
sha256sum -- "$path"
```

- [ ] **Step 5: Recover a missing local payload structurally if required**

If an image appears in the interface but no local PNG exists, parse the current
date's rollout JSONL for the matching `image_generation_call` whose `result`
starts with `iVBOR`. Decode it structurally, verify PNG signature
`89504e470d0a1a0a`, and write only the matching declared candidate path. Never
print or hand-copy base64 through terminal output.

A technical call with no image and no recoverable payload may be retried once
for that same path. Every successfully returned full image consumes its attempt,
including duplicates and candidates that later fail review.

- [ ] **Step 6: Freeze and inventory all eight outputs**

```sh
find akari-v1.2/source/candidates/c06/r01 -maxdepth 1 \
  -type f -name '*.png' -print | sort
file akari-v1.2/source/candidates/c06/r01/*.png
identify -format '%f %wx%h %[colorspace]\n' \
  akari-v1.2/source/candidates/c06/r01/*.png
sha256sum akari-v1.2/source/candidates/c06/r01/*.png
git status --short
```

Expected: exactly eight frozen A/B PNGs and no candidate staged or tracked.
Do not commit local-only outputs.

---

### Task 6: Compare A/B, review continuity, and choose the next branch

**Files:**

- Create local-only:
  `akari-v1.2/comparisons/c06-r01/c06-r01-comparison.webp`.
- Do not modify accepted C06 state before explicit user selection.

**Interfaces:**

- Consumes: eight frozen A/B sources and the C06 identity, state, rendering,
  and production gates.
- Produces: one 2 x 4 comparison, complete A/B set findings, and exactly one of
  three decisions: stop for user selection, activate targeted C, or activate
  full-family C.

- [ ] **Step 1: Build and verify the initial comparison**

```sh
bash -lc 'npm run build:v1-2:c06-comparison'
file akari-v1.2/comparisons/c06-r01/c06-r01-comparison.webp
identify -format '%f %wx%h\n' \
  akari-v1.2/comparisons/c06-r01/c06-r01-comparison.webp
git status --short
```

Expected: a readable 1300 x 1112 WebP with A/B rows and C06-1 through C06-4
columns. It remains untracked.

- [ ] **Step 2: Invoke the review skill and open all evidence**

Invoke `akari-v1-1-image-review`, read its current `SKILL.md`, and use only its
review criteria. Do not run a correction or humanization pass.

Open the comparison, all eight original PNGs, accepted C05, accepted C01, and
accepted C03 with `view_image`. Review original resolution before assigning a
finding.

- [ ] **Step 3: Review each complete family in the required order**

For A, then B, record:

1. Identity — adult age, fixed face width, cheeks, chin, base eyes, bob,
   ornament, palette, and hoodie.
2. Invariants — crop, camera, head angle, morning hair, outfit, backdrop,
   lighting, and rendering stay stable across all four columns.
3. Stage clarity — each image meets its named sleepy-neutral, sleepy-secure,
   loosened-mouth, or soft-smile contract.
4. Gradient continuity — comfort and mouth warmth increase monotonically
   without reversal or a sudden jump; eye opening differs only slightly,
   eye closure is never the main progression device, and later stages do not
   become sleepier than earlier stages.
5. Rendering — face, eyes, mouth, hair, ornament, hoodie, backdrop, and surface
   contain no drawing artifact.
6. Production — exact 1024 x 1536 PNG, canonical path, SHA-256, standalone
   composition, and complete face/hair/crop readability.

Persist eventual face-construction findings as `identity`, stage and continuity
findings as `state`, drawing defects as `rendering`, and file/crop/path findings
as `production`.

- [ ] **Step 4: Apply the repair decision table**

- If at least one complete family is eligible and no one-stage repair would
  clearly produce the stronger quality-first set, present A/B findings and the
  strongest eligible recommendation to the user. Ask for one literal
  `candidate_id` and stop before promotion.
- If an otherwise strongest family has exactly one repair-worthy
  expression-strength, expression-order, technical, or dimension problem while
  its other three stages pass every global invariant, and that one repair is
  clearly justified by the quality-first comparison, continue to Task 7
  targeted-stage mode. The isolated problem may be Minor or Major, but the
  assembled repaired set must be reviewed from the beginning and finish with
  no unresolved Blocker or Major.
- If failures affect more than one stage or any identity, face geometry, crop,
  hair, ornament, outfit, lighting, backdrop, or rendering invariant across a
  family, continue to Task 7 full-family mode.
- Do not close r01 after only A/B visual failure. When neither A nor B is
  eligible, use targeted-stage only for the exact one-stage case above;
  otherwise activate full-family C. If a technical outage prevents a declared C
  call from returning any image or recoverable payload after its one permitted
  retry, stop and report the blocker without recording a visual r01 closure.

Do not ask the user to accept a set with an unresolved Blocker or Major.

---

### Task 7: Activate and execute the one allowed C repair branch

**Files:**

- Modify before generation:
  `akari-v1.2/manifest/generation-requests/c06-r01.yaml`.
- Create local-only: one targeted `-c.png` or four complete C-family PNGs.
- Rebuild local-only comparison after generation.

**Interfaces:**

- Consumes: Task 6 findings and the already-tested repair schema.
- Produces: one committed repair contract and one final three-row review board.

- [ ] **Step 1: Activate exactly one declared repair mode**

For a targeted repair, keep candidates A/B unchanged and replace the inactive
lane with the exact observed base, stage, and canonical C target. For example,
the approved base-A C06-3 form is:

```yaml
repair_lane:
  mode: targeted-stage
  base_family: a
  stage: c06-3
  target_path: source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-c.png
```

Append this exact assembled review set for that example:

```yaml
  - candidate_id: c06-r01-a-repair-c06-3
    source_paths:
      - source/candidates/c06/r01/akari-v1.2_c06-1_sleepy-neutral_r01-a.png
      - source/candidates/c06/r01/akari-v1.2_c06-2_sleepy-secure_r01-a.png
      - source/candidates/c06/r01/akari-v1.2_c06-3_loosened-mouth_r01-c.png
      - source/candidates/c06/r01/akari-v1.2_c06-4_soft-smile_r01-a.png
```

The complete set of allowed targeted IDs is:

- `c06-r01-a-repair-c06-1`
- `c06-r01-a-repair-c06-2`
- `c06-r01-a-repair-c06-3`
- `c06-r01-a-repair-c06-4`
- `c06-r01-b-repair-c06-1`
- `c06-r01-b-repair-c06-2`
- `c06-r01-b-repair-c06-3`
- `c06-r01-b-repair-c06-4`

For the selected ID, replace only that numbered stage in its A or B base set
with the same stage's canonical C path: `c06-1_sleepy-neutral_r01-c.png`,
`c06-2_sleepy-secure_r01-c.png`, `c06-3_loosened-mouth_r01-c.png`, or
`c06-4_soft-smile_r01-c.png`. `validate_generation_request` is the final
authority and must reject any inconsistent mapping.

For full-family repair, use `repair_lane: {mode: full-family}`, append the exact
four-output `complete-family-c` candidate by changing only the A-family suffixes
to `-c.png`, and append `c06-r01-c` with those four paths in stage order.

- [ ] **Step 2: Validate and commit the activated contract before generation**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
git add akari-v1.2/manifest/generation-requests/c06-r01.yaml
git diff --cached --check
git commit -m "feat: activate Natural Form C06 r01 repair"
```

Expected generation count: `(22, 37)` for targeted-stage or `(23, 40)` for
full-family. Stop if validation is red.

- [ ] **Step 3: Generate only the declared C output or family**

Invoke `imagegen` and reopen the same four fixed references before every call.
Use the same role header, shared prompt, and matching existing stage delta as
A/B. Never use A/B/C06 outputs as visual inputs. Save only to the newly declared
C path or paths.

Every C result ends its agent turn. At the start of the next continuation, run
the same complete per-file `set -euo pipefail`, `file`, `identify`, and
`sha256sum` block from Task 5 against the exact declared C filename before the
next C call or comparison build. Apply the same payload-recovery and no-resize
rules from Task 5.

- [ ] **Step 4: Rebuild and review the final three-row board**

```sh
bash -lc 'npm run build:v1-2:c06-comparison'
identify -format '%f %wx%h\n' \
  akari-v1.2/comparisons/c06-r01/c06-r01-comparison.webp
```

Expected: 1300 x 1658. Review all three declared `review_sets` from the
beginning. For targeted repair, judge the literal mixed row, not the isolated C
image.

- [ ] **Step 5: Stop for selection or close r01**

In targeted-stage mode, first apply the branch lock: if the assembled repaired
set has an unresolved Blocker or Major, append rejected reviews for every
declared `review_set`, leave C06 candidate r00, validate and commit the r01
closure, and return to brainstorming for r02. Do not fall back to A/B,
overwrite C, add a second targeted repair, or reinterpret the targeted C image
as a full C family.

In full-family mode, close r01 the same way only when no declared A/B/C set is
eligible. When the targeted assembled set passes, or when at least one
full-family-mode set is eligible, show the final comparison and concise
set-level findings, recommend the strongest eligible set, ask the user for one
literal `candidate_id`, and stop.

---

### Task 8: Promote exactly the user-selected four-image set

**Files:**

- Create: the four C06 accepted PNGs under
  `akari-v1.2/accepted/core/face-hair/`.
- Modify: `akari-v1.2/manifest/assets.yaml`.
- Modify: `akari-v1.2/manifest/review-log.yaml`.
- Modify: `tests/test_akari_v1_2_natural_form_package.py`.

**Interfaces:**

- Consumes: explicit literal user-selected `candidate_id`, its declared ordered
  source paths, frozen hashes, and actual set findings.
- Produces: one accepted C06 r01 asset with four byte-identical files and one
  complete ordered review batch.

- [ ] **Step 1: Reconfirm the selection and every current digest**

Verify the literal selected ID exists exactly once in request `review_sets` and
was explicitly named by the user. Then run:

```sh
sha256sum akari-v1.2/source/candidates/c06/r01/*.png
```

Stop if any source digest differs from its frozen Task 5 or Task 7 value.

- [ ] **Step 2: Write the failing live final-state test**

Add to `NaturalFormLifecycleTests`:

```python
def test_c06_acceptance_links_four_files_to_one_declared_review_set(self):
    c06 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C06"
    )
    self.assertEqual(c06["status"], "accepted")
    self.assertEqual(c06["revision"], "r01")
    self.assertEqual(
        c06["accepted_paths"],
        [
            "accepted/core/face-hair/"
            "akari-v1.2_c06-1_sleepy-neutral_r01.png",
            "accepted/core/face-hair/"
            "akari-v1.2_c06-2_sleepy-secure_r01.png",
            "accepted/core/face-hair/"
            "akari-v1.2_c06-3_loosened-mouth_r01.png",
            "accepted/core/face-hair/"
            "akari-v1.2_c06-4_soft-smile_r01.png",
        ],
    )
    request = next(
        item for item in self.generation_requests
        if (item["asset_id"], item["revision"]) == ("C06", "r01")
    )
    reviews = [
        item for item in self.review_log["reviews"]
        if (item["asset_id"], item["revision"]) == ("C06", "r01")
    ]
    self.assertEqual(
        [item["candidate_id"] for item in reviews],
        [item["candidate_id"] for item in request["review_sets"]],
    )
    self.assertEqual(
        [item["source_paths"] for item in reviews],
        [item["source_paths"] for item in request["review_sets"]],
    )
    accepted = [item for item in reviews if item["status"] == "accepted"]
    self.assertEqual(len(accepted), 1)
    self.assertEqual(len(accepted[0]["source_paths"]), 4)
    self.assertEqual(len(accepted[0]["source_sha256s"]), 4)
    self.assertTrue(
        all(
            item is accepted[0] or item["status"] == "rejected"
            for item in reviews
        )
    )
    self.assertFalse(
        any(
            finding["severity"] in {"blocker", "major"}
            and not finding["resolved"]
            for finding in accepted[0]["findings"]
        )
    )
    for accepted_path in c06["accepted_paths"]:
        with Image.open(PACKAGE_ROOT / accepted_path) as image:
            self.assertEqual(image.format, "PNG")
            self.assertEqual(image.size, (1024, 1536))
    validate_assets(self.assets, PACKAGE_ROOT)
    validate_review_log(self.review_log)
    validate_lifecycle_linkage(
        self.assets,
        self.generation_requests,
        self.review_log,
        PACKAGE_ROOT,
    )
```

- [ ] **Step 3: Run the final-state test and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests.test_c06_acceptance_links_four_files_to_one_declared_review_set -v
```

Expected: FAIL because C06 remains candidate r00 with no accepted files or C06
review batch.

- [ ] **Step 4: Copy the selected sources byte-for-byte in stage order**

Set and export `SELECTED_ID` as the exact literal user response in the same
shell invocation that runs this block; provide no default. Read only the
declared source mapping from YAML, then use shell `cp` for the binary writes:

```sh
set -euo pipefail
: "${SELECTED_ID:?Set SELECTED_ID to the exact user-selected review-set ID}"
export SELECTED_ID
SELECTED_OUTPUT="$(
uv run python - <<'PY'
import os
from pathlib import Path
import yaml

request = yaml.safe_load(
    Path("akari-v1.2/manifest/generation-requests/c06-r01.yaml")
    .read_text(encoding="utf-8")
)
matches = [
    item for item in request["review_sets"]
    if item["candidate_id"] == os.environ["SELECTED_ID"]
]
if len(matches) != 1:
    raise SystemExit("selected review set must exist exactly once")
print("\n".join(matches[0]["source_paths"]))
PY
)"
mapfile -t SELECTED_SOURCES <<<"$SELECTED_OUTPUT"
test "${#SELECTED_SOURCES[@]}" -eq 4
DESTINATIONS=(
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-1_sleepy-neutral_r01.png
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-3_loosened-mouth_r01.png
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-4_soft-smile_r01.png
)
for index in 0 1 2 3; do
  cp -- "akari-v1.2/${SELECTED_SOURCES[$index]}" \
    "${DESTINATIONS[$index]}"
  cmp --silent -- "akari-v1.2/${SELECTED_SOURCES[$index]}" \
    "${DESTINATIONS[$index]}"
done
```

The environment value must equal one declared full or repaired review-set ID
verbatim. Every `cmp` must exit 0.

- [ ] **Step 5: Update only C06 asset state and append exact set reviews**

Change C06 in `assets.yaml` to:

```yaml
    status: accepted
    revision: r01
    accepted_paths:
      - accepted/core/face-hair/akari-v1.2_c06-1_sleepy-neutral_r01.png
      - accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png
      - accepted/core/face-hair/akari-v1.2_c06-3_loosened-mouth_r01.png
      - accepted/core/face-hair/akari-v1.2_c06-4_soft-smile_r01.png
```

Append one review-log record per declared `review_set`, in request order. Copy
each `candidate_id` and `source_paths` literally; record the four observed
lowercase SHA-256 values in the same stage order; persist actual findings using
existing categories; and write a set-level decision. Mark only the user's set
`accepted` and every other set `rejected`. The accepted review must contain no
unresolved Blocker or Major and must never use `accepted-with-notes`.

- [ ] **Step 6: Verify lifecycle, dimensions, hashes, and byte identity**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
file akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-*.png
identify -format '%f %wx%h %[colorspace]\n' \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-*.png
sha256sum \
  akari-v1.2/source/candidates/c06/r01/*.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-*.png
```

Expected: four real 1024 x 1536 PNGs, exactly one accepted review, and each
accepted digest equal to its selected source. Re-run all four selected `cmp`
checks.

- [ ] **Step 7: Commit durable acceptance only**

```sh
git add \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-1_sleepy-neutral_r01.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-3_loosened-mouth_r01.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-4_soft-smile_r01.png \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  tests/test_akari_v1_2_natural_form_package.py
git status --short
git diff --cached --check
git commit -m "feat: accept Natural Form C06 r01 set"
```

Confirm no candidate PNG, comparison WebP, review crop, or unrelated artifact
is staged.

---

### Task 9: Run fresh final-state verification and hand off the branch

**Files:**

- Verify only; do not broaden scope to unrelated changes.

**Interfaces:**

- Consumes: final request mode, references, comparison command, accepted set,
  asset record, and reviews.
- Produces: fresh completion evidence on the final C06 branch and a reviewed
  branch ready for the normal finish/merge decision.

- [ ] **Step 1: Run focused and complete test suites**

```sh
uv run python -m unittest tests.test_build_v1_2_c06_comparison -v
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormInheritanceTests -v
bash -lc 'npm run test:node'
bash -lc 'npm run test:python'
bash -lc 'npm run validate:v1-2'
```

Expected: all focused, Node, root Python, legacy Python, and Natural Form
validation checks pass.

- [ ] **Step 2: Run audits, Markdown lint, and whitespace checks**

```sh
bash -lc 'npm run audit'
bash -lc 'npm run lint:md'
git diff --check
```

Expected: every audit passes and Markdown lint reports zero errors.

- [ ] **Step 3: Prove accepted artifacts and repository hygiene**

```sh
file akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-*.png
identify -format '%f %wx%h %[colorspace]\n' \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-*.png
sha256sum akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-*.png
git status --short --branch
git -C /path/to/akari-design status --short --branch
```

Expected: four 1024 x 1536 RGB/sRGB accepted PNGs, only C06 candidate and
comparison artifacts remain local in the feature worktree, and the main
workspace still lists its preserved C04/C05/C07 review artifacts unchanged.

- [ ] **Step 4: Request code review and verify before claiming completion**

Invoke `superpowers:requesting-code-review` for the complete branch diff against
`main`. Address valid findings with `superpowers:receiving-code-review`, rerun
the affected focused tests, then invoke
`superpowers:verification-before-completion` and repeat the final evidence
commands it requires.

- [ ] **Step 5: Hand off to branch finishing without pushing**

Invoke `superpowers:finishing-a-development-branch`. Offer the normal merge,
PR, keep, or discard options, but do not push. If the user chooses local main
integration, merge only the durable C06 commits and rerun final verification on
merged `main`.

Before removing the C06 worktree, preserve its local-only C06 evidence in the
main workspace without touching the existing C04/C05/C07 paths. Run this from a
shell whose current directory is outside the feature worktree:

```sh
set -euo pipefail
FEATURE=/path/to/akari-design/.worktrees/codex-c06-expression-gradient
MAIN=/path/to/akari-design
for relative in \
  akari-v1.2/source/candidates/c06 \
  akari-v1.2/comparisons/c06-r01 \
  tmp/c06-review
do
  test -e "$FEATURE/$relative" || continue
  test ! -e "$MAIN/$relative"
  mkdir -p "$(dirname "$MAIN/$relative")"
  cp -a -- "$FEATURE/$relative" "$MAIN/$relative"
  diff -qr -- "$FEATURE/$relative" "$MAIN/$relative"
done
PRESERVED=(
  "$MAIN/akari-v1.2/source/candidates/c06"
  "$MAIN/akari-v1.2/comparisons/c06-r01"
)
if test -d "$MAIN/tmp/c06-review"; then
  PRESERVED+=("$MAIN/tmp/c06-review")
fi
find "${PRESERVED[@]}" -type f -print0 \
  | sort -z \
  | xargs -0 -r sha256sum
git -C "$MAIN" status --short --branch
```

Stop if any destination already exists or any `diff -qr` reports a mismatch;
do not overwrite an earlier local C06 run. The main status must show its prior
C04/C05/C07 evidence unchanged plus the copied C06 evidence. Remove the C06
worktree and branch only after this preservation proof and merged-main
verification succeed; a forced worktree removal is permitted only for this
verified duplicate after the user selected the cleanup option.

---

## Execution Stop Conditions

- Stop before generation if the request, dependency, inheritance, or lifecycle
  validator is red.
- Stop a generation slot after a returned image; never overwrite a successful
  result to seek a better-looking variation.
- Stop and preserve any wrong-size output as a production Major; never resize
  it into compliance.
- Stop before any C call until the targeted-stage or full-family repair contract
  is validated and committed.
- Stop after one targeted C stage. If its assembled set fails, close r01 and
  design r02 rather than generating another isolated repair.
- Stop after complete C if no eligible set remains; close r01 and design r02.
- Stop before promotion until the user explicitly names one eligible declared
  `candidate_id`.
- Stop promotion if any selected source hash changed, any accepted/source `cmp`
  fails, or any selected review retains an unresolved Blocker or Major.
- Stop branch completion if focused tests, full suites, validator, audits,
  Markdown lint, or final merged-state verification is red.

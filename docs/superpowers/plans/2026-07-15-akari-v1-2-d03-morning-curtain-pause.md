# Akari v1.2 Daily.1 D03 Morning Curtain Pause Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Register, generate, review, autonomously select, and accept D03 as a
full-body morning curtain-pause scene without changing D01, D02, or v1.2.0.

**Architecture:** Replace the three parallel Daily review maps with one typed
policy registry, then register D03 through the same exact-contract validator,
comparison builder, ordered-review lifecycle, optional-C gate, and
byte-identical promotion path already proven by D02. Keep per-scene creative
contracts frozen in YAML and validator constants; keep generated candidates
and comparisons local.

**Tech Stack:** Python 3.13, `unittest`, PyYAML, Pillow, Node/npm scripts,
Markdown, image generation with visible accepted references

## Global Constraints

- D03 is `D03`, revision `r01`, descriptor `morning-curtain-pause`.
- The accepted path is
  `accepted/daily/morning/akari-v1.2_d03_morning-curtain-pause_r01.png`.
- Generate independent A and B at a 1024 by 1536 target canvas.
- Accept dimensions from 1020-1028 by 1532-1540; never force-resize.
- C is allowed only when both A and B have unresolved D03-scene Blocker or
  Major findings and neither is eligible.
- Akari makes the quality-first selection under the user's explicit delegated
  authority; no selection checkpoint is required.
- Candidates and comparison images remain local and untracked.
- The promoted PNG must be byte-identical to its selected source.
- D01 Gate 4, D02 acceptance, Core PDF, and release pins remain unchanged.
- Run named gates serially on the 3-core, 2 GiB host.

---

## File Structure

- Modify `scripts/akari_v1_2_daily.py`: consolidate Daily review policy data.
- Modify `scripts/validate_akari_v1_2_natural_form.py`: register D03's static,
  generation, dependency, dimension, review, and lifecycle contracts.
- Modify `tests/test_akari_v1_2_daily.py`: cover policy compatibility and D03.
- Modify `akari-v1.2/manifest/assets.yaml`: add D03 as candidate, then accepted.
- Create `akari-v1.2/manifest/generation-requests/d03-r01.yaml`: frozen request.
- Modify `akari-v1.2/manifest/review-log.yaml`: append ordered D03 reviews.
- Modify `package.json`: add D03 comparison and edit-gate commands.
- Local only: `akari-v1.2/source/candidates/d03/r01/*.png`.
- Local only: `akari-v1.2/comparisons/d03-r01/d03-r01-comparison.webp`.

### Task 1: Consolidate Daily Review Policies

**Files:**

- Modify: `scripts/akari_v1_2_daily.py`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_daily.py`

**Interfaces:**

- Produces: `DailyReviewPolicy`, `DAILY_REVIEW_POLICIES`, and
  `daily_review_policy(asset_id)`.
- Preserves: all D01/D02 error messages and lifecycle behavior.

- [ ] **Step 1: Write failing policy-registry tests**

Add imports for `DAILY_REVIEW_POLICIES` and `daily_review_policy`. Assert D01
allows scene-only Minor for optional C, D02 requires Blocker/Major, and an
unknown asset raises `ValidationError("D99: Daily review policy required")`.
Also assert the policy keys initially expected by the live package are
`("D01", "D02")` so the test fails before the registry exists.

- [ ] **Step 2: Run the focused tests and verify RED**

```bash
uv run python -m unittest \
  tests.test_akari_v1_2_daily.DailyPrimitiveTests -v
```

Expected: import failure for `DAILY_REVIEW_POLICIES` or
`daily_review_policy`.

- [ ] **Step 3: Add the minimal immutable policy model**

Implement:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class DailyReviewPolicy:
    controllers: frozenset[str]
    scene_controller: str
    optional_c_finding_severities: frozenset[str]


DAILY_REVIEW_POLICIES = {
    "D01": DailyReviewPolicy(
        frozenset({"C04", "C05", "C06", "C07", "D01-scene"}),
        "D01-scene",
        frozenset({"blocker", "major", "minor"}),
    ),
    "D02": DailyReviewPolicy(
        frozenset({"D01", "C04", "C05", "C06", "C07", "D02-scene"}),
        "D02-scene",
        frozenset({"blocker", "major"}),
    ),
}


def daily_review_policy(asset_id: str) -> DailyReviewPolicy:
    try:
        return DAILY_REVIEW_POLICIES[asset_id]
    except KeyError as error:
        raise ValidationError(
            f"{asset_id}: Daily review policy required"
        ) from error
```

Update review and lifecycle validators to read the one policy object. Remove
`DAILY_CONTROLLERS`, `DAILY_SCENE_CONTROLLER`, and
`DAILY_OPTIONAL_C_FINDING_SEVERITIES` only after all consumers use the new
registry.

- [ ] **Step 4: Run the Daily and Natural Form tests and verify GREEN**

```bash
npm run test:python:daily
npm run test:python:natural-form
```

Expected: 44 Daily tests and 174 Natural Form tests pass before D03 tests are
added.

- [ ] **Step 5: Commit the policy refactor**

```bash
git add scripts/akari_v1_2_daily.py \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_daily.py
git commit -m "refactor: consolidate Daily review policies"
```

### Task 2: Register the D03 Candidate Contract

**Files:**

- Modify: `tests/test_akari_v1_2_daily.py`
- Modify: `scripts/akari_v1_2_daily.py`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Create: `akari-v1.2/manifest/generation-requests/d03-r01.yaml`
- Modify: `package.json`

**Interfaces:**

- Consumes: D03 design's exact five-reference and scene contract.
- Produces: a valid candidate-state D03 asset and A/B request.

- [ ] **Step 1: Write failing D03 contract tests**

Add `D03ContractTests` that load live manifests and assert:

```python
self.assertEqual(self.d03["descriptor"], "morning-curtain-pause")
self.assertEqual(self.d03["depends_on"], [
    "D02", "C01", "C03", "C05", "C06", "C07",
])
self.assertEqual(self.d03["status"], "candidate")
self.assertEqual(self.d03["revision"], "r00")
self.assertEqual(self.d03["accepted_paths"], [])
self.assertEqual(
    [item["variant"] for item in self.request["candidates"]],
    ["a", "b"],
)
```

Assert the five ordered roles are:

```python
[
    "accepted_d02_morning_continuity",
    "accepted_c01_standing_body",
    "accepted_c03_hairpin_three_quarter",
    "accepted_c06_morning_hair_sleepy_neutral",
    "accepted_c07_standing_sock_feet",
]
```

Call `validate_assets`, `validate_generation_request`, and
`validate_generation_dependencies` to cover integration.

- [ ] **Step 2: Run the D03 tests and verify RED**

```bash
uv run python -m unittest \
  tests.test_akari_v1_2_daily.D03ContractTests -v
```

Expected: D03 is absent from `assets.yaml` and no D03 request exists.

- [ ] **Step 3: Add D03 to the policy and asset manifests**

Register controllers:

```python
frozenset({
    "D02", "C01", "C03", "C05", "C06", "C07", "D03-scene",
})
```

Use Blocker/Major as the optional-C severities. Add D03 to `ASSET_IDS` and add
its exact static contract with phase `6`, gate `daily`, one default variant,
and expected path under `accepted/daily/morning/`.

- [ ] **Step 4: Write the exact D03 request**

Create `d03-r01.yaml` from the approved design. Use A/B target paths under
`source/candidates/d03/r01/`, no comparison anchors, the six acceptance gates,
and the eleven hard-reject groups from the design.

Calculate the prompt digest without changing the prompt:

```bash
uv run python - <<'PY'
import hashlib
from pathlib import Path
import yaml

path = Path("akari-v1.2/manifest/generation-requests/d03-r01.yaml")
request = yaml.safe_load(path.read_text(encoding="utf-8"))
print(hashlib.sha256(request["shared_prompt"].encode()).hexdigest())
PY
```

Copy that exact digest into `D03_R01_SHARED_PROMPT_SHA256` and register the
request in `GENERATION_REQUEST_CONTRACTS`.

- [ ] **Step 5: Add D03 dependency and dimension validation**

Require all six dependency assets at their accepted revisions and require the
request reference paths to match their declared accepted sources exactly.
Include D03 in Daily accepted-PNG dimension validation and in generic Daily
request dispatch.

- [ ] **Step 6: Add package commands**

Add:

```json
"build:v1-2:d03-comparison": "uv run python scripts/build_v1_2_daily_comparison.py --request akari-v1.2/manifest/generation-requests/d03-r01.yaml --output akari-v1.2/comparisons/d03-r01/d03-r01-comparison.webp --asset-id D03",
"gate:edit:d03": "npm run test:python:daily && npm run test:python:natural-form && npm run validate:v1-2 && npm run verify:v1-2:release-pins"
```

- [ ] **Step 7: Run tests and verify GREEN**

```bash
npm run test:python:daily
npm run test:python:natural-form
npm run validate:v1-2
```

Expected validator summary: 10 assets, 16 references, 11 generation requests,
28 candidate groups, 42 generated outputs, and 26 reviews.

- [ ] **Step 8: Commit the candidate contract**

```bash
git add scripts/akari_v1_2_daily.py \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_daily.py \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/generation-requests/d03-r01.yaml \
  package.json
git commit -m "feat: register D03 curtain pause"
```

### Task 3: Generate and Review A/B

**Files:**

- Local create: `akari-v1.2/source/candidates/d03/r01/*.png`
- Local create: `akari-v1.2/comparisons/d03-r01/d03-r01-comparison.webp`
- Modify after generation: `akari-v1.2/manifest/review-log.yaml`

**Interfaces:**

- Consumes: frozen D03 request and five accepted visible references.
- Produces: A/B originals, comparison, hashes, findings, and one selection.

- [ ] **Step 1: Open all five references immediately before generation**

Use `view_image` on D02, C01, C03 hairpin-side, C06-1, and C07 standing. C06-1
consolidates C05-lineage morning hair, sleepy-neutral expression, and rendering.
Keep their prompt roles identical to the generation request.

- [ ] **Step 2: Generate independent A**

Call image generation with only the five physical references and the frozen
shared prompt. Save the untouched PNG to the declared A path. Verify PNG
signature, dimensions, and SHA-256.

- [ ] **Step 3: Re-open references and generate independent B**

Do not provide A as a reference. Save untouched B to its declared path and
verify signature, dimensions, and SHA-256.

- [ ] **Step 4: Build and inspect the comparison**

```bash
npm run build:v1-2:d03-comparison
```

Open A, B, and the comparison. Review Identity, Body, State, Continuity,
Rendering, and Production at original resolution.

- [ ] **Step 5: Apply the retry policy**

If either A or B is eligible, select the stronger eligible candidate and skip
C. If both fail only for D03-scene reasons, append rejected A/B reviews, add C
to the request and exact contract, validate, generate C independently, and
review it. If failures share a Core or D02 controller, stop as a blocker.

- [ ] **Step 6: Record ordered reviews and delegated selection**

Append complete review records in request order. Record all findings with
controller and next action. Mark exactly one eligible candidate `accepted` and
state that Akari selected it under the user's autonomous-execution delegation.

### Task 4: Promote and Verify D03

**Files:**

- Modify: `tests/test_akari_v1_2_daily.py`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Create: `akari-v1.2/accepted/daily/morning/akari-v1.2_d03_morning-curtain-pause_r01.png`

- [ ] **Step 1: Write failing accepted-linkage tests**

Assert exactly one accepted D03 review, byte/hash linkage, clean-clone support
when local candidates are absent, and rejection of source or accepted hash
mismatch.

- [ ] **Step 2: Run accepted-linkage tests and verify RED**

Expected: D03 remains candidate and the accepted file is absent.

- [ ] **Step 3: Promote byte-for-byte**

Copy the selected source to the accepted path without image processing. Verify:

```bash
cmp --silent <selected-source> \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d03_morning-curtain-pause_r01.png
sha256sum <selected-source> \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d03_morning-curtain-pause_r01.png
```

Set D03 to `accepted`, `r01`, and the exact accepted path.

- [ ] **Step 4: Run the D03 edit gate**

```bash
npm run gate:edit:d03
```

Expected: all Daily and Natural Form tests, validator, and release pins pass.

- [ ] **Step 5: Commit durable acceptance files only**

```bash
git add tests/test_akari_v1_2_daily.py \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  akari-v1.2/accepted/daily/morning/akari-v1.2_d03_morning-curtain-pause_r01.png
git commit -m "feat: accept D03 morning curtain pause"
```

### Task 5: Final Integration and Main Merge

- [ ] **Step 1: Run serial integration verification**

```bash
npm run gate:integration:v1-2
git diff --check main...HEAD
git status --short
```

Expected: integration gate passes; only local D03 candidate/comparison paths
remain untracked.

- [ ] **Step 2: Merge to main and re-verify**

From the primary checkout, fast-forward or merge the feature branch without
touching unrelated local review artifacts. Run `npm run gate:edit:d03` on the
merged `main` and verify `HEAD` includes all durable commits.

- [ ] **Step 3: Clean up only after merged-state proof**

Remove the D03 worktree and delete the feature branch. Keep local candidates
and comparison evidence unless cleanup would delete the only copy; preserve
them in the primary repo's corresponding local directories first.

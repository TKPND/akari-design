# Akari V2.2 Weekend Strict Identity Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an enforceable, series-local identity-recovery overlay to the
active Weekend Happenings handoff without changing historical approvals,
existing image bytes, prompt cards, or the global Akari V2.2 skill.

**Architecture:** Keep the historical production state immutable and route the
existing `00-START-HERE.md` through a strict recovery runbook. Store the audit
projection, default-deny reference policy, and future actual-call ledger as
sidecars under `tracking/`; enforce them with one Python standard-library
validator and isolated unit tests.

**Tech Stack:** Markdown, CSV, JSON, JSON Lines, Python 3 standard library,
`unittest`, SHA-256, markdownlint-cli2.

## Global Constraints

- Scope is only series `akari_v22_weekend_happenings`.
- `package_generation_permission` remains `false`; this implementation must not
  call image generation or create/edit/crop/mask/composite any image.
- Do not modify `DECISION-LOG.md`, `tracking/shot-status.csv`,
  `tracking/shot-manifest.json`, `shots.yaml`, `prompts/**`,
  `runbook/PRODUCTION-RUNBOOK.md`, existing `outputs/**`, canonical references,
  the installed/bundled skills, or the original `SHA256SUMS`.
- Preserve historical `status`, `identity_status`, and `technical_status` values
  exactly in the post-audit projection.
- All historical generated images remain `reference_eligible=false` and
  `reference_quarantined=true`, including S01 and S06 controls.
- Only canonical portrait and one matching approved canonical angle helper may
  be face-bearing strict-recovery inputs. Canonical full-body is inventory-only
  and may later source a deterministic face-free plate.
- Final Akari identity judgment remains the user's; mechanical validation may
  block strict recovery pass/reference eligibility but never erase a user
  deliverable decision.
- Leave all pre-existing repository working-tree changes untouched.

---

### Task 1: Add the series-local recovery policy and dispatch

**Files:**

- Modify:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/00-START-HERE.md`
- Modify:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/tracking/README.md`
- Create:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/runbook/STRICT-IDENTITY-RECOVERY.md`
- Create:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/tracking/strict-identity-recovery.json`

**Interfaces:**

- Consumes: current handoff root, repository canonical authority paths, and the
  frozen historical hashes listed below.
- Produces: `strict-identity-recovery.json`, the sole machine-readable policy
  consumed by Tasks 2 and 3.

- [ ] **Step 1: Record the current immutable source hashes**

Run from repository root:

```bash
sha256sum \
  tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/DECISION-LOG.md \
  tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/tracking/shot-status.csv \
  tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/tracking/shot-manifest.json
```

Expected hashes, in the same order:

```text
a186d9c46646a3dd41cc38fda2b91989f71247fa52cb406a67d4c1be78a529f3
6b033f8ca3182495be6c1f970db20a8d06a88fcd017cadf4e24c6c161df4e628
8dad2ece22de064ec8819ad2af5bd5e80b994c1bb564c6217dd48fcd9577334a
```

Stop if any differs; a source-state change must be reconciled before applying
the overlay.

- [ ] **Step 2: Write the recovery policy JSON**

Create a JSON object with these top-level fields and exact values:

```json
{
  "schema_version": 1,
  "mode": "strict_identity_recovery",
  "series_id": "akari_v22_weekend_happenings",
  "package_generation_permission": false,
  "audit_attachment_sha256": "05846f006c461b80659378316e1725ad57ad36590b8703df5614b5bf0fedf9c1",
  "historical_sources": [],
  "immutable_output_roots": [
    "outputs/accepted",
    "outputs/review",
    "outputs/comparisons"
  ],
  "recovery_output_root": "outputs/recovery",
  "reference_policy": {},
  "expected_audit_counts": {
    "keep_final_only": 1,
    "manual_regate": 5,
    "rebuild_priority": 11,
    "rebuild_after_anchor": 6,
    "keep_rejected": 1
  },
  "manual_regate_shots": ["S03", "S04", "S07", "S13", "S14"],
  "rebuild_dependencies": {},
  "episode_resets": {}
}
```

Populate `historical_sources` with relative paths and the three hashes from
Step 1. Populate `reference_policy` with `default_decision: "deny"`, denied
prefixes for all three historical output roots, and these exact repository
authority path/hash pairs:

```text
akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp
b076afd95be49c4ed9c5a4ddfb4083c9ead8328313b4d5fa0555a374dd10543c

akari-v2.2/accepted/base/face-angles/akari-v2.2-face-near-front-f00.png
8ff5e5369b9877225b2c2bbc87ea92b6cb0e60309e846cb9250fc2a366cae957

akari-v2.2/accepted/base/face-angles/akari-v2.2-face-hairpin-side-f01-r02.png
a8d1574fd1edb071be5ddf111768aa1e5c8fa38a02d5f7aac76b5023823e6902

akari-v2.2/accepted/base/face-angles/akari-v2.2-face-opposite-side-f02.png
338568d22fc150b5b965b259a731de1d30d33c41d0d1238e3c28c044cb7734ad
```

Record canonical full-body separately as `direct_input_allowed: false`,
`allowed_roles: ["plate_source"]`, with hash:

```text
d93307fe219de81c6fb501e9472725a0ad8f3d242a0ddc741bf53d156f8d7688
```

Set rebuild dependencies exactly to:

```json
{
  "S11": ["S09", "S10"],
  "S17": ["S13", "S16"],
  "S18": ["S17"],
  "S19": ["S18"],
  "S22": ["S21"],
  "S23": ["S22"]
}
```

Set episode resets to S09, S17, S21, and S24; S24 must include
`canonical_portrait_only_face_bearing: true`.

- [ ] **Step 3: Write the strict recovery runbook**

Include these sections with executable rules rather than advisory prose:

```markdown
## Scope and precedence
## Frozen historical state
## Reference default deny
## Actual-input ledger preflight
## Identity-only comparison gate
## Reviewer-recorded outfit gate
## Episode resets and rebuild order
## Recovery output namespace
## Stop conditions
```

The preflight order is: append planned attempt to the actual-input ledger, run
the validator, inspect canonical inputs, then stop unless a separate current
user message explicitly authorizes that image-generation attempt.

- [ ] **Step 4: Route the existing entrypoint to recovery mode**

Add a prominent `strict_identity_recovery` block before the current start
procedure. It must direct the next agent to read the strict runbook and validate
the overlay first. Keep the required global/bundled Skill read; describe the
series profile as a narrowing supplement, never as a replacement for Skill
rules.

- [ ] **Step 5: Document the three tracking layers**

Update `tracking/README.md` to distinguish:

```text
shot-status.csv             immutable historical/user-approved state
shot-status.post-audit.csv  non-destructive audit and reference overlay
recovery-input-ledger.jsonl future actual-call truth
```

Add the exact validation command:

```bash
python3 scripts/validate_strict_identity_recovery.py
```

- [ ] **Step 6: Verify Task 1 text and JSON**

Run:

```bash
python3 -m json.tool tracking/strict-identity-recovery.json >/dev/null
```

Run markdownlint on the three changed Markdown files. Expected: exit 0.

No Git commit is made for these files because the handoff is intentionally
ignored. Confirm no unrelated tracked file changed.

---

### Task 2: Add the non-destructive audit projection and empty actual-input ledger

**Files:**

- Create:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/tracking/shot-status.post-audit.csv`
- Create:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/tracking/recovery-input-ledger.jsonl`

**Interfaces:**

- Consumes: `tracking/shot-status.csv`, the verified GPT Pro overlay fields,
  `shots.yaml` outfit keys, and Task 1 policy enums.
- Produces: the 24-row projection and schema-only ledger consumed by Task 3.

- [ ] **Step 1: Build the post-audit CSV without overwriting history**

Copy all 12 source columns and values in their original order, then append:

```text
audit_status,audit_severity,audit_confidence,face_reviewability,
audit_reason,recommended_action,reference_eligible,reference_quarantined,
manual_regate_status,human_identity_verdict,expected_outfit_key,
observed_outfit_key,outfit_review_status,outfit_verdict,
observed_bottom_category,observed_bottom_color,continuity_notes
```

Use RFC 4180 CSV quoting. Set every row to
`reference_eligible=false,reference_quarantined=true`. Set S03, S04, S07, S13,
and S14 to `manual_regate_status=awaiting_user_verdict` and
`human_identity_verdict=pending`; all other rows use `not_applicable` and
`not_reasked` respectively.

Expected outfit keys by inclusive shot groups are:

```text
S01-S09  sat_base
S10-S12  sat_rain
S13-S17  sun_base
S18-S20  sun_wind
S21-S24  sun_relaxed
```

Seed only S09's visual outfit observation:

```text
observed_outfit_key=sat_shorts_nonconforming
outfit_review_status=reviewed
outfit_verdict=hard_fail
observed_bottom_category=shorts
observed_bottom_color=beige_khaki
continuity_notes=expected dusty-blue below-knee flare skirt; observed shorts
```

All other observations remain empty with
`outfit_review_status=not_reviewed,outfit_verdict=pending`.

- [ ] **Step 2: Preserve the exact audit groups**

Project the audited groups exactly:

```text
keep_final_only: S01
manual_regate: S03 S04 S07 S13 S14
rebuild_priority: S02 S05 S08 S09 S10 S12 S15 S16 S20 S21 S24
rebuild_after_anchor: S11 S17 S18 S19 S22 S23
keep_rejected: S06
```

Use the attached audit's severity, confidence, reviewability, findings, and
recommended action verbatim as structured CSV field values; do not reinterpret
or shorten them during projection.

- [ ] **Step 3: Create the schema-only actual-input ledger**

Write exactly one valid JSON object on the first line:

```json
{"record_type":"schema","schema_version":1,"attempt_required_fields":["call_id","shot_id","operation","output_path","inputs","authorization","outfit_observation","identity_review","user_gate"],"generation_permission":false}
```

Do not add an attempt record and do not create `outputs/recovery/` yet.

- [ ] **Step 4: Verify historical equality and group counts manually**

Run a short read-only Python check that compares the first 12 values of each
post-audit row to `shot-status.csv` by ID and counts `audit_status`. Expected:
24 IDs, zero historical differences, and counts `1/5/11/6/1`.

No Git commit is made; confirm the original CSV hash is still
`6b033f8ca3182495be6c1f970db20a8d06a88fcd017cadf4e24c6c161df4e628`.

---

### Task 3: Implement the standard-library recovery validator with tests

**Files:**

- Create:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/scripts/validate_strict_identity_recovery.py`
- Create:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/scripts/tests/test_validate_strict_identity_recovery.py`

**Interfaces:**

- Consumes: `validate(pack_root: Path, repo_root: Path) -> list[str]`, Task 1
  policy JSON, Task 2 CSV/JSONL, historical files, and live canonical files.
- Produces: deterministic errors and CLI exit 0 on success/1 on validation
  failure.

- [ ] **Step 1: Write failing unit tests**

Use `tempfile.TemporaryDirectory` and copy only the text fixtures needed by each
mutation. Use this concrete test structure (the helper's `BASE_ATTEMPT` contains
the canonical portrait path/hash from Task 1):

```python
import copy
import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_strict_identity_recovery import validate

PACK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PACK_ROOT.parents[2]
FIXTURE_FILES = (
    "DECISION-LOG.md",
    "tracking/shot-status.csv",
    "tracking/shot-manifest.json",
    "tracking/shot-status.post-audit.csv",
    "tracking/strict-identity-recovery.json",
    "tracking/recovery-input-ledger.jsonl",
)
BASE_ATTEMPT = {
    "record_type": "attempt",
    "call_id": "TEST-r01",
    "shot_id": "S01",
    "operation": "generate",
    "output_path": "outputs/recovery/review/test.png",
    "inputs": [{
        "path": "akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp",
        "sha256": "b076afd95be49c4ed9c5a4ddfb4083c9ead8328313b4d5fa0555a374dd10543c",
        "source_class": "canonical_portrait",
        "contains_face": True,
        "role": "canonical_face",
    }],
    "authorization": "explicit_user_generation_request",
    "outfit_observation": {
        "expected_outfit_key": "sat_base",
        "observed_outfit_key": "sat_base",
        "verdict": "pass",
    },
    "identity_review": {
        "reviewability": "clear",
        "major_axis_differences": 0,
    },
    "user_gate": {"identity_verdict": "pass"},
    "strict_recovery_status": "strict_recovery_pass",
}


class StrictIdentityRecoveryTests(unittest.TestCase):
    def assert_fixture_error(self, *, code, attempt=None,
                             history_replacement=None,
                             s23_dependencies=None):
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "pack"
            for relative in FIXTURE_FILES:
                source = PACK_ROOT / relative
                target = fixture / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

            if attempt is not None:
                ledger = fixture / "tracking/recovery-input-ledger.jsonl"
                with ledger.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(attempt, ensure_ascii=False) + "\n")

            if history_replacement is not None:
                source_value, replacement = history_replacement
                status_path = fixture / "tracking/shot-status.csv"
                with status_path.open(encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    fieldnames = reader.fieldnames
                    rows = list(reader)
                self.assertIsNotNone(fieldnames)
                s01 = next(row for row in rows if row["id"] == "S01")
                self.assertEqual(s01["status"], source_value)
                s01["status"] = replacement
                with status_path.open("w", encoding="utf-8-sig", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

            if s23_dependencies is not None:
                policy_path = fixture / "tracking/strict-identity-recovery.json"
                policy = json.loads(policy_path.read_text(encoding="utf-8"))
                policy["rebuild_dependencies"]["S23"] = s23_dependencies
                policy_path.write_text(
                    json.dumps(policy, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            errors = validate(fixture, REPO_ROOT)
            self.assertTrue(any(code in error for error in errors), errors)

    def test_current_pack_passes(self):
        self.assertEqual(validate(PACK_ROOT, REPO_ROOT), [])

    def test_generated_face_bearing_input_is_rejected(self):
        attempt = copy.deepcopy(BASE_ATTEMPT)
        attempt["inputs"][0].update({
            "path": "outputs/accepted/s01-tote-slip-at-entry.png",
            "source_class": "generated_deliverable",
            "role": "edit_canvas",
        })
        self.assert_fixture_error(attempt=attempt,
                                  code="E_INPUT_GENERATED_FACE")

    def test_unregistered_face_free_plate_is_rejected(self):
        attempt = copy.deepcopy(BASE_ATTEMPT)
        attempt["inputs"] = [{
            "path": "outputs/recovery/plates/unregistered.png",
            "sha256": "0" * 64,
            "source_class": "deterministic_face_free_plate",
            "contains_face": False,
            "role": "body_plate",
        }]
        self.assert_fixture_error(attempt=attempt,
                                  code="E_PLATE_PROVENANCE")

    def test_historical_status_change_is_rejected(self):
        self.assert_fixture_error(history_replacement=("accepted", "blocked"),
                                  code="E_HISTORY_CHANGED")

    def test_s09_outfit_hard_fail_cannot_strict_pass(self):
        attempt = copy.deepcopy(BASE_ATTEMPT)
        attempt["shot_id"] = "S09"
        attempt["outfit_observation"] = {
            "expected_outfit_key": "sat_base",
            "observed_outfit_key": "sat_shorts_nonconforming",
            "verdict": "hard_fail",
        }
        attempt["strict_recovery_status"] = "strict_recovery_pass"
        self.assert_fixture_error(attempt=attempt,
                                  code="E_OUTFIT_HARD_FAIL")

    def test_s23_must_depend_on_s22(self):
        self.assert_fixture_error(s23_dependencies=["S21"],
                                  code="E_DEPENDENCY")

    def test_output_must_stay_under_recovery_root(self):
        attempt = copy.deepcopy(BASE_ATTEMPT)
        attempt["output_path"] = "outputs/review/unsafe.png"
        self.assert_fixture_error(attempt=attempt, code="E_OUTPUT_ROOT")
```

Each negative assertion must match a stable error code such as
`E_INPUT_GENERATED_FACE`, `E_PLATE_PROVENANCE`, `E_HISTORY_CHANGED`,
`E_OUTFIT_HARD_FAIL`, `E_DEPENDENCY`, or `E_OUTPUT_ROOT`.

- [ ] **Step 2: Run the tests and verify they fail for the missing validator**

Run from the handoff root:

```bash
python3 -m unittest discover -s scripts/tests -v
```

Expected: FAIL because `validate_strict_identity_recovery` cannot be imported.

- [ ] **Step 3: Implement the validator API and CLI**

Implement these focused functions with the exact public signatures:

- `sha256_file(path: Path) -> str`
- `load_policy(pack_root: Path) -> dict`
- `load_status_rows(pack_root: Path) -> tuple[list[str], list[dict[str, str]]]`
- `load_ledger(pack_root: Path) -> list[dict]`
- `validate_history(pack_root: Path, policy: dict) -> list[str]`
- `validate_audit_projection(pack_root: Path, policy: dict) -> list[str]`
- `validate_authorities(repo_root: Path, policy: dict) -> list[str]`
- `validate_attempt(record: dict, policy: dict, repo_root: Path) -> list[str]`
- `validate(pack_root: Path, repo_root: Path) -> list[str]`
- `main() -> int`

Validation rules:

- source hashes and historical CSV values must match;
- IDs must be exactly S01-S24 once each;
- audit counts and manual-regate set must match policy;
- every generated historical row remains quarantined and ineligible;
- each canonical authority path/hash must match the live repository;
- an attempt input with `contains_face=true` must exactly match an enabled
  canonical face authority path/hash/role;
- a deterministic face-free plate must include source path/hash plus exact
  crop or mask transform provenance and must declare `contains_face=false`;
- any input under a denied historical output prefix fails even when accepted;
- an attempt output path must be beneath `outputs/recovery/`;
- `strict_recovery_pass` requires assessable identity, fewer than two major
  identity-axis differences, no outfit hard fail, and an explicit user pass;
- S23 dependency must be exactly `S22`.

The CLI derives `pack_root` from the script location and repository root from
`pack_root.parents[2]`. It prints one line per error and exits 1, or prints the
status counts plus `STRICT RECOVERY VALIDATION PASSED` and exits 0.

End the implementation with the executable entrypoint:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run tests until all pass**

Run:

```bash
python3 -m unittest discover -s scripts/tests -v
```

Expected: 7 tests, all `ok`.

- [ ] **Step 5: Run the validator against the real handoff**

Run:

```bash
python3 scripts/validate_strict_identity_recovery.py
```

Expected output includes:

```text
keep_final_only=1
manual_regate=5
rebuild_priority=11
rebuild_after_anchor=6
keep_rejected=1
STRICT RECOVERY VALIDATION PASSED
```

No Git commit is made; verify no image file has a modification time newer than
the Task 1 start time.

---

### Task 4: Final integrity report and manual re-gate handoff

**Files:**

- Create:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/STRICT-RECOVERY-VALIDATION.md`
- Create:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/STRICT-RECOVERY-SHA256SUMS`

**Interfaces:**

- Consumes: all Task 1-3 outputs and their live validation results.
- Produces: a reproducible local handoff report and the user's next identity
  decision gate for S03, S04, S07, S13, and S14.

- [ ] **Step 1: Run the complete recovery verification serially**

Run from handoff root:

```bash
python3 -m unittest discover -s scripts/tests -v
python3 scripts/validate_strict_identity_recovery.py
```

Then run repository Markdown lint and targeted lint for the ignored handoff
Markdown. All commands must exit 0.

- [ ] **Step 2: Write the validation report from actual output**

Record:

- date and series ID;
- verified attachment hash;
- unchanged historical source hashes;
- exact audit counts;
- unit-test and validator commands/results;
- explicit confirmation that global/bundled skills, prompts, historical state,
  existing images, and original checksums were not changed;
- explicit confirmation that no image generation/editing occurred;
- the five `awaiting_user_verdict` shot IDs.

- [ ] **Step 3: Create and verify recovery-only checksums**

List only the two edited routing docs and all newly added recovery files. Do not
include `STRICT-RECOVERY-SHA256SUMS` itself and do not rewrite the original
handoff `SHA256SUMS`.

Run:

```bash
sha256sum --check STRICT-RECOVERY-SHA256SUMS
```

Expected: every listed file reports `OK`.

- [ ] **Step 4: Confirm workspace isolation**

Run repository `git status --short` and compare it with the pre-task snapshot.
Expected: the ignored handoff changes do not appear; all pre-existing unrelated
tracked/untracked changes remain untouched.

- [ ] **Step 5: Present the manual re-gate to the user**

Show the existing audit evidence for S03, S04, S07, S13, and S14. Ask only for
the strict identity verdict; do not combine it with anatomy, composition,
outfit, or scene quality. Do not change the five pending rows until the user
answers.

No image generation follows this task. A later user message must explicitly
authorize any crop, mask, face-free plate, generation, edit, or regeneration.

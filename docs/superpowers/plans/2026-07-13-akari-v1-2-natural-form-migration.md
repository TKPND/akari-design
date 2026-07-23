# Akari v1.2 Natural Form Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the pre-Natural Form Akari v1.2 system into a runnable legacy workspace and initialize a validated, provenance-locked `akari-v1.2/` Natural Form package.

**Architecture:** Treat `legacy/akari-v1.2-pre-natural-form/` as a self-contained executable archive whose commands run with that directory as their working root. Keep Natural Form data in `akari-v1.2/`, validate its YAML contracts from a root-level Python command, and allow legacy images into the canonical package only as copied, hashed reference snapshots.

**Tech Stack:** Python 3.11+, `unittest`, PyYAML 6.x, Pillow, Node/npm scripts, Markdown, JSON/YAML manifests, SHA-256.

## Global Constraints

- Preserve `dist/akari-v1.1-settings.pdf` and all existing v1.1 build and audit workflows.
- Move face-hair, turnaround, motion, and overhead-room together; do not delete their assets, reviews, tests, scripts, or history.
- Keep the legacy focused baseline at 137 passing tests.
- Use `legacy:v1-2:*` for every pre-Natural Form command; unqualified v1.2 names are reserved for Natural Form.
- Do not generate or accept C01-C07 or D01 images in this migration.
- Do not read legacy working images directly from Natural Form runtime contracts.
- Every copied reference must record source path, copied path, SHA-256, role, inheritance class, and reuse rationale.
- Keep generated candidate folders ignored unless the user explicitly asks to commit a final deliverable.
- Run Node/npm commands through `bash -lc` so the repository's fnm-managed Node is available.

---

## File Structure

### Runnable legacy workspace

- `legacy/akari-v1.2-pre-natural-form/README.md`: archive identity, boundaries, and command index.
- `legacy/akari-v1.2-pre-natural-form/MIGRATION_BASELINE.md`: pre-move test result and inventory boundary.
- `legacy/akari-v1.2-pre-natural-form/docs/{specs,plans}/`: the five old specs and five old plans.
- `legacy/akari-v1.2-pre-natural-form/scripts/`: the 15 existing pre-Natural Form Python modules.
- `legacy/akari-v1.2-pre-natural-form/tests/`: the 17 existing focused test modules.
- `legacy/akari-v1.2-pre-natural-form/source/{manifests,finished,references,generated}/`: old inputs and outputs.
- `legacy/akari-v1.2-pre-natural-form/evidence/`: old reviews and ignored contact sheets.
- `legacy/akari-v1.2-pre-natural-form/dist/`: the old turnaround contact sheet.

Execution correction approved on 2026-07-13: the old manifests also depended
on selected v1.1 originals, Tonari face references, and two generated body
anchors outside the old v1.2 directories. Copy those exact inputs into the
same relative paths under the legacy root, and retain a legacy-local
`package.json` and `.gitignore`, so the 137 characterization tests and old
internal commands remain self-contained. Repository-root callers still use
only the `legacy:v1-2:*` namespace.

### Canonical Natural Form package

- `akari-v1.2/README.md`: package status, phases, commands, and directory contract.
- `akari-v1.2/docs/akari-v1.2-core-design.md`: exact approved Draft 0.2 supplied by the user.
- `akari-v1.2/docs/akari-v1.2-review-guide.md`: operational gate order and review rules.
- `akari-v1.2/docs/akari-v1.2-change-summary.md`: v1.1 inheritance and legacy relationship.
- `akari-v1.2/docs/akari-v1.2-daily-handoff.md`: D01 boundary and Daily prerequisites.
- `akari-v1.2/manifest/assets.yaml`: C01-C07 and D01 deliverable contract.
- `akari-v1.2/manifest/inheritance.yaml`: copied-reference provenance and hashes.
- `akari-v1.2/manifest/review-log.yaml`: legal states, severities, and initially empty review list.
- `akari-v1.2/references/{v1.1,legacy}/`: immutable reference snapshots.
- `scripts/validate_akari_v1_2_natural_form.py`: canonical manifest and reference validator.
- `tests/test_akari_v1_2_natural_form_package.py`: package, contract, provenance, and isolation tests.

---

### Task 1: Relocate the pre-Natural Form system as a runnable archive

**Files:**

- Create: `legacy/akari-v1.2-pre-natural-form/README.md`
- Create: `legacy/akari-v1.2-pre-natural-form/MIGRATION_BASELINE.md`
- Move: the 15 `scripts/*v1_2*.py` files to `legacy/akari-v1.2-pre-natural-form/scripts/`
- Move: the 17 `tests/test_v1_2*.py` files to `legacy/akari-v1.2-pre-natural-form/tests/`
- Move: old v1.2 specs, plans, source directories, evidence directories, and turnaround contact sheet into the matching legacy subdirectories
- Modify: `.gitignore`
- Modify: `package.json`

**Interfaces:**

- Consumes: current repository-relative `source/`, `evidence/`, and `dist/` paths interpreted through each module's `ROOT` constant.
- Produces: legacy commands that execute after `cd legacy/akari-v1.2-pre-natural-form`, plus `npm run test:python:legacy-v1-2` with 137 passing tests.

- [ ] **Step 1: Record the pre-move focused baseline**

Run:

```bash
bash -lc "uv run python -m unittest discover -s tests -p 'test_v1_2*.py'"
```

Expected: `Ran 137 tests` followed by `OK`.

- [ ] **Step 2: Create the legacy root and baseline record**

Use `apply_patch` to create `MIGRATION_BASELINE.md` with this exact content:

```markdown
# Pre-Natural Form Migration Baseline

- Recorded: 2026-07-13
- Focused command: `uv run python -m unittest discover -s tests -p 'test_v1_2*.py'`
- Result: 137 tests passed
- Collections: face-hair, turnaround, motion, overhead-room
- Rule: generated candidates and ignored contact sheets move when present but remain ignored
```

- [ ] **Step 3: Move tracked implementation and evidence**

Use `mkdir -p` followed by `git mv` for these exact groups:

```bash
mkdir -p legacy/akari-v1.2-pre-natural-form/{docs/specs,docs/plans,scripts,tests,source/manifests,source/finished,source/references,evidence,dist}
git mv scripts/*v1_2*.py legacy/akari-v1.2-pre-natural-form/scripts/
git mv tests/test_v1_2*.py legacy/akari-v1.2-pre-natural-form/tests/
git mv docs/superpowers/specs/2026-07-08-akari-v1-2-face-hair-design.md legacy/akari-v1.2-pre-natural-form/docs/specs/
git mv docs/superpowers/specs/2026-07-08-akari-v1-2-hair-symbol-bangs-design.md legacy/akari-v1.2-pre-natural-form/docs/specs/
git mv docs/superpowers/specs/2026-07-10-akari-v1-2-turnaround-motion-design.md legacy/akari-v1.2-pre-natural-form/docs/specs/
git mv docs/superpowers/specs/2026-07-13-akari-v1-2-representative-motion-poses-design.md legacy/akari-v1.2-pre-natural-form/docs/specs/
git mv docs/superpowers/specs/2026-07-13-akari-v1-2-overhead-room-portraits-design.md legacy/akari-v1.2-pre-natural-form/docs/specs/
git mv docs/superpowers/plans/2026-07-08-akari-v1-2-face-hair.md legacy/akari-v1.2-pre-natural-form/docs/plans/
git mv docs/superpowers/plans/2026-07-08-akari-v1-2-hair-symbol-bangs.md legacy/akari-v1.2-pre-natural-form/docs/plans/
git mv docs/superpowers/plans/2026-07-10-akari-v1-2-canonical-turnaround.md legacy/akari-v1.2-pre-natural-form/docs/plans/
git mv docs/superpowers/plans/2026-07-13-akari-v1-2-representative-motion-poses.md legacy/akari-v1.2-pre-natural-form/docs/plans/
git mv docs/superpowers/plans/2026-07-13-akari-v1-2-overhead-room-portraits.md legacy/akari-v1.2-pre-natural-form/docs/plans/
git mv source/manifests/v1-2-* legacy/akari-v1.2-pre-natural-form/source/manifests/
git mv source/finished/v1-2-* legacy/akari-v1.2-pre-natural-form/source/finished/
git mv source/references/v1-2-* legacy/akari-v1.2-pre-natural-form/source/references/
git mv evidence/v1-2-* legacy/akari-v1.2-pre-natural-form/evidence/
git mv dist/akari-v1.2-turnaround-contact-sheet.webp legacy/akari-v1.2-pre-natural-form/dist/
```

Expected: `git status --short` reports renames for every old tracked v1.2 path; the Natural Form migration spec and this plan remain under `docs/superpowers/`.

- [ ] **Step 4: Move ignored candidate directories when present**

Run this exact idempotent loop:

```bash
mkdir -p legacy/akari-v1.2-pre-natural-form/source/generated
for collection in face-hair turnaround motion overhead-room; do
  source_path="source/generated/v1-2-${collection}"
  if test -d "$source_path"; then
    mv "$source_path" legacy/akari-v1.2-pre-natural-form/source/generated/
  fi
done
```

Expected on the current checkout: no generated candidate directory is present, so the loop succeeds without moving a directory. If later execution finds one, it moves intact.

- [ ] **Step 5: Add the archive README**

Use `apply_patch` to create `legacy/akari-v1.2-pre-natural-form/README.md`:

````markdown
# Akari v1.2 Pre-Natural Form Legacy

This runnable archive preserves the earlier Akari v1.2 face-hair, eight-view
turnaround, representative motion, and overhead-room work. It is not the
canonical Natural Form Core package.

Run commands from the repository root through the `legacy:v1-2:*` npm
namespace. Runtime paths inside old manifests are relative to this legacy
root. Natural Form may reuse an image only by copying it into
`akari-v1.2/references/legacy/` and recording its provenance and SHA-256.

Focused verification:

```sh
npm run test:python:legacy-v1-2
```
````

- [ ] **Step 6: Replace old ignore paths with legacy paths**

Use `apply_patch` to replace the eight old v1.2 ignore entries in `.gitignore` with:

```gitignore
legacy/akari-v1.2-pre-natural-form/source/generated/v1-2-face-hair/
legacy/akari-v1.2-pre-natural-form/evidence/v1-2-face-hair/
legacy/akari-v1.2-pre-natural-form/source/generated/v1-2-turnaround/
legacy/akari-v1.2-pre-natural-form/evidence/v1-2-turnaround/contact-sheets/
legacy/akari-v1.2-pre-natural-form/source/generated/v1-2-motion/
legacy/akari-v1.2-pre-natural-form/evidence/v1-2-motion/contact-sheets/
legacy/akari-v1.2-pre-natural-form/source/generated/v1-2-overhead-room/
legacy/akari-v1.2-pre-natural-form/evidence/v1-2-overhead-room/contact-sheets/batches/
```

- [ ] **Step 7: Replace the old npm command namespace**

Use `apply_patch` to remove every unqualified old `build:v1-2-*` and `promote:v1-2-*` entry and add these scripts to `package.json`:

```json
"test:python:root": "uv run python -m unittest discover -s tests",
"test:python:legacy-v1-2": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m unittest discover -s tests",
"test:python": "npm run test:python:root && npm run test:python:legacy-v1-2",
"legacy:v1-2:face-hair:contact-sheet": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_face_hair_contact_sheet",
"legacy:v1-2:turnaround:requests": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_turnaround_generation_requests",
"legacy:v1-2:turnaround:contact-sheet": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_turnaround_contact_sheet",
"legacy:v1-2:turnaround:promote": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.promote_v1_2_turnaround_candidate",
"legacy:v1-2:motion:handoff": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_motion_handoff",
"legacy:v1-2:motion:requests": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_motion_generation_requests",
"legacy:v1-2:motion:contact-sheet": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_motion_contact_sheet",
"legacy:v1-2:motion:promote": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.promote_v1_2_motion_candidate",
"legacy:v1-2:overhead-room:reference-pack": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_overhead_room_reference_pack",
"legacy:v1-2:overhead-room:requests": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_overhead_room_generation_requests",
"legacy:v1-2:overhead-room:contact-sheet": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.build_v1_2_overhead_room_contact_sheet",
"legacy:v1-2:overhead-room:promote": "cd legacy/akari-v1.2-pre-natural-form && uv run python -m scripts.promote_v1_2_overhead_room_candidate"
```

Keep all unrelated scripts unchanged.

- [ ] **Step 8: Verify the moved archive**

Run:

```bash
bash -lc 'npm run test:python:legacy-v1-2'
bash -lc 'npm run legacy:v1-2:turnaround:requests -- --help'
bash -lc 'npm run legacy:v1-2:motion:requests -- --help'
bash -lc 'npm run legacy:v1-2:overhead-room:requests -- --help'
```

Expected: 137 legacy tests pass; each CLI exits 0 and prints usage without changing manifests.

- [ ] **Step 9: Verify no pre-Natural Form implementation remains at canonical old paths**

Run:

```bash
test -z "$(find scripts tests source evidence dist -maxdepth 3 \( -iname '*v1-2*' -o -iname '*v1_2*' -o -iname '*v1.2*' \) -print)"
```

Expected: exit 0 with no output. The check intentionally excludes `docs/superpowers/`, which contains the approved migration spec and plan.

- [ ] **Step 10: Commit the runnable archive**

```bash
git add .gitignore package.json legacy/akari-v1.2-pre-natural-form
git add -u docs scripts tests source evidence dist
git commit -m "refactor: archive pre-Natural Form v1.2"
```

---

### Task 2: Initialize the canonical Natural Form package and documentation

**Files:**

- Create: `akari-v1.2/README.md`
- Create: `akari-v1.2/docs/akari-v1.2-core-design.md`
- Create: `akari-v1.2/docs/akari-v1.2-review-guide.md`
- Create: `akari-v1.2/docs/akari-v1.2-change-summary.md`
- Create: `akari-v1.2/docs/akari-v1.2-daily-handoff.md`
- Create: `.gitkeep` files under the empty candidate, accepted, comparison, and release directories
- Create: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: the user-approved attachment `/path/to/attachment/akari-v1.2-core-design-draft-0.2.md`.
- Produces: `PACKAGE_ROOT = ROOT / "akari-v1.2"` and the stable documentation/file layout used by later manifest tests.

- [ ] **Step 1: Write the failing package-layout test**

Create `tests/test_akari_v1_2_natural_form_package.py` with:

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"


class NaturalFormPackageTests(unittest.TestCase):
    def test_required_documentation_exists(self):
        expected = {
            "README.md",
            "docs/akari-v1.2-core-design.md",
            "docs/akari-v1.2-review-guide.md",
            "docs/akari-v1.2-change-summary.md",
            "docs/akari-v1.2-daily-handoff.md",
        }
        actual = {
            path.relative_to(PACKAGE_ROOT).as_posix()
            for path in PACKAGE_ROOT.rglob("*.md")
        }
        self.assertTrue(expected.issubset(actual))

    def test_core_design_is_the_approved_draft(self):
        text = (PACKAGE_ROOT / "docs/akari-v1.2-core-design.md").read_text()
        self.assertIn("**Version:** Draft 0.2", text)
        self.assertIn("**Codename:** Natural Form", text)
        self.assertIn("**Status:** Design Approved / Pre-production", text)

    def test_working_directories_are_tracked(self):
        expected = (
            "source/candidates/.gitkeep",
            "source/rejected/.gitkeep",
            "source/superseded/.gitkeep",
            "accepted/core/standing/.gitkeep",
            "accepted/core/sitting/.gitkeep",
            "accepted/core/face-hair/.gitkeep",
            "accepted/core/indoor-feet/.gitkeep",
            "accepted/daily-validation/.gitkeep",
            "comparisons/.gitkeep",
            "release/.gitkeep",
        )
        for relative_path in expected:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((PACKAGE_ROOT / relative_path).is_file())
```

- [ ] **Step 2: Run the package test to verify it fails**

Run:

```bash
bash -lc 'uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v'
```

Expected: FAIL because `akari-v1.2/` does not exist.

- [ ] **Step 3: Copy the approved Core design and create tracked directories**

Copy the attachment to `akari-v1.2/docs/akari-v1.2-core-design.md`, then prepend
`<!-- markdownlint-disable MD024 MD025 MD036 -->` so its approved repeated H1,
duplicate review headings, and emphasized labels remain unchanged while the
repository lint passes. Create the ten `.gitkeep` files asserted by the test.
Use `apply_patch` for the new short Markdown files.

- [ ] **Step 4: Write the package README**

Create `akari-v1.2/README.md` with these exact operational facts:

````markdown
# Akari v1.2 Natural Form

Status: Design Approved / Pre-production.

This is the canonical Akari v1.2 package. It preserves the v1.1 identity lock
and adds natural posture, weight balance, relaxed body state, morning state,
and daily micro-expressions.

Production order:

1. Phase 1: C01, C02, and both C03 views.
2. Phase 2: C04 and both C07 variants.
3. Phase 3: C05 and C06-1 through C06-4.
4. Phase 4: D01 validation.

Validate package contracts from the repository root:

```sh
npm run validate:v1-2
```

The previous face-hair, eight-view turnaround, motion, and overhead-room work
lives under `legacy/akari-v1.2-pre-natural-form/`. It is reference history,
not automatically accepted Natural Form material.
````

- [ ] **Step 5: Write the three operational handoff documents**

Create concise documents with these required sections and statements:

`akari-v1.2/docs/akari-v1.2-review-guide.md`:

```markdown
# Akari v1.2 Review Guide

Review in this order: Identity, Body, State, Rendering, Production. Stop when a
Blocker appears; do not let presentation quality hide an identity or anatomy
failure. C01-C07 require `accepted` for release. D01 may be
`accepted-with-notes` only when all Core assets are accepted.

Blocker means rejection. Major normally requires correction. Minor may be
recorded without reopening an otherwise accepted asset. For C04, inspect
pelvis, thigh, knee, shin, ankle, toe, then whole-body weight balance. For D01,
trace every observed problem back to C04, C05, C06, or C07 before editing the
scene alone.
```

`akari-v1.2/docs/akari-v1.2-change-summary.md`:

```markdown
# Akari v1.2 Change Summary

Natural Form inherits the v1.1 face, hair, ornament side, palette, body type,
standard outfit, socks, sneakers, and bag. It extends the model with natural
standing, floor sitting, indoor sock feet, morning bed hair, sleepiness,
micro-expression continuity, morning roomwear, and indoor context.

The pre-Natural Form v1.2 work is preserved as a runnable legacy archive. A
legacy image becomes a Natural Form reference only after copying, hashing, and
recording its role in `manifest/inheritance.yaml`.
```

`akari-v1.2/docs/akari-v1.2-daily-handoff.md`:

```markdown
# Akari v1.2 Daily Handoff

D01 is the only Daily scene allowed before formal Core release. It validates
C04 floor sitting, C05 morning hair, C06-1 or C06-2 expression, and C07 indoor
sock feet in one morning bedside scene.

Broader Daily production begins only after Gate 4 and the final Core acceptance
gate pass. A D01 failure must reopen the controlling Core asset when the cause
is structural; scene-only corrections are for lighting, background, or staging
problems that do not change the Core rule.
```

- [ ] **Step 6: Run the package tests and Markdown lint**

Run:

```bash
bash -lc 'uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v'
bash -lc 'npm run lint:md'
```

Expected: three package tests pass and Markdown lint reports 0 errors.

- [ ] **Step 7: Commit the canonical package shell**

```bash
git add akari-v1.2 tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: initialize Akari v1.2 Natural Form package"
```

---

### Task 3: Define and validate the Natural Form asset and review contracts

**Files:**

- Create: `akari-v1.2/manifest/assets.yaml`
- Create: `akari-v1.2/manifest/review-log.yaml`
- Create: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`
- Modify: `pyproject.toml`
- Modify: `requirements.txt`
- Modify: `uv.lock`

**Interfaces:**

- Produces: `load_yaml(path: Path) -> dict`, `validate_assets(data: dict) -> None`, `validate_review_log(data: dict) -> None`, and `ValidationError`.
- Consumed by: Task 4 provenance validation and Task 5 command integration.

- [ ] **Step 1: Add PyYAML through the locked dependency workflow**

Run:

```bash
bash -lc "uv add 'PyYAML>=6,<7'"
```

Expected: `pyproject.toml` gains `pyyaml>=6,<7` and `uv.lock` records the resolved 6.x package.

Add the same `pyyaml>=6,<7` line to `requirements.txt`; the repository's
environment contract requires it to match `project.dependencies` exactly.

- [ ] **Step 2: Add failing asset and review validation tests**

Append these imports and tests to `tests/test_akari_v1_2_natural_form_package.py`:

```python
import copy
import sys

sys.path.insert(0, str(ROOT))

from scripts.validate_akari_v1_2_natural_form import (
    ValidationError,
    load_yaml,
    validate_assets,
    validate_review_log,
)


class NaturalFormManifestTests(unittest.TestCase):
    def setUp(self):
        self.assets = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        self.review_log = load_yaml(PACKAGE_ROOT / "manifest/review-log.yaml")

    def test_assets_define_the_exact_core_and_daily_contract(self):
        validate_assets(self.assets)
        self.assertEqual(
            [item["asset_id"] for item in self.assets["assets"]],
            ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "D01"],
        )

    def test_assets_reject_an_accepted_item_without_an_accepted_path(self):
        invalid = copy.deepcopy(self.assets)
        invalid["assets"][0]["status"] = "accepted"
        with self.assertRaisesRegex(ValidationError, "accepted_path"):
            validate_assets(invalid)

    def test_assets_reject_an_unknown_dependency(self):
        invalid = copy.deepcopy(self.assets)
        invalid["assets"][-1]["depends_on"] = ["C99"]
        with self.assertRaisesRegex(ValidationError, "unknown dependency"):
            validate_assets(invalid)

    def test_review_log_starts_empty_with_exact_enums(self):
        validate_review_log(self.review_log)
        self.assertEqual(self.review_log["reviews"], [])
```

- [ ] **Step 3: Run the manifest tests to verify they fail**

Run:

```bash
bash -lc 'uv run python -m unittest tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests -v'
```

Expected: ERROR with `ModuleNotFoundError` for the validator.

- [ ] **Step 4: Create the exact asset and review manifests**

Create `assets.yaml` with ordered IDs and these exact variant/dependency tuples:

```yaml
schema_version: 1
collection: akari-v1.2-natural-form-core
assets:
  - {asset_id: C01, descriptor: front-natural-stance, phase: 1, variants: [default], depends_on: [], gate: identity, status: candidate, revision: r00, accepted_path: null}
  - {asset_id: C02, descriptor: back-natural-stance, phase: 1, variants: [default], depends_on: [C01], gate: identity, status: candidate, revision: r00, accepted_path: null}
  - {asset_id: C03, descriptor: natural-stance-45, phase: 1, variants: [hairpin-side-45, non-hairpin-side-45], depends_on: [C01], gate: identity, status: candidate, revision: r00, accepted_path: null}
  - {asset_id: C04, descriptor: floor-sitting, phase: 2, variants: [default], depends_on: [C01, C02, C03], gate: body, status: candidate, revision: r00, accepted_path: null}
  - {asset_id: C05, descriptor: morning-bedhair, phase: 3, variants: [default], depends_on: [C01], gate: state, status: candidate, revision: r00, accepted_path: null}
  - {asset_id: C06, descriptor: daily-smile-gradient, phase: 3, variants: [sleepy-neutral, sleepy-secure, loosened-mouth, soft-smile], depends_on: [C05], gate: state, status: candidate, revision: r00, accepted_path: null}
  - {asset_id: C07, descriptor: indoor-sock-feet, phase: 2, variants: [standing, seated], depends_on: [C01, C04], gate: body, status: candidate, revision: r00, accepted_path: null}
  - {asset_id: D01, descriptor: morning-bedside, phase: 4, variants: [default], depends_on: [C04, C05, C06, C07], gate: daily, status: candidate, revision: r00, accepted_path: null}
```

Create `review-log.yaml`:

```yaml
schema_version: 1
allowed_statuses: [candidate, review, accepted, accepted-with-notes, rejected, superseded]
allowed_severities: [blocker, major, minor]
reviews: []
```

- [ ] **Step 5: Implement the minimal validator**

Create `scripts/validate_akari_v1_2_natural_form.py` with these public contracts and checks:

```python
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
ASSET_IDS = ("C01", "C02", "C03", "C04", "C05", "C06", "C07", "D01")
STATUSES = (
    "candidate",
    "review",
    "accepted",
    "accepted-with-notes",
    "rejected",
    "superseded",
)
SEVERITIES = ("blocker", "major", "minor")


class ValidationError(ValueError):
    pass


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: expected mapping")
    return data


def validate_assets(data: dict) -> None:
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
        if not isinstance(variants, list) or not variants or len(variants) != len(set(variants)):
            raise ValidationError(f"{asset_id}: variants must be unique and non-empty")
        if item.get("status") not in STATUSES:
            raise ValidationError(f"{asset_id}: invalid status")
        if item.get("revision") != "r00":
            raise ValidationError(f"{asset_id}: initial revision must be r00")
        dependencies = item.get("depends_on")
        if not isinstance(dependencies, list):
            raise ValidationError(f"{asset_id}: depends_on must be a list")
        unknown = set(dependencies) - known
        if unknown:
            raise ValidationError(f"{asset_id}: unknown dependency {sorted(unknown)}")
        accepted_path = item.get("accepted_path")
        if item["status"] in {"accepted", "accepted-with-notes"} and not accepted_path:
            raise ValidationError(f"{asset_id}: accepted_path is required")
        if item["status"] not in {"accepted", "accepted-with-notes"} and accepted_path is not None:
            raise ValidationError(f"{asset_id}: accepted_path must be null")


def validate_review_log(data: dict) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("review-log: schema_version must be 1")
    if tuple(data.get("allowed_statuses", ())) != STATUSES:
        raise ValidationError("review-log: allowed_statuses mismatch")
    if tuple(data.get("allowed_severities", ())) != SEVERITIES:
        raise ValidationError("review-log: allowed_severities mismatch")
    if data.get("reviews") != []:
        raise ValidationError("review-log: initial reviews must be empty")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT)
    args = parser.parse_args()
    manifest_root = args.package_root / "manifest"
    assets = load_yaml(manifest_root / "assets.yaml")
    review_log = load_yaml(manifest_root / "review-log.yaml")
    validate_assets(assets)
    validate_review_log(review_log)
    print(f"validated {len(assets['assets'])} assets and an empty review log")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Run the contract tests**

Run:

```bash
bash -lc 'uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v'
bash -lc 'uv run python scripts/validate_akari_v1_2_natural_form.py'
```

Expected: seven tests pass; the CLI prints `validated 8 assets and an empty review log`.

- [ ] **Step 7: Commit the asset contracts**

```bash
git add pyproject.toml uv.lock akari-v1.2/manifest/assets.yaml akari-v1.2/manifest/review-log.yaml scripts/validate_akari_v1_2_natural_form.py tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: validate Natural Form asset contracts"
```

---

### Task 4: Snapshot and validate v1.1 and legacy references

**Files:**

- Create: `akari-v1.2/references/v1.1/` copies
- Create: `akari-v1.2/references/legacy/` copies
- Create: `akari-v1.2/manifest/inheritance.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: `load_yaml()` and `ValidationError` from Task 3.
- Produces: `sha256_file(path: Path) -> str` and `validate_inheritance(data: dict, repository_root: Path, package_root: Path) -> None`.

- [ ] **Step 1: Add failing provenance tests**

Append:

```python
from scripts.validate_akari_v1_2_natural_form import validate_inheritance


class NaturalFormInheritanceTests(unittest.TestCase):
    def setUp(self):
        self.data = load_yaml(PACKAGE_ROOT / "manifest/inheritance.yaml")

    def test_reference_snapshots_have_valid_provenance_and_hashes(self):
        validate_inheritance(self.data, ROOT, PACKAGE_ROOT)

    def test_changed_hash_is_rejected(self):
        invalid = copy.deepcopy(self.data)
        invalid["references"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValidationError, "SHA-256 mismatch"):
            validate_inheritance(invalid, ROOT, PACKAGE_ROOT)

    def test_duplicate_controlling_role_is_rejected(self):
        invalid = copy.deepcopy(self.data)
        invalid["references"][1]["role"] = invalid["references"][0]["role"]
        with self.assertRaisesRegex(ValidationError, "duplicate role"):
            validate_inheritance(invalid, ROOT, PACKAGE_ROOT)

    def test_copied_paths_cannot_point_into_legacy(self):
        invalid = copy.deepcopy(self.data)
        invalid["references"][0]["copied_path"] = invalid["references"][0]["source_path"]
        with self.assertRaisesRegex(ValidationError, "copied_path"):
            validate_inheritance(invalid, ROOT, PACKAGE_ROOT)
```

- [ ] **Step 2: Run the provenance tests to verify they fail**

Run:

```bash
bash -lc 'uv run python -m unittest tests.test_akari_v1_2_natural_form_package.NaturalFormInheritanceTests -v'
```

Expected: ERROR because `inheritance.yaml` and `validate_inheritance` do not exist.

- [ ] **Step 3: Copy the exact reference snapshot set**

Copy these sources without conversion or metadata editing:

```text
source/palette/akari-v1.1-palette.json -> akari-v1.2/references/v1.1/akari-v1.1-palette.json
source/originals/v1_1_front_1.webp -> akari-v1.2/references/v1.1/front.webp
source/originals/v1_1_back.webp -> akari-v1.2/references/v1.1/back.webp
source/originals/v1_1_髪飾り側_45deg.webp -> akari-v1.2/references/v1.1/hairpin-side-45.webp
source/originals/v1_1_非髪飾り側45deg.webp -> akari-v1.2/references/v1.1/non-hairpin-side-45.webp
source/originals/v1_1_standard_foot_set.webp -> akari-v1.2/references/v1.1/standard-foot-set.webp
source/originals/v1_1_shoes.webp -> akari-v1.2/references/v1.1/shoes.webp
legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp -> akari-v1.2/references/legacy/standard-face.webp
legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-turnaround/front.webp -> akari-v1.2/references/legacy/front.webp
legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-turnaround/back.webp -> akari-v1.2/references/legacy/back.webp
legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-turnaround/character-left-front-three-quarter.webp -> akari-v1.2/references/legacy/character-left-front-three-quarter.webp
legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-turnaround/character-right-front-three-quarter.webp -> akari-v1.2/references/legacy/character-right-front-three-quarter.webp
legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-motion/seated.webp -> akari-v1.2/references/legacy/seated.webp
```

Expected: 7 v1.1 snapshots and 6 legacy snapshots.

- [ ] **Step 4: Create the inheritance manifest with real hashes**

Create 13 ordered records in `inheritance.yaml`. Use these exact role and class mappings; calculate each `sha256` from the copied bytes:

```yaml
schema_version: 1
references:
  - {role: palette, inheritance_class: inherited, source_path: source/palette/akari-v1.1-palette.json, copied_path: akari-v1.2/references/v1.1/akari-v1.1-palette.json, source_collection: v1.1, reuse_rationale: D65 sRGB object colors, sha256: 3dc24ce693e9f2e43081042d6856f13fed313e4dc1e6b3543d5aaaa188d96332}
  - {role: v1.1-front-identity, inheritance_class: inherited, source_path: source/originals/v1_1_front_1.webp, copied_path: akari-v1.2/references/v1.1/front.webp, source_collection: v1.1, reuse_rationale: face body and standard outfit lock, sha256: 6b2896e98657ca4079ea94652c16bb05285c1626f255cd08ea1e56f298151f9a}
  - {role: v1.1-back-identity, inheritance_class: inherited, source_path: source/originals/v1_1_back.webp, copied_path: akari-v1.2/references/v1.1/back.webp, source_collection: v1.1, reuse_rationale: back hair and outfit lock, sha256: 77449961e7ae3eebe54be20ee428795fed8b897a08d9dc7c15319315773154f3}
  - {role: v1.1-hairpin-side-45, inheritance_class: inherited, source_path: source/originals/v1_1_髪飾り側_45deg.webp, copied_path: akari-v1.2/references/v1.1/hairpin-side-45.webp, source_collection: v1.1, reuse_rationale: character-left ornament and cheek silhouette, sha256: dd144b66f5228934ca95060467ec96f9ef33f38315a3e7a7c70074111cf85a50}
  - {role: v1.1-non-hairpin-side-45, inheritance_class: inherited, source_path: source/originals/v1_1_非髪飾り側45deg.webp, copied_path: akari-v1.2/references/v1.1/non-hairpin-side-45.webp, source_collection: v1.1, reuse_rationale: opposite cheek and bob silhouette, sha256: 76b95abbffedb77f392bda065b60f5c9194310996af418b59913868025ac3853}
  - {role: v1.1-indoor-foot-base, inheritance_class: inherited, source_path: source/originals/v1_1_standard_foot_set.webp, copied_path: akari-v1.2/references/v1.1/standard-foot-set.webp, source_collection: v1.1, reuse_rationale: sock stripe and foot construction, sha256: 5b4175d87a813f4887cbf3e3361f4007acffa5a25cccfb19ecec431447b4978b}
  - {role: v1.1-shoe-base, inheritance_class: inherited, source_path: source/originals/v1_1_shoes.webp, copied_path: akari-v1.2/references/v1.1/shoes.webp, source_collection: v1.1, reuse_rationale: inherited sneaker construction, sha256: acc31bf31a55b770388b796b34f2b57dbeb48dc2fb974fe8e6896d0cda70f344}
  - {role: legacy-face-comparison, inheritance_class: reference-only, source_path: legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp, copied_path: akari-v1.2/references/legacy/standard-face.webp, source_collection: pre-natural-form, reuse_rationale: compare the previous accepted face direction without granting acceptance, sha256: e130b7e00d98d02fc05f139ddc3b01f206e7eabf61987e4ad385ed7870fadb66}
  - {role: legacy-front-comparison, inheritance_class: reference-only, source_path: legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-turnaround/front.webp, copied_path: akari-v1.2/references/legacy/front.webp, source_collection: pre-natural-form, reuse_rationale: compare corrected front proportions and stance, sha256: 7b17fb7169c67376a41a8bdfff4ab7d50d90ec8bf113ab1c50aba85511c92423}
  - {role: legacy-back-comparison, inheritance_class: reference-only, source_path: legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-turnaround/back.webp, copied_path: akari-v1.2/references/legacy/back.webp, source_collection: pre-natural-form, reuse_rationale: compare rear construction and body consistency, sha256: e6e9249d704fc60fdbb1ea298dcfc05b43645ffe3b5ec3a1e52e8379e246bb5d}
  - {role: legacy-hairpin-side-45-comparison, inheritance_class: reference-only, source_path: legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-turnaround/character-left-front-three-quarter.webp, copied_path: akari-v1.2/references/legacy/character-left-front-three-quarter.webp, source_collection: pre-natural-form, reuse_rationale: compare ornament-side construction, sha256: 425a865eeef4fded914be9ca8dab089457448711b4701a339e5cda903980a412}
  - {role: legacy-non-hairpin-side-45-comparison, inheritance_class: reference-only, source_path: legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-turnaround/character-right-front-three-quarter.webp, copied_path: akari-v1.2/references/legacy/character-right-front-three-quarter.webp, source_collection: pre-natural-form, reuse_rationale: compare non-ornament-side construction, sha256: f2bc997c592c58457c08561215d529ffbcf248cc774ee1bf79abbb89a6224ea2}
  - {role: legacy-seated-anatomy-comparison, inheritance_class: reference-only, source_path: legacy/akari-v1.2-pre-natural-form/source/finished/v1-2-motion/seated.webp, copied_path: akari-v1.2/references/legacy/seated.webp, source_collection: pre-natural-form, reuse_rationale: compare pelvis leg and garment compression while redesigning C04, sha256: ecad0f6a76bcd81a4bfb7607c5bf4dd8d791d4e14aea048eeedb974ec0342b66}
```

Recompute the hashes before copying and stop if any digest differs from the
recorded value. This protects the plan from silently snapshotting changed
source material.

- [ ] **Step 5: Implement inheritance validation**

Add imports for `hashlib` and `PurePosixPath`, then add:

```python
def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_inheritance(data: dict, repository_root: Path, package_root: Path) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("inheritance: schema_version must be 1")
    references = data.get("references")
    if not isinstance(references, list) or len(references) != 13:
        raise ValidationError("inheritance: expected 13 references")
    roles: set[str] = set()
    copied_paths: set[str] = set()
    for record in references:
        role = record.get("role")
        if not isinstance(role, str) or role in roles:
            raise ValidationError(f"inheritance: duplicate role {role}")
        roles.add(role)
        if record.get("inheritance_class") not in {"inherited", "reference-only"}:
            raise ValidationError(f"{role}: invalid inheritance_class")
        source_relative = record.get("source_path")
        copied_relative = record.get("copied_path")
        if not isinstance(source_relative, str) or not isinstance(copied_relative, str):
            raise ValidationError(f"{role}: paths must be strings")
        copied_parts = PurePosixPath(copied_relative).parts
        if copied_parts[:2] != ("akari-v1.2", "references") or "legacy" in copied_parts[:1]:
            raise ValidationError(f"{role}: copied_path must be a canonical reference snapshot")
        if copied_relative in copied_paths:
            raise ValidationError(f"{role}: duplicate copied_path")
        copied_paths.add(copied_relative)
        source = repository_root / source_relative
        copied = repository_root / copied_relative
        if not source.is_file() or not copied.is_file():
            raise ValidationError(f"{role}: source and copied files must exist")
        expected = record.get("sha256")
        if not isinstance(expected, str) or len(expected) != 64:
            raise ValidationError(f"{role}: invalid SHA-256")
        if sha256_file(source) != expected or sha256_file(copied) != expected:
            raise ValidationError(f"{role}: SHA-256 mismatch")
        if not record.get("reuse_rationale"):
            raise ValidationError(f"{role}: reuse_rationale is required")
```

Also update `main()` to load `inheritance.yaml`, call `validate_inheritance(inheritance, ROOT, args.package_root)`, and print `validated 8 assets, 13 references, and an empty review log`.

- [ ] **Step 6: Run provenance and complete package tests**

Run:

```bash
bash -lc 'uv run python -m unittest tests.test_akari_v1_2_natural_form_package -v'
bash -lc 'uv run python scripts/validate_akari_v1_2_natural_form.py'
```

Expected: eleven tests pass and the CLI reports 8 assets and 13 references.

- [ ] **Step 7: Commit reference snapshots and provenance**

```bash
git add akari-v1.2/references akari-v1.2/manifest/inheritance.yaml scripts/validate_akari_v1_2_natural_form.py tests/test_akari_v1_2_natural_form_package.py
git commit -m "feat: lock Natural Form reference provenance"
```

---

### Task 5: Integrate validation, repository guidance, and full regression checks

**Files:**

- Modify: `package.json`
- Modify: `AGENTS.md`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`

**Interfaces:**

- Consumes: validator CLI from Tasks 3-4 and the legacy npm namespace from Task 1.
- Produces: `npm run validate:v1-2`, repository guidance that resolves unqualified v1.2 work to Natural Form, and full-suite verification.

- [ ] **Step 1: Add a failing command and isolation test**

Append:

```python
import json


class NaturalFormIsolationTests(unittest.TestCase):
    def test_package_command_reserves_unqualified_v1_2_for_natural_form(self):
        package = json.loads((ROOT / "package.json").read_text())
        scripts = package["scripts"]
        self.assertEqual(
            scripts["validate:v1-2"],
            "uv run python scripts/validate_akari_v1_2_natural_form.py",
        )
        old_unqualified = [
            name
            for name in scripts
            if (name.startswith("build:v1-2") or name.startswith("promote:v1-2"))
        ]
        self.assertEqual(old_unqualified, [])

    def test_runtime_contracts_do_not_point_directly_into_legacy(self):
        assets_text = (PACKAGE_ROOT / "manifest/assets.yaml").read_text()
        reviews_text = (PACKAGE_ROOT / "manifest/review-log.yaml").read_text()
        self.assertNotIn("legacy/akari-v1.2-pre-natural-form", assets_text)
        self.assertNotIn("legacy/akari-v1.2-pre-natural-form", reviews_text)
```

- [ ] **Step 2: Run the isolation tests to verify the missing command fails**

Run:

```bash
bash -lc 'uv run python -m unittest tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests -v'
```

Expected: FAIL because `validate:v1-2` is absent.

- [ ] **Step 3: Add the canonical validation command**

Add to `package.json`:

```json
"validate:v1-2": "uv run python scripts/validate_akari_v1_2_natural_form.py"
```

Do not add an unqualified generation or promotion command in this migration.

- [ ] **Step 4: Update repository guidance**

Use `apply_patch` to add a new `Akari v1.2` section to `AGENTS.md` with these exact rules:

```markdown
## Akari v1.2

- Unqualified `v1.2` means the Natural Form package under `akari-v1.2/`.
- The previous face-hair, eight-view turnaround, motion, and overhead-room work
  lives under `legacy/akari-v1.2-pre-natural-form/` and uses only
  `legacy:v1-2:*` commands.
- Do not use a legacy working path as a Natural Form generation reference.
  Copy the selected file into `akari-v1.2/references/legacy/` and record its
  role, rationale, and SHA-256 in `akari-v1.2/manifest/inheritance.yaml`.
- Run `npm run validate:v1-2` after changing Natural Form manifests or
  references.
- The default PDF remains `dist/akari-v1.1-settings.pdf` until a Natural Form
  release PDF exists and repository guidance is explicitly updated.
```

- [ ] **Step 5: Run focused validation and both Python suites**

Run:

```bash
bash -lc 'npm run validate:v1-2'
bash -lc 'npm run test:python:root'
bash -lc 'npm run test:python:legacy-v1-2'
```

Expected: Natural Form reports 8 assets and 13 references; root tests pass; legacy reports exactly 137 passing tests.

- [ ] **Step 6: Run the broad repository verification**

Run:

```bash
bash -lc 'npm run lint:md'
bash -lc 'npm run test:node'
bash -lc 'npm run test:python'
bash -lc 'npm run audit'
git diff --check
```

Expected: Markdown lint has 0 errors; Node, combined Python, and audits pass; `git diff --check` has no output.

- [ ] **Step 7: Audit path separation**

Run:

```bash
rg -n 'source/(manifests|finished|generated|references)/v1-2|evidence/v1-2|dist/akari-v1\.2-turnaround' \
  --glob '!legacy/akari-v1.2-pre-natural-form/**' \
  --glob '!docs/superpowers/**' \
  --glob '!akari-v1.2/manifest/inheritance.yaml' \
  .
```

Expected: no output. `inheritance.yaml` is excluded because its `source_path` fields intentionally identify legacy provenance.

- [ ] **Step 8: Commit integration and guidance**

```bash
git add package.json AGENTS.md tests/test_akari_v1_2_natural_form_package.py
git commit -m "chore: integrate Natural Form validation"
```

- [ ] **Step 9: Confirm final worktree and history**

Run:

```bash
git status --short
git log -5 --oneline
```

Expected: clean worktree and five implementation commits after the design and plan commits:

```text
chore: integrate Natural Form validation
feat: lock Natural Form reference provenance
feat: validate Natural Form asset contracts
feat: initialize Akari v1.2 Natural Form package
refactor: archive pre-Natural Form v1.2
```

The exact abbreviated hashes vary. There are five implementation commits in the list; the archive relocation is the first implementation commit.

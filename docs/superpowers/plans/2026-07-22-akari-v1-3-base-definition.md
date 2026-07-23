# Akari v1.3 Base Definition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and accept the six-image Akari v1.3 Base Definition package,
with reproducible provenance, review history, and focused validation gates.

**Architecture:** Create `akari-v1.3/` as an independent package and copy only
two immutable inputs into it: the approved v04 style source and the accepted
v1.2 C01 standing reference. A focused Python validator owns manifest,
provenance, lifecycle, review, and promotion integrity. Image production then
advances through four human-reviewed gates, with V13-01 and V13-02 locking the
identity before expression or wardrobe work begins.

**Tech Stack:** Python 3.11, `unittest`, PyYAML, Pillow, npm scripts,
ImageMagick, Codex `imagegen`, SHA-256, Markdown.

## Global Constraints

- `source/references/style-study/akari-v04-a.png` is the highest visual authority for face,
  amber eye finish, airy-bob silhouette, smile energy, and rendering.
- The v04 source remains immutable; V13-01 is a new artifact.
- The complete pale-blue crossed-pin and small-ribbon ornament belongs on
  character-left, normally image-right in a front-facing image.
- The v1.2 C01 reference controls only healthy leg volume, body connection,
  natural standing weight, and inherited outdoor garment facts.
- v1.2 material grants no v1.3 face, hair, ornament, age, or rendering
  authority.
- Akari must read as a young adult without assigning a fixed numerical age.
- V13-01 and V13-02 must both be accepted as the same person before V13-03 or
  V13-04 production starts.
- Every accepted Base Definition image must have an overall `pass` verdict;
  a `major` cannot be waived into an accepted anchor.
- Every promotion must be byte-identical to the selected candidate and have a
  matching SHA-256 in the review log.
- `akari-v1.3/source/candidates/` and `akari-v1.3/comparisons/` remain local and
  untracked; references, manifests, docs, and accepted assets are durable.
- Before every identity-sensitive generation, open the current anchor and all
  role-relevant references at original resolution and state each role in the
  generation prompt.
- Keep generation, comparison, validation, and image inspection serial on the
  3-core, 2 GiB host.
- Do not add a v1.3 PDF, release gate, or Daily scene package in this work.
- Do not modify any file under `akari-v1.2/` or
  `legacy/akari-v1.2-pre-natural-form/`.

---

## File Map and Interfaces

Create these durable paths:

```text
akari-v1.3/README.md
akari-v1.3/docs/akari-v1.3-base-design.md
akari-v1.3/manifest/assets.yaml
akari-v1.3/manifest/inheritance.yaml
akari-v1.3/manifest/review-log.yaml
akari-v1.3/references/style/akari-v04-a.png
akari-v1.3/references/v1.2/akari-v1.2_c01_front-natural-stance_r01.png
akari-v1.3/accepted/base/key-visual/.gitkeep
akari-v1.3/accepted/base/full-body/.gitkeep
akari-v1.3/accepted/base/expressions/.gitkeep
akari-v1.3/accepted/base/wardrobe/.gitkeep
scripts/validate_akari_v1_3_base.py
tests/test_akari_v1_3_base_package.py
```

Modify `.gitignore`, `package.json`, and
`tests/test_workflow_gate_contract.py`. Production candidates and comparison
sheets live only below the two ignored v1.3 scratch directories.

The validator exposes `ValidationError`, `load_yaml(path: Path) -> dict`,
`sha256_file(path: Path) -> str`,
`validate_assets(data: dict, package_root: Path) -> None`,
`validate_inheritance(data: dict, repo_root: Path) -> None`,
`validate_review_log(data: dict, assets: dict, package_root: Path,
require_complete: bool) -> None`, and
`validate_package(package_root: Path = PACKAGE_ROOT, repo_root: Path = ROOT,
require_complete: bool = True) -> None`.

### Task 1: Create the independent package and inheritance boundary

**Files:**

- Create: all `akari-v1.3/` docs, manifests, references, and `.gitkeep` files
  listed above.
- Modify: `.gitignore`
- Test: `tests/test_akari_v1_3_base_package.py`

**Interfaces:**

- Consumes: the approved design and two immutable source images.
- Produces: the package paths and initial manifest state used by later tasks.

- [ ] **Step 1: Write the failing package-boundary tests**

Create `tests/test_akari_v1_3_base_package.py`:

```python
from pathlib import Path
import hashlib
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.3"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    if not isinstance(data, dict):
        raise AssertionError(f"expected mapping: {path}")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class V13PackageBoundaryTests(unittest.TestCase):
    def test_required_package_files_exist(self):
        expected = (
            "README.md",
            "docs/akari-v1.3-base-design.md",
            "manifest/assets.yaml",
            "manifest/inheritance.yaml",
            "manifest/review-log.yaml",
            "references/style/akari-v04-a.png",
            "references/v1.2/akari-v1.2_c01_front-natural-stance_r01.png",
            "accepted/base/key-visual/.gitkeep",
            "accepted/base/full-body/.gitkeep",
            "accepted/base/expressions/.gitkeep",
            "accepted/base/wardrobe/.gitkeep",
        )
        for relative_path in expected:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((PACKAGE_ROOT / relative_path).is_file())

    def test_copied_references_match_sources_and_pins(self):
        pairs = (
            (
                ROOT / "source/references/style-study/akari-v04-a.png",
                PACKAGE_ROOT / "references/style/akari-v04-a.png",
                "aafad35807788120542bd650039da6f88297de8f366534ab3d2c38920100c579",
            ),
            (
                ROOT / "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
                PACKAGE_ROOT / "references/v1.2/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
                "a977f2798d15f3da9ef0d7720d6f9fc41bd2f84f54f4c8a69908a482596a75c5",
            ),
        )
        for source, copied, expected_sha in pairs:
            with self.subTest(copied=copied):
                self.assertEqual(source.read_bytes(), copied.read_bytes())
                self.assertEqual(expected_sha, sha256_file(copied))

    def test_initial_assets_define_four_ids_and_six_images(self):
        data = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        self.assertEqual(data["required_image_count"], 6)
        self.assertEqual(
            [asset["asset_id"] for asset in data["assets"]],
            ["V13-01", "V13-02", "V13-03", "V13-04"],
        )
        self.assertEqual(
            sum(len(asset["variants"]) for asset in data["assets"]), 6
        )

    def test_package_docs_keep_base_definition_scope(self):
        readme = (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8")
        design = (
            PACKAGE_ROOT / "docs/akari-v1.3-base-design.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Base Definition", readme)
        self.assertIn("V13-01", design)
        self.assertIn("V13-04B", design)
        self.assertNotIn("settings PDF", readme)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```sh
bash -lc 'uv run python -m unittest tests.test_akari_v1_3_base_package -v'
```

Expected: failure because `akari-v1.3/` does not exist.

- [ ] **Step 3: Create package docs and ignored scratch paths**

Add to `.gitignore`:

```gitignore
akari-v1.3/source/candidates/
akari-v1.3/comparisons/
```

Create `akari-v1.3/README.md` with status `Base Definition production`, the
ordered V13-01 through V13-04 production sequence, both v1.3 npm commands, and
the rule that candidates/comparisons stay local. Create
`akari-v1.3/docs/akari-v1.3-base-design.md` from sections 5, 6, 7, 9, 11, and
15 of `docs/superpowers/specs/2026-07-22-akari-v1-3-base-definition-design.md`,
preserving their headings and requirements. Retain the explicit statement that
this package adds neither broad Daily scenes nor a v1.3 settings PDF.

- [ ] **Step 4: Create the initial asset and review manifests**

Create `manifest/assets.yaml` with this contract:

```yaml
schema_version: 1
collection: akari-v1.3-base-definition
required_image_count: 6
assets:
  - asset_id: V13-01
    descriptor: corrected-key-visual
    variants: [default]
    expected_paths:
      - accepted/base/key-visual/akari-v1.3_v13-01_corrected-key-visual_rNN.png
    depends_on: []
    controlling_gate: identity
    status: planned
    revision: null
    accepted_paths: []
  - asset_id: V13-02
    descriptor: natural-full-body
    variants: [default]
    expected_paths:
      - accepted/base/full-body/akari-v1.3_v13-02_natural-full-body_rNN.png
    depends_on: [V13-01]
    controlling_gate: body
    status: planned
    revision: null
    accepted_paths: []
  - asset_id: V13-03
    descriptor: expression-pair
    variants: [everyday, bright-smile]
    expected_paths:
      - accepted/base/expressions/akari-v1.3_v13-03a_everyday_rNN.png
      - accepted/base/expressions/akari-v1.3_v13-03b_bright-smile_rNN.png
    depends_on: [V13-01, V13-02]
    controlling_gate: expression
    status: planned
    revision: null
    accepted_paths: []
  - asset_id: V13-04
    descriptor: wardrobe-pair
    variants: [outdoor, roomwear]
    expected_paths:
      - accepted/base/wardrobe/akari-v1.3_v13-04a_outdoor_rNN.png
      - accepted/base/wardrobe/akari-v1.3_v13-04b_roomwear_rNN.png
    depends_on: [V13-01, V13-02]
    controlling_gate: wardrobe
    status: planned
    revision: null
    accepted_paths: []
```

Create `manifest/review-log.yaml`:

```yaml
schema_version: 1
allowed_statuses: [accepted, rejected, superseded]
allowed_verdicts: [pass, minor, major, not-applicable]
reviews: []
base_identity_lock:
  status: pending
  v13_01_revision: null
  v13_02_revision: null
  same_person_verdict: null
  user_confirmed: false
```

- [ ] **Step 5: Create the inheritance manifest and copy references**

The style entry records SHA
`aafad35807788120542bd650039da6f88297de8f366534ab3d2c38920100c579`,
controls face, amber eyes, airy bob, bright smile, rendering, and roomwear, and
explicitly excludes ornament side, exact pose, and yellow background. The C01
entry records SHA
`a977f2798d15f3da9ef0d7720d6f9fc41bd2f84f54f4c8a69908a482596a75c5`,
controls only healthy leg volume, standing body connection, natural weight,
and the four outdoor garments, and excludes face, age, hair, ornament, and
rendering. Each entry includes `source_path`, `copied_path`,
`source_collection`, `controlling_roles`, `reuse_rationale`,
`inherited_traits`, `excluded_traits`, and `sha256`.

Copy with:

```sh
install -D -m 0644 source/references/style-study/akari-v04-a.png \
  akari-v1.3/references/style/akari-v04-a.png
install -D -m 0644 \
  akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png \
  akari-v1.3/references/v1.2/akari-v1.2_c01_front-natural-stance_r01.png
```

Create the four accepted directories and `.gitkeep` files with `apply_patch`.

- [ ] **Step 6: Test, lint, and commit**

Run:

```sh
bash -lc 'uv run python -m unittest tests.test_akari_v1_3_base_package -v'
bash -lc './node_modules/.bin/markdownlint-cli2 akari-v1.3/README.md akari-v1.3/docs/akari-v1.3-base-design.md'
```

Expected: all tests pass and markdownlint reports `0 error(s)`.

Commit only `.gitignore`, the new test, and `akari-v1.3/`:

```sh
git add .gitignore tests/test_akari_v1_3_base_package.py akari-v1.3
git commit -m "feat: scaffold Akari v1.3 base package"
```

### Task 2: Implement focused manifest and lifecycle validation

**Files:**

- Create: `scripts/validate_akari_v1_3_base.py`
- Modify: `tests/test_akari_v1_3_base_package.py`

**Interfaces:**

- Consumes: the three v1.3 manifests.
- Produces: the validator interfaces in the File Map.

- [ ] **Step 1: Add failing tests for all hard contracts**

Import the validator and add tests that prove:

```python
validate_package(require_complete=False)
with self.assertRaisesRegex(
    ValidationError, "required accepted image count: expected 6, got 0"
):
    validate_package(require_complete=True)
```

Use `copy.deepcopy` mutations to assert that validation rejects: a missing
V13-03 variant; an unknown dependency; a copied-reference hash mismatch; a
C01 inheritance entry that does not exclude `face`; an accepted review whose
overall verdict is `major`; an accepted review without `user_selected: true`;
mismatched source/promoted hashes; a promoted file whose computed hash does not
match the recorded source hash; and an accepted V13-03 or V13-04 while Base
Identity Lock is pending. Also prove a complete package remains valid when its
ignored candidate files are absent.

- [ ] **Step 2: Run tests and verify the missing-module error**

Run the v1.3 unittest module. Expected: import error for
`scripts.validate_akari_v1_3_base`.

- [ ] **Step 3: Implement the complete static contract**

In `scripts/validate_akari_v1_3_base.py`, define:

```python
ASSET_CONTRACT = {
    "V13-01": {
        "descriptor": "corrected-key-visual",
        "variants": ["default"],
        "expected_paths": [
            "accepted/base/key-visual/"
            "akari-v1.3_v13-01_corrected-key-visual_rNN.png"
        ],
        "depends_on": [],
        "controlling_gate": "identity",
        "required_review_gates": {
            "identity", "ornament", "expression", "rendering", "preservation"
        },
    },
    "V13-02": {
        "descriptor": "natural-full-body",
        "variants": ["default"],
        "expected_paths": [
            "accepted/base/full-body/"
            "akari-v1.3_v13-02_natural-full-body_rNN.png"
        ],
        "depends_on": ["V13-01"],
        "controlling_gate": "body",
        "required_review_gates": {
            "identity", "ornament", "body", "rendering"
        },
    },
    "V13-03": {
        "descriptor": "expression-pair",
        "variants": ["everyday", "bright-smile"],
        "expected_paths": [
            "accepted/base/expressions/"
            "akari-v1.3_v13-03a_everyday_rNN.png",
            "accepted/base/expressions/"
            "akari-v1.3_v13-03b_bright-smile_rNN.png",
        ],
        "depends_on": ["V13-01", "V13-02"],
        "controlling_gate": "expression",
        "required_review_gates": {
            "identity", "ornament", "expression", "rendering",
            "pair-consistency"
        },
    },
    "V13-04": {
        "descriptor": "wardrobe-pair",
        "variants": ["outdoor", "roomwear"],
        "expected_paths": [
            "accepted/base/wardrobe/"
            "akari-v1.3_v13-04a_outdoor_rNN.png",
            "accepted/base/wardrobe/"
            "akari-v1.3_v13-04b_roomwear_rNN.png",
        ],
        "depends_on": ["V13-01", "V13-02"],
        "controlling_gate": "wardrobe",
        "required_review_gates": {
            "identity", "ornament", "body", "wardrobe", "rendering",
            "pair-consistency"
        },
    },
}
```

Implement the declared interfaces with these exact rules:

- Require schema version 1, four ordered asset IDs, and six total variants.
- Require static descriptor, variants, expected paths, dependencies, and gate.
- Allow asset states `planned`, `candidate`, `review`, and `accepted`.
- For `accepted`, require an `rNN` revision, ordered paths obtained by replacing
  `rNN` in the contract, and existing PNG files. Non-accepted assets must have
  null revision and no accepted paths.
- Require exactly two inheritance entries, all role/rationale/trait fields,
  safe relative copied paths, existing files, 64-character lowercase SHA-256,
  and matching computed hashes.
- Require C01's excluded traits to contain face, age, hair, ornament, and
  rendering.
- Allow review statuses `accepted`, `rejected`, and `superseded`; allow verdicts
  `pass`, `minor`, `major`, and `not-applicable`.
- An accepted review requires overall `pass`, `user_selected: true`, exactly
  the asset's required gates all set to `pass`, ordered source/promoted paths
  and hashes equal to variant count, identical source/promoted hash lists,
  existing promoted files, and matching computed promoted hashes. Candidate
  paths remain local audit history and their files are optional after
  promotion. When a candidate file is present, additionally verify its bytes
  and computed hash against the promoted file.
- Require exactly one accepted review for each accepted asset.
- Reject accepted V13-03/V13-04 unless the lock status, same-person verdict,
  and user confirmation are `accepted`, `pass`, and `true`.
- With `require_complete=True`, require six accepted paths. With false, validate
  the current lifecycle without requiring completion.
- The CLI defaults to complete validation; `--allow-incomplete` selects the
  development-stage mode. Print one success line or one actionable error and
  exit 0 or 1.

- [ ] **Step 4: Run focused tests and incomplete validation**

```sh
bash -lc 'uv run python -m unittest tests.test_akari_v1_3_base_package -v'
bash -lc 'uv run python scripts/validate_akari_v1_3_base.py --allow-incomplete'
```

Expected: all tests pass and the CLI prints
`akari v1.3 validation passed`.

- [ ] **Step 5: Commit**

```sh
git add scripts/validate_akari_v1_3_base.py \
  tests/test_akari_v1_3_base_package.py
git commit -m "feat: validate Akari v1.3 base lifecycle"
```

### Task 3: Add explicit npm validation and integration gates

**Files:**

- Modify: `package.json`
- Modify: `tests/test_workflow_gate_contract.py`

**Interfaces:**

- Consumes: the validator and v1.3 unittest module.
- Produces: `npm run validate:v1-3` and
  `npm run gate:integration:v1-3`.

- [ ] **Step 1: Write failing workflow assertions**

Add these exact expected scripts:

```python
"test:python:v1-3": (
    "uv run python -m unittest tests.test_akari_v1_3_base_package -v"
),
"validate:v1-3": "uv run python scripts/validate_akari_v1_3_base.py",
"gate:integration:v1-3": (
    "npm run test:python:v1-3 && npm run validate:v1-3 && npm run lint:md"
),
```

Add a test that the integration command equals the string above and contains
none of `pdf`, `ocr`, `tesseract`, or `chromium`.

- [ ] **Step 2: Verify failure, then add the npm scripts**

Run the workflow contract test and confirm it fails on missing keys. Add the
same three strings to `package.json` without changing any existing command.

- [ ] **Step 3: Verify and commit**

```sh
bash -lc 'uv run python -m unittest tests.test_workflow_gate_contract -v'
bash -lc 'npm run test:python:v1-3'
bash -lc 'uv run python scripts/validate_akari_v1_3_base.py --allow-incomplete'
git add package.json tests/test_workflow_gate_contract.py
git commit -m "build: add Akari v1.3 integration gate"
```

`npm run validate:v1-3` is expected to remain red until all six images are
accepted; the direct `--allow-incomplete` command is the production-stage gate.

### Task 4: Generate, review, and promote V13-01 corrected key visual

**Files:**

- Create locally: `akari-v1.3/source/candidates/v13-01/r01/*.png`
- Create locally: `akari-v1.3/comparisons/v13-01-r01/*`
- Create after selection:
  `akari-v1.3/accepted/base/key-visual/akari-v1.3_v13-01_corrected-key-visual_r01.png`
- Modify: `akari-v1.3/manifest/assets.yaml`
- Modify: `akari-v1.3/manifest/review-log.yaml`

**Interfaces:**

- Consumes: copied v04 style authority.
- Produces: accepted V13-01, the close-view identity and rendering anchor.

- [ ] **Step 1: Open and state the source role before generation**

Open `akari-v1.3/references/style/akari-v04-a.png` at original resolution.
State that it controls composition, face, amber eyes, airy bob, open-mouth
smile, palette, light, and rendering. Its ornament side is a known defect and
is not inherited.

- [ ] **Step 2: Generate independent candidates A and B**

Use the `imagegen` skill with the copied v04 image as the referenced image.
Make two independent calls with this prompt, changing only the final attempt
letter:

```text
Edit the referenced image as a close successor, not a redesign. The reference
is the highest authority for Akari's face, large jewel-like amber eyes, softly
rounded cheeks, natural blush, warm chestnut airy short bob, layered ends,
fine flyaways, cheek strands, bright open-mouth smile, gaze energy,
composition, yellow background, palette, soft light, white oversized T-shirt,
pale-blue lounge shorts, and polished pastel cel rendering.

Make exactly one required design correction: move the complete hair ornament
to Akari's character-left, which is image-right in this front-facing view.
The ornament is two pale-blue crossed pins immediately above a small pale-blue
ribbon with short tails. Make the ribbon slightly smaller and the tails shorter
than in the source. It must sit naturally in and follow the hair. Remove every
ornament trace from image-left. Do not duplicate, mirror, hide, enlarge, or
split the ornament.

Preserve the same person and young-adult reading. Preserve face width, chin,
eye size and structure, smile shape, gaze, airy hair volume, head angle, raised
hand, torso, raised leg, anatomy, skin color, clothing finish, light, and
overall appeal. Do not flatten the rendering. Do not patch with visible seams,
truncate hair strands, disconnect anatomy, add text, add a watermark, or add
another character.

This is independent attempt A.
```

Save returned PNGs as:

```text
akari-v1.3/source/candidates/v13-01/r01/akari-v1.3_v13-01_corrected-key-visual_r01-a.png
akari-v1.3/source/candidates/v13-01/r01/akari-v1.3_v13-01_corrected-key-visual_r01-b.png
```

- [ ] **Step 3: Inspect and record both reviews**

Open source, A, and B at original resolution. Review in order: same identity
and age read; one complete ornament at character-left/image-right; preserved
head/hand/torso/leg anatomy; preserved airy hair; preserved light and finish.
For each candidate, append a review with exact candidate ID, source path,
literal `sha256sum`, findings, decision, and gate verdicts `identity`,
`ornament`, `expression`, `rendering`, and `preservation`. Only all-`pass`
candidates are eligible.

- [ ] **Step 4: Request explicit user selection and stop**

Show eligible candidates with a concise text comparison. Do not promote until
the user selects A or B. If neither passes, retain both review entries,
increment the revision to `r02`, and repeat with the recorded defects added to
the prompt.

- [ ] **Step 5: Promote the selected candidate byte-for-byte**

Copy the selected A or B path to the accepted r01 path. Run `cmp --silent` and
`sha256sum` against the exact source and accepted paths. Record matching source
and promoted hashes in its accepted review. Set V13-01 to `status: accepted`,
`revision: r01`, and its single ordered accepted path; keep Base Identity Lock
pending.

- [ ] **Step 6: Validate and commit the durable selection**

```sh
bash -lc 'npm run test:python:v1-3'
bash -lc 'uv run python scripts/validate_akari_v1_3_base.py --allow-incomplete'
git add akari-v1.3/accepted/base/key-visual \
  akari-v1.3/manifest/assets.yaml akari-v1.3/manifest/review-log.yaml
git commit -m "feat: accept Akari v1.3 corrected key visual"
```

Stage only the accepted image and two manifests. Candidate and comparison
paths remain ignored.

### Task 5: Generate, review, and promote V13-02 natural full body

**Files:**

- Create locally: `akari-v1.3/source/candidates/v13-02/r01/*.png`
- Create locally: `akari-v1.3/comparisons/v13-02-r01/*`
- Create after selection:
  `akari-v1.3/accepted/base/full-body/akari-v1.3_v13-02_natural-full-body_r01.png`
- Modify: `akari-v1.3/manifest/assets.yaml`
- Modify: `akari-v1.3/manifest/review-log.yaml`

**Interfaces:**

- Consumes: V13-01 for identity/rendering and copied C01 for body-only facts.
- Produces: accepted V13-02 and the passed Base Identity Lock.

- [ ] **Step 1: Open and state both reference roles**

Open accepted V13-01 and copied v1.2 C01 at original resolution. State that
V13-01 controls face, eyes, hair, ornament, young-adult read, color, and
rendering. C01 controls only healthy legs, pelvis-to-leg connection, joints,
feet, and natural standing weight.

- [ ] **Step 2: Generate independent full-body candidates A and B**

Use both images as references with this prompt, changing only the final attempt
letter:

```text
Create a neutral-background natural front full-body validation image of Akari.
Reference Image 1, accepted V13-01, is the controlling authority for her exact
v1.3 face, large structured amber eyes, softly rounded cheeks, young-adult
reading, warm chestnut airy short bob, fine flyaways and cheek strands,
character-left/image-right crossed-pin and small short-tail ribbon ornament,
skin color, line language, pastel cel shading, glossy structured hair, and
overall rendering. Reference Image 2, copied v1.2 C01, controls only healthy
leg volume, believable pelvis-to-leg connection, readable knees and ankles,
complete feet, and natural standing weight. Do not copy Image 2's face, hair,
ornament proportions, age impression, or flatter rendering.

Show one complete person head-to-toe on a restrained warm off-white neutral
background. Use a relaxed, nearly front-facing natural stance with a subtle
weight shift, unlocked knees, grounded feet, and enough margin to inspect the
complete hair, hands, legs, ankles, and toes. The upper body is light and
graceful; the legs retain healthy v1.2 volume and are not lengthened or made
uniformly slender.

Wardrobe is a loose opaque white short-sleeved T-shirt and simple opaque
pale-blue lounge shorts with a restrained drawstring. Bare legs and bare feet;
no socks, shoes, underwear exposure, sensual framing, props, text, watermark,
border, collage, or additional character. Keep the same coherent rendering as
V13-01 while simplifying only distance-dependent microdetail.

Hard rejects include childlike drift, a different face, compact v1.2 hair,
wrong-side or duplicate ornament, excessively long or thin legs, pinched
ankles, fused or disconnected joints, floating feet, broken hands, or a flat
separate art style.

This is independent attempt A.
```

Save A and B below `source/candidates/v13-02/r01/` with stem
`akari-v1.3_v13-02_natural-full-body_r01`.

- [ ] **Step 3: Review and record cross-distance evidence**

Open V13-01, C01, A, and B at original resolution. Record gates `identity`,
`ornament`, `body`, and `rendering`. Different-person drift, childlike drift,
wrong ornament side, broken anatomy, and a separate art style are `major`.

- [ ] **Step 4: Request explicit user selection and stop**

Show eligible A/B candidates. Do not promote or begin pair work before explicit
selection. If neither passes, retain history, increment revision, and retry.

- [ ] **Step 5: Promote and record Base Identity Lock**

Copy the selected candidate to the accepted V13-02 r01 path. Verify exact bytes
and hashes. Update V13-02 and its accepted review, then set:

```yaml
base_identity_lock:
  status: accepted
  v13_01_revision: r01
  v13_02_revision: r01
  same_person_verdict: pass
  user_confirmed: true
```

The explicit V13-02 selection after side-by-side identity review supplies the
user confirmation.

- [ ] **Step 6: Validate and commit the lock**

```sh
bash -lc 'npm run test:python:v1-3'
bash -lc 'uv run python scripts/validate_akari_v1_3_base.py --allow-incomplete'
git add akari-v1.3/accepted/base/full-body \
  akari-v1.3/manifest/assets.yaml akari-v1.3/manifest/review-log.yaml
git commit -m "feat: lock Akari v1.3 full-body identity"
```

Stage only the accepted image and two manifests.

### Task 6: Build and accept the V13-03 expression pair

**Files:**

- Create locally: `akari-v1.3/source/candidates/v13-03/r01/*`
- Create after selection: both r01 files under
  `akari-v1.3/accepted/base/expressions/`
- Modify: `akari-v1.3/manifest/assets.yaml`
- Modify: `akari-v1.3/manifest/review-log.yaml`

**Interfaces:**

- Consumes: accepted V13-01/V13-02 and the passed identity lock.
- Produces: same-condition relaxed and bright chest-up anchors.

- [ ] **Step 1: Derive the bright baseline without resampling**

Open V13-01 and V13-02 at original resolution and restate their roles. Verify
V13-01 is 1024x1536, then run:

```sh
magick \
  akari-v1.3/accepted/base/key-visual/akari-v1.3_v13-01_corrected-key-visual_r01.png \
  -crop 1024x1024+0+0 +repage \
  akari-v1.3/source/candidates/v13-03/r01/akari-v1.3_v13-03b_bright-smile_r01-a.png
```

Open the crop. It is eligible only if crown, ornament, eyes, face outline,
shoulders, and upper chest are all reviewable. Otherwise stop and define a
literal alternate crop geometry from original-resolution inspection before
continuing; do not rescale or hide the failed crop.

- [ ] **Step 2: Generate relaxed attempts A and B from the same baseline**

Use the bright crop as direct edit source and V13-02 only as identity
cross-check:

```text
Edit Reference Image 1 directly. It is the controlling same-condition
bright-smile crop from accepted V13-01. Preserve its exact crop, canvas, head
angle, gaze direction, lighting, background, face width, chin, nose, base eye
identity, hair silhouette, flyaways, ornament design and character-left/image-
right placement, shoulders, clothing, color, and rendering. Reference Image 2,
accepted V13-02, is an identity cross-check only and must not change the crop.

Change only the expression into Akari's everyday anchor: relaxed, familiar,
quietly intimate, attentive to the viewer, and softly warm without becoming
blank, sleepy, sad, sultry, or childlike. Close the mouth into a natural relaxed
line with the faintest warmth at the corners. Slightly soften upper-eyelid
opening and brow tension while keeping the large structured amber eyes and
viewer-directed gaze. Use mild natural cheek softness, not a strong blush.

Do not change face width, chin shape, eye construction, hair volume, ornament,
head position, camera, wardrobe, lighting, background, or art style. No hand,
prop, text, watermark, border, collage, or additional character.

This is independent relaxed-expression attempt A.
```

Save relaxed A/B using stem `akari-v1.3_v13-03a_everyday_r01`. Byte-copy the
same bright baseline to matching `-a` and `-b` pair members so the only choice
is the relaxed edit.

- [ ] **Step 3: Review pair consistency and request selection**

Record one review per A/B family with two ordered source paths and gates
`identity`, `ornament`, `expression`, `rendering`, and `pair-consistency`.
Show both families. Stop until the user explicitly selects one. If neither
passes, retain history, increment revision, and retry only the relaxed edit.

- [ ] **Step 4: Promote, verify, validate, and commit both members**

Copy the selected relaxed and bright files to the ordered accepted V13-03 r01
paths. Run `cmp --silent` and `sha256sum` for both. Update manifests, then run:

```sh
bash -lc 'npm run test:python:v1-3'
bash -lc 'uv run python scripts/validate_akari_v1_3_base.py --allow-incomplete'
git add akari-v1.3/accepted/base/expressions \
  akari-v1.3/manifest/assets.yaml akari-v1.3/manifest/review-log.yaml
git commit -m "feat: accept Akari v1.3 expression anchors"
```

### Task 7: Build and accept the V13-04 wardrobe pair

**Files:**

- Create locally: `akari-v1.3/source/candidates/v13-04/r01/*`
- Create after selection: both r01 files under
  `akari-v1.3/accepted/base/wardrobe/`
- Modify: `akari-v1.3/manifest/assets.yaml`
- Modify: `akari-v1.3/manifest/review-log.yaml`

**Interfaces:**

- Consumes: V13-02 as roomwear/base pose and C01 for garment facts only.
- Produces: same-condition outdoor and roomwear anchors.

- [ ] **Step 1: Open references and derive roomwear members**

Open accepted V13-02 and copied C01 at original resolution. State that V13-02
controls identity, body, pose, camera, expression, ornament, rendering, and
roomwear. C01 controls only the four outdoor garment facts. Byte-copy V13-02
to both A/B roomwear candidate paths; this intentional reuse guarantees the
accepted base pose rather than a regenerated approximation.

- [ ] **Step 2: Generate outdoor edits A and B**

Use V13-02 as direct edit source and C01 as garment reference:

```text
Edit Reference Image 1 directly. Accepted V13-02 controls Akari's exact v1.3
face, amber eyes, young-adult reading, airy chestnut bob, fine flyaways,
character-left/image-right ornament, full body, healthy leg volume, natural
standing weight, pose, hand positions, camera, expression, neutral background,
light, and rendering. Reference Image 2, copied v1.2 C01, controls only these
outdoor garment facts: white oversized hoodie, gray pleated skirt, white socks
with exactly two pale-blue stripes, and white chunky sneakers. Do not inherit
Image 2's face, compact hair, ornament proportions, age impression, body
slenderness, or flatter rendering.

Change only the wardrobe of Image 1 to the four specified outdoor garments.
Preserve the same visible body volume beneath the clothes, stance, weight,
limb lengths, joint positions, head, hair silhouette, camera, and expression.
The hoodie is opaque and relaxed, the skirt is gray and clearly pleated, both
socks have exactly two pale-blue stripes, and both sneakers are complete white
chunky sneakers with restrained pale-blue details.

Do not add a bag, prop, scenery, text, logo, watermark, border, collage, or
another character. Reject missing or duplicated ornament, childlike or
different-person drift, changed body proportions, hidden or broken hands,
fused legs, pinched ankles, mismatched shoes, wrong stripe count, or a separate
rendering style.

This is independent outdoor-wardrobe attempt A.
```

Save outdoor A/B with stem `akari-v1.3_v13-04a_outdoor_r01` and their exact
V13-02 copies with stem `akari-v1.3_v13-04b_roomwear_r01`.

- [ ] **Step 3: Review pair consistency and request selection**

Record gates `identity`, `ornament`, `body`, `wardrobe`, `rendering`, and
`pair-consistency`. Confirm only the outfit changes. Show eligible A/B pairs
and stop for explicit selection. If neither passes, retain history, increment
revision, and retry only the outdoor edit.

- [ ] **Step 4: Promote, verify, and run the complete gate**

Promote both selected members byte-for-byte, record ordered paths/hashes, and
set V13-04 accepted. Run:

```sh
bash -lc 'npm run validate:v1-3'
bash -lc 'npm run gate:integration:v1-3'
```

Expected: both pass for all six images. Commit the two accepted assets and
manifests with:

```sh
git add akari-v1.3/accepted/base/wardrobe \
  akari-v1.3/manifest/assets.yaml akari-v1.3/manifest/review-log.yaml
git commit -m "feat: accept Akari v1.3 wardrobe anchors"
```

### Task 8: Close Base Definition with fresh evidence

**Files:**

- Modify: `akari-v1.3/README.md`
- Modify: `akari-v1.3/docs/akari-v1.3-base-design.md`
- Modify: `tests/test_akari_v1_3_base_package.py`

**Interfaces:**

- Consumes: six accepted images and four accepted review decisions.
- Produces: the completed handoff without changing v1.2 or adding a PDF.

- [ ] **Step 1: Write the failing completion-document test**

```python
def test_completed_docs_register_all_six_images(self):
    readme = (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8")
    design = (
        PACKAGE_ROOT / "docs/akari-v1.3-base-design.md"
    ).read_text(encoding="utf-8")
    self.assertIn("Status: Base Definition complete.", readme)
    for asset in (
        "V13-01", "V13-02", "V13-03A", "V13-03B", "V13-04A", "V13-04B"
    ):
        with self.subTest(asset=asset):
            self.assertIn(asset, design)
    self.assertIn("Base Identity Lock: Pass", design)
```

Run `npm run test:python:v1-3`; expect failure on the production status.

- [ ] **Step 2: Record exact completion facts**

Change README to `Status: Base Definition complete.` Add a six-row table to
the package design using each literal revision and repository-relative accepted
path from `assets.yaml`, plus `Base Identity Lock: Pass`. Do not claim a v1.3
PDF or Daily completion.

- [ ] **Step 3: Run final serial verification**

```sh
bash -lc 'npm run gate:integration:v1-3'
bash -lc 'npm run gate:integration:v1-2'
git diff --check
git status --short
```

Expected: both gates pass, diff check is clean, no v1.2 file is changed by this
work, and no v1.3 candidate/comparison is staged.

- [ ] **Step 4: Commit and re-prove the committed tree**

Commit docs and the completion test, then re-prove:

```sh
git add akari-v1.3/README.md akari-v1.3/docs/akari-v1.3-base-design.md \
  tests/test_akari_v1_3_base_package.py
git commit -m "docs: complete Akari v1.3 base definition"
bash -lc 'npm run gate:integration:v1-3'
git status --short
```

Expected: v1.3 passes; status lists only pre-existing local v1.2 scratch paths,
if any.

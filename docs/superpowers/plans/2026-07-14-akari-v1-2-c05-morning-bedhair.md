# Akari v1.2 C05 Morning Bed Hair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, review, and accept one C05 chest-up reference that fixes
Akari's reversible just-awake hair and incomplete-wakefulness state before C06.

**Architecture:** Copy two immutable supporting state snapshots into the
Natural Form package, then add one exact manifest-driven C05 r01 request to the
existing validator. Reuse the single-output A/B/C comparison builder, generate
three independent candidates from one role-locked prompt, stop for explicit
user selection, and promote only the selected PNG byte-for-byte while closing
the complete review lifecycle.

**Tech Stack:** Python 3.12+, PyYAML, Pillow, `unittest`, Node/npm scripts,
built-in `image_gen`, PNG/WebP assets, Git

## Global Constraints

- Use a 1024 x 1536 portrait canvas with one standalone character and one
  composition.
- Frame Akari from the chest upward at near eye level in a front-biased light
  three-quarter view.
- Keep the complete head, outer hair silhouette, character-left ornament,
  shoulders, hoodie neckline, and upper chest visible.
- Generate exactly three independent candidates, A/B/C, from the same prompt,
  ordered references, state strength, crop, camera, outfit, backdrop, and light.
- Open all four references with `view_image` before every generation and state
  each role in the prompt.
- Use accepted C01 r01 as the primary controller for adult identity, face,
  white hoodie, palette, and Natural Form rendering.
- Use accepted hairpin-side C03 r02 as the controller for character-left
  ornament construction, cheek silhouette, and bob side volume, not pose.
- Use `sleepy-reply-v3.webp` only for coordinated eyelid weight, lower gaze
  energy, and incomplete focus; never copy its hand, mouth, blush, scene, crop,
  or rendering finish.
- Use `morning-glance-h05.png` only for small crown flyaways, a cheek strand,
  and lower-bob end irregularity; never copy its hand, room, window light, pose,
  or alert expression.
- Apply exactly four reversible hair changes: small crown lifts or flyaways,
  asymmetric bang separation, a partial nape flick with lower-bob end
  irregularity, and one cheek-falling strand.
- Build sleepiness from eyelids, brows, gaze, neutral closed lips, and relaxed
  facial tension together; do not reduce it to smaller or closed eyes.
- Keep the accepted white oversized hoodie. Do not add hands, props, furniture,
  a bed, a window, a room scene, C06 smile progression, or D01 scene content.
- Treat about 70 px above the hair and about 60 px lateral hair margin as
  advisory guidance only.
- Reject framing only when crop or scale prevents complete face, hair, ornament,
  or hoodie-state review; never reject from a small numerical miss alone.
- C05 release status must be `accepted`, never `accepted-with-notes`.
- Do not patch, mask, warp, blend, resize, or mechanically composite a
  candidate into compliance.
- Stop r01 after three successfully returned images. If all three retain a
  Blocker or Major, close r01 as rejected and design r02 separately.
- Keep C05 candidates and comparison output local-only. Commit only durable
  references, contracts, tests, review metadata, and the selected accepted PNG.
- Stop for explicit user selection before changing accepted C05 state.
- Keep the lifecycle declaration `depends_on: [C01]`; C03 is a controlling
  generation reference, not a new lifecycle dependency.
- C06 cannot become accepted until C05 is strictly `accepted`.
- Preserve the existing untracked C04/C07 candidates and comparisons. Never use
  broad staging such as `git add -A` or `git add akari-v1.2`.
- Run Node/npm commands through `bash -lc` so fnm-managed Node is available.

---

## File Map

### Durable files created before generation

- `akari-v1.2/references/supporting/sleepy-reply-v3.webp` — immutable,
  byte-identical sleepy-expression snapshot.
- `akari-v1.2/references/supporting/morning-glance-h05.png` — immutable,
  byte-identical morning-hair snapshot.
- `akari-v1.2/manifest/generation-requests/c05-r01.yaml` — exact ordered
  references, shared prompt, advisory framing, A/B/C paths, and review gates.

### Durable files modified before generation

- `akari-v1.2/manifest/inheritance.yaml` — provenance and SHA-256 for both
  supporting snapshots.
- `scripts/validate_akari_v1_2_natural_form.py` — reference count, C05 request,
  per-candidate-field, hard-reject, dependency, and C05/C06 status validation.
- `tests/test_akari_v1_2_natural_form_package.py` — provenance, request,
  collection, dependency, status, command, and lifecycle coverage.
- `package.json` — `build:v1-2:c05-comparison`.

### Durable files created or modified only after user selection

- `akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png`
  — selected candidate copied byte-for-byte.
- `akari-v1.2/manifest/assets.yaml` — C05 moves from candidate r00 to accepted
  r01.
- `akari-v1.2/manifest/review-log.yaml` — complete ordered A/B/C review batch.

### Existing code reused unchanged unless a failing test proves otherwise

- `scripts/build_v1_2_candidate_comparison.py` — manifest-driven three-card
  comparison builder.
- `tests/test_build_v1_2_candidate_comparison.py` — A/B/C ordering, dimensions,
  and missing-input coverage.

### Local-only files

- `akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-a.png`
- `akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-b.png`
- `akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-c.png`
- `akari-v1.2/comparisons/c05-r01/c05-r01-comparison.webp`

---

### Task 1: Add immutable C05 supporting reference snapshots

**Files:**

- Create: `akari-v1.2/references/supporting/sleepy-reply-v3.webp`
- Create: `akari-v1.2/references/supporting/morning-glance-h05.png`
- Modify: `akari-v1.2/manifest/inheritance.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py:791-837`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:1405-1431`

**Interfaces:**

- Consumes: the two tracked source assets and
  `validate_inheritance(data: dict, repository_root: Path, package_root: Path)
  -> None`.
- Produces: two canonical `reference-only` package snapshots, exact provenance
  records, and a validated total of fifteen references.

- [ ] **Step 1: Write the failing exact-provenance test**

Add to `NaturalFormInheritanceTests`:

```python
def test_c05_supporting_snapshots_have_exact_provenance_and_hashes(self):
    records = {record["role"]: record for record in self.data["references"]}
    expected = {
        "supporting_sleepy_expression": {
            "role": "supporting_sleepy_expression",
            "inheritance_class": "reference-only",
            "source_path": (
                "source/generated/tonari-no-hyoujou/"
                "20260705_sleepy-reply_v3.webp"
            ),
            "copied_path": (
                "akari-v1.2/references/supporting/sleepy-reply-v3.webp"
            ),
            "source_collection": "tonari-no-hyoujou",
            "reuse_rationale": (
                "C05 eyelid weight gaze energy and incomplete visual focus "
                "only from a high-priority draft without identity rendering "
                "or acceptance authority"
            ),
            "sha256": (
                "a0b4dc00d8b32a0232c6579f3c28f792f49f5ede8f1d3527969c"
                "367cc3a9d6b2"
            ),
        },
        "supporting_morning_hair": {
            "role": "supporting_morning_hair",
            "inheritance_class": "reference-only",
            "source_path": (
                "source/finished/tonari-no-akari/"
                "20260701_morning-glance_v1_finish_h05_v1.png"
            ),
            "copied_path": (
                "akari-v1.2/references/supporting/morning-glance-h05.png"
            ),
            "source_collection": "tonari-no-akari",
            "reuse_rationale": (
                "C05 crown flyaways cheek strand and lower-bob end "
                "irregularity only without identity rendering or scene "
                "authority"
            ),
            "sha256": (
                "282379918dd6ff553305bf07e7d7aa47693fcd7edc19908ea94e1a"
                "0c5771ba7b"
            ),
        },
    }
    for role, record in expected.items():
        with self.subTest(role=role):
            self.assertEqual(records.get(role), record)
```

- [ ] **Step 2: Run the focused test and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormInheritanceTests.test_c05_supporting_snapshots_have_exact_provenance_and_hashes -v
```

Expected: FAIL because neither supporting role exists yet.

- [ ] **Step 3: Copy both snapshots byte-for-byte**

```sh
mkdir -p akari-v1.2/references/supporting
cp -- \
  source/generated/tonari-no-hyoujou/20260705_sleepy-reply_v3.webp \
  akari-v1.2/references/supporting/sleepy-reply-v3.webp
cp -- \
  source/finished/tonari-no-akari/20260701_morning-glance_v1_finish_h05_v1.png \
  akari-v1.2/references/supporting/morning-glance-h05.png
cmp --silent -- \
  source/generated/tonari-no-hyoujou/20260705_sleepy-reply_v3.webp \
  akari-v1.2/references/supporting/sleepy-reply-v3.webp
cmp --silent -- \
  source/finished/tonari-no-akari/20260701_morning-glance_v1_finish_h05_v1.png \
  akari-v1.2/references/supporting/morning-glance-h05.png
```

Expected: both `cmp` commands exit 0.

- [ ] **Step 4: Append the exact provenance records**

Append to `akari-v1.2/manifest/inheritance.yaml` in sleepy-then-morning order:

```yaml
  - role: supporting_sleepy_expression
    inheritance_class: reference-only
    source_path: source/generated/tonari-no-hyoujou/20260705_sleepy-reply_v3.webp
    copied_path: akari-v1.2/references/supporting/sleepy-reply-v3.webp
    source_collection: tonari-no-hyoujou
    reuse_rationale: C05 eyelid weight gaze energy and incomplete visual focus only from a high-priority draft without identity rendering or acceptance authority
    sha256: a0b4dc00d8b32a0232c6579f3c28f792f49f5ede8f1d3527969c367cc3a9d6b2
  - role: supporting_morning_hair
    inheritance_class: reference-only
    source_path: source/finished/tonari-no-akari/20260701_morning-glance_v1_finish_h05_v1.png
    copied_path: akari-v1.2/references/supporting/morning-glance-h05.png
    source_collection: tonari-no-akari
    reuse_rationale: C05 crown flyaways cheek strand and lower-bob end irregularity only without identity rendering or scene authority
    sha256: 282379918dd6ff553305bf07e7d7aa47693fcd7edc19908ea94e1a0c5771ba7b
```

- [ ] **Step 5: Raise the exact inheritance count from thirteen to fifteen**

Change `validate_inheritance` to:

```python
references = data.get("references")
if not isinstance(references, list) or len(references) != 15:
    raise ValidationError("inheritance: expected 15 references")
```

- [ ] **Step 6: Verify hashes, provenance, and package validation**

```sh
sha256sum \
  source/generated/tonari-no-hyoujou/20260705_sleepy-reply_v3.webp \
  akari-v1.2/references/supporting/sleepy-reply-v3.webp \
  source/finished/tonari-no-akari/20260701_morning-glance_v1_finish_h05_v1.png \
  akari-v1.2/references/supporting/morning-glance-h05.png
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormInheritanceTests -v
bash -lc 'npm run validate:v1-2'
```

Expected: each source/copy pair has the same specified digest, inheritance
tests pass, and validation reports fifteen references.

- [ ] **Step 7: Commit only the durable reference contract**

```sh
git add \
  akari-v1.2/references/supporting/sleepy-reply-v3.webp \
  akari-v1.2/references/supporting/morning-glance-h05.png \
  akari-v1.2/manifest/inheritance.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: add Natural Form C05 supporting references"
```

---

### Task 2: Add the exact C05 generation request contract

**Files:**

- Create: `akari-v1.2/manifest/generation-requests/c05-r01.yaml`
- Modify: `scripts/validate_akari_v1_2_natural_form.py:64-456`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:211-666`

**Interfaces:**

- Consumes: `GENERATION_REQUEST_CONTRACTS`,
  `validate_generation_request(data: dict) -> None`, and the C05 descriptor
  `morning-bedhair` from `assets.yaml`.
- Produces: exact contract key `("C05", "r01")`, one shared prompt, ordered
  four-reference input, canonical A/B/C outputs, advisory framing, exact hard
  rejects, and no per-candidate state-delta fields.

- [ ] **Step 1: Load C05 and write failing request tests**

Add to `NaturalFormGenerationRequestTests.setUp`:

```python
self.c05 = load_yaml(
    PACKAGE_ROOT / "manifest/generation-requests/c05-r01.yaml"
)
```

Add these tests:

```python
def test_c05_request_has_exact_single_output_contract(self):
    validate_generation_request(self.c05)
    self.assertEqual(self.c05["asset_id"], "C05")
    self.assertEqual(self.c05["revision"], "r01")
    self.assertEqual(
        self.c05["variation_axis"], "independent_generation_attempt"
    )
    self.assertEqual(
        [candidate["variant"] for candidate in self.c05["candidates"]],
        ["a", "b", "c"],
    )
    self.assertEqual(
        [candidate["title"] for candidate in self.c05["candidates"]],
        [
            "independent-attempt-a",
            "independent-attempt-b",
            "independent-attempt-c",
        ],
    )
    self.assertEqual(
        [candidate["target_path"] for candidate in self.c05["candidates"]],
        [
            "source/candidates/c05/r01/"
            "akari-v1.2_c05_morning-bedhair_r01-a.png",
            "source/candidates/c05/r01/"
            "akari-v1.2_c05_morning-bedhair_r01-b.png",
            "source/candidates/c05/r01/"
            "akari-v1.2_c05_morning-bedhair_r01-c.png",
        ],
    )
    self.assertEqual(
        self.c05["acceptance_gates"],
        ["identity", "state", "rendering"],
    )

def test_c05_uses_exact_ordered_reference_roles(self):
    self.assertEqual(
        [reference["role"] for reference in self.c05["references"]],
        [
            "accepted_c01_front_identity",
            "accepted_c03_hairpin_three_quarter",
            "supporting_sleepy_expression",
            "supporting_morning_hair",
        ],
    )

def test_c05_framing_guidance_is_advisory(self):
    self.assertEqual(
        self.c05["framing_guidance"],
        {
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
                "crop-or-scale-prevents-complete-face-hair-state-review"
            ),
        },
    )

def test_c05_rejects_strict_pixel_enforcement(self):
    invalid = copy.deepcopy(self.c05)
    invalid["framing_guidance"]["enforcement"] = "hard"
    with self.assertRaisesRegex(
        ValidationError, "exact framing guidance required"
    ):
        validate_generation_request(invalid)

def test_c05_rejects_reordered_references(self):
    invalid = copy.deepcopy(self.c05)
    invalid["references"][2], invalid["references"][3] = (
        invalid["references"][3],
        invalid["references"][2],
    )
    with self.assertRaisesRegex(ValidationError, "exact reference contract"):
        validate_generation_request(invalid)

def test_c05_rejects_per_candidate_state_delta(self):
    invalid = copy.deepcopy(self.c05)
    invalid["candidates"][0]["state_strength"] = "sleepier"
    with self.assertRaisesRegex(ValidationError, "candidate fields mismatch"):
        validate_generation_request(invalid)

def test_c05_rejects_changed_hard_rejects(self):
    invalid = copy.deepcopy(self.c05)
    invalid["hard_rejects"].pop()
    with self.assertRaisesRegex(ValidationError, "exact hard rejects required"):
        validate_generation_request(invalid)
```

- [ ] **Step 2: Run the focused tests and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
```

Expected: ERROR because `c05-r01.yaml` does not exist.

- [ ] **Step 3: Create the exact C05 request manifest**

Create `akari-v1.2/manifest/generation-requests/c05-r01.yaml`:

```yaml
schema_version: 1
request_id: akari-v1.2-c05-r01
asset_id: C05
revision: r01
variation_axis: independent_generation_attempt
references:
  - role: accepted_c01_front_identity
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
  - role: accepted_c03_hairpin_three_quarter
    path: akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
  - role: supporting_sleepy_expression
    path: akari-v1.2/references/supporting/sleepy-reply-v3.webp
  - role: supporting_morning_hair
    path: akari-v1.2/references/supporting/morning-glance-h05.png
shared_prompt: >-
  Use the four visible images only in their declared roles. Create one
  standalone chest-up illustration of the same naturally cute 25-year-old
  Akari on a 1024 x 1536 nearly plain warm off-white or pale neutral backdrop.
  Use soft diffuse near-neutral light without a visible source, hard shadow,
  dramatic rim light, or room context. Use a near-eye-level front-biased light
  three-quarter view with both eyes and the complete face outline visible. C01
  controls the 25-year-old adult identity, face proportions, warm amber eyes,
  healthy impression, fixed white oversized hoodie, palette, and Natural Form
  rendering. C03 r02 controls the character-left pale-blue crossed pins and
  ribbon-like ornament, cheek silhouette, and short warm-brown bob side volume;
  do not copy its full-body pose or exact camera angle. The sleepy supporting
  image controls only coordinated upper-eyelid weight, lower gaze energy, and
  incomplete visual focus; do not copy its cheek-rest hand, open mouth, blush,
  background, crop, or more rendered finish. The morning-hair supporting image
  controls only small crown flyaways, one cheek-side strand, and slight
  lower-bob end irregularity; do not copy its doorway, room, strong window
  light, hand, pose, or alert expression. C01 and C03 control whenever a
  supporting image conflicts with them. Apply exactly four reversible morning
  hair changes: one or two small crown lifts or flyaways; a light asymmetric
  separation in the bangs; a partial outward nape flick with small lower-bob end
  irregularity; and one soft strand falling toward a cheek. Preserve the normal
  short-bob length, overall outer contour, warm-brown color, part direction,
  face visibility, and complete ornament. Build sleepiness with slightly heavy
  upper eyelids without substantially shrinking the eyes, subtly lower or
  softer brows without sadness, a viewer-directed gaze that is not fully
  focused, closed neutral lips with no smile, and relaxed facial tension without
  intoxication, illness, distress, or sensual posing. Keep the complete crown,
  hair silhouette, ornament, chin, shoulders, hoodie neckline, and upper chest
  visible, with about 70 px above the hair and about 60 px beside it as advisory
  targets. No hands, props, furniture, bed, window, room scene, profile,
  top-down angle, strong tilt, closed eyes, wink, yawn, strong blush, parted-lip
  emphasis, haircut, longer hair, wind effect, wet hair, or extreme bed head.
  Do not add the C06 smile progression or D01 room-scene content. No readable
  text, logo, watermark, border, grid, collage, or multiple character.
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
  major_only_when: crop-or-scale-prevents-complete-face-hair-state-review
candidates:
  - variant: a
    title: independent-attempt-a
    target_path: source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-a.png
  - variant: b
    title: independent-attempt-b
    target_path: source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-b.png
  - variant: c
    title: independent-attempt-c
    target_path: source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-c.png
comparison_anchors: []
acceptance_gates: [identity, state, rendering]
hard_rejects:
  - severe identity age face-shape or eye-construction drift
  - missing mirrored relocated duplicated or materially redesigned ornament
  - corrupted face eyes hair or hoodie construction
  - different longer windblown wet or extreme-bed-head hairstyle
  - sleepiness shown only by closed or substantially shrunken eyes
  - sultry intoxicated ill distressed childlike or strong-blush drift
  - smile yawn open-mouth emphasis cheek-rest hand prop or room-scene leak
  - crop or scale that prevents complete face hair ornament or hoodie review
  - readable text logo watermark border grid collage or multiple character
```

- [ ] **Step 4: Add the exact C05 framing and request constants**

Add beside `C04_R01_FRAMING_GUIDANCE`:

```python
C05_R01_FRAMING_GUIDANCE = {
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
        "crop-or-scale-prevents-complete-face-hair-state-review"
    ),
}
```

Add `("C05", "r01")` after the C04 contract:

```python
("C05", "r01"): {
    "variation_axis": "independent_generation_attempt",
    "references": (
        (
            "accepted_c01_front_identity",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
        ),
        (
            "accepted_c03_hairpin_three_quarter",
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c03_hairpin-side-45_r02.png",
        ),
        (
            "supporting_sleepy_expression",
            "akari-v1.2/references/supporting/sleepy-reply-v3.webp",
        ),
        (
            "supporting_morning_hair",
            "akari-v1.2/references/supporting/morning-glance-h05.png",
        ),
    ),
    "candidate_prefix": "source/candidates/c05/r01/",
    "candidate_stem": "akari-v1.2_c05_morning-bedhair_r01",
    "candidate_detail": None,
    "candidate_fields": ("variant", "title", "target_path"),
    "candidate_titles": (
        "independent-attempt-a",
        "independent-attempt-b",
        "independent-attempt-c",
    ),
    "output_specs": None,
    "comparison_anchors": (),
    "framing_contract": None,
    "framing_guidance": C05_R01_FRAMING_GUIDANCE,
    "acceptance_gates": ("identity", "state", "rendering"),
    "required_prompt_phrases": (
        "C01 controls the 25-year-old adult identity",
        "C03 r02 controls the character-left pale-blue crossed pins",
        "one or two small crown lifts or flyaways",
        "a light asymmetric separation in the bangs",
        "a partial outward nape flick with small lower-bob end irregularity",
        "one soft strand falling toward a cheek",
        "slightly heavy upper eyelids without substantially shrinking the eyes",
        "a viewer-directed gaze that is not fully focused",
        "closed neutral lips with no smile",
        "No hands, props, furniture, bed, window, room scene",
        "Do not add the C06 smile progression or D01 room-scene content",
    ),
    "hard_rejects": (
        "severe identity age face-shape or eye-construction drift",
        "missing mirrored relocated duplicated or materially redesigned ornament",
        "corrupted face eyes hair or hoodie construction",
        "different longer windblown wet or extreme-bed-head hairstyle",
        "sleepiness shown only by closed or substantially shrunken eyes",
        "sultry intoxicated ill distressed childlike or strong-blush drift",
        "smile yawn open-mouth emphasis cheek-rest hand prop or room-scene leak",
        "crop or scale that prevents complete face hair ornament or hoodie review",
        "readable text logo watermark border grid collage or multiple character",
    ),
},
```

- [ ] **Step 5: Enforce candidate fields, titles, prompt phrases, and hard rejects**

Inside the candidate loop in `validate_generation_request`, after the title
check, add:

```python
candidate_fields = contract.get("candidate_fields")
if candidate_fields is not None and set(candidate) != set(candidate_fields):
    raise ValidationError("generation request: candidate fields mismatch")
```

After the candidate loop, add:

```python
candidate_titles = contract.get("candidate_titles")
if candidate_titles is not None and tuple(
    candidate["title"] for candidate in candidates
) != candidate_titles:
    raise ValidationError("generation request: candidate titles mismatch")
```

Replace the final shared-prompt and hard-reject checks with:

```python
shared_prompt = data.get("shared_prompt")
if not isinstance(shared_prompt, str) or not shared_prompt.strip():
    raise ValidationError("generation request: shared prompt required")
for phrase in contract.get("required_prompt_phrases", ()):
    if phrase not in shared_prompt:
        raise ValidationError(
            "generation request: required prompt phrase missing"
        )
if data.get("acceptance_gates") != list(contract["acceptance_gates"]):
    raise ValidationError("generation request: acceptance gates mismatch")
expected_hard_rejects = contract.get("hard_rejects")
if expected_hard_rejects is None:
    if not data.get("hard_rejects"):
        raise ValidationError("generation request: hard rejects required")
elif data.get("hard_rejects") != list(expected_hard_rejects):
    raise ValidationError("generation request: exact hard rejects required")
```

Existing contracts omit the new optional keys and retain their current
behavior. C05 alone receives the stricter no-delta and exact-reject checks.

- [ ] **Step 6: Update collection expectations**

Change the exact request order to:

```python
[
    ("C01", "r01"),
    ("C02", "r01"),
    ("C03", "r01"),
    ("C03", "r02"),
    ("C04", "r01"),
    ("C05", "r01"),
    ("C07", "r01"),
]
```

Change the generation-count expectation to:

```python
self.assertEqual(count_generation_work(self.requests), (20, 28))
```

Add the descriptor/state assertion to
`NaturalFormGenerationCollectionTests`:

```python
def test_c05_uses_assets_descriptor_and_starts_unaccepted(self):
    c05 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C05"
    )
    self.assertEqual(c05["descriptor"], "morning-bedhair")
    self.assertEqual(c05["status"], "candidate")
    self.assertEqual(c05["revision"], "r00")
    self.assertEqual(c05["accepted_paths"], [])
```

- [ ] **Step 7: Verify the exact request contract and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests -v
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests -v
bash -lc 'npm run validate:v1-2'
git add \
  akari-v1.2/manifest/generation-requests/c05-r01.yaml \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: define Natural Form C05 generation contract"
```

Expected: focused tests pass and validation reports seven requests, twenty
candidate groups, twenty-eight outputs, fifteen references, and seventeen
reviews.

---

### Task 3: Enforce the exact C05 generation dependency

**Files:**

- Modify: `scripts/validate_akari_v1_2_natural_form.py:459-545`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:751-797`

**Interfaces:**

- Consumes: the C01 and C05 asset records plus C05 request reference zero.
- Produces: `validate_generation_dependencies(assets: dict, requests:
  list[dict]) -> None` enforcement that C05 declares only C01 and uses the
  exact accepted C01 r01 path without turning C03 into a lifecycle dependency.

- [ ] **Step 1: Write failing C05 dependency tests**

Add to `NaturalFormGenerationDependencyTests`:

```python
def test_c05_declares_only_c01_dependency(self):
    c05 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C05"
    )
    self.assertEqual(c05["depends_on"], ["C01"])

def test_c05_requires_accepted_c01_r01(self):
    invalid = copy.deepcopy(self.assets)
    c01 = next(
        item for item in invalid["assets"] if item["asset_id"] == "C01"
    )
    c01.update(status="candidate", revision="r00", accepted_paths=[])
    c05_requests = [
        request for request in self.requests if request["asset_id"] == "C05"
    ]
    with self.assertRaisesRegex(
        ValidationError, "C05 requires accepted C01 r01"
    ):
        validate_generation_dependencies(invalid, c05_requests)

def test_c05_requires_exact_accepted_c01_path(self):
    c05_requests = [
        copy.deepcopy(request)
        for request in self.requests
        if request["asset_id"] == "C05"
    ]
    c05_requests[0]["references"][0]["path"] = (
        "akari-v1.2/accepted/core/standing/substituted-c01.png"
    )
    with self.assertRaisesRegex(
        ValidationError, "C05 requires accepted C01 r01"
    ):
        validate_generation_dependencies(self.assets, c05_requests)

def test_c05_candidate_paths_use_assets_descriptor(self):
    invalid = copy.deepcopy(self.assets)
    c05 = next(
        item for item in invalid["assets"] if item["asset_id"] == "C05"
    )
    c05["descriptor"] = "substituted-morning-state"
    c05_requests = [
        request for request in self.requests if request["asset_id"] == "C05"
    ]
    with self.assertRaisesRegex(
        ValidationError, "C05 candidate paths must use assets descriptor"
    ):
        validate_generation_dependencies(invalid, c05_requests)
```

- [ ] **Step 2: Run the focused tests and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests -v
```

Expected: FAIL because C05 has no dependency-validation branch.

- [ ] **Step 3: Add minimal C05 dependency validation**

Bind `c05 = assets_by_id["C05"]` and add after the C04 block:

```python
c05_requests = [item for item in requests if item["asset_id"] == "C05"]
c01_paths = c01.get("accepted_paths")
expected_c05_anchor = (
    f"akari-v1.2/{c01_paths[0]}"
    if isinstance(c01_paths, list) and len(c01_paths) == 1
    else None
)
for request in c05_requests:
    if (
        c05.get("depends_on") != ["C01"]
        or (c01.get("status"), c01.get("revision"))
        != ("accepted", "r01")
        or request["references"][0]["path"] != expected_c05_anchor
    ):
        raise ValidationError(
            "C05 requires accepted C01 r01 at its declared anchor"
        )
    expected_targets = [
        "source/candidates/c05/r01/"
        f"akari-v1.2_c05_{c05['descriptor']}_r01-{variant}.png"
        for variant in ("a", "b", "c")
    ]
    if [
        candidate["target_path"] for candidate in request["candidates"]
    ] != expected_targets:
        raise ValidationError(
            "C05 candidate paths must use assets descriptor"
        )
```

Do not bind C03 as an additional C05 dependency. Its exact accepted reference
path is already enforced by the request contract.

- [ ] **Step 4: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests -v
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests -v
bash -lc 'npm run validate:v1-2'
git add \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "test: enforce Natural Form C05 dependency"
```

---

### Task 4: Enforce C05 release status and C06 sequencing

**Files:**

- Modify: `scripts/validate_akari_v1_2_natural_form.py:548-611`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:67-162`

**Interfaces:**

- Consumes: C05 and C06 asset records in `validate_assets(data: dict,
  package_root: Path | None = None) -> None`.
- Produces: rejection of C05 `accepted-with-notes` and rejection of any accepted
  C06 state until C05 is strictly `accepted`.

- [ ] **Step 1: Write failing manifest-status tests**

Add to `NaturalFormManifestTests`:

```python
def test_c05_rejects_accepted_with_notes(self):
    invalid = copy.deepcopy(self.assets)
    c05 = next(
        item for item in invalid["assets"] if item["asset_id"] == "C05"
    )
    c05.update(
        status="accepted-with-notes",
        revision="r01",
        accepted_paths=[
            "accepted/core/face-hair/"
            "akari-v1.2_c05_morning-bedhair_r01.png"
        ],
    )
    with self.assertRaisesRegex(
        ValidationError, "C05: accepted-with-notes is not allowed"
    ):
        validate_assets(invalid)

def test_c06_cannot_be_accepted_before_c05(self):
    invalid = copy.deepcopy(self.assets)
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

def test_c06_may_be_accepted_after_strict_c05_acceptance(self):
    valid = copy.deepcopy(self.assets)
    c05 = next(
        item for item in valid["assets"] if item["asset_id"] == "C05"
    )
    c05.update(
        status="accepted",
        revision="r01",
        accepted_paths=[
            "accepted/core/face-hair/"
            "akari-v1.2_c05_morning-bedhair_r01.png"
        ],
    )
    c06 = next(
        item for item in valid["assets"] if item["asset_id"] == "C06"
    )
    c06.update(
        status="accepted",
        revision="r01",
        accepted_paths=[
            path.replace("rNN", "r01") for path in c06["expected_paths"]
        ],
    )
    validate_assets(valid)
```

- [ ] **Step 2: Run the focused tests and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests -v
```

Expected: the two negative cases fail because current validation permits them.

- [ ] **Step 3: Add the C05/C06 status rules**

Inside the asset loop, immediately after validating `status`, add:

```python
if asset_id == "C05" and status == "accepted-with-notes":
    raise ValidationError("C05: accepted-with-notes is not allowed")
```

After the asset loop, add:

```python
assets_by_id = {item["asset_id"]: item for item in assets}
if (
    assets_by_id["C06"]["status"] in {"accepted", "accepted-with-notes"}
    and assets_by_id["C05"]["status"] != "accepted"
):
    raise ValidationError("C06 acceptance requires accepted C05")
```

- [ ] **Step 4: Verify green and commit**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests -v
bash -lc 'npm run validate:v1-2'
git add \
  scripts/validate_akari_v1_2_natural_form.py \
  tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "test: enforce Natural Form C05 state sequencing"
```

---

### Task 5: Add the C05 comparison command without new layout code

**Files:**

- Modify: `package.json`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:1433-1509`
- Verify unchanged: `scripts/build_v1_2_candidate_comparison.py`
- Verify unchanged: `tests/test_build_v1_2_candidate_comparison.py`

**Interfaces:**

- Consumes: `build_comparison(request_path: Path, package_root: Path,
  output_path: Path, anchor_path: Path | None = None) -> Path`.
- Produces: npm command `build:v1-2:c05-comparison` and the equal-scale
  three-card C05 comparison WebP.

- [ ] **Step 1: Add the failing package-command expectation**

Add to `natural_form_commands` in `NaturalFormIsolationTests`:

```python
"build:v1-2:c05-comparison": (
    "uv run python scripts/build_v1_2_candidate_comparison.py "
    "--request akari-v1.2/manifest/generation-requests/c05-r01.yaml "
    "--output akari-v1.2/comparisons/c05-r01/"
    "c05-r01-comparison.webp"
),
```

- [ ] **Step 2: Run the exact isolation test and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests.test_package_command_reserves_unqualified_v1_2_for_natural_form -v
```

Expected: FAIL because `scripts.get("build:v1-2:c05-comparison")` is `None`.

- [ ] **Step 3: Add the exact package command**

Add beside the C04 command in `package.json`:

```json
"build:v1-2:c05-comparison": "uv run python scripts/build_v1_2_candidate_comparison.py --request akari-v1.2/manifest/generation-requests/c05-r01.yaml --output akari-v1.2/comparisons/c05-r01/c05-r01-comparison.webp"
```

- [ ] **Step 4: Prove the reused builder and package command**

```sh
uv run python -m unittest tests.test_build_v1_2_candidate_comparison -v
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests -v
```

Expected: PASS. Do not modify the generic builder while these tests remain
green.

- [ ] **Step 5: Commit the command only**

```sh
git add package.json tests/test_akari_v1_2_natural_form_package.py
git diff --cached --check
git commit -m "feat: add Natural Form C05 comparison command"
```

---

### Task 6: Generate and freeze three local C05 candidates

**Files:**

- Create local-only: `akari-v1.2/source/candidates/c05/r01/*.png`
- Do not modify durable manifests or accepted assets.

**Interfaces:**

- Consumes: four ordered references and the exact role header plus
  `shared_prompt` from `c05-r01.yaml`.
- Produces: exactly three independent, unedited PNGs at the declared A/B/C
  paths.

- [ ] **Step 1: Invoke the required image-generation skill and validate first**

Invoke `imagegen`, read its current `SKILL.md`, and follow it for all three new
generations. Then run:

```sh
bash -lc 'npm run validate:v1-2'
git status --short --branch
```

Expected validator summary:

```text
validated 8 assets, 15 references, 7 generation requests with 20 candidate groups and 28 generated outputs, and 17 reviews
```

Confirm C05 remains candidate r00, and record the existing untracked C04/C07
paths so they are not mistaken for new C05 output.

- [ ] **Step 2: Open all four references in exact order**

Use `view_image` with `detail: original` for:

```text
akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png
akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png
akari-v1.2/references/supporting/sleepy-reply-v3.webp
akari-v1.2/references/supporting/morning-glance-h05.png
```

Reconfirm that images 3 and 4 are non-controlling state references. Repeat
this four-image opening immediately before each generation call.

- [ ] **Step 3: Generate A with the exact role header and prompt**

Call built-in `image_gen` as a new generation, not an edit, using the four
absolute paths in the same order. Prefix the manifest's exact `shared_prompt`
with this role header:

```text
Use case: stylized-concept
Asset type: Akari v1.2 canonical chest-up state reference
Input images: Image 1 is the primary controlling adult identity, white-hoodie,
palette, and Natural Form rendering reference; Image 2 is the controlling
character-left ornament, cheek-silhouette, and bob-side-volume reference and
must not force its pose; Image 3 is a non-controlling sleepy eyelid and gaze
reference only; Image 4 is a non-controlling reversible morning-hair detail
reference only. When state references conflict, Images 1 and 2 control.
```

Save the returned full-frame PNG, without editing, as:

```text
akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-a.png
```

- [ ] **Step 4: Repeat independently for B and C**

Reopen the same four references before each call. Use the byte-identical role
header and `shared_prompt`; do not name A/B/C inside the prompt, use an earlier
candidate as a reference, or change state strength. Save each returned PNG to
its already-declared B or C path without overwriting an earlier candidate.

- [ ] **Step 5: Recover a missing local payload structurally if needed**

If a generated image appears in the interface but no local PNG exists, search
the current-date rollout for `image_generation_call`. Parse JSONL records,
decode only a `result` beginning with `iVBOR`, verify the decoded signature is
`89504e470d0a1a0a`, and write it to the matching candidate path. Never print or
copy the base64 payload through terminal output.

A technical call with no image and no recoverable payload may be retried once
for the same declared path. A successfully returned full image consumes that
candidate attempt even when it later fails review.

- [ ] **Step 6: Verify and freeze all three candidates**

```sh
file akari-v1.2/source/candidates/c05/r01/*.png
identify -format '%f %wx%h\n' \
  akari-v1.2/source/candidates/c05/r01/*.png
sha256sum akari-v1.2/source/candidates/c05/r01/*.png
git status --short
```

Expected: exactly three real 1024 x 1536 PNGs, three recorded lowercase
SHA-256 values, and no candidate staged or tracked. Duplicate content still
consumes its successful attempt and is reported during review; it is not
silently regenerated. A wrong-size image remains frozen as review evidence and
is ineligible; never resize it into compliance.

Do not commit this task's local-only outputs.

---

### Task 7: Build the comparison, review A/B/C, and stop for selection

**Files:**

- Create local-only: `akari-v1.2/comparisons/c05-r01/c05-r01-comparison.webp`
- Conditional modify: `akari-v1.2/manifest/review-log.yaml` only when all
  three candidates are rejected and r01 must be closed.
- Do not modify accepted C05 state.

**Interfaces:**

- Consumes: three frozen candidate PNGs in request order.
- Produces: one equal-scale A/B/C sheet, complete candidate findings, and an
  explicit user selection or an all-rejected r01 closure path.

- [ ] **Step 1: Build and verify the comparison**

```sh
bash -lc 'npm run build:v1-2:c05-comparison'
file akari-v1.2/comparisons/c05-r01/c05-r01-comparison.webp
identify -format '%f %wx%h\n' \
  akari-v1.2/comparisons/c05-r01/c05-r01-comparison.webp
git status --short
```

Expected: the command prints the declared output path and produces a readable
980 x 566 WebP with A/B/C at equal scale. No comparison file is staged.

- [ ] **Step 2: Invoke the one-image review skill and open every source**

Invoke `akari-v1-1-image-review`, read its current `SKILL.md` and required
rules, and use only its review criteria one candidate at a time. Do not run a
Correction Pass, Humanization Pass, edit, or composite.

Open the comparison and each full-resolution PNG with `view_image`, keeping C01
and C03 available for identity and ornament comparison.

- [ ] **Step 3: Review each candidate in the required order**

For A, then B, then C, record:

1. Identity — adult age, face width, rounded cheeks, compact chin, eye
   construction, bob, ornament side/design, palette, and white hoodie.
2. State — all four reversible hair changes, heavy lids plus soft brows,
   incomplete focus, neutral closed lips, and no C06 smile progression.
3. Rendering — hair and ornament integrity, facial artifacts, backdrop,
   lighting, text, logos, noise, props, hands, or room leakage.
4. Production — 1024 x 1536 PNG, standalone composition, canonical filename,
   SHA-256, complete crown/hair/ornament/chin/hoodie visibility, and advisory
   margin observations.

Stop detailed polish review after a Blocker. Never convert a small advisory
framing miss into a Major by itself.

- [ ] **Step 4: Present the quality-first comparison and stop**

Show the user the comparison, concise A/B/C findings, eligibility, and a
quality-first recommendation. Ask for an explicit `A`, `B`, or `C` selection.
Do not promote, edit manifests, or generate another candidate in this task.

If every candidate has an unresolved Blocker or Major, do not ask the user to
accept one. Append all three `rejected` records to `review-log.yaml` in declared
A/B/C order with their literal paths, hashes, findings, and decisions. Leave
C05 candidate r00, then run and commit only the closure:

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
git add akari-v1.2/manifest/review-log.yaml
git diff --cached --check
git commit -m "test: close rejected Natural Form C05 r01 round"
```

Then return to `superpowers:brainstorming` for a separate C05 r02 design. Do
not create a hidden fourth or fifth r01 attempt.

---

### Task 8: Promote exactly the user-selected C05 candidate

**Files:**

- Create: `akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Modify: `tests/test_akari_v1_2_natural_form_package.py:853-1403`

**Interfaces:**

- Consumes: explicit user selection, frozen A/B/C paths and hashes, and Task 7
  findings.
- Produces: one accepted C05 r01 PNG and an ordered three-review batch with
  exactly one `accepted`, two `rejected`, and no `accepted-with-notes`.

- [ ] **Step 1: Reconfirm selection and all candidate digests**

Map the user's literal selection to exactly one declared source. Run:

```sh
sha256sum akari-v1.2/source/candidates/c05/r01/*.png
```

Stop if any digest differs from Task 6. Do not infer a selection from the
assistant's recommendation.

- [ ] **Step 2: Write the failing final-state lifecycle test**

Add to `NaturalFormLifecycleTests`:

```python
def test_c05_acceptance_links_asset_review_and_declared_candidate(self):
    c05 = next(
        item for item in self.assets["assets"] if item["asset_id"] == "C05"
    )
    self.assertEqual(c05["status"], "accepted")
    self.assertEqual(c05["revision"], "r01")
    self.assertEqual(
        c05["accepted_paths"],
        [
            "accepted/core/face-hair/"
            "akari-v1.2_c05_morning-bedhair_r01.png"
        ],
    )
    reviews = [
        review
        for review in self.review_log["reviews"]
        if (review["asset_id"], review["revision"]) == ("C05", "r01")
    ]
    self.assertEqual(
        [review["candidate_id"] for review in reviews],
        ["c05-r01-a", "c05-r01-b", "c05-r01-c"],
    )
    statuses = [review["status"] for review in reviews]
    self.assertEqual(statuses.count("accepted"), 1)
    self.assertEqual(statuses.count("rejected"), 2)
    self.assertNotIn("accepted-with-notes", statuses)
    accepted = next(
        review for review in reviews if review["status"] == "accepted"
    )
    self.assertFalse(
        any(
            finding["severity"] in {"blocker", "major"}
            and not finding["resolved"]
            for finding in accepted["findings"]
        )
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

- [ ] **Step 3: Run the lifecycle class and verify red**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
```

Expected: FAIL because C05 is still candidate r00 with no C05 review batch.

- [ ] **Step 4: Copy exactly one selected source byte-for-byte**

Run only the block matching the user's literal selection:

```sh
# Selection A only
cp -- \
  akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-a.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
cmp --silent -- \
  akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-a.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png

# Selection B only
cp -- \
  akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-b.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
cmp --silent -- \
  akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-b.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png

# Selection C only
cp -- \
  akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-c.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
cmp --silent -- \
  akari-v1.2/source/candidates/c05/r01/akari-v1.2_c05_morning-bedhair_r01-c.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
```

Exactly one `cmp` must exit 0: the selected source.

- [ ] **Step 5: Update only C05 asset state and append all reviews**

Change only the C05 state fields in `assets.yaml` to:

```yaml
    status: accepted
    revision: r01
    accepted_paths:
      - accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
```

Append exactly three C05 r01 records to `review-log.yaml` in A/B/C order. Use
candidate IDs `c05-r01-a`, `c05-r01-b`, and `c05-r01-c`; their exact declared
source paths; the literal lowercase SHA-256 values from Step 1; and the actual
Task 7 findings. The selected record alone uses `status: accepted`; the other
two use `status: rejected`. Every decision states the user's choice or the
specific rejection rationale. The accepted record has no unresolved Blocker or
Major and never uses `accepted-with-notes`.

- [ ] **Step 6: Verify lifecycle, dimensions, and byte identity**

```sh
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests -v
bash -lc 'npm run validate:v1-2'
file \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
identify -format '%f %wx%h\n' \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
sha256sum \
  akari-v1.2/source/candidates/c05/r01/*.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
```

Expected: lifecycle tests pass, validation reports twenty reviews, the accepted
file is a real 1024 x 1536 PNG, and its digest matches exactly the selected
source. Re-run that selection's `cmp --silent` and require exit 0.

- [ ] **Step 7: Commit durable acceptance only**

```sh
git add \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png \
  akari-v1.2/manifest/assets.yaml \
  akari-v1.2/manifest/review-log.yaml \
  tests/test_akari_v1_2_natural_form_package.py
git status --short
git diff --cached --check
git commit -m "feat: accept Natural Form C05 r01"
```

Confirm no C04, C05, or C07 candidate/comparison artifact is staged.

---

### Task 9: Run fresh final-state verification

**Files:**

- Verify only; do not expand scope to repair unrelated failures.

**Interfaces:**

- Consumes: final C05 snapshots, request, command, accepted asset, and reviews.
- Produces: fresh completion evidence and a clean durable tracked state while
  preserving local-only review artifacts.

- [ ] **Step 1: Run focused and full test suites**

```sh
uv run python -m unittest tests.test_build_v1_2_candidate_comparison -v
uv run python -m unittest \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationRequestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationCollectionTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormGenerationDependencyTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormManifestTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormInheritanceTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormLifecycleTests \
  tests.test_akari_v1_2_natural_form_package.NaturalFormIsolationTests -v
bash -lc 'npm run test:node'
bash -lc 'npm run test:python'
bash -lc 'npm run validate:v1-2'
```

Expected: every command exits 0. Validator summary:

```text
validated 8 assets, 15 references, 7 generation requests with 20 candidate groups and 28 generated outputs, and 20 reviews
```

- [ ] **Step 2: Run audits and Markdown lint**

```sh
bash -lc 'npm run audit'
bash -lc 'npm run lint:md'
```

Expected: PASS with zero Markdown errors.

- [ ] **Step 3: Prove reference and accepted-asset byte identity**

```sh
cmp --silent -- \
  source/generated/tonari-no-hyoujou/20260705_sleepy-reply_v3.webp \
  akari-v1.2/references/supporting/sleepy-reply-v3.webp
cmp --silent -- \
  source/finished/tonari-no-akari/20260701_morning-glance_v1_finish_h05_v1.png \
  akari-v1.2/references/supporting/morning-glance-h05.png
sha256sum \
  akari-v1.2/references/supporting/sleepy-reply-v3.webp \
  akari-v1.2/references/supporting/morning-glance-h05.png \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
```

Re-run the selected candidate's exact `cmp --silent` from Task 8 and require
exit 0.

- [ ] **Step 4: Prove final dimensions and repository hygiene**

```sh
file \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
identify -format '%f %wx%h\n' \
  akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png
git ls-files -- \
  akari-v1.2/source/candidates/c05 \
  akari-v1.2/comparisons/c05-r01
git diff --check
git status --short --branch
```

Expected: a real 1024 x 1536 accepted PNG, no tracked C05 candidate/comparison
output, no whitespace errors, and no unintended durable changes. Report local
C04/C05/C07 candidates and comparisons separately; do not call them cleanup
failures.

---

## Out of Scope

- Reworking accepted C01, C02, C03, C04, or C07 assets.
- Generating or accepting C06-1 through C06-4 or D01.
- Creating a hair-ornament-free Daily morning variant.
- Running a Humanization Pass or Correction Pass on a failed C05 candidate.
- Candidate-to-candidate compositing, local patch repair, or resizing.
- Building a new generic comparison-layout framework.
- Producing a Natural Form release PDF.

---

## Execution Stop Conditions

- Stop before Task 6 if reference, request, dependency, status, or command
  validation is red.
- Stop after three successfully returned candidates; never create a hidden
  fourth or fifth r01 candidate.
- Stop a candidate's detailed review after a Blocker.
- Stop after Task 7 until the user explicitly selects A, B, or C.
- Stop before promotion if the selected candidate has an unresolved Blocker or
  Major.
- If all three are ineligible, close r01 as rejected and return to a separate
  r02 design; do not patch or composite a rescue.
- Stop completion claims until every Task 9 command has fresh passing output.

# Akari v1.2 Daily.1 D04 Morning Drink Fetch Implementation Plan

> **Execution:** Autonomous inline execution is authorized. Apply TDD, frozen
> prompt generation, original-resolution review, byte-identical promotion, and
> merged-state verification without a user selection pause.

**Goal:** Register, generate, review, select, accept, and integrate D04 as the
fourth Wave 1 morning scene.

**Architecture:** Extend the registry-driven Daily workflow introduced for
D03. Keep D01-D03 frozen. Register one D04 static contract and one exact r01
generation request, then reuse generic Daily review, candidate-order,
dimension, optional-C, and lifecycle linkage validation.

**Verification:** Use focused D04 unit tests during edits,
`npm run gate:edit:d04` for acceptance, and
`npm run gate:integration:v1-2` before merge. Run named gates serially.

## Contract Summary

- Asset: `D04`
- Revision: `r01`
- Descriptor: `morning-drink-fetch`
- Phase: `7`
- Direct references: D03, C01, C03, C06-1, C07 standing
- Dependencies: D03, C01, C03, C05, C06, C07
- Variants: independent A/B; C only after rejected scene-only or distinct
  candidate-local A/B with no shared non-scene controller
- Accepted path:
  `accepted/daily/morning/akari-v1.2_d04_morning-drink-fetch_r01.png`

## Task 1: Register the Candidate Contract

**Files:**

- Modify: `scripts/akari_v1_2_daily.py`
- Modify: `scripts/validate_akari_v1_2_natural_form.py`
- Modify: `tests/test_akari_v1_2_daily.py`
- Modify: `tests/test_akari_v1_2_natural_form_package.py`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Create: `akari-v1.2/manifest/generation-requests/d04-r01.yaml`
- Modify: `package.json`

### Step 1: Write failing D04 contract tests

Add `D04ContractTests` that assert the descriptor, phase, dependencies,
candidate state, exact ordered roles, A/B paths, frozen prompt digest, strict
accepted dependencies, and generic request validation.

Update package collection expectations for 11 assets and 12 generation
requests. Run:

```bash
uv run python -m unittest \
  tests.test_akari_v1_2_daily.D04ContractTests -v
```

Expected RED: D04 and its request are absent.

### Step 2: Add the D04 policy and manifest asset

Register controllers D03, C01, C03, C05, C06, C07, and D04-scene. Optional C
requires Blocker or Major scene-only findings on both A and B.

Add D04 candidate r00 to `assets.yaml` with the exact design contract.

### Step 3: Add the frozen D04 request

Write the five ordered references, shared prompt, scene contract, production
requirements, candidate policy, A/B paths, six acceptance gates, and hard
rejects. Calculate SHA-256 from the YAML-loaded prompt and pin it in the
validator.

### Step 4: Extend exact validation and commands

Register D04 in `ASSET_IDS`, generation request contracts, dependency checks,
accepted PNG dimension checks, and generic Daily dispatch. Add:

```json
"build:v1-2:d04-comparison": "uv run python scripts/build_v1_2_daily_comparison.py --request akari-v1.2/manifest/generation-requests/d04-r01.yaml --output akari-v1.2/comparisons/d04-r01/d04-r01-comparison.webp --asset-id D04",
"gate:edit:d04": "npm run test:python:daily && npm run test:python:natural-form && npm run validate:v1-2 && npm run verify:v1-2:release-pins"
```

### Step 5: Verify and commit registration

Run D04 tests, the full Daily tests, Natural Form tests, validator, Markdown
lint for the plan/design, and `git diff --check`. Commit durable contract files.

## Task 2: Generate and Select

**Local outputs:**

- `akari-v1.2/source/candidates/d04/r01/*.png`
- `akari-v1.2/comparisons/d04-r01/d04-r01-comparison.webp`

### Step 1: Open all five references

Use `view_image` on D03, C01, C03 hairpin-side, C06-1, and C07 standing. Keep
their roles identical to the request.

### Step 2: Generate independent A

Call image generation with the frozen prompt and only the five physical
references. Save the untouched result to the declared A path. Verify PNG
signature, dimensions, and SHA-256.

### Step 3: Re-open references and generate independent B

Do not provide A. Use the same prompt and reference order. Save untouched B and
verify production properties.

### Step 4: Compare and review

Build `d04-r01-comparison.webp`. Inspect A, B, comparison, and detail crops at
original resolution. Review Identity, Body, State, Continuity, Rendering, and
Production in that order.

### Step 5: Apply retry and selection policy

If either initial candidate is eligible, select the stronger and skip C. If
both fail for D04-scene reasons or distinct candidate-local Major defects,
record rejected A/B, register C, validate, generate independently, and review.
A shared non-scene accepted-asset controller is a blocker.

Append complete reviews in request order and record Akari's delegated
selection.

## Task 3: Promote and Verify

**Files:**

- Modify: `tests/test_akari_v1_2_daily.py`
- Modify: `akari-v1.2/manifest/assets.yaml`
- Modify: `akari-v1.2/manifest/review-log.yaml`
- Create: accepted D04 PNG

### Step 1: Write failing accepted-linkage tests

Assert exactly one accepted D04 review, exact candidate and hash, byte linkage,
clean-clone support without local candidates, and rejection of source or
accepted hash mismatch. Run the focused test and confirm RED while D04 remains
candidate.

### Step 2: Promote byte-for-byte

Copy the selected source without processing, set D04 to accepted r01, append
ordered reviews, and verify source/accepted equality with `cmp` and SHA-256.

### Step 3: Run the D04 edit gate

```bash
npm run gate:edit:d04
```

Commit only tests, manifests, review records, and the accepted asset.

## Task 4: Integrate and Clean Up

### Step 1: Run formal integration

Run `npm run gate:integration:v1-2` in a persistent command session, followed
by `git diff --check main...HEAD` and status inspection.

### Step 2: Preserve local review evidence and merge

Copy D04 candidates and comparison into the primary checkout without tracking
them. Fast-forward `main` to the verified branch.

### Step 3: Reverify merged main

Run `npm run gate:edit:d04` on main, verify the accepted hash, and confirm only
the expected local candidate/comparison directories remain untracked.

### Step 4: Remove the worktree and merged branch

Only after byte-identical evidence preservation and merged-state proof, remove
the D04 worktree and delete the merged feature branch. Continue directly to
D05.

## r02 Recovery Execution

The r01 A/B/C review closed without an eligible candidate because the
front-biased walking scene repeatedly produced crossed fashion-walk topology.
Execute this recovery before Task 3:

1. preserve all rejected r01 reviews with `D04-scene` provenance and keep the
   local r01 images and comparison;
2. add failing tests for a D04 r02 request, ordered request collection, exact
   generation counts, and the r02 comparison command;
3. register `d04-r02.yaml` with the unchanged five accepted references, a
   profile-biased frame-right camera, separate projected foot lanes, and only
   independent A/B candidates;
4. generate r02 A and B after reopening all five accepted references before
   each call, never using an r01 candidate;
5. build `d04-r02-comparison.webp`, review both originals, and select only an
   eligible candidate under Akari's delegated authority;
6. promote byte-for-byte as D04 r02, update linkage tests and manifests, then
   resume the existing edit, integration, preservation, merge, and main
   verification steps.

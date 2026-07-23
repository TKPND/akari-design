# Akari v1.2 Daily.1 D05 Morning Washroom Route Implementation Plan

> Execute autonomously under the user's delegated A/B selection authority.

**Goal:** Build, select, promote, verify, and integrate the fifth Wave 1
morning scene, then close the `v1.2-Daily.1` morning set.

**Architecture:** Extend the registry-driven Daily validator with D05 while
keeping D01-D04 frozen. Generate local independent A/B candidates from five
accepted references, promote one byte-for-byte, and record Wave 1 closure in
durable package documentation.

## Task 1: Register D05

1. Write failing tests for the D05 asset, request, ordered references,
   dependencies, generation counts, comparison command, edit gate, and review
   controller policy.
2. Add D05 candidate r00 to `assets.yaml`, add the exact r01 generation
   request, and pin its prompt hash and scene contract in the validator.
3. Add `build:v1-2:d05-comparison` and `gate:edit:d05`.
4. Run focused Daily/Natural Form tests, validator, Markdown lint, and
   `git diff --check`; commit the durable registration.

## Task 2: Generate and Select

1. Open accepted D04 r02, C02, C03 hairpin-side, C06-1, and C07 standing in
   their declared roles immediately before each generation.
2. Generate independent A and B with the frozen prompt; never use another D05
   candidate as a reference.
3. Verify PNG signature, 1024 by 1536 production tolerance, and SHA-256.
4. Build the D05 comparison, inspect originals and comparison, then apply the
   retry policy. Akari selects the strongest eligible candidate; skip C when
   either A or B is eligible.

## Task 3: Promote and Verify

1. Add failing live linkage, clean-clone, and selected-hash tests.
2. Append ordered reviews, promote the selected source without processing,
   and set D05 to accepted r01.
3. Verify source/accepted byte equality and run `npm run gate:edit:d05`.
4. Commit only durable tests, code, manifests, documentation, and accepted
   output.

## Task 4: Close Wave 1 and Integrate

1. Update `akari-v1.2-daily-handoff.md` and add a compact Wave 1 release record
   listing D01-D05 accepted paths, revisions, and selection status.
2. Run Markdown lint and the formal v1.2 integration gate serially.
3. Preserve D05 candidates/comparison in the primary checkout, fast-forward
   main, rerun the D05 edit gate, and verify the accepted hash.
4. Remove the worktree and merged branch, then continue directly to D06.

# Akari v1.2 Daily.2 D10 Implementation Plan

**Goal:** Build, select, promote, verify, and integrate the final Wave 2 rug
rest scene, then publish the Daily.2 release register.

## Tasks

1. Add failing D10 asset, generation, dependency, count, script, and Wave 2
   release-contract tests.
2. Register the D10 r01 manifest, validator policy, A/B comparison command, and
   focused edit gate; keep the asset at candidate r00.
3. Run the pending-state gate and commit the generation contract.
4. Open the five accepted references, generate independent A/B images, build
   the local comparison, and select quality-first under delegated authority.
5. Promote the selected bytes, record ordered reviews and hash linkage, add
   clean-clone lifecycle coverage, and pass the focused gate.
6. Add the Daily.2 D06-D10 release register, update the handoff to Wave 3, and
   prove that accepted Core bytes remain unchanged.
7. Verify in a clean integration worktree, fast-forward main, re-run focused
   and full integration gates on main, preserve local candidate/comparison
   evidence, and clean the branch/worktrees.

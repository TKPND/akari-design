# Akari v1.2 Daily.3 D12 Implementation Plan

**Goal:** Build, select, promote, verify, and integrate the second Wave 3 life
action: opening the compact refrigerator.

## Tasks

1. Add failing D12 asset, generation, dependency, count, script, and lifecycle
   tests.
2. Register the D12 r01 manifest, validator policy, A/B comparison command, and
   focused edit gate; keep the asset at candidate r00.
3. Run the pending-state gate and commit the generation contract.
4. Open the five accepted references, generate independent A/B images, build
   the local comparison, and select quality-first under delegated authority.
5. Promote the selected bytes, record ordered reviews and hash linkage, add
   clean-clone lifecycle coverage, and pass the focused gate.
6. Verify in a clean integration worktree, fast-forward main, re-run focused
   and full integration gates on main, preserve local candidate/comparison
   evidence, and clean the branch/worktrees.

# Akari v1.2 Natural Form Migration Design

## Summary

Replace the repository's existing Akari v1.2 working model with the approved
Natural Form Core design without discarding the earlier work. Move the four
existing v1.2 collections into one runnable legacy workspace, then initialize
`akari-v1.2/` as the canonical package for the new C01-C07 Core assets and D01
Daily validation asset.

The migration must make the distinction visible in paths, commands, manifests,
and documentation. Existing assets remain reusable evidence, but they do not
implicitly become Natural Form references or accepted assets.

## Approved Decisions

- Treat the existing face-hair, turnaround, motion, and overhead-room work as
  the pre-Natural Form legacy specification.
- Collect all four systems under
  `legacy/akari-v1.2-pre-natural-form/`.
- Keep the legacy generation, review, contact-sheet, promotion, and test
  workflows runnable after the move.
- Reserve `akari-v1.2/` and unqualified v1.2 terminology for Natural Form.
- Copy an old asset into the new reference package only after recording its
  source, role, reason for reuse, and SHA-256 digest.
- Establish the new package and its validation contracts before starting image
  generation.

## Goals

- Remove ambiguity between the old v1.2 work and the approved Natural Form
  specification.
- Preserve the old work as an executable and inspectable archive.
- Initialize a self-contained Natural Form package based on the approved Core
  design.
- Make asset identity, provenance, status, and inheritance machine-checkable.
- Prevent implicit dependencies between the canonical and legacy workspaces.
- Preserve the existing Akari v1.1 PDF and its build and audit workflows.

## Non-Goals

- Do not delete old candidates, accepted images, reviews, or implementation
  history.
- Do not treat old v1.2 accepted images as automatically accepted Natural Form
  assets.
- Do not generate C01-C07 or D01 images during this migration.
- Do not rebuild or replace `dist/akari-v1.1-settings.pdf`.
- Do not redesign the user-approved Natural Form Core specification.
- Do not refactor unrelated v1.1, Daybook, Tonari, or coordinate workflows.

## Legacy Workspace

The old v1.2 implementation becomes one bounded workspace:

```text
legacy/akari-v1.2-pre-natural-form/
├── README.md
├── docs/
│   ├── specs/
│   └── plans/
├── source/
│   ├── finished/
│   ├── manifests/
│   └── references/
├── evidence/
├── scripts/
├── tests/
└── dist/
```

The move includes every repository path belonging to these old collections:

- `v1-2-face-hair`
- `v1-2-turnaround`
- `v1-2-motion`
- `v1-2-overhead-room`

Associated specifications, plans, scripts, tests, package commands, contact
sheets, accepted assets, manifests, evidence, and applicable ignored candidate
directories move with their collection. The legacy README documents the old
design boundaries, commands, inputs, outputs, and relationship to Natural
Form.

### Executable Archive Contract

Legacy Python modules use package-safe imports within the legacy workspace.
Path resolution must be anchored to the repository or legacy package instead
of relying on the caller's current directory. Tests move beside the legacy
implementation and continue to cover request generation, validation, contact
sheets, promotion, and failure cases.

Root package commands use the `legacy:v1-2:` namespace. Examples include:

```text
legacy:v1-2-face-hair:contact-sheet
legacy:v1-2-turnaround:requests
legacy:v1-2-turnaround:contact-sheet
legacy:v1-2-turnaround:promote
legacy:v1-2-motion:requests
legacy:v1-2-motion:contact-sheet
legacy:v1-2-motion:promote
legacy:v1-2-overhead-room:requests
legacy:v1-2-overhead-room:contact-sheet
legacy:v1-2-overhead-room:promote
```

Commands may be adjusted to follow one consistent verb ordering during
implementation, but every current operation must retain an explicit legacy
equivalent.

## Natural Form Package

The canonical package follows the structure approved in the Core design:

```text
akari-v1.2/
├── README.md
├── docs/
│   ├── akari-v1.2-core-design.md
│   ├── akari-v1.2-review-guide.md
│   ├── akari-v1.2-change-summary.md
│   └── akari-v1.2-daily-handoff.md
├── manifest/
│   ├── assets.yaml
│   ├── inheritance.yaml
│   └── review-log.yaml
├── references/
│   ├── v1.1/
│   └── legacy/
├── source/
│   ├── candidates/
│   ├── rejected/
│   └── superseded/
├── accepted/
│   ├── core/
│   │   ├── standing/
│   │   ├── sitting/
│   │   ├── face-hair/
│   │   └── indoor-feet/
│   └── daily-validation/
├── comparisons/
└── release/
```

The supplied `Akari v1.2 Core` Draft 0.2 becomes the package's canonical Core
design document. Its approved status is design approval, not asset or release
approval.

### Initial Asset Contract

`manifest/assets.yaml` defines exactly these initial deliverables:

- C01 natural front stance
- C02 natural back stance
- C03 character-left and character-right 45-degree views
- C04 floor-sitting master
- C05 morning bed hair and sleepiness
- C06-1 through C06-4 daily smile gradient
- C07 standing and seated indoor sock-foot references
- D01 morning bedside validation

Each record includes an asset ID, descriptor, phase, required variants,
expected path, revision, status, dependency IDs, and applicable acceptance
gate. Initial statuses must make it clear that no image has yet been accepted.

`manifest/inheritance.yaml` records inherited v1.1 rules, Natural Form
extensions, and the standing-view criteria superseded only after formal v1.2
release. It also records every physical reference with:

- source path
- copied reference path
- SHA-256 digest
- controlling role
- inheritance class
- reuse rationale
- source version or collection

`manifest/review-log.yaml` begins as a valid empty review history and defines
the permitted states `candidate`, `review`, `accepted`,
`accepted-with-notes`, `rejected`, and `superseded`.

## Reference Isolation

Natural Form never reads a working asset directly from the legacy workspace.
An explicitly selected legacy asset is copied to
`akari-v1.2/references/legacy/`, hashed, and recorded in the inheritance
manifest. Required v1.1 assets receive the same treatment under
`akari-v1.2/references/v1.1/`.

This snapshot boundary ensures that a later legacy review or replacement does
not silently alter a Natural Form generation input. Missing references,
changed hashes, duplicate controlling roles, and unrecorded files cause
validation to fail.

## Migration Data Flow

```text
current pre-Natural Form v1.2 files
                  |
                  v
 inventory and baseline verification
                  |
                  v
 legacy/akari-v1.2-pre-natural-form/
          | runnable commands and tests
          | explicitly selected references only
          v
 akari-v1.2/references/legacy/ + provenance
                  |
 v1.1 references + approved Core design
                  |
                  v
 canonical Natural Form manifests
                  |
                  v
 Phase 1 image production in a later plan
```

## Failure Handling

- Stop the legacy move if the pre-migration inventory is incomplete or the
  focused baseline tests cannot be classified.
- Do not delete the old path merely to resolve an import or fixture failure;
  update the moved implementation and verify its equivalent command.
- Reject legacy operations that escape their workspace for v1.2 runtime data.
- Reject Natural Form manifests with unknown asset IDs, missing required
  variants, invalid statuses, or duplicate accepted revisions.
- Reject a copied reference whose recorded digest does not match its contents.
- Reject untracked reference files and manifest entries without files.
- Reject canonical manifests that contain direct pre-Natural Form runtime
  paths.
- Preserve failed, rejected, and superseded records as review history.

## Implementation Sequence

1. Record the tracked and ignored old v1.2 inventory and focused test baseline.
2. Create the legacy workspace and move all four old collections into it.
3. Repair imports, path resolution, fixtures, and package commands.
4. Run the moved legacy tests and compare results with the baseline.
5. Initialize the canonical `akari-v1.2/` package.
6. Install the approved Core design and supporting documentation.
7. Add initial asset, inheritance, and review manifests.
8. Add validators for canonical manifests, hashes, state transitions, and
   cross-workspace path isolation.
9. Run focused legacy and Natural Form tests.
10. Run repository-wide Markdown, Node, Python, and audit verification.

## Verification

Before moving files, record the output of the focused current v1.2 tests. After
the move, verify that the same behavioral cases pass from the legacy paths.
Generated image quality is outside this migration's automated scope.

The completed migration must satisfy all of the following:

- All old v1.2 implementation and runtime data live under
  `legacy/akari-v1.2-pre-natural-form/`.
- Every existing old operation has a documented `legacy:v1-2:*` command.
- The moved legacy tests produce results equivalent to the baseline.
- The canonical asset manifest contains C01-C07 and D01 without omissions or
  extra deliverables.
- Every canonical physical reference has a valid provenance record and
  SHA-256 digest.
- Natural Form contains no direct runtime reference to an old v1.2 path.
- Old unqualified `build:v1-2-*` and `promote:v1-2-*` commands no longer imply
  the legacy specification.
- Existing v1.1 workflows continue to pass.

Run focused verification first, followed by the broad repository checks:

```sh
npm run lint:md
npm run test:node
npm run test:python
npm run audit
```

The implementation plan must identify the exact focused legacy and Natural
Form test commands after deciding the final Python package entry points.

## Completion Boundary

This migration is complete when the old system is runnable only through its
explicit legacy identity and the new Natural Form package has validated,
traceable, generation-ready contracts. Producing or accepting C01 is the next
production phase, not part of this migration.

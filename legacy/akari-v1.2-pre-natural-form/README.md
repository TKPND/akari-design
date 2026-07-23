# Akari v1.2 Pre-Natural Form Legacy

This runnable archive preserves the earlier Akari v1.2 face-hair, eight-view
turnaround, representative motion, and overhead-room work. It is not the
canonical Natural Form Core package.

Run commands from the repository root through the `legacy:v1-2:*` npm
namespace. Runtime paths inside old manifests are relative to this legacy
root. Natural Form may reuse an image only by copying it into
`akari-v1.2/references/legacy/` and recording its provenance and SHA-256.

The archive contains local snapshots of every v1.1 and Hyoujou reference used
by its manifests. Its internal `package.json` retains the historical command
names for contract tests; callers from the repository root must use the
explicit legacy namespace.

Focused verification:

```sh
npm run test:python:legacy-v1-2
```

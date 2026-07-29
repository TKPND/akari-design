# Akari v1.5 Kawaii 1000 Gallery Runbook

The gallery data lives outside Git at
`/home/takahiro/workspace/akari_generated/v1.5-1000`.

## Initialize or verify the external reference snapshot

Run the initializer again to create missing files and verify that every
existing snapshot still matches its source:

```bash
uv run python scripts/init_akari_v1_5_kawaii_1000.py \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --texture-reference /home/takahiro/neesocks.jpeg
```

The command refuses a changed existing snapshot. Inspect
`references/manifest.json` and `state/novelty-ledger.json` under the external
data root after initialization.

## Create or refresh B000

```bash
uv run python scripts/create_akari_review_demo.py \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000
```

The command creates or refreshes exactly fifty PNG demo cards and their WebP
thumbnails. It preserves an existing `batches/B000/reviews.json` and refuses
to overwrite a non-demo B000. If the proposed artifact content or paths have
changed while reviews exist, it fails with a reset-required error before
changing B000.

B000 is demo-only. It never enters the 1,000 production-image count, and no
image generation occurs when it is created or reviewed.

## Run the focused gate

Run the serial, lightweight gallery gate before previewing or installing the
service:

```bash
bash -lc 'npm run gate:v1-5:gallery'
```

This gate does not build or audit a PDF.

## Preview the systemd unit

The preview prints the proposed unit and does not change systemd:

```bash
uv run python scripts/install_akari_review_gallery_service.py \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --host 100.125.117.75 \
  --port 8787
```

During an unmerged implementation review, use the active worktree as
`--repo-root` for a temporary foreground server only. Install the persistent
service from `/home/takahiro/workspace/akari-design` after the reviewed branch
has been integrated.

## Install and start the service

```bash
uv run python scripts/install_akari_review_gallery_service.py \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --host 100.125.117.75 \
  --port 8787 \
  --install
systemctl --user status akari-review-gallery.service
```

The service binds only to the named Tailscale IPv4 address.

## Inspect service logs

```bash
journalctl --user -u akari-review-gallery.service
```

For a live follow mode, add `-f`.

## Verify the listener

```bash
ss -ltnp | rg '100\.125\.117\.75:8787'
```

No listener should appear on `0.0.0.0:8787`.

## Open the gallery

Open this address from a tailnet device:

```text
http://100.125.117.75:8787
```

Do not expose the gallery through a public bind, proxy, or port forward.

## Rate all B000 cards from PC and mobile

On a PC, open each original in the detail dialog and use `1`, `2`, or `3` for
Reject, Keep, or Favorite. For rejected cards, select at least one reason.
Exercise note entry and save each review.

On a mobile tailnet device, open the same address at a narrow viewport, verify
that the controls fit without horizontal scrolling, and save reviews with the
visible buttons. Finish all fifty cards and confirm both `50 / 50` and
`Ready for next batch`.

## Restart and confirm reviews persist

```bash
systemctl --user restart akari-review-gallery.service
systemctl --user status akari-review-gallery.service
```

Reload B000 on both devices. Confirm the prior statuses, reject reasons, and
notes remain present, and that readiness still shows `50 / 50`.

## Stop, disable, or reinstall the service

Stop without disabling startup:

```bash
systemctl --user stop akari-review-gallery.service
```

Disable and stop:

```bash
systemctl --user disable --now akari-review-gallery.service
```

After repository, executable, host, port, or data-root changes, rerun the
installer to rewrite and enable the unit. Then explicitly restart an already
active service so it loads the rewritten command:

```bash
uv run python scripts/install_akari_review_gallery_service.py \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --host 100.125.117.75 \
  --port 8787 \
  --install
systemctl --user restart akari-review-gallery.service
systemctl --user status akari-review-gallery.service
```

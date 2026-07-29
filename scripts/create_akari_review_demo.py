#!/usr/bin/env python3
"""Create the non-counting B000 review-gallery demo batch."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

if __package__:
    from scripts.build_akari_review_thumbnail import (
        build_thumbnail,
        inspect_png,
    )
else:
    from build_akari_review_thumbnail import (
        build_thumbnail,
        inspect_png,
    )


LANES = (
    "classic-school-uniform",
    "professional-service-uniform",
    "sports-ceremony-fictional-uniform",
    "everyday-girly",
    "outings-special-days",
    "hobbies-making",
    "travel-walking",
    "retro-storybook",
    "magic-fantasy-sf",
    "subculture-wildcard",
)
COLORS = (
    "#f2d8d5",
    "#ead8ca",
    "#d9e4ef",
    "#efe2c6",
    "#dce7d6",
    "#e5daf0",
    "#f0d9e3",
    "#d7e8e6",
    "#e8dfd5",
    "#d9d8e9",
)
PREVIOUS_BATCH_NAME = ".B000.previous"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _reference(data_root: Path, name: str, role: str) -> dict[str, object]:
    path = data_root / "references" / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": f"references/{name}",
        "role": role,
        "exclusions": ["outfit", "pose", "background"],
        "sha256": _sha256(path),
    }


def _build_staged_batch(data_root: Path, staged: Path) -> dict[str, object]:
    images = staged / "images"
    thumbs = staged / "thumbs"
    images.mkdir(parents=True, exist_ok=True)
    thumbs.mkdir(parents=True, exist_ok=True)
    authorities = (
        _reference(
            data_root,
            "akari-v1.5-b3-body-balance.png",
            "v1.5 identity and body balance",
        ),
        _reference(
            data_root,
            "akari-v1.4-g2-balanced-lines.png",
            "rendering and skin authority",
        ),
    )
    entries = []
    for lane_index, lane in enumerate(LANES):
        for offset in range(5):
            ordinal = lane_index * 5 + offset + 1
            image_id = f"B000-{ordinal:03d}"
            stem = f"demo-{ordinal:03d}"
            image_path = images / f"{stem}.png"
            thumb_path = thumbs / f"{stem}.webp"
            canvas = Image.new("RGB", (768, 1152), COLORS[lane_index])
            draw = ImageDraw.Draw(canvas)
            draw.text((64, 80), image_id, fill="#352f32")
            draw.text((64, 150), lane, fill="#352f32")
            draw.text(
                (64, 240),
                "1 Reject   2 Keep   3 Favorite",
                fill="#554b50",
            )
            canvas.save(image_path, "PNG")
            build_thumbnail(image_path, thumb_path)
            technical = inspect_png(image_path)
            entries.append(
                {
                    "id": image_id,
                    "lane": lane,
                    "cuteBeat": f"demo-beat-{ordinal}",
                    "wardrobeFamily": f"demo-wardrobe-{ordinal}",
                    "setting": f"demo-setting-{ordinal}",
                    "action": f"demo-action-{ordinal}",
                    "sceneMode": (
                        "action-reaction" if ordinal <= 40 else "quiet-posed"
                    ),
                    "composition": f"demo-composition-{ordinal}",
                    "camera": f"demo-camera-{ordinal}",
                    "lighting": f"demo-lighting-{ordinal}",
                    "cast": (
                        "solo"
                        if ordinal <= 35
                        else "viewer-pov"
                        if ordinal <= 45
                        else "group"
                    ),
                    "dominantColor": COLORS[lane_index],
                    "textureFocus": ordinal <= 10,
                    "textureType": (
                        f"demo-texture-{ordinal}"
                        if ordinal <= 10
                        else "none"
                    ),
                    "subculture": lane == "subculture-wildcard",
                    "prompt": f"Demo card only; no image generation; {image_id}",
                    "references": [dict(item) for item in authorities],
                    "generation": {
                        "toolMode": "demo",
                        "generationId": None,
                        "requestId": None,
                        "sourcePath": None,
                        "technicalStatus": "valid",
                        "failureReason": None,
                    },
                    "artifact": {
                        "imagePath": f"batches/B000/images/{stem}.png",
                        "thumbnailPath": f"batches/B000/thumbs/{stem}.webp",
                        "sha256": technical["sha256"],
                        "width": technical["width"],
                        "height": technical["height"],
                    },
                }
            )
    manifest = {
        "schemaVersion": 1,
        "batchType": "demo",
        "batchId": "B000",
        "title": "Akari Kawaii 1000 Review Demo",
        "entries": entries,
    }
    reviews = {
        "schemaVersion": 1,
        "batchId": "B000",
        "reviews": {
            entry["id"]: {
                "status": "unreviewed",
                "reasons": [],
                "note": "",
                "revision": 0,
                "updatedAt": None,
            }
            for entry in entries
        },
    }
    _write_json_atomic(staged / "manifest.json", manifest)
    _write_json_atomic(staged / "reviews.json", reviews)
    _validate_staged_batch(staged, manifest)
    return manifest


def _validate_staged_batch(staged: Path, manifest: dict[str, object]) -> None:
    _assert_safe_batch_tree(staged)
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != 50:
        raise ValueError("staged B000 must contain exactly 50 entries")
    expected_images = set()
    expected_thumbs = set()
    for entry in entries:
        artifact = entry["artifact"]
        image_name = Path(artifact["imagePath"]).name
        thumb_name = Path(artifact["thumbnailPath"]).name
        expected_images.add(image_name)
        expected_thumbs.add(thumb_name)
        image_path = staged / "images" / image_name
        thumb_path = staged / "thumbs" / thumb_name
        technical = inspect_png(image_path)
        if (
            technical["sha256"] != artifact["sha256"]
            or technical["width"] != artifact["width"]
            or technical["height"] != artifact["height"]
        ):
            raise ValueError(f"staged artifact mismatch: {entry['id']}")
        with Image.open(thumb_path) as thumbnail:
            thumbnail.verify()
            if thumbnail.format != "WEBP":
                raise ValueError(f"invalid staged thumbnail: {entry['id']}")
    actual_images = {
        path.name
        for path in (staged / "images").iterdir()
        if not path.is_symlink() and path.is_file()
    }
    actual_thumbs = {
        path.name
        for path in (staged / "thumbs").iterdir()
        if not path.is_symlink() and path.is_file()
    }
    if actual_images != expected_images or actual_thumbs != expected_thumbs:
        raise ValueError("staged B000 media set does not match manifest")


def _assert_not_symlink(path: Path, label: str) -> None:
    if path.is_symlink():
        raise ValueError(f"refusing symlink {label}: {path}")


def _assert_safe_batch_tree(batch: Path) -> None:
    _assert_not_symlink(batch, "B000")
    if not batch.is_dir():
        raise ValueError(f"invalid B000 directory: {batch}")
    for name in ("manifest.json", "reviews.json", "reviews.json.bak"):
        path = batch / name
        _assert_not_symlink(path, name)
        if os.path.lexists(path) and not path.is_file():
            raise ValueError(f"invalid B000 file: {path}")
    for name in ("images", "thumbs"):
        directory = batch / name
        _assert_not_symlink(directory, name)
        if not directory.is_dir():
            raise ValueError(f"invalid B000 media directory: {directory}")
        for path in directory.rglob("*"):
            _assert_not_symlink(path, f"{name} media")


def _verified_batches_directory(data_root: Path) -> Path:
    batches = data_root / "batches"
    if os.path.lexists(batches):
        _assert_not_symlink(batches, "batches directory")
        if not batches.is_dir():
            raise ValueError(f"invalid batches directory: {batches}")
    else:
        batches.mkdir(parents=True)
    resolved = batches.resolve(strict=True)
    try:
        resolved.relative_to(data_root)
    except ValueError as error:
        raise ValueError("batches directory escapes data root") from error
    if resolved != batches:
        raise ValueError("batches directory escapes data root")
    return batches


def _declared_media_path(batch: Path, declared: str) -> Path:
    declared_path = Path(declared)
    try:
        relative = declared_path.relative_to("batches/B000")
    except ValueError as error:
        raise ValueError(f"unsafe B000 artifact path: {declared}") from error
    candidate = batch / relative
    _assert_not_symlink(candidate, "declared media")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(batch.resolve(strict=True))
    except (FileNotFoundError, ValueError) as error:
        raise ValueError(f"unsafe B000 artifact path: {declared}") from error
    if not candidate.is_file():
        raise ValueError(f"invalid B000 artifact: {declared}")
    return candidate


def _review_fingerprint(
    batch: Path,
    manifest: dict[str, object],
) -> tuple[str, tuple[tuple[str, str, str], ...]]:
    try:
        entries = sorted(manifest["entries"], key=lambda entry: entry["id"])
        normalized_entries = json.dumps(
            entries,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        media_hashes = tuple(
            (
                entry["id"],
                _sha256(
                    _declared_media_path(
                        batch,
                        entry["artifact"]["imagePath"],
                    )
                ),
                _sha256(
                    _declared_media_path(
                        batch,
                        entry["artifact"]["thumbnailPath"],
                    )
                ),
            )
            for entry in entries
        )
        return normalized_entries, media_hashes
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError("invalid existing B000 manifest") from error


def _media_snapshot(batch: Path) -> dict[str, str] | None:
    snapshot = {}
    for directory_name in ("images", "thumbs"):
        directory = batch / directory_name
        _assert_not_symlink(directory, directory_name)
        if not directory.is_dir():
            return None
        for path in directory.iterdir():
            _assert_not_symlink(path, f"{directory_name} media")
            if not path.is_file():
                return None
            snapshot[f"{directory_name}/{path.name}"] = _sha256(path)
    return snapshot


def _unchanged(path: Path, snapshot: bytes | None) -> bool:
    try:
        if path.is_symlink():
            return False
        current = path.read_bytes() if path.is_file() else None
    except OSError:
        return False
    return current == snapshot


def _load_demo_manifest(batch: Path) -> tuple[dict[str, object], bytes]:
    _assert_safe_batch_tree(batch)
    manifest_path = batch / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError("refusing to refresh incomplete B000")
    manifest_snapshot = manifest_path.read_bytes()
    manifest = json.loads(manifest_snapshot)
    if not isinstance(manifest, dict) or manifest.get("batchType") != "demo":
        raise ValueError("refusing to overwrite non-demo B000")
    return manifest, manifest_snapshot


def _validate_recovery_batch(batch: Path) -> None:
    manifest, _ = _load_demo_manifest(batch)
    if not (batch / "reviews.json").is_file():
        raise ValueError("invalid recoverable B000 reviews")
    _validate_staged_batch(batch, manifest)


def _cleanup_previous(previous: Path) -> bool:
    try:
        shutil.rmtree(previous)
    except OSError:
        return False
    return True


def _recover_interrupted_swap(batch: Path, previous: Path) -> None:
    if not os.path.lexists(previous):
        return
    _assert_not_symlink(previous, "previous B000")
    if not os.path.lexists(batch):
        _validate_recovery_batch(previous)
        os.replace(previous, batch)
        return
    _validate_recovery_batch(batch)
    _assert_safe_batch_tree(previous)
    _cleanup_previous(previous)


def _replace_batch(batch: Path, staged: Path, previous: Path) -> None:
    if not batch.exists():
        os.replace(staged, batch)
        return
    if os.path.lexists(previous):
        raise RuntimeError("previous B000 cleanup required before refresh")
    os.replace(batch, previous)
    try:
        os.replace(staged, batch)
    except BaseException:
        os.replace(previous, batch)
        raise
    _cleanup_previous(previous)


def create_demo_batch(data_root: Path) -> Path:
    """Create or safely refresh the demo-only B000 batch."""

    data_root = data_root.resolve()
    batches = _verified_batches_directory(data_root)
    batch = batches / "B000"
    previous = batches / PREVIOUS_BATCH_NAME
    _recover_interrupted_swap(batch, previous)
    manifest_path = batch / "manifest.json"
    reviews_path = batch / "reviews.json"
    current_manifest = None
    manifest_snapshot = None
    reviews_snapshot = None
    backup_snapshot = None
    if os.path.lexists(batch):
        current_manifest, manifest_snapshot = _load_demo_manifest(batch)
        if reviews_path.is_file():
            reviews_snapshot = reviews_path.read_bytes()
        backup_path = batch / "reviews.json.bak"
        if backup_path.is_file():
            backup_snapshot = backup_path.read_bytes()

    staged = Path(tempfile.mkdtemp(prefix=".B000-", dir=batches))
    try:
        proposed_manifest = _build_staged_batch(data_root, staged)
        if (
            reviews_snapshot is not None
            and _review_fingerprint(batch, current_manifest)
            != _review_fingerprint(staged, proposed_manifest)
        ):
            raise ValueError(
                "demo content changed; reset B000 reviews before refresh"
            )
        if current_manifest is not None:
            if not _unchanged(manifest_path, manifest_snapshot) or not _unchanged(
                reviews_path, reviews_snapshot
            ):
                raise RuntimeError("B000 changed during refresh; retry")
            if (
                manifest_snapshot == (staged / "manifest.json").read_bytes()
                and reviews_snapshot is not None
                and _media_snapshot(batch) == _media_snapshot(staged)
            ):
                return batch
        if reviews_snapshot is not None:
            (staged / "reviews.json").write_bytes(reviews_snapshot)
        if backup_snapshot is not None:
            (staged / "reviews.json.bak").write_bytes(backup_snapshot)
        _replace_batch(batch, staged, previous)
    finally:
        if staged.exists():
            shutil.rmtree(staged)
    return batch


def _absolute_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("must be an absolute path")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the non-counting B000 review-gallery demo batch."
    )
    parser.add_argument("--data-root", required=True, type=_absolute_path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(create_demo_batch(args.data_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

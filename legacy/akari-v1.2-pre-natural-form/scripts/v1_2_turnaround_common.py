from __future__ import annotations

import hashlib
import json
from pathlib import Path


LANDMARK_NAMES = (
    "crown",
    "chin",
    "shoulder",
    "hoodie_hem",
    "skirt_hem",
    "knee",
    "ankle",
    "sole",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def resolve_path(project_root: Path, path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else project_root / path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_landmarks(
    landmark_y_px: dict[str, int | float],
    image_height: int = 1536,
) -> dict[str, float]:
    if set(landmark_y_px) != set(LANDMARK_NAMES):
        raise ValueError("landmark_y_px must contain the eight canonical landmarks")
    values = [float(landmark_y_px[name]) for name in LANDMARK_NAMES]
    if not all(0 <= value < image_height for value in values):
        raise ValueError("landmark y values must be inside the image")
    if any(first >= second for first, second in zip(values, values[1:])):
        raise ValueError("landmark y values must be strictly increasing")
    crown = float(landmark_y_px["crown"])
    standing_height = float(landmark_y_px["sole"]) - crown
    return {
        name: round(
            (float(landmark_y_px[name]) - crown) / standing_height,
            6,
        )
        for name in LANDMARK_NAMES
    }

from __future__ import annotations

import argparse
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml
from PIL import Image


PACKAGE = Path("akari-v1.2/artbooks/ame-no-sei-ni-shite")
SCENE_RE = re.compile(r"^scene-(0[1-9]|1[0-2])$")
VALID_STATUSES = {
    "planned",
    "candidate",
    "review",
    "accepted",
    "rejected",
    "superseded",
}
REVIEW_CATEGORIES = {
    "identity",
    "hair",
    "pov",
    "continuity",
    "body",
    "emotion",
    "rendering",
    "production",
}
REVIEW_SEVERITIES = {"blocker", "major", "minor"}


class ValidationError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"expected mapping in {path}")
    return data


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def _package(root: Path) -> Path:
    return root / PACKAGE


def _resolve_package_path(root: Path, path: Path) -> Path:
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] in {"evidence", "accepted", "source"}:
        return _package(root) / path
    return root / path


def _rfc3339_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _with_lifecycle(scene: dict) -> dict:
    scene = dict(scene)
    scene_id = scene["id"]
    scene.setdefault("revision", "r01")
    scene.setdefault("status", "planned")
    scene.setdefault(
        "candidates",
        [
            {
                "variant": variant,
                "path": (
                    f"source/candidates/{scene_id}/r01/"
                    f"{scene_id}-r01-{variant}.png"
                ),
            }
            for variant in ("a", "b")
        ],
    )
    scene.setdefault("accepted_path", None)
    scene.setdefault("accepted_sha256", None)
    scene.setdefault("review_path", None)
    return scene


def load_contract(root: Path) -> dict:
    package = root / PACKAGE
    book = _load_yaml(package / "manifest/book.yaml")
    continuity = _load_yaml(package / "manifest/continuity.yaml")
    scene_data = _load_yaml(package / "manifest/scenes/index.yaml")
    return {
        "root": root,
        "package": package,
        "book": book,
        "continuity": continuity,
        "scenes": [_with_lifecycle(scene) for scene in scene_data["scenes"]],
    }


def render_scene_prompt(contract: dict, scene_id: str) -> str:
    scene = next(
        (item for item in contract["scenes"] if item["id"] == scene_id),
        None,
    )
    if scene is None:
        raise ValidationError(f"unknown scene: {scene_id}")
    outfit_key = "outdoor" if scene["act"] <= 2 else "indoor"
    outfit = contract["continuity"]["outfits"][outfit_key]
    sleeve = (
        "Only the edge of the viewer's sleeve may appear at the bottom of the frame."
        if scene_id == "scene-12"
        else ""
    )
    return " ".join(
        part
        for part in (
            "Create one 3:2 landscape illustration at 1536 by 1024 or larger.",
            "Show the same naturally cute 25-year-old adult Akari from the pinned Core references.",
            "Keep her warm-brown short bob, character-left parallel pins and pale-blue small ribbon, round face, warm-brown eyes, compact anime proportions, and healthy substantial legs.",
            f"Scene action: {scene['action']}.",
            f"Composition: {scene['composition']}.",
            f"Emotion: {scene['emotion']}.",
            f"Wetness state: {scene['wetness']}. Lighting: {scene['lighting']}.",
            f"Outfit: {outfit['prompt']}.",
            "Use a physically possible first-person point of view belonging to the viewer.",
            sleeve,
            "No viewer face, body, hand, reflection, or shadow.",
            "No readable text, logo, watermark, collage, or grid. One scene, one time, one outfit.",
        )
        if part
    )


def validate_contract(root: Path, require_release: bool = False) -> None:
    contract = load_contract(root)
    book = contract["book"]
    scenes = contract["scenes"]
    if book["page_count"] != 18 or [p["page"] for p in book["pages"]] != list(
        range(1, 19)
    ):
        raise ValidationError("book must contain pages 1 through 18")
    expected_ids = [f"scene-{number:02d}" for number in range(1, 13)]
    if [scene["id"] for scene in scenes] != expected_ids:
        raise ValidationError("scenes must be ordered scene-01 through scene-12")
    expected_acts = [1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4]
    if [scene["act"] for scene in scenes] != expected_acts:
        raise ValidationError("scene act membership is invalid")
    for scene in scenes:
        if not SCENE_RE.fullmatch(scene["id"]):
            raise ValidationError(f"invalid scene id: {scene['id']}")
        if len(scene["dialogue"]) > 1:
            raise ValidationError(f"dialogue limit exceeded: {scene['id']}")
        if scene["status"] not in VALID_STATUSES:
            raise ValidationError(f"invalid lifecycle status: {scene['id']}")
        expected = [
            f"source/candidates/{scene['id']}/r01/{scene['id']}-r01-{v}.png"
            for v in ("a", "b")
        ]
        if [item["path"] for item in scene["candidates"]] != expected:
            raise ValidationError(f"non-canonical candidates: {scene['id']}")
        if scene["status"] == "planned" and any(
            scene[key]
            for key in ("accepted_path", "accepted_sha256", "review_path")
        ):
            raise ValidationError(f"planned scene has accepted data: {scene['id']}")
        if scene["status"] == "accepted" and not all(
            scene[key]
            for key in ("accepted_path", "accepted_sha256", "review_path")
        ):
            raise ValidationError(f"accepted scene is incomplete: {scene['id']}")
        if scene["status"] == "accepted":
            accepted = contract["package"] / scene["accepted_path"]
            if not accepted.is_file():
                raise ValidationError(f"accepted image is missing: {scene['id']}")
            expected_accepted_path = f"accepted/{scene['id']}.webp"
            if scene["accepted_path"] != expected_accepted_path:
                raise ValidationError(
                    f"accepted image path must be {expected_accepted_path}: "
                    f"{scene['id']}"
                )
            with Image.open(accepted) as image:
                if image.format != "WEBP":
                    raise ValidationError(
                        f"accepted image must be WEBP: {scene['id']}"
                    )
                width, height = image.size
            minimum = book["minimum_image"]
            if width < minimum["width"] or height < minimum["height"]:
                raise ValidationError(f"accepted image is too small: {scene['id']}")
            if width * 2 != height * 3:
                raise ValidationError(f"accepted image must be 3:2: {scene['id']}")
            if sha256_file(accepted) != scene["accepted_sha256"]:
                raise ValidationError(f"accepted image hash mismatch: {scene['id']}")
    for reference in contract["continuity"]["core_references"]:
        path = root / reference["path"]
        if sha256_file(path) != reference["sha256"]:
            raise ValidationError(f"core reference hash mismatch: {reference['role']}")
    if require_release and not (contract["package"] / book["release_pdf"]).is_file():
        raise ValidationError("release PDF is missing")


def _reference_rows(contract: dict, scene_id: str) -> list[dict]:
    references = {
        reference["role"]: reference
        for reference in contract["continuity"]["core_references"]
    }
    rows = []
    for role in contract["continuity"]["reference_sets"][scene_id]:
        if role in references:
            rows.append(references[role])
        else:
            rows.append({"role": role, "path": "resolved after anchor approval", "sha256": "pending"})
    return rows


def _validate_scene_review(
    review: dict,
    scene_id: str,
    revision: str,
    variant: str,
) -> None:
    if review.get("scene_id") != scene_id:
        raise ValidationError("review scene_id mismatch")
    if review.get("revision") != revision:
        raise ValidationError("review revision mismatch")
    if review.get("selected_variant") != variant:
        raise ValidationError("review selected_variant mismatch")
    if review.get("status") not in {"accepted", "accepted-with-notes"}:
        raise ValidationError("review status must be accepted")
    findings = review.get("findings", [])
    if not isinstance(findings, list):
        raise ValidationError("review findings must be a list")
    for finding in findings:
        if set(finding) != {"severity", "category", "note"}:
            raise ValidationError("review finding keys are invalid")
        if finding["severity"] not in REVIEW_SEVERITIES:
            raise ValidationError("review finding severity is invalid")
        if finding["category"] not in REVIEW_CATEGORIES:
            raise ValidationError("review finding category is invalid")
    if any(finding["severity"] in {"blocker", "major"} for finding in findings):
        raise ValidationError("accepted review cannot contain blocker or major findings")
    if review["status"] == "accepted" and findings:
        raise ValidationError("accepted review must have no findings")
    if review["status"] == "accepted-with-notes" and any(
        finding["severity"] != "minor" for finding in findings
    ):
        raise ValidationError("accepted-with-notes permits minor findings only")


def promote_scene(
    root: Path,
    scene_id: str,
    revision: str,
    variant: str,
    review_path: Path,
    *,
    replace: bool = False,
) -> Path:
    if not SCENE_RE.fullmatch(scene_id):
        raise ValidationError(f"invalid scene id: {scene_id}")
    if revision != "r01" or variant not in {"a", "b"}:
        raise ValidationError("unknown revision or variant")
    review_path = _resolve_package_path(root, review_path)
    review = _load_yaml(review_path)
    _validate_scene_review(review, scene_id, revision, variant)

    package = _package(root)
    candidate = (
        package
        / f"source/candidates/{scene_id}/{revision}/"
        f"{scene_id}-{revision}-{variant}.png"
    )
    if not candidate.is_file():
        raise ValidationError(f"candidate image is missing: {candidate}")
    with Image.open(candidate) as image:
        width, height = image.size
        if image.format != "PNG":
            raise ValidationError("candidate image must be PNG")
    if width < 1536 or height < 1024 or width * 2 != height * 3:
        raise ValidationError("candidate image must be 3:2 and at least 1536 x 1024")

    destination = package / f"accepted/{scene_id}.webp"
    if destination.exists() and not replace:
        raise ValidationError("accepted image exists; pass --replace to overwrite")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(candidate) as image:
        image.convert("RGB").save(
            destination,
            "WEBP",
            quality=95,
            method=6,
        )
    accepted_sha = sha256_file(destination)

    index_path = package / "manifest/scenes/index.yaml"
    index = _load_yaml(index_path)
    scene = next(item for item in index["scenes"] if item["id"] == scene_id)
    scene.update(
        {
            "revision": revision,
            "status": "accepted",
            "candidates": [
                {
                    "variant": item_variant,
                    "path": (
                        f"source/candidates/{scene_id}/{revision}/"
                        f"{scene_id}-{revision}-{item_variant}.png"
                    ),
                }
                for item_variant in ("a", "b")
            ],
            "accepted_path": f"accepted/{scene_id}.webp",
            "accepted_sha256": accepted_sha,
            "review_path": review_path.relative_to(package).as_posix(),
        }
    )
    review["reviewed_at"] = _rfc3339_now()
    _write_yaml(review_path, review)
    _write_yaml(index_path, index)
    return destination


def _act_scene_ids(act: int) -> list[str]:
    mapping = {
        1: ["scene-01", "scene-02", "scene-03"],
        2: ["scene-04", "scene-05", "scene-06", "scene-07"],
        3: ["scene-08", "scene-09", "scene-10"],
        4: ["scene-11", "scene-12"],
    }
    if act not in mapping:
        raise ValidationError(f"invalid act: {act}")
    return mapping[act]


def _validate_approval_review(review: dict, scope: str) -> None:
    if review.get("scope") != scope or review.get("status") != "review":
        raise ValidationError(f"{scope} review must have review status")
    checks = review.get("checks")
    if not isinstance(checks, dict) or not checks or set(checks.values()) != {"pass"}:
        raise ValidationError(f"{scope} review checks must all pass")
    findings = review.get("findings", [])
    if any(item.get("severity") in {"blocker", "major"} for item in findings):
        raise ValidationError(f"{scope} review has blocker or major findings")


def approve_act(root: Path, act: int, review_path: Path) -> Path:
    contract = load_contract(root)
    scene_ids = _act_scene_ids(act)
    accepted = {
        scene["id"]
        for scene in contract["scenes"]
        if scene["status"] == "accepted"
    }
    if not set(scene_ids).issubset(accepted):
        raise ValidationError(f"act-{act} requires all scenes accepted")
    review_path = _resolve_package_path(root, review_path)
    review = _load_yaml(review_path)
    _validate_approval_review(review, f"act-{act}")
    sheet = contract["package"] / f"evidence/contact-sheets/act-{act}.webp"
    if not sheet.is_file():
        raise ValidationError(f"act-{act} contact sheet is missing")
    review.update(
        {
            "status": "accepted",
            "contact_sheet_sha256": sha256_file(sheet),
            "reviewed_at": _rfc3339_now(),
        }
    )
    _write_yaml(review_path, review)
    return review_path


def validate_act(root: Path, act: int) -> None:
    acts = range(1, 5) if act == 0 else (act,)
    contract = load_contract(root)
    for item in acts:
        scene_ids = _act_scene_ids(item)
        scenes = {scene["id"]: scene for scene in contract["scenes"]}
        if not all(scenes[scene_id]["status"] == "accepted" for scene_id in scene_ids):
            raise ValidationError(f"act-{item} scenes are not all accepted")
        review_path = contract["package"] / f"evidence/reviews/act-{item}.yaml"
        review = _load_yaml(review_path)
        if review.get("status") != "accepted":
            raise ValidationError(f"act-{item} review is not accepted")
        sheet = contract["package"] / f"evidence/contact-sheets/act-{item}.webp"
        if review.get("contact_sheet_sha256") != sha256_file(sheet):
            raise ValidationError(f"act-{item} contact sheet hash mismatch")
    validate_contract(root)


def approve_full(root: Path, review_path: Path) -> Path:
    contract = load_contract(root)
    if sum(scene["status"] == "accepted" for scene in contract["scenes"]) != 12:
        raise ValidationError("full continuity requires 12 accepted scenes")
    review_path = _resolve_package_path(root, review_path)
    review = _load_yaml(review_path)
    _validate_approval_review(review, "full-continuity")
    sheet = contract["package"] / "evidence/contact-sheets/full-continuity.webp"
    if not sheet.is_file():
        raise ValidationError("full continuity contact sheet is missing")
    review.update(
        {
            "status": "accepted",
            "contact_sheet_sha256": sha256_file(sheet),
            "reviewed_at": _rfc3339_now(),
        }
    )
    _write_yaml(review_path, review)
    return review_path


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    prompt_parser = subparsers.add_parser("prompt")
    prompt_parser.add_argument("--scene", required=True)
    promote_parser = subparsers.add_parser("promote")
    promote_parser.add_argument("--scene", required=True)
    promote_parser.add_argument("--revision", required=True)
    promote_parser.add_argument("--variant", required=True)
    promote_parser.add_argument("--review", type=Path, required=True)
    promote_parser.add_argument("--replace", action="store_true")
    approve_act_parser = subparsers.add_parser("approve-act")
    approve_act_parser.add_argument("--act", type=int, required=True)
    approve_act_parser.add_argument("--review", type=Path, required=True)
    validate_act_parser = subparsers.add_parser("validate-act")
    validate_act_parser.add_argument("--act", required=True)
    approve_full_parser = subparsers.add_parser("approve-full")
    approve_full_parser.add_argument("--review", type=Path, required=True)
    args = parser.parse_args()
    root = Path.cwd()
    if args.command == "validate":
        validate_contract(root)
        print("rain-day artbook contract: ok")
        return
    if args.command == "promote":
        output = promote_scene(
            root,
            args.scene,
            args.revision,
            args.variant,
            args.review,
            replace=args.replace,
        )
        print(output)
        return
    if args.command == "approve-act":
        print(approve_act(root, args.act, args.review))
        return
    if args.command == "validate-act":
        validate_act(root, 0 if args.act == "all" else int(args.act))
        print("rain-day artbook act validation: ok")
        return
    if args.command == "approve-full":
        print(approve_full(root, args.review))
        return
    contract = load_contract(root)
    print(render_scene_prompt(contract, args.scene))
    print("\nReferences:")
    for reference in _reference_rows(contract, args.scene):
        print(f"- {reference['role']}: {reference['path']} [{reference['sha256']}]")


if __name__ == "__main__":
    main()

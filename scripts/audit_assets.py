#!/usr/bin/env python3
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from akari_assets import SOURCE_ASSETS


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "source/manifests/source-assets.json"
ASSET_MANIFEST = ROOT / "source/manifests/asset-manifest.json"
PAGE_MANIFEST = ROOT / "source/manifests/page-manifest.json"
GENERATION_REQUESTS = ROOT / "source/manifests/generation-requests.json"
PALETTE = ROOT / "source/palette/akari-v1.1-palette.json"

ALLOWED_ASSET_STATUSES = {
    "needs_review",
    "accepted",
    "rejected",
    "needs_correction",
}
ALLOWED_GENERATION_REQUEST_STATUSES = {"queued", "needs_review", "accepted"}
GENERATED_ASSET_MODEL_OR_TOOL = "image_generation"
GENERATION_REQUEST_PREFIX = "request:"
GENERATED_CANDIDATE_DIR = Path("source/generated")
MIN_GENERATED_CANDIDATE_DIMENSION = 64
MAX_ASPECT_RATIO_RELATIVE_ERROR = 0.001
JAPANESE_TEXT_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
ASPECT_RATIO_RE = re.compile(r"^[1-9][0-9]*:[1-9][0-9]*$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_required_json(path: Path, label: str, errors: list[str]) -> dict:
    if not path.exists():
        errors.append(f"{label} manifest missing")
        return {}
    return load_json(path)


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def image_metadata(path: Path) -> dict:
    result = subprocess.run(
        ["identify", "-format", "%w %h %[colorspace]", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height, colorspace = result.stdout.strip().split()
    return {
        "width": int(width),
        "height": int(height),
        "colorspace": colorspace,
    }


def parse_aspect_ratio(value: object) -> tuple[int, int] | None:
    if not isinstance(value, str) or not ASPECT_RATIO_RE.fullmatch(value):
        return None
    width, height = value.split(":", 1)
    return int(width), int(height)


def aspect_ratio_matches(width: int, height: int, ratio: tuple[int, int]) -> bool:
    if min(width, height) < MIN_GENERATED_CANDIDATE_DIMENSION:
        return False
    expected_width, expected_height = ratio
    delta = abs(width * expected_height - height * expected_width)
    relative_error = delta / (height * expected_width)
    return relative_error <= MAX_ASPECT_RATIO_RELATIVE_ERROR


def generation_requests_by_id(data: dict) -> dict[str, dict]:
    requests = data.get("requests", [])
    if not isinstance(requests, list):
        return {}

    by_id = {}
    for request in requests:
        if not isinstance(request, dict):
            continue
        request_id = request.get("id")
        if is_non_empty_string(request_id) and request_id not in by_id:
            by_id[request_id] = request
    return by_id


def _validate_source_path(asset: dict, root: Path, errors: list[str]) -> Path:
    asset_id = asset.get("id", "<missing id>")
    source_path_value = asset.get("source_path")
    original_filename = asset.get("original_filename")

    if not isinstance(source_path_value, str):
        errors.append(f"source_path must be a string: {asset_id}")
        return root / "__missing_source_path__"
    if not isinstance(original_filename, str):
        errors.append(f"original_filename must be a string: {asset_id}")
        return root / source_path_value

    source_path = Path(source_path_value)
    if source_path.is_absolute():
        errors.append(f"source_path must be relative: {asset_id}")
        return source_path

    root_resolved = root.resolve()
    resolved_path = (root / source_path).resolve()
    try:
        resolved_path.relative_to(root_resolved)
    except ValueError:
        errors.append(f"source_path escapes project root: {asset_id}")

    expected_source_path = (Path("source/originals") / original_filename).as_posix()
    if source_path_value != expected_source_path:
        errors.append(
            f"source_path mismatch for {asset_id}: expected "
            f"{expected_source_path} got {source_path_value}"
        )

    return root / source_path


def _is_generated_asset(asset: dict) -> bool:
    seed_or_generation_id = asset.get("seed_or_generation_id")
    return (
        asset.get("model_or_tool") == GENERATED_ASSET_MODEL_OR_TOOL
        or "candidate_path" in asset
        or (
            isinstance(seed_or_generation_id, str)
            and seed_or_generation_id.startswith(GENERATION_REQUEST_PREFIX)
        )
    )


def _validate_generated_asset_request(
    asset_id: str,
    asset: dict,
    generation_request_by_id: dict[str, dict],
    errors: list[str],
) -> str | None:
    seed_or_generation_id = asset.get("seed_or_generation_id")
    if not is_non_empty_string(seed_or_generation_id) or not seed_or_generation_id.startswith(
        GENERATION_REQUEST_PREFIX
    ):
        errors.append(
            f"generated asset seed_or_generation_id must reference generation request: {asset_id}"
        )
        return None

    request_id = seed_or_generation_id.removeprefix(GENERATION_REQUEST_PREFIX)
    if request_id not in generation_request_by_id:
        errors.append(
            f"generated asset seed_or_generation_id must reference existing generation request: "
            f"{asset_id} -> {seed_or_generation_id}"
        )
        return None

    return request_id


def _validate_generated_candidate_path(
    asset_id: str,
    asset: dict,
    request: dict,
    root: Path,
    errors: list[str],
) -> Path | None:
    candidate_path_value = asset.get("candidate_path")
    if candidate_path_value is None:
        return None
    if not is_non_empty_string(candidate_path_value):
        errors.append(f"candidate_path must be a non-empty string: {asset_id}")
        return None

    candidate_path = Path(candidate_path_value)
    if candidate_path.is_absolute():
        errors.append(f"candidate_path must be relative: {asset_id}")
        return None

    generated_root = (root / GENERATED_CANDIDATE_DIR).resolve()
    resolved_path = (root / candidate_path).resolve()
    try:
        resolved_path.relative_to(generated_root)
    except ValueError:
        errors.append(
            f"candidate_path must be under {GENERATED_CANDIDATE_DIR.as_posix()}: {asset_id}"
        )
        return None

    return resolved_path


def validate_source_manifest(data: dict, root: Path, errors: list[str]) -> None:
    assets = data.get("assets", [])
    if not isinstance(assets, list):
        errors.append("source assets must be a list")
        return

    if data.get("asset_count") != len(assets):
        errors.append("source asset_count must equal assets length")
    if data.get("asset_count") != len(SOURCE_ASSETS):
        errors.append(f"source asset_count must be {len(SOURCE_ASSETS)}")
    if len(assets) != len(SOURCE_ASSETS):
        errors.append(f"source assets length must be {len(SOURCE_ASSETS)}")

    ids = set()
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append("source assets must be objects")
            continue
        raw_asset_id = asset.get("id", f"asset[{index}]")
        if not is_non_empty_string(raw_asset_id):
            errors.append(f"source asset id must be a non-empty string: asset[{index}]")
            asset_id = f"asset[{index}]"
        else:
            asset_id = raw_asset_id

        if asset_id in ids:
            errors.append(f"duplicate source asset id: {asset_id}")
        ids.add(asset_id)

        if index < len(SOURCE_ASSETS):
            expected = SOURCE_ASSETS[index]
            expected_fields = {
                "id": expected["id"],
                "original_filename": expected["filename"],
                "role": expected["role"],
                "orientation_state": expected["orientation_state"],
            }
            for field, expected_value in expected_fields.items():
                actual_value = asset.get(field)
                if actual_value != expected_value:
                    errors.append(
                        f"source catalog mismatch at index {index} for {field}: "
                        f"expected {expected_value} got {actual_value}"
                    )

        _validate_source_path(asset, root, errors)
        if asset.get("colorspace") not in {"sRGB", "RGB"}:
            errors.append(
                f"unexpected colorspace for {asset_id}: {asset.get('colorspace')}"
            )

    expected_ids = {asset["id"] for asset in SOURCE_ASSETS}
    if set(ids) != expected_ids:
        errors.append(
            "source asset ids must match catalog: expected "
            f"{sorted(expected_ids)} got {sorted(ids)}"
        )


def _source_path_for_verification(asset: dict, root: Path) -> Path | None:
    path_errors: list[str] = []
    path = _validate_source_path(asset, root, path_errors)
    if path_errors:
        return None
    return path


def verify_source_files(
    data: dict,
    root: Path,
    errors: list[str],
    *,
    file_exists=None,
    hash_reader=None,
    metadata_reader=None,
) -> None:
    file_exists = (lambda path: path.is_file()) if file_exists is None else file_exists
    hash_reader = sha256 if hash_reader is None else hash_reader
    metadata_reader = image_metadata if metadata_reader is None else metadata_reader

    assets = data.get("assets", [])
    if not isinstance(assets, list):
        return
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        asset_id = asset.get("id", "<missing id>")
        path = _source_path_for_verification(asset, root)
        if path is None:
            continue
        if not file_exists(path):
            errors.append(f"missing source asset: {asset.get('source_path')}")
            continue

        actual_hash = hash_reader(path)
        if actual_hash != asset.get("sha256"):
            errors.append(f"sha256 mismatch: {asset_id}")

        try:
            actual_metadata = metadata_reader(path)
        except subprocess.CalledProcessError as error:
            errors.append(f"metadata read failed for {asset_id}: {error}")
            continue

        for field in ("width", "height", "colorspace"):
            if asset.get(field) != actual_metadata[field]:
                errors.append(
                    f"metadata mismatch for {asset_id} {field}: "
                    f"manifest {asset.get(field)} actual {actual_metadata[field]}"
                )


def audit_source_manifest(
    source_manifest_path: Path | None = None,
    root: Path | None = None,
) -> list[str]:
    source_manifest_path = (
        SOURCE_MANIFEST if source_manifest_path is None else source_manifest_path
    )
    root = ROOT if root is None else root
    data = load_json(source_manifest_path)
    errors: list[str] = []
    validate_source_manifest(data, root, errors)
    verify_source_files(data, root, errors)
    return errors


def audit_asset_manifest(
    data: dict,
    source: dict,
    palette: dict,
    errors: list[str],
    generation_request_by_id: dict[str, dict] | None = None,
    root: Path | None = None,
) -> tuple[set[str], set[str]]:
    generation_request_by_id = (
        {} if generation_request_by_id is None else generation_request_by_id
    )
    root = ROOT if root is None else root
    palette_version = palette.get("palette_version")
    if data.get("palette_version") != palette_version:
        errors.append("asset-manifest palette_version must match palette palette_version")

    source_assets = source.get("assets", [])
    source_ids = {
        asset["id"]
        for asset in source_assets
        if isinstance(asset, dict) and isinstance(asset.get("id"), str)
    }
    source_orientations = {
        asset["id"]: asset.get("orientation_state")
        for asset in source_assets
        if isinstance(asset, dict) and isinstance(asset.get("id"), str)
    }

    assets = data.get("assets", [])
    if not isinstance(assets, list):
        errors.append("asset-manifest assets must be a list")
        return set(), set()

    ids = set()
    accepted = set()
    generated_asset_request_ids = set()
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append("asset-manifest assets must be objects")
            continue

        raw_asset_id = asset.get("id")
        if not is_non_empty_string(raw_asset_id):
            errors.append(f"asset id must be a non-empty string: asset[{index}]")
            asset_id = f"asset[{index}]"
            valid_asset_id = False
        else:
            asset_id = raw_asset_id
            valid_asset_id = True

        if valid_asset_id:
            if asset_id in ids:
                errors.append(f"duplicate asset-manifest asset id: {asset_id}")
            ids.add(asset_id)

        status = asset.get("status")
        if not isinstance(status, str) or status not in ALLOWED_ASSET_STATUSES:
            errors.append(f"bad asset status: {asset_id}")
        if status == "accepted" and valid_asset_id:
            accepted.add(asset_id)
        elif asset.get("used_in_final_pdf", False):
            errors.append(f"unaccepted asset used in final PDF: {asset_id}")

        if asset.get("palette_version") != palette_version:
            errors.append(f"asset palette_version must match palette: {asset_id}")

        if (
            asset_id in source_orientations
            and asset.get("orientation_state") != source_orientations[asset_id]
        ):
            errors.append(f"asset orientation_state must match source asset: {asset_id}")

        source_inputs = asset.get("source_inputs")
        if not isinstance(source_inputs, list) or not source_inputs:
            errors.append(f"asset source_inputs must be a non-empty list: {asset_id}")
            continue

        for source_input in source_inputs:
            if not is_non_empty_string(source_input):
                errors.append(f"asset source_input must be a non-empty string: {asset_id}")
                continue
            if source_input not in source_ids:
                errors.append(
                    f"asset source_input must reference source asset: {asset_id} -> {source_input}"
                )

        if _is_generated_asset(asset):
            request_id = _validate_generated_asset_request(
                asset_id, asset, generation_request_by_id, errors
            )
            if request_id is not None:
                request = generation_request_by_id[request_id]
                request_status = request.get("status")
                if request_status == "queued":
                    errors.append(
                        "generated asset must not reference queued generation request: "
                        f"{asset_id} -> {request_id}"
                    )
                if request_status == "needs_review" and not is_non_empty_string(
                    asset.get("candidate_path")
                ):
                    errors.append(
                        f"needs_review generated asset candidate_path must be non-empty: {asset_id}"
                    )
                generated_asset_request_ids.add(request_id)
                _validate_generated_candidate_path(
                    asset_id,
                    asset,
                    request,
                    root,
                    errors,
                )

    missing_source_ids = source_ids - ids
    if missing_source_ids:
        errors.append(
            "asset-manifest must include all source asset ids: missing "
            f"{sorted(missing_source_ids)}"
        )

    return accepted, generated_asset_request_ids


def verify_generated_files(
    data: dict,
    generation_request_by_id: dict[str, dict],
    root: Path,
    errors: list[str],
    *,
    file_exists=None,
    metadata_reader=None,
) -> None:
    file_exists = (lambda path: path.is_file()) if file_exists is None else file_exists
    metadata_reader = image_metadata if metadata_reader is None else metadata_reader

    assets = data.get("assets", [])
    if not isinstance(assets, list):
        return
    for asset in assets:
        if not isinstance(asset, dict) or not _is_generated_asset(asset):
            continue
        asset_id = asset.get("id", "<missing id>")
        seed_or_generation_id = asset.get("seed_or_generation_id")
        if not (
            is_non_empty_string(seed_or_generation_id)
            and seed_or_generation_id.startswith(GENERATION_REQUEST_PREFIX)
        ):
            continue
        request_id = seed_or_generation_id.removeprefix(GENERATION_REQUEST_PREFIX)
        request = generation_request_by_id.get(request_id)
        if request is None:
            continue

        path_errors: list[str] = []
        resolved_path = _validate_generated_candidate_path(
            asset_id,
            asset,
            request,
            root,
            path_errors,
        )
        if resolved_path is None or path_errors:
            continue
        if not file_exists(resolved_path):
            errors.append(f"generated candidate missing: {asset.get('candidate_path')}")
            continue

        try:
            actual_metadata = metadata_reader(resolved_path)
        except subprocess.CalledProcessError as error:
            errors.append(
                f"generated candidate metadata read failed for {asset_id}: {error}"
            )
            continue

        if actual_metadata["colorspace"] not in {"sRGB", "RGB"}:
            errors.append(
                f"generated candidate colorspace must be sRGB/RGB for {asset_id}: "
                f"{actual_metadata['colorspace']}"
            )

        if (
            min(actual_metadata["width"], actual_metadata["height"])
            < MIN_GENERATED_CANDIDATE_DIMENSION
        ):
            errors.append(
                "generated candidate minimum dimensions must be at least "
                f"{MIN_GENERATED_CANDIDATE_DIMENSION}px for {asset_id}: "
                f"{actual_metadata['width']}x{actual_metadata['height']}"
            )
            continue

        ratio = parse_aspect_ratio(request.get("aspect_ratio"))
        if ratio is None:
            continue
        if not aspect_ratio_matches(
            actual_metadata["width"], actual_metadata["height"], ratio
        ):
            errors.append(
                f"generated candidate aspect ratio mismatch for {asset_id}: expected "
                f"{request.get('aspect_ratio')} got "
                f"{actual_metadata['width']}x{actual_metadata['height']}"
            )


def audit_page_manifest(data: dict, accepted_asset_ids: set[str], errors: list[str]) -> set[int]:
    pages = data.get("pages", [])
    if not isinstance(pages, list):
        errors.append("page-manifest pages must be a list")
        return set()

    page_count = data.get("page_count")
    if page_count != len(pages):
        errors.append("page-manifest page_count must equal pages length")
    if page_count != 14 or len(pages) != 14:
        errors.append("page-manifest must define 14 pages")

    page_numbers = []
    page_ids = set()
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            errors.append("page-manifest pages must be objects")
            continue

        page_number = page.get("page")
        page_numbers.append(page_number)
        if not isinstance(page_number, int) or isinstance(page_number, bool):
            errors.append(f"page number must be an integer: page[{index}]")

        page_id = page.get("id")
        if not is_non_empty_string(page_id):
            errors.append(f"page id must be a non-empty string: page[{index}]")
        elif page_id in page_ids:
            errors.append(f"duplicate page id: {page_id}")
        else:
            page_ids.add(page_id)

        title = page.get("title")
        if not is_non_empty_string(title):
            errors.append(f"page title must be a non-empty string: page[{index}]")
        elif JAPANESE_TEXT_RE.search(title):
            errors.append(f"page title must not contain Japanese characters: {page_id}")

        source_inputs = page.get("source_inputs")
        if not isinstance(source_inputs, list) or not source_inputs:
            errors.append(f"page source_inputs must be a non-empty list: page[{index}]")
            continue

        for asset_id in source_inputs:
            if not is_non_empty_string(asset_id):
                errors.append(
                    f"page source_input must be a non-empty string: {page_number}"
                )
                continue
            if asset_id not in accepted_asset_ids:
                errors.append(
                    f"page source_input must reference accepted asset: {page_number} -> {asset_id}"
                )

    expected_numbers = list(range(1, 15))
    if page_numbers != expected_numbers:
        errors.append(
            "page-manifest page numbers must be 1..14: got "
            f"{page_numbers}"
        )

    return {number for number in page_numbers if isinstance(number, int)}


def audit_generation_requests(
    data: dict,
    page_numbers: set[int],
    errors: list[str],
    generated_asset_request_ids: set[str],
) -> None:
    requests = data.get("requests", [])
    if not isinstance(requests, list):
        errors.append("generation-requests requests must be a list")
        return

    ids = set()
    for index, request in enumerate(requests):
        if not isinstance(request, dict):
            errors.append("generation-requests requests must be objects")
            continue

        raw_request_id = request.get("id")
        if not is_non_empty_string(raw_request_id):
            errors.append(f"generation request id must be a non-empty string: request[{index}]")
            request_id = f"request[{index}]"
            valid_request_id = False
        else:
            request_id = raw_request_id
            valid_request_id = True

        if valid_request_id:
            if request_id in ids:
                errors.append(f"duplicate generation request id: {request_id}")
            ids.add(request_id)

        status = request.get("status")
        if not is_non_empty_string(status):
            errors.append(f"generation request status must be a non-empty string: {request_id}")
        elif status not in ALLOWED_GENERATION_REQUEST_STATUSES:
            errors.append(
                "generation request status must be queued, needs_review, or "
                f"accepted: {request_id}"
            )
        elif (
            status in {"needs_review", "accepted"}
            and valid_request_id
            and request_id not in generated_asset_request_ids
        ):
            errors.append(
                f"{status} generation request must have generated asset: {request_id}"
            )

        target_page = request.get("target_page")
        if not isinstance(target_page, int) or isinstance(target_page, bool):
            errors.append(f"generation request target_page must be an integer: {request_id}")
        elif target_page not in page_numbers:
            errors.append(f"generation request target_page must exist: {request_id}")

        aspect_ratio = request.get("aspect_ratio")
        if not is_non_empty_string(aspect_ratio):
            errors.append(f"generation request aspect_ratio must be non-empty: {request_id}")
        elif not ASPECT_RATIO_RE.fullmatch(aspect_ratio):
            errors.append(
                f"generation request aspect_ratio must be positive integer ratio: {request_id}"
            )

        for field in ("prompt", "acceptance"):
            value = request.get(field)
            if not is_non_empty_string(value):
                errors.append(f"generation request {field} must be non-empty: {request_id}")


def verify_manifest_files(
    source: dict,
    asset_manifest: dict,
    generation_requests: dict,
    root: Path,
    *,
    file_exists=None,
    hash_reader=None,
    metadata_reader=None,
) -> list[str]:
    errors: list[str] = []
    verify_source_files(
        source,
        root,
        errors,
        file_exists=file_exists,
        hash_reader=hash_reader,
        metadata_reader=metadata_reader,
    )
    verify_generated_files(
        asset_manifest,
        generation_requests_by_id(generation_requests),
        root,
        errors,
        file_exists=file_exists,
        metadata_reader=metadata_reader,
    )
    return errors


def audit_manifest_data(
    source: dict,
    asset_manifest: dict,
    page_manifest: dict,
    generation_requests: dict,
    palette: dict,
    root: Path,
) -> list[str]:
    errors: list[str] = []
    validate_source_manifest(source, root, errors)

    generation_request_by_id = generation_requests_by_id(generation_requests)
    accepted_asset_ids, generated_asset_request_ids = audit_asset_manifest(
        asset_manifest,
        source,
        palette,
        errors,
        generation_request_by_id,
        root,
    )
    page_numbers = audit_page_manifest(page_manifest, accepted_asset_ids, errors)
    audit_generation_requests(
        generation_requests,
        page_numbers,
        errors,
        generated_asset_request_ids,
    )

    return errors


def main() -> int:
    errors: list[str] = []
    source = load_required_json(SOURCE_MANIFEST, "source-assets", errors)
    palette = load_required_json(PALETTE, "palette", errors)
    asset_manifest = load_required_json(ASSET_MANIFEST, "asset-manifest", errors)
    page_manifest = load_required_json(PAGE_MANIFEST, "page-manifest", errors)
    generation_requests = load_required_json(
        GENERATION_REQUESTS, "generation-requests", errors
    )

    errors.extend(
        audit_manifest_data(
            source,
            asset_manifest,
            page_manifest,
            generation_requests,
            palette,
            ROOT,
        )
    )
    errors.extend(
        verify_manifest_files(
            source,
            asset_manifest,
            generation_requests,
            ROOT,
        )
    )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("asset audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

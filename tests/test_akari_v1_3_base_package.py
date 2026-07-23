from pathlib import Path
import copy
import hashlib
import shutil
import tempfile
import unittest

import yaml

from scripts.validate_akari_v1_3_base import (
    ASSET_CONTRACT,
    ValidationError,
    validate_assets,
    validate_inheritance,
    validate_package,
    validate_review_log,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.3"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    if not isinstance(data, dict):
        raise AssertionError(f"expected mapping: {path}")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(data, stream, sort_keys=False)


def build_empty_package(package_root: Path) -> tuple[dict, dict]:
    shutil.copytree(PACKAGE_ROOT, package_root, dirs_exist_ok=True)
    for scratch_path in (
        package_root / "source/candidates",
        package_root / "comparisons",
    ):
        if scratch_path.exists():
            shutil.rmtree(scratch_path)
    assets = load_yaml(package_root / "manifest/assets.yaml")
    review_log = load_yaml(package_root / "manifest/review-log.yaml")
    for asset in assets["assets"]:
        asset["status"] = "planned"
        asset["revision"] = None
        asset["accepted_paths"] = []
    review_log["reviews"] = []
    review_log["base_identity_lock"] = {
        "status": "pending",
        "v13_01_revision": None,
        "v13_02_revision": None,
        "same_person_verdict": None,
        "user_confirmed": False,
    }
    write_yaml(package_root / "manifest/assets.yaml", assets)
    write_yaml(package_root / "manifest/review-log.yaml", review_log)
    return assets, review_log


def build_complete_package(package_root: Path) -> tuple[dict, dict]:
    assets, review_log = build_empty_package(package_root)
    reference = package_root / "references/style/akari-v04-a.png"
    reference_hash = sha256_file(reference)

    for asset in assets["assets"]:
        contract = ASSET_CONTRACT[asset["asset_id"]]
        accepted_paths = [
            expected.replace("rNN", "r01") for expected in asset["expected_paths"]
        ]
        source_paths = []
        for index, accepted_path in enumerate(accepted_paths):
            promoted = package_root / accepted_path
            promoted.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(reference, promoted)
            source_paths.append(
                f"source/candidates/{asset['asset_id'].lower()}/r01/"
                f"candidate-{index + 1}.png"
            )

        asset["status"] = "accepted"
        asset["revision"] = "r01"
        asset["accepted_paths"] = accepted_paths
        review_log["reviews"].append(
            {
                "candidate_id": f"{asset['asset_id']}-r01-a",
                "asset_id": asset["asset_id"],
                "revision": "r01",
                "status": "accepted",
                "user_selected": True,
                "source_paths": source_paths,
                "promoted_paths": accepted_paths,
                "source_sha256": [reference_hash] * len(accepted_paths),
                "promoted_sha256": [reference_hash] * len(accepted_paths),
                "overall_verdict": "pass",
                "gate_verdicts": {
                    gate: "pass" for gate in contract["required_review_gates"]
                },
                "findings": [],
                "decision": "selected for complete-package fixture",
            }
        )

    review_log["base_identity_lock"] = {
        "status": "accepted",
        "v13_01_revision": "r01",
        "v13_02_revision": "r01",
        "same_person_verdict": "pass",
        "user_confirmed": True,
    }
    write_yaml(package_root / "manifest/assets.yaml", assets)
    write_yaml(package_root / "manifest/review-log.yaml", review_log)
    return assets, review_log


class V13PackageBoundaryTests(unittest.TestCase):
    def test_required_package_files_exist(self):
        expected = (
            "README.md",
            "docs/akari-v1.3-base-design.md",
            "manifest/assets.yaml",
            "manifest/inheritance.yaml",
            "manifest/review-log.yaml",
            "references/style/akari-v04-a.png",
            "references/v1.2/akari-v1.2_c01_front-natural-stance_r01.png",
            "accepted/base/key-visual/.gitkeep",
            "accepted/base/full-body/.gitkeep",
            "accepted/base/expressions/.gitkeep",
            "accepted/base/wardrobe/.gitkeep",
        )
        for relative_path in expected:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((PACKAGE_ROOT / relative_path).is_file())

    def test_copied_references_match_sources_and_pins(self):
        pairs = (
            (
                ROOT / "source/references/style-study/akari-v04-a.png",
                PACKAGE_ROOT / "references/style/akari-v04-a.png",
                "aafad35807788120542bd650039da6f88297de8f366534ab3d2c38920100c579",
            ),
            (
                ROOT
                / "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
                PACKAGE_ROOT
                / "references/v1.2/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
                "a977f2798d15f3da9ef0d7720d6f9fc41bd2f84f54f4c8a69908a482596a75c5",
            ),
        )
        for source, copied, expected_sha in pairs:
            with self.subTest(copied=copied):
                self.assertEqual(source.read_bytes(), copied.read_bytes())
                self.assertEqual(expected_sha, sha256_file(copied))

    def test_initial_assets_define_four_ids_and_six_images(self):
        data = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        self.assertEqual(data["required_image_count"], 6)
        self.assertEqual(
            [asset["asset_id"] for asset in data["assets"]],
            ["V13-01", "V13-02", "V13-03", "V13-04"],
        )
        self.assertEqual(sum(len(asset["variants"]) for asset in data["assets"]), 6)

    def test_package_docs_keep_base_definition_scope(self):
        readme = (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8")
        design = (PACKAGE_ROOT / "docs/akari-v1.3-base-design.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Base Definition", readme)
        self.assertIn("V13-01", design)
        self.assertIn("V13-04B", design)
        self.assertNotIn("settings PDF", readme)

    def test_completed_docs_register_all_six_images(self):
        readme = (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8")
        design = (PACKAGE_ROOT / "docs/akari-v1.3-base-design.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Status: Base Definition complete.", readme)
        for asset in (
            "V13-01",
            "V13-02",
            "V13-03A",
            "V13-03B",
            "V13-04A",
            "V13-04B",
        ):
            with self.subTest(asset=asset):
                self.assertIn(asset, design)
        self.assertIn("Base Identity Lock: Pass", design)


class V13ValidatorTests(unittest.TestCase):
    def test_incomplete_package_passes_static_validation(self):
        validate_package(require_complete=False)

    def test_complete_validation_requires_six_accepted_images(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "akari-v1.3"
            build_empty_package(package_root)

            with self.assertRaisesRegex(
                ValidationError, "required accepted image count: expected 6, got 0"
            ):
                validate_package(
                    package_root=package_root,
                    repo_root=ROOT,
                    require_complete=True,
                )

    def test_assets_reject_missing_v13_03_variant(self):
        assets = copy.deepcopy(load_yaml(PACKAGE_ROOT / "manifest/assets.yaml"))
        assets["assets"][2]["variants"] = ["everyday"]

        with self.assertRaisesRegex(ValidationError, "V13-03 variants"):
            validate_assets(assets, PACKAGE_ROOT)

    def test_assets_reject_unknown_dependency(self):
        assets = copy.deepcopy(load_yaml(PACKAGE_ROOT / "manifest/assets.yaml"))
        assets["assets"][1]["depends_on"] = ["V13-99"]

        with self.assertRaisesRegex(ValidationError, "unknown dependency V13-99"):
            validate_assets(assets, PACKAGE_ROOT)

    def test_inheritance_rejects_copied_reference_hash_mismatch(self):
        inheritance = copy.deepcopy(
            load_yaml(PACKAGE_ROOT / "manifest/inheritance.yaml")
        )
        inheritance["references"][0]["sha256"] = "0" * 64

        with self.assertRaisesRegex(ValidationError, "style-v04-a.*SHA-256"):
            validate_inheritance(inheritance, ROOT)

    def test_inheritance_requires_c01_to_exclude_face_authority(self):
        inheritance = copy.deepcopy(
            load_yaml(PACKAGE_ROOT / "manifest/inheritance.yaml")
        )
        inheritance["references"][1]["excluded_traits"].remove("face")

        with self.assertRaisesRegex(ValidationError, "v1.2-c01-standing.*face"):
            validate_inheritance(inheritance, ROOT)

    def test_accepted_review_rejects_major_overall_verdict(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "akari-v1.3"
            assets, review_log = build_complete_package(package_root)
            review_log["reviews"][0]["overall_verdict"] = "major"

            with self.assertRaisesRegex(
                ValidationError, "V13-01 accepted review must have overall pass"
            ):
                validate_review_log(review_log, assets, package_root, True)

    def test_accepted_review_requires_explicit_user_selection(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "akari-v1.3"
            assets, review_log = build_complete_package(package_root)
            review_log["reviews"][0]["user_selected"] = False

            with self.assertRaisesRegex(
                ValidationError, "V13-01 accepted review requires user_selected"
            ):
                validate_review_log(review_log, assets, package_root, True)

    def test_accepted_review_rejects_source_and_promoted_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "akari-v1.3"
            assets, review_log = build_complete_package(package_root)
            review_log["reviews"][0]["source_sha256"] = ["0" * 64]

            with self.assertRaisesRegex(
                ValidationError, "V13-01 source and promoted hashes must match"
            ):
                validate_review_log(review_log, assets, package_root, True)

    def test_accepted_review_rejects_computed_promoted_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "akari-v1.3"
            assets, review_log = build_complete_package(package_root)
            review_log["reviews"][0]["source_sha256"] = ["0" * 64]
            review_log["reviews"][0]["promoted_sha256"] = ["0" * 64]

            with self.assertRaisesRegex(
                ValidationError, "V13-01 promoted SHA-256 mismatch"
            ):
                validate_review_log(review_log, assets, package_root, True)

    def test_downstream_acceptance_requires_base_identity_lock(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "akari-v1.3"
            assets, review_log = build_complete_package(package_root)
            review_log["base_identity_lock"] = {
                "status": "pending",
                "v13_01_revision": None,
                "v13_02_revision": None,
                "same_person_verdict": None,
                "user_confirmed": False,
            }

            with self.assertRaisesRegex(
                ValidationError, "V13-03 acceptance requires Base Identity Lock"
            ):
                validate_review_log(review_log, assets, package_root, True)

    def test_complete_package_is_valid_without_ignored_candidates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "akari-v1.3"
            build_complete_package(package_root)

            self.assertFalse((package_root / "source/candidates").exists())
            validate_package(
                package_root=package_root,
                repo_root=ROOT,
                require_complete=True,
            )


if __name__ == "__main__":
    unittest.main()

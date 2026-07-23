import copy
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"

sys.path.insert(0, str(ROOT))

from scripts.validate_akari_v1_2_natural_form import (  # noqa: E402
    ValidationError,
    candidate_source_paths,
    count_generation_work,
    load_generation_requests,
    load_yaml,
    sha256_file,
    validate_assets,
    validate_d01_candidate_dimensions,
    validate_d01_png_dimensions,
    validate_gate4,
    validate_generation_dependencies,
    validate_generation_request,
    validate_inheritance,
    validate_lifecycle_linkage,
    validate_review_log,
)


def fixture_fingerprint(*values: object) -> str:
    serialized = json.dumps(
        values,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


class ImmutableFixtureTestCase(unittest.TestCase):
    @classmethod
    def freeze_fixtures(cls, *names: str) -> None:
        cls._shared_fixture_names = names
        cls._shared_fixture_fingerprint = fixture_fingerprint(
            *(getattr(cls, name) for name in names)
        )

    @classmethod
    def tearDownClass(cls):
        try:
            current = fixture_fingerprint(
                *(getattr(cls, name) for name in cls._shared_fixture_names)
            )
            if current != cls._shared_fixture_fingerprint:
                raise AssertionError(
                    f"{cls.__name__} mutated its shared canonical fixture"
                )
        finally:
            super().tearDownClass()


class NaturalFormSharedFixtureTests(unittest.TestCase):
    def test_fixture_fingerprint_detects_nested_mutation(self):
        fixture = {"assets": [{"asset_id": "C01", "status": "accepted"}]}
        before = fixture_fingerprint(fixture)
        fixture["assets"][0]["status"] = "candidate"
        self.assertNotEqual(before, fixture_fingerprint(fixture))


class NaturalFormD01DimensionTests(ImmutableFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml"
        )
        cls.freeze_fixtures("request")

    def test_accepts_target_and_all_tolerance_corners(self):
        sizes = (
            (1024, 1536),
            (1020, 1532),
            (1020, 1540),
            (1028, 1532),
            (1028, 1540),
        )
        for size in sizes:
            with self.subTest(size=size), TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / self.request["candidates"][0]["target_path"]
                source.parent.mkdir(parents=True)
                Image.new("RGB", size, "white").save(source)
                validate_d01_candidate_dimensions(self.request, root)

    def test_rejects_each_just_outside_dimension(self):
        sizes = ((1019, 1536), (1029, 1536), (1024, 1531), (1024, 1541))
        for size in sizes:
            with self.subTest(size=size), TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / self.request["candidates"][0]["target_path"]
                source.parent.mkdir(parents=True)
                Image.new("RGB", size, "white").save(source)
                with self.assertRaisesRegex(
                    ValidationError,
                    "D01 r01: candidate dimensions outside "
                    "1020-1028 x 1532-1540",
                ):
                    validate_d01_candidate_dimensions(self.request, root)

    def test_allows_declared_candidates_to_be_absent_before_generation(self):
        with TemporaryDirectory() as directory:
            validate_d01_candidate_dimensions(self.request, Path(directory))

    def test_rejects_outside_tolerance_promoted_png(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "accepted.png"
            Image.new("RGB", (1019, 1536), "white").save(source)
            with self.assertRaisesRegex(
                ValidationError,
                "D01 r01: candidate dimensions outside "
                "1020-1028 x 1532-1540",
            ):
                validate_d01_png_dimensions(source)

    def test_rejects_jpeg_bytes_with_png_suffix(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "not-really.png"
            Image.new("RGB", (1024, 1536), "white").save(
                source, format="JPEG"
            )
            with self.assertRaisesRegex(
                ValidationError, "D01 r01: candidate must be PNG"
            ):
                validate_d01_png_dimensions(source)


class NaturalFormPackageTests(unittest.TestCase):
    def test_required_documentation_exists(self):
        expected = {
            "README.md",
            "docs/akari-v1.2-core-design.md",
            "docs/akari-v1.2-review-guide.md",
            "docs/akari-v1.2-change-summary.md",
            "docs/akari-v1.2-daily-handoff.md",
            "docs/akari-v1.2-daily-wave-1.md",
            "docs/akari-v1.2-daily-wave-2.md",
            "docs/akari-v1.2-daily-wave-3.md",
        }
        actual = {
            path.relative_to(PACKAGE_ROOT).as_posix()
            for path in PACKAGE_ROOT.rglob("*.md")
        }
        self.assertTrue(expected.issubset(actual))

    def test_daily_wave_one_release_registers_all_five_accepted_scenes(self):
        text = (PACKAGE_ROOT / "docs/akari-v1.2-daily-wave-1.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Daily.1", text)
        self.assertIn("Wave 1 Complete", text)
        for asset_id in ("D01", "D02", "D03", "D04", "D05"):
            with self.subTest(asset_id=asset_id):
                self.assertIn(asset_id, text)
        self.assertIn("Core unchanged", text)

    def test_daily_wave_two_release_registers_all_five_accepted_scenes(self):
        text = (PACKAGE_ROOT / "docs/akari-v1.2-daily-wave-2.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Daily.2", text)
        self.assertIn("Wave 2 Complete", text)
        expected = {
            "D06": ("r01", "d06-r01-a"),
            "D07": ("r01", "d07-r01-b"),
            "D08": ("r03", "d08-r03-a"),
            "D09": ("r01", "d09-r01-a"),
            "D10": ("r01", "d10-r01-a"),
        }
        for asset_id, (revision, candidate_id) in expected.items():
            with self.subTest(asset_id=asset_id):
                self.assertIn(
                    f"| {asset_id} | {revision} | {candidate_id} |",
                    text,
                )
        self.assertIn("Core unchanged", text)
        self.assertIn("Wave 3 starts at D11", text)

    def test_daily_wave_three_release_registers_all_five_accepted_scenes(self):
        text = (PACKAGE_ROOT / "docs/akari-v1.2-daily-wave-3.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Daily.3", text)
        self.assertIn("Wave 3 Complete", text)
        expected = {
            "D11": ("r02", "d11-r02-b"),
            "D12": ("r01", "d12-r01-a"),
            "D13": ("r02", "d13-r02-b"),
            "D14": ("r02", "d14-r02-b"),
            "D15": ("r01", "d15-r01-a"),
        }
        for asset_id, (revision, candidate_id) in expected.items():
            with self.subTest(asset_id=asset_id):
                self.assertIn(
                    f"| {asset_id} | {revision} | {candidate_id} |",
                    text,
                )
        self.assertIn("Core unchanged", text)
        self.assertIn("ce3bebe", text)
        self.assertIn("643cf2ce58c3f320250c4cd85428cc0087fccc70", text)

    def test_daily_handoff_records_d01_through_d15_completion(self):
        text = (
            PACKAGE_ROOT / "docs/akari-v1.2-daily-handoff.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Daily.3 / Wave 3 is complete", text)
        self.assertIn("D01-D15 accepted", text)
        for register in ("wave-1", "wave-2", "wave-3"):
            with self.subTest(register=register):
                self.assertIn(
                    f"docs/akari-v1.2-daily-{register}.md",
                    text,
                )
        self.assertIn("643cf2ce58c3f320250c4cd85428cc0087fccc70", text)

    def test_core_design_is_the_v1_2_0_release(self):
        text = (PACKAGE_ROOT / "docs/akari-v1.2-core-design.md").read_text()
        self.assertIn("**Version:** v1.2.0", text)
        self.assertIn("**Codename:** Natural Form", text)
        self.assertIn("**Status:** Natural Form Core Release", text)
        self.assertIn(
            "The v1.2.0 PDF and SHA-256 checksum are published under `release/`.",
            text,
        )
        self.assertIn(
            "現在は Natural Form Core Release。C01〜C07 と D01 の採用、"
            "Gate 4 通過により v1.2.0 Release とする。",
            text,
        )
        self.assertNotIn(
            "現在は Design Approved / Pre-production。画像アセットが未制作のため "
            "v1.2.0 Release ではない。",
            text,
        )
        self.assertIn(
            "Status: Natural Form Core Release.",
            (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "第22〜23節はライブ進捗ではなく、再利用可能な受け入れ・"
            "レビューテンプレートである。",
            text,
        )

    def test_working_directories_are_tracked(self):
        expected = (
            "source/candidates/.gitkeep",
            "source/rejected/.gitkeep",
            "source/superseded/.gitkeep",
            "accepted/core/standing/.gitkeep",
            "accepted/core/sitting/.gitkeep",
            "accepted/core/face-hair/.gitkeep",
            "accepted/core/indoor-feet/.gitkeep",
            "accepted/daily-validation/.gitkeep",
            "comparisons/.gitkeep",
        )
        for relative_path in expected:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((PACKAGE_ROOT / relative_path).is_file())
        self.assertFalse((PACKAGE_ROOT / "release/.gitkeep").exists())

    def test_release_guidance_uses_v1_2_default_and_preserves_v1_1(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        package_readme = (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8")
        daily_handoff = (
            PACKAGE_ROOT / "docs/akari-v1.2-daily-handoff.md"
        ).read_text(encoding="utf-8")

        for text in (agents, root_readme, package_readme):
            self.assertIn(
                "akari-v1.2/release/akari-v1.2-core-settings.pdf", text
            )
            self.assertIn("dist/akari-v1.1-settings.pdf", text)
        self.assertIn("akari-v1.2/release/checksums.txt", package_readme)
        self.assertIn("npm run release:v1-2", package_readme)
        self.assertIn("Daily.3 / Wave 3 is complete", daily_handoff)
        self.assertIn("D01-D15 accepted", daily_handoff)


class NaturalFormManifestTests(ImmutableFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.assets = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        cls.review_log = load_yaml(PACKAGE_ROOT / "manifest/review-log.yaml")
        cls.freeze_fixtures("assets", "review_log")

    def test_assets_define_the_exact_core_and_daily_contract(self):
        validate_assets(self.assets)
        self.assertEqual(
            [item["asset_id"] for item in self.assets["assets"]],
            [
                "C01",
                "C02",
                "C03",
                "C04",
                "C05",
                "C06",
                "C07",
                "D01",
                "D02",
                "D03",
                "D04",
                "D05",
                "D06",
                "D07",
                "D08",
                "D09",
                "D10",
                "D11",
                "D12",
                "D13",
                "D14",
                "D15",
            ],
        )

    def test_d01_has_exact_static_asset_contract(self):
        d01 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "D01"
        )
        self.assertEqual(
            {key: d01[key] for key in (
                "descriptor", "phase", "variants", "expected_paths",
                "depends_on", "gate",
            )},
            {
                "descriptor": "morning-bedside",
                "phase": 4,
                "variants": ["default"],
                "expected_paths": [
                    "accepted/daily-validation/"
                    "akari-v1.2_d01_morning-bedside_rNN.png"
                ],
                "depends_on": ["C04", "C05", "C06", "C07"],
                "gate": "daily",
            },
        )

    def test_c06_rejects_static_contract_mutations(self):
        alternative_expected_paths = [
            "accepted/core/face-hair/"
            "akari-v1.2_c06-1_sleepy-neutral_rNN.png",
            "accepted/core/face-hair/"
            "akari-v1.2_c06-2_sleepy-secure_rNN.png",
            "accepted/core/face-hair/"
            "akari-v1.2_c06-3_loosened-mouth_rNN.png",
            "accepted/core/face-hair/"
            "akari-v1.2_c06-4_gentle-smile_rNN.png",
        ]
        mutations = {
            "descriptor": "daily-smile-gradient-alt",
            "phase": 4,
            "variants": [
                "sleepy-secure",
                "sleepy-neutral",
                "loosened-mouth",
                "soft-smile",
            ],
            "expected_paths": alternative_expected_paths,
            "depends_on": ["C01"],
            "gate": "daily",
        }
        for field, alternative in mutations.items():
            with self.subTest(field=field):
                invalid = copy.deepcopy(self.assets)
                c06 = next(
                    item
                    for item in invalid["assets"]
                    if item["asset_id"] == "C06"
                )
                c06[field] = copy.deepcopy(alternative)
                if field == "expected_paths":
                    c06["accepted_paths"] = [
                        path.replace("rNN", "r01")
                        for path in alternative_expected_paths
                    ]
                with self.assertRaisesRegex(
                    ValidationError, "C06: static asset contract mismatch"
                ):
                    validate_assets(invalid)

    def test_assets_reject_an_accepted_item_without_accepted_paths(self):
        invalid = copy.deepcopy(self.assets)
        invalid["assets"][0]["status"] = "accepted"
        invalid["assets"][0]["revision"] = "r01"
        invalid["assets"][0]["accepted_paths"] = []
        with self.assertRaisesRegex(ValidationError, "accepted_paths"):
            validate_assets(invalid)

    def test_assets_reject_an_unknown_dependency(self):
        invalid = copy.deepcopy(self.assets)
        invalid["assets"][0]["depends_on"] = ["C99"]
        with self.assertRaisesRegex(ValidationError, "unknown dependency"):
            validate_assets(invalid)

    def test_assets_reject_paths_outside_the_canonical_package(self):
        invalid = copy.deepcopy(self.assets)
        invalid["assets"][0]["expected_paths"] = ["legacy/c01.png"]
        with self.assertRaisesRegex(ValidationError, "expected_paths"):
            validate_assets(invalid)

    def test_assets_use_ordered_accepted_paths(self):
        for asset in self.assets["assets"]:
            self.assertIsInstance(asset.get("accepted_paths"), list)
            self.assertNotIn("accepted_path", asset)

    def test_assets_reject_accepted_path_count_mismatch(self):
        invalid = copy.deepcopy(self.assets)
        c01 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C01"
        )
        c01["accepted_paths"] = []
        with self.assertRaisesRegex(ValidationError, "accepted_paths must match"):
            validate_assets(invalid)

    def test_c05_rejects_accepted_with_notes(self):
        invalid = copy.deepcopy(self.assets)
        c05 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C05"
        )
        c05.update(
            status="accepted-with-notes",
            revision="r01",
            accepted_paths=[
                "accepted/core/face-hair/"
                "akari-v1.2_c05_morning-bedhair_r01.png"
            ],
        )
        with self.assertRaisesRegex(
            ValidationError, "C05: accepted-with-notes is not allowed"
        ):
            validate_assets(invalid)

    def test_c06_rejects_accepted_with_notes(self):
        invalid = copy.deepcopy(self.assets)
        c06 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C06"
        )
        c06.update(
            status="accepted-with-notes",
            revision="r01",
            accepted_paths=[
                path.replace("rNN", "r01") for path in c06["expected_paths"]
            ],
        )
        with self.assertRaisesRegex(
            ValidationError, "C06: accepted-with-notes is not allowed"
        ):
            validate_assets(invalid)

    def test_d01_acceptance_requires_complete_accepted_c06(self):
        invalid = copy.deepcopy(self.assets)
        c06 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C06"
        )
        c06.update(status="candidate", revision="r00", accepted_paths=[])
        d01 = next(
            item for item in invalid["assets"] if item["asset_id"] == "D01"
        )
        d01.update(
            status="accepted",
            revision="r01",
            accepted_paths=[
                path.replace("rNN", "r01") for path in d01["expected_paths"]
            ],
        )
        with self.assertRaisesRegex(
            ValidationError, "D01 acceptance requires accepted C06"
        ):
            validate_assets(invalid)

    def test_c06_acceptance_requires_strict_c05_acceptance(self):
        invalid = copy.deepcopy(self.assets)
        c05 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C05"
        )
        c05.update(status="candidate", revision="r00", accepted_paths=[])
        c06 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C06"
        )
        c06.update(
            status="accepted",
            revision="r01",
            accepted_paths=[
                path.replace("rNN", "r01") for path in c06["expected_paths"]
            ],
        )
        with self.assertRaisesRegex(
            ValidationError, "C06 acceptance requires accepted C05"
        ):
            validate_assets(invalid)

    def test_c06_may_be_accepted_after_strict_c05_acceptance(self):
        valid = copy.deepcopy(self.assets)
        c05 = next(
            item for item in valid["assets"] if item["asset_id"] == "C05"
        )
        c05.update(
            status="accepted",
            revision="r01",
            accepted_paths=[
                "accepted/core/face-hair/"
                "akari-v1.2_c05_morning-bedhair_r01.png"
            ],
        )
        c06 = next(
            item for item in valid["assets"] if item["asset_id"] == "C06"
        )
        c06.update(
            status="accepted",
            revision="r01",
            accepted_paths=[
                path.replace("rNN", "r01") for path in c06["expected_paths"]
            ],
        )
        validate_assets(valid)

    def test_review_log_accepts_live_c01_reviews_with_exact_enums(self):
        validate_review_log(self.review_log)
        self.assertEqual(
            self.review_log["allowed_statuses"],
            [
                "candidate",
                "review",
                "accepted",
                "accepted-with-notes",
                "rejected",
                "superseded",
            ],
        )
        self.assertEqual(
            self.review_log["allowed_severities"],
            ["blocker", "major", "minor"],
        )
        self.assertEqual(
            [
                review["candidate_id"]
                for review in self.review_log["reviews"]
                if review["asset_id"] == "C01"
            ],
            ["c01-r01-a", "c01-r01-b", "c01-r01-c"],
        )
        self.assertEqual(
            [
                review["status"]
                for review in self.review_log["reviews"]
                if review["asset_id"] == "C01"
            ],
            ["rejected", "accepted", "rejected"],
        )

    def test_reviews_use_ordered_paths_and_hashes(self):
        for review in self.review_log["reviews"]:
            self.assertIsInstance(review.get("source_paths"), list)
            self.assertIsInstance(review.get("source_sha256s"), list)
            self.assertEqual(
                len(review.get("source_paths", [])),
                len(review.get("source_sha256s", [])),
            )
            self.assertNotIn("source_path", review)

    def test_review_rejects_invalid_source_hash(self):
        invalid = copy.deepcopy(self.review_log)
        invalid["reviews"][0]["source_sha256s"] = ["not-a-sha256"]
        with self.assertRaisesRegex(ValidationError, "source SHA-256"):
            validate_review_log(invalid)

    def test_c03_r01_reviews_close_all_three_pairs_as_rejected(self):
        reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("C03", "r01")
        ]
        self.assertEqual(
            [review["candidate_id"] for review in reviews],
            ["c03-r01-a", "c03-r01-b", "c03-r01-c"],
        )
        self.assertEqual(
            [review["status"] for review in reviews],
            ["rejected"] * 3,
        )
        self.assertEqual(
            [review["source_sha256s"] for review in reviews],
            [
                [
                    "3fdf1dc9e5d15f438f512fc2750e05b9830f4f2fb5cad32a2afbcf20fe24d8e8",
                    "c681bff18d3dccc17f3edabbb45e4cd6356a66e3ac186581354b7d8586b2a61f",
                ],
                [
                    "5aa985aaeccac830aaa9c53819905aea02596a0e0cf2ff768ac348e5d7969374",
                    "98f1a3578f5056294610010f2116f2ae798da7cfaaa49ccabbda0703a6d0d4f8",
                ],
                [
                    "33d89602f14ed2f73dc6eac5c95ac7798c5d740fa909e7251546d0c50299fa47",
                    "7fc375236ca9ffe1c69d95e537af19745233bd153d60bfbab27277f4487e1d9a",
                ],
            ],
        )
        self.assertTrue(
            all(
                finding["resolved"] is False
                for review in reviews
                for finding in review["findings"]
                if finding["severity"] == "major"
            )
        )
        self.assertFalse(
            list(
                (PACKAGE_ROOT / "accepted/core/standing").glob(
                    "akari-v1.2_c03_*_r01.png"
                )
            )
        )


C06_STAGE_PAIRS = (
    ("c06-1", "sleepy-neutral"),
    ("c06-2", "sleepy-secure"),
    ("c06-3", "loosened-mouth"),
    ("c06-4", "soft-smile"),
)


def c06_candidate_path(stage_index: int, variant: str) -> str:
    stage, descriptor = C06_STAGE_PAIRS[stage_index]
    return (
        "source/candidates/c06/r01/"
        f"akari-v1.2_{stage}_{descriptor}_r01-{variant}.png"
    )


def make_c06_family(variant: str) -> dict:
    return {
        "variant": variant,
        "title": f"complete-family-{variant}",
        "outputs": [
            {
                "stage": stage,
                "descriptor": descriptor,
                "edit_source_role": "accepted_c05_edit_source",
                "target_path": c06_candidate_path(index, variant),
            }
            for index, (stage, descriptor) in enumerate(C06_STAGE_PAIRS)
        ],
    }


def inactive_c06_request(request: dict) -> dict:
    updated = copy.deepcopy(request)
    updated["candidates"] = updated["candidates"][:2]
    updated["repair_lane"] = {"mode": "inactive"}
    updated["review_sets"] = updated["review_sets"][:2]
    return updated


def targeted_c06_request(request: dict, base: str, stage_index: int) -> dict:
    updated = inactive_c06_request(request)
    stage, _ = C06_STAGE_PAIRS[stage_index]
    target = c06_candidate_path(stage_index, "c")
    updated["repair_lane"] = {
        "mode": "targeted-stage",
        "base_family": base,
        "stage": stage,
        "target_path": target,
    }
    family = next(
        candidate
        for candidate in updated["candidates"]
        if candidate["variant"] == base
    )
    sources = candidate_source_paths(family)
    sources[stage_index] = target
    updated["review_sets"].append(
        {
            "candidate_id": f"c06-r01-{base}-repair-{stage}",
            "source_paths": sources,
        }
    )
    return updated


def full_family_c06_request(request: dict) -> dict:
    updated = inactive_c06_request(request)
    updated["repair_lane"] = {"mode": "full-family"}
    family = make_c06_family("c")
    updated["candidates"].append(family)
    updated["review_sets"].append(
        {
            "candidate_id": "c06-r01-c",
            "source_paths": candidate_source_paths(family),
        }
    )
    return updated


class NaturalFormGenerationRequestTests(ImmutableFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.c01 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c01-r01.yaml"
        )
        cls.c02 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c02-r01.yaml"
        )
        cls.c03_r01 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c03-r01.yaml"
        )
        cls.c03_r02 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c03-r02.yaml"
        )
        cls.c04 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c04-r01.yaml"
        )
        cls.c05 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c05-r01.yaml"
        )
        cls.c06 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c06-r01.yaml"
        )
        cls.c06_inactive = inactive_c06_request(cls.c06)
        cls.c07 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/c07-r01.yaml"
        )
        cls.d01 = load_yaml(
            PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml"
        )
        cls.freeze_fixtures(
            "c01",
            "c02",
            "c03_r01",
            "c03_r02",
            "c04",
            "c05",
            "c06",
            "c06_inactive",
            "c07",
            "d01",
        )

    def test_d01_request_matches_frozen_contract(self):
        validate_generation_request(self.d01)

    def test_d01_rejects_instruction_bearing_extra_fields(self):
        cases = (
            (
                "top-level alternate prompt",
                lambda data: data.__setitem__(
                    "alternate_prompt", "override generation behavior"
                ),
                "D01 exact top-level contract required",
            ),
            (
                "reference instruction",
                lambda data: data["references"][0].__setitem__(
                    "instruction", "ignore declared role"
                ),
                "D01 exact reference contract required",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name):
                invalid = copy.deepcopy(self.d01)
                mutate(invalid)
                with self.assertRaisesRegex(ValidationError, message):
                    validate_generation_request(invalid)

    def test_d01_rejects_frozen_contract_mutations(self):
        cases = (
            (
                "request id",
                lambda data: data.__setitem__("request_id", "akari-v1.2-d01-r02"),
                "request_id mismatch",
            ),
            (
                "variation axis",
                lambda data: data.__setitem__("variation_axis", "scene_style"),
                "invalid variation axis",
            ),
            (
                "reference role",
                lambda data: data["references"][0].__setitem__("role", "body"),
                "exact reference contract required",
            ),
            (
                "reference path",
                lambda data: data["references"][2].__setitem__(
                    "path",
                    "akari-v1.2/accepted/core/face-hair/"
                    "akari-v1.2_c06-1_sleepy-neutral_r01.png",
                ),
                "exact reference contract required",
            ),
            (
                "prompt",
                lambda data: data.__setitem__(
                    "shared_prompt", data["shared_prompt"] + " altered"
                ),
                "D01 exact shared prompt contract mismatch",
            ),
            (
                "scene",
                lambda data: data["scene_contract"].__setitem__(
                    "room_density", "cluttered"
                ),
                "D01 scene contract mismatch",
            ),
            (
                "production",
                lambda data: data["production_requirements"][
                    "accepted_width"
                ].__setitem__("minimum", 1019),
                "D01 production contract mismatch",
            ),
            (
                "policy",
                lambda data: data["candidate_policy"].__setitem__(
                    "cross_candidate_references", "allowed"
                ),
                "D01 candidate policy mismatch",
            ),
            (
                "candidate order",
                lambda data: data["candidates"].reverse(),
                "D01 candidate contract mismatch",
            ),
            (
                "candidate path",
                lambda data: data["candidates"][0].__setitem__(
                    "target_path", "source/candidates/d01/r01/substitute.png"
                ),
                "D01 candidate contract mismatch",
            ),
            (
                "gates",
                lambda data: data.__setitem__(
                    "acceptance_gates", ["identity", "body"]
                ),
                "D01 acceptance gates mismatch",
            ),
            (
                "hard rejects",
                lambda data: data["hard_rejects"].pop(),
                "D01 exact hard rejects required",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name):
                invalid = copy.deepcopy(self.d01)
                mutate(invalid)
                with self.assertRaisesRegex(ValidationError, message):
                    validate_generation_request(invalid)

    def test_c06_live_request_is_valid_in_its_committed_repair_mode(self):
        validate_generation_request(self.c06)

    def test_c06_inactive_contract_declares_exact_families_and_review_sets(self):
        validate_generation_request(self.c06_inactive)
        self.assertEqual(
            [
                candidate["variant"]
                for candidate in self.c06_inactive["candidates"]
            ],
            ["a", "b"],
        )
        self.assertEqual(
            self.c06_inactive["repair_lane"], {"mode": "inactive"}
        )
        self.assertEqual(
            [item["candidate_id"] for item in self.c06_inactive["review_sets"]],
            ["c06-r01-a", "c06-r01-b"],
        )
        for candidate, review_set in zip(
            self.c06_inactive["candidates"],
            self.c06_inactive["review_sets"],
        ):
            self.assertEqual(
                [output["stage"] for output in candidate["outputs"]],
                [stage for stage, _ in C06_STAGE_PAIRS],
            )
            self.assertEqual(
                [output["descriptor"] for output in candidate["outputs"]],
                [descriptor for _, descriptor in C06_STAGE_PAIRS],
            )
            self.assertEqual(
                review_set["source_paths"],
                candidate_source_paths(candidate),
            )
        self.assertEqual(
            self.c06_inactive["acceptance_gates"],
            ["identity", "state", "rendering"],
        )

    def test_c06_targeted_stage_repair_is_one_literal_mixed_set(self):
        request = targeted_c06_request(
            self.c06_inactive, base="a", stage_index=2
        )
        validate_generation_request(request)
        repaired = request["review_sets"][-1]
        self.assertEqual(
            repaired["candidate_id"], "c06-r01-a-repair-c06-3"
        )
        self.assertEqual(
            [path.rsplit("-", 1)[-1] for path in repaired["source_paths"]],
            ["a.png", "a.png", "c.png", "a.png"],
        )

    def test_c06_full_family_repair_declares_complete_c(self):
        request = full_family_c06_request(self.c06_inactive)
        validate_generation_request(request)
        self.assertEqual(
            [candidate["variant"] for candidate in request["candidates"]],
            ["a", "b", "c"],
        )
        self.assertEqual(
            [item["candidate_id"] for item in request["review_sets"]],
            ["c06-r01-a", "c06-r01-b", "c06-r01-c"],
        )

    def test_c06_repair_modes_reject_undeclared_or_mixed_attempts(self):
        cases = {}

        inactive_with_c = copy.deepcopy(self.c06_inactive)
        inactive_with_c["candidates"].append(make_c06_family("c"))
        cases["inactive with C family"] = inactive_with_c

        targeted_plus_full = targeted_c06_request(
            self.c06_inactive, base="a", stage_index=2
        )
        targeted_plus_full["candidates"].append(make_c06_family("c"))
        cases["targeted plus full C"] = targeted_plus_full

        two_c_sources = targeted_c06_request(
            self.c06_inactive, base="a", stage_index=2
        )
        two_c_sources["review_sets"][-1]["source_paths"][1] = (
            c06_candidate_path(1, "c")
        )
        cases["two targeted C sources"] = two_c_sources

        partial_c = full_family_c06_request(self.c06_inactive)
        partial_c["candidates"][-1]["outputs"].pop()
        cases["partial C family"] = partial_c

        reordered_sets = copy.deepcopy(self.c06_inactive)
        reordered_sets["review_sets"].reverse()
        cases["reordered review sets"] = reordered_sets

        for name, invalid in cases.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ValidationError, "C06 .*contract|C06 .*repair"
                ):
                    validate_generation_request(invalid)

    def test_c06_rejects_changed_shared_or_stage_prompt(self):
        cases = {}
        changed_shared = copy.deepcopy(self.c06_inactive)
        changed_shared["shared_prompt"] += " Redesign the hair."
        cases["shared"] = changed_shared

        changed_stage = copy.deepcopy(self.c06_inactive)
        changed_stage["stages"][2]["prompt_delta"] += " Change the outfit."
        cases["stage"] = changed_stage

        for name, invalid in cases.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ValidationError, "C06 exact .* prompt contract"
                ):
                    validate_generation_request(invalid)

    def test_c06_scalar_stage_member_raises_validation_error(self):
        invalid = copy.deepcopy(self.c06_inactive)
        invalid["stages"][0] = "not-a-stage-mapping"

        with self.assertRaisesRegex(ValidationError, "C06 stage contract"):
            validate_generation_request(invalid)

    def test_c06_scalar_candidate_member_raises_validation_error(self):
        invalid = copy.deepcopy(self.c06_inactive)
        invalid["candidates"][0] = "not-a-candidate-mapping"

        with self.assertRaisesRegex(
            ValidationError, "C06 candidate family contract"
        ):
            validate_generation_request(invalid)

    def test_c07_request_has_exact_ordered_pair_contract(self):
        validate_generation_request(self.c07)
        self.assertEqual(self.c07["asset_id"], "C07")
        self.assertEqual(self.c07["revision"], "r01")
        self.assertEqual(
            self.c07["variation_axis"], "paired_generation_attempt"
        )
        self.assertEqual(
            [candidate["variant"] for candidate in self.c07["candidates"]],
            ["a", "b"],
        )
        for candidate in self.c07["candidates"]:
            self.assertEqual(
                [output["view"] for output in candidate["outputs"]],
                ["standing", "seated"],
            )
        self.assertEqual(self.c07["acceptance_gates"], ["body", "rendering"])

    def test_c07_framing_guidance_is_advisory(self):
        framing = self.c07["framing_guidance"]
        self.assertEqual(framing["canvas"], {"width": 1024, "height": 1536})
        self.assertEqual(framing["enforcement"], "advisory")
        self.assertEqual(
            framing["views"],
            {
                "standing": {
                    "upper_crop": "both-legs-visible-from-at-least-mid-thigh",
                    "intended_bottom_margin_pixels": [46, 150],
                    "intended_lateral_margin_pixels": 48,
                },
                "seated": {
                    "upper_crop": "pelvis-skirt-hem-and-both-thigh-roots-visible",
                    "intended_bottom_margin_pixels": [46, 150],
                    "intended_lateral_margin_pixels": 48,
                },
            },
        )
        self.assertFalse(framing["reject_on_numeric_miss_alone"])

    def test_c07_rejects_strict_pixel_enforcement(self):
        invalid = copy.deepcopy(self.c07)
        invalid["framing_guidance"]["enforcement"] = "hard"
        with self.assertRaisesRegex(
            ValidationError, "exact framing guidance required"
        ):
            validate_generation_request(invalid)

    def test_c07_rejects_reordered_references(self):
        invalid = copy.deepcopy(self.c07)
        invalid["references"].reverse()
        with self.assertRaisesRegex(
            ValidationError, "exact reference contract required"
        ):
            validate_generation_request(invalid)

    def test_c07_rejects_reordered_pair_outputs(self):
        invalid = copy.deepcopy(self.c07)
        invalid["candidates"][0]["outputs"].reverse()
        with self.assertRaisesRegex(
            ValidationError, "ordered paired outputs required"
        ):
            validate_generation_request(invalid)

    def test_c07_requires_same_candidate_standing_anchor_policy(self):
        invalid = copy.deepcopy(self.c07)
        invalid["pair_generation_policy"][
            "second_view_additional_reference"
        ]["source_view"] = "seated"
        with self.assertRaisesRegex(
            ValidationError, "pair generation policy mismatch"
        ):
            validate_generation_request(invalid)

    def test_c07_rejects_readding_unfinished_c_pair(self):
        invalid = copy.deepcopy(self.c07)
        candidate = copy.deepcopy(invalid["candidates"][-1])
        candidate["variant"] = "c"
        for output in candidate["outputs"]:
            output["target_path"] = output["target_path"].replace(
                "-b.png", "-c.png"
            )
        invalid["candidates"].append(candidate)
        with self.assertRaisesRegex(ValidationError, "expected candidates a, b"):
            validate_generation_request(invalid)

    def test_c04_request_has_exact_single_output_contract(self):
        validate_generation_request(self.c04)
        self.assertEqual(self.c04["asset_id"], "C04")
        self.assertEqual(self.c04["revision"], "r01")
        self.assertEqual(
            self.c04["variation_axis"], "independent_generation_attempt"
        )
        self.assertEqual(
            [candidate["variant"] for candidate in self.c04["candidates"]],
            ["a", "b", "c"],
        )

    def test_c04_framing_guidance_is_advisory_and_broad(self):
        framing = self.c04["framing_guidance"]
        self.assertEqual(framing["enforcement"], "advisory")
        self.assertEqual(framing["head_top_y"], [70, 160])
        self.assertEqual(framing["lowest_toe_y"], [1360, 1490])
        self.assertEqual(framing["intended_lateral_margin_pixels"], 48)
        self.assertFalse(framing["reject_on_numeric_miss_alone"])

    def test_c04_prompt_uses_positive_modest_coverage_language(self):
        prompt = self.c04["shared_prompt"]
        self.assertIn(
            "Keep all clothing fully opaque and arrange the skirt hem "
            "securely over the lap to the knees",
            prompt,
        )
        self.assertNotIn("exposed underwear", prompt)
        self.assertNotIn("sexualized pose", prompt)

    def test_c04_rejects_strict_pixel_enforcement(self):
        invalid = copy.deepcopy(self.c04)
        invalid["framing_guidance"]["enforcement"] = "hard"
        with self.assertRaisesRegex(
            ValidationError, "exact framing guidance required"
        ):
            validate_generation_request(invalid)

    def test_c04_rejects_reordered_references(self):
        invalid = copy.deepcopy(self.c04)
        invalid["references"][0], invalid["references"][1] = (
            invalid["references"][1],
            invalid["references"][0],
        )
        with self.assertRaisesRegex(
            ValidationError, "exact reference contract"
        ):
            validate_generation_request(invalid)

    def test_c04_rejects_noncanonical_candidate_path(self):
        invalid = copy.deepcopy(self.c04)
        invalid["candidates"][0]["target_path"] = "source/candidates/c04/a.png"
        with self.assertRaisesRegex(
            ValidationError, "candidate target path"
        ):
            validate_generation_request(invalid)

    def test_c05_request_has_exact_single_output_contract(self):
        validate_generation_request(self.c05)
        self.assertEqual(self.c05["asset_id"], "C05")
        self.assertEqual(self.c05["revision"], "r01")
        self.assertEqual(
            self.c05["variation_axis"], "independent_generation_attempt"
        )
        self.assertEqual(
            [candidate["variant"] for candidate in self.c05["candidates"]],
            ["a", "b", "c"],
        )
        self.assertEqual(
            [candidate["title"] for candidate in self.c05["candidates"]],
            [
                "independent-attempt-a",
                "independent-attempt-b",
                "independent-attempt-c",
            ],
        )
        self.assertEqual(
            [candidate["target_path"] for candidate in self.c05["candidates"]],
            [
                "source/candidates/c05/r01/"
                "akari-v1.2_c05_morning-bedhair_r01-a.png",
                "source/candidates/c05/r01/"
                "akari-v1.2_c05_morning-bedhair_r01-b.png",
                "source/candidates/c05/r01/"
                "akari-v1.2_c05_morning-bedhair_r01-c.png",
            ],
        )
        self.assertEqual(
            self.c05["acceptance_gates"],
            ["identity", "state", "rendering"],
        )

    def test_c05_uses_exact_ordered_reference_roles(self):
        self.assertEqual(
            [reference["role"] for reference in self.c05["references"]],
            [
                "accepted_c01_front_identity",
                "accepted_c03_hairpin_three_quarter",
                "supporting_sleepy_expression",
                "supporting_morning_hair",
            ],
        )

    def test_c05_framing_guidance_is_advisory(self):
        self.assertEqual(
            self.c05["framing_guidance"],
            {
                "canvas": {"width": 1024, "height": 1536},
                "enforcement": "advisory",
                "crop": "chest-up-below-hoodie-neckline-and-upper-chest",
                "intended_top_breathing_room_pixels": 70,
                "intended_lateral_hair_margin_pixels": 60,
                "face_placement": "vertical-upper-middle",
                "required_visible_features": [
                    "complete-crown-and-outer-hair-silhouette",
                    "complete-character-left-ornament",
                    "both-eyes-face-outline-cheek-strand-and-lower-bob-ends",
                    "shoulders-hoodie-neckline-and-upper-chest",
                ],
                "reject_on_numeric_miss_alone": False,
                "major_only_when": (
                    "crop-or-scale-prevents-complete-face-hair-state-review"
                ),
            },
        )

    def test_c05_rejects_strict_pixel_enforcement(self):
        invalid = copy.deepcopy(self.c05)
        invalid["framing_guidance"]["enforcement"] = "hard"
        with self.assertRaisesRegex(
            ValidationError, "exact framing guidance required"
        ):
            validate_generation_request(invalid)

    def test_c05_rejects_reordered_references(self):
        invalid = copy.deepcopy(self.c05)
        invalid["references"][2], invalid["references"][3] = (
            invalid["references"][3],
            invalid["references"][2],
        )
        with self.assertRaisesRegex(ValidationError, "exact reference contract"):
            validate_generation_request(invalid)

    def test_c05_rejects_per_candidate_state_delta(self):
        invalid = copy.deepcopy(self.c05)
        invalid["candidates"][0]["state_strength"] = "sleepier"
        with self.assertRaisesRegex(ValidationError, "candidate fields mismatch"):
            validate_generation_request(invalid)

    def test_c05_rejects_changed_hard_rejects(self):
        invalid = copy.deepcopy(self.c05)
        invalid["hard_rejects"].pop()
        with self.assertRaisesRegex(ValidationError, "exact hard rejects required"):
            validate_generation_request(invalid)

    def test_c01_and_c02_requests_have_exact_contracts(self):
        validate_generation_request(self.c01)
        validate_generation_request(self.c02)
        self.assertEqual(self.c02["asset_id"], "C02")
        self.assertEqual(self.c02["revision"], "r01")
        self.assertEqual(self.c02["variation_axis"], "generation_attempt")
        self.assertEqual(
            [candidate["variant"] for candidate in self.c02["candidates"]],
            ["a", "b", "c"],
        )

    def test_c03_request_manifest_exists(self):
        self.assertTrue(
            (
                PACKAGE_ROOT
                / "manifest/generation-requests/c03-r01.yaml"
            ).is_file()
        )

    def test_c03_r02_request_manifest_exists(self):
        self.assertTrue(
            (
                PACKAGE_ROOT
                / "manifest/generation-requests/c03-r02.yaml"
            ).is_file()
        )

    def test_c03_r02_has_exact_framing_contract(self):
        validate_generation_request(self.c03_r02)
        self.assertEqual(
            self.c03_r02["framing_contract"],
            {
                "canvas": {"width": 1024, "height": 1536},
                "measurement": {
                    "tool": "imagemagick",
                    "fuzz_percent": 6,
                    "geometry_format": "%@",
                    "head_top_formula": "y",
                    "sole_formula": "y_plus_height_minus_1",
                },
                "anchors": [
                    {
                        "asset_id": "C01",
                        "revision": "r01",
                        "head_top_y": 65,
                        "sole_y": 1450,
                    },
                    {
                        "asset_id": "C02",
                        "revision": "r01",
                        "head_top_y": 65,
                        "sole_y": 1463,
                    },
                ],
                "maximum_displacement": {
                    "percent_of_canvas_height": 2,
                    "integer_pixels": 30,
                },
                "required_intersection": {
                    "head_top_y": [35, 95],
                    "sole_y": [1433, 1480],
                },
                "prompt_target": {
                    "head_top_y": 65,
                    "sole_y": 1456,
                    "bottom_margin_pixels": 79,
                },
            },
        )

    def test_c03_r02_rejects_missing_changed_reordered_and_extra_framing_data(
        self,
    ):
        invalid_cases = []

        missing = copy.deepcopy(self.c03_r02)
        del missing["framing_contract"]["prompt_target"][
            "bottom_margin_pixels"
        ]
        invalid_cases.append(missing)

        changed = copy.deepcopy(self.c03_r02)
        changed["framing_contract"]["maximum_displacement"][
            "integer_pixels"
        ] = 31
        invalid_cases.append(changed)

        reordered = copy.deepcopy(self.c03_r02)
        framing = reordered["framing_contract"]
        reordered["framing_contract"] = {
            "measurement": framing["measurement"],
            "canvas": framing["canvas"],
            **{
                key: value
                for key, value in framing.items()
                if key not in {"canvas", "measurement"}
            },
        }
        invalid_cases.append(reordered)

        extra = copy.deepcopy(self.c03_r02)
        extra["framing_contract"]["prompt_target"]["tolerance"] = 1
        invalid_cases.append(extra)

        for invalid in invalid_cases:
            with self.subTest(contract=invalid["framing_contract"]):
                with self.assertRaisesRegex(ValidationError, "framing contract"):
                    validate_generation_request(invalid)

    def test_c03_r02_prompt_binds_standalone_target_coordinates(self):
        prompt = self.c03_r02["shared_prompt"]
        self.assertIn("head top at y=65", prompt)
        self.assertIn("soles at y=1456", prompt)
        self.assertIn("79 px bottom margin", prompt)
        self.assertIn("never reproduce the board", prompt)

    def test_c03_request_has_three_ordered_pairs(self):
        try:
            validate_generation_request(self.c03_r01)
        except ValidationError as error:
            self.fail(str(error))
        self.assertEqual(
            self.c03_r01["variation_axis"], "paired_generation_attempt"
        )
        self.assertEqual(
            [candidate["variant"] for candidate in self.c03_r01["candidates"]],
            ["a", "b", "c"],
        )
        for candidate in self.c03_r01["candidates"]:
            self.assertEqual(
                [output["view"] for output in candidate["outputs"]],
                ["hairpin-side-45", "non-hairpin-side-45"],
            )

    def test_generation_requests_use_ordered_comparison_anchor_lists(self):
        self.assertEqual(self.c01.get("comparison_anchors"), [])
        self.assertEqual(
            self.c02.get("comparison_anchors"),
            [
                "accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png"
            ],
        )
        self.assertEqual(len(self.c03_r01.get("comparison_anchors", [])), 2)

    def test_c03_rejects_reordered_outputs(self):
        invalid = copy.deepcopy(self.c03_r01)
        invalid["candidates"][0]["outputs"].reverse()
        with self.assertRaisesRegex(ValidationError, "ordered paired outputs"):
            validate_generation_request(invalid)

    def test_c03_rejects_noncanonical_paired_output_path(self):
        invalid = copy.deepcopy(self.c03_r01)
        invalid["candidates"][0]["outputs"][0]["target_path"] = (
            "source/candidates/c03/r01/arbitrary.png"
        )
        with self.assertRaisesRegex(ValidationError, "paired output path"):
            validate_generation_request(invalid)

    def test_c03_rejects_reordered_comparison_anchors(self):
        invalid = copy.deepcopy(self.c03_r01)
        invalid["comparison_anchors"].reverse()
        with self.assertRaisesRegex(ValidationError, "comparison anchors"):
            validate_generation_request(invalid)

    def test_c03_rejects_substituted_anchor(self):
        invalid = copy.deepcopy(self.c03_r01)
        invalid["references"][1]["path"] = invalid["references"][0]["path"]
        with self.assertRaisesRegex(ValidationError, "exact reference contract"):
            validate_generation_request(invalid)

    def test_c03_requires_both_view_prompts(self):
        invalid = copy.deepcopy(self.c03_r01)
        invalid["view_prompts"]["non-hairpin-side-45"] = ""
        with self.assertRaisesRegex(ValidationError, "view prompts required"):
            validate_generation_request(invalid)

    def test_c03_rejects_changed_pair_generation_policy(self):
        invalid = copy.deepcopy(self.c03_r01)
        invalid["pair_generation_policy"]["second_view_additional_reference"][
            "priority"
        ] = "controlling"
        with self.assertRaisesRegex(ValidationError, "pair generation policy"):
            validate_generation_request(invalid)

    def test_c02_rejects_reordered_references(self):
        invalid = copy.deepcopy(self.c02)
        invalid["references"][0], invalid["references"][1] = (
            invalid["references"][1],
            invalid["references"][0],
        )
        with self.assertRaisesRegex(ValidationError, "exact reference contract"):
            validate_generation_request(invalid)

    def test_c02_rejects_legacy_reference(self):
        invalid = copy.deepcopy(self.c02)
        invalid["references"][1]["path"] = (
            "akari-v1.2/references/legacy/back.webp"
        )
        with self.assertRaisesRegex(ValidationError, "exact reference contract"):
            validate_generation_request(invalid)

    def test_c02_rejects_substituted_anchor(self):
        invalid = copy.deepcopy(self.c02)
        invalid["references"][0]["path"] = (
            "akari-v1.2/accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r99.png"
        )
        with self.assertRaisesRegex(ValidationError, "exact reference contract"):
            validate_generation_request(invalid)

    def test_c02_rejects_noncanonical_candidate_path(self):
        invalid = copy.deepcopy(self.c02)
        invalid["candidates"][0]["target_path"] = "source/candidates/c02/a.png"
        with self.assertRaisesRegex(ValidationError, "candidate target path"):
            validate_generation_request(invalid)

    def test_c02_prompt_binds_landmark_tolerances(self):
        prompt = self.c02["shared_prompt"]
        self.assertIn(
            "head-top and sole landmarks within 2% of the canvas height",
            prompt,
        )
        self.assertIn(
            "shoulder, visual-waist, and knee landmarks within 3% "
            "of the canvas height",
            prompt,
        )

    def test_c02_prompt_uses_accepted_c01_as_primary_rendering_anchor(self):
        prompt = self.c02["shared_prompt"]
        self.assertIn(
            "Treat accepted C01 as the primary rendering anchor and preserve "
            "its rendering treatment",
            prompt,
        )
        self.assertIn("v1.1 rear hair and outfit construction", prompt)

    def test_generation_request_rejects_extra_non_mapping_reference(self):
        for request in (self.c01, self.c02):
            with self.subTest(asset_id=request["asset_id"]):
                invalid = copy.deepcopy(request)
                invalid["references"].append("unexpected-reference")
                with self.assertRaisesRegex(
                    ValidationError, "exact reference contract"
                ):
                    validate_generation_request(invalid)

    def test_generation_request_rejects_legacy_reference(self):
        invalid = copy.deepcopy(self.c01)
        invalid["references"][0]["path"] = (
            "legacy/akari-v1.2-pre-natural-form/front.webp"
        )
        with self.assertRaisesRegex(ValidationError, "exact reference contract"):
            validate_generation_request(invalid)

    def test_generation_request_rejects_duplicate_reference(self):
        invalid = copy.deepcopy(self.c01)
        invalid["references"][1] = copy.deepcopy(invalid["references"][0])
        with self.assertRaisesRegex(ValidationError, "exact reference contract"):
            validate_generation_request(invalid)

    def test_generation_request_rejects_substituted_canonical_reference(self):
        invalid = copy.deepcopy(self.c01)
        invalid["references"][0]["path"] = (
            "akari-v1.2/references/v1.1/substitute-front.webp"
        )
        with self.assertRaisesRegex(ValidationError, "exact reference contract"):
            validate_generation_request(invalid)


class NaturalFormGenerationCollectionTests(ImmutableFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.assets = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        cls.requests = load_generation_requests(
            PACKAGE_ROOT / "manifest/generation-requests"
        )
        cls.freeze_fixtures("assets", "requests")

    def test_requests_load_in_asset_revision_order(self):
        self.assertEqual(
            [(item["asset_id"], item["revision"]) for item in self.requests],
            [
                ("C01", "r01"),
                ("C02", "r01"),
                ("C03", "r01"),
                ("C03", "r02"),
                ("C04", "r01"),
                ("C05", "r01"),
                ("C06", "r01"),
                ("C07", "r01"),
                ("D01", "r01"),
                ("D02", "r01"),
                ("D03", "r01"),
                ("D04", "r01"),
                ("D04", "r02"),
                ("D05", "r01"),
                ("D06", "r01"),
                ("D07", "r01"),
                ("D08", "r01"),
                ("D08", "r02"),
                ("D08", "r03"),
                ("D09", "r01"),
                ("D10", "r01"),
                ("D11", "r01"),
                ("D11", "r02"),
                ("D12", "r01"),
                ("D13", "r01"),
                ("D13", "r02"),
                ("D14", "r01"),
                ("D14", "r02"),
                ("D15", "r01"),
            ],
        )

    def test_generation_counts_distinguish_groups_from_outputs(self):
        c06 = next(
            item
            for item in self.requests
            if (item["asset_id"], item["revision"]) == ("C06", "r01")
        )
        expected_by_mode = {
            "inactive": (67, 81),
            "targeted-stage": (67, 82),
            "full-family": (68, 85),
        }
        self.assertEqual(
            count_generation_work(self.requests),
            expected_by_mode[c06["repair_lane"]["mode"]],
        )

    def test_non_c06_targeted_stage_metadata_does_not_change_counts(self):
        requests = copy.deepcopy(self.requests)
        c05 = next(item for item in requests if item["asset_id"] == "C05")
        c05["repair_lane"] = {"mode": "targeted-stage"}

        self.assertEqual(
            count_generation_work(requests),
            count_generation_work(self.requests),
        )

    def test_c06_repair_modes_have_exact_generation_counts(self):
        live_c06 = next(
            item
            for item in self.requests
            if (item["asset_id"], item["revision"]) == ("C06", "r01")
        )
        c06 = inactive_c06_request(live_c06)
        cases = (
            (targeted_c06_request(c06, base="a", stage_index=2), (67, 82)),
            (full_family_c06_request(c06), (68, 85)),
        )
        for replacement, expected in cases:
            requests = [
                replacement
                if (item["asset_id"], item["revision"]) == ("C06", "r01")
                else item
                for item in self.requests
            ]
            with self.subTest(mode=replacement["repair_lane"]["mode"]):
                self.assertEqual(count_generation_work(requests), expected)

    def test_c05_uses_assets_descriptor_and_records_accepted_r01(self):
        c05 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C05"
        )
        self.assertEqual(c05["descriptor"], "morning-bedhair")
        self.assertEqual(c05["status"], "accepted")
        self.assertEqual(c05["revision"], "r01")
        self.assertEqual(
            c05["accepted_paths"],
            [
                "accepted/core/face-hair/"
                "akari-v1.2_c05_morning-bedhair_r01.png"
            ],
        )

    def test_c02_requires_the_accepted_c01_anchor(self):
        validate_generation_dependencies(self.assets, self.requests)

    def test_c02_rejects_a_nonaccepted_c01_dependency(self):
        invalid = copy.deepcopy(self.assets)
        c01 = next(item for item in invalid["assets"] if item["asset_id"] == "C01")
        c01.update(status="candidate", revision="r00", accepted_paths=[])
        with self.assertRaisesRegex(ValidationError, "C02 requires accepted C01"):
            validate_generation_dependencies(invalid, self.requests)

    def test_c03_declares_both_accepted_standing_dependencies(self):
        c03 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C03"
        )
        self.assertEqual(c03["depends_on"], ["C01", "C02"])

    def test_c03_requires_accepted_c01_and_c02(self):
        invalid = copy.deepcopy(self.assets)
        c02 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C02"
        )
        c02.update(status="candidate", revision="r00", accepted_paths=[])
        with self.assertRaisesRegex(
            ValidationError, "C03 requires accepted C01 and C02"
        ):
            validate_generation_dependencies(invalid, self.requests)

    def test_dependency_validation_checks_both_c03_revisions(self):
        for revision in ("r01", "r02"):
            invalid = copy.deepcopy(self.requests)
            request = next(
                item
                for item in invalid
                if (item["asset_id"], item["revision"])
                == ("C03", revision)
            )
            request["references"][0]["path"] = (
                "akari-v1.2/accepted/core/standing/substituted-c01.png"
            )
            with self.subTest(revision=revision):
                with self.assertRaisesRegex(
                    ValidationError, "C03 requires accepted C01 and C02"
                ):
                    validate_generation_dependencies(self.assets, invalid)

    def test_c04_declares_all_standing_dependencies(self):
        c04 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C04"
        )
        self.assertEqual(c04["depends_on"], ["C01", "C02", "C03"])

    def test_c04_requires_accepted_c01_c02_and_c03(self):
        c04_requests = [
            item for item in self.requests if item["asset_id"] == "C04"
        ]
        for asset_id in ("C01", "C02", "C03"):
            with self.subTest(asset_id=asset_id):
                invalid = copy.deepcopy(self.assets)
                asset = next(
                    item
                    for item in invalid["assets"]
                    if item["asset_id"] == asset_id
                )
                asset.update(status="candidate", revision="r00", accepted_paths=[])
                with self.assertRaisesRegex(
                    ValidationError,
                    "C04 requires accepted C01 r01, C02 r01, and C03 r02",
                ):
                    validate_generation_dependencies(invalid, c04_requests)

    def test_c04_requires_exact_accepted_reference_paths(self):
        invalid = copy.deepcopy(self.requests)
        c04 = next(item for item in invalid if item["asset_id"] == "C04")
        c04["references"][1]["path"] = (
            "akari-v1.2/accepted/core/standing/substituted-c03.png"
        )
        with self.assertRaisesRegex(
            ValidationError,
            "C04 requires accepted C01 r01, C02 r01, and C03 r02",
        ):
            validate_generation_dependencies(self.assets, invalid)


class NaturalFormGenerationDependencyTests(ImmutableFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.assets = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        cls.requests = load_generation_requests(
            PACKAGE_ROOT / "manifest/generation-requests"
        )
        cls.freeze_fixtures("assets", "requests")

    def test_c05_declares_only_c01_dependency(self):
        c05 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C05"
        )
        self.assertEqual(c05["depends_on"], ["C01"])

    def test_c05_rejects_nonexact_dependency_list(self):
        invalid = copy.deepcopy(self.assets)
        c05 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C05"
        )
        c05["depends_on"] = ["C01", "C03"]
        c05_requests = [
            request for request in self.requests if request["asset_id"] == "C05"
        ]
        with self.assertRaisesRegex(
            ValidationError, "C05 requires accepted C01 r01"
        ):
            validate_generation_dependencies(invalid, c05_requests)

    def test_c05_requires_c01_accepted_status(self):
        invalid = copy.deepcopy(self.assets)
        c01 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C01"
        )
        c01["status"] = "accepted-with-notes"
        c05_requests = [
            request for request in self.requests if request["asset_id"] == "C05"
        ]
        with self.assertRaisesRegex(
            ValidationError, "C05 requires accepted C01 r01"
        ):
            validate_generation_dependencies(invalid, c05_requests)

    def test_c05_requires_c01_r01_revision(self):
        invalid = copy.deepcopy(self.assets)
        c01 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C01"
        )
        c01["revision"] = "r02"
        c05_requests = [
            request for request in self.requests if request["asset_id"] == "C05"
        ]
        with self.assertRaisesRegex(
            ValidationError, "C05 requires accepted C01 r01"
        ):
            validate_generation_dependencies(invalid, c05_requests)

    def test_c05_requires_exact_accepted_c01_path(self):
        c05_requests = [
            copy.deepcopy(request)
            for request in self.requests
            if request["asset_id"] == "C05"
        ]
        c05_requests[0]["references"][0]["path"] = (
            "akari-v1.2/accepted/core/standing/substituted-c01.png"
        )
        with self.assertRaisesRegex(
            ValidationError, "C05 requires accepted C01 r01"
        ):
            validate_generation_dependencies(self.assets, c05_requests)

    def test_c05_candidate_paths_use_assets_descriptor(self):
        invalid = copy.deepcopy(self.assets)
        c05 = next(
            item for item in invalid["assets"] if item["asset_id"] == "C05"
        )
        c05["descriptor"] = "substituted-morning-state"
        c05_requests = [
            request for request in self.requests if request["asset_id"] == "C05"
        ]
        with self.assertRaisesRegex(
            ValidationError, "C05 candidate paths must use assets descriptor"
        ):
            validate_generation_dependencies(invalid, c05_requests)

    def test_c06_declares_only_c05_dependency(self):
        c06 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C06"
        )
        self.assertEqual(c06["depends_on"], ["C05"])

    def test_c06_requires_strict_accepted_c05_r01_at_exact_edit_source(self):
        for mutation in ("status", "revision", "path", "dependency"):
            with self.subTest(mutation=mutation):
                assets = copy.deepcopy(self.assets)
                requests = copy.deepcopy(self.requests)
                c05 = next(
                    item for item in assets["assets"] if item["asset_id"] == "C05"
                )
                c06 = next(
                    item for item in requests if item["asset_id"] == "C06"
                )
                c06_asset = next(
                    item for item in assets["assets"] if item["asset_id"] == "C06"
                )
                if mutation == "status":
                    c05["status"] = "accepted-with-notes"
                elif mutation == "revision":
                    c05["revision"] = "r02"
                elif mutation == "path":
                    c06["references"][0]["path"] = (
                        "akari-v1.2/accepted/substitute.png"
                    )
                else:
                    c06_asset["depends_on"] = ["C01", "C05"]
                with self.assertRaisesRegex(
                    ValidationError, "C06 requires accepted C05 r01"
                ):
                    validate_generation_dependencies(assets, requests)

    def test_c07_declares_c01_and_c04_dependencies(self):
        c07 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C07"
        )
        self.assertEqual(c07["depends_on"], ["C01", "C04"])

    def test_c07_requires_accepted_c01_and_c04(self):
        c07_requests = [
            item for item in self.requests if item["asset_id"] == "C07"
        ]
        for asset_id in ("C01", "C04"):
            with self.subTest(asset_id=asset_id):
                invalid = copy.deepcopy(self.assets)
                asset = next(
                    item
                    for item in invalid["assets"]
                    if item["asset_id"] == asset_id
                )
                asset.update(status="candidate", revision="r00", accepted_paths=[])
                with self.assertRaisesRegex(
                    ValidationError,
                    "C07 requires accepted C01 r01 and C04 r01",
                ):
                    validate_generation_dependencies(invalid, c07_requests)

    def test_c07_requires_exact_accepted_reference_paths(self):
        c07_requests = [
            copy.deepcopy(item)
            for item in self.requests
            if item["asset_id"] == "C07"
        ]
        c07_requests[0]["references"][1]["path"] = (
            "akari-v1.2/accepted/core/sitting/substituted-c04.png"
        )
        with self.assertRaisesRegex(
            ValidationError,
            "C07 requires accepted C01 r01 and C04 r01",
        ):
            validate_generation_dependencies(self.assets, c07_requests)

    def test_live_d01_has_all_strict_accepted_core_dependencies(self):
        d01_requests = [
            copy.deepcopy(item)
            for item in self.requests
            if item["asset_id"] == "D01"
        ]

        validate_generation_dependencies(self.assets, d01_requests)

    def test_d01_requires_all_strict_accepted_core_dependencies(self):
        d01_requests = [
            copy.deepcopy(item)
            for item in self.requests
            if item["asset_id"] == "D01"
        ]
        for asset_id in ("C04", "C05", "C06", "C07"):
            with self.subTest(asset_id=asset_id):
                invalid = copy.deepcopy(self.assets)
                asset = next(
                    item
                    for item in invalid["assets"]
                    if item["asset_id"] == asset_id
                )
                asset.update(
                    status="candidate", revision="r00", accepted_paths=[]
                )
                with self.assertRaisesRegex(
                    ValidationError,
                    "D01 requires strict accepted C04 r01, C05 r01, "
                    "C06 r01 C06-2, and C07 r01 seated",
                ):
                    validate_generation_dependencies(invalid, d01_requests)

    def test_d01_requires_each_dependency_revision_r01(self):
        d01_requests = [
            copy.deepcopy(item)
            for item in self.requests
            if item["asset_id"] == "D01"
        ]
        for asset_id in ("C04", "C05", "C06", "C07"):
            with self.subTest(asset_id=asset_id):
                invalid = copy.deepcopy(self.assets)
                asset = next(
                    item
                    for item in invalid["assets"]
                    if item["asset_id"] == asset_id
                )
                asset["revision"] = "r00"
                with self.assertRaisesRegex(
                    ValidationError,
                    "D01 requires strict accepted C04 r01, C05 r01, "
                    "C06 r01 C06-2, and C07 r01 seated",
                ):
                    validate_generation_dependencies(invalid, d01_requests)

    def test_d01_requires_exact_accepted_core_reference_paths(self):
        expected_paths = (
            "akari-v1.2/accepted/core/sitting/"
            "akari-v1.2_c04_floor-sitting_r01.png",
            "akari-v1.2/accepted/core/face-hair/"
            "akari-v1.2_c05_morning-bedhair_r01.png",
            "akari-v1.2/accepted/core/face-hair/"
            "akari-v1.2_c06-2_sleepy-secure_r01.png",
            "akari-v1.2/accepted/core/indoor-feet/"
            "akari-v1.2_c07_indoor-socks-seated_r01.png",
        )
        for index, expected_path in enumerate(expected_paths):
            with self.subTest(index=index, expected_path=expected_path):
                requests = [
                    copy.deepcopy(item)
                    for item in self.requests
                    if item["asset_id"] == "D01"
                ]
                requests[0]["references"][index]["path"] = (
                    f"{expected_path}.substituted"
                )
                with self.assertRaisesRegex(
                    ValidationError,
                    "D01 requires strict accepted C04 r01, C05 r01, "
                    "C06 r01 C06-2, and C07 r01 seated",
                ):
                    validate_generation_dependencies(self.assets, requests)

    def test_d01_requires_exact_c06_2_and_c07_seated_paths(self):
        replacements = {
            2: (
                "akari-v1.2/accepted/core/face-hair/"
                "akari-v1.2_c06-1_sleepy-neutral_r01.png"
            ),
            3: (
                "akari-v1.2/accepted/core/indoor-feet/"
                "akari-v1.2_c07_indoor-socks-standing_r01.png"
            ),
        }
        for index, path in replacements.items():
            with self.subTest(index=index):
                requests = [
                    copy.deepcopy(item)
                    for item in self.requests
                    if item["asset_id"] == "D01"
                ]
                requests[0]["references"][index]["path"] = path
                with self.assertRaisesRegex(
                    ValidationError,
                    "D01 requires strict accepted C04 r01, C05 r01, "
                    "C06 r01 C06-2, and C07 r01 seated",
                ):
                    validate_generation_dependencies(self.assets, requests)


def d01_review(status="review", findings=None, candidate_id="d01-r01-a"):
    variant = candidate_id[-1]
    return {
        "asset_id": "D01",
        "revision": "r01",
        "candidate_id": candidate_id,
        "status": status,
        "source_paths": [
            "source/candidates/d01/r01/"
            f"akari-v1.2_d01_morning-bedside_r01-{variant}.png"
        ],
        "source_sha256s": [f"{1 if variant == 'a' else 2:064x}"],
        "findings": [] if findings is None else findings,
        "decision": f"Synthetic D01 {candidate_id} decision.",
    }


def d01_finding(
    severity="minor", controller="D01-scene", resolved=False
):
    return {
        "severity": severity,
        "category": "production",
        "note": "Synthetic original-resolution evidence.",
        "resolved": resolved,
        "controlling_source_asset": controller,
        "recommended_next_action": "Preserve or regenerate the scene.",
    }


def accepted_d01_assets(assets: dict, status="accepted") -> dict:
    updated = copy.deepcopy(assets)
    d01 = next(item for item in updated["assets"] if item["asset_id"] == "D01")
    d01.update(
        status=status,
        revision="r01",
        accepted_paths=[
            "accepted/daily-validation/"
            "akari-v1.2_d01_morning-bedside_r01.png"
        ],
    )
    return updated


class NaturalFormReviewLogTests(ImmutableFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.review_log = load_yaml(PACKAGE_ROOT / "manifest/review-log.yaml")
        cls.freeze_fixtures("review_log")

    def test_d01_findings_require_controller_and_next_action(self):
        for missing in ("controlling_source_asset", "recommended_next_action"):
            with self.subTest(missing=missing):
                log = copy.deepcopy(self.review_log)
                finding = d01_finding()
                finding.pop(missing)
                log["reviews"].append(d01_review(findings=[finding]))
                with self.assertRaisesRegex(
                    ValidationError, "D01: exact finding provenance required"
                ):
                    validate_review_log(log)

    def test_d01_findings_reject_extra_fields_and_unknown_controller(self):
        cases = []
        extra = d01_finding()
        extra["evidence"] = "undeclared"
        cases.append(extra)
        cases.append(d01_finding(controller="C03"))
        for finding in cases:
            with self.subTest(finding=finding):
                log = copy.deepcopy(self.review_log)
                log["reviews"].append(d01_review(findings=[finding]))
                with self.assertRaisesRegex(
                    ValidationError, "D01: exact finding provenance required"
                ):
                    validate_review_log(log)

    def test_d01_accepted_rejects_every_unresolved_finding(self):
        log = copy.deepcopy(self.review_log)
        log["reviews"].append(
            d01_review(status="accepted", findings=[d01_finding()])
        )
        with self.assertRaisesRegex(
            ValidationError, "D01: accepted requires no unresolved finding"
        ):
            validate_review_log(log)

    def test_d01_accepted_with_notes_allows_only_scene_minor(self):
        allowed = copy.deepcopy(self.review_log)
        allowed["reviews"].append(
            d01_review(status="accepted-with-notes", findings=[d01_finding()])
        )
        validate_review_log(allowed)
        cases = (
            ("major", "D01-scene", False),
            ("minor", "C04", False),
            ("minor", "D01-scene", True),
        )
        for severity, controller, resolved in cases:
            with self.subTest(
                severity=severity, controller=controller, resolved=resolved
            ):
                invalid = copy.deepcopy(self.review_log)
                invalid["reviews"].append(
                    d01_review(
                        status="accepted-with-notes",
                        findings=[d01_finding(severity, controller, resolved)],
                    )
                )
                with self.assertRaisesRegex(
                    ValidationError,
                    "D01: accepted-with-notes requires D01-scene Minor only",
                ):
                    validate_review_log(invalid)


def accepted_c01_assets(assets: dict) -> dict:
    updated = copy.deepcopy(assets)
    c01 = updated["assets"][0]
    c01["status"] = "accepted"
    c01["revision"] = "r01"
    c01["accepted_paths"] = [
        "accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png"
    ]
    return updated


def accepted_c03_lifecycle(
    assets: dict, generation_requests: list[dict], review_log: dict
) -> tuple[dict, dict]:
    updated_assets = copy.deepcopy(assets)
    c03 = next(
        item for item in updated_assets["assets"] if item["asset_id"] == "C03"
    )
    c03.update(
        status="accepted",
        revision="r02",
        accepted_paths=[
            "accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png",
            "accepted/core/standing/"
            "akari-v1.2_c03_non-hairpin-side-45_r02.png",
        ],
    )
    c03_request = next(
        request
        for request in generation_requests
        if (request["asset_id"], request["revision"]) == ("C03", "r02")
    )
    updated_reviews = copy.deepcopy(review_log)
    updated_reviews["reviews"] = [
        review
        for review in updated_reviews["reviews"]
        if (review["asset_id"], review["revision"]) != ("C03", "r02")
    ]
    for index, candidate in enumerate(c03_request["candidates"]):
        updated_reviews["reviews"].append(
            {
                "asset_id": "C03",
                "revision": "r02",
                "candidate_id": f"c03-r02-{candidate['variant']}",
                "status": "accepted" if candidate["variant"] == "b" else "rejected",
                "source_paths": candidate_source_paths(candidate),
                "source_sha256s": [f"{index + 1:064x}"] * 2,
                "findings": [],
                "decision": f"Synthetic paired decision {candidate['variant']}.",
            }
        )
    return updated_assets, updated_reviews


def accepted_c06_lifecycle(
    assets: dict,
    generation_requests: list[dict],
    review_log: dict,
    request: dict,
    accepted_id: str,
):
    updated_assets = copy.deepcopy(assets)
    c06 = next(
        item for item in updated_assets["assets"] if item["asset_id"] == "C06"
    )
    c06.update(
        status="accepted",
        revision="r01",
        accepted_paths=[
            path.replace("rNN", "r01") for path in c06["expected_paths"]
        ],
    )
    updated_requests = [
        copy.deepcopy(request)
        if (item["asset_id"], item["revision"]) == ("C06", "r01")
        else copy.deepcopy(item)
        for item in generation_requests
    ]
    updated_reviews = copy.deepcopy(review_log)
    updated_reviews["reviews"] = [
        review
        for review in updated_reviews["reviews"]
        if (review["asset_id"], review["revision"]) != ("C06", "r01")
    ]
    for index, review_set in enumerate(request["review_sets"], start=1):
        updated_reviews["reviews"].append(
            {
                "asset_id": "C06",
                "revision": "r01",
                "candidate_id": review_set["candidate_id"],
                "status": (
                    "accepted"
                    if review_set["candidate_id"] == accepted_id
                    else "rejected"
                ),
                "source_paths": copy.deepcopy(review_set["source_paths"]),
                "source_sha256s": [f"{index:064x}"] * 4,
                "findings": [],
                "decision": f"Synthetic C06 set decision {index}.",
            }
        )
    return updated_assets, updated_requests, updated_reviews


class NaturalFormLifecycleTests(ImmutableFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.assets = load_yaml(PACKAGE_ROOT / "manifest/assets.yaml")
        cls.generation_requests = load_generation_requests(
            PACKAGE_ROOT / "manifest/generation-requests"
        )
        cls.review_log = load_yaml(PACKAGE_ROOT / "manifest/review-log.yaml")
        cls.c06 = next(
            item
            for item in cls.generation_requests
            if (item["asset_id"], item["revision"]) == ("C06", "r01")
        )
        cls.c06_inactive = inactive_c06_request(cls.c06)
        cls.freeze_fixtures(
            "assets",
            "generation_requests",
            "review_log",
            "c06",
            "c06_inactive",
        )

    def test_d01_acceptance_links_selected_source_and_gate4(self):
        expected_selected_id = "d01-r01-a"
        d01 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "D01"
        )
        self.assertIn(d01["status"], {"accepted", "accepted-with-notes"})
        self.assertEqual(d01["revision"], "r01")
        self.assertEqual(
            d01["accepted_paths"],
            [
                "accepted/daily-validation/"
                "akari-v1.2_d01_morning-bedside_r01.png"
            ],
        )
        request = next(
            item for item in self.generation_requests
            if (item["asset_id"], item["revision"]) == ("D01", "r01")
        )
        reviews = [
            item for item in self.review_log["reviews"]
            if (item["asset_id"], item["revision"]) == ("D01", "r01")
        ]
        self.assertEqual(
            [item["candidate_id"] for item in reviews],
            [f"d01-r01-{item['variant']}" for item in request["candidates"]],
        )
        selected = [
            item for item in reviews
            if item["status"] in {"accepted", "accepted-with-notes"}
        ]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["candidate_id"], expected_selected_id)
        self.assertEqual(selected[0]["status"], d01["status"])
        self.assertEqual(
            selected[0]["source_sha256s"],
            [sha256_file(PACKAGE_ROOT / d01["accepted_paths"][0])],
        )
        self.assertEqual(
            self.review_log["gate_4"]["selected_candidate_id"],
            expected_selected_id,
        )
        self.assertEqual(
            self.review_log["gate_4"]["outcome"],
            "release" if d01["status"] == "accepted" else "conditional-release",
        )

    def test_d01_acceptance_rejects_existing_selected_source_hash_mismatch(self):
        request = next(
            item
            for item in self.generation_requests
            if (item["asset_id"], item["revision"]) == ("D01", "r01")
        )
        selected_source = request["candidates"][0]["target_path"]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "accepted").symlink_to(PACKAGE_ROOT / "accepted")
            source = root / selected_source
            source.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "black").save(source)
            with self.assertRaisesRegex(
                ValidationError,
                "D01 r01: selected source file SHA-256 mismatch",
            ):
                validate_lifecycle_linkage(
                    self.assets,
                    self.generation_requests,
                    self.review_log,
                    root,
                )

    def test_d01_acceptance_allows_selected_source_absent_in_clean_clone(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "accepted").symlink_to(PACKAGE_ROOT / "accepted")
            validate_lifecycle_linkage(
                self.assets,
                self.generation_requests,
                self.review_log,
                root,
            )

    def test_superseded_daily_revision_allows_reviewed_sources_absent(self):
        assets = copy.deepcopy(self.assets)
        d13 = next(
            item for item in assets["assets"] if item["asset_id"] == "D13"
        )
        d13.update(status="candidate", revision="r00", accepted_paths=[])
        reviews = copy.deepcopy(self.review_log)
        reviews["reviews"] = [
            review
            for review in reviews["reviews"]
            if (review["asset_id"], review["revision"]) != ("D13", "r02")
        ]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "accepted").symlink_to(PACKAGE_ROOT / "accepted")
            validate_lifecycle_linkage(
                assets,
                self.generation_requests,
                reviews,
                root,
            )

    def pending_d01_inputs(self, reviews):
        assets = copy.deepcopy(self.assets)
        for asset in assets["assets"]:
            if asset["asset_id"] != "D01":
                asset.update(status="candidate", accepted_paths=[])
            else:
                asset.update(
                    status="candidate", revision="r00", accepted_paths=[]
                )
        return assets, {"reviews": reviews}

    def d01_only_requests(self):
        return [
            request
            for request in self.generation_requests
            if (request["asset_id"], request["revision"]) == ("D01", "r01")
        ]

    def pending_d01_assets(self):
        assets = copy.deepcopy(self.assets)
        d01 = next(
            item for item in assets["assets"] if item["asset_id"] == "D01"
        )
        d01.update(status="candidate", revision="r00", accepted_paths=[])
        return assets

    def review_log_without_d01(self):
        reviews = copy.deepcopy(self.review_log)
        reviews["reviews"] = [
            review
            for review in reviews["reviews"]
            if (review["asset_id"], review["revision"]) != ("D01", "r01")
        ]
        reviews.pop("gate_4", None)
        return reviews

    def write_d01_candidates(self, root, variants):
        request = next(
            item
            for item in self.generation_requests
            if (item["asset_id"], item["revision"]) == ("D01", "r01")
        )
        for candidate in request["candidates"]:
            if candidate["variant"] in variants:
                source = root / candidate["target_path"]
                source.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (1024, 1536), "white").save(source)

    def test_d01_generated_ab_allows_review_lag_before_selection(self):
        cases = ([], [d01_review()])
        for reviews in cases:
            with (
                self.subTest(review_count=len(reviews)),
                TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.write_d01_candidates(root, {"a", "b"})
                assets, log = self.pending_d01_inputs(reviews)
                validate_lifecycle_linkage(
                    assets,
                    self.d01_only_requests(),
                    log,
                    root,
                )

    def test_d01_generated_a_with_review_a_is_valid(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_d01_candidates(root, {"a"})
            assets, log = self.pending_d01_inputs([d01_review()])
            validate_lifecycle_linkage(
                assets,
                self.d01_only_requests(),
                log,
                root,
            )

    def test_d01_pending_review_requires_local_candidate_when_root_is_known(self):
        with TemporaryDirectory() as directory:
            assets, log = self.pending_d01_inputs([d01_review()])
            with self.assertRaisesRegex(
                ValidationError,
                "D01 r01: generated candidates require ordered reviews",
            ):
                validate_lifecycle_linkage(
                    assets,
                    self.d01_only_requests(),
                    log,
                    Path(directory),
                )

    def test_d01_generated_candidate_files_must_be_an_ordered_prefix(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_d01_candidates(root, {"b"})
            assets, log = self.pending_d01_inputs([d01_review()])
            with self.assertRaisesRegex(
                ValidationError,
                "D01 r01: generated candidates require ordered reviews",
            ):
                validate_lifecycle_linkage(
                    assets,
                    self.d01_only_requests(),
                    log,
                    root,
                )

    def test_d01_pre_acceptance_allows_only_an_ordered_prefix(self):
        reviews = self.review_log_without_d01()
        reviews["reviews"].append(d01_review())
        pending_assets = self.pending_d01_assets()
        validate_lifecycle_linkage(
            pending_assets, self.generation_requests, reviews
        )
        invalid = self.review_log_without_d01()
        invalid["reviews"].append(d01_review(candidate_id="d01-r01-b"))
        with self.assertRaisesRegex(
            ValidationError, "reviews must match declared D01 candidates in order"
        ):
            validate_lifecycle_linkage(
                pending_assets, self.generation_requests, invalid
            )

    def test_d01_acceptance_requires_full_declared_list_and_one_match(self):
        assets = accepted_d01_assets(self.assets)
        reviews = self.review_log_without_d01()
        reviews["reviews"].extend(
            [
                d01_review(status="accepted"),
                d01_review(status="rejected", candidate_id="d01-r01-b"),
            ]
        )
        validate_lifecycle_linkage(assets, self.generation_requests, reviews)
        partial = copy.deepcopy(reviews)
        partial["reviews"].pop()
        with self.assertRaisesRegex(
            ValidationError, "reviews must match declared D01 candidates in order"
        ):
            validate_lifecycle_linkage(
                assets, self.generation_requests, partial
            )
        duplicated = copy.deepcopy(reviews)
        duplicated["reviews"][-1]["status"] = "accepted"
        with self.assertRaisesRegex(
            ValidationError, "expected exactly one accepted review"
        ):
            validate_lifecycle_linkage(
                assets, self.generation_requests, duplicated
            )

    def test_d01_optional_c_allows_only_rejected_scene_only_ab_prefix(self):
        request = next(
            copy.deepcopy(item)
            for item in self.generation_requests
            if (item["asset_id"], item["revision"]) == ("D01", "r01")
        )
        request["candidates"].append(
            {
                "variant": "c",
                "title": "independent-scene-c",
                "target_path": (
                    "source/candidates/d01/r01/"
                    "akari-v1.2_d01_morning-bedside_r01-c.png"
                ),
            }
        )
        requests = [
            request
            if (item["asset_id"], item["revision"]) == ("D01", "r01")
            else copy.deepcopy(item)
            for item in self.generation_requests
        ]
        reviews = self.review_log_without_d01()
        reviews["reviews"].extend(
            [
                d01_review(
                    status="rejected",
                    findings=[d01_finding()],
                    candidate_id=f"d01-r01-{variant}",
                )
                for variant in ("a", "b")
            ]
        )
        pending_assets = self.pending_d01_assets()
        validate_lifecycle_linkage(pending_assets, requests, reviews)
        invalid = copy.deepcopy(reviews)
        invalid["reviews"][-1]["findings"][0][
            "controlling_source_asset"
        ] = "C04"
        with self.assertRaisesRegex(
            ValidationError,
            "D01 r01: optional C requires rejected scene-only A/B",
        ):
            validate_lifecycle_linkage(pending_assets, requests, invalid)

    def test_d01_acceptance_requires_all_core_assets_strictly_accepted_r01(self):
        for asset_id in ("C04", "C05", "C06", "C07"):
            with self.subTest(asset_id=asset_id):
                assets = accepted_d01_assets(self.assets)
                core = next(
                    item for item in assets["assets"]
                    if item["asset_id"] == asset_id
                )
                core.update(
                    revision="r02",
                    accepted_paths=[
                        path.replace("r01", "r02")
                        for path in core["accepted_paths"]
                    ],
                )
                with self.assertRaisesRegex(
                    ValidationError,
                    "D01 acceptance requires strict accepted "
                    "C04 r01, C05 r01, C06 r01, and C07 r01",
                ):
                    validate_assets(assets)

    def test_d01_promoted_png_uses_the_same_dimension_gate(self):
        assets = accepted_d01_assets(self.assets)
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for item in assets["assets"]:
                for accepted_path in item["accepted_paths"]:
                    source = root / accepted_path
                    source.parent.mkdir(parents=True, exist_ok=True)
                    size = (
                        (1019, 1536)
                        if item["asset_id"] == "D01"
                        else (1024, 1536)
                    )
                    Image.new("RGB", size, "white").save(source)
            with self.assertRaisesRegex(
                ValidationError,
                "D01 r01: candidate dimensions outside "
                "1020-1028 x 1532-1540",
            ):
                validate_assets(assets, root)

    def test_gate4_outcome_matches_d01_status_and_selection(self):
        cases = (
            ("accepted", "release", "d01-r01-a"),
            ("accepted-with-notes", "conditional-release", "d01-r01-a"),
            ("candidate", "hold", None),
        )
        for status, outcome, selected in cases:
            with self.subTest(status=status):
                assets = copy.deepcopy(self.assets)
                d01 = next(
                    item for item in assets["assets"] if item["asset_id"] == "D01"
                )
                d01.update(
                    status=status,
                    revision="r01" if status != "candidate" else "r00",
                    accepted_paths=(
                        [
                            "accepted/daily-validation/"
                            "akari-v1.2_d01_morning-bedside_r01.png"
                        ]
                        if status != "candidate" else []
                    ),
                )
                log = self.review_log_without_d01()
                if selected is not None:
                    findings = (
                        [d01_finding()]
                        if status == "accepted-with-notes" else None
                    )
                    log["reviews"].append(
                        d01_review(status=status, findings=findings)
                    )
                log["gate_4"] = {
                    "asset_id": "D01",
                    "revision": "r01",
                    "outcome": outcome,
                    "selected_candidate_id": selected,
                    "controlling_source_asset": "D01-scene",
                    "decision": "Synthetic Gate 4 decision.",
                }
                validate_gate4(assets, log)

    def test_gate4_is_required_for_accepted_d01_and_rejects_wrong_selection(self):
        assets = accepted_d01_assets(self.assets)
        log = self.review_log_without_d01()
        log["reviews"].append(d01_review(status="accepted"))
        with self.assertRaisesRegex(
            ValidationError, "Gate 4 record required for accepted D01"
        ):
            validate_gate4(assets, log)
        log["gate_4"] = {
            "asset_id": "D01",
            "revision": "r01",
            "outcome": "release",
            "selected_candidate_id": "d01-r01-b",
            "controlling_source_asset": "D01-scene",
            "decision": "Synthetic Gate 4 decision.",
        }
        with self.assertRaisesRegex(
            ValidationError, "Gate 4 selection does not match D01 review"
        ):
            validate_gate4(assets, log)

    def test_lifecycle_linkage_accepts_current_c01_decisions(self):
        validate_lifecycle_linkage(
            self.assets, self.generation_requests, self.review_log
        )

    def test_c06_lifecycle_accepts_initial_review_sets(self):
        assets, requests, reviews = accepted_c06_lifecycle(
            self.assets,
            self.generation_requests,
            self.review_log,
            self.c06_inactive,
            "c06-r01-a",
        )
        validate_review_log(reviews)
        validate_lifecycle_linkage(assets, requests, reviews)

    def test_c06_targeted_repair_matches_review_sets_not_candidates(self):
        request = targeted_c06_request(
            self.c06_inactive, base="a", stage_index=2
        )
        assets, requests, reviews = accepted_c06_lifecycle(
            self.assets,
            self.generation_requests,
            self.review_log,
            request,
            "c06-r01-a-repair-c06-3",
        )
        validate_review_log(reviews)
        validate_lifecycle_linkage(assets, requests, reviews)

    def test_c06_lifecycle_accepts_complete_c_family(self):
        request = full_family_c06_request(self.c06_inactive)
        assets, requests, reviews = accepted_c06_lifecycle(
            self.assets,
            self.generation_requests,
            self.review_log,
            request,
            "c06-r01-c",
        )
        validate_review_log(reviews)
        validate_lifecycle_linkage(assets, requests, reviews)

    def test_c06_lifecycle_rejects_changed_review_sets(self):
        cases = {}
        request = targeted_c06_request(
            self.c06_inactive, base="a", stage_index=2
        )
        assets, requests, reviews = accepted_c06_lifecycle(
            self.assets,
            self.generation_requests,
            self.review_log,
            request,
            "c06-r01-a-repair-c06-3",
        )

        missing = copy.deepcopy(reviews)
        missing["reviews"] = [
            item
            for item in missing["reviews"]
            if item["candidate_id"] != "c06-r01-b"
        ]
        cases["missing"] = missing

        reordered = copy.deepcopy(reviews)
        c06_reviews = [
            index
            for index, item in enumerate(reordered["reviews"])
            if item["asset_id"] == "C06"
        ]
        left, right = c06_reviews[0], c06_reviews[1]
        reordered["reviews"][left], reordered["reviews"][right] = (
            reordered["reviews"][right],
            reordered["reviews"][left],
        )
        cases["reordered"] = reordered

        replaced = copy.deepcopy(reviews)
        selected = next(
            item
            for item in replaced["reviews"]
            if item["candidate_id"] == "c06-r01-a-repair-c06-3"
        )
        selected["source_paths"][2] = c06_candidate_path(2, "b")
        cases["replaced path"] = replaced

        for name, invalid in cases.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ValidationError,
                    "reviews must match declared C06 review sets in order",
                ):
                    validate_lifecycle_linkage(assets, requests, invalid)

    def test_c06_acceptance_links_four_files_to_one_declared_review_set(self):
        c06 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C06"
        )
        self.assertEqual(c06["status"], "accepted")
        self.assertEqual(c06["revision"], "r01")
        self.assertEqual(
            c06["accepted_paths"],
            [
                "accepted/core/face-hair/"
                "akari-v1.2_c06-1_sleepy-neutral_r01.png",
                "accepted/core/face-hair/"
                "akari-v1.2_c06-2_sleepy-secure_r01.png",
                "accepted/core/face-hair/"
                "akari-v1.2_c06-3_loosened-mouth_r01.png",
                "accepted/core/face-hair/"
                "akari-v1.2_c06-4_soft-smile_r01.png",
            ],
        )
        request = next(
            item for item in self.generation_requests
            if (item["asset_id"], item["revision"]) == ("C06", "r01")
        )
        reviews = [
            item for item in self.review_log["reviews"]
            if (item["asset_id"], item["revision"]) == ("C06", "r01")
        ]
        self.assertEqual(
            [item["candidate_id"] for item in reviews],
            [item["candidate_id"] for item in request["review_sets"]],
        )
        self.assertEqual(
            [item["source_paths"] for item in reviews],
            [item["source_paths"] for item in request["review_sets"]],
        )
        self.assertEqual(
            [item["status"] for item in reviews],
            ["accepted", "rejected"],
        )
        accepted = [item for item in reviews if item["status"] == "accepted"]
        self.assertEqual(len(accepted), 1)
        self.assertEqual(accepted[0]["candidate_id"], "c06-r01-a")
        self.assertEqual(len(accepted[0]["source_paths"]), 4)
        self.assertEqual(len(accepted[0]["source_sha256s"]), 4)
        self.assertEqual(
            accepted[0]["source_sha256s"],
            [
                "44608f8da382c44bce81c3031373e7045"
                "e3d6f5db5488c3d2d3474a99a542abd",
                "2ca9bb82bac9d3a2b7a2b887d5bb56af"
                "fe9e31d7b4fe2fd7e4297e69ae5d18ba",
                "4a1647426b73b1bd22380b88783a7bf51"
                "336be03d6638ea28e1b164113b98dfa",
                "7db1ea102a95d45d16e66a7390642d1c"
                "eb958ef631af072c40af87b2ee0b71d6",
            ],
        )
        self.assertTrue(
            all(
                item is accepted[0] or item["status"] == "rejected"
                for item in reviews
            )
        )
        self.assertFalse(
            any(
                finding["severity"] in {"blocker", "major"}
                and not finding["resolved"]
                for finding in accepted[0]["findings"]
            )
        )
        for accepted_path in c06["accepted_paths"]:
            with Image.open(PACKAGE_ROOT / accepted_path) as image:
                self.assertEqual(image.format, "PNG")
                self.assertEqual(image.size, (1024, 1536))
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.generation_requests,
            self.review_log,
            PACKAGE_ROOT,
        )

    def test_c07_acceptance_links_asset_review_and_declared_pair(self):
        c07 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C07"
        )
        self.assertEqual(c07["status"], "accepted")
        self.assertEqual(c07["revision"], "r01")
        self.assertEqual(
            c07["accepted_paths"],
            [
                "accepted/core/indoor-feet/"
                "akari-v1.2_c07_indoor-socks-standing_r01.png",
                "accepted/core/indoor-feet/"
                "akari-v1.2_c07_indoor-socks-seated_r01.png",
            ],
        )
        reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("C07", "r01")
        ]
        self.assertEqual(
            [review["candidate_id"] for review in reviews],
            ["c07-r01-a", "c07-r01-b"],
        )
        self.assertEqual(
            [review["status"] for review in reviews],
            ["accepted", "rejected"],
        )
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.generation_requests,
            self.review_log,
            PACKAGE_ROOT,
        )

    def test_rejected_c03_r01_review_batch_must_still_be_complete(self):
        invalid = copy.deepcopy(self.review_log)
        invalid["reviews"] = [
            review
            for review in invalid["reviews"]
            if review["candidate_id"] != "c03-r01-b"
        ]
        with self.assertRaisesRegex(
            ValidationError, "reviews must match declared"
        ):
            validate_lifecycle_linkage(
                self.assets,
                self.generation_requests,
                invalid,
            )

    def test_c03_r02_final_lifecycle_accepts_user_selected_a_pair(self):
        c03 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C03"
        )
        self.assertEqual(c03["status"], "accepted")
        self.assertEqual(c03["revision"], "r02")
        self.assertEqual(
            c03["accepted_paths"],
            [
                "accepted/core/standing/"
                "akari-v1.2_c03_hairpin-side-45_r02.png",
                "accepted/core/standing/"
                "akari-v1.2_c03_non-hairpin-side-45_r02.png",
            ],
        )
        reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("C03", "r02")
        ]
        self.assertEqual(
            [review["candidate_id"] for review in reviews],
            ["c03-r02-a", "c03-r02-b", "c03-r02-c"],
        )
        self.assertEqual(
            [review["status"] for review in reviews],
            ["accepted", "rejected", "rejected"],
        )
        self.assertEqual(
            reviews[0]["source_sha256s"],
            [
                "19c8c96113bcbc47f7d1e4cc1d58af466d3a573f0dae40cfcdf9bf456b1a0a9b",
                "9e60812e14ba0cb2223187a4764334986125e0781a8eaae2124da1d19bd92209",
            ],
        )
        self.assertTrue(
            any(
                finding["severity"] == "major"
                and finding["resolved"] is False
                for finding in reviews[2]["findings"]
            )
        )
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.generation_requests,
            self.review_log,
            PACKAGE_ROOT,
        )

    def test_lifecycle_rejects_corrupted_c03_r02_review_batches(self):
        cases = {}

        missing = copy.deepcopy(self.review_log)
        missing["reviews"] = [
            review
            for review in missing["reviews"]
            if review["candidate_id"] != "c03-r02-b"
        ]
        cases["missing"] = missing

        duplicated = copy.deepcopy(self.review_log)
        duplicate_b = copy.deepcopy(
            next(
                review
                for review in duplicated["reviews"]
                if review["candidate_id"] == "c03-r02-b"
            )
        )
        c_index = next(
            index
            for index, review in enumerate(duplicated["reviews"])
            if review["candidate_id"] == "c03-r02-c"
        )
        duplicated["reviews"][c_index] = duplicate_b
        cases["duplicated"] = duplicated

        reordered = copy.deepcopy(self.review_log)
        b_index = next(
            index
            for index, review in enumerate(reordered["reviews"])
            if review["candidate_id"] == "c03-r02-b"
        )
        c_index = next(
            index
            for index, review in enumerate(reordered["reviews"])
            if review["candidate_id"] == "c03-r02-c"
        )
        reordered["reviews"][b_index], reordered["reviews"][c_index] = (
            reordered["reviews"][c_index],
            reordered["reviews"][b_index],
        )
        cases["reordered"] = reordered

        replaced = copy.deepcopy(self.review_log)
        replaced_a = next(
            review
            for review in replaced["reviews"]
            if review["candidate_id"] == "c03-r02-a"
        )
        replaced_a["candidate_id"] = "c03-r02-arbitrary"
        cases["replaced"] = replaced

        mixed_source = copy.deepcopy(self.review_log)
        mixed_a = next(
            review
            for review in mixed_source["reviews"]
            if review["candidate_id"] == "c03-r02-a"
        )
        mixed_a["source_paths"][0] = (
            "source/candidates/c03/r01/"
            "akari-v1.2_c03_hairpin-side-45_r01-a.png"
        )
        cases["mixed source revision"] = mixed_source

        for name, reviews in cases.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ValidationError, "reviews must match declared"
                ):
                    validate_lifecycle_linkage(
                        self.assets,
                        self.generation_requests,
                        reviews,
                    )

    def test_lifecycle_rejects_c03_accepted_member_hash_mismatch(self):
        invalid = copy.deepcopy(self.review_log)
        accepted = next(
            review
            for review in invalid["reviews"]
            if (review["asset_id"], review["revision"]) == ("C03", "r02")
            and review["status"] == "accepted"
        )
        accepted["source_sha256s"][0] = "0" * 64
        with self.assertRaisesRegex(ValidationError, "accepted file SHA-256"):
            validate_lifecycle_linkage(
                self.assets,
                self.generation_requests,
                invalid,
                PACKAGE_ROOT,
            )

    def test_lifecycle_rejects_accepted_file_hash_mismatch(self):
        invalid = copy.deepcopy(self.review_log)
        accepted_c01 = next(
            review
            for review in invalid["reviews"]
            if review["asset_id"] == "C01" and review["status"] == "accepted"
        )
        accepted_c01["source_sha256s"] = ["0" * 64]
        with self.assertRaisesRegex(ValidationError, "accepted file SHA-256"):
            validate_lifecycle_linkage(
                self.assets,
                self.generation_requests,
                invalid,
                PACKAGE_ROOT,
            )

    def test_lifecycle_accepts_three_exact_c03_pair_reviews(self):
        assets, reviews = accepted_c03_lifecycle(
            self.assets, self.generation_requests, self.review_log
        )
        validate_review_log(reviews)
        try:
            validate_lifecycle_linkage(
                assets, self.generation_requests, reviews
            )
        except ValidationError as error:
            self.fail(str(error))

    def test_lifecycle_rejects_mixed_c03_pair_sources(self):
        assets, reviews = accepted_c03_lifecycle(
            self.assets, self.generation_requests, self.review_log
        )
        c03_b = next(
            review
            for review in reviews["reviews"]
            if review["candidate_id"] == "c03-r02-b"
        )
        c03_c = next(
            review
            for review in reviews["reviews"]
            if review["candidate_id"] == "c03-r02-c"
        )
        c03_b["source_paths"][1] = c03_c["source_paths"][1]
        with self.assertRaisesRegex(ValidationError, "declared C03 candidates"):
            validate_lifecycle_linkage(
                assets, self.generation_requests, reviews
            )

    def test_lifecycle_rejects_two_accepted_c03_pairs(self):
        assets, reviews = accepted_c03_lifecycle(
            self.assets, self.generation_requests, self.review_log
        )
        c03_a = next(
            review
            for review in reviews["reviews"]
            if review["candidate_id"] == "c03-r02-a"
        )
        c03_a["status"] = "accepted"
        with self.assertRaisesRegex(ValidationError, "exactly one accepted review"):
            validate_lifecycle_linkage(
                assets, self.generation_requests, reviews
            )

    def test_c02_acceptance_links_asset_review_and_declared_candidate(self):
        c02 = next(item for item in self.assets["assets"] if item["asset_id"] == "C02")
        self.assertEqual(c02["status"], "accepted")
        self.assertEqual(c02["revision"], "r01")
        self.assertEqual(
            c02["accepted_paths"],
            [
                "accepted/core/standing/"
                "akari-v1.2_c02_back-natural-stance_r01.png"
            ],
        )
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets, self.generation_requests, self.review_log
        )

    def test_c04_acceptance_links_asset_review_and_declared_candidate(self):
        c04 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C04"
        )
        self.assertEqual(c04["status"], "accepted")
        self.assertEqual(c04["revision"], "r01")
        self.assertEqual(
            c04["accepted_paths"],
            [
                "accepted/core/sitting/"
                "akari-v1.2_c04_floor-sitting_r01.png"
            ],
        )
        reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("C04", "r01")
        ]
        self.assertEqual(
            [review["candidate_id"] for review in reviews],
            ["c04-r01-a", "c04-r01-b", "c04-r01-c"],
        )
        accepted = [
            review for review in reviews if review["status"] == "accepted"
        ]
        self.assertEqual(len(accepted), 1)
        self.assertEqual(accepted[0]["candidate_id"], "c04-r01-c")
        self.assertEqual(
            accepted[0]["source_sha256s"],
            [
                "7289ca0d9cbc74b4f1becb949dcf174f"
                "dd691af08d19f185de47d7657c1d7c64"
            ],
        )
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.generation_requests,
            self.review_log,
            PACKAGE_ROOT,
        )

    def test_c05_acceptance_links_asset_review_and_declared_candidate(self):
        c05 = next(
            item for item in self.assets["assets"] if item["asset_id"] == "C05"
        )
        self.assertEqual(c05["status"], "accepted")
        self.assertEqual(c05["revision"], "r01")
        self.assertEqual(
            c05["accepted_paths"],
            [
                "accepted/core/face-hair/"
                "akari-v1.2_c05_morning-bedhair_r01.png"
            ],
        )
        reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("C05", "r01")
        ]
        self.assertEqual(
            [review["candidate_id"] for review in reviews],
            ["c05-r01-a", "c05-r01-b", "c05-r01-c"],
        )
        statuses = [review["status"] for review in reviews]
        self.assertEqual(statuses.count("accepted"), 1)
        self.assertEqual(statuses.count("rejected"), 2)
        self.assertNotIn("accepted-with-notes", statuses)
        accepted = next(
            review for review in reviews if review["status"] == "accepted"
        )
        self.assertEqual(accepted["candidate_id"], "c05-r01-b")
        self.assertEqual(
            accepted["source_sha256s"],
            [
                "4aae292203b389b7ab1f1a44171ec5cf"
                "45498843705d7dbefbc47f4452ac8ffa"
            ],
        )
        accepted_path = PACKAGE_ROOT / c05["accepted_paths"][0]
        with Image.open(accepted_path) as accepted_image:
            self.assertEqual(accepted_image.size, (1024, 1536))
        self.assertFalse(
            any(
                finding["severity"] in {"blocker", "major"}
                and not finding["resolved"]
                for finding in accepted["findings"]
            )
        )
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.generation_requests,
            self.review_log,
            PACKAGE_ROOT,
        )

    def test_lifecycle_rejects_c05_selected_review_status_mismatch(self):
        invalid = copy.deepcopy(self.review_log)
        selected = next(
            review
            for review in invalid["reviews"]
            if review["candidate_id"] == "c05-r01-b"
        )
        selected["status"] = "accepted-with-notes"
        with self.assertRaisesRegex(
            ValidationError, "accepted review status must match asset status"
        ):
            validate_lifecycle_linkage(
                self.assets,
                self.generation_requests,
                invalid,
            )

    def test_lifecycle_rejects_c05_nonselected_nonrejected_statuses(self):
        for candidate_id in ("c05-r01-a", "c05-r01-c"):
            for status in ("candidate", "review", "superseded"):
                with self.subTest(candidate_id=candidate_id, status=status):
                    invalid = copy.deepcopy(self.review_log)
                    nonselected = next(
                        review
                        for review in invalid["reviews"]
                        if review["candidate_id"] == candidate_id
                    )
                    nonselected["status"] = status
                    with self.assertRaisesRegex(
                        ValidationError,
                        "non-selected reviews must be rejected",
                    ):
                        validate_lifecycle_linkage(
                            self.assets,
                            self.generation_requests,
                            invalid,
                        )

    def test_lifecycle_linkage_rejects_empty_reviews_for_accepted_c01(self):
        invalid = copy.deepcopy(self.review_log)
        invalid["reviews"] = []
        with self.assertRaisesRegex(ValidationError, "exactly one accepted review"):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, invalid
            )

    def test_lifecycle_linkage_rejects_accepted_review_revision_mismatch(self):
        invalid = copy.deepcopy(self.review_log)
        invalid["reviews"][1]["revision"] = "r99"
        with self.assertRaisesRegex(
            ValidationError, "reviews require a matching generation request"
        ):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, invalid
            )

    def test_lifecycle_linkage_rejects_arbitrary_accepted_candidate(self):
        invalid = copy.deepcopy(self.review_log)
        invalid["reviews"][1]["candidate_id"] = "c01-r01-arbitrary"
        with self.assertRaisesRegex(ValidationError, "declared C01 candidate"):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, invalid
            )

    def test_lifecycle_linkage_rejects_arbitrary_accepted_source_path(self):
        invalid = copy.deepcopy(self.review_log)
        invalid["reviews"][1]["source_paths"] = [
            "source/candidates/c01/r01/arbitrary.png"
        ]
        with self.assertRaisesRegex(ValidationError, "declared C01 candidate"):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, invalid
            )

    def test_lifecycle_linkage_rejects_multiple_accepted_candidate_decisions(self):
        invalid = copy.deepcopy(self.review_log)
        invalid["reviews"][0]["status"] = "accepted-with-notes"
        with self.assertRaisesRegex(ValidationError, "exactly one accepted review"):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, invalid
            )

    def test_lifecycle_linkage_rejects_accepted_review_for_unaccepted_asset(self):
        invalid_assets = copy.deepcopy(self.assets)
        invalid_assets["assets"][0]["status"] = "candidate"
        invalid_assets["assets"][0]["revision"] = "r00"
        invalid_assets["assets"][0]["accepted_paths"] = []
        with self.assertRaisesRegex(ValidationError, "accepted asset"):
            validate_lifecycle_linkage(
                invalid_assets, self.generation_requests, self.review_log
            )

    def test_c02_accepted_review_must_match_declared_candidate(self):
        reviews = copy.deepcopy(self.review_log)
        accepted_c02 = next(
            review
            for review in reviews["reviews"]
            if review["asset_id"] == "C02" and review["status"] == "accepted"
        )
        accepted_c02["candidate_id"] = "c02-r01-arbitrary"
        accepted_c02["source_paths"] = [
            "source/candidates/c02/r01/arbitrary.png"
        ]
        with self.assertRaisesRegex(ValidationError, "declared C02 candidate"):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, reviews
            )

    def test_lifecycle_linkage_rejects_missing_rejected_c02_review(self):
        reviews = copy.deepcopy(self.review_log)
        reviews["reviews"] = [
            review
            for review in reviews["reviews"]
            if review["candidate_id"] != "c02-r01-b"
        ]
        with self.assertRaisesRegex(
            ValidationError, "declared C02 candidates in order"
        ):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, reviews
            )

    def test_lifecycle_linkage_rejects_reordered_c02_reviews(self):
        reviews = copy.deepcopy(self.review_log)
        c02_start = next(
            index
            for index, review in enumerate(reviews["reviews"])
            if review["asset_id"] == "C02"
        )
        reviews["reviews"][c02_start + 1], reviews["reviews"][c02_start + 2] = (
            reviews["reviews"][c02_start + 2],
            reviews["reviews"][c02_start + 1],
        )
        with self.assertRaisesRegex(
            ValidationError, "declared C02 candidates in order"
        ):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, reviews
            )

    def test_lifecycle_linkage_rejects_duplicated_declared_c02_review(self):
        reviews = copy.deepcopy(self.review_log)
        c02_b = next(
            review
            for review in reviews["reviews"]
            if review["candidate_id"] == "c02-r01-b"
        )
        c02_c_index = next(
            index
            for index, review in enumerate(reviews["reviews"])
            if review["candidate_id"] == "c02-r01-c"
        )
        reviews["reviews"][c02_c_index] = copy.deepcopy(c02_b)
        with self.assertRaisesRegex(
            ValidationError, "declared C02 candidates in order"
        ):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, reviews
            )

    def test_lifecycle_linkage_rejects_arbitrary_rejected_c02_candidate(self):
        reviews = copy.deepcopy(self.review_log)
        rejected_c02 = next(
            review
            for review in reviews["reviews"]
            if review["asset_id"] == "C02" and review["status"] == "rejected"
        )
        rejected_c02["candidate_id"] = "c02-r01-arbitrary"
        with self.assertRaisesRegex(
            ValidationError, "declared C02 candidates in order"
        ):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, reviews
            )

    def test_lifecycle_linkage_rejects_arbitrary_rejected_c02_source_path(self):
        reviews = copy.deepcopy(self.review_log)
        rejected_c02 = next(
            review
            for review in reviews["reviews"]
            if review["asset_id"] == "C02" and review["status"] == "rejected"
        )
        rejected_c02["source_paths"] = [
            "source/candidates/c02/r01/arbitrary.png"
        ]
        with self.assertRaisesRegex(
            ValidationError, "declared C02 candidates in order"
        ):
            validate_lifecycle_linkage(
                self.assets, self.generation_requests, reviews
            )

    def test_assets_accept_a_canonical_nonzero_revision(self):
        validate_assets(accepted_c01_assets(self.assets))

    def test_assets_reject_revision_path_mismatch(self):
        invalid = accepted_c01_assets(self.assets)
        invalid["assets"][0]["accepted_paths"] = [
            "accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r02.png"
        ]
        with self.assertRaisesRegex(ValidationError, "variants and revision"):
            validate_assets(invalid)

    def test_review_log_accepts_resolved_c01_decisions(self):
        data = copy.deepcopy(self.review_log)
        data["reviews"] = [
            {
                "asset_id": "C01",
                "revision": "r01",
                "candidate_id": "c01-r01-b",
                "status": "accepted",
                "source_paths": [
                    "source/candidates/c01/r01/"
                    "akari-v1.2_c01_front-natural-stance_r01-b.png"
                ],
                "source_sha256s": [
                    "a977f2798d15f3da9ef0d7720d6f9fc41bd2f84f54f4c8a6"
                    "9908a482596a75c5"
                ],
                "findings": [],
                "decision": "Selected after three-candidate posture review.",
            }
        ]
        validate_review_log(data)

    def test_accepted_review_rejects_unresolved_major(self):
        data = copy.deepcopy(self.review_log)
        data["reviews"] = [
            {
                "asset_id": "C01",
                "revision": "r01",
                "candidate_id": "c01-r01-b",
                "status": "accepted",
                "source_paths": [
                    "source/candidates/c01/r01/"
                    "akari-v1.2_c01_front-natural-stance_r01-b.png"
                ],
                "source_sha256s": [
                    "a977f2798d15f3da9ef0d7720d6f9fc41bd2f84f54f4c8a6"
                    "9908a482596a75c5"
                ],
                "findings": [
                    {
                        "severity": "major",
                        "category": "body",
                        "note": "Right ankle connection is unclear.",
                        "resolved": False,
                    }
                ],
                "decision": "Accepted incorrectly.",
            }
        ]
        with self.assertRaisesRegex(ValidationError, "unresolved major"):
            validate_review_log(data)


class NaturalFormInheritanceTests(ImmutableFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = load_yaml(PACKAGE_ROOT / "manifest/inheritance.yaml")
        cls.freeze_fixtures("data")

    def test_reference_snapshots_have_valid_provenance_and_hashes(self):
        validate_inheritance(self.data, ROOT, PACKAGE_ROOT)

    def test_c05_supporting_snapshots_have_exact_provenance_and_hashes(self):
        records = {record["role"]: record for record in self.data["references"]}
        expected = {
            "supporting_sleepy_expression": {
                "role": "supporting_sleepy_expression",
                "inheritance_class": "reference-only",
                "source_path": (
                    "source/generated/tonari-no-hyoujou/"
                    "20260705_sleepy-reply_v3.webp"
                ),
                "copied_path": (
                    "akari-v1.2/references/supporting/sleepy-reply-v3.webp"
                ),
                "source_collection": "tonari-no-hyoujou",
                "reuse_rationale": (
                    "C05 eyelid weight gaze energy and incomplete visual focus "
                    "only from a high-priority draft without identity rendering "
                    "or acceptance authority"
                ),
                "sha256": (
                    "a0b4dc00d8b32a0232c6579f3c28f792f49f5ede8f1d3527969c"
                    "367cc3a9d6b2"
                ),
            },
            "supporting_morning_hair": {
                "role": "supporting_morning_hair",
                "inheritance_class": "reference-only",
                "source_path": (
                    "source/finished/tonari-no-akari/"
                    "20260701_morning-glance_v1_finish_h05_v1.png"
                ),
                "copied_path": (
                    "akari-v1.2/references/supporting/morning-glance-h05.png"
                ),
                "source_collection": "tonari-no-akari",
                "reuse_rationale": (
                    "C05 crown flyaways cheek strand and lower-bob end "
                    "irregularity only without identity rendering or scene "
                    "authority"
                ),
                "sha256": (
                    "282379918dd6ff553305bf07e7d7aa47693fcd7edc19908ea94e1a"
                    "0c5771ba7b"
                ),
            },
        }
        for role, record in expected.items():
            with self.subTest(role=role):
                self.assertEqual(records.get(role), record)

    def test_c06_expression_grid_has_exact_provenance_and_hash(self):
        records = {record["role"]: record for record in self.data["references"]}
        self.assertEqual(
            records.get("v1.1-expression-range"),
            {
                "role": "v1.1-expression-range",
                "inheritance_class": "reference-only",
                "source_path": "source/originals/v1_1_front_3.webp",
                "copied_path": (
                    "akari-v1.2/references/v1.1/expression-grid.webp"
                ),
                "source_collection": "v1.1",
                "reuse_rationale": (
                    "C06 neutral relaxed-mouth and closed-mouth soft-smile "
                    "mechanics only; open-mouth laughing surprised worried "
                    "pouting yawning and closed-eye examples are excluded and "
                    "grant no identity crop rendering hair outfit or background "
                    "authority"
                ),
                "sha256": (
                    "2b70c639b320275cde6787263bd6fe0f88ad59068154e4c2439ae"
                    "69502e6f919"
                ),
            },
        )

    def test_c06_expression_grid_rejects_contract_mutations(self):
        mutations = {
            "role": "v1.1-expression-range-renamed",
            "source_collection": "v1.1-alternate",
            "reuse_rationale": "Different but still non-empty rationale.",
        }
        for field, alternative in mutations.items():
            with self.subTest(field=field):
                invalid = copy.deepcopy(self.data)
                record = next(
                    item
                    for item in invalid["references"]
                    if item["role"] == "v1.1-expression-range"
                )
                record[field] = alternative
                with self.assertRaisesRegex(
                    ValidationError,
                    "inheritance: C06 expression reference contract mismatch",
                ):
                    validate_inheritance(invalid, ROOT, PACKAGE_ROOT)

    def test_changed_hash_is_rejected(self):
        invalid = copy.deepcopy(self.data)
        invalid["references"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValidationError, "SHA-256 mismatch"):
            validate_inheritance(invalid, ROOT, PACKAGE_ROOT)

    def test_duplicate_controlling_role_is_rejected(self):
        invalid = copy.deepcopy(self.data)
        invalid["references"][1]["role"] = invalid["references"][0]["role"]
        with self.assertRaisesRegex(ValidationError, "duplicate role"):
            validate_inheritance(invalid, ROOT, PACKAGE_ROOT)

    def test_copied_paths_cannot_point_into_legacy(self):
        invalid = copy.deepcopy(self.data)
        invalid["references"][0]["copied_path"] = invalid["references"][0][
            "source_path"
        ]
        with self.assertRaisesRegex(ValidationError, "copied_path"):
            validate_inheritance(invalid, ROOT, PACKAGE_ROOT)


class NaturalFormIsolationTests(unittest.TestCase):
    def test_package_command_reserves_unqualified_v1_2_for_natural_form(self):
        package = json.loads((ROOT / "package.json").read_text())
        scripts = package["scripts"]
        self.assertEqual(
            scripts["validate:v1-2"],
            "uv run python scripts/validate_akari_v1_2_natural_form.py",
        )
        natural_form_commands = {
            "build:v1-2:c01-comparison": (
                "uv run python scripts/build_v1_2_c01_comparison.py"
            ),
            "build:v1-2:c02-comparison": (
                "uv run python scripts/build_v1_2_candidate_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/c02-r01.yaml "
                "--output akari-v1.2/comparisons/c02-r01/"
                "c02-r01-comparison.webp"
            ),
            "build:v1-2:c02-alignment-comparison": (
                "uv run python scripts/build_v1_2_candidate_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/c02-r01.yaml "
                "--output akari-v1.2/comparisons/c02-r01/"
                "c02-r01-alignment-comparison.webp "
                "--anchor accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png"
            ),
            "build:v1-2:c03-comparison": (
                "uv run python scripts/build_v1_2_c03_comparisons.py "
                "--request akari-v1.2/manifest/generation-requests/c03-r01.yaml "
                "--output akari-v1.2/comparisons/c03-r01/"
                "c03-r01-pair-comparison.webp"
            ),
            "build:v1-2:c03-alignment-comparison": (
                "uv run python scripts/build_v1_2_c03_comparisons.py "
                "--request akari-v1.2/manifest/generation-requests/c03-r01.yaml "
                "--output akari-v1.2/comparisons/c03-r01/"
                "c03-r01-alignment-comparison.webp --alignment"
            ),
            "audit:v1-2:c03-r02-landmarks": (
                "uv run python scripts/audit_v1_2_c03_landmarks.py "
                "--request akari-v1.2/manifest/generation-requests/c03-r02.yaml "
                "--package-root akari-v1.2"
            ),
            "build:v1-2:c03-r02-comparison": (
                "uv run python scripts/build_v1_2_c03_comparisons.py "
                "--request akari-v1.2/manifest/generation-requests/c03-r02.yaml "
                "--output akari-v1.2/comparisons/c03-r02/"
                "c03-r02-pair-comparison.webp"
            ),
            "build:v1-2:c03-r02-alignment-comparison": (
                "uv run python scripts/build_v1_2_c03_comparisons.py "
                "--request akari-v1.2/manifest/generation-requests/c03-r02.yaml "
                "--output akari-v1.2/comparisons/c03-r02/"
                "c03-r02-alignment-comparison.webp --alignment"
            ),
            "build:v1-2:c04-comparison": (
                "uv run python scripts/build_v1_2_candidate_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/c04-r01.yaml "
                "--output akari-v1.2/comparisons/c04-r01/"
                "c04-r01-comparison.webp"
            ),
            "build:v1-2:c05-comparison": (
                "uv run python scripts/build_v1_2_candidate_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/c05-r01.yaml "
                "--output akari-v1.2/comparisons/c05-r01/"
                "c05-r01-comparison.webp"
            ),
            "build:v1-2:c06-comparison": (
                "uv run python scripts/build_v1_2_c06_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/c06-r01.yaml "
                "--output akari-v1.2/comparisons/c06-r01/"
                "c06-r01-comparison.webp"
            ),
            "build:v1-2:c07-comparison": (
                "uv run python scripts/build_v1_2_paired_candidate_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/c07-r01.yaml "
                "--output akari-v1.2/comparisons/c07-r01/"
                "c07-r01-pair-comparison.webp"
            ),
            "build:v1-2:d01-comparison": (
                "uv run python scripts/build_v1_2_d01_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d01-r01.yaml "
                "--output akari-v1.2/comparisons/d01-r01/"
                "d01-r01-comparison.webp"
            ),
            "build:v1-2:d02-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d02-r01.yaml "
                "--output akari-v1.2/comparisons/d02-r01/"
                "d02-r01-comparison.webp --asset-id D02"
            ),
            "build:v1-2:d03-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d03-r01.yaml "
                "--output akari-v1.2/comparisons/d03-r01/"
                "d03-r01-comparison.webp --asset-id D03"
            ),
            "build:v1-2:d04-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d04-r01.yaml "
                "--output akari-v1.2/comparisons/d04-r01/"
                "d04-r01-comparison.webp --asset-id D04"
            ),
            "build:v1-2:d04-r02-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d04-r02.yaml "
                "--output akari-v1.2/comparisons/d04-r02/"
                "d04-r02-comparison.webp --asset-id D04"
            ),
            "build:v1-2:d05-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d05-r01.yaml "
                "--output akari-v1.2/comparisons/d05-r01/"
                "d05-r01-comparison.webp --asset-id D05"
            ),
            "build:v1-2:d06-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d06-r01.yaml "
                "--output akari-v1.2/comparisons/d06-r01/"
                "d06-r01-comparison.webp --asset-id D06"
            ),
            "build:v1-2:d07-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d07-r01.yaml "
                "--output akari-v1.2/comparisons/d07-r01/"
                "d07-r01-comparison.webp --asset-id D07"
            ),
            "build:v1-2:d08-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d08-r01.yaml "
                "--output akari-v1.2/comparisons/d08-r01/"
                "d08-r01-comparison.webp --asset-id D08"
            ),
            "build:v1-2:d08-r02-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d08-r02.yaml "
                "--output akari-v1.2/comparisons/d08-r02/"
                "d08-r02-comparison.webp --asset-id D08"
            ),
            "build:v1-2:d08-r03-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d08-r03.yaml "
                "--output akari-v1.2/comparisons/d08-r03/"
                "d08-r03-comparison.webp --asset-id D08"
            ),
            "build:v1-2:d09-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d09-r01.yaml "
                "--output akari-v1.2/comparisons/d09-r01/"
                "d09-r01-comparison.webp --asset-id D09"
            ),
            "build:v1-2:d10-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d10-r01.yaml "
                "--output akari-v1.2/comparisons/d10-r01/"
                "d10-r01-comparison.webp --asset-id D10"
            ),
            "build:v1-2:d11-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d11-r01.yaml "
                "--output akari-v1.2/comparisons/d11-r01/"
                "d11-r01-comparison.webp --asset-id D11"
            ),
            "build:v1-2:d11-r02-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d11-r02.yaml "
                "--output akari-v1.2/comparisons/d11-r02/"
                "d11-r02-comparison.webp --asset-id D11"
            ),
            "build:v1-2:d12-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d12-r01.yaml "
                "--output akari-v1.2/comparisons/d12-r01/"
                "d12-r01-comparison.webp --asset-id D12"
            ),
            "build:v1-2:d13-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d13-r01.yaml "
                "--output akari-v1.2/comparisons/d13-r01/"
                "d13-r01-comparison.webp --asset-id D13"
            ),
            "build:v1-2:d13-r02-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d13-r02.yaml "
                "--output akari-v1.2/comparisons/d13-r02/"
                "d13-r02-comparison.webp --asset-id D13"
            ),
            "build:v1-2:d14-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d14-r01.yaml "
                "--output akari-v1.2/comparisons/d14-r01/"
                "d14-r01-comparison.webp --asset-id D14"
            ),
            "build:v1-2:d14-r02-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d14-r02.yaml "
                "--output akari-v1.2/comparisons/d14-r02/"
                "d14-r02-comparison.webp --asset-id D14"
            ),
            "build:v1-2:d15-comparison": (
                "uv run python scripts/build_v1_2_daily_comparison.py "
                "--request akari-v1.2/manifest/generation-requests/d15-r01.yaml "
                "--output akari-v1.2/comparisons/d15-r01/"
                "d15-r01-comparison.webp --asset-id D15"
            ),
        }
        for name, command in natural_form_commands.items():
            self.assertEqual(scripts.get(name), command)
        old_unqualified = [
            name
            for name in scripts
            if name.startswith("build:v1-2") or name.startswith("promote:v1-2")
            if name not in natural_form_commands
            and name not in {"build:v1-2:previews", "build:v1-2:pdf"}
        ]
        self.assertEqual(old_unqualified, [])

    def test_runtime_contracts_do_not_point_directly_into_legacy(self):
        assets_text = (PACKAGE_ROOT / "manifest/assets.yaml").read_text()
        reviews_text = (PACKAGE_ROOT / "manifest/review-log.yaml").read_text()
        self.assertNotIn("legacy/akari-v1.2-pre-natural-form", assets_text)
        self.assertNotIn("legacy/akari-v1.2-pre-natural-form", reviews_text)

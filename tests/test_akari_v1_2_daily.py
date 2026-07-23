import copy
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

from PIL import Image
import yaml

from scripts.akari_v1_2_daily import (
    DAILY_REVIEW_POLICIES,
    ValidationError,
    daily_candidate_path,
    daily_review_policy,
    validate_daily_candidate_dimensions,
    validate_daily_generation_request,
)
from scripts.validate_akari_v1_2_natural_form import (
    validate_assets,
    validate_gate4,
    validate_generation_dependencies,
    validate_generation_request,
    validate_lifecycle_linkage,
    validate_review_log,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"


def daily_contract(request: dict) -> dict:
    return {
        "descriptor": "morning-bedside",
        "scene_contract": request["scene_contract"],
        "production_requirements": request["production_requirements"],
        "candidate_policy": request["candidate_policy"],
        "shared_prompt_sha256": hashlib.sha256(
            request["shared_prompt"].encode("utf-8")
        ).hexdigest(),
        "acceptance_gates": request["acceptance_gates"],
        "hard_rejects": request["hard_rejects"],
    }


def d02_review(variant: str, status: str = "review", findings=None) -> dict:
    source = (
        "source/candidates/d02/r01/"
        f"akari-v1.2_d02_morning-rug-daze_r01-{variant}.png"
    )
    return {
        "asset_id": "D02",
        "revision": "r01",
        "candidate_id": f"d02-r01-{variant}",
        "status": status,
        "source_paths": [source],
        "source_sha256s": ["0" * 64],
        "findings": [] if findings is None else findings,
        "decision": "Original-resolution ordered review recorded.",
    }


def d02_finding(controller: str = "D02-scene") -> dict:
    return {
        "severity": "major",
        "category": "continuity",
        "note": "The room no longer reads as the D01 morning bedroom.",
        "resolved": False,
        "controlling_source_asset": controller,
        "recommended_next_action": "Reject this scene attempt.",
    }


def d04_review(variant: str, controller: str) -> dict:
    category = "continuity" if controller == "D04-scene" else "identity"
    return {
        "asset_id": "D04",
        "revision": "r01",
        "candidate_id": f"d04-r01-{variant}",
        "status": "rejected",
        "source_paths": [
            "source/candidates/d04/r01/"
            f"akari-v1.2_d04_morning-drink-fetch_r01-{variant}.png"
        ],
        "source_sha256s": ["0" * 64],
        "findings": [
            {
                "severity": "major",
                "category": category,
                "note": "Candidate-local generated defect blocks selection.",
                "resolved": False,
                "controlling_source_asset": controller,
                "recommended_next_action": "Reject this candidate and use C.",
            }
        ],
        "decision": "Rejected after original-resolution review.",
    }


class DailyPrimitiveTests(unittest.TestCase):
    def test_daily_review_policies_preserve_d01_and_d02_rules(self):
        self.assertEqual(
            tuple(DAILY_REVIEW_POLICIES),
            (
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
            ),
        )
        self.assertEqual(
            daily_review_policy("D01").optional_c_finding_severities,
            frozenset({"blocker", "major", "minor"}),
        )
        self.assertEqual(
            daily_review_policy("D02").optional_c_finding_severities,
            frozenset({"blocker", "major"}),
        )
        self.assertEqual(
            daily_review_policy("D04").scene_controller,
            "D04-scene",
        )
        self.assertEqual(
            daily_review_policy("D05").scene_controller,
            "D05-scene",
        )
        self.assertTrue(
            daily_review_policy("D05").optional_c_allows_distinct_candidate_local
        )
        self.assertEqual(
            daily_review_policy("D06").scene_controller,
            "D06-scene",
        )
        self.assertTrue(
            daily_review_policy("D06").optional_c_allows_distinct_candidate_local
        )
        self.assertEqual(
            daily_review_policy("D07").scene_controller,
            "D07-scene",
        )
        self.assertEqual(
            daily_review_policy("D08").scene_controller,
            "D08-scene",
        )
        self.assertEqual(
            daily_review_policy("D11").scene_controller,
            "D11-scene",
        )
        self.assertEqual(
            daily_review_policy("D12").scene_controller,
            "D12-scene",
        )
        self.assertEqual(
            daily_review_policy("D13").scene_controller,
            "D13-scene",
        )
        self.assertEqual(
            daily_review_policy("D14").scene_controller,
            "D14-scene",
        )
        self.assertEqual(
            daily_review_policy("D15").scene_controller,
            "D15-scene",
        )

    def test_unknown_daily_review_policy_is_rejected(self):
        with self.assertRaisesRegex(
            ValidationError, "D99: Daily review policy required"
        ):
            daily_review_policy("D99")

    def test_candidate_path_is_derived_from_declared_scene(self):
        self.assertEqual(
            daily_candidate_path("D02", "r01", "morning-rug-daze", "a"),
            "source/candidates/d02/r01/"
            "akari-v1.2_d02_morning-rug-daze_r01-a.png",
        )

    def test_d01_live_request_keeps_dimension_tolerance(self):
        request = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml")
            .read_text(encoding="utf-8")
        )
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / request["candidates"][0]["target_path"]
            source.parent.mkdir(parents=True)
            Image.new("RGB", (1028, 1540), "white").save(source)
            validate_daily_candidate_dimensions(request, root)
            Image.new("RGB", (1029, 1540), "white").save(source)
            with self.assertRaisesRegex(
                ValidationError, "D01 r01: candidate dimensions outside"
            ):
                validate_daily_candidate_dimensions(request, root)

    def test_generation_request_rejects_reordered_scene_contract(self):
        request = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml")
            .read_text(encoding="utf-8")
        )
        contract = daily_contract(request)
        request["scene_contract"] = dict(
            reversed(request["scene_contract"].items())
        )

        with self.assertRaisesRegex(
            ValidationError, "D01 scene_contract mismatch"
        ):
            validate_daily_generation_request(request, contract)

    def test_generation_request_allows_reordered_production_requirements(self):
        request = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml")
            .read_text(encoding="utf-8")
        )
        contract = daily_contract(request)
        request["production_requirements"] = dict(
            reversed(request["production_requirements"].items())
        )

        validate_daily_generation_request(request, contract)

    def test_generation_request_allows_reordered_candidate_policy(self):
        request = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml")
            .read_text(encoding="utf-8")
        )
        contract = daily_contract(request)
        request["candidate_policy"] = dict(
            reversed(request["candidate_policy"].items())
        )

        validate_daily_generation_request(request, contract)

    def test_d01_non_string_prompt_keeps_legacy_mismatch_message(self):
        request = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/generation-requests/d01-r01.yaml")
            .read_text(encoding="utf-8")
        )
        request["shared_prompt"] = None

        with self.assertRaisesRegex(
            ValidationError, "D01 exact shared prompt contract mismatch"
        ):
            validate_generation_request(request)


class D02ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.request = yaml.safe_load(
            (request_root / "d02-r01.yaml").read_text(encoding="utf-8")
        )
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]

    def test_live_d02_asset_contract_is_valid(self):
        validate_assets(self.assets)

    def test_live_d02_generation_request_is_valid(self):
        validate_generation_request(self.request)

    def test_live_d02_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)

    def test_live_d02_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d01_morning_continuity",
                "accepted_c04_floor_sitting_body",
                "accepted_c05_morning_hair",
                "accepted_c06_sleepy_neutral_expression",
                "accepted_c07_seated_sock_feet",
            ],
        )


class D03ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        cls.d03 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D03"
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.request = yaml.safe_load(
            (request_root / "d03-r01.yaml").read_text(encoding="utf-8")
        )
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]

    def test_live_d03_asset_is_registered_and_accepted(self):
        self.assertEqual(self.d03["descriptor"], "morning-curtain-pause")
        self.assertEqual(
            self.d03["depends_on"],
            ["D02", "C01", "C03", "C05", "C06", "C07"],
        )
        self.assertEqual(self.d03["status"], "accepted")
        self.assertEqual(self.d03["revision"], "r01")
        self.assertEqual(
            self.d03["accepted_paths"],
            [
                "accepted/daily/morning/"
                "akari-v1.2_d03_morning-curtain-pause_r01.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d03_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d03_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d02_morning_continuity",
                "accepted_c01_standing_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_morning_hair_sleepy_neutral",
                "accepted_c07_standing_sock_feet",
            ],
        )

    def test_live_d03_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D04ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]

    def d04_asset(self) -> dict:
        return next(
            asset
            for asset in self.assets["assets"]
            if asset["asset_id"] == "D04"
        )

    def d04_request(self) -> dict:
        return next(
            request
            for request in self.requests
            if (request["asset_id"], request["revision"]) == ("D04", "r01")
        )

    def test_live_d04_asset_is_registered_and_accepted_r02(self):
        d04 = self.d04_asset()
        self.assertEqual(d04["descriptor"], "morning-drink-fetch")
        self.assertEqual(d04["phase"], 7)
        self.assertEqual(
            d04["depends_on"],
            ["D03", "C01", "C03", "C05", "C06", "C07"],
        )
        self.assertEqual(d04["status"], "accepted")
        self.assertEqual(d04["revision"], "r02")
        self.assertEqual(
            d04["accepted_paths"],
            [
                "accepted/daily/morning/"
                "akari-v1.2_d04_morning-drink-fetch_r02.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d04_generation_request_is_valid(self):
        request = self.d04_request()
        self.assertEqual(
            [item["variant"] for item in request["candidates"]],
            ["a", "b", "c"],
        )
        validate_generation_request(request)

    def test_live_d04_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.d04_request()["references"]],
            [
                "accepted_d03_morning_continuity",
                "accepted_c01_standing_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_morning_hair_sleepy_neutral",
                "accepted_c07_standing_sock_feet",
            ],
        )

    def test_live_d04_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D04R02ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D04", "r02")
        )

    def test_live_d04_r02_request_uses_two_independent_candidates(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        self.assertEqual(
            [item["target_path"] for item in self.request["candidates"]],
            [
                "source/candidates/d04/r02/"
                "akari-v1.2_d04_morning-drink-fetch_r02-a.png",
                "source/candidates/d04/r02/"
                "akari-v1.2_d04_morning-drink-fetch_r02-b.png",
            ],
        )
        validate_generation_request(self.request)

    def test_live_d04_r02_contract_eliminates_crossover_staging(self):
        self.assertEqual(
            self.request["scene_contract"]["camera"],
            "room-side-profile-biased-three-quarter-moving-frame-right",
        )
        self.assertEqual(
            self.request["scene_contract"]["pose"],
            "short-weight-transfer-on-two-visible-parallel-foot-lanes",
        )
        prompt = self.request["shared_prompt"]
        for phrase in (
            "two visibly separate parallel floor lanes",
            "at least one sock-width of clear image-plane gap",
            "less than one foot length",
            "never overlap or cross in the image plane",
            "Do not use any D04 r01 candidate as a reference",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, prompt)

    def test_live_d04_r02_reuses_only_the_frozen_accepted_references(self):
        r01 = next(
            request
            for request in self.requests
            if (request["asset_id"], request["revision"]) == ("D04", "r01")
        )
        self.assertEqual(self.request["references"], r01["references"])
        validate_generation_dependencies(self.assets, self.requests)


class D05ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d05 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D05"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D05", "r01")
        )

    def test_live_d05_asset_is_registered_as_wave_one_acceptance(self):
        self.assertEqual(self.d05["descriptor"], "morning-washroom-route")
        self.assertEqual(self.d05["phase"], 8)
        self.assertEqual(
            self.d05["depends_on"],
            ["D04", "C02", "C03", "C05", "C06", "C07"],
        )
        self.assertEqual(self.d05["status"], "accepted")
        self.assertEqual(self.d05["revision"], "r01")
        self.assertEqual(
            self.d05["accepted_paths"],
            [
                "accepted/daily/morning/"
                "akari-v1.2_d05_morning-washroom-route_r01.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d05_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d05_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d04_morning_continuity",
                "accepted_c02_rear_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_morning_hair_sleepy_neutral",
                "accepted_c07_standing_sock_feet",
            ],
        )

    def test_live_d05_scene_contract_is_distinct_from_kitchenette(self):
        self.assertEqual(
            self.request["scene_contract"]["camera"],
            "hall-side-rear-left-three-quarter-natural-standing-height",
        )
        self.assertEqual(
            self.request["scene_contract"]["destination"],
            "closed-or-barely-ajar-frosted-washroom-door",
        )
        for phrase in (
            "momentary slowdown rather than a walking stride",
            "two visibly separate parallel floor lanes",
            "No mirror, sink, toilet, toothbrush",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d05_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D06ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d06 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D06"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D06", "r01")
        )

    def test_live_d06_asset_is_registered_as_wave_two_acceptance(self):
        self.assertEqual(self.d06["descriptor"], "evening-entryway-floor-sit")
        self.assertEqual(self.d06["phase"], 9)
        self.assertEqual(
            self.d06["depends_on"],
            ["D05", "C01", "C03", "C04", "C06", "C07"],
        )
        self.assertEqual(self.d06["status"], "accepted")
        self.assertEqual(self.d06["revision"], "r01")
        self.assertEqual(
            self.d06["accepted_paths"],
            [
                "accepted/daily/evening/"
                "akari-v1.2_d06_evening-entryway-floor-sit_r01.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d06_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d06_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_c04_grounded_floor_sitting",
                "accepted_c01_normal_hair_identity",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_2_safe_relief_expression",
                "accepted_c07_seated_sock_feet",
            ],
        )

    def test_live_d06_scene_contract_is_return_home_not_collapse(self):
        self.assertEqual(
            self.request["scene_contract"]["camera"],
            "room-side-front-left-three-quarter-natural-seated-height",
        )
        self.assertEqual(
            self.request["scene_contract"]["location"],
            "compact-closed-apartment-entryway",
        )
        for phrase in (
            "controlled low floor sit",
            "safe private relief after arriving home",
            "one neat pair of removed",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d06_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D07ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d07 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D07"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D07", "r01")
        )

    def test_live_d07_asset_is_registered_as_wave_two_acceptance(self):
        self.assertEqual(self.d07["descriptor"], "evening-shallow-sofa-sit")
        self.assertEqual(self.d07["phase"], 10)
        self.assertEqual(
            self.d07["depends_on"],
            ["D06", "C03", "C04", "C06", "C07"],
        )
        self.assertEqual(self.d07["status"], "accepted")
        self.assertEqual(self.d07["revision"], "r01")
        self.assertEqual(
            self.d07["accepted_paths"],
            [
                "accepted/daily/evening/"
                "akari-v1.2_d07_evening-shallow-sofa-sit_r01.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d07_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d07_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d06_same_evening_continuity",
                "accepted_c04_grounded_seated_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_2_safe_relief_expression",
                "accepted_c07_seated_sock_feet",
            ],
        )

    def test_live_d07_scene_contract_is_shallow_sofa_support(self):
        self.assertEqual(
            self.request["scene_contract"]["camera"],
            "room-side-front-left-three-quarter-natural-seated-height",
        )
        self.assertEqual(
            self.request["scene_contract"]["seat"],
            "front-third-of-compact-low-backed-neutral-fabric-sofa",
        )
        for phrase in (
            "shallow but fully supported sofa-edge sit",
            "both socked soles fully flat",
            "safe quiet decompression",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d07_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D08ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d08 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D08"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D08", "r01")
        )

    def test_live_d08_asset_is_registered_as_wave_two_acceptance(self):
        self.assertEqual(self.d08["descriptor"], "evening-bed-edge-sock-adjust")
        self.assertEqual(self.d08["phase"], 11)
        self.assertEqual(
            self.d08["depends_on"],
            ["D07", "C03", "C04", "C06", "C07"],
        )
        self.assertEqual(self.d08["status"], "accepted")
        self.assertEqual(self.d08["revision"], "r03")
        self.assertEqual(
            self.d08["accepted_paths"],
            [
                "accepted/daily/evening/"
                "akari-v1.2_d08_evening-bed-edge-sock-adjust_r03.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d08_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b", "c"],
        )
        validate_generation_request(self.request)

    def test_live_d08_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d07_same_evening_continuity",
                "accepted_c04_grounded_seated_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_2_safe_relief_expression",
                "accepted_c07_seated_sock_feet",
            ],
        )

    def test_live_d08_scene_contract_is_supported_sock_adjustment(self):
        self.assertEqual(
            self.request["scene_contract"]["camera"],
            "bed-foot-side-front-left-three-quarter-natural-seated-height",
        )
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "two-hand-character-right-sock-top-adjustment",
        )
        for phrase in (
            "Both hands lightly straighten",
            "character-right sock",
            "heel and sole grounded",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d08_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D08R02ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D08", "r02")
        )

    def test_live_d08_r02_uses_three_independent_candidates_after_ab_rejection(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b", "c"],
        )
        validate_generation_request(self.request)

    def test_live_d08_r02_reuses_only_frozen_accepted_references(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d07_same_evening_continuity",
                "accepted_c04_grounded_seated_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_2_safe_relief_expression",
                "accepted_c07_seated_sock_feet",
            ],
        )
        self.assertNotIn("r01-a", self.request["shared_prompt"])
        self.assertNotIn("r01-b", self.request["shared_prompt"])
        self.assertNotIn("r01-c", self.request["shared_prompt"])

    def test_live_d08_r02_keeps_right_sock_lower_while_adjusting_left(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "two-hand-character-left-sock-top-smoothing",
        )
        self.assertEqual(
            self.request["scene_contract"]["humanization"],
            [
                "character-right-hoodie-cuff-pushed-up-one-thumb-width",
                "untouched-character-right-sock-slightly-lower-with-both-stripes-complete",
            ],
        )
        for phrase in (
            "character-left sock",
            "character-right sock stays slightly lower",
            "Do not stretch either sock mouth into a detached band",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d08_r02_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D08R03ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D08", "r03")
        )

    def test_live_d08_r03_starts_with_two_independent_candidates(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d08_r03_uses_explicit_screen_side_coordinates(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "two-hand-image-right-character-left-sock-top-smoothing",
        )
        self.assertEqual(
            self.request["scene_contract"]["humanization"],
            [
                "character-right-hoodie-cuff-pushed-up-one-thumb-width",
                "image-left-character-right-sock-slightly-lower-with-both-stripes-complete",
            ],
        )
        for phrase in (
            "IMAGE-RIGHT side of the final picture",
            "ONLY the IMAGE-RIGHT leg and sock",
            "untouched character-right leg and sock must appear on IMAGE-LEFT",
            "Do not mirror this working-side relationship",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d08_r03_reuses_only_frozen_accepted_references(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d07_same_evening_continuity",
                "accepted_c04_grounded_seated_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_2_safe_relief_expression",
                "accepted_c07_seated_sock_feet",
            ],
        )
        for revision in ("r01", "r02"):
            for variant in ("a", "b", "c"):
                self.assertNotIn(
                    f"{revision}-{variant}", self.request["shared_prompt"]
                )

    def test_live_d08_r03_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D09ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d09 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D09"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D09", "r01")
        )

    def test_live_d09_asset_is_registered_as_wave_two_acceptance(self):
        self.assertEqual(self.d09["descriptor"], "evening-phone-sleepy-bed-sit")
        self.assertEqual(self.d09["phase"], 12)
        self.assertEqual(
            self.d09["depends_on"],
            ["D08", "C03", "C04", "C06", "C07"],
        )
        self.assertEqual(self.d09["status"], "accepted")
        self.assertEqual(self.d09["revision"], "r01")
        self.assertEqual(
            self.d09["accepted_paths"],
            [
                "accepted/daily/evening/"
                "akari-v1.2_d09_evening-phone-sleepy-bed-sit_r01.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d09_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d09_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d08_same_evening_bedroom_continuity",
                "accepted_c04_grounded_seated_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_1_sleepy_awake_expression",
                "accepted_c07_seated_sock_feet",
            ],
        )

    def test_live_d09_scene_contract_is_sleepy_but_awake_phone_use(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "two-hand-single-phone-viewing-above-lap",
        )
        for phrase in (
            "both eyes visibly open",
            "one ordinary smartphone in both hands",
            "screen content completely unreadable",
            "not sleep or collapse",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d09_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D10ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d10 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D10"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D10", "r01")
        )

    def test_live_d10_asset_is_registered_as_wave_two_acceptance(self):
        self.assertEqual(self.d10["descriptor"], "evening-rug-side-rest")
        self.assertEqual(self.d10["phase"], 13)
        self.assertEqual(
            self.d10["depends_on"],
            ["D09", "D02", "C03", "C06", "C07"],
        )
        self.assertEqual(self.d10["status"], "accepted")
        self.assertEqual(self.d10["revision"], "r01")
        self.assertEqual(
            self.d10["accepted_paths"],
            [
                "accepted/daily/evening/"
                "akari-v1.2_d10_evening-rug-side-rest_r01.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d10_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d10_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d09_same_evening_continuity",
                "accepted_d02_plain_rug_contact",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c06_1_sleepy_awake_expression",
                "accepted_c07_seated_sock_feet",
            ],
        )

    def test_live_d10_scene_contract_is_awake_supported_side_rest(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "character-right-side-lying-rest-on-rug",
        )
        for phrase in (
            "both eyes visibly open",
            "character-right side",
            "fully supported by the rug",
            "not sleep or collapse",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d10_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D11ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d11 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D11"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D11", "r02")
        )

    def test_live_d11_asset_is_registered_as_wave_three_acceptance(self):
        self.assertEqual(self.d11["descriptor"], "life-laundry-fold")
        self.assertEqual(self.d11["phase"], 14)
        self.assertEqual(
            self.d11["depends_on"],
            ["D10", "D07", "D02", "C03", "C07"],
        )
        self.assertEqual(self.d11["status"], "accepted")
        self.assertEqual(self.d11["revision"], "r02")
        self.assertEqual(
            self.d11["accepted_paths"],
            ["accepted/daily/life/akari-v1.2_d11_life-laundry-fold_r02.png"],
        )
        validate_assets(self.assets)

    def test_live_d11_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d11_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d10_recent_identity_outfit",
                "accepted_d07_shallow_sofa_support",
                "accepted_d02_plain_rug_contact",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c07_seated_sock_feet",
            ],
        )

    def test_live_d11_scene_contract_is_single_towel_fold(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "two-hand-single-towel-fold-across-lap",
        )
        for phrase in (
            "one small pale-blue rectangular towel",
            "Each hand holds a different near corner",
            "both socked feet fully flat on the rug",
            "not posing",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d11_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D12ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d12 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D12"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D12", "r01")
        )

    def test_live_d12_asset_is_registered_as_wave_three_acceptance(self):
        self.assertEqual(self.d12["descriptor"], "life-fridge-open")
        self.assertEqual(self.d12["phase"], 15)
        self.assertEqual(
            self.d12["depends_on"],
            ["D11", "D04", "C03", "C01", "C07"],
        )
        self.assertEqual(self.d12["status"], "accepted")
        self.assertEqual(self.d12["revision"], "r01")
        self.assertEqual(
            self.d12["accepted_paths"],
            ["accepted/daily/life/akari-v1.2_d12_life-fridge-open_r01.png"],
        )
        validate_assets(self.assets)

    def test_live_d12_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d12_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d11_recent_identity_outfit",
                "accepted_d04_compact_kitchenette_route",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c01_standing_body",
                "accepted_c07_standing_sock_feet",
            ],
        )

    def test_live_d12_scene_contract_is_single_fridge_open_action(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "character-right-hand-open-fridge-door",
        )
        for phrase in (
            "opens the refrigerator door",
            "door never crosses in front of her body",
            "both socked feet fully flat",
            "no second action",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d12_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D13ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d13 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D13"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D13", "r01")
        )

    def test_live_d13_asset_is_registered_as_wave_three_acceptance(self):
        self.assertEqual(self.d13["descriptor"], "life-charger-search")
        self.assertEqual(self.d13["phase"], 16)
        self.assertEqual(
            self.d13["depends_on"],
            ["D12", "D04", "C03", "C01", "C07"],
        )
        self.assertEqual(self.d13["status"], "accepted")
        self.assertEqual(self.d13["revision"], "r02")
        self.assertEqual(
            self.d13["accepted_paths"],
            [
                "accepted/daily/life/"
                "akari-v1.2_d13_life-charger-search_r02.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d13_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d13_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d12_recent_identity_outfit_action",
                "accepted_d04_compact_room_route",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c01_standing_body",
                "accepted_c07_standing_sock_feet",
            ],
        )

    def test_live_d13_scene_contract_is_search_before_retrieval(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "right-hand-open-drawer-left-hand-hover-search",
        )
        for phrase in (
            "searches one shallow desk drawer",
            "Neither hand holds",
            "both socked feet fully flat",
            "no second action",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d13_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D13R02ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D13", "r02")
        )

    def test_live_d13_r02_uses_two_independent_candidates(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d13_r02_uses_explicit_screen_side_hands(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "screen-right-hand-open-drawer-screen-left-hand-hover-search",
        )
        for phrase in (
            "screen-right hand grips",
            "screen-left hand hovers",
            "Do not reinterpret screen-right",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d13_r02_reuses_only_frozen_accepted_references(self):
        r01 = next(
            request
            for request in self.requests
            if (request["asset_id"], request["revision"]) == ("D13", "r01")
        )
        self.assertEqual(self.request["references"], r01["references"])

    def test_live_d13_r02_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D14ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d14 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D14"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D14", "r01")
        )

    def test_live_d14_asset_is_registered_as_wave_three_acceptance(self):
        self.assertEqual(self.d14["descriptor"], "life-bag-unpack")
        self.assertEqual(self.d14["phase"], 17)
        self.assertEqual(
            self.d14["depends_on"],
            ["D13", "D11", "D06", "C03", "C07"],
        )
        self.assertEqual(self.d14["status"], "accepted")
        self.assertEqual(self.d14["revision"], "r02")
        self.assertEqual(
            self.d14["accepted_paths"],
            [
                "accepted/daily/life/"
                "akari-v1.2_d14_life-bag-unpack_r02.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d14_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d14_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d13_recent_identity_outfit_action",
                "accepted_d11_sofa_edge_support",
                "accepted_d06_soft_bag_family",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c07_seated_sock_feet",
            ],
        )

    def test_live_d14_scene_contract_is_single_bag_unpack_action(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "screen-left-hand-hold-bag-open-screen-right-hand-lift-notebook",
        )
        for phrase in (
            "unpacks one pale soft shoulder tote",
            "exactly three bag contents",
            "both socked feet fully flat",
            "There is no second action",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d14_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D14R02ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]

    def test_live_d14_r02_uses_two_independent_candidates(self):
        request_keys = [
            (request["asset_id"], request["revision"])
            for request in self.requests
        ]
        self.assertIn(("D14", "r02"), request_keys)
        request = next(
            request
            for request in self.requests
            if (request["asset_id"], request["revision"]) == ("D14", "r02")
        )
        self.assertEqual(
            [item["variant"] for item in request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(request)

    def test_live_d14_r02_uses_side_neutral_hand_roles(self):
        request = next(
            (
                request
                for request in self.requests
                if (request["asset_id"], request["revision"]) == ("D14", "r02")
            ),
            None,
        )
        self.assertIsNotNone(request)
        self.assertEqual(
            request["scene_contract"]["action"],
            "one-visible-hand-hold-bag-open-other-visible-hand-lift-notebook",
        )
        for phrase in (
            "One visible hand holds",
            "The other visible hand lifts",
            "Keep both hands distinct",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, request["shared_prompt"])

    def test_live_d14_r02_reuses_only_frozen_accepted_references(self):
        r01 = next(
            request
            for request in self.requests
            if (request["asset_id"], request["revision"]) == ("D14", "r01")
        )
        r02 = next(
            (
                request
                for request in self.requests
                if (request["asset_id"], request["revision"]) == ("D14", "r02")
            ),
            None,
        )
        self.assertIsNotNone(r02)
        self.assertEqual(r02["references"], r01["references"])

    def test_live_d14_r02_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D14R01RejectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def test_live_d14_r01_reviews_reject_ordered_ab_for_shared_scene_failure(self):
        reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("D14", "r01")
        ]
        self.assertEqual(
            [
                (review["candidate_id"], review["status"])
                for review in reviews
            ],
            [("d14-r01-a", "rejected"), ("d14-r01-b", "rejected")],
        )
        for review in reviews:
            with self.subTest(candidate_id=review["candidate_id"]):
                self.assertEqual(review["findings"][0]["severity"], "major")
                self.assertEqual(
                    review["findings"][0]["controlling_source_asset"],
                    "D14-scene",
                )


class D15ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.d15 = next(
            asset for asset in cls.assets["assets"] if asset["asset_id"] == "D15"
        )
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D15", "r01")
        )

    def test_live_d15_asset_is_registered_as_wave_three_acceptance(self):
        self.assertEqual(self.d15["descriptor"], "life-pc-posture-break")
        self.assertEqual(self.d15["phase"], 18)
        self.assertEqual(
            self.d15["depends_on"],
            ["D14", "D13", "D11", "C03", "C07"],
        )
        self.assertEqual(self.d15["status"], "accepted")
        self.assertEqual(self.d15["revision"], "r01")
        self.assertEqual(
            self.d15["accepted_paths"],
            [
                "accepted/daily/life/"
                "akari-v1.2_d15_life-pc-posture-break_r01.png"
            ],
        )
        validate_assets(self.assets)

    def test_live_d15_generation_request_is_valid(self):
        self.assertEqual(
            [item["variant"] for item in self.request["candidates"]],
            ["a", "b"],
        )
        validate_generation_request(self.request)

    def test_live_d15_reference_roles_are_ordered(self):
        self.assertEqual(
            [reference["role"] for reference in self.request["references"]],
            [
                "accepted_d14_recent_identity_outfit_action",
                "accepted_d13_compact_desk_room",
                "accepted_d11_supported_seated_body",
                "accepted_c03_hairpin_three_quarter",
                "accepted_c07_seated_sock_feet",
            ],
        )

    def test_live_d15_scene_contract_is_supported_awake_posture_break(self):
        self.assertEqual(
            self.request["scene_contract"]["action"],
            "desk-side-elbow-supported-awake-chair-posture-break",
        )
        for phrase in (
            "relaxes her posture in front of one desktop computer",
            "both open eyes",
            "dark blank unreadable screen",
            "never collapsed, ill, or asleep",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.request["shared_prompt"])

    def test_live_d15_generation_dependencies_are_valid(self):
        validate_generation_dependencies(self.assets, self.requests)


class D04RetryPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def request_with_optional_c(self) -> dict:
        return copy.deepcopy(
            next(item for item in self.requests if item["asset_id"] == "D04")
        )

    def requests_with_d04(self, d04_request: dict) -> list[dict]:
        return [
            d04_request
            if (item["asset_id"], item["revision"]) == ("D04", "r01")
            else item
            for item in self.requests
            if (item["asset_id"], item["revision"]) != ("D04", "r02")
        ]

    def candidate_d04_assets(self) -> dict:
        assets = copy.deepcopy(self.assets)
        d04 = next(
            item for item in assets["assets"] if item["asset_id"] == "D04"
        )
        d04.update(status="candidate", revision="r00", accepted_paths=[])
        return assets

    def log_with_d04(self, reviews: list[dict]) -> dict:
        log = copy.deepcopy(self.review_log)
        log["reviews"] = [
            review for review in log["reviews"] if review["asset_id"] != "D04"
        ]
        log["reviews"].extend(reviews)
        return log

    def test_d04_optional_c_allows_distinct_candidate_local_controllers(self):
        request = self.request_with_optional_c()
        reviews = [d04_review("a", "C03"), d04_review("b", "D04-scene")]
        review_log = self.log_with_d04(reviews)
        validate_review_log(review_log)
        validate_lifecycle_linkage(
            self.candidate_d04_assets(),
            self.requests_with_d04(request),
            review_log,
        )

    def test_d04_optional_c_rejects_shared_non_scene_controller(self):
        request = self.request_with_optional_c()
        reviews = [d04_review("a", "C03"), d04_review("b", "C03")]
        with self.assertRaisesRegex(
            ValidationError,
            "D04 r01: optional C requires rejected scene-only A/B",
        ):
            validate_lifecycle_linkage(
                self.candidate_d04_assets(),
                self.requests_with_d04(request),
                self.log_with_d04(reviews),
            )


class D02LifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.request = next(
            request
            for request in cls.requests
            if (request["asset_id"], request["revision"]) == ("D02", "r01")
        )
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def log_with_d02(self, reviews: list[dict]) -> dict:
        log = copy.deepcopy(self.review_log)
        log["reviews"] = [
            review for review in log["reviews"] if review["asset_id"] != "D02"
        ]
        log["reviews"].extend(reviews)
        return log

    def isolated_assets(self, accepted: bool = False) -> dict:
        assets = copy.deepcopy(self.assets)
        for asset in assets["assets"]:
            asset.update(status="candidate", revision="r00", accepted_paths=[])
        if accepted:
            d02 = next(
                asset for asset in assets["assets"] if asset["asset_id"] == "D02"
            )
            d02.update(
                status="accepted",
                revision="r01",
                accepted_paths=[
                    "accepted/daily/morning/"
                    "akari-v1.2_d02_morning-rug-daze_r01.png"
                ],
            )
        return assets

    def assets_with_candidate_d02(self) -> dict:
        assets = copy.deepcopy(self.assets)
        d02 = next(
            asset for asset in assets["assets"] if asset["asset_id"] == "D02"
        )
        d02.update(status="candidate", revision="r00", accepted_paths=[])
        return assets

    def request_with_optional_c(self) -> dict:
        request = copy.deepcopy(self.request)
        request["candidates"].append(
            {
                "variant": "c",
                "title": "independent-scene-c",
                "target_path": (
                    "source/candidates/d02/r01/"
                    "akari-v1.2_d02_morning-rug-daze_r01-c.png"
                ),
            }
        )
        return request

    def test_live_d02_accepted_linkage_matches_explicit_selection(self):
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )
        validate_gate4(self.assets, self.review_log)

        d02 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D02"
        )
        accepted_path = (
            "accepted/daily/morning/"
            "akari-v1.2_d02_morning-rug-daze_r01.png"
        )
        self.assertEqual(d02["status"], "accepted")
        self.assertEqual(d02["revision"], "r01")
        self.assertEqual(d02["accepted_paths"], [accepted_path])

        accepted_reviews = [
            review
            for review in self.review_log["reviews"]
            if review["asset_id"] == "D02" and review["status"] == "accepted"
        ]
        self.assertEqual(len(accepted_reviews), 1)
        selected_review = accepted_reviews[0]
        self.assertEqual(selected_review["candidate_id"], "d02-r01-b")

        selected_sha256 = (
            "0d0341a592adb9cf4e0a3b90ccf78989eb3a7da99c3a757106fce0d98a72cd2e"
        )
        source_path = PACKAGE_ROOT / selected_review["source_paths"][0]
        promoted_path = PACKAGE_ROOT / accepted_path
        promoted_sha256 = hashlib.sha256(promoted_path.read_bytes()).hexdigest()
        self.assertEqual(selected_review["source_sha256s"], [selected_sha256])
        self.assertEqual(promoted_sha256, selected_sha256)
        if source_path.exists():
            source_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
            self.assertEqual(source_sha256, selected_sha256)

    def test_live_d02_accepted_linkage_allows_absent_local_candidate(self):
        candidate_path = (
            PACKAGE_ROOT
            / "source/candidates/d02/r01/"
            "akari-v1.2_d02_morning-rug-daze_r01-b.png"
        )
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def exists_without_candidate(path: Path) -> bool:
            if path == candidate_path:
                return False
            return original_exists(path)

        def read_without_candidate(path: Path) -> bytes:
            if path == candidate_path:
                raise FileNotFoundError(candidate_path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "exists", new=exists_without_candidate),
            mock.patch.object(Path, "read_bytes", new=read_without_candidate),
        ):
            try:
                self.test_live_d02_accepted_linkage_matches_explicit_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local candidate: {error}")

    def test_d02_findings_allow_every_declared_controller(self):
        for controller in ("D01", "C04", "C05", "C06", "C07", "D02-scene"):
            with self.subTest(controller=controller):
                validate_review_log(
                    self.log_with_d02(
                        [d02_review("a", findings=[d02_finding(controller)])]
                    )
                )

    def test_d02_findings_reject_unknown_controller(self):
        with self.assertRaisesRegex(
            ValidationError, "D02: exact finding provenance required"
        ):
            validate_review_log(
                self.log_with_d02(
                    [d02_review("a", findings=[d02_finding("C03")])]
                )
            )

    def test_d02_acceptance_uses_daily_review_status_rules(self):
        with self.assertRaisesRegex(
            ValidationError, "D02: accepted requires no unresolved finding"
        ):
            validate_review_log(
                self.log_with_d02(
                    [
                        d02_review(
                            "a", status="accepted", findings=[d02_finding()]
                        )
                    ]
                )
            )

        allowed = d02_finding()
        allowed["severity"] = "minor"
        validate_review_log(
            self.log_with_d02(
                [d02_review("a", status="accepted-with-notes", findings=[allowed])]
            )
        )

        invalid = copy.deepcopy(allowed)
        invalid["controlling_source_asset"] = "D01"
        with self.assertRaisesRegex(
            ValidationError,
            "D02: accepted-with-notes requires D02-scene Minor only",
        ):
            validate_review_log(
                self.log_with_d02(
                    [
                        d02_review(
                            "a",
                            status="accepted-with-notes",
                            findings=[invalid],
                        )
                    ]
                )
            )

    def test_d02_candidate_reviews_are_an_ordered_prefix(self):
        validate_lifecycle_linkage(
            self.assets_with_candidate_d02(),
            self.requests,
            self.log_with_d02([d02_review("a")]),
        )
        with self.assertRaisesRegex(
            ValidationError, "reviews must match declared D02 candidates in order"
        ):
            validate_lifecycle_linkage(
                self.assets_with_candidate_d02(),
                self.requests,
                self.log_with_d02([d02_review("b")]),
            )

    def test_d02_generated_ab_allows_review_lag_before_selection(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for candidate in self.request["candidates"]:
                source = root / candidate["target_path"]
                source.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (1024, 1536), "white").save(source)
            for reviews in ([], [d02_review("a")]):
                with self.subTest(review_count=len(reviews)):
                    validate_lifecycle_linkage(
                        self.isolated_assets(),
                        [self.request],
                        {"reviews": reviews},
                        root,
                    )

    def test_d02_reviews_cannot_outpace_generated_candidates(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_a = root / self.request["candidates"][0]["target_path"]
            source_a.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "white").save(source_a)
            with self.assertRaisesRegex(
                ValidationError,
                "D02 r01: generated candidates require ordered reviews",
            ):
                validate_lifecycle_linkage(
                    self.isolated_assets(),
                    [self.request],
                    {"reviews": [d02_review("a"), d02_review("b")]},
                    root,
                )

    def test_d02_review_requires_a_generated_candidate_when_root_is_known(self):
        with TemporaryDirectory() as directory:
            with self.assertRaisesRegex(
                ValidationError,
                "D02 r01: generated candidates require ordered reviews",
            ):
                validate_lifecycle_linkage(
                    self.isolated_assets(),
                    [self.request],
                    {"reviews": [d02_review("a")]},
                    Path(directory),
                )

    def test_d02_generated_candidates_must_be_an_ordered_prefix(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_b = root / self.request["candidates"][1]["target_path"]
            source_b.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "white").save(source_b)
            with self.assertRaisesRegex(
                ValidationError,
                "D02 r01: generated candidates require ordered reviews",
            ):
                validate_lifecycle_linkage(
                    self.isolated_assets(),
                    [self.request],
                    {"reviews": []},
                    root,
                )

    def test_d02_optional_c_requires_rejected_scene_only_ab(self):
        request = self.request_with_optional_c()
        reviews = [
            d02_review(variant, status="rejected", findings=[d02_finding()])
            for variant in ("a", "b")
        ]
        validate_lifecycle_linkage(
            self.isolated_assets(), [request], {"reviews": reviews}
        )

        invalid = copy.deepcopy(reviews)
        invalid[1]["findings"][0]["controlling_source_asset"] = "D01"
        with self.assertRaisesRegex(
            ValidationError,
            "D02 r01: optional C requires rejected scene-only A/B",
        ):
            validate_lifecycle_linkage(
                self.isolated_assets(), [request], {"reviews": invalid}
            )

    def test_d02_optional_c_requires_completed_ab_reviews(self):
        request = self.request_with_optional_c()
        with self.assertRaisesRegex(
            ValidationError,
            "D02 r01: optional C requires rejected scene-only A/B",
        ):
            validate_lifecycle_linkage(
                self.isolated_assets(), [request], {"reviews": []}
            )

    def test_d02_optional_c_rejects_minor_only_ab_findings(self):
        request = self.request_with_optional_c()
        findings = []
        for _ in ("a", "b"):
            finding = d02_finding()
            finding["severity"] = "minor"
            findings.append(finding)
        reviews = [
            d02_review(variant, status="rejected", findings=[finding])
            for variant, finding in zip(("a", "b"), findings)
        ]
        with self.assertRaisesRegex(
            ValidationError,
            "D02 r01: optional C requires rejected scene-only A/B",
        ):
            validate_lifecycle_linkage(
                self.isolated_assets(), [request], {"reviews": reviews}
            )

    def test_d02_promotion_requires_exactly_one_accepted_selection(self):
        reviews = [d02_review("a", status="accepted"), d02_review("b", "rejected")]
        validate_lifecycle_linkage(
            self.isolated_assets(accepted=True),
            [self.request],
            {"reviews": reviews},
        )

        invalid = copy.deepcopy(reviews)
        invalid[1]["status"] = "accepted"
        with self.assertRaisesRegex(
            ValidationError, "D02 r01: expected exactly one accepted review"
        ):
            validate_lifecycle_linkage(
                self.isolated_assets(accepted=True),
                [self.request],
                {"reviews": invalid},
            )

    def test_d02_promotion_links_selected_source_and_accepted_hash(self):
        reviews = [d02_review("a", status="accepted"), d02_review("b", "rejected")]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / reviews[0]["source_paths"][0]
            accepted = (
                root
                / "accepted/daily/morning/"
                "akari-v1.2_d02_morning-rug-daze_r01.png"
            )
            source.parent.mkdir(parents=True)
            accepted.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "white").save(source)
            selected_bytes = source.read_bytes()
            accepted.write_bytes(selected_bytes)
            reviews[0]["source_sha256s"] = [
                hashlib.sha256(selected_bytes).hexdigest()
            ]
            validate_lifecycle_linkage(
                self.isolated_assets(accepted=True),
                [self.request],
                {"reviews": reviews},
                root,
            )

            Image.new("RGB", (1024, 1536), "black").save(source)
            with self.assertRaisesRegex(
                ValidationError,
                "D02 r01: selected source file SHA-256 mismatch",
            ):
                validate_lifecycle_linkage(
                    self.isolated_assets(accepted=True),
                    [self.request],
                    {"reviews": reviews},
                    root,
                )

            source.write_bytes(selected_bytes)
            Image.new("RGB", (1024, 1536), "black").save(accepted)
            with self.assertRaisesRegex(
                ValidationError, "D02 r01: accepted file SHA-256 mismatch"
            ):
                validate_lifecycle_linkage(
                    self.isolated_assets(accepted=True),
                    [self.request],
                    {"reviews": reviews},
                    root,
                )

    def test_gate4_remains_d01_only_and_accepts_live_record(self):
        validate_gate4(self.assets, self.review_log)


class D03LifecycleTests(unittest.TestCase):
    SELECTED_SHA256 = (
        "58bcce16338042ec63489c388c5bd1173477e18cfbecdfd1949f3d5ac84c7bc4"
    )
    ACCEPTED_PATH = (
        "accepted/daily/morning/"
        "akari-v1.2_d03_morning-curtain-pause_r01.png"
    )
    SOURCE_PATH = (
        "source/candidates/d03/r01/"
        "akari-v1.2_d03_morning-curtain-pause_r01-b.png"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d03_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d03 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D03"
        )
        self.assertEqual(d03["status"], "accepted")
        self.assertEqual(d03["revision"], "r01")
        self.assertEqual(d03["accepted_paths"], [self.ACCEPTED_PATH])

        accepted_reviews = [
            review
            for review in self.review_log["reviews"]
            if review["asset_id"] == "D03"
            and review["status"] in {"accepted", "accepted-with-notes"}
        ]
        self.assertEqual(len(accepted_reviews), 1)
        selected_review = accepted_reviews[0]
        self.assertEqual(selected_review["candidate_id"], "d03-r01-b")
        self.assertEqual(selected_review["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(
            selected_review["source_sha256s"], [self.SELECTED_SHA256]
        )

        promoted = PACKAGE_ROOT / self.ACCEPTED_PATH
        self.assertEqual(
            hashlib.sha256(promoted.read_bytes()).hexdigest(),
            self.SELECTED_SHA256,
        )
        source = PACKAGE_ROOT / self.SOURCE_PATH
        if source.exists():
            self.assertEqual(
                hashlib.sha256(source.read_bytes()).hexdigest(),
                self.SELECTED_SHA256,
            )

    def test_live_d03_accepted_linkage_matches_akari_selection(self):
        self.assert_live_d03_selection()

    def test_live_d03_linkage_allows_absent_local_candidate(self):
        candidate_path = PACKAGE_ROOT / self.SOURCE_PATH
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def exists_without_candidate(path: Path) -> bool:
            return False if path == candidate_path else original_exists(path)

        def read_without_candidate(path: Path) -> bytes:
            if path == candidate_path:
                raise FileNotFoundError(candidate_path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "exists", new=exists_without_candidate),
            mock.patch.object(Path, "read_bytes", new=read_without_candidate),
        ):
            try:
                self.assert_live_d03_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local candidate: {error}")

    def isolated_d03_lifecycle(self) -> tuple[dict, dict, dict]:
        assets = copy.deepcopy(self.assets)
        for asset in assets["assets"]:
            asset.update(status="candidate", revision="r00", accepted_paths=[])
        d03 = next(
            asset for asset in assets["assets"] if asset["asset_id"] == "D03"
        )
        d03.update(
            status="accepted",
            revision="r01",
            accepted_paths=[self.ACCEPTED_PATH],
        )
        request = next(
            request
            for request in self.requests
            if (request["asset_id"], request["revision"]) == ("D03", "r01")
        )
        review_log = {
            "reviews": [
                copy.deepcopy(review)
                for review in self.review_log["reviews"]
                if review["asset_id"] == "D03"
            ]
        }
        return assets, request, review_log

    def write_isolated_d03_files(
        self, root: Path, request: dict, review_log: dict
    ) -> tuple[Path, Path]:
        for candidate in request["candidates"]:
            source = root / candidate["target_path"]
            source.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (1024, 1536), "white").save(source)
        selected_source = root / self.SOURCE_PATH
        accepted = root / self.ACCEPTED_PATH
        accepted.parent.mkdir(parents=True, exist_ok=True)
        accepted.write_bytes(selected_source.read_bytes())
        selected_hash = hashlib.sha256(selected_source.read_bytes()).hexdigest()
        selected_review = next(
            review
            for review in review_log["reviews"]
            if review["status"] == "accepted"
        )
        selected_review["source_sha256s"] = [selected_hash]
        return selected_source, accepted

    def test_d03_linkage_rejects_selected_source_hash_mismatch(self):
        assets, request, review_log = self.isolated_d03_lifecycle()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            selected_source, _ = self.write_isolated_d03_files(
                root, request, review_log
            )
            Image.new("RGB", (1024, 1536), "black").save(selected_source)
            with self.assertRaisesRegex(
                ValidationError,
                "D03 r01: selected source file SHA-256 mismatch",
            ):
                validate_lifecycle_linkage(
                    assets, [request], review_log, root
                )

    def test_d03_linkage_rejects_accepted_hash_mismatch(self):
        assets, request, review_log = self.isolated_d03_lifecycle()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            _, accepted = self.write_isolated_d03_files(root, request, review_log)
            Image.new("RGB", (1024, 1536), "black").save(accepted)
            with self.assertRaisesRegex(
                ValidationError,
                "D03 r01: accepted file SHA-256 mismatch",
            ):
                validate_lifecycle_linkage(
                    assets, [request], review_log, root
                )


class D04R02LifecycleTests(unittest.TestCase):
    SELECTED_SHA256 = (
        "4def96ec68c8b7146f055fefb1f8049c7560b53b07943f03972422c9556e893c"
    )
    ACCEPTED_PATH = (
        "accepted/daily/morning/"
        "akari-v1.2_d04_morning-drink-fetch_r02.png"
    )
    SOURCE_PATH = (
        "source/candidates/d04/r02/"
        "akari-v1.2_d04_morning-drink-fetch_r02-b.png"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d04_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d04 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D04"
        )
        self.assertEqual(d04["status"], "accepted")
        self.assertEqual(d04["revision"], "r02")
        self.assertEqual(d04["accepted_paths"], [self.ACCEPTED_PATH])
        selected = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"], review["status"])
            == ("D04", "r02", "accepted")
        ]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["candidate_id"], "d04-r02-b")
        self.assertEqual(selected[0]["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected[0]["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d04_r02_linkage_matches_akari_selection(self):
        self.assert_live_d04_selection()

    def test_live_d04_r02_linkage_allows_all_local_d04_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d04_candidates(path: Path) -> bool:
            if "source/candidates/d04" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d04_candidates(path: Path) -> bool:
            if "source/candidates/d04" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d04_candidates(path: Path) -> bytes:
            if "source/candidates/d04" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d04_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d04_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d04_candidates),
        ):
            try:
                self.assert_live_d04_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D04 candidate: {error}")


class D05R01LifecycleTests(unittest.TestCase):
    SELECTED_SHA256 = (
        "7077af4a288696faa3f79c43726d2b946c05a0386264c7deb56097a2cda82dde"
    )
    ACCEPTED_PATH = (
        "accepted/daily/morning/"
        "akari-v1.2_d05_morning-washroom-route_r01.png"
    )
    SOURCE_PATH = (
        "source/candidates/d05/r01/"
        "akari-v1.2_d05_morning-washroom-route_r01-b.png"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d05_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d05 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D05"
        )
        self.assertEqual(d05["status"], "accepted")
        self.assertEqual(d05["revision"], "r01")
        self.assertEqual(d05["accepted_paths"], [self.ACCEPTED_PATH])
        selected = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"], review["status"])
            == ("D05", "r01", "accepted")
        ]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["candidate_id"], "d05-r01-b")
        self.assertEqual(selected[0]["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected[0]["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d05_r01_linkage_matches_akari_selection(self):
        self.assert_live_d05_selection()

    def test_live_d05_r01_linkage_allows_all_local_d05_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d05_candidates(path: Path) -> bool:
            if "source/candidates/d05" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d05_candidates(path: Path) -> bool:
            if "source/candidates/d05" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d05_candidates(path: Path) -> bytes:
            if "source/candidates/d05" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d05_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d05_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d05_candidates),
        ):
            try:
                self.assert_live_d05_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D05 candidate: {error}")


class D06R01LifecycleTests(unittest.TestCase):
    SELECTED_SHA256 = (
        "1b88dff62d7a3588f498b431d0931f98c7eb766cf3fb67d1624c0f05279c5c0d"
    )
    ACCEPTED_PATH = (
        "accepted/daily/evening/"
        "akari-v1.2_d06_evening-entryway-floor-sit_r01.png"
    )
    SOURCE_PATH = (
        "source/candidates/d06/r01/"
        "akari-v1.2_d06_evening-entryway-floor-sit_r01-a.png"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d06_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d06 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D06"
        )
        self.assertEqual(d06["status"], "accepted")
        self.assertEqual(d06["revision"], "r01")
        self.assertEqual(d06["accepted_paths"], [self.ACCEPTED_PATH])
        selected = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"], review["status"])
            == ("D06", "r01", "accepted")
        ]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["candidate_id"], "d06-r01-a")
        self.assertEqual(selected[0]["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected[0]["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d06_r01_linkage_matches_akari_selection(self):
        self.assert_live_d06_selection()

    def test_live_d06_r01_linkage_allows_all_local_d06_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d06_candidates(path: Path) -> bool:
            if "source/candidates/d06" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d06_candidates(path: Path) -> bool:
            if "source/candidates/d06" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d06_candidates(path: Path) -> bytes:
            if "source/candidates/d06" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d06_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d06_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d06_candidates),
        ):
            try:
                self.assert_live_d06_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D06 candidate: {error}")


class D07R01LifecycleTests(unittest.TestCase):
    SELECTED_SHA256 = (
        "cad79b2480b4d3392ebdca2cefebcf2dcb5f5c0e0108f64ce8b127aee83c8ef5"
    )
    ACCEPTED_PATH = (
        "accepted/daily/evening/"
        "akari-v1.2_d07_evening-shallow-sofa-sit_r01.png"
    )
    SOURCE_PATH = (
        "source/candidates/d07/r01/"
        "akari-v1.2_d07_evening-shallow-sofa-sit_r01-b.png"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d07_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d07 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D07"
        )
        self.assertEqual(d07["status"], "accepted")
        self.assertEqual(d07["revision"], "r01")
        self.assertEqual(d07["accepted_paths"], [self.ACCEPTED_PATH])
        selected = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"], review["status"])
            == ("D07", "r01", "accepted")
        ]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["candidate_id"], "d07-r01-b")
        self.assertEqual(selected[0]["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected[0]["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d07_r01_linkage_matches_akari_selection(self):
        self.assert_live_d07_selection()

    def test_live_d07_r01_linkage_allows_all_local_d07_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d07_candidates(path: Path) -> bool:
            if "source/candidates/d07" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d07_candidates(path: Path) -> bool:
            if "source/candidates/d07" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d07_candidates(path: Path) -> bytes:
            if "source/candidates/d07" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d07_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d07_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d07_candidates),
        ):
            try:
                self.assert_live_d07_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D07 candidate: {error}")


class D08R03LifecycleTests(unittest.TestCase):
    SELECTED_SHA256 = (
        "9e238261e18ca68753bc697bc7be9811eac7e397da143a143555ea7c10671fd7"
    )
    ACCEPTED_PATH = (
        "accepted/daily/evening/"
        "akari-v1.2_d08_evening-bed-edge-sock-adjust_r03.png"
    )
    SOURCE_PATH = (
        "source/candidates/d08/r03/"
        "akari-v1.2_d08_evening-bed-edge-sock-adjust_r03-a.png"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d08_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d08 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D08"
        )
        self.assertEqual(d08["status"], "accepted")
        self.assertEqual(d08["revision"], "r03")
        self.assertEqual(d08["accepted_paths"], [self.ACCEPTED_PATH])
        selected = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"], review["status"])
            == ("D08", "r03", "accepted")
        ]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["candidate_id"], "d08-r03-a")
        self.assertEqual(selected[0]["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected[0]["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d08_r03_linkage_matches_akari_selection(self):
        self.assert_live_d08_selection()

    def test_live_d08_r03_linkage_allows_all_local_d08_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d08_candidates(path: Path) -> bool:
            if "source/candidates/d08" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d08_candidates(path: Path) -> bool:
            if "source/candidates/d08" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d08_candidates(path: Path) -> bytes:
            if "source/candidates/d08" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d08_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d08_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d08_candidates),
        ):
            try:
                self.assert_live_d08_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D08 candidate: {error}")


class D09R01LifecycleTests(unittest.TestCase):
    SELECTED_SHA256 = (
        "489f1a7117b8a7e27edbe1fb1cd1405c029b551676c00c57caf13f19d2344657"
    )
    ACCEPTED_PATH = (
        "accepted/daily/evening/"
        "akari-v1.2_d09_evening-phone-sleepy-bed-sit_r01.png"
    )
    SOURCE_PATH = (
        "source/candidates/d09/r01/"
        "akari-v1.2_d09_evening-phone-sleepy-bed-sit_r01-a.png"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d09_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d09 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D09"
        )
        self.assertEqual(d09["status"], "accepted")
        self.assertEqual(d09["revision"], "r01")
        self.assertEqual(d09["accepted_paths"], [self.ACCEPTED_PATH])
        selected = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"], review["status"])
            == ("D09", "r01", "accepted")
        ]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["candidate_id"], "d09-r01-a")
        self.assertEqual(selected[0]["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected[0]["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d09_r01_linkage_matches_akari_selection(self):
        self.assert_live_d09_selection()

    def test_live_d09_r01_linkage_allows_all_local_d09_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d09_candidates(path: Path) -> bool:
            if "source/candidates/d09" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d09_candidates(path: Path) -> bool:
            if "source/candidates/d09" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d09_candidates(path: Path) -> bytes:
            if "source/candidates/d09" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d09_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d09_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d09_candidates),
        ):
            try:
                self.assert_live_d09_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D09 candidate: {error}")


class D10R01LifecycleTests(unittest.TestCase):
    SELECTED_SHA256 = (
        "6197d29399f21e98f43e237d53fbb999eabfd64dcc71c0ecdbefe2c6402c4769"
    )
    ACCEPTED_PATH = (
        "accepted/daily/evening/"
        "akari-v1.2_d10_evening-rug-side-rest_r01.png"
    )
    SOURCE_PATH = (
        "source/candidates/d10/r01/"
        "akari-v1.2_d10_evening-rug-side-rest_r01-a.png"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d10_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d10 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D10"
        )
        self.assertEqual(d10["status"], "accepted")
        self.assertEqual(d10["revision"], "r01")
        self.assertEqual(d10["accepted_paths"], [self.ACCEPTED_PATH])
        selected = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"], review["status"])
            == ("D10", "r01", "accepted")
        ]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["candidate_id"], "d10-r01-a")
        self.assertEqual(selected[0]["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected[0]["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d10_r01_linkage_matches_akari_selection(self):
        self.assert_live_d10_selection()

    def test_live_d10_r01_linkage_allows_all_local_d10_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d10_candidates(path: Path) -> bool:
            if "source/candidates/d10" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d10_candidates(path: Path) -> bool:
            if "source/candidates/d10" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d10_candidates(path: Path) -> bytes:
            if "source/candidates/d10" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d10_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d10_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d10_candidates),
        ):
            try:
                self.assert_live_d10_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D10 candidate: {error}")

class D11R02LifecycleTests(unittest.TestCase):
    ACCEPTED_PATH = (
        "accepted/daily/life/akari-v1.2_d11_life-laundry-fold_r02.png"
    )
    SOURCE_PATH = (
        "source/candidates/d11/r02/"
        "akari-v1.2_d11_life-laundry-fold_r02-b.png"
    )
    SELECTED_SHA256 = (
        "ab9f4a7ac3e61f8550f0d6426b2891b0363f6da11049a8daade74df157703832"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d11_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )

        d11 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D11"
        )
        self.assertEqual(d11["status"], "accepted")
        self.assertEqual(d11["revision"], "r02")
        self.assertEqual(d11["accepted_paths"], [self.ACCEPTED_PATH])
        d11_reviews = [
            review
            for review in self.review_log["reviews"]
            if review["asset_id"] == "D11"
        ]
        self.assertEqual(
            [
                (review["revision"], review["candidate_id"], review["status"])
                for review in d11_reviews
            ],
            [
                ("r01", "d11-r01-a", "rejected"),
                ("r01", "d11-r01-b", "rejected"),
                ("r02", "d11-r02-a", "rejected"),
                ("r02", "d11-r02-b", "accepted"),
            ],
        )
        selected = d11_reviews[-1]
        self.assertEqual(selected["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d11_r02_linkage_matches_akari_selection(self):
        self.assert_live_d11_selection()

    def test_live_d11_r02_linkage_allows_all_local_d11_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d11_candidates(path: Path) -> bool:
            if "source/candidates/d11" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d11_candidates(path: Path) -> bool:
            if "source/candidates/d11" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d11_candidates(path: Path) -> bytes:
            if "source/candidates/d11" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d11_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d11_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d11_candidates),
        ):
            try:
                self.assert_live_d11_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D11 candidate: {error}")


class D12R01LifecycleTests(unittest.TestCase):
    ACCEPTED_PATH = (
        "accepted/daily/life/akari-v1.2_d12_life-fridge-open_r01.png"
    )
    SOURCE_PATH = (
        "source/candidates/d12/r01/"
        "akari-v1.2_d12_life-fridge-open_r01-a.png"
    )
    SELECTED_SHA256 = (
        "1ebb3da5e17d31bc6b9c38c8b2a8495c142d8afcbee87f4a01e36f1d4d082f85"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d12_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )
        d12 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D12"
        )
        self.assertEqual(d12["status"], "accepted")
        self.assertEqual(d12["revision"], "r01")
        self.assertEqual(d12["accepted_paths"], [self.ACCEPTED_PATH])
        d12_reviews = [
            review
            for review in self.review_log["reviews"]
            if review["asset_id"] == "D12"
        ]
        self.assertEqual(
            [
                (review["candidate_id"], review["status"])
                for review in d12_reviews
            ],
            [("d12-r01-a", "accepted"), ("d12-r01-b", "rejected")],
        )
        selected = d12_reviews[0]
        self.assertEqual(selected["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d12_r01_linkage_matches_akari_selection(self):
        self.assert_live_d12_selection()

    def test_live_d12_r01_linkage_allows_all_local_d12_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d12_candidates(path: Path) -> bool:
            if "source/candidates/d12" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d12_candidates(path: Path) -> bool:
            if "source/candidates/d12" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d12_candidates(path: Path) -> bytes:
            if "source/candidates/d12" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d12_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d12_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d12_candidates),
        ):
            try:
                self.assert_live_d12_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D12 candidate: {error}")


class D13R02LifecycleTests(unittest.TestCase):
    ACCEPTED_PATH = (
        "accepted/daily/life/akari-v1.2_d13_life-charger-search_r02.png"
    )
    SOURCE_PATH = (
        "source/candidates/d13/r02/"
        "akari-v1.2_d13_life-charger-search_r02-b.png"
    )
    SELECTED_SHA256 = (
        "76e0328057e1b118e53999ae98ba3e46248e182ca26e69ad42720a0c585d8c8c"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d13_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )
        d13 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D13"
        )
        self.assertEqual(d13["status"], "accepted")
        self.assertEqual(d13["revision"], "r02")
        self.assertEqual(d13["accepted_paths"], [self.ACCEPTED_PATH])
        d13_reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("D13", "r02")
        ]
        self.assertEqual(
            [
                (review["candidate_id"], review["status"])
                for review in d13_reviews
            ],
            [("d13-r02-a", "rejected"), ("d13-r02-b", "accepted")],
        )
        selected = d13_reviews[1]
        self.assertEqual(selected["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d13_r02_linkage_matches_akari_selection(self):
        self.assert_live_d13_selection()

    def test_live_d13_r02_linkage_allows_all_local_d13_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d13_candidates(path: Path) -> bool:
            if "source/candidates/d13" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d13_candidates(path: Path) -> bool:
            if "source/candidates/d13" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d13_candidates(path: Path) -> bytes:
            if "source/candidates/d13" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d13_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d13_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d13_candidates),
        ):
            try:
                self.assert_live_d13_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D13 candidate: {error}")


class D14R02LifecycleTests(unittest.TestCase):
    ACCEPTED_PATH = (
        "accepted/daily/life/akari-v1.2_d14_life-bag-unpack_r02.png"
    )
    SOURCE_PATH = (
        "source/candidates/d14/r02/"
        "akari-v1.2_d14_life-bag-unpack_r02-b.png"
    )
    SELECTED_SHA256 = (
        "7bfd02acf39f3c80390e22d1b5867775f0911b019ba380bf0d31e6b9d6e0a880"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d14_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )
        d14 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D14"
        )
        self.assertEqual(d14["status"], "accepted")
        self.assertEqual(d14["revision"], "r02")
        self.assertEqual(d14["accepted_paths"], [self.ACCEPTED_PATH])
        d14_reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("D14", "r02")
        ]
        self.assertEqual(
            [
                (review["candidate_id"], review["status"])
                for review in d14_reviews
            ],
            [("d14-r02-a", "rejected"), ("d14-r02-b", "accepted")],
        )
        selected = d14_reviews[1]
        self.assertEqual(selected["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d14_r02_linkage_matches_akari_selection(self):
        self.assert_live_d14_selection()

    def test_live_d14_r02_linkage_allows_all_local_d14_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d14_candidates(path: Path) -> bool:
            if "source/candidates/d14" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d14_candidates(path: Path) -> bool:
            if "source/candidates/d14" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d14_candidates(path: Path) -> bytes:
            if "source/candidates/d14" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d14_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d14_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d14_candidates),
        ):
            try:
                self.assert_live_d14_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D14 candidate: {error}")


class D15R01LifecycleTests(unittest.TestCase):
    ACCEPTED_PATH = (
        "accepted/daily/life/akari-v1.2_d15_life-pc-posture-break_r01.png"
    )
    SOURCE_PATH = (
        "source/candidates/d15/r01/"
        "akari-v1.2_d15_life-pc-posture-break_r01-a.png"
    )
    SELECTED_SHA256 = (
        "138a2a0afdb237efc5ed6796b0ff2243ecf48402ab237f202130d8f7fccf797e"
    )

    @classmethod
    def setUpClass(cls):
        cls.assets = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/assets.yaml").read_text(encoding="utf-8")
        )
        request_root = PACKAGE_ROOT / "manifest/generation-requests"
        cls.requests = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(request_root.glob("*.yaml"))
        ]
        cls.review_log = yaml.safe_load(
            (PACKAGE_ROOT / "manifest/review-log.yaml").read_text(
                encoding="utf-8"
            )
        )

    def assert_live_d15_selection(self) -> None:
        validate_assets(self.assets, PACKAGE_ROOT)
        validate_review_log(self.review_log)
        validate_lifecycle_linkage(
            self.assets,
            self.requests,
            self.review_log,
            PACKAGE_ROOT,
        )
        d15 = next(
            asset for asset in self.assets["assets"] if asset["asset_id"] == "D15"
        )
        self.assertEqual(d15["status"], "accepted")
        self.assertEqual(d15["revision"], "r01")
        self.assertEqual(d15["accepted_paths"], [self.ACCEPTED_PATH])
        d15_reviews = [
            review
            for review in self.review_log["reviews"]
            if (review["asset_id"], review["revision"]) == ("D15", "r01")
        ]
        self.assertEqual(
            [
                (review["candidate_id"], review["status"])
                for review in d15_reviews
            ],
            [("d15-r01-a", "accepted"), ("d15-r01-b", "rejected")],
        )
        selected = d15_reviews[0]
        self.assertEqual(selected["source_paths"], [self.SOURCE_PATH])
        self.assertEqual(selected["source_sha256s"], [self.SELECTED_SHA256])
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE_ROOT / self.ACCEPTED_PATH).read_bytes()
            ).hexdigest(),
            self.SELECTED_SHA256,
        )

    def test_live_d15_r01_linkage_matches_akari_selection(self):
        self.assert_live_d15_selection()

    def test_live_d15_r01_linkage_allows_all_local_d15_candidates_absent(self):
        original_is_file = Path.is_file
        original_exists = Path.exists
        original_read_bytes = Path.read_bytes

        def is_file_without_d15_candidates(path: Path) -> bool:
            if "source/candidates/d15" in path.as_posix():
                return False
            return original_is_file(path)

        def exists_without_d15_candidates(path: Path) -> bool:
            if "source/candidates/d15" in path.as_posix():
                return False
            return original_exists(path)

        def read_without_d15_candidates(path: Path) -> bytes:
            if "source/candidates/d15" in path.as_posix():
                raise FileNotFoundError(path)
            return original_read_bytes(path)

        with (
            mock.patch.object(Path, "is_file", new=is_file_without_d15_candidates),
            mock.patch.object(Path, "exists", new=exists_without_d15_candidates),
            mock.patch.object(Path, "read_bytes", new=read_without_d15_candidates),
        ):
            try:
                self.assert_live_d15_selection()
            except FileNotFoundError as error:
                self.fail(f"live linkage required local D15 candidate: {error}")


if __name__ == "__main__":
    unittest.main()

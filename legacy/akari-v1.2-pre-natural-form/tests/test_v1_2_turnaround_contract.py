import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.build_v1_2_motion_handoff import build_handoff


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-turnaround"
IDENTITY_LOCK = MANIFEST_DIR / "identity-lock.json"
ANGLE_SLOTS = MANIFEST_DIR / "angle-slots.json"
GENERATION_REQUESTS = MANIFEST_DIR / "generation-requests.json"
ACCEPTED_ANGLES = MANIFEST_DIR / "accepted-angles.json"
FINAL_REVIEW = (
    ROOT / "evidence/v1-2-turnaround/reviews/final-eight-view-review.json"
)
PHASE_2_HANDOFF = ROOT / "source/manifests/v1-2-motion/phase-2-handoff.json"
SELECTION = ROOT / "source/manifests/v1-2-face-hair/accepted-selection.json"
FACE_ASSET = (
    ROOT / "source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp"
)
COLLECTION_ID = "akari-v1.2-canonical-turnaround"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AkariV12TurnaroundContractTest(unittest.TestCase):
    def test_face_hair_prerequisite_is_explicitly_accepted(self):
        self.assertTrue(SELECTION.is_file())
        selection = load_json(SELECTION)
        self.assertEqual("accepted", selection["decision"])
        self.assertEqual(
            "source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp",
            selection["accepted_asset"],
        )
        self.assertTrue(FACE_ASSET.is_file())
        self.assertEqual(
            selection["accepted_asset_sha256"],
            hashlib.sha256(FACE_ASSET.read_bytes()).hexdigest(),
        )
        self.assertTrue(selection["identity_rules"])

    def test_identity_lock_records_exact_sources(self):
        manifest = load_json(IDENTITY_LOCK)
        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual("accepted", manifest["prerequisite"]["required_status"])
        selection = load_json(SELECTION)
        self.assertEqual(
            hashlib.sha256(SELECTION.read_bytes()).hexdigest(),
            manifest["prerequisite"]["selection_manifest_sha256"],
        )
        self.assertEqual(
            selection["accepted_asset_sha256"],
            manifest["prerequisite"]["accepted_asset_sha256"],
        )
        self.assertEqual(selection["identity_rules"], manifest["identity_rules"])
        self.assertEqual(
            (1024, 1536),
            tuple(manifest["canvas"][key] for key in ("width", "height")),
        )
        for entry in manifest["reference_inputs"]:
            self.assertTrue((ROOT / entry["path"]).is_file(), entry["path"])

    def test_working_outputs_are_ignored_but_reviews_are_trackable(self):
        ignored = [
            "source/generated/v1-2-turnaround/example.png",
            "evidence/v1-2-turnaround/contact-sheets/example.webp",
        ]
        tracked = "evidence/v1-2-turnaround/reviews/example.json"
        for path in ignored:
            result = subprocess.run(
                ["git", "check-ignore", path],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
        result = subprocess.run(
            ["git", "check-ignore", tracked],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)

    def test_state_manifests_cover_the_completed_turnaround(self):
        requests = load_json(GENERATION_REQUESTS)
        accepted = load_json(ACCEPTED_ANGLES)
        canonical_slots = [
            slot["slug"] for slot in load_json(ANGLE_SLOTS)["slots"]
        ]
        self.assertEqual(COLLECTION_ID, requests["collection_id"])
        self.assertEqual(set(canonical_slots), set(requests["active_batches"]))
        self.assertTrue(requests["requests"])
        self.assertEqual(COLLECTION_ID, accepted["collection_id"])
        self.assertEqual(
            canonical_slots,
            [record["slot"] for record in accepted["accepted_angles"]],
        )

    def test_angle_slots_are_complete_and_canonical(self):
        manifest = load_json(ANGLE_SLOTS)
        slots = manifest["slots"]
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual(
            [
                "front",
                "character-left-front-three-quarter",
                "character-left-profile",
                "character-left-rear-three-quarter",
                "back",
                "character-right-rear-three-quarter",
                "character-right-profile",
                "character-right-front-three-quarter",
            ],
            [slot["slug"] for slot in slots],
        )
        self.assertEqual(list(range(1, 9)), [slot["angle_order"] for slot in slots])
        self.assertEqual(8, len({slot["azimuth_degrees"] for slot in slots}))

    def test_angle_dependencies_form_two_branches_that_converge_at_back(self):
        slots = {slot["slug"]: slot for slot in load_json(ANGLE_SLOTS)["slots"]}
        self.assertEqual([], slots["front"]["upstream_slots"])
        self.assertEqual(
            ["front"],
            slots["character-left-front-three-quarter"]["upstream_slots"],
        )
        self.assertEqual(
            ["front", "character-left-front-three-quarter"],
            slots["character-left-profile"]["upstream_slots"],
        )
        self.assertEqual(
            [
                "front",
                "character-left-front-three-quarter",
                "character-left-profile",
            ],
            slots["character-left-rear-three-quarter"]["upstream_slots"],
        )
        self.assertEqual(
            ["front"],
            slots["character-right-front-three-quarter"]["upstream_slots"],
        )
        self.assertEqual(
            ["front", "character-right-front-three-quarter"],
            slots["character-right-profile"]["upstream_slots"],
        )
        self.assertEqual(
            [
                "front",
                "character-right-front-three-quarter",
                "character-right-profile",
            ],
            slots["character-right-rear-three-quarter"]["upstream_slots"],
        )
        self.assertEqual(
            [
                "front",
                "character-left-rear-three-quarter",
                "character-right-rear-three-quarter",
            ],
            slots["back"]["upstream_slots"],
        )

    def test_slot_orientation_and_hair_ornament_rules_are_explicit(self):
        allowed_sides = {"center", "character_left", "character_right"}
        allowed_visibility = {"prominent", "visible", "partial", "occluded"}
        for slot in load_json(ANGLE_SLOTS)["slots"]:
            with self.subTest(slot=slot["slug"]):
                self.assertIn(slot["side"], allowed_sides)
                self.assertIn(
                    slot["hair_ornament_visibility"],
                    allowed_visibility,
                )
                self.assertEqual(3, slot["candidate_count"])
                self.assertEqual("neutral_standing", slot["pose"])
                self.assertTrue(slot["japanese_title"])

    def test_package_scripts_expose_turnaround_request_builder(self):
        scripts = load_json(ROOT / "package.json")["scripts"]
        self.assertEqual(
            (
                "uv run python -m "
                "scripts.build_v1_2_turnaround_generation_requests"
            ),
            scripts["build:v1-2-turnaround:requests"],
        )

    def test_request_builder_cli_can_import_shared_helpers(self):
        result = subprocess.run(
            [
                "npm",
                "run",
                "build:v1-2-turnaround:requests",
                "--",
                "--help",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--revision", result.stdout)

    def test_package_scripts_expose_turnaround_contact_sheet_builder(self):
        scripts = load_json(ROOT / "package.json")["scripts"]
        self.assertEqual(
            "uv run python -m scripts.build_v1_2_turnaround_contact_sheet",
            scripts["build:v1-2-turnaround:contact-sheet"],
        )

    def test_package_scripts_expose_turnaround_promotion(self):
        scripts = load_json(ROOT / "package.json")["scripts"]
        self.assertEqual(
            "uv run python -m scripts.promote_v1_2_turnaround_candidate",
            scripts["promote:v1-2-turnaround"],
        )

    def test_final_review_accepts_all_eight_canonical_slots(self):
        review = load_json(FINAL_REVIEW)
        slots = load_json(ANGLE_SLOTS)["slots"]
        self.assertEqual("accepted", review["decision"])
        self.assertEqual("approved", review["user_decision"])
        self.assertEqual(
            [slot["slug"] for slot in slots],
            review["accepted_slots"],
        )
        self.assertEqual(
            hashlib.sha256(ACCEPTED_ANGLES.read_bytes()).hexdigest(),
            review["source_manifest_sha256"],
        )
        self.assertEqual({"pass"}, set(review["gate_summary"].values()))
        self.assertEqual(
            "ready_for_contract_build",
            review["motion_phase_handoff"]["status"],
        )

    def test_phase_2_handoff_has_exactly_three_turnaround_dependent_slots(self):
        accepted = load_json(ACCEPTED_ANGLES)["accepted_angles"]
        handoff = load_json(PHASE_2_HANDOFF)
        self.assertEqual(
            ["walking", "seated", "turning"],
            [slot["slug"] for slot in handoff["motion_slots"]],
        )
        expected_slots = [record["slot"] for record in accepted]
        expected_inputs = [
            {
                "slot": record["slot"],
                "accepted_path": record["accepted_path"],
                "sha256": record["sha256"],
            }
            for record in accepted
        ]
        self.assertEqual(expected_inputs, handoff["turnaround_inputs"])
        self.assertEqual(
            hashlib.sha256(ACCEPTED_ANGLES.read_bytes()).hexdigest(),
            handoff["source_turnaround_manifest_sha256"],
        )
        for slot in handoff["motion_slots"]:
            self.assertTrue(slot["requires_complete_turnaround"])
            self.assertEqual(
                expected_slots,
                slot["required_turnaround_slots"],
            )
            self.assertEqual(1, slot["deliverable_count"])

    def test_motion_handoff_rejects_missing_or_tampered_assets(self):
        accepted = load_json(ACCEPTED_ANGLES)
        review = load_json(FINAL_REVIEW)
        accepted_sha = hashlib.sha256(ACCEPTED_ANGLES.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "missing accepted asset"):
                build_handoff(
                    accepted,
                    review,
                    accepted_sha,
                    project_root=Path(temporary),
                )
        tampered = copy.deepcopy(accepted)
        tampered["accepted_angles"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            build_handoff(tampered, review, accepted_sha, project_root=ROOT)
        substituted = copy.deepcopy(accepted)
        substituted["accepted_angles"][0]["accepted_path"] = (
            substituted["accepted_angles"][1]["accepted_path"]
        )
        with self.assertRaisesRegex(ValueError, "unexpected accepted path"):
            build_handoff(
                substituted,
                review,
                accepted_sha,
                project_root=ROOT,
            )

    def test_motion_handoff_rejects_invalid_final_approval(self):
        accepted = load_json(ACCEPTED_ANGLES)
        review = load_json(FINAL_REVIEW)
        accepted_sha = hashlib.sha256(ACCEPTED_ANGLES.read_bytes()).hexdigest()
        invalid_values = {
            "rejected review decision": ("decision", "rejected"),
            "rejected user decision": ("user_decision", "rejected"),
            "failed gate": ("gate_summary.quality", "fail"),
            "wrong source manifest": ("source_manifest", "tmp/other.json"),
            "stale manifest": ("source_manifest_sha256", "0" * 64),
            "handoff not ready": ("motion_phase_handoff.status", "blocked"),
        }
        for label, (field, value) in invalid_values.items():
            with self.subTest(label=label):
                invalid = copy.deepcopy(review)
                target = invalid
                parts = field.split(".")
                for part in parts[:-1]:
                    target = target[part]
                target[parts[-1]] = value
                with self.assertRaises(ValueError):
                    build_handoff(
                        accepted,
                        invalid,
                        accepted_sha,
                        project_root=ROOT,
                    )

    def test_motion_handoff_reports_override_provenance(self):
        accepted = load_json(ACCEPTED_ANGLES)
        review = load_json(FINAL_REVIEW)
        accepted_sha = hashlib.sha256(ACCEPTED_ANGLES.read_bytes()).hexdigest()
        review["source_manifest"] = "tmp/custom-accepted.json"
        handoff = build_handoff(
            accepted,
            review,
            accepted_sha,
            project_root=ROOT,
            source_turnaround_manifest="tmp/custom-accepted.json",
            source_final_review="tmp/custom-final-review.json",
        )
        self.assertEqual(
            "tmp/custom-accepted.json",
            handoff["source_turnaround_manifest"],
        )
        self.assertEqual(
            "tmp/custom-final-review.json",
            handoff["source_final_review"],
        )

    def test_motion_handoff_cli_reports_override_provenance(self):
        accepted = load_json(ACCEPTED_ANGLES)
        review = load_json(FINAL_REVIEW)
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            accepted_path = temporary_root / "accepted.json"
            review_path = temporary_root / "review.json"
            output_path = temporary_root / "handoff.json"
            accepted_path.write_text(
                json.dumps(accepted, indent=2) + "\n",
                encoding="utf-8",
            )
            review["source_manifest"] = accepted_path.as_posix()
            review["source_manifest_sha256"] = hashlib.sha256(
                accepted_path.read_bytes()
            ).hexdigest()
            review_path.write_text(
                json.dumps(review, indent=2) + "\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-m",
                    "scripts.build_v1_2_motion_handoff",
                    "--accepted",
                    accepted_path.as_posix(),
                    "--final-review",
                    review_path.as_posix(),
                    "--output",
                    output_path.as_posix(),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            handoff = load_json(output_path)
            self.assertEqual(
                accepted_path.as_posix(),
                handoff["source_turnaround_manifest"],
            )
            self.assertEqual(
                review_path.as_posix(),
                handoff["source_final_review"],
            )

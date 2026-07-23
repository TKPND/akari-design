import copy
from contextlib import redirect_stderr
import importlib.util
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageDraw
import yaml

from scripts import audit_v1_2_c03_landmarks as audit
from scripts.validate_akari_v1_2_natural_form import C03_R02_FRAMING_CONTRACT


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
BACKGROUND = "#f1f2f1"


def make_figure(
    path: Path,
    head: int,
    sole: int,
    size: tuple[int, int] = (1024, 1536),
) -> None:
    image = Image.new("RGB", size, BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rectangle((320, head, 703, sole), fill="#202124")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def make_request(root: Path) -> Path:
    make_figure(root / "anchors/c01.png", 65, 1450)
    make_figure(root / "anchors/c02.png", 65, 1463)
    candidates = []
    for variant in ("a", "b", "c"):
        outputs = []
        for view in ("hairpin-side-45", "non-hairpin-side-45"):
            target = Path("candidates") / f"{variant}-{view}.png"
            make_figure(root / target, 65, 1456)
            outputs.append({"view": view, "target_path": target.as_posix()})
        candidates.append({"variant": variant, "outputs": outputs})
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump(
            {
                "references": [
                    {
                        "role": "accepted_c01_front_stance",
                        "path": "anchors/c01.png",
                    },
                    {
                        "role": "accepted_c02_back_stance",
                        "path": "anchors/c02.png",
                    },
                ],
                "framing_contract": copy.deepcopy(C03_R02_FRAMING_CONTRACT),
                "candidates": candidates,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return request


class C03LandmarkAuditModuleTests(unittest.TestCase):
    def test_landmark_audit_module_exists(self):
        self.assertIsNotNone(
            importlib.util.find_spec("scripts.audit_v1_2_c03_landmarks")
        )

    def test_landmark_audit_exposes_the_focused_interface(self):
        for name in (
            "AuditError",
            "Measurement",
            "TrimGeometry",
            "audit_request",
            "main",
            "measure_image",
            "measurement_errors",
            "parse_geometry",
        ):
            with self.subTest(name=name):
                self.assertTrue(hasattr(audit, name), name)


class C03GeometryTests(unittest.TestCase):
    def test_parse_geometry_uses_y_plus_height_minus_one_for_sole(self):
        geometry = audit.parse_geometry("423x1386+300+65")
        self.assertEqual(
            geometry,
            audit.TrimGeometry(width=423, height=1386, x=300, y=65),
        )
        measurement = audit.Measurement(1024, 1536, geometry)
        self.assertEqual(measurement.head_top_y, 65)
        self.assertEqual(measurement.sole_y, 1450)

    def test_parse_geometry_rejects_malformed_and_empty_foreground(self):
        for value in ("not-geometry", "0x0+1024+1536"):
            with self.subTest(value=value):
                with self.assertRaises(audit.AuditError):
                    audit.parse_geometry(value)

    def test_30_pixels_passes_and_31_pixels_fails(self):
        contract = copy.deepcopy(C03_R02_FRAMING_CONTRACT)
        anchors = contract["anchors"]
        at_limit = audit.Measurement(
            1024,
            1536,
            audit.TrimGeometry(400, 1362, 300, 95),
        )
        over_limit = audit.Measurement(
            1024,
            1536,
            audit.TrimGeometry(400, 1361, 300, 96),
        )
        self.assertEqual(audit.measurement_errors(at_limit, contract, anchors), [])
        self.assertTrue(
            any(
                "31 px" in message
                for message in audit.measurement_errors(
                    over_limit,
                    contract,
                    anchors,
                )
            )
        )

    def test_intersection_endpoints_are_inclusive(self):
        contract = copy.deepcopy(C03_R02_FRAMING_CONTRACT)
        anchors = contract["anchors"]
        lower = audit.Measurement(
            1024,
            1536,
            audit.TrimGeometry(400, 1399, 300, 35),
        )
        self.assertEqual(lower.head_top_y, 35)
        self.assertEqual(lower.sole_y, 1433)
        self.assertEqual(audit.measurement_errors(lower, contract, anchors), [])
        outside = audit.Measurement(
            1024,
            1536,
            audit.TrimGeometry(400, 1399, 300, 34),
        )
        self.assertTrue(
            any(
                "required intersection" in message
                for message in audit.measurement_errors(
                    outside,
                    contract,
                    anchors,
                )
            )
        )


class C03LandmarkAuditTests(unittest.TestCase):
    def test_committed_anchors_match_the_contract(self):
        c01 = audit.measure_image(
            PACKAGE_ROOT
            / "accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
            6,
        )
        c02 = audit.measure_image(
            PACKAGE_ROOT
            / "accepted/core/standing/"
            "akari-v1.2_c02_back-natural-stance_r01.png",
            6,
        )
        self.assertEqual((c01.head_top_y, c01.sole_y), (65, 1450))
        self.assertEqual((c02.head_top_y, c02.sole_y), (65, 1463))

    def test_audit_reports_all_six_candidates_in_request_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            lines = audit.audit_request(make_request(root), root)
            candidate_lines = [
                line for line in lines if line.startswith("PASS candidates/")
            ]
            self.assertEqual(
                [
                    line.split(":", 1)[0].removeprefix("PASS ")
                    for line in candidate_lines
                ],
                [
                    f"candidates/{variant}-{view}.png"
                    for variant in ("a", "b", "c")
                    for view in ("hairpin-side-45", "non-hairpin-side-45")
                ],
            )

    def test_one_out_of_range_member_makes_cli_nonzero_and_names_the_file(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            make_figure(
                root / "candidates/b-non-hairpin-side-45.png",
                96,
                1456,
            )
            stderr = StringIO()
            with redirect_stderr(stderr):
                status = audit.main(
                    [
                        "--request",
                        str(request),
                        "--package-root",
                        str(root),
                    ]
                )
            self.assertEqual(status, 1)
            self.assertIn("b-non-hairpin-side-45.png", stderr.getvalue())
            self.assertIn("31 px", stderr.getvalue())

    def test_wrong_canvas_and_missing_foreground_fail_and_name_both_files(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            make_figure(
                root / "candidates/a-hairpin-side-45.png",
                65,
                1456,
                (1000, 1536),
            )
            Image.new("RGB", (1024, 1536), BACKGROUND).save(
                root / "candidates/c-non-hairpin-side-45.png"
            )
            with self.assertRaises(audit.AuditError) as caught:
                audit.audit_request(request, root)
            message = str(caught.exception)
            self.assertIn("a-hairpin-side-45.png", message)
            self.assertIn("expected 1024x1536", message)
            self.assertIn("c-non-hairpin-side-45.png", message)
            self.assertIn("missing foreground", message)

    def test_changed_contract_and_anchor_measurement_stop_the_audit(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["framing_contract"]["maximum_displacement"][
                "integer_pixels"
            ] = 31
            request.write_text(
                yaml.safe_dump(data, sort_keys=False),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(audit.AuditError, "exact C03 r02"):
                audit.audit_request(request, root)

            request = make_request(root)
            make_figure(root / "anchors/c02.png", 65, 1462)
            with self.assertRaisesRegex(audit.AuditError, "anchor C02 r01"):
                audit.audit_request(request, root)


if __name__ == "__main__":
    unittest.main()

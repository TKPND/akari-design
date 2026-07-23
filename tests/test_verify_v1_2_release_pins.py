import hashlib
from pathlib import Path
import tempfile
import unittest

from scripts.verify_v1_2_release_pins import PinError, verify_release_pins


PDF_PATH = "akari-v1.2/release/akari-v1.2-core-settings.pdf"
CHECKSUM_PATH = "akari-v1.2/release/checksums.txt"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


class VerifyV12ReleasePinsTests(unittest.TestCase):
    def write_artifacts(
        self,
        root: Path,
        pdf_payload: bytes = b"closed-release-pdf",
        checksum_payload: bytes = b"closed-release-checksum",
    ) -> dict[str, str]:
        pdf = root / PDF_PATH
        checksum = root / CHECKSUM_PATH
        pdf.parent.mkdir(parents=True)
        pdf.write_bytes(pdf_payload)
        checksum.write_bytes(checksum_payload)
        return {
            PDF_PATH: digest(b"closed-release-pdf"),
            CHECKSUM_PATH: digest(b"closed-release-checksum"),
        }

    def test_accepts_artifacts_matching_every_pin(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pins = self.write_artifacts(root)
            verify_release_pins(root, pins)

    def test_reports_single_and_simultaneous_drift(self):
        cases = {
            "pdf only": (b"changed-pdf", b"closed-release-checksum", [PDF_PATH]),
            "checksum only": (
                b"closed-release-pdf",
                b"changed-checksum",
                [CHECKSUM_PATH],
            ),
            "both": (
                b"changed-pdf",
                b"changed-checksum",
                [PDF_PATH, CHECKSUM_PATH],
            ),
        }
        for name, (pdf_payload, checksum_payload, changed_paths) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                pins = self.write_artifacts(root, pdf_payload, checksum_payload)
                with self.assertRaises(PinError) as raised:
                    verify_release_pins(root, pins)
                for path in changed_paths:
                    self.assertIn(path, str(raised.exception))

    def test_reports_every_missing_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pins = {
                PDF_PATH: digest(b"closed-release-pdf"),
                CHECKSUM_PATH: digest(b"closed-release-checksum"),
            }
            with self.assertRaises(PinError) as raised:
                verify_release_pins(root, pins)
            self.assertIn(PDF_PATH, str(raised.exception))
            self.assertIn(CHECKSUM_PATH, str(raised.exception))


if __name__ == "__main__":
    unittest.main()

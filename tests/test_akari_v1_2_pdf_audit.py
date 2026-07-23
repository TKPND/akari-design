import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts/audit_akari_v1_2_pdf.py"


def load_audit():
    spec = importlib.util.spec_from_file_location("audit_akari_v1_2_pdf", AUDIT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AkariV12PdfAuditTests(unittest.TestCase):
    def setUp(self):
        self.audit = load_audit()

    def test_pdfinfo_accepts_14_page_16_by_9_document(self):
        self.audit.require_pdfinfo_contract(
            "Pages:           14\nPage size:       960 x 540 pts\n"
        )

    def test_pdfinfo_rejects_wrong_page_count(self):
        with self.assertRaisesRegex(self.audit.AuditError, "14 pages"):
            self.audit.require_pdfinfo_contract(
                "Pages:           13\nPage size:       960 x 540 pts\n"
            )

    def test_pdfinfo_rejects_non_16_by_9_page(self):
        with self.assertRaisesRegex(self.audit.AuditError, "16:9"):
            self.audit.require_pdfinfo_contract(
                "Pages:           14\nPage size:       595 x 842 pts\n"
            )

    def test_font_table_requires_embedded_unicode_font(self):
        valid = "\n".join(
            [
                "name type encoding emb sub uni object ID",
                "----------------------------------------",
                "Inter Type 3 Custom yes yes yes 4 0",
            ]
        )
        self.audit.require_font_table(valid)

        for row in (
            "Inter Type 3 Custom no yes yes 4 0",
            "Inter Type 3 Custom yes yes no 4 0",
        ):
            with self.subTest(row=row):
                with self.assertRaisesRegex(self.audit.AuditError, "embedded Unicode"):
                    self.audit.require_font_table(
                        "name type encoding emb sub uni object ID\n"
                        "----------------------------------------\n"
                        f"{row}\n"
                    )

    def test_searchable_text_requires_every_release_term(self):
        complete = "\n".join(self.audit.REQUIRED_TEXT)
        self.audit.require_searchable_text(complete)

        missing_title = complete.replace("Floor Sitting Anatomy Notes", "")
        with self.assertRaisesRegex(
            self.audit.AuditError, "Floor Sitting Anatomy Notes"
        ):
            self.audit.require_searchable_text(missing_title)

    def test_checksum_contract_accepts_exact_gnu_line(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            release = Path(temp_dir)
            pdf = release / "akari-v1.2-core-settings.pdf"
            checksum = release / "checksums.txt"
            payload = b"natural-form-pdf"
            pdf.write_bytes(payload)
            digest = hashlib.sha256(payload).hexdigest()
            checksum.write_text(
                f"{digest}  akari-v1.2-core-settings.pdf\n",
                encoding="utf-8",
            )

            self.audit.require_checksum_contract(pdf, checksum)

    def test_checksum_contract_rejects_malformed_or_wrong_digest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            release = Path(temp_dir)
            pdf = release / "akari-v1.2-core-settings.pdf"
            checksum = release / "checksums.txt"
            pdf.write_bytes(b"natural-form-pdf")
            digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
            invalid_values = (
                f"{digest.upper()}  akari-v1.2-core-settings.pdf\n",
                f"{digest} akari-v1.2-core-settings.pdf\n",
                f"{digest}  wrong.pdf\n",
                f"{digest}  akari-v1.2-core-settings.pdf",
                f"{digest}  akari-v1.2-core-settings.pdf\nextra\n",
                f"{'0' * 64}  akari-v1.2-core-settings.pdf\n",
            )

            for value in invalid_values:
                with self.subTest(value=value):
                    checksum.write_text(value, encoding="utf-8")
                    with self.assertRaises(self.audit.AuditError):
                        self.audit.require_checksum_contract(pdf, checksum)

    def test_audit_levels_select_expected_owners_and_checksum_once(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            release = Path(temp_dir)
            pdf = release / "akari-v1.2-core-settings.pdf"
            checksum = release / "checksums.txt"
            pdf.write_bytes(b"pdf")
            checksum.write_text("checksum\n", encoding="utf-8")

            expected_calls = {
                "structure": (1, 0),
                "raster": (0, 1),
                "full": (1, 1),
            }
            for level, (structure_calls, raster_calls) in expected_calls.items():
                with self.subTest(level=level), mock.patch.object(
                    self.audit, "require_checksum_contract"
                ) as checksum_contract, mock.patch.object(
                    self.audit, "audit_pdf_structure"
                ) as structure, mock.patch.object(
                    self.audit, "audit_pdf_raster"
                ) as raster:
                    self.audit.audit_release(pdf, checksum, level=level)
                    self.assertEqual(1, checksum_contract.call_count)
                    self.assertEqual(structure_calls, structure.call_count)
                    self.assertEqual(raster_calls, raster.call_count)

    def test_audit_release_rejects_unknown_level(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            release = Path(temp_dir)
            pdf = release / "akari-v1.2-core-settings.pdf"
            checksum = release / "checksums.txt"
            pdf.write_bytes(b"pdf")
            checksum.write_text("checksum\n", encoding="utf-8")
            with self.assertRaisesRegex(self.audit.AuditError, "audit level"):
                self.audit.audit_release(pdf, checksum, level="quick")

    def test_audit_release_rejects_missing_files_before_external_commands(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with self.assertRaisesRegex(self.audit.AuditError, "PDF missing"):
                self.audit.audit_release(root / "missing.pdf", root / "checksums.txt")

            pdf = root / "akari-v1.2-core-settings.pdf"
            pdf.write_bytes(b"pdf")
            with self.assertRaisesRegex(self.audit.AuditError, "checksum missing"):
                self.audit.audit_release(pdf, root / "checksums.txt")


if __name__ == "__main__":
    unittest.main()

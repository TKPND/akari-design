from pathlib import Path
import unittest

from scripts import audit_ame_no_sei_ni_shite_pdf as audit


class AmeNoSeiNiShitePdfAuditTest(unittest.TestCase):
    def test_pdfinfo_requires_eighteen_a4_landscape_pages(self):
        output = "Pages: 18\nPage size: 841.68 x 595.44 pts\n"
        audit.require_pdfinfo_contract(output)

    def test_pdfinfo_rejects_wrong_page_count(self):
        with self.assertRaisesRegex(audit.AuditError, "18 pages"):
            audit.require_pdfinfo_contract(
                "Pages: 17\nPage size: 841.68 x 595.44 pts\n"
            )

    def test_pdfinfo_rejects_non_a4_landscape_size(self):
        with self.assertRaisesRegex(audit.AuditError, "A4 landscape"):
            audit.require_pdfinfo_contract(
                "Pages: 18\nPage size: 960 x 540 pts\n"
            )

    def test_checksum_line_uses_pdf_sha(self):
        line = audit.checksum_line(Path("book.pdf"), "a" * 64)
        self.assertEqual(f"{'a' * 64}  book.pdf", line)

    def test_required_text_includes_story_extremes_and_release_id(self):
        text = "\n".join(audit.REQUIRED_TEXT)
        audit.require_searchable_text(text)
        with self.assertRaisesRegex(audit.AuditError, "searchable text missing"):
            audit.require_searchable_text(text.replace("21:08", ""))


if __name__ == "__main__":
    unittest.main()

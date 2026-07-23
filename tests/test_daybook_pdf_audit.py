import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DAYBOOK_PDF = ROOT / "scripts/audit_daybook_pdf.py"


def load_audit_daybook_pdf():
    spec = importlib.util.spec_from_file_location(
        "audit_daybook_pdf", AUDIT_DAYBOOK_PDF
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DaybookPdfAuditTest(unittest.TestCase):
    def setUp(self):
        self.audit_daybook_pdf = load_audit_daybook_pdf()

    def test_rendered_page_sort_key_orders_numeric_suffixes(self):
        pages = [
            Path("page-1.png"),
            Path("page-10.png"),
            Path("page-2.png"),
        ]

        sorted_pages = sorted(
            pages, key=self.audit_daybook_pdf.rendered_page_sort_key
        )

        self.assertEqual(
            [Path("page-1.png"), Path("page-2.png"), Path("page-10.png")],
            sorted_pages,
        )

    def test_searchable_text_normalization_is_case_insensitive(self):
        self.assertIn(
            "akari v1.1 situation daybook",
            self.audit_daybook_pdf.normalize_searchable_text(
                "AKARI V1.1 SITUATION DAYBOOK / MOOD STANDARD"
            ),
        )


if __name__ == "__main__":
    unittest.main()

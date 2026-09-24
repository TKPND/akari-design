"""Observable regression checks for the portable compositor, with real ImageMagick."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().with_name("compose.py")


def magick(*args):
    return subprocess.check_output(["magick", *map(str, args)])


class ComposeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def manifest(self, canvas, regions, **extra):
        magick("-size", f"{canvas[0]}x{canvas[1]}", "xc:#203040",
               "-fill", "#d05030", "-draw", "rectangle 3,4 9,13", self.root / "master.png")
        data = {"canvas": canvas, "master": "master.png", "max_aspect_drift": 0.02,
                "regions": regions, **extra}
        p = self.root / "layout.json"
        p.write_text(json.dumps(data))
        return p

    def call(self, command, layout, destination, ok=True):
        self.assertTrue(SCRIPT.is_file(), "portable compositor has not been implemented")
        p = subprocess.run([sys.executable, str(SCRIPT), command, str(layout), str(destination)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode == 0, ok, p.stdout + p.stderr)
        return p

    def test_landscape_and_portrait_guides_use_top_left_coordinates(self):
        # Catches inherited center-gravity crops and accidental width/height swapping.
        for canvas in ([48, 27], [27, 48]):
            with self.subTest(canvas=canvas):
                layout = self.manifest(canvas, [{"id": "subject", "rect": [2, 3, 12, 14]}])
                dest = self.root / f"prepare-{canvas[0]}"
                self.call("prepare", layout, dest)
                pixels = magick(dest / "guides/subject.png", "-depth", "8", "rgb:-")
                self.assertEqual(len(pixels), 12 * 14 * 3)
                # At local (1,1), the global (3,4) red rectangle starts.
                k = (1 * 12 + 1) * 3
                self.assertEqual(pixels[k:k + 3], bytes([208, 80, 48]))
                self.assertEqual(pixels[:3], bytes([32, 48, 64]))
                report = json.loads((dest / "report.json").read_text())
                self.assertEqual(report["canvas"], canvas)

    def test_actual_native_scale_masks_and_fair_crop(self):
        # Catches stretch, mask polarity, placement offsets and misleading resized QA crops.
        layout = self.manifest([48, 27], [{"id": "subject", "rect": [8, 4, 16, 12],
                                        "native": "native.png", "mask": "mask.png"}],
                               qa=[{"id": "join", "rect": [8, 4, 16, 12]}])
        magick("-size", "8x6", "xc:#10a0e0", self.root / "native.png")
        magick("-size", "16x12", "xc:white", "-fill", "black", "-draw",
               "rectangle 0,0 7,11", self.root / "mask.png")
        before = hashlib.sha256((self.root / "native.png").read_bytes()).hexdigest()
        dest = self.root / "assembled"
        self.call("assemble", layout, dest)
        report = json.loads((dest / "report.json").read_text())
        self.assertEqual(report["regions"][0]["uniform_scale"], 2)
        self.assertEqual(report["regions"][0]["native_size"], [8, 6])
        data = magick(dest / "composite.png", "-depth", "8", "rgb:-")
        for x, expected in [(10, bytes([32, 48, 64])), (20, bytes([16, 160, 224]))]:
            k = (10 * 48 + x) * 3
            self.assertEqual(data[k:k + 3], expected)
        crop = magick(dest / "qa/join-composite.png", "-depth", "8", "rgb:-")
        self.assertEqual(len(crop), 16 * 12 * 3)
        hand_slice = b"".join(data[((4 + row) * 48 + 8) * 3:((4 + row) * 48 + 24) * 3]
                              for row in range(12))
        self.assertEqual(crop, hand_slice)
        self.assertEqual(hashlib.sha256((self.root / "native.png").read_bytes()).hexdigest(), before)

    def test_feather_selection_and_missing_unselected_region(self):
        # Catches silently using a failed region, and feather direction reversal.
        layout = self.manifest([48, 27], [
            {"id": "ok", "rect": [10, 2, 16, 12], "native": "native.png",
             "feather": {"left": [0, 8]}},
            {"id": "failed", "rect": [20, 2, 16, 12], "native": "missing.png"}],
            selected_region_ids=["ok"])
        magick("-size", "16x12", "xc:white", self.root / "native.png")
        dest = self.root / "selection"
        self.call("assemble", layout, dest)
        data = magick(dest / "composite.png", "-depth", "8", "rgb:-")
        self.assertEqual(data[(5 * 48 + 10) * 3:(5 * 48 + 10) * 3 + 3], bytes([32, 48, 64]))
        self.assertEqual(data[(5 * 48 + 20) * 3:(5 * 48 + 20) * 3 + 3], bytes([255] * 3))
        report = json.loads((dest / "report.json").read_text())
        self.assertEqual([r["id"] for r in report["regions"]], ["ok"])
        self.assertEqual(report["excluded_region_ids"], ["failed"])

    def test_invalid_inputs_fail_before_creating_outputs(self):
        # Catches destructive partial writes, silent stretching and hidden missing-output fallback.
        cases = [
            {"id": "bad", "rect": [40, 1, 16, 12], "native": "native.png"},
            {"id": "bad", "rect": [1, 1, 16, 12], "native": "missing.png"},
            {"id": "bad", "rect": [1, 1, 16, 12], "native": "square.png"},
            {"id": "bad", "rect": [1, 1, 16, 12], "native": "native.png", "mask": "square.png"},
        ]
        magick("-size", "16x12", "xc:red", self.root / "native.png")
        magick("-size", "8x8", "xc:white", self.root / "square.png")
        for n, region in enumerate(cases):
            with self.subTest(region=region):
                layout = self.manifest([48, 27], [region])
                dest = self.root / f"bad-{n}"
                self.call("assemble", layout, dest, ok=False)
                self.assertFalse(dest.exists())

    def test_existing_output_is_preserved(self):
        # Catches reruns clobbering reviewable derivations or originals.
        layout = self.manifest([48, 27], [{"id": "A", "rect": [0, 0, 12, 12]}])
        dest = self.root / "existing"
        dest.mkdir()
        sentinel = dest / "keep.txt"
        sentinel.write_text("keep this candidate")
        self.call("prepare", layout, dest, ok=False)
        self.assertEqual(sentinel.read_text(), "keep this candidate")
        self.assertEqual(list(dest.iterdir()), [sentinel])


if __name__ == "__main__":
    unittest.main()

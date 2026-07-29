from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from scripts import init_akari_v1_5_kawaii_1000 as initializer
from scripts.init_akari_v1_5_kawaii_1000 import initialize_data_root


class InitializeAkariKawaii1000Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.data = self.root / "data"
        self._image(
            self.repo
            / "akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png",
            "#d6c0aa",
        )
        self._image(
            self.repo
            / "akari-v1.4/style-tests/line-refinement/"
            "akari-v14-g2-balanced-lines.png",
            "#c59d80",
        )
        self._image(
            self.repo
            / "akari-v1.4/style-tests/reproducibility-i-seated/"
            "akari-v14-i2-chair-seated-repro.png",
            "#b9a38f",
        )
        self._image(
            self.repo
            / "akari-v1.4/style-tests/reproducibility-j-action/"
            "akari-v14-j1-mandarin-action-repro.png",
            "#d8a45a",
        )
        self.texture = self.root / "neesocks.jpeg"
        Image.new("RGB", (16, 16), "#dddddd").save(self.texture, "JPEG")

    def _image(self, path: Path, color: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (16, 24), color).save(path, "PNG")

    def _initialize(self) -> Path:
        expected = hashlib.sha256(self.texture.read_bytes()).hexdigest()
        with patch.object(
            initializer,
            "NEESOCKS_REFERENCE_SHA256",
            expected,
        ):
            return initialize_data_root(self.repo, self.data, self.texture)

    def test_initialization_copies_references_and_records_hashes(self):
        result = self._initialize()
        manifest = json.loads(
            (result / "references/manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(5, len(manifest["references"]))
        self.assertTrue(
            all(len(item["sha256"]) == 64 for item in manifest["references"])
        )
        self.assertTrue((result / "state/novelty-ledger.json").is_file())

    def test_texture_reference_must_match_the_pinned_source_hash(self):
        with self.assertRaisesRegex(
            ValueError,
            "neesocks.jpeg SHA-256 mismatch",
        ):
            initialize_data_root(self.repo, self.data, self.texture)
        self.assertFalse(
            (
                self.data
                / "references/neesocks-pressure-study.jpeg"
            ).exists()
        )

    def test_initialization_refuses_changed_existing_reference(self):
        self._initialize()
        copied = self.data / "references/akari-v1.5-b3-body-balance.png"
        copied.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "reference snapshot mismatch"):
            self._initialize()

    def test_texture_source_symlink_is_rejected_even_when_hash_matches(self):
        real_texture = self.root / "real-neesocks.jpeg"
        os.replace(self.texture, real_texture)
        self.texture.symlink_to(real_texture)

        with self.assertRaisesRegex(ValueError, "regular non-symlink"):
            self._initialize()

    def test_existing_texture_snapshot_symlink_is_never_accepted(self):
        self._initialize()
        snapshot = (
            self.data / "references/neesocks-pressure-study.jpeg"
        )
        external = self.root / "external-neesocks.jpeg"
        snapshot.replace(external)
        snapshot.symlink_to(external)
        before = external.read_bytes()

        with self.assertRaisesRegex(ValueError, "regular non-symlink"):
            self._initialize()

        self.assertEqual(before, external.read_bytes())

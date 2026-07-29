from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.install_akari_review_gallery_service import (
    install_service,
    render_unit,
)


class InstallReviewGalleryServiceTests(unittest.TestCase):
    def test_unit_uses_exact_node_repo_data_and_tailscale_host(self):
        unit = render_unit(
            node=Path("/opt/node/bin/node"),
            python=Path("/opt/venv/bin/python"),
            repo_root=Path("/srv/akari-design"),
            data_root=Path("/srv/akari-generated/v1.5-1000"),
            host="100.125.117.75",
            port=8787,
        )
        self.assertIn('ExecStart="/opt/node/bin/node"', unit)
        self.assertIn('--python "/opt/venv/bin/python"', unit)
        self.assertIn('"/srv/akari-design/tools/review-gallery/server.mjs"', unit)
        self.assertIn('--host "100.125.117.75"', unit)
        self.assertNotIn("0.0.0.0", unit)
        self.assertIn("Restart=on-failure", unit)
        self.assertIn("NoNewPrivileges=yes", unit)
        self.assertIn("ProtectSystem=strict", unit)
        self.assertIn('ReadWritePaths="/srv/akari-generated/v1.5-1000/batches"', unit)

    def test_unit_rejects_wildcard_host(self):
        with self.assertRaisesRegex(ValueError, "Tailscale IPv4"):
            render_unit(
                node=Path("/opt/node/bin/node"),
                python=Path("/opt/venv/bin/python"),
                repo_root=Path("/srv/akari-design"),
                data_root=Path("/srv/data"),
                host="0.0.0.0",
                port=8787,
            )

    def test_unit_rejects_unsafe_path_and_out_of_range_port(self):
        with self.assertRaisesRegex(ValueError, "unsafe absolute path"):
            render_unit(
                node=Path('relative"node'),
                python=Path("/opt/venv/bin/python"),
                repo_root=Path("/srv/akari-design"),
                data_root=Path("/srv/data"),
                host="100.125.117.75",
                port=8787,
            )
        with self.assertRaisesRegex(ValueError, "port must be in 1..65535"):
            render_unit(
                node=Path("/opt/node/bin/node"),
                python=Path("/opt/venv/bin/python"),
                repo_root=Path("/srv/akari-design"),
                data_root=Path("/srv/data"),
                host="100.125.117.75",
                port=65536,
            )

    def test_install_writes_unit_and_runs_user_systemd(self):
        with tempfile.TemporaryDirectory() as temporary:
            calls = []

            def runner(command, *, check):
                calls.append((command, check))

            destination = install_service(
                "[Unit]\nDescription=Test\n",
                user_config=Path(temporary),
                runner=runner,
            )
            self.assertEqual(
                "[Unit]\nDescription=Test\n",
                destination.read_text(encoding="utf-8"),
            )
            self.assertEqual(
                [
                    (["systemctl", "--user", "daemon-reload"], True),
                    (
                        [
                            "systemctl",
                            "--user",
                            "enable",
                            "--now",
                            "akari-review-gallery.service",
                        ],
                        True,
                    ),
                ],
                calls,
            )


if __name__ == "__main__":
    unittest.main()

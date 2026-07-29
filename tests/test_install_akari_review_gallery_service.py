from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts import install_akari_review_gallery_service as installer
from scripts.install_akari_review_gallery_service import (
    _require_install_inputs,
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

    def test_unit_is_exactly_hardened_with_only_batches_writable(self):
        self.assertEqual(
            """[Unit]
Description=Akari review gallery

[Service]
Type=simple
ExecStart="/opt/node/bin/node" "/srv/akari-design/tools/review-gallery/server.mjs" --repo-root "/srv/akari-design" --data-root "/srv/akari-generated/v1.5-1000" --host "100.125.117.75" --port "8787" --python "/opt/venv/bin/python"
Restart=on-failure
RestartSec=5
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadOnlyPaths="/srv/akari-design" "/srv/akari-generated/v1.5-1000"
ReadWritePaths="/srv/akari-generated/v1.5-1000/batches"

[Install]
WantedBy=default.target
""",
            render_unit(
                node=Path("/opt/node/bin/node"),
                python=Path("/opt/venv/bin/python"),
                repo_root=Path("/srv/akari-design"),
                data_root=Path("/srv/akari-generated/v1.5-1000"),
                host="100.125.117.75",
                port=8787,
            ),
        )

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

    def test_unit_rejects_systemd_interpreted_path_characters(self):
        for label, path in {
            "backslash_escape": Path(r"/opt/node\\n/bin/node"),
            "trailing_backslash": Path("/opt/node/bin/node\\"),
            "specifier": Path("/opt/%n/bin/node"),
            "carriage_return": Path("/opt/node\r/bin/node"),
            "nul": Path("/opt/node\0/bin/node"),
            "control": Path("/opt/node\x1f/bin/node"),
        }.items():
            with self.subTest(label=label), self.assertRaisesRegex(
                ValueError, "unsafe absolute path"
            ):
                render_unit(
                    node=path,
                    python=Path("/opt/venv/bin/python"),
                    repo_root=Path("/srv/akari-design"),
                    data_root=Path("/srv/data"),
                    host="100.125.117.75",
                    port=8787,
                )

    def test_unit_rejects_unsafe_repository_path_before_deriving_server_path(self):
        with self.assertRaisesRegex(ValueError, "unsafe absolute path"):
            render_unit(
                node=Path("/opt/node/bin/node"),
                python=Path("/opt/venv/bin/python"),
                repo_root=Path("/srv/akari%design"),
                data_root=Path("/srv/data"),
                host="100.125.117.75",
                port=8787,
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

    def test_preview_prints_unit_without_install_or_systemd(self):
        expected = render_unit(
            node=Path("/opt/node/bin/node"),
            python=Path("/opt/venv/bin/python"),
            repo_root=Path("/srv/akari-design"),
            data_root=Path("/srv/data"),
            host="100.125.117.75",
            port=8787,
        )

        def unexpected_install(*args, **kwargs):
            self.fail("preview must not install or invoke systemd")

        output = io.StringIO()
        with (
            patch.object(installer, "_resolve_node", return_value=Path("/opt/node/bin/node")),
            patch.object(installer, "_resolve_python", return_value=Path("/opt/venv/bin/python")),
            patch.object(installer, "install_service", side_effect=unexpected_install),
            patch.object(
                sys,
                "argv",
                [
                    "installer",
                    "--repo-root",
                    "/srv/akari-design",
                    "--data-root",
                    "/srv/data",
                    "--host",
                    "100.125.117.75",
                ],
            ),
            contextlib.redirect_stdout(output),
        ):
            self.assertEqual(0, installer.main())
        self.assertEqual(expected, output.getvalue())

    def test_install_resolves_exact_commands_validates_inputs_and_installs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            node = root / "bin/node"
            python = root / "venv/bin/python"
            server = root / "repo/tools/review-gallery/server.mjs"
            data_root = root / "data"
            for executable in (node, python):
                executable.parent.mkdir(parents=True, exist_ok=True)
                executable.touch()
                executable.chmod(0o755)
            server.parent.mkdir(parents=True)
            server.touch()
            (data_root / "batches").mkdir(parents=True)
            commands = []
            installed = []

            def resolver(command, *, check, capture_output, text):
                commands.append((command, check, capture_output, text))
                if command == ["bash", "-lc", "command -v node"]:
                    return SimpleNamespace(stdout=f"{node}\n")
                if command == [
                    "uv",
                    "run",
                    "python",
                    "-c",
                    "import sys; print(sys.executable)",
                ]:
                    return SimpleNamespace(stdout=f"{python}\n")
                self.fail(f"unexpected subprocess command: {command}")

            def fake_install(unit, *, user_config):
                installed.append((unit, user_config))
                return user_config / "systemd/user/akari-review-gallery.service"

            output = io.StringIO()
            with (
                patch.object(installer.subprocess, "run", side_effect=resolver),
                patch.object(installer, "install_service", side_effect=fake_install),
                patch.object(installer.Path, "home", return_value=root / "home"),
                patch.object(
                    sys,
                    "argv",
                    [
                        "installer",
                        "--repo-root",
                        str(root / "repo"),
                        "--data-root",
                        str(data_root),
                        "--host",
                        "100.125.117.75",
                        "--install",
                    ],
                ),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(0, installer.main())

            self.assertEqual(
                [
                    (["bash", "-lc", "command -v node"], True, True, True),
                    (
                        [
                            "uv",
                            "run",
                            "python",
                            "-c",
                            "import sys; print(sys.executable)",
                        ],
                        True,
                        True,
                        True,
                    ),
                ],
                commands,
            )
            self.assertEqual(
                [
                    (
                        render_unit(
                            node=node,
                            python=python,
                            repo_root=root / "repo",
                            data_root=data_root,
                            host="100.125.117.75",
                            port=8787,
                        ),
                        root / "home/.config",
                    )
                ],
                installed,
            )
            self.assertEqual(
                f"installed service: {root / 'home/.config/systemd/user/akari-review-gallery.service'}\n",
                output.getvalue(),
            )

    def test_install_boundary_rejects_missing_required_inputs(self):
        for label, relative_missing, message in (
            ("node", "bin/node", "Node executable missing"),
            ("python", "venv/bin/python", "Python executable missing"),
            (
                "server",
                "repo/tools/review-gallery/server.mjs",
                "review gallery server missing",
            ),
            ("data_root", "data", "data root missing"),
            ("batches", "data/batches", "batches directory missing"),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                node = root / "bin/node"
                python = root / "venv/bin/python"
                server = root / "repo/tools/review-gallery/server.mjs"
                data_root = root / "data"
                for executable in (node, python):
                    executable.parent.mkdir(parents=True, exist_ok=True)
                    executable.touch()
                    executable.chmod(0o755)
                server.parent.mkdir(parents=True)
                server.touch()
                (data_root / "batches").mkdir(parents=True)
                missing = root / relative_missing
                if missing.is_dir():
                    if missing == data_root:
                        os.rmdir(data_root / "batches")
                    os.rmdir(missing)
                else:
                    missing.unlink()
                with self.assertRaisesRegex(FileNotFoundError, message):
                    _require_install_inputs(
                        node=node,
                        python=python,
                        repo_root=root / "repo",
                        data_root=data_root,
                    )


if __name__ == "__main__":
    unittest.main()

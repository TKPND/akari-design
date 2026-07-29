#!/usr/bin/env python3
"""Install the Akari review gallery as a hardened systemd user service."""

from __future__ import annotations

import argparse
import ipaddress
import os
import subprocess
from pathlib import Path


SERVICE_NAME = "akari-review-gallery.service"
UNSAFE_UNIT_PATH_CHARACTERS = {'"', "$", "\\", "%"}


def _unit_path(path: Path) -> str:
    value = str(path)
    if (
        not path.is_absolute()
        or any(char in UNSAFE_UNIT_PATH_CHARACTERS for char in value)
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        raise ValueError(f"unsafe absolute path: {value}")
    return value


def render_unit(
    *,
    node: Path,
    python: Path,
    repo_root: Path,
    data_root: Path,
    host: str,
    port: int,
) -> str:
    """Return a service unit without touching the filesystem."""

    address = ipaddress.ip_address(host)
    network = ipaddress.ip_network("100.64.0.0/10")
    if address.version != 4 or address not in network:
        raise ValueError("Tailscale IPv4 required")
    if not 1 <= port <= 65535:
        raise ValueError("port must be in 1..65535")
    node_value = _unit_path(node)
    python_value = _unit_path(python)
    repo_value = _unit_path(repo_root)
    data_value = _unit_path(data_root)
    server = _unit_path(repo_root / "tools/review-gallery/server.mjs")
    return f"""[Unit]
Description=Akari review gallery

[Service]
Type=simple
ExecStart=\"{node_value}\" \"{server}\" --repo-root \"{repo_value}\" --data-root \"{data_value}\" --host \"{host}\" --port \"{port}\" --python \"{python_value}\"
Restart=on-failure
RestartSec=5
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadOnlyPaths=\"{repo_value}\" \"{data_value}\"
ReadWritePaths=\"{data_value}/batches\"

[Install]
WantedBy=default.target
"""


def install_service(
    unit: str,
    *,
    user_config: Path,
    runner=subprocess.run,
) -> Path:
    """Atomically write the unit, reload systemd, and enable the service."""

    unit_dir = user_config / "systemd/user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    destination = unit_dir / SERVICE_NAME
    temporary = unit_dir / f".{SERVICE_NAME}.{os.getpid()}.tmp"
    temporary.write_text(unit, encoding="utf-8")
    os.replace(temporary, destination)
    runner(
        ["systemctl", "--user", "daemon-reload"],
        check=True,
    )
    runner(
        ["systemctl", "--user", "enable", "--now", SERVICE_NAME],
        check=True,
    )
    return destination


def _resolve_node() -> Path:
    result = subprocess.run(
        ["bash", "-lc", "command -v node"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def _resolve_python() -> Path:
    result = subprocess.run(
        ["uv", "run", "python", "-c", "import sys; print(sys.executable)"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def _require_install_inputs(
    *, node: Path, python: Path, repo_root: Path, data_root: Path
) -> None:
    for label, executable in (("Node", node), ("Python", python)):
        if not executable.is_file() or not os.access(executable, os.X_OK):
            raise FileNotFoundError(f"{label} executable missing: {executable}")
    server = repo_root / "tools/review-gallery/server.mjs"
    if not repo_root.is_dir() or not server.is_file():
        raise FileNotFoundError(f"review gallery server missing: {server}")
    if not data_root.is_dir():
        raise FileNotFoundError(f"data root missing: {data_root}")
    batches = data_root / "batches"
    if not batches.is_dir():
        raise FileNotFoundError(f"batches directory missing: {batches}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    node = _resolve_node()
    python = _resolve_python()
    unit = render_unit(
        node=node,
        python=python,
        repo_root=args.repo_root,
        data_root=args.data_root,
        host=args.host,
        port=args.port,
    )
    if not args.install:
        print(unit, end="")
        return 0

    _require_install_inputs(
        node=node,
        python=python,
        repo_root=args.repo_root,
        data_root=args.data_root,
    )
    destination = install_service(unit, user_config=Path.home() / ".config")
    print(f"installed service: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

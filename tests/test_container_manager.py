from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aihost.container_manager import (  # noqa: E402
    ContainerInfo,
    list_containers,
    list_apps,
    start_app,
    stop_app,
    rebuild_app,
    remove_app,
)


class DummyContainer:
    name = "my_container"
    attrs = {"NetworkSettings": {"Ports": {"80/tcp": [{"HostPort": "8080"}]}}}

    def __init__(self) -> None:
        self.start = MagicMock()
        self.stop = MagicMock()
        self.remove = MagicMock()


def test_list_containers(monkeypatch):
    container = DummyContainer()
    client = MagicMock()
    client.containers.list.return_value = [container]
    monkeypatch.setattr(
        "aihost.container_manager.docker.from_env",
        lambda: client,
    )

    result = list_containers()

    assert result == [
        ContainerInfo(name="my_container", ports=["http://localhost:8080"])
    ]


def test_list_apps(tmp_path: Path, monkeypatch):
    (tmp_path / "app1").mkdir()
    (tmp_path / "app1" / "docker-compose.yml").write_text("version: '3'")
    (tmp_path / "app2").mkdir()
    (tmp_path / "app2" / "docker-compose.yml").write_text("version: '3'")

    monkeypatch.setattr("aihost.container_manager.COMPOSE_DIR", tmp_path)

    apps = list_apps()
    assert apps == ["app1", "app2"]


def test_compose_actions(tmp_path: Path, monkeypatch):
    app_dir = tmp_path / "app"
    app_dir.mkdir(parents=True)
    compose_file = app_dir / "docker-compose.yml"
    compose_file.write_text("version: '3'")

    monkeypatch.setattr("aihost.container_manager.COMPOSE_DIR", tmp_path)

    calls = []

    def fake_call(cmd, cwd=None):
        calls.append((cmd, cwd))

    monkeypatch.setattr(
        "aihost.container_manager.subprocess.check_call",
        fake_call,
    )

    start_app("app")
    stop_app("app")
    rebuild_app("app")
    remove_app("app")

    expected_cwd = compose_file.parent
    assert calls == [
        (
            ["docker", "compose", "-f", str(compose_file), "up", "-d"],
            expected_cwd,
        ),
        (
            ["docker", "compose", "-f", str(compose_file), "stop"],
            expected_cwd,
        ),
        (
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "build",
                "--no-cache",
            ],
            expected_cwd,
        ),
        (["docker", "compose", "-f", str(compose_file), "down"], expected_cwd),
    ]

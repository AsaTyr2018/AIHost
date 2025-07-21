from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aihost.container_manager import (  # noqa: E402
    ContainerInfo,
    list_containers,
    list_apps,
    start_container,
    stop_container,
    rebuild_container,
    install_app,
    deinstall_app,
    get_app_logs,
    install_app_async,
)


class DummyContainer:
    name = "my_container"
    attrs = {"NetworkSettings": {"Ports": {"80/tcp": [{"HostPort": "8080"}]}}}

    def __init__(self) -> None:
        self.start = MagicMock()
        self.stop = MagicMock()


def test_list_containers(monkeypatch):
    container = DummyContainer()
    client = MagicMock()
    client.containers.list.return_value = [container]
    client.containers.get.return_value = container
    monkeypatch.setattr(
        "aihost.container_manager.docker.from_env",
        lambda: client,
    )

    result = list_containers()

    assert result == [
        ContainerInfo(name="my_container", ports=["http://localhost:8080"])
    ]


def test_container_actions(monkeypatch):
    container = DummyContainer()
    client = MagicMock()
    client.containers.get.return_value = container
    monkeypatch.setattr(
        "aihost.container_manager.docker.from_env",
        lambda: client,
    )

    start_container("my_container")
    stop_container("my_container")

    assert container.start.called
    assert container.stop.called


def test_list_apps(tmp_path: Path, monkeypatch):
    (tmp_path / "app1").mkdir()
    (tmp_path / "app1" / "docker-compose.yml").write_text("version: '3'")
    (tmp_path / "app2").mkdir()
    (tmp_path / "app2" / "docker-compose.yml").write_text("version: '3'")

    monkeypatch.setattr("aihost.container_manager.COMPOSE_DIR", tmp_path)

    apps = list_apps()
    assert apps == ["app1", "app2"]


def test_app_actions(tmp_path: Path, monkeypatch):
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

    install_app("app")
    deinstall_app("app")

    expected_cwd = compose_file.parent
    assert calls == [
        (
            ["docker", "compose", "-f", str(compose_file), "up", "-d"],
            expected_cwd,
        ),
        (
            ["docker", "compose", "-f", str(compose_file), "down", "-v"],
            expected_cwd,
        ),
    ]


def test_rebuild_container(tmp_path: Path, monkeypatch):
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

    rebuild_container("app")

    expected_cwd = compose_file.parent
    assert calls == [
        (["docker", "compose", "-f", str(compose_file), "pull"], expected_cwd),
        (
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "up",
                "-d",
                "--force-recreate",
            ],
            expected_cwd,
        ),
    ]


def test_get_app_logs(tmp_path: Path, monkeypatch):
    app_dir = tmp_path / "app"
    app_dir.mkdir(parents=True)
    compose_file = app_dir / "docker-compose.yml"
    compose_file.write_text("version: '3'")

    monkeypatch.setattr("aihost.container_manager.COMPOSE_DIR", tmp_path)

    def fake_output(cmd, cwd=None, text=None, stderr=None):
        assert cwd == compose_file.parent
        return "logs"

    monkeypatch.setattr(
        "aihost.container_manager.subprocess.check_output",
        fake_output,
    )

    logs = get_app_logs("app", lines=10)
    assert logs == "logs"


def test_install_app_async(tmp_path: Path, monkeypatch):
    app_dir = tmp_path / "app"
    app_dir.mkdir(parents=True)
    compose_file = app_dir / "docker-compose.yml"
    compose_file.write_text("version: '3'")

    monkeypatch.setattr("aihost.container_manager.COMPOSE_DIR", tmp_path)
    monkeypatch.setattr("aihost.container_manager.LOGS_DIR", tmp_path / "logs")

    calls = []

    class DummyProc:
        pass

    def fake_popen(cmd, cwd=None, stdout=None, stderr=None):
        calls.append((cmd, cwd))
        return DummyProc()

    monkeypatch.setattr(
        "aihost.container_manager.subprocess.Popen",
        fake_popen,
    )

    install_app_async("app")

    expected_cmd = ["docker", "compose", "-f", str(compose_file), "up", "-d"]
    assert calls == [(expected_cmd, compose_file.parent)]

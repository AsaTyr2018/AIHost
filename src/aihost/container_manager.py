from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import subprocess
import docker

# Resolve compose directory relative to the package root so the path does not
# depend on the current working directory.
COMPOSE_DIR = Path(__file__).resolve().parents[2] / "compose"


@dataclass
class ContainerInfo:
    """Representation of a Docker container."""

    name: str
    ports: List[str]


def _client() -> docker.DockerClient:
    """Return Docker client connected to the host."""

    return docker.from_env()


def list_containers() -> List[ContainerInfo]:
    """Return all containers known to the Docker host."""

    client = _client()
    containers: List[ContainerInfo] = []
    for container in client.containers.list(all=True):
        ports = []
        port_info = container.attrs.get("NetworkSettings", {}).get("Ports", {})
        for mappings in port_info.values():
            if not mappings:
                continue
            for mapping in mappings:
                host_port = mapping.get("HostPort")
                if host_port:
                    ports.append(f"http://localhost:{host_port}")
        containers.append(ContainerInfo(name=container.name, ports=ports))
    return containers


def list_apps() -> List[str]:
    """Return names of available applications."""

    apps: List[str] = []
    if not COMPOSE_DIR.exists():
        return apps
    for child in COMPOSE_DIR.iterdir():
        if child.is_dir() and (child / "docker-compose.yml").exists():
            apps.append(child.name)
    return sorted(apps)


def _compose(app: str, *args: str) -> None:
    """Run a docker compose command for *app* with *args*."""

    compose_file = COMPOSE_DIR / app / "docker-compose.yml"
    if not compose_file.exists():
        raise FileNotFoundError(compose_file)
    cmd = ["docker", "compose", "-f", str(compose_file)] + list(args)
    subprocess.check_call(cmd, cwd=compose_file.parent)


def start_app(app: str) -> None:
    _compose(app, "up", "-d")


def stop_app(app: str) -> None:
    _compose(app, "stop")


def remove_app(app: str) -> None:
    _compose(app, "down")


def rebuild_app(app: str) -> None:
    _compose(app, "build", "--no-cache")

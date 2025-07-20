from __future__ import annotations

from dataclasses import dataclass
from typing import List

import docker


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
        for container_port, mappings in port_info.items():
            if not mappings:
                continue
            for mapping in mappings:
                host_port = mapping.get("HostPort")
                if host_port:
                    ports.append(f"http://localhost:{host_port}")
        containers.append(ContainerInfo(name=container.name, ports=ports))
    return containers


def start_container(name: str) -> None:
    """Start a container by name."""

    client = _client()
    container = client.containers.get(name)
    container.start()


def stop_container(name: str) -> None:
    """Stop a container by name."""

    client = _client()
    container = client.containers.get(name)
    container.stop()


def remove_container(name: str) -> None:
    """Remove a container by name."""

    client = _client()
    container = client.containers.get(name)
    container.remove(force=True)


def rebuild_container(name: str, path: str) -> None:
    """Rebuild the Docker image of a container.

    The build context is provided by *path*.
    """

    client = _client()
    client.images.build(path=path, tag=name, rm=True)

from __future__ import annotations

from unittest.mock import MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aihost.container_manager import (  # noqa: E402
    ContainerInfo,
    list_containers,
    remove_container,
    rebuild_container,
    start_container,
    stop_container,
)


def _mock_client(container: MagicMock) -> MagicMock:
    client = MagicMock()
    client.containers.list.return_value = [container]
    client.containers.get.return_value = container
    client.images.build.return_value = (MagicMock(), [])
    return client


def test_list_containers():
    container = MagicMock()
    container.name = "my_container"
    container.attrs = {
        "NetworkSettings": {"Ports": {"80/tcp": [{"HostPort": "8080"}]}}
    }  # noqa: E501

    client = _mock_client(container)
    with patch(
        "aihost.container_manager.docker.from_env",
        return_value=client,
    ):
        result = list_containers()

    assert result == [
        ContainerInfo(name="my_container", ports=["http://localhost:8080"])
    ]


def test_start_stop_remove_rebuild():
    container = MagicMock()
    client = _mock_client(container)
    with patch(
        "aihost.container_manager.docker.from_env",
        return_value=client,
    ):
        start_container("my_container")
        stop_container("my_container")
        remove_container("my_container")
        rebuild_container("MyContainer", path=".")

    container.start.assert_called_once()
    container.stop.assert_called_once()
    container.remove.assert_called_once_with(force=True)

    client.images.build.assert_called_once_with(
        path=".", tag="mycontainer", rm=True, decode=False
    )  # noqa: E501

from __future__ import annotations

from pathlib import Path
import subprocess

import docker

from .registry import RepoInfo


# Use a specific CUDA base image tag that exists on Docker Hub.
# The previous tag `12.1.1-base` is invalid and caused build failures
# because the manifest is missing. The `ubuntu20.04` variant is
# available and includes Python.
DEFAULT_BASE_IMAGE = "nvidia/cuda:12.1.1-base-ubuntu20.04"
DATA_DIR = Path("data")


def _client() -> docker.DockerClient:
    return docker.from_env()


def clone_repo(repo: RepoInfo, dest: Path) -> None:
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["git", "clone", repo.url, str(dest)])


def write_dockerfile(
    dest: Path, start_command: str, base_image: str = DEFAULT_BASE_IMAGE
) -> None:
    dockerfile = dest / "Dockerfile"
    content = f"""FROM {base_image}
WORKDIR /app
COPY . /app
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
CMD {start_command}
"""
    dockerfile.write_text(content)


def build_image(name: str, path: Path) -> None:
    client = _client()
    client.images.build(path=str(path), tag=name, rm=True)


def install_repo(repo: RepoInfo, base_image: str = DEFAULT_BASE_IMAGE) -> None:
    dest = DATA_DIR / repo.name
    clone_repo(repo, dest)
    write_dockerfile(dest, repo.start_command, base_image)
    build_image(repo.name, dest)

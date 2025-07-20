from __future__ import annotations

from pathlib import Path
import subprocess

import docker

from .registry import RepoInfo


def _normalize_tag(name: str) -> str:
    """Return a Docker-compatible lowercase image tag."""

    return name.lower()


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
    dest: Path,
    start_command: str,
    requirements_file: str = "requirements.txt",
    base_image: str = DEFAULT_BASE_IMAGE,
) -> None:
    dockerfile = dest / "Dockerfile"
    content = f"""FROM {base_image}
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN if [ -f {requirements_file} ]; then pip3 install -r {requirements_file}; fi  # noqa
CMD {start_command}
"""
    dockerfile.write_text(content)


def _print_build_logs(logs) -> None:
    """Print Docker build output lines."""

    for chunk in logs:
        if "stream" in chunk:
            line = chunk["stream"].strip()
            if line:
                print(line)
        elif "status" in chunk:
            status = chunk.get("status", "").strip()
            progress = chunk.get("progress", "")
            print(f"{status} {progress}".strip())
        elif "error" in chunk:
            print(chunk["error"].strip())


def build_image(name: str, path: Path) -> None:
    """Build the Docker image located at *path* and show progress."""

    client = _client()
    # Docker already decodes build output into dictionaries, so disable
    # additional decoding to avoid bytes/string mismatches in newer
    # docker-py versions.
    _, logs = client.images.build(
        path=str(path), tag=_normalize_tag(name), rm=True, decode=False
    )
    _print_build_logs(logs)


def install_repo(repo: RepoInfo, base_image: str = DEFAULT_BASE_IMAGE) -> None:
    dest = DATA_DIR / repo.name
    clone_repo(repo, dest)
    write_dockerfile(
        dest,
        repo.start_command,
        requirements_file=repo.requirements_file,
        base_image=base_image,
    )
    build_image(repo.name, dest)

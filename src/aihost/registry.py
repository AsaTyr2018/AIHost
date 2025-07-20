from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List
import json


@dataclass
class RepoInfo:
    name: str
    url: str
    start_command: str
    requirements_file: str = "requirements.txt"


REGISTRY_FILE = Path("data/registry.json")


def _load() -> List[RepoInfo]:
    if not REGISTRY_FILE.exists():
        return []
    data = json.loads(REGISTRY_FILE.read_text())
    repos: List[RepoInfo] = []
    for item in data:
        if "requirements_file" not in item:
            item["requirements_file"] = "requirements.txt"
        repos.append(RepoInfo(**item))
    return repos


def _save(repos: List[RepoInfo]) -> None:
    REGISTRY_FILE.parent.mkdir(exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps([asdict(r) for r in repos], indent=2))


def list_repos() -> List[RepoInfo]:
    return _load()


def add_repo(
    name: str,
    url: str,
    start_command: str,
    requirements_file: str = "requirements.txt",
) -> None:
    repos = _load()
    if any(r.name == name for r in repos):
        raise ValueError(f"Repository '{name}' already exists")
    repos.append(
        RepoInfo(
            name=name,
            url=url,
            start_command=start_command,
            requirements_file=requirements_file,
        )
    )
    _save(repos)


def delete_repo(name: str) -> None:
    repos = [r for r in _load() if r.name != name]
    _save(repos)

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pytest  # noqa: E402
from aihost.registry import (  # noqa: E402
    add_repo,
    delete_repo,
    list_repos,
    RepoInfo,
)  # noqa: E402


def test_registry(tmp_path: Path, monkeypatch):
    file = tmp_path / "registry.json"
    monkeypatch.setattr("aihost.registry.REGISTRY_FILE", file)

    add_repo("repo1", "https://example.com", "run.sh")
    repos = list_repos()
    assert repos == [
        RepoInfo(
            name="repo1",
            url="https://example.com",
            start_command="run.sh",
        )
    ]

    add_repo("repo2", "https://e.com", "start")
    delete_repo("repo1")
    repos = list_repos()
    assert len(repos) == 1
    assert repos[0].name == "repo2"


def test_add_duplicate(tmp_path: Path, monkeypatch):
    file = tmp_path / "registry.json"
    monkeypatch.setattr("aihost.registry.REGISTRY_FILE", file)

    add_repo("dup", "url", "cmd")
    with pytest.raises(ValueError):
        add_repo("dup", "url2", "cmd2")

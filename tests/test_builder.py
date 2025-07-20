from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aihost.registry import RepoInfo  # noqa: E402
from aihost import builder  # noqa: E402


def test_install_repo(tmp_path: Path, monkeypatch):
    repo = RepoInfo(
        name="myrepo",
        url="https://example.com/repo.git",
        start_command="python app.py",
    )
    monkeypatch.setattr(builder, "DATA_DIR", tmp_path)

    run_calls = []

    def fake_call(cmd):
        run_calls.append(cmd)
        Path(cmd[-1]).mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(builder.subprocess, "check_call", fake_call)

    client = MagicMock()
    monkeypatch.setattr(builder, "_client", lambda: client)

    builder.install_repo(repo)

    expected_dir = tmp_path / repo.name
    assert run_calls[0] == ["git", "clone", repo.url, str(expected_dir)]

    dockerfile = expected_dir / "Dockerfile"
    assert dockerfile.exists()
    text = dockerfile.read_text()
    assert builder.DEFAULT_BASE_IMAGE in text
    assert repo.start_command in text

    client.images.build.assert_called_once_with(
        path=str(expected_dir), tag=repo.name, rm=True
    )

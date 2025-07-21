from __future__ import annotations

import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aihost.gpu import get_gpu_stats  # noqa: E402


def test_get_gpu_stats_no_library(monkeypatch):
    monkeypatch.setitem(sys.modules, "pynvml", None)
    assert get_gpu_stats() is None


def test_get_gpu_stats_success(monkeypatch):
    mem = types.SimpleNamespace(total=4 * 1024 * 1024, used=2 * 1024 * 1024)

    def fake_nvmlInit():
        pass

    def fake_nvmlShutdown():
        pass

    def fake_nvmlDeviceGetCount():
        return 1

    def fake_nvmlDeviceGetHandleByIndex(index):
        return "h"

    def fake_nvmlDeviceGetName(handle):
        return b"FakeGPU"

    def fake_nvmlDeviceGetMemoryInfo(handle):
        return mem

    fake_module = types.SimpleNamespace(
        nvmlInit=fake_nvmlInit,
        nvmlShutdown=fake_nvmlShutdown,
        nvmlDeviceGetCount=fake_nvmlDeviceGetCount,
        nvmlDeviceGetHandleByIndex=fake_nvmlDeviceGetHandleByIndex,
        nvmlDeviceGetName=fake_nvmlDeviceGetName,
        nvmlDeviceGetMemoryInfo=fake_nvmlDeviceGetMemoryInfo,
    )
    monkeypatch.setitem(sys.modules, "pynvml", fake_module)

    stats = get_gpu_stats()
    assert stats == {
        "name": "FakeGPU",
        "memory_total": 4,
        "memory_used": 2,
        "memory_percent": 50,
    }

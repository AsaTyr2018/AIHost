from __future__ import annotations

from typing import Optional, Dict


def get_gpu_stats() -> Optional[Dict[str, int | str]]:
    """Return GPU statistics if available.

    The function queries the first available NVIDIA GPU using ``pynvml``.
    Results are returned in megabytes. If no GPU or NVML library is
    present, ``None`` is returned.
    """

    try:
        import pynvml  # type: ignore
    except Exception:
        return None

    try:
        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
        if count < 1:
            return None
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        name = pynvml.nvmlDeviceGetName(handle).decode()
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        total_mb = mem.total // (1024 * 1024)
        used_mb = mem.used // (1024 * 1024)
        percent = int(used_mb / total_mb * 100) if total_mb else 0
        return {
            "name": name,
            "memory_total": total_mb,
            "memory_used": used_mb,
            "memory_percent": percent,
        }
    except Exception:
        return None
    finally:
        try:
            pynvml.nvmlShutdown()
        except Exception:
            pass

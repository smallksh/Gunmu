"""追踪所有 Nothing 的产生位置。

默认关闭，零开销。
"""
from __future__ import annotations

import threading
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class _TraceState:
    enabled: bool = False
    records: list[tuple[str, str]] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)


_state = _TraceState()


def enable() -> None:
    """开启追踪。之后所有 Nothing 都会被记录。"""
    with _state.lock:
        _state.enabled = True


def disable() -> None:
    with _state.lock:
        _state.enabled = False


def clear() -> None:
    with _state.lock:
        _state.records.clear()


def record_nothing(reason: str, origin: str) -> None:
    if not _state.enabled:
        return
    with _state.lock:
        _state.records.append((reason, origin))


def records() -> list[tuple[str, str]]:
    with _state.lock:
        return list(_state.records)


def summary() -> dict:
    """按原因统计滚木。"""
    with _state.lock:
        counter = Counter(reason for reason, _ in _state.records)
        total = len(_state.records)
        recs = list(_state.records)
    return {
        "total": total,
        "by_reason": dict(counter.most_common()),
        "records": recs,
    }


def report() -> str:
    """人类可读的报告。"""
    s = summary()
    if s["total"] == 0:
        return "没有滚木。"
    lines = [f"共 {s['total']} 个滚木："]
    for reason, count in s["by_reason"].items():
        lines.append(f"  [{count}] {reason}")
    lines.append("")
    lines.append("产生位置：")
    for reason, origin in s["records"]:
        lines.append(f"  {origin}  ->  {reason}")
    return "\n".join(lines)
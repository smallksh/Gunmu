"""把一组 Gunmu 收成一个 Gunmu[list]。

- 全部 Some → Some([...])
- 有任意 Nothing → 第一个 Nothing（fail-fast）
- 也可以选择收集所有原因

用法：
    collect([some(1), some(2)])            # Some([1, 2])
    collect([some(1), nothing("a")])       # Nothing("a")
    collect_all([some(1), nothing("a"), nothing("b")])
    # Nothing("a; b")
"""
from __future__ import annotations

from typing import Iterable, TypeVar

from .core import Gunmu, Nothing, Some

T = TypeVar("T")


def collect(items: Iterable[Gunmu[T]]) -> Gunmu[list[T]]:
    """fail-fast：遇到第一个 Nothing 就返回它。"""
    values: list[T] = []
    for item in items:
        if item.is_nothing():
            return item  # type: ignore[return-value]
        values.append(item.unwrap())
    return Some(values)


def collect_all(items: Iterable[Gunmu[T]]) -> Gunmu[list[T]]:
    """收集所有原因，合并成一个 Nothing。"""
    values: list[T] = []
    reasons: list[str] = []
    for item in items:
        if item.is_nothing():
            reasons.append(item.reason())
        else:
            values.append(item.unwrap())
    if reasons:
        return Nothing("; ".join(reasons))
    return Some(values)


def collect_dict(mapping: dict[str, Gunmu[T]]) -> Gunmu[dict[str, T]]:
    """收集一个 dict。fail-fast。"""
    result: dict[str, T] = {}
    for key, item in mapping.items():
        if item.is_nothing():
            return Nothing(f"{key}: {item.reason()}")
        result[key] = item.unwrap()
    return Some(result)
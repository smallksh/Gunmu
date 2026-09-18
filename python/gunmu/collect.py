from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import TypeVar

from .core import Gunmu, Nothing, Some

T = TypeVar("T")


def collect(items: Iterable[Gunmu[T]]) -> Gunmu[list[T]]:
    """收集所有 Some；遇到第一个 Nothing 立即返回。"""
    values: list[T] = []

    for item in items:
        if isinstance(item, Nothing):
            return item

        values.append(item.unwrap())

    return Some(values)


def collect_all(items: Iterable[Gunmu[T]]) -> Gunmu[list[T]]:
    """收集所有值；若存在 Nothing，则合并所有 reason。"""
    values: list[T] = []
    reasons: list[str] = []

    for item in items:
        if isinstance(item, Nothing):
            reasons.append(item.reason())
        else:
            values.append(item.unwrap())

    if reasons:
        return Nothing("; ".join(reasons))

    return Some(values)


def collect_dict(
    mapping: Mapping[str, Gunmu[T]],
) -> Gunmu[dict[str, T]]:
    """收集字典中的所有 Some；遇到 Nothing 则失败。"""
    result: dict[str, T] = {}

    for key, item in mapping.items():
        if isinstance(item, Nothing):
            return Nothing(f"{key}: {item.reason()}")

        result[key] = item.unwrap()

    return Some(result)
"""gunmu —— 显式空值处理。

滚木 = 值不存在。
当你拿到一个 Gunmu，你必须处理它，不能假装它不存在。
"""
from __future__ import annotations

import inspect
from typing import Callable, Generic, Iterator, TypeVar

from .trace import record_nothing

T = TypeVar("T")
U = TypeVar("U")


class Gunmu(Generic[T]):
    """滚木的抽象基类。

    不要直接实例化，用 Some / Nothing。
    """

    __slots__ = ()

    def is_some(self) -> bool:
        raise NotImplementedError

    def is_nothing(self) -> bool:
        return not self.is_some()

    def unwrap(self) -> T:
        """取出值。如果是滚木，抛 GunmuError。"""
        raise NotImplementedError

    def unwrap_or(self, default: T) -> T:
        raise NotImplementedError

    def unwrap_or_else(self, f: Callable[[str], T]) -> T:
        raise NotImplementedError

    def map(self, f: Callable[[T], U]) -> "Gunmu[U]":
        raise NotImplementedError

    def flat_map(self, f: Callable[[T], "Gunmu[U]"]) -> "Gunmu[U]":
        raise NotImplementedError

    def filter(
        self,
        predicate: Callable[[T], bool],
        reason: str = "不满足条件",
    ) -> "Gunmu[T]":
        raise NotImplementedError

    def match(
        self,
        *,
        some: Callable[[T], U],
        nothing: Callable[[str], U],
    ) -> U:
        raise NotImplementedError

    def reason(self) -> str:
        """滚木的原因。Some 返回空字符串。"""
        raise NotImplementedError

    def __bool__(self) -> bool:
        return self.is_some()

    def __iter__(self) -> Iterator[T]:
        if self.is_some():
            yield self.unwrap()

    def __repr__(self) -> str:
        if self.is_some():
            return f"Some({self.unwrap()!r})"
        return f"Nothing({self.reason()!r})"


class Some(Gunmu[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def is_some(self) -> bool:
        return True

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def unwrap_or_else(self, f: Callable[[str], T]) -> T:
        return self._value

    def map(self, f: Callable[[T], U]) -> "Gunmu[U]":
        return Some(f(self._value))

    def flat_map(self, f: Callable[[T], "Gunmu[U]"]) -> "Gunmu[U]":
        return f(self._value)

    def filter(
        self,
        predicate: Callable[[T], bool],
        reason: str = "不满足条件",
    ) -> "Gunmu[T]":
        if predicate(self._value):
            return self
        return Nothing(reason)

    def match(
        self,
        *,
        some: Callable[[T], U],
        nothing: Callable[[str], U],
    ) -> U:
        return some(self._value)

    def reason(self) -> str:
        return ""


class Nothing(Gunmu[T]):
    __slots__ = ("_reason", "_origin")

    def __init__(self, reason: str = "滚木", *, _origin: str | None = None) -> None:
        self._reason = reason
        self._origin = _origin or _caller_location()
        record_nothing(self._reason, self._origin)

    def is_some(self) -> bool:
        return False

    def unwrap(self) -> T:
        raise GunmuError(self._reason, self._origin)

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: Callable[[str], T]) -> T:
        return f(self._reason)

    def map(self, f: Callable[[T], U]) -> "Gunmu[U]":
        return self  # type: ignore[return-value]

    def flat_map(self, f: Callable[[T], "Gunmu[U]"]) -> "Gunmu[U]":
        return self  # type: ignore[return-value]

    def filter(
        self,
        predicate: Callable[[T], bool],
        reason: str = "不满足条件",
    ) -> "Gunmu[T]":
        return self

    def match(
        self,
        *,
        some: Callable[[T], U],
        nothing: Callable[[str], U],
    ) -> U:
        return nothing(self._reason)

    def reason(self) -> str:
        return self._reason

    def origin(self) -> str:
        return self._origin


class GunmuError(Exception):
    """试图从滚木里取值。"""

    def __init__(self, reason: str, origin: str = "") -> None:
        msg = f"滚木：{reason}"
        if origin:
            msg += f"（产生于 {origin}）"
        super().__init__(msg)
        self.reason = reason
        self.origin = origin


def _caller_location() -> str:
    """找到第一个不在 gunmu 包内的调用者。"""
    frame = inspect.currentframe()
    if frame is None:
        return ""
    frame = frame.f_back
    while frame is not None:
        module = frame.f_globals.get("__name__", "")
        if not module.startswith("gunmu"):
            return f"{frame.f_code.co_filename}:{frame.f_lineno}"
        frame = frame.f_back
    return ""


def some(value: T) -> Gunmu[T]:
    return Some(value)


def nothing(reason: str = "滚木") -> Gunmu[T]:
    return Nothing(reason)


def from_optional(value: T | None, reason: str = "值为 None") -> Gunmu[T]:
    """把 Optional 转成 Gunmu。"""
    if value is None:
        return Nothing(reason)
    return Some(value)
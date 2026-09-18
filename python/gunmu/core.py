from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import Callable, Generic, Iterator, TypeVar, cast

from .trace import record_nothing

T = TypeVar("T")
U = TypeVar("U")


class Gunmu(Generic[T], ABC):
    """显式空值容器。

    Gunmu 要么包含一个 Some(value)，
    要么表示 Nothing(reason)。
    """

    __slots__ = ()

    @abstractmethod
    def is_some(self) -> bool:
        ...

    def is_nothing(self) -> bool:
        return not self.is_some()

    @abstractmethod
    def unwrap(self) -> T:
        ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        ...

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[str], T]) -> T:
        ...

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> Gunmu[U]:
        ...

    @abstractmethod
    def flat_map(self, f: Callable[[T], Gunmu[U]]) -> Gunmu[U]:
        ...

    @abstractmethod
    def filter(
        self,
        predicate: Callable[[T], bool],
        reason: str = "不满足条件",
    ) -> Gunmu[T]:
        ...

    @abstractmethod
    def match(
        self,
        *,
        some: Callable[[T], U],
        nothing: Callable[[str], U],
    ) -> U:
        ...

    @abstractmethod
    def reason(self) -> str:
        ...

    def __bool__(self) -> bool:
        return self.is_some()

    def __iter__(self) -> Iterator[T]:
        if isinstance(self, Some):
            yield self._value

    def __repr__(self) -> str:
        if isinstance(self, Some):
            return f"Some({self._value!r})"
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

    def map(self, f: Callable[[T], U]) -> Gunmu[U]:
        return Some(f(self._value))

    def flat_map(self, f: Callable[[T], Gunmu[U]]) -> Gunmu[U]:
        result = f(self._value)
        if not isinstance(result, Gunmu):
            raise TypeError(
                "flat_map() 的函数必须返回 Gunmu，"
                f"实际得到 {type(result).__name__}"
            )
        return result

    def filter(
        self,
        predicate: Callable[[T], bool],
        reason: str = "不满足条件",
    ) -> Gunmu[T]:
        return self if predicate(self._value) else Nothing(reason)

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

    def __init__(
        self,
        reason: str = "滚木",
        *,
        _origin: str | None = None,
    ) -> None:
        if not isinstance(reason, str):
            raise TypeError("Nothing 的 reason 必须是 str")

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

    def map(self, f: Callable[[T], U]) -> Gunmu[U]:
        return cast(Gunmu[U], self)

    def flat_map(self, f: Callable[[T], Gunmu[U]]) -> Gunmu[U]:
        return cast(Gunmu[U], self)

    def filter(
        self,
        predicate: Callable[[T], bool],
        reason: str = "不满足条件",
    ) -> Gunmu[T]:
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
    """尝试从 Nothing 中取值。"""

    def __init__(self, reason: str, origin: str = "") -> None:
        message = f"滚木：{reason}"

        if origin:
            message += f"（产生于 {origin}）"

        super().__init__(message)

        self.reason = reason
        self.origin = origin


def _caller_location() -> str:
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


def from_optional(
    value: T | None,
    reason: str = "值为 None",
) -> Gunmu[T]:
    if value is None:
        return Nothing(reason)

    return Some(value)
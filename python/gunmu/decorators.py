"""@gunmu 装饰器。

把返回 None 的函数自动包成 Nothing，返回正常值自动包成 Some。
也支持直接返回 Gunmu 的函数（原样透传）。
"""
from __future__ import annotations

import functools
import inspect
from typing import Any, Callable

from .core import Gunmu, Nothing, Some


def gunmu(
    reason: str | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Gunmu[Any]]]:
    """装饰器工厂。

    用法：
        @gunmu()
        def find(uid): ...

        @gunmu(reason="没查到")
        def find(uid): ...
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Gunmu[Any]]:
        default_reason = reason or f"{func.__name__} 返回了 None"

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Gunmu[Any]:
                result = await func(*args, **kwargs)
                return _wrap(result, default_reason)

            return async_wrapper  # type: ignore[return-value]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Gunmu[Any]:
            result = func(*args, **kwargs)
            return _wrap(result, default_reason)

        return wrapper

    return decorator


def _wrap(result: Any, reason: str) -> Gunmu[Any]:
    if isinstance(result, Gunmu):
        return result
    if result is None:
        return Nothing(reason)
    return Some(result)
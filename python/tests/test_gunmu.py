import pytest

from gunmu import GunmuError, from_optional, nothing, some


def test_some_basic():
    g = some(42)
    assert g.is_some()
    assert not g.is_nothing()
    assert g.unwrap() == 42
    assert bool(g) is True


def test_nothing_basic():
    g = nothing("用户不存在")
    assert g.is_nothing()
    assert not g.is_some()
    assert bool(g) is False
    assert g.reason() == "用户不存在"


def test_unwrap_nothing_raises():
    with pytest.raises(GunmuError) as exc:
        nothing("空").unwrap()
    assert "滚木" in str(exc.value)


def test_unwrap_or():
    assert nothing("空").unwrap_or(0) == 0
    assert some(1).unwrap_or(0) == 1


def test_unwrap_or_else():
    assert nothing("空").unwrap_or_else(lambda r: f"原因:{r}") == "原因:空"
    assert some(1).unwrap_or_else(lambda r: 0) == 1


def test_map():
    assert some(2).map(lambda x: x * 10).unwrap() == 20
    assert nothing("空").map(lambda x: x * 10).is_nothing()


def test_flat_map():
    def half(x: int):
        if x % 2 == 0:
            return some(x // 2)
        return nothing("奇数")

    assert some(4).flat_map(half).unwrap() == 2
    assert some(3).flat_map(half).is_nothing()
    assert nothing("空").flat_map(half).is_nothing()


def test_filter():
    assert some(4).filter(lambda x: x % 2 == 0).unwrap() == 4
    assert some(3).filter(lambda x: x % 2 == 0, "奇数").reason() == "奇数"
    assert nothing("空").filter(lambda x: True).is_nothing()


def test_match():
    result = some(1).match(
        some=lambda x: f"有 {x}",
        nothing=lambda r: f"滚木 {r}",
    )
    assert result == "有 1"

    result = nothing("空").match(
        some=lambda x: f"有 {x}",
        nothing=lambda r: f"滚木 {r}",
    )
    assert result == "滚木 空"


def test_iter():
    assert list(some(1)) == [1]
    assert list(nothing("空")) == []


def test_from_optional():
    assert from_optional(1).unwrap() == 1
    assert from_optional(None, "没查到").reason() == "没查到"


def test_repr():
    assert repr(some(1)) == "Some(1)"
    assert repr(nothing("空")) == "Nothing('空')"


def test_chaining():
    """真实场景：查用户 → 取名字 → 转大写 → 兜底。"""

    def find_user(uid: int):
        if uid == 1:
            return some({"name": "otto"})
        return nothing("用户不存在")

    assert (
        find_user(1)
        .map(lambda u: u["name"])
        .map(str.upper)
        .unwrap_or("匿名")
        == "OTTO"
    )

    assert (
        find_user(2)
        .map(lambda u: u["name"])
        .map(str.upper)
        .unwrap_or("匿名")
        == "匿名"
    )
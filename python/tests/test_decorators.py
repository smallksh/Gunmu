import pytest

from gunmu import gunmu, some, nothing


def test_gunmu_decorator_wraps_none():
    @gunmu()
    def find(uid: int):
        if uid == 1:
            return {"name": "otto"}
        return None

    assert find(1).unwrap() == {"name": "otto"}
    r = find(2)
    assert r.is_nothing()
    assert "find" in r.reason()


def test_gunmu_decorator_custom_reason():
    @gunmu(reason="用户不存在")
    def find(uid: int):
        return None

    assert find(1).reason() == "用户不存在"


def test_gunmu_decorator_passthrough():
    @gunmu()
    def find(uid: int):
        if uid == 1:
            return some("ok")
        return nothing("没有")

    assert find(1).unwrap() == "ok"
    assert find(2).reason() == "没有"


@pytest.mark.asyncio
async def test_gunmu_decorator_async():
    @gunmu()
    async def find(uid: int):
        if uid == 1:
            return "ok"
        return None

    assert (await find(1)).unwrap() == "ok"
    assert (await find(2)).is_nothing()
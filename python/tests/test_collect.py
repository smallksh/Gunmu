from gunmu import collect, collect_all, collect_dict, nothing, some


def test_collect_all_some():
    assert collect([some(1), some(2), some(3)]).unwrap() == [1, 2, 3]


def test_collect_fail_fast():
    r = collect([some(1), nothing("a"), nothing("b")])
    assert r.is_nothing()
    assert r.reason() == "a"


def test_collect_all_reasons():
    r = collect_all([some(1), nothing("a"), nothing("b")])
    assert r.reason() == "a; b"


def test_collect_dict():
    r = collect_dict({"name": some("otto"), "age": nothing("没填")})
    assert r.is_nothing()
    assert r.reason() == "age: 没填"

    r2 = collect_dict({"name": some("otto"), "age": some(18)})
    assert r2.unwrap() == {"name": "otto", "age": 18}
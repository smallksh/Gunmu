from gunmu import nothing, some, trace


def setup_function():
    trace.clear()
    trace.disable()


def teardown_function():
    trace.clear()
    trace.disable()


def test_trace_disabled_by_default():
    nothing("a")
    assert trace.records() == []


def test_trace_records_nothing():
    trace.enable()
    nothing("a")
    nothing("b")
    some(1)  # 不记录
    records = trace.records()
    assert len(records) == 2
    assert records[0][0] == "a"
    assert records[1][0] == "b"
    assert "test_trace.py" in records[0][1]


def test_trace_summary():
    trace.enable()
    nothing("a")
    nothing("a")
    nothing("b")
    s = trace.summary()
    assert s["total"] == 3
    assert s["by_reason"]["a"] == 2
    assert s["by_reason"]["b"] == 1


def test_trace_report():
    trace.enable()
    nothing("用户不存在")
    report = trace.report()
    assert "共 1 个滚木" in report
    assert "用户不存在" in report
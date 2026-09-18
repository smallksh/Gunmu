import { describe, it, expect, beforeEach } from "vitest";
import { nothing, some, trace } from "../gunmu/index.js";

beforeEach(() => {
  trace.clear();
  trace.disable();
});

describe("trace", () => {
  it("默认关闭", () => {
    nothing("a");
    expect(trace.records()).toEqual([]);
  });

  it("开启后记录 Nothing", () => {
    trace.enable();
    nothing("a");
    nothing("b");
    some(1);
    const rs = trace.records();
    expect(rs).toHaveLength(2);
    expect(rs[0]!.reason).toBe("a");
    expect(rs[1]!.reason).toBe("b");
  });

  it("summary 统计", () => {
    trace.enable();
    nothing("a");
    nothing("a");
    nothing("b");
    const s = trace.summary();
    expect(s.total).toBe(3);
    expect(s.byReason["a"]).toBe(2);
    expect(s.byReason["b"]).toBe(1);
  });

  it("report 输出", () => {
    trace.enable();
    nothing("用户不存在");
    const r = trace.report();
    expect(r).toContain("共 1 个滚木");
    expect(r).toContain("用户不存在");
  });
});
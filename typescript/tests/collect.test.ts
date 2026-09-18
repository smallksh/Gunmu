import { describe, it, expect } from "vitest";
import {
  collect,
  collectAll,
  collectDict,
  some,
  nothing,
  isNothing,
  unwrap,
  reason,
} from "../gunmu/index.js";

describe("collect", () => {
  it("全部 Some", () => {
    expect(unwrap(collect([some(1), some(2), some(3)]))).toEqual([1, 2, 3]);
  });

  it("fail-fast", () => {
    const r = collect([some(1), nothing("a"), nothing("b")]);
    expect(isNothing(r)).toBe(true);
    if (isNothing(r)) {
      expect(r.reason).toBe("a");
    }
  });
});

describe("collectAll", () => {
  it("收集所有原因", () => {
    const r = collectAll([some(1), nothing("a"), nothing("b")]);
    expect(reason(r)).toBe("a; b");
  });

  it("全部 Some", () => {
    expect(unwrap(collectAll([some(1), some(2)]))).toEqual([1, 2]);
  });
});

describe("collectDict", () => {
  it("fail-fast 带 key", () => {
    const r = collectDict({ name: some("otto"), age: nothing("没填") });
    expect(reason(r)).toBe("age: 没填");
  });

  it("全部 Some", () => {
    const r = collectDict({ name: some("otto"), age: some(18) });
    expect(unwrap(r)).toEqual({ name: "otto", age: 18 });
  });
});
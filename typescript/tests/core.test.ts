import { describe, it, expect } from "vitest";
import {
  some,
  nothing,
  fromOptional,
  isSome,
  isNothing,
  unwrap,
  unwrapOr,
  unwrapOrElse,
  map,
  flatMap,
  filter,
  match,
  reason,
  GunmuError,
} from "../gunmu/index.js";

describe("some / nothing", () => {
  it("some 有值", () => {
    const g = some(42);
    expect(isSome(g)).toBe(true);
    expect(isNothing(g)).toBe(false);
    if (isSome(g)) {
      expect(g.value).toBe(42);
    }
  });

  it("some(null) 是合法的 Some", () => {
    const g = some(null);
    expect(isSome(g)).toBe(true);
    if (isSome(g)) {
      expect(g.value).toBeNull();
    }
  });

  it("nothing 携带 reason", () => {
    const g = nothing("用户不存在");
    expect(isNothing(g)).toBe(true);
    if (isNothing(g)) {
      expect(g.reason).toBe("用户不存在");
    }
  });
});

describe("unwrap", () => {
  it("unwrap 从 Some 取值", () => {
    expect(unwrap(some(1))).toBe(1);
  });

  it("unwrap 从 Nothing 抛错", () => {
    expect(() => unwrap(nothing("空"))).toThrow(GunmuError);
  });

  it("unwrapOr 兜底", () => {
    expect(unwrapOr(nothing("空"), 0)).toBe(0);
    expect(unwrapOr(some(1), 0)).toBe(1);
  });

  it("unwrapOrElse 用 reason 计算", () => {
    expect(unwrapOrElse(nothing("空"), (r) => `原因:${r}`)).toBe("原因:空");
    expect(unwrapOrElse(some(1), () => 0)).toBe(1);
  });
});

describe("变换", () => {
  it("map", () => {
    expect(unwrap(map(some(2), (x) => x * 10))).toBe(20);
    expect(isNothing(map(nothing("空"), (x: number) => x * 10))).toBe(true);
  });

  it("flatMap", () => {
    const half = (x: number) =>
      x % 2 === 0 ? some(x / 2) : nothing("奇数");

    expect(unwrap(flatMap(some(4), half))).toBe(2);
    expect(isNothing(flatMap(some(3), half))).toBe(true);
    expect(isNothing(flatMap(nothing("空"), half))).toBe(true);
  });

  it("filter", () => {
    expect(unwrap(filter(some(4), (x) => x % 2 === 0))).toBe(4);
    expect(reason(filter(some(3), (x) => x % 2 === 0, "奇数"))).toBe("奇数");
    expect(isNothing(filter(nothing("空"), () => true))).toBe(true);
  });
});

describe("match", () => {
  it("处理 Some 和 Nothing", () => {
    expect(
      match(some(1), {
        some: (x) => `有 ${x}`,
        nothing: (r) => `滚木 ${r}`,
      }),
    ).toBe("有 1");

    expect(
      match(nothing("空"), {
        some: (x) => `有 ${x}`,
        nothing: (r) => `滚木 ${r}`,
      }),
    ).toBe("滚木 空");
  });
});

describe("fromOptional", () => {
  it("非空转 Some", () => {
    expect(unwrap(fromOptional(1))).toBe(1);
  });

  it("null 转 Nothing", () => {
    const g = fromOptional(null, "没查到");
    expect(isNothing(g)).toBe(true);
    expect(reason(g)).toBe("没查到");
  });

  it("undefined 转 Nothing", () => {
    expect(isNothing(fromOptional(undefined))).toBe(true);
  });
});

describe("类型收窄", () => {
  it("if 分支里类型自动变窄", () => {
    const g = some({ name: "otto" });
    if (isSome(g)) {
      expect(g.value.name).toBe("otto");
    }
  });
});
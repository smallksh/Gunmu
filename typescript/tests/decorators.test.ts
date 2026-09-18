import { describe, it, expect } from "vitest";
import {
  gunmu,
  isSome,
  isNothing,
  some,
  nothing,
  unwrap,
} from "../gunmu/index.js";

describe("@gunmu", () => {
  it("把返回 null 的函数包成 Nothing", async () => {
    const find = gunmu()(async (uid: number) => {
      if (uid === 1) {
        return { name: "otto" };
      }
      return null;
    });

    const r1 = await find(1);
    expect(isSome(r1)).toBe(true);
    if (isSome(r1)) {
      expect(r1.value).toEqual({ name: "otto" });
    }

    const r2 = await find(2);
    expect(isNothing(r2)).toBe(true);
  });

  it("自定义 reason", async () => {
    const find = gunmu("用户不存在")(async () => null);
    const r = await find();
    expect(isNothing(r)).toBe(true);
    if (isNothing(r)) {
      expect(r.reason).toBe("用户不存在");
    }
  });

  it("已经是 Gunmu 的返回值透传", async () => {
    const find = gunmu()(async (uid: number) => {
      if (uid === 1) {
        return some("ok");
      }
      return nothing("没有");
    });

    expect(unwrap(await find(1))).toBe("ok");
    const r = await find(2);
    expect(isNothing(r)).toBe(true);
    if (isNothing(r)) {
      expect(r.reason).toBe("没有");
    }
  });
});
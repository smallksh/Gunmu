/**
 * @gunmu 装饰器。
 *
 * 把返回 null / undefined 的函数自动包成 Nothing，
 * 返回正常值自动包成 Some。
 */

import { Gunmu, some, nothing } from "./core.js";

type AnyFn = (...args: any[]) => any;

export function gunmu(reason?: string) {
  return function decorator<F extends AnyFn>(
    fn: F,
  ): (...args: Parameters<F>) => Promise<Gunmu<Awaited<ReturnType<F>>>> {
    const defaultReason = reason ?? `${fn.name || "anonymous"} 返回了 null`;

    return async function wrapped(
      ...args: Parameters<F>
    ): Promise<Gunmu<Awaited<ReturnType<F>>>> {
      const result = await fn(...args);
      return wrap(result, defaultReason);
    };
  };
}

function wrap<T>(result: T, reason: string): Gunmu<T> {
  if (
    result !== null &&
    typeof result === "object" &&
    "kind" in result &&
    ((result as any).kind === "some" || (result as any).kind === "nothing")
  ) {
    return result as unknown as Gunmu<T>;
  }
  if (result === null || result === undefined) {
    return nothing(reason);
  }
  return some(result);
}
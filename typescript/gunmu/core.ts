/**
 * gunmu —— 显式空值处理。
 *
 * 滚木 = 值不存在。
 * 当你拿到一个 Gunmu，你必须处理它，不能假装它不存在。
 */

export interface Some<T> {
  readonly kind: "some";
  readonly value: T;
}

export interface Nothing {
  readonly kind: "nothing";
  readonly reason: string;
  readonly origin: string;
}

export type Gunmu<T> = Some<T> | Nothing;

// ---- 构造 ----

export function some<T>(value: T): Some<T> {
  return { kind: "some", value };
}

export function nothing(reason = "滚木"): Nothing {
  return {
    kind: "nothing",
    reason,
    origin: callerLocation(),
  };
}

export function fromOptional<T>(
  value: T | null | undefined,
  reason = "值为 null 或 undefined",
): Gunmu<T> {
  if (value === null || value === undefined) {
    return nothing(reason);
  }
  return some(value);
}

// ---- 判断 ----

export function isSome<T>(g: Gunmu<T>): g is Some<T> {
  return g.kind === "some";
}

export function isNothing<T>(g: Gunmu<T>): g is Nothing {
  return g.kind === "nothing";
}

// ---- 取值 ----

export class GunmuError extends Error {
  readonly reason: string;
  readonly origin: string;

  constructor(reason: string, origin = "") {
    const suffix = origin ? `（产生于 ${origin}）` : "";
    super(`滚木：${reason}${suffix}`);
    this.name = "GunmuError";
    this.reason = reason;
    this.origin = origin;
  }
}

export function unwrap<T>(g: Gunmu<T>): T {
  if (isSome(g)) {
    return g.value;
  }
  throw new GunmuError(g.reason, g.origin);
}

export function unwrapOr<T>(g: Gunmu<T>, defaultValue: T): T {
  return isSome(g) ? g.value : defaultValue;
}

export function unwrapOrElse<T>(g: Gunmu<T>, f: (reason: string) => T): T {
  return isSome(g) ? g.value : f(g.reason);
}

// ---- 变换 ----

export function map<T, U>(g: Gunmu<T>, f: (value: T) => U): Gunmu<U> {
  return isSome(g) ? some(f(g.value)) : g;
}

export function flatMap<T, U>(
  g: Gunmu<T>,
  f: (value: T) => Gunmu<U>,
): Gunmu<U> {
  return isSome(g) ? f(g.value) : g;
}

export function filter<T>(
  g: Gunmu<T>,
  predicate: (value: T) => boolean,
  reason = "不满足条件",
): Gunmu<T> {
  if (isNothing(g)) {
    return g;
  }
  return predicate(g.value) ? g : nothing(reason);
}

// ---- 强制处理 ----

export function match<T, U>(
  g: Gunmu<T>,
  handlers: {
    some: (value: T) => U;
    nothing: (reason: string) => U;
  },
): U {
  return isSome(g) ? handlers.some(g.value) : handlers.nothing(g.reason);
}

// ---- 原因 ----

export function reason(g: Gunmu<unknown>): string {
  return isNothing(g) ? g.reason : "";
}

// ---- 内部 ----

function callerLocation(): string {
  const stack = new Error().stack;
  if (!stack) {
    return "";
  }
  const lines = stack.split("\n");
  for (const line of lines) {
    if (line.includes("/gunmu/") || line.includes("gunmu/dist")) {
      continue;
    }
    const m =
      line.match(/\((.+):(\d+):(\d+)\)/) ?? line.match(/at (.+):(\d+):(\d+)/);
    if (m) {
      return `${m[1]}:${m[2]}`;
    }
  }
  return "";
}
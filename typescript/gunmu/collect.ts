/**
 * 把一组 Gunmu 收成一个 Gunmu<T[]>。
 */

import { Gunmu, some, nothing, isSome } from "./core.js";

export function collect<T>(items: Iterable<Gunmu<T>>): Gunmu<T[]> {
  const values: T[] = [];
  for (const item of items) {
    if (!isSome(item)) {
      return item;
    }
    values.push(item.value);
  }
  return some(values);
}

export function collectAll<T>(items: Iterable<Gunmu<T>>): Gunmu<T[]> {
  const values: T[] = [];
  const reasons: string[] = [];
  for (const item of items) {
    if (isSome(item)) {
      values.push(item.value);
    } else {
      reasons.push(item.reason);
    }
  }
  if (reasons.length > 0) {
    return nothing(reasons.join("; "));
  }
  return some(values);
}

export function collectDict<T>(
  map: Record<string, Gunmu<T>>,
): Gunmu<Record<string, T>> {
  const result: Record<string, T> = {};
  for (const [key, item] of Object.entries(map)) {
    if (isSome(item)) {
      result[key] = item.value;
    } else {
      return nothing(`${key}: ${item.reason}`);
    }
  }
  return some(result);
}
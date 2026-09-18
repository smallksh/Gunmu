export {
  GunmuError,
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
} from "./core.js";

export type { Gunmu, Some, Nothing } from "./core.js";

export { gunmu } from "./decorators.js";

export { collect, collectAll, collectDict } from "./collect.js";

export * as trace from "./trace.js";
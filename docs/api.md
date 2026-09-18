# API

跨语言统一 API。各语言命名风格不同，语义一致。

## Python

| 语义 | API |
|---|---|
| 构造有值 | `some(v)` |
| 构造滚木 | `nothing(reason)` |
| 从 Optional 转换 | `from_optional(v, reason)` |
| 判断有值 | `.is_some()` |
| 判断滚木 | `.is_nothing()` |
| 取值 | `.unwrap()` |
| 兜底 | `.unwrap_or(default)` |
| 兜底并计算 | `.unwrap_or_else(f)` |
| 映射 | `.map(f)` |
| 展平映射 | `.flat_map(f)` |
| 过滤 | `.filter(pred, reason)` |
| 强制处理 | `.match(some=, nothing=)` |
| 原因 | `.reason()` |
| 装饰器 | `@gunmu(reason?)` |
| 收集 | `collect([...])` |
| 收集所有原因 | `collect_all([...])` |
| 收集 dict | `collect_dict({...})` |
| 追踪 | `trace.enable()` / `trace.report()` |

## TypeScript

| 语义 | API |
|---|---|
| 构造有值 | `some(v)` |
| 构造滚木 | `nothing(reason)` |
| 从 Optional 转换 | `fromOptional(v, reason)` |
| 判断有值 | `isSome(g)` |
| 判断滚木 | `isNothing(g)` |
| 取值 | `unwrap(g)` |
| 兜底 | `unwrapOr(g, default)` |
| 兜底并计算 | `unwrapOrElse(g, f)` |
| 映射 | `map(g, f)` |
| 展平映射 | `flatMap(g, f)` |
| 过滤 | `filter(g, pred, reason)` |
| 强制处理 | `match(g, { some, nothing })` |
| 原因 | `reason(g)` |
| 装饰器 | `gunmu(reason?)(fn)` |
| 收集 | `collect([...])` |
| 收集所有原因 | `collectAll([...])` |
| 收集 dict | `collectDict({...})` |
| 追踪 | `trace.enable()` / `trace.report()` |
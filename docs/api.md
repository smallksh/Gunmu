# API

跨语言统一 API。目前只有 Python 实现。

| 语义 | Python |
|---|---|
| 构造有值 | `some(1)` |
| 构造滚木 | `nothing("原因")` |
| 取值 | `.unwrap()` |
| 兜底 | `.unwrap_or(0)` |
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
# 滚木语义规范 v0.2

所有语言实现必须遵守本规范，保证跨语言语义一致。

## 1. 类型

- `Gunmu<T>`：抽象类型，表示“可能有值，可能是滚木”
- `Some<T>`：有值
- `Nothing`：滚木，必须携带 reason

## 2. 必须实现的方法

| 方法 | 语义 |
|---|---|
| `is_some()` | 是否有值 |
| `is_nothing()` | 是否滚木 |
| `unwrap()` | 取值，滚木则抛错 |
| `unwrap_or(default)` | 取值，滚木则返回 default |
| `unwrap_or_else(f)` | 取值，滚木则调用 f(reason) |
| `map(f)` | 映射，滚木则跳过 |
| `flat_map(f)` | 映射并展平 |
| `filter(pred, reason)` | 过滤，不满足则变滚木 |
| `match({some, nothing})` | 强制处理两种分支 |
| `reason()` | 返回滚木原因，Some 返回空 |

## 3. 必须实现的函数

- `some(v)` / `nothing(reason)`
- `from_optional(v, reason)`
- `collect(items)` / `collect_all(items)` / `collect_dict(map)`

## 4. 必须实现的装饰器 / 包装

- `gunmu(reason?)`：把返回 None/null/nil 的函数自动包成 Nothing
- 各语言对应异步版本

## 5. 必须实现的追踪

- `trace.enable()` / `disable()` / `clear()`
- `trace.records()` / `summary()` / `report()`
- 默认关闭，零开销

## 6. 命名约定

- 类型名：`Gunmu` / `Some` / `Nothing`
- 函数名：`some` / `nothing`
- reason 默认值：各语言用本地化文案，中文环境用“滚木”
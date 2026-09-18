# 滚木

> 显式空值处理。滚木 = 值不存在。

## 语言

| 语言 | 版本 | 安装 | 目录 |
|---|---|---|---|
| Python | 0.3.0 | `pip install gunmu` | [`python/`](./python) |
| TypeScript | 0.1.0 | `npm i gunmu` | [`typescript/`](./typescript) |

## 语义规范

所有语言实现必须遵守 [`SPEC.md`](./SPEC.md)。

## 快速示例

### Python

```python
from gunmu import some, nothing, gunmu

@gunmu(reason="用户不存在")
def find_user(uid: int):
    if uid == 1:
        return {"name": "otto"}
    return None

find_user(1).match(
    some=lambda u: print(f"找到 {u['name']}"),
    nothing=lambda r: print(f"滚木：{r}"),
)
# 找到 otto

find_user(2).match(
    some=lambda u: print(f"找到 {u['name']}"),
    nothing=lambda r: print(f"滚木：{r}"),
)
# 滚木：用户不存在
```

### TypeScript

```ts
import { some, nothing, isSome, match } from "gunmu";

function findUser(uid: number) {
  if (uid === 1) {
    return some({ name: "otto" });
  }
  return nothing("用户不存在");
}

// 方式一：类型收窄
const r = findUser(1);
if (isSome(r)) {
  console.log(r.value.name); // TS 知道这里有值
} else {
  console.log(r.reason);
}

// 方式二：match
match(findUser(2), {
  some: (u) => console.log(`找到 ${u.name}`),
  nothing: (r) => console.log(`滚木：${r}`),
});
```

## 目录

| 路径 | 说明 |
|---|---|
| [`python/`](./python) | Python 实现 |
| [`typescript/`](./typescript) | TypeScript 实现 |
| [`docs/`](./docs) | 语义文档 |
| [`SPEC.md`](./SPEC.md) | 跨语言语义规范 |

## License

MIT License © 2026 smallksh
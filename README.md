# 滚木

> 显式空值处理。滚木 = 值不存在。

目前提供 Python 实现。目录结构为多语言预留。

## 安装

```bash
pip install gunmu
```

## 快速示例

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

## 语义规范

所有语言实现必须遵守 [`SPEC.md`](./SPEC.md)。

## 目录

| 路径 | 说明 |
|---|---|
| [`python/`](./python) | Python 实现 |
| [`docs/`](./docs) | 语义文档 |
| [`SPEC.md`](./SPEC.md) | 跨语言语义规范 |

## License

MIT License © 2026 smallksh
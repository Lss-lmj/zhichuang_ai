# 生成样例：代码实操案例

## 任务：实现一个最小 Markdown 检索器

目标：

输入一个问题，从 Markdown 文档片段中找出最相关的 3 个片段。

伪代码：

```python
def search_chunks(query: str, chunks: list[dict]) -> list[dict]:
    query_terms = set(query.lower().split())
    scored = []
    for chunk in chunks:
        text = chunk["text"].lower()
        score = sum(1 for term in query_terms if term in text)
        scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored[:3] if score > 0]
```

改进方向：

1. 支持中文分词。
2. 增加标题权重。
3. 增加向量检索。
4. 返回引用路径和更新时间。

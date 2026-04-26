"""
第三章 3.2.2 文档切分 — 基于文档结构的Markdown标题切分示例

【章节学习重点】
- MarkdownHeaderTextSplitter 的使用：按 Markdown 标题层级切分文档
- 基于文档结构的切分策略：利用标题层级保持语义完整性
- metadata 中标题层级信息的保留：每个块自动附带所属标题链

【代码功能】
演示如何使用 MarkdownHeaderTextSplitter 按 Markdown 标题层级（H1/H2/H3）切分文档。
切分后的每个 Document 会自动在 metadata 中记录其所属的各级标题信息，
便于后续检索时提供上下文定位。

【实现思路】
1. 准备 Markdown 格式的文本内容
2. 配置要追踪的标题层级（headers_to_split_on）
3. 创建 MarkdownHeaderTextSplitter 实例
4. 调用 split_text() 方法进行切分
5. 输出每个块的 metadata（标题链）和内容

【关键参数说明】
- headers_to_split_on: 要追踪的标题层级列表，格式为 [("#", "level_1"), ("##", "level_2"), ...]
  键为 Markdown 标题符号，值为 metadata 中对应的字段名
- strip_headers: 是否从内容中移除标题文本，默认 True
- split_text(): 切分方法，注意此方法接受纯文本而非 Document 列表
- metadata: 每个块自动包含其所属标题链，如 {"level_1": "产品使用手册", "level_2": "一、快速开始"}

【应用场景】
- 技术文档、使用手册等结构化 Markdown 文档的切分
- 需要保留标题层级信息以便精确定位的场景
- 文档有明确章节结构时，比按长度切分更能保持语义完整性
"""
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_text = """
# 产品使用手册

## 一、快速开始
这里介绍如何快速完成安装与登录。

### 1.1 安装步骤
详细安装步骤说明……

### 1.2 首次登录
首次登录需要注意的事项……

## 二、高级功能
这里是高级功能的概览。

### 2.1 自动化规则
如何配置自动化规则……

### 2.2 报表分析
如何查看和定制报表……
"""

headers_to_split_on = [
    ("#", "level_1"),
    ("##", "level_2"),
    ("###", "level_3"),
]

md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=True,
)

md_docs = md_splitter.split_text(markdown_text)

for i, d in enumerate(md_docs[:4], start=1):
    print(f"--- Chunk {i} ---")
    print(d.metadata)
    print(d.page_content[:80])

"""
第三章 3.2.2 文档切分 — 基于文本结构的递归切分示例

【章节学习重点】
- RecursiveCharacterTextSplitter 的使用：按分隔符层级递归切分
- 递归切分的优势：优先在段落、句子等自然边界处切分，保持语义完整性
- add_start_index 参数的作用：记录每个块在原文中的起始位置

【代码功能】
演示如何使用 RecursiveCharacterTextSplitter 对 PDF 文档进行递归切分。
该切分器会按分隔符优先级（段落→换行→句号→逗号→空格）逐级尝试切分，
尽可能在自然语义边界处分割文本。

【实现思路】
1. 使用 PyPDFLoader 加载 PDF 文件
2. 创建 RecursiveCharacterTextSplitter，配置块大小和重叠
3. 调用 split_documents() 方法进行递归切分
4. 输出原始文档数和切分后的块数对比

【关键参数说明】
- chunk_size: 每个块的最大字符数，默认500
- chunk_overlap: 相邻块之间的重叠字符数，默认50
- add_start_index: 是否记录每个块在原文中的起始位置，便于溯源
- separators: 可选的自定义分隔符列表，按优先级从高到低排列
  默认为 ["\\n\\n", "\\n", " ", ""]，中文场景可添加 ["。", "！", "？"] 等

【应用场景】
- 中文文档的智能切分，优先在句号、感叹号等处断句
- 需要保持段落完整性的文档切分场景
- 比固定长度切分更智能的选择，适合大多数 RAG 应用
"""
from typing import List
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = Path(__file__).resolve().parent / "files" / "XX销售有限公司员工守则.pdf"
if not file_path.exists():
    raise FileNotFoundError(
        f"未找到 PDF 文件：{file_path}\n"
        "请确认已在当前目录下创建 files/XX销售有限公司员工守则.pdf"
    )

loader = PyPDFLoader(str(file_path))

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

splits: List[Document] = text_splitter.split_documents(docs)

print(f"原始文档数量: {len(docs)}")
print(f"切分之后的文档块数量: {len(splits)}")

print("-"*100)
for split in splits:
    print(split.page_content[:100])
    print("-"*100)
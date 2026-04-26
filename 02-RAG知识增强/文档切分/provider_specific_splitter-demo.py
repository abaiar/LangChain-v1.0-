"""
第三章 3.2.2 文档切分 — 基于模型提供方的语义切分示例

【章节学习重点】
- WriterTextSplitter 的使用：基于 LLM 的语义感知切分
- 语义切分 vs 规则切分的区别：语义切分能理解文本含义，在语义边界处切分
- 不同切分策略的选择：llm_split（精确）/ fast_split（快速）/ hybrid_split（混合）

【代码功能】
演示如何使用 WriterTextSplitter（Writer AI 提供的语义切分器）对 PDF 文档进行切分。
该切分器利用 LLM 理解文本语义，在语义边界处进行切分，比规则切分更智能。

【实现思路】
1. 使用 PyPDFLoader 加载 PDF 文件
2. 合并所有页面的文本内容和元数据
3. 创建 WriterTextSplitter，选择切分策略
4. 调用 split_text() 方法进行语义切分
5. 手动创建 Document 对象列表（WriterTextSplitter 返回纯文本列表）

【关键参数说明】
- api_key: Writer AI 的 API 密钥
- strategy: 切分策略
  - "llm_split"：使用 LLM 进行精确语义分段，质量最高但速度最慢
  - "fast_split"：快速语义分段，速度较快
  - "hybrid_split"：混合策略，兼顾质量和速度
- split_text(): 返回纯文本列表，需手动封装为 Document 对象

【应用场景】
- 对切分质量要求较高的场景（如法律文档、技术规范）
- 文档语义结构复杂，规则切分难以保持语义完整性
- 需要避免在句子中间或语义不完整处切分的场景
"""
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_writer.text_splitter import WriterTextSplitter
from langchain_core.documents import Document


file_path = Path(__file__).resolve().parent / "files" / "XX销售有限公司员工守则.pdf"
if not file_path.exists():
    raise FileNotFoundError(
        f"未找到 PDF 文件：{file_path}\n"
        "请确认已在当前目录下创建 files/XX销售有限公司员工守则.pdf"
    )

loader = PyPDFLoader(str(file_path))

docs = loader.load()

combined_text = "\n\n".join([doc.page_content for doc in docs])
base_metadata = docs[0].metadata if docs else {}

splitter = WriterTextSplitter(
    api_key="xxxxxx",
    strategy="fast_split",
)

text_chunks = splitter.split_text(combined_text)

chunks = [Document(page_content=text, metadata=base_metadata) for text in text_chunks]

print(f"WRITER 返回的 chunk 数量: {len(chunks)}")
print("-"*100)
for chunk in chunks:
    print(chunk.metadata)
    print(chunk.page_content[:100])
    print("-"*100)

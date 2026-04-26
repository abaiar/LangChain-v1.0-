"""
第三章 3.2.2 文档切分 — 基于长度的文本切分示例

【章节学习重点】
- CharacterTextSplitter 的使用：基于字符数/token数进行文本切分
- tiktoken 编码器的集成：通过 from_tiktoken_encoder 方法按 token 数切分
- chunk_size 和 chunk_overlap 参数的作用与选择原则

【代码功能】
演示如何使用 CharacterTextSplitter 配合 tiktoken 编码器对 PDF 文档进行切分。
先加载 PDF 文档，然后按 token 数将长文档切分为多个固定大小的块。

【实现思路】
1. 使用 PyPDFLoader 加载 PDF 文件
2. 创建 CharacterTextSplitter，使用 tiktoken 编码器按 token 数切分
3. 调用 split_documents() 方法对文档进行切分
4. 输出切分后的文档块数量和内容摘要

【关键参数说明】
- encoding_name: tiktoken 编码器名称，"cl100k_base" 是 GPT-4/3.5 使用的编码
- chunk_size: 每个文档块的最大 token 数，通常设为 500-1000
- chunk_overlap: 相邻块之间的重叠 token 数，用于保留边界处的上下文信息，通常为 chunk_size 的 10%-20%
- split_documents(): 切分方法，保留原始 Document 的 metadata

【应用场景】
- RAG 系统中对长文档进行预处理，生成适合向量化的文档块
- 控制每个文档块的大小，避免超过 Embedding 模型的输入限制
- 通过 chunk_overlap 保留跨块边界的语义连续性
"""
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

file_path = Path(__file__).resolve().parent / "files" / "XX销售有限公司员工守则.pdf"
if not file_path.exists():
    raise FileNotFoundError(
        f"未找到 PDF 文件：{file_path}\n"
        "请确认已在当前目录下创建 files/XX销售有限公司员工守则.pdf"
    )

loader = PyPDFLoader(str(file_path))

docs = loader.load()

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=500,
    chunk_overlap=50
)
texts = text_splitter.split_documents(docs)

print(f"共分割到 {len(texts)} 个 Chunk")
print("-"*100)
for text in texts:
    print(text.page_content[:100])
    print("-"*100)
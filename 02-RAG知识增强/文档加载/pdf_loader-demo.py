"""
第三章 3.2.1 文档加载 — PDF文档加载示例

【章节学习重点】
- PyPDFLoader 的使用：LangChain 中最常用的 PDF 文档加载器
- Document 对象的结构：page_content（文本内容）和 metadata（元数据）
- PDF 文档按页加载的特性：每页生成一个独立的 Document 对象

【代码功能】
演示如何使用 PyPDFLoader 加载 PDF 文件，将其转换为 LangChain 的 Document 对象列表。
每个 Document 包含该页的文本内容和元数据（如页码、来源文件等）。

【实现思路】
1. 导入 PyPDFLoader 类
2. 指定 PDF 文件路径
3. 创建 loader 实例并调用 load() 方法加载文档
4. 遍历输出每个 Document 的元数据和内容摘要

【关键参数说明】
- file_path: PDF 文件的路径（相对路径或绝对路径）
- loader.load(): 加载方法，返回 List[Document]，每个 Document 对应 PDF 的一页
- doc.metadata: 文档元数据，包含 source（文件路径）和 page（页码）等信息
- doc.page_content: 该页的纯文本内容

【应用场景】
- RAG 系统中加载企业文档（规章制度、合同、报告等）
- 知识库构建的第一步：将非结构化 PDF 转为可处理的 Document 对象
- 配合文本切分器进一步处理，生成适合向量化的文档块
"""
from langchain_community.document_loaders import PyPDFLoader

file_path = "files/XX销售有限公司员工守则.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

print(f"共加载到 {len(docs)} 个 Document")

print("-"*100)

for doc in docs:
    print(doc.metadata)
    print(doc.page_content[:100])
    print("-"*100)


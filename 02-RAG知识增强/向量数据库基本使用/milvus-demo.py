"""
第三章 3.3.3 向量数据库的基本使用 — Milvus 向量数据库完整示例

【章节学习重点】
- Milvus 向量数据库的连接与使用：LangChain 集成 Milvus 的完整流程
- 向量数据库的核心操作：创建集合、写入数据、相似度检索
- 从文档加载到向量检索的完整 RAG 数据流

【代码功能】
演示从 PDF 文档加载到 Milvus 向量数据库写入和检索的完整流程。
包括：PDF加载 → 文本切分 → 向量化 → 写入Milvus → 验证 → 相似度检索。

【实现思路】
1. 使用 PyPDFLoader 加载 PDF 文件
2. 使用 RecursiveCharacterTextSplitter 切分文档（中文分隔符优化）
3. 初始化 DashScope Embedding 模型
4. 清理旧 Collection（避免重复数据）
5. 创建 Milvus 向量存储实例并写入数据
6. 验证数据插入是否成功
7. 执行相似度检索测试

【关键参数说明】
- Milvus(): LangChain 的 Milvus 封装类
  - embedding_function: Embedding 模型实例
  - collection_name: 集合名称，类似数据库表名
  - connection_args: 连接参数，uri 为 Milvus 服务地址
  - index_params: 索引参数
    - index_type: "FLAT" 为暴力搜索索引，适合小数据量；大数据量可用 "IVF_FLAT" 等
    - metric_type: "L2" 为欧氏距离，也可选 "IP"（内积）或 "COSINE"（余弦相似度）
- similarity_search(query, k): 相似度检索，k 为返回结果数
- URI: Milvus 服务地址，默认端口 19530

【应用场景】
- 企业知识库的持久化存储和检索
- 生产环境 RAG 系统的向量数据库选型
- 需要高性能向量检索的大规模文档管理
"""
import time
from pathlib import Path
from pymilvus import connections, utility, Collection
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_milvus import Milvus

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
    separators=["\n\n", "\n", "。", "！", "？"]
)
split_docs = text_splitter.split_documents(docs)

print(f"文档切分完成，共 {len(split_docs)} 个文档块")

embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key="xxxxxx"
)

try:
    URI = "http://localhost:19530"
    if not connections.has_connection("default"):
        connections.connect("default", uri=URI)
    utility.drop_collection("employee_handbook")
    print("已删除旧的 collection: employee_handbook")
except Exception as e:
    print(f"删除 collection 时出错（可能本就不存在，忽略继续）: {e}")

vector_store = Milvus(
    embedding_function=embeddings,
    collection_name="employee_handbook",
    connection_args={"uri": "http://localhost:19530"},
    index_params={"index_type": "FLAT", "metric_type": "L2"},
)

ids = vector_store.add_documents(split_docs)

print(f"数据已插入到 Milvus，共写入 {len(ids)} 条")

try:
    collection = Collection("employee_handbook")
    collection.load()
    
    collection.flush()
    time.sleep(0.5)
    
    num_entities = collection.num_entities
    print(f"✓ 验证：Collection 中包含 {num_entities} 条数据")
    
    if num_entities == len(split_docs):
        print(f"✓ 插入成功！数据条数匹配（期望 {len(split_docs)} 条，实际 {num_entities} 条）")
    elif num_entities > 0:
        print(f"⚠ 数据已插入，但数量不匹配（期望 {len(split_docs)} 条，实际 {num_entities} 条）")
    else:
        print("⚠ Collection 数量为 0，但数据可能在内存中（将通过查询验证）")
        
except Exception as e:
    print(f"⚠ 验证时出错: {e}")

query = "公司对迟到、早退是如何处理的？"
results = vector_store.similarity_search(query, k=3)

print(f"\n查询：{query}")
print(f"找到 {len(results)} 条相关结果：\n")

if len(results) > 0:
    print("✓ 查询成功，数据可用！插入验证通过")
    for i, doc in enumerate(results, 1):
        print(f"--- 结果 {i} ---")
        print(doc.page_content[:200])
        print()
else:
    print("✗ 警告：查询没有返回结果，数据可能未正确插入")

"""
第三章 3.2.4 文档检索（Retrieval）— 基于向量相似度的文档检索示例

【章节学习重点】
- InMemoryVectorStore 的使用：LangChain 内置的内存向量存储
- 相似度检索的原理：将查询向量化后与文档向量计算余弦相似度，返回最相关的文档
- similarity_search 方法的使用与参数配置

【代码功能】
演示如何使用 InMemoryVectorStore 构建一个完整的文档检索流程：
文档准备 → 向量化 → 存储 → 相似度检索。
使用员工守则文档作为示例数据，展示从写入到检索的完整流程。

【实现思路】
1. 准备几条"员工守则"文档，封装为 Document 对象（含 page_content 和 metadata）
2. 配置 DashScope Embedding 模型
3. 初始化 InMemoryVectorStore 并写入文档
4. 使用 similarity_search() 进行相似度检索
5. 输出检索结果

【关键参数说明】
- InMemoryVectorStore(embeddings): 创建内存向量存储，传入 Embedding 模型实例
- add_documents(): 将文档列表写入向量存储，内部自动调用 embed_documents 进行向量化
- similarity_search(query, k): 相似度检索
  - query: 查询文本
  - k: 返回最相似的 k 个文档，默认4
- Document: LangChain 文档对象，包含 page_content（文本内容）和 metadata（元数据）

【应用场景】
- RAG 系统中的文档检索环节
- 快速原型验证：InMemoryVectorStore 无需外部数据库，适合开发调试
- 生产环境应替换为 Milvus、Pinecone 等持久化向量数据库
"""
from typing import List
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings

docs: List[Document] = [
    Document(
        page_content=(
            "公司要求全体员工遵守考勤制度，按时上下班。"
            "对于迟到、早退的员工，将视次数和情节轻重给予口头提醒、书面警告或绩效扣分。"
        ),
        metadata={"section": "考勤与纪律"},
    ),
    Document(
        page_content=(
            "员工在对外邮件和客户沟通中必须使用公司统一的邮件签名模板，"
            "严禁通过个人邮箱发送包含客户隐私或商业机密的信息。"
        ),
        metadata={"section": "对外沟通与信息安全"},
    ),
    Document(
        page_content=(
            "员工必须遵守信息安全制度，不得随意使用个人U盘等外部存储设备，"
            "不得将内部资料拷贝至非授权设备。"
        ),
        metadata={"section": "设备与资料管理"},
    ),
]

embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key="xxxxxx",
)

vector_store = InMemoryVectorStore(embeddings)

ids = vector_store.add_documents(documents=docs)
print(f"已写入 {len(ids)} 条文档到 InMemoryVectorStore")

query = "公司对迟到早退有什么处罚规定？"

results: List[Document] = vector_store.similarity_search(
    query,
    k=2,
)

print(f"\n查询：{query}")
print("检索到的相关条款：")
for i, doc in enumerate(results, start=1):
    print(f"\n--- 结果 {i} ---")
    print(doc.page_content)
    print(f"metadata: {doc.metadata}")

"""
第三章 3.2.1 文档加载 — Notion数据库加载示例

【章节学习重点】
- NotionDBLoader 的使用：从 Notion 数据库加载文档
- Notion API 的集成方式：通过 Integration Token 和 Database ID 连接
- 不同数据源的文档加载器统一接口：load() 方法返回 List[Document]

【代码功能】
演示如何使用 NotionDBLoader 从 Notion 数据库加载文档，
将 Notion 页面转换为 LangChain 的 Document 对象列表。

【实现思路】
1. 导入 NotionDBLoader 类
2. 配置 Notion API 凭证和数据库 ID
3. 创建 loader 实例并调用 load() 方法
4. 遍历输出每个 Document 的元数据和内容摘要

【关键参数说明】
- integration_token: Notion Integration 的访问令牌，需在 Notion 中创建 Integration 后获取
- database_id: Notion 数据库的唯一标识符，可从数据库 URL 中获取
- request_timeout_sec: 请求超时时间（秒），默认30秒，网络较慢时可适当增大

【应用场景】
- 从企业 Notion 知识库中批量加载文档用于 RAG
- 将团队协作文档纳入智能体知识体系
- 定期同步 Notion 数据库内容到向量数据库
"""
from langchain_community.document_loaders import NotionDBLoader

loader = NotionDBLoader(
    integration_token="xxxxxx",
    database_id="xxxxxx",
    request_timeout_sec=30,
)

docs = loader.load()

print(f"共从 Notion 数据库加载到 {len(docs)} 个 Document")

print("-"*100)

for doc in docs:
    print(doc.metadata)
    print(doc.page_content[:100])
    print("-"*100)
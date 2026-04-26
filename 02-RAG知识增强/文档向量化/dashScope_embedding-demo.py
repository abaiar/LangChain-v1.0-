"""
第三章 3.2.3 文档向量化（Embedding）— DashScope Embedding 示例

【章节学习重点】
- Embedding 的概念：将文本转换为高维向量，使语义相似的文本在向量空间中距离更近
- DashScopeEmbeddings 的使用：阿里通义千问提供的文本向量化模型
- embed_documents 和 embed_query 的区别：文档向量化 vs 查询向量化

【代码功能】
演示如何使用 DashScopeEmbeddings（通义千问 text-embedding-v4 模型）对文本进行向量化。
分别展示文档文本和查询文本的向量化过程，输出向量维度和部分向量值。

【实现思路】
1. 准备一段原始文档文本
2. 配置 DashScope Embedding 模型
3. 使用 embed_documents() 对文档文本进行向量化
4. 使用 embed_query() 对查询文本进行向量化
5. 输出向量维度和前10个向量值

【关键参数说明】
- model: Embedding 模型名称，"text-embedding-v4" 是通义千问最新的向量模型
- dashscope_api_key: 阿里云 DashScope API 密钥
- embed_documents(): 对文档列表进行向量化，输入为 List[str]，返回 List[List[float]]
- embed_query(): 对查询文本进行向量化，输入为 str，返回 List[float]
- 向量维度: text-embedding-v4 输出 1024 维向量

【应用场景】
- RAG 系统中将文档块转换为向量存入向量数据库
- 语义搜索：将用户查询向量化后与文档向量进行相似度匹配
- 文本聚类和分类：基于向量距离进行语义分析
"""
from langchain_community.embeddings import DashScopeEmbeddings

document_text = """
XX销售有限公司员工守则：
公司要求全体员工遵守职业行为规范，包括准时上下班、客户接待礼仪、
办公环境维护、信息保密义务、安全生产责任制度等。
违反规定将根据情节轻重给予警告、记过、停职直至解除劳动合同的处理。
"""

embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key="xxxxxx"
)

doc_embedding = embeddings.embed_documents([document_text])[0]

print(f"文档向量维度：{len(doc_embedding)}")
print(f"前 10 个向量值：{doc_embedding[:10]}")

query = "公司的迟到早退处罚规则是什么？"
query_embedding = embeddings.embed_query(query)

print(f"查询向量维度：{len(query_embedding)}")
print(f"前 10 个向量值：{query_embedding[:10]}")

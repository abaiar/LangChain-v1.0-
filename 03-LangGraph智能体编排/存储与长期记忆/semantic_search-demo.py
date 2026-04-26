"""
第四章 4.3.3 存储与长期记忆 — 基于语义搜索的长期记忆示例

【章节学习重点】
- InMemoryStore 配合 Embedding 实现语义搜索
- 语义搜索 vs 关键词搜索的区别：语义搜索理解查询含义，而非简单匹配关键词
- Store 在图节点中的注入使用：通过 store 参数自动注入

【代码功能】
演示如何使用 InMemoryStore 配合 DashScopeEmbeddings 实现语义搜索。
在图节点中通过 store 参数注入存储实例，根据用户查询语义检索相关记忆，
并将检索到的记忆注入系统提示词中。

【实现思路】
1. 初始化 LLM 模型和 Embedding 模型
2. 创建带索引的 InMemoryStore（配置 embed 和 dims）
3. 预存一些用户记忆数据
4. 定义 chat 节点，通过 store 参数注入存储实例
5. 在节点内使用 store.search() 进行语义搜索
6. 将检索到的记忆注入系统提示词
7. 编译图时传入 store 参数

【关键参数说明】
- InMemoryStore(index={"embed": embeddings, "dims": 1536}): 带语义索引的存储
- store.search(namespace, query=..., limit=1): 语义搜索，query为查询文本
- builder.compile(store=store): 编译图时注入存储实例
- MessagesState: 内置消息状态类型，自动管理消息列表

【应用场景】
- 智能助手的个性化记忆系统
- 基于语义的用户偏好检索
- RAG 场景中结合长期记忆和实时对话
"""
from langchain_community.embeddings import DashScopeEmbeddings
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.graph import START, MessagesState, StateGraph
import uuid

# ========== 1. 初始化模型 ==========
model = init_chat_model(
    model="qwen-plus",
    temperature=0.7,
    api_key="xxxxxx",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model_provider="openai"
)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key="xxxxxx"
)

# ========== 2. 配置语义搜索存储 ==========
store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1536
    }
)

user_id = "user_001"
namespace_for_memory = (user_id, "memories")

store.put(namespace_for_memory, str(uuid.uuid4()), {"text": "我喜欢苹果"})
store.put(namespace_for_memory, str(uuid.uuid4()), {"text": "我是张三"})

# ========== 3. 定义节点 ==========
def chat(state, *, store: BaseStore):
    """使用语义搜索检索相关记忆"""
    items = store.search(
        namespace_for_memory, 
        query=state["messages"][-1].content,
        limit=1
    )
    
    memories = "\n".join(item.value["text"] for item in items)
    memories = f"## 用户记忆\n{memories}" if memories else ""
    
    response = model.invoke(
        [
            SystemMessage(content=f"你是一个帮助用户解决问题的助手。\n{memories}"),
            *state["messages"],
        ]
    )
    return {"messages": [response]}

# ========== 4. 构建图 ==========
builder = StateGraph(MessagesState)
builder.add_node(chat)
builder.add_edge(START, "chat")
graph = builder.compile(store=store)

# ========== 5. 执行 ==========
if __name__ == "__main__":
    for message, metadata in graph.stream(
        input={"messages": [HumanMessage(content="我饿了")]},
        stream_mode="messages",
    ):
        print(message.content, end="")

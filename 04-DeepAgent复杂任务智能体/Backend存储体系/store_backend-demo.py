"""
第五章 5.3.1 Backend存储体系 — StoreBackend 存储后端示例

【章节学习重点】
- StoreBackend 的概念：将 Agent 的键值存储持久化到指定后端
- StoreBackend 与 InMemoryStore 的关系：StoreBackend 是 InMemoryStore 的持久化包装

【代码功能】
演示 StoreBackend 的使用，将 Deep Agent 的键值存储持久化。

【关键参数说明】
- StoreBackend: 存储后端，负责键值数据的持久化
- InMemoryStore: 内存键值存储，StoreBackend 对其进行包装

【应用场景】
- Agent 长期记忆的持久化
- 跨会话共享键值数据
"""
from deepagents import create_deep_agent
from deepagents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore
from langchain_deepseek import ChatDeepSeek

# 初始化 DeepSeek 模型
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key="xxxxxx",
    temperature=0.3,
)
store = InMemoryStore()

agent = create_deep_agent(
    model=llm,
    backend=lambda rt: StoreBackend(rt),
    store=store,
    system_prompt="""
你有一个可持久化的文件系统。
请将用户的偏好信息写入 /profile/preferences.txt，
后续对话可以读取这个文件以保持一致的风格。
"""
)

# 第一次，在 thread A 里写入偏好
config_a = {"configurable": {"thread_id": "user-001-session-A"}}

result1 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "我喜欢回答风格简洁、有条理，并尽量使用列表。",
            }
        ]
    },
    config=config_a,
)

print("【第一次写入偏好】")
print(result1["messages"][-1].content)

# 第二次，在 thread B 里读取同一个文件，验证跨线程持久化
config_b = {"configurable": {"thread_id": "user-001-session-B"}}

result2 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "现在请根据你之前记录的我的偏好，回答：什么是 Deep Agents？",
            }
        ]
    },
    config=config_b,
)

print("\n【跨线程读取偏好后的回答】")
print(result2["messages"][-1].content)

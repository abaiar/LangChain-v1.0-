"""
第五章 5.3.1 Backend存储体系 — CompositeBackend 组合后端示例

【章节学习重点】
- CompositeBackend 的概念：组合多种后端，实现分层持久化策略
- 后端组合的设计模式：状态后端+存储后端+文件系统后端的灵活搭配

【代码功能】
演示 CompositeBackend 的使用，将 StateBackend、StoreBackend、FilesystemBackend
组合为一个统一的后端，实现分层持久化。

【关键参数说明】
- CompositeBackend: 组合后端，将多个 Backend 组合为一个
- StateBackend + StoreBackend + FilesystemBackend: 典型的三层后端组合

【应用场景】
- 生产环境的分层持久化策略
- 需要同时持久化状态、存储和文件的场景
"""
import os
from deepagents import create_deep_agent
from deepagents.backends import (
    CompositeBackend,
    StateBackend,
    StoreBackend,
    FilesystemBackend,
)
from langgraph.store.memory import InMemoryStore
from langchain_deepseek import ChatDeepSeek

# 初始化 DeepSeek 模型
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key="xxxxxx",
    temperature=0.3,
)

store = InMemoryStore()
docs_root = os.path.abspath("./project_docs")

def composite_backend_factory(rt):
    return CompositeBackend(
        default=StateBackend(rt),  # 默认：线程内临时
        routes={
            "/memories/": StoreBackend(rt),  # 长期记忆
            "/docs/": FilesystemBackend(root_dir=docs_root, virtual_mode=True),  # 本地文档
        },
    )

agent = create_deep_agent(
    model=llm,
    backend=composite_backend_factory,
    store=store,  # 提供给 StoreBackend 使用
    system_prompt="""
你有一个分层文件系统：
- /workspace/ 下是短期工作区（临时）
- /memories/ 下是长期记忆（持久化）
- /docs/ 下是本地项目文档（只在当前机器存在）

请合理使用这些路径来完成任务。
"""
)

if __name__ == "__main__":
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "请从 /docs/ 目录中查找项目文档，"
                        "在 /workspace/ 下写一个草稿，"
                        "并把最终确认的结论保存到 /memories/summary.txt。"
                    ),
                }
            ]
        }
    )

    print(result["messages"][-1].content)

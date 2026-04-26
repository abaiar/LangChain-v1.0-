"""
第五章 5.3.1 Backend存储体系 — FilesystemBackend 文件系统后端示例

【章节学习重点】
- FilesystemBackend 的概念：将 Agent 数据持久化到文件系统
- 文件系统持久化的优势：简单直观，便于查看和调试

【代码功能】
演示 FilesystemBackend 的使用，将 Deep Agent 的数据持久化到本地文件系统。

【关键参数说明】
- FilesystemBackend: 文件系统后端，将数据写入指定目录
- 适合开发调试和小规模部署

【应用场景】
- 开发调试时的持久化方案
- 小规模部署的简单持久化
- 需要直接查看持久化数据的场景
"""
import os
from langchain_deepseek import ChatDeepSeek
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

# 初始化 DeepSeek 模型
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key="xxxxxx",
    temperature=0.3,
)

project_root = os.path.abspath(".")  # 当前目录作为 root_dir

agent = create_deep_agent(
    model=llm,
    backend=FilesystemBackend(
        root_dir=project_root,
        virtual_mode=True,   # 启用路径沙箱和规范化
    ),
    system_prompt="""
你可以访问一个本地项目目录。
请使用文件工具（例如 write_file）在项目根目录创建并写入一个 README.md 文件。
"""
)

if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "请为这个项目创建一个 README.md 文件，包含项目介绍、功能特性和使用方法等内容。"}]}
    )
    print(result["messages"][-1].content)

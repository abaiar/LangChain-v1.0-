"""
第五章 5.3.4 中间件体系 — TodoListMiddleware 示例

【章节学习重点】
- Deep Agent 中间件的使用方式
- TodoListMiddleware 的作用：让智能体在处理多步骤任务时先写 TODO 再执行

【代码功能】
演示 TodoListMiddleware 的使用，让智能体在处理多步骤任务时，
先规划 TODO 列表再逐步执行，提升任务执行的条理性。

【关键参数说明】
- TodoListMiddleware: 待办列表中间件，自动规划任务步骤

【应用场景】
- 多步骤任务的规范化执行
- 需要明确任务规划的场景
"""

import uuid
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain_deepseek import ChatDeepSeek
from langchain.messages import HumanMessage

# 1. 初始化模型
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key="xxxxxx",
    temperature=0.3,
)

# 2. 创建带 TodoListMiddleware 的 Agent
agent = create_agent(
    model=model,
    middleware=[
        TodoListMiddleware(
            system_prompt=(
                "面对多步骤任务时，先调用 write_todos 写出待办列表，"
                "然后根据 TODO 逐步执行，并在任务完成时更新 TODO。"
            )
        )
    ],
)

# 3. 发起一个明显是“多步骤”的请求
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "帮我规划一个为期三天的 LangGraph 学习计划："
                    "包括每天的学习目标和要完成的任务，并先给出你的 TODO 列表，再执行第一天的任务。"
                )
            )
        ]
    },
    config=config,
)

print("\n=== 最终回答 ===")
print(result["messages"][-1].content)
print("================\n")

"""
第二章 2.4.3 结构化输出 — ToolStrategy

【章节学习重点】
- 结构化输出：让智能体返回符合预定义 Schema 的结构化数据，而非自由文本
- ToolStrategy：通过 Tool Calling 机制实现结构化输出，兼容性强
- Pydantic BaseModel 用于定义输出结构，Field 提供字段描述

【代码功能】
演示使用 ToolStrategy 让智能体输出结构化的 UserProfile 数据。
ToolStrategy 将输出结构封装为一个特殊的"工具"，模型通过 Tool Calling 机制
返回结构化数据，而非自由文本。

【实现思路】
1. 使用 Pydantic BaseModel 定义 UserProfile 结构（username、age、is_active）
2. 定义一个占位工具 dummy_tool，确保智能体有可用工具列表
3. 使用 ToolStrategy(UserProfile) 封装输出结构
4. 创建智能体时通过 response_format 参数传入 ToolStrategy
5. 执行后通过 result["structured_response"] 获取结构化数据

【关键参数说明】
- ToolStrategy: 结构化输出策略，将 Pydantic 模型转为工具调用格式
- UserProfile: Pydantic 模型，定义输出字段及类型
- Field(description=...): 字段描述，帮助模型理解每个字段的含义
- response_format: create_agent() 的参数，指定输出格式策略
- structured_response: 智能体返回值中的结构化数据字段
- model_dump(): 将 Pydantic 模型转为字典

【应用场景】
- 信息提取：从自然语言中提取结构化数据（如用户档案、订单信息）
- 表单填充：将用户描述自动转为结构化表单数据
- API 集成：需要固定格式输出的下游系统对接
- 当模型不支持原生 JSON API 时的兼容方案
"""
import json
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy

class UserProfile(BaseModel):
    """用于存储用户信息的结构。"""
    username: str = Field(description="用户的唯一用户名。")
    age: int = Field(description="用户的年龄，必须是整数。")
    is_active: bool = Field(description="用户的账户当前是否处于活跃状态。")

@tool
def dummy_tool(query: str) -> str:
    """一个占位符工具，确保智能体有可用的工具列表。"""
    return "Tool is available."

tools = [dummy_tool]
input_text = "请为我创建一个档案：用户名是 'Jane_D', 她今年 32 岁，账户当前是活跃状态。"

print(">>> 智能体: ToolStrategy")

llm_tool = ChatDeepSeek(
    model="deepseek-chat", 
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.3
)

agent_tool = create_agent(
    model=llm_tool,
    tools=tools,
    response_format=ToolStrategy(UserProfile),
    system_prompt="你是一位通用信息提取助理，请使用 Tool Calling 机制提取信息。",
)

result_tool = agent_tool.invoke(
    {"messages": [HumanMessage(content=input_text)]}
)

structured_data = result_tool.get("structured_response")

print(f"类型: {type(structured_data).__name__}")
print(json.dumps(structured_data.model_dump(), indent=2, ensure_ascii=False))

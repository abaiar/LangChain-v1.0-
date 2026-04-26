"""
第二章 2.2.4 消息的使用 — ToolMessage（工具调用反馈）

【章节学习重点】
- ToolMessage 是工具调用流程中的关键消息类型，用于将工具执行结果反馈给模型
- 工具调用的完整消息流：HumanMessage → AIMessage(tool_calls) → ToolMessage(result) → AIMessage(最终答案)
- tool_call_id 是关联工具调用与结果的核心标识

【代码功能】
演示 ToolMessage 的构造和使用方式。模拟一个完整的工具调用流程：
1. 模型决定调用工具（AIMessage 包含 tool_calls）
2. 外部代码执行工具并获取结果
3. 创建 ToolMessage 将结果反馈给模型
4. 模型基于工具结果生成最终答案

【实现思路】
1. 创建 AIMessage 模拟模型的工具调用请求，包含 tool_calls 列表
2. 每个 tool_call 包含：id（唯一标识）、name（工具名）、args（参数）
3. 工具执行后，创建 ToolMessage，必须指定 tool_call_id 以关联对应的调用
4. 将 AIMessage 和 ToolMessage 组成消息序列，供模型继续处理

【关键参数说明】
- AIMessage.tool_calls: 列表类型，每个元素包含：
  - id: 工具调用的唯一标识符，由模型生成
  - name: 要调用的工具名称
  - args: 传给工具的参数字典
- ToolMessage.content: 工具执行的结果内容（字符串）
- ToolMessage.tool_call_id: 必须与 AIMessage.tool_calls 中的 id 对应，
  模型通过此 ID 将工具结果与调用请求匹配

【应用场景】
- 智能体（Agent）中的工具调用流程
- ReAct 模式中的观察（Observation）步骤
- 任何需要模型调用外部工具并获取结果的场景
"""
from langchain.messages import AIMessage, ToolMessage

model_tool_call = AIMessage(
    content="",
    tool_calls=[{"id": "call_123", "name": "calculator", "args": {"a": 2, "b": 3}}]
)

calculation_result = "5"

tool_feedback = ToolMessage(
    content=calculation_result,
    tool_call_id=model_tool_call.tool_calls[0]["id"]
)

final_messages = [
    model_tool_call,
    tool_feedback
]

print("--- ToolMessage 反馈格式示例 ---")
print(f"类型: {tool_feedback.type}")
print(f"内容: {tool_feedback.content}")
print(f"关联ID: {tool_feedback.tool_call_id}")

"""
第四章 4.4.1 中断机制 — 工具调用前的 interrupt 审批

【章节学习重点】
- 在 @tool 工具函数中使用 interrupt()：工具执行前暂停等待审批
- 工具参数的动态修改：审批时可以修改工具的执行参数
- 工具节点与智能体节点的协作模式

【代码功能】
演示在工具函数中使用 interrupt() 实现工具调用审批。
以邮件发送工具为例，在发送前中断等待人工审批，
审批时可以修改收件人、主题、正文等参数。

【实现思路】
1. 定义 AgentState 状态类
2. 创建 send_email 工具，在发送前使用 interrupt() 暂停
3. interrupt() 传递邮件详情和审批提示
4. 审批通过后获取最终参数（可能被修改）
5. 定义智能体节点和工具执行节点
6. 编译图并执行审批流程

【关键参数说明】
- @tool: LangChain 工具装饰器，将函数注册为可调用工具
- interrupt({"action": ..., "to": ..., "subject": ..., "body": ...}): 传递审批详情
- response.get("action") == "approve": 判断审批结果
- model.bind_tools([send_email]): 将工具绑定到模型
- ToolMessage: 工具执行结果消息

【应用场景】
- 敏感操作审批：邮件发送、文件删除、资金转账等
- 工具参数的人工修正
- 需要在自动化流程中加入人工审核关卡的场景
"""
from typing import TypedDict
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.messages import ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

# ========== 1. 状态定义 ==========
class AgentState(TypedDict):
    """智能体状态类型定义"""
    messages: list[dict]  # 消息列表，包含用户消息和 AI 响应

# ========== 2. 工具定义 ==========
@tool
def send_email(to: str, subject: str, body: str):
    """
    发送邮件工具：在发送前中断执行，等待人工审批
    
    Args:
        to: 收件人邮箱地址
        subject: 邮件主题
        body: 邮件正文
        
    Returns:
        str: 发送结果消息
    """
    # 在发送前暂停执行；信息会出现在 result["__interrupt__"] 中
    response = interrupt({
        "action": "send_email",
        "to": to,
        "subject": subject,
        "body": body,
        "message": "是否批准发送此邮件？"
    })

    # 如果用户批准了发送
    if response.get("action") == "approve":
        # 获取最终参数（用户可能修改了参数）
        final_to = response.get("to", to)
        final_subject = response.get("subject", subject)
        final_body = response.get("body", body)

        # 实际发送邮件
        print(f"[send_email] to={final_to} subject={final_subject} body={final_body}")
        return f"邮件已发送至 {final_to}"

    # 用户取消了发送
    return "邮件已被用户取消"

# ========== 3. 初始化模型 ==========
model = init_chat_model(
    model="deepseek-chat",
    temperature=0.7,
    api_key="xxxxxx",
    base_url="https://api.deepseek.com/v1",
    model_provider="openai"
).bind_tools([send_email])

# ========== 4. 节点定义 ==========
def agent_node(state: AgentState):
    """智能体节点：调用模型处理消息"""
    result = model.invoke(state["messages"])
    return {"messages": state["messages"] + [result]}


def tools_node(state: AgentState):
    """工具执行节点：执行工具调用"""
    last_msg = state["messages"][-1]
    tool_calls = getattr(last_msg, 'tool_calls', [])
    
    tool_messages = []
    for tool_call in tool_calls:
        # 执行工具
        result = send_email.invoke(tool_call["args"])
        tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
    
    return {"messages": tool_messages}

# ========== 5. 构建图 ==========
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tools_node)
builder.add_edge(START, "agent")
builder.add_edge("agent", "tools")
builder.add_edge("tools", END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# ========== 6. 执行演示 ==========
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "tools1"}}
    
    # 第一次执行：工作流在工具节点中断
    initial = graph.invoke(
        {
            "messages": [
                {"role": "user", "content": "向 xxxxxx@163.com 发送一封关于会议的邮件，主题为：会议通知，正文为：请参加会议，时间：2025-11-18 10:00，地点：会议室101"}
            ]
        },
        config=config
    )
    
    print("中断信息:")
    print(initial["__interrupt__"])
    
    # 恢复执行：传入审批结果和可选的编辑后的参数
    resumed = graph.invoke(
        Command(resume={"action": "approve", "subject": "会议通知", "body": "请参加会议，时间：2025-11-18 10:00，地点：会议室102"}),
        config=config
    )
    print("\n最终结果：", resumed["messages"][-1])
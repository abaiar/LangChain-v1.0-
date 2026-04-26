"""
第二章 2.4.6 基于装饰器的中间件

【章节学习重点】
- 装饰器中间件是 LangChain 提供的轻量级、函数式中间件机制
- 六种钩子装饰器：before_agent、after_agent、before_model、after_model、wrap_model_call、dynamic_prompt
- 节点式中间件（before/after）可返回 dict 修改状态或 None 放行
- 包裹式中间件（wrap_model_call）可完全控制模型调用的输入输出

【代码功能】
综合演示六种装饰器中间件的使用：
1. @dynamic_prompt: 动态系统提示，根据运行时上下文生成个性化提示
2. @before_agent: Agent 执行前的预处理（如日志记录）
3. @after_agent: Agent 执行后的后处理（如日志记录）
4. @before_model: 模型调用前的预处理（如日志记录）
5. @after_model(can_jump_to=["end"]): 模型调用后的校验（如安全拦截）
6. @wrap_model_call: 包裹模型调用（如重试、耗时统计）

【实现思路】
1. personalized_prompt: 从 runtime.context 获取用户 ID，生成个性化系统提示
2. log_before_agent/log_after_agent: 打印 Agent 级别的消息数日志
3. log_before_model: 打印模型调用前的消息数
4. validate_output: 检测模型输出中的 "BLOCKED_CN" 关键词，触发安全跳转
5. retry_and_timing: 包裹模型调用，添加重试（指数退避）和耗时统计
6. 按顺序组装中间件列表，传入 create_agent

【关键参数说明】
- @dynamic_prompt: 便捷装饰器，返回字符串作为动态系统提示
- @before_agent/@after_agent: Agent 级别钩子，每次 invoke 触发一次
- @before_model/@after_model: 模型级别钩子，每次模型调用触发
- can_jump_to=["end"]: after_model 的参数，允许跳转到指定节点
- @wrap_model_call: 包裹式钩子，接收 request 和 handler，返回 response
- AgentState: 状态字典，包含 messages 等字段
- ModelRequest/ModelResponse: 模型请求/响应对象
- jump_to="end": 跳转到结束节点，终止当前流程

【应用场景】
- 日志记录和监控
- 安全拦截和内容过滤
- 模型调用的重试和降级
- 动态提示词生成
- 性能统计和耗时分析
"""
from typing import Any, Callable
import time
import math

from langchain.agents import create_agent
from langchain.agents.middleware import (
    before_agent,
    after_agent,
    before_model,
    after_model,
    wrap_model_call,
    dynamic_prompt,
    AgentState,
    ModelRequest,
    ModelResponse,
)
from langchain.messages import AIMessage, HumanMessage
from langgraph.runtime import Runtime
from langchain_openai import ChatOpenAI


@dynamic_prompt
def personalized_prompt(req: ModelRequest) -> str:
    runtime = getattr(req, "runtime", None)
    user_id = "访客"
    if runtime and getattr(runtime, "context", None):
        user_id = runtime.context.get("user_id", "访客")
    return f"你是一名贴心的中文助手，正在为用户「{user_id}」提供帮助。回答时要简洁、自然。"

@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"[before_agent] 本次会话开始，已有消息数：{len(state.get('messages', []))}")
    return None

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"[after_agent] 会话结束，最终消息数：{len(state.get('messages', []))}")
    return None


@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"[before_model] 准备进行模型调用，当前消息数：{len(state['messages'])}")
    return None

@after_model(can_jump_to=["end"])
def validate_output(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """简单的输出校验：若模型输出包含"BLOCKED_CN"，则改写消息并跳转到 end。"""
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and "BLOCKED_CN" in (last.content or ""):
        print("[after_model] 触发安全规则：检测到 BLOCKED_CN，跳转到 end")
        return {
            "messages": [AIMessage("该请求触发了安全校验，无法继续。")],
            "jump_to": "end",
        }
    return None

@wrap_model_call
def retry_and_timing(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    max_retries = 2
    start = time.time()
    try:
        for i in range(max_retries + 1):
            try:
                return handler(request)
            except Exception as e:
                if i == max_retries:
                    raise
                backoff = 0.1 * math.pow(2, i)
                print(f"[wrap_model_call] 调用失败，将在 {backoff:.2f}s 后重试：{e}")
                time.sleep(backoff)
    finally:
        cost = (time.time() - start) * 1000
        print(f"[wrap_model_call] 本次模型调用耗时：{cost:.0f} ms")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.3,
)

agent = create_agent(
    model=llm,
    tools=[],
    middleware=[
        personalized_prompt,
        log_before_agent,
        log_before_model,
        retry_and_timing,
        validate_output,
        log_after_agent,
    ],
)

if __name__ == "__main__":
    res1 = agent.invoke(
        {"messages": [HumanMessage("用一句话解释 LangGraph 是什么。")]},
        config={"context": {"user_id": "alice"}},
    )
    print("\n[Result-1]", res1["messages"][-1].content)
    
    print("--------------------------------")

    res2 = agent.invoke(
        {"messages": [HumanMessage("请只回复：BLOCKED_CN")]},
        config={"context": {"user_id": "bob"}},
    )
    print("\n[Result-2]", res2["messages"][-1].content)

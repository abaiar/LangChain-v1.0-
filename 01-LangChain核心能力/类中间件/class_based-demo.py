"""
第二章 2.4.7 基于类的中间件 — 类中间件完整示例

【章节学习重点】
- AgentMiddleware 类的继承与实现方式
- Node-style 中间件（before_agent/before_model/after_model/after_agent）的钩子机制
- Wrap-style 中间件（wrap_model_call）的包裹调用机制
- 多个类中间件的组装顺序与执行优先级

【代码功能】
演示如何通过继承 AgentMiddleware 基类来编写两种风格的中间件：
1. PolicyGuardMiddleware（Node-style）：在智能体执行的关键节点进行日志记录和安全拦截
2. RetryAndMetricsMiddleware（Wrap-style）：包裹模型调用，实现退避重试和耗时统计
然后将两个中间件组装到 Agent 中，展示正常调用和安全拦截两种场景。

【实现思路】
1. 定义 PolicyGuardMiddleware，继承 AgentMiddleware，实现 before_agent/before_model/after_model/after_agent 四个钩子
   - before_agent/before_model：打印日志，记录当前消息数
   - after_model：检测 AI 回复中是否包含安全关键词 "BLOCKED_CN"，若命中则返回替换消息并跳转到 end
   - after_agent：打印会话结束日志
2. 定义 RetryAndMetricsMiddleware，继承 AgentMiddleware，实现 wrap_model_call 方法
   - 对模型调用进行指数退避重试（最多重试 max_retries 次）
   - 统计每次模型调用的耗时（毫秒）
3. 创建 DeepSeek 模型实例，使用 create_agent 组装 Agent
   - middleware 列表中 wrap 型按"从外到内"包裹，RetryAndMetricsMiddleware 放前面作为最外层
   - node 型按列表顺序执行 before_*，after_* 逆序回卷

【关键参数说明】
- AgentState: 智能体状态字典，包含 messages 等字段
- Runtime: LangGraph 运行时上下文，提供配置和元数据访问
- ModelRequest: 模型请求对象，包含消息列表和调用参数
- ModelResponse: 模型响应对象，包含 AI 生成的消息
- max_retries: 最大重试次数，默认2次
- base_delay: 退避基础延迟（秒），每次重试延迟 = base_delay * 2^i
- jump_to: 中间件返回的特殊字段，用于跳转到指定节点（如 "end"）

【应用场景】
- 安全合规：在 after_model 中检测敏感内容，拦截违规输出
- 可观测性：在 before/after 钩子中记录日志，追踪智能体执行流程
- 容错重试：在 wrap_model_call 中实现指数退避重试，提升调用稳定性
- 性能监控：统计模型调用耗时，辅助性能优化
"""
from typing import Any, Callable
import time, math

from langchain.agents import create_agent
from langchain.agents.middleware import (
    AgentMiddleware, AgentState, ModelRequest, ModelResponse,
)
from langchain.messages import AIMessage, HumanMessage
from langgraph.runtime import Runtime
from langchain_openai import ChatOpenAI

# ========== 中间件 A：日志 + 安全拦截（Node-style） ==========
class PolicyGuardMiddleware(AgentMiddleware):
    """在关键节点打印日志，并在 after_model 命中关键词时跳转 end"""

    def before_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"[before_agent] 会话开始，消息数：{len(state.get('messages', []))}")
        return None

    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"[before_model] 准备进行模型调用，当前消息数：{len(state['messages'])}")
        return None

    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        last = state["messages"][-1]
        if isinstance(last, AIMessage) and "BLOCKED_CN" in (last.content or ""):
            print("[after_model] 触发安全规则：检测到 BLOCKED_CN，跳转 end")
            return {
                "messages": [AIMessage("该请求触发了安全校验，无法继续。")],
                "jump_to": "end",
            }
        return None

    def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"[after_agent] 会话结束，最终消息数：{len(state.get('messages', []))}")
        return None


# ========== 中间件 B：重试 + 耗时统计（Wrap-style） ==========
class RetryAndMetricsMiddleware(AgentMiddleware):
    """包裹每次模型调用，做退避重试与耗时统计"""

    def __init__(self, max_retries: int = 2, base_delay: float = 0.1):
        self.max_retries = max_retries
        self.base_delay = base_delay  # 秒

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        start = time.time()
        try:
            for i in range(self.max_retries + 1):
                try:
                    return handler(request)
                except Exception as e:
                    if i == self.max_retries:
                        raise
                    backoff = self.base_delay * math.pow(2, i)
                    print(f"[wrap_model_call] 失败，将在 {backoff:.2f}s 后重试：{e}")
                    time.sleep(backoff)
        finally:
            cost = (time.time() - start) * 1000
            print(f"[wrap_model_call] 本次模型调用耗时：{cost:.0f} ms")


# ========== 组装 Agent（DeepSeek 模型） ==========
llm = ChatOpenAI(
    model="deepseek-chat", 
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.3
)

# 注意执行顺序：
# - wrap 型按列表“从外到内”包裹；我们希望“重试/计时”最外层，所以把 RetryAndMetricsMiddleware放前面
# - node 型按列表顺序执行 before_*，after_* 逆序回卷
agent = create_agent(
    model=llm,
    tools=[],
    middleware=[
        RetryAndMetricsMiddleware(max_retries=2, base_delay=0.1),  # 外层：重试+计时
        PolicyGuardMiddleware(),                                   # 内层：日志+安全拦截
    ],
)

if __name__ == "__main__":
    # 1) 正常问答
    res1 = agent.invoke({"messages": [HumanMessage("用一句话解释 LangGraph 是什么。")]})
    print("\n[Result-1]", res1["messages"][-1].content)

    print("\n" + "-" * 64 + "\n")

    # 2) 触发安全跳转（让模型回复包含关键字）
    res2 = agent.invoke({"messages": [HumanMessage("请只回复：BLOCKED_CN")]})
    print("\n[Result-2]", res2["messages"][-1].content)

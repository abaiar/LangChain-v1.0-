"""
第二章 2.4.5 智能体中的预置中间件 — HumanInTheLoopMiddleware

【章节学习重点】
- HumanInTheLoopMiddleware（HITL）: 人工在环中间件，拦截敏感工具调用等待人工审批
- 中断-恢复机制：interrupt → 人工决策 → Command(resume) → 继续执行
- InMemorySaver: HITL 必须配合 checkpointer 使用，用于保存中断时的状态
- 三种审批决策：approve（批准）、edit（修改参数后批准）、reject（拒绝）

【代码功能】
演示 HITL 中间件在数据库写操作场景下的使用。
当智能体调用 dangerous_write 工具时，中间件自动中断执行，
等待人工从命令行输入审批决策后恢复执行。

【实现思路】
1. 定义高风险工具 dangerous_write（数据库写操作）
2. 配置 HITL 中间件，指定拦截 dangerous_write 工具
3. 创建智能体时传入 HITL 中间件和 InMemorySaver
4. 执行多轮对话，安全问答正常通过，SQL 操作触发中断
5. handle_interrupt() 函数处理中断：读取决策、调用 Command(resume) 恢复

【关键参数说明】
- HumanInTheLoopMiddleware: 人工在环中间件
- interrupt_on: 指定需要拦截的工具及允许的决策类型
  {"dangerous_write": {"allowed_decisions": ["approve", "edit", "reject"]}}
- InMemorySaver: 内存检查点保存器，HITL 必需组件
- Command(resume=...): 恢复执行的命令
  - approve: {"decisions": [{"type": "approve"}]}
  - edit: {"decisions": [{"type": "edit", "updates": {"sql": new_sql}}]}
  - reject: {"decisions": [{"type": "reject", "override": {"content": "..."}}]}
- __interrupt__: 中断信息，包含被拦截的工具名和参数
- thread_id: 线程 ID，中断恢复时必须使用相同 ID

【应用场景】
- 数据库写操作、资金操作等高风险场景的安全审批
- 生产环境中 AI 自主操作的风险控制
- 需要人工确认关键决策的自动化流程
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.0,
    max_tokens=20,
)

@tool
def dangerous_write(sql: str) -> str:
    """对数据库执行写操作（插入/更新/删除）。当请求涉及数据库写操作或出现以'SQL:'开头的指令时，必须调用本工具。"""
    return f"[模拟执行] {sql}"

hitl = HumanInTheLoopMiddleware(
    interrupt_on={"dangerous_write": {"allowed_decisions": ["approve", "edit", "reject"]}}
)

agent = create_agent(
    model=llm,
    tools=[dangerous_write],
    middleware=[hitl],
    system_prompt=(
        "只用一句极短中文回答（≤20字）。"
        "凡是涉及数据库写操作，或消息以'SQL:'开头时，必须调用工具 dangerous_write，不得直接回答。"
    ),
    checkpointer=InMemorySaver(),
)

CFG = {"configurable": {"thread_id": "hitl-demo-interactive"}}

conversation = [
    "你是谁？",
    "SQL: INSERT INTO logs(content) VALUES ('hello');",
    "继续。",
    "SQL: DELETE FROM orders WHERE created_at >= date('now','-7 days');",
]

state = {"messages": []}

def handle_interrupt(result) -> dict:
    """处理 HITL 中断：从命令行读取决策，并用 Command(resume=...) 恢复。"""
    interrupt = result.get("__interrupt__")
    if not interrupt:
        return result

    print("\n⚠️ 检测到人工在环中断：")
    print(interrupt)

    decision = input("请输入决策 (approve/edit/reject)：").strip().lower()

    if decision == "approve":
        return agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}), config=CFG)

    elif decision == "edit":
        new_sql = input("请输入修改后的 SQL：").strip()
        return agent.invoke(
            Command(
                resume={
                    "decisions": [{
                        "type": "edit",
                        "updates": {"sql": new_sql}
                    }]
                }
            ),
            config=CFG
        )

    elif decision == "reject":
        return agent.invoke(
            Command(
                resume={
                    "decisions": [{
                        "type": "reject",
                        "override": {"content": "[操作已被人工拒绝]"}
                    }]
                }
            ),
            config=CFG
        )
    else:
        print("输入无效，按拒绝处理。")
        return agent.invoke(
            Command(
                resume={
                    "decisions": [{
                        "type": "reject",
                        "override": {"content": "[操作已被人工拒绝]"}
                    }]
                }
            ),
            config=CFG
        )

for i, q in enumerate(conversation, 1):
    user_msg = HumanMessage(content=q)
    result = agent.invoke({"messages": state["messages"] + [user_msg]}, config=CFG)

    if result.get("__interrupt__"):
        result = handle_interrupt(result)

    state = result
    ans = state["messages"][-1].content

    print(f"\n🧩 第 {i} 轮")
    print(f"Q: {q}")
    print(f"A: {ans}")

print("\n✅ 对话结束。")

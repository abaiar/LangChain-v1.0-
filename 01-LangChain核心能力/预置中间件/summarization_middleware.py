"""
第二章 2.4.5 智能体中的预置中间件 — SummarizationMiddleware

【章节学习重点】
- 预置中间件是 LangChain 官方提供的开箱即用的中间件
- SummarizationMiddleware: 自动摘要对话上下文，防止 Token 超限
- 中间件的工作原理：当上下文累积超过阈值时，自动将早期消息压缩为摘要

【代码功能】
演示 SummarizationMiddleware 的使用。设置极低的阈值（30 tokens）以快速触发摘要，
在多轮对话中观察摘要中间件的效果：早期消息被压缩，仅保留最近的几条原文。

【实现思路】
1. 创建主对话模型和摘要模型（可使用不同模型以节省成本）
2. 配置 SummarizationMiddleware，设置触发阈值和保留消息数
3. 创建智能体时将中间件传入 middleware 参数
4. 执行多轮对话，观察摘要中间件何时触发

【关键参数说明】
- SummarizationMiddleware: 官方预置的对话摘要中间件
- model: 用于生成摘要的 LLM 模型（可与主模型不同，建议用轻量模型节省成本）
- max_tokens_before_summary: 触发摘要的 Token 阈值
  当上下文估算 Token 数超过此值时，自动将早期消息压缩为摘要
- messages_to_keep: 摘要后保留的最近 N 条原文消息
- summary_prompt: 自定义摘要提示词，控制摘要的风格和长度
- max_tokens=20: 限制模型输出长度，配合极简提示词演示效果

【应用场景】
- 长对话场景，防止上下文 Token 超限
- 客服系统中的多轮对话管理
- 需要保留对话要点但控制成本的长会话场景
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.messages import HumanMessage

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.0,
    max_tokens=20,
)

summ_llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.0,
    max_tokens=20,
)

middleware = SummarizationMiddleware(
    model=summ_llm,
    max_tokens_before_summary=30,
    messages_to_keep=5,
    summary_prompt="用20个字以内概括要点。",
)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="只用一句极短中文回答，且不超过30个字。",
    middleware=[middleware],
)


conversation = [
    "RAG是什么？",
    "有何用途？",
    "主要缺点？",
    "一句话总结",
]

state = {"messages": []}

for i, question in enumerate(conversation, 1):
    user_msg = HumanMessage(content=question)
    state = agent.invoke({"messages": state["messages"] + [user_msg]})
    answer = state["messages"][-1].content

    print(f"\n🧩 第 {i} 轮")
    print(f"Q: {question}")
    print(f"A: {answer}")

print("\n✅ 对话结束。")

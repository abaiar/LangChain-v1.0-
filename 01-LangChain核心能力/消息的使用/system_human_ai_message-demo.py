"""
第二章 2.2.4 消息的使用 — SystemMessage、HumanMessage、AIMessage

【章节学习重点】
- LangChain 的消息机制：对话通过 Messages 列表传递，每条消息有明确的角色类型
- 三种核心消息类型：SystemMessage（系统指令）、HumanMessage（用户输入）、AIMessage（AI回复）
- 多轮对话的核心：必须将历史消息完整传递给模型，模型本身无状态

【代码功能】
演示如何手动构建多轮对话的 Messages 列表，包括：
1. 第一轮：SystemMessage 设定角色 + HumanMessage 提问 → 获取 AIMessage 回复
2. 第二轮：保留历史消息 + 追加新的 HumanMessage → 模型基于上下文回复

【实现思路】
1. 创建模型实例（DeepSeek）
2. 第一轮：构建 [SystemMessage, HumanMessage] 列表，调用 model.invoke() 获取 AIMessage
3. 第二轮：构建 [SystemMessage, 历史HumanMessage, 历史AIMessage, 新HumanMessage] 列表
4. 关键点：SystemMessage 必须在每轮都保留，它是模型的行为准则

【关键概念说明】
- SystemMessage: 设定 AI 的角色、风格和行为约束，对整个对话生效
- HumanMessage: 用户的输入内容
- AIMessage: 模型的回复内容，在多轮对话中需要作为历史传递回去
- 多轮对话原理：LLM 本身是无状态的，每次调用都需要传入完整的对话历史

【应用场景】
- 构建多轮对话系统
- 需要为 AI 设定特定角色和风格的场景
- 对话历史的持久化与恢复
"""
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage, AIMessage

model = ChatOpenAI(
    model="deepseek-chat",
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.3
)

print("--- 第一轮对话 ---")

messages_round_1 = [
    SystemMessage(content="你是一个幽默风趣的诗人，所有的回复必须包含一个笑话。"),
    HumanMessage(content="写一首关于'AI学习'的短诗。")
]

response_1 = model.invoke(messages_round_1)

print(f"AI回复: {response_1.content}")
print("-" * 20)

print("--- 第二轮对话 ---")

messages_round_2 = [
    messages_round_1[0],
    messages_round_1[1],
    AIMessage(content=response_1.content),
    HumanMessage(content="非常好！现在将它翻译成英文。")
]

response_2 = model.invoke(messages_round_2)

print(f"AI回复: {response_2.content}")

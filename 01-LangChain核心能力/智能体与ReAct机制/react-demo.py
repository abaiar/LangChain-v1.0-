"""
第二章 2.4.2 智能体的基本使用与ReAct机制 — ReAct多步推理演示

【章节学习重点】
- ReAct（Reasoning + Acting）机制：智能体通过"推理→行动→观察"循环解决复杂问题
- 多步工具调用：一个复杂问题可能需要连续调用多个工具
- ReAct 的核心流程：Thought(推理) → Action(调用工具) → Observation(观察结果) → 最终回答

【代码功能】
演示 ReAct 机制在多步推理场景下的工作方式。
复杂问题"1500美元可兑换多少人民币"需要两步：
1. 先调用 get_exchange_rate 获取汇率（Action 1）
2. 再调用 calculate 进行计算（Action 2）
3. 综合两次工具结果给出最终回答

【实现思路】
1. 初始化 DeepSeek 模型
2. 定义两个工具：calculate（计算器）和 get_exchange_rate（汇率查询）
3. 创建 ReAct 智能体，系统提示词强调必须使用工具
4. 提交一个需要多步工具调用的复杂问题
5. 智能体自动执行 ReAct 循环：推理→调用汇率工具→推理→调用计算工具→综合回答

【关键参数说明】
- ReAct 循环: Thought → Action → Observation → Thought → ... → Final Answer
- create_agent() 内部默认使用 ReAct 推理模式
- system_prompt 中强调"必须使用工具"可避免模型直接回答而不调用工具
- 智能体自动决定工具调用顺序和次数，无需手动编排

【应用场景】
- 需要多步推理和工具协作的复杂任务
- 数据获取+数据处理组合场景（如查询+计算）
- 金融分析、信息检索+摘要等需要多源信息整合的任务
"""
from langchain_openai import ChatOpenAI
from langchain.tools import tool 
from langchain.agents import create_agent
from langchain.messages import HumanMessage 
from typing import List

llm = ChatOpenAI(
    model="deepseek-chat", 
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.3
)

@tool
def calculate(expression: str) -> str:
    """这是一个数学计算器。当需要计算数学表达式时调用此工具。
    输入必须是一个有效的Python表达式字符串，例如 '10 * 5 + 3'。"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """用于查询两种货币之间的实时汇率。返回 'from_currency' 兑换 'to_currency' 的比率。"""
    if from_currency == "USD" and to_currency == "CNY":
        return 7.21
    if from_currency == "EUR" and to_currency == "USD":
        return 1.08
    return 1.0

tools: List[tool] = [calculate, get_exchange_rate]

agent_react = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一位专业的金融计算助理，必须使用工具进行汇率查询和数学运算。",
)

complex_question = "如果当前美元兑人民币的汇率是实时汇率，那么 1500 美元可以兑换多少人民币？"

print("\n--- 任务三：多步 ReAct 机制演示（汇率查询 + 乘法计算） ---")
print(f"复杂问题: {complex_question}")

result_complex = agent_react.invoke(
    {"messages": [HumanMessage(content=complex_question)]}
)

print(f"智能体最终输出:\n{result_complex['messages'][-1].content}")

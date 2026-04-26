"""
第二章 2.4.2 智能体的基本使用与ReAct机制 — create_agent创建智能体

【章节学习重点】
- 使用 create_agent() 创建智能体，将 LLM + 工具 + 系统提示词组合为自主决策的 Agent
- 智能体的核心能力：根据用户问题自主选择合适的工具进行处理
- create_agent 是 LangChain 1.0 中创建智能体的推荐方式

【代码功能】
演示使用 create_agent() 创建一个具备计算和信息查询能力的智能体。
智能体根据用户问题的语义，自主判断应该调用哪个工具：
- 涉及数学计算 → 调用 calculate 工具
- 涉及城市信息 → 调用 get_info 工具

【实现思路】
1. 初始化 DeepSeek 模型作为智能体的推理引擎
2. 定义两个工具：calculate（数学计算）和 get_info（城市信息查询）
3. 使用 create_agent() 将模型、工具和系统提示词组装为智能体
4. 执行两个不同类型的任务，验证智能体的工具选择能力

【关键参数说明】
- create_agent(): LangChain 1.0 的智能体创建函数
- model: 底层 LLM 模型，负责推理和工具选择决策
- tools: 工具列表，智能体可调用的工具集合
- system_prompt: 系统提示词，定义智能体的角色和行为准则
- agent.invoke(): 执行智能体，传入 {"messages": [HumanMessage(...)]}
- 返回值: 包含 messages 列表的字典，最后一条为智能体的最终回复

【应用场景】
- 构建具备工具调用能力的智能助手
- 客服系统：根据问题类型自动路由到不同处理工具
- 信息查询与计算一体化的问答系统
"""
from langchain_openai import ChatOpenAI
from langchain.tools import tool 
from langchain.agents import create_agent
from langchain.messages import HumanMessage

llm = ChatOpenAI(
    model="deepseek-chat", 
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.3
)

@tool
def calculate(expression: str) -> str:
    """这是一个数学计算器。当需要计算数学表达式时调用此工具。
    输入必须是一个有效的Python表达式字符串。"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误：{e}"

@tool
def get_info(city_name: str) -> str:
    """用于查询指定城市的基本信息，例如城市别名、主要产业等。"""
    city_data = {
        "深圳": "别称'鹏城'，是中国改革开放建立的第一个经济特区，以高新技术产业闻名。",
        "上海": "别称'沪'或'申'，是中国最大的城市和金融中心，拥有繁荣的港口贸易。",
        "北京": "中国的首都，拥有深厚的历史文化底蕴，是政治和文化中心。"
    }
    return city_data.get(city_name, f"未找到关于城市 '{city_name}' 的特定信息。")


agent = create_agent(
    model=llm,
    tools=[calculate, get_info],
    system_prompt="你是一位专业的智能助理，拥有计算和信息查询的能力。请根据用户需求，自主选择最合适的工具进行处理。",
)

print("--- 任务一：智能体自主选择 'calculate' 工具 ---")
question_one = "请计算 (256 减去 88) 再乘以 5 的结果是多少？"

result_one = agent.invoke(
    {"messages": [HumanMessage(content=question_one)]}
)

print(f"用户问题: {question_one}")
print(f"智能体最终输出:\n{result_one['messages'][-1].content}")


print("\n--- 任务二：智能体自主选择 'get_info' 工具 ---")
question_two = "深圳的别称是什么？它以什么产业闻名？"

result_two = agent.invoke(
    {"messages": [HumanMessage(content=question_two)]}
)

print(f"用户问题: {question_two}")
print(f"智能体最终输出:\n{result_two['messages'][-1].content}")

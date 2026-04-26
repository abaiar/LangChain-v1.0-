"""
第二章 2.4.4 MCP的使用 — MCP客户端连接示例

【章节学习重点】
- MultiServerMCPClient: LangChain 提供的 MCP 多服务客户端
- 同时连接多个 MCP 服务：stdio 模式（本地子进程）和 streamable-http 模式（远程HTTP）
- MCP 工具自动转为 LangChain Tool 格式，可直接传给 create_agent

【代码功能】
演示如何使用 MultiServerMCPClient 同时连接 Math（stdio）和 Weather（HTTP）两个 MCP 服务，
获取工具列表后创建智能体，分别执行数学计算和天气查询任务。

【实现思路】
1. 初始化 DeepSeek 模型
2. 配置 MultiServerMCPClient 连接两个 MCP 服务：
   - math: stdio 模式，通过 command + args 启动本地 Python 脚本
   - weather: streamable_http 模式，连接到已运行的 HTTP 服务
3. 调用 client.get_tools() 获取所有 MCP 工具（异步方法）
4. 使用 create_agent() 创建智能体，MCP 工具自动适配
5. 分别执行数学和天气任务

【关键参数说明】
- MultiServerMCPClient: 多服务 MCP 客户端，接受服务配置字典
- transport: "stdio" 或 "streamable_http"
- command/args: stdio 模式下启动子进程的命令和参数
- url: HTTP 模式下的服务端点地址
- get_tools(): 异步方法，返回 LangChain Tool 列表
- arun(): 同步封装函数，将异步协程转为同步调用
- agent.ainvoke(): 异步调用智能体

【应用场景】
- 同时集成多个 MCP 工具服务
- 混合使用本地子进程和远程 HTTP 工具服务
- MCP 协议的客户端集成实战
"""
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="xxxxxx",
    base_url="https://api.deepseek.com",
    temperature=0.3,
)

client = MultiServerMCPClient({
    "math": {
        "transport": "stdio",
        "command": "python",
        "args": ["./math_mcp_server.py"],
    },
    "weather": {
        "transport": "streamable_http",
        "url": "http://localhost:8000/mcp",
    },
})

def arun(coro):
    """同步封装：把异步协程在顶层跑完，主逻辑仍然是"同步写法" """
    return asyncio.run(coro)

tools = arun(client.get_tools())
print("✅ 已加载的工具：", [t.name for t in tools])

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "你是一个助理。涉及数学计算，使用 math 工具（add / multiply）；"
        "涉及天气，使用 weather 工具（geocode_city / get_current_weather / get_current_weather_by_city）。"
    ),
)

math_question = "请帮我计算 (3 + 5) × 12 的结果"
print("\n🔢 数学任务：", math_question)
math_result = arun(agent.ainvoke({"messages": [HumanMessage(content=math_question)]}))
print("✅ 智能体输出：", math_result["messages"][-1].content)

weather_question = "请告诉我北京现在的天气情况"
print("\n🌤 天气任务：", weather_question)
weather_result = arun(agent.ainvoke({"messages": [HumanMessage(content=weather_question)]}))
print("✅ 智能体输出：", weather_result["messages"][-1].content)

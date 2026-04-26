"""
第三章 3.4 实战集成私有知识库 — MCP 工具装配模块

【章节学习重点】
- MultiServerMCPClient 的使用：同时连接多个 MCP 服务
- MCP 两种传输协议：stdio 和 streamable-http

【代码功能】
通过 MultiServerMCPClient 同时连接本地 math 与 weather 两个 MCP 服务，
返回 LangChain Agent 可直接使用的 Tool 列表。

【实现思路】
1. 定位 MCP 服务端脚本路径
2. 创建 MultiServerMCPClient，配置 math（stdio）和 weather（streamable-http）
3. 获取工具列表

【关键参数说明】
- transport: 传输协议类型（stdio / streamable_http）
- command/args: stdio 模式下的启动命令和参数
- url: streamable-http 模式下的服务端点

【应用场景】
- 智能体集成多个外部工具服务
"""
import asyncio
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient

def build_tools():
    """
    封装 math 与 weather 两个 MCP 服务：
    - math：通过 stdio 启动本地 math_server.py
    - weather：通过 streamable-http 连接到固定端口（http://localhost:8000/mcp）
    """
    project_root = Path(__file__).parent.parent
    math_server_path = project_root / "mcp_server" / "math_server.py"
    
    client = MultiServerMCPClient({
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": [str(math_server_path)],
        },
        "weather": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp",
        },
    })

    return asyncio.run(client.get_tools())


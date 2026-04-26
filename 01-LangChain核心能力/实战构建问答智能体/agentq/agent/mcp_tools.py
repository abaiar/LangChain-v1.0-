"""
第二章 2.5.3 集成MCP工具层 — MCP 工具装配模块

【章节学习重点】
- MultiServerMCPClient 的使用：同时连接多个 MCP 服务
- MCP 两种传输协议的区别：stdio（标准输入输出）和 streamable-http（HTTP流式）
- MCP 工具的发现与加载机制：客户端自动获取服务端注册的所有工具

【代码功能】
通过 MultiServerMCPClient 同时连接本地 math 与 weather 两个 MCP 服务，
返回 LangChain Agent 可直接使用的 Tool 列表。
这是智能体集成外部工具的核心桥梁模块。

【实现思路】
1. 确定项目根目录，定位 MCP 服务端脚本的路径
2. 创建 MultiServerMCPClient，配置两个 MCP 服务连接：
   - math 服务：使用 stdio 传输协议，通过启动本地 Python 脚本运行
   - weather 服务：使用 streamable-http 传输协议，连接到固定 HTTP 端点
3. 调用 client.get_tools() 获取所有工具的 LangChain Tool 对象列表
4. 使用 asyncio.run() 在同步上下文中安全执行异步获取操作

【关键参数说明】
- transport: 传输协议类型
  - "stdio"：通过标准输入输出通信，适合本地进程间调用，客户端自动启动服务端进程
  - "streamable_http"：通过 HTTP 协议通信，适合远程服务或需要独立部署的场景
- command: stdio 模式下启动服务端的命令（如 "python"）
- args: stdio 模式下传递给命令的参数列表（如服务端脚本路径）
- url: streamable-http 模式下 MCP 服务的 HTTP 端点地址

【应用场景】
- 智能体需要集成多个外部工具服务时的统一装配
- 本地工具（如数学计算）使用 stdio 协议，远程工具（如天气API）使用 HTTP 协议
- 通过 MCP 协议实现工具的即插即用，无需修改智能体核心代码
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


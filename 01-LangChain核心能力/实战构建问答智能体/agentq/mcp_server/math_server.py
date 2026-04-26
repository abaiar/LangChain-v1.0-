"""
第二章 2.5.3 集成MCP工具层 — Math MCP 服务端

【章节学习重点】
- FastMCP 的使用：通过 @mcp.tool() 装饰器将 Python 函数注册为 MCP 工具
- stdio 传输协议的特点：通过标准输入输出通信，适合本地进程间调用
- stdio 模式下的调试技巧：使用 stderr 输出调试信息，避免干扰 MCP 协议通信

【代码功能】
提供最基础的算术工具（加法 add、乘法 multiply），通过 stdio 传输协议供 LangChain MCP 客户端调用。
这是实战项目中数学计算能力的后端服务。

【实现思路】
1. 创建 FastMCP 实例，命名为 "Math"
2. 使用 @mcp.tool() 装饰器注册两个工具函数：
   - add(a, b)：计算两数之和
   - multiply(a, b)：计算两数之积
3. 每个工具函数内部使用 sys.stderr 输出调试信息（stdio 模式下 stdout 被 MCP 协议占用）
4. 通过 mcp.run(transport="stdio") 启动服务

【关键参数说明】
- FastMCP("Math"): 创建名为 "Math" 的 MCP 服务，名称用于客户端识别
- @mcp.tool(): 装饰器，将函数注册为 MCP 工具，函数名即为工具名，docstring 即为工具描述
- a, b: 整数参数，MCP 会自动根据类型注解生成参数 Schema
- transport="stdio": 使用标准输入输出作为通信通道

【应用场景】
- 为智能体提供精确的数学计算能力，避免 LLM 直接计算可能产生的错误
- 作为 MCP 工具服务的基础模板，可扩展更多数学工具（减法、除法、幂运算等）
- stdio 模式适合本地开发调试，客户端自动启动服务端进程
"""
import sys
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两数之和，同时输出调试信息便于排查。"""
    print(f"-----> [Math Server] Adding {a} and {b}", file=sys.stderr)
    result = a + b
    print(f"-----> [Math Server] Result: {result}", file=sys.stderr)
    return result

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """计算两数之积，同时输出调试信息便于排查。"""
    print(f"-----> [Math Server] Multiplying {a} and {b}", file=sys.stderr)
    result = a * b
    print(f"-----> [Math Server] Result: {result}", file=sys.stderr)
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")
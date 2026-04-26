"""
第二章 2.4.4 MCP的使用 — Math MCP服务端

【章节学习重点】
- MCP（Model Context Protocol）是 LangChain 的工具协议标准
- FastMCP 是 MCP 的 Python 实现框架，可快速创建 MCP 服务
- MCP 支持两种传输协议：stdio（标准输入输出）和 streamable-http（HTTP服务）
- @mcp.tool() 装饰器将函数注册为 MCP 工具，自动提取名称、描述和参数Schema

【代码功能】
创建一个名为 "Math" 的 MCP 服务，提供两个基础算术工具：
1. add(a, b): 两数相加
2. multiply(a, b): 两数相乘
使用 stdio 传输协议，适合作为子进程被 MCP 客户端启动。

【实现思路】
1. 使用 FastMCP("Math") 创建 MCP 服务实例
2. 使用 @mcp.tool() 装饰器注册工具函数
3. 函数的 docstring 成为工具描述，类型注解成为参数 Schema
4. mcp.run(transport="stdio") 启动服务，通过标准输入输出通信

【关键参数说明】
- FastMCP("Math"): 创建 MCP 服务，"Math" 为服务名称
- @mcp.tool(): 将函数注册为 MCP 工具的装饰器
- transport="stdio": 通过标准输入输出通信，适合子进程模式
  客户端通过 command + args 启动此脚本，自动建立通信管道
- transport="streamable-http": 通过 HTTP 通信，适合独立服务模式

【应用场景】
- 将现有 Python 函数封装为标准化的 MCP 工具服务
- 数学计算、数据处理等通用工具的标准化暴露
- 多个 Agent 共享同一套工具服务
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")

"""
第二章 2.3.1 工具的定义

【章节学习重点】
- LangChain 中工具（Tool）的定义方式：使用 @tool 装饰器将函数转为工具
- 工具的三要素：名称（name）、描述（description）、参数Schema（args）
- 工具的描述和参数类型信息会被传递给模型，模型据此决定是否调用工具

【代码功能】
演示使用 @tool 装饰器定义最基础的工具，并展示工具的三个核心属性：
name（工具名称）、description（工具描述）、args（参数Schema）。

【实现思路】
1. 使用 @tool 装饰器修饰一个普通 Python 函数
2. 装饰器自动从函数签名和 docstring 提取工具元信息：
   - name: 函数名
   - description: 函数的 docstring
   - args: 从类型注解自动生成的 JSON Schema
3. 工具可通过 invoke() 方法手动调用

【关键参数说明】
- @tool: 装饰器，将函数注册为 LangChain 工具
- 函数签名中的类型注解（a: int, b: int）会被自动转为参数 Schema
- 函数的 docstring 会成为工具的 description，模型通过它理解工具用途
- multiply.name: 工具名称，默认为函数名
- multiply.description: 工具描述，默认为函数 docstring
- multiply.args: 参数的 JSON Schema，描述每个参数的名称和类型

【应用场景】
- 为智能体定义可调用的工具
- 将现有 Python 函数快速封装为 LLM 可调用的工具
- 工具定义是构建 Agent 的基础步骤
"""
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """返回两个整数相乘的结果"""
    return a * b

print(multiply.name)
print(multiply.description)
print(multiply.args)

print(multiply.invoke({"a": 3, "b": 4}))

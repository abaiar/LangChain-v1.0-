"""
第二章 2.3.2 工具的基本使用 — 自定义工具名称和描述

【章节学习重点】
- @tool 装饰器的高级参数：自定义工具名称（name）和描述（description）
- 工具参数Schema的高级定义：通过装饰器参数覆盖默认值
- 工具名称和描述对模型决策的影响

【代码功能】
演示如何通过 @tool 装饰器参数自定义工具的名称和描述，
而非依赖默认的函数名和 docstring。这对于工具的对外展示和模型理解至关重要。

【实现思路】
1. 使用 @tool("exchange_rate_helper", description="...") 格式自定义工具元信息
2. 第一个参数为自定义工具名称，替代默认的函数名 convert_currency
3. description 参数提供更详细的工具用途说明，帮助模型判断何时调用
4. 函数内部的 docstring 仍保留，作为工具的辅助说明

【关键参数说明】
- @tool 第一个参数: 自定义工具名称，如 "exchange_rate_helper"
  默认为函数名 convert_currency，自定义后模型看到的是 exchange_rate_helper
- description: 工具描述，比 docstring 更详细，直接传递给模型
  好的描述应包含：工具用途、适用场景、输入输出说明
- convert_currency.name: 输出 "exchange_rate_helper"（自定义名称）
- convert_currency.description: 输出自定义描述文本

【应用场景】
- 工具函数名不够直观时，自定义更语义化的名称
- 需要为模型提供更丰富的工具描述以提升工具选择准确性
- 同名工具的区分（不同模块有相同功能但不同实现）
"""
from langchain.tools import tool

@tool(
    "exchange_rate_helper",
    description="用于进行人民币与美元之间的汇率换算。当用户询问金额转换时使用此工具。"
)
def convert_currency(amount: float, to_currency: str) -> str:
    """执行基础的货币汇率换算（示例比例：1 USD = 7.2 CNY）。"""
    rate = 7.2
    if to_currency.lower() == "usd":
        result = amount / rate
        return f"{amount} 人民币 ≈ {result:.2f} 美元"
    elif to_currency.lower() == "cny":
        result = amount * rate
        return f"{amount} 美元 ≈ {result:.2f} 人民币"
    else:
        return "暂不支持该货币类型。"

print(convert_currency.name)
print(convert_currency.description)
print(convert_currency.invoke({"amount": 100, "to_currency": "USD"}))

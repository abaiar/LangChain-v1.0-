"""
第二章 2.3.2 工具的基本使用 — invoke调用与参数传递

【章节学习重点】
- 工具的 invoke() 调用方式：支持字典参数和简化字符串参数
- 不同参数类型的工具调用方式差异
- 工具参数类型注解对调用方式的影响

【代码功能】
演示两种工具调用方式：
1. 多参数工具：使用字典传入参数（如 {"user_id": "U001", "is_active": True}）
2. 单参数工具：可直接传入字符串，无需包装为字典

【实现思路】
1. 定义多参数工具 process_user_data，包含 str 和 bool 类型参数
2. 使用 invoke() + 字典参数调用多参数工具
3. 定义单参数工具 simple_greeting，仅包含一个 str 参数
4. 使用 invoke() + 字符串直接调用单参数工具

【关键参数说明】
- invoke(): 工具调用方法，接受字典或字符串作为输入
- 多参数工具：invoke() 必须传入字典，键名与函数参数名一致
- 单参数工具：invoke() 可直接传入字符串，框架自动匹配到唯一参数
- @tool 装饰器：自动从函数签名提取参数 Schema

【应用场景】
- 理解工具调用的参数传递机制
- 为智能体定义不同参数复杂度的工具
- 调试工具的独立调用和验证
"""
from langchain.tools import tool

@tool
def process_user_data(user_id: str, is_active: bool) -> str:
    """
    根据用户ID和活动状态，更新用户记录。
    
    参数:
      user_id (str): 用户的唯一标识符。
      is_active (bool): 表示用户是否处于活动状态 (True/False)。
    """
    status = "激活" if is_active else "禁用"
    return f"用户ID: {user_id} 已成功更新为 {status} 状态。"

tool_input_dict = {"user_id": "U001", "is_active": True}
print("--- 传入字典参数 ---")
result = process_user_data.invoke(tool_input_dict) 
print(f"调用结果: {result}") 
print("-" * 30)

@tool
def simple_greeting(name: str) -> str:
    """对给定的人名说一句问候语。"""
    return f"你好，{name}！"

print("--- 传入简化的字符串 ---")
result_simple = simple_greeting.invoke("张三")
print(f"调用结果: {result_simple}")

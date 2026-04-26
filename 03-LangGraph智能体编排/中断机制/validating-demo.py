"""
第四章 4.4.1 中断机制 — interrupt 循环验证输入

【章节学习重点】
- interrupt() 的循环验证模式：在 while 循环中反复中断直到获得有效输入
- 表单数据校验的实现方式：中断-验证-重新提示的循环
- interrupt() 返回值的类型处理

【代码功能】
演示 interrupt() 的循环验证模式。
通过 while 循环反复中断，提示用户输入年龄，
直到获得有效的正整数输入为止。

【实现思路】
1. 定义 FormState 状态类
2. 创建 get_age_node，在 while True 循环中使用 interrupt()
3. 验证 interrupt() 返回的值是否为有效正整数
4. 有效则返回状态更新，无效则更新提示信息继续循环
5. 编译图并执行验证流程

【关键参数说明】
- interrupt(prompt): 中断并显示提示信息
- Command(resume=value): 传入用户输入作为 interrupt() 的返回值
- while True 循环: 反复中断直到获得有效输入
- isinstance(answer, int) and answer > 0: 输入验证逻辑

【应用场景】
- 表单数据的交互式校验
- 需要多次提示用户直到输入合法的场景
- 复杂业务规则的数据采集
"""
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

# ========== 1. 状态定义 ==========
class FormState(TypedDict):
    """表单状态类型定义"""
    age: int | None  # 年龄，可以是整数或 None

# ========== 2. 节点定义 ==========
def get_age_node(state: FormState):
    """
    收集年龄节点：通过中断机制循环提示用户输入，直到获得有效数据
    
    Args:
        state: 当前状态，包含年龄字段
        
    Returns:
        dict: 更新后的状态，包含有效的年龄值
    """
    prompt = "请输入您的年龄："

    # 循环提示，直到获得有效输入
    while True:
        # 中断执行，提示用户输入；负载信息会出现在 result["__interrupt__"] 中
        answer = interrupt(prompt)

        # 验证输入：必须是正整数
        if isinstance(answer, int) and answer > 0:
            return {"age": answer}

        # 输入无效，更新提示信息，继续循环
        prompt = f"'{answer}' 不是有效的年龄。请输入一个正整数。"

# ========== 3. 构建图 ==========
builder = StateGraph(FormState)
builder.add_node("collect_age", get_age_node)
builder.add_edge(START, "collect_age")
builder.add_edge("collect_age", END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# ========== 4. 执行演示 ==========
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "validating1"}}
    
    # 第一次执行：工作流在收集年龄节点中断
    first = graph.invoke({"age": None}, config=config)
    print("第一次中断信息:")
    print(first["__interrupt__"])
    
    # 提供无效数据；节点会重新提示
    retry = graph.invoke(Command(resume="三十"), config=config)
    print("\n无效输入后的中断信息（包含错误提示）:")
    print(retry["__interrupt__"])
    
    # 提供有效数据；循环退出，状态更新
    final = graph.invoke(Command(resume=30), config=config)
    print("\n最终年龄:")
    print(final["age"])
"""
第四章 4.3.4 持久化执行 — 可中断工作流示例

【章节学习重点】
- 持久化执行的概念：工作流因异常中断后可从检查点恢复
- 检查点在异常恢复中的作用：保存执行进度，失败后可重试
- InMemorySaver 配合异常处理的模式

【代码功能】
演示可中断工作流的持久化执行机制。
模拟一个可能随机失败的操作节点，当执行失败时，
通过检查点保存中断时的状态，便于排查和恢复。

【实现思路】
1. 定义 InterruptibleState 状态类
2. 创建 risky_step 节点，模拟50%概率失败
3. 编译图时指定 InMemorySaver 作为 checkpointer
4. 执行工作流，捕获异常
5. 异常发生时通过 get_state() 查看中断时的状态

【关键参数说明】
- InMemorySaver(): 内存检查点，确保工作流状态在异常时不会丢失
- random.choice([True, False]): 模拟随机失败
- get_state(config): 异常后获取中断时的状态快照
- thread_id: 线程标识，用于定位特定执行实例的检查点

【应用场景】
- 需要容错能力的长时间运行工作流
- 调用外部API可能失败的场景
- 需要在失败后重试或人工干预的工作流
"""
import random
import operator
from typing import Dict, Annotated, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

# ========== 1. 状态定义 ==========
class InterruptibleState(TypedDict):
    """可中断工作流状态"""
    messages: Annotated[list, operator.add]
    current_step: str

# ========== 2. 节点定义 ==========
def risky_step(state: InterruptibleState) -> Dict[str, Any]:
    """模拟可能失败的操作"""
    if random.choice([True, False]):
        raise Exception("模拟随机错误！工作流中断！")
    return {"messages": ["成功完成危险步骤!"], "current_step": "completed"}

# ========== 3. 构建图 ==========
def create_interruptible_graph():
    """创建可中断的工作流图"""
    builder = StateGraph(InterruptibleState)
    builder.add_node("risky_operation", risky_step)
    builder.add_edge(START, "risky_operation")
    builder.add_edge("risky_operation", END)
    
    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)

# ========== 4. 执行演示 ==========
def print_state(title: str, state: Any):
    """打印状态信息"""
    print(f"\n{title}")
    print("-" * 50)
    if state and hasattr(state, "values"):
        print(f"当前步骤: {state.values.get('current_step', 'N/A')}")
        print(f"消息: {state.values.get('messages', [])}")
    else:
        print(state if state else "状态为空")

if __name__ == "__main__":
    graph = create_interruptible_graph()
    config: RunnableConfig = {"configurable": {"thread_id": "interruptible_thread"}}
    
    try:
        print("=== 第一次执行 ===")
        result = graph.invoke(
            {"messages": ["开始执行"], "current_step": "start"}, 
            config=config
        )
        print("\n执行成功:")
        print(f"  当前步骤: {result.get('current_step', 'N/A')}")
        print(f"  消息: {result.get('messages', [])}")
    except Exception as e:
        print(f"\n执行中断: {e}")
        current_state = graph.get_state(config)
        print_state("中断时的状态", current_state)

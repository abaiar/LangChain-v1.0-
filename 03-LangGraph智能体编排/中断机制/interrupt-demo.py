"""
第四章 4.4.1 中断机制 — interrupt() 基本使用与审批工作流

【章节学习重点】
- interrupt() 函数的使用：暂停工作流执行，等待外部输入
- Command(goto=...) 的路由机制：根据中断恢复值决定后续执行路径
- MemorySaver 与中断的配合：检查点保存中断状态，支持恢复执行
- 中断-恢复的完整生命周期

【代码功能】
演示 interrupt() 的基本使用模式：审批工作流。
工作流在审批节点中断，等待人工决策（批准/拒绝），
根据决策结果路由到不同的后续节点。

【实现思路】
1. 定义 ApprovalState 状态类
2. 创建 approval_node，使用 interrupt() 暂停执行并传递审批信息
3. interrupt() 返回的值来自 Command(resume=decision_value)
4. 根据 decision 值使用 Command(goto=...) 路由到 proceed 或 cancel 节点
5. 编译图时指定 MemorySaver 作为 checkpointer
6. 第一次 invoke 触发中断，第二次 invoke 传入决策恢复执行

【关键参数说明】
- interrupt({"question": ..., "details": ...}): 中断执行，传递信息给调用方
- Command(goto="proceed"/"cancel"): 路由命令，指定下一步执行的节点
- Command(resume=True/False): 恢复命令，传入值作为 interrupt() 的返回值
- MemorySaver(): 内存检查点，中断时保存状态
- __interrupt__: 中断信息，包含 interrupt() 传递的负载

【应用场景】
- 审批流程：转账审批、操作确认等需要人工决策的场景
- 人工干预点：在关键步骤暂停等待人工确认
- 条件路由：根据人工决策选择不同的执行路径
"""
from typing import Literal, Optional, TypedDict, Dict, Any
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

# ========== 1. 状态定义 ==========
class ApprovalState(TypedDict):
    """审批状态"""
    action_details: str
    status: Optional[Literal["pending", "approved", "rejected"]]

# ========== 2. 节点定义 ==========
def approval_node(state: ApprovalState) -> Command[Literal["proceed", "cancel"]]:
    """审批节点：中断执行等待人工决策"""
    decision = interrupt({
        "question": "是否批准此操作？",
        "details": state["action_details"],
    })
    return Command(goto="proceed" if decision else "cancel")

def proceed_node(state: ApprovalState) -> Dict[str, Any]:
    """批准节点"""
    return {"status": "approved"}

def cancel_node(state: ApprovalState) -> Dict[str, Any]:
    """取消节点"""
    return {"status": "rejected"}

# ========== 3. 构建图 ==========
def create_approval_graph():
    """创建审批工作流图"""
    builder = StateGraph(ApprovalState)
    builder.add_node("approval", approval_node)
    builder.add_node("proceed", proceed_node)
    builder.add_node("cancel", cancel_node)
    builder.add_edge(START, "approval")
    builder.add_edge("proceed", END)
    builder.add_edge("cancel", END)
    
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)

# ========== 4. 执行演示 ==========
if __name__ == "__main__":
    graph = create_approval_graph()
    config = {"configurable": {"thread_id": "approval1"}}
    
    print("=== 审批工作流演示 ===\n")
    
    # 第一次执行：工作流在审批节点中断
    initial = graph.invoke(
        {"action_details": "转账500", "status": "pending"},
        config=config
    )
    
    print("中断信息:")
    print(f"  {initial.get('__interrupt__', {})}")
    print("\n等待人工决策...")
    
    # 决策路由说明：
    # interrupt() 返回的值来自 Command(resume=decision_value)
    # - 如果 decision=True，路由到 "proceed" 节点（批准）
    # - 如果 decision=False，路由到 "cancel" 节点（拒绝）
    
    # 示例1：批准决策（decision=True）
    print("\n--- 场景1：批准操作 ---")
    resumed = graph.invoke(Command(resume=True), config=config)
    print(f"最终状态: {resumed.get('status', 'N/A')}")
    
    # 示例2：拒绝决策（需要新的线程ID）
    print("\n--- 场景2：拒绝操作 ---")
    config2 = {"configurable": {"thread_id": "approval2"}}
    initial2 = graph.invoke(
        {"action_details": "转账1000", "status": "pending"},
        config=config2
    )
    resumed2 = graph.invoke(Command(resume=False), config=config2)
    print(f"最终状态: {resumed2.get('status', 'N/A')}")


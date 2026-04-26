"""
第四章 4.4.1 中断机制 — interrupt() 审核编辑模式

【章节学习重点】
- interrupt() 的审核编辑模式：中断后将内容交给人工审核编辑
- Command(resume=edited_content) 恢复执行：传入编辑后的内容继续工作流
- 内容审核工作流的实现模式

【代码功能】
演示 interrupt() 的审核编辑模式。
工作流在审核节点中断，将生成的内容交给审核者编辑，
审核者编辑完成后通过 Command(resume=...) 传入编辑后的内容恢复执行。

【实现思路】
1. 定义 ReviewState 状态类
2. 创建 review_node，使用 interrupt() 暂停并传递待审核内容
3. interrupt() 返回审核者编辑后的内容
4. 将编辑后的内容更新到状态中
5. 编译图时指定 MemorySaver
6. 第一次 invoke 触发中断，第二次 invoke 传入编辑内容恢复

【关键参数说明】
- interrupt({"instruction": ..., "content": ...}): 中断并传递审核信息
- Command(resume="审核后改进的草稿"): 传入编辑后的内容作为 interrupt() 的返回值
- __interrupt__: 中断信息列表，包含审核指令和待审核内容

【应用场景】
- AI 生成内容的审核编辑流程
- 文档起草-审核-定稿工作流
- 需要人工修改 AI 输出后再继续的场景
"""
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

# ========== 1. 状态定义 ==========
class ReviewState(TypedDict):
    """审核状态类型定义"""
    generated_text: str  # 生成的文本内容

# ========== 2. 节点定义 ==========
def review_node(state: ReviewState):
    """
    审核节点：中断执行，等待审核者编辑生成的内容
    
    Args:
        state: 当前状态，包含生成的文本
        
    Returns:
        dict: 更新后的状态，包含编辑后的文本
    """
    # 中断执行，请求审核者编辑生成的内容
    updated = interrupt({
        "instruction": "请审核并编辑此内容",
        "content": state["generated_text"],
    })
    return {"generated_text": updated}

# ========== 3. 构建图 ==========
builder = StateGraph(ReviewState)
builder.add_node("review", review_node)
builder.add_edge(START, "review")
builder.add_edge("review", END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# ========== 4. 执行演示 ==========
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "review1"}}
    
    # 第一次执行：工作流在审核节点中断
    initial = graph.invoke({"generated_text": "初始草稿"}, config=config)
    print("中断信息:")
    print(initial["__interrupt__"])
    
    # 恢复执行：传入审核者编辑后的文本
    final_state = graph.invoke(
        Command(resume="审核后改进的草稿"),
        config=config,
    )
    print("\n最终状态中的文本内容:")
    print(final_state["generated_text"])

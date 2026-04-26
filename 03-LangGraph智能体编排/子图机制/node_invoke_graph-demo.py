"""
第四章 4.4.3 子图机制 — 在节点内部调用子图

【章节学习重点】
- 节点内调用子图的方式：在节点函数中手动调用子图的 invoke() 方法
- 父子图状态的手动转换：需要显式将父图状态转为子图状态，再将结果转回
- subgraphs=True 参数：在 stream() 中查看子图的执行输出

【代码功能】
演示在节点内部调用子图的方式。
与"子图作为节点"不同，这种方式需要手动处理状态转换，
但提供了更灵活的控制能力。

【实现思路】
1. 定义子图状态 SubgraphState（child_value）
2. 构建子图并编译
3. 定义父图状态 State（parent_value）
4. 在 call_subgraph 节点中手动调用 subgraph.invoke()
5. 手动转换：父图状态 → 子图输入 → 子图输出 → 父图状态
6. 使用 subgraphs=True 查看子图执行细节

【关键参数说明】
- subgraph.invoke({"child_value": state["parent_value"]}): 手动调用子图
- call_subgraph: 包装节点，负责状态转换和子图调用
- subgraphs=True: stream() 参数，在输出中包含子图的执行信息
- 手动转换 vs 自动映射: 节点内调用需要手动转换，子图作为节点则自动映射

【应用场景】
- 需要对子图输入输出进行自定义转换的场景
- 子图状态与父图状态差异较大时的灵活处理
- 需要在调用子图前后执行额外逻辑的场景
"""
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START

# ========== 1. 定义子图 ==========
class SubgraphState(TypedDict):
    """子图状态"""
    child_value: str

def subgraph_node_1(state: SubgraphState):
    """子图节点"""
    return {"child_value": "你好! " + state["child_value"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# ========== 2. 定义父图 ==========
class State(TypedDict):
    """父图状态"""
    parent_value: str

def call_subgraph(state: State):
    """在节点内部调用子图"""
    # 将父图状态转换为子图状态并调用子图
    subgraph_output = subgraph.invoke({"child_value": state["parent_value"]})
    # 将子图输出转换回父图状态
    return {"parent_value": subgraph_output["child_value"]}

# ========== 3. 构建图 ==========
builder = StateGraph(State)
builder.add_node("node_1", call_subgraph)
builder.add_edge(START, "node_1")
graph = builder.compile()

# ========== 4. 执行演示 ==========
if __name__ == "__main__":
    for chunk in graph.stream({"parent_value": "今天天气不错"}, subgraphs=True):
        print(chunk)


"""
第四章 4.4.3 子图机制 — 子图作为节点直接添加到父图

【章节学习重点】
- 子图作为节点的添加方式：将编译后的子图直接作为节点添加到父图
- 父子图状态共享机制：通过同名字段实现状态自动映射
- 子图私有状态：子图可以有父图不具备的私有字段

【代码功能】
演示将子图作为节点直接添加到父图的方式。
子图和父图通过 parent_value 字段共享状态，
子图还有自己的私有字段 child_value。

【实现思路】
1. 定义子图状态 SubgraphState（parent_value + child_value）
2. 构建子图：subgraph_node_1 → subgraph_node_2
3. 定义父图状态 ParentState（仅 parent_value）
4. 将编译后的子图直接作为节点添加：builder.add_node("node_2", subgraph)
5. 父子图自动通过同名字段 parent_value 交换数据

【关键参数说明】
- SubgraphState: 子图状态，包含共享字段和私有字段
- ParentState: 父图状态，只包含共享字段
- builder.add_node("node_2", subgraph): 将编译后的子图作为节点
- 共享字段: 父子图中同名的字段会自动映射和同步

【应用场景】
- 将复杂工作流拆分为可复用的子图模块
- 团队协作中不同模块的独立开发和集成
- 需要封装内部逻辑同时暴露必要接口的场景
"""
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START

# ========== 1. 定义子图 ==========
class SubgraphState(TypedDict):
    """子图状态"""
    parent_value: str  # 与父图共享
    child_value: str  # 子图私有

def subgraph_node_1(state: SubgraphState):
    """子图节点1"""
    return {"child_value": "你好！"}

def subgraph_node_2(state: SubgraphState):
    """子图节点2：更新共享状态"""
    return {"parent_value": state["child_value"] + state["parent_value"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph = subgraph_builder.compile()

# ========== 2. 定义父图 ==========
class ParentState(TypedDict):
    """父图状态"""
    parent_value: str  # 与子图共享

def node_1(state: ParentState):
    """父图节点1"""
    return {"parent_value": state["parent_value"]}

# ========== 3. 构建图 ==========
builder = StateGraph(ParentState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", subgraph)  # 将子图直接作为节点
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
graph = builder.compile()

# ========== 4. 执行演示 ==========
if __name__ == "__main__":
    for chunk in graph.stream({"parent_value": "今天天气不错"}):
        print(chunk)
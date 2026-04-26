"""
第四章 4.4.2 流式输出 — stream() 多模式流式输出示例

【章节学习重点】
- stream() 方法的多种 stream_mode：updates/values/debug
- 同步流式输出和异步流式输出的使用
- 不同流式模式的输出格式差异

【代码功能】
演示 LangGraph stream() 方法的多种流式输出模式：
1. stream_mode="updates"：输出每个节点的状态更新增量
2. stream_mode=["updates", "values"]：多模式组合输出
3. stream_mode="debug"：输出调试信息，包含图的执行细节

【实现思路】
1. 定义 State 状态类（topic + story）
2. 创建两个节点：refine_topic 和 generate_story
3. 使用链式 API 构建图
4. 分别用三种 stream_mode 执行流式输出

【关键参数说明】
- stream_mode="updates": 只输出节点执行后的状态增量
- stream_mode="values": 输出每个步骤后的完整状态
- stream_mode="debug": 输出调试信息（节点名、执行时间等）
- stream_mode=["updates", "values"]: 多模式组合，输出元组 (mode, data)
- astream(): 异步流式输出方法

【应用场景】
- 实时展示工作流执行进度
- 调试图执行流程
- 前端逐步渲染 AI 生成内容
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import asyncio

# ========== 1. 状态定义 ==========
class State(TypedDict):
    """状态类型定义"""
    topic: str  # 主题
    story: str  # 故事内容

# ========== 2. 节点定义 ==========
def refine_topic(state: State):
    """
    精炼主题节点：在原有主题基础上添加内容
    
    Args:
        state: 当前状态，包含主题
        
    Returns:
        dict: 更新后的状态，包含精炼后的主题
    """
    return {"topic": state["topic"] + "的故事"}


def generate_story(state: State):
    """
    生成故事节点：根据主题生成故事
    
    Args:
        state: 当前状态，包含主题
        
    Returns:
        dict: 更新后的状态，包含生成的故事
    """
    return {"story": f"这是一个关于{state['topic']}"}

# ========== 3. 构建图 ==========
graph = (
    StateGraph(State)
    .add_node("refine_topic", refine_topic)      # 添加精炼主题节点
    .add_node("generate_story", generate_story)  # 添加生成故事节点
    .add_edge(START, "refine_topic")             # 从开始节点到精炼主题节点
    .add_edge("refine_topic", "generate_story")  # 从精炼主题节点到生成故事节点
    .add_edge("generate_story", END)             # 从生成故事节点到结束节点
    .compile()                                   # 编译图
)

# ========== 4. 执行演示 ==========
if __name__ == "__main__":
    print("=== 同步指定流模式输出 ===")
    for chunk in graph.stream(
        {"topic": "童话"},  # 初始状态：主题为"童话"
        stream_mode="updates",
    ):
        print(chunk)
    
    print("\n=== 异步多模式流式输出 ===")
    async def stream_demo():
        async for chunk in graph.astream(
            {"topic": "猫"},
            stream_mode=["updates", "values"],
        ):
            print(chunk)
    asyncio.run(stream_demo())
    
    print("\n=== 调试模式流式输出 ===")
    for chunk in graph.stream(
        {"topic": "日常"},
        stream_mode="debug",
    ):
        print(chunk)

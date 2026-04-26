"""
第五章 5.3.2 子智能体 — 文本编辑器子图实现

【章节学习重点】
- 使用 LangGraph 构建子智能体图：StateGraph 作为子智能体的核心
- 子图的独立状态管理：子图有自己的状态定义和节点逻辑

【代码功能】
实现一个文本润色智能体子图，使用 LangGraph StateGraph 构建。

【关键参数说明】
- StateGraph: LangGraph 状态图，作为子智能体的执行框架
- Annotated: 自定义状态字段的归约函数

【应用场景】
- 作为 CompiledSubAgent 的子图实现
- 文本处理类的子智能体
"""

import operator
from typing_extensions import TypedDict, Annotated
from langchain.messages import AnyMessage, SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END

# 初始化聊天模型
model = init_chat_model(
    model="deepseek-chat",
    temperature=0.3,
    api_key="xxxxxx",
    base_url="https://api.deepseek.com/v1",
    model_provider="openai"
)

# 定义状态结构：消息列表
class TextEditorState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# 文本润色节点：调用模型进行文本润色
def rewrite_node(state: TextEditorState) -> TextEditorState:
    response = model.invoke(
        [
            SystemMessage(
                content=(
                    "你是一名中文文本润色助手..."
                )
            )
        ] + state["messages"]
    )
    return {"messages": [response]}

# 构建图：START -> rewrite -> END
graph_builder = StateGraph(TextEditorState)
graph_builder.add_node("rewrite", rewrite_node)
graph_builder.add_edge(START, "rewrite")
graph_builder.add_edge("rewrite", END)

# 编译图得到可执行的智能体
text_editor_agent = graph_builder.compile()

if __name__ == "__main__":
    result = text_editor_agent.invoke(
        {"messages": [HumanMessage(content="请将以下文本进行润色：今天天气真不错，适合出去玩。")]},
    )
    print(result["messages"][-1].content)
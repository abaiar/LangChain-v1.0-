"""
第四章 4.4.2 流式输出 — LLM Token 级别流式输出示例

【章节学习重点】
- stream_mode="messages" 的使用：获取 LLM 的 token 级别流式输出
- message_chunk 的结构：包含 content 字段的部分 token
- dataclass 状态定义方式：与 TypedDict 的对比

【代码功能】
演示 stream_mode="messages" 实现 LLM token 级别的流式输出。
每个 token 实时输出，实现打字机效果的流式响应。

【实现思路】
1. 使用 @dataclass 定义 MyState 状态类
2. 初始化 DeepSeek 模型
3. 定义 call_model 节点，调用 LLM 生成故事
4. 使用 stream_mode="messages" 获取 token 级别流式输出
5. 逐 token 打印，实现打字机效果

【关键参数说明】
- @dataclass: Python 数据类装饰器，LangGraph 也支持 dataclass 作为状态
- stream_mode="messages": 返回 (message_chunk, metadata) 元组
- message_chunk.content: 当前 token 的文本内容
- flush=True: 立即刷新输出缓冲区，确保实时显示

【应用场景】
- 聊天界面的实时流式响应
- 长文本生成的进度展示
- 需要逐 token 显示的交互场景
"""
from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START

# ========== 1. 状态定义 ==========
@dataclass
class MyState:
    """状态类"""
    topic: str 
    story: str = "" 

# ========== 2. 初始化模型 ==========
model = init_chat_model(
    model="deepseek-chat",
    temperature=0.7,
    api_key="xxxxxx",
    base_url="https://api.deepseek.com/v1",
    model_provider="openai"
)

# ========== 3. 节点定义 ==========
def call_model(state: MyState):
    """调用 LLM 生成故事"""
    model_response = model.invoke(
        [
            {"role": "user", "content": f"生成一个关于 {state.topic} 的故事"}
        ]
    )
    return {"story": model_response.content}

# ========== 4. 构建图 ==========
graph = (
    StateGraph(MyState)
    .add_node(call_model)
    .add_edge(START, "call_model")
    .compile()
)

# ========== 5. 执行演示 ==========
if __name__ == "__main__":
    # stream_mode="messages" 返回 (message_chunk, metadata) 元组
    # message_chunk 是 LLM 流式输出的 token
    for message_chunk, metadata in graph.stream(
        {"topic": "悬疑"},
        stream_mode="messages",
    ):
        if message_chunk.content:
            print(message_chunk.content, end="|", flush=True)
"""
第四章 4.4.2 流式输出 — 自定义流式数据输出示例

【章节学习重点】
- get_stream_writer() 的使用：在节点和工具中发送自定义流式数据
- stream_mode="custom" 的使用：接收自定义键值对流式数据
- 自定义流式数据与节点执行的解耦：进度信息独立于状态更新

【代码功能】
演示 get_stream_writer() 在节点和工具中发送自定义流式数据。
通过 stream_mode="custom" 接收进度更新等自定义信息，
实现工作流执行进度的实时推送。

【实现思路】
1. 定义 State 状态类（query + answer）
2. 创建 query_database_tool 工具，使用 get_stream_writer() 发送进度
3. 定义 process_query 和 query_database 节点
4. 在节点中也使用 get_stream_writer() 发送状态信息
5. 使用 stream_mode="custom" 接收自定义流式数据

【关键参数说明】
- get_stream_writer(): 获取流式写入器，可在节点和工具中调用
- writer({"data": ..., "type": "progress"}): 发送自定义键值对
- stream_mode="custom": 只接收通过 get_stream_writer() 发送的自定义数据
- @tool: LangChain 工具装饰器，工具中也可使用 get_stream_writer()

【应用场景】
- 工作流执行进度的实时推送
- 自定义监控指标的流式输出
- 前端进度条和状态提示的实现
"""
from typing import TypedDict
from langgraph.config import get_stream_writer
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END

# ========== 1. 状态定义 ==========
class State(TypedDict):
    """状态类型定义"""
    query: str    # 查询内容
    answer: str   # 查询结果

# ========== 2. 工具定义 ==========
@tool
def query_database_tool(query: str) -> str:
    """
    查询数据库工具：执行数据库查询
    
    Args:
        query: 查询内容
        
    Returns:
        str: 查询结果
    """
    # 访问流式写入器以发送自定义数据
    writer = get_stream_writer()
    
    # 发送第一个进度更新
    writer({"data": "已检索 0/100 条记录", "type": "progress"})
    
    # 执行查询（模拟）
    # 这里可以执行实际的数据库查询操作
    
    # 发送第二个进度更新
    writer({"data": "已检索 100/100 条记录", "type": "progress"})
    
    # 返回查询结果
    return f"查询 '{query}' 的结果：找到 100 条相关记录"

# ========== 3. 节点定义 ==========
def process_query(state: State):
    """
    处理查询节点：验证和预处理查询请求
    
    Args:
        state: 当前状态，包含查询内容
        
    Returns:
        dict: 更新后的状态，包含处理后的查询
    """
    # 获取流式写入器以发送自定义数据
    writer = get_stream_writer()
    # 发送自定义键值对（例如：进度更新）
    writer({"status": "正在处理查询请求...", "type": "progress"})
    
    # 验证和预处理查询
    processed_query = state["query"].strip()
    if not processed_query:
        processed_query = "默认查询"
    
    writer({"status": f"查询已处理：{processed_query}", "type": "info"})
    return {"query": processed_query}


def query_database(state: State):
    """
    查询数据库节点：调用数据库查询工具
    
    Args:
        state: 当前状态，包含处理后的查询
        
    Returns:
        dict: 更新后的状态，包含查询结果
    """
    # 调用数据库查询工具
    result = query_database_tool.invoke(state["query"])
    return {"answer": result}

# ========== 4. 构建图 ==========
graph = (
    StateGraph(State)
    .add_node("process_query", process_query)        # 添加处理查询节点
    .add_node("query_database", query_database)      # 添加查询数据库节点
    .add_edge(START, "process_query")                # 从开始到处理查询节点
    .add_edge("process_query", "query_database")     # 从处理查询到查询数据库
    .add_edge("query_database", END)                 # 从查询数据库到结束
    .compile()                                       # 编译图
)

# ========== 5. 执行演示 ==========
if __name__ == "__main__":
    # 输入数据
    inputs = {"query": "用户信息"}
    
    # 设置 stream_mode="custom" 以在流中接收自定义数据
    print("=== 自定义流式输出 ===")
    for chunk in graph.stream(inputs, stream_mode="custom"):
        print(chunk)
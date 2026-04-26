"""
第四章 4.5.8 集成持久化管理与智能体调度器 — Agent Runner 模块

【章节学习重点】
- 图的编译与单例管理：应用级别共享编译后的图实例
- interrupt 与恢复的封装：invoke_once 和 resume_with_decision 的配合
- 流式输出的封装：stream_updates 方法

【代码功能】
封装理赔流程图的调用入口，提供三种调用方式：
1. invoke_once: 执行一次图，遇到 interrupt 会在返回结果中包含 __interrupt__
2. resume_with_decision: 人工审批后恢复执行
3. stream_updates: 流式输出执行进度

【关键参数说明】
- build_main_graph(): 构建主图（包含所有子图和业务逻辑）
- get_checkpointer(): 获取检查点实例，支持持久化执行
- Command(resume=decision_payload): 恢复命令，传入审批决策
- thread_id: 线程标识，用于管理不同理赔案件的执行状态

【应用场景】
- 理赔流程的后端调度入口
- Streamlit 前端与图执行的桥接层
"""
from typing import Dict, Any, Iterator
from langgraph.types import Command
from agent.graphs.main_graph import build_main_graph
from agent.persistence import get_checkpointer

# 构建并编译图（应用级别单例）
_builder = build_main_graph()
_app = _builder.compile(checkpointer=get_checkpointer())

def get_app():
    return _app

def invoke_once(initial_state: Dict[str, Any], thread_id: str) -> Dict[str, Any]:
    """执行一次图。如果中间遇到 interrupt，会在返回结果中包含 __interrupt__ 字段。"""
    config = {"configurable": {"thread_id": thread_id}}
    result: Dict[str, Any] = _app.invoke(initial_state, config=config)
    return result

def resume_with_decision(decision_payload: Dict[str, Any], thread_id: str) -> Dict[str, Any]:
    """当 approval_node 触发 interrupt 后，用人工决策恢复执行。"""
    config = {"configurable": {"thread_id": thread_id}}
    cmd = Command(resume=decision_payload)
    result: Dict[str, Any] = _app.invoke(cmd, config=config)
    return result

def stream_updates(initial_state: Dict[str, Any], thread_id: str) -> Iterator[Dict[str, Any]]:
    """使用 stream_mode='updates' 进行 streaming，可用于 CLI 或前端进度展示。"""
    config = {"configurable": {"thread_id": thread_id}}
    for chunk in _app.stream(initial_state, config=config, stream_mode="updates"):
        yield chunk

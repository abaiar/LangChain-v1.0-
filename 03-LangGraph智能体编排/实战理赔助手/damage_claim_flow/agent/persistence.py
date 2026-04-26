"""
第四章 4.5.8 集成持久化管理与智能体调度器 — 持久化模块

【章节学习重点】
- MemorySaver 的单例管理：应用级别共享检查点实例
- 持久化与演示环境的区分：内存存储用于演示，生产应替换为数据库

【代码功能】
提供检查点实例的单例管理，使用 MemorySaver 进行内存持久化。

【应用场景】
- 演示环境的快速持久化方案
- 生产环境应替换为 SqliteSaver 或 PostgresSaver
"""
from langgraph.checkpoint.memory import MemorySaver

# In-memory checkpointer，用于演示持久化和耐久执行。
_memory = MemorySaver()


def get_checkpointer() -> MemorySaver:
    return _memory

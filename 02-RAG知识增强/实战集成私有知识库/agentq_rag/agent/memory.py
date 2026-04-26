"""
第三章 3.4 实战集成私有知识库 — 对话短期记忆模块

【章节学习重点】
- 滑动窗口记忆机制：控制对话历史长度，避免超出模型上下文限制
- 短期记忆的适用场景：单次会话内的对话管理

【代码功能】
提供轻量级滑动窗口记忆 ConversationWindow，用于保存最近若干轮会话消息。
基于内存存储（不落库），适合单次运行期间的短期对话管理。

【实现思路】
1. ConversationWindow 类维护消息缓冲区 buffer
2. add() 方法新增消息并自动裁剪窗口
3. get() 方法返回当前窗口消息
4. clear() 方法清空缓冲区
5. build_memory() 工厂方法创建实例

【关键参数说明】
- window_size: 窗口大小（轮数），默认5轮
- buffer: 内部消息缓冲区

【应用场景】
- 单次会话的短期记忆管理
- 配合 AgentRunner 使用
"""
from typing import List
from langchain_core.messages import BaseMessage


class ConversationWindow:
    """
    对话短期记忆窗口。
    - 基于内存存储（仅进程内存储，不落库）
    - 按 window_size 控制保留最近若干轮对话消息
    """

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.buffer: List[BaseMessage] = []

    def add(self, msgs: List[BaseMessage]):
        """新增消息并自动裁剪窗口"""
        self.buffer.extend(msgs)
        print(f"-----> Memory: Adding messages: {self.buffer}")
        if len(self.buffer) > self.window_size * 2:
            self.buffer = self.buffer[-self.window_size * 2 :]

    def get(self) -> List[BaseMessage]:
        """返回当前会话窗口中的消息"""
        print(f"-----> Memory: Getting messages: {self.buffer}")
        return list(self.buffer)

    def clear(self):
        """清空对话缓存"""
        print(f"-----> Memory: Clearing messages: {self.buffer}")
        self.buffer = []
        print(f"-----> Memory: Cleared messages: {self.buffer}")

def build_memory(window_size: int = 5) -> ConversationWindow:
    """工厂方法：创建对话记忆对象"""
    return ConversationWindow(window_size=window_size)

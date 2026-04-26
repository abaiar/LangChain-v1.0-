"""
第二章 2.5 实战构建问答智能体 — 对话短期记忆模块

【章节学习重点】
- 智能体对话记忆的管理方式：滑动窗口机制
- 短期记忆（窗口记忆）与长期记忆（持久化存储）的区别
- 记忆窗口大小的选择对智能体上下文理解能力的影响

【代码功能】
提供轻量级滑动窗口记忆 ConversationWindow，用于保存最近若干轮会话消息。
基于内存存储（不落库），适合单次运行期间的短期对话管理。

【实现思路】
1. ConversationWindow 类维护一个消息缓冲区 buffer（List[BaseMessage]）
2. add() 方法：新增消息并自动裁剪窗口
   - 当消息数量超过 window_size * 2 时，只保留最近 window_size * 2 条消息
   - 乘以2是因为一轮对话包含一条用户消息和一条AI消息
3. get() 方法：返回当前窗口中的消息列表（副本）
4. clear() 方法：清空缓冲区
5. build_memory() 工厂方法：创建 ConversationWindow 实例

【关键参数说明】
- window_size: 窗口大小（轮数），默认5轮。即保留最近5轮=10条消息
- buffer: 内部消息缓冲区，存储 BaseMessage 对象列表
- msgs: 新增的消息列表，通常为一轮对话的所有消息

【应用场景】
- 单次会话的短期记忆管理，避免上下文过长导致模型调用超限
- 配合 AgentRunner 使用，在每次调用后自动裁剪历史消息
- 适合不需要跨会话持久化的轻量级对话场景
- 若需跨会话持久化，应使用第四章介绍的 Checkpoint 机制
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

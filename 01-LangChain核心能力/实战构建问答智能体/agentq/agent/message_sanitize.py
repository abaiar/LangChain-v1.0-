"""
第二章 2.5 实战构建问答智能体 — 消息内容规范化模块

【章节学习重点】
- LangChain 消息对象的 content 字段可能为字符串或块列表（Block List）两种格式
- 部分模型接口（如 DeepSeek）要求 content 必须为字符串，不支持块列表格式
- 消息规范化是智能体与不同模型对接时的必要兼容处理

【代码功能】
将消息的 content 字段统一规范化为字符串格式，兼容 DeepSeek 等要求 content 不能为块列表的模型接口。
提供三个层级的转换函数：单内容转换、单消息转换、对话列表批量转换。

【实现思路】
1. stringify_content(content)：处理单个 content 字段
   - 若 content 为 None → 返回空字符串
   - 若 content 已是字符串 → 直接返回
   - 若 content 为列表（块列表格式）→ 遍历每个块，提取文本内容后拼接
     - 字符串块：直接追加
     - 字典块：优先取 "text" 键或 type="text" 的文本，否则 JSON 序列化
     - 对象块：尝试取 .text 属性，否则 str() 转换
   - 其他类型 → str() 转换
2. stringify_message(msg)：对单条消息进行转换，若 content 已是字符串则跳过
3. stringify_dialog(messages)：批量转换消息列表，用于整个对话历史的规范化

【关键参数说明】
- content: 消息内容，可能为 str / None / list[dict] / list[str] 等多种格式
- msg: BaseMessage 对象，LangChain 消息基类（HumanMessage/AIMessage 等的父类）
- messages: 消息序列，通常为完整的对话历史

【应用场景】
- 切换不同模型提供方时确保消息格式兼容
- 处理多模态模型返回的块列表格式内容（如图文混合回复）
- 在智能体流水线中对消息进行预处理，避免格式不匹配导致的调用失败
"""
from __future__ import annotations

import json
from typing import Any, List, Sequence

from langchain_core.messages import BaseMessage


def stringify_content(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if "text" in block:
                    parts.append(str(block["text"]))
                elif block.get("type") == "text":
                    parts.append(str(block.get("text", "")))
                else:
                    parts.append(json.dumps(block, ensure_ascii=False))
            else:
                text = getattr(block, "text", None)
                parts.append(str(text) if text is not None else str(block))
        return "\n".join(parts)
    return str(content)


def stringify_message(msg: BaseMessage) -> BaseMessage:
    if isinstance(msg.content, str):
        return msg
    return msg.model_copy(update={"content": stringify_content(msg.content)})


def stringify_dialog(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    return [stringify_message(m) for m in messages]

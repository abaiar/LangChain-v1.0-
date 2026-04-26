"""
第二章 2.2.3 ChatPromptTemplate的构建

【章节学习重点】
- ChatPromptTemplate 是 LangChain 中构建对话提示词模板的核心工具
- Prompt机制从简单字符串演进到结构化 Messages 列表，ChatPromptTemplate 是这一演进的产物
- 模板支持变量占位符（如 {topic}），运行时动态填充

【代码功能】
演示如何使用 ChatPromptTemplate 创建包含 system 和 user 角色的提示词模板，
并通过变量替换渲染出完整的消息列表。

【实现思路】
1. 使用 ChatPromptTemplate.from_messages() 定义消息模板列表
2. 每个元素是 (角色, 内容模板) 的元组，角色包括 "system"、"user"、"assistant"
3. 使用 {变量名} 语法定义占位符
4. 调用 invoke() 传入变量值，生成完整的消息列表
5. 也可使用 format_prompt() 获取格式化后的文本

【关键参数说明】
- from_messages(): 接受消息元组列表，每个元组为 (role, content_template)
- role: 消息角色，"system" 设定行为准则，"user" 用户输入，"assistant" AI回复
- {topic}: 变量占位符，调用时通过字典传入实际值
- invoke(): 渲染模板，返回 PromptValue 对象
- to_messages(): 将 PromptValue 转为 Message 对象列表
- format_prompt().to_string(): 转为纯文本格式

【应用场景】
- 构建可复用的对话提示词模板
- 批量生成不同主题的问答提示
- 与 LLM Chain 配合实现自动化提示词管理
"""
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的AI助理。"),
    ("user", "请用简短的语言解释：{topic}")
])

pv = chat_prompt.invoke({"topic": "LangChain 的核心理念"})

print("=== ChatPromptTemplate 结果 ===")
for msg in pv.to_messages():
    print(msg.content)

print("\n=== 格式化后的文本 ===")
print(chat_prompt.format_prompt(topic="LangChain 的核心理念").to_string())

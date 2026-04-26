"""
第二章 2.1.2 使用ChatGPT — 示例1：直接使用ChatOpenAI类

【章节学习重点】
- LangChain模型接口的统一性：不同模型提供方可以通过统一的接口调用
- ChatOpenAI是LangChain中最常用的聊天模型封装类，可直接对接OpenAI的GPT系列模型

【代码功能】
演示如何使用 langchain_openai.ChatOpenAI 直接创建并调用 ChatGPT 模型。
这是最基础的模型调用方式，适合快速验证 OpenAI 模型的连通性。

【实现思路】
1. 导入 ChatOpenAI 类（LangChain 对 OpenAI Chat 模型的封装）
2. 通过构造函数指定模型名称、温度参数和 API Key
3. 调用 invoke() 方法发送提示词并获取响应
4. 从响应对象中提取 content 字段输出结果

【关键参数说明】
- model: 模型名称，如 "gpt-4o-mini"（轻量版GPT-4o）、"gpt-4o"、"gpt-3.5-turbo" 等
- temperature: 控制输出随机性，范围0-1。0=确定性输出，1=最大随机性。创意任务建议0.7，精确任务建议0
- api_key: OpenAI API密钥，也可通过环境变量 OPENAI_API_KEY 设置

【应用场景】
- 快速验证OpenAI模型连通性
- 单轮问答、文本生成、信息提取等基础LLM调用
"""
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key="xxxxxxx"
)

response = model.invoke("请解释LangChain模型接口的统一性。")
print(response.content)

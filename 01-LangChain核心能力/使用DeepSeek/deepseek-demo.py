"""
第二章 2.1.3 使用DeepSeek

【章节学习重点】
- DeepSeek 是国产大模型，提供 OpenAI 兼容接口，可通过 LangChain 无缝接入
- 掌握 base_url 参数的使用：当模型提供方兼容 OpenAI 协议时，只需更改 base_url 即可切换
- 流式输出（stream）的使用方法

【代码功能】
演示如何通过 LangChain 的统一接口 init_chat_model 调用 DeepSeek 模型，
并使用流式输出（stream）逐字打印模型响应。

【实现思路】
1. 使用 init_chat_model 创建模型，指定 model_provider="openai"
2. 通过 base_url 参数指向 DeepSeek 的 API 端点
3. 调用 model.stream() 进行流式输出，逐 token 获取响应

【关键参数说明】
- model: "deepseek-chat" 为通用对话模型，"deepseek-reasoner" 为推理增强模型
- base_url: DeepSeek API 端点地址 "https://api.deepseek.com/v1"
  DeepSeek 兼容 OpenAI 协议，因此 model_provider 设为 "openai"
- api_key: DeepSeek 平台的 API Key
- model.stream(): 流式调用方法，返回迭代器，每个 chunk 包含一个 token

【流式输出 vs 同步输出】
- invoke(): 同步调用，等待完整响应后返回，适合批量处理
- stream(): 流式调用，逐 token 返回，适合实时展示（如聊天界面）

【应用场景】
- 聊天机器人的实时响应展示
- 需要国产模型替代方案的场景
- 对推理能力有较高要求时可切换 deepseek-reasoner 模型
"""
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="deepseek-chat",
    temperature=0.7,
    api_key="xxxxxx",
    base_url="https://api.deepseek.com/v1",
    model_provider="openai"
)

for chunk in model.stream("天为什么是蓝色的"):
    print(chunk.content, end="")

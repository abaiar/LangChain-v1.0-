"""
第二章 2.1.2 使用ChatGPT — 示例2：使用统一接口init_chat_model

【章节学习重点】
- LangChain 1.0 推荐使用 init_chat_model 统一接口创建模型
- 统一接口的优势：同一套代码只需更改 model_provider 参数即可切换不同模型提供方

【代码功能】
演示如何使用 langchain.chat_models.init_chat_model 统一接口创建 ChatGPT 模型。
init_chat_model 是 LangChain 提供的工厂函数，通过 model_provider 参数自动选择
对应的模型实现类，无需手动导入不同的模型类。

【实现思路】
1. 导入 init_chat_model 工厂函数
2. 指定模型名称、温度、API Key 和 model_provider
3. init_chat_model 内部根据 model_provider 自动选择正确的模型类实例化
4. 调用 invoke() 方法获取响应

【关键参数说明】
- model: 模型名称字符串，具体取值取决于提供方（如 "gpt-4o-mini"、"deepseek-chat"）
- model_provider: 模型提供方标识，如 "openai"、"anthropic"、"google" 等
  指定后 init_chat_model 会自动路由到对应的模型实现类
- temperature: 同上，控制输出随机性

【与示例1的对比】
- 示例1（ChatOpenAI）：直接使用特定模型类，需要知道确切的类名
- 示例2（init_chat_model）：使用统一工厂函数，切换模型只需改参数，代码更灵活

【应用场景】
- 需要在多个模型提供方之间灵活切换的场景
- 生产环境中通过配置文件动态选择模型
"""
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key="xxxxxxxx",
    model_provider="openai"
)

response = model.invoke("请用一句话总结LangChain的核心设计思想。")
print(response.content)

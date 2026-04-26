"""
第二章 2.1.4 使用Qwen系列模型

【章节学习重点】
- 通义千问（Qwen）是阿里云推出的大语言模型系列
- LangChain 通过 langchain_community.llms.tongyi.Tongyi 类集成 Qwen
- 注意：Tongyi 类是 LLM（文本补全）接口，非 Chat 接口

【代码功能】
演示如何使用 LangChain 的 Tongyi 类调用通义千问文本补全模型。
Tongyi 类封装了阿里云 DashScope API，支持 qwen-plus、qwen-turbo、qwen-max 等模型。

【实现思路】
1. 安装 dashscope SDK（pip3 install -U dashscope）
2. 导入 Tongyi 类（位于 langchain_community 包中）
3. 指定模型名称和 API Key 创建实例
4. 调用 invoke() 方法获取文本补全结果

【关键参数说明】
- model: Qwen 模型名称，常用选项：
  - "qwen-plus": 均衡型，性价比高，适合大多数场景
  - "qwen-turbo": 速度优先，适合实时交互
  - "qwen-max": 能力最强，适合复杂推理任务
- api_key: 阿里云 DashScope API Key
- temperature: 控制输出随机性

【注意事项】
- Tongyi 是 LLM 接口（单轮文本补全），如需多轮对话建议使用 Chat 模型接口
- 需要先安装 dashscope: pip3 install -U dashscope

【应用场景】
- 中文文本生成与理解任务
- 需要国产模型且对中文能力有要求的场景
- 阿里云生态内的应用集成
"""
from langchain_community.llms.tongyi import Tongyi

model = Tongyi(
    model="qwen-plus",
    api_key="xxxxxx",
    temperature=0.7
)

result = model.invoke("请解释 LangChain 的核心理念。")
print(result)

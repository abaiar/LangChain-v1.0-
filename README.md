# 🤖 LangChain v1.0 实战学习笔记

[English](./README_EN.md) | 中文

> 基于 LangChain 1.0 的系统化学习项目，从模型接口到智能体编排，从 RAG 知识增强到可观测性评估，覆盖 LangChain 生态核心技术栈的完整实战代码。

## 📖 项目概述

本项目是学习 LangChain v1.0 的配套代码仓库，按照由浅入深的学习路线，涵盖以下核心领域：

- **LangChain 核心能力**：模型接口、消息机制、工具定义、MCP 协议、中间件体系
- **RAG 知识增强**：文档加载、切分、向量化、检索、向量数据库
- **LangGraph 智能体编排**：状态图、检查点、中断机制、流式输出、子图
- **Deep Agent**：面向复杂任务的智能体框架，支持子智能体、Backend 存储、人工协作
- **LangSmith 可观测性**：项目追踪、评估数据集、LLM-as-a-judge

每个章节包含概念讲解的示例代码和完整的实战项目，可直接运行体验。

## ✨ 主要功能

| 模块 | 功能 |
|------|------|
| 🔗 模型接口 | ChatGPT / DeepSeek / Qwen 多模型统一调用 |
| 💬 消息机制 | SystemMessage / HumanMessage / AIMessage / ToolMessage |
| 🛠️ 工具定义 | @tool 装饰器、ToolRuntime、MCP 协议集成 |
| 🛡️ 中间件 | 预置中间件、装饰器中间件、类中间件三层体系 |
| 📚 RAG | PDF/Notion 加载 → 切分 → DashScope Embedding → Milvus 检索 |
| 🕸️ LangGraph | StateGraph、条件边、Send 并行、检查点、中断恢复 |
| 🤖 Deep Agent | 自主规划、子智能体、Backend 存储、人工协作 |
| 📊 LangSmith | 数据集创建、评估器构建、LLM-as-a-judge |
| 🎯 实战项目 | 问答智能体、知识库问答、理赔助手、Deep Research |

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 核心框架 | LangChain 1.0+ / LangGraph 1.0+ / DeepAgents 0.2+ |
| LLM 模型 | DeepSeek / OpenAI GPT / Qwen (通义千问) |
| Embedding | DashScope Embeddings (text-embedding-v4) |
| 向量数据库 | Milvus |
| MCP 协议 | FastMCP / langchain-mcp-adapters |
| 前端界面 | Streamlit |
| 可观测性 | LangSmith |
| 搜索 API | Tavily |

## 📂 目录结构

```
LangChain-v1.0-/
├── 01-LangChain核心能力/              # 模型接口、消息、工具、MCP、中间件、智能体
│   ├── 使用ChatGPT/                   # ChatGPT 模型调用示例
│   ├── 使用DeepSeek/                  # DeepSeek 模型调用示例
│   ├── 使用Qwen模型/                  # 通义千问模型调用示例
│   ├── 使用Qwen生成图片/              # Qwen 图像生成示例
│   ├── ChatPromptTemplate构建/        # 提示词模板构建
│   ├── 消息的使用/                    # 消息类型（System/Human/AI/Tool）
│   ├── 工具的定义/                    # @tool 装饰器定义工具
│   ├── 工具的基本使用/                # 工具调用与自定义名称
│   ├── ToolRuntime与执行机制/         # 工具运行时机制
│   ├── 智能体与ReAct机制/             # Agent 创建与 ReAct 循环
│   ├── 结构化输出/                    # 结构化输出示例
│   ├── MCP的使用/                     # MCP 服务端与客户端
│   ├── 预置中间件/                    # SummarizationMiddleware / HITL
│   ├── 装饰器中间件/                  # @before_agent / @after_model 等
│   ├── 类中间件/                      # AgentMiddleware 继承实现
│   └── 实战构建问答智能体/            # 🎯 完整问答智能体项目
│       └── agentq/
│           ├── agent/                 # Runner / Prompts / Middlewares / Memory / MCP Tools
│           ├── mcp_server/            # Math MCP + Weather MCP
│           └── app_streamlit.py       # Streamlit 前端
│
├── 02-RAG知识增强/                    # 文档处理、向量化、检索、向量数据库
│   ├── 文档加载/                      # PyPDFLoader / NotionDBLoader
│   ├── 文档切分/                      # 长度切分 / 递归切分 / Markdown切分 / 语义切分
│   ├── 文档向量化/                    # DashScope Embedding
│   ├── 文档检索/                      # InMemoryVectorStore 相似度检索
│   ├── 向量数据库基本使用/            # Milvus 完整示例
│   └── 实战集成私有知识库/            # 🎯 问答智能体 + RAG 知识库
│       └── agentq_rag/
│           ├── agent/                 # Runner + CompanyKB + Prompts + Middlewares
│           ├── mcp_server/            # Math MCP + Weather MCP
│           └── files/                 # PDF 知识库文件
│
├── 03-LangGraph智能体编排/            # 状态图、检查点、中断、流式、子图
│   ├── 快速上手LangGraph/             # StateGraph 完整示例 + Functional API
│   ├── 线程与检查点/                  # InMemorySaver / 状态历史
│   ├── 持久化执行/                    # 可中断工作流 + 检查点恢复
│   ├── 存储与长期记忆/                # InMemoryStore / 语义搜索
│   ├── 中断机制/                      # interrupt() / 审批 / 工具审批 / 循环验证
│   ├── 流式输出/                      # stream() 多模式 / Token 流 / 自定义流
│   ├── 子图机制/                      # 子图作为节点 / 节点内调用子图
│   └── 实战理赔助手/                  # 🎯 破损商品智能理赔助手
│       └── damage_claim_flow/
│           ├── agent/                 # State / Runner / Graphs / Logic / Prompts
│           └── data/                  # 理赔案例数据
│
├── 04-DeepAgent复杂任务智能体/        # Deep Agent 框架
│   ├── 快速上手DeepAgent/             # create_deep_agent 基本使用
│   ├── Backend存储体系/               # State / Store / Filesystem / Composite Backend
│   ├── 子智能体/                      # SubAgent / CompiledSubAgent / 文本编辑器子图
│   ├── 人工协作/                      # 子智能体 HITL / 多工具审批
│   ├── 中间件体系/                    # TodoList / SubAgent / Filesystem 中间件
│   └── 实战DeepResearch/              # 🎯 Deep Research 智能体
│       └── deep_research_planner/
│           ├── agent/                 # Runner / SubAgents / WriterGraph / Backends
│           └── files/                 # 研究输出目录
│
└── 05-LangSmith可观测性与评估/        # LangSmith 平台
    ├── 评估数据集使用/                # 数据集创建与管理
    └── 评估器构建与执行/              # LLM-as-a-judge 评估
```

## 🚀 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/your-username/LangChain-v1.0-demo.git
cd LangChain-v1.0-demo
```

### 2. 创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. 安装依赖

每个实战项目有独立的 `requirements.txt`，按需安装：

```bash
# 第一章：问答智能体
pip install -r 01-LangChain核心能力/实战构建问答智能体/agentq/requirements.txt

# 第二章：RAG 知识库问答
pip install -r 02-RAG知识增强/实战集成私有知识库/agentq_rag/requirements.txt

# 第三章：理赔助手
pip install -r 03-LangGraph智能体编排/实战理赔助手/damage_claim_flow/requirements.txt

# 第四章：Deep Research
pip install -r 04-DeepAgent复杂任务智能体/实战DeepResearch/deep_research_planner/requirements.txt
```

### 4. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# DashScope (通义千问)
DASHSCOPE_API_KEY=your_dashscope_api_key

# OpenAI API (可选)
OPENAI_API_KEY=your_openai_api_key

# LangSmith (可选，用于可观测性)
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true

# Tavily (Deep Research 搜索)
TAVILY_API_KEY=your_tavily_api_key
```

### 5. 外部服务（按需启动）

- **Milvus**：第二章 RAG 示例需要，默认连接 `http://localhost:19530`
- **Weather MCP Server**：第一章/第二章实战项目需要，启动命令见各项目说明

## 📖 使用方法

### 运行基础示例

每个子目录下的 `*-demo.py` 文件都是独立可运行的示例：

```bash
# 运行 ChatGPT 示例
python 01-LangChain核心能力/使用ChatGPT/chatgpt-demo1.py

# 运行 PDF 加载示例
python 02-RAG知识增强/文档加载/pdf_loader-demo.py

# 运行 LangGraph 基础示例
python 03-LangGraph智能体编排/快速上手LangGraph/langgraph-demo.py
```

### 运行实战项目

实战项目使用 Streamlit 提供 Web 界面：

```bash
# 第一章：问答智能体
streamlit run 01-LangChain核心能力/实战构建问答智能体/agentq/app_streamlit.py

# 第二章：RAG 知识库问答（需先启动 Milvus 和 Weather MCP Server）
streamlit run 02-RAG知识增强/实战集成私有知识库/agentq_rag/app_streamlit.py

# 第三章：理赔助手
streamlit run 03-LangGraph智能体编排/实战理赔助手/damage_claim_flow/app_streamlit.py

# 第四章：Deep Research
streamlit run 04-DeepAgent复杂任务智能体/实战DeepResearch/deep_research_planner/app_streamlit.py
```

## 🗺️ 学习路线

```
第1步：LangChain 核心能力 ──────→ 掌握模型/消息/工具/中间件
   │
第2步：RAG 知识增强 ──────────→ 掌握文档处理/向量化/检索
   │
第3步：LangGraph 智能体编排 ──→ 掌握状态图/检查点/中断/流式
   │
第4步：Deep Agent ────────────→ 掌握复杂任务/子智能体/人工协作
   │
第5步：LangSmith 可观测性 ────→ 掌握追踪/评估/质量保障
```

## 🤝 贡献指南

欢迎对本项目提出改进建议！请遵循以下步骤：

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 **Pull Request**

### 贡献规范

- 代码风格：遵循 PEP 8，使用中文注释
- 提交信息：使用简洁明了的中文或英文描述
- 新增示例：请参照现有目录结构和注释格式
- Bug 修复：请附上问题描述和复现步骤

## 📄 许可证

本项目仅供学习参考使用。代码基于 MIT 许可证开源，详见 [LICENSE](./LICENSE) 文件。

## ⚠️ 免责声明

- 本项目中的 API Key 均为占位符（`xxxxxx`），请替换为自己的密钥
- 部分示例需要外部服务（Milvus、MCP Server 等），请确保服务已启动
- 代码仅供学习参考，生产环境使用请进行充分的安全审查和性能优化

---

> 💡 如果本项目对你有帮助，欢迎 Star ⭐ 支持！

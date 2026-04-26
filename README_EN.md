# 🤖 LangChain v1.0 Practical Learning Notes

English | [中文](./README.md)

> A systematic learning project based on LangChain 1.0, covering the complete practical code from model interfaces to agent orchestration, from RAG knowledge enhancement to observability and evaluation.

## 📖 Project Overview

This repository is a companion codebase for learning LangChain v1.0, following a progressive learning path covering:

- **LangChain Core Capabilities**: Model interfaces, message mechanisms, tool definitions, MCP protocol, middleware systems
- **RAG Knowledge Enhancement**: Document loading, splitting, vectorization, retrieval, vector databases
- **LangGraph Agent Orchestration**: State graphs, checkpoints, interrupt mechanisms, streaming output, subgraphs
- **Deep Agent**: Framework for complex task agents, supporting sub-agents, Backend storage, human-in-the-loop
- **LangSmith Observability**: Project tracing, evaluation datasets, LLM-as-a-judge

Each chapter includes conceptual example code and complete practical projects that can be run directly.

## ✨ Key Features

| Module | Features |
|--------|----------|
| 🔗 Model Interface | Unified calling for ChatGPT / DeepSeek / Qwen |
| 💬 Message Mechanism | SystemMessage / HumanMessage / AIMessage / ToolMessage |
| 🛠️ Tool Definition | @tool decorator, ToolRuntime, MCP protocol integration |
| 🛡️ Middleware | Three-tier system: built-in / decorator-based / class-based |
| 📚 RAG | PDF/Notion loading → Splitting → DashScope Embedding → Milvus retrieval |
| 🕸️ LangGraph | StateGraph, conditional edges, Send parallel, checkpoints, interrupt recovery |
| 🤖 Deep Agent | Autonomous planning, sub-agents, Backend storage, human-in-the-loop |
| 📊 LangSmith | Dataset creation, evaluator building, LLM-as-a-judge |
| 🎯 Practical Projects | Q&A Agent, Knowledge Base Q&A, Claims Assistant, Deep Research |

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Core Framework | LangChain 1.0+ / LangGraph 1.0+ / DeepAgents 0.2+ |
| LLM Models | DeepSeek / OpenAI GPT / Qwen (Tongyi Qianwen) |
| Embedding | DashScope Embeddings (text-embedding-v4) |
| Vector Database | Milvus |
| MCP Protocol | FastMCP / langchain-mcp-adapters |
| Frontend | Streamlit |
| Observability | LangSmith |
| Search API | Tavily |

## 📂 Directory Structure

```
LangChain-v1.0-demo/
├── 01-LangChain核心能力/              # Model, Message, Tool, MCP, Middleware, Agent
│   ├── 使用ChatGPT/                   # ChatGPT model examples
│   ├── 使用DeepSeek/                  # DeepSeek model examples
│   ├── 使用Qwen模型/                  # Qwen model examples
│   ├── 使用Qwen生成图片/              # Qwen image generation
│   ├── ChatPromptTemplate构建/        # Prompt template construction
│   ├── 消息的使用/                    # Message types (System/Human/AI/Tool)
│   ├── 工具的定义/                    # @tool decorator examples
│   ├── 工具的基本使用/                # Tool invocation basics
│   ├── ToolRuntime与执行机制/         # Tool runtime mechanism
│   ├── 智能体与ReAct机制/             # Agent creation & ReAct loop
│   ├── 结构化输出/                    # Structured output examples
│   ├── MCP的使用/                     # MCP server & client
│   ├── 预置中间件/                    # SummarizationMiddleware / HITL
│   ├── 装饰器中间件/                  # @before_agent / @after_model etc.
│   ├── 类中间件/                      # AgentMiddleware inheritance
│   └── 实战构建问答智能体/            # 🎯 Complete Q&A Agent Project
│       └── agentq/
│           ├── agent/                 # Runner / Prompts / Middlewares / Memory / MCP Tools
│           ├── mcp_server/            # Math MCP + Weather MCP
│           └── app_streamlit.py       # Streamlit frontend
│
├── 02-RAG知识增强/                    # Document processing, vectorization, retrieval
│   ├── 文档加载/                      # PyPDFLoader / NotionDBLoader
│   ├── 文档切分/                      # Length / Recursive / Markdown / Semantic splitting
│   ├── 文档向量化/                    # DashScope Embedding
│   ├── 文档检索/                      # InMemoryVectorStore similarity search
│   ├── 向量数据库基本使用/            # Milvus complete example
│   └── 实战集成私有知识库/            # 🎯 Q&A Agent + RAG Knowledge Base
│       └── agentq_rag/
│           ├── agent/                 # Runner + CompanyKB + Prompts + Middlewares
│           ├── mcp_server/            # Math MCP + Weather MCP
│           └── files/                 # PDF knowledge base files
│
├── 03-LangGraph智能体编排/            # State graph, checkpoint, interrupt, streaming, subgraph
│   ├── 快速上手LangGraph/             # StateGraph complete example + Functional API
│   ├── 线程与检查点/                  # InMemorySaver / state history
│   ├── 持久化执行/                    # Interruptible workflow + checkpoint recovery
│   ├── 存储与长期记忆/                # InMemoryStore / semantic search
│   ├── 中断机制/                      # interrupt() / approval / tool approval / loop validation
│   ├── 流式输出/                      # stream() modes / Token stream / custom stream
│   ├── 子图机制/                      # Subgraph as node / invoke subgraph in node
│   └── 实战理赔助手/                  # 🎯 Damage Claims Assistant
│       └── damage_claim_flow/
│           ├── agent/                 # State / Runner / Graphs / Logic / Prompts
│           └── data/                  # Claims case data
│
├── 04-DeepAgent复杂任务智能体/        # Deep Agent framework
│   ├── 快速上手DeepAgent/             # create_deep_agent basics
│   ├── Backend存储体系/               # State / Store / Filesystem / Composite Backend
│   ├── 子智能体/                      # SubAgent / CompiledSubAgent / Text editor subgraph
│   ├── 人工协作/                      # Sub-agent HITL / Multi-tool approval
│   ├── 中间件体系/                    # TodoList / SubAgent / Filesystem middleware
│   └── 实战DeepResearch/              # 🎯 Deep Research Agent
│       └── deep_research_planner/
│           ├── agent/                 # Runner / SubAgents / WriterGraph / Backends
│           └── files/                 # Research output directory
│
└── 05-LangSmith可观测性与评估/        # LangSmith platform
    ├── 评估数据集使用/                # Dataset creation and management
    └── 评估器构建与执行/              # LLM-as-a-judge evaluation
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/LangChain-v1.0-demo.git
cd LangChain-v1.0-demo
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

Each practical project has its own `requirements.txt`:

```bash
# Chapter 1: Q&A Agent
pip install -r 01-LangChain核心能力/实战构建问答智能体/agentq/requirements.txt

# Chapter 2: RAG Knowledge Base Q&A
pip install -r 02-RAG知识增强/实战集成私有知识库/agentq_rag/requirements.txt

# Chapter 3: Claims Assistant
pip install -r 03-LangGraph智能体编排/实战理赔助手/damage_claim_flow/requirements.txt

# Chapter 4: Deep Research
pip install -r 04-DeepAgent复杂任务智能体/实战DeepResearch/deep_research_planner/requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# DashScope (Qwen)
DASHSCOPE_API_KEY=your_dashscope_api_key

# OpenAI API (optional)
OPENAI_API_KEY=your_openai_api_key

# LangSmith (optional, for observability)
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true

# Tavily (Deep Research search)
TAVILY_API_KEY=your_tavily_api_key
```

### 5. External Services (as needed)

- **Milvus**: Required for Chapter 2 RAG examples, default connection `http://localhost:19530`
- **Weather MCP Server**: Required for Chapter 1/2 practical projects, see project docs for startup commands

## 📖 Usage

### Run Basic Examples

Each subdirectory contains standalone `*-demo.py` files:

```bash
# Run ChatGPT example
python 01-LangChain核心能力/使用ChatGPT/chatgpt-demo1.py

# Run PDF loading example
python 02-RAG知识增强/文档加载/pdf_loader-demo.py

# Run LangGraph basic example
python 03-LangGraph智能体编排/快速上手LangGraph/langgraph-demo.py
```

### Run Practical Projects

Practical projects use Streamlit for web interface:

```bash
# Chapter 1: Q&A Agent
streamlit run 01-LangChain核心能力/实战构建问答智能体/agentq/app_streamlit.py

# Chapter 2: RAG Knowledge Base Q&A (requires Milvus and Weather MCP Server)
streamlit run 02-RAG知识增强/实战集成私有知识库/agentq_rag/app_streamlit.py

# Chapter 3: Claims Assistant
streamlit run 03-LangGraph智能体编排/实战理赔助手/damage_claim_flow/app_streamlit.py

# Chapter 4: Deep Research
streamlit run 04-DeepAgent复杂任务智能体/实战DeepResearch/deep_research_planner/app_streamlit.py
```

## 🗺️ Learning Path

```
Step 1: LangChain Core ──────────→ Master Model/Message/Tool/Middleware
   │
Step 2: RAG Enhancement ─────────→ Master Document Processing/Vectorization/Retrieval
   │
Step 3: LangGraph Orchestration ─→ Master State Graph/Checkpoint/Interrupt/Streaming
   │
Step 4: Deep Agent ──────────────→ Master Complex Tasks/Sub-agents/Human-in-the-loop
   │
Step 5: LangSmith Observability ─→ Master Tracing/Evaluation/Quality Assurance
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a **Pull Request**

### Contribution Guidelines

- Code style: Follow PEP 8, use Chinese comments
- Commit messages: Use clear and concise Chinese or English descriptions
- New examples: Follow existing directory structure and comment format
- Bug fixes: Include problem description and reproduction steps

## 📄 License

This project is for learning reference only. Code is open-sourced under the MIT License, see [LICENSE](./LICENSE) file.

## ⚠️ Disclaimer

- API Keys in this project are placeholders (`xxxxxx`), please replace with your own keys
- Some examples require external services (Milvus, MCP Server, etc.), ensure they are running
- Code is for learning reference only; conduct thorough security review and performance optimization for production use

---

> 💡 If this project helps you, please consider giving it a Star ⭐!

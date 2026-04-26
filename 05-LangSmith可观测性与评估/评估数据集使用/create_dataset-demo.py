"""
第六章 6.3.2 评估数据集的使用 — LangSmith 数据集创建示例

【章节学习重点】
- LangSmith Client 的使用：与 LangSmith 平台交互的核心客户端
- 数据集的创建与管理：通过 API 创建评估数据集
- 评估数据集在 LLM 评估流程中的作用

【代码功能】
演示如何使用 LangSmith Client 创建评估数据集，
为后续的评估器执行提供标准化的测试数据。

【实现思路】
1. 加载环境变量（LangSmith API Key 等）
2. 初始化 LangSmith Client
3. 创建数据集并添加示例数据

【关键参数说明】
- Client(): LangSmith 客户端，自动读取环境变量中的 API Key
- create_dataset(): 创建数据集
- 数据集: 评估的输入输出标准，用于衡量 LLM 应用的质量

【应用场景】
- LLM 应用的质量评估
- A/B 测试不同模型或提示词的效果
- 持续监控 AI 应用的输出质量
"""
import os
from langsmith import Client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化LangSmith客户端
client = Client()

# 线程ID，用于筛选特定的对话会话
thread_id = "cb1a5665-070c-46d7-a4c1-af3ecfdd83b6"

# 获取数据集
datasets = client.list_datasets(dataset_name="drp-eval-basic-v1")
dataset = next(datasets)

# 构建过滤器字符串，用于查找包含指定thread_id的trace
filter_string = (
    f'and(in(metadata_key, ["session_id","conversation_id","thread_id"]), '
    f'eq(metadata_value, "{thread_id}"))'
)

# 获取最后一次trace（根节点）
last_trace_iters = client.list_runs(
    project_name=os.getenv("LANGSMITH_PROJECT"),
    filter=filter_string,
    is_root=True,
)

if last_trace_iters:
    # 定义输出字段的映射关系：索引 -> 字段名
    md_name_dict = {
        0: "research_notes_output",
        1: "outline_output",
        2: "report_output",
    }
    
    # 创建示例字典，初始化所有输出字段为空字符串
    example = {
        "inputs": {"human_input": ""},
        "outputs": {
            "research_notes_output": "",
            "outline_output": "",
            "report_output": "",
            "summary_output": "",
        }
    }
    
    # 按开始时间排序，获取最后一次trace
    last_trace = sorted(last_trace_iters, key=lambda r: r.start_time)[-1]
    
    # 从trace中提取messages列表
    messages = last_trace.outputs.get("messages", [{}])
    
    # 提取human输入（第一条消息）
    human_input = messages[0].get("content", "")
    example["inputs"]["human_input"] = human_input
    
    # 提取summary输出（最后一条消息）
    summary_output = messages[-1].get("content", "")
    example["outputs"]["summary_output"] = summary_output
    
    # 遍历messages，提取工具调用的输出
    output_idx = 0
    for msg in messages:
        # 检查是否为AI消息且包含工具调用
        tool_calls = msg.get("tool_calls", [])
        is_ai_with_tool = (
            msg.get("type", "") == "ai"
            and tool_calls
            and tool_calls[0].get("name") == "write_file"
        )
        
        if is_ai_with_tool:
            # 根据索引获取对应的输出字段名
            md_name = md_name_dict[output_idx]
            # 提取工具调用的内容
            example["outputs"][md_name] = (
                tool_calls[0].get("args", {}).get("content", "")
            )
            output_idx += 1
    
    # 创建示例并添加到数据集
    client.create_example(dataset_id=dataset.id, **example)
else:
    print("No last trace found")
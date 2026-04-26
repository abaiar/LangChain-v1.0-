"""
第二章 2.3.4 ToolRuntime与执行机制

【章节学习重点】
- ToolRuntime 是 LangChain 工具的运行时上下文对象，提供对 context、state、store 的访问
- 工具不再是无状态函数，可以通过 ToolRuntime 获取运行环境信息
- ToolRuntime 由 LangGraph 框架在工具调用时自动注入，开发者无需手动创建

【代码功能】
演示 ToolRuntime 的核心能力：
1. runtime.context: 访问不可变的上下文信息（如用户ID、权限等）
2. runtime.state: 访问可变的对话状态（如消息列表）
3. runtime.store: 访问持久化存储
4. runtime.stream_writer: 流式输出自定义更新

【实现思路】
1. 使用 @dataclass 定义 UserContext 上下文结构
2. 定义 check_user_profile 工具，通过 runtime.context 获取用户信息
3. 定义 get_message_count 工具，通过 runtime.state 获取消息数量
4. 手动构造 ToolRuntime 模拟运行环境（实际由框架自动注入）
5. 分别演示 context 和 state 的访问方式

【关键参数说明】
- ToolRuntime[T]: 泛型类，T 为上下文类型（如 UserContext）
- runtime.context: 不可变上下文，通常包含 user_id、权限等会话级信息
- runtime.state: 可变状态字典，包含 messages 等图状态数据
- runtime.store: 持久化存储（BaseStore），用于跨会话数据
- runtime.stream_writer: 流式写入器，用于实时输出自定义数据
- runtime.config: 运行时配置对象
- runtime.tool_call_id: 当前工具调用的唯一标识

【应用场景】
- 工具需要根据用户身份执行不同逻辑（如权限控制）
- 工具需要读取或修改对话状态
- 工具需要访问持久化存储（如用户偏好、历史记录）
- 需要在工具执行过程中实时推送进度更新
"""
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id: str = "GUEST_001"

@tool
def check_user_profile(runtime: ToolRuntime[UserContext]) -> str:
    """
    检查并返回当前用户的配置信息。
    必须在具有用户上下文的环境中调用。
    """
    current_user_id = runtime.context.user_id
    
    if current_user_id == "GUEST_001":
        return "当前用户未登录，仅能执行公共查询。"
    else:
        return f"用户 {current_user_id} 已登录，具有高级权限。"

@tool
def get_message_count(runtime: ToolRuntime) -> str:
    """获取当前对话中的消息数量"""
    messages = runtime.state.get("messages", [])
    return f"当前对话有 {len(messages)} 条消息"

print("--- 演示 ToolRuntime 的使用 ---\n")

print("场景 1: 通过 runtime.context 访问用户上下文")
mock_context = UserContext(user_id="VIP_456")
mock_state = {"messages": []}

mock_runtime = ToolRuntime(
    context=mock_context,
    state=mock_state,
    config={},
    stream_writer=lambda x: None,
    tool_call_id="mock_tool_call_001",
    store=None
)

result = check_user_profile.invoke({"runtime": mock_runtime})
print(f"✓ 工具返回: {result}\n")

print("场景 2: 通过 runtime.state 访问对话状态")
mock_state_with_messages = {
    "messages": ["msg1", "msg2", "msg3"]
}

mock_runtime2 = ToolRuntime(
    context=None,
    state=mock_state_with_messages,
    config={},
    stream_writer=lambda x: None,
    tool_call_id="mock_tool_call_002",
    store=None
)

result2 = get_message_count.invoke({"runtime": mock_runtime2})
print(f"✓ 工具返回: {result2}\n")

print("=" * 50)
print("说明:")
print("- runtime.context: 访问不可变的上下文信息（如 user_id）")
print("- runtime.state: 访问可变的状态信息（如 messages）")
print("- runtime.store: 访问持久化存储")
print("- runtime.stream_writer: 流式输出自定义更新")
print("\n在实际的 Agent 应用中，ToolRuntime 由 LangGraph")
print("框架自动注入，工具函数无需手动创建。")

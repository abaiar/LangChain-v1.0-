"""
第四章 4.3.3 存储与长期记忆 — InMemoryStore 基本使用示例

【章节学习重点】
- InMemoryStore 的使用：LangGraph 的键值存储，独立于检查点的长期记忆
- 命名空间（namespace）的概念：通过元组组织存储空间，实现多用户/多类型隔离
- Store vs Checkpoint 的区别：Store 用于跨线程共享的长期记忆，Checkpoint 用于线程内状态

【代码功能】
演示 InMemoryStore 的基本操作：创建存储、写入记忆、检索记忆。
通过命名空间实现用户级别的记忆隔离。

【实现思路】
1. 创建 InMemoryStore 实例
2. 定义命名空间（user_id, "memories"）实现用户隔离
3. 使用 put() 方法存储记忆数据
4. 使用 search() 方法检索命名空间中的所有记忆

【关键参数说明】
- InMemoryStore(): 内存键值存储，生产环境应替换为持久化方案
- namespace: 命名空间元组，如 (user_id, "memories")，用于组织和隔离数据
- memory_id: 记忆的唯一标识符，通常使用 UUID
- put(namespace, key, value): 写入数据
- search(namespace): 检索命名空间中的所有数据

【应用场景】
- 跨会话的用户偏好记忆（如饮食偏好、个人信息）
- 多用户系统的记忆隔离
- 智能体的长期知识积累
"""
from langgraph.store.memory import InMemoryStore
import uuid
from typing import Tuple, Dict, Any

# ========== 1. 初始化存储 ==========
def create_store() -> InMemoryStore:
    """创建内存存储实例"""
    return InMemoryStore()

# ========== 2. 存储操作 ==========
def store_memory(
    store: InMemoryStore, 
    namespace: Tuple[str, str], 
    memory_id: str, 
    memory_data: Dict[str, Any]
) -> None:
    """存储记忆到指定命名空间"""
    store.put(namespace, memory_id, memory_data)

def retrieve_memories(store: InMemoryStore, namespace: Tuple[str, str]) -> list:
    """从指定命名空间检索所有记忆"""
    return store.search(namespace)

# ========== 3. 演示 ==========
if __name__ == "__main__":
    # 初始化
    in_memory_store = create_store()
    user_id = "1"
    namespace = (user_id, "memories")
    memory_id = str(uuid.uuid4())
    memory_data = {"food_preference": "我喜欢苹果"}
    
    # 存储记忆
    store_memory(in_memory_store, namespace, memory_id, memory_data)
    print(f"已存储记忆 ID: {memory_id}")
    
    # 检索记忆
    memories = retrieve_memories(in_memory_store, namespace)
    print(f"\n命名空间 '{namespace}' 中的记忆数量: {len(memories)}")
    
    if memories:
        print("\n最新记忆内容:")
        print("-" * 50)
        latest_memory = memories[-1]
        if hasattr(latest_memory, "dict"):
            print(latest_memory.dict())
        else:
            print(latest_memory)

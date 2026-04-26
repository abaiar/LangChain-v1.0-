"""
第四章 4.5.4 集成状态建模 — 理赔流程状态定义

【章节学习重点】
- LangGraph 状态建模：使用 TypedDict 定义图的状态结构
- Annotated 自定义归约函数：使用 append_logs 实现日志的累加而非覆盖
- Optional 和 Literal 类型：精确描述可选字段和枚举值

【代码功能】
定义破损理赔流程的统一状态 ClaimState，包含从请求信息到最终方案的完整字段。
使用 Annotated[List[str], append_logs] 实现日志的累加语义。

【关键参数说明】
- request_id/user_id/order_id: 请求、用户、订单标识
- policy_result: 规则检查结果（eligible/ineligible）
- risk_level: 风险等级（low/medium/high）
- similar_cases_summary: 相似案例总结
- proposed_solution/final_solution: 推荐方案和最终方案
- need_approval: 是否需要人工审批
- approval_decision: 审批决定（approve/modify/reject）
- logs: Annotated[List[str], append_logs] 日志列表，使用自定义归约函数累加

【应用场景】
- 复杂业务流程的状态建模
- 多分支并行处理后状态合并
- 需要精确类型约束的业务状态定义
"""
from typing import Optional, List, Literal, TypedDict, Annotated

def append_logs(existing: List[str], new: List[str]) -> List[str]:
    return (existing or []) + (new or [])


class ClaimState(TypedDict, total=False):
    """破损理赔流程的统一 State 定义"""

    # 基本请求信息
    request_id: str
    user_id: str
    order_id: str
    order_amount: float
    order_category: str   # 商品品类，如 "electronics" / "fragile" / "virtual" 等
    damage_description: str

    # 风险评估用的 mock 统计数据
    total_claims_count: int
    recent_claims_count: int
    total_orders_count: int

    # 分支 A：规则检查结果
    policy_result: Optional[Literal["eligible", "ineligible"]]
    policy_reason: Optional[str]

    # 分支 B：风险评估结果
    risk_level: Optional[Literal["low", "medium", "high"]]
    risk_reason: Optional[str]

    # 分支 C：相似案例总结
    similar_cases_summary: Optional[str]

    # 推荐方案 & 审批
    proposed_solution: Optional[str]
    solution_reason: Optional[str]
    need_approval: Optional[bool]

    approval_decision: Optional[Literal["approve", "modify", "reject"]]
    approval_comment: Optional[str]

    # 最终方案 & 用户说明
    final_solution: Optional[str]
    user_notice: Optional[str]

    # 日志（用于 streaming updates）
    logs: Annotated[List[str], append_logs]
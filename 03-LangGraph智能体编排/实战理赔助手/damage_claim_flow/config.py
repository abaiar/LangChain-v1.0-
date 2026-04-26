"""
第四章 4.5.3 集成配置文件与理赔参考数据 — 项目配置模块

【章节学习重点】
- 项目配置的集中管理：使用 dataclass 统一管理业务参数
- 业务阈值的配置化：将关键业务规则参数提取为可配置项

【代码功能】
集中管理理赔助手项目的配置参数，包括 DeepSeek API 配置和理赔业务阈值。

【关键参数说明】
- DEEPSEEK_API_KEY/BASE_URL/MODEL: DeepSeek 模型 API 配置
- approval_amount_threshold: 理赔金额阈值，超过此金额建议人工审核
- high_risk_level: 高风险等级标识，high 风险必须人工审核
- enable_streaming: 是否启用流式输出

【应用场景】
- 项目配置的统一管理和环境切换
- 业务规则的参数化配置
"""
from dataclasses import dataclass

# ===== DeepSeek 配置 =====
DEEPSEEK_API_KEY = "xxxxxx"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"


@dataclass
class Settings:
    # 理赔业务阈值
    approval_amount_threshold: float = 300.0  # 超过这个金额建议人工审核
    high_risk_level: str = "high"            # high 风险一定要人工审核

    # Streaming 相关（Graph 自身 streaming）
    enable_streaming: bool = True

settings = Settings()

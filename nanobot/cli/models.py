"""初始配置向导的模型信息助手。

模型数据库/自动完成功能暂时禁用（正在替换 litellm）。所有公共函数签名
保持不变，以便调用者无需更改即可继续工作。
"""

from __future__ import annotations

from typing import Any


def get_all_models() -> list[str]:
    return []


def find_model_info(model_name: str) -> dict[str, Any] | None:
    return None


def get_model_context_limit(model: str, provider: str = "auto") -> int | None:
    return None


def get_model_suggestions(partial: str, provider: str = "auto", limit: int = 20) -> list[str]:
    return []


def format_token_count(tokens: int) -> str:
    """Format token count for display (e.g., 200000 -> '200,000')."""
    return f"{tokens:,}"

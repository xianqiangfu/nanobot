"""Runtime context for tool construction.

设计思路：
- RequestContext：每次请求的上下文信息（channel、chat_id等）
- ContextAware协议：工具可以感知当前请求的上下文
- ToolContext：工具构造时需要的配置和依赖

为什么需要这个模块：
- 工具执行时需要知道来源channel和chat_id，用于消息发送
- 某些工具（如cron、spawn）需要根据上下文决定行为
- 将上下文与工具实现解耦，便于测试和复用
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol, runtime_checkable


@dataclass(frozen=True)
class RequestContext:
    """Per-request context injected into tools at message-processing time."""
    channel: str
    chat_id: str
    message_id: str | None = None
    session_key: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class ContextAware(Protocol):
    def set_context(self, ctx: RequestContext) -> None:
        ...


@dataclass
class ToolContext:
    config: Any
    workspace: str
    bus: Any | None = None
    subagent_manager: Any | None = None
    cron_service: Any | None = None
    file_state_store: Any = field(default=None)
    provider_snapshot_loader: Callable[[], Any] | None = None
    image_generation_provider_configs: dict[str, Any] | None = None
    timezone: str = "UTC"

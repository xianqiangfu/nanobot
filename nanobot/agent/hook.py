"""Shared lifecycle hook primitives for agent runs.

共享生命周期钩子原语，用于 agent 运行。

钩子允许在 agent 运行的各个生命周期事件中插入自定义逻辑：
- before_iteration: 迭代开始前
- on_stream: 流式输出时
- on_stream_end: 流式输出结束
- before_execute_tools: 工具执行前
- emit_reasoning: 发送推理内容
- emit_reasoning_end: 推理内容结束
- after_iteration: 迭代结束后
- finalize_content: 最终化内容
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from loguru import logger

from nanobot.providers.base import LLMResponse, ToolCallRequest


@dataclass(slots=True)
class AgentHookContext:
    """每次迭代的可变状态，暴露给 runner 钩子。

    包含当前迭代的所有状态信息，允许钩子读取和修改。
    """

    iteration: int                              # 当前迭代次数
    messages: list[dict[str, Any]]             # 消息历史
    response: LLMResponse | None = None         # LLM 响应
    usage: dict[str, int] = field(default_factory=dict)  # token 使用统计
    tool_calls: list[ToolCallRequest] = field(default_factory=list)  # 工具调用请求
    tool_results: list[Any] = field(default_factory=list)  # 工具执行结果
    tool_events: list[dict[str, str]] = field(default_factory=list)  # 工具事件
    streamed_content: bool = False              # 是否已流式输出内容
    streamed_reasoning: bool = False            # 是否已流式输出推理
    final_content: str | None = None           # 最终内容
    stop_reason: str | None = None             # 停止原因
    error: str | None = None                   # 错误信息


class AgentHook:
    """最小生命周期接口，用于共享 runner 自定义。

    默认实现为空，子类可以覆盖需要的方法。
    """

    def __init__(self, reraise: bool = False) -> None:
        self._reraise = reraise

    def wants_streaming(self) -> bool:
        return False

    async def before_iteration(self, context: AgentHookContext) -> None:
        pass

    async def on_stream(self, context: AgentHookContext, delta: str) -> None:
        pass

    async def on_stream_end(self, context: AgentHookContext, *, resuming: bool) -> None:
        pass

    async def before_execute_tools(self, context: AgentHookContext) -> None:
        pass

    async def emit_reasoning(self, reasoning_content: str | None) -> None:
        pass

    async def emit_reasoning_end(self) -> None:
        """Mark the end of an in-flight reasoning stream.

        Hooks that buffer ``emit_reasoning`` chunks (for in-place UI updates)
        flush and freeze the rendered group here. One-shot hooks ignore.
        """
        pass

    async def after_iteration(self, context: AgentHookContext) -> None:
        pass

    def finalize_content(self, context: AgentHookContext, content: str | None) -> str | None:
        return content


class CompositeHook(AgentHook):
    """扇出钩子，将调用委托给有序的钩子列表。

    错误隔离：
    - 异步方法会捕获并记录每个钩子的异常
    - 确保一个有故障的自定义钩子不会导致 agent 循环崩溃
    - finalize_content 是管道模式（无隔离，bug 应该暴露）
    """

    __slots__ = ("_hooks",)

    def __init__(self, hooks: list[AgentHook]) -> None:
        super().__init__()
        self._hooks = list(hooks)

    def wants_streaming(self) -> bool:
        return any(h.wants_streaming() for h in self._hooks)

    async def _for_each_hook_safe(self, method_name: str, *args: Any, **kwargs: Any) -> None:
        for h in self._hooks:
            if getattr(h, "_reraise", False):
                await getattr(h, method_name)(*args, **kwargs)
                continue

            try:
                await getattr(h, method_name)(*args, **kwargs)
            except Exception:
                logger.exception("AgentHook.{} error in {}", method_name, type(h).__name__)

    async def before_iteration(self, context: AgentHookContext) -> None:
        await self._for_each_hook_safe("before_iteration", context)

    async def on_stream(self, context: AgentHookContext, delta: str) -> None:
        await self._for_each_hook_safe("on_stream", context, delta)

    async def on_stream_end(self, context: AgentHookContext, *, resuming: bool) -> None:
        await self._for_each_hook_safe("on_stream_end", context, resuming=resuming)

    async def before_execute_tools(self, context: AgentHookContext) -> None:
        await self._for_each_hook_safe("before_execute_tools", context)

    async def emit_reasoning(self, reasoning_content: str | None) -> None:
        await self._for_each_hook_safe("emit_reasoning", reasoning_content)

    async def emit_reasoning_end(self) -> None:
        await self._for_each_hook_safe("emit_reasoning_end")

    async def after_iteration(self, context: AgentHookContext) -> None:
        await self._for_each_hook_safe("after_iteration", context)

    def finalize_content(self, context: AgentHookContext, content: str | None) -> str | None:
        for h in self._hooks:
            content = h.finalize_content(context, content)
        return content


class SDKCaptureHook(AgentHook):
    """记录工具名称和最终消息列表用于 ``RunResult``。

    注意：
    - runner 会就地修改 ``context.messages``
    - 每次调用 ``after_iteration`` 时会刷新快照
    - 最后一次调用反映了 SDK 调用者关心的轮次结束状态
    """

    def __init__(self) -> None:
        super().__init__()
        self.tools_used: list[str] = []
        self.messages: list[dict[str, Any]] = []

    async def after_iteration(self, context: AgentHookContext) -> None:
        for call in context.tool_calls:
            self.tools_used.append(call.name)
        self.messages = list(context.messages)

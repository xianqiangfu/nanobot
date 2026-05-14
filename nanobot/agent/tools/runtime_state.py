"""RuntimeState protocol: agent loop state exposed to MyTool.

设计思路：
- 使用Protocol定义最小接口契约
- MyTool通过动态getattr/setattr访问任意属性
- 运行时验证属性路径，而非编译时

为什么需要这个模块：
- MyTool需要检查和修改AgentLoop的运行时配置
- Protocol解耦具体实现，便于测试和替换
- 动态属性访问支持灵活的配置路径（如web_config.enable）
"""

from typing import Any, Protocol


class RuntimeState(Protocol):
    """Minimum contract that MyTool requires from its runtime state provider.

    In practice, this is always satisfied by ``AgentLoop``.  MyTool also
    accesses arbitrary attributes dynamically (via ``getattr`` / ``setattr``)
    for dot-path inspection and modification; those paths are validated at
    runtime rather than by this protocol.
    """

    @property
    def model(self) -> str: ...

    @property
    def max_iterations(self) -> int: ...

    @property
    def current_iteration(self) -> int: ...

    @property
    def tool_names(self) -> list[str]: ...

    @property
    def workspace(self) -> str: ...

    @property
    def provider_retry_mode(self) -> str: ...

    @property
    def max_tool_result_chars(self) -> int: ...

    @property
    def context_window_tokens(self) -> int: ...

    @property
    def web_config(self) -> Any: ...

    @property
    def exec_config(self) -> Any: ...

    @property
    def subagents(self) -> Any: ...

    @property
    def _runtime_vars(self) -> dict[str, Any]: ...

    @property
    def _last_usage(self) -> Any: ...

    def _sync_subagent_runtime_limits(self) -> None: ...

    @property
    def model_preset(self) -> str | None: ...

    _active_preset: str | None

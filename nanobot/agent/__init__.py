"""Agent core module.

Agent 核心模块。

主要组件：
- AgentLoop: 核心处理引擎，管理消息路由和会话
- ContextBuilder: 构建系统提示词和消息上下文
- AgentRunner: 执行 LLM 对话循环和工具调用
- AgentHook/CompositeHook: 生命周期钩子系统
- MemoryStore: 纯文件 I/O 记忆存储
- Consolidator: 基于 token 预算的整合器
- Dream: 两阶段记忆处理器
- AutoCompact: 空闲会话自动压缩
- SkillsLoader: 技能加载器
- SubagentManager: 后台任务管理器
"""

from nanobot.agent.context import ContextBuilder
from nanobot.agent.hook import AgentHook, AgentHookContext, CompositeHook
from nanobot.agent.loop import AgentLoop
from nanobot.agent.memory import Dream, MemoryStore
from nanobot.agent.skills import SkillsLoader
from nanobot.agent.subagent import SubagentManager

__all__ = [
    "AgentHook",
    "AgentHookContext",
    "AgentLoop",
    "CompositeHook",
    "ContextBuilder",
    "Dream",
    "MemoryStore",
    "SkillsLoader",
    "SubagentManager",
]

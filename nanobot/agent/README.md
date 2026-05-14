# Agent 循环与运行器

本模块包含 nanobot 的核心处理引擎，负责管理智能体生命周期和执行 LLM 对话。

## 主要组件

### AgentLoop (`loop.py`)

智能体循环是核心处理引擎，负责：

- **会话键管理** - 为每个聊天会话维护唯一标识
- **钩子系统** - 支持在关键点插入自定义逻辑
- **上下文构建** - 收集系统提示词、历史消息、工具定义等
- **消息分发** - 协调入站消息和出站响应

### AgentRunner (`runner.py`)

执行实际的 LLM 对话循环：

- 发送消息到 LLM 提供商
- 接收并解析工具调用请求
- 执行工具并将结果反馈给模型
- 流式传输响应内容
- 处理错误和重试逻辑

### 其他组件

- **ContextBuilder** (`context.py`) - 构建对话上下文，包括系统提示词、历史消息、工具定义
- **AgentHook** (`hook.py`) - 钩子接口，支持在关键点执行自定义逻辑
- **Dream** (`memory.py`) - Dream 两阶段记忆整合系统
- **SubagentManager** (`subagent.py`) - 子智能体管理，支持派生辅助任务
- **AutoCompact** (`autocompact.py`) - 自动上下文压缩管理
- **SkillsLoader** (`skills.py`) - 技能加载器
- **ModelPresets** (`model_presets.py`) - 模型预设配置

## 使用示例

```python
from nanobot.agent import AgentLoop, AgentRunner
from nanobot.providers import LLMProvider
from nanobot.session import SessionManager

# 初始化组件
session_manager = SessionManager()
provider = LLMProvider(...)
agent_runner = AgentRunner(provider=provider)

# 创建并启动 AgentLoop
loop = AgentLoop(
    runner=agent_runner,
    session_manager=session_manager,
)
await loop.start()
```

## 关键特性

- **异步设计** - 全异步架构，支持高并发
- **流式响应** - 支持实时流式输出
- **工具执行** - 内置工具调用和结果反馈
- **记忆管理** - 自动会话历史管理和压缩
- **错误恢复** - 内置重试和错误处理机制
- **可扩展** - 通过钩子系统支持自定义扩展
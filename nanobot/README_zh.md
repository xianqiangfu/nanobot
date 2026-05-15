# nanobot 核心包

nanobot 是一个轻量级的开源 AI 智能体框架，使用 Python 编写，配有 React/TypeScript WebUI。

## 核心架构

nanobot 围绕一个小型智能体循环构建，该循环从聊天频道接收消息，调用 LLM 提供商，执行工具，并管理会话记忆。

## 主要组件

- **Agent Loop** (`agent/`) - 核心处理引擎，管理会话、钩子和上下文构建
- **Agent Runner** (`agent/runner.py`) - 执行多轮 LLM 对话，处理工具调用和响应流式传输
- **LLM Providers** (`providers/`) - 多种 LLM 提供商实现（Anthropic、OpenAI、Azure、GitHub Copilot 等）
- **Channels** (`channels/`) - 平台集成（Telegram、Discord、Slack、飞书、Matrix、WhatsApp、QQ、微信等）
- **Tools** (`agent/tools/`) - 暴露给 LLM 的工具能力（文件系统、Shell 执行、Web 搜索/获取、MCP 服务器等）
- **Memory** (`agent/memory.py`) - 会话历史持久化，支持 Dream 两阶段记忆整合
- **Session Management** (`session/manager.py`) - 每会话历史记录、上下文压缩和基于 TTL 的自动压缩
- **Config** (`config/`) - 基于 Pydantic 的配置系统，支持从 `~/.nanobot/config.json` 加载
- **Message Bus** (`bus/queue.py`) - 解耦聊天频道和智能体核心的异步消息队列

## 数据流

消息通过异步 `MessageBus` 流动，该总线将聊天频道与智能体核心解耦：

1. **Channels** 从外部平台接收消息并发布 `InboundMessage` 事件到总线
2. **AgentLoop** 消费入站消息，构建上下文，并协调轮次
3. **AgentRunner** 处理实际的 LLM 对话循环：发送消息到提供商、接收工具调用、执行工具和流式传输响应
4. 响应作为 `OutboundMessage` 事件发布回相应的频道

## 入口点

- **CLI**: `nanobot/cli/commands.py`
- **Python SDK**: `nanobot/nanobot.py`

## 版本

当前版本: `0.1.5.post3`
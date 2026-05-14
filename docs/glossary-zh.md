# 术语表

本文档解释 nanobot 项目中使用的专业术语和概念。

## 核心概念

### Agent

AI 代理，是 nanobot 的核心组件。Agent 负责处理用户消息、调用 LLM（大语言模型）、执行工具并管理会话记忆。

**相关文件**：`nanobot/agent/loop.py`, `nanobot/agent/runner.py`

### AgentLoop

Agent 的主循环，管理会话状态和执行流程。它通过状态机（RESTORE → COMPACT → COMMAND → BUILD → RUN → SAVE → RESPOND → DONE）控制每一轮对话的处理流程。

**相关文件**：`nanobot/agent/loop.py`

### AgentRunner

执行实际的 LLM 对话循环。负责发送消息到提供商、接收工具调用、执行工具并流式传输响应。

**相关文件**：`nanobot/agent/runner.py`

## 消息系统

### MessageBus

异步消息总线，使用 asyncio.Queue 实现渠道和 Agent 之间的解耦。包含两个队列：inbound_queue（入站消息）和 outbound_queue（出站消息）。

**相关文件**：`nanobot/bus/queue.py`

### InboundMessage

入站消息事件，表示从外部平台接收到的消息。包含渠道、发送者、聊天ID、内容、媒体文件等信息。

**相关文件**：`nanobot/bus/events.py`

### OutboundMessage

出站消息事件，表示要发送到外部平台的消息。包含目标渠道、聊天ID、内容等信息。

**相关文件**：`nanobot/bus/events.py`

### Channel

渠道适配器，负责连接 nanobot 和外部聊天平台（如 Telegram、Discord、WeChat 等）。实现 `publish_inbound()`（发布入站消息）和 `consume_outbound()`（消费出站消息）方法。

**相关文件**：`nanobot/channels/base.py`

## LLM 集成

### Provider

LLM 提供商实现，负责与不同的 LLM 服务通信。继承自 `LLMProvider` 基类，实现统一的聊天接口。

**支持提供商**：Anthropic、OpenAI、Azure、GitHub Copilot、DeepSeek、Groq 等

**相关文件**：`nanobot/providers/base.py`

### ContextBuilder

上下文构建器，负责组装发送给 LLM 的提示词。包括会话历史、技能、提示词模板等。

**相关文件**：`nanobot/agent/context.py`

### Session

会话，表示与特定用户或聊天的对话历史。包含消息列表、元数据和管理信息。

**相关文件**：`nanobot/session/manager.py`

## 工具系统

### Tool

工具，是 Agent 可以调用的功能接口。工具让 LLM 能够执行实际操作，如文件操作、Shell 命令、Web 搜索等。

**相关文件**：`nanobot/agent/tools/`

### ToolRegistry

工具注册表，管理所有可用工具。负责工具的发现、注册和执行。

**相关文件**：`nanobot/agent/tools/registry.py`

### ToolCall

工具调用，表示 LLM 请求执行某个工具的指令。包含工具名称和参数。

### ToolResult

工具执行结果，表示工具执行后的返回值。用于反馈给 LLM。

### MCP (Model Context Protocol)

模型上下文协议，一种标准化的工具协议。MCP 服务器可以提供可插拔的工具给 Agent 使用。

**相关文档**：[`configuration-zh.md#mcp-服务器`](./configuration-zh.md#mcp-服务器)

## 记忆管理

### Memory

记忆系统，负责存储和管理 Agent 的会话历史。使用 Dream 两阶段记忆整合策略。

**相关文件**：`nanobot/agent/memory.py`

### Dream

两阶段记忆整合策略，包括：
1. **短期记忆**：当前的会话历史
2. **长期记忆**：通过整合和压缩生成的摘要

### Compaction

压缩，减少上下文大小以适应 token 限制的过程。可以删除旧消息、整合重复内容或生成摘要。

## 配置和会话

### Session Key

会话密钥，唯一标识一个会话的字符串。通常由渠道和聊天ID组成，格式为 `{channel}:{chat_id}`。

### Config

配置文件，存储在 `~/.nanobot/config.json`。包含提供商、渠道、工具、Agent 等配置。

**相关文件**：`nanobot/config/schema.py`

### Hook

钩子，允许在 Agent 执行周期的特定点注入自定义行为。用于进度追踪、流式传输、日志记录等。

**相关文件**：`nanobot/agent/hooks/`

## WebUI 相关

### Gateway

网关，nanobot 的 HTTP/WS 服务器，处理 WebUI 的请求。提供 REST API 和 WebSocket 端点。

### WebSocket Channel

WebSocket 通道，通过 WebSocket 协议与 WebUI 通信的渠道适配器。

**相关文档**：[`websocket.md`](./websocket.md)

## 开发相关

### Skill

技能，包含提示词和工具配置的 Markdown 文件。用于扩展 Agent 的能力和行为。

### Prompt Caching

提示词缓存， Anthropic 的优化功能，用于缓存提示词内容以减少 API 调用成本。

### SSRF (Server-Side Request Forgery)

服务器端请求伪造，一种安全漏洞。nanobot 实现了 SSRF 防护机制来限制内部网络访问。

**相关文件**：`nanobot/security/network.py`

## 其他术语

### Identity

身份，定义 Agent 的角色、行为和知识。通过 `identity.md` 文件配置。

### TTL (Time To Live)

生存时间，会话的自动清理时间。超过 TTL 未活动的会话会被自动清理。

### Turn

一轮对话，从接收到用户消息到返回响应的完整过程。

### State Machine

状态机，用于控制 Agent 执行流程的有限状态自动机。通过 `TurnState` 枚举定义状态转换。

## 缩写对照表

| 缩写 | 全称 | 说明 |
|------|------|------|
| LLM | Large Language Model | 大语言模型 |
| MCP | Model Context Protocol | 模型上下文协议 |
| API | Application Programming Interface | 应用程序编程接口 |
| CLI | Command Line Interface | 命令行界面 |
| TTL | Time To Live | 生存时间 |
| SSRF | Server-Side Request Forgery | 服务器端请求伪造 |
| SDK | Software Development Kit | 软件开发工具包 |
| WebUI | Web User Interface | Web 用户界面 |
| WS | WebSocket | WebSocket 协议 |
| REST | Representational State Transfer | 表述性状态传递 |
| JSON | JavaScript Object Notation | JavaScript 对象表示法 |
| PyPI | Python Package Index | Python 包索引 |

## 参考文档

- [快速开始](./quick-start-zh.md)
- [项目架构](./architecture-zh.md)
- [配置说明](./configuration-zh.md)
- [数据流程](./dataflow-zh.md)
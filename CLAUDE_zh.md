# CLAUDE.md

此文件为 Claude Code (claude.ai/code) 在本仓库中工作时提供指导。

## 项目概述

nanobot 是一个轻量级的开源 AI 代理框架，使用 Python 编写，并配有 React/TypeScript WebUI。它以一个小的代理循环为核心，该循环接收来自聊天频道的消息，调用 LLM 提供商，执行工具，并管理会话内存。

## 开发命令

```bash
# Python: 运行单个测试 / 代码检查
pytest tests/test_openai_api.py::test_function -v
ruff check nanobot/

# WebUI: 开发服务器（将 API/WS 代理到网关 :8765），构建，测试
# 构建输出到 ../nanobot/web/dist（打包到 Python wheel 中）
cd webui && bun run dev      # 或 NANOBOT_API_URL=... bun run dev
cd webui && bun run build
cd webui && bun run test

# 网关
nanobot gateway
```

## 高层架构

### 核心数据流

消息通过异步 `MessageBus` (`nanobot/bus/queue.py`) 流动，该总线将聊天频道与代理核心解耦：

1. **频道** (`nanobot/channels/`) 从外部平台接收消息并将 `InboundMessage` 事件发布到总线。
2. **`AgentLoop`** (`nanobot/agent/loop.py`) 消费入站消息，构建上下文，并协调轮次。
3. **`AgentRunner`** (`nanobot/agent/runner.py`) 处理实际的 LLM 对话循环：向提供商发送消息，接收工具调用，执行工具，并流式传输响应。
4. 响应作为 `OutboundMessage` 事件发布回相应的频道。

### 关键子系统

- **代理循环** (`nanobot/agent/loop.py`, `runner.py`)：核心处理引擎。`AgentLoop` 管理会话密钥、钩子和上下文构建。`AgentRunner` 执行带有工具执行的多轮 LLM 对话。
- **LLM 提供商** (`nanobot/providers/`)：基于公共基础 (`base.py`) 构建的提供商实现（Anthropic、OpenAI 兼容、Azure、GitHub Copilot 等）。`factory.py` 和 `registry.py` 处理实例化和模型发现。
- **频道** (`nanobot/channels/`)：平台集成（Telegram、Discord、Slack、飞书、Matrix、WhatsApp、QQ、微信、WebSocket 等）。`manager.py` 发现并协调它们。频道通过 `pkgutil` 扫描 + 入口点插件自动发现。
- **工具** (`nanobot/agent/tools/`)：暴露给 LLM 的代理能力：文件系统（读/写/编辑/列表）、Shell 执行、Web 搜索/获取、MCP 服务器、定时任务、笔记本编辑、子代理生成，以及用于自我修改的 `MyTool`。
- **内存** (`nanobot/agent/memory.py`)：会话历史持久化，采用 Dream 两阶段内存整合。使用原子写入和 fsync 确保持久性。
- **会话管理** (`nanobot/session/manager.py`)：每会话历史、上下文压缩和基于 TTL 的自动压缩。
- **配置** (`nanobot/config/schema.py`, `loader.py`)：基于 Pydantic 的配置，从 `~/.nanobot/config.json` 加载。支持 camelCase 别名以实现 JSON 兼容性。
- **桥接** (`bridge/`)：通过 `pyproject.toml` 的 `force-include` 打包到 wheel 中的 TypeScript 服务（例如 WhatsApp 桥接）。
- **WebUI** (`webui/`)：基于 Vite 的 React SPA，通过 WebSocket 多路复用协议与网关通信。开发服务器将 `/api`、`/webui`、`/auth` 和 WebSocket 流量代理到网关。

### 入口点

- **CLI**：`nanobot/cli/commands.py`
- **Python SDK**：`nanobot/nanobot.py`

## 项目特定说明

- 架构约束：[`.agent/design.md`](.agent/design.md)
- 安全边界：[`.agent/security.md`](.agent/security.md)
- 常见陷阱：[`.agent/gotchas.md`](.agent/gotchas.md)

## 分支策略

完整的双分支模型（`main` 与 `nightly`）和 PR 指南请参阅 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

## 代码风格

- Python 3.11+，全程使用 asyncio。
- 行长度：100。
- 代码检查：`ruff` 使用规则 E、F、I、N、W（忽略 E501）。
- pytest 配置 `asyncio_mode = "auto"`。

## 常用文件位置

- 配置模式：`nanobot/config/schema.py`
- 提供商基类 / 新提供商模板：`nanobot/providers/base.py`
- 频道基类 / 新频道模板：`nanobot/channels/base.py`
- 工具注册表：`nanobot/agent/tools/registry.py`
- WebUI 开发代理配置：`webui/vite.config.ts`
- 测试镜像 `nanobot/` 包结构。
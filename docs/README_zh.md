# nanobot 文档

欢迎来到 nanobot 文档！

> 最新文档请访问：[nanobot.wiki](https://nanobot.wiki/docs/latest/getting-started/nanobot-overview)
>
> 本目录中的文档跟踪当前仓库，可能比已发布的网站更新更快。

## 快速导航

| 文档 | 说明 |
|------|------|
| [快速开始](./quick-start-zh.md) | 安装、配置和首次运行 |
| [项目架构](./architecture-zh.md) | 项目架构总览和设计理念 |
| [配置说明](./configuration-zh.md) | 详细的配置选项和示例 |
| [数据流程](./dataflow-zh.md) | 消息流和处理流程详解 |
| [术语表](./glossary-zh.md) | 项目中使用的专业术语解释 |
| [常见问题](./faq-zh.md) | 安装、配置、使用和开发 FAQ |

## 核心文档

### 入门指南

| 文档 | 说明 |
|------|------|
| [`quick-start-zh.md`](./quick-start-zh.md) | 安装、入门和首次运行设置 |
| [`chat-apps.md`](./chat-apps.md) | 连接 nanobot 到 Telegram、Discord、WeChat、Feishu 等平台 |
| [`configuration-zh.md`](./configuration-zh.md) | 提供商、工具、通道、MCP 和运行时设置 |

### 高级功能

| 文档 | 说明 |
|------|------|
| [`agent-social-network.md`](./agent-social-network.md) | 从 nanobot 加入外部 agent 社区 |
| [`image-generation.md`](./image-generation.md) | 配置图片提供商、WebUI 图片模式和生成的工件 |
| [`multiple-instances.md`](./multiple-instances.md) | 使用独立配置和工作空间运行隔离的 bot |
| [`memory.md`](./memory.md) | nanobot 如何存储、整合和恢复记忆 |

### 参考手册

| 文档 | 说明 |
|------|------|
| [`cli-reference.md`](./cli-reference.md) | 核心 CLI 命令和常见入口点 |
| [`chat-commands.md`](./chat-commands.md) | 斜杠命令和周期性任务行为 |
| [`openai-api.md`](./openai-api.md) | 本地 API 端点、请求格式和文件上传 |

### 开发和扩展

| 文档 | 说明 |
|------|------|
| [`python-sdk.md`](./python-sdk.md) | 从 Python 编程使用 nanobot |
| [`channel-plugin-guide.md`](./channel-plugin-guide.md) | 构建和测试自定义聊天通道插件 |
| [`websocket.md`](./websocket.md) | 实时 WebSocket 访问和协议详情 |
| [`my-tool.md`](./my-tool.md) | 使用 `my` 工具检查和调整运行时状态 |

### 深入理解

| 文档 | 说明 |
|------|------|
| [`architecture-zh.md`](./architecture-zh.md) | 项目架构、设计理念和技术栈 |
| [`dataflow-zh.md`](./dataflow-zh.md) | 完整的消息流程和状态机 |
| [`glossary-zh.md`](./glossary-zh.md) | 术语表和缩写对照 |
| [`faq-zh.md`](./faq-zh.md) | 常见问题解答 |

## 文档结构

```
docs/
├── README.md              # 英文文档索引
├── README-zh.md           # 中文文档索引
├── quick-start.md         # 快速开始（英文）
├── quick-start-zh.md      # 快速开始（中文）
├── architecture-zh.md     # 项目架构（中文）
├── configuration-zh.md    # 配置说明（中文）
├── dataflow-zh.md         # 数据流程（中文）
├── glossary-zh.md         # 术语表（中文）
├── faq-zh.md              # 常见问题（中文）
├── chat-apps.md           # 聊天应用集成
├── agent-social-network.md # Agent 社交网络
├── configuration.md       # 配置指南（英文）
├── image-generation.md    # 图片生成
├── multiple-instances.md  # 多实例部署
├── cli-reference.md       # CLI 参考手册
├── chat-commands.md       # 聊天命令
├── openai-api.md          # OpenAI 兼容 API
├── deployment.md          # 部署指南
├── memory.md              # 记忆系统
├── python-sdk.md          # Python SDK
├── channel-plugin-guide.md # 通道插件开发
├── websocket.md           # WebSocket 通道
└── my-tool.md             # My Tool 指南
```

## 文档贡献

欢迎为文档做出贡献！请遵循以下指南：

1. 使用清晰的中文
2. 提供代码示例
3. 包含实际的配置示例
4. 保持文档与代码同步更新
5. 使用适当的格式（表格、列表、代码块等）

## 获取帮助

如果文档无法解决您的问题，请：

- 查看 [FAQ](./faq-zh.md)
- 访问 [nanobot.wiki](https://nanobot.wiki)
- 提交 [GitHub Issue](https://github.com/HKUDS/nanobot/issues)

## 在线文档

最新文档请访问：[nanobot.wiki](https://nanobot.wiki/docs/latest/getting-started/nanobot-overview)

本目录中的页面跟踪当前仓库，可能比已发布的网站更新更快。
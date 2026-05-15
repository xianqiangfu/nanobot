# nanobot 文档

欢迎来到 nanobot 文档！

> 最新文档请访问：[nanobot.wiki](https://nanobot.wiki/docs/latest/getting-started/nanobot-overview)
>
> 本目录中的文档跟踪当前仓库，可能比已发布的网站更新更快。

## 快速导航

| 文档 | 说明 |
|------|------|
| [快速开始](./quickstart-zh.md) | 安装、配置和首次运行 |
| [项目架构](./architecture-zh.md) | 项目架构总览和设计理念 |
| [技术栈](./tech-stack-zh.md) | 技术栈详解和选型说明 |
| [设计原则](./design-principles-zh.md) | 设计原则和架构约束 |
| [配置说明](./configuration-zh.md) | 详细的配置选项和示例 |
| [数据流程](./dataflow-zh.md) | 消息流和处理流程详解 |
| [术语表](./glossary-zh.md) | 项目中使用的专业术语解释 |
| [常见问题](./faq-zh.md) | 安装、配置、使用和开发 FAQ |
| [注意事项](./gotchas-zh.md) | 开发注意事项和常见陷阱 |
| [安全指南](./security-zh.md) | 安全边界和最佳实践 |

## 核心文档

### 入门指南

| 文档 | 说明 |
|------|------|
| [`quickstart-zh.md`](./quickstart-zh.md) | 快速入门指南：安装、配置和首次运行 |
| [`deployment-zh.md`](./deployment-zh.md) | 部署指南：Docker、Linux、macOS、Windows 部署 |
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
| [`development-zh.md`](./development-zh.md) | 开发指南：环境搭建、调试、测试和贡献流程 |
| [`extension-zh.md`](./extension-zh.md) | 扩展开发：提供商、通道、工具、技能和 MCP 服务器开发 |
| [`python-sdk.md`](./python-sdk.md) | 从 Python 编程使用 nanobot |
| [`channel-plugin-guide.md`](./channel-plugin-guide.md) | 构建和测试自定义聊天通道插件 |
| [`websocket.md`](./websocket.md) | 实时 WebSocket 访问和协议详情 |
| [`my-tool.md`](./my-tool.md) | 使用 `my` 工具检查和调整运行时状态 |

### 最佳实践

| 文档 | 说明 |
|------|------|
| [`best-practices-zh.md`](./best-practices-zh.md) | 最佳实践：异步编程、错误处理、日志记录和代码风格 |
| [`gotchas-zh.md`](./gotchas-zh.md) | 注意事项：开发陷阱、Windows 兼容性、配置语法 |
| [`security-zh.md`](./security-zh.md) | 安全指南：API 密钥、工作目录、SSRF 防护 |

## 文档结构

```
docs/
├── README.md              # 英文文档索引
├── README-zh.md           # 中文文档索引（本文档）
├── README_zh.md           # 中文文档索引（备用）
├── 快速开始
│   ├── quick-start.md     # 快速开始（英文）
│   └── quickstart-zh.md  # 快速开始（中文）
├── 部署
│   ├── deployment.md      # 部署指南（英文）
│   └── deployment-zh.md   # 部署指南（中文）
├── 架构与设计
│   ├── architecture-zh.md # 项目架构（中文）
│   ├── tech-stack-zh.md  # 技术栈（中文）
│   └── design-principles-zh.md  # 设计原则（中文）
├── 配置与参考
│   ├── configuration.md  # 配置指南（英文）
│   ├── configuration-zh.md # 配置说明（中文）
│   ├── cli-reference.md  # CLI 参考手册（英文）
│   ├── cli-reference-zh.md  # CLI 参考手册（中文）
│   ├── chat-commands.md  # 聊天命令
│   └── openai-api.md    # OpenAI 兼容 API
├── 集成与使用
│   ├── chat-apps.md     # 聊天应用集成
│   ├── agent-social-network.md  # Agent 社交网络
│   ├── multiple-instances.md  # 多实例部署
│   └── image-generation.md  # 图片生成
├── 开发与扩展
│   ├── development-zh.md  # 开发指南（中文）
│   ├── extension-zh.md   # 扩展开发（中文）
│   ├── python-sdk.md    # Python SDK
│   ├── channel-plugin-guide.md  # 通道插件开发
│   └── websocket.md     # WebSocket 通道
├── 深入理解
│   ├── memory.md        # 记忆系统
│   ├── my-tool.md      # My Tool 指南
│   ├── glossary-zh.md  # 术语表（中文）
│   └── faq-zh.md       # 常见问题（中文）
├── 最佳实践与安全
│   ├── best-practices-zh.md  # 最佳实践（中文）
│   ├── gotchas-zh.md   # 注意事项（中文）
│   └── security-zh.md  # 安全指南（中文）
└── diagrams/           # 图表目录
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
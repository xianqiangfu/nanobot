# nanobot 🐈

[![PyPI](https://img.shields.io/pypi/v/nanobot-ai)](https://pypi.org/project/nanobot-ai/)
[![Python](https://img.shields.io/badge/python-%E2%89%A5-3.11-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docs](https://img.shields.io/badge/Docs-nanobot.wiki-blue?style=flat&logo=readthedocs&logoColor=white)](https://nanobot.wiki/docs/latest/getting-started/nanobot-overview)

> **nanobot** 是一个开源的超轻量级 AI 代理框架，灵感来自 [OpenClaw](https://github.com/openclaw/openclaw)、[Claude Code](https://www.anthropic.com/claude-code) 和 [Codex](https://www.openai.com/codex)。它保持核心代理循环小巧易读，同时支持聊天通道、记忆、MCP 和实用的部署路径，让您可以从本地设置轻松过渡到长期运行的个人代理。

## 📢 最新动态

- **2026-05-15** 📚 完整的中文文档体系：快速入门、部署指南、开发指南、最佳实践和技术调研报告
- **2026-04-29** 🚀 发布 **v0.1.5.post3** — Feishu、Discord、Slack 和 Teams 的更智能线程；**DeepSeek-V4**；Hugging Face 和 Olostep；选择、`/history` 和更稳定的长对话
- **2026-04-28** 🌐 Olostep 网络搜索、Hugging Face 提供商、更安全的工作空间工具中断
- **2026-04-27** 💬 `/history` 命令、更智能的会话重放上限、更流畅的 Discord/Slack 线程
- **2026-04-26** 🧭 自然 cron 提醒、线程感知重启、更安全的本地提供商和 shell 行为

## ✨ 特性

- **轻量级架构**：核心代理循环小巧易读，易于理解和修改
- **多平台支持**：支持 Telegram、Discord、Slack、Feishu、Matrix、WhatsApp、QQ、WeChat 等平台
- **多提供商支持**：统一支持 Anthropic、OpenAI、Azure OpenAI、Bedrock、GitHub Copilot 等提供商
- **工具系统**：内置文件操作、命令执行、Web 搜索等工具
- **技能系统**：通过 Markdown 文件定义技能，支持动态加载
- **MCP 协议**：支持 Model Context Protocol，动态加载 MCP 服务器工具
- **WebUI**：现代化的 Web 界面，支持实时聊天和图像生成
- **CLI 模式**：强大的命令行界面，支持交互式聊天和批量处理

## 📚 文档

完整的中文文档请查看 [docs/](./docs/) 目录：

- [快速入门](./docs/quickstart-zh.md) - 安装、配置和首次运行
- [部署指南](./docs/deployment-zh.md) - Docker、Linux、macOS、Windows 部署
- [项目架构](./docs/architecture-zh.md) - 项目架构总览和设计理念
- [技术栈](./docs/tech-stack-zh.md) - 技术栈详解和选型说明
- [开发指南](./docs/development-zh.md) - 开发环境、调试、测试和贡献
- [扩展开发](./docs/extension-zh.md) - 提供商、通道、工具、技能开发
- [最佳实践](./docs/best-practices-zh.md) - 异步编程、错误处理、日志记录
- [注意事项](./docs/gotchas-zh.md) - 开发陷阱、Windows 兼容性、配置语法
- [安全指南](./docs/security-zh.md) - API 密钥、SSRF 防护、安全边界
- [技术调研报告](./技术调研报告.md) - 完整的技术调研报告

更多文档请参考 [docs/README-zh.md](./docs/README-zh.md)。

## 🚀 快速开始

```bash
# 安装
pip install nanobot-ai

# 初始化配置
nanobot onboard

# 启动交互式聊天
nanobot agent
```

详细的安装和配置说明请参考[快速入门指南](./docs/quickstart-zh.md)。

## 🧩 扩展性

nanobot 支持多种扩展方式：

- **聊天通道**：通过插件系统添加新的聊天平台支持
- **LLM 提供商**：继承 `LLMProvider` 基类实现新的提供商
- **工具**：使用 `@tool_parameters` 装饰器添加自定义工具
- **技能**：通过 Markdown 文件定义技能
- **MCP 服务器**：动态加载 MCP 服务器并暴露工具

详细的扩展开发指南请参考[扩展开发文档](./docs/extension-zh.md)。

## 🤝 贡献

欢迎贡献代码、报告问题或提出改进建议！请参考 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解贡献流程。

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

## 🌐 社区

- **GitHub**: https://github.com/HKUDS/nanobot
- **文档**: https://nanobot.wiki
- **问题跟踪**: https://github.com/HKUDS/nanobot/issues
- **Discord**: https://discord.gg/MnCvHqpUGB
- **Feishu**: [加入群组](./COMMUNICATION.md)
- **WeChat**: [加入群组](./COMMUNICATION.md)

---

*nanobot - 轻量级 AI 代理框架*

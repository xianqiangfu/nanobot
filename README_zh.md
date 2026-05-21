![cover-v5-optimized](./images/GitHub_README.png)

<div align="center">
  <p>
    <a href="https://pypi.org/project/nanobot-ai/"><img src="https://img.shields.io/pypi/v/nanobot-ai" alt="PyPI"></a>
    <a href="https://pepy.tech/project/nanobot-ai"><img src="https://static.pepy.tech/badge/nanobot-ai" alt="下载量"></a>
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="许可证">
    <a href="https://github.com/HKUDS/nanobot/graphs/commit-activity" target="_blank">
        <img alt="上月提交次数" src="https://img.shields.io/github/commit-activity/m/HKUDS/nanobot?labelColor=%20%2332b583&color=%20%2312b76a"></img></a>
    <a href="https://github.com/HKUDS/nanobot/issues?q=is%3Aissue%20is%3Aclosed" target="_blank">
        <img alt="已关闭问题" src="https://img.shields.io/github/issues-search?query=repo%3AHKUDS%2Fnanobot%20is%3Aissue%20is%3Aclosed&label=已关闭问题&labelColor=%20%237d89b0&color=%20%235d6b98"></img></a>
    <a href="https://twitter.com/intent/follow?screen_name=nanobot_project" target="_blank">
        <img src="https://img.shields.io/twitter/follow/nanobot_project?logo=X&color=%20%23f5f5f5" alt="在X(Twitter)上关注"></img></a>
    <a href="https://nanobot.wiki/docs/latest/getting-started/nanobot-overview"><img src="https://img.shields.io/badge/文档-nanobot.wiki-blue?style=flat&logo=readthedocs&logoColor=white" alt="文档"></a>
    <a href="./COMMUNICATION.md"><img src="https://img.shields.io/badge/飞书-群组-E9DBFC?style=flat&logo=feishu&logoColor=white" alt="飞书"></a>
    <a href="./COMMUNICATION.md"><img src="https://img.shields.io/badge/微信-群组-C5EAB4?style=flat&logo=wechat&logoColor=white" alt="微信"></a>
    <a href="https://discord.gg/MnCvHqpUGB"><img src="https://img.shields.io/badge/Discord-社区-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord"></a>
  </p>
</div>

🐈 **nanobot** 是一个开源的超轻量级 AI 智能体，秉承着 [OpenClaw](https://github.com/openclaw/openclaw)、[Claude Code](https://www.anthropic.com/claude-code) 和 [Codex](https://www.openai.com/codex/) 的精神。它保持核心智能体循环的小巧和可读性，同时支持聊天渠道、内存、MCP 和实用的部署路径，让你可以以最小的开销从本地设置转向长期运行的个人智能体。

## 📢 新闻

- **2026-04-29** 🚀 发布 **v0.1.5.post3** — 飞书、Discord、Slack 和 Teams 上的智能线程；**DeepSeek-V4**；Hugging Face & Olostep；选项、`/history` 和更稳定的长对话。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.5.post3)。
- **2026-04-28** 🌐 Olostep 网络搜索、Hugging Face 提供商、更安全的工作区工具中断。
- **2026-04-27** 💬 `/history` 命令、更智能的会话回放上限、更流畅的 Discord / Slack 线程。
- **2026-04-26** 🧭 自然的 cron 提醒、线程感知重启、更安全的本地提供商和 shell 行为。
- **2026-04-25** 🧩 `ask_user` 选项、macOS LaunchAgent 部署、MSTeams 过时引用清理。
- **2026-04-24** 🎥 渠道的视频附件、DeepSeek 思考控制、更快的文档启动。
- **2026-04-23** 🧵 Discord 线程会话、Telegram 内联按钮、结构化工具进度更新。
- **2026-04-22** 🔎 GitHub Copilot GPT-5 / o 系列支持、可配置的网络获取、WebUI 图片上传。
- **2026-04-21** 🚀 发布 **v0.1.5.post2** — Windows 和 Python 3.14 支持、Office 文档读取、OpenAI 兼容 API 的 SSE 流式传输，以及更强的会话、内存和渠道可靠性。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.5.post2)。
- **2026-04-20** 🎨 Kimi K2.6 支持、Telegram 长消息分割、WebUI 排版和暗模式优化。
- **2026-04-19** 🌐 WebUI 国际化区域切换器、具有自动修复功能的原子会话写入。
- **2026-04-18** 🧪 初始 WebUI 聊天、更智能的设置向导菜单、WebSocket 多路聊天多路复用。
- **2026-04-17** 🪟 Windows 和 Python 3.14 CI、Dream 行龄内存、电子邮件自循环保护。
- **2026-04-16** 📡 OpenAI 兼容 API 的 SSE 流式传输、Discord 频道允许列表。
- **2026-04-15** 🎛️ LM Studio 和可空 API 密钥、MiniMax 思考端点、运行时 SelfTool。
- **2026-04-14** 🚀 发布 **v0.1.5.post1** — Dream 技能发现、回合中间的后续注入、WebSocket 渠道和更深入的渠道集成。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.5.post1)。
- **2026-04-13** 🛡️ 智能体回合增强 — 用户消息提前持久化、自动压缩跳过活动任务。
- **2026-04-12** 🔒 Lark 全局域支持、Dream 学习发现的技能、shell 沙箱收紧。
- **2026-04-11** ⚡ 上下文压缩即时缩小会话；Kagi 网络搜索；QQ 和企业微信的完整媒体支持。

<details>
<summary>早期新闻</summary>

- **2026-04-10** 📓 笔记本编辑工具、多个 MCP 服务器、飞书流式传输和完成表情符号。
- **2026-04-09** 🔌 WebSocket 渠道、统一的跨渠道会话、`disabled_skills` 配置。
- **2026-04-08** 📤 API 文件上传、OpenAI 推理自动路由和 Responses 后备。
- **2026-04-07** 🧠 Anthropic 自适应思考、MCP 资源和提示作为工具暴露。
- **2026-04-06** 🛰️ Langfuse 可观测性、统一的 Whisper 转录、电子邮件附件。
- **2026-04-05** 🚀 发布 **v0.1.5** — 更稳固的长期运行任务、Dream 两阶段内存、生产就绪的沙箱和编程智能体 SDK。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.5)。
- **2026-04-04** 🚀 Jinja2 响应模板、Dream 内存增强、更智能的重试处理。
- **2026-04-03** 🧠 小米 MiMo 提供商、可见的链式思考推理、Telegram UX 优化。
- **2026-04-02** 🧱 长期运行任务更可靠地运行 — 核心运行时增强。
- **2026-04-01** 🔑 GitHub Copilot 身份验证恢复；更严格的工作区路径；OpenRouter Claude 缓存修复。
- **2026-03-31** 🛰️ 微信多模态对齐、Discord/Matrix 优化、Python SDK 外观、MCP 和工具修复。
- **2026-03-30** 🧩 OpenAI 兼容 API 收紧；可组合的智能体生命周期挂钩。
- **2026-03-29** 💬 微信语音、输入、二维码/媒体弹性；固定会话的 OpenAI 兼容 API。
- **2026-03-28** 📚 提供商文档刷新；技能模板措辞修复。
- **2026-03-27** 🚀 发布 **v0.1.4.post6** — 架构解耦、移除 litellm、端到端流式传输、微信渠道和安全修复。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post6)。
- **2026-03-26** 🏗️ 智能体运行器提取和生命周期挂钩统一；边界处的流增量合并。
- **2026-03-25** 🌏 StepFun 提供商、可配置时区、Gemini 思考签名。
- **2026-03-24** 🔧 微信兼容性、飞书 CardKit 流式传输、测试套件重组。
- **2026-03-23** 🔧 命令路由为插件重构、WhatsApp/微信媒体、统一渠道登录 CLI。
- **2026-03-22** ⚡ 端到端流式传输、微信渠道、Anthropic 缓存优化、`/status` 命令。
- **2026-03-21** 🔒 用原生 `openai` + `anthropic` SDK 替换 `litellm`。详细信息请参见[提交](https://github.com/HKUDS/nanobot/commit/3dfdab7)。
- **2026-03-20** 🧙 交互式设置向导 — 选择你的提供商、模型自动完成，然后你就可以开始了。
- **2026-03-19** 💬 Telegram 在负载下更弹性；飞书现在正确渲染代码块。
- **2026-03-18** 📷 Telegram 现在可以通过 URL 发送媒体。Cron 计划显示人类可读的详细信息。
- **2026-03-17** ✨ 飞书格式化升级、Slack 完成时反应、自定义端点支持额外标头，以及更可靠的图像处理。
- **2026-03-16** 🚀 发布 **v0.1.4.post5** — 一个专注于优化的发布，具有更强的可靠性和渠道支持，以及更可靠的日常体验。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post5)。
- **2026-03-15** 🧩 钉钉富媒体、更智能的内置技能和更干净的模型兼容性。
- **2026-03-14** 💬 渠道插件、飞书回复，以及更稳定的 MCP、QQ 和媒体处理。
- **2026-03-13** 🌐 多提供商网络搜索、LangSmith，以及更广泛的可靠性改进。
- **2026-03-12** 🚀 火山引擎支持、Telegram 回复上下文、`/restart` 和更稳固的内存。
- **2026-03-11** 🔌 企业微信、Ollama、更干净的发现，以及更安全的工具行为。
- **2026-03-10** 🧠 基于令牌的内存、共享重试，以及更干净的网关和 Telegram 行为。
- **2026-03-09** 💬 Slack 线程优化和更好的飞书音频兼容性。
- **2026-03-08** 🚀 发布 **v0.1.4.post4** — 一个可靠性丰富的发布，具有更安全的默认值、更好的多实例支持、更稳固的 MCP，以及主要的渠道和提供商改进。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post4)。
- **2026-03-07** 🚀 Azure OpenAI 提供商、WhatsApp 媒体、QQ 群聊，以及更多 Telegram/飞书优化。
- **2026-03-06** 🪄 更轻量的提供商、更智能的媒体处理，以及更稳固的内存和 CLI 兼容性。
- **2026-03-05** ⚡️ Telegram 草稿流式传输、MCP SSE 支持，以及更广泛的渠道可靠性修复。
- **2026-03-04** 🛠️ 依赖清理、更安全的文件读取，以及另一轮测试和 Cron 修复。
- **2026-03-03** 🧠 更干净的用户消息合并、更安全的多模态保存，以及更强的 Cron 保护。
- **2026-03-02** 🛡️ 更安全的默认访问控制、更稳固的 Cron 重新加载，以及更干净的 Matrix 媒体处理。
- **2026-03-01** 🌐 Web 代理支持、更智能的 Cron 提醒，以及飞书富文本解析改进。
- **2026-02-28** 🚀 发布 **v0.1.4.post3** — 更干净的上下文、增强的会话历史和更智能的智能体。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post3)。
- **2026-02-27** 🧠 实验性思考模式支持、钉钉媒体消息、飞书和 QQ 渠道修复。
- **2026-02-26** 🛡️ 会话污染修复、WhatsApp 去重、Windows 路径保护、Mistral 兼容性。
- **2026-02-25** 🧹 新的 Matrix 渠道、更干净的会话上下文、自动工作区模板同步。
- **2026-02-24** 🚀 发布 **v0.1.4.post2** — 一个专注于可靠性的发布，具有重新设计的心跳、提示缓存优化和增强的提供商及渠道稳定性。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post2)。
- **2026-02-23** 🔧 虚拟工具调用心跳、提示缓存优化、Slack mrkdwn 修复。
- **2026-02-22** 🛡️ Slack 线程隔离、Discord 输入修复、智能体可靠性改进。
- **2026-02-21** 🎉 发布 **v0.1.4.post1** — 新的提供商、跨渠道媒体支持，以及主要的稳定性改进。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post1)。
- **2026-02-20** 🐦 飞书现在从用户那里接收多模态文件。底层更可靠的内存。
- **2026-02-19** ✨ Slack 现在发送文件、Discord 分割长消息，以及子智能体在 CLI 模式下工作。
- **2026-02-18** ⚡️ nanobot 现在支持火山引擎、MCP 自定义身份验证标头和 Anthropic 提示缓存。
- **2026-02-17** 🎉 发布 **v0.1.4** — MCP 支持、进度流式传输、新的提供商和多个渠道改进。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4)。
- **2026-02-16** 🦞 nanobot 现在集成了 [ClawHub](https://clawhub.ai) 技能 — 搜索和安装公共智能体技能。
- **2026-02-15** 🔑 nanobot 现在支持具有 OAuth 登录支持的 OpenAI Codex 提供商。
- **2026-02-14** 🔌 nanobot 现在支持 MCP！详细信息请参见 [MCP 部分](#mcp-model-context-protocol)。
- **2026-02-13** 🎉 发布 **v0.1.3.post7** — 包括安全增强和多项改进。**请升级到最新版本以解决安全问题**。详细信息请参见[发布说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post7)。
- **2026-02-12** 🧠 重新设计的内存系统 — 更少的代码，更可靠。加入关于它的[讨论](https://github.com/HKUDS/nanobot/discussions/566)！
- **2026-02-11** ✨ 增强的 CLI 体验和添加了 MiniMax 支持！
- **2026-02-10** 🎉 发布 **v0.1.3.post6** 并进行了改进！查看更新[说明](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post6)和我们的[路线图](https://github.com/HKUDS/nanobot/discussions/431)。
- **2026-02-09** 💬 添加了 Slack、电子邮件和 QQ 支持 — nanobot 现在支持多个聊天平台！
- **2026-02-08** 🔧 重构提供商 — 现在添加新的 LLM 提供商只需 2 个简单步骤！详细信息请查看[这里](#providers)。
- **2026-02-07** 🚀 发布 **v0.1.3.post5** 并提供 Qwen 支持和几项关键改进！详细信息请查看[这里](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post5)。
- **2026-02-06** ✨ 添加了 Moonshot/Kimi 提供商、Discord 集成和增强的安全增强！
- **2026-02-05** ✨ 添加了飞书渠道、DeepSeek 提供商和增强的计划任务支持！
- **2026-02-04** 🚀 发布 **v0.1.3.post4** 并提供多提供商和 Docker 支持！详细信息请查看[这里](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post4)。
- **2026-02-03** ⚡ 集成 vLLM 以支持本地 LLM 并改进自然语言任务调度！
- **2026-02-02** 🎉 nanobot 正式发布！欢迎尝试 🐈 nanobot！

</details>


## 💡 nanobot 的关键特性

- **超轻量级**：稳定长期运行的智能体行为，具有小巧、可读的核心。
- **研究就绪**：代码库有意设计得足够简单，便于研究、修改和扩展。
- **实用**：聊天渠道、API、内存、MCP 和部署路径已内置。
- **可黑客化**：你可以快速开始，然后通过仓库文档深入了解，而不是通过单一的大型落地页面。

## 📦 安装

> [!IMPORTANT]
> 如果你想要最新的功能和实验性功能，请从源代码安装。
> 
> 如果你想要最稳定的日常体验，请从 PyPI 或使用 `uv` 安装。

**从源代码安装**

```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
pip install -e .
```

**使用 `uv` 安装**

```bash
uv tool install nanobot-ai
```

**从 PyPI 安装**

```bash
pip install nanobot-ai
```

## 🚀 快速开始

**1. 初始化**

```bash
nanobot onboard
```

**2. 配置** (`~/.nanobot/config.json`)

在配置中配置这**两个部分**（其他选项具有默认值）。将以下块添加或合并到现有配置中，而不是替换整个文件。

*设置你的 API 密钥*（例如 [OpenRouter](https://openrouter.ai/keys)，推荐给全球用户）：

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  }
}
```

*设置你的模型*（可选地固定提供商 — 默认为自动检测）：

```json
{
  "agents": {
    "defaults": {
      "provider": "openrouter",
      "model": "anthropic/claude-opus-4-6"
    }
  }
}
```

**3. 聊天**

```bash
nanobot agent
```


- 想要不同的 LLM 提供商、网络搜索、MCP、安全设置或更多配置选项？请参阅[配置](./docs/configuration-zh.md)
- 想要在 Telegram、Discord、微信或飞书等聊天应用中运行 nanobot？请参阅[聊天应用](./docs/chat-apps-zh.md)
- 想要 Docker 或 Linux 服务部署？请参阅[部署](./docs/deployment-zh.md)

## 🧪 WebUI（开发）

> [!NOTE]
> WebUI 开发工作流程目前需要源代码检出，尚未与官方打包版本一起发布。有关完整的 WebUI 开发文档和构建步骤，请参阅 [WebUI 文档](./webui/README.md)。

<p align="center">
  <img src="images/nanobot_webui.png" alt="nanobot webui 预览" width="900">
</p>

**1. 在 `~/.nanobot/config.json` 中启用 WebSocket 渠道**

```json
{ "channels": { "websocket": { "enabled": true } } }
```

**2. 启动网关**

```bash
nanobot gateway
```

**3. 启动 webui 开发服务器**

```bash
cd webui
bun install
bun run dev
```

## 🏗️ 架构

<p align="center">
  <img src="images/nanobot_arch.png" alt="nanobot 架构" width="800">
</p>

🐈 nanobot 通过围绕一个小型智能体循环来保持轻量级：消息来自聊天应用，LLM 决定何时需要工具，内存或技能仅作为上下文引入，而不是成为繁重的编排层。这使核心路径保持可读性且易于扩展，同时仍然允许你添加渠道、工具、内存和部署选项，而不会将系统变成单体。

## ✨ 功能

<table align="center">
  <tr align="center">
    <th><p align="center">📈 24/7 实时市场分析</p></th>
    <th><p align="center">🚀 全栈软件工程师</p></th>
    <th><p align="center">📅 智能日常事务管理器</p></th>
    <th><p align="center">📚 个人知识助手</p></th>
  </tr>
  <tr>
    <td align="center"><p align="center"><img src="case/search.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/code.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/schedule.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/memory.gif" width="180" height="400"></p></td>
  </tr>
  <tr>
    <td align="center">发现 • 洞察 • 趋势</td>
    <td align="center">开发 • 部署 • 扩展</td>
    <td align="center">计划 • 自动化 • 组织</td>
    <td align="center">学习 • 记忆 • 推理</td>
  </tr>
</table>

## 📚 文档

浏览[仓库文档](./docs/README_zh.md)以了解最新功能和 GitHub 开发版本，或访问 [nanobot.wiki](https://nanobot.wiki/docs/latest/getting-started/nanobot-overview)以获取稳定发布文档。

- 使用熟悉的聊天应用与你的 nanobot 交谈：[聊天应用](./docs/chat-apps-zh.md)
- 配置提供商、网络搜索、MCP 和运行时行为：[配置](./docs/configuration-zh.md)
- 将 nanobot 与本地工具和自动化集成：[OpenAI 兼容 API](./docs/openai-api-zh.md) · [Python SDK](./docs/python-sdk-zh.md)
- 使用 Docker 或作为 Linux 服务运行 nanobot：[部署](./docs/deployment-zh.md)

## 🤝 贡献与路线图

欢迎 PR！代码库有意设计得小巧和可读。🤗

### 分支策略

| 分支 | 目的 |
|------|------|
| `main` | 稳定发布 — 错误修复和小改进 |
| `nightly` | 实验性功能 — 新功能和破坏性更改 |

**不确定要针对哪个分支？**详细信息请参阅 [CONTRIBUTING.md](./CONTRIBUTING.md)。

**路线图** — 选择一个项目并[打开 PR](https://github.com/HKUDS/nanobot/pulls)！

- **多模态** — 看见和听到（图像、语音、视频）
- **长期记忆** — 永不忘记重要上下文
- **更好的推理** — 多步规划和反思
- **更多集成** — 日历等
- **自我改进** — 从反馈和错误中学习

## 联系方式

本项目由 [Xubin Ren](https://github.com/re-bin) 作为个人开源项目启动，并继续以个人身份使用个人资源进行维护，并接受开源社区的贡献。如有问题、想法或合作意向，欢迎联系 [xubinrencs@gmail.com](mailto:xubinrencs@gmail.com)。

### 贡献者

<a href="https://github.com/HKUDS/nanobot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/nanobot&max=100&columns=12&updated=20260210" alt="贡献者" />
</a>


## ⭐ Star 历史

<div align="center">
  <a href="https://star-history.com/#HKUDS/nanobot&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date" />
      <img alt="Star 历史图表" src="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date" style="border-radius: 15px; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);" />
    </picture>
  </a>
</div>

<p align="center">
  <em> 感谢访问 ✨ nanobot！</em><br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.nanobot&style=for-the-badge&color=00d4ff" alt="浏览量">
</p>
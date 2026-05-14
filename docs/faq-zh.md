# 常见问题解答 (FAQ)

本文档回答 nanobot 的常见问题，涵盖安装、配置、使用和开发等方面。

## 安装

### 如何安装 nanobot？

有三种安装方式：

**从源码安装**（推荐，获取最新功能）：
```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
pip install -e .
```

**使用 uv 安装**（稳定版本，快速）：
```bash
uv tool install nanobot-ai
```

**从 PyPI 安装**（稳定版本）：
```bash
pip install nanobot-ai
```

**相关文档**：[快速开始](./quick-start-zh.md)

### 如何更新 nanobot？

**PyPI / pip**：
```bash
pip install -U nanobot-ai
nanobot --version
```

**uv**：
```bash
uv tool upgrade nanobot-ai
nanobot --version
```

**使用 WhatsApp？升级后需要重建本地桥接**：
```bash
rm -rf ~/.nanobot/bridge
nanobot channels login whatsapp
```

## 配置

### 配置文件在哪里？

配置文件位于 `~/.nanobot/config.json`（Windows 上为 `C:\Users\你的用户名\.nanobot\config.json`）。

### 如何使用环境变量存储密钥？

可以在配置文件中使用 `${VAR_NAME}` 引用环境变量：

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "${OPENROUTER_API_KEY}"
    }
  },
  "channels": {
    "telegram": {
      "token": "${TELEGRAM_TOKEN}"
    }
  }
}
```

**相关文档**：[配置说明](./configuration-zh.md#环境变量用于密钥管理)

### 如何刷新配置文件而不丢失现有设置？

运行 `nanobot onboard`，然后当询问是否覆盖配置时回答 `N`。nanobot 会合并缺失的默认字段并保留您当前的设置。

### 支持哪些 LLM 提供商？

nanobot 支持以下提供商：

- OpenRouter（推荐，访问所有模型）
- Anthropic (Claude)
- OpenAI
- Azure OpenAI
- DeepSeek
- Groq
- MiniMax
- Gemini
- Qwen (阿里云百炼)
- Zhipu (智谱)
- 以及更多...

**完整列表**：[配置说明 - 提供商](./configuration-zh.md#提供商)

## 使用

### 如何启动 nanobot？

```bash
nanobot agent
```

这将在当前终端启动交互式聊天。

### 如何连接到 Telegram？

1. 获取 Telegram Bot Token（通过 @BotFather）
2. 在配置中添加：
```json
{
  "channels": {
    "telegram": {
      "token": "你的-bot-token"
    }
  }
}
```
3. 运行 `nanobot agent`

**相关文档**：[聊天应用集成](./chat-apps.md)

### 如何启用网页搜索？

在配置中添加：

```json
{
  "agents": {
    "defaults": {
      "tools": ["web_search", "web_fetch"]
    }
  }
}
```

**相关文档**：[配置说明 - Web 搜索](./configuration-zh.md#web-search)

### 如何处理长对话？

nanobot 会自动管理上下文：
- 使用 `max_messages` 和 `max_tokens` 限制历史消息
- 自动压缩旧对话
- 支持记忆整合

可以通过以下配置调整：
```json
{
  "agents": {
    "defaults": {
      "context": {
        "maxMessages": 50,
        "maxTokens": 4000
      }
    }
  }
}
```

### 如何查看会话历史？

会话历史存储在 `~/.nanobot/sessions/` 目录下。每个会话对应一个 JSON 文件。

### 如何重置会话？

在聊天中发送 `/reset` 命令，或删除对应的会话文件。

## 开发

### 如何添加新渠道？

1. 继承 `BaseChannel` 类
2. 实现 `publish_inbound()` 和 `consume_outbound()` 方法
3. 在配置中注册

**相关文档**：[渠道插件开发指南](./channel-plugin-guide.md)

### 如何添加新工具？

1. 在 `nanobot/agent/tools/` 创建工具类
2. 继承适当的基类
3. 在 `ToolLoader` 中注册

**相关文档**：[Python SDK](./python-sdk.md)

### 如何使用 Python SDK？

```python
from nanobot import Nanobot

bot = Nanobot()
result = bot.run("你好！")
print(result)
```

**相关文档**：[Python SDK](./python-sdk.md)

### 如何运行测试？

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_openai_api.py::test_function -v

# 运行代码检查
ruff check nanobot/
```

### 如何构建 WebUI？

```bash
cd webui
bun run build
```

## 故障排除

### nanobot 无法连接到 LLM 提供商

检查：
1. API 密钥是否正确
2. 网络连接是否正常
3. 提供商是否需要特殊配置（如 `apiBase`）
4. 查看日志输出了解详细错误

### 渠道连接失败

检查：
1. 渠道配置是否正确（token、密钥等）
2. 渠道平台的服务是否正常运行
3. 防火墙设置是否允许连接

### 记忆丢失

nanobot 使用原子写入和 fsync 确保持久性。如果仍然丢失记忆：
1. 检查磁盘空间
2. 检查文件权限
3. 查看日志中的错误信息

### 性能问题

优化建议：
1. 减少会话历史大小（调整 `maxMessages` 和 `maxTokens`）
2. 使用更快的 LLM 提供商
3. 禁用不必要的工具
4. 考虑使用提示词缓存（如果提供商支持）

### 配置错误

如果配置文件有问题：
```bash
# 验证配置
nanobot validate-config

# 重新初始化（会创建默认配置）
nanobot onboard
```

## 部署

### 如何使用 Docker 部署？

请参考部署指南中的 Docker 部分。

**相关文档**：[部署指南](./deployment.md)

### 如何使用 systemd 部署（Linux）？

创建 systemd 服务单元文件：

```ini
[Unit]
Description=nanobot AI Agent
After=network.target

[Service]
Type=simple
User=nanobot
WorkingDirectory=/home/nanobot
ExecStart=/usr/local/bin/nanobot agent
Restart=always
EnvironmentFile=/home/nanobot/nanobot_secrets.env

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl enable nanobot
sudo systemctl start nanobot
```

**相关文档**：[部署指南](./deployment.md)

### 如何使用 LaunchAgent 部署（macOS）？

创建 LaunchAgent plist 文件并加载：

```bash
launchctl load ~/Library/LaunchAgents/com.nanobot.agent.plist
```

**相关文档**：[部署指南](./deployment.md)

## 其他

### nanobot 是开源的吗？

是的，nanobot 是开源项目。欢迎贡献！

**GitHub**：https://github.com/HKUDS/nanobot

### 如何报告 Bug？

请在 GitHub Issues 中提交问题：
1. 描述问题的详细步骤
2. 提供错误信息和日志
3. 说明你的环境（操作系统、Python 版本等）
4. 如果可能，提供最小复现示例

### 如何贡献代码？

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

**相关文档**：[CONTRIBUTING.md](../CONTRIBUTING.md)

### 在哪里获取帮助？

- **文档**：[nanobot.wiki](https://nanobot.wiki)
- **GitHub Issues**：https://github.com/HKUDS/nanobot/issues
- **源码**：https://github.com/HKUDS/nanobot

### nanobot 和其他 Agent 框架有什么区别？

nanobot 的特点：
- 轻量级，核心保持精简
- 在边缘扩展（通过 channels、tools、MCP）
- 支持多种聊天平台
- 灵活的配置系统
- 开源且社区驱动

**相关文档**：[项目架构](./architecture-zh.md)

## WebUI 相关

### 如何启动 WebUI？

```bash
cd webui
bun run dev
```

### WebUI 需要什么？

- Node.js 18+
- bun（推荐）或 npm
- 运行中的 nanobot gateway（默认端口 :8765）

### 如何配置 WebUI 代理？

WebUI 开发服务器会自动代理 `/api`、`/webui`、`/auth` 和 WebSocket 流量到网关。

**配置文件**：`webui/vite.config.ts`

## 更多问题？

如果这里没有回答您的问题，请：

1. 查看完整文档：[nanobot.wiki](https://nanobot.wiki)
2. 搜索 GitHub Issues
3. 提交新的 Issue

**参考文档**：
- [快速开始](./quick-start-zh.md)
- [配置说明](./configuration-zh.md)
- [部署指南](./deployment.md)
- [术语表](./glossary-zh.md)
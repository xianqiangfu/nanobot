# 快速入门指南

## 安装

> [!IMPORTANT]
> 本 README 可能描述的功能首先在最新源代码中可用。
> 如果您想要最新功能和实验性功能，请从源代码安装。
> 如果您想要最稳定的日常使用体验，请从 PyPI 或使用 `uv` 安装。

**从源代码安装**（最新功能，实验性更改可能首先在这里落地；推荐用于开发）

```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
pip install -e .
```

**使用 [uv](https://github.com/astral-sh/uv) 安装**（稳定版本，快速）

```bash
uv tool install nanobot-ai
```

**从 PyPI 安装**（稳定版本）

```bash
pip install nanobot-ai
```

### 更新到最新版本

**PyPI / pip**

```bash
pip install -U nanobot-ai
nanobot --version
```

**uv**

```bash
uv tool upgrade nanobot-ai
nanobot --version
```

**使用 WhatsApp？** 升级后重建本地桥接器：

```bash
rm -rf ~/.nanobot/bridge
nanobot channels login whatsapp
```

## 快速开始

> [!TIP]
> 在 `~/.nanobot/config.json` 中设置您的 API 密钥。
> 获取 API 密钥：[OpenRouter](https://openrouter.ai/keys)（全球）
>
> 对于其他 LLM 提供商，请参阅 [`configuration.md`](./configuration.md)。
>
> 关于网络搜索功能设置，请参阅 [`configuration.md`](./configuration.md#web-search) 中的网络搜索部分。

**1. 初始化**

```bash
nanobot onboard
```

如果您想要交互式设置向导，请使用 `nanobot onboard --wizard`。

**2. 配置**（`~/.nanobot/config.json`）

在您的配置中配置这**两个部分**（其他选项有默认值）。

*设置您的 API 密钥*（例如 OpenRouter，推荐全球用户使用）：
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  }
}
```

*设置您的模型*（可选地指定提供商 — 默认为自动检测）：
```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  }
}
```

**3. 开始聊天**

```bash
nanobot agent
```

就这样！您在 2 分钟内就拥有了一个可用的 AI 代理。

## 环境准备

### 系统要求

- **Python 版本**：Python 3.11 或更高版本
- **操作系统**：Linux、macOS、Windows（Windows 需要额外的 UTF-8 编码设置）
- **网络连接**：需要访问 LLM 提供商的 API 端点

### Python 环境准备

```bash
# 检查 Python 版本
python --version

# 如果版本低于 3.11，请先安装 Python 3.11+
# 推荐使用 pyenv 或 conda 管理多个 Python 版本

# 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 升级 pip
pip install --upgrade pip
```

## 安装步骤详解

### 方法一：从源代码安装（推荐用于开发）

```bash
# 1. 克隆仓库
git clone https://github.com/HKUDS/nanobot.git
cd nanobot

# 2. 安装到开发模式
pip install -e .

# 3. 验证安装
nanobot --version
nanobot --help
```

### 方法二：使用 uv 安装（推荐用于日常使用）

```bash
# 确保 uv 已安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 nanobot
uv tool install nanobot-ai

# 验证安装
nanobot --version
```

### 方法三：从 PyPI 安装

```bash
pip install nanobot-ai
nanobot --version
```

## 配置文件详解

### 配置文件位置

默认配置文件位于：`~/.nanobot/config.json`

### 基础配置示例

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-sonnet-4-6",
      "provider": "openrouter"
    }
  },
  "tools": {
    "exec": {
      "enabled": true,
      "restrictToWorkspace": true
    },
    "web": {
      "enabled": true
    }
  }
}
```

### 配置选项说明

#### 提供商配置（providers）

支持多种 LLM 提供商：

```json
{
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-xxx"
    },
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    },
    "openai": {
      "apiKey": "sk-xxx",
      "baseUrl": "https://api.openai.com/v1"
    },
    "azureOpenai": {
      "apiKey": "xxx",
      "endpoint": "https://xxx.openai.azure.com/",
      "apiVersion": "2024-02-15-preview"
    }
  }
}
```

#### 代理配置（agents）

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-sonnet-4-6",
      "provider": "auto",
      "maxToolIterations": 30,
      "maxConcurrentSubagents": 3,
      "temperature": 0.7
    }
  }
}
```

#### 工具配置（tools）

```json
{
  "tools": {
    "exec": {
      "enabled": true,
      "restrictToWorkspace": true,
      "allowedCommands": ["ls", "cat", "grep", "find"]
    },
    "web": {
      "enabled": true,
      "ssrfWhitelist": ["example.com"]
    },
    "my": {
      "enable": false
    }
  }
}
```

## 第一次运行指南

### 1. 初始化配置

```bash
# 使用交互式向导
nanobot onboard --wizard

# 或使用命令行方式
nanobot onboard
```

### 2. 编辑配置文件

```bash
# 打开配置文件
vim ~/.nanobot/config.json

# 或使用其他编辑器
nano ~/.nanobot/config.json
code ~/.nanobot/config.json
```

### 3. 运行 CLI 模式

```bash
# 启动交互式聊天
nanobot agent

# 发送单个请求
nanobot agent -m "你好，请介绍一下你自己"

# 使用特定模型
nanobot agent -m "你好" --model anthropic/claude-sonnet-4-6
```

### 4. 启动网关（用于聊天应用）

```bash
# 启动网关（连接 Telegram、Discord 等）
nanobot gateway

# 查看状态
nanobot status
```

## 常见问题

### Q: 如何获取 API 密钥？

**OpenRouter**（推荐）：访问 [https://openrouter.ai/keys](https://openrouter.ai/keys)

**Anthropic**：访问 [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

**OpenAI**：访问 [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Q: 如何切换到不同的 LLM 提供商？

编辑 `~/.nanobot/config.json`，更改 `providers` 和 `agents.defaults.provider` 部分。

### Q: 如何限制工具执行权限？

在配置文件中设置 `tools.exec.restrictToWorkspace: true`，这将限制文件操作只在工作区目录内执行。

### Q: 如何启用网络搜索功能？

在配置文件中启用 `tools.web.enabled: true`，并可选设置 `tools.web.ssrfWhitelist` 来限制可访问的域名。

### Q: 如何配置多个代理实例？

使用 `--workspace` 参数指定不同的工作目录，每个工作目录有独立的配置和会话。

```bash
nanobot agent --workspace ~/bot1
nanobot agent --workspace ~/bot2
```

## 下一步

- 查看[部署指南](./deployment-zh.md)了解如何将 nanobot 部署到生产环境
- 阅读[配置说明](./configuration.md)了解所有配置选项
- 查看[聊天应用集成](./chat-apps.md)了解如何连接到 Telegram、Discord、WeChat 等平台
- 阅读[开发指南](./developer-guide-zh.md)了解如何扩展和定制 nanobot

## 获取帮助

- 查看 [FAQ](./faq-zh.md)
- 访问 [nanobot.wiki](https://nanobot.wiki)
- 提交 [GitHub Issue](https://github.com/HKUDS/nanobot/issues)
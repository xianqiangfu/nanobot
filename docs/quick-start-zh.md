# 安装和快速入门

## 安装

> [!IMPORTANT]
> 本 README 可能描述的功能首先在最新源代码中可用。
> 如果您想要最新的功能和实验性功能，请从源码安装。
> 如果您想要最稳定的日常使用体验，请从 PyPI 或使用 `uv` 安装。

**从源码安装**（最新功能，实验性更改可能首先在此处落地；推荐用于开发）

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

**使用 WhatsApp？** 升级后重新构建本地桥接：

```bash
rm -rf ~/.nanobot/bridge
nanobot channels login whatsapp
```

## 快速入门

> [!TIP]
> 在 `~/.nanobot/config.json` 中设置您的 API 密钥。
> 获取 API 密钥：[OpenRouter](https://openrouter.ai/keys)（全球）
>
> 对于其他 LLM 提供商，请参阅 [`configuration-zh.md`](./configuration-zh.md)。
>
> 关于网页搜索功能设置，请参阅 [`configuration-zh.md`](./configuration-zh.md#web-search) 中的网页搜索部分。

**1. 初始化**

```bash
nanobot onboard
```

如果需要交互式设置向导，请使用 `nanobot onboard --wizard`。

**2. 配置**（`~/.nanobot/config.json`）

在您的配置中配置这**两个部分**（其他选项有默认值）。

*设置您的 API 密钥*（例如 OpenRouter，推荐全球用户）：
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  }
}
```

*设置您的模型*（可选择固定提供商 — 默认为自动检测）：
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

**3. 聊天**

```bash
nanobot agent
```

就这样！您在 2 分钟内就拥有了一个可用的 AI 助手。
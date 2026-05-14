# 配置系统

本模块提供基于 Pydantic 的配置管理系统。

## 核心组件

### Config Schema (`schema.py`)

使用 Pydantic 定义配置模式，支持：

- 类型验证
- 默认值
- 别名（camelCase 和 snake_case）
- 嵌套配置

### Config Loader (`loader.py`)

配置加载器，负责：

- 从文件加载配置
- 环境变量覆盖
- 配置验证
- 默认值合并

### Config Paths (`paths.py`)

配置路径管理，提供：

- 配置文件路径
- 会话目录路径
- 其他数据目录路径

## 配置文件

默认配置文件位于 `~/.nanobot/config.json`。

### 基本结构

```json
{
  "providers": {
    "default": "anthropic",
    "anthropic": {
      "enabled": true,
      "apiKey": "your_api_key",
      "model": "claude-3-5-sonnet-20241022"
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "your_bot_token"
    }
  },
  "agent": {
    "systemPrompt": "You are a helpful assistant.",
    "maxToolCallsPerTurn": 10,
    "maxTurns": 100
  }
}
```

## 配置模式

### ProvidersConfig

LLM 提供商配置：

```python
class ProvidersConfig(Base):
    default: str = "anthropic"
    anthropic: dict | None = None
    openai: dict | None = None
    # ... 其他提供商
    fallback_models: list[FallbackCandidate] | None = None
```

### ChannelsConfig

聊天频道配置：

```python
class ChannelsConfig(Base):
    send_progress: bool = True
    send_tool_hints: bool = False
    show_reasoning: bool = True
    send_max_retries: int = 3
    transcription_provider: str = "groq"
    transcription_language: str | None = None
```

### AgentConfig

智能体配置：

```python
class AgentConfig(Base):
    system_prompt: str = ""
    max_tool_calls_per_turn: int = 10
    max_turns: int = 100
    temperature: float | None = None
    max_tokens: int | None = None
```

### ToolsConfig

工具配置：

```python
class ToolsConfig(Base):
    filesystem: FilesystemToolConfig | None = None
    shell: ExecToolConfig | None = None
    web: WebToolsConfig | None = None
    # ... 其他工具配置
```

### DreamConfig

Dream 记忆整合配置：

```python
class DreamConfig(Base):
    interval_h: int = 2
    cron: str | None = None
    enabled: bool = True
```

## 配置加载

```python
from nanobot.config import load_config, Config

# 加载配置
config = await load_config()

# 访问配置
provider_config = config.providers.anthropic
channel_config = config.channels.telegram
```

## 环境变量

支持通过环境变量覆盖配置：

```bash
export NANOBOT_PROVIDERS_ANTHROPIC_API_KEY="your_key"
export NANOBOT_CHANNELS_TELEGRAM_TOKEN="your_token"
```

## 配置验证

配置加载时自动验证：

- 类型检查
- 必填字段检查
- 格式验证（如正则表达式）
- 范围验证

## 模型预设

支持模型预设配置：

```json
{
  "modelPresets": {
    "fast": {
      "provider": "anthropic",
      "model": "claude-3-5-haiku-20241022",
      "maxTokens": 4096
    },
    "smart": {
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022",
      "maxTokens": 8192
    }
  }
}
```

## 注意事项

- 配置文件使用 JSON 格式
- 支持 camelCase 和 snake_case 字段名
- 所有配置验证在加载时进行
- 环境变量使用 `NANOBOT_` 前缀
- 配置更新需要重启服务生效
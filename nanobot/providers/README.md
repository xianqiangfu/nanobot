# LLM 提供商

本模块提供多种 LLM 提供商的统一接口实现。

## 支持的提供商

- **Anthropic** (`anthropic_provider.py`) - Anthropic Claude API
- **OpenAI** (`openai_compat_provider.py`) - OpenAI 及兼容 API
- **Azure OpenAI** (`azure_openai_provider.py`) - Azure OpenAI Service
- **GitHub Copilot** (`github_copilot_provider.py`) - GitHub Copilot
- **Amazon Bedrock** (`bedrock_provider.py`) - AWS Bedrock

## 核心组件

### LLMProvider (`base.py`)

所有提供商的基础抽象类，定义了统一的接口：

```python
from nanobot.providers import LLMProvider

class MyProvider(LLMProvider):
    """自定义 LLM 提供商。"""

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs
    ) -> LLMResponse:
        """执行 LLM 完成。"""
        # 实现调用逻辑
        return LLMResponse(...)
```

### ProviderFactory (`factory.py`)

提供商工厂，负责根据配置创建提供商实例。

### ProviderRegistry (`registry.py`)

提供商注册表，管理所有可用的提供商。

### FallbackProvider (`fallback_provider.py`)

回退提供商，支持多提供商故障转移。

## 数据结构

### ToolCallRequest

工具调用请求：

```python
@dataclass
class ToolCallRequest:
    id: str
    name: str
    arguments: dict[str, Any]
    extra_content: dict[str, Any] | None = None
```

### LLMResponse

LLM 响应：

```python
@dataclass
class LLMResponse:
    content: str
    tool_calls: list[ToolCallRequest] | None = None
    model: str | None = None
    usage: dict[str, int] | None = None
```

## 配置

提供商配置在 `~/.nanobot/config.json` 中：

```json
{
  "providers": {
    "default": "anthropic",
    "anthropic": {
      "enabled": true,
      "apiKey": "your_api_key",
      "model": "claude-3-5-sonnet-20241022"
    },
    "openai": {
      "enabled": true,
      "apiKey": "your_api_key",
      "model": "gpt-4",
      "baseUrl": "https://api.openai.com/v1"
    }
  }
}
```

## 使用示例

```python
from nanobot.providers import ProviderFactory
from nanobot.config import load_config

# 加载配置
config = load_config()

# 创建提供商
factory = ProviderFactory(config)
provider = factory.create_provider("anthropic")

# 调用 LLM
messages = [
    {"role": "user", "content": "你好！"}
]
response = await provider.complete(messages)

print(response.content)
```

## 回退配置

支持多提供商回退：

```json
{
  "providers": {
    "fallback_models": [
      {"provider": "anthropic", "model": "claude-3-5-sonnet"},
      {"provider": "openai", "model": "gpt-4"}
    ]
  }
}
```

## 附加功能

### 图像生成 (`image_generation.py`)

支持图像生成提供商。

### 转录 (`transcription.py`)

支持音频转文本功能。

## 创建自定义提供商

```python
from nanobot.providers.base import LLMProvider, LLMResponse

class MyCustomProvider(LLMProvider):
    """自定义 LLM 提供商。"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("apiKey")
        self.model = config.get("model", "default")

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs
    ) -> LLMResponse:
        # 调用自定义 API
        # ...
        return LLMResponse(content="响应内容")

    async def stream_complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs
    ):
        # 流式响应
        async for chunk in self._stream(messages, tools, **kwargs):
            yield chunk
```

## 注意事项

- 所有 API 调用都是异步的
- 提供商应正确处理错误和重试
- 支持流式和非流式两种模式
- 工具调用使用统一的 `ToolCallRequest` 格式
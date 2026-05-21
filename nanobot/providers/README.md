# LLM Providers

This module provides a unified interface implementation for multiple LLM providers.

## Supported Providers

- **Anthropic** (`anthropic_provider.py`) - Anthropic Claude API
- **OpenAI** (`openai_compat_provider.py`) - OpenAI and compatible APIs
- **Azure OpenAI** (`azure_openai_provider.py`) - Azure OpenAI Service
- **GitHub Copilot** (`github_copilot_provider.py`) - GitHub Copilot
- **Amazon Bedrock** (`bedrock_provider.py`) - AWS Bedrock

## Core Components

### LLMProvider (`base.py`)

Base abstract class for all providers, defining a unified interface:

```python
from nanobot.providers import LLMProvider

class MyProvider(LLMProvider):
    """Custom LLM provider."""

    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs
    ) -> LLMResponse:
        """Execute LLM completion."""
        # Implementation logic
        return LLMResponse(...)
```

### ProviderFactory (`factory.py`)

Provider factory responsible for creating provider instances based on configuration.

### ProviderRegistry (`registry.py`)

Provider registry that manages all available providers.

### FallbackProvider (`fallback_provider.py`)

Fallback provider supporting multi-provider failover.

## Data Structures

### ToolCallRequest

Tool call request:

```python
@dataclass
class ToolCallRequest:
    id: str
    name: str
    arguments: dict[str, Any]
    extra_content: dict[str, Any] | None = None
```

### LLMResponse

LLM response:

```python
@dataclass
class LLMResponse:
    content: str
    tool_calls: list[ToolCallRequest] | None = None
    model: str | None = None
    usage: dict[str, int] | None = None
```

## Configuration

Provider configuration is in `~/.nanobot/config.json`:

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

## Usage Example

```python
from nanobot.providers import ProviderFactory
from nanobot.config import load_config

# Load configuration
config = load_config()

# Create provider
factory = ProviderFactory(config)
provider = factory.create_provider("anthropic")

# Call LLM
messages = [
    {"role": "user", "content": "Hello!"}
]
response = await provider.complete(messages)

print(response.content)
```

## Fallback Configuration

Supports multi-provider fallback:

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

## Additional Features

### Image Generation (`image_generation.py`)

Supports image generation providers.

### Transcription (`transcription.py`)

Supports audio-to-text functionality.

## Creating Custom Providers

```python
from nanobot.providers.base import LLMProvider, LLMResponse

class MyCustomProvider(LLMProvider):
    """Custom LLM provider."""

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
        # Call custom API
        # ...
        return LLMResponse(content="Response content")

    async def stream_complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs
    ):
        # Streaming response
        async for chunk in self._stream(messages, tools, **kwargs):
            yield chunk
```

## Notes

- All API calls are asynchronous
- Providers should properly handle errors and retries
- Supports both streaming and non-streaming modes
- Tool calls use a unified `ToolCallRequest` format
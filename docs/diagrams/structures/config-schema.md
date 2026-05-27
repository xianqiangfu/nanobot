# Configuration Schema 层次

```mermaid
classDiagram
    class Config {
        +ProvidersConfig providers
        +ChannelsConfig channels
        +AgentConfig agent
        +ToolsConfig tools
        +DreamConfig dream
        +SessionConfig session
        +WebConfig web
    }

    class ProvidersConfig {
        +str default
        +AnthropicConfig anthropic
        +OpenAIConfig openai
        +AzureConfig azure
        +list fallback_models
    }

    class ChannelsConfig {
        +bool send_progress
        +bool send_tool_hints
        +bool show_reasoning
        +int send_max_retries
        +str transcription_provider
        +str transcription_language
    }

    class AgentConfig {
        +str system_prompt
        +int max_tool_calls_per_turn
        +int max_turns
        +float temperature
        +int max_tokens
        +int reasoning_effort
    }

    class ToolsConfig {
        +FilesystemToolConfig filesystem
        +ExecToolConfig shell
        +WebToolsConfig web
        +ImageGenerationConfig image_generation
        +dict ssrf_whitelist
    }

    class DreamConfig {
        +int interval_h
        +str cron
        +str model_override
        +int max_batch_size
        +int max_iterations
        +bool annotate_line_ages
    }

    Config --> ProvidersConfig
    Config --> ChannelsConfig
    Config --> AgentConfig
    Config --> ToolsConfig
    Config --> DreamConfig
```

## 配置示例

### 完整配置结构

```json
{
  "providers": {
    "default": "anthropic",
    "anthropic": {
      "enabled": true,
      "apiKey": "...",
      "model": "claude-3-5-sonnet-20241022"
    },
    "fallback_models": [
      {"provider": "anthropic", "model": "claude-3-5-haiku"},
      {"provider": "openai", "model": "gpt-4"}
    ]
  },
  "channels": {
    "send_progress": true,
    "send_tool_hints": false,
    "show_reasoning": true,
    "telegram": {
      "enabled": true,
      "token": "..."
    }
  },
  "agent": {
    "system_prompt": "You are a helpful assistant.",
    "max_tool_calls_per_turn": 10,
    "max_turns": 100
  },
  "tools": {
    "filesystem": {
      "enabled": true,
      "allowed_dirs": ["~/.nanobot/workspace"]
    },
    "shell": {
      "enabled": true,
      "restrict_to_workspace": true
    }
  },
  "dream": {
    "interval_h": 2,
    "enabled": true
  }
}
```
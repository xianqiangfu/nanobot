# nanobot 开发者扩展指南

本指南帮助开发者扩展 nanobot 的功能，包括添加新的 LLM 提供商、聊天通道、工具和技能。

## 目录

- [新增 LLM 提供商](#新增-llm-提供商)
- [新增聊天通道](#新增聊天通道)
- [新增工具](#新增工具)
- [新增技能](#新增技能)

---

## 新增 LLM 提供商

### 概述

LLM 提供商负责与不同的 AI 模型服务进行通信，包括 API 调用、消息格式转换、错误处理和重试逻辑。nanobot 提供了一个统一的抽象基类 `LLMProvider`，所有提供商都必须继承此类。

### 开发步骤

#### 1. 创建提供商类

创建一个新的 Python 文件，如 `nanobot/providers/my_provider.py`：

```python
"""My custom LLM provider implementation."""

from __future__ import annotations

from typing import Any

from nanobot.providers.base import LLMProvider, LLMResponse, ToolCallRequest


class MyProvider(LLMProvider):
    """LLM provider for My Service."""

    def __init__(
        self,
        api_key: str | None = None,
        api_base: str | None = None,
        default_model: str = "my-default-model",
    ):
        super().__init__(api_key, api_base)
        self.default_model = default_model
        # 初始化 SDK 客户端
        self._client = ...  # 初始化你的 SDK

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        reasoning_effort: str | None = None,
        tool_choice: str | dict[str, Any] | None = None,
    ) -> LLMResponse:
        """发送聊天完成请求并返回响应。"""
        # 1. 使用提供的模型或默认模型
        model = model or self.default_model

        # 2. 调用提供商的 API
        try:
            response = await self._client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                max_tokens=max_tokens,
                temperature=temperature,
                **self._build_extra_args(reasoning_effort, tool_choice),
            )
        except Exception as e:
            # 转换错误为 LLMResponse
            return self._handle_error(e)

        # 3. 解析响应
        return self._parse_response(response)

    def get_default_model(self) -> str:
        """返回提供商的默认模型名称。"""
        return self.default_model

    def _handle_error(self, e: Exception) -> LLMResponse:
        """处理 API 错误并返回 LLMResponse。"""
        # 提取错误信息和重试建议
        return LLMResponse(
            content=f"Error: {str(e)}",
            finish_reason="error",
        )

    def _parse_response(self, response: Any) -> LLMResponse:
        """解析提供商的响应为 LLMResponse。"""
        # 提取内容
        content = response.choices[0].message.content

        # 提取工具调用
        tool_calls = []
        if hasattr(response.choices[0].message, 'tool_calls'):
            for tc in response.choices[0].message.tool_calls:
                tool_calls.append(ToolCallRequest(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=self._parse_arguments(tc.function.arguments),
                ))

        # 提取推理内容（如果有）
        reasoning_content = getattr(response.choices[0].message, 'reasoning_content', None)

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason=response.choices[0].finish_reason,
            reasoning_content=reasoning_content,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        )

    async def chat_stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        reasoning_effort: str | None = None,
        tool_choice: str | dict[str, Any] | None = None,
        on_content_delta: Callable[[str], Awaitable[None]] | None = None,
    ) -> LLMResponse:
        """流式聊天完成。"""
        # 如果提供商不支持原生流式，基类会回退到非流式调用
        # 支持原生流式的提供商应重写此方法
        stream = await self._client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            tools=tools,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
            **self._build_extra_args(reasoning_effort, tool_choice),
        )

        full_content = ""
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_content += delta
                if on_content_delta:
                    await on_content_delta(delta)

        return LLMResponse(content=full_content, finish_reason="stop")

    def _build_extra_args(self, reasoning_effort: str | None, tool_choice: Any) -> dict[str, Any]:
        """构建提供商特定的额外参数。"""
        args = {}
        if reasoning_effort:
            args["reasoning_effort"] = reasoning_effort
        if tool_choice:
            args["tool_choice"] = tool_choice
        return args

    def _parse_arguments(self, arguments_str: str) -> dict[str, Any]:
        """解析工具调用参数字符串为字典。"""
        import json
        try:
            return json.loads(arguments_str)
        except json.JSONDecodeError:
            return {}
```

#### 2. 注册提供商

在 `nanobot/providers/registry.py` 的 `PROVIDERS` 元组中添加你的提供商规范：

```python
from nanobot.providers.registry import ProviderSpec, PROVIDERS

PROVIDERS = (
    # ... 其他提供商 ...

    # === My Provider =====================================================
    ProviderSpec(
        name="my_provider",                      # 配置字段名
        keywords=("my_provider", "my-model"),    # 模型名匹配关键词（小写）
        env_key="MY_PROVIDER_API_KEY",           # API 密钥环境变量
        display_name="My Provider",              # 在 `nanobot status` 中显示
        backend="my_provider",                   # 提供商实现类型
        default_api_base="https://api.my-provider.com/v1",  # 默认 API 基础 URL
        # 可选配置
        supports_prompt_caching=True,            # 是否支持提示缓存
        supports_max_completion_tokens=True,     # 是否支持 max_completion_tokens
        thinking_style="thinking_type",          # 推理模式注入方式
        # 可选：模型特定的参数覆盖
        model_overrides=(
            ("my-model-v2", {"temperature": 1.0}),
        ),
    ),
)
```

#### 3. 添加配置字段

在 `nanobot/providers/factory.py` 中添加创建提供商实例的逻辑：

```python
def create_provider(provider_spec: ProviderSpec, config: Any) -> LLMProvider:
    """根据配置创建提供商实例。"""
    if provider_spec.backend == "my_provider":
        from nanobot.providers.my_provider import MyProvider
        return MyProvider(
            api_key=config.api_key or os.environ.get("MY_PROVIDER_API_KEY"),
            api_base=config.api_base or provider_spec.default_api_base,
            default_model=config.model or provider_spec.default_api_base,
        )
    # ... 其他提供商 ...
```

或者在 `nanobot/config/schema.py` 中添加专门的配置类：

```python
class MyProviderConfig(Base):
    """My Provider 配置。"""
    enabled: bool = False
    apiKey: str = ""  # 兼容 camelCase 和 snake_case
    apiBase: str = ""
    model: str = "my-default-model"
```

### 提供商实现要点

#### LLMProvider 基类接口

| 方法/属性 | 说明 | 必须实现 |
|-----------|------|---------|
| `async chat()` | 发送聊天完成请求 | 是 |
| `get_default_model()` | 返回默认模型名称 | 是 |
| `async chat_stream()` | 流式聊天完成 | 否（默认回退到非流式） |

#### LLMResponse 响应结构

```python
@dataclass
class LLMResponse:
    content: str | None              # 响应文本内容
    tool_calls: list[ToolCallRequest] # 工具调用列表
    finish_reason: str               # 完成原因（stop/error/tool_calls等）
    usage: dict[str, int]            # Token 使用统计
    reasoning_content: str | None    # 推理内容（如 DeepSeek-R1）
    thinking_blocks: list[dict] | None  # Anthropic 扩展思考块
    # 错误元数据
    error_status_code: int | None
    error_kind: str | None
    error_type: str | None
    error_code: str | None
    error_should_retry: bool | None
```

#### 重试机制

`LLMProvider` 基类内置了智能重试机制：

- **瞬态错误**：网络超时、429 速率限制、5xx 服务器错误等会自动重试
- **非瞬态错误**：配额不足、认证失败等不会重试
- **重试延迟**：从响应头或错误消息中提取 `Retry-After`
- **心跳通知**：通过 `on_retry_wait` 回调通知用户重试进度

提供商可以通过设置 `LLMResponse` 的错误字段来控制重试行为：

```python
return LLMResponse(
    content="Rate limit exceeded",
    error_status_code=429,
    error_kind="rate_limit",
    error_type="rate_limit_exceeded",
    error_retry_after_s=60.0,  # 建议 60 秒后重试
    error_should_retry=True,   # 明确建议重试
)
```

#### 消息格式处理

基类提供了消息清理和规范化工具：

- `_sanitize_empty_content()`：修复空内容块
- `_enforce_role_alternation()`：合并连续相同角色的消息
- `_strip_image_content()`：移除图片内容（用于降级重试）

```python
# 在 chat() 中使用清理后的消息
cleaned_messages = self._sanitize_empty_content(messages)
alternated_messages = self._enforce_role_alternation(cleaned_messages)
```

### 测试提供商

创建测试文件 `tests/providers/test_my_provider.py`：

```python
import pytest
from nanobot.providers.my_provider import MyProvider


@pytest.mark.asyncio
async def test_chat_basic():
    """测试基本聊天功能。"""
    provider = MyProvider(api_key="test-key")
    response = await provider.chat(
        messages=[{"role": "user", "content": "Hello"}],
    )
    assert response.content is not None
    assert response.finish_reason == "stop"


@pytest.mark.asyncio
async def test_tool_call():
    """测试工具调用。"""
    provider = MyProvider(api_key="test-key")
    tools = [{
        "type": "function",
        "function": {
            "name": "my_tool",
            "parameters": {"type": "object"},
        },
    }]
    response = await provider.chat(
        messages=[{"role": "user", "content": "Use my_tool"}],
        tools=tools,
        tool_choice="auto",
    )
    assert len(response.tool_calls) > 0
```

---

## 新增聊天通道

### 概述

聊天通道负责将 nanobot 连接到不同的消息平台（如 Telegram、Discord、Slack 等）。通道必须继承 `BaseChannel` 并实现消息接收和发送的核心接口。

### 开发步骤

#### 1. 创建通道类

创建新的通道实现，如 `nanobot/channels/my_channel.py`：

```python
"""My custom channel implementation."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from pydantic import Field
from loguru import logger

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.base import BaseChannel
from nanobot.config.schema import Base


class MyChannelConfig(Base):
    """My Channel 配置。"""
    enabled: bool = False
    token: str = ""
    allow_from: list[str] = Field(default_factory=list)
    streaming: bool = False


class MyChannel(BaseChannel):
    """My 聊天通道实现。"""
    name = "my_channel"  # 通道唯一标识符
    display_name = "My Channel"  # 显示名称

    def __init__(self, config: Any, bus: MessageBus):
        if isinstance(config, dict):
            config = MyChannelConfig(**config)
        super().__init__(config, bus)
        # 初始化平台 SDK
        self._client = ...  # 初始化你的平台客户端

    @classmethod
    def default_config(cls) -> dict[str, Any]:
        """返回默认配置。"""
        return MyChannelConfig().model_dump(by_alias=True)

    async def start(self) -> None:
        """启动通道并开始监听消息。

        此方法必须阻塞直到 stop() 被调用。
        """
        self._running = True
        logger.info("My Channel starting...")

        # 设置消息处理器
        self._client.add_handler(self._on_message)

        # 开始监听
        await self._client.start()

        # 阻塞直到停止
        while self._running:
            await asyncio.sleep(1)

        await self._client.stop()

    async def stop(self) -> None:
        """停止通道并清理资源。"""
        self._running = False
        await self._client.stop()

    async def send(self, msg: OutboundMessage) -> None:
        """发送消息到平台。"""
        try:
            # 处理媒体附件
            if msg.media:
                for media_path in msg.media:
                    await self._client.send_file(
                        chat_id=msg.chat_id,
                        file_path=media_path,
                    )

            # 发送文本内容
            if msg.content:
                await self._client.send_message(
                    chat_id=msg.chat_id,
                    text=msg.content,
                )
        except Exception as e:
            logger.error("Failed to send message: {}", e)
            raise

    async def send_delta(self, chat_id: str, delta: str, metadata: dict[str, Any] | None = None) -> None:
        """发送流式文本片段。"""
        meta = metadata or {}

        if meta.get("_stream_end"):
            # 流式传输结束
            return

        # 增量更新消息
        await self._client.update_message(chat_id, delta)

    async def _on_message(self, message: Any) -> None:
        """处理来自平台的入站消息。"""
        # 解析发送者信息
        sender_id = str(message.sender_id)
        chat_id = str(message.chat_id)

        # 提取文本内容
        content = message.text or ""

        # 提取媒体
        media = []
        if message.photos:
            for photo in message.photos:
                media.append(await self._download_photo(photo))

        # 转发到消息总线
        await self._handle_message(
            sender_id=sender_id,
            chat_id=chat_id,
            content=content,
            media=media,
        )

    async def _download_photo(self, photo: Any) -> str:
        """下载照片到本地媒体目录。"""
        from nanobot.config.paths import get_media_dir
        media_dir = get_media_dir()
        file_path = media_dir / f"{photo.file_id}.jpg"
        await self._client.download_file(photo.file_id, file_path)
        return str(file_path)
```

#### 2. 注册通道

通道可以通过两种方式注册：

**方式一：内置通道（直接添加到代码库）**

在 `nanobot/channels/__init__.py` 中导出：

```python
from nanobot.channels.my_channel import MyChannel

__all__ = ["MyChannel", ...]
```

**方式二：插件通道（独立包）**

创建独立的 Python 包，使用 entry points 注册：

```toml
# pyproject.toml
[project]
name = "nanobot-channel-my-channel"
version = "0.1.0"
dependencies = ["nanobot-ai", "my-platform-sdk"]

[project.entry-points."nanobot.channels"]
my_channel = "nanobot_channel_my_channel:MyChannel"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["nanobot_channel_my_channel"]
```

包结构：
```
nanobot-channel-my-channel/
├── nanobot_channel_my_channel/
│   ├── __init__.py
│   └── channel.py
└── pyproject.toml
```

#### 3. 配置通道

编辑 `~/.nanobot/config.json`：

```json
{
  "channels": {
    "myChannel": {
      "enabled": true,
      "token": "your-platform-token",
      "allowFrom": ["*"],
      "streaming": true
    }
  }
}
```

### BaseChannel 基类接口

| 方法/属性 | 说明 | 必须实现 |
|-----------|------|---------|
| `async start()` | 启动通道并监听消息，必须阻塞 | 是 |
| `async stop()` | 停止通道并清理资源 | 是 |
| `async send(msg)` | 发送出站消息 | 是 |
| `async send_delta(chat_id, delta, metadata?)` | 流式发送文本片段 | 否 |
| `async send_reasoning_delta()` | 流式发送推理内容 | 否 |
| `async send_reasoning_end()` | 标记推理结束 | 否 |
| `async login(force)` | 交互式登录（如二维码） | 否 |

### 消息处理流程

1. **接收消息**：在 `start()` 中设置平台的消息处理器
2. **验证权限**：调用 `_handle_message()` 自动检查 `allowFrom`
3. **发布到总线**：消息被发布到 `MessageBus` 供 agent 处理
4. **发送响应**：通过 `send()` 或 `send_delta()` 发送回平台

```python
# 典型的消息处理流程
async def _on_message(self, message: Any) -> None:
    await self._handle_message(
        sender_id=str(message.from_user.id),
        chat_id=str(message.chat.id),
        content=message.text,
        media=self._extract_media(message),
    )
```

### 流式支持

通道可以支持实时流式响应：

```python
async def send_delta(self, chat_id: str, delta: str, metadata: dict[str, Any] | None = None) -> None:
    meta = metadata or {}

    if meta.get("_stream_end"):
        # 流式结束，执行最终清理
        self._buffers.pop(chat_id, None)
        return

    # 累积内容并更新显示
    self._buffers.setdefault(chat_id, "")
    self._buffers[chat_id] += delta
    await self._update_message(chat_id, self._buffers[chat_id])
```

当配置中设置 `"streaming": true` 且通道重写了 `send_delta()` 时，agent 会自动使用流式传输。

### 访问控制

通道通过 `allowFrom` 配置实现访问控制：

- `[]`：拒绝所有用户
- `["*"]`：允许所有用户
- `["user1", "user2"]`：仅允许特定用户

```python
# 在 _handle_message() 中自动检查
if not self.is_allowed(sender_id):
    logger.warning("Access denied for sender {}", sender_id)
    return
```

### 交互式登录

支持交互式认证的通道（如二维码扫描）应重写 `login()` 方法：

```python
async def login(self, force: bool = False) -> bool:
    """执行交互式登录。"""
    if not force:
        # 检查是否已认证
        if self._load_credentials():
            return True

    # 显示二维码
    qr_code = await self._client.get_qr_code()
    print(f"请扫描二维码登录: {qr_code}")

    # 轮询确认
    while True:
        if await self._client.check_qr_status(qr_code):
            self._save_credentials()
            return True
        await asyncio.sleep(2)
```

用户可以通过 CLI 触发登录：

```bash
nanobot channels login my_channel
nanobot channels login my_channel --force
```

---

## 新增工具

### 概述

工具（Tool）是 agent 可以调用的能力，如文件操作、命令执行、Web 搜索等。所有工具必须继承 `Tool` 抽象基类并实现特定的接口。

### 开发步骤

#### 1. 创建工具类

创建新的工具实现，如 `nanobot/agent/tools/my_tool.py`：

```python
"""My custom tool implementation."""

from __future__ import annotations

from typing import Any

from pydantic import Field
from loguru import logger

from nanobot.agent.tools.base import Tool, tool_parameters
from nanobot.agent.tools.schema import StringSchema, IntegerSchema, tool_parameters_schema
from nanobot.config.schema import Base


class MyToolConfig(Base):
    """My Tool 配置。"""
    enabled: bool = True
    max_results: int = 10


@tool_parameters(
    tool_parameters_schema(
        query=StringSchema(
            "The search query string",
            min_length=1,
            max_length=500,
        ),
        limit=IntegerSchema(
            10,
            description="Maximum number of results to return",
            minimum=1,
            maximum=100,
        ),
        required=["query"],
    )
)
class MyTool(Tool):
    """自定义工具：执行特定操作。

    这个工具可以向 agent 提供特定的能力。
    """
    # 工具配置
    config_key = "my_tool"

    # 工具作用域
    _scopes = {"core"}

    # 是否为只读操作（安全可并行）
    @property
    def read_only(self) -> bool:
        return True

    # 是否可以与其他工具并发运行
    @property
    def concurrency_safe(self) -> bool:
        return self.read_only and not self.exclusive

    @classmethod
    def config_cls(cls) -> type[Base] | None:
        """返回配置类。"""
        return MyToolConfig

    @classmethod
    def enabled(cls, ctx: Any) -> bool:
        """检查工具是否启用。"""
        return ctx.config.my_tool.enabled

    @classmethod
    def create(cls, ctx: Any) -> Tool:
        """创建工具实例。"""
        cfg = ctx.config.my_tool
        return cls(
            max_results=cfg.max_results,
        )

    async def execute(self, **kwargs: Any) -> Any:
        """执行工具逻辑。"""
        query = kwargs.get("query", "")
        limit = kwargs.get("limit", 10)

        try:
            # 执行你的操作
            results = await self._perform_search(query, limit)

            # 格式化返回结果
            return self._format_results(results)
        except Exception as e:
            logger.exception("MyTool execution failed")
            return f"Error: {str(e)}"

    async def _perform_search(self, query: str, limit: int) -> list[dict]:
        """执行实际的搜索操作。"""
        # 实现你的逻辑
        results = []
        # ... 搜索逻辑 ...
        return results

    def _format_results(self, results: list[dict]) -> str:
        """格式化结果为可读的文本。"""
        if not results:
            return "No results found."

        lines = ["## Search Results"]
        for i, result in enumerate(results, 1):
            lines.append(f"{i}. {result.get('title', 'Untitled')}")
            lines.append(f"   {result.get('url', '')}")
            lines.append(f"   {result.get('snippet', '')}")
            lines.append("")

        return "\n".join(lines)
```

#### 2. 注册工具

在 `nanobot/agent/tools/__init__.py` 中导入工具：

```python
from nanobot.agent.tools.my_tool import MyTool

__all__ = ["MyTool", ...]
```

工具会自动通过 `pkgutil` 扫描被发现，无需额外注册。

#### 3. 配置工具

编辑 `~/.nanobot/config.json`：

```json
{
  "tools": {
    "myTool": {
      "enabled": true,
      "maxResults": 20
    }
  }
}
```

### Tool 基类接口

| 属性/方法 | 说明 | 必须实现 |
|---------|------|---------|
| `name` | 工具名称 | 是 |
| `description` | 工具描述 | 是 |
| `parameters` | JSON Schema 参数定义 | 是 |
| `async execute(**kwargs)` | 执行工具逻辑 | 是 |
| `read_only` | 是否为只读操作 | 否（默认 False） |
| `concurrency_safe` | 是否可并发 | 否（自动计算） |
| `exclusive` | 是否独占运行 | 否（默认 False） |
| `config_cls()` | 返回配置类 | 否 |
| `enabled(ctx)` | 检查是否启用 | 否（默认 True） |
| `create(ctx)` | 创建实例 | 否（默认调用无参构造） |

### 参数定义

使用 `@tool_parameters` 装饰器定义参数：

```python
from nanobot.agent.tools.base import tool_parameters
from nanobot.agent.tools.schema import StringSchema, IntegerSchema, BooleanSchema, tool_parameters_schema

@tool_parameters(
    tool_parameters_schema(
        # 必需参数
        path=StringSchema("File path to read"),
        # 可选参数
        offset=IntegerSchema(0, description="Starting line number", minimum=0),
        limit=IntegerSchema(100, description="Maximum lines to read", minimum=1),
        # 布尔参数
        raw=BooleanSchema(False, description="Return raw content without formatting"),
        required=["path"],
    )
)
class MyTool(Tool):
    ...
```

可用的 Schema 类型：

- `StringSchema(description, min_length?, max_length?)`
- `IntegerSchema(default, description?, minimum?, maximum?)`
- `BooleanSchema(default, description?)`
- `ArraySchema(description?, items?, min_items?, max_items?)`
- `ObjectSchema(description?, properties?, required?)`

### 工具生命周期

```python
# 1. 工具发现
# 系统通过 pkgutil 扫描 nanobot/agent/tools/ 目录

# 2. 配置检查
enabled = MyTool.enabled(ctx)

# 3. 实例创建
tool = MyTool.create(ctx)

# 4. 准备调用
cast_params = tool.cast_params(params)  # 类型转换
errors = tool.validate_params(cast_params)  # 参数验证

# 5. 执行调用
result = await tool.execute(**cast_params)
```

### 类型转换

工具会自动进行参数类型转换：

```python
# LLM 可能传递字符串 "42"
params = {"limit": "42"}

# cast_params 自动转换为整数
cast_params = tool.cast_params(params)
# => {"limit": 42}
```

支持的转换：

- `"42"` → `42` (string to int)
- `"3.14"` → `3.14` (string to float)
- `"true"` → `True` (string to bool)
- `["1", "2"]` → `[1, 2]` (array of strings to array of ints)

### 参数验证

参数根据 JSON Schema 自动验证：

```python
errors = tool.validate_params({"limit": 200})
# => ["limit must be at most 100"]

errors = tool.validate_params({"path": ""})
# => ["path must be at least 1 chars"]
```

### 工具作用域

工具可以指定作用域来控制可用性：

```python
# 仅在核心 agent 中可用
_scopes = {"core"}

# 在核心和子 agent 中可用
_scopes = {"core", "subagent"}

# 插件工具默认使用 {"core"}
```

### 测试工具

创建测试文件 `tests/tools/test_my_tool.py`：

```python
import pytest
from nanobot.agent.tools.my_tool import MyTool
from nanobot.agent.tools.context import ToolContext


@pytest.mark.asyncio
async def tool_context():
    """创建测试用的工具上下文。"""
    from nanobot.config.schema import AgentConfig
    config = AgentConfig()
    return ToolContext(config=config, workspace="/tmp")


@pytest.mark.asyncio
async def test_basic_execution(tool_context):
    """测试基本执行。"""
    tool = MyTool(max_results=5)
    result = await tool.execute(query="test", limit=3)
    assert result is not None
    assert "Search Results" in result


@pytest.mark.asyncio
async def test_parameter_validation(tool_context):
    """测试参数验证。"""
    tool = MyTool(max_results=5)

    # 有效参数
    errors = tool.validate_params({"query": "test", "limit": 5})
    assert errors == []

    # 无效参数
    errors = tool.validate_params({"limit": 0})
    assert "must be at least 1" in str(errors)
```

---

## 新增技能

### 概述

技能（Skill）是通过 Markdown 文件定义的 agent 能力，教 agent 如何使用特定工具或执行特定任务。技能位于 `skills/` 目录或工作区的 `skills/` 子目录中。

### 开发步骤

#### 1. 创建技能目录

在 `skills/` 目录中创建新的技能目录：

```
skills/
└── my_skill/
    └── SKILL.md
```

或者在项目工作区中：

```
~/.nanobot/workspace/skills/
└── my_skill/
    └── SKILL.md
```

#### 2. 编写技能文件

创建 `SKILL.md` 文件，包含技能描述和指导：

```markdown
---
description: 执行特定的数据分析任务
requires:
  bins:
    - python
  env:
    - DATA_API_KEY
nanobot:
  always: false
---

# 数据分析技能

这个技能教 agent 如何执行数据分析任务。

## 前提条件

- 安装了 Python 环境
- 设置了 DATA_API_KEY 环境变量

## 使用方法

1. 使用 `read_file` 工具读取数据文件
2. 使用 `exec` 工具运行 Python 分析脚本
3. 使用 `write_file` 工具保存分析结果

## 示例

### 基础数据统计

要计算 CSV 文件的基础统计信息：

```bash
# 读取数据文件
read_file("data.csv")

# 运行 Python 分析
exec(
    command="python -c 'import pandas as pd; df = pd.read_csv(\"data.csv\"); print(df.describe())'"
)
```

### 数据可视化

要创建数据可视化：

```bash
# 使用 matplotlib 创建图表
exec(
    command="python -c 'import matplotlib.pyplot as plt; import pandas as pd; df = pd.read_csv(\"data.csv\"); df.plot(); plt.savefig(\"plot.png\")'"
)

# 发送图片文件
# (平台会自动附加本地图片)
```

## 最佳实践

1. 始终先检查数据文件是否存在
2. 对大数据集使用分块处理
3. 在分析前验证数据格式
4. 保存中间结果以便调试
```

#### 3. 技能元数据

技能文件开头的 YAML frontmatter 包含元数据：

```yaml
---
description: 技能的简短描述
requires:
  bins:          # 需要的命令行工具
    - python
    - git
  env:           # 需要的环境变量
    - API_KEY
    - DATABASE_URL
nanobot:
  always: false  # 是否始终加载此技能
---
```

| 字段 | 说明 |
|------|------|
| `description` | 技能描述（显示在技能列表中） |
| `requires.bins` | 需要的命令行工具（使用 `which` 检查） |
| `requires.env` | 需要的环境变量 |
| `nanobot.always` | 是否始终加载（默认 false） |

#### 4. 技能加载

技能通过 `SkillsLoader` 加载：

```python
from nanobot.agent.skills import SkillsLoader
from pathlib import Path

loader = SkillsLoader(workspace=Path("/path/to/workspace"))

# 列出所有技能
skills = loader.list_skills()
for skill in skills:
    print(f"{skill['name']}: {skill['source']}")

# 加载特定技能
content = loader.load_skill("my_skill")

# 构建技能摘要
summary = loader.build_skills_summary()
```

#### 5. 技能使用

技能内容会在 agent 上下文中可用：

```python
# 在 agent 运行时，技能内容会被添加到系统提示中
skills_content = loader.load_skills_for_context(["my_skill"])

system_prompt = f"""
You are an AI assistant with the following skills:

{skills_content}

Use these skills when appropriate.
"""
```

### 技能最佳实践

#### 1. 清晰的结构

```markdown
# 技能标题

简短描述技能的用途。

## 何时使用

描述何时应该使用此技能。

## 如何使用

详细的使用步骤和示例。

## 注意事项

重要的警告和限制。
```

#### 2. 实用的示例

提供可复制粘贴的示例：

```markdown
## 示例

### 读取大文件

对于大文件，使用 `limit` 参数：

```bash
read_file("large_file.txt", limit=100)
```

### 搜索内容

使用 Bash 命令搜索：

```bash
exec(command='grep "pattern" file.txt')
```
```

#### 3. 错误处理

说明常见的错误和解决方法：

```markdown
## 故障排除

### 权限错误

如果遇到权限错误：

```bash
exec(command="chmod +x script.sh && ./script.sh")
```

### 内存不足

对于大文件，使用分块处理：

```bash
# 分批读取
exec(command="split -l 10000 large_file.txt chunk_")
```
```

#### 4. 性能建议

```markdown
## 性能优化

1. 使用流式处理大文件
2. 缓存常用数据
3. 使用并行处理

## 示例：并行处理

```bash
# 使用 GNU parallel
exec(command="cat files.txt | parallel process_file")
```
```

### 内置技能

nanobot 包含一些内置技能：

- `file-operations`：文件操作最佳实践
- `shell-commands`：常用 shell 命令
- `debugging`：调试技巧
- `testing`：测试方法

这些技能位于 `nanobot/skills/` 目录中。

### 测试技能

技能可以通过实际使用 agent 进行测试：

```bash
# 启动 agent 并测试技能
nanobot gateway

# 在聊天中触发技能
User: 使用数据分析技能帮我分析 data.csv
```

或通过 CLI 查看技能状态：

```bash
# 列出所有技能
nanobot skills list

# 查看技能内容
nanobot skills show my_skill

# 检查技能依赖
nanobot skills check my_skill
```

---

## 通用开发建议

### 代码风格

- Python 3.11+，全面使用 asyncio
- 行长度：100 字符
- 使用 `ruff` 进行代码检查：`ruff check nanobot/`
- 使用 `pytest` 进行测试：`pytest tests/`

### 错误处理

```python
try:
    result = await some_operation()
except SpecificException as e:
    logger.error("Operation failed: {}", e)
    raise  # 或返回友好的错误消息
```

### 日志记录

```python
from loguru import logger

logger.info("Starting operation")
logger.debug("Debug information: {}", details)
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)  # 包含堆栈跟踪
```

### 配置管理

```python
# 使用 Pydantic 配置类
from nanobot.config.schema import Base

class MyConfig(Base):
    enabled: bool = False
    timeout: int = 60
    # 支持 camelCase 和 snake_case
```

### 测试

```python
import pytest

@pytest.mark.asyncio
async def test_my_function():
    result = await my_async_function()
    assert result is not None
```

---

## 贡献代码

1. Fork 项目仓库
2. 创建功能分支：`git checkout -b feature/my-feature`
3. 提交更改：`git commit -m 'Add my feature'`
4. 推送到分支：`git push origin feature/my-feature`
5. 创建 Pull Request

详细的贡献指南请参考 [CONTRIBUTING.md](../CONTRIBUTING.md)。

---

## 获取帮助

- GitHub Issues: https://github.com/nanobot-ai/nanobot/issues
- 文档: https://docs.nanobot.ai
- Discord 社区: https://discord.gg/nanobot
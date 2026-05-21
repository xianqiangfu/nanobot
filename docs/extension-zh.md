# nanobot 扩展开发指南

本指南介绍如何扩展 nanobot 的功能，包括添加新的 LLM 提供商、聊天通道、工具和技能。

## 目录

- [新增 LLM 提供商](#新增-llm-提供商)
- [新增聊天通道](#新增聊天通道)
- [新增工具](#新增工具)
- [新增技能](#新增技能)
- [MCP 服务器开发](#mcp-服务器开发)

---

## 新增 LLM 提供商

### 概述

LLM 提供商负责与不同的 AI 模型服务进行通信，包括 API 调用、消息格式转换、错误处理和重试逻辑。

### 开发步骤

#### 1. 创建提供商类

创建 `nanobot/providers/my_provider.py`：

```python
from nanobot.providers.base import LLMProvider, LLMResponse, ToolCallRequest

class MyProvider(LLMProvider):
    """LLM provider for My Service."""
    
    def __init__(self, api_key: str | None = None, default_model: str = "my-model"):
        super().__init__(api_key)
        self.default_model = default_model
        self._client = ...  # 初始化 SDK
    
    async def chat(self, messages: list[dict], tools=None, **kwargs) -> LLMResponse:
        """发送聊天完成请求。"""
        response = await self._client.chat.completions.create(
            model=kwargs.get('model') or self.default_model,
            messages=messages,
            tools=tools,
        )
        return self._parse_response(response)
    
    def get_default_model(self) -> str:
        return self.default_model
```

#### 2. 注册提供商

在 `nanobot/providers/registry.py` 中添加：

```python
from nanobot.providers.registry import ProviderSpec, PROVIDERS

PROVIDERS = (
    ProviderSpec(
        name="my_provider",
        keywords=("my_provider", "my-model"),
        env_key="MY_PROVIDER_API_KEY",
        display_name="My Provider",
        backend="my_provider",
        default_api_base="https://api.my-provider.com/v1",
    ),
)
```

#### 3. 添加配置字段

在 `nanobot/config/schema.py` 中添加：

```python
class MyProviderConfig(Base):
    enabled: bool = False
    apiKey: str = ""
    apiBase: str = ""
    model: str = "my-default-model"
```

---

## 新增聊天通道

### 概述

聊天通道负责将 nanobot 连接到不同的消息平台。

### 开发步骤

#### 1. 创建通道类

创建 `nanobot/channels/my_channel.py`：

```python
from nanobot.channels.base import BaseChannel
from nanobot.bus.events import OutboundMessage
from nanobot.config.schema import Base

class MyChannelConfig(Base):
    enabled: bool = False
    token: str = ""
    allowFrom: list[str] = Field(default_factory=list)

class MyChannel(BaseChannel):
    name = "my_channel"
    display_name = "My Channel"
    
    def __init__(self, config, bus):
        super().__init__(config, bus)
        self._client = ...  # 初始化平台客户端
    
    async def start(self) -> None:
        """启动通道并监听消息。"""
        self._running = True
        await self._client.start()
        while self._running:
            await asyncio.sleep(1)
    
    async def stop(self) -> None:
        """停止通道。"""
        self._running = False
        await self._client.stop()
    
    async def send(self, msg: OutboundMessage) -> None:
        """发送消息到平台。"""
        await self._client.send_message(msg.chat_id, msg.content)
```

#### 2. 注册通道

在 `nanobot/channels/__init__.py` 中导出：

```python
from nanobot.channels.my_channel import MyChannel
__all__ = ["MyChannel"]
```

#### 3. 配置通道

编辑 `~/.nanobot/config.json`：

```json
{
  "channels": {
    "myChannel": {
      "enabled": true,
      "token": "your-platform-token"
    }
  }
}
```

---

## 新增工具

### 概述

工具是 agent 可以调用的能力，如文件操作、命令执行、Web 搜索等。

### 开发步骤

#### 1. 创建工具类

创建 `nanobot/agent/tools/my_tool.py`：

```python
from nanobot.agent.tools.base import Tool, tool_parameters
from nanobot.agent.tools.schema import StringSchema, tool_parameters_schema

@tool_parameters(
    tool_parameters_schema(
        query=StringSchema("The search query"),
        required=["query"],
    )
)
class MyTool(Tool):
    """自定义工具：执行特定操作。"""
    
    async def execute(self, **kwargs) -> Any:
        """执行工具逻辑。"""
        query = kwargs.get("query", "")
        result = await self._perform_operation(query)
        return self._format_result(result)
    
    async def _perform_operation(self, query: str) -> list:
        """执行实际操作。"""
        # 实现你的逻辑
        return []
    
    def _format_result(self, results: list) -> str:
        """格式化结果。"""
        return "\n".join(str(r) for r in results)
```

#### 2. 注册工具

在 `nanobot/agent/tools/__init__.py` 中导入：

```python
from nanobot.agent.tools.my_tool import MyTool
__all__ = ["MyTool"]
```

---

## 新增技能

### 概述

技能是通过 Markdown 文件定义的 agent 能力。

### 开发步骤

#### 1. 创建技能目录

```
skills/
└── my_skill/
    └── SKILL.md
```

#### 2. 编写技能文件

创建 `SKILL.md`：

```markdown
---
description: 执行特定的数据分析任务
nanobot:
  always: false
---

# 数据分析技能

这个技能教 agent 如何执行数据分析任务。

## 使用方法

1. 使用 `read_file` 工具读取数据文件
2. 使用 `exec` 工具运行 Python 分析脚本

## 示例

```bash
read_file("data.csv")
exec(command="python -c 'import pandas as pd; df = pd.read_csv("data.csv"); print(df.describe())'")
```
```

---

## MCP 服务器开发

### 概述

MCP (Model Context Protocol) 服务器提供扩展功能。

### 开发步骤

#### 1. 创建 MCP 服务器

创建 `mcp/my_server.py`：

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-mcp-server")

@server.list_resources()
async def list_resources() -> list[dict]:
    return [
        {
            "uri": "my://resource",
            "name": "My Resource",
            "description": "Description",
        }
    ]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )

if __name__ == "__main__":
    asyncio.run(main())
```

#### 2. 注册 MCP 服务器

在 `~/.nanobot/config.json` 中配置：

```json
{
  "tools": {
    "mcp": {
      "servers": [
        {
          "name": "my-server",
          "command": "python",
          "args": ["mcp/my_server.py"]
        }
      ]
    }
  }
}
```

---

## 通用建议

### 代码风格

- Python 3.11+，全面使用 asyncio
- 行长度：100 字符
- 使用 `ruff` 检查代码
- 使用 `pytest` 进行测试

### 错误处理

```python
try:
    result = await some_operation()
except SpecificException as e:
    logger.error("Operation failed: {}", e)
    raise
```

### 日志记录

```python
from loguru import logger
logger.info("Starting operation")
logger.debug("Debug: {}", details)
logger.error("Error occurred", exc_info=True)
```

---

## 获取帮助

- GitHub Issues: https://github.com/HKUDS/nanobot/issues
- 文档: https://nanobot.wiki

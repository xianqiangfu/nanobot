# 聊天通道集成

本模块提供与各种聊天平台的集成，让 nanobot 可以通过多个平台与用户交互。

## 内置频道

- **Telegram** (`telegram.py`) - Telegram Bot API
- **Discord** (`discord.py`) - Discord Bot
- **Slack** (`slack.py`) - Slack Bot
- **飞书** (`feishu.py`) - 飞书开放平台
- **Matrix** (`matrix.py`) - Matrix 协议
- **WhatsApp** (`whatsapp.py`) - WhatsApp Business API
- **企业微信** (`wecom.py`) - 企业微信机器人
- **微信** (`weixin.py`) - 微信公众号/小程序
- **QQ** (`qq.py`) - QQ Bot
- **钉钉** (`dingtalk.py`) - 钉钉机器人
- **Microsoft Teams** (`msteams.py`) - Teams Bot
- **WebSocket** (`websocket.py`) - WebSocket 通道
- **Email** (`email.py`) - 邮件通道
- **MochaChat** (`mochat.py`) - MochaChat 平台

## 核心组件

### BaseChannel (`base.py`)

所有频道的基础抽象类，定义了频道必须实现的接口：

```python
from nanobot.channels import BaseChannel

class MyChannel(BaseChannel):
    """自定义频道实现。"""

    async def start(self) -> None:
        """启动频道。"""
        # 初始化连接
        pass

    async def stop(self) -> None:
        """停止频道。"""
        # 清理资源
        pass

    async def send(self, msg: OutboundMessage) -> bool:
        """发送出站消息。"""
        # 实现发送逻辑
        return True
```

### ChannelManager (`manager.py`)

频道管理器，负责：

- 初始化启用的频道
- 启动/停止频道
- 路由出站消息到相应频道

## 配置

频道配置在 `~/.nanobot/config.json` 中：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "your_bot_token"
    },
    "discord": {
      "enabled": true,
      "token": "your_bot_token"
    }
  }
}
```

## 频道特性

### 流式输出

某些频道支持流式输出，实时显示智能体响应进度：

```json
{
  "channels": {
    "streaming": true
  }
}
```

### 进度提示

可以配置是否发送工具调用提示：

```json
{
  "channels": {
    "send_tool_hints": true
  }
}
```

### 推理显示

支持显示模型推理过程（如果频道支持）：

```json
{
  "channels": {
    "show_reasoning": true
  }
}
```

## 创建自定义频道

1. 继承 `BaseChannel` 类
2. 实现必需的方法
3. 在 `__init__.py` 中注册频道

```python
from nanobot.channels.base import BaseChannel
from nanobot.bus.events import InboundMessage, OutboundMessage

class MyCustomChannel(BaseChannel):
    """自定义频道。"""

    def __init__(self, config: dict[str, Any], bus: MessageBus):
        super().__init__(config, bus)
        # 初始化频道
        pass

    async def _receive_loop(self) -> None:
        """接收消息循环。"""
        # 接收来自平台的消息
        msg = InboundMessage(
            channel=self.name,
            session_key="session_key",
            content="用户消息",
        )
        await self.bus.publish_inbound(msg)
```

## 注意事项

- 所有频道操作都是异步的
- 频道应正确处理错误和重试
- 频道应支持并发消息处理
- 使用 `ChannelManager` 统一管理所有频道
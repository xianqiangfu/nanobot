# 消息总线

消息总线提供解耦聊天频道与智能体核心的异步消息队列机制。

## 核心组件

### MessageBus (`queue.py`)

异步消息队列，使用两个独立的队列：

- **inbound** - 入站消息队列，从频道到智能体
- **outbound** - 出站消息队列，从智能体到频道

## API

### 消息发布

```python
from nanobot.bus.queue import MessageBus
from nanobot.bus.events import InboundMessage, OutboundMessage

bus = MessageBus()

# 发布入站消息（频道 -> 智能体）
await bus.publish_inbound(InboundMessage(...))

# 发布出站消息（智能体 -> 频道）
await bus.publish_outbound(OutboundMessage(...))
```

### 消息消费

```python
# 消费入站消息（在智能体中）
msg = await bus.consume_inbound()

# 消费出站消息（在频道中）
msg = await bus.consume_outbound()
```

### 队列状态

```python
# 获取队列大小
inbound_size = bus.inbound_size
outbound_size = bus.outbound_size
```

## 事件类型

### InboundMessage

入站消息，包含：

- `id` - 消息唯一标识
- `channel` - 来源频道名称
- `session_key` - 会话键
- `content` - 消息内容
- `attachments` - 附件列表
- `metadata` - 额外元数据
- `timestamp` - 时间戳

### OutboundMessage

出站消息，包含：

- `id` - 消息唯一标识
- `channel` - 目标频道名称
- `session_key` - 会话键
- `content` - 响应内容
- `attachments` - 附件列表
- `metadata` - 额外元数据
- `timestamp` - 时间戳

## 架构优势

- **解耦** - 频道和智能体核心完全解耦，各自独立运行
- **异步** - 全异步设计，支持高并发
- **可扩展** - 易于添加新频道或智能体实例
- **缓冲** - 队列提供缓冲，防止生产者阻塞消费者

## 使用场景

```python
import asyncio

from nanobot.bus.queue import MessageBus
from nanobot.agent import AgentLoop
from nanobot.channels import ChannelManager

# 创建消息总线
bus = MessageBus()

# 创建智能体和频道管理器
loop = AgentLoop(bus=bus)
manager = ChannelManager(bus=bus)

# 并发运行
async def main():
    await asyncio.gather(
        loop.start(),
        manager.start(),
    )

asyncio.run(main())
```
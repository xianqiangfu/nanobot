"""异步消息队列，实现聊天通道与智能体核心的解耦。

使用asyncio.Queue实现生产者-消费者模式，通道实例将入站消息推送到队列，
智能体从队列消费消息并处理后推送出站响应。这种解耦设计允许独立地扩展
通道数量和智能体处理能力，同时提供背压机制防止消息堆积。
"""

import asyncio

from nanobot.bus.events import InboundMessage, OutboundMessage


class MessageBus:
    """
    异步消息总线，实现聊天通道与智能体核心的解耦。

    双队列设计实现了消息流的双向解耦：入站队列缓冲来自各通道的用户消息，
    出站队列缓冲智能体生成的响应。这种设计允许通道和智能体异步运行，
    互不阻塞，支持多通道并发和优雅降级。
    """

    def __init__(self):
        # 入站队列：从通道到智能体的消息流
        self.inbound: asyncio.Queue[InboundMessage] = asyncio.Queue()
        # 出站队列：从智能体到通道的响应流
        self.outbound: asyncio.Queue[OutboundMessage] = asyncio.Queue()

    async def publish_inbound(self, msg: InboundMessage) -> None:
        """将通道接收的消息发布到入站队列，供智能体消费。

        当聊天平台有新消息时，对应的通道实例调用此方法将消息推入队列。
        使用async/await确保在高并发场景下的线程安全。
        """
        await self.inbound.put(msg)

    async def consume_inbound(self) -> InboundMessage:
        """从入站队列消费下一条消息，阻塞直到有消息可用。

        智能体循环调用此方法获取待处理的消息。阻塞行为确保在没有消息时
        智能体不会空转，降低CPU使用率。
        """
        return await self.inbound.get()

    async def publish_outbound(self, msg: OutboundMessage) -> None:
        """将智能体的响应发布到出站队列，供通道发送。

        智能体处理完用户消息后，通过此方法将响应推入队列，由通道管理器
        协调发送到对应的聊天平台。
        """
        await self.outbound.put(msg)

    async def consume_outbound(self) -> OutboundMessage:
        """从出站队列消费下一条响应，阻塞直到有响应可用。

        通道管理器调用此方法获取待发送的消息，并根据消息的channel字段
        路由到对应的通道实例进行实际发送。
        """
        return await self.outbound.get()

    @property
    def inbound_size(self) -> int:
        """获取入站队列的待处理消息数量，用于监控消息积压情况。

        当此值持续增长时，可能表明智能体处理能力不足，需要扩展或优化。
        """
        return self.inbound.qsize()

    @property
    def outbound_size(self) -> int:
        """获取出站队列的待发送消息数量，用于监控响应发送延迟。

        当此值持续增长时，可能表明网络连接问题或通道发送速率受限。
        """
        return self.outbound.qsize()

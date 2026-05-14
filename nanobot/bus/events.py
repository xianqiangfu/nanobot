"""消息总线的事件类型定义。

这些数据类用于在聊天通道和智能体核心之间传递消息，
采用不可变数据结构确保消息在异步队列中的安全性。
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class InboundMessage:
    """从聊天通道接收到的入站消息。

    当用户在聊天平台发送消息时，对应的通道实例会创建此对象
    并通过消息总线传递给智能体进行处理。
    """

    channel: str  # 消息来源通道名称（telegram, discord, slack, whatsapp等）
    sender_id: str  # 发送者唯一标识符，用于权限控制和会话关联
    chat_id: str  # 聊天/频道标识符，用于回复消息定位
    content: str  # 消息文本内容，用于LLM处理
    timestamp: datetime = field(default_factory=datetime.now)  # 消息接收时间戳，用于时序分析和日志
    media: list[str] = field(default_factory=list)  # 媒体文件路径列表，支持图片/音频/视频等附件
    metadata: dict[str, Any] = field(default_factory=dict)  # 通道特定的元数据，如消息ID、平台特有字段
    session_key_override: str | None = None  # 可选会话键覆盖，用于线程级别会话隔离

    @property
    def session_key(self) -> str:
        """生成会话唯一键，用于会话历史管理。

        默认使用通道名和聊天ID的组合作为键，这样可以确保不同平台的会话隔离。
        覆盖此键可以实现线程级别的会话隔离（如Slack的thread）。
        """
        return self.session_key_override or f"{self.channel}:{self.chat_id}"


@dataclass
class OutboundMessage:
    """发送到聊天通道的出站消息。

    智能体处理完成后创建此对象，通过消息总线传递给对应的通道实例
    进行实际的平台消息发送。
    """

    channel: str  # 目标通道名称
    chat_id: str  # 目标聊天/频道标识符
    content: str  # 消息文本内容
    reply_to: str | None = None  # 可选的回复目标消息ID，用于上下文关联
    media: list[str] = field(default_factory=list)  # 媒体文件路径列表
    metadata: dict[str, Any] = field(default_factory=dict)  # 元数据，包含流式传输标记、进度信息等
    buttons: list[list[str]] = field(default_factory=list)  # 交互式按钮矩阵，用于复杂对话流程


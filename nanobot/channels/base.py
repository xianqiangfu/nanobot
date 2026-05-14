"""聊天通道的基类接口定义。

所有聊天平台（Telegram、Discord、Slack等）的通道实现都必须继承此类，
实现统一的消息收发接口，从而与nanobot消息总线无缝集成。这种抽象层设计
使得添加新平台只需实现基类接口，无需修改智能体核心代码。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from loguru import logger

from nanobot.bus.events import InboundMessage, OutboundMessage
from nanobot.bus.queue import MessageBus


class BaseChannel(ABC):
    """
    聊天通道实现的抽象基类。

    定义了所有通道必须实现的核心接口，包括启动、停止、发送消息等。
    通过这种统一的抽象，消息总线和智能体核心可以与任何聊天平台交互，
    实现平台无关的智能体逻辑。
    """

    name: str = "base"  # 通道唯一标识符，用于配置和路由
    display_name: str = "Base"  # 通道显示名称，用于日志和UI展示
    transcription_provider: str = "groq"  # 音频转写服务提供商（openai或groq）
    transcription_api_key: str = ""  # 转写服务的API密钥
    transcription_api_base: str = ""  # 转写服务的API基础URL
    transcription_language: str | None = None  # 转写目标语言，None表示自动检测
    send_progress: bool = True  # 是否发送处理进度消息，提升用户体验
    send_tool_hints: bool = False  # 是否发送工具调用提示，用于调试和透明度
    show_reasoning: bool = True  # 是否显示模型推理过程，用于复杂任务的可解释性

    def __init__(self, config: Any, bus: MessageBus):
        """
        初始化通道实例。

        Args:
            config: 通道特定配置对象（dict或Pydantic模型）
            bus: 消息总线实例，用于与智能体核心通信
        """
        self.config = config
        self.logger = logger.bind(channel=self.name)  # 绑定通道名到日志上下文
        self.bus = bus
        self._running = False  # 运行状态标志，用于优雅关闭

    async def transcribe_audio(self, file_path: str | Path) -> str:
        """通过Whisper服务转写音频文件，失败返回空字符串。

        支持OpenAI和Groq两种转写服务。当API密钥未配置时静默失败，
        避免因缺少转写能力而阻塞主消息处理流程。
        """
        if not self.transcription_api_key:
            return ""
        try:
            if self.transcription_provider == "openai":
                from nanobot.providers.transcription import OpenAITranscriptionProvider
                provider = OpenAITranscriptionProvider(
                    api_key=self.transcription_api_key,
                    api_base=self.transcription_api_base or None,
                    language=self.transcription_language or None,
                )
            else:
                from nanobot.providers.transcription import GroqTranscriptionProvider
                provider = GroqTranscriptionProvider(
                    api_key=self.transcription_api_key,
                    api_base=self.transcription_api_base or None,
                    language=self.transcription_language or None,
                )
            return await provider.transcribe(file_path)
        except Exception:
            self.logger.exception("Audio transcription failed")
            return ""

    async def login(self, force: bool = False) -> bool:
        """
        执行通道特定的交互式登录流程（如二维码扫描）。

        Args:
            force: 为True时忽略已有凭证，强制重新认证

        Returns:
            如果已认证或登录成功返回True
        注：仅支持交互式登录的子类需要重写此方法
        """
        return True

    @abstractmethod
    async def start(self) -> None:
        """
        启动通道并开始监听消息。

        此方法应是一个长期运行的异步任务，负责：
        1. 建立与聊天平台的连接
        2. 持续监听入站消息
        3. 通过_handle_message()将消息转发到总线

        典型实现会启动一个while循环，使用平台的SDK或API订阅事件。
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """停止通道并清理资源。

        应关闭所有网络连接、取消订阅事件、释放SDK资源等。
        确保可以安全地重新启动通道而不会残留状态。
        """
        pass

    @abstractmethod
    async def send(self, msg: OutboundMessage) -> None:
        """
        通过此通道发送消息。

        Args:
            msg: 要发送的消息对象

        注：实现时应在投递失败时抛出异常，以便通道管理器统一应用重试策略。
        """
        pass

    async def send_delta(self, chat_id: str, delta: str, metadata: dict[str, Any] | None = None) -> None:
        """发送流式文本片段。

        子类重写此方法以启用流式响应。实现时应在投递失败时抛出异常，
        以便通道管理器重试。

        流式传输契约：_stream_delta是增量片段，_stream_end标记当前段结束，
        有状态实现必须使用_stream_id而不仅是chat_id来索引缓冲区。
        """
        pass

    async def send_reasoning_delta(
        self, chat_id: str, delta: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """流式发送模型推理/思考内容的片段。

        默认实现为空操作。支持原生低优先级渲染原语的通道（Slack上下文块、
        Telegram可展开引用块、Discord副文本、WebUI斜体气泡等）应重写此方法，
        将推理渲染为随着模型思考而原地更新的从属轨迹。

        流式传输契约与send_delta镜像：_reasoning_delta是片段，
        _reasoning_end标记当前推理段结束，有状态实现应使用_stream_id
        而不仅是chat_id来索引缓冲区。
        """
        return

    async def send_reasoning_end(
        self, chat_id: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """标记推理流段的结束。

        默认实现为空操作。缓冲send_reasoning_delta片段以实现原地更新的通道
        使用此信号刷新并冻结渲染组；一次性发送通道可以完全忽略它。
        """
        return

    async def send_reasoning(self, msg: OutboundMessage) -> None:
        """发送完整的推理块。

        默认实现重用流式传输对，使插件只需重写delta/end方法。等价于一个包含
        全部内容的delta后紧跟一个结束标记——为流式和一次性推理保持单一渲染路径
        （如DeepSeek-R1的final-response reasoning_content）。
        """
        if not msg.content:
            return
        meta = dict(msg.metadata or {})
        meta.setdefault("_reasoning_delta", True)
        await self.send_reasoning_delta(msg.chat_id, msg.content, meta)
        end_meta = dict(meta)
        end_meta.pop("_reasoning_delta", None)
        end_meta["_reasoning_end"] = True
        await self.send_reasoning_end(msg.chat_id, end_meta)

    @property
    def supports_streaming(self) -> bool:
        """当配置启用流式传输且此类实现了send_delta时返回True。

        双重检查确保即使配置启用，子类未实现流式接口也不会错误激活。
        """
        cfg = self.config
        streaming = cfg.get("streaming", False) if isinstance(cfg, dict) else getattr(cfg, "streaming", False)
        return bool(streaming) and type(self).send_delta is not BaseChannel.send_delta

    def is_allowed(self, sender_id: str) -> bool:
        """检查sender_id是否被允许。空列表→拒绝所有；"*"→允许所有。

        此方法实现访问控制白名单机制，防止未授权用户使用机器人。
        支持从dict配置和Pydantic模型配置中读取allowFrom/allow_from字段。
        """
        if isinstance(self.config, dict):
            if "allow_from" in self.config:
                allow_list = self.config.get("allow_from")
            else:
                allow_list = self.config.get("allowFrom", [])
        else:
            allow_list = getattr(self.config, "allow_from", [])
        if not allow_list:
            self.logger.warning("allow_from is empty — all access denied")
            return False
        if "*" in allow_list:
            return True
        return str(sender_id) in allow_list

    async def _handle_message(
        self,
        sender_id: str,
        chat_id: str,
        content: str,
        media: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        session_key: str | None = None,
    ) -> None:
        """
        处理从聊天平台接收到的入站消息。

        此方法检查权限并将消息转发到总线。

        Args:
            sender_id: 发送者标识符
            chat_id: 聊天/频道标识符
            content: 消息文本内容
            media: 可选的媒体URL列表
            metadata: 可选的通道特定元数据
            session_key: 可选的会话键覆盖（如线程级别会话）
        """
        if not self.is_allowed(sender_id):
            self.logger.warning(
                "Access denied for sender {}. "
                "Add them to allowFrom list in config to grant access.",
                sender_id,
            )
            return

        meta = metadata or {}
        if self.supports_streaming:
            meta = {**meta, "_wants_stream": True}  # 标记期望流式响应

        msg = InboundMessage(
            channel=self.name,
            sender_id=str(sender_id),
            chat_id=str(chat_id),
            content=content,
            media=media or [],
            metadata=meta,
            session_key_override=session_key,
        )

        await self.bus.publish_inbound(msg)

    @classmethod
    def default_config(cls) -> dict[str, Any]:
        """返回默认配置用于初始化。插件应重写此方法以自动填充config.json。

        当用户首次启用某个通道时，系统会调用此方法生成默认配置，
        简化配置流程并降低错误风险。
        """
        return {"enabled": False}

    @property
    def is_running(self) -> bool:
        """检查通道是否正在运行。

        此属性用于监控通道状态和实现优雅关闭逻辑。
        """
        return self._running

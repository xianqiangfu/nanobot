"""通道管理器，协调所有聊天通道的消息路由。

此类是通道系统的核心协调器，负责通道的生命周期管理、出站消息分发、
流式传输合并、重复消息抑制等关键功能。通过集中管理，实现了统一的
错误处理、重试策略和监控能力。
"""

from __future__ import annotations

import asyncio
import hashlib
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Any

from loguru import logger

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.base import BaseChannel
from nanobot.config.schema import Config
from nanobot.utils.restart import consume_restart_notice_from_env, format_restart_completed_message

if TYPE_CHECKING:
    from nanobot.session.manager import SessionManager


def _default_webui_dist() -> Path | None:
    """返回捆绑的webui dist目录的绝对路径（如果存在）。

    WebSocket通道需要此路径来托管嵌入式WebUI界面。
    如果web包未安装或dist目录不存在，返回None。
    """
    try:
        import nanobot.web as web_pkg  # type: ignore[import-not-found]
    except ImportError:
        return None
    candidate = Path(web_pkg.__file__).resolve().parent / "dist"
    return candidate if candidate.is_dir() else None


# 消息发送重试延迟（指数退避：1秒、2秒、4秒）
# 使用指数退避可以在网络波动时自动调整重试频率，避免雪崩
_SEND_RETRY_DELAYS = (1, 2, 4)

# 布尔配置字段的camelCase别名映射
# 支持从JSON/TOML配置文件读取驼峰命名的字段，提高配置灵活性
_BOOL_CAMEL_ALIASES: dict[str, str] = {
    "send_progress": "sendProgress",
    "send_tool_hints": "sendToolHints",
    "show_reasoning": "showReasoning",
}

class ChannelManager:
    """
    管理聊天通道并协调消息路由。

    职责：
    - 初始化启用的通道（Telegram、WhatsApp等）
    - 启动/停止通道
    - 路由出站消息

    通过集中管理所有通道实例，实现了统一的配置解析、错误处理和
    状态监控，同时提供流式传输合并、重复消息抑制等优化功能。
    """

    def __init__(
        self,
        config: Config,
        bus: MessageBus,
        *,
        session_manager: "SessionManager | None" = None,
    ):
        self.config = config
        self.bus = bus
        self._session_manager = session_manager
        self.channels: dict[str, BaseChannel] = {}
        self._dispatch_task: asyncio.Task | None = None
        self._origin_reply_fingerprints: dict[tuple[str, str, str], str] = {}

        self._init_channels()

    def _init_channels(self) -> None:
        """初始化通过pkgutil扫描和entry_points插件发现的通道。

        此方法自动发现所有可用的通道实现，根据配置启用对应的通道，
        并注入共享的转写服务配置和发送行为设置。
        """
        from nanobot.channels.registry import discover_all

        transcription_provider = self.config.channels.transcription_provider
        transcription_key = self._resolve_transcription_key(transcription_provider)
        transcription_base = self._resolve_transcription_base(transcription_provider)
        transcription_language = self.config.channels.transcription_language

        for name, cls in discover_all().items():
            section = getattr(self.config.channels, name, None)
            if section is None:
                continue
            enabled = (
                section.get("enabled", False)
                if isinstance(section, dict)
                else getattr(section, "enabled", False)
            )
            if not enabled:
                continue
            try:
                kwargs: dict[str, Any] = {}
                # 只有WebSocket通道当前托管嵌入式webui界面；
                # 其他通道保持对这些配置的无感知。
                if cls.name == "websocket" and self._session_manager is not None:
                    kwargs["session_manager"] = self._session_manager
                    static_path = _default_webui_dist()
                    if static_path is not None:
                        kwargs["static_dist_path"] = static_path
                channel = cls(section, self.bus, **kwargs)
                # 注入共享的转写服务配置
                channel.transcription_provider = transcription_provider
                channel.transcription_api_key = transcription_key
                channel.transcription_api_base = transcription_base
                channel.transcription_language = transcription_language
                # 注入发送行为配置，支持通道级覆盖
                channel.send_progress = self._resolve_bool_override(
                    section, "send_progress", self.config.channels.send_progress,
                )
                channel.send_tool_hints = self._resolve_bool_override(
                    section, "send_tool_hints", self.config.channels.send_tool_hints,
                )
                channel.show_reasoning = self._resolve_bool_override(
                    section, "show_reasoning", self.config.channels.show_reasoning,
                )
                self.channels[name] = channel
                logger.info("{} channel enabled", cls.display_name)
            except Exception as e:
                logger.warning("{} channel not available: {}", name, e)

        self._validate_allow_from()

    def _resolve_transcription_key(self, provider: str) -> str:
        """为配置的转写提供商选择API密钥。"""
        try:
            if provider == "openai":
                return self.config.providers.openai.api_key
            return self.config.providers.groq.api_key
        except AttributeError:
            return ""

    def _resolve_transcription_base(self, provider: str) -> str:
        """为配置的转写提供商选择API基础URL。"""
        try:
            if provider == "openai":
                return self.config.providers.openai.api_base or ""
            return self.config.providers.groq.api_base or ""
        except AttributeError:
            return ""

    def _validate_allow_from(self) -> None:
        """验证所有通道的allow_from配置不为空列表。

        空列表会拒绝所有访问，通常表示配置错误，应提前阻止启动。
        """
        for name, ch in self.channels.items():
            cfg = ch.config
            if isinstance(cfg, dict):
                if "allow_from" in cfg:
                    allow = cfg.get("allow_from")
                else:
                    allow = cfg.get("allowFrom")
            else:
                allow = getattr(cfg, "allow_from", None)
            if allow == []:
                raise SystemExit(
                    f'Error: "{name}" has empty allowFrom (denies all). '
                    f'Set ["*"] to allow everyone, or add specific user IDs.'
                )

    def _should_send_progress(self, channel_name: str, *, tool_hint: bool = False) -> bool:
        """返回是否可以向channel_name发送进度（或工具提示）。"""
        ch = self.channels.get(channel_name)
        if ch is None:
            logger.warning("Progress check for unknown channel: {}", channel_name)
            return False
        return ch.send_tool_hints if tool_hint else ch.send_progress

    def _resolve_bool_override(self, section: Any, key: str, default: bool) -> bool:
        """如果section中key是布尔值则返回，否则返回default。

        对于dict配置还会检查camelCase别名（如sendProgress对应send_progress），
        使原始JSON/TOML配置可以与Pydantic模型一起工作。
        """
        if isinstance(section, dict):
            value = section.get(key)
            if value is None:
                camel = _BOOL_CAMEL_ALIASES.get(key)
                if camel:
                    value = section.get(camel)
            return value if isinstance(value, bool) else default
        value = getattr(section, key, None)
        return value if isinstance(value, bool) else default

    async def _start_channel(self, name: str, channel: BaseChannel) -> None:
        """启动一个通道并记录任何异常。

        将通道启动包装在try-except中，确保单个通道失败不会影响其他通道。
        """
        try:
            await channel.start()
        except Exception:
            logger.exception("Failed to start channel {}", name)

    async def start_all(self) -> None:
        """启动所有通道和出站分发器。"""
        if not self.channels:
            logger.warning("No channels enabled")
            return

        # 启动出站分发器
        self._dispatch_task = asyncio.create_task(self._dispatch_outbound())

        # 启动通道
        tasks = []
        for name, channel in self.channels.items():
            logger.info("Starting {} channel...", name)
            tasks.append(asyncio.create_task(self._start_channel(name, channel)))

        self._notify_restart_done_if_needed()

        # 等待所有任务完成（它们应该永久运行）
        await asyncio.gather(*tasks, return_exceptions=True)

    def _notify_restart_done_if_needed(self) -> None:
        """当运行时环境标记存在时发送重启完成消息。

        系统通过环境变量传递重启通知信息，此方法检查并发送完成消息
        到触发重启的聊天会话。
        """
        notice = consume_restart_notice_from_env()
        if not notice:
            return
        target = self.channels.get(notice.channel)
        if not target:
            return
        asyncio.create_task(self._send_with_retry(
            target,
            OutboundMessage(
                channel=notice.channel,
                chat_id=notice.chat_id,
                content=format_restart_completed_message(notice.started_at_raw),
                metadata=dict(notice.metadata or {}),
            ),
        ))

    async def stop_all(self) -> None:
        """停止所有通道和分发器。"""
        logger.info("Stopping all channels...")

        # 停止分发器
        if self._dispatch_task:
            self._dispatch_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._dispatch_task

        # 停止所有通道
        for name, channel in self.channels.items():
            try:
                await channel.stop()
                logger.info("Stopped {} channel", name)
            except Exception:
                logger.exception("Error stopping {}", name)

    @staticmethod
    def _fingerprint_content(content: str) -> str:
        """生成消息内容的哈希指纹，用于重复检测。

        规范化空格后使用SHA1哈希，确保相同内容的消息具有相同指纹。
        """
        normalized = " ".join(content.split())
        return hashlib.sha1(normalized.encode("utf-8")).hexdigest() if normalized else ""

    def _should_suppress_outbound(self, msg: OutboundMessage) -> bool:
        """检查是否应该抑制此出站消息以避免重复发送。

        基于消息内容指纹和关联的消息ID进行判断。相同的指纹且关联到
        同一源消息则认为是重复。进度消息和流式片段不被抑制。
        """
        metadata = msg.metadata or {}
        if metadata.get("_progress"):
            return False
        fingerprint = self._fingerprint_content(msg.content)
        if not fingerprint:
            return False

        origin_message_id = metadata.get("origin_message_id")
        if isinstance(origin_message_id, str) and origin_message_id:
            key = (msg.channel, msg.chat_id, origin_message_id)
            if self._origin_reply_fingerprints.get(key) == fingerprint:
                return True
            self._origin_reply_fingerprints[key] = fingerprint

        message_id = metadata.get("message_id")
        if isinstance(message_id, str) and message_id:
            key = (msg.channel, msg.chat_id, message_id)
            self._origin_reply_fingerprints[key] = fingerprint

        return False

    async def _dispatch_outbound(self) -> None:
        """Dispatch outbound messages to the appropriate channel."""
        logger.info("Outbound dispatcher started")

        # Buffer for messages that couldn't be processed during delta coalescing
        # (since asyncio.Queue doesn't support push_front)
        pending: list[OutboundMessage] = []

        while True:
            try:
                # First check pending buffer before waiting on queue
                if pending:
                    msg = pending.pop(0)
                else:
                    msg = await asyncio.wait_for(
                        self.bus.consume_outbound(),
                        timeout=1.0
                    )

                if (
                    msg.metadata.get("_reasoning_delta")
                    or msg.metadata.get("_reasoning_end")
                    or msg.metadata.get("_reasoning")
                ):
                    # Reasoning rides its own plugin channel: only delivered
                    # when the destination channel opts in via ``show_reasoning``
                    # and overrides the streaming primitives. Channels without
                    # a low-emphasis UI affordance keep the base no-op and the
                    # content silently drops here. ``_reasoning`` (one-shot)
                    # is accepted for backward compatibility with hooks that
                    # haven't migrated to delta/end yet.
                    channel = self.channels.get(msg.channel)
                    if channel is not None and channel.show_reasoning:
                        await self._send_with_retry(channel, msg)
                    continue

                if msg.metadata.get("_progress"):
                    if msg.metadata.get("_tool_hint") and not self._should_send_progress(
                        msg.channel, tool_hint=True,
                    ):
                        continue
                    if not msg.metadata.get("_tool_hint") and not self._should_send_progress(
                        msg.channel, tool_hint=False,
                    ):
                        continue

                if msg.metadata.get("_retry_wait"):
                    continue

                if (
                    msg.metadata.get("_runtime_model_updated")
                    and msg.channel == "websocket"
                    and "websocket" not in self.channels
                ):
                    continue

                # Coalesce consecutive _stream_delta messages for the same (channel, chat_id)
                # to reduce API calls and improve streaming latency
                if msg.metadata.get("_stream_delta") and not msg.metadata.get("_stream_end"):
                    msg, extra_pending = self._coalesce_stream_deltas(msg)
                    pending.extend(extra_pending)

                channel = self.channels.get(msg.channel)
                if channel:
                    # Duplicate suppression is scoped to a known source message
                    # so repeated content from separate turns is still delivered.
                    if (
                        not msg.metadata.get("_stream_delta")
                        and not msg.metadata.get("_stream_end")
                        and not msg.metadata.get("_streamed")
                    ):
                        if self._should_suppress_outbound(msg):
                            logger.info("Suppressing duplicate outbound message to {}:{}", msg.channel, msg.chat_id)
                            continue
                    await self._send_with_retry(channel, msg)
                else:
                    logger.warning("Unknown channel: {}", msg.channel)

            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    @staticmethod
    async def _send_once(channel: BaseChannel, msg: OutboundMessage) -> None:
        """发送一条出站消息而不应用重试策略。"""
        if msg.metadata.get("_reasoning_end"):
            await channel.send_reasoning_end(msg.chat_id, msg.metadata)
        elif msg.metadata.get("_reasoning_delta"):
            await channel.send_reasoning_delta(msg.chat_id, msg.content, msg.metadata)
        elif msg.metadata.get("_reasoning"):
            # Back-compat: one-shot reasoning. BaseChannel translates this
            # to a single delta + end pair so plugins only implement the
            # streaming primitives.
            await channel.send_reasoning(msg)
        elif msg.metadata.get("_stream_delta") or msg.metadata.get("_stream_end"):
            await channel.send_delta(msg.chat_id, msg.content, msg.metadata)
        elif not msg.metadata.get("_streamed"):
            await channel.send(msg)

    def _coalesce_stream_deltas(
        self, first_msg: OutboundMessage
    ) -> tuple[OutboundMessage, list[OutboundMessage]]:
        """合并同一(channel, chat_id)的连续_stream_delta消息。

        当队列累积多个delta时，这会减少API调用数，这种情况发生在
        LLM生成速度快于通道处理速度时。

        Returns:
            (合并后的消息, 不匹配消息列表)的元组
        """
        target_key = (first_msg.channel, first_msg.chat_id)
        combined_content = first_msg.content
        final_metadata = dict(first_msg.metadata or {})
        non_matching: list[OutboundMessage] = []

        # Only merge consecutive deltas. As soon as we hit any other message,
        # stop and hand that boundary back to the dispatcher via `pending`.
        while True:
            try:
                next_msg = self.bus.outbound.get_nowait()
            except asyncio.QueueEmpty:
                break

            # Check if this message belongs to the same stream
            same_target = (next_msg.channel, next_msg.chat_id) == target_key
            is_delta = next_msg.metadata and next_msg.metadata.get("_stream_delta")
            is_end = next_msg.metadata and next_msg.metadata.get("_stream_end")

            if same_target and is_delta and not final_metadata.get("_stream_end"):
                # Accumulate content
                combined_content += next_msg.content
                # If we see _stream_end, remember it and stop coalescing this stream
                if is_end:
                    final_metadata["_stream_end"] = True
                    # Stream ended - stop coalescing this stream
                    break
            else:
                # First non-matching message defines the coalescing boundary.
                non_matching.append(next_msg)
                break

        merged = OutboundMessage(
            channel=first_msg.channel,
            chat_id=first_msg.chat_id,
            content=combined_content,
            metadata=final_metadata,
        )
        return merged, non_matching

    async def _send_with_retry(self, channel: BaseChannel, msg: OutboundMessage) -> None:
        """使用指数退避的重试策略发送消息。

        注：CancelledError被重新抛出以允许优雅关闭。
        """
        max_attempts = max(self.config.channels.send_max_retries, 1)

        for attempt in range(max_attempts):
            try:
                await self._send_once(channel, msg)
                return  # Send succeeded
            except asyncio.CancelledError:
                raise  # Propagate cancellation for graceful shutdown
            except Exception as e:
                if attempt == max_attempts - 1:
                    logger.exception(
                        "Failed to send to {} after {} attempts",
                        msg.channel, max_attempts
                    )
                    return
                delay = _SEND_RETRY_DELAYS[min(attempt, len(_SEND_RETRY_DELAYS) - 1)]
                logger.warning(
                    "Send to {} failed (attempt {}/{}): {}, retrying in {}s",
                    msg.channel, attempt + 1, max_attempts, type(e).__name__, delay
                )
                try:
                    await asyncio.sleep(delay)
                except asyncio.CancelledError:
                    raise  # Propagate cancellation during sleep

    def get_channel(self, name: str) -> BaseChannel | None:
        """按名称获取通道。"""
        return self.channels.get(name)

    def get_status(self) -> dict[str, Any]:
        """获取所有通道的状态。"""
        return {
            name: {
                "enabled": True,
                "running": channel.is_running
            }
            for name, channel in self.channels.items()
        }

    @property
    def enabled_channels(self) -> list[str]:
        """获取启用的通道名称列表。"""
        return list(self.channels.keys())

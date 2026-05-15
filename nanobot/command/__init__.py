"""斜杠命令路由和内置处理器。"""

from nanobot.command.builtin import register_builtin_commands
from nanobot.command.router import CommandContext, CommandRouter

__all__ = ["CommandContext", "CommandRouter", "register_builtin_commands"]

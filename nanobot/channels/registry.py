"""内置通道模块和外部插件的自动发现系统。

通过pkgutil扫描内置通道实现，通过entry_points发现外部插件，
实现通道的动态加载和插件化扩展。内置通道优先，防止外部插件覆盖
内置实现，确保核心功能的稳定性。
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from nanobot.channels.base import BaseChannel

_INTERNAL = frozenset({"base", "manager", "registry"})  # 排除内部模块，只发现实际的通道实现


def discover_channel_names() -> list[str]:
    """通过扫描包返回所有内置通道模块名称（零导入）。

    使用pkgutil.iter_modules而不导入任何模块，实现零开销的通道发现。
    排除内部模块，只返回实际的通道实现模块名。
    """
    import nanobot.channels as pkg

    return [
        name
        for _, name, ispkg in pkgutil.iter_modules(pkg.__path__)
        if name not in _INTERNAL and not ispkg
    ]


def load_channel_class(module_name: str) -> type[BaseChannel]:
    """导入module_name并返回找到的第一个BaseChannel子类。

    动态导入指定的通道模块并查找其中的通道实现类。如果找不到
    有效的BaseChannel子类则抛出ImportError。
    """
    from nanobot.channels.base import BaseChannel as _Base

    mod = importlib.import_module(f"nanobot.channels.{module_name}")
    for attr in dir(mod):
        obj = getattr(mod, attr)
        if isinstance(obj, type) and issubclass(obj, _Base) and obj is not _Base:
            return obj
    raise ImportError(f"No BaseChannel subclass in nanobot.channels.{module_name}")


def discover_plugins() -> dict[str, type[BaseChannel]]:
    """发现通过entry_points注册的外部通道插件。

    扫描nanobot.channels组的所有entry_points，动态加载插件通道。
    加载失败时记录警告但不中断发现流程，确保一个插件故障不影响
    其他插件的加载。
    """
    from importlib.metadata import entry_points

    plugins: dict[str, type[BaseChannel]] = {}
    for ep in entry_points(group="nanobot.channels"):
        try:
            cls = ep.load()
            plugins[ep.name] = cls
        except Exception as e:
            logger.warning("Failed to load channel plugin '{}': {}", ep.name, e)
    return plugins


def discover_all() -> dict[str, type[BaseChannel]]:
    """返回所有通道：内置（pkgutil）与外部（entry_points）的合并。

    内置通道具有优先权——外部插件不能遮蔽内置名称。这确保核心功能的
    稳定性，防止第三方插件意外覆盖系统通道。
    """
    builtin: dict[str, type[BaseChannel]] = {}
    for modname in discover_channel_names():
        try:
            builtin[modname] = load_channel_class(modname)
        except ImportError as e:
            logger.debug("Skipping built-in channel '{}': {}", modname, e)

    external = discover_plugins()
    shadowed = set(external) & set(builtin)
    if shadowed:
        logger.warning("Plugin(s) shadowed by built-in channels (ignored): {}", shadowed)

    return {**external, **builtin}

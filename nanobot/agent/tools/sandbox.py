"""Sandbox backends for shell command execution.

设计思路：
- _BACKENDS字典注册所有可用的沙箱后端
- 每个后端函数返回包装后的完整命令字符串
- bubblewrap（bwrap）后端创建隔离的文件系统环境
- workspace目录可读写，其他系统目录只读或隐藏

为什么需要这个模块：
- Shell执行可能破坏系统（删除文件、修改配置等）
- 沙箱隔离提供安全边界，防止意外破坏
- 只读绑定系统目录确保基本命令可用
"""

import shlex
from pathlib import Path

from nanobot.config.paths import get_media_dir


def _bwrap(command: str, workspace: str, cwd: str) -> str:
    """Wrap command in a bubblewrap sandbox (requires bwrap in container).

    Only the workspace is bind-mounted read-write; its parent dir (which holds
    config.json) is hidden behind a fresh tmpfs.  The media directory is
    bind-mounted read-only so exec commands can read uploaded attachments.
    """
    ws = Path(workspace).resolve()
    media = get_media_dir().resolve()

    try:
        sandbox_cwd = str(ws / Path(cwd).resolve().relative_to(ws))
    except ValueError:
        sandbox_cwd = str(ws)

    required  = ["/usr"]
    optional  = ["/bin", "/lib", "/lib64", "/etc/alternatives",
                 "/etc/ssl/certs", "/etc/resolv.conf", "/etc/ld.so.cache"]

    args = ["bwrap", "--new-session", "--die-with-parent"]
    for p in required: args += ["--ro-bind",     p, p]
    for p in optional: args += ["--ro-bind-try", p, p]
    args += [
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
        "--tmpfs", str(ws.parent),        # mask config dir
        "--dir", str(ws),                 # recreate workspace mount point
        "--bind", str(ws), str(ws),
        "--ro-bind-try", str(media), str(media),  # read-only access to media
        "--chdir", sandbox_cwd,
        "--", "sh", "-c", command,
    ]
    return shlex.join(args)


_BACKENDS = {"bwrap": _bwrap}


def wrap_command(sandbox: str, command: str, workspace: str, cwd: str) -> str:
    """Wrap *command* using the named sandbox backend."""
    if backend := _BACKENDS.get(sandbox):
        return backend(command, workspace, cwd)
    raise ValueError(f"Unknown sandbox backend {sandbox!r}. Available: {list(_BACKENDS)}")

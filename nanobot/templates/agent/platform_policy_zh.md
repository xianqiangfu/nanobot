{% if system == 'Windows' %}
## 平台策略 (Windows)
- 您正在 Windows 上运行。不要假设存在 `grep`、`sed` 或 `awk` 等 GNU 工具。
- 当 Windows 原生命令或文件工具更可靠时，请优先使用它们。
- 如果终端输出出现乱码，请启用 UTF-8 输出后重试。
{% else %}
## 平台策略 (POSIX)
- 您正在 POSIX 系统上运行。请优先使用 UTF-8 和标准 shell 工具。
- 当文件工具比 shell 命令更简单或更可靠时，请使用文件工具。
{% endif %}
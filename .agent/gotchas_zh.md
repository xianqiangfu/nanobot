# 常见陷阱

## 不要使用 `ruff format`

`CONTRIBUTING.md` 中提到了 `ruff format`，但**不要运行它**——它会破坏 git blame 历史。应该只使用 `ruff check`。

## 配置 `${VAR}` 引用

`config/loader.py` 在加载时会解析 `config.json` 中的 `${VAR}` 模式。这**不是**类似 shell 的默认值语法。如果环境变量缺失，`load_config` 会抛出 `ValueError`，代理会回退到默认配置。

有效的使用示例：
```json
{ "providers": { "openrouter": { "apiKey": "${OPENROUTER_KEY}" } } }
```

## Windows 兼容性

nanobot 明确支持 Windows。需要注意的关键差异：
- `ExecTool` 在 Windows 上使用 `cmd /c` 而不是 `sh -c`（`shell.py`）。
- `cli/commands.py` 在启动时强制将 `sys.stdout`/`stderr` 设置为 UTF-8，以处理表情符号和多语言输入。
- MCP stdio 服务器命令已针对 Windows 路径分隔符进行了规范化（`mcp.py`）。
- 始终使用 `pathlib.Path` 进行路径操作；不要假设使用 `/` 分隔符。

## 提示词模板

代理系统提示词和特定场景指令位于 `nanobot/templates/` 中，作为 Jinja2 markdown 文件（`identity.md`、`platform_policy.md`、`HEARTBEAT.md`、`SOUL.md` 等）。更改这些文件会像更改 Python 代码一样直接影响代理行为。它们由 `utils/prompt_templates.py` 加载。

工具描述、技能和重放的会话历史也会塑造模型行为。将这些表面的更改视为运行时代码：保持其范围狭窄，尽可能添加有针对性的回归测试，并避免教模型重复内部标记、本地路径或工具调用文本。

## 上下文污染会持续存在

任何写入内存、会话历史或提示词输入的内容都可以在未来的 LLM 调用中重放。必须对元数据（如时间戳、本地媒体路径、工具调用回显和原始回退转储）进行边界控制和清理，然后再将其作为模型模仿的示例。

## 心跳虚拟工具调用

心跳服务（`heartbeat/service.py`）不解析自由文本 LLM 输出。相反，它会向对话中注入一个带有 `action: skip | run` 的虚拟 `heartbeat` 工具。阶段 1 是结构化决策；阶段 2 仅在 `run` 时执行。添加新的定期后台检查时，应遵循此虚拟工具调用模式，而不是字符串匹配。

## 技能作为扩展点

内置技能位于 `nanobot/skills/` 中（markdown + YAML 前置元数据格式）。属于"知识"而非代码的代理能力应作为技能添加，而不是硬编码到代理循环中。外部技能可以发布到 ClawHub 并从中安装。

## 原子会话写入

`agent/memory.py` 以原子方式写入 `history.jsonl`（临时文件 + fsync + 重命名 + 目录 fsync）。这保证了崩溃时的持久性。不要将其替换为普通的 `open(..., "w")` 写入。
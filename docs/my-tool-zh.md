# My Tool

让代理能够感知和调整其自身的运行时状态 —— 就像问同事"你忙吗？能切换到更大的显示器吗？"

## 为什么需要它

普通工具让代理能够操作外部世界（读/写文件、搜索代码）。但代理对自己一无所知 —— 它不知道自己运行在哪个模型上、还剩多少次迭代，或者已经消耗了多少 token。

My tool 填补了这个空白。有了它，代理可以：

- **知道自己是谁**：我在使用什么模型？我的工作区在哪里？还剩多少次迭代？
- **实时调整**：复杂任务？扩大上下文窗口。简单聊天？切换到更快的模型。
- **跨轮次记忆**：在便签本中存储笔记，这些笔记会持续到下一个对话轮次。

## 配置

默认启用（只读模式）。代理可以检查其状态但不能设置。

```yaml
tools:
  my:
    enable: true       # 默认: true
    allow_set: false   # 默认: false（只读）
```

要允许代理设置其配置（例如切换模型、调整参数），请设置 `tools.my.allow_set: true`。

旧的 `tools.myEnabled` / `tools.mySet` 键在加载时会自动迁移，并在下一次 `nanobot onboard` 刷新配置时原地重写。

所有修改仅在内存中保存 —— 重启后会恢复默认值。

---

## check — 检查 "my" 的当前状态

不带参数时，返回关键的配置概览：

```text
my(action="check")
# → max_iterations: 40
#   context_window_tokens: 65536
#   model: 'anthropic/claude-sonnet-4-20250514'
#   workspace: PosixPath('/tmp/workspace')
#   provider_retry_mode: 'standard'
#   max_tool_result_chars: 16000
#   _current_iteration: 3
#   _last_usage: {'prompt_tokens': 45000, 'completion_tokens': 8000}
#   注意: prompt_tokens 是所有轮次的累计值，不是当前上下文窗口的占用。
```

带 key 参数时，深入查看特定配置：

```text
my(action="check", key="_last_usage.prompt_tokens")
# → 我已经使用了多少提示 token

my(action="check", key="model")
# → 我当前运行在什么模型上

my(action="check", key="web_config.enable")
# → 是否启用了网络搜索
```

### 你可以用它做什么

| 场景 | 方法 |
|----------|-----|
| "你在使用什么模型？" | `check("model")` |
| "你还能进行多少次工具调用？" | `check("max_iterations")` 减去 `check("_current_iteration")` |
| "这次对话已经使用了多少 token？" | `check("_last_usage")` — 所有轮次的累计值 |
| "你的工作目录在哪里？" | `check("workspace")` |
| "显示你的完整配置" | `check()` |
| "有子代理在运行吗？" | `check("subagents")` — 显示阶段、迭代、已用时间、工具事件 |

---

## set — 运行时调整

更改立即生效，无需重启。

```text
my(action="set", key="max_iterations", value=80)
# → 将迭代限制从 40 增加到 80

my(action="set", key="model", value="fast-model")
# → 切换到更快的模型

my(action="set", key="context_window_tokens", value=131072)
# → 为长文档扩大上下文窗口
```

你还可以在便签本中存储自定义状态：

```text
my(action="set", key="current_project", value="nanobot")
my(action="set", key="user_style_preference", value="concise")
my(action="set", key="task_complexity", value="high")
# → 这些值会持续到下一个对话轮次
```

### 受保护的参数

这些参数具有类型和范围验证 —— 无效值将被拒绝：

| 参数 | 类型 | 范围 | 用途 |
|-----------|------|-------|---------|
| `max_iterations` | int | 1–100 | 每个对话轮次的最大工具调用次数 |
| `context_window_tokens` | int | 4,096–1,000,000 | 上下文窗口大小 |
| `model` | str | 非空 | 要使用的 LLM 模型 |

其他参数（如 `workspace`、`provider_retry_mode`、`max_tool_result_chars`）可以自由设置，只要值是 JSON 安全的。

---

## 实际场景

### "这个任务很复杂，我需要更多空间"

```text
Agent: 这个代码库很大，让我扩大上下文窗口来处理它。
→ my(action="set", key="context_window_tokens", value=131072)
```

### "简单的问题，不要浪费计算"

```text
Agent: 这是一个直接的问题，让我切换到更快的模型。
→ my(action="set", key="model", value="fast-model")
```

### "跨轮次记住用户偏好"

```text
Turn 1: my(action="set", key="user_prefers_concise", value=True)
Turn 2: my(action="check", key="user_prefers_concise")
# → True（仍然记住用户喜欢简洁的回复）
```

### "自我诊断"

```text
User: "你为什么不在网上搜索？"
Agent: 让我检查我的网络配置。
→ my(action="check", key="web_config.enable")
# → False
Agent: 网络搜索已禁用 —— 请在你的配置中设置 web.enable: true。
```

### "Token 预算管理"

```text
Agent: 让我检查我还有多少预算。
→ my(action="check", key="_last_usage")
# → {"prompt_tokens": 45000, "completion_tokens": 8000}
Agent: 到目前为止我总共使用了约 53k token。我会保持剩余回复简洁。
```

### "子代理监控"

```text
Agent: 让我检查后台任务。
→ my(action="check", key="subagents")
# → 2 个子代理:
#   [task-1] '代码审查'
#     phase: running, iteration: 5, elapsed: 12.3s
#     tools: read(✓), grep(✓)
#     usage: {'prompt_tokens': 8000, 'completion_tokens': 1200}
#   [task-2] '编写测试'
#     phase: pending, iteration: 0, elapsed: 0.2s
#     tools: none
Agent: 代码审查进展良好。测试任务尚未开始。
```

---

## 安全机制

核心设计原则：**所有修改仅在内存中保存。重启后恢复默认值。** 代理无法造成持久性损害。

### 禁止访问（已阻止）

无法检查或修改 —— 完全隐藏：

| 类别 | 属性 | 原因 |
|----------|-----------|--------|
| 核心基础设施 | `bus`、`provider`、`_running` | 更改会使系统崩溃 |
| 工具注册表 | `tools` | 不能删除自己的工具 |
| 子系统 | `runner`、`sessions`、`consolidator` 等 | 影响其他用户/会话 |
| 敏感数据 | `_mcp_servers`、`_pending_queues` 等 | 包含凭据和消息路由 |
| 安全边界 | `restrict_to_workspace`、`channels_config` | 绕过会违反隔离 |
| Python 内部 | `__class__`、`__dict__` 等 | 防止沙箱逃逸 |

### 只读（仅检查）

可以检查但不能设置：

| 类别 | 属性 | 原因 |
|----------|-----------|--------|
| 子代理管理器 | `subagents` | 可观察，但替换会破坏系统 |
| 执行配置 | `exec_config` | 可以检查沙箱/启用状态，但不能更改 |
| 网络配置 | `web_config` | 可以检查启用状态，但不能更改 |
| 迭代计数器 | `_current_iteration` | 仅由 runner 更新 |

### 敏感字段保护

匹配敏感名称的子字段（`api_key`、`password`、`secret`、`token` 等）将被阻止检查和设置，无论父路径如何。这可以防止通过点路径遍历泄露凭据（例如 `web_config.search.api_key`）。
# 聊天内命令

这些命令在聊天频道和交互式代理会话中有效：

| 命令 | 描述 |
|---------|-------------|
| `/new` | 停止当前任务并开始新对话 |
| `/stop` | 停止当前任务 |
| `/restart` | 重启机器人 |
| `/status` | 显示机器人状态 |
| `/model` | 显示当前模型和可用模型预设 |
| `/model <preset>` | 切换后续对话轮次的运行时模型预设 |
| `/dream` | 立即运行 Dream 记忆整合 |
| `/dream-log` | 显示最新的 Dream 记忆更改 |
| `/dream-log <sha>` | 显示特定的 Dream 记忆更改 |
| `/dream-restore` | 列出最近的 Dream 记忆版本 |
| `/dream-restore <sha>` | 将记忆恢复到特定更改之前的状态 |
| `/help` | 显示可用的聊天内命令 |

## 模型预设

使用 `/model` 检查当前运行时模型：

```text
/model
```

响应会显示当前模型、当前预设和可用的预设名称。`default` 始终可用，代表来自 `agents.defaults.*` 的模型设置。

要为后续对话轮次切换预设：

```text
/model fast
/model deep
/model default
```

预设名称来自顶层的 `modelPresets` 配置。切换仅影响运行时：不会重写 `config.json`，正在进行的对话轮次将继续使用其启动时的模型。有关设置详情，请参阅 [配置：模型预设](./configuration.md#model-presets)。

## 定期任务

网关每 30 分钟唤醒一次并检查工作区（`~/.nanobot/workspace/HEARTBEAT.md`）中的 `HEARTBEAT.md`。如果文件包含任务，代理会执行它们并将结果发送到您最近活跃的聊天频道。

**设置：** 编辑 `~/.nanobot/workspace/HEARTBEAT.md`（由 `nanobot onboard` 自动创建）：

```markdown
## 定期任务

- [ ] 检查天气预报并发送摘要
- [ ] 扫描收件箱中的紧急邮件
```

代理也可以自行管理此文件 — 让它"添加定期任务"，它就会为您更新 `HEARTBEAT.md`。

> **注意：** 网关必须正在运行（`nanobot gateway`），并且您必须至少与机器人聊过一次，这样它才知道要将结果发送到哪个频道。
# 心跳服务

本模块提供周期性心跳唤醒功能，让智能体定期检查和处理任务。

## 核心组件

### HeartbeatService (`service.py`)

心跳服务，实现两个阶段：

1. **决策阶段** - 读取 HEARTBEAT.md 并询问 LLM 是否有活动任务
2. **执行阶段** - 如果决策返回 "run"，则执行任务

## 工作原理

### 阶段 1：决策

服务定期醒来，通过虚拟工具调用询问 LLM 是否有任务：

```python
_HEARTBEAT_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "heartbeat",
            "description": "报告心跳决策和任务摘要",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["skip", "run"],
                        "description": "skip = 无任务，run = 有活动任务"
                    },
                    "tasks": {
                        "type": "string",
                        "description": "活动任务的自然语言摘要（run 时必需）"
                    }
                },
                "required": ["action"]
            }
        }
    }
]
```

### 阶段 2：执行

只有当决策返回 `action: "run"` 时才执行任务。

## HEARTBEAT.md

在项目根目录创建 `HEARTBEAT.md` 文件来描述待办任务：

```markdown
# 心跳任务

## 待办事项

- [ ] 修复 Bug #123
- [ ] 审查 PR #456
- [ ] 更新文档

## 截止日期

- Bug 修复：2024-05-15
- PR 审查：2024-05-16
```

## API 示例

### 创建心跳服务

```python
from nanobot.heartbeat import HeartbeatService
from nanobot.providers import LLMProvider

provider = LLMProvider(...)
service = HeartbeatService(
    provider=provider,
    interval_minutes=30,  # 每 30 分钟检查一次
    heartbeat_file="HEARTBEAT.md"
)
```

### 注册执行回调

```python
async def execute_handler(tasks: str) -> str:
    """执行心跳检测到的任务。"""
    # 通过完整的 agent 循环执行任务
    return await run_agent_loop(tasks)

service.on_execute = execute_handler
```

### 启动服务

```python
# 启动心跳服务
await service.start()

# 停止服务
await service.stop()
```

## 配置选项

### interval_minutes

心跳间隔（分钟），默认 30 分钟：

```python
service = HeartbeatService(
    provider=provider,
    interval_minutes=60  # 每小时检查一次
)
```

### heartbeat_file

心跳任务文件路径，默认 `HEARTBEAT.md`：

```python
service = HeartbeatService(
    provider=provider,
    heartbeat_file="path/to/tasks.md"
)
```

## 使用场景

- **自动任务检查** - 定期检查是否有待办事项
- **提醒系统** - 定期提醒用户重要任务
- **监控服务** - 定期检查系统状态
- **批处理** - 定期执行批处理任务

## 执行流程

1. 定时器到期
2. 读取 HEARTBEAT.md
3. 调用 LLM，传递 HEARTBEAT.md 内容
4. LLM 决定是 "skip" 还是 "run"
5. 如果 "run"，调用 on_execute 回调
6. 等待下一个间隔

## 注意事项

- 心跳文件必须存在
- LLM 通过工具调用返回决策
- 执行阶段使用完整的 agent 循环
- 适合检查性和监控性任务
- 不适合需要实时响应的任务
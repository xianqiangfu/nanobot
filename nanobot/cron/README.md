# 定时任务服务

本模块提供定时任务调度和执行功能。

## 核心组件

### CronService (`service.py`)

定时任务服务，支持：

- 多种调度策略
- 任务执行历史
- 错误处理和重试
- 持久化存储

### Cron Types (`types.py`)

定时任务类型定义：

```python
class CronSchedule(TypedDict):
    kind: Literal["every", "at", "cron"]  # 调度类型
    every_ms: int | None                   # 间隔（毫秒）
    at_ms: int | None                      # 指定时间（毫秒）
    expr: str | None                       # Cron 表达式
    tz: str | None                         # 时区

class CronJob(TypedDict):
    id: str
    schedule: CronSchedule
    enabled: bool
    state: CronJobState

class CronRunRecord(TypedDict):
    job_id: str
    run_id: str
    started_at: int
    finished_at: int
    status: Literal["success", "failed", "skipped"]
    result: str | None
    error: str | None
```

## 调度策略

### Every - 间隔调度

每隔指定时间执行：

```python
schedule = {
    "kind": "every",
    "every_ms": 60000  # 每分钟
}
```

### At - 指定时间

在指定时间执行一次：

```python
schedule = {
    "kind": "at",
    "at_ms": 1715691600000  # 2024-05-14 10:00:00
}
```

### Cron - Cron 表达式

使用 Cron 表达式调度：

```python
schedule = {
    "kind": "cron",
    "expr": "0 10 * * *",  # 每天 10:00
    "tz": "Asia/Shanghai"  # 时区
}
```

## API 示例

### 创建定时任务

```python
from nanobot.cron import CronService

service = CronService(store_dir="~/.nanobot/cron")

# 创建任务
job = await service.create_job(
    id="daily_backup",
    schedule={
        "kind": "cron",
        "expr": "0 2 * * *",  # 每天凌晨 2 点
        "tz": "Asia/Shanghai"
    },
    enabled=True
)
```

### 注册执行回调

```python
async def backup_handler(job: CronJob) -> str:
    """执行备份。"""
    # 执行备份逻辑
    return "备份完成"

service.register_handler("daily_backup", backup_handler)
```

### 查询任务

```python
# 获取所有任务
jobs = await service.list_jobs()

# 获取特定任务
job = await service.get_job("daily_backup")

# 获取执行历史
runs = await service.get_job_runs("daily_backup", limit=10)
```

### 管理任务

```python
# 启用任务
await service.enable_job("daily_backup")

# 禁用任务
await service.disable_job("daily_backup")

# 删除任务
await service.delete_job("daily_backup")
```

### 启动服务

```python
# 启动定时任务服务
await service.start()

# 停止服务
await service.stop()
```

## 存储格式

任务数据存储在 `~/.nanobot/cron/` 目录：

```
~/.nanobot/cron/
├── jobs.json          # 任务定义
├── runs.json          # 执行历史
└── locks/             # 文件锁
```

## 执行流程

1. 定期检查任务调度
2. 找到到期的任务
3. 获取文件锁（防止并发执行）
4. 调用注册的处理器
5. 记录执行结果
6. 释放锁

## 错误处理

- 失败的任务会被记录
- 不自动重试（由调用者决定）
- 执行历史包含错误信息

## 注意事项

- 使用文件锁防止并发执行
- 支持分布式部署（通过文件锁协调）
- 执行历史自动轮转
- 所有操作都是异步的
# 命令路由系统

本模块提供斜杠命令（slash commands）的路由和分发功能。

## 核心组件

### CommandRouter (`router.py`)

命令路由器，支持多级命令分发：

- **priority** - 优先级命令，在分发锁前处理（如 `/stop`, `/restart`）
- **exact** - 精确匹配命令
- **prefix** - 前缀匹配（如 `/team `）
- **interceptors** - 拦截器，作为回退处理

### CommandContext

命令上下文，包含执行命令所需的所有信息：

```python
@dataclass
class CommandContext:
    msg: InboundMessage       # 入站消息
    session: Session | None   # 会话对象
    key: str                  # 会话键
    raw: str                  # 原始命令文本
    args: str = ""            # 命令参数
    loop: Any = None          # AgentLoop 引用
```

### Builtin Commands (`builtin.py`)

内置命令处理器。

## 内置命令

| 命令 | 描述 |
|------|------|
| `/new` | 停止当前任务并开始新对话 |
| `/stop` | 取消当前活动的智能体轮次 |
| `/restart` | 重启 nanobot 服务 |
| `/status` | 显示服务状态 |
| `/help` | 显示帮助信息 |
| `/models` | 列出可用模型 |
| `/preset` | 切换模型预设 |
| `/team` | 团队模式（多智能体协作） |

## 创建自定义命令

### 注册命令

```python
from nanobot.command import CommandRouter, CommandContext
from nanobot.bus.events import OutboundMessage

router = CommandRouter()

# 优先级命令
@router.priority("/stop")
async def stop_handler(ctx: CommandContext) -> OutboundMessage | None:
    """停止命令。"""
    # 停止当前任务
    return OutboundMessage(
        channel=ctx.msg.channel,
        session_key=ctx.key,
        content="已停止当前任务"
    )

# 精确匹配命令
@router.exact("/hello")
async def hello_handler(ctx: CommandContext) -> OutboundMessage | None:
    """打招呼命令。"""
    return OutboundMessage(
        channel=ctx.msg.channel,
        session_key=ctx.key,
        content="你好！"
    )

# 前缀匹配命令
@router.prefix("/echo ")
async def echo_handler(ctx: CommandContext) -> OutboundMessage | None:
    """回显命令。"""
    return OutboundMessage(
        channel=ctx.msg.channel,
        session_key=ctx.key,
        content=ctx.args
    )
```

### 拦截器

```python
@router.interceptor
async def team_mode_interceptor(ctx: CommandContext) -> OutboundMessage | None:
    """团队模式拦截器。"""
    if is_team_mode_active(ctx.key):
        # 重定向到团队模式处理
        return handle_team_command(ctx)
    return None
```

## 命令规范

### Handler 类型

```python
Handler = Callable[[CommandContext], Awaitable[OutboundMessage | None]]
```

### 返回值

- 返回 `OutboundMessage` - 发送响应
- 返回 `None` - 不发送响应

## 使用示例

### 集成到 AgentLoop

```python
from nanobot.command import CommandRouter, register_builtin_commands

# 创建路由器
router = CommandRouter()

# 注册内置命令
register_builtin_commands(router)

# 注册自定义命令
@router.exact("/mycommand")
async def my_handler(ctx: CommandContext) -> OutboundMessage | None:
    # 处理命令
    pass

# 在 AgentLoop 中使用
loop = AgentLoop(
    command_router=router
)
```

## 命令执行流程

1. 收到入站消息
2. 检查是否为命令（以 `/` 开头）
3. 优先检查 `priority` 命令
4. 获取分发锁
5. 检查 `exact` 命令
6. 检查 `prefix` 命令
7. 检查 `interceptors`
8. 执行匹配的 handler
9. 发送响应（如果有）

## 注意事项

- 命令名区分大小写
- 前缀匹配按最长前缀优先
- 拦截器按注册顺序执行
- 所有 handler 都是异步的
- 使用分发锁防止并发问题
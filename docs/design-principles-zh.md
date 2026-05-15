# nanobot 架构设计原理

本文档深入分析 nanobot 的核心架构设计原理和模式。

## 消息总线解耦模式

### 设计原理

消息总线（MessageBus）实现了聊天通道与智能体核心的完全解耦。这种解耦设计遵循生产者-消费者模式，通过异步队列实现松耦合。

### 核心组件

```python
class MessageBus:
    inbound: asyncio.Queue[InboundMessage]   # 通道 → 智能体
    outbound: asyncio.Queue[OutboundMessage] # 智能体 → 通道
```

### 优势分析

1. **独立扩展** - 通道和智能体可以独立扩展
2. **背压控制** - 队列提供缓冲，防止生产者压垮消费者
3. **故障隔离** - 通道故障不会直接影响智能体
4. **并发处理** - 支持多通道并发和智能体并发

### 工作流程

```
通道 → InboundMessage → inbound队列 → AgentLoop
AgentLoop → OutboundMessage → outbound队列 → ChannelManager → 通道
```

### 关键设计决策

- **双队列设计** - 入站和出站分离，避免死锁
- **无界队列** - 使用 asyncio.Queue 的无界模式，通过监控系统规模控制
- **阻塞消费** - 使用 `queue.get()` 阻塞等待，避免空转

## Agent 循环状态机设计

### 状态机模型

Agent 循环使用有限状态机（FSM）管理每个消息轮次的生命周期。

### 状态定义

```python
class TurnState(Enum):
    RESTORE = auto()   # 恢复会话
    COMPACT = auto()   # 自动压缩
    COMMAND = auto()   # 命令处理
    BUILD = auto()     # 构建上下文
    RUN = auto()       # 执行 LLM 调用
    SAVE = auto()      # 保存会话
    RESPOND = auto()   # 发送响应
    DONE = auto()      # 完成
```

### 状态流转

```
RESTORE → COMPACT → COMMAND → BUILD → RUN → SAVE → RESPOND → DONE
                    ↓
                 (命令?) → 处理命令 → DONE
```

### 关键设计原则

1. **单一职责** - 每个状态只做一件事
2. **线性推进** - 状态按顺序流转，避免回退
3. **错误隔离** - 每个状态独立处理错误
4. **可追踪性** - 记录状态转换和耗时

### 状态追踪

```python
@dataclass
class StateTraceEntry:
    state: TurnState
    started_at: float
    duration_ms: float
    event: str
    error: str | None = None
```

### 优化策略

- **短路跳转** - 某些条件下跳过非必要状态
- **并行处理** - 部分状态可以并行执行
- **缓存复用** - 重复请求复用之前的结果

## 通道插件化架构

### 设计原理

通道系统采用插件化架构，新通道通过继承 `BaseChannel` 类实现，无需修改核心代码。

### 扩展点

```python
class BaseChannel(ABC):
    name: str                    # 通道唯一标识
    display_name: str            # 显示名称
    
    async def login(self) -> bool: ...
    async def start(self) -> None: ...
    async def stop(self) -> None: ...
    async def send(self, msg: OutboundMessage) -> None: ...
    async def send_delta(self, delta: str) -> None: ...
```

### 发现机制

通道通过 `pkgutil` 扫描和 entry-point 插件两种方式发现：

1. **动态扫描** - 运行时扫描 `nanobot/channels/` 目录
2. **Entry-point** - 通过 `setup.py` 或 `pyproject.toml` 注册

### 管理策略

ChannelManager 负责通道的生命周期管理：

- **初始化** - 根据配置初始化启用的通道
- **启动/停止** - 协调所有通道的启动和停止
- **消息路由** - 将出站消息路由到正确的通道

### 设计约束

- **自包含** - 每个通道应该是自包含的
- **最小依赖** - 通道不应依赖其他通道
- **故障隔离** - 单个通道故障不影响其他通道

## 工具注册与发现机制

### 注册表设计

ToolRegistry 集中管理所有可用工具，提供统一的注册和查找接口。

### 注册流程

```python
registry = ToolRegistry()

# 注册工具
registry.register(FilesystemTool())
registry.register(ShellTool())
registry.register(WebTools())

# 获取工具
tool = registry.get("read_file")
definitions = registry.get_definitions()
```

### 缓存策略

- **定义缓存** - 工具定义（schema）被缓存
- **失效机制** - 注册/注销工具时失效缓存
- **稳定排序** - 内置工具按字母序，MCP 工具后置

### 发现机制

工具通过以下方式发现：

1. **内置工具** - 自动注册内置工具
2. **MCP 服务器** - 动态发现 MCP 工具
3. **Entry-point** - 通过插件注册自定义工具

### 工具命名

- **内置工具** - 简短、描述性名称（如 `read_file`）
- **MCP 工具** - 使用 `mcp_` 前缀避免冲突

## 会话隔离与共享策略

### 会话隔离

每个会话完全隔离，包括：

- **消息历史** - 每个会话独立的历史记录
- **工具上下文** - 每个会话独立的工具状态
- **元数据** - 每个会话独立的元数据

### 会话键设计

```
{channel}:{chat_id}
```

例如：
- `telegram:123456789` - Telegram 用户会话
- `discord:987654321` - Discord 用户会话
- `api:default` - API 默认会话

### 持久化策略

- **原子写入** - 使用 temp file + fsync + rename 模式
- **文件隔离** - 每个会话独立文件
- **自动轮转** - 单文件超过 2000 条消息自动轮转

### 共享资源

虽然会话隔离，但共享以下资源：

- **LLM 提供商** - 多会话共享同一个提供商实例
- **工具注册表** - 所有会话共享工具定义
- **配置** - 所有会话共享配置

## 内存合并 (Dream) 机制

### 两阶段合并

Dream 采用两阶段记忆合并策略：

### 阶段 1: 模式识别

识别重复和相似的模式：

```python
# 读取 MEMORY.md
memory_content = read_file("MEMORY.md")

# 询问 LLM 识别重复模式
patterns = await llm.complete([
    {"role": "system", "content": "识别重复模式"},
    {"role": "user", "content": memory_content}
])
```

### 阶段 2: 知识蒸馏

将模式合并为结构化知识：

```python
# 生成摘要
summary = await llm.complete([
    {"role": "system", "content": "生成知识摘要"},
    {"role": "user", "content": patterns}
])

# 写入 MEMORY.md
write_file("MEMORY.md", summary)
```

### 执行时机

- **定时执行** - 默认每 2 小时执行一次
- **批量处理** - 每批最多处理 20 条记录
- **Git 注释** - 可选地为每行添加 git-blame 年龄注释

### 设计目标

- **信息保留** - 保留关键信息，去除冗余
- **可读性** - 生成可读的摘要文档
- **可追溯性** - 保留来源信息

## 自动压缩 (AutoCompact) 策略

### 压缩触发条件

自动压缩在以下条件下触发：

- **Token 限制** - 会话历史超过配置的 token 阈值
- **消息数量** - 消息数量超过限制
- **时间限制** - 消息时间超过 TTL

### 压缩策略

#### 智能压缩

保留重要的历史消息：

```python
# 保留最近的消息
keep_recent = 50

# 保留包含关键信息的消息
keep_important = [
    msg for msg in messages
    if contains_tool_calls(msg) or contains_reasoning(msg)
]

# 压缩中间的消息
compressed = compress_messages(messages[keep_recent:-keep_recent])
```

#### 微压缩

在工具调用过多时进行微压缩：

- **限制工具结果** - 截断过长的工具结果
- **合并相似结果** - 合并重复的工具调用
- **保留关键信息** - 保留错误和异常信息

### 压缩算法

1. **计算优先级** - 为每条消息计算优先级
2. **选择保留** - 根据优先级选择保留的消息
3. **生成摘要** - 为被删除的消息生成摘要
4. **更新会话** - 更新会话历史

### 配置选项

```python
{
  "autoCompact": {
    "enabled": true,
    "thresholdTokens": 100000,
    "keepRecent": 50,
    "intervalHours": 24
  }
}
```

## 其他设计原理

### 幂等性设计

- **会话保存** - 多次保存会话结果一致
- **工具执行** - 相同参数的重复调用返回相同结果
- **消息发送** - 重复发送相同消息不影响状态

### 优雅降级

- **功能降级** - 非核心功能故障时降级而非失败
- **超时处理** - 操作超时时返回默认值而非错误
- **重试策略** - 可重试的操作自动重试

### 可观测性

- **日志记录** - 关键操作记录日志
- **指标收集** - 收集性能指标
- **追踪** - 支持分布式追踪

## 架构约束总结

来自 `.agent/design.md` 的核心约束：

1. **核心保持简洁** - 新功能在边缘扩展
2. **结构少一点，智能多一点** - 避免过早抽象
3. **优先重复而非过早抽象** - 通道和提供商允许重复逻辑
4. **最小化更改** - 只更改必要的代码
5. **保持 PR 可审查** - 单一焦点，清晰的变更
6. **显式优于魔法** - 配置显式声明
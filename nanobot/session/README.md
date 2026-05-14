# 会话管理

本模块负责管理对话会话和历史记录。

## 核心组件

### SessionManager (`manager.py`)

会话管理器，提供：

- 会话创建和获取
- 会话历史存储和检索
- 会话列表和元数据
- 会话 TTL 管理
- 自动会话压缩

### Session

会话数据结构：

```python
@dataclass
class Session:
    key: str                    # 会话唯一键
    created_at: int             # 创建时间（毫秒）
    updated_at: int             # 更新时间（毫秒）
    messages: list[dict]        # 消息历史
    metadata: dict[str, Any]    # 元数据
```

## 会话键

会话键用于标识和关联对话：

- 格式：`{channel}:{chat_id}` 或自定义格式
- 每个频道可以自定义键生成逻辑
- 键应该是唯一的和可预测的

## 消息存储

### 存储位置

会话数据存储在 `~/.nanobot/sessions/` 目录下：

```
~/.nanobot/sessions/
├── telegram:123456789/
│   └── session.json
├── discord:987654321/
│   └── session.json
└── sessions.json
```

### 消息格式

```json
{
  "role": "user|assistant|system",
  "content": "消息内容",
  "timestamp": 1234567890000
}
```

### 存储限制

- 每个文件最多存储 2000 条消息
- 超过限制时创建新文件
- 支持消息旋转和压缩

## 会话压缩

### 自动压缩

会话可以配置自动压缩，基于：

- 消息数量
- Token 使用量
- 时间 TTL

### 压缩策略

```json
{
  "autoCompact": {
    "enabled": true,
    "thresholdTokens": 100000,
    "keepRecent": 50,
    "intervalHours": 24
  }
}
```

## 会话 TTL

支持会话过期清理：

```json
{
  "session": {
    "ttlDays": 30
  }
}
```

## API 示例

```python
from nanobot.session import SessionManager

# 创建会话管理器
manager = SessionManager(
    sessions_dir="~/.nanobot/sessions",
    ttl_days=30
)

# 获取或创建会话
session = await manager.get_or_create(
    key="telegram:123456789",
    metadata={"user": "username"}
)

# 添加消息
await manager.add_message(
    session.key,
    {"role": "user", "content": "你好"}
)

# 获取会话历史
history = await manager.get_messages(session.key)

# 列出所有会话
sessions = await manager.list_sessions()

# 删除会话
await manager.delete_session(session.key)
```

## 会话预览

```python
# 获取会话预览信息
preview = await manager.get_session_preview(session.key)
# preview: {"key": "...", "preview": "...", "created_at": ...}
```

## 注意事项

- 所有会话操作都是异步的
- 会话数据持久化到磁盘
- 使用 fsync 确保数据安全
- 支持并发访问和更新
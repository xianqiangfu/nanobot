# Session 数据结构

```mermaid
classDiagram
    class Session {
        +str key
        +list messages
        +datetime created_at
        +datetime updated_at
        +dict metadata
        +int last_consolidated
        +dict state
    }

    class SessionManager {
        +str sessions_dir
        +int ttl_days
        +create_session()
        +get_session()
        +add_message()
        +update_session()
        +delete_session()
        +list_sessions()
    }

    class Message {
        +str role
        +str content
        +list content_blocks
        +dict tool_calls
        +list tool_results
        +float timestamp
        +dict metadata
    }

    class ContentBlock {
        +str type
        +str text
        +dict image_url
        +str reasoning
    }

    class ToolCall {
        +str id
        +str name
        +dict arguments
        +str extra_content
    }

    class ToolResult {
        +str tool_call_id
        +str content
        +bool is_error
        +dict metadata
    }

    SessionManager "1" --> "1..*" Session
    Session "1" --> "*" Message
    Message "1" --> "*" ContentBlock
    Message "1" --> "*" ToolCall
    Message "1" --> "*" ToolResult
    ToolResult --> ToolCall
```

## 字段说明

### Session

| 字段 | 类型 | 说明 |
|------|------|------|
| `key` | str | 会话唯一键 (格式: `{channel}:{chat_id}`) |
| `messages` | list | 消息历史列表 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |
| `metadata` | dict | 元数据 (用户信息、标签等) |
| `last_consolidated` | int | 最后巩固的消息索引 |
| `state` | dict | 运行时状态 |

### Message

| 字段 | 类型 | 说明 |
|------|------|------|
| `role` | str | 角色 (user/assistant/system) |
| `content` | str | 文本内容 |
| `content_blocks` | list | 内容块 (多模态) |
| `tool_calls` | list | 工具调用列表 |
| `tool_results` | list | 工具结果列表 |
| `timestamp` | float | 时间戳 |
| `metadata` | dict | 元数据 |

### ContentBlock

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | str | 类型 (text/image/reasoning) |
| `text` | str | 文本内容 |
| `image_url` | dict | 图片信息 |
| `reasoning` | str | 推理内容 |
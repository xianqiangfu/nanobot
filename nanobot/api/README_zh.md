# API 服务

本模块提供 OpenAI 兼容的 HTTP API 服务器，用于固定的 nanobot 会话。

## 核心功能

### 端点

- `POST /v1/chat/completions` - OpenAI 兼容的聊天完成端点
- `GET /v1/models` - 列出可用模型

### 会话管理

所有请求路由到单个持久化的 API 会话：

- 会话键：`api:default`
- 聊天 ID：`default`

## 使用示例

### 聊天完成

```bash
curl -X POST http://localhost:8765/api/v1/chat/completions \n  -H "Content-Type: application/json" \n  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "你好！"}
    ]
  }'
```

### 列出模型

```bash
curl http://localhost:8765/api/v1/models
```

### 文件上传

```bash
curl -X POST http://localhost:8765/api/v1/chat/completions \n  -H "Content-Type: application/json" \n  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "这是什么图片？"},
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,/9j/4AAQ..."
            }
          }
        ]
      }
    ]
  }'
```

## 配置

### 端口

API 服务默认在端口 8765 上运行。

### 会话配置

API 会话使用与 nanobot 配置相同的设置：
- 提供商配置
- 工具配置
- 智能体配置

## 响应格式

### 成功响应

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1715691600,
  "model": "claude-3-5-sonnet-20241022",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！有什么可以帮助你的？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### 错误响应

```json
{
  "error": {
    "message": "Invalid request",
    "type": "invalid_request_error",
    "code": 400
  }
}
```

## 注意事项

- 所有请求异步处理
- 支持流式响应
- 文件大小限制：MAX_FILE_SIZE
- 文件存储在媒体目录中
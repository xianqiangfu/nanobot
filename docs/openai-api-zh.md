# OpenAI 兼容 API

nanobot 可以为本地集成提供一个最小的 OpenAI 兼容端点：

```bash
pip install "nanobot-ai[api]"
nanobot serve
```

默认情况下，API 绑定到 `127.0.0.1:8900`。您可以在 `config.json` 中更改此设置。

## 行为

- **会话隔离**：在请求体中传递 `"session_id"` 以隔离对话；如果省略，则使用共享的默认会话（`api:default`）
- **单消息输入**：每个请求必须恰好包含一条 `user` 消息
- **固定模型**：省略 `model`，或者传递与 `/v1/models` 显示的相同的模型
- **流式传输**：设置 `stream=true` 以接收带有 OpenAI 兼容增量块的 Server-Sent Events（`text/event-stream`），以 `data: [DONE]` 结尾；省略或设置 `stream=false` 以获取单个 JSON 响应
- **文件上传**：支持通过 JSON base64 或 `multipart/form-data` 上传图片、PDF、Word（.docx）、Excel（.xlsx）、PowerPoint（.pptx）（每个文件最大 10MB）
- API 请求在合成的 `api` 通道中运行，因此 `message` 工具**不会**自动发送到 Telegram/Discord 等。要主动发送到其他聊天，请调用 `message` 并为启用的通道指定显式的 `channel` 和 `chat_id`。

从 API 会话进行跨通道传递的工具调用示例：

```json
{
  "content": "构建成功完成。",
  "channel": "telegram",
  "chat_id": "123456789"
}
```

如果 `channel` 指向您的配置中未启用的通道，nanobot 将排队等待出站事件，但不会发生平台传递。

## 端点

- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`

## curl

```bash
curl http://127.0.0.1:8900/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "你好"}],
    "session_id": "my-session"
  }'
```

## 文件上传（JSON base64）

使用 OpenAI 多模态内容格式内联发送图片：

```bash
curl http://127.0.0.1:8900/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": [
      {"type": "text", "text": "描述这张图片"},
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,iVBOR..."}}
    ]}]
  }'
```

## 文件上传（multipart/form-data）

通过 multipart 上传任何支持的文件类型（图片、PDF、Word、Excel、PPT）：

```bash
# 单个文件
curl http://127.0.0.1:8900/v1/chat/completions \
  -F "message=总结这份报告" \
  -F "files=@report.docx"

# 多个文件与会话隔离
curl http://127.0.0.1:8900/v1/chat/completions \
  -F "message=比较这些文件" \
  -F "files=@chart.png" \
  -F "files=@data.xlsx" \
  -F "session_id=my-session"
```

支持的文件类型：
- **图片**：PNG、JPEG、GIF、WebP（作为 base64 发送给 AI 进行视觉分析）
- **文档**：PDF、Word（.docx）、Excel（.xlsx）、PowerPoint（.pptx）（提取文本并发送给 AI）
- **文本**：TXT、Markdown、CSV、JSON 等（直接读取）

## Python (`requests`)

```python
import requests

resp = requests.post(
    "http://127.0.0.1:8900/v1/chat/completions",
    json={
        "messages": [{"role": "user", "content": "你好"}],
        "session_id": "my-session",  # 可选：隔离对话
    },
    timeout=120,
)
resp.raise_for_status()
print(resp.json()["choices"][0]["message"]["content"])
```

## Python (`openai`)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8900/v1",
    api_key="dummy",
)

resp = client.chat.completions.create(
    model="MiniMax-M2.7",
    messages=[{"role": "user", "content": "你好"}],
    extra_body={"session_id": "my-session"},  # 可选：隔离对话
)
print(resp.choices[0].message.content)
```
# WebSocket 服务器通道

Nanobot 可以充当 WebSocket 服务器,允许外部客户端(网页应用、CLI、脚本)通过持久连接与代理进行实时交互。

## 功能特性

- 通过 WebSocket 进行双向实时通信
- 流式传输支持 — 逐个 token 接收代理响应
- 基于令牌的身份验证(静态令牌和短期颁发的令牌)
- 多会话多路复用 — 一个连接可以运行多个并发的 `chat_id`
- 支持 TLS/SSL (WSS),强制要求最低 TLSv1.2 版本
- 通过 `allowFrom` 实现客户端白名单
- 自动清理失效连接

## 快速开始

### 1. 配置

在 `config.json` 的 `channels.websocket` 下添加:

```json
{
  "channels": {
    "websocket": {
      "enabled": true,
      "host": "127.0.0.1",
      "port": 8765,
      "path": "/",
      "websocketRequiresToken": false,
      "allowFrom": ["*"],
      "streaming": true
    }
  }
}
```

### 2. 启动 nanobot

```bash
nanobot gateway
```

您应该会看到:

```text
WebSocket server listening on ws://127.0.0.1:8765/
```

### 3. 连接客户端

```bash
# 使用 websocat
websocat ws://127.0.0.1:8765/?client_id=alice

# 使用 Python
import asyncio, json, websockets

async def main():
    async with websockets.connect("ws://127.0.0.1:8765/?client_id=alice") as ws:
        ready = json.loads(await ws.recv())
        print(ready)  # {"event": "ready", "chat_id": "...", "client_id": "alice"}
        await ws.send(json.dumps({"content": "Hello nanobot!"}))
        reply = json.loads(await ws.recv())
        print(reply["text"])

asyncio.run(main())
```

## 连接 URL

```text
ws://{host}:{port}{path}?client_id={id}&token={token}
```

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `client_id` | 否 | 用于 `allowFrom` 授权的标识符。如果省略,将自动生成为 `anon-xxxxxxxxxxxx`。最多截断到 128 个字符。 |
| `token` | 条件 | 身份验证令牌。当 `websocketRequiresToken` 为 `true` 或配置了 `token`(静态密钥)时必需。 |

## 线路协议

所有帧都是 JSON 文本。每条消息都有一个 `event` 字段。

### 服务器 → 客户端

**`ready`** — 连接建立后立即发送:

```json
{
  "event": "ready",
  "chat_id": "uuid-v4",
  "client_id": "alice"
}
```

**`message`** — 完整的代理响应:

```json
{
  "event": "message",
  "chat_id": "uuid-v4",
  "text": "Hello! How can I help?",
  "media": ["/tmp/image.png"],
  "reply_to": "msg-id"
}
```

`media` 和 `reply_to` 仅在适用时出现。

**`delta`** — 流式文本块(仅当 `streaming: true` 时):

```json
{
  "event": "delta",
  "chat_id": "uuid-v4",
  "text": "Hello",
  "stream_id": "s1"
}
```

**`stream_end`** — 标记流式传输段的结束:

```json
{
  "event": "stream_end",
  "chat_id": "uuid-v4",
  "stream_id": "s1"
}
```

**`reasoning_delta`** — 当前助手轮次的增量模型推理/思考块。镜像 `delta`,但针对答案上方的推理气泡而不是答案正文:

```json
{
  "event": "reasoning_delta",
  "chat_id": "uuid-v4",
  "text": "Let me decompose ",
  "stream_id": "r1"
}
```

**`reasoning_end`** — 当前推理流的关闭标记。WebUI 使用此事件来锁定原位气泡,并从闪烁的头部切换到静态折叠状态:

```json
{
  "event": "reasoning_end",
  "chat_id": "uuid-v4",
  "stream_id": "r1"
}
```

仅当通道的 `showReasoning` 为 `true`(默认)且模型返回推理内容时(DeepSeek-R1 / Kimi / MiMo / OpenAI 推理模型、Anthropic 扩展思考或内联 `````` / `<thought>` 标签),推理帧才会流动。没有推理的模型产生零个 `reasoning_delta` 帧。

**`runtime_model_updated`** — 当网关运行时模型更改时广播,例如在 `/model <preset>` 之后:

```json
{
  "event": "runtime_model_updated",
  "model_name": "openai/gpt-4.1-mini",
  "model_preset": "fast"
}
```

当没有激活的命名预设时,`model_preset` 被省略。WebUI 客户端使用此事件在斜杠命令、配置重新加载和设置更改之间保持显示的模型徽章同步。

**`attached`** — 确认 `new_chat` / `attach` 入站信封(参见[多会话多路复用](#多会话多路复用)):

```json
{"event": "attached", "chat_id": "uuid-v4"}
```

**`error`** — 格式错误的入站信封的软错误。连接保持打开:

```json
{"event": "error", "detail": "invalid chat_id"}
```

### 客户端 → 服务器

**传统(默认会话):** 发送纯字符串,或包含可识别文本字段的 JSON 对象:

```json
"Hello nanobot!"
```

```json
{"content": "Hello nanobot!"}
```

可识别的字段:`content`、`text`、`message`(按该顺序检查)。无效的 JSON 被视为纯文本。这些帧路由到连接的默认 `chat_id`(在 `ready` 中宣布的那个)。

**类型化信封(多会话):** 任何带有字符串 `type` 字段的 JSON 对象都是类型化信封:

| `type` | 字段 | 效果 |
|--------|--------|--------|
| `new_chat` | — | 服务器创建一个新的 `chat_id`,订阅此连接,用 `attached` 回复。 |
| `attach` | `chat_id` | 订阅现有的 `chat_id`(例如页面重新加载后)。用 `attached` 回复。 |
| `message` | `chat_id`, `content` | 在 `chat_id` 上发送 `content`。首次使用自动附加;无需显式 `attach`。 |

有关完整流程,请参见[多会话多路复用](#多会话多路复用)。

## 配置参考

所有字段都位于 `config.json` 的 `channels.websocket` 下。

### 连接

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `enabled` | bool | `false` | 启用 WebSocket 服务器。 |
| `host` | string | `"127.0.0.1"` | 绑定地址。使用 `"0.0.0.0"` 接受外部连接。 |
| `port` | int | `8765` | 监听端口。 |
| `path` | string | `"/"` | WebSocket 升级路径。尾部斜杠被规范化(根 `/` 被保留)。 |
| `maxMessageBytes` | int | `37748736` | 入站消息的最大字节大小(1 KB – 40 MB)。默认值(36 MB)的大小可接受最多 4 个 base64 编码的图像附件,每个 8 MB;如果通道仅传输文本,请降低此值。 |

### 身份验证

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `token` | string | `""` | 静态共享密钥。设置后,客户端必须提供与此密钥匹配的 `?token=<value>`(时序安全比较)。颁发的令牌也作为后备被接受。 |
| `websocketRequiresToken` | bool | `true` | 当为 `true` 且未配置静态 `token` 时,客户端仍必须提供有效的颁发令牌。设置为 `false` 以允许未经身份验证的连接(仅对本地/受信任网络安全)。 |
| `tokenIssuePath` | string | `""` | 用于颁发短期令牌的 HTTP 路径。必须与 `path` 不同。参见[令牌颁发](#令牌颁发)。 |
| `tokenIssueSecret` | string | `""` | 通过颁发端点获取令牌所需的密钥。如果为空,任何客户端都可以获取令牌(记录为警告)。 |
| `tokenTtlS` | int | `300` | 颁发令牌的生存时间(秒)(30 – 86,400)。 |

### 访问控制

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `allowFrom` | 字符串列表 | `["*"]` | 允许的 `client_id` 值。`"*"` 允许所有;`[]` 拒绝所有。 |

### 流式传输

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `streaming` | bool | `true` | 启用流式传输模式。代理发送 `delta` + `stream_end` 帧而不是单个 `message`。 |

### 保活

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `pingIntervalS` | float | `20.0` | WebSocket ping 间隔(秒)(5 – 300)。 |
| `pingTimeoutS` | float | `20.0` | 在关闭连接之前等待 pong 的时间(秒)(5 – 300)。 |

### TLS/SSL

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `sslCertfile` | string | `""` | TLS 证书文件的路径 (PEM)。必须同时设置 `sslCertfile` 和 `sslKeyfile` 才能启用 WSS。 |
| `sslKeyfile` | string | `""` | TLS 私钥文件的路径 (PEM)。强制要求最低 TLS 版本为 TLSv1.2。 |

## 令牌颁发

对于 `websocketRequiresToken: true` 的生产部署,使用短期令牌而不是在客户端中嵌入静态密钥。

### 工作原理

1. 客户端发送 `GET {tokenIssuePath}` 并附带 `Authorization: Bearer {tokenIssueSecret}` (或 `X-Nanobot-Auth` 头部)。
2. 服务器响应一次性令牌:

```json
{"token": "nbwt_aBcDeFg...", "expires_in": 300}
```

3. 客户端使用 `?token=nbwt_aBcDeFg...&client_id=...` 打开 WebSocket。
4. 令牌被消耗(单次使用),无法重复使用。

### 示例设置

```json
{
  "channels": {
    "websocket": {
      "enabled": true,
      "port": 8765,
      "path": "/ws",
      "tokenIssuePath": "/auth/token",
      "tokenIssueSecret": "your-secret-here",
      "tokenTtlS": 300,
      "websocketRequiresToken": true,
      "allowFrom": ["*"],
      "streaming": true
    }
  }
}
```

客户端流程:

```bash
# 1. 获取令牌
curl -H "Authorization: Bearer your-secret-here" http://127.0.0.1:8765/auth/token

# 2. 使用令牌连接
websocat "ws://127.0.0.1:8765/ws?client_id=alice&token=nbwt_aBcDeFg..."
```

### 限制

- 颁发的令牌是单次使用的 — 每个令牌只能完成一次握手。
- 未完成的令牌上限为 10,000 个。超过此数量的请求返回 HTTP 429。
- 过期的令牌在每次颁发或验证请求时被延迟清除。

## 多会话多路复用

单个 WebSocket 可以承载多个并发会话。服务器将 `chat_id -> {connections}` 跟踪为扇出集,因此同一会话也可以跨多个连接镜像(例如两个浏览器选项卡)。

### 典型流程(带有侧边栏的 Web UI)

```text
客户端                                服务器
  | --- 连接 -------------------->  |
  | <-- {"event":"ready",              |
  |      "chat_id":"d3..."}   (默认)  |
  |                                     |
  | --- {"type":"new_chat"} --------->  |
  | <-- {"event":"attached",            |
  |      "chat_id":"a1..."}             |
  |                                     |
  | --- {"type":"message",              |
  |      "chat_id":"a1...",             |
  |      "content":"hi"} ------------>  |
  | <-- {"event":"delta", ...}          |
  | <-- {"event":"stream_end", ...}     |
  |                                     |
  | --- {"type":"attach",               |  # 页面重新加载后
  |      "chat_id":"a1..."} --------->  |
  | <-- {"event":"attached", ...}       |
```

### 规则

- 每个出站事件都携带 `chat_id`。客户端必须按该字段分发。
- `chat_id` 格式:`^[A-Za-z0-9_:-]{1,64}$`。不匹配的值返回 `error`。
- `message` 在首次使用时自动附加 — 对于服务器在同一连接上创建的会话(`new_chat`),无需单独的 `attach`。
- 错误(无效信封、未知 `type`、错误的 `chat_id`)是软错误:服务器用 `{"event":"error","detail":"..."}` 回复并保持连接打开。

### 向后兼容性

仅发送纯文本或 `{"content": ...}` 的传统客户端可以继续正常工作:这些帧路由到连接的默认 `chat_id`(来自 `ready` 的那个)。无需配置标志。

### 安全边界

`chat_id` 是一个*能力(capability)*:任何持有有效 WebSocket 身份验证凭据和 chat_id 的人都可以附加到该对话并查看其输出。这对于 nanobot 的本地单用户模型是安全的。多租户部署应该按用户命名空间 chat_ids(或引入每个租户的身份验证网关) — nanobot 目前不这样做。

## 安全说明

- **时序安全比较**: 静态令牌验证使用 `hmac.compare_digest` 以防止时序攻击。
- **深度防御**: `allowFrom` 在 HTTP 握手级别和消息级别都进行检查。
- **chat_id 作为能力**: 参见[多会话多路复用](#多会话多路复用)。WebSocket 握手上的身份验证是唯一的防线;通过它的调用者可以附加到他们知道的任何 chat_id。
- **TLS 强制执行**: 启用 SSL 时,TLSv1.2 是允许的最低版本。
- **默认安全**: `websocketRequiresToken` 默认为 `true`。仅在受信任网络上显式设置为 `false`。

## 媒体文件

出站 `message` 事件可能包含本地文件系统路径的 `media` 字段。远程客户端无法直接访问这些文件 — 它们需要以下任一选项:

- 共享文件系统挂载,或
- 为 nanobot 媒体目录提供服务的 HTTP 文件服务器

## 常见模式

### 受信任的本地网络(无需身份验证)

```json
{
  "channels": {
    "websocket": {
      "enabled": true,
      "host": "0.0.0.0",
      "port": 8765,
      "websocketRequiresToken": false,
      "allowFrom": ["*"],
      "streaming": true
    }
  }
}
```

### 静态令牌(简单身份验证)

```json
{
  "channels": {
    "websocket": {
      "enabled": true,
      "token": "my-shared-secret",
      "allowFrom": ["alice", "bob"]
    }
  }
}
```

客户端使用 `?token=my-shared-secret&client_id=alice` 连接。

### 具有颁发令牌的公共端点

```json
{
  "channels": {
    "websocket": {
      "enabled": true,
      "host": "0.0.0.0",
      "port": 8765,
      "path": "/ws",
      "tokenIssuePath": "/auth/token",
      "tokenIssueSecret": "production-secret",
      "websocketRequiresToken": true,
      "sslCertfile": "/etc/ssl/certs/server.pem",
      "sslKeyfile": "/etc/ssl/private/server-key.pem",
      "allowFrom": ["*"]
    }
  }
}
```

### 自定义路径

```json
{
  "channels": {
    "websocket": {
      "enabled": true,
      "path": "/chat/ws",
      "allowFrom": ["*"]
    }
  }
}
```

客户端连接到 `ws://127.0.0.1:8765/chat/ws?client_id=...`。尾部斜杠被规范化,因此 `/chat/ws/` 工作方式相同。
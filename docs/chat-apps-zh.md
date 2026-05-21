# 聊天应用

将 nanobot 连接到您喜欢的聊天平台。想构建自己的平台吗？请参阅 [通道插件指南](./channel-plugin-guide.md)。

| 通道 | 所需内容 |
|---------|---------------|
| **Telegram** | 来自 @BotFather 的 Bot Token |
| **Discord** | Bot Token + 消息内容意图 |
| **WhatsApp** | 扫描二维码 (`nanobot channels login whatsapp`) |
| **WeChat (微信)** | 扫描二维码 (`nanobot channels login weixin`) |
| **Feishu (飞书)** | App ID + App Secret |
| **DingTalk (钉钉)** | App Key + App Secret |
| **Slack** | Bot Token + 应用级 Token |
| **Matrix** | 主服务器 URL + 访问令牌 |
| **Email (邮件)** | IMAP/SMTP 凭证 |
| **QQ** | App ID + App Secret |
| **Wecom (企业微信)** | Bot ID + Bot Secret |
| **Microsoft Teams** | App ID + App Password + 公共 HTTPS 端点 |
| **Mochat** | Claw Token (支持自动设置) |

<details>
<summary><b>Telegram</b> (推荐)</summary>

**1. 创建 Bot**
- 打开 Telegram，搜索 `@BotFather`
- 发送 `/newbot`，按照提示操作
- 复制 Token

**2. 配置**

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

> 您可以在 Telegram 设置中找到您的 **用户 ID**。它显示为 `@yourUserId`。
> 复制此值时**不要包含 `@` 符号**，并将其粘贴到配置文件中。


**3. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Mochat (Claw IM)</b></summary>

默认使用 **Socket.IO WebSocket**，HTTP 轮询作为后备。

**1. 让 nanobot 为您设置 Mochat**

只需向 nanobot 发送此消息（将 `xxx@xxx` 替换为您的真实邮箱）：

```
Read https://raw.githubusercontent.com/HKUDS/MoChat/refs/heads/main/skills/nanobot/skill.md and register on MoChat. My Email account is xxx@xxx Bind me as your owner and DM me on MoChat.
```

nanobot 将自动注册、配置 `~/.nanobot/config.json`，并连接到 Mochat。

**2. 重启网关**

```bash
nanobot gateway
```

就这样 — nanobot 会处理其余部分！

<br>

<details>
<summary>手动配置（高级）</summary>

如果您更喜欢手动配置，请将以下内容添加到 `~/.nanobot/config.json`：

> 请妥善保管 `claw_token`。它应该只在 `X-Claw-Token` 请求头中发送到您的 Mochat API 端点。

```json
{
  "channels": {
    "mochat": {
      "enabled": true,
      "base_url": "https://mochat.io",
      "socket_url": "https://mochat.io",
      "socket_path": "/socket.io",
      "claw_token": "claw_xxx",
      "agent_user_id": "6982abcdef",
      "sessions": ["*"],
      "panels": ["*"],
      "reply_delay_mode": "non-mention",
      "reply_delay_ms": 120000
    }
  }
}
```



</details>

</details>

<details>
<summary><b>Discord</b></summary>

**1. 创建 Bot**
- 访问 https://discord.com/developers/applications
- 创建应用程序 → Bot → 添加 Bot
- 复制 Bot Token

**2. 启用意图**
- 在 Bot 设置中，启用 **消息内容意图 (MESSAGE CONTENT INTENT)**
- （可选）如果您计划使用基于成员数据的允许列表，启用 **服务器成员意图 (SERVER MEMBERS INTENT)**

**3. 获取您的用户 ID**
- Discord 设置 → 高级 → 启用 **开发者模式**
- 右键点击您的头像 → **复制用户 ID**

**4. 配置**

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"],
      "allowChannels": [],
      "groupPolicy": "mention",
      "streaming": true
    }
  }
}
```

> `groupPolicy` 控制 Bot 在群组频道中的响应方式：
> - `"mention"`（默认）— 仅在被 @ 提及时响应
> - `"open"` — 响应所有消息
> 私信中，只要发送者在 `allowFrom` 中，Bot 总是响应。
> - 如果您将群组策略设置为 open，创建新线程时请将其设为私有线程，然后在其中 @ Bot。否则，线程本身及其所在的频道都会触发 Bot 会话。
> `allowChannels` 将 Bot 限制为特定的 Discord 频道 ID。空值（默认）表示在 Bot 可见的每个频道中响应。例如：`["1234567890", "0987654321"]`。该过滤在 `allowFrom` 之后应用，因此两者都必须通过。允许的父频道下的 Discord 线程也会被允许；对于论坛频道，允许父论坛频道即允许该论坛中的所有线程/帖子。
> `streaming` 默认为 `true`。仅在您明确想要非流式响应时才禁用它。

**5. 邀请 Bot**
- OAuth2 → URL 生成器
- 范围：`bot`
- Bot 权限：`Send Messages`、`Read Message History`
- 打开生成的邀请 URL 并将 Bot 添加到您的服务器

**6. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Matrix (Element)</b></summary>

首先安装 Matrix 依赖：

```bash
pip install nanobot-ai[matrix]
```

> [!NOTE]
> Matrix 在 Windows 上不支持。`matrix-nio[e2e]` 依赖于
> `python-olm`，该库没有预构建的 Windows wheel，并且会被
> `matrix` 额外包在 `sys_platform == 'win32'` 时跳过。上述命令在
> Windows 上仍然会成功，但不会安装 `matrix-nio`，因此启用 Matrix
> 通道将在启动时失败。请使用 macOS、Linux 或 WSL2。

**1. 创建/选择 Matrix 账户**

- 在您的主服务器上创建或重用 Matrix 账户（例如 `matrix.org`）。
- 确认您可以使用 Element 登录。

**2. 获取凭证**

- 您需要：
  - `userId`（例如：`@nanobot:matrix.org`）
  - `password`（密码）

（注意：出于遗留原因，仍然支持 `accessToken` 和 `deviceId`，但
为了可靠的加密，建议改用密码登录。如果提供了
`password`，`accessToken` 和 `deviceId` 将被忽略。）

**3. 配置**

```json
{
  "channels": {
    "matrix": {
      "enabled": true,
      "homeserver": "https://matrix.org",
      "userId": "@nanobot:matrix.org",
      "password": "mypasswordhere",
      "e2eeEnabled": true,
      "allowFrom": ["@your_user:matrix.org"],
      "groupPolicy": "open",
      "groupAllowFrom": [],
      "allowRoomMentions": false,
      "maxMediaBytes": 20971520
    }
  }
}
```

> 保持 `matrix-store` 持久化 — 如果这些在重启之间发生变化，加密的会话状态将丢失。

| 选项 | 描述 |
|--------|-------------|
| `allowFrom` | 允许交互的用户 ID。空值拒绝所有；使用 `["*"]` 允许所有人。 |
| `groupPolicy` | `open`（默认）、`mention` 或 `allowlist`。 |
| `groupAllowFrom` | 房间允许列表（当策略为 `allowlist` 时使用）。 |
| `allowRoomMentions` | 在提及模式下接受 `@room` 提及。 |
| `e2eeEnabled` | 端到端加密支持（默认 `true`）。设置为 `false` 以仅使用明文。 |
| `maxMediaBytes` | 最大附件大小（默认 `20MB`）。设置为 `0` 以阻止所有媒体。 |




**4. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>WhatsApp</b></summary>

需要 **Node.js ≥18**。

**1. 链接设备**

```bash
nanobot channels login whatsapp
# 使用 WhatsApp → 设置 → 链接设备扫描二维码
```

**2. 配置**

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+1234567890"]
    }
  }
}
```

**3. 运行**（两个终端）

```bash
# 终端 1
nanobot channels login whatsapp

# 终端 2
nanobot gateway
```

> WhatsApp 桥接更新不会自动应用于现有安装。
> 升级 nanobot 后，使用以下命令重建本地桥接：
> `rm -rf ~/.nanobot/bridge && nanobot channels login whatsapp`

</details>

<details>
<summary><b>Feishu (飞书)</b></summary>

使用 **WebSocket** 长连接 — 无需公共 IP。

**1. 创建飞书 Bot**
- 访问 [飞书开放平台](https://open.feishu.cn/app)
- 创建新应用 → 启用 **Bot** 能力
- **权限**：
  - `im:message`（发送消息）和 `im:message.p2p_msg:readonly`（接收消息）
  - **流式回复**（nanobot 中默认）：添加 **`cardkit:card:write`**（在飞书开发者控制台中通常标记为 **创建和更新卡片**）。CardKit 实体和流式助手文本需要此权限。较旧的应用可能还没有此权限 — 打开 **权限管理**，启用该作用域，如果控制台需要，则 **发布** 新的应用版本。
  - 如果您**无法**添加 `cardkit:card:write`，请在 `channels.feishu` 下设置 `"streaming": false`（见下文）。Bot 仍然可以工作；回复使用普通的交互式卡片，而没有逐个 token 的流式传输。
- **事件**：添加 `im.message.receive_v1`（接收消息）
  - 选择 **长连接** 模式（需要先运行 nanobot 以建立连接）
- 从"凭证与基础信息"中获取 **App ID** 和 **App Secret**
- 发布应用

**2. 配置**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": ["ou_YOUR_OPEN_ID"],
      "groupPolicy": "mention",
      "reactEmoji": "OnIt",
      "doneEmoji": "DONE",
      "toolHintPrefix": "🔧",
      "streaming": true,
      "domain": "feishu"
    }
  }
}
```

> `streaming` 默认为 `true`。如果您的应用没有 **`cardkit:card:write`**（请参阅上面的权限），则使用 `false`。
> 对于长连接模式，`encryptKey` 和 `verificationToken` 是可选的。
> `allowFrom`：添加您的 open_id（当您向 Bot 发送消息时，可以在 nanobot 日志中找到它）。使用 `["*"]` 允许所有用户。
> `groupPolicy`：`"mention"`（默认 — 仅在被 @ 提及时响应），`"open"`（响应所有群组消息）。私聊总是响应。
> `reactEmoji`：表示"处理中"状态的表情符号（默认：`OnIt`）。请参阅[可用的表情符号](https://open.larkoffice.com/document/server-docs/im-v1/message-reaction/emojis-introduce)。
> `doneEmoji`：表示"已完成"状态的可选表情符号（例如 `DONE`、`OK`、`HEART`）。设置后，Bot 在移除 `reactEmoji` 后会添加此反应。
> `toolHintPrefix`：流式卡片中内联工具提示的前缀（默认：`🔧`）。
> `domain`：`"feishu"`（默认）用于中国（open.feishu.cn），`"lark"` 用于国际版 Lark（open.larksuite.com）。

**3. 运行**

```bash
nanobot gateway
```

> [!TIP]
> 飞书使用 WebSocket 接收消息 — 无需 webhook 或公共 IP！

</details>

<details>
<summary><b>QQ (QQ单聊)</b></summary>

使用带有 WebSocket 的 **botpy SDK** — 无需公共 IP。目前仅支持**私聊**。

**1. 注册并创建 Bot**
- 访问 [QQ 开放平台](https://q.qq.com) → 注册为开发者（个人或企业）
- 创建新的 Bot 应用
- 进入 **开发设置** → 复制 **AppID** 和 **AppSecret**

**2. 设置沙箱以进行测试**
- 在 Bot 管理控制台中，找到 **沙箱配置**
- 在 **消息列表配置** 下，点击 **添加成员** 并添加您自己的 QQ 号码
- 添加后，使用手机 QQ 扫描 Bot 的二维码 → 打开 Bot 资料页面 → 点击"发消息"开始聊天

**3. 配置**

> - `allowFrom`：添加您的 openid（当您向 Bot 发送消息时，可以在 nanobot 日志中找到它）。使用 `["*"]` 公开访问。
> - `msgFormat`：可选。使用 `"plain"`（默认）以获得与旧版 QQ 客户端的最大兼容性，或使用 `"markdown"` 在较新的客户端上获得更丰富的格式。
> - 生产环境：在 Bot 控制台中提交审核并发布。请参阅 [QQ Bot 文档](https://bot.q.qq.com/wiki/) 了解完整的发布流程。

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_OPENID"],
      "msgFormat": "plain"
    }
  }
}
```

**4. 运行**

```bash
nanobot gateway
```

现在从 QQ 向 Bot 发送消息 — 它应该会回复！

</details>

<details>
<summary><b>DingTalk (钉钉)</b></summary>

使用 **流模式** — 无需公共 IP。

**1. 创建钉钉 Bot**
- 访问 [钉钉开放平台](https://open-dev.dingtalk.com/)
- 创建新应用 → 添加 **机器人** 能力
- **配置**：
  - 打开 **流模式** 开关
- **权限**：添加发送消息所需的权限
- 从"凭证"中获取 **AppKey**（Client ID）和 **AppSecret**（Client Secret）
- 发布应用

**2. 配置**

```json
{
  "channels": {
    "dingtalk": {
      "enabled": true,
      "clientId": "YOUR_APP_KEY",
      "clientSecret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_STAFF_ID"]
    }
  }
}
```

> `allowFrom`：添加您的员工 ID。使用 `["*"]` 允许所有用户。

**3. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Slack</b></summary>

使用 **Socket 模式** — 无需公共 URL。

**1. 创建 Slack 应用**
- 访问 [Slack API](https://api.slack.com/apps) → **创建新应用** → "从头开始"
- 选择名称并选择您的工作区

**2. 配置应用**
- **Socket 模式**：打开开关 → 生成具有 `connections:write` 范围的 **应用级 Token** → 复制它（`xapp-...`）
- **OAuth 和权限**：添加 Bot 范围：`chat:write`、`reactions:write`、`app_mentions:read`、`files:read`、`files:write`、`channels:history`、`groups:history`、`im:history`、`mpim:history`
- **事件订阅**：打开开关 → 订阅 Bot 事件：`message.im`、`message.channels`、`app_mention` → 保存更改
- **应用主页**：向下滚动到 **显示标签页** → 启用 **消息标签页** → 勾选 **"允许用户从消息标签页发送斜杠命令和消息"**
- **安装应用**：点击 **安装到工作区** → 授权 → 复制 **Bot Token**（`xoxb-...`）

> `files:read` 是读取用户发送给 nanobot 的文件所必需的。`files:write` 是 nanobot 发送图像、视频和其他文件上传所必需的。如果您稍后添加任一范围，请将 Slack 应用重新安装到工作区并重启 nanobot，以便它使用更新的 Bot Token。

**3. 配置 nanobot**

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "botToken": "xoxb-...",
      "appToken": "xapp-...",
      "allowFrom": ["YOUR_SLACK_USER_ID"],
      "groupPolicy": "mention"
    }
  }
}
```

**4. 运行**

```bash
nanobot gateway
```

直接私信 Bot 或在频道中 @ 提及它 — 它应该会回复！

> [!TIP]
> - `groupPolicy`：`"mention"`（默认 — 仅在被 @ 提及时响应），`"open"`（响应所有频道消息），或 `"allowlist"`（限制为特定频道）。
> - 私信策略默认为开放。设置 `"dm": {"enabled": false}` 以禁用私信。

</details>

<details>
<summary><b>Email (邮件)</b></summary>

为 nanobot 提供它自己的电子邮件账户。它通过 **IMAP** 轮询传入邮件，并通过 **SMTP** 回复 — 就像个人电子邮件助手一样。

**1. 获取凭证（Gmail 示例）**
- 为您的 Bot 创建专用的 Gmail 账户（例如 `my-nanobot@gmail.com`）
- 启用两步验证 → 创建[应用密码](https://myaccount.google.com/apppasswords)
- 将此应用密码用于 IMAP 和 SMTP

**2. 配置**

> - `consentGranted` 必须为 `true` 才能允许邮箱访问。这是一个安全门 — 设置为 `false` 以完全禁用。
> - `allowFrom`：添加您的电子邮件地址。使用 `["*"]` 接受任何人的电子邮件。
> - `smtpUseTls` 和 `smtpUseSsl` 分别默认为 `true` / `false`，这对于 Gmail（端口 587 + STARTTLS）是正确的。无需显式设置。
> - 如果您只想阅读/分析电子邮件而不发送自动回复，请设置 `"autoReplyEnabled": false`。
> - `allowedAttachmentTypes`：保存匹配这些 MIME 类型的传入附件 — `["*"]` 表示全部，例如 `["application/pdf", "image/*"]`（默认 `[]` = 已禁用）。
> - `maxAttachmentSize`：每个附件的最大大小（以字节为单位，默认 `2000000` / 2MB）。
> - `maxAttachmentsPerEmail`：每封电子邮件保存的最大附件数（默认 `5`）。

```json
{
  "channels": {
    "email": {
      "enabled": true,
      "consentGranted": true,
      "imapHost": "imap.gmail.com",
      "imapPort": 993,
      "imapUsername": "my-nanobot@gmail.com",
      "imapPassword": "your-app-password",
      "smtpHost": "smtp.gmail.com",
      "smtpPort": 587,
      "smtpUsername": "my-nanobot@gmail.com",
      "smtpPassword": "your-app-password",
      "fromAddress": "my-nanobot@gmail.com",
      "allowFrom": ["your-real-email@gmail.com"],
      "allowedAttachmentTypes": ["application/pdf", "image/*"]
    }
  }
}
```


**3. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>WeChat (微信 / Weixin)</b></summary>

通过 ilinkai 个人微信 API 使用带有二维码登录的 **HTTP 长轮询**。无需本地微信桌面客户端。

**1. 安装微信支持**

```bash
pip install "nanobot-ai[weixin]"
```

**2. 配置**

```json
{
  "channels": {
    "weixin": {
      "enabled": true,
      "allowFrom": ["YOUR_WECHAT_USER_ID"]
    }
  }
}
```

> - `allowFrom`：添加您在 nanobot 日志中为您的微信帐户看到的发送者 ID。使用 `["*"]` 允许所有用户。
> - `token`：可选。如果省略，则以交互方式登录，nanobot 将为您保存 Token。
> - `routeTag`：可选。当您的上游 Weixin 部署需要请求路由时，nanobot 将将其作为 `SKRouteTag` 请求头发送。
> - `stateDir`：可选。默认为 nanobot 的运行时目录，用于 Weixin 状态。
> - `pollTimeout`：可选长轮询超时（以秒为单位）。

**3. 登录**

```bash
nanobot channels login weixin
```

使用 `--force` 重新认证并忽略任何保存的 Token：

```bash
nanobot channels login weixin --force
```

**4. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Wecom (企业微信)</b></summary>

> 这里我们使用 [wecom-aibot-sdk-python](https://github.com/chengyongru/wecom_aibot_sdk)（官方 [@wecom/aibot-node-sdk](https://www.npmjs.com/package/@wecom/aibot-node-sdk) 的社区 Python 版本）。
>
> 使用 **WebSocket** 长连接 — 无需公共 IP。

**1. 安装可选依赖**

```bash
pip install nanobot-ai[wecom]
```

**2. 创建企业微信 AI Bot**

进入企业微信管理控制台 → 智能机器人 → 创建机器人 → 选择带长连接的 **API 模式**。复制 Bot ID 和 Secret。

**3. 配置**

```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "botId": "your_bot_id",
      "secret": "your_bot_secret",
      "allowFrom": ["your_id"]
    }
  }
}
```

**4. 运行**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Microsoft Teams</b> (MVP — 仅私信)</summary>

> 直接消息文本输入/输出，租户感知 OAuth，对话引用持久化。
> 使用公共 HTTPS webhook — 没有 WebSocket；您需要隧道或反向代理。

**1. 安装可选依赖**

```bash
pip install nanobot-ai[msteams]
```

**2. 创建 Teams / Azure Bot 应用注册**

创建或重用 Microsoft Teams / Azure Bot 应用注册。将 Bot 消息传递端点设置为以 `/api/messages` 结尾的公共 HTTPS URL。

**3. 配置**

```json
{
  "channels": {
    "msteams": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "appPassword": "YOUR_APP_SECRET",
      "tenantId": "YOUR_TENANT_ID",
      "host": "0.0.0.0",
      "port": 3978,
      "path": "/api/messages",
      "allowFrom": ["*"],
      "replyInThread": true,
      "mentionOnlyResponse": "Hi — what can I help with?",
      "validateInboundAuth": true,
      "refTtlDays": 30,
      "pruneWebChatRefs": true,
      "pruneNonPersonalRefs": true,
      "refTouchIntervalS": 300
    }
  }
}
```

> - `replyInThread: true` 在有存储的 `activity_id` 时回复触发的 Teams 活动。
> - `mentionOnlyResponse` 控制当用户仅发送 Bot 提及（`<at>Nanobot</at>`）时 Nanobot 接收的内容。设置为 `""` 以忽略仅提及消息。
> - `validateInboundAuth: true` 启用入站 Bot Framework 持有者令牌验证（签名、颁发者、受众、生存期、`serviceUrl`）。这是公共部署的安全默认设置。仅对本地开发或严格控制的测试将其设置为 `false`。
> - `refTtlDays`（默认 `30`）控制存储的对话引用在被修剪之前可以使用多久。
> - `pruneWebChatRefs`（默认 `true`）丢弃具有 `webchat.botframework.com` 服务 URL 的引用。
> - `pruneNonPersonalRefs`（默认 `true`）丢弃其 `conversation_type` 不是 `personal` 的引用。
> - `refTouchIntervalS`（默认 `300`）限制成功发送刷新活动引用的 `updated_at` 的频率。

**4. 运行**

```bash
nanobot gateway
```

</details>
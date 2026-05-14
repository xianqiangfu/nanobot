# 通道测试

本目录包含各个聊天平台通道的集成测试。

## 测试范围

### 平台通道测试

#### Telegram
- `test_telegram_channel.py` - Telegram 通道集成
  - 消息接收和发送
  - 媒体处理
  - Markdown 渲染

#### Discord
- `test_discord_channel.py` - Discord 通道集成
  - Slash 命令处理
  - 消息编辑
  - 附件处理

#### Slack
- `test_slack_channel.py` - Slack 通道集成
  - 事件处理
  - 消息格式化
  - 用户信息解析

#### Feishu (飞书)
- `test_feishu_channel.py` - 飞书通道基础测试
- `test_feishu_domain.py` - 域名处理
- `test_feishu_markdown_rendering.py` - Markdown 渲染
- `test_feishu_mention.py` - @提及处理
- `test_feishu_mentions.py` - 多提及处理
- `test_feishu_post_content.py` - 帖子内容
- `test_feishu_reaction.py` - 表情回应
- `test_feishu_reply.py` - 回复处理
- `test_feishu_streaming.py` - 流式输出
- `test_feishu_table_split.py` - 表格分割
- `test_feishu_tool_hint_code_block.py` - 工具提示代码块

#### WeChat (微信)
- `test_weixin_channel.py` - 微信通道集成

#### WhatsApp
- `test_whatsapp_channel.py` - WhatsApp 通道集成

#### WebSocket
- `test_websocket_channel.py` - WebSocket 通道核心功能
- `test_websocket_integration.py` - WebSocket 集成测试
- `test_websocket_http_routes.py` - HTTP 路由
- `test_websocket_envelope_media.py` - 媒体封装
- `test_websocket_media_route.py` - 媒体路由

#### Matrix
- `test_matrix_channel.py` - Matrix 通道集成

#### QQ
- `test_qq_channel.py` - QQ 通道基础功能
- `test_qq_media.py` - 媒体处理
- `test_qq_ack_message.py` - 确认消息

#### 其他平台
- `test_dingtalk_channel.py` - 钉钉通道
- `test_wecom_channel.py` - 企业微信通道
- `test_email_channel.py` - 邮件通道

### 通道管理器测试

- `test_channel_manager_delta_coalescing.py` - 增量合并
- `test_channel_manager_reasoning.py` - 推理处理
- `test_channel_plugins.py` - 通道插件

### 基础测试

- `test_base_channel.py` - 通道基类测试

### 测试工具

- `ws_test_client.py` - WebSocket 测试客户端

## 运行测试

### 运行所有通道测试

```bash
pytest tests/channels/
```

### 运行特定平台测试

```bash
pytest tests/channels/test_telegram_channel.py
pytest tests/channels/test_feishu_channel.py
```

### 运行 WebSocket 相关测试

```bash
pytest tests/channels/test_websocket_*.py
```

## 测试特性

### 消息处理
- 入站消息解析
- 出站消息格式化
- 消息类型识别（文本、媒体、文件等）

### 媒体处理
- 图片上传和下载
- 文件处理
- 媒体 URL 签名

### 用户交互
- 用户信息获取
- 用户提及
- 回复和转发

### 实时功能
- WebSocket 连接
- 流式输出
- 心跳和重连

### 错误处理
- 网络错误
- API 错误
- 认证失败

## 测试工具

### ws_test_client.py

WebSocket 测试客户端，用于测试 WebSocket 通道：

```python
from tests.channels.ws_test_client import WebSocketTestClient

async with WebSocketTestClient(url) as client:
    await client.connect()
    await client.send_message("hello")
    response = await client.receive_message()
```

## 测试注意事项

1. **隔离性** - 每个平台测试应该独立运行
2. **Mock 使用** - 避免依赖实际的平台 API
3. **网络处理** - 处理网络延迟和超时
4. **认证测试** - 测试各种认证场景
5. **媒体处理** - 测试不同类型的媒体文件
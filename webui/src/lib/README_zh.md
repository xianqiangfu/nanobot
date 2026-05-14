# 核心库

本目录包含 WebUI 的核心工具函数和 API 客户端。

## 目录结构

```
lib/
├── api.ts                # REST API 客户端
├── bootstrap.ts          # 应用启动逻辑
├── format.ts             # 格式化工具
├── imageEncode.ts        # 图片编码工具
├── media.ts              # 媒体附件处理
├── nanobot-client.ts     # WebSocket 客户端
├── tool-traces.ts        # 工具调用追踪
├── types.ts              # TypeScript 类型定义
└── utils.ts              # 通用工具函数
```

## 模块说明

### api.ts
提供与 nanobot 网关 REST API 交互的函数。

**主要功能**：
- `listSessions()` - 获取会话列表
- `fetchSessionMessages()` - 获取会话消息历史
- `deleteSession()` - 删除会话
- `fetchSettings()` - 获取配置
- `updateSettings()` - 更新配置
- `listSlashCommands()` - 获取斜杠命令列表

**错误处理**：
- 使用 `ApiError` 类处理 HTTP 错误
- 自动添加认证 token

### nanobot-client.ts
WebSocket 客户端实现，负责与网关的实时通信。

**主要类**：
- `NanobotClient` - WebSocket 客户端主类

**功能**：
- 建立和维持 WebSocket 连接
- 处理多路复用消息流
- 心跳检测和自动重连
- 消息事件订阅

### types.ts
定义整个 WebUI 的 TypeScript 类型。

**主要类型**：
- `UIMessage` - UI 消息接口
- `ChatSummary` - 会话摘要
- `SettingsPayload` - 配置载荷
- `InboundEvent` - 网关事件
- `OutboundMedia` - 出站媒体
- `StreamError` - 流错误

### format.ts
文本格式化工具函数。

**功能**：
- 时间格式化
- 文本截断
- Markdown 清理

### media.ts
媒体附件处理工具。

**功能**：
- 媒体类型检测
- 媒体 URL 解析
- 媒体附件转换

### tool-traces.ts
工具调用追踪和渲染。

**功能**：
- 工具调用事件解析
- 追踪信息格式化
- 工具调用历史记录

### imageEncode.ts
图片编码处理（使用 Web Worker）。

**功能**：
- 将图片转换为 base64
- 图片压缩
- 批量图片处理

### utils.ts
通用工具函数。

**主要函数**：
- `cn()` - Tailwind CSS 类名合并
- 常用的字符串处理
- 对象和数组工具

### bootstrap.ts
应用启动初始化逻辑。

**功能**：
- 检测运行环境
- 初始化配置
- 设置主题
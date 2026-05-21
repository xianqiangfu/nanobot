# React Hooks

此目录包含 WebUI 的自定义 React Hooks。

## 目录结构

```
hooks/
├── useAttachedImages.ts    # 图片附件管理
├── useClipboardAndDrop.ts  # 剪贴板和拖放处理
├── useNanobotStream.ts     # nanobot 流式消息处理
├── useSessions.ts          # 会话管理
└── useTheme.ts             # 主题管理
```

## Hook 描述

### useAttachedImages
管理消息编辑器中的图片附件。

**功能**:
- 添加和删除图片
- 将图片转换为 base64 格式
- 生成预览 URL

### useClipboardAndDrop
处理剪贴板粘贴和文件拖放。

**功能**:
- 监听剪贴板粘贴事件
- 处理文件拖放
- 提取图片内容

### useNanobotStream
处理与 nanobot 网关的 WebSocket 流式通信。

**功能**:
- 订阅聊天会话
- 处理流式消息增量
- 管理消息状态（流式传输/已完成）
- 处理工具调用和推理内容
- 错误处理和重试

**主要特性**:
- 智能合并消息增量以减少渲染
- 支持推理内容流式传输
- 工具调用和推理阶段的占位符管理
- 自动清理临时占位符

### useSessions
管理会话列表和会话切换。

**功能**:
- 加载会话列表
- 创建新会话
- 删除会话
- 切换当前会话
- 会话搜索和筛选

### useTheme
管理应用程序主题（暗色/亮色模式）。

**功能**:
- 切换主题
- 持久化主题设置
- 响应系统主题变化

## 使用示例

### useNanobotStream

```typescript
const {
  messages,
  isStreaming,
  send,
  stop,
  streamError,
  dismissStreamError
} = useNanobotStream(
  chatId,
  initialMessages,
  hasPendingToolCalls,
  onTurnEnd
);

// 发送消息
send("Hello", images);

// 停止生成
stop();
```

### useSessions

```typescript
const {
  sessions,
  activeKey,
  loading,
  createNew,
  select,
  delete: deleteSession
} = useSessions();

// 创建新会话
createNew();
```

### useTheme

```typescript
const { theme, toggleTheme } = useTheme();

// 切换主题
toggleTheme();
```

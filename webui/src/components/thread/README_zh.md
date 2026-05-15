# 线程相关组件

本目录包含 nanobot WebUI 的线程相关组件。

## 组件说明

### ThreadShell (`ThreadShell.tsx`)

线程的根容器组件，负责：
- 管理线程的生命周期
- 协调线程内的所有组件
- 处理线程打开/关闭状态
- 管理线程动画和布局

**关键特性**：
- 动态创建和管理线程
- 支持多线程并发
- 响应式布局
- 平滑的打开/关闭动画

### ThreadComposer (`ThreadComposer.tsx`)

线程内的消息编辑器，负责：
- 处理用户输入
- 管理图片附件
- 发送消息到服务器
- 支持格式化和工具调用

**功能**：
- 多行文本输入
- 图片上传和预览
- 发送和停止生成
- 快捷键支持（Enter 发送，Shift+Enter 换行）

### ThreadHeader (`ThreadHeader.tsx`)

线程头部组件，显示：
- 线程标题
- 关闭按钮
- 工具调用信息
- 当前状态指示器

### ThreadMessages (`ThreadMessages.tsx`)

线程消息列表，负责：
- 渲染线程内的消息
- 显示工具调用和推理内容
- 消息滚动和自动定位
- Markdown 渲染

### ThreadViewport (`ThreadViewport.tsx`)

线程视口组件，负责：
- 管理线程的可滚动区域
- 自动滚动到底部
- 处理新消息通知
- 滚动位置管理

### StreamErrorNotice (`StreamErrorNotice.tsx`)

流式错误提示组件，负责：
- 显示流式传输错误
- 提供重试选项
- 错误详情展示

## 线程生命周期

1. **创建** - 通过回复消息创建新线程
2. **打开** - 显示线程编辑器和消息
3. **交互** - 用户发送新消息或查看历史
4. **关闭** - 最小化或关闭线程
5. **删除** - 从 DOM 中移除线程

## 使用示例

### 创建线程

线程通常通过回复操作自动创建，但也可以手动触发：

```tsx
const { createThread } = useThreadShell();
createThread(parentMessageId);
```

### 线程状态

线程有以下状态：
- `closed` - 关闭状态
- `opening` - 打开中
- `open` - 打开状态
- `closing` - 关闭中

## 注意事项

- 线程组件应该是自包含的
- 线程不应影响主聊天界面的滚动
- 线程消息应该与主消息共享相同的样式
- 线程关闭后应保留其内容以便重新打开

# 组件说明

本目录包含 WebUI 的所有 React 组件。

## 目录结构

```
components/
├── ChatList.tsx          # 会话列表组件
├── ChatPane.tsx          # 聊天面板主组件
├── CodeBlock.tsx         # 代码块渲染组件
├── Composer.tsx          # 消息编辑器组件
├── ConnectionBadge.tsx   # 连接状态指示器
├── DeleteConfirm.tsx     # 删除确认对话框
├── EmptyState.tsx        # 空状态提示
├── ImageLightbox.tsx     # 图片查看器
├── LanguageSwitcher.tsx  # 语言切换器
├── MarkdownText.tsx      # Markdown 文本渲染
├── MarkdownTextRenderer.tsx  # Markdown 渲染器
├── MessageBubble.tsx     # 消息气泡组件
├── MessageList.tsx       # 消息列表组件
├── Sidebar.tsx           # 侧边栏导航
├── settings/
│   └── SettingsView.tsx  # 设置视图
├── thread/
│   ├── StreamErrorNotice.tsx   # 流错误提示
│   ├── ThreadComposer.tsx      # 线程编辑器
│   ├── ThreadHeader.tsx        # 线程头部
│   ├── ThreadMessages.tsx      # 线程消息
│   ├── ThreadShell.tsx         # 线程容器
│   └── ThreadViewport.tsx      # 线程视口
└── ui/                     # shadcn/ui 基础组件
    ├── alert-dialog.tsx
    ├── avatar.tsx
    ├── button.tsx
    ├── dialog.tsx
    ├── dropdown-menu.tsx
    ├── input.tsx
    ├── scroll-area.tsx
    ├── separator.tsx
    ├── sheet.tsx
    ├── textarea.tsx
    └── tooltip.tsx
```

## 核心组件

### ChatPane
聊天面板的主容器，管理消息列表、输入区域和线程视图。

### Sidebar
侧边栏导航，包含会话列表、搜索和设置入口。

### MessageBubble
单个消息的气泡组件，支持用户和助手消息的不同样式。

### Composer
消息编辑器，支持文本输入、图片上传和发送。

### ThreadShell
线程的根容器，管理线程的生命周期和布局。

## UI 组件

`ui/` 目录包含从 [shadcn/ui](https://ui.shadcn.com/) 导入的基础 UI 组件：

- **Button** - 按钮组件，支持多种变体
- **Dialog** - 对话框组件
- **Input** - 输入框组件
- **Textarea** - 多行文本输入组件
- **ScrollArea** - 可滚动区域组件
- **Tooltip** - 工具提示组件
- **Avatar** - 头像组件
- **Sheet** - 侧边抽屉组件
- **DropdownMenu** - 下拉菜单组件
- **AlertDialog** - 警告对话框组件
- **Separator** - 分隔线组件

## 组件特性

- **国际化支持**：所有组件通过 `react-i18next` 支持多语言
- **响应式设计**：使用 Tailwind CSS 实现响应式布局
- **深色模式**：支持深色和浅色主题切换
- **无障碍访问**：遵循 ARIA 规范，支持键盘导航
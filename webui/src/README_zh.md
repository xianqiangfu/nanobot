# WebUI 源代码

本目录包含 nanobot WebUI 的 React TypeScript 源代码。

## 目录结构

```
src/
├── App.tsx              # 应用根组件
├── main.tsx             # 应用入口
├── globals.css          # 全局样式
├── components/          # React 组件
├── hooks/               # 自定义 Hooks
├── i18n/                # 国际化配置
├── lib/                 # 工具库
├── providers/           # React Context Providers
├── tests/               # 测试文件
└── workers/             # Web Workers
```

## 主要组件

### App.tsx

应用根组件，负责：
- 路由管理
- 主题上下文提供
- 国际化上下文提供

### main.tsx

应用入口，负责：
- 注册 service worker
- 初始化根组件

## 目录说明

### components/

包含所有 React UI 组件：
- 聊天相关组件（ChatPane、ChatList、MessageBubble 等）
- UI 基础组件（Button、Dialog、Input 等）
- 设置相关组件（SettingsView）
- 线程相关组件（ThreadShell、ThreadComposer 等）

### hooks/

自定义 React Hooks：
- useAttachedImages - 图片附件管理
- useClipboardAndDrop - 剪贴板和拖放
- useNanobotStream - WebSocket 流式通信
- useSessions - 会话管理
- useTheme - 主题切换

### i18n/

国际化配置：
- 语言切换
- 翻译资源
- 语言检测

### lib/

工具库：
- API 客户端
- 格式化函数
- 媒体处理
- nanobot 客户端
- 类型定义
- 工具函数

### providers/

React Context Providers：
- nanobot 客户端 provider
- 其他应用级别的 providers

### tests/

测试文件：
- 组件测试
- Hook 测试
- API 测试
- 集成测试

### workers/

Web Workers：
- imageEncode.worker.ts - 图片编码 worker

## 技术栈

- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Tailwind CSS** - 样式框架
- **shadcn/ui** - UI 组件库
- **react-i18next** - 国际化
- **Vitest** - 测试框架
- **React Testing Library** - 组件测试

## 开发指南

### 添加新组件

1. 在 `components/` 目录下创建组件文件
2. 使用 TypeScript 编写
3. 导入必要的 shadcn/ui 组件
4. 添加国际化文本

### 添加新 Hook

1. 在 `hooks/` 目录下创建 Hook 文件
2. 遵循 React Hooks 规则
3. 添加适当的类型定义
4. 编写测试

### 添加新翻译

1. 在 `i18n/config.ts` 中添加语言配置
2. 在 `i18n/` 目录下添加翻译资源

## 注意事项

- 所有组件都应该支持深色模式
- 使用 Tailwind CSS 进行样式设计
- 遵循组件命名约定
- 保持测试覆盖率
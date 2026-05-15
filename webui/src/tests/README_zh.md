# 测试文件

本目录包含 WebUI 的所有测试文件。

## 测试框架

- **Vitest** - 测试运行器
- **React Testing Library** - 组件测试工具
- **jsdom** - DOM 环境

## 测试文件

### API 测试

- **api.test.ts** - API 客户端测试

### 组件测试

- **app-layout.test.tsx** - 应用布局测试
- **message-bubble.test.tsx** - 消息气泡组件测试
- **i18n.test.tsx** - 国际化测试
- **thread-composer.test.tsx** - 线程编辑器测试
- **thread-composer-attach.test.tsx** - 线程附件测试
- **thread-messages.test.tsx** - 线程消息测试
- **thread-shell.test.tsx** - 线程容器测试
- **thread-viewport.test.tsx** - 线程视口测试

### Hook 测试

- **useNanobotStream.test.tsx** - WebSocket 流式通信 Hook 测试
- **useSessions.test.tsx** - 会话管理 Hook 测试

### 功能测试

- **format.i18n.test.ts** - 格式化和国际化测试
- **main-randomuuid.test.tsx** - UUID 生成测试

## 测试运行

```bash
# 运行所有测试
npm test

# 运行特定测试
npm test api.test.ts

# 监听模式
npm test -- --watch

# 覆盖率报告
npm test -- --coverage
```

## 测试最佳实践

1. **测试用户行为** - 测试用户实际如何使用应用
2. **使用语义化查询** - 优先使用语义化查询方法
3. **保持测试独立** - 每个测试应该独立运行
4. **使用描述性名称** - 测试名称应该清晰描述测试内容
5. **适当的断言** - 只断言关键行为

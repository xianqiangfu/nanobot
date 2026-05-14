# Context Providers

本目录包含 React Context Providers，用于全局状态管理。

## 目录结构

```
providers/
└── ClientProvider.tsx    # nanobot 客户端 Provider
```

## Provider 说明

### ClientProvider
提供 nanobot 客户端和配置给整个应用树。

**提供的值**：
- `client: NanobotClient` - WebSocket 客户端实例
- `token: string` - 认证 token
- `modelName: string | null` - 当前模型名称

**使用示例**：

```typescript
import { useClient } from '@/providers/ClientProvider';

function MyComponent() {
  const { client, token, modelName } = useClient();
  // 使用 client 发送消息
}
```

## 设计模式

### Provider 模式
使用 React Context API 实现全局状态共享：

1. **创建 Context**：定义数据的形状和默认值
2. **提供 Context**：在应用顶层使用 Provider 组件
3. **消费 Context**：通过 `useClient` hook 获取数据

### 优势
- **避免 prop drilling**：不需要逐层传递 props
- **集中管理**：客户端和配置集中管理
- **类型安全**：TypeScript 提供完整的类型检查
- **易于测试**：可以轻松创建 mock provider

## 未来扩展

随着应用的发展，可能需要添加更多的 Provider：

- `ThemeProvider` - 主题管理
- `I18nProvider` - 国际化配置
- `NotificationProvider` - 通知系统
- `ModalProvider` - 模态框管理
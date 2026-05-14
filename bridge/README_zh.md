# TypeScript 桥接服务

本目录包含 nanobot 的 TypeScript 桥接服务，用于连接外部服务到 Python 后端。

## 目录结构

```
bridge/
├── src/
│   ├── index.ts          # 主入口点
│   ├── server.ts         # 桥接服务器实现
│   ├── whatsapp.ts       # WhatsApp 桥接实现
│   └── types.d.ts        # TypeScript 类型定义
├── package.json          # NPM 包配置
└── tsconfig.json         # TypeScript 配置
```

## 当前实现

### WhatsApp Bridge

WhatsApp 桥接服务连接 WhatsApp Web 到 nanobot 的 Python 后端。

**功能**：
- 认证和会话管理
- 消息转发
- 重连逻辑
- 媒体处理

**运行方式**：

```bash
# 通过 nanobot 启动
nanobot gateway

# 或直接启动
BRIDGE_PORT=3001 BRIDGE_TOKEN=your-token npm start
```

**环境变量**：
- `BRIDGE_PORT` - 桥接服务端口（默认：3001）
- `AUTH_DIR` - 认证目录（默认：~/.nanobot/whatsapp-auth）
- `BRIDGE_TOKEN` - 认证令牌（必需）

**使用方法**：

1. 在 nanobot 配置中启用 WhatsApp 通道
2. nanobot 会自动启动桥接服务
3. 桥接服务通过 WebSocket 连接到 nanobot 后端
4. 处理 WhatsApp Web 的消息并转发

## 构建

```bash
npm install
npm run build
```

## 开发

```bash
npm run dev
```

## TypeScript 配置

TypeScript 配置在 `tsconfig.json` 中：

- 目标：ES2020
- 模块：ESNext
- 严格模式：启用
- 模块解析：node

## 依赖

### 生产依赖
- Baileys - WhatsApp Web API
- ws - WebSocket 客户端
- node-cron - 定时任务

### 开发依赖
- TypeScript - TypeScript 编译器
- @types/node - Node.js 类型定义
- tsx - TypeScript 执行器

## 未来扩展

桥接服务架构支持添加其他桥接：

- 更多聊天平台的桥接
- 自定义服务桥接
- 第三方 API 桥接

## 注意事项

1. **认证存储** - 认证数据存储在本地目录中
2. **安全性** - 使用 BRIDGE_TOKEN 进行认证
3. **重连机制** - 桥接服务会自动重连
4. **日志记录** - 详细的日志记录用于调试
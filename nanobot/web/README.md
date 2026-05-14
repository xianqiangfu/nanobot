# Web 服务

本模块包含 nanobot Web UI 的嵌入资产。

## 概述

`dist/` 子目录通过运行 `cd webui && bun run build` 填充，并随 Python wheel 一起打包。在源码检出时，该目录保持为空，直到运行构建命令。

## 目录结构

```
nanobot/web/
├── __init__.py      # 模块初始化
└── dist/            # 构建输出（运行 build 后生成）
    ├── index.html   # 主 HTML 文件
    ├── assets/      # 静态资产
    └── ...
```

## 构建 Web UI

在 `webui/` 目录下运行构建命令：

```bash
cd webui
bun run build
```

构建输出会自动打包到 `nanobot/web/dist/` 中。

## WebUI 项目结构

WebUI 是一个独立的 React + TypeScript 项目，位于 `webui/` 目录：

```
webui/
├── src/
│   ├── hooks/           # React Hooks
│   │   ├── useAttachedImages.ts
│   │   ├── useClipboardAndDrop.ts
│   │   ├── useNanobotStream.ts
│   │   ├── useSessions.ts
│   │   └── useTheme.ts
│   ├── i18n/            # 国际化
│   │   ├── config.ts
│   │   └── index.ts
│   ├── lib/             # 库和工具
│   │   ├── api.ts
│   │   ├── bootstrap.ts
│   │   ├── format.ts
│   │   ├── imageEncode.ts
│   │   ├── media.ts
│   │   ├── nanobot-client.ts
│   │   ├── tool-traces.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   ├── tests/           # 测试
│   │   ├── api.test.ts
│   │   ├── format.i18n.test.ts
│   │   ├── nanobot-client.test.ts
│   │   └── setup.ts
│   └── workers/         # Web Workers
│       └── imageEncode.worker.ts
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── ...
```

## 开发服务器

启动开发服务器：

```bash
cd webui
bun run dev
```

开发服务器代理 `/api`、`/webui`、`/auth` 和 WebSocket 流量到网关（端口 8765）。

## 与 Gateway 集成

WebUI 通过 WebSocket 与 gateway 通信，使用多路复用协议：

- **API 调用** - 通过 `/api` 端点
- **实时消息** - 通过 WebSocket
- **认证** - 通过 `/auth` 端点

## 主要功能

### 会话管理

- 查看和管理所有会话
- 创建新会话
- 删除会话

### 消息流

- 实时显示智能体响应
- 支持流式输出
- 显示工具调用和结果

### 图像处理

- 支持图像上传
- 图像编码 worker
- 图像占位符显示

### 主题切换

- 支持明暗主题
- 主题持久化

## 测试

运行 WebUI 测试：

```bash
cd webui
bun run test
```

## 注意事项

- `dist/` 目录在源码检出时为空
- 构建后，`dist/` 内容被打包到 Python wheel
- 开发时使用 dev 服务器代理 API 请求
- WebSocket 连接使用多路复用协议
# nanobot webui

nanobot 网关的浏览器前端。它使用 Vite + React 18 + TypeScript + Tailwind 3 + shadcn/ui 构建，通过 WebSocket 多路复用协议与网关通信，并从同一端口上的嵌入式 REST 表面读取会话元数据。

有关项目概述、安装指南和一般文档地图，请参阅根目录的 [`README.md`](../README.md)。

## 当前状态

> [!NOTE]
> 独立 WebUI 开发工作流程目前需要源代码检出。
>
> GitHub 仓库中的 WebUI 更新可能会在包含在下一个打包版本之前发布，因此源代码安装和已发布的包版本目前还不能保证同步。

## 目录结构

```text
webui/                 源代码树（本目录）
nanobot/web/dist/      由网关服务的构建输出
```

## 从源代码开发

### 1. 从源代码安装 nanobot

在仓库根目录：

```bash
pip install -e .
```

### 2. 启用 WebSocket 通道

在 `~/.nanobot/config.json` 中：

```json
{ "channels": { "websocket": { "enabled": true } } }
```

### 3. 启动网关

在一个终端中：

```bash
nanobot gateway
```

### 4. 启动 WebUI 开发服务器

在另一个终端中：

```bash
cd webui
bun install            # npm install 也可以
bun run dev
```

然后打开 `http://127.0.0.1:5173`。

默认情况下，开发服务器会将 `/api`、`/webui`、`/auth` 和 WebSocket 流量代理到 `http://127.0.0.1:8765`。

如果你的网关监听非默认端口，请将开发服务器指向它：

```bash
NANOBOT_API_URL=http://127.0.0.1:9000 bun run dev
```

### 从其他设备访问（局域网）

要在同一网络中的其他设备上使用 webui，请在 `~/.nanobot/config.json` 中将 `host` 设置为 `"0.0.0.0"` 并配置 `token` 或 `tokenIssueSecret`：

```json
{
  "channels": {
    "websocket": {
      "enabled": true,
      "host": "0.0.0.0",
      "port": 8765,
      "tokenIssueSecret": "your-secret-here"
    }
  }
}
```

如果 `host` 是 `"0.0.0.0"` 且未设置 `token` 或 `tokenIssueSecret`，网关将拒绝启动。

然后在其他设备上打开 `http://<your-ip>:8765`。webui 将显示一个身份验证表单，你可以在其中输入密钥。它会保存在浏览器中，因此只需输入一次。

## 构建用于打包运行时

```bash
cd webui
bun run build
```

这将生产资源写入 `../nanobot/web/dist`，这是 `nanobot gateway` 服务的目录，并捆绑到 Python wheel 中。

如果你要发布版本，请在打包之前运行构建，以便已发布的 wheel 包含当前的 WebUI 资源。

## 测试

```bash
cd webui
bun run test
```

## 致谢

- [`agent-chat-ui`](https://github.com/langchain-ai/agent-chat-ui) 为聊天界面和交互提供了 UI 和交互灵感。
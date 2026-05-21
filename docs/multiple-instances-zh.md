# 多实例运行

使用独立的配置和运行数据同时运行多个 nanobot 实例。使用 `--config` 作为主要入口点。如果您想初始化或更新特定实例的已保存工作区，可以在 `onboard` 时选择传递 `--workspace`。

## 快速开始

如果您希望每个实例从一开始就拥有自己专属的工作区，请在引导过程中同时传递 `--config` 和 `--workspace`。

**初始化实例：**

```bash
# 创建独立的实例配置和工作区
nanobot onboard --config ~/.nanobot-telegram/config.json --workspace ~/.nanobot-telegram/workspace
nanobot onboard --config ~/.nanobot-discord/config.json --workspace ~/.nanobot-discord/workspace
nanobot onboard --config ~/.nanobot-feishu/config.json --workspace ~/.nanobot-feishu/workspace
```

**配置每个实例：**

编辑 `~/.nanobot-telegram/config.json`、`~/.nanobot-discord/config.json` 等，为每个实例设置不同的通道配置。在 `onboard` 期间传递的工作区将作为该实例的默认工作区保存到每个配置中。

**运行实例：**

```bash
# 实例 A - Telegram 机器人
nanobot gateway --config ~/.nanobot-telegram/config.json

# 实例 B - Discord 机器人
nanobot gateway --config ~/.nanobot-discord/config.json

# 实例 C - 使用自定义端口的飞书机器人
nanobot gateway --config ~/.nanobot-feishu/config.json --port 18792
```

## 路径解析

使用 `--config` 时，nanobot 从配置文件位置派生其运行数据目录。工作区仍然来自 `agents.defaults.workspace`，除非您使用 `--workspace` 覆盖它。

要本地打开针对这些实例之一的 CLI 会话：

```bash
nanobot agent -c ~/.nanobot-telegram/config.json -m "来自 Telegram 实例的问候"
nanobot agent -c ~/.nanobot-discord/config.json -m "来自 Discord 实例的问候"

# 可选的一次性工作区覆盖
nanobot agent -c ~/.nanobot-telegram/config.json -w /tmp/nanobot-telegram-test
```

> `nanobot agent` 使用所选工作区/配置启动本地 CLI 代理。它不会附加到或代理到已运行的 `nanobot gateway` 进程。

| 组件 | 解析来源 | 示例 |
|-----------|---------------|---------|
| **配置** | `--config` 路径 | `~/.nanobot-A/config.json` |
| **工作区** | `--workspace` 或配置 | `~/.nanobot-A/workspace/` |
| **定时任务** | 配置目录 | `~/.nanobot-A/cron/` |
| **媒体 / 运行状态** | 配置目录 | `~/.nanobot-A/media/` |

## 工作原理

- `--config` 选择要加载的配置文件
- 默认情况下，工作区来自该配置中的 `agents.defaults.workspace`
- 如果您传递 `--workspace`，它将覆盖配置文件中的工作区

## 最小化设置

1. 将基础配置复制到新的实例目录。
2. 为该实例设置不同的 `agents.defaults.workspace`。
3. 使用 `--config` 启动实例。

配置示例：

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot-telegram/workspace",
      "model": "anthropic/claude-sonnet-4-6"
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_TELEGRAM_BOT_TOKEN"
    }
  },
  "gateway": {
    "host": "127.0.0.1",
    "port": 18790
  }
}
```

启动独立实例：

```bash
nanobot gateway --config ~/.nanobot-telegram/config.json
nanobot gateway --config ~/.nanobot-discord/config.json
```

每个网关实例也会在 `gateway.host:gateway.port` 上暴露一个轻量级 HTTP 健康端点。默认情况下，网关绑定到 `127.0.0.1`，因此该端点保持本地访问，除非您明确将 `gateway.host` 设置为公共或局域网地址。

- `GET /health` 返回 `{"status":"ok"}`
- 其他路径返回 `404`

需要时覆盖工作区用于一次性运行：

```bash
nanobot gateway --config ~/.nanobot-telegram/config.json --workspace /tmp/nanobot-telegram-test
```

## 常见用例

- 为 Telegram、Discord、飞书和其他平台运行独立的机器人
- 保持测试和生产实例隔离
- 为不同团队使用不同的模型或提供商
- 使用独立的配置和运行数据为多个租户提供服务

## 注意事项

- 如果同时运行，每个实例必须使用不同的端口
- 如果您想要隔离的记忆、会话和技能，请为每个实例使用不同的工作区
- `--workspace` 覆盖配置文件中定义的工作区
- 定时任务和运行时媒体/状态从配置目录派生

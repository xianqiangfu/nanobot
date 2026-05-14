# CLI 参考手册

| 命令 | 描述 |
|---------|-------------|
| `nanobot onboard` | 在 `~/.nanobot/` 初始化配置和工作空间 |
| `nanobot onboard --wizard` | 启动交互式入职向导 |
| `nanobot onboard -c <config> -w <workspace>` | 初始化或刷新特定实例配置和工作空间 |
| `nanobot agent -m "..."` | 与代理聊天 |
| `nanobot agent -w <workspace>` | 针对特定工作空间聊天 |
| `nanobot agent -w <workspace> -c <config>` | 针对特定工作空间/配置聊天 |
| `nanobot agent` | 交互式聊天模式 |
| `nanobot agent --no-markdown` | 显示纯文本回复 |
| `nanobot agent --logs` | 聊天期间显示运行时日志 |
| `nanobot serve` | 启动 OpenAI 兼容 API |
| `nanobot gateway` | 启动网关 |
| `nanobot status` | 显示状态 |
| `nanobot provider login openai-codex` | 提供商的 OAuth 登录 |
| `nanobot channels login <channel>` | 交互式身份验证通道 |
| `nanobot channels status` | 显示通道状态 |

交互式模式退出：`exit`、`quit`、`/exit`、`/quit`、`:q` 或 `Ctrl+D`。
# 部署指南

## Docker

> [!TIP]
> `-v ~/.nanobot:/home/nanobot/.nanobot` 标志将您的本地配置目录挂载到容器中，以便您的配置和工作空间在容器重启之间持久化。
> 容器以非 root 用户（`nanobot`，UID 1000）运行，并从 `/home/nanobot/.nanobot` 读取配置。始终将主机配置目录挂载到 `/home/nanobot/.nanobot`，而不是 `/root/.nanobot`。
> 如果遇到**权限被拒绝**错误，请先在主机上修复所有权：`sudo chown -R 1000:1000 ~/.nanobot`，或传递 `--user $(id -u):$(id -g)` 以匹配您的主机 UID。Podman 用户可以改用 `--userns=keep-id`。
>
> [!IMPORTANT]
> 官方 Docker 使用目前意味着使用此仓库中包含的 `Dockerfile` 进行构建。第三方命名空间下的 Docker Hub 镜像未由 HKUDS/nanobot 维护或验证；除非您信任发布者，否则不要向它们挂载 API 密钥或机器人令牌。

### Docker Compose

```bash
docker compose run --rm nanobot-cli onboard   # 首次设置
vim ~/.nanobot/config.json                     # 添加 API 密钥
docker compose up -d nanobot-gateway           # 启动网关
```

```bash
docker compose run --rm nanobot-cli agent -m "你好！"   # 运行 CLI
docker compose logs -f nanobot-gateway                   # 查看日志
docker compose down                                      # 停止
```

### Docker

```bash
# 构建镜像
docker build -t nanobot .

# 初始化配置（仅首次）
docker run -v ~/.nanobot:/home/nanobot/.nanobot --rm nanobot onboard

# 在主机上编辑配置以添加 API 密钥
vim ~/.nanobot/config.json

# 运行网关（连接到启用的通道，例如 Telegram/Discord/Mochat）
docker run -v ~/.nanobot:/home/nanobot/.nanobot -p 18790:18790 nanobot gateway

# 或运行单个命令
docker run -v ~/.nanobot:/home/nanobot/.nanobot --rm nanobot agent -m "你好！"
docker run -v ~/.nanobot:/home/nanobot/.nanobot --rm nanobot status
```

## Linux 服务

将网关作为 systemd 用户服务运行，以便它自动启动并在失败时重新启动。

**1. 找到 nanobot 二进制文件路径：**

```bash
which nanobot   # 例如 /home/user/.local/bin/nanobot
```

**2. 创建服务文件**，位于 `~/.config/systemd/user/nanobot-gateway.service`（如需要替换 `ExecStart` 路径）：

```ini
[Unit]
Description=Nanobot Gateway
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/bin/nanobot gateway
Restart=always
RestartSec=10
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=%h

[Install]
WantedBy=default.target
```

**3. 启用并启动：**

```bash
systemctl --user daemon-reload
systemctl --user enable --now nanobot-gateway
```

**常用操作：**

```bash
systemctl --user status nanobot-gateway        # 检查状态
systemctl --user restart nanobot-gateway       # 配置更改后重启
journalctl --user -u nanobot-gateway -f        # 跟踪日志
```

如果编辑 `.service` 文件本身，请在重启之前运行 `systemctl --user daemon-reload`。

> **注意：** 用户服务仅在您登录时运行。要在注销后保持网关运行，请启用 lingering：
>
> ```bash
> loginctl enable-linger $USER
> ```

## macOS LaunchAgent

当您希望 `nanobot gateway` 在登录后保持在线，而无需保持终端打开时，请使用 LaunchAgent。

**1. 获取绝对 `nanobot` 路径：**

```bash
which nanobot   # 例如 /Users/youruser/.local/bin/nanobot
```

在 plist 中使用该确切路径。它保留了您的安装方法的 Python 环境。

**2. 创建 `~/Library/LaunchAgents/ai.nanobot.gateway.plist`：**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.nanobot.gateway</string>

  <key>ProgramArguments</key>
  <array>
    <string>/Users/youruser/.local/bin/nanobot</string>
    <string>gateway</string>
    <string>--workspace</string>
    <string>/Users/youruser/.nanobot/workspace</string>
  </array>

  <key>WorkingDirectory</key>
  <string>/Users/youruser/.nanobot/workspace</string>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <dict>
    <key>SuccessfulExit</key>
    <false/>
  </dict>

  <key>StandardOutPath</key>
  <string>/Users/youruser/.nanobot/logs/gateway.log</string>

  <key>StandardErrorPath</key>
  <string>/Users/youruser/.nanobot/logs/gateway.error.log</string>
</dict>
</plist>
```

**3. 加载并启动它：**

```bash
mkdir -p ~/Library/LaunchAgents ~/.nanobot/logs
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.nanobot.gateway.plist
launchctl enable gui/$(id -u)/ai.nanobot.gateway
launchctl kickstart -k gui/$(id -u)/ai.nanobot.gateway
```

**常用操作：**

```bash
launchctl list | grep ai.nanobot.gateway
launchctl kickstart -k gui/$(id -u)/ai.nanobot.gateway   # 重启
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.nanobot.gateway.plist
```

编辑 plist 后，再次运行 `launchctl bootout ...` 和 `launchctl bootstrap ...`。

> **注意：** 如果启动失败并出现"address already in use"，请先停止手动启动的 `nanobot gateway` 进程。
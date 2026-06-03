# 部署

本指南介绍如何在不同环境下部署 nanobot，包括 Docker、Linux 系统服务、macOS LaunchAgent、Windows 服务以及多实例部署方案。

## Docker 部署

### Docker Compose 部署

**1. 创建 docker-compose.yml**

```yaml
services:
  nanobot-gateway:
    build: .
    container_name: nanobot-gateway
    volumes:
      - ~/.nanobot:/home/nanobot/.nanobot
    ports:
      - "18790:18790"
    restart: unless-stopped
    command: ["gateway"]
```

**2. 首次设置**

```bash
docker compose run --rm nanobot-cli onboard   # 首次设置
vim ~/.nanobot/config.json                     # 添加 API 密钥
docker compose up -d nanobot-gateway           # 启动网关
```

## Linux 系统服务部署

### 用户服务部署

**1. 创建服务文件** `~/.config/systemd/user/nanobot-gateway.service`：

```ini
[Unit]
Description=Nanobot Gateway
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/bin/nanobot gateway
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

**2. 启用并启动：**

```bash
systemctl --user daemon-reload
systemctl --user enable --now nanobot-gateway
```

## 多实例部署

使用独立配置和工作空间运行多个 nanobot 实例：

```bash
# 实例 1
mkdir -p ~/.nanobot-bot1
nanobot gateway --workspace ~/.nanobot-bot1

# 实例 2
mkdir -p ~/.nanobot-bot2
nanobot gateway --workspace ~/.nanobot-bot2
```

## 生产环境配置建议

1. 使用专用用户运行服务
2. 配置适当的资源限制
3. 启用日志轮转
4. 设置定期备份

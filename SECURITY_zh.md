# 安全策略

## 报告漏洞

如果您在 nanobot 中发现安全漏洞，请通过以下方式报告：

1. **切勿**在 GitHub 上公开提出 issue
2. 在 GitHub 上创建私有安全建议，或联系仓库维护者（xubinrencs@gmail.com）
3. 包含：
   - 漏洞描述
   - 复现步骤
   - 潜在影响
   - 建议修复方案（如有）

我们将在 48 小时内回复安全报告。

## 安全最佳实践

### 1. API 密钥管理

**关键**：切勿将 API 密钥提交到版本控制系统。

```bash
# ✅ 良好：将密钥存储在具有受限权限的配置文件中
chmod 600 ~/.nanobot/config.json

# ❌ 不良：在代码中硬编码密钥或提交密钥
```

**建议：**
- 将 API 密钥存储在 `~/.nanobot/config.json` 中，并将文件权限设置为 `0600`
- 考虑使用环境变量存储敏感密钥
- 对于生产部署，使用操作系统密钥环/凭据管理器
- 定期轮换 API 密钥
- 为开发和生产环境使用不同的 API 密钥

### 2. 通道访问控制

**重要**：始终为生产环境配置 `allowFrom` 列表。

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["123456789", "987654321"]
    },
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+1234567890"]
    }
  }
}
```

**安全说明：**
- 在 `v0.1.4.post3` 及更早版本中，空的 `allowFrom` 允许所有用户访问。自 `v0.1.4.post4` 起，空的 `allowFrom` 默认拒绝所有访问 — 如需允许所有人，请设置 `["*"]`
- 从 `@userinfobot` 获取您的 Telegram 用户 ID
- 对于 WhatsApp，请使用包含国家/地区代码的完整电话号码
- 定期检查访问日志，查找未授权的访问尝试

### 3. Shell 命令执行

`exec` 工具可以执行 shell 命令。虽然已阻止危险命令模式，但您应该：

- ✅ **启用 bwrap 沙箱**（`"tools.exec.sandbox": "bwrap"`）以实现内核级隔离（仅限 Linux）
- ✅ 在 agent 日志中检查所有工具使用情况
- ✅ 了解 agent 正在运行的命令
- ✅ 使用具有有限权限的专用用户账户
- ✅ 切勿以 root 身份运行 nanobot
- ❌ 不要禁用安全检查
- ❌ 未经仔细审查，不要在包含敏感数据的系统上运行

**Exec 沙箱（bwrap）：**

在 Linux 上，设置 `"tools.exec.sandbox": "bwrap"` 可以将每个 shell 命令封装在 [bubblewrap](https://github.com/containers/bubblewrap) 沙箱中。这使用 Linux 内核命名空间来限制进程可以看到的内容：

- 工作区目录 → **读写**（agent 正常工作）
- 媒体目录 → **只读**（可以读取上传的附件）
- 系统目录（`/usr`、`/bin`、`/lib`）→ **只读**（命令仍可工作）
- 配置文件和 API 密钥（`~/.nanobot/config.json`）→ **隐藏**（由 tmpfs 屏蔽）

需要安装 `bwrap`（`apt install bubblewrap`）。官方 Docker 镜像中已预安装。**在 macOS 或 Windows 上不可用** — bubblewrap 依赖于 Linux 内核命名空间。

启用沙箱还会自动为文件工具激活 `restrictToWorkspace`。

**阻止的模式：**
- `rm -rf /` - 根文件系统删除
- Fork 炸弹
- 文件系统格式化（`mkfs.*`）
- 原始磁盘写入
- 其他破坏性操作

### 4. 文件系统访问

文件操作具有路径遍历保护，但仍需注意：

- ✅ 启用 `restrictToWorkspace` 或 bwrap 沙箱以限制文件访问
- ✅ 使用专用用户账户运行 nanobot
- ✅ 使用文件系统权限保护敏感目录
- ✅ 定期审计日志中的文件操作
- ❌ 不要对敏感文件给予无限制的访问权限

### 5. 网络安全

**API 调用：**
- 所有外部 API 调用默认使用 HTTPS
- 已配置超时以防止请求挂起
- 如有需要，考虑使用防火墙限制出站连接

**WhatsApp 桥接器：**
- 桥接器绑定到 `127.0.0.1:3001`（仅限本地主机，无法从外部网络访问）
- 在配置中设置 `bridgeToken` 以启用 Python 和 Node.js 之间的共享密钥身份验证
- 确保认证数据在 `~/.nanobot/whatsapp-auth` 中安全（权限模式 0700）

### 6. 依赖项安全

**关键**：保持依赖项更新！

```bash
# 检查易受攻击的依赖项
pip install pip-audit
pip-audit

# 更新到最新的安全版本
pip install --upgrade nanobot-ai
```

对于 Node.js 依赖项（WhatsApp 桥接器）：
```bash
cd bridge
npm audit
npm audit fix
```

**重要说明：**
- 保持 `litellm` 更新到最新版本以获取安全修复
- 我们已将 `ws` 更新到 `>=8.17.1` 以修复 DoS 漏洞
- 定期运行 `pip-audit` 或 `npm audit`
- 订阅 nanobot 及其依赖项的安全建议

### 7. 生产部署

用于生产环境：

1. **隔离环境**
   ```bash
   # 在容器或 VM 中运行
   docker run --rm -it python:3.11
   pip install nanobot-ai
   ```

2. **使用专用用户**
   ```bash
   sudo useradd -m -s /bin/bash nanobot
   sudo -u nanobot nanobot gateway
   ```

3. **设置适当的权限**
   ```bash
   chmod 700 ~/.nanobot
   chmod 600 ~/.nanobot/config.json
   chmod 700 ~/.nanobot/whatsapp-auth
   ```

4. **启用日志记录**
   ```bash
   # 配置日志监控
   tail -f ~/.nanobot/logs/nanobot.log
   ```

5. **使用速率限制**
   - 在您的 API 提供商上配置速率限制
   - 监控使用情况以检测异常
   - 在 LLM API 上设置支出限制

6. **定期更新**
   ```bash
   # 每周检查更新
   pip install --upgrade nanobot-ai
   ```

### 8. 开发与生产

**开发环境：**
- 使用独立的 API 密钥
- 使用非敏感数据进行测试
- 启用详细日志记录
- 使用测试 Telegram 机器人

**生产环境：**
- 使用具有支出限制的专用 API 密钥
- 限制文件系统访问
- 启用审计日志
- 定期进行安全审查
- 监控异常活动

### 9. 数据隐私

- **日志可能包含敏感信息** — 适当地保护日志文件
- **LLM 提供商会看到您的提示** — 审查其隐私政策
- **聊天历史记录存储在本地** — 保护 `~/.nanobot` 目录
- **API 密钥以明文存储** — 生产环境使用操作系统密钥环

### 10. 事件响应

如果您怀疑发生安全漏洞：

1. **立即撤销受损的 API 密钥**
2. **检查日志中的未授权访问**
   ```bash
   grep "Access denied" ~/.nanobot/logs/nanobot.log
   ```
3. **检查意外的文件修改**
4. **轮换所有凭据**
5. **更新到最新版本**
6. **向维护者报告事件**

## 安全功能

### 内置安全控制

✅ **输入验证**
- 文件操作的路径遍历保护
- 危险命令模式检测
- HTTP 请求的输入长度限制

✅ **身份验证**
- 基于允许列表的访问控制 — 在 `v0.1.4.post3` 及更早版本中，空的 `allowFrom` 允许所有人访问；自 `v0.1.4.post4` 起，它拒绝所有访问（`["*"]` 显式允许所有人）
- 失败的身份验证尝试记录

✅ **资源保护**
- 命令执行超时（默认 60 秒）
- 输出截断（10KB 限制）
- HTTP 请求超时（10-30 秒）

✅ **安全通信**
- 所有外部 API 调用使用 HTTPS
- Telegram API 使用 TLS
- WhatsApp 桥接器：仅限本地绑定 + 可选令牌身份验证

## 已知限制

⚠️ **当前安全限制：**

1. **无速率限制** — 用户可以发送无限数量的消息（如需要，请自行添加）
2. **明文配置** — API 密钥以明文存储（生产环境使用密钥环）
3. **无会话管理** — 无自动会话过期
4. **有限的命令过滤** — 仅阻止明显的危险模式（在 Linux 上启用 bwrap 沙箱以实现内核级隔离）
5. **无审计跟踪** — 有限的安全事件日志记录（根据需要增强）

## 安全检查清单

在部署 nanobot 之前：

- [ ] API 密钥安全存储（不在代码中）
- [ ] 配置文件权限设置为 0600
- [ ] 为所有通道配置 `allowFrom` 列表
- [ ] 以非 root 用户身份运行
- [ ] 在 Linux 部署上启用 Exec 沙箱（`"tools.exec.sandbox": "bwrap"`）
- [ ] 文件系统权限受到适当限制
- [ ] 依赖项更新到最新的安全版本
- [ ] 监控日志中的安全事件
- [ ] 在 API 提供商上配置速率限制
- [ ] 制定备份和灾难恢复计划
- [ ] 对自定义技能/工具进行安全审查

## 更新

**最后更新**：2026-04-05

获取最新的安全更新和公告，请查看：
- GitHub 安全建议：https://github.com/HKUDS/nanobot/security/advisories
- 发行说明：https://github.com/HKUDS/nanobot/releases

## 许可证

详细信息请参阅 LICENSE 文件。
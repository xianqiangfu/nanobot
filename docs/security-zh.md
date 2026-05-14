# 安全边界文档

## 概述

nanobot Agent 拥有显著的权限（文件系统、Shell、Web）。以下安全边界在修改相关代码时必须严格遵守。绕过这些边界可能导致安全漏洞、数据泄露或系统损坏。

## 工作空间限制机制

### 文件系统工具限制

所有文件系统工具（`read_file`、`write_file`、`edit_file`、`list_dir`）都必须通过 `_resolve_path()` 进行路径解析和验证。

**实现位置**：`nanobot/agent/tools/filesystem.py`

**验证逻辑**：
```python
def _resolve_path(self, path: str, allow_none: bool = False) -> Path:
    """
    解析路径并确保其在允许的目录内
    """
    # 1. 规范化路径
    # 2. 检查是否在 allowed_dir 下
    # 3. 允许的例外：媒体上传目录、extra_allowed_dirs
    # 4. 拒绝不符合要求的路径
```

**允许的路径**：
- 配置的工作空间目录（`allowed_dir`）
- 媒体上传目录（`get_media_dir()`）
- 额外的允许目录（`config.extra_allowed_dirs`）

**违规处理**：
- 首次违规：返回软错误 + 提示
- 重复违规：升级为更强硬的错误
- 在会话级别追踪违规计数

### Shell 工具限制

Shell 执行工具（`ExecTool`）也尊重工作空间限制。

**实现位置**：`nanobot/agent/tools/shell.py`

**验证逻辑**：
```python
def execute(self, command: str, working_dir: str | None = None):
    """
    执行 Shell 命令
    """
    if config.restrict_to_workspace and working_dir:
        # 检查 working_dir 是否在工作空间内
        if not self._is_in_workspace(working_dir):
            raise PermissionError("Command outside workspace")
```

**配置选项**：
- `restrict_to_workspace`：启用工作空间限制
- `allow_shell`：允许 Shell 执行

**违规处理**：
- 如果命令将在工作空间外执行，拒绝执行
- 在执行前进行检查，防止部分执行

### 规则

**任何新的路径处理逻辑必须：**
1. 通过 `_resolve_path()` 或执行等效的 `allowed_dir` 检查
2. 不得绕过路径验证
3. 处理符号链接（resolve 后进行检查）
4. 处理相对路径和绝对路径
5. 使用 `pathlib.Path` 而非字符串拼接

## SSRF 防护

### 验证机制

所有从 Agent 工具发出的 HTTP 请求都必须通过 `validate_url_target()` 验证。

**实现位置**：`nanobot/security/network.py`

**验证逻辑**：
```python
def validate_url_target(url: str, whitelist: list[str] | None = None):
    """
    验证 URL 目标是否安全
    """
    # 1. 解析 URL
    # 2. 提取 IP 地址
    # 3. 检查是否在被阻止的 CIDR 范围内
    # 4. 如果在白名单中，允许
    # 5. 否则拒绝
```

### 默认阻止的范围

**RFC1918 私有地址**：
- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

**链路本地地址**：
- `169.254.0.0/16`

**云元数据端点**：
- `169.254.169.254`（常见于 AWS、GCP、Azure）

**本地回环**：
- `127.0.0.0/8`
- `::1`

### 白名单机制

**配置位置**：`config.tools.ssrf_whitelist`

**格式**：CIDR 列表
```json
{
  "tools": {
    "ssrf_whitelist": [
      "192.168.1.0/24",
      "10.10.0.100"
    ]
  }
}
```

**加载时机**：配置加载时（`configure_ssrf_whitelist(cidrs)`）

### 受影响的工具

以下工具必须使用 SSRF 防护：
- `web_search`（通过 web fetch）
- `web_fetch`
- 任何 MCP 服务器的 HTTP 客户端
- 任何自定义网络工具

### 规则

**任何新的网络请求必须：**
1. 使用现有的 web fetch 工具或复制 `validate_url_target()` 检查
2. 不得添加直接的 `httpx.get()` / `requests.get()` 调用
3. 通过 `validate_url_target()` 验证所有 URL 目标
4. 正确处理 DNS 解析后的 IP 地址（CNAME、A 记录等）
5. 记录被阻止的请求（用于审计）

### 违规处理

- **首次违规**：返回非重试工具错误 + 边界说明
- **重复违规**：升级为更强硬的错误
- **永久阻止**：某些严重的违规类型（如元数据端点）

## Shell 沙箱

### 沙箱实现

**实现位置**：`nanobot/tools/sandbox.py`

**支持的沙箱后端**：
- `bwrap`（bubblewrap）：Linux 容器化隔离
- `none`：无沙箱（默认）

### 沙箱后端接口

每个沙箱后端必须实现：
```python
def _wrap_<name>(command: str, workspace: Path, cwd: Path | None) -> str:
    """
    包装命令以在沙箱中执行
    """
    # 返回包装后的命令字符串
```

### 沙箱限制

**bubblewrap 限制**：
- 网络隔离（可选）
- 文件系统只读/读写限制
- 用户/组隔离
- 进程命名空间隔离
- 挂载命名空间隔离

**无沙箱限制**：
- 工作空间限制（`restrict_to_workspace`）
- 运行在原生 Shell 中

### 规则

**添加新的沙箱后端必须：**
1. 实现 `_wrap_<name>(command, workspace, cwd) -> str`
2. 在 `_BACKENDS` 字典中注册
3. 提供足够的安全隔离
4. 处理错误情况（沙箱失败）
5. 支持不同操作系统（Windows、Linux、macOS）

### 沙箱配置

**配置选项**：
```json
{
  "tools": {
    "sandbox_backend": "bwrap",
    "sandbox_options": {
      "network": false,
      "readonly": true
    }
  }
}
```

## 其他安全边界

### 工具调用限制

**重复外部查找限制**：
- 限制相同工具的重复调用
- 防止无限循环或过度消耗资源
- 按会话级别追踪

**并发工具限制**：
- 某些工具只能串行执行
- `concurrency_safe` 标记

### 内存限制

**工具结果预算**：
- `max_tool_result_chars`：工具结果最大字符数
- 超过预算的结果会被截断
- 防止上下文窗口溢出

**上下文窗口限制**：
- `context_window_tokens`：上下文窗口令牌预算
- 超过预算的历史会被剪枝
- 确保角色交替有效

### 会话隔离

**会话密钥**：
- 每个会话有唯一的密钥
- 不同会话之间相互隔离
- 会话历史不会泄露

**待处理队列**：
- 每个会话有独立的待处理队列
- 消息不会混淆
- 最多缓存 20 条消息

### 认证和授权

**API 密钥管理**：
- 存储在 `~/.nanobot/config.json` 或环境变量
- 使用 `${VAR}` 语法引用
- 不会在日志中泄露

**渠道认证**：
- 每个渠道有自己的认证机制
- API 密钥不会被共享
- OAuth 令牌安全存储

## 安全审计

### 日志记录

**安全事件**：
- SSRF 违规
- 工作空间违规
- 沙箱失败
- 工具调用错误
- 认证失败

**日志格式**：
```
[INFO] Security violation: SSRF - URL blocked: 192.168.1.1
[WARN] Workspace violation: Attempt to access /etc/passwd
[ERROR] Sandbox failed: bubblewrap not available
```

### 审计建议

**定期检查**：
- 审查日志中的安全违规
- 检查配置文件中的敏感信息
- 验证白名单配置

**安全最佳实践**：
- 启用 `restrict_to_workspace`
- 配置 SSRF 白名单（最小必要范围）
- 使用沙箱（如果可用）
- 限制 Shell 执行
- 定期更新依赖
- 使用强密钥

## 安全漏洞报告

**如何报告**：
- 通过 GitHub Issues 报告
- 使用 `security` 标签
- 提供复现步骤
- 描述影响范围
- 建议修复方案

**响应时间**：
- 高危：24 小时内响应
- 中危：72 小时内响应
- 低危：1 周内响应

**奖励计划**：
nanobot 不提供官方赏金计划，但会认可和感谢安全研究人员的贡献。

## 安全检查清单

在提交任何涉及以下内容的代码更改前：

- [ ] 文件系统路径处理：使用 `_resolve_path()` 或等效检查
- [ ] 网络请求：通过 `validate_url_target()` 验证
- [ ] Shell 执行：检查工作空间限制
- [ ] 沙箱后端：实现 `_wrap_<name>()` 并注册
- [ ] 新工具：添加安全边界检查
- [ ] 敏感数据：避免在日志中泄露
- [ ] 配置变更：更新 schema 并验证
- [ ] 会话隔离：确保不同会话不会混淆
- [ ] 错误处理：不泄露敏感信息
- [ ] 权限提升：避免不必要的权限

## 总结

nanobot 的安全边界是为了保护：
1. 系统资源（文件系统、Shell）
2. 网络资源（SSRF 防护）
3. 用户数据（会话隔离）
4. 敏感信息（日志、配置）

任何绕过这些边界的更改都必须：
- 有充分的理由
- 经过安全审查
- 有适当的测试
- 更新文档

记住：安全是一个持续的过程，不是一次性的设置。
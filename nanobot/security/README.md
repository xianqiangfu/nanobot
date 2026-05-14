# 安全模块

本模块提供网络安全相关的工具和功能。

## 核心组件

### Network Security (`network.py`)

网络安全工具，提供：

- SSRF (Server-Side Request Forgery) 防护
- 内部 URL 检测
- DNS 解析验证
- 重定向目标检查

## SSRF 防护

### 功能

防止智能体访问内部网络资源：

```python
from nanobot.security import validate_url_target, contains_internal_url

# 验证 URL 是否安全
ok, error = validate_url_target("https://example.com")
if not ok:
    print(f"不安全的 URL: {error}")

# 检查命令是否包含内部 URL
if contains_internal_url("curl http://localhost:8080"):
    print("命令包含内部 URL")
```

### 默认阻止的网络

以下网络范围默认被阻止：

- `0.0.0.0/8` - 当前网络
- `10.0.0.0/8` - 私有网络
- `100.64.0.0/10` - 运营商级 NAT
- `127.0.0.0/8` - 回环地址
- `169.254.0.0/16` - 链路本地 / 云元数据
- `172.16.0.0/12` - 私有网络
- `192.168.0.0/16` - 私有网络
- `::1/128` - IPv6 回环
- `fc00::/7` - IPv6 唯一本地
- `fe80::/10` - IPv6 链路本地

## 白名单配置

### 配置允许的网络范围

```python
from nanobot.security import configure_ssrf_whitelist

# 允许 Tailscale 网络范围
configure_ssrf_whitelist([
    "100.64.0.0/10"
])
```

## API 参考

### validate_url_target(url: str)

验证 URL 目标是否安全：

- 检查协议（仅允许 http/https）
- 检查主机名
- 解析 DNS 并检查 IP 地址
- 返回 `(ok, error_message)`

```python
ok, error = validate_url_target("https://example.com")
# (True, "")

ok, error = validate_url_target("http://localhost:8080")
# (False, "Blocked: localhost resolves to private address 127.0.0.1")
```

### validate_resolved_url(url: str)

验证已解析的 URL（用于检查重定向）：

- 仅检查 IP 地址
- 跳过 DNS 解析
- 适用于重定向目标验证

```python
ok, error = validate_resolved_url("https://192.168.1.1/api")
# (False, "Redirect target is a private address: 192.168.1.1")
```

### contains_internal_url(command: str)

检查命令字符串是否包含指向内部网络的 URL：

- 使用正则表达式提取 URL
- 对每个 URL 调用 `validate_url_target`
- 返回 `True` 如果发现内部 URL

```python
if contains_internal_url("curl http://127.0.0.1/admin"):
    print("拒绝执行包含内部 URL 的命令")
```

### configure_ssrf_whitelist(cidrs: list[str])

配置 SSRF 白名单，允许特定的 CIDR 范围：

```python
configure_ssrf_whitelist([
    "100.64.0.0/10",  # Tailscale
    "10.100.0.0/16"   # 内网特定范围
])
```

## 使用场景

### Web 工具中的安全检查

```python
from nanobot.security import validate_url_target

async def web_fetch(url: str) -> str:
    ok, error = validate_url_target(url)
    if not ok:
        return f"安全错误: {error}"

    # 安全获取 URL
    return await fetch(url)
```

### Shell 命令中的安全检查

```python
from nanobot.security import contains_internal_url

async def exec_command(command: str) -> str:
    if contains_internal_url(command):
        return "错误: 命令包含内部网络地址"

    # 安全执行命令
    return await execute(command)
```

## 注意事项

- SSRF 防护是安全机制，不是功能限制
- 白名单应谨慎配置
- DNS 解析可能失败，需要正确处理
- 安全检查应在实际操作前进行
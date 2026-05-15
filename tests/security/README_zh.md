# 安全模块测试

本目录包含 nanobot 安全模块的测试。

## 测试内容

安全测试覆盖：

- **SSRF 防护** - 内部 URL 检测
- **URL 验证** - URL 目标验证
- **DNS 解析** - DNS 解析验证
- **白名单** - 白名单配置

## 测试文件

### 主要测试文件

- **network_test.py** - 网络安全测试
- **ssrf_test.py** - SSRF 防护测试

## 运行测试

### 运行所有安全测试

```bash
pytest tests/security/
```

### 带覆盖率运行

```bash
pytest tests/security/ --cov=nanobot.security --cov-report=term-missing
```

## 注意事项

- 测试所有被阻止的网络范围
- 测试白名单功能
- Mock DNS 解析

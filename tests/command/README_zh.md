# 命令路由测试

本目录包含 nanobot 内置命令的测试。

## 测试内容

命令测试覆盖以下功能：

- **命令路由** - 命令解析和分发
- **优先级命令** - `/stop`、`/restart` 等高优先级命令
- **精确匹配** - 精确命令匹配
- **前缀匹配** - 前缀命令匹配
- **拦截器** - 命令拦截器功能

## 测试文件

### 主要测试文件

- **路由器测试** - 测试 CommandRouter 功能
- **内置命令测试** - 测试所有内置命令
- **上下文测试** - 测试 CommandContext 处理

## 运行测试

### 运行所有命令测试

```bash
pytest tests/command/
```

### 运行特定测试

```bash
pytest tests/command/test_router.py::test_exact_match
pytest tests/command/test_builtin.py::test_stop_command
```

### 带覆盖率运行

```bash
pytest tests/command/ --cov=nanobot.command --cov-report=term-missing
```

## 测试场景

### 命令解析

测试命令字符串的正确解析：

```python
def test_command_parsing():
    ctx = parse_command("/echo hello")
    assert ctx.command == "echo"
    assert ctx.args == "hello"
```

### 命令路由

测试命令路由到正确的处理器：

```python
def test_command_routing():
    router = CommandRouter()
    router.register("/test", test_handler)
    result = router.route("/test arg1")
    assert result is not None
```

### 拦截器

测试命令拦截器功能：

```python
def test_interceptor():
    router = CommandRouter()
    router.add_interceptor(interceptor)
    result = router.route("/any command")
    assert interceptor.called
```

## Mock 使用

使用 Mock 模拟命令上下文和响应：

```python
from unittest.mock import Mock

ctx = Mock()
ctx.msg = InboundMessage(...)
ctx.session = Session(...)
```

## 注意事项

- 命令测试应该独立运行
- 测试所有内置命令
- 验证命令参数解析
- 测试错误处理

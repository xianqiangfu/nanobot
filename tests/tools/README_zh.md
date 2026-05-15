# 工具模块测试

本目录包含 nanobot 工具模块的测试。

## 测试内容

工具测试覆盖：

- **工具注册** - 工具注册和注销
- **工具执行** - 工具调用和结果
- **工具验证** - 参数验证
- **工具上下文** - 工具上下文处理

## 测试文件

### 主要测试文件

- **registry_test.py** - 工具注册表测试
- **filesystem_test.py** - 文件系统工具测试
- **shell_test.py** - Shell 工具测试
- **web_test.py** - Web 工具测试

## 运行测试

### 运行所有工具测试

```bash
pytest tests/tools/
```

### 带覆盖率运行

```bash
pytest tests/tools/ --cov=nanobot.agent.tools --cov-report=term-missing
```

## 注意事项

- Mock 文件系统操作
- Mock 外部 API 调用
- 测试沙箱模式

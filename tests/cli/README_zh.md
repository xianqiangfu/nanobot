# CLI 命令测试

本目录包含 nanobot 命令行界面的测试。

## 测试内容

CLI 测试覆盖以下功能：

- **命令解析** - 参数解析和验证
- **配置加载** - 配置文件读取和解析
- **模型管理** - 模型列表、切换等命令
- **交互式输入** - 用户输入处理
- **输出格式化** - 日志和输出格式

## 测试文件

### 主要测试文件

- **CLI 集成测试** - 测试完整 CLI 命令流程
- **模型命令测试** - 测试模型相关命令
- **配置命令测试** - 测试配置相关命令

## 运行测试

### 运行所有 CLI 测试

```bash
pytest tests/cli/
```

### 运行特定测试

```bash
pytest tests/cli/test_cli_commands.py::test_command
```

### 带覆盖率运行

```bash
pytest tests/cli/ --cov=nanobot.cli --cov-report=term-missing
```

## 测试环境

CLI 测试需要：

- 配置文件（测试用）
- 模拟的 LLM 提供商
- 测试用的工作目录

## Mock 使用

CLI 测试大量使用 Mock：

```python
from unittest.mock import AsyncMock, MagicMock

mock_provider = MagicMock()
mock_provider.complete = AsyncMock(return_value=response)
```

## 注意事项

- CLI 测试应该独立运行
- 避免修改实际配置文件
- 使用临时目录进行文件操作
- 清理测试环境

# 测试总览

本目录包含 nanobot 项目的所有测试。

## 目录结构

```
tests/
├── agent/              # Agent 核心测试
├── channels/           # 通道集成测试
├── providers/          # LLM 提供商测试
├── cli/                # CLI 命令测试
├── command/            # 内置命令测试
└── conftest.py         # pytest 配置
```

## 测试框架

- **pytest** - 测试框架
- **pytest-asyncio** - 异步测试支持
- **unittest.mock** - Mock 工具

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定模块的测试

```bash
pytest tests/agent/
pytest tests/channels/
pytest tests/providers/
```

### 运行特定测试函数

```bash
pytest tests/agent/test_runner_core.py::test_runner_preserves_reasoning_fields
```

### 查看测试覆盖

```bash
pytest --cov=nanobot
```

## 测试组织

### Agent 测试 (tests/agent/)
测试 agent 的核心功能：

- **AgentRunner** - 消息传递、迭代限制、超时处理
- **AgentLoop** - 循环逻辑、钩子执行、上下文构建
- **Memory** - 记忆存储、整合、恢复
- **SessionManager** - 会话管理、历史记录
- **Tools** - 工具注册、执行、作用域
- **Subagent** - 子代理创建和生命周期
- **MCP** - MCP 服务器连接和重试

### Channel 测试 (tests/channels/)
测试各个聊天平台的通道：

- **Telegram** - Telegram 通道集成
- **Discord** - Discord 通道集成
- **Slack** - Slack 通道集成
- **Feishu** - 飞书通道集成
- **WeChat** - 微信通道集成
- **WhatsApp** - WhatsApp 通道集成
- **WebSocket** - WebSocket 通道集成
- **Matrix** - Matrix 通道集成
- **QQ** - QQ 通道集成

### Provider 测试 (tests/providers/)
测试 LLM 提供商的实现：

- **Anthropic** - Claude 模型支持
- **OpenAI** - OpenAI 模型支持
- **Azure** - Azure OpenAI 支持
- **GitHub Copilot** - GitHub Copilot 支持
- **Gemini** - Google Gemini 支持

### CLI 测试 (tests/cli/)
测试命令行界面：

- **命令解析** - 参数解析和验证
- **交互式输入** - 用户输入处理
- **命令执行** - 各种命令的执行逻辑

## 测试配置

### conftest.py
包含所有测试共享的 fixtures 和配置：

- pytest 插件配置
- 异步测试模式设置
- 共享 fixtures（如消息总线、配置等）

## 编写测试

### 异步测试

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### 使用 Mock

```python
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_with_mock():
    mock_provider = MagicMock()
    mock_provider.chat_with_retry = AsyncMock(return_value="result")

    result = await function_with_provider(mock_provider)
    assert result == "result"
```

### 使用 Fixtures

```python
@pytest.fixture
def sample_config():
    return {"enabled": True, "port": 8765}

def test_with_fixture(sample_config):
    assert sample_config["enabled"] is True
```

## 测试最佳实践

1. **隔离性** - 每个测试应该独立运行
2. **清晰的命名** - 测试函数名应该描述测试内容
3. **适当的断言** - 使用具体的断言，而不是通用的
4. **Mock 外部依赖** - 避免依赖外部服务
5. **异步测试** - 使用 `@pytest.mark.asyncio` 标记异步测试
6. **参数化测试** - 使用 `@pytest.mark.parametrize` 测试多种情况
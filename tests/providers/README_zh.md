# 提供商测试

本目录包含各个 LLM 提供商的测试。

## 测试范围

### 提供商实现测试

测试各个 LLM 提供商的实现是否符合接口规范：

- **Anthropic** - Claude 模型（Claude 3 Opus, Sonnet, Haiku）
- **OpenAI** - GPT-4, GPT-3.5 等模型
- **Azure OpenAI** - Azure 托管的 OpenAI 模型
- **GitHub Copilot** - GitHub Copilot 模型
- **Google Gemini** - Gemini 模型

### 测试内容

#### 核心功能
- 消息发送和接收
- 流式响应处理
- 工具调用（function calling）
- 推理内容（reasoning_content）
- 思维块（thinking_blocks）
- 使用统计（usage）

#### 高级特性
- 提示缓存
- 重试逻辑
- 超时处理
- 错误处理
- 配置验证

#### 模型特定功能
- 系统提示
- 温度和其他参数
- 最大 token 限制
- 停止序列

## 运行测试

### 运行所有提供商测试

```bash
pytest tests/providers/
```

### 运行特定提供商测试

```bash
pytest tests/providers/test_anthropic_provider.py
pytest tests/providers/test_openai_provider.py
```

### 使用 verbose 模式

```bash
pytest tests/providers/ -v
```

## 测试模式

### Mock 测试

使用 mock 对象测试提供商逻辑，避免实际的 API 调用：

```python
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_provider_with_mock():
    mock_http = AsyncMock()
    mock_http.post.return_value = MockResponse(status_code=200, json_data={...})

    provider = Provider(config, http_client=mock_http)
    result = await provider.chat_with_retry(messages=[...])
    assert result.content is not None
```

### 参数化测试

测试不同的配置和参数组合：

```python
@pytest.mark.parametrize("temperature,max_tokens", [
    (0.7, 1000),
    (0.5, 2000),
    (1.0, 500),
])
async def test_provider_parameters(temperature, max_tokens):
    config = {..., "temperature": temperature, "max_tokens": max_tokens}
    provider = Provider(config)
    # 测试逻辑
```

### 集成测试

测试与实际提供商 API 的集成（需要 API 密钥）：

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_provider_real_api():
    # 需要设置环境变量 ANTHROPIC_API_KEY
    config = {"api_key": os.getenv("ANTHROPIC_API_KEY")}
    provider = AnthropicProvider(config)
    result = await provider.chat_with_retry(messages=[...])
    assert result.content is not None
```

## 测试覆盖

### 接口合规性
- 所有提供商必须实现 `LLMProvider` 接口
- 测试确保所有方法都存在并且签名正确

### 边界情况
- 空消息列表
- 超长消息
- 无效参数
- 网络错误
- API 错误响应

### 性能测试
- 响应时间
- 流式性能
- 内存使用

## 测试环境

### 环境变量

集成测试需要设置相应的 API 密钥：

```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export AZURE_API_KEY="your-key"
```

### 跳过集成测试

默认情况下跳过需要 API 密钥的集成测试：

```bash
pytest tests/providers/ -m "not integration"
```

## 注意事项

1. **API 密钥安全** - 不要在测试代码中硬编码 API 密钥
2. **成本控制** - 集成测试会产生 API 调用费用
3. **速率限制** - 注意提供商的速率限制
4. **网络稳定性** - 测试应该能处理网络不稳定的情况
5. **Mock 优先** - 优先使用 mock 测试，只在必要时使用集成测试
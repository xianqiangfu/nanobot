# 工具函数测试

本目录包含 nanobot 工具函数的测试。

## 测试内容

工具函数测试覆盖：

- **字符串处理** - 截断、格式化等
- **路径处理** - 路径解析、缩写等
- **Token 估算** - 消息 token 数估算
- **媒体处理** - 图片编码、解码等
- **辅助函数** - 通用辅助函数

## 测试文件

### 主要测试文件

- **truncate_text_test.py** - 文本截断测试
- **path_test.py** - 路径处理测试
- **token_test.py** - Token 估算测试
- **media_test.py** - 媒体处理测试
- **helpers_test.py** - 辅助函数测试

## 运行测试

### 运行所有工具测试

```bash
pytest tests/utils/
```

### 运行特定测试

```bash
pytest tests/utils/test_helpers.py::test_truncate_text
```

### 带覆盖率运行

```bash
pytest tests/utils/ --cov=nanobot.utils --cov-report=term-missing
```

## 测试示例

### 文本截断

```python
def test_truncate_text():
    text = "这是一段很长的文本..."
    result = truncate_text(text, max_length=10)
    assert len(result) <= 10
    assert result.endswith("...")
```

### 路径处理

```python
def test_abbreviate_path():
    path = "/home/user/projects/nanobot"
    result = abbreviate_path(path)
    assert result.startswith("~")
```

### Token 估算

```python
def test_estimate_tokens():
    messages = [{"role": "user", "content": "Hello"}]
    tokens = estimate_message_tokens(messages)
    assert tokens > 0
```

## 注意事项

- 工具函数应该是纯函数，易于测试
- 测试边界情况（空输入、极大输入等）
- 验证函数的正确性，不要过度测试

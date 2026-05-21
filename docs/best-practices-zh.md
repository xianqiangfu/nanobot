# nanobot 最佳实践指南

本文档介绍了 nanobot 开发和使用过程中的最佳实践，涵盖异步编程、错误处理、日志记录、代码风格、测试以及性能优化等方面。

## 异步编程最佳实践

### 1. 始终使用 async/await

nanobot 全面使用 asyncio，所有 I/O 操作都应该异步化：

```python
# 正确
async def fetch_data(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# 错误 - 阻塞调用
def fetch_data_sync(url: str) -> str:
    response = requests.get(url)  # 阻塞整个事件循环
    return response.text
```

### 2. 使用 asyncio.gather 并发执行

```python
# 并发执行多个异步操作
async def fetch_multiple(urls: list[str]) -> list[str]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### 3. 避免阻塞操作

```python
# 正确 - 使用异步文件操作
async def read_file(path: str) -> str:
    return await aiofiles.read_text(path)

# 错误 - 阻塞文件操作
def read_file_sync(path: str) -> str:
    return open(path).read()
```

## 错误处理模式

### 1. 捕获特定异常

```python
# 正确
try:
    result = await provider.chat(messages)
except httpx.TimeoutError as e:
    logger.warning("Request timeout: {}", e)
    # 重试逻辑
except httpx.HTTPStatusError as e:
    logger.error("HTTP error: {}", e)
    raise
except Exception as e:
    logger.error("Unexpected error", exc_info=True)
    raise
```

### 2. 使用结构化错误响应

```python
# 提供商应该返回结构化的错误响应
return LLMResponse(
    content="Error: rate limit exceeded",
    error_status_code=429,
    error_kind="rate_limit",
    error_should_retry=True,
    error_retry_after_s=60.0,
)
```

### 3. 重试策略

```python
# 使用 tenacity 实现重试
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
async def fetch_with_retry(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
```

## 日志记录规范

### 1. 使用 loguru

```python
from loguru import logger

logger.info("Starting operation")
logger.debug("Debug details: {}", details)
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
```

### 2. 结构化日志

```python
# 包含上下文信息
logger.info("Processing message", chat_id=chat_id, sender=sender_id, message_len=len(content))
```

### 3. 日志级别

| 级别 | 用途 |
|------|------|
| DEBUG | 详细的调试信息 |
| INFO | 正常的操作信息 |
| WARNING | 警告但不影响功能 |
| ERROR | 错误但可以恢复 |
| CRITICAL | 严重错误 |

## 代码风格指南

### 1. 行长度限制

```python
# 每行最多 100 个字符
very_long_function_name(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10)  # 错误

# 正确 - 多行写法
very_long_function_name(
    arg1, arg2, arg3, arg4,
    arg5, arg6, arg7, arg8,
    arg9, arg10,
)
```

### 2. 导入顺序

```python
# 标准库导入
import asyncio
from pathlib import Path

# 第三方导入
import httpx
from loguru import logger

# 本地导入
from nanobot.config import load_config
from nanobot.providers.base import LLMProvider
```

### 3. 代码检查

```bash
# 只使用 ruff check，不要使用 ruff format
ruff check nanobot/

# 自动修复可修复的问题
ruff check --fix nanobot/
```

## 测试覆盖率要求

### 1. 目标覆盖率

- **单元测试**：90%+ 覆盖率
- **集成测试**：80%+ 覆盖率
- **E2E 测试**：关键路径 100% 覆盖

### 2. 测试结构

```python
# tests/test_providers/test_anthropic.py
import pytest
from nanobot.providers.anthropic import AnthropicProvider

@pytest.mark.asyncio
async def test_chat_basic():
    """测试基本聊天功能。"""
    provider = AnthropicProvider(api_key="test-key")
    response = await provider.chat(
        messages=[{"role": "user", "content": "Hello"}],
    )
    assert response.content is not None
    assert response.finish_reason == "stop"
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 生成覆盖率报告
pytest --cov=nanobot --cov-report=html

# 只运行失败的测试
pytest --lf
```

## 性能优化建议

### 1. 提示词缓存

```python
# 在配置中启用提示词缓存
{
  "providers": {
    "openai": {
      "supportsPromptCaching": true
    }
  }
}
```

### 2. 会话压缩策略

```python
# 自动压缩历史
{
  "sessions": {
    "maxHistory": 100,
    "compressionThreshold": 50
  }
}
```

### 3. 并发控制

```python
# 限制并发请求数
import asyncio

async def process_with_limit(items: list, max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process(item):
        async with semaphore:
            return await process_item(item)
    
    return await asyncio.gather(*[process(item) for item in items])
```

### 4. 资源管理

```python
# 使用上下文管理器
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url)
    # 客户端自动关闭

# 使用连接池
client = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
)
```

### 5. 网络请求优化

```python
# 设置合理的超时
timeout = httpx.Timeout(10.0, connect=5.0)

# 使用 HTTP/2
async with httpx.AsyncClient(http2=True) as client:
    response = await client.get(url)
```

## 安全实践

### 1. API 密钥管理

```python
# 使用环境变量
import os

api_key = os.environ.get("API_KEY")

# 或使用配置文件
from nanobot.config import load_config

config = load_config()
api_key = config.providers.anthropic.api_key
```

### 2. 工作目录限制

```python
# 验证路径在工作目录内
from pathlib import Path

def ensure_safe_path(path: Path, workspace: Path) -> Path:
    resolved = path.resolve()
    if not str(resolved).startswith(str(workspace)):
        raise PermissionError(f"Path {path} is not within workspace")
    return resolved
```

### 3. SSRF 防护

```python
# 白名单允许的域名
ALLOWED_DOMAINS = ["example.com", "api.example.com"]

def is_allowed_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc in ALLOWED_DOMAINS
```

### 4. 命令执行安全

```python
# 使用参数化命令，避免命令注入
import shlex

def safe_command(command: str, args: list[str]) -> list[str]:
    cmd = shlex.split(command)
    return cmd + [shlex.quote(arg) for arg in args]
```

### 5. 文件访问控制

```python
# 验证文件路径
def validate_file_path(path: Path, allowed_dirs: list[Path]) -> bool:
    resolved = path.resolve()
    return any(str(resolved).startswith(str(d)) for d in allowed_dirs)
```

## 内存管理

### 1. 避免内存泄漏

```python
# 清理资源
async def process_large_file(path: Path):
    try:
        async with aiofiles.open(path) as f:
            async for line in f:
                await process_line(line)
    finally:
        # 确保资源被清理
        pass
```

### 2. 使用生成器

```python
# 处理大数据集时使用生成器
def process_lines(file_path: Path):
    with open(file_path) as f:
        for line in f:
            yield process_line(line)
```

## 并发处理注意事项

### 1. 避免竞争条件

```python
# 使用 asyncio.Lock
lock = asyncio.Lock()

async def shared_resource_operation():
    async with lock:
        # 安全地访问共享资源
        await update_shared_resource()
```

### 2. 使用队列协调任务

```python
queue = asyncio.Queue(maxsize=100)

async def producer():
    for item in items:
        await queue.put(item)

async def consumer():
    while True:
        item = await queue.get()
        await process_item(item)
        queue.task_done()
```

## Windows 兼容性

### 1. 路径处理

```python
# 使用 pathlib.Path
from pathlib import Path

path = Path("some/file.txt")
```

### 2. 文件编码

```python
# Windows 上强制 UTF-8
import sys

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
```

## 调试技巧

### 1. 使用断点

```python
import pdb; pdb.set_trace()
# 或
breakpoint()
```

### 2. 日志调试

```python
logger.debug("Variable value: {}", variable_value)
```

### 3. 性能分析

```bash
# 使用 cProfile
python -m cProfile -o profile.stats -m nanobot agent

# 使用 py-spy
py-spy top --pid <PID>
```

## 总结

遵循这些最佳实践可以：

- 提高代码质量和可维护性
- 避免常见的陷阱和错误
- 优化性能和资源使用
- 确保安全性和可靠性
- 简化调试和问题解决

记住：清晰的代码比聪明的代码更重要。保持代码简单、可读和可测试。

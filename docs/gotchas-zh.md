# 注意事项文档

## 概述

本文档记录了 nanobot 开发过程中的常见陷阱、Windows 兼容性注意事项、配置语法说明等关键信息。遵循这些指导可以避免常见错误并确保代码质量。

## 开发过程中的常见陷阱

### 1. 不要使用 `ruff format`

**问题**：`CONTRIBUTING.md` 中提到了 `ruff format`，但实际上**不应该运行它**。

**原因**：`ruff format` 会破坏 git blame 历史，使得追踪代码变更变得困难。

**解决方案**：只使用 `ruff check` 进行代码检查，不要使用格式化工具。

```bash
# 正确
ruff check nanobot/

# 错误 - 不要运行！
ruff format nanobot/
```

### 2. 配置 `${VAR}` 引用语法

**问题**：`config/loader.py` 在加载时解析 `config.json` 中的 `${VAR}` 模式。这**不是** Shell 风格的默认值语法。

**规则**：如果环境变量缺失，`load_config` 会引发 `ValueError`，Agent 会回退到默认配置。

**正确用法**：
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "${OPENROUTER_KEY}"
    }
  }
}
```

**错误用法**（不支持默认值）：
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "${OPENROUTER_KEY:-default}"  // 不支持
    }
  }
}
```

**行为**：
- 如果 `OPENROUTER_KEY` 存在：使用其值
- 如果 `OPENROUTER_KEY` 不存在：引发 `ValueError`，回退到默认配置

### 3. Prompt 模板修改的影响

**问题**：Agent 系统提示词和特定场景指令存储在 `nanobot/templates/` 中，修改这些文件会像修改 Python 代码一样直接影响 Agent 行为。

**模板文件**：
- `identity.md`：Agent 身份定义
- `platform_policy.md`：平台特定策略
- `HEARTBEAT.md`：心跳服务指令
- `SOUL.md`：Agent 性格定义
- 其他场景特定模板

**加载方式**：通过 `nanobot/utils/prompt_templates.py` 加载

**影响**：
- 修改模板会立即影响所有使用该模板的会话
- 不会在当前会话中生效（需要新会话）
- 可能影响 Agent 的工具使用和对话模式

**建议**：
- 像对待运行时代码一样对待模板更改
- 保持更改狭窄和专注
- 添加回归测试（如果可能）
- 避免教导模型重复内部标记、本地路径或工具调用文本

### 4. 上下文污染持久性

**问题**：任何写入内存、会话历史或提示输入的内容都可以在未来的 LLM 调用中重放。

**污染源**：
- 时间戳
- 本地媒体路径
- 工具调用回显
- 原始回退转储
- 其他元数据

**影响**：
- 模型可能模仿污染的内容
- 上下文窗口可能被污染数据填充
- 用户可能看到敏感的内部信息

**解决方案**：
- 在成为模型示例之前，对元数据进行边界和清理
- 对敏感信息进行截断或遮蔽
- 使用摘要而非原始数据
- 定期清理会话历史

### 5. Heartbeat 虚拟工具调用模式

**问题**：心跳服务（`heartbeat/service.py`）不解析自由文本 LLM 输出。

**实现方式**：
- 注入虚拟 `heartbeat` 工具到对话中
- 工具有 `action: skip | run` 参数
- 第一阶段：结构化决策
- 第二阶段：仅在 `run` 时执行

**示例**：
```python
{
  "role": "assistant",
  "tool_use": [
    {
      "name": "heartbeat",
      "input": {"action": "run"}
    }
  ]
}
```

**建议**：
- 添加新的定期后台检查时，遵循此虚拟工具调用模式
- 不要使用字符串匹配
- 保持工具调用结构化

### 6. Skills 作为扩展点

**内置技能**：存储在 `nanobot/skills/` 中

**格式**：Markdown + YAML 前置数据
```markdown
---
name: "example_skill"
description: "Example skill description"
---

技能内容...
```

**建议**：
- "Know-how" 而非代码的能力应该添加为技能
- 不要硬编码到 Agent 循环中
- 外部技能可以发布到 ClawHub 并从中安装

### 7. 原子会话写入

**实现位置**：`nanobot/agent/memory.py`

**写入流程**：
```python
# 1. 写入临时文件
with open(tmp_path, "w") as f:
    json.dump(data, f)
    f.flush()
    os.fsync(f.fileno())

# 2. 原子重命名
os.rename(tmp_path, target_path)

# 3. 目录 fsync
dirfd = os.open(dir_path, os.O_RDONLY)
os.fsync(dirfd)
os.close(dirfd)
```

**保证**：
- 崩溃恢复一致性
- 无数据损坏
- 无历史丢失

**规则**：
- 不要用普通的 `open(..., "w")` 写入替换此机制
- 使用提供的 `save_session()` 方法
- 确保会话持久化使用原子写入

### 8. 最小变更解决真实问题

**问题**：修复 Bug 时应该只更改必要的内容。

**规则**：
- 不要将不相关的重构或清理捆绑到功能或 bugfix PR 中
- 如果确实需要重构，应该是针对 `nightly` 分支的单独 PR
- 保持变更聚焦和可审查

### 9. 保持 PR 可审查

**原则**：
- Bugfix 应该使受保护的不变量清晰
- 更改强制执行该不变量的最小表面
- 仅添加最近的回归测试

**警告信号**：
- 差异开始更改所有权边界
- 将行为更改与清理混合
- 变更难以理解

**解决方案**：
- 在变得难以审查之前拆分
- 分离不同类型的更改
- 保持 PR 聚焦

## Windows 兼容性注意事项

nanobot 明确支持 Windows，但有一些关键差异需要注意。

### 1. Shell 命令执行

**问题**：`ExecTool` 在 Windows 上使用 `cmd /c` 而非 `sh -c`。

**实现位置**：`nanobot/agent/tools/shell.py`

**差异**：
- 命令语法不同（`dir` vs `ls`，`type` vs `cat`）
- 环境变量语法不同（`%VAR%` vs `$VAR`）
- 路径分隔符不同（`\` vs `/`）

**建议**：
- 使用跨平台命令（`python`、`npm`、`bun`）
- 避免使用特定平台的命令
- 测试脚本在两个平台上的兼容性

### 2. 输出编码

**问题**：CLI 命令在启动时强制 `sys.stdout`/`stderr` 为 UTF-8。

**实现位置**：`nanobot/cli/commands.py`

```python
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
```

**影响**：
- 处理 emoji 和多语言输入
- 确保输出一致

### 3. MCP stdio 服务器命令

**问题**：MCP stdio 服务器命令为 Windows 路径分隔符进行规范化。

**实现位置**：`nanobot/agent/tools/mcp.py`

**差异**：
- 命令中的路径需要规范化
- 正斜杠和反斜杠的处理

**建议**：
- 使用 `pathlib.Path` 处理路径
- 避免硬编码路径分隔符

### 4. 路径处理

**规则**：
- 始终使用 `pathlib.Path` 进行路径操作
- 不要假设 `/` 分隔符
- 使用 `Path.as_posix()` 进行显示
- 使用 `Path.resolve()` 规范化路径

**示例**：
```python
# 正确
from pathlib import Path
path = Path("some/path") / "file.txt"
resolved = path.resolve()

# 错误
path = "some/path/file.txt"  # 跨平台问题
```

### 5. 文件锁定

**问题**：Windows 上的文件锁定更严格。

**影响**：
- 原子写入可能失败（文件被锁定）
- 需要更谨慎的错误处理

**建议**：
- 使用临时文件 + 重命名模式
- 捕获权限错误
- 提供有用的错误消息

### 6. 进程管理

**差异**：
- 进程创建 API 不同
- 信号处理不同
- 进程组管理不同

**建议**：
- 使用 `asyncio.create_subprocess_exec` 而非 `os.system`
- 避免依赖 Unix 特定的信号
- 测试进程创建和终止

### 7. 权限和权限位

**问题**：Windows 不支持 Unix 风格的权限位。

**差异**：
- 没有 `chmod`
- 权限通过 ACL 管理
- 文件属性不同

**建议**：
- 避免使用 `os.chmod` 和 `stat` 模块
- 使用 `pathlib.Path` 的高层方法
- 提供跨平台的行为

### 8. 临时文件

**差异**：
- 临时目录位置不同
- 清理行为不同

**建议**：
- 使用 `tempfile` 模块
- 使用 `tempfile.mkstemp()` 或 `tempfile.TemporaryDirectory()`
- 正确清理临时文件

## 配置引用语法说明

### `${VAR}` 语法

**用途**：在 `config.json` 中引用环境变量。

**解析时机**：配置加载时（`config/loader.py`）

**规则**：
- 如果环境变量存在：使用其值
- 如果环境变量不存在：引发 `ValueError`，回退到默认配置
- 不支持默认值语法（如 `${VAR:-default}`）

**示例**：
```json
{
  "providers": {
    "openai": {
      "apiKey": "${OPENAI_API_KEY}",
      "baseUrl": "${OPENAI_BASE_URL:https://api.openai.com/v1}"  // 错误 - 不支持
    }
  }
}
```

**正确使用**：
```bash
# 设置环境变量
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"

# 配置文件
{
  "providers": {
    "openai": {
      "apiKey": "${OPENAI_API_KEY}",
      "baseUrl": "${OPENAI_BASE_URL}"
    }
  }
}
```

### 配置加载顺序

1. 读取 `~/.nanobot/config.json`
2. 解析 `${VAR}` 引用
3. 验证 Pydantic 模型
4. 应用 camelCase 别名
5. 如果失败，回退到默认配置

### camelCase 支持

**用途**：支持 JSON 的 camelCase 属性名。

**实现**：Pydantic 模型的字段别名。

**示例**：
```json
{
  "maxIterations": 10,
  "maxMessages": 100,
  "contextWindowTokens": 200000
}
```

**映射到 Python**：
```python
max_iterations: int
max_messages: int
context_window_tokens: int
```

### 配置验证

**验证器**：`nanobot/config/schema.py`

**错误处理**：
- 类型错误：引发 `ValidationError`
- 缺失字段：使用默认值
- 无效值：引发 `ValidationError`

**建议**：
- 使用 Pydantic 模型确保类型安全
- 为可选字段提供默认值
- 验证配置格式

## 常见错误和解决方案

### 错误 1：路径不在工作空间内

**错误消息**：
```
PermissionError: Path /etc/passwd is not within the allowed workspace
```

**原因**：文件系统工具检查工作空间限制

**解决方案**：
- 检查 `allowed_dir` 配置
- 使用 `extra_allowed_dirs` 添加额外目录
- 确保路径在允许的目录内

### 错误 2：SSRF 防护阻止请求

**错误消息**：
```
SecurityError: URL target 192.168.1.1 is blocked by SSRF protection
```

**原因**：URL 目标在阻止的 CIDR 范围内

**解决方案**：
- 检查 `ssrf_whitelist` 配置
- 添加必要的 CIDR 到白名单
- 避免访问内部网络

### 错误 3：配置变量未定义

**错误消息**：
```
ValueError: Environment variable OPENAI_API_KEY is not defined
```

**原因**：`${VAR}` 引用的环境变量未设置

**解决方案**：
- 设置环境变量
- 在配置文件中使用硬编码值（不推荐）
- 使用默认配置

### 错误 4：上下文窗口溢出

**错误消息**：
```
ContextError: Context exceeds context_window_tokens limit
```

**原因**：会话历史超过令牌预算

**解决方案**：
- 增加 `context_window_tokens`
- 启用自动压缩
- 减少会话历史

### 错误 5：工具结果超过预算

**错误消息**：
```
ToolError: Tool result exceeds max_tool_result_chars limit
```

**原因**：工具输出超过字符预算

**解决方案**：
- 增加 `max_tool_result_chars`
- 使用持久化大型结果
- 截断工具输出

## 性能注意事项

### 1. 异步 I/O

**原则**：nanobot 全面使用 asyncio。

**建议**：
- 使用 `async`/`await` 而非同步调用
- 使用 `asyncio.gather()` 并发执行
- 避免阻塞调用

### 2. 内存管理

**关注点**：
- 会话历史大小
- 工具结果大小
- 媒体文件缓存

**建议**：
- 定期清理旧会话
- 持久化大型工具结果
- 限制缓存大小

### 3. 网络请求

**建议**：
- 使用 `httpx` 异步客户端
- 设置合理的超时
- 重试失败的请求

### 4. 文件 I/O

**建议**：
- 使用异步文件 I/O
- 批量操作（如果可能）
- 使用临时文件 + 重命名

## 测试注意事项

### 1. 测试隔离

**原则**：每个测试应该独立。

**建议**：
- 使用临时目录
- 清理资源
- 使用 fixture

### 2. 异步测试

**配置**：`asyncio_mode = "auto"`

**示例**：
```python
@pytest.mark.asyncio
async def test_something():
    result = await async_function()
    assert result == expected
```

### 3. Mock 外部依赖

**建议**：
- Mock 网络请求
- Mock 文件系统
- Mock LLM 调用

### 4. 测试覆盖率

**目标**：80%+ 覆盖率（单元、集成、E2E）

**建议**：
- 使用 pytest-cov
- 定期检查覆盖率
- 添加缺失的测试

## 调试技巧

### 1. 日志配置

**配置**：`~/.nanobot/config.json`
```json
{
  "logging": {
    "level": "DEBUG",
    "file": "/path/to/logfile.log"
  }
}
```

### 2. 调试模式

**启用**：设置 `DEBUG=1` 环境变量

**影响**：
- 更详细的日志
- 堆栈跟踪
- 额外验证

### 3. 断点

**使用**：
```python
import pdb; pdb.set_trace()
# 或
import ipdb; ipdb.set_trace()
```

### 4. 性能分析

**工具**：
- `cProfile`
- `py-spy`
- `memory_profiler`

## 总结

遵循这些注意事项可以：
- 避免常见陷阱
- 确保跨平台兼容性
- 正确使用配置
- 提高代码质量
- 简化调试

记住：nanobot 是一个轻量级框架，保持代码简单和可读是关键。
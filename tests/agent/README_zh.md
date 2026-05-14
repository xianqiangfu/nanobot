# Agent 测试

本目录包含 nanobot agent 核心功能的测试。

## 测试范围

### 核心组件测试

#### AgentRunner
- `test_runner_core.py` - 核心运行器行为
- `test_runner_errors.py` - 错误处理
- `test_runner_fallback.py` - 模型故障转移
- `test_runner_governance.py` - 运行时治理
- `test_runner_hooks.py` - 钩子执行
- `test_runner_injections.py` - 消息注入
- `test_runner_persistence.py` - 持久化
- `test_runner_progress_deltas.py` - 进度增量
- `test_runner_reasoning.py` - 推理内容处理
- `test_runner_safety.py` - 安全检查
- `test_runner_tool_execution.py` - 工具执行

#### AgentLoop
- `test_loop_consolidation_tokens.py` - 整合 token 限制
- `test_loop_cron_timezone.py` - Cron 时区处理
- `test_loop_image_generation_media.py` - 图片生成媒体
- `test_loop_progress.py` - 进度报告
- `test_loop_runner_integration.py` - 与 Runner 集成
- `test_loop_save_turn.py` - 轮次保存
- `test_loop_tool_context.py` - 工具上下文

#### Memory
- `test_memory_store.py` - 记忆存储
- `test_dream.py` - Dream 记忆整合
- `test_consolidator.py` - 整合器
- `test_consolidate_offset.py` - 整合偏移量
- `test_consolidation_ratio.py` - 整合比率
- `test_auto_compact.py` - 自动压缩
- `test_autocompact_unit.py` - 自动压缩单元测试

#### Session Management
- `test_session_manager_history.py` - 会话历史管理
- `test_session_atomic.py` - 会话原子操作
- `test_session_delete.py` - 会话删除
- `test_unified_session.py` - 统一会话
- `test_cursor_recovery.py` - 游标恢复

### 工具测试

#### Tool Registry
- `test_tool_loader_entrypoints.py` - 入口点加载
- `test_tool_loader_scopes.py` - 作用域管理
- `test_skill_creator_scripts.py` - Skill 创建脚本

#### Built-in Tools
- `test_self_tool.py` - my 工具
- `test_self_tool_runtime_sync.py` - my 工具运行时同步
- `test_subagent_tools.py` - 子代理工具
- `test_dream_tools.py` - Dream 工具
- `test_tool_hint.py` - 工具提示

### MCP 测试

- `test_mcp_connection.py` - MCP 服务器连接
- `test_mcp_transient_retry.py` - MCP 临时重试

### 其他功能测试

- `test_context_builder.py` - 上下文构建
- `test_context_aware.py` - 上下文感知
- `test_context_prompt_cache.py` - 提示缓存
- `test_evaluator.py` - 评估器
- `test_heartbeat_service.py` - 心跳服务
- `test_hook_composite.py` - 复合钩子
- `test_onboard_logic.py` - 入站逻辑
- `test_runtime_refresh.py` - 运行时刷新
- `test_self_model_preset.py` - 自模型预设
- `test_skills_loader.py` - Skills 加载器
- `test_stop_preserves_context.py` - 停止保留上下文
- `test_subagent.py` - 子代理
- `test_subagent_lifecycle.py` - 子代理生命周期
- `test_task_cancel.py` - 任务取消
- `test_max_messages_config.py` - 最大消息配置
- `test_gemini_thought_signature.py` - Gemini 思维签名
- `test_git_store.py` - Git 存储

## 运行测试

### 运行所有 Agent 测试

```bash
pytest tests/agent/
```

### 运行特定测试文件

```bash
pytest tests/agent/test_runner_core.py
```

### 运行特定测试函数

```bash
pytest tests/agent/test_runner_core.py::test_runner_preserves_reasoning_fields
```

### 查看输出

```bash
pytest tests/agent/ -v
```

## 测试工具

### Fixtures (conftest.py)

共享的 fixtures 包括：
- `mock_provider` - Mock 的 LLM 提供商
- `mock_tools` - Mock 的工具注册表
- `mock_bus` - Mock 的消息总线
- `sample_config` - 示例配置

## 测试模式

### 异步测试

所有测试都使用 `@pytest.mark.asyncio` 标记：

```python
@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result is not None
```

### Mock 使用

使用 `unittest.mock` 进行隔离测试：

```python
from unittest.mock import AsyncMock, MagicMock

mock_provider = MagicMock(spec=LLMProvider)
mock_provider.chat_with_retry = AsyncMock(return_value=LLMResponse(...))
```

## 覆盖率目标

- 核心组件覆盖率目标：80%+
- 关键路径覆盖率：90%+
- 错误处理路径：100%
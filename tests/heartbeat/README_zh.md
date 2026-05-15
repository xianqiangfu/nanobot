# 心跳服务测试

本目录包含 nanobot 心跳服务的测试。

## 测试内容

心跳服务测试覆盖：

- **决策阶段** - LLM 决策逻辑
- **执行阶段** - 任务执行
- **定时器** - 定时触发
- **状态管理** - 服务状态

## 测试文件

### 主要测试文件

- **heartbeat_service_test.py** - 心跳服务测试
- **decision_test.py** - 决策逻辑测试

## 运行测试

### 运行所有心跳测试

```bash
pytest tests/heartbeat/
```

### 带覆盖率运行

```bash
pytest tests/heartbeat/ --cov=nanobot.heartbeat --cov-report=term-missing
```

## 注意事项

- Mock LLM 提供商避免实际调用
- 测试决策和执行的分离

# 定时任务测试

本目录包含 nanobot 定时任务服务的测试。

## 测试内容

定时任务测试覆盖：

- **任务创建** - 创建新的定时任务
- **调度逻辑** - 任务调度和触发
- **任务执行** - 任务执行和结果处理
- **持久化** - 任务存储和恢复
- **错误处理** - 执行失败处理

## 测试文件

### 主要测试文件

- **cron_service_test.py** - 定时服务测试
- **schedule_test.py** - 调度逻辑测试
- **storage_test.py** - 持久化测试

## 运行测试

### 运行所有定时任务测试

```bash
pytest tests/cron/
```

### 带覆盖率运行

```bash
pytest tests/cron/ --cov=nanobot.cron --cov-report=term-missing
```

## 注意事项

- 使用时间旅行测试调度逻辑
- Mock 文件系统避免实际 I/O
- 测试并发执行

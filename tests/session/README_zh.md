# 会话管理测试

本目录包含 nanobot 会话管理的测试。

## 测试内容

会话测试覆盖：

- **会话创建** - 创建新会话
- **会话存储** - 会话数据持久化
- **会话检索** - 查询会话
- **会话更新** - 更新会话
- **会话删除** - 删除会话
- **TTL 管理** - 会话过期

## 测试文件

### 主要测试文件

- **session_manager_test.py** - 会话管理器测试
- **storage_test.py** - 存储测试

## 运行测试

### 运行所有会话测试

```bash
pytest tests/session/
```

### 带覆盖率运行

```bash
pytest tests/session/ --cov=nanobot.session --cov-report=term-missing
```

## 注意事项

- 使用临时目录进行测试
- 测试文件锁和并发
- 验证 fsync 确保持久化

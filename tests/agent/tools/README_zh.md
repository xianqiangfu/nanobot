# Agent 工具测试

本目录包含 agent 工具的测试。

## 测试内容

Agent 工具测试覆盖：

- **MyTool** - 自我修改工具测试
- **Subagent Tools** - 子代理工具测试

## 测试文件

### 主要测试文件

- **test_self_tool.py** - MyTool 功能测试
- **test_subagent_tools.py** - 子代理工具测试

## 运行测试

### 运行所有 agent 工具测试

```bash
pytest tests/agent/tools/
```

### 运行特定测试

```bash
pytest tests/agent/tools/test_self_tool.py
```

## 注意事项

- 测试工具的安全限制
- Mock 文件系统操作

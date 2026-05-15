# 配置系统测试

本目录包含 nanobot 配置系统的测试。

## 测试内容

配置测试覆盖：

- **配置加载** - 从文件加载配置
- **环境变量** - 环境变量覆盖
- **配置验证** - Pydantic 验证
- **默认值** - 默认值合并
- **错误处理** - 无效配置处理

## 测试文件

### 主要测试文件

- **config_loader_test.py** - 配置加载器测试
- **schema_test.py** - 配置 schema 测试
- **env_test.py** - 环境变量测试

## 运行测试

### 运行所有配置测试

```bash
pytest tests/config/
```

### 带覆盖率运行

```bash
pytest tests/config/ --cov=nanobot.config --cov-report=term-missing
```

## 注意事项

- 使用临时配置文件进行测试
- 验证所有必需字段
- 测试错误配置的处理

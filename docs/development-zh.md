# nanobot 开发指南

本指南介绍如何搭建 nanobot 的本地开发环境、进行调试、编写测试以及贡献代码。

## 开发环境搭建

### 系统要求

- **Python 版本**：Python 3.11 或更高版本
- **操作系统**：Linux、macOS、Windows
- **Git**：用于克隆仓库和版本控制
- **Node.js**：18+（用于 WebUI 开发）

### 克隆仓库

```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
```

### 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## 项目结构

```
nanobot/
├── nanobot/              # 主包
│   ├── agent/            # Agent 核心逻辑
│   ├── api/              # HTTP API 服务器
│   ├── bus/              # 消息总线
│   ├── channels/         # 聊天通道
│   ├── cli/              # CLI 命令
│   ├── config/           # 配置管理
│   ├── providers/        # LLM 提供商
│   └── utils/            # 工具函数
├── webui/                # WebUI 前端
├── tests/                # 测试文件
└── docs/                 # 文档
```

## 开发工作流

### 分支策略

```bash
main          # 稳定版本
feature/*     # 新功能开发
fix/*         # 错误修复
```

### 提交消息规范

使用 Conventional Commits 格式：

```
feat: add new feature
fix: resolve bug
docs: update documentation
```

## 调试技巧

### 日志调试

```python
from loguru import logger
logger.debug("Debug information")
logger.info("Starting operation")
logger.error("Error occurred", exc_info=True)
```

### 配置日志级别

```bash
export NANOBOT_LOG_LEVEL=DEBUG
nanobot agent
```

## 测试编写

### 基本测试

```python
import pytest

@pytest.mark.asyncio
async def test_my_function():
    result = await my_async_function()
    assert result is not None
```

### 运行测试

```bash
pytest
pytest -v
pytest --cov=nanobot
```

## 代码贡献流程

1. Fork 仓库
2. 创建功能分支
3. 进行开发
4. 提交更改
5. 创建 Pull Request

## 常见问题

### 依赖安装失败

```bash
pip install --upgrade pip
pip cache purge
```

### 配置文件问题

```bash
# 验证配置文件
python -c "import json; json.load(open('~/.nanobot/config.json'))"
```

## 获取帮助

- GitHub Issues: https://github.com/HKUDS/nanobot/issues
- 文档: https://nanobot.wiki

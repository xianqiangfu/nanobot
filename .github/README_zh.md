# GitHub 配置目录

本目录包含 GitHub 相关的 CI/CD 配置和 issue 模板。

## 目录结构

```
.github/
├── workflows/
│   └── ci.yml               # 持续集成测试工作流
└── ISSUE_TEMPLATE/
    ├── bug_report.yml       # Bug 报告模板
    ├── feature_request.yml  # 功能请求模板
    └── config.yml           # 配置说明
```

## CI/CD 工作流

### ci.yml

在 push 到 `main` 或 `nightly` 分支，以及针对这些分支的 PR 时触发。

**矩阵配置**：
- **操作系统**：PR 仅测试 Ubuntu，push 测试 Ubuntu 和 Windows
- **Python 版本**：PR 测试 3.11 和 3.14，push 测试 3.11、3.12、3.13 和 3.14

**测试步骤**：
1. 检出代码
2. 设置 Python 环境
3. 安装 uv
4. 安装系统依赖（Linux）
5. 同步所有依赖（`uv sync --all-extras`）
6. 使用 ruff 进行代码检查
7. 运行 pytest 测试套件

**超时**：20 分钟

**并发控制**：相同工作流的相同 ref 会取消进行中的运行

## Issue 模板

### bug_report.yml

用于报告 bug 或意外行为。

**必填字段**：
- Bug 描述
- 重现步骤
- 预期行为
- nanobot 版本
- Python 版本
- 操作系统
- 聊天平台/通道
- LLM 提供商

**可选字段**：
- 相关日志
- 配置片段
- 额外上下文

### feature_request.yml

用于提出新功能请求。

### config.yml

包含 issue 模板的配置说明。

## 注意事项

1. **敏感信息** - 在提交 issue 或 PR 时，务必移除 API 密钥、密码等敏感信息
2. **日志级别** - 运行 `nanobot --log-level DEBUG` 获取更详细的日志
3. **版本信息** - 使用 `nanobot --version` 或 `pip show nanobot-ai` 获取版本信息

## 贡献指南

在提交 PR 之前，确保：

1. 代码通过 ruff 检查
2. 所有测试通过
3. Python 3.11+ 兼容
4. Windows 和 Linux 平台测试通过（如适用）

## 相关资源

- [CONTRIBUTING.md](../CONTRIBUTING.md) - 贡献指南
- [开发者指南](../docs/developer-guide-zh.md) - 开发相关文档
- [测试文档](../tests/README_zh.md) - 测试体系说明
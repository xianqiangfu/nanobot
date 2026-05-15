# Agent 设计约束与安全边界

本目录包含 nanobot agent 的核心设计约束和安全边界文档。

## 目录结构

```
.agent/
├── design.md       # 设计约束
├── gotchas.md      # 常见陷阱
└── security.md     # 安全边界
```

## 文档说明

### design.md - 设计约束

定义了 nanobot 架构决策必须遵循的核心规则：

- **核心保持简洁，在边缘扩展** - 新功能通过 channels、tools、skills 或 MCP 服务器添加
- **结构少一点，智能多一点** - 优先考虑简洁可读的代码，而不是新的框架层
- **优先考虑重复，而非过早抽象** - 允许通道和提供商重复类似逻辑
- **最小化更改** - 仅更改必要的代码来修复 bug
- **保持 PR 可审查** - 单一焦点，清晰的受保护不变量
- **显式优于魔法** - 配置必须显式声明在 Pydantic 模型中

### gotchas.md - 常见陷阱

开发过程中需要注意的常见问题：

- **不要使用 `ruff format`** - 会破坏 git blame 历史
- **配置 `${VAR}` 引用** - 在加载时解析，不是 shell 默认值语法
- **Windows 兼容性** - 使用 `pathlib.Path`，注意路径分隔符
- **提示词模板** - 修改这些文件直接影响 agent 行为
- **上下文污染持续存在** - 元数据必须受到限制和清理
- **心跳虚拟工具调用** - 使用结构化决策，而非字符串匹配
- **Skills 作为扩展点** - "know-how" 类型的能力应该作为 skills 添加
- **原子会话写入** - 保留现有的原子写入模式

### security.md - 安全边界

定义了 agent 操作的安全边界：

- **工作空间限制** - 文件系统和 shell 工具必须检查允许的目录
- **SSRF 保护** - 所有出站 HTTP 请求必须通过 `validate_url_target`
- **Shell 沙箱** - 可选的命令包装，目前支持 bwrap（bubblewrap）

## 使用指南

这些文档在开发过程中应作为参考：

1. 在添加新功能前，阅读 `design.md` 确保符合架构约束
2. 在编写代码时，参考 `gotchas.md` 避免常见陷阱
3. 在处理安全敏感代码时，遵循 `security.md` 中的规则

## 相关资源

- [架构分析文档](../docs/architecture-zh.md)
- [安全文档](../docs/security-zh.md)
- [开发指南](../docs/developer-guide-zh.md)
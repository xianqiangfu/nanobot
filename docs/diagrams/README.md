# 架构图索引

本目录包含 nanobot 项目的完整架构图系列，使用 Mermaid 语法编写。

## 架构图列表

| 图表 | 文件 | 说明 |
|------|------|------|
| 项目整体架构图 | [overall-architecture.md](./overall-architecture.md) | 完整的系统架构，展示所有模块和它们的交互关系 |
| 核心模块依赖关系图 | [core-dependencies.md](./core-dependencies.md) | 核心模块之间的依赖关系 |
| 消息流转架构图 | [message-flow.md](./message-flow.md) | 消息在系统中的完整流转过程 |
| Agent 循环状态机图 | [agent-state-machine.md](./agent-state-machine.md) | Agent 循环的状态机和状态转换 |
| 通道插件架构图 | [channel-plugin.md](./channel-plugin.md) | 通道插件化架构和通道生命周期 |
| 工具系统架构图 | [tool-system.md](./tool-system.md) | 工具注册、发现和执行机制 |
| 提供商抽象架构图 | [provider-abstraction.md](./provider-abstraction.md) | LLM 提供商的统一抽象和选择流程 |
| 会话管理架构图 | [session-management.md](./session-management.md) | 会话管理、存储和生命周期 |
| Memory 系统架构图 | [memory-system.md](./memory-system.md) | Dream 两阶段记忆合并机制 |
| WebUI 网关架构图 | [webui-gateway.md](./webui-gateway.md) | WebUI 前端和网关的交互架构 |

## 使用说明

### 在 Markdown 中使用

```markdown
查看项目整体架构：

![项目整体架构](./diagrams/overall-architecture.md)
```

### 在 GitHub 中渲染

GitHub 原生支持 Mermaid 图表，直接在 Markdown 中使用 mermaid 代码块即可渲染。

### 在本地预览

使用支持 Mermaid 的 Markdown 预览工具，如：
- VS Code + Mermaid 插件
- Typora
- Obsidian

## 设计说明

所有架构图遵循以下设计原则：

- **清晰性** - 使用简化的视图展示关键概念
- **一致性** - 统一的命名和配色方案
- **完整性** - 覆盖系统的主要方面
- **可维护性** - 易于理解和更新

## 相关文档

- [架构分析文档](../architecture-zh.md)
- [设计原理文档](../design-principles-zh.md)
- [技术栈文档](../tech-stack-zh.md)
# 业务流程图索引

本目录包含 nanobot 项目关键业务流程的流程图，使用 Mermaid 语法编写。

## 流程图列表

| 流程图 | 文件 | 说明 |
|--------|------|------|
| 消息处理流程 | [message-handling.md](./message-handling.md) | 从用户发送消息到接收完整响应的流程 |
| Agent 循环执行流程 | [agent-loop-execution.md](./agent-loop-execution.md) | Agent 循环的完整执行流程和状态转换 |
| 工具执行流程 | [tool-execution.md](./tool-execution.md) | 工具调用和执行的完整流程，包括安全检查 |
| 上下文构建流程 | [context-building.md](./context-building.md) | 会话上下文构建的详细流程 |
| Dream 记忆合并流程 | [dream-consolidation.md](./dream-consolidation.md) | Dream 两阶段记忆合并流程 |
| MCP 连接流程 | [mcp-connection.md](./mcp-connection.md) | MCP 服务器连接和工具调用流程 |
| 子 Agent 启动流程 | [subagent-spawn.md](./subagent-spawn.md) | 子 Agent 创建和执行流程 |
| 定时任务调度流程 | [cron-scheduling.md](./cron-scheduling.md) | 定时任务调度和执行流程 |

## 使用说明

### 在 Markdown 中使用

```markdown
查看消息处理流程：

![消息处理流程](./diagrams/flows/message-handling.md)
```

### 流程图说明

每个流程图展示了关键的业务流程，包括：

- **开始/结束节点** - 流程的起点和终点
- **决策节点** - 条件判断和分支
- **处理节点** - 主要的处理步骤
- **连接线** - 流程的流转路径

### 在 GitHub 中渲染

GitHub 原生支持 Mermaid 流程图，直接在 Markdown 中使用 mermaid 代码块即可渲染。

## 相关文档

- [架构图索引](../README.md)
- [架构分析文档](../../architecture-zh.md)
- [设计原理文档](../../design-principles-zh.md)
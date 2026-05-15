# 时序图索引

本目录包含 nanobot 项目关键业务流程的时序图，使用 Mermaid 语法编写。

## 时序图列表

| 时序图 | 文件 | 说明 |
|--------|------|------|
| 用户消息处理时序图 | [message-processing.md](./message-processing.md) | 从用户发送消息到接收完整响应的时序 |
| 流式响应时序图 | [streaming-response.md](./streaming-response.md) | 流式响应和增量处理的时序 |
| 工具调用时序图 | [tool-call.md](./tool-call.md) | 工具调用的执行时序，包括并行执行 |
| 多通道并发时序图 | [multi-channel.md](./multi-channel.md) | 多通道并发消息处理的时序 |
| 子 Agent 调用时序图 | [subagent.md](./subagent.md) | 子 Agent 创建和执行的时序 |

## 使用说明

### 在 Markdown 中使用

```markdown
查看消息处理时序图：

![消息处理时序图](./diagrams/sequence/message-processing.md)
```

### 在 GitHub 中渲染

GitHub 原生支持 Mermaid 时序图，直接在 Markdown 中使用 mermaid 代码块即可渲染。

## 时序图说明

每个时序图展示了关键的交互流程，包括：

- **参与者** - 图中显示的各个组件/角色
- **消息传递** - 组件间的消息流向
- **并发处理** - 使用 `par` 关键字表示并发
- **循环结构** - 使用 `loop` 关键字表示循环
- **注释** - 使用 `Note` 关键字添加说明

## 相关文档

- [数据结构图索引](../structures/)
- [架构图索引](../README.md)
- [流程图索引](../flows/)
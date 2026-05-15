# 数据结构图索引

本目录包含 nanobot 项目核心数据结构的类图和字段说明，使用 Mermaid 语法编写。

## 数据结构图列表

| 数据结构 | 文件 | 说明 |
|----------|------|------|
| InboundMessage/OutboundMessage | [messages.md](./messages.md) | 入站/出站消息的结构和字段说明 |
| Session 数据结构 | [session.md](./session.md) | Session 对象和相关组件的结构 |
| Tool Call 结构 | [tool-call.md](./tool-call.md) | 工具调用和响应的结构 |
| Configuration Schema 层次 | [config-schema.md](./config-schema.md) | 配置系统的层次结构和示例 |

## 使用说明

### 在 Markdown 中使用

```markdown
查看消息结构：

![消息结构](./diagrams/structures/messages.md)
```

### 在 GitHub 中渲染

GitHub 原生支持 Mermaid 类图，直接在 Markdown 中使用 mermaid 代码块即可渲染。

## 类图说明

每个数据结构图包含：

- **类定义** - 主要的类及其关系
- **字段列表** - 详细的字段说明表格
- **关系说明** - 类之间的关系和基数

## 相关文档

- [时序图索引](../sequence/)
- [架构图索引](../README.md)
- [架构分析文档](../../architecture-zh.md)
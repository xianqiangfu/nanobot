# nanobot 中的记忆

nanobot 的记忆建立在一个简单的信念之上：记忆应该是鲜活的，但不应该是混乱的。

好的记忆不是一堆笔记。它是一个安静的注意力系统。它注意到值得保留的内容，释放那些不再需要关注的内容，并将生活经验转化为平静、持久且有用的东西。

这就是 nanobot 中记忆的形态。

## 设计理念

nanobot 不将记忆视为一个巨大的文件。

它将记忆分层，因为不同类型的记忆需要不同的工具：

- `session.messages` 保存正在进行中的短期对话。
- `memory/history.jsonl` 是已压缩的过往回合的运行归档。
- `SOUL.md`、`USER.md` 和 `memory/MEMORY.md` 是持久化的知识文件。
- `GitStore` 记录这些持久化文件随时间的变化。

这使得系统在当下保持轻量，但能够随时间推移进行反思。

## 记忆流程

记忆在 nanobot 中通过两个阶段流动。

### 阶段 1：Consolidator（整合器）

当对话增长到足以对上下文窗口造成压力时，nanobot 不会尝试永远保留每条旧消息。

相反，`Consolidator` 会总结对话中最安全的最早切片，并将该总结追加到 `memory/history.jsonl` 中。

该文件具有以下特点：

- 仅追加
- 基于游标
- 首先优化为机器消费，其次供人类检查

每一行都是一个 JSON 对象：

```json
{"cursor": 42, "timestamp": "2026-04-03 00:02", "content": "- 用户偏好深色模式\n- 决定使用 PostgreSQL"}
```

它不是最终的记忆。它是塑造最终记忆的原始材料。

### 阶段 2：Dream（梦境）

`Dream` 是一个更慢、更深思熟虑的层。它默认按 cron 计划运行，也可以手动触发。

Dream 会读取：

- `memory/history.jsonl` 中的新条目
- 当前的 `SOUL.md`
- 当前的 `USER.md`
- 当前的 `memory/MEMORY.md`

然后它在两个阶段中工作：

1. 它研究什么是新的，什么是已知的。
2. 它对长期文件进行精确编辑，不是重写所有内容，而是进行最小的诚实更改，以保持记忆的连贯性。

这就是为什么 nanobot 的记忆不仅仅是归档。它是解释性的。

## 文件结构

```text
workspace/
├── SOUL.md              # 机器人的长期语音和沟通风格
├── USER.md              # 关于用户的稳定知识
└── memory/
    ├── MEMORY.md        # 项目事实、决策和持久化上下文
    ├── history.jsonl    # 仅追加的历史摘要
    ├── .cursor          # Consolidator 写入游标
    ├── .dream_cursor    # Dream 消费游标
    └── .git/            # 长期记忆文件的版本历史
```

这些文件扮演不同的角色：

- `SOUL.md` 记住 nanobot 应该如何表达。
- `USER.md` 记住用户是谁以及他们偏好什么。
- `MEMORY.md` 记住关于工作本身哪些保持真实。
- `history.jsonl` 记住到达那里过程中发生了什么。

## 为什么使用 `history.jsonl`

旧的 `HISTORY.md` 格式适合随意阅读，但作为操作基础太过脆弱。

`history.jsonl` 为 nanobot 提供了：

- 稳定的增量游标
- 更安全的机器解析
- 更容易的批处理
- 更清晰的迁移和压缩
- 原始历史与策划知识之间更好的边界

您仍然可以使用熟悉的工具搜索它：

```bash
# grep
grep -i "keyword" memory/history.jsonl

# jq
cat memory/history.jsonl | jq -r 'select(.content | test("keyword"; "i")) | .content' | tail -20

# Python
python -c "import json; [print(json.loads(l).get('content','')) for l in open('memory/history.jsonl','r',encoding='utf-8') if l.strip() and 'keyword' in l.lower()][-20:]"
```

这种差异在哲学上与技术上同样重要：

- `history.jsonl` 用于结构
- `SOUL.md`、`USER.md` 和 `MEMORY.md` 用于意义

## 命令

记忆不是隐藏在幕后的。用户可以检查和引导它。

| 命令 | 功能 |
|---------|--------------|
| `/dream` | 立即运行 Dream |
| `/dream-log` | 显示最新的 Dream 记忆更改 |
| `/dream-log <sha>` | 显示特定的 Dream 更改 |
| `/dream-restore` | 列出最近的 Dream 记忆版本 |
| `/dream-restore <sha>` | 将记忆恢复到特定更改之前的状态 |

这些命令的存在是有原因的：自动记忆很强大，但用户应该始终保留检查、理解和恢复它的权利。

## 版本化记忆

在 Dream 更改长期记忆文件后，nanobot 可以使用 `GitStore` 记录该更改。

这赋予了记忆自己的历史：

- 您可以检查发生了什么变化
- 您可以比较版本
- 您可以恢复到之前的状态

这将记忆从静默的突变变成了可审计的过程。

## 配置

Dream 在 `agents.defaults.dream` 下配置：

```json
{
  "agents": {
    "defaults": {
      "dream": {
        "intervalH": 2,
        "modelOverride": null,
        "maxBatchSize": 20,
        "maxIterations": 10
      }
    }
  }
}
```

| 字段 | 含义 |
|-------|---------|
| `intervalH` | Dream 运行的频率，以小时为单位 |
| `modelOverride` | 可选的 Dream 专用模型覆盖 |
| `maxBatchSize` | Dream 每次运行处理的历史条目数 |
| `maxIterations` | Dream 编辑阶段的工具预算 |

在实际应用中：

- `modelOverride: null` 表示 Dream 使用与主代理相同的模型。仅在希望 Dream 在不同模型上运行时才设置它。
- `maxBatchSize` 控制 Dream 在一次运行中消耗多少新的 `history.jsonl` 条目。较大的批次追赶得更快；较小的批次更轻量、更稳定。
- `maxIterations` 限制 Dream 在更新 `SOUL.md`、`USER.md` 和 `MEMORY.md` 时可以采取的读取/编辑步骤数量。它是一个安全预算，而不是质量评分。
- `intervalH` 是配置 Dream 的正常方式。它在内部作为 `every` 计划运行，而不是作为 cron 表达式。

遗留说明：

- 较旧的基于源代码的配置可能仍然包含 `dream.cron`。nanobot 为了向后兼容继续支持它，但新配置应该使用 `intervalH`。
- 较旧的基于源代码的配置可能仍然包含 `dream.model`。nanobot 为了向后兼容继续支持它，但新配置应该使用 `modelOverride`。

## 实际应用

这在日常使用中意味着：

- 对话可以保持快速，而无需承载无限的上下文
- 持久的事实可以随时间变得更清晰，而不是更嘈杂
- 用户可以在需要时检查和恢复记忆

记忆不应该感觉像是垃圾堆。它应该感觉像是连续性。

这就是该设计试图保护的东西。
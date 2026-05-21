# 工具使用说明

工具签名通过函数调用自动提供。
本文档记录了非显而易见的约束和使用模式。

## exec — 安全限制

- 命令具有可配置的超时时间（默认 60 秒）
- 危险命令会被阻止（rm -rf、format、dd、shutdown 等）
- 输出会被截断至 10,000 个字符
- `restrictToWorkspace` 配置可以将文件访问限制在工作区范围内

## glob — 文件发现

- 在回退到 shell 命令之前，使用 `glob` 通过模式查找文件
- 简单模式如 `*.py` 会递归地按文件名匹配
- 当您需要匹配目录而非文件时，使用 `entry_type="dirs"`
- 使用 `head_limit` 和 `offset` 来分页浏览大型结果集
- 当您只需要文件路径时，优先使用此工具而非 `exec`

## grep — 内容搜索

- 使用 `grep` 在工作区内搜索文件内容
- 默认行为仅返回匹配的文件路径（`output_mode="files_with_matches"`）
- 支持可选的 `glob` 过滤器以及 `context_before` / `context_after`
- 支持 `type="py"`、`type="ts"`、`type="md"` 和类似的简写过滤器
- 对于包含正则字符的字面关键字，使用 `fixed_strings=true`
- 使用 `output_mode="files_with_matches"` 仅获取匹配的文件路径
- 使用 `output_mode="count"` 在读取完整匹配结果之前评估搜索规模
- 使用 `head_limit` 和 `offset` 分页浏览结果
- 对于代码和历史记录搜索，优先使用此工具而非 `exec`
- 二进制或超大文件可能会被跳过以保持结果可读性

## cron — 定时提醒

- 使用方法请参阅 cron 技能文档。
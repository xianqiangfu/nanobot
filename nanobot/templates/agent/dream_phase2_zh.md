根据以下分析更新内存文件。
- [FILE] 条目：将描述的内容添加到相应的文件中
- [FILE-REMOVE] 条目：从内存文件中删除相应的内容
- [SKILL] 条目：使用 write_file 在 skills/<name>/SKILL.md 下创建新技能

## 文件路径（相对于工作区根目录）
- SOUL.md
- USER.md
- memory/MEMORY.md
- skills/<name>/SKILL.md（仅用于 [SKILL] 条目）

不要猜测路径。

## 编辑规则
- 直接编辑 — 文件内容在下面提供，无需 read_file
- 使用精确的文本作为 old_text，包括周围空行以确保唯一匹配
- 将同一文件的多个更改合并到一个 edit_file 调用中
- 对于删除：章节标题 + 所有项目符号作为 old_text，new_text 为空
- 仅进行精确编辑 — 绝不重写整个文件
- 如果没有需要更新的内容，停止而不调用工具

## 技能创建规则（用于 [SKILL] 条目）
- 使用 write_file 创建 skills/<name>/SKILL.md
- 在写入之前，读取 `{{ skill_creator_path }}` 作为格式参考（frontmatter 结构、命名约定、质量标准）
- **去重检查**：读取下面列出的现有技能，以验证新技能在功能上不重复。如果现有技能已经涵盖相同的工作流，则跳过创建
- 包含带有 name 和 description 字段的 YAML frontmatter
- 保持 SKILL.md 在 2000 字以内 — 简洁且可操作
- 包括：何时使用、步骤、输出格式、至少一个示例
- 不要覆盖现有技能 — 如果技能目录已存在则跳过
- 引用代理可以访问的特定工具（read_file、write_file、exec、web_search 等）
- 技能是指令集，不是代码 — 不要包含实现代码

## 质量
- 每一行都必须有独立的价值
- 清晰标题下的简洁项目符号
- 在减少（而非删除）时：保留基本事实，删除冗长的细节
- 如果不确定是否删除，保留但添加"（验证时效性）"
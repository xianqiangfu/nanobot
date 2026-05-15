# 内置技能

本目录包含 nanobot 内置的技能，用于扩展智能体的能力。

## 技能格式

每个技能是一个包含 `SKILL.md` 文件的目录，文件内容包含：

- YAML 前言（名称、描述、元数据）
- Markdown 格式的智能体指令

## 可用技能

| 技能 | 描述 |
|------|------|
| `github` | 使用 `gh` CLI 与 GitHub 交互 |
| `weather` | 使用 wttr.in 和 Open-Meteo 获取天气信息 |
| `summarize` | 总结 URL、文件和 YouTube 视频 |
| `tmux` | 远程控制 tmux 会话 |
| `clawhub` | 从 ClawHub 注册表搜索和安装技能 |
| `skill-creator` | 创建新技能 |

## 技能示例

### GitHub 技能

```markdown
---
name: github
description: 与 GitHub 交互
---

你可以使用 gh CLI 与 GitHub 交互。常用命令：

- 查看仓库: `gh repo view`
- 创建 issue: `gh issue create`
- 列出 PR: `gh pr list`
```

### Weather 技能

```markdown
---
name: weather
description: 获取天气信息
---

你可以使用以下方式获取天气信息：

1. wttr.in: `curl wttr.in/城市名`
2. Open-Meteo: 通过 API 获取
```

## 使用技能

### 加载技能

技能由 `SkillsLoader` 自动加载：

```python
from nanobot.agent import SkillsLoader

loader = SkillsLoader()
skills = loader.load_skills("nanobot/skills/")
```

### 技能内容

技能内容被添加到系统提示词中：

```
系统提示词...

## 技能

### GitHub
你可以使用 gh CLI 与 GitHub 交互...

### Weather
你可以获取天气信息...
```

## 创建自定义技能

### 技能目录结构

```
my-skill/
└── SKILL.md
```

### SKILL.md 格式

```markdown
---
name: my_skill
description: 我的自定义技能
version: 1.0.0
author: Your Name
---

# 技能说明

这是一个自定义技能，用于...

## 使用方法

1. 步骤一
2. 步骤二
3. 步骤三

## 示例

示例文本...
```

## 技能引用大型文档

当技能引用大型本地文档或日志时：

1. 优先使用内置的 `grep` / `glob` 工具缩小搜索范围
2. 使用 `grep(output_mode="count")` / `files_with_matches` 进行广泛搜索
3. 使用 `head_limit` / `offset` 分页浏览大型结果集
4. 当发现目录结构很重要时，使用 `glob(entry_type="dirs")`

## 技能系统来源

这些技能改编自 [OpenClaw](https://github.com/openclaw/openclaw) 的技能系统。技能格式和元数据结构遵循 OpenClaw 的约定以保持兼容性。

## 注意事项

- 技能应该简洁明了
- 技能内容应该使用 Markdown 格式
- YAML 前言用于元数据
- 技能可以引用其他技能
- 技能内容会被添加到系统提示词中
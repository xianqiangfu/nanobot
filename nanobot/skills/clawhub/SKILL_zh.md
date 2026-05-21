---
name: clawhub
description: 从 ClawHub 公共技能注册表搜索和安装 AI 智能体技能。
homepage: https://clawhub.ai
metadata: {"nanobot":{"emoji":"🦞"}}
---

# ClawHub

AI 智能体的公共技能注册表。通过自然语言搜索（向量搜索）。

## 使用场景

当用户提出以下任何请求时，使用此技能：
- "找一个用于……的技能"
- "搜索技能"
- "安装一个技能"
- "有哪些可用的技能？"
- "更新我的技能"

## 搜索

```bash
npx --yes clawhub@latest search "web scraping" --limit 5
```

## 安装

```bash
npx --yes clawhub@latest install <slug> --workdir ~/.nanobot/workspace
```

将 `<slug>` 替换为搜索结果中的技能名称。这会将技能放入 `~/.nanobot/workspace/skills/`，nanobot 从此目录加载工作区技能。始终包含 `--workdir`。

## 更新

```bash
npx --yes clawhub@latest update --all --workdir ~/.nanobot/workspace
```

## 列出已安装的技能

```bash
npx --yes clawhub@latest list --workdir ~/.nanobot/workspace
```

## 注意事项

- 需要 Node.js（`npx` 随其附赠）。
- 搜索和安装无需 API 密钥。
- 登录（`npx --yes clawhub@latest login`）仅在发布时需要。
- `--workdir ~/.nanobot/workspace` 至关重要 —— 没有它，技能将安装到当前目录而非 nanobot 工作区。
- 安装后，提醒用户启动新会话以加载该技能。
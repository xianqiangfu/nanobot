---
name: summarize
description: 总结或从 URL、播客和本地文件中提取文本/转录文本（适用于"转录此 YouTube/视频"的回退方案）。
homepage: https://summarize.sh
metadata: {"nanobot":{"emoji":"🧾","requires":{"bins":["summarize"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/summarize","bins":["summarize"],"label":"安装 summarize (brew)"}]}}
---

# Summarize

用于总结 URL、本地文件和 YouTube 链接的快速 CLI 工具。

## 何时使用（触发短语）

当用户提出以下任何请求时，立即使用此技能：
- "使用 summarize.sh"
- "这个链接/视频是关于什么的？"
- "总结此 URL/文章"
- "转录此 YouTube/视频"（尽力而为的转录文本提取；无需 `yt-dlp`）

## 快速开始

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

## YouTube：摘要 vs 转录文本

尽力而为的转录文本（仅限 URL）：

```bash
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto --extract-only
```

如果用户要求提供转录文本但内容过长，先返回紧凑的摘要，然后询问需要展开哪个部分/时间段。

## 模型和密钥

为您的提供商设置 API 密钥：
- OpenAI：`OPENAI_API_KEY`
- Anthropic：`ANTHROPIC_API_KEY`
- xAI：`XAI_API_KEY`
- Google：`GEMINI_API_KEY`（别名：`GOOGLE_GENERATIVE_AI_API_KEY`、`GOOGLE_API_KEY`）

如果未设置模型，默认为 `google/gemini-3-flash-preview`。

## 常用标志

- `--length short|medium|long|xl|xxl|<chars>` （设置输出长度）
- `--max-output-tokens <count>` （最大输出 token 数）
- `--extract-only` （仅提取，仅限 URL）
- `--json` （机器可读格式）
- `--firecrawl auto|off|always` （回退提取方式）
- `--youtube auto` （如果设置了 `APIFY_API_TOKEN`，则使用 Apify 回退）

## 配置

可选配置文件：`~/.summarize/config.json`

```json
{ "model": "openai/gpt-5.2" }
```

可选服务：
- `FIRECRAWL_API_KEY` 用于无法访问的网站
- `APIFY_API_TOKEN` 用于 YouTube 回退
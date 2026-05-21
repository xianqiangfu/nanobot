---
name: update-setup
description: nanobot升级技能的一次性设置向导。触发词：setup update, configure update, 切设置更新, 初始化更新。
---

# 更新设置

为此工作区生成个性化的升级技能。

## 步骤 1：检查现有内容

使用 `read_file` 检查工作区中是否已存在 `skills/update/SKILL.md`。

如果存在，询问用户："已存在升级技能。是否重新配置？" 等待用户回复。如果否，在此停止。

## 步骤 2：当前版本和安装线索

使用 `exec` 运行 `nanobot --version`。告知用户当前版本。

然后使用 `exec` 收集安装线索。这些命令是尽力而为；如果一个命令失败，
继续执行并显示有用的输出：

```
command -v nanobot || true
python -m pip show nanobot-ai || true
pipx list | sed -n '/nanobot-ai/,+3p' || true
uv tool list | sed -n '/nanobot-ai/,+3p' || true
```

用一段简短的段落总结你发现的内容。仅使用线索来建议可能的安装方法。不要将其视为确认。

## 步骤 3：确认必需的输入

关键：在用户明确确认安装方法之前，不要编写 `skills/update/SKILL.md`。安装方法必须来自用户回答或确认，而不是仅靠推断。如果你无法获得明确的答案，停止并要求用户在他们知道 nanobot 如何安装时重新运行此设置。

在你的响应文本中，逐一询问用户以下问题。等待用户回复后再进行下一个问题。如果无法获得明确答案，在不编写技能的情况下停止。

**问题 1 — 安装方法：**

```
question: "我发现以下安装线索：<SUMMARY>。此工作区应该使用哪种更新方法？"
options: ["uv", "pipx", "pip", "source (git clone)", "not sure"]
```

如果用户选择 `not sure`，解释选项之间的区别并停止。不要生成升级技能。

如果用户选择 `source (git clone)`，询问本地检出路径：
`question: "你的 nanobot 源代码检出位置在哪里？请输入绝对路径或相对于此工作区的路径："`。

**问题 2 — 可选依赖：**

```
question: "你需要哪些可选依赖？列出名称，用空格分隔，或回复 'none'。可用：api, wecom, weixin, msteams, matrix, discord, langsmith, pdf"
```

解析回复。如果用户说 "none" 或类似内容，将 extras 设置为空。否则收集有效名称。

**问题 3 — 代理：**

```
question: "你是否需要 HTTP 代理来访问 PyPI 或 GitHub？"
options: ["no", "yes"]
```

如果是，再询问一次代理 URL：`question: "输入代理 URL（例如：http://127.0.0.1:7890）："`。

## 步骤 4：生成技能

构建 extras 字符串。如果用户选择了依赖项，格式为 `[dep1,dep2,...]`。否则完全省略括号。

根据安装方法确定升级命令：

| 方法 | 命令 |
|--------|---------|
| uv | `uv tool install "nanobot-ai[EXTRAS]" --force` |
| pipx | `pipx install --force "nanobot-ai[EXTRAS]"` |
| pip | `python -m pip install --upgrade "nanobot-ai[EXTRAS]"` |
| source | `cd <SOURCE_CHECKOUT> && git pull && python -m pip install -e ".[EXTRAS]"` |

对于源码安装，在选择时将 extras 包含在可编辑安装命令中。如果源代码检出路径包含空格，请加引号。

根据安装方法确定预检检查：

| 方法 | 预检检查 |
|--------|-----------------|
| uv | `command -v uv` |
| pipx | `command -v pipx` |
| pip | `python -m pip --version` |
| source | `test -d <SOURCE_CHECKOUT> && test -d <SOURCE_CHECKOUT>/.git && test -f <SOURCE_CHECKOUT>/pyproject.toml` |

对于源码安装，如果源代码检出路径包含空格，请在预检检查中加引号。

构建技能内容。如果配置了代理，在升级命令之前添加 `export http_proxy=URL` 和 `export https_proxy=URL` 行。

使用 `write_file` 编写 `skills/update/SKILL.md`，内容如下：

```
---
name: update
description: "将 nanobot 升级到最新版本。触发词：upgrade nanobot, update nanobot, 升级nanobot, 更新nanobot。"
---

# 更新 Nanobot

1. （如果配置了代理）设置代理：`export http_proxy=URL && export https_proxy=URL`
2. 使用 `exec` 运行预检检查：<PREFLIGHT_CHECK>。如果失败，停止并告诉用户重新运行 `update-setup`，因为保存的安装方法不再匹配此环境。
3. 使用 `exec` 运行升级命令：<UPGRADE_COMMAND>
4. 使用 `exec` 验证：`nanobot --version`
5. 告知用户新版本。说："运行 `/restart` 以重启 nanobot 并应用更新。如果此频道中 `/restart` 不可用，请手动重启 nanobot 进程。"
```

## 步骤 5：确认

告诉用户："升级技能已创建。当你想要更新时说 'upgrade nanobot'。"
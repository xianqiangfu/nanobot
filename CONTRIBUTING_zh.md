# 为 nanobot 做贡献

感谢你的到来。

nanobot 基于一个简单的信念而构建：好的工具应该感觉平静、清晰和人性化。
我们深切关注有用的功能，但也相信少即是多：
解决方案应该强大而不沉重，有野心而不不必要的复杂。

本指南不仅关于如何打开 PR。它也关于我们希望如何一起构建软件：
用心、清晰，并尊重阅读代码的下一个人。

## 维护者

| 维护者 | 关注点 |
|--------|--------|
| [@re-bin](https://github.com/re-bin) | 项目负责人，`main` 分支 |
| [@chengyongru](https://github.com/chengyongru) | `nightly` 分支，实验性功能 |

## 分支策略

我们使用双分支模型来平衡稳定性和探索：

| 分支 | 目的 | 稳定性 |
|------|------|--------|
| `main` | 稳定版本 | 生产就绪 |
| `nightly` | 实验性功能 | 可能有 bug 或破坏性更改 |

### 我应该针对哪个分支？

**如果你的 PR 包含以下内容，请针对 `nightly`：**

- 新功能或功能
- 可能影响现有行为的重构
- API 或配置的更改

**如果你的 PR 包含以下内容，请针对 `main`：**

- 没有行为更改的 bug 修复
- 文档改进
- 不影响功能的小调整

**如果有疑问，请针对 `nightly`。** 将稳定的想法从 `nightly` 移动到 `main` 比在稳定分支中实施冒险更改后撤销它更容易。

### 开始工作

在进行更改之前，同步目标分支并从中创建主题分支。
对于稳定的 bug 修复和仅文档更改，请从最新的 `main` 开始。
对于实验性工作，请从最新的 `nightly` 开始。

```bash
git fetch upstream
git switch main
git pull --ff-only upstream main
git switch -c your-topic-branch
```

如果你的检出使用了不同的远程名称，请使用你的主要 HKUDS/nanobot 远程代替 `upstream`。

保持主题分支中没有无关的本地更改。如果你的检出已经有进行中的工作，请使用单独的工作树或在开始新分支之前完成该工作。

### Nightly 如何合并到 Main？

我们不合并整个 `nightly` 分支。相反，稳定的功能会从 `nightly` 中**挑选**（cherry-picked）到针对 `main` 的单个 PR 中：

```
nightly  ──┬── feature A (stable) ──► PR ──► main
           ├── feature B (testing)
           └── feature C (stable) ──► PR ──► main
```

这大约每周发生一次，但时间取决于功能何时变得足够稳定。

### 快速总结

| 你的更改 | 目标分支 |
|----------|----------|
| 新功能 | `nightly` |
| Bug 修复 | `main` |
| 文档 | `main` |
| 重构 | `nightly` |
| 不确定 | `nightly` |

## 开发设置

保持设置无聊且可靠。目标是让你快速进入代码：

```bash
# 克隆仓库
git clone https://github.com/HKUDS/nanobot.git
cd nanobot

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 检查代码
ruff check nanobot/

# 格式化代码
ruff format nanobot/
```

## 贡献许可

通过提交贡献，你确认你有权提交它，并同意它将根据项目的 MIT 许可证进行许可。

## 代码风格

我们不仅关心通过 lint 检查。我们希望 nanobot 保持小、平静和可读。

在贡献时，请编写感觉像是以下的代码：

- 简单：优先选择解决真正问题的最小更改
- 清晰：为下一位读者优化，而不是为了聪明
- 解耦：保持边界清洁，避免不必要的新的抽象
- 诚实：不要隐藏复杂性，但也不要创建额外的复杂性
- 耐用：选择易于维护、测试和扩展的解决方案

在实践中：

- 行长度：100 个字符（`ruff`）
- 目标：Python 3.11+
- Lint：`ruff` 使用规则 E、F、I、N、W（E501 被忽略）
- 异步：全程使用 `asyncio`；pytest 配置为 `asyncio_mode = "auto"`
- 优先选择可读的代码而不是魔术代码
- 优先选择专注的补丁而不是广泛的重写
- 如果引入新的抽象，它应该清楚地减少复杂性而不是移动它

## 修改 CI 工作流

如果你的 PR 涉及 `.github/workflows/`，请保持在 GitHub Actions 免费层内：

- 仅使用标准的 GitHub 托管运行器（`ubuntu-latest`、`windows-latest`）
- 避免使用 macOS 运行器、更大的运行器（`*-cores`、`*-xlarge`、`*-gpu`）
  和自托管运行器
- 避免上传大型工件或使用长期保留
- 避免使用付费的 Marketplace 操作

如果你的更改确实需要超出此范围，请在 PR 描述中明确说明，以便在合并之前进行讨论。

## 有问题？

如果你有疑问、想法或不完整的见解，我们热烈欢迎你。

请随意打开 [issue](https://github.com/HKUDS/nanobot/issues)，加入社区，或直接联系：

- [Discord](https://discord.gg/MnCvHqpUGB)
- [飞书/微信](./COMMUNICATION.md)
- 邮箱：Xubin Ren (@Re-bin) — <xubinrencs@gmail.com>

感谢你花时间和精力为 nanobot 做贡献。我们希望更多人参与这个社区，我们真诚地欢迎各种规模的贡献。
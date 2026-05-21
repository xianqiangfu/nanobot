---
name: image-generation
description: 生成图像并迭代编辑保存的图像工件。
---

# 图像生成

当用户要求您创建、渲染、绘制、设计、生成或编辑图像时，使用 `generate_image` 工具。

如果当前工具列表中没有 `generate_image` 工具，请告诉用户该 nanobot 实例未启用图像生成功能。

## 使用时机

- **文本到图像**：使用具体的 `prompt` 调用 `generate_image`。
- **图像编辑**：将保存的工件路径或用户图像路径传递给 `reference_images`。
- **同一对话中的迭代编辑**：如果用户说诸如"让它更亮"、"更改背景"或"尝试另一个版本"之类的话，优先使用最近生成的图像工件。
- **模糊的编辑请求**：如果多个最近的图像都可能是目标，请询问一个简短的澄清问题。
- 在当前聊天中，不要仅仅为了宣布或重新发送生成的图像而调用 `message`。运行时会自动将来自 `generate_image` 的图像附加到最终助手回复中。

## 提示词规则

编写包含足够细节的提示词以满足图像模型的要求：

- 主体和场景。
- 构图和相机角度或布局。
- 风格、情绪、光照和调色板。
- 必须出现在图像中的文本，需精确引用。
- 约束条件，例如"保持相同角色"、"保留徽标"或"不要更改背景"。

## 工件规则

该工具将生成的图像作为持久化工件存储在 nanobot 的媒体目录下，并返回结构化元数据：

- `id`：生成的图像 ID，例如 `img_ab12cd34ef56`。
- `path`：用于内部后续编辑的本地文件路径。
- `mime`：图像 MIME 类型。
- `prompt`、`model` 和 `source_images`：用于后续编辑的来源信息。

在面向用户的正常回复中，不要暴露本地文件系统路径。保持回复自然，例如"已完成，我已生成它。"如果有助于用户引用特定图像，可以包含简短的图像 `id`，但除非用户明确要求调试详细信息或本地工件引用，否则将原始 `path` 保持在内部。永远不要粘贴 base64。

对于后续编辑，将先前工件的 `path` 传递给 `reference_images`。如果用户提供新上传的图像，则使用该路径作为参考。

不要在面向用户的回复中包含内部重播标记，例如 `[Message Time: ...]`、`[image: /local/path]`、`generate_image(...)` 或 `message(...)`。

## 提供商说明

不要要求用户将 API 密钥粘贴到聊天中。如果需要配置，请描述相应字段；LLM 提供商和 BYOK（自带密钥）的更改会在新的轮次中热重新加载。

对于 OpenRouter，图像工具期望的配置如下：

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-..."
    }
  },
  "tools": {
    "imageGeneration": {
      "enabled": true,
      "provider": "openrouter",
      "model": "openai/gpt-5.4-image-2"
    }
  }
}
```

对于 AIHubMix，图像工具期望的配置如下：

```json
{
  "providers": {
    "aihubmix": {
      "apiKey": "sk-..."
    }
  },
  "tools": {
    "imageGeneration": {
      "enabled": true,
      "provider": "aihubmix",
      "model": "gpt-image-2-free"
    }
  }
}
```

AIHubMix 的 `gpt-image-2-free` 在内部使用 AIHubMix 的统一预测端点（`/v1/models/openai/gpt-image-2-free/predictions`），而不是 OpenAI Images 的 `/v1/images/generations` 端点。如果失败并显示"模型 ID 不正确"，在检查提供商配置、模型名称和网关重启之前，不要假设密钥缺少权限。

`providers.aihubmix.extraBody` 可用于提供商特定的选项。例如，`"extraBody": {"quality": "low"}` 是可选的，但可以使 `gpt-image-2-free` 更快且不太可能超时。

## 示例

生成新图像：

```text
generate_image(
  prompt="nanobot 的极简应用图标：友好的机器人头部、圆角正方形、柔和的蓝白色调、简洁的矢量风格、无文本",
  aspect_ratio="1:1",
  image_size="1K"
)
```

编辑最新生成的工件：

```text
generate_image(
  prompt="使用参考图像。保持相同的机器人和构图，但将调色板更改为暖橙色并添加微妙的日出背景。",
  reference_images=["/home/user/.nanobot/media/generated/2026-05-08/img_ab12cd34ef56.png"],
  aspect_ratio="1:1",
  image_size="1K"
)
```
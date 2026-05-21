# 图像生成

nanobot 可以通过 `generate_image` 工具生成和编辑图像。在 WebUI 中，用户可以从编辑器中启用 **图像生成**，选择宽高比，并在同一聊天中继续迭代生成的图像。

该功能默认禁用。在 `~/.nanobot/config.json` 中启用它，配置支持的图像提供商，然后重启网关。

## 快速设置

OpenRouter 示例：

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "${OPENROUTER_API_KEY}"
    }
  },
  "tools": {
    "imageGeneration": {
      "enabled": true,
      "provider": "openrouter",
      "model": "openai/gpt-5.4-image-2",
      "defaultAspectRatio": "1:1",
      "defaultImageSize": "1K"
    }
  }
}
```

AIHubMix 示例：

```json
{
  "providers": {
    "aihubmix": {
      "apiKey": "${AIHUBMIX_API_KEY}"
    }
  },
  "tools": {
    "imageGeneration": {
      "enabled": true,
      "provider": "aihubmix",
      "model": "gpt-image-2-free",
      "defaultAspectRatio": "1:1",
      "defaultImageSize": "1K"
    }
  }
}
```

> [!TIP]
> 优先使用环境变量存储 API 密钥。nanobot 在启动时从环境中解析 `${VAR_NAME}` 值。

## WebUI 使用

在 WebUI 编辑器中：

1. 点击 **图像生成**。
2. 选择宽高比：`Auto`、`1:1`、`3:4`、`9:16`、`4:3` 或 `16:9`。
3. 描述你想要的图像或编辑内容。
4. 编辑现有图像时，附上参考图像。

生成的图像在聊天中作为助手媒体呈现。后续提示词如"让它更暖一些"、"更改背景"或"尝试 16:9 版本"可以重复使用最新生成的工件。

WebUI 对用户隐藏了提供商存储详细信息。代理在内部看到保存的工件路径，并可以将其作为 `reference_images` 传递回 `generate_image` 以进行迭代编辑。

## 配置参考

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `tools.imageGeneration.enabled` | boolean | `false` | 注册 `generate_image` 工具 |
| `tools.imageGeneration.provider` | string | `"openrouter"` | 图像提供商名称。目前支持 `openrouter` 和 `aihubmix` |
| `tools.imageGeneration.model` | string | `"openai/gpt-5.4-image-2"` | 提供商模型名称 |
| `tools.imageGeneration.defaultAspectRatio` | string | `"1:1"` | 提示词/工具调用未指定时的默认宽高比 |
| `tools.imageGeneration.defaultImageSize` | string | `"1K"` | 默认大小提示，例如 `1K`、`2K`、`4K` 或 `1024x1024` |
| `tools.imageGeneration.maxImagesPerTurn` | number | `4` | 单个工具调用接受的最大 `count`。有效范围：`1` 到 `8` |
| `tools.imageGeneration.saveDir` | string | `"generated"` | nanobot 媒体目录下用于存储生成工件的相对目录 |

提供商设置重用普通提供商配置字段：

| 选项 | 说明 |
|--------|-------------|
| `providers.<name>.apiKey` | 提供商 API 密钥。推荐使用 `${ENV_VAR}` |
| `providers.<name>.apiBase` | 可选的自定义基础 URL |
| `providers.<name>.extraHeaders` | 合并到提供商请求中的标头 |
| `providers.<name>.extraBody` | 合并到提供商请求正文中的额外 JSON 字段 |

camelCase 和 snake_case 配置键都被接受，但文档使用 camelCase 以匹配 `config.json`。

## 提供商说明

### OpenRouter

OpenRouter 使用聊天完成风格的图像响应。配置：

```json
{
  "tools": {
    "imageGeneration": {
      "enabled": true,
      "provider": "openrouter",
      "model": "openai/gpt-5.4-image-2"
    }
  }
}
```

如果需要参考图像编辑，请使用支持图像生成和图像编辑的模型。

### AIHubMix

通过 AIHubMix 的统一预测 API 支持 AIHubMix `gpt-image-2-free`。nanobot 在内部调用：

```text
/v1/models/openai/gpt-image-2-free/predictions
```

配置：

```json
{
  "providers": {
    "aihubmix": {
      "apiKey": "${AIHUBMIX_API_KEY}",
      "extraBody": {
        "quality": "low"
      }
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

`quality: low` 是可选的。它可以使免费图像模型更快且更不容易超时，但对于正确性而言不是必需的。

## 工件

生成的图像存储在活动 nanobot 实例的媒体目录下：

```text
~/.nanobot/media/generated/YYYY-MM-DD/img_<id>.<ext>
~/.nanobot/media/generated/YYYY-MM-DD/img_<id>.json
```

对于非默认配置位置，媒体目录相对于活动配置文件目录。

JSON 副本文件存储：

| 字段 | 含义 |
|-------|---------|
| `id` | 短生成的图像 ID，例如 `img_ab12cd34ef56` |
| `path` | 内部用于后续编辑的本地图像路径 |
| `mime` | 检测到的图像 MIME 类型 |
| `prompt` | 用于生成的提示词 |
| `model` | 提供商模型 |
| `provider` | 提供商名称 |
| `source_images` | 用于编辑的参考图像路径 |
| `created_at` | 创建时间戳 |

不要将 base64 图像负载粘贴到聊天中。代理应保持本地工件路径内部，除非用户明确要求调试详细信息。

## 提示词

良好的图像提示词包括：

- 主题和场景。
- 构图、相机或布局。
- 风格、情绪、照明和调色板。
- 必须出现在图像中的确切文本，用引号括起来。
- 约束条件，如"保持相同角色"或"保留徽标"。

示例：

```text
nanobot 的最小应用图标：友好的机器人头部、圆角方形、柔和的蓝色和白色调色板、干净的矢量风格、无文本
```

对于编辑，描述应该更改什么以及必须保持什么不变：

```text
使用参考图像。保持相同的机器人和构图，将调色板更改为暖橙色，并添加微妙的日出背景。
```

## 故障排除

| 症状 | 检查 |
|---------|-------|
| `generate_image` 不可用 | 将 `tools.imageGeneration.enabled` 设置为 `true` 并重启网关 |
| 缺少 API 密钥错误 | 配置 `providers.<provider>.apiKey`；如果使用 `${VAR_NAME}`，确认环境变量对网关进程可见 |
| `unsupported image generation provider` | 使用 `openrouter` 或 `aihubmix` |
| AIHubMix 提示 `Incorrect model ID` | 使用 `model: "gpt-image-2-free"`；nanobot 会在内部将其扩展到所需的 `openai/gpt-image-2-free` 模型路径 |
| 生成超时 | 尝试较小/默认图像大小，设置 AIHubMix `extraBody.quality` 为 `"low"`，或稍后重试 |
| 参考图像被拒绝 | 参考图像路径必须在工作区或 nanobot 媒体目录内，并且必须是有效的图像文件 |

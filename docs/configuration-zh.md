# 配置

配置文件: `~/.nanobot/config.json`

> [!NOTE]
> 如果您的配置文件版本早于当前架构，您可以刷新它而不会覆盖现有值：
> 运行 `nanobot onboard`，然后在询问是否覆盖配置时回答 `N`。
> nanobot 会合并缺失的默认字段，并保留您当前的设置。

## 密钥的环境变量

除了直接在 `config.json` 中存储密钥，您还可以使用 `${VAR_NAME}` 引用，这些引用会在启动时从环境变量中解析：

```json
{
  "channels": {
    "telegram": { "token": "${TELEGRAM_TOKEN}" },
    "email": {
      "imapPassword": "${IMAP_PASSWORD}",
      "smtpPassword": "${SMTP_PASSWORD}"
    }
  },
  "providers": {
    "groq": { "apiKey": "${GROQ_API_KEY}" }
  }
}
```

对于 **systemd** 部署，请在服务单元中使用 `EnvironmentFile=` 从一个只有部署用户可读的文件中加载变量：

```ini
# /etc/systemd/system/nanobot.service (节选)
[Service]
EnvironmentFile=/home/youruser/nanobot_secrets.env
User=nanobot
ExecStart=...
```

```bash
# /home/youruser/nanobot_secrets.env (模式 600，归 youruser 所有)
TELEGRAM_TOKEN=your-token-here
IMAP_PASSWORD=your-password-here
```

## 提供商

> [!TIP]
> - **语音转录**：语音消息（Telegram、WhatsApp）会自动使用 Whisper 转录。默认使用 Groq（免费层）。在 `channels` 下设置 `"transcriptionProvider": "openai"` 可改用 OpenAI Whisper，并可选择设置 `"transcriptionLanguage": "en"`（或其他 ISO-639-1 代码）以获得更准确的转录。API 密钥从匹配的提供商配置中选取。
> - **MiniMax 编程计划**：nanobot 社区专属折扣链接：[海外](https://platform.minimax.io/subscribe/coding-plan?code=9txpdXw04g&source=link) · [中国大陆](https://platform.minimaxi.com/subscribe/token-plan?code=GILTJpMTqZ&source=link)
> - **MiniMax（中国大陆）**：如果您的 API 密钥来自 MiniMax 的大陆平台（minimaxi.com），请在 minimax 提供商配置中设置 `"apiBase": "https://api.minimaxi.com/v1"`。
> - **MiniMax 思维模式**：当您需要 `reasoningEffort` / 思维模式时使用 `providers.minimaxAnthropic`。MiniMax 通过其 Anthropic 兼容端点公开该功能，因此 nanobot 将其保留为单独的提供商，而不是在通用的 OpenAI 兼容 `minimax` 端点上猜测 MiniMax 特定的思维参数。它使用相同的 `MINIMAX_API_KEY`。默认 Anthropic 兼容基 URL：`https://api.minimax.io/anthropic`；中国大陆使用 `https://api.minimaxi.com/anthropic`。
> - **火山引擎 / BytePlus 编程计划**：使用专门的提供商 `volcengineCodingPlan` 或 `byteplusCodingPlan`，而不是按需付费的 `volcengine` / `byteplus` 提供商。
> - **智谱编程计划**：如果您使用的是智谱的编程计划，请在 zhipu 提供商配置中设置 `"apiBase": "https://open.bigmodel.cn/api/coding/paas/v4"`。
> - **阿里云百炼**：如果您使用阿里云百炼的 OpenAI 兼容端点，请在 dashscope 提供商配置中设置 `"apiBase": "https://dashscope.aliyuncs.com/compatible-mode/v1"`。
> - **阶跃星辰（中国大陆）**：如果您的 API 密钥来自阶跃星辰的大陆平台（stepfun.com），请在 stepfun 提供商配置中设置 `"apiBase": "https://api.stepfun.com/v1"`。
> - **小米 MiMo 思维模式**：MiMo 模型（例如 `mimo-v2.5-pro`）默认启用思维。使用 `agents.defaults.reasoningEffort: "none"` 禁用它，或使用 `"low"` / `"medium"` / `"high"` 保持启用。省略该字段将保留提供商的每个模型默认值。

| 提供商 | 用途 | 获取 API 密钥 |
|----------|---------|-------------|
| `custom` | 任何 OpenAI 兼容端点 | — |
| `openrouter` | LLM（推荐，访问所有模型） | [openrouter.ai](https://openrouter.ai) |
| `huggingface` | LLM（Hugging Face 推理提供商） | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `volcengine` | LLM（火山引擎，按需付费） | [编程计划](https://www.volcengine.com/activity/codingplan?utm_campaign=nanobot&utm_content=nanobot&utm_medium=devrel&utm_source=OWO&utm_term=nanobot) · [volcengine.com](https://www.volcengine.com) |
| `byteplus` | LLM（火山引擎国际版，按需付费） | [编程计划](https://www.byteplus.com/en/activity/codingplan?utm_campaign=nanobot&utm_content=nanobot&utm_medium=devrel&utm_source=OWO&utm_term=nanobot) · [byteplus.com](https://www.byteplus.com) |
| `anthropic` | LLM（Claude 直连） | [console.anthropic.com](https://console.anthropic.com) |
| `azure_openai` | LLM（Azure OpenAI） | [portal.azure.com](https://portal.azure.com) |
| `bedrock` | LLM（AWS Bedrock Converse，Claude/Nova/Llama 等） | [aws.amazon.com/bedrock](https://aws.amazon.com/bedrock/) |
| `openai` | LLM + 语音转录（Whisper） | [platform.openai.com](https://platform.openai.com) |
| `deepseek` | LLM（DeepSeek 直连） | [platform.deepseek.com](https://platform.deepseek.com) |
| `groq` | LLM + 语音转录（Whisper，默认） | [console.groq.com](https://console.groq.com) |
| `minimax` | LLM（MiniMax 直连） | [platform.minimaxi.com](https://platform.minimaxi.com) |
| `minimax_anthropic` | LLM（MiniMax Anthropic 兼容端点，思维模式） | [platform.minimaxi.com](https://platform.minimaxi.com) |
| `gemini` | LLM（Gemini 直连） | [aistudio.google.com](https://aistudio.google.com) |
| `aihubmix` | LLM（API 网关，访问所有模型） | [aihubmix.com](https://aihubmix.com) |
| `siliconflow` | LLM（SiliconFlow/硅基流动） | [siliconflow.cn](https://siliconflow.cn) |
| `dashscope` | LLM（Qwen） | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) |
| `moonshot` | LLM（Moonshot/Kimi） | [platform.moonshot.cn](https://platform.moonshot.cn) |
| `zhipu` | LLM（智谱 GLM） | [open.bigmodel.cn](https://open.bigmodel.cn) |
| `mimo` | LLM（MiMo） | [platform.xiaomimimo.com](https://platform.xiaomimimo.com) |
| `longcat` | LLM（LongCat） | [longcat.chat](https://longcat.chat/platform/docs/zh/) |
| `ollama` | LLM（本地，Ollama） | — |
| `lm_studio` | LLM（本地，LM Studio） | — |
| `mistral` | LLM | [docs.mistral.ai](https://docs.mistral.ai/) |
| `stepfun` | LLM（阶跃星辰） | [platform.stepfun.com](https://platform.stepfun.com) |
| `ovms` | LLM（本地，OpenVINO 模型服务器） | [docs.openvino.ai](https://docs.openvino.ai/2026/model-server/ovms_docs_llm_quickstart.html) |
| `vllm` | LLM（本地，任何 OpenAI 兼容服务器） | — |
| `openai_codex` | LLM（Codex，OAuth） | `nanobot provider login openai-codex` |
| `github_copilot` | LLM（GitHub Copilot，OAuth） | `nanobot provider login github-copilot` |
| `qianfan` | LLM（百度千帆） | [cloud.baidu.com](https://cloud.baidu.com/doc/qianfan/s/Hmh4suq26) |

<details>
<summary><b>AWS Bedrock (Converse API)</b></summary>

Bedrock 使用原生的 `bedrock-runtime` Converse API，因此可以调用 Bedrock 模型 ID，如 Claude Opus 4.7、Claude Sonnet、Amazon Nova、Meta Llama、Mistral、Qwen 以及其他支持 Converse 的模型。它支持正常聊天、流式传输、工具调用、工具结果、令牌使用情况和 Bedrock 错误元数据。

此提供商用于 Bedrock 的原生 Converse API，而不是 Bedrock 的 OpenAI 兼容 `/openai/v1` 端点。对于 OpenAI 兼容的 Bedrock 模型，如果您特别想要该 API 表面，您仍然可以使用 `custom`。

**1. 配置凭据**

使用正常的 AWS 凭据链（`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`、AWS 配置文件或 IAM 角色）。IAM 身份需要：

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "bedrock:InvokeModelWithResponseStream"
  ],
  "Resource": "*"
}
```

您还可以设置 `providers.bedrock.apiKey` 为 Bedrock API 密钥；nanobot 将其导出为 `AWS_BEARER_TOKEN_BEDROCK` 供 AWS SDK 使用。

凭据选项：

- **AWS CLI/默认配置文件**：将 `apiKey` 和 `profile` 留空，然后运行 `aws configure` 或提供 `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`。
- **命名 AWS 配置文件**：将 `profile` 设置为 `~/.aws/config` 或 `~/.aws/credentials` 中的配置文件。
- **IAM 角色**：在 EC2/ECS/Lambda 上，将 `apiKey` 和 `profile` 留空并附加具有 Bedrock 权限的角色。
- **Bedrock API 密钥**：设置 `apiKey` 或 `AWS_BEARER_TOKEN_BEDROCK`；`profile` 可以保持 `null`。

**2. 最小配置**

对于非 Anthropic 模型，例如 Amazon Nova：

```json
{
  "providers": {
    "bedrock": {
      "region": "us-east-1"
    }
  },
  "agents": {
    "defaults": {
      "provider": "bedrock",
      "model": "bedrock/amazon.nova-lite-v1:0",
      "reasoningEffort": null
    }
  }
}
```

使用 Bedrock API 密钥：

```json
{
  "providers": {
    "bedrock": {
      "region": "us-east-1",
      "apiKey": "${AWS_BEARER_TOKEN_BEDROCK}"
    }
  },
  "agents": {
    "defaults": {
      "provider": "bedrock",
      "model": "bedrock/amazon.nova-lite-v1:0",
      "reasoningEffort": null
    }
  }
}
```

使用命名 AWS 配置文件：

```json
{
  "providers": {
    "bedrock": {
      "region": "us-east-1",
      "profile": "my-bedrock-profile"
    }
  },
  "agents": {
    "defaults": {
      "provider": "bedrock",
      "model": "bedrock/amazon.nova-lite-v1:0"
    }
  }
}
```

**3. Claude Opus 4.7 示例**

```json
{
  "providers": {
    "bedrock": {
      "region": "us-east-1"
    }
  },
  "agents": {
    "defaults": {
      "provider": "bedrock",
      "model": "bedrock/global.anthropic.claude-opus-4-7",
      "reasoningEffort": "medium",
      "maxTokens": 8192
    }
  }
}
```

对于区域路由，使用 Bedrock 的推理 ID 之一，例如 `bedrock/us.anthropic.claude-opus-4-7`、`bedrock/eu.anthropic.claude-opus-4-7` 或 `bedrock/jp.anthropic.claude-opus-4-7`。

Claude Opus 4.7 不接受 `temperature`、`top_p` 或 `top_k`；nanobot 会自动为此模型省略 `temperature`。如果 `reasoningEffort` 设置为 `low`、`medium`、`high`、`max` 或 `adaptive`，nanobot 会发送 Bedrock 的自适应思维参数。

Bedrock 上的 Anthropic 模型也可能需要 Anthropic 用例注册，并受 Anthropic 支持的国家/地区限制。如果 Claude 因不支持的国家或地区而失败并显示 `ValidationException`，请尝试非 Anthropic Bedrock 模型（例如 Amazon Nova）以验证提供商设置。

**4. 模型 ID**

在 nanobot 配置中使用带有 `bedrock/` 前缀的 Bedrock 模型 ID 或推理配置文件 ID。nanobot 在调用 AWS 之前会删除该前缀。

示例：

- `bedrock/amazon.nova-micro-v1:0`
- `bedrock/amazon.nova-lite-v1:0`
- `bedrock/global.anthropic.claude-opus-4-7`
- `bedrock/us.anthropic.claude-opus-4-7`
- `bedrock/openai.gpt-oss-20b-1:0`
- `bedrock/meta.llama...`
- `bedrock/mistral...`

请检查 Bedrock 控制台以获取确切的模型 ID 和区域可用性。某些模型需要跨区域推理配置文件 ID，例如 `us.*`、`eu.*` 或 `global.*`。

**5. 高级模型字段**

可以使用 `extraBody` 提供模型特定字段；nanobot 会将其合并到 Converse `additionalModelRequestFields` 中：

```json
{
  "providers": {
    "bedrock": {
      "region": "us-east-1",
      "extraBody": {
        "thinking": {
          "type": "adaptive",
          "effort": "medium",
          "display": "summarized"
        }
      }
    }
  }
}
```

仅当自定义 Bedrock Runtime 端点 URL（例如 VPC 端点或代理）时才使用 `apiBase`。对于正常的 AWS 区域，它不是必需的。

当前范围：nanobot 传递 `messages`、`system`、`inferenceConfig`、`toolConfig` 和 `additionalModelRequestFields`。Bedrock 提示管理、护栏、`serviceTier` 和其他顶级 Converse 选项尚未成为一流的配置字段。

**6. 快速检查**

```bash
# 对于 AWS 凭据链使用：
aws sts get-caller-identity

# 对于 API 密钥使用：
export AWS_BEARER_TOKEN_BEDROCK="your-bedrock-api-key"
export AWS_REGION="us-east-1"
```

然后运行：

```bash
nanobot agent -m "用一句话回复。"
```

</details>


<details>
<summary><b>OpenAI Codex (OAuth)</b></summary>

Codex 使用 OAuth 而不是 API 密钥。需要 ChatGPT Plus 或 Pro 账户。
在 `config.json` 中不需要 `providers.openaiCodex` 块；`nanobot provider login` 将 OAuth 会话存储在配置之外。

**1. 登录：**
```bash
nanobot provider login openai-codex
```

**2. 设置模型**（合并到 `~/.nanobot/config.json`）：
```json
{
  "agents": {
    "defaults": {
      "model": "openai-codex/gpt-5.1-codex"
    }
  }
}
```

**3. 聊天：**
```bash
nanobot agent -m "你好！"

# 本地定位特定工作区/配置
nanobot agent -c ~/.nanobot-telegram/config.json -m "你好！"

# 在该配置之上进行一次性工作区覆盖
nanobot agent -c ~/.nanobot-telegram/config.json -w /tmp/nanobot-telegram-test -m "你好！"
```

> Docker 用户：使用 `docker run -it` 进行交互式 OAuth 登录。

</details>


<details>
<summary><b>GitHub Copilot (OAuth)</b></summary>

GitHub Copilot 使用 OAuth 而不是 API 密钥。需要配置了计划的 [GitHub 账户](https://github.com/features/copilot/plans)。
在 `config.json` 中不需要 `providers.githubCopilot` 块；`nanobot provider login` 将 OAuth 会话存储在配置之外。

**1. 登录：**
```bash
nanobot provider login github-copilot
```

**2. 设置模型**（合并到 `~/.nanobot/config.json`）：
```json
{
  "agents": {
    "defaults": {
      "model": "github-copilot/gpt-4.1"
    }
  }
}
```

**3. 聊天：**
```bash
nanobot agent -m "你好！"

# 本地定位特定工作区/配置
nanobot agent -c ~/.nanobot-telegram/config.json -m "你好！"

# 在该配置之上进行一次性工作区覆盖
nanobot agent -c ~/.nanobot-telegram/config.json -w /tmp/nanobot-telegram-test -m "你好！"
```

> Docker 用户：使用 `docker run -it` 进行交互式 OAuth 登录。

</details>

<details>
<summary><b>LongCat (OpenAI 兼容)</b></summary>

LongCat 可通过 nanobot 内置的 OpenAI 兼容提供商流程使用。
默认 API 基础已经指向 `https://api.longcat.chat/openai/v1`，因此您
通常只需要设置 `apiKey`。

```json
{
  "providers": {
    "longcat": {
      "apiKey": "${LONGCAT_API_KEY}"
    }
  },
  "agents": {
    "defaults": {
      "provider": "longcat",
      "model": "LongCat-Flash-Chat"
    }
  }
}
```

官方模型名称包括 `LongCat-Flash-Chat`、`LongCat-Flash-Thinking`、
`LongCat-Flash-Thinking-2601` 和 `LongCat-Flash-Lite`。

</details>

<details>
<summary><b>自定义提供商（任何 OpenAI 兼容 API）</b></summary>

直接连接到任何 OpenAI 兼容端点 — llama.cpp、Together AI、Fireworks、Azure OpenAI 或任何自托管服务器。模型名称按原样传递。

```json
{
  "providers": {
    "custom": {
      "apiKey": "your-api-key",
      "apiBase": "https://api.your-provider.com/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "your-model-name"
    }
  }
}
```

> 对于不需要身份验证的本地服务器，将 `apiKey` 设置为 `null`。
>
> `custom` 是暴露 OpenAI 兼容**聊天完成**API 的提供商的正确选择。它**不会**将第三方端点强制到 OpenAI/Azure **响应 API** 上。
>
> 如果您的代理或网关专门与响应 API 兼容，请改用 `azure_openai` 提供商形状并将 `apiBase` 指向该端点：
>
> ```json
> {
>   "providers": {
>     "azure_openai": {
>       "apiKey": "your-api-key",
>       "apiBase": "https://api.your-provider.com",
>       "defaultModel": "your-model-name"
>     }
>   },
>   "agents": {
>     "defaults": {
>       "provider": "azure_openai",
>       "model": "your-model-name"
>     }
>   }
> }
> ```
>
> 简而言之：**聊天完成兼容端点 → `custom`**；**响应兼容端点 → `azure_openai`**。

一些 OpenAI 兼容网关暴露请求正文扩展，例如 vLLM 引导解码或本地采样控制。将它们放在 `extraBody` 下；nanobot 在其提供商默认值之后将它们合并到聊天完成请求正文中：

```json
{
  "providers": {
    "custom": {
      "apiKey": "your-api-key",
      "apiBase": "https://api.your-provider.com/v1",
      "extraBody": {
        "repetition_penalty": 1.15,
        "chat_template_kwargs": {
          "enable_thinking": false
        }
      }
    }
  }
}
```

</details>

<details>
<summary><b>Ollama（本地）</b></summary>

使用 Ollama 运行本地模型，然后添加到配置：

**1. 启动 Ollama**（示例）：
```bash
ollama run llama3.2
```

**2. 添加到配置**（部分 — 合并到 `~/.nanobot/config.json`）：
```json
{
  "providers": {
    "ollama": {
      "apiBase": "http://localhost:11434"
    }
  },
  "agents": {
    "defaults": {
      "provider": "ollama",
      "model": "llama3.2"
    }
  }
}
```

> 当配置了 `providers.ollama.apiBase` 时，`provider: "auto"` 也可以工作，但设置 `"provider": "ollama"` 是最清晰的选择。

</details>

<details>
<summary><b>LM Studio（本地）</b></summary>

[LM Studio](https://lmstudio.ai/) 提供了一个本地 OpenAI 兼容服务器，用于运行 LLM。通过 LM Studio UI 下载模型，然后启动本地服务器。

**1. 启动 LM Studio 服务器：**
- 启动 LM Studio
- 转到"本地服务器"选项卡
- 加载模型（例如 Llama、Mistral、Qwen）
- 点击"启动服务器"（默认端口：1234）

**2. 添加到配置**（部分 — 合并到 `~/.nanobot/config.json`）：
```json
{
  "providers": {
    "lm_studio": {
      "apiKey": null,
      "apiBase": "http://localhost:1234/v1"
    }
  },
  "agents": {
    "defaults": {
      "provider": "lm_studio",
      "model": "local-model"
    }
  }
}
```

> **注意：** 对于 LM Studio，将 `apiKey` 设置为 `null`，因为它在本地运行且不需要身份验证。模型名称应与 LM Studio UI 中显示的名称匹配。
> 当配置了 `providers.lm_studio.apiBase` 时，`provider: "auto"` 也可以工作，但设置 `"provider": "lm_studio"` 是最清晰的选择。

</details>

<details>
<summary><b>OpenVINO 模型服务器（本地 / OpenAI 兼容）</b></summary>

使用 [OpenVINO 模型服务器](https://docs.openvino.ai/2026/model-server/ovms_docs_llm_quickstart.html) 在 Intel GPU 上本地运行 LLM。OVMS 在 `/v3` 上公开 OpenAI 兼容 API。

> 需要 Docker 和具有驱动程序访问权限的 Intel GPU（`/dev/dri`）。

**1. 拉取模型**（示例）：

```bash
mkdir -p ov/models && cd ov

docker run -d \
  --rm \
  --user $(id -u):$(id -g) \
  -v $(pwd)/models:/models \
  openvino/model_server:latest-gpu \
  --pull \
  --model_name openai/gpt-oss-20b \
  --model_repository_path /models \
  --source_model OpenVINO/gpt-oss-20b-int4-ov \
  --task text_generation \
  --tool_parser gptoss \
  --reasoning_parser gptoss \
  --enable_prefix_caching true \
  --target_device GPU
```

> 这会下载模型权重。在继续之前等待容器完成。

**2. 启动服务器**（示例）：

```bash
docker run -d \
  --rm \
  --name ovms \
  --user $(id -u):$(id -g) \
  -p 8000:8000 \
  -v $(pwd)/models:/models \
  --device /dev/dri \
  --group-add=$(stat -c "%g" /dev/dri/render* | head -n 1) \
  openvino/model_server:latest-gpu \
  --rest_port 8000 \
  --model_name openai/gpt-oss-20b \
  --model_repository_path /models \
  --source_model OpenVINO/gpt-oss-20b-int4-ov \
  --task text_generation \
  --tool_parser gptoss \
  --reasoning_parser gptoss \
  --enable_prefix_caching true \
  --target_device GPU
```

**3. 添加到配置**（部分 — 合并到 `~/.nanobot/config.json`）：

```json
{
  "providers": {
    "ovms": {
      "apiBase": "http://localhost:8000/v3"
    }
  },
  "agents": {
    "defaults": {
      "provider": "ovms",
      "model": "openai/gpt-oss-20b"
    }
  }
}
```

> OVMS 是本地服务器 — 不需要 API 密钥。支持工具调用（`--tool_parser gptoss`）、推理（`--reasoning_parser gptoss`）和流式传输。
> 有关更多详细信息，请参阅[官方 OVMS 文档](https://docs.openvino.ai/2026/model-server/ovms_docs_llm_quickstart.html)。
</details>

<details>
<summary><b>vLLM（本地 / OpenAI 兼容）</b></summary>

使用 vLLM 或任何 OpenAI 兼容服务器运行您自己的模型，然后添加到配置：

**1. 启动服务器**（示例）：
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
```

**2. 添加到配置**（部分 — 合并到 `~/.nanobot/config.json`）：

*提供商（将 API 密钥设置为 null 以用于本地服务器）：*
```json
{
  "providers": {
    "vllm": {
      "apiKey": null,
      "apiBase": "http://localhost:8000/v1"
    }
  }
}
```

*模型：*
```json
{
  "agents": {
    "defaults": {
      "model": "meta-llama/Llama-3.1-8B-Instruct"
    }
  }
}
```

</details>

<details>
<summary><b>添加新提供商（开发人员指南）</b></summary>

nanobot 使用**提供商注册表**（`nanobot/providers/registry.py`）作为单一事实来源。
添加新提供商只需要**2 个步骤** — 无需触及 if-elif 链。

**步骤 1.** 在 `nanobot/providers/registry.py` 的 `PROVIDERS` 中添加 `ProviderSpec` 条目：

```python
ProviderSpec(
    name="myprovider",                   # 配置字段名称
    keywords=("myprovider", "mymodel"),  # 用于自动匹配的模型名称关键字
    env_key="MYPROVIDER_API_KEY",        # 环境变量名称
    display_name="My Provider",          # 在 `nanobot status` 中显示
    default_api_base="https://api.myprovider.com/v1",  # OpenAI 兼容端点
)
```

**步骤 2.** 在 `nanobot/config/schema.py` 的 `ProvidersConfig` 中添加字段：

```python
class ProvidersConfig(BaseModel):
    ...
    myprovider: ProviderConfig = ProviderConfig()
```

就是这样！环境变量、模型路由、配置匹配和 `nanobot status` 显示都将自动工作。

**常见的 `ProviderSpec` 选项：**

| 字段 | 描述 | 示例 |
|-------|-------------|---------|
| `default_api_base` | OpenAI 兼容基础 URL | `"https://api.deepseek.com"` |
| `env_extras` | 要设置的附加环境变量 | `(("ZHIPUAI_API_KEY", "{api_key}"),)` |
| `model_overrides` | 每模型参数覆盖 | `(("kimi-k2.5", {"temperature": 1.0}), ("kimi-k2.6", {"temperature": 1.0}),)` |
| `is_gateway` | 可以路由任何模型（如 OpenRouter） | `True` |
| `detect_by_key_prefix` | 通过 API 密钥前缀检测网关 | `"sk-or-"` |
| `detect_by_base_keyword` | 通过 API 基础 URL 检测网关 | `"openrouter"` |
| `strip_model_prefix` | 在发送到网关之前删除提供商前缀 | `True`（对于 AiHubMix） |
| `supports_max_completion_tokens` | 使用 `max_completion_tokens` 而不是 `max_tokens`；对于同时拒绝两者的提供商（例如火山引擎）是必需的 | `True` |

</details>

## 模型预设

模型预设让您可以为完整的模型配置命名，并在运行时使用 `/model <preset>` 切换它。

现有配置无需更改。如果您不设置 `modelPresets` 或 `agents.defaults.modelPreset`，nanobot 将完全按照以前的方式继续使用 `agents.defaults.*`。

```json
{
  "agents": {
    "defaults": {
      "model": "openai/gpt-4.1",
      "provider": "openai",
      "maxTokens": 8192,
      "contextWindowTokens": 128000,
      "temperature": 0.1,
      "modelPreset": "fast",
      "fallbackModels": ["deep"]
    }
  },
  "modelPresets": {
    "fast": {
      "model": "openai/gpt-4.1-mini",
      "provider": "openai",
      "maxTokens": 4096,
      "contextWindowTokens": 128000,
      "temperature": 0.2,
      "reasoningEffort": "low"
    },
    "deep": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "anthropic",
      "maxTokens": 8192,
      "contextWindowTokens": 200000,
      "reasoningEffort": "high"
    }
  }
}
```

`modelPresets` 是一个顶级对象。它下面的键（`fast`、`deep`、`coding` 等）是用户定义的预设名称。每个预设支持：

| 字段 | 描述 |
|-------|-------------|
| `model` | 用于此预设的模型名称。 |
| `provider` | 提供商名称，或 `"auto"` 以使用提供商自动检测。 |
| `maxTokens` | 最大完成/输出令牌数。 |
| `contextWindowTokens` | 提示构建和合并决策使用的上下文窗口大小。 |
| `temperature` | 采样温度。 |
| `reasoningEffort` | 可选推理/思维设置。提供商支持各不相同。 |

`default` 是保留的，始终表示由 `agents.defaults.*` 构建的隐式预设；不要定义 `modelPresets.default`。使用 `/model default` 切换回 `agents.defaults.*`。

### 模型回退

`agents.defaults.fallbackModels` 定义活动模型配置的有序故障转移链。主模型仍由 `agents.defaults.modelPreset`（或在没有活动预设时的隐式默认配置）选择。

每个回退候选可以是：

- 来自 `modelPresets` 的预设名称，例如 `"deep"`。预设的完整模型、提供商、生成和上下文窗口配置将被使用。
- 至少具有 `provider` 和 `model` 的内联回退对象。可选的 `maxTokens`、`contextWindowTokens` 和 `temperature` 字段在省略时从活动主配置继承。`reasoningEffort` 不继承；省略它以关闭该回退的推理，或为支持推理的模型显式设置它。

```json
{
  "agents": {
    "defaults": {
      "modelPreset": "fast",
      "fallbackModels": [
        "deep",
        {
          "provider": "deepseek",
          "model": "deepseek-v4-pro",
          "maxTokens": 4096,
          "contextWindowTokens": 262144
        }
      ]
    }
  }
}
```

字符串条目是预设名称，而不是原始模型名称。如果您想使用尚未成为预设的模型，请使用内联对象形式。

故障转移仅在主提供商在流式传输任何答案文本之前返回可重试的模型/提供商错误时运行。典型的回退情况包括超时、连接错误、5xx 服务器错误、429 速率限制、过载和配额/余额耗尽。它不会针对格式错误的请求、身份验证/权限错误、内容过滤/拒绝或上下文长度/消息格式错误运行。

如果回退候选使用较小的 `contextWindowTokens` 值，nanobot 将使用活动链中的最小窗口构建上下文，以便每个候选都能接收相同的提示。

设置 `agents.defaults.modelPreset` 以从命名预设开始：

```json
{
  "agents": {
    "defaults": {
      "modelPreset": "fast"
    }
  }
}
```

当 `modelPreset` 为 `null` 或省略时，启动使用 `agents.defaults.*` 的隐式 `default` 预设。使用 `/model <preset>` 进行的运行时更改不会写回 `config.json`；它们影响未来的回合，直到进程重启或另一个模型/配置更改替换它们。

## 通道设置

适用于所有通道的全局设置。在 `~/.nanobot/config.json` 的 `channels` 部分下配置：

```json
{
  "channels": {
    "sendProgress": true,
    "sendToolHints": false,
    "sendMaxRetries": 3,
    "transcriptionProvider": "groq",
    "transcriptionLanguage": null,
    "telegram": { ... }
  }
}
```

| 设置 | 默认值 | 描述 |
|---------|---------|-------------|
| `sendProgress` | `true` | 将代理的文本进度流式传输到通道 |
| `sendToolHints` | `false` | 流式传输工具调用提示（例如 `read_file("…")`） |
| `showReasoning` | `true` | 允许通道显示模型推理/思维内容（DeepSeek-R1 `reasoning_content`、Anthropic `thinking_blocks`、内联 ````thinking` 标签）。推理作为带有 `_reasoning_delta` / `_reasoning_end` 标记的专用流流动 — 通道覆盖 `send_reasoning_delta` / `send_reasoning_end` 以呈现就地更新。即使为 `true`，没有这些覆盖的通道也会保持静默无操作。目前在 CLI 和 WebSocket/WebUI 上公开（斜体闪烁标题，流结束后自动折叠）；Telegram / Slack / Discord / 飞书 / 微信 / Matrix 保持基础无操作，直到其气泡 UI 被调整。独立于 `sendProgress`。 |
| `sendMaxRetries` | `3` | 每个出站消息的最大传递尝试次数，包括初始发送（0-10 配置，最少 1 次实际尝试） |
| `transcriptionProvider` | `"groq"` | 语音转录后端：`"groq"`（免费层，默认）或 `"openai"`。API 密钥从匹配的提供商配置中自动解析。 |
| `transcriptionLanguage` | `null` | 音频转录的可选 ISO-639-1 语言提示，例如 `"en"`、`"ko"`、`"ja"`。 |

`sendProgress` 和 `sendToolHints` 也可以按通道覆盖。
全局值对于未设置自己值的通道保持默认：

```json
{
  "channels": {
    "sendProgress": true,
    "sendToolHints": false,
    "telegram": {
      "enabled": true,
      "sendProgress": false
    },
    "websocket": {
      "enabled": true,
      "sendToolHints": true
    }
  }
}
```

### 重试行为

重试有意设计得简单。

当通道 `send()` 引发错误时，nanobot 在通道管理器层重试。默认情况下，`channels.sendMaxRetries` 为 `3`，该计数包括初始发送。

- **尝试 1**：立即发送
- **尝试 2**：`1s` 后重试
- **尝试 3**：`2s` 后重试
- **更高的重试预算**：退避继续为 `1s`、`2s`、`4s`，然后保持在 `4s` 上限
- **瞬态故障**：网络故障和临时 API 限制通常在下一次尝试时恢复
- **永久故障**：无效令牌、撤销的访问或被禁止的通道将耗尽重试预算并干净地失败

> [!NOTE]
> 这种设计是故意的：通道实现应该在传递失败时引发，通道管理器拥有共享的重试策略。
>
> 某些通道可能仍会在内部应用特定于 API 的小型重试。例如，Telegram 在向管理器呈现最终失败之前分别重试超时和洪水控制错误。
>
> 如果通道完全无法访问，nanobot 无法通过同一通道通知用户。观察日志中的 `Failed to send to {channel} after N attempts` 以发现持久的传递故障。

## Web 工具

nanobot 包含用于访问 Web 的基本工具。这些包括通过 API 搜索，以及以 Markdown 格式获取任意网页。它们默认启用，可以在 `~/.nanobot/config.json` 的 `tools.web` 下配置。

如果您想禁用它们，这将从发送给 LLM 的工具列表中删除 `web_search` 和 `web_fetch`，请将 `tools.web.enable` 设置为 `false`：

```json
{
  "tools": {
    "web": {
      "enable": false
    }
  }
}
```

如果您需要允许受信任的私有范围（例如 Tailscale / CGNAT 地址），您可以使用 `tools.ssrfWhitelist` 明确豁免它们免受 SSRF 阻止：

```json
{
  "tools": {
    "ssrfWhitelist": ["100.64.0.0/10"]
  }
}
```

> [!TIP]
> 使用 `tools.web` 中的 `proxy` 通过代理路由所有 Web 请求（搜索 + 获取）：
> ```json
> { "tools": { "web": { "proxy": "http://127.0.0.1:7890" } } }
> ```

### `tools.web`

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `enable` | boolean | `true` | 启用或禁用所有内置 Web 工具（`web_search` + `web_fetch`） |
| `proxy` | string 或 null | `null` | 所有 Web 请求的代理，例如 `http://127.0.0.1:7890` |
| `userAgent` | string 或 null | `null` | 所有 Web 请求的 User-Agent 标头。如果为 null，将使用浏览器的 User-Agent |

### Web 搜索

nanobot 支持多个 Web 搜索提供商。在 `~/.nanobot/config.json` 的 `tools.web.search` 下配置。

默认情况下，Web 搜索使用 `duckduckgo`，它无需 API 密钥即可开箱即用。

| 提供商 | 配置字段 | 环境变量回退 | 免费 |
|----------|--------------|------------------|------|
| `brave` | `apiKey` | `BRAVE_API_KEY` | 否 |
| `tavily` | `apiKey` | `TAVILY_API_KEY` | 否 |
| `jina` | `apiKey` | `JINA_API_KEY` | 免费层（1000 万令牌） |
| `kagi` | `apiKey` | `KAGI_API_KEY` | 否 |
| `olostep` | `apiKey` | `OLOSTEP_API_KEY` | 否 |
| `searxng` | `baseUrl` | `SEARXNG_BASE_URL` | 是（自托管） |
| `duckduckgo`（默认） | — | — | 是 |

**Brave：**
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "BSA..."
      }
    }
  }
}
```

**Tavily：**
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "tavily",
        "apiKey": "tvly-..."
      }
    }
  }
}
```

**Jina**（包含 1000 万令牌的免费层）：
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "jina",
        "apiKey": "jina_..."
      }
    }
  }
}
```

**Kagi：**
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "kagi",
        "apiKey": "your-kagi-api-key"
      }
    }
  }
}
```

**Olostep：**
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "olostep",
        "apiKey": "YOUR_OLOSTEP_API_KEY"
      }
    }
  }
}
```

您也可以在环境中设置 `OLOSTEP_API_KEY`，而不是将其存储在配置中。

**SearXNG**（自托管，不需要 API 密钥）：
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "searxng",
        "baseUrl": "https://searx.example"
      }
    }
  }
}
```

**DuckDuckGo**（零配置）：
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "duckduckgo"
      }
    }
  }
}
```

#### `tools.web.search`

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `provider` | string | `"duckduckgo"` | 搜索后端：`brave`、`tavily`、`jina`、`searxng`、`duckduckgo` |
| `apiKey` | string | `""` | Brave 或 Tavily 的 API 密钥 |
| `baseUrl` | string | `""` | SearXNG 的基础 URL |
| `maxResults` | integer | `5` | 每次搜索的结果数（1–10） |

### Web 获取

> [!TIP]
> 如果您遇到 JS 工作量证明或 Cloudflare 验证码问题，请设置随机用户代理并禁用 Jina Reader：
> ```json
> { "tools": { "web": { "userAgent": "Not-A-Browser", "fetch": { "useJinaReader": false } } } }
> ```

nanobot 默认使用 [Jina Reader](https://jina.ai/reader/)（第三方 API）将任意页面转换为 Markdown 格式，以便 LLM 轻松消化，如果前者失败，则使用基于 [readability-lxml](https://github.com/buriy/python-readability) 的本地回退。

如果您想始终使用本地转换，可以使用以下命令强制使用：

```json
{
  "tools": {
    "web": {
      "fetch": {
        "useJinaReader": false
      }
    }
  }
}
```

#### `tools.web.fetch`

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `useJinaReader` | boolean | `true` | 如果为 true，Jina Reader 将优先于本地转换 |

## 图像生成

图像生成在 `tools.imageGeneration` 下配置，并使用来自 `providers.openrouter` 或 `providers.aihubmix` 的提供商凭据。

有关 WebUI 用法、提供商示例、工件存储和故障排除，请参阅[图像生成](./image-generation-zh.md)。

## MCP（模型上下文协议）

> [!TIP]
> 配置格式与 Claude Desktop / Cursor 兼容。您可以直接从任何 MCP 服务器的 README 复制 MCP 服务器配置。

nanobot 支持 [MCP](https://modelcontextprotocol.io/) — 连接外部工具服务器并将其用作原生代理工具。

将 MCP 服务器添加到您的 `config.json`：

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
      },
      "my-remote-mcp": {
        "url": "https://example.com/mcp/",
        "headers": {
          "Authorization": "Bearer xxxxx"
        }
      }
    }
  }
}
```

支持两种传输模式：

| 模式 | 配置 | 示例 |
|------|--------|---------|
| **Stdio** | `command` + `args` | 通过 `npx` / `uvx` 的本地进程 |
| **HTTP** | `url` + `headers`（可选） | 远程端点（`https://mcp.example.com/sse`） |

使用 `toolTimeout` 覆盖慢速服务器的默认 30 秒每次调用超时：

```json
{
  "tools": {
    "mcpServers": {
      "my-slow-server": {
        "url": "https://example.com/mcp/",
        "toolTimeout": 120
      }
    }
  }
}
```

使用 `enabledTools` 仅注册来自 MCP 服务器的工具子集：

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
        "enabledTools": ["read_file", "mcp_filesystem_write_file"]
      }
    }
  }
}
```

`enabledTools` 接受原始 MCP 工具名称（例如 `read_file`）或包装的 nanobot 工具名称（例如 `mcp_filesystem_write_file`）。

- 省略 `enabledTools`，或将其设置为 `["*"]`，以注册所有工具。
- 将 `enabledTools` 设置为 `[]`，以不从该服务器注册任何工具。
- 将 `enabledTools` 设置为非空名称列表，以仅注册该子集。

MCP 工具在启动时自动发现和注册。LLM 可以将它们与内置工具一起使用 — 无需额外配置。




## 安全

> [!TIP]
> 对于生产部署，请在您的配置中设置 `"restrictToWorkspace": true` 和 `"tools.exec.sandbox": "bwrap"` 以对代理进行沙箱化。
> 在 `v0.1.4.post3` 及更早版本中，空的 `allowFrom` 允许所有发送者。自 `v0.1.4.post4` 起，空的 `allowFrom` 默认拒绝所有访问。要允许所有发送者，请设置 `"allowFrom": ["*"]`。

| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `tools.restrictToWorkspace` | `false` | 当为 `true` 时，将**所有**代理工具（shell、文件读/写/编辑、列表）限制在工作区目录内。防止路径遍历和超出范围的访问。 |
| `tools.exec.sandbox` | `""` | Shell 命令的沙箱后端。设置为 `"bwrap"` 以将 exec 调用包装在 [bubblewrap](https://github.com/containers/bubblewrap) 沙箱中 — 进程只能看到工作区（读写）和媒体目录（只读）；配置文件和 API 密钥是隐藏的。自动为文件工具启用 `restrictToWorkspace`。**仅限 Linux** — 需要安装 `bwrap`（`apt install bubblewrap`；Docker 镜像中预装）。在 macOS 或 Windows 上不可用（bwrap 依赖于 Linux 内核命名空间）。 |
| `tools.exec.enable` | `true` | 当为 `false` 时，根本不会注册 shell `exec` 工具。使用此选项完全禁用 shell 命令执行。 |
| `tools.exec.pathAppend` | `""` | 在运行 shell 命令时要附加到 `PATH` 的额外目录（例如用于 `ufw` 的 `/usr/sbin`）。 |
| `channels.*.allowFrom` | `[]`（拒绝所有） | 用户 ID 白名单。空表示拒绝所有；使用 `["*"]` 允许所有人。 |

**Docker 安全**：官方 Docker 镜像以非 root 用户（`nanobot`，UID 1000）运行，并预装了 bubblewrap。使用 `docker-compose.yml` 时，容器会删除所有 Linux 功能，除了 `SYS_ADMIN`（bwrap 的命名空间隔离所需）。


## 子代理并发

默认情况下，nanobot 一次只允许一个生成的子代理。当达到限制时，`spawn` 工具会返回错误，以便代理可以决定等待或重新安排其工作。这可以保护本地 LLM 服务器不会一次加载多个 KV 缓存。如果您的提供商可以处理更多并行工作，请提高限制：

```json
{
  "agents": {
    "defaults": {
      "maxConcurrentSubagents": 2
    }
  }
}
```

| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `agents.defaults.maxConcurrentSubagents` | `1` | 可以同时运行的最大生成子代理数。尝试生成超过此限制的子代理将返回错误。 |


## 自动压缩

当用户空闲时间超过配置的阈值时，nanobot 会**主动**将会话上下文的较旧部分压缩为摘要，同时保留最近的有效后缀实时消息。这可以减少令牌成本和首令牌延迟，当用户返回时 — 模型不会重新处理过期的 KV 缓存的陈旧上下文，而是接收紧凑的摘要、最新的实时上下文和新鲜输入。

```json
{
  "agents": {
    "defaults": {
      "idleCompactAfterMinutes": 15
    }
  }
}
```

| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `agents.defaults.idleCompactAfterMinutes` | `0`（禁用） | 自动压缩开始前的空闲分钟数。设置为 `0` 以禁用。建议：`15` — 接近典型的 LLM KV 缓存过期窗口，以便陈旧会话在用户返回之前被压缩。 |

`sessionTtlMinutes` 仍被接受为向后兼容的传统别名，但 `idleCompactAfterMinutes` 是将来首选的配置键。

工作原理：
1. **空闲检测**：在每个空闲滴答（~1 秒）时，检查所有会话是否过期。
2. **后台压缩**：空闲会话通过 LLM 总结较旧的实时前缀，并保留最新的有效后缀（当前为 8 条消息）。
3. **摘要注入**：当用户返回时，摘要将作为运行时上下文（一次性，不持久化）与保留的最近后缀一起注入。
4. **重启安全恢复**：摘要也会镜像到会话元数据中，以便在进程重启后仍可恢复。

> [!NOTE]
> 心智模型："总结较旧的上下文，保留最新的实时回合，**并使用紧凑形式覆盖会话文件。**" 这不是完整的 `session.clear()`，但这是一个写入 — 而不是软光标移动。
>
> 具体来说，自动压缩就地重写 `sessions/<key>.jsonl`：较旧的消息（包括其结构化的 `tool_calls` / `tool_call_id` / `reasoning_content`）被替换为仅保留的最近后缀（当前为 8 条消息），而存档的前缀仅作为附加到 `memory/history.jsonl` 的纯文本摘要（或如果 LLM 总结失败，则为 `[RAW] ...` 展平转储）保留。这些回合的原始 JSON 不再可以从会话文件中恢复。
>
> 这与在提示超过上下文预算时触发的**令牌驱动的软合并**不同：该路径仅推进内部 `last_consolidated` 光标并保持会话文件不变，因此原始工具调用轨迹仍保留在磁盘上，仍可重播或审计。如果您依赖该轨迹进行调试或审计，请将 `idleCompactAfterMinutes` 保持在默认值 `0`，并仅运行令牌驱动的路径。

## 时区

时间就是上下文。上下文应该精确。

默认情况下，nanobot 使用 `UTC` 作为运行时时间上下文。如果您希望代理按您的本地时间思考，请将 `agents.defaults.timezone` 设置为有效的 [IANA 时区名称](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)：

```json
{
  "agents": {
    "defaults": {
      "timezone": "Asia/Shanghai"
    }
  }
}
```

这会影响显示给模型的运行时时间字符串，例如运行时上下文和心跳提示。它也成为 cron 计划的默认时区（当 cron 表达式省略 `tz` 时），以及一次性 `at` 时间的默认时区（当 ISO 日期时间没有明确偏移时）。

常见示例：`UTC`、`America/New_York`、`America/Los_Angeles`、`Europe/London`、`Europe/Berlin`、`Asia/Tokyo`、`Asia/Shanghai`、`Asia/Singapore`、`Australia/Sydney`。

> 需要其他时区？浏览完整的 [IANA 时区数据库](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)。

## 统一会话

默认情况下，每个通道 × 聊天 ID 组合都有自己的会话。如果您在多个通道（例如 Telegram + Discord + CLI）中使用 nanobot 并希望它们共享相同的对话，请启用 `unifiedSession`：

```json
{
  "agents": {
    "defaults": {
      "unifiedSession": true
    }
  }
}
```

启用后，所有传入消息 — 无论它们在哪个通道上到达 — 都会路由到单个共享会话。从 Telegram 切换到 Discord（或任何其他通道）可以无缝继续相同的对话。

| 行为 | `false`（默认） | `true` |
|----------|-------------------|--------|
| 会话键 | `channel:chat_id` | `unified:default` |
| 跨通道连续性 | 否 | 是 |
| `/new` 清除 | 当前通道会话 | 共享会话 |
| `/stop` 查找任务 | 按通道会话 | 按共享会话 |
| 现有 `session_key_override`（例如 Telegram 线程） | 受尊重 | 仍受尊重 — 未覆盖 |

> 这是为单用户多设备设置设计的。它**默认关闭** — 现有用户看到零行为更改。

## 禁用的技能

nanobot 附带内置技能，您的工作区也可以在 `skills/` 下定义自定义技能。如果您想从代理中隐藏特定技能，请将 `agents.defaults.disabledSkills` 设置为技能目录名称列表：

```json
{
  "agents": {
    "defaults": {
      "disabledSkills": ["github", "weather"]
    }
  }
}
```

禁用的技能从主代理的技能摘要、始终启用的技能注入和子代理技能摘要中排除。当某些捆绑技能对于您的部署不必要或不应该暴露给最终用户时，这很有用。

| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `agents.defaults.disabledSkills` | `[]` | 要从加载中排除的技能目录名称列表。适用于内置技能和工作区技能。 |

## 工具提示最大长度

工具提示是代理调用工具时显示的简短进度消息（例如 `$ cd …/project && npm test`）。默认情况下，这些在 40 个字符处截断，这可能会使长命令难以阅读。

设置 `agents.defaults.toolHintMaxLength` 以控制截断阈值：

```json
{
  "agents": {
    "defaults": {
      "toolHintMaxLength": 120
    }
  }
}
```

| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `agents.defaults.toolHintMaxLength` | `40` | 工具提示显示的最大字符数。范围：20–500。较高的值显示更多的命令或路径；较低的值保持提示紧凑。 |
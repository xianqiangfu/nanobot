# 工具函数

本模块提供 nanobot 中使用的各种工具函数和辅助函数。

## 核心组件

### Helpers (`helpers.py`)

通用辅助函数：

- `ensure_dir` - 确保目录存在
- `truncate_text` - 截断文本
- `build_assistant_message` - 构建助手消息
- `extract_reasoning` - 提取推理内容
- `strip_think` - 移除思考标记
- `estimate_message_tokens` - 估算消息 token 数
- `image_placeholder_text` - 生成图片占位符文本

### Path (`path.py`)

路径处理工具：

- `abbreviate_path` - 缩写路径（如 `/home/user/project` → `~/project`）

### Artifacts (`artifacts.py`)

工件处理：

- `generated_image_paths_from_messages` - 从消息中提取生成的图片路径

### Document (`document.py`)

文档处理：

- `extract_documents` - 从消息中提取文档内容

### Evaluator (`evaluator.py`)

评估工具。

### GitStore (`gitstore.py`)

Git 存储工具。

### Image Generation Intent (`image_generation_intent.py`)

图像生成意图检测：

- `image_generation_prompt` - 检测并格式化图像生成提示词

### Logging Bridge (`logging_bridge.py`)

日志桥接工具。

### Media Decode (`media_decode.py`)

媒体解码工具。

### Progress Events (`progress_events.py`)

进度事件处理。

### Prompt Templates (`prompt_templates.py`)

提示词模板：

- `render_template` - 渲染提示词模板

### Restart (`restart.py`)

重启管理：

- `set_restart_notice_to_env` - 设置重启通知
- `consume_restart_notice_from_env` - 消费重启通知
- `format_restart_completed_message` - 格式化重启完成消息

### Runtime (`runtime.py`)

运行时工具：
- `EMPTY_FINAL_RESPONSE_MESSAGE` - 空响应消息常量
- `build_finalization_retry_message` - 构建最终重试消息
- `build_length_recovery_message` - 构建长度恢复消息
- `ensure_nonempty_tool_result` - 确保工具结果非空
- `is_blank_text` - 检查文本是否为空
- `repeated_external_lookup_error` - 检测重复的外部查找错误
- `repeated_workspace_violation_error` - 检测重复的工作区违规错误

### Search Usage (`searchusage.py`)

搜索使用统计。

### Tool Hints (`tool_hints.py`)

工具提示生成。

### WebUI Titles (`webui_titles.py`)

WebUI 标题生成：
- `mark_webui_session` - 标记 WebUI 会话
- `maybe_generate_webui_title_after_turn` - 生成 WebUI 会话标题

## API 示例

### 目录操作

```python
from nanobot.utils import ensure_dir

# 确保目录存在
ensure_dir("~/.nanobot/sessions")
ensure_dir("/tmp/nanobot/cache")
```

### 路径处理

```python
from nanobot.utils import abbreviate_path

# 缩写路径
path = "/home/user/projects/nanobot"
short_path = abbreviate_path(path)  # "~/projects/nanobot"
```

### 文本处理

```python
from nanobot.utils.helpers import truncate_text, build_assistant_message

# 截断文本
text = "这是一段很长的文本..."
short_text = truncate_text(text, max_length=100)

# 构建助手消息
msg = build_assistant_message(
    content="回复内容",
    tool_calls=[...]
)
```

### Token 估算

```python
from nanobot.utils.helpers import estimate_message_tokens

# 估算消息 token 数
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的？"}
]
tokens = estimate_message_tokens(messages)
```

### 提示词模板

```python
from nanobot.utils.prompt_templates import render_template

# 渲染模板
template = "你是 {{name}}，任务是 {{task}}。"
result = render_template(
    template,
    name="助手",
    task="帮助用户"
)
# "你是 助手，任务是 帮助用户。"
```

### 重启管理

```python
from nanobot.utils.restart import (
    set_restart_notice_to_env,
    consume_restart_notice_from_env
)

# 设置重启通知
set_restart_notice_to_env("升级成功，正在重启...")

# 消费重启通知
notice = consume_restart_notice_from_env()
if notice:
    print(f"重启原因: {notice}")
```

## 注意事项

- 大多数函数都是纯函数，无副作用
- 路径处理支持 `~` 展开为家目录
- Token 估算是近似值
- 所有路径都应使用绝对路径

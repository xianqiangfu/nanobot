# 提示词模板

本模块提供提示词模板管理和渲染功能。

## 概述

`templates/` 目录包含 nanobot 使用的提示词模板，用于构建和格式化发送给 LLM 的系统提示词和上下文。

## 核心组件

### Prompt Templates (`utils/prompt_templates.py`)

提示词模板工具：

```python
def render_template(template: str, **kwargs) -> str:
    """渲染提示词模板。"""
    # 实现模板渲染逻辑
    pass
```

## 模板语法

模板使用简单的变量替换语法：

```
你是一个 {{role}}，主要任务是 {{task}}。

## 能力

- {{ability1}}
- {{ability2}}
- {{ability3}}

## 约束

- {{constraint1}}
- {{constraint2}}
```

## 使用示例

### 基本渲染

```python
from nanobot.utils.prompt_templates import render_template

template = """你是一个 {{role}}，帮助用户完成 {{task}}。"""

result = render_template(
    template,
    role="编程助手",
    task="代码审查"
)

# "你是一个 编程助手，帮助用户完成 代码审查。"
```

### 复杂模板

```python
template = """
# 系统提示

你是一个 {{role}}。

## 职责

{{responsibilities}}

## 工具

你有以下工具可用：
{{#tools}}
- {{name}}: {{description}}
{{/tools}}

## 约束

{{constraints}}
"""

result = render_template(
    template,
    role="AI 助手",
    responsibilities="帮助用户解决问题",
    tools=[
        {"name": "搜索", "description": "搜索网络信息"},
        {"name": "计算", "description": "执行计算"}
    ],
    constraints="不执行危险操作"
)
```

## 模板变量

### 常用变量

- `role` - 角色定义
- `task` - 主要任务
- `abilities` - 能力列表
- `constraints` - 约束条件
- `tools` - 可用工具

## 配置集成

模板可以在配置文件中定义：

```json
{
  "agent": {
    "systemPrompt": "你是一个 {{role}}，任务是 {{task}}。",
    "promptVariables": {
      "role": "编程助手",
      "task": "帮助用户编写和调试代码"
    }
  }
}
```

## 上下文构建

模板用于构建对话上下文：

```python
from nanobot.agent import ContextBuilder
from nanobot.utils.prompt_templates import render_template

# 构建系统提示词
system_prompt = render_template(
    template="你是 {{role}}",
    role="AI 助手"
)

# 添加到上下文
context = ContextBuilder()
context.add_system_message(system_prompt)
```

## 注意事项

- 模板使用简单的字符串替换
- 变量名区分大小写
- 未定义的变量会保持原样
- 模板应该使用 UTF-8 编码
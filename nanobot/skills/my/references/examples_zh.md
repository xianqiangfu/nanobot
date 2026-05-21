# My Tool — 实用示例

展示何时以及如何有效使用 my 工具的具体场景。

## 诊断

### "为什么你不能搜索网络?"
```
→ my(action="check", key="web_config.enable")
  → False
→ "网络搜索已禁用。在配置中添加 web.enable: true 以启用它。"
```

### "你为什么停止了?"
```
→ my(action="check", key="max_iterations")
  → 40
→ my(action="check", key="_last_usage")
  → {"prompt_tokens": 62000, "completion_tokens": 3000}
→ "我达到了迭代限制 (40)。这个任务很复杂。我可以询问用户是否想要增加它。"
```

### "你在运行什么模型?"
```
→ my(action="check", key="model")
  → 'anthropic/claude-sonnet-4-20250514'
```

## 自适应行为

### 大型代码库分析
```
→ my(action="check")
  → context_window_tokens: 65536
→ my(action="set", key="context_window_tokens", value=131072)
  → "Set context_window_tokens = 131072 (was 65536)"
→ "我已经扩展了我的上下文窗口来处理这个大型代码库。"
```

### 切换到更快的模型用于重复性任务
```
→ my(action="set", key="model", value="anthropic/claude-haiku-4-5-20251001")
  → "Set model = 'anthropic/claude-haiku-4-5-20251001' (was 'anthropic/claude-sonnet-4-20250514')"
→ "已切换到更快的模型来处理这些批量任务。"
```

## 跨轮次记忆

### 记住用户偏好
```
# 第 1 轮: 用户说"保持简洁"
→ my(action="set", key="user_style", value="concise")
  → "Set scratchpad.user_style = 'concise'"

# 第 3 轮: 新话题
→ my(action="check", key="user_style")
  → 'concise'
  (相应地调整响应风格)
```

### 跟踪项目上下文
```
→ my(action="set", key="active_branch", value="feat/auth")
→ my(action="set", key="test_framework", value="pytest")
→ my(action="set", key="has_docker", value=true)
```

## 预算意识

### token 感知行为
```
→ my(action="check", key="_last_usage")
  → {"prompt_tokens": 58000, "completion_tokens": 12000}
→ "我已经消耗了约 70k token。我会保持剩余响应的简洁性。"
```

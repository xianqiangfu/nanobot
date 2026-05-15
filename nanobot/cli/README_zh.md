# 命令行接口

本模块提供 nanobot 的命令行工具。

## 主要命令

### nanobot gateway

启动 nanobot 网关，处理所有频道和智能体循环：

```bash
nanobot gateway
```

### nanobot model

模型管理命令：

```bash
nanobot model list              # 列出可用模型
nanobot model set <model>       # 设置默认模型
```

### nanobot onboard

交互式配置向导，帮助用户初始化配置：

```bash
nanobot onboard
```

## 核心组件

### Commands (`commands.py`)

CLI 命令实现，使用 Typer 框架。

### Models (`models.py`)

模型管理命令。

### Onboard (`onboard.py`)

配置向导实现。

### Stream (`stream.py`)

流式输出处理。

## 使用示例

### 启动网关

```bash
# 基本启动
nanobot gateway

# 指定配置文件
nanobot gateway --config /path/to/config.json

# 调试模式
nanobot gateway --debug

# 指定日志级别
nanobot gateway --log-level DEBUG
```

### 模型管理

```bash
# 列出所有可用模型
nanobot model list

# 设置默认模型
nanobot model set anthropic:claude-3-5-sonnet-20241022

# 查看当前模型
nanobot model current
```

### 配置向导

```bash
# 启动配置向导
nanobot onboard

# 向导会引导你完成：
# 1. 选择 LLM 提供商
# 2. 配置 API 密钥
# 3. 选择要启用的频道
# 4. 配置频道凭证
```

## 日志格式

统一的日志格式：

```
2024-05-14 10:30:45 | INFO  | telegram:123456 | 收到新消息
2024-05-14 10:30:46 | DEBUG | agent          | 调用工具: read_file
2024-05-14 10:30:47 | INFO  | agent          | 完成轮次，用时 2.1s
```

## Windows 支持

CLI 在 Windows 上强制使用 UTF-8 编码：

```python
# 自动配置控制台编码
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

## 交互功能

### REPL 模式

支持交互式 REPL 模式：

```bash
nanobot repl
```

### 丰富的输出

使用 Rich 库提供格式化输出：

- 表格显示
- Markdown 渲染
- 语法高亮
- 进度条

## 注意事项

- 所有命令使用异步执行
- 支持 Ctrl+C 优雅停止
- 配置文件路径默认为 `~/.nanobot/config.json`
- 会话数据存储在 `~/.nanobot/sessions/`
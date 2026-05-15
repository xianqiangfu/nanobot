# 工具系统

本模块提供可扩展的工具系统，允许 LLM 调用外部能力。

## 核心组件

### Tool (`base.py`)

工具基类，所有工具都必须继承自此类：

```python
from nanobot.agent.tools import Tool, tool_parameters

class MyTool(Tool):
    """我的自定义工具。"""

    async def execute(self, params: dict[str, Any]) -> str:
        # 实现工具逻辑
        return "工具结果"
```

### ToolRegistry (`registry.py`)

工具注册表，管理所有可用工具：

- 注册和注销工具
- 工具查询和枚举
- 工具元数据管理

### ToolLoader (`loader.py`)

动态加载工具，支持从配置加载和插件系统。

### ToolContext (`context.py`)

工具执行上下文，提供：

- 当前会话信息
- 消息总线
- 配置访问
- 其他工具引用

### Schema (`schema.py`)

工具参数 schema 定义，支持：

- StringSchema - 字符串类型
- IntegerSchema - 整数类型
- NumberSchema - 数字类型
- BooleanSchema - 布尔类型
- ObjectSchema - 对象类型
- ArraySchema - 数组类型

## 内置工具

### 文件系统工具 (`filesystem.py`)

- `read_file` - 读取文件内容
- `write_file` - 写入文件内容
- `edit_file` - 编辑文件
- `list_dir` - 列出目录内容

### Shell 工具 (`shell.py`)

- `exec` - 执行 Shell 命令

### Web 工具 (`web.py`)

- `web_search` - Web 搜索
- `web_fetch` - 获取 Web 页面

### 搜索工具 (`search.py`)

- `grep` - 文本搜索
- `glob` - 文件模式匹配

### MCP 工具 (`mcp.py`)

- 支持 MCP (Model Context Protocol) 服务器
- 自动发现和加载 MCP 工具

### 其他工具

- `message` - 发送消息到频道
- `spawn` - 派生子智能体
- `notebook` - 编辑 Jupyter 笔记本
- `cron` - 定时任务管理
- `image_generation` - 图像生成

## 创建自定义工具

```python
from nanobot.agent.tools import Tool

class MyCustomTool(Tool):
    """自定义工具描述。"""

    name = "my_tool"

    async def execute(self, params: dict[str, Any]) -> str:
        # 从 params 中获取参数
        param1 = params.get("param1")

        # 执行工具逻辑
        result = do_something(param1)

        # 返回结果
        return str(result)
```

## 工具参数验证

使用 schema 定义工具参数：

```python
from nanobot.agent.tools import Tool
from nanobot.agent.tools.schema import StringSchema, IntegerSchema

class ValidatedTool(Tool):
    """带参数验证的工具。"""

    parameters = {
        "name": StringSchema(description="名称", required=True),
        "count": IntegerSchema(description="数量", default=1),
    }

    async def execute(self, params: dict[str, Any]) -> str:
        name = params["name"]
        count = params.get("count", 1)
        return f"{name} x {count}"
```

## 注意事项

- 工具执行是异步的
- 工具应返回字符串或可序列化为字符串的结果
- 工具可以访问工具上下文获取额外信息
- 工具注册到注册表后才能被 LLM 调用
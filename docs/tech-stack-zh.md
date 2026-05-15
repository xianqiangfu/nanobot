# nanobot 技术栈梳理

本文档梳理 nanobot 项目使用的核心技术栈和设计模式。

## 核心技术栈

### Python 3.11+ 核心库

#### 异步编程 (asyncio)

nanobot 完全基于 asyncio 构建，关键特性：

- **事件循环驱动** - 所有 I/O 操作都使用 async/await
- **并发处理** - 多个会话和工具调用可以并发执行
- **非阻塞 I/O** - WebSocket、HTTP、文件操作都不阻塞主线程
- **任务管理** - 使用 `asyncio.create_task` 创建并发任务
- **超时控制** - 使用 `asyncio.wait_for` 和 `asyncio.timeout`

**关键模式**：

```python
# 并发处理多个消息
tasks = [process_message(msg) for msg in messages]
results = await asyncio.gather(*tasks)

# 超时控制
async with asyncio.timeout(30):
    result = await long_running_operation()
```

#### Pydantic 配置与验证体系

**配置 Schema** (`nanobot/config/schema.py`)

- **类型验证** - 使用 Pydantic 模型定义配置结构
- **默认值** - 为所有配置项提供合理默认值
- **别名支持** - 支持 camelCase 和 snake_case 双模式
- **嵌套结构** - 支持复杂嵌套配置
- **环境变量** - 通过 `pydantic-settings` 支持环境变量覆盖

**关键特性**：

```python
class Base(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
```

#### 日志系统 (loguru)

**日志架构** (`nanobot/` 各模块)

- **结构化日志** - 使用 loguru 的 bind 功能添加上下文
- **日志级别** - DEBUG、INFO、WARNING、ERROR、CRITICAL
- **日志轮转** - 自动日志文件轮转和压缩
- **彩色输出** - 终端彩色输出提升可读性
- **性能优化** - 异步日志写入不阻塞主流程

**关键用法**：

```python
logger = logger.bind(channel="telegram", chat_id=123456)
logger.info("Received message")
logger.debug("Tool called", tool="read_file")
```

#### WebSocket 协议实现

**WebSocket 通信** (`nanobot/channels/websocket.py`, `nanobot/web/`)

- **双工通信** - 全双工实时通信
- **消息复用** - 多路复用协议支持多个会话
- **心跳保活** - 定期心跳保持连接
- **自动重连** - 连接断开时自动重连
- **二进制支持** - 支持二进制数据传输

**协议特点**：

```python
# 消息复用协议
{
    "type": "message",
    "chat_id": "session_key",
    "payload": {...}
}
```

#### Jinja2 模板引擎

**提示词模板** (`nanobot/templates/`, `nanobot/utils/prompt_templates.py`)

- **变量替换** - 支持 `{{variable}}` 语法
- **条件渲染** - 支持 `{% if %}` 条件
- **循环渲染** - 支持 `{% for %}` 循环
- **模板继承** - 支持模板继承和包含
- **缓存优化** - 编译后的模板缓存

**应用场景**：

- 系统提示词构建
- 响应格式化
- 技能系统

## LLM 提供商生态

### Anthropic API 集成

**Claude 模型** (`nanobot/providers/anthropic_provider.py`)

- **完整支持** - 支持 Claude 3.5 Sonnet、Opus、Haiku 等模型
- **工具调用** - 原生支持 Claude 工具调用 API
- **流式响应** - 支持 Claude 流式 API
- **思考模式** - 支持 Claude extended thinking
- **提示词缓存** - 支持 Claude prompt caching
- **图片输入** - 支持多模态图片输入

### OpenAI API 兼容层

**统一抽象** (`nanobot/providers/openai_compat_provider.py`)

- **统一接口** - 为所有 OpenAI 兼容 API 提供统一接口
- **多提供商** - 支持 OpenAI、DeepSeek、Moonshot、Kimi 等
- **流式兼容** - 统一的流式响应处理
- **工具适配** - 将 OpenAI 格式的工具调用转换为统一格式

**支持的提供商**：

- OpenAI (GPT-4、GPT-3.5)
- DeepSeek (DeepSeek 系列)
- Moonshot (Moonshot 系列)
- Kimi (月之暗面)
- 其他 OpenAI 兼容 API

### 多提供商统一抽象

**基类设计** (`nanobot/providers/base.py`)

- **LLMProvider** - 所有提供商的基类
- **统一响应** - `LLMResponse` 统一响应格式
- **工具调用** - `ToolCallRequest` 统一工具调用格式
- **错误处理** - 统一的错误处理和重试逻辑
- **流式接口** - 统一的流式 API

**关键接口**：

```python
class LLMProvider(ABC):
    async def complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs
    ) -> LLMResponse:
        ...

    async def stream_complete(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        **kwargs
    ):
        ...
```

### 流式响应处理机制

**增量处理** (`nanobot/agent/runner.py`)

- **Delta 合并** - 智能合并消息增量，减少渲染次数
- **占位符管理** - 工具调用和推理阶段的占位符管理
- **自动清理** - 完成后自动清理临时占位符
- **错误恢复** - 流式中断时的错误恢复

**处理流程**：

```python
async for chunk in provider.stream_complete(messages, tools):
    if chunk.content_delta:
        message.content += chunk.content_delta
    if chunk.tool_calls:
        handle_tool_calls(chunk.tool_calls)
```

### 思考模式 (reasoning) 支持

**模型推理** (`nanobot/providers/base.py`)

- **推理内容** - `reasoning_content` 字段存储推理过程
- **思考块** - `thinking_blocks` 存储结构化思考块
- **控制显示** - 通过配置控制是否显示推理
- **Token 优化** - 推理不计入响应 token

**支持的模型**：

- Anthropic Claude (extended thinking)
- Kimi (推理模式)
- DeepSeek-R1 (推理模式)

### 提示词缓存 (prompt caching) 机制

**缓存策略** (`nanobot/providers/`)

- **系统提示** - 缓存不变的系统提示词
- **技能内容** - 缓存技能系统内容
- **减少成本** - 缓存的提示词不计入费用
- **性能提升** - 减少网络传输和解析时间

## 前端技术栈

### React + TypeScript 架构

**组件化设计** (`webui/src/components/`)

- **函数组件** - 所有组件使用函数组件
- **Hooks 模式** - 使用 React Hooks 管理状态
- **TypeScript** - 完整的类型安全
- **组件库** - shadcn/ui + Radix UI
- **模块化** - 按功能组织组件

**目录结构**：

```
src/
├── components/     # UI 组件
├── hooks/          # 自定义 Hooks
├── lib/            # 工具库
├── i18n/           # 国际化
└── providers/      # Context Providers
```

### Vite 构建系统

**构建配置** (`webui/vite.config.ts`)

- **快速热更新** - 原生 ES 模块热更新
- **开发代理** - 代理 API 请求到后端
- **生产优化** - 自动代码分割和压缩
- **TypeScript 支持** - 内置 TypeScript 支持
- **路径别名** - `@/` 指向 `src/` 目录

**关键配置**：

```ts
{
  server: {
    proxy: {
      '/api': 'http://localhost:8765',
      '/webui': 'http://localhost:8765',
      '/auth': 'http://localhost:8765',
    }
  }
}
```

### TailwindCSS 样式系统

**样式架构** (`webui/`, `webui/src/globals.css`)

- **实用优先** - 使用 utility-first 方法
- **深色模式** - 完整的深色模式支持
- **响应式** - 移动优先的响应式设计
- **自定义主题** - 扩展 Tailwind 主题
- **组件样式** - 使用 `@apply` 复用样式

**关键特性**：

```css
/* 深色模式 */
@media (prefers-color-scheme: dark) {
  :root {
    --background: 222.2 84% 4.9%;
  }
}
```

### Radix UI 组件库

**基础组件** (`webui/src/components/ui/`)

- **无障碍** - 完整的 ARIA 支持
- **键盘导航** - 完整的键盘操作支持
- **可定制** - 高度可定制的组件
- **轻量级** - 按需导入，减少打包体积

**主要组件**：

- Dialog - 模态对话框
- Sheet - 侧边抽屉
- ScrollArea - 可滚动区域
- Tooltip - 工具提示
- Dropdown - 下拉菜单
- AlertDialog - 警告对话框

### i18next 国际化

**国际化系统** (`webui/src/i18n/`)

- **多语言支持** - 支持中英文切换
- **命名空间** - 按模块组织翻译
- **插值** - 支持变量插值
- **复数** - 支持复数形式
- **日期格式化** - 本地化日期格式

**使用示例**：

```tsx
const { t } = useTranslation();
const text = t('common.send');
const message = t('chat.welcome', { name: 'User' });
```

### Vitest 测试框架

**测试架构** (`webui/src/tests/`)

- **组件测试** - 使用 React Testing Library
- **Hook 测试** - 使用 `@testing-library/react`
- **单元测试** - 测试函数和工具
- **集成测试** - 测试组件交互
- **覆盖率报告** - 完整的覆盖率报告

**测试命令**：

```bash
npm test              # 运行所有测试
npm test -- --watch   # 监听模式
npm test -- --coverage # 覆盖率报告
```

## 设计模式

### 架构模式

| 模式 | 应用 | 说明 |
|------|------|------|
| 生产者-消费者 | MessageBus | 解耦通道和智能体 |
| 策略模式 | Channels/Providers | 不同平台/提供商适配 |
| 工厂模式 | ProviderFactory | 提供商实例化 |
| 注册表模式 | ToolRegistry | 工具管理 |
| 状态机 | TurnState | 轮次流程控制 |
| 模板方法 | BaseChannel | 通道生命周期 |
| 观察者 | Hook 系统 | 事件扩展 |
| 中介者 | ChannelManager | 通道协调 |

### 代码模式

- **异步优先** - 所有 I/O 操作使用 async/await
- **依赖注入** - 通过构造函数注入依赖
- **单一职责** - 每个模块职责单一
- **开闭原则** - 通过扩展而非修改添加功能
- **接口隔离** - 最小化接口定义

## 性能优化

### 后端优化

- **异步 I/O** - 非阻塞的文件、网络操作
- **连接池** - HTTP 连接复用
- **缓存策略** - 工具定义、提示词缓存
- **流式处理** - 流式响应减少延迟
- **并发控制** - 控制并发工具调用数量

### 前端优化

- **代码分割** - 按路由分割代码
- **懒加载** - 组件和资源懒加载
- **虚拟滚动** - 大列表虚拟滚动
- **防抖节流** - 输入防抖，滚动节流
- **Web Worker** - 图片编码使用 Worker

## 安全考虑

- **输入验证** - Pydantic 验证所有输入
- **路径限制** - 工具操作限制在工作目录
- **SSRF 防护** - 阻止内部网络访问
- **API 密钥保护** - 不记录日志，环境变量存储
- **MCP 隔离** - MCP 工具独立命名空间
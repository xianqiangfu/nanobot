# nanobot 项目全方位深度调研与梳理 - Todo 清单

> 本清单记录了对 nanobot 项目进行全面深度调研、文档编写、代码注释、图表绘制等任务的完整工作计划。

## GitHub Issues 追踪

本项目的所有任务已拆分为 GitHub Issues，详情请查看：
- **总览 Issue**: [nanobot 项目全方位深度调研与梳理 - 总览](https://github.com/xianqiangfu/nanobot/issues/37)

---

## 📋 任务概览

| 类别 | 任务数 | 完成度 | 说明 |
|------|--------|--------|------|
| 项目调研与梳理 | 10 | 0% | 核心架构分析、技术栈整理 |
| 文档编写 | 30 | 0% | README 编写、教程编写 |
| 图表绘制 | 15 | 0% | 架构图、流程图、时序图 |
| 代码注释 | 150+ | 0% | 为所有代码文件添加中文注释 |
| 资料补充 | 20 | 0% | 补充开发指南、最佳实践等 |

---

## 第一阶段：项目调研与基础梳理

### 1.1 核心架构调研
- [ ] 分析项目整体架构设计
- [ ] 梳理核心数据流（消息总线、Agent 循环）
- [ ] 分析模块间依赖关系
- [ ] 整理关键技术栈和依赖库
- [ ] 识别项目设计模式和架构约束

### 1.2 子模块深度调研
- [ ] Agent 循环模块 (`nanobot/agent/`) 调研
- [ ] 消息总线模块 (`nanobot/bus/`) 调研
- [ ] 通道模块 (`nanobot/channels/`) 调研
- [ ] 提供商模块 (`nanobot/providers/`) 调研
- [ ] 工具模块 (`nanobot/agent/tools/`) 调研
- [ ] 配置系统 (`nanobot/config/`) 调研
- [ ] 会话管理 (`nanobot/session/`) 调研
- [ ] WebUI 前端 (`webui/`) 调研
- [ ] Bridge 组件 (`bridge/`) 调研
- [ ] 测试体系 (`tests/`) 调研

### 1.3 现有文档梳理
- [ ] 整理现有文档清单
- [ ] 识别文档覆盖范围
- [ ] 标记文档缺失项
- [ ] 整理现有架构图和设计文档

---

## 第二阶段：文件夹中文 README 文档

### 2.1 根目录文件夹
- [ ] `.agent/` - 设计约束与安全边界中文 README
- [ ] `.github/` - GitHub CI/CD 配置中文 README
- [ ] `bridge/` - WhatsApp 桥接服务中文 README
- [ ] `case/` - 使用案例中文 README
- [ ] `docs/` - 文档目录中文 README
- [ ] `images/` - 图片资源中文 README
- [ ] `nanobot/` - 主包中文 README
- [ ] `tests/` - 测试目录中文 README
- [ ] `webui/` - WebUI 前端中文 README

### 2.2 nanobot 核心子目录
- [ ] `nanobot/agent/` - Agent 循环核心中文 README
- [ ] `nanobot/agent/tools/` - 工具注册与实现中文 README
- [ ] `nanobot/api/` - API 服务中文 README
- [ ] `nanobot/bus/` - 消息总线中文 README
- [ ] `nanobot/channels/` - 聊天通道中文 README
- [ ] `nanobot/cli/` - CLI 命令中文 README
- [ ] `nanobot/command/` - 命令路由中文 README
- [ ] `nanobot/config/` - 配置系统中文 README
- [ ] `nanobot/cron/` - 定时任务中文 README
- [ ] `nanobot/heartbeat/` - 心跳服务中文 README
- [ ] `nanobot/providers/` - LLM 提供商中文 README
- [ ] `nanobot/security/` - 安全模块中文 README
- [ ] `nanobot/session/` - 会话管理中文 README
- [ ] `nanobot/skills/` - 技能系统中文 README
- [ ] `nanobot/templates/` - 提示词模板中文 README
- [ ] `nanobot/utils/` - 工具函数中文 README
- [ ] `nanobot/web/` - Web 相关中文 README

### 2.3 WebUI 子目录
- [ ] `webui/src/` - 源代码目录中文 README
- [ ] `webui/src/components/` - UI 组件中文 README
- [ ] `webui/src/components/ui/` - UI 基础组件中文 README
- [ ] `webui/src/components/thread/` - 线程相关组件中文 README
- [ ] `webui/src/components/settings/` - 设置组件中文 README
- [ ] `webui/src/hooks/` - React Hooks 中文 README
- [ ] `webui/src/lib/` - 工具库中文 README
- [ ] `webui/src/i18n/` - 国际化中文 README
- [ ] `webui/src/tests/` - 测试文件中文 README
- [ ] `webui/src/workers/` - Web Workers 中文 README

### 2.4 测试子目录
- [ ] `tests/agent/` - Agent 测试中文 README
- [ ] `tests/agent/tools/` - 工具测试中文 README
- [ ] `tests/channels/` - 通道测试中文 README
- [ ] `tests/cli/` - CLI 测试中文 README
- [ ] `tests/command/` - 命令测试中文 README
- [ ] `tests/providers/` - 提供商测试中文 README
- [ ] `tests/utils/` - 工具测试中文 README

---

## 第三阶段：技术栈与架构梳理

### 3.1 核心技术栈
- [ ] Python 3.11+ 核心库梳理
- [ ] 异步编程 (asyncio) 使用模式
- [ ] Pydantic 配置与验证体系
- [ ] 日志系统 (loguru) 架构
- [ ] WebSocket 协议实现
- [ ] Jinja2 模板引擎使用

### 3.2 LLM 提供商生态
- [ ] Anthropic API 集成
- [ ] OpenAI API 兼容层
- [ ] 多提供商统一抽象
- [ ] 流式响应处理机制
- [ ] 思考模式 (reasoning) 支持
- [ ] 提示词缓存 (prompt caching) 机制

### 3.3 前端技术栈
- [ ] React + TypeScript 架构
- [ ] Vite 构建系统
- [ ] TailwindCSS 样式系统
- [ ] Radix UI 组件库
- [ ] i18next 国际化
- [ ] Vitest 测试框架

### 3.4 架构设计原理
- [ ] 消息总线解耦模式
- [ ] Agent 循环状态机设计
- [ ] 通道插件化架构
- [ ] 工具注册与发现机制
- [ ] 会话隔离与共享策略
- [ ] 内存合并 (Dream) 机制
- [ ] 自动压缩 (AutoCompact) 策略

---

## 第四阶段：图表绘制

### 4.1 架构图
- [ ] 项目整体架构图
- [ ] 核心模块依赖关系图
- [ ] 消息流转架构图
- [ ] Agent 循环状态机图
- [ ] 通道插件架构图
- [ ] 工具系统架构图
- [ ] 提供商抽象架构图
- [ ] 会话管理架构图
- [ ] Memory 系统架构图
- [ ] WebUI 网关架构图

### 4.2 流程图
- [ ] 消息接收到响应完整流程
- [ ] Agent 循环执行流程
- [ ] 工具调用与执行流程
- [ ] 会话上下文构建流程
- [ ] 内存合并 (Dream) 流程
- [ ] MCP 连接与调用流程
- [ ] 子 Agent 启动流程
- [ ] 定时任务调度流程

### 4.3 时序图
- [ ] 用户消息处理时序图
- [ ] 流式响应时序图
- [ ] 工具调用时序图
- [ ] 多通道并发时序图
- [ ] 子 Agent 调用时序图

### 4.4 数据结构图
- [ ] InboundMessage/OutboundMessage 结构
- [ ] Session 数据结构
- [ ] Tool Call 结构
- [ ] Configuration Schema 层次

---

## 第五阶段：代码文件中文注释

### 5.1 Agent 核心模块
- [ ] `nanobot/agent/__init__.py` - 注释补充
- [ ] `nanobot/agent/loop.py` - 注释补充 (已有部分注释)
- [ ] `nanobot/agent/runner.py` - 注释补充
- [ ] `nanobot/agent/context.py` - 注释补充
- [ ] `nanobot/agent/hook.py` - 注释补充
- [ ] `nanobot/agent/memory.py` - 注释补充
- [ ] `nanobot/agent/autocompact.py` - 注释补充
- [ ] `nanobot/agent/model_presets.py` - 注释补充
- [ ] `nanobot/agent/progress_hook.py` - 注释补充
- [ ] `nanobot/agent/skills.py` - 注释补充
- [ ] `nanobot/agent/subagent.py` - 注释补充

### 5.2 工具模块
- [ ] `nanobot/agent/tools/__init__.py` - 注释补充
- [ ] `nanobot/agent/tools/base.py` - 注释补充
- [ ] `nanobot/agent/tools/context.py` - 注释补充
- [ ] `nanobot/agent/tools/cron.py` - 注释补充
- [ ] `nanobot/agent/tools/file_state.py` - 注释补充
- [ ] `nanobot/agent/tools/filesystem.py` - 注释补充
- [ ] `nanobot/agent/tools/image_generation.py` - 注释补充
- [ ] `nanobot/agent/tools/loader.py` - 注释补充
- [ ] `nanobot/agent/tools/mcp.py` - 注释补充
- [ ] `nanobot/agent/tools/message.py` - 注释补充
- [ ] `nanobot/agent/tools/notebook.py` - 注释补充
- [ ] `nanobot/agent/tools/registry.py` - 注释补充
- [ ] `nanobot/agent/tools/runtime_state.py` - 注释补充
- [ ] `nanobot/agent/tools/sandbox.py` - 注释补充
- [ ] `nanobot/agent/tools/schema.py` - 注释补充
- [ ] `nanobot/agent/tools/search.py` - 注释补充
- [ ] `nanobot/agent/tools/self.py` - 注释补充
- [ ] `nanobot/agent/tools/shell.py` - 注释补充
- [ ] `nanobot/agent/tools/spawn.py` - 注释补充
- [ ] `nanobot/agent/tools/web.py` - 注释补充

### 5.3 消息总线模块
- [ ] `nanobot/bus/__init__.py` - 注释补充
- [ ] `nanobot/bus/events.py` - 注释补充
- [ ] `nanobot/bus/queue.py` - 注释补充 (已有中文注释)

### 5.4 通道模块
- [ ] `nanobot/channels/__init__.py` - 注释补充
- [ ] `nanobot/channels/base.py` - 注释补充 (已有部分中文注释)
- [ ] `nanobot/channels/manager.py` - 注释补充
- [ ] `nanobot/channels/registry.py` - 注释补充
- [ ] `nanobot/channels/discord.py` - 注释补充
- [ ] `nanobot/channels/feishu.py` - 注释补充
- [ ] `nanobot/channels/slack.py` - 注释补充
- [ ] `nanobot/channels/telegram.py` - 注释补充
- [ ] `nanobot/channels/websocket.py` - 注释补充
- [ ] `nanobot/channels/whatsapp.py` - 注释补充
- [ ] `nanobot/channels/qq.py` - 注释补充
- [ ] `nanobot/channels/wecom.py` - 注释补充
- [ ] `nanobot/channels/weixin.py` - 注释补充
- [ ] `nanobot/channels/matrix.py` - 注释补充
- [ ] `nanobot/channels/dingtalk.py` - 注释补充
- [ ] `nanobot/channels/email.py` - 注释补充
- [ ] `nanobot/channels/mochat.py` - 注释补充
- [ ] `nanobot/channels/msteams.py` - 注释补充

### 5.5 提供商模块
- [ ] `nanobot/providers/__init__.py` - 注释补充
- [ ] `nanobot/providers/base.py` - 注释补充
- [ ] `nanobot/providers/factory.py` - 注释补充
- [ ] `nanobot/providers/registry.py` - 注释补充
- [ ] `nanobot/providers/anthropic_provider.py` - 注释补充
- [ ] `nanobot/providers/openai_compat_provider.py` - 注释补充
- [ ] `nanobot/providers/azure_openai_provider.py` - 注释补充
- [ ] `nanobot/providers/bedrock_provider.py` - 注释补充
- [ ] `nanobot/providers/github_copilot_provider.py` - 注释补充
- [ ] `nanobot/providers/openai_codex_provider.py` - 注释补充
- [ ] `nanobot/providers/fallback_provider.py` - 注释补充
- [ ] `nanobot/providers/image_generation.py` - 注释补充
- [ ] `nanobot/providers/transcription.py` - 注释补充
- [ ] `nanobot/providers/openai_responses/` - 子目录注释补充

### 5.6 配置模块
- [ ] `nanobot/config/__init__.py` - 注释补充
- [ ] `nanobot/config/schema.py` - 注释补充
- [ ] `nanobot/config/loader.py` - 注释补充
- [ ] `nanobot/config/paths.py` - 注释补充

### 5.7 CLI 模块
- [ ] `nanobot/cli/__init__.py` - 注释补充
- [ ] `nanobot/cli/commands.py` - 注释补充
- [ ] `nanobot/cli/models.py` - 注释补充
- [ ] `nanobot/cli/onboard.py` - 注释补充
- [ ] `nanobot/cli/stream.py` - 注释补充

### 5.8 命令模块
- [ ] `nanobot/command/__init__.py` - 注释补充
- [ ] `nanobot/command/builtin.py` - 注释补充
- [ ] `nanobot/command/router.py` - 注释补充

### 5.9 会话与内存
- [ ] `nanobot/session/__init__.py` - 注释补充
- [ ] `nanobot/session/manager.py` - 注释补充

### 5.10 定时与心跳
- [ ] `nanobot/cron/__init__.py` - 注释补充
- [ ] `nanobot/cron/service.py` - 注释补充
- [ ] `nanobot/cron/types.py` - 注释补充
- [ ] `nanobot/heartbeat/__init__.py` - 注释补充
- [ ] `nanobot/heartbeat/service.py` - 注释补充

### 5.11 安全模块
- [ ] `nanobot/security/__init__.py` - 注释补充
- [ ] `nanobot/security/network.py` - 注释补充

### 5.12 工具函数
- [ ] `nanobot/utils/__init__.py` - 注释补充
- [ ] `nanobot/utils/artifacts.py` - 注释补充
- [ ] `nanobot/utils/document.py` - 注释补充
- [ ] `nanobot/utils/evaluator.py` - 注释补充
- [ ] `nanobot/utils/gitstore.py` - 注释补充
- [ ] `nanobot/utils/helpers.py` - 注释补充
- [ ] `nanobot/utils/image_generation_intent.py` - 注释补充
- [ ] `nanobot/utils/logging_bridge.py` - 注释补充
- [ ] `nanobot/utils/media_decode.py` - 注释补充
- [ ] `nanobot/utils/path.py` - 注释补充
- [ ] `nanobot/utils/progress_events.py` - 注释补充
- [ ] `nanobot/utils/prompt_templates.py` - 注释补充
- [ ] `nanobot/utils/restart.py` - 注释补充
- [ ] `nanobot/utils/runtime.py` - 注释补充
- [ ] `nanobot/utils/searchusage.py` - 注释补充
- [ ] `nanobot/utils/tool_hints.py` - 注释补充
- [ ] `nanobot/utils/webui_titles.py` - 注释补充

### 5.13 API 与 Web
- [ ] `nanobot/api/__init__.py` - 注释补充
- [ ] `nanobot/api/server.py` - 注释补充
- [ ] `nanobot/web/__init__.py` - 注释补充

### 5.14 技能与模板
- [ ] `nanobot/skills/` - 各技能 README 已有中文，补充代码注释
- [ ] `nanobot/templates/` - 各模板已有中文，补充代码注释
- [ ] `nanobot/skills/skill-creator/` - 技能创建工具注释

### 5.15 主入口
- [ ] `nanobot/__init__.py` - 注释补充
- [ ] `nanobot/__main__.py` - 注释补充
- [ ] `nanobot/nanobot.py` - 注释补充

### 5.16 WebUI 前端代码
- [ ] `webui/src/main.tsx` - 注释补充
- [ ] `webui/src/App.tsx` - 注释补充
- [ ] `webui/src/components/*.tsx` - 所有组件注释补充
- [ ] `webui/src/hooks/*.ts` - 所有 hooks 注释补充
- [ ] `webui/src/lib/*.ts` - 所有工具库注释补充
- [ ] `webui/src/i18n/*.ts` - 国际化注释补充

### 5.17 Bridge 组件
- [ ] `bridge/src/index.ts` - 注释补充
- [ ] `bridge/src/server.ts` - 注释补充
- [ ] `bridge/src/whatsapp.ts` - 注释补充

---

## 第六阶段：使用教程与部署指南

### 6.1 快速入门教程
- [ ] 编写完整的中文快速入门指南
- [ ] 环境准备步骤详解
- [ ] 安装步骤详解
- [ ] 配置文件详解
- [ ] 第一次运行指南

### 6.2 部署指南
- [ ] Docker 部署详细步骤
- [ ] Linux 系统服务部署
- [ ] macOS LaunchAgent 部署
- [ ] Windows 服务部署
- [ ] 多实例部署方案
- [ ] 生产环境配置建议

### 6.3 开发指南
- [ ] 本地开发环境搭建
- [ ] 调试技巧与方法
- [ ] 测试编写指南
- [ ] 代码贡献流程
- [ ] 常见问题解决方案

### 6.4 扩展开发
- [ ] 添加新通道指南
- [ ] 添加新提供商指南
- [ ] 添加新工具指南
- [ ] 开发自定义技能指南
- [ ] MCP 服务器开发指南

---

## 第七阶段：最佳实践与踩坑点

### 7.1 开发注意事项
- [ ] 异步编程最佳实践
- [ ] 错误处理模式
- [ ] 日志记录规范
- [ ] 代码风格指南
- [ ] 测试覆盖率要求

### 7.2 常见踩坑点
- [ ] Windows 兼容性问题
- [ ] 配置文件陷阱
- [ ] 会话管理注意事项
- [ ] 内存泄漏防范
- [ ] 并发处理注意事项
- [ ] 安全边界注意

### 7.3 性能优化建议
- [ ] 提示词缓存使用
- [ ] 会话压缩策略
- [ ] 并发控制优化
- [ ] 资源管理建议
- [ ] 网络请求优化

### 7.4 安全实践
- [ ] API 密钥管理
- [ ] 工作目录限制
- [ ] SSRF 防护
- [ ] 命令执行安全
- [ ] 文件访问控制

---

## 第八阶段：完整技术调研报告

### 8.1 报告结构规划
- [ ] 项目概述与背景
- [ ] 核心架构分析
- [ ] 技术栈详解
- [ ] 模块设计分析
- [ ] 数据流分析
- [ ] 扩展机制分析
- [ ] 部署与运维
- [ ] 开发指南
- [ ] 最佳实践
- [ ] 未来发展建议

### 8.2 报告内容编写
- [ ] 第一章：项目概述
- [ ] 第二章：架构设计
- [ ] 第三章：核心模块分析
- [ ] 第四章：通道与集成
- [ ] 第五章：LLM 提供商生态
- [ ] 第六章：前端系统分析
- [ ] 第七章：数据与状态管理
- [ ] 第八章：扩展与定制
- [ ] 第九章：部署与运维
- [ ] 第十章：最佳实践

### 8.3 报告图表整理
- [ ] 整理所有架构图
- [ ] 整理所有流程图
- [ ] 整理所有时序图
- [ ] 整理所有数据结构图
- [ ] 图表交叉引用索引

---

## 第九阶段：资料整合与输出

### 9.1 文档组织
- [ ] 创建完整的文档索引
- [ ] 建立文档交叉引用
- [ ] 整理代码注释索引
- [ ] 建立图表索引

### 9.2 输出格式
- [ ] Markdown 格式完整报告
- [ ] PDF 格式完整报告（可选）
- [ ] 代码注释版本
- [ ] 独立的图表资源包

### 9.3 质量检查
- [ ] 文档完整性检查
- [ ] 代码注释质量检查
- [ ] 图表准确性检查
- [ ] 交叉引用检查

---

## 执行说明

### 执行顺序
1. 先完成第一阶段调研，建立对项目的整体认识
2. 同时进行第二阶段文档编写和第三阶段架构梳理
3. 第四阶段图表绘制需要基于第三阶段的成果
4. 第五阶段代码注释可以并行进行，按模块分配
5. 第六、七阶段可以在文档完成后进行
6. 最后完成第八、九阶段报告整合

### 注意事项
- 代码注释仅增加中文说明，不修改任何业务逻辑
- 新建的 README 文件使用 `README_zh.md` 命名，避免与现有文档冲突
- 图表建议使用 Mermaid 语法，便于 Markdown 渲染
- 技术调研报告采用 `技术调研报告.md` 命名

### 工具推荐
- 图表绘制：Mermaid、PlantUML、Draw.io
- 文档编辑：Typora、VS Code
- 代码注释：IDE 的批量注释功能

---

## 进度跟踪

- 开始时间：2026-05-15
- 预计完成时间： TBD
- 当前状态：Issues 已创建 (2026-05-15)

### Issues 创建记录
- 总览 Issue: #37
- 子 Issues: #15-#36

---

> 本清单将随工作进展持续更新，确保所有任务清晰可见、可追踪。
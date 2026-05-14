# 图片资源

本目录包含 nanobot 项目使用的图片资源。

## 目录结构

```
images/
├── GitHub_README.png    # GitHub README 横幅
├── nanobot_arch.png     # nanobot 架构图
├── nanobot_logo.png     # nanobot Logo
└── nanobot_webui.png    # WebUI 截图
```

## 图片说明

### GitHub_README.png
用于 GitHub 仓库主页的横幅图片，展示 nanobot 的品牌形象。

### nanobot_arch.png
nanobot 的架构图，展示核心组件和数据流：

- **消息总线** - 连接通道和 agent
- **Agent Loop** - 核心处理引擎
- **LLM 提供商** - 支持多个 LLM
- **通道** - 连接各种聊天平台
- **工具** - agent 的能力
- **记忆** - 会话历史管理

### nanobot_logo.png
nanobot 的官方 Logo，用于品牌展示。

**用途**：
- 文档头部
- WebUI 顶部导航
- 社交媒体
- 宣传材料

### nanobot_webui.png
WebUI 的截图，展示用户界面：

- 会话列表
- 聊天界面
- 消息气泡
- 工具调用显示
- 设置面板

## 图片格式

所有图片使用 PNG 格式，确保：

- 跨平台兼容性
- 透明背景支持
- 高质量显示

## 使用指南

### 在 Markdown 中使用

```markdown
![nanobot Logo](../images/nanobot_logo.png)

![nanobot 架构](../images/nanobot_arch.png)
```

### 在 HTML 中使用

```html
<img src="/images/nanobot_logo.png" alt="nanobot Logo" />
```

### 在 WebUI 中使用

```tsx
<img
  src="/brand/nanobot_logo.png"
  alt="nanobot"
  className="h-6 w-auto"
/>
```

## 图片优化

为了保持良好的加载速度：

- 控制图片文件大小
- 使用适当的分辨率
- 考虑使用 WebP 格式（在某些情况下）

## 添加新图片

1. 使用 PNG 格式
2. 保持合理的文件大小
3. 使用描述性的文件名
4. 更新本 README 文件
5. 考虑添加到相应文档中

## 注意事项

1. **版权** - 确保所有图片都有适当的授权
2. **大小** - 保持文件大小合理，避免过大的图片
3. **质量** - 确保图片质量足够清晰
4. **一致性** - 保持视觉风格的一致性
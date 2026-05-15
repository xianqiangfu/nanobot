# UI 基础组件

本目录包含从 [shadcn/ui](https://ui.shadcn.com/) 导入的基础 UI 组件。

## 组件列表

- **alert-dialog.tsx** - 警告对话框，用于需要用户确认的危险操作
- **avatar.tsx** - 用户头像显示组件
- **button.tsx** - 按钮组件，支持多种变体和尺寸
- **dialog.tsx** - 模态对话框组件
- **dropdown-menu.tsx** - 下拉菜单组件
- **input.tsx** - 文本输入框组件
- **scroll-area.tsx** - 可滚动区域组件
- **separator.tsx** - 分隔线组件
- **sheet.tsx** - 侧边抽屉组件
- **textarea.tsx** - 多行文本输入组件
- **tooltip.tsx** - 工具提示组件

## 组件特性

### Button

支持多种样式：
- `default` - 默认样式
- `destructive` - 危险操作样式
- `outline` - 轮廓样式
- `secondary` - 次要样式
- `ghost` - 幽灵样式
- `link` - 链接样式

支持多种尺寸：
- `default` - 默认尺寸
- `sm` - 小尺寸
- `lg` - 大尺寸
- `icon` - 图标尺寸

## 注意事项

- 所有组件都使用 Tailwind CSS 样式
- 组件支持深色模式
- 使用 Radix UI 作为底层组件库

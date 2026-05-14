# 国际化 (i18n)

本目录包含 WebUI 的国际化配置和翻译文件。

## 目录结构

```
i18n/
├── index.ts                    # i18next 配置和初始化
├── config.ts                   # 区域设置配置
└── locales/                    # 翻译文件
    ├── en/common.json          # 英语（默认）
    ├── zh-CN/common.json       # 简体中文
    ├── zh-TW/common.json       # 繁体中文
    ├── fr/common.json          # 法语
    ├── ja/common.json          # 日语
    ├── ko/common.json          # 韩语
    ├── es/common.json          # 西班牙语
    ├── vi/common.json          # 越南语
    └── id/common.json          # 印尼语
```

## 支持的语言

| 语言代码 | 语言名称 | 区域 |
|---------|---------|------|
| `en` | 英语 | 默认 |
| `zh-CN` | 简体中文 | 中国大陆 |
| `zh-TW` | 繁体中文 | 台湾 |
| `fr` | 法语 | 法国 |
| `ja` | 日语 | 日本 |
| `ko` | 韩语 | 韩国 |
| `es` | 西班牙语 | 西班牙 |
| `vi` | 越南语 | 越南 |
| `id` | 印尼语 | 印度尼西亚 |

## 配置 (config.ts)

### 主要设置

```typescript
export const defaultLocale = 'en';
export const fallbackLocale = 'en';
export const LOCALE_STORAGE_KEY = 'nanobot:locale';
```

### 工具函数

- `normalizeLocale(locale)` - 规范化区域设置代码
- `resolveInitialLocale()` - 解析初始区域设置
- `persistLocale(locale)` - 保存区域设置到本地存储
- `applyDocumentLocale(locale)` - 应用区域设置到文档

## 使用方法

### 在组件中使用翻译

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();

  return <h1>{t('sidebar.newChat')}</h1>;
}
```

### 切换语言

```typescript
import { setAppLanguage } from '@/i18n';

// 切换到简体中文
await setAppLanguage('zh-CN');
```

### 获取当前语言

```typescript
import { currentLocale } from '@/i18n';

const locale = currentLocale(); // 'zh-CN'
```

## 翻译文件结构

翻译文件使用 JSON 格式，按功能模块组织：

```json
{
  "sidebar": {
    "newChat": "新建对话",
    "searchPlaceholder": "搜索...",
    "settings": "设置"
  },
  "chat": {
    "noSessions": "没有会话",
    "sendMessage": "发送消息"
  }
}
```

## 添加新语言

1. 在 `locales/` 目录创建新的翻译文件
2. 在 `index.ts` 中导入并添加到 `resources` 对象
3. 在 `config.ts` 中添加到支持的语言列表

## 注意事项

- 所有翻译键使用点号分隔的命名空间
- 回退语言是英语
- 区域设置保存在 `localStorage` 中
- 应用启动时自动加载保存的区域设置
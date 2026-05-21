# Internationalization (i18n)

This directory contains the WebUI's internationalization configuration and translation files.

## Directory Structure

```
i18n/
├── index.ts                    # i18next configuration and initialization
├── config.ts                   # Locale configuration
└── locales/                    # Translation files
    ├── en/common.json          # English (default)
    ├── zh-CN/common.json       # Simplified Chinese
    ├── zh-TW/common.json       # Traditional Chinese
    ├── fr/common.json          # French
    ├── ja/common.json          # Japanese
    ├── ko/common.json          # Korean
    ├── es/common.json          # Spanish
    ├── vi/common.json          # Vietnamese
    └── id/common.json          # Indonesian
```

## Supported Languages

| Language Code | Language Name | Region |
|--------------|---------------|--------|
| `en` | English | Default |
| `zh-CN` | Chinese (Simplified) | Mainland China |
| `zh-TW` | Chinese (Traditional) | Taiwan |
| `fr` | French | France |
| `ja` | Japanese | Japan |
| `ko` | Korean | Korea |
| `es` | Spanish | Spain |
| `vi` | Vietnamese | Vietnam |
| `id` | Indonesian | Indonesia |

## Configuration (config.ts)

### Main Settings

```typescript
export const defaultLocale = 'en';
export const fallbackLocale = 'en';
export const LOCALE_STORAGE_KEY = 'nanobot.locale';
```

### Utility Functions

- `normalizeLocale(locale)` - Normalize locale codes
- `resolveInitialLocale()` - Resolve initial locale
- `persistLocale(locale)` - Save locale to localStorage
- `applyDocumentLocale(locale)` - Apply locale to document

## Usage

### Using Translations in Components

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();

  return <h1>{t('sidebar.newChat')}</h1>;
}
```

### Switching Languages

```typescript
import { setAppLanguage } from '@/i18n';

// Switch to Simplified Chinese
await setAppLanguage('zh-CN');
```

### Getting Current Language

```typescript
import { currentLocale } from '@/i18n';

const locale = currentLocale(); // 'zh-CN'
```

## Translation File Structure

Translation files use JSON format, organized by functional modules:

```json
{
  "sidebar": {
    "newChat": "New Chat",
    "searchPlaceholder": "Search...",
    "settings": "Settings"
  },
  "chat": {
    "noSessions": "No sessions",
    "sendMessage": "Send Message"
  }
}
```

## Adding a New Language

1. Create a new translation file in the `locales/` directory
2. Import and add to the `resources` object in `index.ts`
3. Add to the supported languages list in `config.ts`

## Notes

- All translation keys use dot-separated namespaces
- Fallback language is English
- Locale is saved in `localStorage`
- Saved locale is automatically loaded when the app starts
# Components Documentation

This directory contains all React components for the WebUI.

## Directory Structure

```
components/
├── ChatList.tsx          # Session list component
├── ChatPane.tsx          # Chat panel main component
├── CodeBlock.tsx         # Code block rendering component
├── Composer.tsx          # Message editor component
├── ConnectionBadge.tsx   # Connection status indicator
├── DeleteConfirm.tsx     # Delete confirmation dialog
├── EmptyState.tsx        # Empty state prompt
├── ImageLightbox.tsx     # Image viewer
├── LanguageSwitcher.tsx  # Language switcher
├── MarkdownText.tsx      # Markdown text rendering
├── MarkdownTextRenderer.tsx  # Markdown renderer
├── MessageBubble.tsx     # Message bubble component
├── MessageList.tsx       # Message list component
├── Sidebar.tsx           # Sidebar navigation
├── settings/
│   └── SettingsView.tsx  # Settings view
├── thread/
│   ├── StreamErrorNotice.tsx   # Stream error prompt
│   ├── ThreadComposer.tsx      # Thread editor
│   ├── ThreadHeader.tsx        # Thread header
│   ├── ThreadMessages.tsx      # Thread messages
│   ├── ThreadShell.tsx         # Thread container
│   └── ThreadViewport.tsx      # Thread viewport
└── ui/                     # shadcn/ui base components
    ├── alert-dialog.tsx
    ├── avatar.tsx
    ├── button.tsx
    ├── dialog.tsx
    ├── dropdown-menu.tsx
    ├── input.tsx
    ├── scroll-area.tsx
    ├── separator.tsx
    ├── sheet.tsx
    ├── textarea.tsx
    └── tooltip.tsx
```

## Core Components

### ChatPane
Main container for the chat panel, managing message list, input area, and thread view.

### Sidebar
Sidebar navigation, containing session list, search, and settings entry.

### MessageBubble
Bubble component for individual messages, supporting different styles for user and assistant messages.

### Composer
Message editor, supporting text input, image upload, and sending.

### ThreadShell
Root container for threads, managing thread lifecycle and layout.

## UI Components

The `ui/` directory contains basic UI components imported from [shadcn/ui](https://ui.shadcn.com/):

- **Button** - Button component, supporting multiple variants
- **Dialog** - Dialog component
- **Input** - Input field component
- **Textarea** - Multi-line text input component
- **ScrollArea** - Scrollable area component
- **Tooltip** - Tooltip component
- **Avatar** - Avatar component
- **Sheet** - Side drawer component
- **DropdownMenu** - Dropdown menu component
- **AlertDialog** - Alert dialog component
- **Separator** - Separator component

## Component Features

- **Internationalization support**: All components support multiple languages via `react-i18next`
- **Responsive design**: Using Tailwind CSS for responsive layouts
- **Dark mode**: Supporting dark and light theme switching
- **Accessibility**: Following ARIA standards, supporting keyboard navigation
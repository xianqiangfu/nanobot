# React Hooks

This directory contains custom React Hooks for the WebUI.

## Directory Structure

```
hooks/
├── useAttachedImages.ts    # Image attachment management
├── useClipboardAndDrop.ts  # Clipboard and drag-and-drop handling
├── useNanobotStream.ts     # nanobot streaming message processing
├── useSessions.ts          # Session management
└── useTheme.ts             # Theme management
```

## Hook Descriptions

### useAttachedImages
Manages image attachments in the message editor.

**Features**:
- Add and remove images
- Convert images to base64 format
- Generate preview URLs

### useClipboardAndDrop
Handles clipboard paste and file drag-and-drop.

**Features**:
- Listen to clipboard paste events
- Process file drag-and-drop
- Extract image content

### useNanobotStream
Handles WebSocket streaming communication with the nanobot gateway.

**Features**:
- Subscribe to chat sessions
- Process streaming message deltas
- Manage message states (streaming/completed)
- Handle tool calls and reasoning content
- Error handling and retry

**Key Features**:
- Intelligently merge message deltas to reduce rendering
- Support reasoning content streaming
- Placeholder management for tool calls and reasoning phases
- Automatic cleanup of temporary placeholders

### useSessions
Manages session list and session switching.

**Features**:
- Load session list
- Create new sessions
- Delete sessions
- Switch current session
- Session search and filtering

### useTheme
Manages application theme (dark/light mode).

**Features**:
- Toggle theme
- Persist theme settings
- Respond to system theme changes

## Usage Examples

### useNanobotStream

```typescript
const {
  messages,
  isStreaming,
  send,
  stop,
  streamError,
  dismissStreamError
} = useNanobotStream(
  chatId,
  initialMessages,
  hasPendingToolCalls,
  onTurnEnd
);

// Send message
send("Hello", images);

// Stop generation
stop();
```

### useSessions

```typescript
const {
  sessions,
  activeKey,
  loading,
  createNew,
  select,
  delete: deleteSession
} = useSessions();

// Create new session
createNew();
```

### useTheme

```typescript
const { theme, toggleTheme } = useTheme();

// Toggle theme
toggleTheme();
```
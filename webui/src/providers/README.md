# Context Providers

This directory contains React Context Providers for global state management.

## Directory Structure

```
providers/
└── ClientProvider.tsx    # nanobot client Provider
```

## Provider Documentation

### ClientProvider
Provides the nanobot client and configuration to the entire application tree.

**Provided values**:
- `client: NanobotClient` - WebSocket client instance
- `token: string` - Authentication token
- `modelName: string | null` - Current model name

**Usage example**:

```typescript
import { useClient } from '@/providers/ClientProvider';

function MyComponent() {
  const { client, token, modelName } = useClient();
  // Use client to send messages
}
```

## Design Patterns

### Provider Pattern
Uses React Context API to implement global state sharing:

1. **Create Context**: Define the shape and default values of data
2. **Provide Context**: Use Provider component at the top level of the application
3. **Consume Context**: Get data through the `useClient` hook

### Advantages
- **Avoid prop drilling**: No need to pass props layer by layer
- **Centralized management**: Client and configuration are managed centrally
- **Type safety**: TypeScript provides complete type checking
- **Easy to test**: Can easily create mock providers

## Future Extensions

As the application grows, more Providers may need to be added:

- `ThemeProvider` - Theme management
- `I18nProvider` - Internationalization configuration
- `NotificationProvider` - Notification system
- `ModalProvider` - Modal management
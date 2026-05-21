# API Service

This module provides an OpenAI-compatible HTTP API server for persistent nanobot sessions.

## Core Features

### Endpoints

- `POST /v1/chat/completions` - OpenAI-compatible chat completions endpoint
- `GET /v1/models` - List available models

### Session Management

All requests route to a single persistent API session:

- Session key: `api:default`
- Chat ID: `default`

## Usage Examples

### Chat Completions

```bash
curl -X POST http://localhost:8765/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### List Models

```bash
curl http://localhost:8765/api/v1/models
```

### File Upload

```bash
curl -X POST http://localhost:8765/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "What is this image?"},
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,/9j/4AAQ..."
            }
          }
        ]
      }
    ]
  }'
```

## Configuration

### Port

The API service runs on port 8765 by default.

### Session Configuration

API sessions use the same settings as nanobot configuration:
- Provider configuration
- Tool configuration
- Agent configuration

## Response Format

### Success Response

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1715691600,
  "model": "claude-3-5-sonnet-20241022",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### Error Response

```json
{
  "error": {
    "message": "Invalid request",
    "type": "invalid_request_error",
    "code": 400
  }
}
```

## Notes

- All requests are processed asynchronously
- Streaming responses are supported
- File size limit: MAX_FILE_SIZE
- Files are stored in the media directory
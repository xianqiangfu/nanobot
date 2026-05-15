# 多通道并发时序图

```mermaid
sequenceDiagram
    participant U1 as 用户 1 (Telegram)
    participant U2 as 用户 2 (Discord)
    participant U3 as 用户 3 (Slack)
    participant T as TelegramChannel
    participant D as DiscordChannel
    participant S as SlackChannel
    participant MB as MessageBus
    participant AL as AgentLoop

    Note over U1,T,MB: 用户 1 发送消息
    par 并发处理
        U1->>T: 发送消息 A
        T->>MB: publish_inbound(InboundMessage A)
        MB->>AL: consume_inbound() - 处理消息 A

    and Note over U2,D,MB: 用户 2 发送消息
        U2->>D: 发送消息 B
        D->>MB: publish_inbound(InboundMessage B)
        MB->>AL: consume_inbound() - 处理消息 B

    and Note over U3,S,MB: 用户 3 发送消息
        U3->>S: 发送消息 C
        S->>MB: publish_inbound(InboundMessage C)
        MB->>AL: consume_inbound() - 处理消息 C
    end

    Note over AL: 并发处理多个消息
    AL->>AL: 处理消息 A (会话 1)
    AL->>AL: 处理消息 B (会话 2)
    AL->>AL: 处理消息 C (会话 3)

    Note over AL,MB: 发布响应
    par 并发发布
        AL->>MB: publish_outbound(OutboundMessage A)
    and AL->>MB: publish_outbound(OutboundMessage B)
    and AL->>MB: publish_outbound(OutboundMessage C)
    end

    Note over MB,通道: 路由响应
    MB->>T: consume_outbound() - 响应 A
    MB->>D: consume_outbound() - 响应 B
    MB->>S: consume_outbound() - 响应 C

    Note over 通道,用户: 发送响应
    par 并发发送
        T->>U1: 发送响应 A
    and D->>U2: 发送响应 B
    and S->>U3: 发送响应 C
    end
```
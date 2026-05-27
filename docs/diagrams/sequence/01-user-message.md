# 用户消息处理时序图

```mermaid
sequenceDiagram
    participant User as 用户
    participant Channel as 聊天通道
    participant Bus as 消息总线
    participant Loop as AgentLoop
    participant Runner as AgentRunner
    participant LLM as LLM提供商
    participant Session as 会话管理

    User->>Channel: 发送消息
    Channel->>Channel: 解析消息
    Channel->>Bus: 发布 InboundMessage 事件
    Bus->>Loop: 消费消息事件

    Loop->>Session: 获取会话上下文
    Session-->>Loop: 返回历史消息
    Loop->>Loop: 构建完整上下文

    Loop->>Runner: 启动 AgentRunner
    Runner->>LLM: 发送上下文请求
    LLM-->>Runner: 返回响应（可能包含工具调用）

    alt 响应包含工具调用
        Runner->>Runner: 执行工具
        Runner->>Loop: 发送工具结果
        Loop->>Session: 更新会话历史
        Runner->>LLM: 继续对话
        LLM-->>Runner: 返回最终响应
    end

    Runner-->>Loop: 返回处理结果
    Loop->>Bus: 发布 OutboundMessage 事件
    Bus->>Channel: 消费响应事件
    Channel->>User: 发送响应

    Loop->>Session: 保存会话状态
```
# 流式响应时序图

```mermaid
sequenceDiagram
    participant User as 用户
    participant Channel as 聊天通道
    participant Bus as 消息总线
    participant Loop as AgentLoop
    participant Runner as AgentRunner
    participant LLM as LLM提供商
    participant Stream as 流式处理器

    User->>Channel: 发送消息
    Channel->>Bus: 发布 InboundMessage
    Bus->>Loop: 消费消息
    Loop->>Runner: 启动流式对话

    Runner->>LLM: 发送流式请求<br/>(stream: true)
    activate LLM
    LLM-->>Runner: 返回流式迭代器

    loop 流式数据传输
        LLM-->>Stream: 发送数据块
        Stream->>Runner: 处理数据块
        Runner->>Runner: 解析内容/工具调用

        alt 收集到完整内容
            Runner->>Bus: 发布流式 OutboundMessage
            Bus->>Channel: 消费事件
            Channel->>User: 实时显示内容
        end
    end
    deactivate LLM

    Runner-->>Loop: 流式处理完成
    Loop->>Bus: 发布完成事件
    Bus->>Channel: 通知完成
```
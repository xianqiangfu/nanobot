# Agent 循环执行流程

```mermaid
flowchart TD
    Start([收到入站消息]) --> InitTurn[初始化轮次]
    InitTurn --> CreateContext[创建 TurnContext]
    CreateContext --> RestoreState[状态: RESTORE]

    RestoreState --> GetSession[获取会话]
    GetSession --> CompactCheck{需要压缩?}
    CompactCheck -->|是| Compact[状态: COMPACT]
    CompactCheck -->|否| CommandState
    Compact --> CommandState

    CommandState[状态: COMMAND] --> IsCommand{是命令?}
    IsCommand -->|是| HandleCommand[处理命令]
    IsCommand -->|否| BuildState

    HandleCommand --> CheckStop{停止命令?}
    CheckStop -->|是| StopLoop[停止当前轮次]
    CheckStop -->|否| ExecuteCommand[执行命令]
    ExecuteCommand --> CommandDone[命令完成]
    CommandDone --> SaveState

    BuildState[状态: BUILD] --> BuildContext1[构建上下文]
    BuildContext1 --> RunState

    RunState[状态: RUN] --> AgentRunner[AgentRunner]
    AgentRunner --> Provider[LLM 提供商]

    Provider --> StreamCheck[流式响应?]
    StreamCheck -->|是| StreamLoop[流式处理循环]
    StreamCheck -->|否| SingleCall[单次调用]

    StreamLoop --> StreamDelta[处理增量]
    StreamDelta --> HasMore{更多内容?}
    HasMore -->|是| StreamDelta
    HasMore -->|否| StreamDone[流式完成]
    StreamDone --> SaveState

    SingleCall --> ResponseCheck[检查响应]
    ResponseCheck --> ToolCheck{有工具调用?}

    ToolCheck -->|是| ExecuteTool[执行工具]
    ExecuteTool --> ToolNext{需要下一轮?}
    ToolNext -->|是| Provider
    ToolNext -->|否| SaveState

    ToolCheck -->|否| SaveState

    SaveState[状态: SAVE] --> UpdateSession[更新会话]
    UpdateSession --> Persist[持久化存储]
    Persist --> RespondState

    RespondState[状态: RESPOND] --> Publish[发布出站消息]
    Publish --> DoneState

    DoneState[状态: DONE] --> Cleanup[清理资源]
    Cleanup --> End([轮次结束])

    StopLoop --> End

    style Start fill:#e1f5ff
    style End fill:#ffe1f5
    style AgentLoop fill:#fff4e1
    style AgentRunner fill:#fff4e1
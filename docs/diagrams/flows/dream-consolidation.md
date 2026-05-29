# Dream 记忆合并流程

```mermaid
flowchart TD
    Start([触发 Dream]) --> CheckTimer{定时触发?}
    CheckTimer -->|是| GetSchedule[获取调度配置]
    CheckTimer -->|否| ManualTrigger[手动触发]
    GetSchedule --> LoadSessions[加载会话列表]

    ManualTrigger --> LoadSessions
    LoadSessions --> FilterSessions[过滤会话]
    FilterSessions --> CheckBatch{达到批量大小?}

    CheckBatch -->|否| Wait[等待下一批]
    Wait --> CheckTimer

    CheckBatch -->|是| ProcessBatch[处理批量会话]

    ProcessBatch --> ReadMemory[读取 MEMORY.md]
    ReadMemory --> CheckEmpty{MEMORY.md 空?}
    CheckEmpty -->|是| InitializeMemory[初始化 MEMORY.md]
    CheckEmpty -->|否| Phase1

    InitializeMemory --> Phase1

    Phase1[阶段 1: 模式识别] --> BuildPrompt1[构建识别提示词]
    BuildPrompt1 --> IncludeMemory[包含当前 MEMORY.md]
    IncludeMemory --> AnnotateAge{注释 git-blame 年龄?}
    AnnotateAge -->|是| AddAnnotations[添加年龄注释]
    AnnotateAge -->|否| CallLLM1

    AddAnnotations --> CallLLM1
    CallLLM1[调用 LLM] --> LLMResponse1[LLM 响应]
    LLMResponse1 --> ParsePatterns[解析重复模式]

    ParsePatterns --> CheckPatterns{发现模式?}
    CheckPatterns -->|是| Phase2[阶段 2: 知识蒸馏]
    CheckPatterns -->|否| SaveMemory1[保存当前内容]
    SaveMemory1 --> End([完成])

    Phase2 --> BuildPrompt2[构建蒸馏提示词]
    BuildPrompt2 --> IncludePatterns[包含识别的模式]
    IncludePatterns --> CallLLM2[调用 LLM]

    CallLLM2 --> LLMResponse2[LLM 响应]
    LLMResponse2 --> ParseSummary[解析摘要]
    ParseSummary --> FormatSummary[格式化摘要]

    FormatSummary --> BackupMemory[备份原内容]
    BackupMemory --> WriteMemory[写入 MEMORY.md]
    WriteMemory --> ValidateWrite[验证写入]

    ValidateWrite --> WriteOK{写入成功?}
    WriteOK -->|是| UpdateSessions[更新会话状态]
    WriteOK -->|否| Rollback[回滚]
    Rollback --> SaveMemory1

    UpdateSessions --> UpdateConsolidated[更新 consolidated 标记]
    UpdateConsolidated --> End

    style Start fill:#e1f5ff
    style End fill:#ffe1f5
    style Phase1 fill:#bbf,stroke:#333,stroke-width:2px
    style Phase2 fill:#bbf,stroke:#333,stroke-width:2px
    style Dream fill:#f9f,stroke:#333,stroke-width:4px
"
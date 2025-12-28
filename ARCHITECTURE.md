# Pathway-Hack Architecture Documentation

This document contains Mermaid diagrams to visualize the architecture, data flow, and components of the Pathway-Hack system.

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Data Flow Diagram](#data-flow-diagram)
3. [Agent Workflow (LangGraph)](#agent-workflow-langgraph)
4. [Backend Component Structure](#backend-component-structure)
5. [Frontend Component Structure](#frontend-component-structure)
6. [Pathway Engine Pipeline](#pathway-engine-pipeline)
7. [API Interaction Flow](#api-interaction-flow)

---

## System Architecture Overview

High-level architecture showing the main components and their relationships.

```mermaid
graph TB
    subgraph Frontend["Frontend (React + TypeScript)"]
        UI[React UI Components]
        Pages[Pages: Dashboard, AskTheAgent, etc.]
        Router[React Router]
    end
    
    subgraph Backend["Backend (Python + FastAPI)"]
        API[FastAPI Server :8003]
        Agent[DevAgent - LangGraph]
        
        subgraph PathwayEngine["Pathway Engine"]
            VectorServer[Vector Store Server :8765]
            Ingestion[Data Ingestion]
            Indexing[Live Indexing]
            Query[Query & Retrieval]
        end
        
        LLM[Gemini LLM Client]
    end
    
    subgraph DataSources["Data Sources"]
        Local[Local Folder Watch]
        GitHub[GitHub Webhook :8000]
    end
    
    User[User] -->|HTTP| UI
    UI -->|API Calls| API
    API -->|Query| Agent
    Agent -->|Retrieve Context| VectorServer
    Agent -->|Generate Response| LLM
    
    Local -->|File Changes| Ingestion
    GitHub -->|Webhook Events| Ingestion
    Ingestion -->|Stream| Indexing
    Indexing -->|Index| VectorServer
    VectorServer -->|Results| Query
    
    style Frontend fill:#e1f5ff
    style Backend fill:#fff4e1
    style PathwayEngine fill:#f0f0f0
    style DataSources fill:#e8f5e8
```

---

## Data Flow Diagram

Shows how data flows through the system from ingestion to user response.

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant FastAPI
    participant Agent
    participant PathwayEngine
    participant Gemini
    participant DataSources
    
    Note over DataSources,PathwayEngine: Continuous Background Process
    DataSources->>PathwayEngine: File changes / GitHub events
    PathwayEngine->>PathwayEngine: Incremental indexing
    PathwayEngine->>PathwayEngine: Generate embeddings
    
    Note over User,Gemini: User Query Flow
    User->>Frontend: Ask question
    Frontend->>FastAPI: POST /v1/agent/ask
    FastAPI->>Agent: answer_question(query)
    
    Note over Agent: LangGraph Workflow
    Agent->>PathwayEngine: Retrieve relevant context
    PathwayEngine-->>Agent: Return documents
    Agent->>Agent: Plan strategy
    Agent->>Agent: Use tools (optional)
    Agent->>Gemini: Generate response
    Gemini-->>Agent: LLM response
    Agent->>Agent: Assess confidence
    Agent->>Agent: Format output
    
    Agent-->>FastAPI: Structured result
    FastAPI-->>Frontend: JSON response
    Frontend-->>User: Display answer
```

---

## Agent Workflow (LangGraph)

The DevAgent uses LangGraph to orchestrate a multi-step reasoning process.

```mermaid
graph TD
    Start([User Query]) --> Observe[🔍 Observe Node]
    Observe -->|Retrieve & Build Context| Plan[🧠 Plan Node]
    
    Plan -->|Analyze Query| Route{Tools Needed?}
    
    Route -->|Yes| Tools[🛠️ Use Tools Node]
    Route -->|No| Generate[💬 Generate Node]
    
    Tools -->|Tool Results| Generate
    
    Generate -->|Create Response| Assess[📊 Assess Confidence Node]
    Assess -->|Calculate Score| Format[✨ Format Output Node]
    Format --> End([Return Result])
    
    style Observe fill:#e3f2fd
    style Plan fill:#fff3e0
    style Tools fill:#f3e5f5
    style Generate fill:#e8f5e9
    style Assess fill:#fce4ec
    style Format fill:#f1f8e9
    style Route fill:#ffecb3
```

### Agent Strategies

```mermaid
graph LR
    Query[User Query] --> Classify{Query Type}
    
    Classify -->|Simple Factual| Direct[Direct Answer Strategy]
    Classify -->|Complex/Multi-part| Summarize[Summarize Strategy]
    Classify -->|Ambiguous/Unclear| Uncertain[Uncertain Strategy]
    Classify -->|File Comparison| Compare[Compare Strategy]
    
    Direct --> Tools1[Tools: None]
    Summarize --> Tools2[Tools: llm_summarize, extract_key_points]
    Uncertain --> Tools3[Tools: express_uncertainty]
    Compare --> Tools4[Tools: compare_versions]
    
    Tools1 --> Generate[Generate Response]
    Tools2 --> Generate
    Tools3 --> Generate
    Tools4 --> Generate
    
    style Classify fill:#ffecb3
    style Direct fill:#c8e6c9
    style Summarize fill:#b3e5fc
    style Uncertain fill:#ffccbc
    style Compare fill:#d1c4e9
```

---

## Backend Component Structure

Detailed view of backend module organization.

```mermaid
graph TB
    subgraph Backend["Backend Structure"]
        Main[main.py - FastAPI App]
        
        subgraph Agent["agent/"]
            AgentPy[agent.py - DevAgent]
            Planner[planner.py - Strategy Planning]
            Tools[tools.py - Agent Tools]
            Confidence[confidence.py - Confidence Assessment]
        end
        
        subgraph PathwayEngine["pathway_engine/"]
            EngineMain[main.py - Pathway Runtime]
            
            subgraph Ingestion["ingestion/"]
                LocalSource[local_source.py]
                GitHubSource[github_source.py]
                Loader[loader.py]
            end
            
            subgraph Indexing["indexing/"]
                LiveIndex[live_index.py]
                Embeddings[embeddings.py]
            end
            
            subgraph QueryModule["query/"]
                Retriever[retriever.py]
                ContextBuilder[context_builder.py]
            end
            
            subgraph State["state/"]
                VersionTracker[version_tracker.py]
            end
        end
        
        subgraph LLM["llm/"]
            GeminiClient[gemini_client.py]
        end
    end
    
    Main --> AgentPy
    AgentPy --> Planner
    AgentPy --> Tools
    AgentPy --> Confidence
    AgentPy --> Retriever
    AgentPy --> ContextBuilder
    AgentPy --> GeminiClient
    
    EngineMain --> LocalSource
    EngineMain --> GitHubSource
    EngineMain --> Loader
    EngineMain --> LiveIndex
    EngineMain --> Embeddings
    
    Retriever --> EngineMain
    
    style Main fill:#ff9800
    style Agent fill:#e1f5ff
    style PathwayEngine fill:#fff4e1
    style LLM fill:#f3e5f5
```

---

## Frontend Component Structure

React application structure with routing and components.

```mermaid
graph TB
    subgraph Frontend["Frontend Structure"]
        MainTsx[main.tsx - Entry Point]
        AppTsx[App.tsx - Router Setup]
        
        subgraph Pages["pages/"]
            Dashboard[Dashboard.tsx]
            AskAgent[AskTheAgentPage.tsx]
            Reasoning[ReasoningConfidence.tsx]
            ChangeIntel[ChangeIntelligence.tsx]
        end
        
        subgraph Components["components/"]
            Sidebar[Sidebar.tsx - Navigation]
            Header[Header.tsx]
            AskTheAgent[AskTheAgent.tsx - Query Interface]
            FilesIndexed[FilesIndexed.tsx]
            SystemEvents[SystemEventsLog.tsx]
            Throughput[IndexingThroughput.tsx]
            TargetRepo[TargetRepository.tsx]
            SystemViz[SystemVisualization.tsx]
            AILoad[AIModelLoad.tsx]
        end
    end
    
    MainTsx --> AppTsx
    AppTsx --> Sidebar
    AppTsx --> Dashboard
    AppTsx --> AskAgent
    AppTsx --> Reasoning
    AppTsx --> ChangeIntel
    
    Dashboard --> Header
    Dashboard --> FilesIndexed
    Dashboard --> SystemEvents
    Dashboard --> Throughput
    Dashboard --> TargetRepo
    Dashboard --> SystemViz
    Dashboard --> AILoad
    
    AskAgent --> AskTheAgent
    
    style MainTsx fill:#ff9800
    style AppTsx fill:#ffa726
    style Pages fill:#e1f5ff
    style Components fill:#f3e5f5
```

---

## Pathway Engine Pipeline

Detailed view of the Pathway streaming pipeline.

```mermaid
graph LR
    subgraph Sources["Data Sources"]
        Local[Local Folder<br/>./watched_folder]
        GitHub[GitHub Webhook<br/>:8000]
    end
    
    subgraph Ingestion["Ingestion Layer"]
        LocalWatch[watch_local_folder]
        GitHubWatch[watch_github_repo]
        Normalize[loader.py<br/>Normalize Data]
    end
    
    subgraph Processing["Processing Pipeline"]
        Combine[Concat Streams]
        Split[Token Splitter<br/>max_tokens=400]
        Embed[Embedder<br/>Generate Vectors]
    end
    
    subgraph Storage["Vector Store"]
        Index[Live Index<br/>Incremental Updates]
        VectorDB[(Vector Database)]
    end
    
    subgraph API["Query API"]
        Server[VectorStoreServer<br/>:8765]
        Retrieve[/v1/retrieve]
        Stats[/v1/statistics]
    end
    
    Local --> LocalWatch
    GitHub --> GitHubWatch
    LocalWatch --> Normalize
    GitHubWatch --> Normalize
    Normalize --> Combine
    Combine --> Split
    Split --> Embed
    Embed --> Index
    Index --> VectorDB
    VectorDB --> Server
    Server --> Retrieve
    Server --> Stats
    
    style Sources fill:#e8f5e8
    style Ingestion fill:#fff3e0
    style Processing fill:#e1f5ff
    style Storage fill:#f3e5f5
    style API fill:#fce4ec
```

---

## API Interaction Flow

Complete request/response flow between frontend and backend.

```mermaid
sequenceDiagram
    participant Browser
    participant React
    participant FastAPI
    participant DevAgent
    participant PathwayRetriever
    participant VectorStore
    participant Planner
    participant Tools
    participant Gemini
    participant ConfidenceAssessor
    
    Browser->>React: User enters question
    React->>FastAPI: POST /v1/agent/ask<br/>{query: "..."}
    
    FastAPI->>DevAgent: answer_question(query)
    
    rect rgb(225, 245, 255)
        Note over DevAgent,VectorStore: Step 1: OBSERVE
        DevAgent->>PathwayRetriever: retrieve(query)
        PathwayRetriever->>VectorStore: POST /v1/retrieve
        VectorStore-->>PathwayRetriever: documents + metadata
        PathwayRetriever-->>DevAgent: raw_docs
        DevAgent->>DevAgent: build_prompt_context()
    end
    
    rect rgb(255, 243, 225)
        Note over DevAgent,Planner: Step 2: PLAN
        DevAgent->>Planner: plan(query, context, metadata)
        Planner-->>DevAgent: strategy, tools_needed, reasoning
    end
    
    rect rgb(243, 229, 245)
        Note over DevAgent,Tools: Step 3: USE TOOLS (conditional)
        alt Tools Needed
            DevAgent->>Tools: execute_tool(tool_name)
            Tools-->>DevAgent: tool_results
        end
    end
    
    rect rgb(232, 245, 233)
        Note over DevAgent,Gemini: Step 4: GENERATE
        DevAgent->>Gemini: generate(prompt, context)
        Gemini-->>DevAgent: LLM response
        DevAgent->>DevAgent: parse JSON response
    end
    
    rect rgb(252, 228, 236)
        Note over DevAgent,ConfidenceAssessor: Step 5: ASSESS CONFIDENCE
        DevAgent->>ConfidenceAssessor: assess(query, context, answer)
        ConfidenceAssessor-->>DevAgent: confidence score & level
    end
    
    rect rgb(241, 248, 233)
        Note over DevAgent: Step 6: FORMAT OUTPUT
        DevAgent->>DevAgent: format with hedge phrases
    end
    
    DevAgent-->>FastAPI: {explanation, code, instruction,<br/>confidence, strategy, sources, trace}
    FastAPI-->>React: JSON response
    React-->>Browser: Display formatted answer
```

---

## Component Dependencies

Module dependency graph showing import relationships.

```mermaid
graph TD
    subgraph External["External Dependencies"]
        FastAPI[FastAPI]
        Pathway[Pathway]
        LangGraph[LangGraph]
        Gemini[Google Gemini API]
        React[React]
        Vite[Vite]
    end
    
    subgraph BackendModules["Backend Modules"]
        Main[main.py]
        Agent[agent/agent.py]
        Planner[agent/planner.py]
        Tools[agent/tools.py]
        Confidence[agent/confidence.py]
        
        PathwayMain[pathway_engine/main.py]
        Retriever[pathway_engine/query/retriever.py]
        ContextBuilder[pathway_engine/query/context_builder.py]
        LocalSource[pathway_engine/ingestion/local_source.py]
        GitHubSource[pathway_engine/ingestion/github_source.py]
        Embeddings[pathway_engine/indexing/embeddings.py]
        
        GeminiClient[llm/gemini_client.py]
    end
    
    subgraph FrontendModules["Frontend Modules"]
        MainTSX[main.tsx]
        AppTSX[App.tsx]
        Pages[Pages Components]
        Components[UI Components]
    end
    
    FastAPI --> Main
    Main --> Agent
    
    LangGraph --> Agent
    Agent --> Planner
    Agent --> Tools
    Agent --> Confidence
    Agent --> Retriever
    Agent --> ContextBuilder
    Agent --> GeminiClient
    
    Pathway --> PathwayMain
    PathwayMain --> LocalSource
    PathwayMain --> GitHubSource
    PathwayMain --> Embeddings
    
    Retriever --> PathwayMain
    
    Gemini --> GeminiClient
    
    React --> MainTSX
    Vite --> MainTSX
    MainTSX --> AppTSX
    AppTSX --> Pages
    AppTSX --> Components
    
    style External fill:#ffecb3
    style BackendModules fill:#e1f5ff
    style FrontendModules fill:#f3e5f5
```

---

## Deployment Architecture

Production deployment view with all services.

```mermaid
graph TB
    subgraph Internet["Internet"]
        Users[Users/Browsers]
        GitHubWebhook[GitHub Webhooks]
    end
    
    subgraph Server["Server/Container"]
        subgraph FrontendProcess["Frontend Process"]
            Vite[Vite Dev Server<br/>:5173]
        end
        
        subgraph BackendProcess["Backend Process"]
            FastAPIServer[FastAPI Server<br/>:8003]
        end
        
        subgraph PathwayProcess["Pathway Process"]
            WebhookServer[Webhook Server<br/>:8000]
            VectorServer[Vector Store Server<br/>:8765]
            PathwayRuntime[Pathway Runtime<br/>Streaming Engine]
        end
        
        subgraph Storage["File System"]
            WatchedFolder[./watched_folder]
            Cache[./Cache]
            Output[./pathway_output]
        end
    end
    
    subgraph ExternalAPIs["External APIs"]
        GeminiAPI[Google Gemini API]
    end
    
    Users -->|HTTP :5173| Vite
    Vite -->|Proxy/API| FastAPIServer
    FastAPIServer -->|Query| VectorServer
    FastAPIServer -->|Generate| GeminiAPI
    
    GitHubWebhook -->|POST :8000| WebhookServer
    WebhookServer -->|Events| PathwayRuntime
    
    PathwayRuntime -->|Watch| WatchedFolder
    PathwayRuntime -->|Index| VectorServer
    PathwayRuntime -->|Cache| Cache
    PathwayRuntime -->|Output| Output
    
    style FrontendProcess fill:#e1f5ff
    style BackendProcess fill:#fff4e1
    style PathwayProcess fill:#f0f0f0
    style Storage fill:#e8f5e8
    style ExternalAPIs fill:#ffecb3
```

---

## Technology Stack

Overview of technologies used in the project.

```mermaid
mindmap
  root((Pathway-Hack))
    Frontend
      React 19.2
      TypeScript
      Vite
      React Router
      Lucide Icons
      React Markdown
      Highlight.js
    Backend
      Python
      FastAPI
      Pydantic
      Uvicorn
      python-dotenv
    AI/ML
      Pathway
        Vector Store
        Live Indexing
        Embeddings
        Streaming
      LangGraph
        State Management
        Workflow Orchestration
        Conditional Routing
      Google Gemini
        Text Generation
        JSON Parsing
    Data Processing
      Token Splitter
      Context Builder
      Document Retriever
      Version Tracker
    Development
      ESLint
      TypeScript Compiler
      Git
      npm
```

---

## State Flow in Agent

State transformations through the LangGraph workflow.

```mermaid
stateDiagram-v2
    [*] --> QueryReceived: User query
    
    QueryReceived --> ObserveState: Initialize state
    
    ObserveState --> PlanState: Add context, raw_docs, metadata
    note right of ObserveState
        State fields added:
        - raw_docs: list
        - context: str
        - metadata: dict
    end note
    
    PlanState --> ToolsDecision: Add strategy, tools_needed, reasoning
    note right of PlanState
        State fields added:
        - strategy: str
        - plan_reasoning: str
        - tools_needed: list
    end note
    
    ToolsDecision --> ToolsState: if tools_needed
    ToolsDecision --> GenerateState: else
    
    ToolsState --> GenerateState: Add tool_results
    note right of ToolsState
        State fields added:
        - tool_results: dict
    end note
    
    GenerateState --> AssessState: Add answer, explanation, code, instruction
    note right of GenerateState
        State fields added:
        - answer: str
        - explanation: str
        - code: str
        - instruction: str
    end note
    
    AssessState --> FormatState: Add confidence metrics
    note right of AssessState
        State fields added:
        - confidence_score: float
        - confidence_level: str
        - confidence_reasoning: str
        - should_hedge: bool
    end note
    
    FormatState --> [*]: Add final_answer
    note right of FormatState
        State fields added:
        - final_answer: str
    end note
```

---

## File Structure Tree

Directory structure of the repository.

```mermaid
graph TD
    Root[/Pathway-Hack]
    
    Root --> Backend[backend/]
    Root --> Frontend[frontend/]
    Root --> README[README.md]
    Root --> ARCH[ARCHITECTURE.md]
    
    Backend --> BMain[main.py]
    Backend --> BTest[test_agent.py]
    Backend --> BAgent[agent/]
    Backend --> BLLM[llm/]
    Backend --> BPathway[pathway_engine/]
    Backend --> BCache[Cache/]
    Backend --> BOutput[pathway_output]
    
    BAgent --> AgentPy[agent.py]
    BAgent --> PlannerPy[planner.py]
    BAgent --> ToolsPy[tools.py]
    BAgent --> ConfPy[confidence.py]
    
    BLLM --> GeminiPy[gemini_client.py]
    
    BPathway --> PMain[main.py]
    BPathway --> PConfig[config.py]
    BPathway --> PIngest[ingestion/]
    BPathway --> PIndex[indexing/]
    BPathway --> PQuery[query/]
    BPathway --> PState[state/]
    
    PIngest --> LocalSrc[local_source.py]
    PIngest --> GitHubSrc[github_source.py]
    PIngest --> LoaderPy[loader.py]
    
    PIndex --> LiveIdx[live_index.py]
    PIndex --> EmbedPy[embeddings.py]
    
    PQuery --> RetrieverPy[retriever.py]
    PQuery --> ContextPy[context_builder.py]
    
    PState --> VersionPy[version_tracker.py]
    
    Frontend --> FPackage[package.json]
    Frontend --> FVite[vite.config.ts]
    Frontend --> FIndex[index.html]
    Frontend --> FSrc[src/]
    Frontend --> FPublic[public/]
    
    FSrc --> FMain[main.tsx]
    FSrc --> FApp[App.tsx]
    FSrc --> FPages[pages/]
    FSrc --> FComps[components/]
    FSrc --> FAssets[assets/]
    
    FPages --> PageDash[Dashboard.tsx]
    FPages --> PageAsk[AskTheAgentPage.tsx]
    FPages --> PageReason[ReasoningConfidence.tsx]
    FPages --> PageChange[ChangeIntelligence.tsx]
    
    FComps --> CompSide[Sidebar.tsx]
    FComps --> CompHead[Header.tsx]
    FComps --> CompAsk[AskTheAgent.tsx]
    FComps --> CompFiles[FilesIndexed.tsx]
    FComps --> CompEvents[SystemEventsLog.tsx]
    FComps --> CompThrough[IndexingThroughput.tsx]
    FComps --> CompTarget[TargetRepository.tsx]
    FComps --> CompViz[SystemVisualization.tsx]
    FComps --> CompAI[AIModelLoad.tsx]
    
    style Root fill:#ff9800
    style Backend fill:#e1f5ff
    style Frontend fill:#f3e5f5
    style BPathway fill:#fff4e1
    style FSrc fill:#e8f5e9
```

---

## Key Features Overview

```mermaid
mindmap
  root((Key Features))
    Live Code Intelligence
      Incremental Indexing
      Real-time Updates
      GitHub Integration
      Local File Watching
    Agentic System
      Multi-step Reasoning
      Strategy Planning
      Tool Selection
      Confidence Assessment
    Developer Experience
      Natural Language Queries
      Code Context Retrieval
      Structured Responses
      Source Attribution
    Technical Innovation
      Pathway Streaming
      LangGraph Orchestration
      Vector Embeddings
      Live Vector Store
```

---

## Summary

This repository implements a **Live Code Intelligence Agent** with the following key characteristics:

1. **Real-time Data Pipeline**: Uses Pathway to continuously index code from local files and GitHub webhooks
2. **Agentic Reasoning**: LangGraph-based multi-step workflow with planning, tool use, and confidence assessment
3. **Modern Stack**: React frontend, FastAPI backend, Pathway for streaming, and Gemini for LLM generation
4. **Live Vector Store**: Incremental indexing with embedding-based retrieval for context-aware responses

The system enables developers to ask natural language questions about their codebase and receive intelligent, context-aware answers with source attribution and confidence scores.

# Pathway-Hack System Architecture

Complete system architecture diagram showing all components, data flow, and interactions.

```mermaid
graph TB
    subgraph Users["👥 Users"]
        User[Developer/User]
    end
    
    subgraph Frontend["🎨 Frontend (React + Vite :5173)"]
        UI[React UI]
        Dashboard[Dashboard]
        AskAgent[Ask The Agent]
        Pages[Other Pages]
    end
    
    subgraph Backend["🚀 Backend (FastAPI :8003)"]
        API[FastAPI Server<br/>main.py]
        
        subgraph Agent["🧠 Agentic System (LangGraph)"]
            DevAgent[DevAgent<br/>agent.py]
            Planner[Planner<br/>Strategy Selection]
            Tools[Tools<br/>Summarize, Compare, etc.]
            Confidence[Confidence Assessor<br/>Score & Hedge]
        end
        
        LLM[Gemini Client<br/>gemini_client.py]
    end
    
    subgraph PathwayEngine["🔥 Pathway Engine"]
        VectorServer[Vector Store Server<br/>:8765]
        
        subgraph Ingestion["📥 Ingestion"]
            LocalWatch[Local Folder Watch<br/>local_source.py]
            GitHubWatch[GitHub Webhook<br/>github_source.py<br/>:8000]
            Loader[Loader<br/>Normalize Data]
        end
        
        subgraph Processing["⚙️ Processing"]
            Splitter[Token Splitter<br/>max_tokens=400]
            Embedder[Embeddings<br/>embeddings.py]
            LiveIndex[Live Index<br/>Incremental Updates]
        end
        
        subgraph Query["🔍 Query"]
            Retriever[Retriever<br/>retriever.py]
            ContextBuilder[Context Builder<br/>context_builder.py]
        end
    end
    
    subgraph External["🌐 External"]
        LocalFiles[📁 Local Files<br/>./watched_folder]
        GitHub[📦 GitHub Repo]
        GeminiAPI[🤖 Google Gemini API]
    end
    
    %% User Interactions
    User -->|Browse UI| UI
    UI --> Dashboard
    UI --> AskAgent
    UI --> Pages
    
    %% Query Flow
    AskAgent -->|POST /v1/agent/ask| API
    API -->|answer_question| DevAgent
    
    %% Agent Workflow
    DevAgent -->|1. Observe| Retriever
    Retriever -->|query| VectorServer
    VectorServer -->|relevant docs| Retriever
    Retriever -->|context| DevAgent
    
    DevAgent -->|2. Plan| Planner
    Planner -->|strategy| DevAgent
    
    DevAgent -->|3. Use Tools| Tools
    Tools -->|results| DevAgent
    
    DevAgent -->|4. Generate| LLM
    LLM -->|request| GeminiAPI
    GeminiAPI -->|response| LLM
    LLM -->|answer| DevAgent
    
    DevAgent -->|5. Assess| Confidence
    Confidence -->|score| DevAgent
    
    DevAgent -->|response| API
    API -->|JSON| AskAgent
    AskAgent -->|display| User
    
    %% Data Ingestion Flow (Background)
    LocalFiles -.->|file changes| LocalWatch
    GitHub -.->|webhook events| GitHubWatch
    
    LocalWatch -->|stream| Loader
    GitHubWatch -->|stream| Loader
    Loader -->|normalized| Splitter
    Splitter -->|chunks| Embedder
    Embedder -->|vectors| LiveIndex
    LiveIndex -->|index| VectorServer
    
    %% Context Building
    Retriever --> ContextBuilder
    ContextBuilder -->|formatted context| DevAgent
    
    %% Styling
    style Users fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Frontend fill:#61dafb,stroke:#333,stroke-width:2px
    style Backend fill:#009688,stroke:#333,stroke-width:2px
    style Agent fill:#ff6b6b,stroke:#333,stroke-width:2px
    style PathwayEngine fill:#ffd93d,stroke:#333,stroke-width:3px
    style Ingestion fill:#e8f5e9,stroke:#333,stroke-width:1px
    style Processing fill:#e1f5ff,stroke:#333,stroke-width:1px
    style Query fill:#fff3e0,stroke:#333,stroke-width:1px
    style External fill:#f3e5f5,stroke:#333,stroke-width:2px
    
    style DevAgent fill:#ff5252,stroke:#333,stroke-width:2px
    style VectorServer fill:#ffeb3b,stroke:#333,stroke-width:2px
    style LLM fill:#4285f4,stroke:#fff,stroke-width:2px
    style GeminiAPI fill:#4285f4,stroke:#fff,stroke-width:2px
```

## Key Components

### Frontend (Port 5173)
- **React + TypeScript** UI with Dashboard, Ask The Agent interface, and monitoring pages
- **Vite** for development and building

### Backend (Port 8003)
- **FastAPI** server exposing agent endpoints
- **LangGraph-based Agent** with multi-step reasoning:
  1. **Observe** - Retrieve relevant context from vector store
  2. **Plan** - Select strategy (direct, summarize, uncertain, compare)
  3. **Use Tools** - Execute tools if needed (summarize, compare, etc.)
  4. **Generate** - Create response using Gemini LLM
  5. **Assess** - Calculate confidence score and add hedge phrases
  6. **Format** - Final output structuring

### Pathway Engine (Port 8765)
- **Live Streaming Pipeline**: Continuous ingestion from local files and GitHub webhooks
- **Incremental Indexing**: Real-time vector embeddings as code changes
- **Vector Store Server**: Fast semantic search for context retrieval
- **GitHub Webhook Server** (Port 8000): Receives repository events

### Data Flow

**Background (Continuous):**
1. Code changes → Ingestion (local/GitHub)
2. Normalization → Token splitting (400 tokens)
3. Embedding generation → Live indexing
4. Vector store updates (incremental)

**User Query:**
1. User asks question → React UI
2. API call → FastAPI Backend
3. DevAgent workflow (6 steps via LangGraph)
4. Context retrieval from Vector Store
5. LLM generation via Gemini
6. Structured response with confidence score
7. Display to user with source attribution

### Technology Stack
- **Frontend**: React 19, TypeScript, Vite, React Router
- **Backend**: Python, FastAPI, Pydantic, LangGraph
- **AI/ML**: Pathway (streaming + vector store), Google Gemini (LLM)
- **Integration**: GitHub webhooks, file system watchers

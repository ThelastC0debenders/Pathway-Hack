# Quick Mermaid Diagrams Reference

This is a quick reference guide for the Mermaid diagrams in this repository.

## 📚 Full Documentation

See **[ARCHITECTURE.md](./ARCHITECTURE.md)** for complete, detailed diagrams with explanations.

---

## Quick System Overview

```mermaid
graph LR
    User[👤 User] --> Frontend[⚛️ React Frontend<br/>:5173]
    Frontend --> API[🚀 FastAPI Backend<br/>:8003]
    API --> Agent[🧠 DevAgent<br/>LangGraph]
    Agent --> Vector[🔥 Pathway Vector Store<br/>:8765]
    Agent --> Gemini[🤖 Gemini LLM]
    
    GitHub[📦 GitHub] -.->|webhooks| Webhook[Webhook Server<br/>:8000]
    Local[📁 Local Files] -.->|watch| Webhook
    Webhook --> Vector
    
    style Frontend fill:#61dafb
    style API fill:#009688
    style Agent fill:#ff6b6b
    style Vector fill:#ffd93d
    style Gemini fill:#4285f4
```

---

## Agent Workflow

```mermaid
graph TD
    Start([Query]) --> Observe[🔍 Observe<br/>Retrieve Context]
    Observe --> Plan[🧠 Plan<br/>Select Strategy]
    Plan --> Decision{Tools<br/>Needed?}
    Decision -->|Yes| Tools[🛠️ Use Tools]
    Decision -->|No| Generate[💬 Generate]
    Tools --> Generate
    Generate --> Assess[📊 Assess<br/>Confidence]
    Assess --> Format[✨ Format]
    Format --> End([Response])
    
    style Observe fill:#e3f2fd
    style Plan fill:#fff3e0
    style Tools fill:#f3e5f5
    style Generate fill:#e8f5e9
    style Assess fill:#fce4ec
    style Format fill:#f1f8e9
```

---

## Technology Stack

```mermaid
graph TB
    subgraph Frontend
        React[React 19.2]
        TS[TypeScript]
        Vite[Vite]
        Router[React Router]
    end
    
    subgraph Backend
        FastAPI[FastAPI]
        Python[Python]
        Pydantic[Pydantic]
    end
    
    subgraph AI_ML[AI/ML]
        Pathway[Pathway<br/>Streaming & Vector Store]
        LangGraph[LangGraph<br/>Workflow Orchestration]
        Gemini[Google Gemini<br/>LLM Generation]
    end
    
    Frontend --> Backend
    Backend --> AI_ML
    
    style Frontend fill:#61dafb
    style Backend fill:#009688
    style AI_ML fill:#ff6b6b
```

---

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Agent
    participant Pathway
    participant Gemini
    
    Note over Pathway: Continuous indexing<br/>of code changes
    
    User->>Frontend: Ask question
    Frontend->>API: POST /v1/agent/ask
    API->>Agent: answer_question()
    
    Agent->>Pathway: Retrieve context
    Pathway-->>Agent: Relevant documents
    
    Agent->>Agent: Plan strategy
    Agent->>Agent: Use tools (optional)
    
    Agent->>Gemini: Generate response
    Gemini-->>Agent: LLM output
    
    Agent->>Agent: Assess confidence
    Agent->>Agent: Format output
    
    Agent-->>API: Structured response
    API-->>Frontend: JSON
    Frontend-->>User: Display answer
```

---

## Repository Structure

```
Pathway-Hack/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── agent/                  # Agentic reasoning
│   │   ├── agent.py            # LangGraph workflow
│   │   ├── planner.py          # Strategy selection
│   │   ├── tools.py            # Agent tools
│   │   └── confidence.py       # Confidence scoring
│   ├── pathway_engine/         # Core streaming engine
│   │   ├── main.py             # Pathway runtime
│   │   ├── ingestion/          # Data sources
│   │   ├── indexing/           # Vector indexing
│   │   ├── query/              # Retrieval
│   │   └── state/              # Version tracking
│   └── llm/
│       └── gemini_client.py    # LLM client
├── frontend/
│   └── src/
│       ├── pages/              # Dashboard, AskTheAgent, etc.
│       └── components/         # UI components
└── ARCHITECTURE.md             # Full documentation
```

---

## Key Services & Ports

| Service | Port | Purpose |
|---------|------|---------|
| Frontend (Vite) | 5173 | React development server |
| Backend (FastAPI) | 8003 | Agent API endpoints |
| Pathway Vector Store | 8765 | Document retrieval API |
| GitHub Webhook Server | 8000 | Receives GitHub events |

---

## Key Features

🔥 **Live Indexing**: Pathway continuously indexes code changes in real-time

🧠 **Agentic Workflow**: LangGraph orchestrates multi-step reasoning process

📚 **Context-Aware**: Vector search retrieves relevant code snippets

🎯 **Confidence Scoring**: Assesses answer reliability and adds hedge phrases

🤖 **LLM Generation**: Gemini API generates natural language responses

📊 **Source Attribution**: Shows which files and chunks informed the answer

---

## Quick Links

- 📖 [Full Architecture Documentation](./ARCHITECTURE.md)
- 🔙 [Backend README](./backend/README.md)
- 🎨 [Frontend README](./frontend/README.md)

---

## Diagram Formats Supported

All diagrams in this repository use **Mermaid** syntax, which is natively supported by:

- ✅ GitHub
- ✅ GitLab
- ✅ VS Code (with Mermaid extension)
- ✅ Markdown editors
- ✅ Documentation sites (MkDocs, Docusaurus, etc.)

You can also render them online at [mermaid.live](https://mermaid.live/)

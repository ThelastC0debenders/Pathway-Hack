# Pathway-Hack

A Live Code Intelligence Agent built with Pathway, LangGraph, and React.

## 📊 Architecture

For detailed architecture diagrams and system visualization, see **[ARCHITECTURE.md](./ARCHITECTURE.md)** which includes:
- System Architecture Overview
- Data Flow Diagrams
- Agent Workflow (LangGraph)
- Component Structures
- API Interaction Flows
- Technology Stack
- And more Mermaid diagrams!

## 📁 Repository Structure

```
backend/
│
├── main.py                     # 🚀 FastAPI entry point
├── test_agent.py               # Test scripts
│
├── pathway_engine/             # 🔥 CORE LIVE ENGINE (Pathway)
│   ├── main.py                 # Starts Pathway runtime
│   │
│   ├── ingestion/
│   │   ├── github_source.py    # Watches GitHub repo
│   │   ├── local_source.py     # Watches local folder
│   │   └── loader.py           # Normalizes code/docs
│   │
│   ├── indexing/
│   │   ├── live_index.py       # Incremental live indexing
│   │   └── embeddings.py       # Pathway-managed embeddings
│   │
│   ├── query/
│   │   ├── retriever.py        # Fetches fresh context
│   │   └── context_builder.py  # Builds prompt-ready context
│   │
│   └── state/
│       └── version_tracker.py  # Tracks commits / file versions
│
├── agent/                      # 🧠 AGENTIC REASONING
│   ├── agent.py                # Observe → reason → respond
│   ├── planner.py              # Multi-step reasoning
│   ├── tools.py                # Diff, summarize, search
│   └── confidence.py           # Confidence & uncertainty
│
└── llm/                        # 🤖 LLM CLIENT (GENERATION ONLY)
    └── gemini_client.py        # Gemini API wrapper

frontend/
│
├── src/
│   ├── main.tsx                # Entry point
│   ├── App.tsx                 # Router setup
│   │
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── AskTheAgentPage.tsx
│   │   ├── ReasoningConfidence.tsx
│   │   └── ChangeIntelligence.tsx
│   │
│   └── components/
│       ├── Sidebar.tsx
│       ├── Header.tsx
│       ├── AskTheAgent.tsx
│       ├── FilesIndexed.tsx
│       ├── SystemEventsLog.tsx
│       └── ... (more components)
│
└── package.json
```
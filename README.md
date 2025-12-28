backend/
│
├── main.py                     # 🚀 FastAPI entry point
├── api.py                      # API routes (query, status)
├── schemas.py                  # Request/response models
├── config.py                   # Env vars, repo paths, API keys
│
├── pathway_engine/             # 🔥 CORE LIVE ENGINE (Pathway)
│   ├── engine.py               # Starts Pathway runtime
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
├── llm/                        # 🤖 LLM CLIENT (GENERATION ONLY)
│   └── gemini_client.py        # Gemini API wrapper
│
├── change_intelligence/        # 🔍 DIFFERENTIATION
│   ├── change_detector.py      # What changed?
│   ├── breaking_change.py      # API breaking change detection
│   └── impact_analysis.py      # Downstream impact
│
├── memory/                     # 🧠 DEVELOPER MEMORY
│   ├── memory_store.py         # Stores past answers/decisions
│   └── memory_retriever.py
│
└── utils/
    └── logger.py               # Logging / debug helpers


# new test  
# webhook works
# it works fr
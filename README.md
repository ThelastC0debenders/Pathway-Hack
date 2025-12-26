# Pathway-Hack

live-codebase-agent/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── pathway_engine/                 # 🔥 CORE ENGINE (Pathway runs continuously)
│   ├── main.py                     # Entry point: starts Pathway app
│   ├── config.py                   # Repo paths, indexing config
│   │
│   ├── ingestion/                  # LIVE DATA INGESTION
│   │   ├── github_source.py         # Watches GitHub repo
│   │   ├── local_source.py          # Watches local folder
│   │   └── loader.py                # Normalizes code + docs
│   │
│   ├── indexing/                   # LIVE / INCREMENTAL INDEXING
│   │   ├── live_index.py            # Core Pathway indexing logic
│   │   └── embeddings.py            # Embedding schema (Pathway‑managed)
│   │
│   ├── query/                      # PATHWAY QUERY LAYER
│   │   ├── retriever.py             # Fetches fresh context
│   │   └── context_builder.py       # Builds prompt context
│   │
│   └── state/                      # VERSION / CHANGE TRACKING
│       └── version_tracker.py
│
├── agent/                          # 🧠 AGENTIC REASONING (THIN LAYER)
│   ├── agent.py                    # Observe → reason → respond
│   ├── planner.py                  # Multi‑step planning
│   ├── tools.py                    # Diff, summarize, search
│   └── confidence.py               # Confidence / uncertainty
│
├── llm/                            # 🤖 LLM CLIENT (GENERATION ONLY)
│   └── gemini_client.py            # Gemini API wrapper
│
├── change_intelligence/             # 🔍 DIFFERENTIATION
│   ├── change_detector.py           # What changed?
│   ├── breaking_change.py           # API breaking changes
│   └── impact_analysis.py           # Downstream impact
│
├── memory/                         # 🧠 DEVELOPER MEMORY
│   ├── memory_store.py
│   └── memory_retriever.py
│
├── ui/                             # 🎨 STREAMLIT UI
│   ├── app.py                      # Main UI
│   └── components.py               # Panels (answer, change, confidence)
│
├── demo/                           # 🎬 JUDGE‑FRIENDLY
│   ├── demo_script.md               # 90‑sec demo flow
│   └── sample_questions.md
│
└── assets/
    └── architecture.png             # Architecture diagram

"""
Manual test for Person-2 Agent.
Make sure Pathway Engine (Person-1) is already running.
"""

from pathway_engine.main import engine

from agent.agent import LiveAgent
from agent.planner import plan_step
from agent.tools import fetch_live_context
from agent.confidence import estimate_confidence

from pathway_engine.query.retriever import LiveRetriever
from pathway_engine.query.context_builder import build_context


def main():
    if engine.table is None:
        print("⚡ Engine not running. Starting in-process mode...")
        engine.start(start_web_server=False)

    print("✅ Connected to Pathway Engine")

    # ----------------------------
    # Live data from Pathway
    # ----------------------------
    live_table = engine.get_live_table()

    retriever = LiveRetriever(live_table)
    context_builder = build_context(retriever)

    # ----------------------------
    # Agent stack
    # ----------------------------
    tools = fetch_live_context()
    planner = plan_step(tools)
    confidence = estimate_confidence()

    agent = LiveAgent(
        planner=planner,
        context_builder=context_builder,
        confidence_scorer=confidence,
    )

    # ----------------------------
    # Test query
    # ----------------------------
    query = "What changed recently in the repository?"

    print("\n🧠 Running agent query...")
    result = agent.run(query)

    print("\n================ RESULT ================\n")
    print("📌 Answer:\n", result["answer"])
    print("\n📚 Sources:\n", result["sources"])
    print("\n🎯 Confidence:", result["confidence"])


if __name__ == "__main__":
    main()

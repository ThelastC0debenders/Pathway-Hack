"""
Manual test for Person-2 Agent.
Make sure Pathway Engine (Person-1) is already running.
"""

from pathway_engine.main import engine

from agent.agent import Agent
from agent.planner import Planner
from agent.tools import ToolRegistry
from agent.confidence import ConfidenceScorer

from pathway_engine.query.retriever import LiveRetriever
from pathway_engine.query.context_builder import ContextBuilder


def main():
    if engine is None:
        raise RuntimeError(
            "Pathway Engine is not running. "
            "Start it first using: python -m pathway_engine.main"
        )

    print("✅ Connected to Pathway Engine")

    # ----------------------------
    # Live data from Pathway
    # ----------------------------
    live_table = engine.get_live_table()

    retriever = LiveRetriever(live_table)
    context_builder = ContextBuilder(retriever)

    # ----------------------------
    # Agent stack
    # ----------------------------
    tools = ToolRegistry()
    planner = Planner(tools)
    confidence = ConfidenceScorer()

    agent = Agent(
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

"""
Manual test for Person-2 Agent.
Make sure Pathway Engine (Person-1) is already running.
"""

from dotenv import load_dotenv
from pathway_engine.main import engine
from pathway_engine.query.retriever import LiveRetriever

from agent.agent import LiveAgent
from agent.confidence import estimate_confidence
from llm.gemini_client import get_gemini_llm


def main():
    load_dotenv()
    if engine.table is None:
        print("⚡ Engine not running. Starting in-process mode...")
        engine.start(start_web_server=False, mode="static")

    print("✅ Connected to Pathway Engine")

    # ----------------------------
    # Live data from Pathway
    # ----------------------------
    live_table = engine.get_live_table()
    retriever = LiveRetriever(live_table)

    # ----------------------------
    # Agent stack
    # ----------------------------
    llm = get_gemini_llm()
    
    agent = LiveAgent(
        llm=llm,
        retriever=retriever,
        confidence_scorer=estimate_confidence,
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

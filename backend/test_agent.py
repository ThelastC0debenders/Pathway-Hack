from llm.gemini_client import get_gemini_llm
from pathway_engine.query.retriever import LiveRetriever
from agent.agent import LiveAgent
from pathway_engine.main import engine


def main():
    print("🔍 Testing agent with LIVE Pathway engine")

    # Get live Pathway table
    live_table = engine.get_live_table()

    # Init retriever
    retriever = LiveRetriever(live_table)

    # Init LLM
    llm = get_gemini_llm()

    # Init Agent
    agent = LiveAgent(llm, retriever)

    # Ask a question
    question = "What files exist in this repository?"
    answer = agent.run(question)

    print("\n🧠 AGENT ANSWER:\n")
    print(answer)


if __name__ == "__main__":
    main()

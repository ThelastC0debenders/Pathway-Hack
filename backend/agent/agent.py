from langgraph.graph import StateGraph
from agent.tools import fetch_live_context
from agent.planner import plan_step


class LiveAgent:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(dict)

        def retrieve(state):
            state["context"] = fetch_live_context(self.retriever)
            return state

        def respond(state):
            prompt = f"""
You are an expert developer assistant.

Context:
{state['context']}

Question:
{state['question']}
"""
            response = self.llm.invoke(prompt)
            state["answer"] = response.content
            return state

        graph.add_node("retrieve", retrieve)
        graph.add_node("respond", respond)

        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "respond")

        return graph.compile()

    def run(self, question: str):
        return self.graph.invoke({"question": question})["answer"]

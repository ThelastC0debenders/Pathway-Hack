from langgraph.graph import StateGraph
from agent.tools import fetch_live_context
from agent.planner import plan_step


class LiveAgent:
    def __init__(self, llm, retriever, confidence_scorer=None):
        self.llm = llm
        self.retriever = retriever
        self.confidence_scorer = confidence_scorer
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(dict)

        def retrieve(state):
            # Returns { "content": ..., "sources": ... }
            context_data = fetch_live_context(self.retriever)
            state["context"] = context_data["content"]
            state["sources"] = context_data["sources"]
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
            
            if self.confidence_scorer:
                state["confidence"] = self.confidence_scorer(state["answer"])
            else:
                state["confidence"] = 0.0
                
            return state

        graph.add_node("retrieve", retrieve)
        graph.add_node("respond", respond)

        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "respond")

        return graph.compile()

    def run(self, question: str):
        result = self.graph.invoke({"question": question})
        return {
            "answer": result["answer"],
            "sources": result.get("sources", []),
            "confidence": result.get("confidence", 0.0)
        }

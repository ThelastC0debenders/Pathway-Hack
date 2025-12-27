from pathway_engine.query.retriever import PathwayRetriever
from pathway_engine.query.context_builder import ContextBuilder
from llm.gemini_client import GeminiClient

class DevAgent:
    def __init__(self):
        self.retriever = PathwayRetriever()
        self.builder = ContextBuilder()
        self.llm = GeminiClient()

    def answer_question(self, user_query: str):
        # 1. Retrieve
        raw_docs = self.retriever.retrieve(user_query)
        
        # 2. Build Context
        context = self.builder.build_prompt_context(raw_docs)

        # 🔥 DEBUG: Print the first 500 characters of context
        # print("\n--- [DEBUG] CONTEXT SENT TO GEMINI ---")
        # print(context[:500] if context else "⚠️ CONTEXT IS EMPTY!")
        # print("--------------------------------------\n")

        # ✅ FIX: Proper indentation - exit early if no context
        if not context or context.strip() == "":
            return "I found relevant files, but they appear to be empty or unreadable."
        
        # ✅ This is now at the correct indentation level
        # 3. ASK GEMINI
        system_msg = "You are a 'Live Code Agent'. Answer only using the provided snippets. If unsure, say 'The current codebase state doesn't specify this'."
        
        full_prompt = f"User Question: {user_query}\n\nLive Context:\n{context}"
        
        return self.llm.generate(full_prompt, system_instruction=system_msg)

# Test it
if __name__ == "__main__":
    agent = DevAgent()
    print("Agent Result:", agent.answer_question("How is the file loading handled?"))
import os
from agent.agent import DevAgent

# 1. Set your Gemini API Key for this session
os.environ["GEMINI_API_KEY"] = "your_actual_key_here"

def test_pipeline():
    print("\n--- 🧪 STARTING INTEGRATION TEST ---")
    agent = DevAgent()
    
    # Ask a question about the file you just dropped in Step 2
    question = "What does the README.md say?"
    print(f"❓ Question: {question}")
    
    try:
        response = agent.answer_question(question)
        print(f"\n🤖 Agent Response:\n{response}")
        print("\n--- ✅ TEST COMPLETE ---")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    test_pipeline()
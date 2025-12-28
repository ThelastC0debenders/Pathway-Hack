# test_agent.py

from agent.agent import DevAgent


def main():
    print("\n" + "=" * 80)
    print("🧪 TESTING LANGGRAPH DEV AGENT")
    print("=" * 80)

    agent = DevAgent()

    while True:
        try:
            query = input("\n❓ Ask a question (or type 'exit'): ").strip()

            if query.lower() in {"exit", "quit"}:
                print("\n👋 Exiting test runner.")
                break

            result = agent.answer_question(query, verbose=True)

            print("\n" + "-" * 80)
            print("🧠 FINAL ANSWER")
            print("-" * 80)
            print(result["answer"])

            print("\n📊 CONFIDENCE")
            print(f"Score   : {result['confidence']:.2%}")
            print(f"Level   : {result['confidence_level']}")
            print(f"Strategy: {result['strategy']}")
            
            # Display memory information
            if result.get('metadata', {}).get('memory_items_found'):
                memory_info = result['metadata']['memory_items_found']
                print("\n💾 MEMORY")
                print(f"Related questions found: {memory_info.get('related_questions', 0)}")
                print(f"Related explanations found: {memory_info.get('related_explanations', 0)}")
                print(f"Related design decisions found: {memory_info.get('related_decisions', 0)}")
            
            # Display change intelligence information
            if result.get('metadata', {}).get('change_analysis'):
                change_info = result['metadata']['change_analysis']
                print("\n🔍 CHANGE INTELLIGENCE")
                if change_info.get('changed'):
                    print(f"Files changed: {', '.join(change_info.get('files_changed', []))}")
                    print(f"Breaking changes: {'Yes' if change_info.get('breaking_change') else 'No'}")
                    if change_info.get('breaking_change'):
                        print(f"  - Details: {change_info.get('breaking_details', 'N/A')[:100]}")
                    print(f"Impact: {change_info.get('impact', ['N/A'])[0] if change_info.get('impact') else 'N/A'}")

        except KeyboardInterrupt:
            print("\n\n⛔ Interrupted by user. Exiting.")
            break

        except Exception as e:
            print("\n❌ ERROR DURING EXECUTION")
            print(e)
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

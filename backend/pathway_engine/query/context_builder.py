from typing import List, Dict

def build_context(docs: List[Dict], max_chars: int = 4000) -> Dict:
    combined = ""
    sources = set()

    for doc in docs:
        if len(combined) >= max_chars:
            break
        combined += doc["content"] + "\n\n"
        sources.add(doc["source"])

    return {
        "content": combined.strip(),
        "sources": list(sources)
    }

# import pathway as pw
# from pathway.xpacks.llm.vector_store import VectorStoreClient

# class PathwayRetriever:
#     def __init__(self, host="127.0.0.1", port=8765):
#         # Connects to the VectorServer started in main.py
#         self.client = VectorStoreClient(host=host, port=port)

#     def retrieve(self, query: str, k: int = 5):
#         print(f"[RETRIEVER] Searching for: '{query}'")
#         # k=5 means get the 5 most relevant code chunks
#         results = self.client.query(query, k=k)
        
#         if not results:
#             print("[RETRIEVER] ⚠️ No relevant context found.")
#         else:
#             print(f"[RETRIEVER] ✅ Found {len(results)} relevant snippets.")
            
#         return results
import re
import pathway as pw
from pathway.xpacks.llm.vector_store import VectorStoreClient

class PathwayRetriever:
    def __init__(self, host="127.0.0.1", port=8765):
        self.client = VectorStoreClient(host=host, port=port)

    def retrieve(self, query: str, k: int = 5):
        print(f"[RETRIEVER] Searching for: '{query}'")
        
        # 🎯 SMART FILENAME DETECTION
        filename_match = self._extract_filename(query)
        
        if filename_match:
            print(f"[RETRIEVER] 🎯 Detected target file: {filename_match}")
            # Get more results for filtering
            results = self.client.query(query, k=k*4)
            
            # Filter by filename found in the text
            filtered = self._filter_by_filename_in_text(results, filename_match)
            
            if filtered:
                print(f"[RETRIEVER] ✅ Found {len(filtered)} snippets from {filename_match}")
                return filtered[:k]
            else:
                print(f"[RETRIEVER] ⚠️ No results for {filename_match}, using general search")
                return results[:k]
        else:
            # 📚 General semantic search
            results = self.client.query(query, k=k)
        
        if not results:
            print("[RETRIEVER] ⚠️ No relevant context found.")
        else:
            print(f"[RETRIEVER] ✅ Found {len(results)} relevant snippets.")
        
        # 🔍 DEBUG: Show what was retrieved
        self._debug_results(results)
        
        return results

    def _extract_filename(self, query: str) -> str:
        """
        Extracts filename from queries like:
        - "What does README.md say?"
        - "Show me config.py"
        - "What's in the main.py file?"
        """
        # Pattern 1: Explicit filename with extension
        pattern1 = r'\b([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)\b'
        matches = re.findall(pattern1, query)
        
        # Filter out common false positives
        exclude = {'claude.ai', 'openai.com', 'v1.0', 'api.key', '127.0.0.1'}
        matches = [m for m in matches if m.lower() not in exclude and '/' not in m]
        
        if matches:
            return matches[0]
        
        # Pattern 2: Common file references without extension
        pattern2 = r'\b(readme|license|makefile|dockerfile|package)\b'
        match = re.search(pattern2, query, re.IGNORECASE)
        if match:
            # Try to guess the extension
            name = match.group(1).upper()
            if name == "README":
                return "README.md"
            return name
        
        return None

    def _filter_by_filename_in_text(self, results: list, target_filename: str) -> list:
        """
        Since Pathway doesn't expose metadata in results, we look for
        the filename in the actual text content of each chunk.
        
        This works because your context builder includes file paths!
        """
        filtered = []
        target_lower = target_filename.lower()
        
        for result in results:
            text = result.get('text', '')
            text_lower = text.lower()
            
            # Multiple matching strategies
            # 1. Direct filename match (README.md)
            # 2. With path (watched_folder/README.md)
            # 3. With quotes ("README.md")
            # 4. Case variations (readme.md, README.MD)
            
            if (target_lower in text_lower or
                f'"{target_lower}"' in text_lower or
                f"'{target_lower}'" in text_lower or
                target_lower.replace('.md', '') in text_lower):
                filtered.append(result)
        
        return filtered

    def _debug_results(self, results: list, max_preview: int = 3):
        """Print debug info about retrieved results"""
        if not results:
            return
        
        print(f"\n[RETRIEVER DEBUG] Top {min(len(results), max_preview)} results:")
        for i, result in enumerate(results[:max_preview]):
            text = result.get('text', '')
            dist = result.get('dist', 'N/A')
            
            # Try to extract filename from text
            file_match = re.search(r'FILE.*?:\s*(.+?)(?:\n|```)', text)
            file_info = file_match.group(1) if file_match else "unknown"
            
            print(f"\n  #{i+1}: {file_info} (dist: {dist})")
            print(f"  Preview: {text[:150]}...")
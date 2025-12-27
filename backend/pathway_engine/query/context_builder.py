# class ContextBuilder:
#     @staticmethod
#     def build_prompt_context(retrieved_docs):
#         if not retrieved_docs:
#             return "No relevant files found in the codebase."

#         context_blocks = ["Here are the most relevant snippets from the LIVE codebase:"]
        
#         for i, doc in enumerate(retrieved_docs):
#             text = doc.get("data") or doc.get("text") or ""
#             metadata = doc.get("metadata", {})
#             path = metadata.get("path", "Unknown File")
            
#             # Skip noise like requirements or lock files for this specific question
#             if any(x in path for x in ["requirements.txt", ".lock", "venv"]):
#                 continue

#             block = f"\nFILE #{i+1}: {path}\n```\n{text}\n```\n"
#             context_blocks.append(block)
        
#         return "\n".join(context_blocks)

import re

class ContextBuilder:
    def build_prompt_context(self, raw_docs: list) -> str:
        """
        Converts raw retrieval results into a formatted context string.
        
        CRITICAL: This method MUST extract and display file paths so that:
        1. The LLM knows which file each snippet is from
        2. The retriever can filter by filename (via text matching)
        """
        if not raw_docs:
            return ""
        
        context_parts = ["Here are the most relevant snippets from the LIVE codebase:"]
        
        for i, doc in enumerate(raw_docs, 1):
            text = doc.get('text', '').strip()
            
            # 🔍 Try to extract file path from the chunk text
            # Pathway chunks might already contain this from your loader
            file_path = self._extract_file_path(text)
            
            if not file_path:
                file_path = f"Source #{i}"
            
            # 📝 Format the snippet with clear file identification
            context_parts.append(f"\nFILE #{i}: {file_path}")
            context_parts.append(f"```\n{text}\n```")
        
        return "\n".join(context_parts)
    
    def _extract_file_path(self, text: str) -> str:
        """
        Extracts file path from chunk text.
        
        Your loader.py might already be adding this, e.g.:
        "# File: watched_folder/README.md\ncontent here..."
        """
        # Pattern 1: Explicit file path marker
        patterns = [
            r'#\s*[Ff]ile:\s*(.+?)(?:\n|$)',           # # File: path/to/file.py
            r'[Ff]ile\s*path:\s*(.+?)(?:\n|$)',        # File path: path/to/file.py
            r'Source:\s*(.+?)(?:\n|$)',                # Source: path/to/file.py
            r'([^\n]+?\.(?:py|js|ts|md|txt|json|yaml|yml))' # any/path/file.ext
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text[:200])  # Check first 200 chars
            if match:
                return match.group(1).strip()
        
        return None
    
    def build_prompt_context_with_relevance(self, raw_docs: list) -> str:
        """
        Alternative version that includes relevance scores.
        Use this if you want the LLM to know which sources are most relevant.
        """
        if not raw_docs:
            return ""
        
        context_parts = [
            "Here are the most relevant snippets from the LIVE codebase:",
            "(Ordered by relevance, most relevant first)\n"
        ]
        
        for i, doc in enumerate(raw_docs, 1):
            text = doc.get('text', '').strip()
            dist = doc.get('dist', None)
            
            file_path = self._extract_file_path(text)
            if not file_path:
                file_path = f"Source #{i}"
            
            # Add relevance indicator
            relevance = ""
            if dist is not None:
                # Lower distance = more relevant
                relevance = f" (relevance: {1 - dist:.2f})"
            
            context_parts.append(f"\nFILE #{i}: {file_path}{relevance}")
            context_parts.append(f"```\n{text}\n```")
        
        return "\n".join(context_parts)
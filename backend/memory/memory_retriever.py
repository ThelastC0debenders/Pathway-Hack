"""
Memory Retriever - Retrieves stored developer memory.

Queries the memory store to find:
- Past questions and answers
- Past explanations
- Design decisions
- Change contexts

Provides simple text-based search (no embeddings).
"""

import re
from typing import Dict, List, Optional
from .memory_store import MemoryStore, get_default_store


class MemoryRetriever:
    """
    Retrieves information from the memory store.
    
    Provides simple text-based search and retrieval capabilities.
    """
    
    def __init__(self, memory_store: Optional[MemoryStore] = None):
        """
        Initialize the memory retriever.
        
        Args:
            memory_store: MemoryStore instance to use. If None, uses default store.
        """
        self.store = memory_store or get_default_store()
    
    def search_questions(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Searches for questions matching the query.
        
        Uses simple text matching (case-insensitive, keyword-based).
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching question entries
        """
        questions = self.store.get_all_questions()
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        matches = []
        for question in questions:
            score = self._calculate_match_score(
                question.get("question", ""),
                question.get("answer", ""),
                question.get("tags", []),
                query_words,
                query_lower
            )
            if score > 0:
                matches.append((score, question))
        
        # Sort by score (descending) and return top results
        matches.sort(key=lambda x: x[0], reverse=True)
        return [q for _, q in matches[:limit]]
    
    def search_explanations(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Searches for explanations matching the query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching explanation entries
        """
        explanations = self.store.get_all_explanations()
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        matches = []
        for explanation in explanations:
            score = self._calculate_match_score(
                explanation.get("topic", ""),
                explanation.get("explanation", ""),
                explanation.get("tags", []),
                query_words,
                query_lower
            )
            if score > 0:
                matches.append((score, explanation))
        
        matches.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in matches[:limit]]
    
    def search_design_decisions(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Searches for design decisions matching the query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching design decision entries
        """
        decisions = self.store.get_all_design_decisions()
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        matches = []
        for decision in decisions:
            score = self._calculate_match_score(
                decision.get("decision", ""),
                decision.get("rationale", ""),
                decision.get("tags", []),
                query_words,
                query_lower
            )
            if score > 0:
                matches.append((score, decision))
        
        matches.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in matches[:limit]]
    
    def get_change_context_for_file(
        self,
        file_path: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Retrieves change contexts for a specific file.
        
        Args:
            file_path: Path to the file
            limit: Maximum number of results to return
            
        Returns:
            List of change context entries for the file
        """
        contexts = self.store.get_all_change_contexts()
        matches = [
            c for c in contexts
            if file_path in c.get("file_path", "") or c.get("file_path", "") in file_path
        ]
        
        # Sort by timestamp (most recent first)
        matches.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return matches[:limit]
    
    def find_related_context(
        self,
        query: str,
        file_path: Optional[str] = None
    ) -> Dict:
        """
        Finds all related context (questions, explanations, decisions) for a query.
        
        Args:
            query: Search query string
            file_path: Optional file path to filter by
            
        Returns:
            Dictionary with related items from all categories
        """
        results = {
            "questions": self.search_questions(query, limit=3),
            "explanations": self.search_explanations(query, limit=3),
            "design_decisions": self.search_design_decisions(query, limit=3),
            "change_contexts": []
        }
        
        if file_path:
            results["change_contexts"] = self.get_change_context_for_file(file_path, limit=3)
        
        return results
    
    def get_memory_summary(self) -> Dict:
        """
        Returns a summary of all stored memory.
        
        Returns:
            Dictionary with counts and recent items
        """
        all_questions = self.store.get_all_questions()
        all_explanations = self.store.get_all_explanations()
        all_decisions = self.store.get_all_design_decisions()
        all_contexts = self.store.get_all_change_contexts()
        
        recent = self.store.get_recent_items(limit=3)
        
        return {
            "counts": {
                "questions": len(all_questions),
                "explanations": len(all_explanations),
                "design_decisions": len(all_decisions),
                "change_contexts": len(all_contexts)
            },
            "recent": recent
        }
    
    def format_memory_response(
        self,
        related_context: Dict
    ) -> str:
        """
        Formats memory context into a human-readable response.
        
        Args:
            related_context: Dictionary with related items from find_related_context
            
        Returns:
            Formatted string for display
        """
        lines = []
        
        if related_context.get("questions"):
            lines.append("📋 Related Past Questions:")
            for q in related_context["questions"][:2]:
                lines.append(f"  Q: {q.get('question', '')}")
                lines.append(f"  A: {q.get('answer', '')[:100]}...")
        
        if related_context.get("explanations"):
            lines.append("\n📖 Related Explanations:")
            for e in related_context["explanations"][:2]:
                lines.append(f"  Topic: {e.get('topic', '')}")
                lines.append(f"  {e.get('explanation', '')[:100]}...")
        
        if related_context.get("design_decisions"):
            lines.append("\n🎯 Related Design Decisions:")
            for d in related_context["design_decisions"][:2]:
                lines.append(f"  Decision: {d.get('decision', '')}")
                lines.append(f"  Rationale: {d.get('rationale', '')[:100]}...")
        
        if related_context.get("change_contexts"):
            lines.append("\n🔄 Related Change Context:")
            for c in related_context["change_contexts"][:2]:
                lines.append(f"  File: {c.get('file_path', '')}")
                lines.append(f"  Summary: {c.get('change_summary', '')[:100]}...")
        
        if not lines:
            return "No related memory found."
        
        return "\n".join(lines)
    
    def _calculate_match_score(
        self,
        text1: str,
        text2: str,
        tags: List[str],
        query_words: set,
        query_lower: str
    ) -> float:
        """
        Calculates a match score between query and content.
        
        Simple keyword-based scoring:
        - Exact phrase matches: high score
        - Multiple keyword matches: medium score
        - Tag matches: medium score
        - Single keyword match: low score
        
        Args:
            text1: First text field (e.g., question/topic)
            text2: Second text field (e.g., answer/explanation)
            tags: List of tags
            query_words: Set of query words
            query_lower: Lowercase query string
            
        Returns:
            Match score (0.0 to 1.0+)
        """
        score = 0.0
        
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        combined_text = f"{text1_lower} {text2_lower}"
        
        # Exact phrase match (highest score)
        if query_lower in combined_text:
            score += 2.0
        
        # Count matching words
        text_words = set(combined_text.split())
        matching_words = query_words & text_words
        
        if matching_words:
            # More matching words = higher score
            score += len(matching_words) * 0.5
        
        # Tag matches
        tag_text = " ".join(tags).lower()
        if any(word in tag_text for word in query_words):
            score += 0.8
        
        # Boost if match is in text1 (title/topic) vs text2 (body)
        if any(word in text1_lower for word in query_words):
            score += 0.5
        
        return score


# Convenience function
def retrieve_related_memory(query: str, file_path: Optional[str] = None) -> Dict:
    """
    Convenience function to retrieve related memory.
    
    Args:
        query: Search query string
        file_path: Optional file path to filter by
        
    Returns:
        Dictionary with related memory items
    """
    retriever = MemoryRetriever()
    return retriever.find_related_context(query, file_path)


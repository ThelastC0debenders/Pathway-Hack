"""
Memory Store - Lightweight JSON-based storage for developer memory.

Stores:
- Past questions and answers
- Past explanations
- Design decisions
- Code change contexts

No embeddings, no vector DB - simple JSON storage.
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class MemoryStore:
    """
    Lightweight memory store using JSON files.
    
    Stores developer memory including past questions, explanations,
    and design decisions for anti-forgetfulness.
    """
    
    def __init__(self, storage_path: str = "./memory_data.json"):
        """
        Initialize the memory store.
        
        Args:
            storage_path: Path to the JSON file for storage
        """
        self.storage_path = Path(storage_path)
        self._ensure_storage_file()
        self._memory = self._load_memory()
    
    def _ensure_storage_file(self):
        """Ensures the storage file exists, creates it if not."""
        if not self.storage_path.exists():
            # Create directory if needed
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            # Initialize with empty structure
            initial_data = {
                "questions": [],
                "explanations": [],
                "design_decisions": [],
                "change_contexts": [],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            }
            with open(self.storage_path, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _load_memory(self) -> Dict:
        """Loads memory from JSON file."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty structure if file is corrupted or missing
            return {
                "questions": [],
                "explanations": [],
                "design_decisions": [],
                "change_contexts": [],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            }
    
    def _save_memory(self):
        """Saves memory to JSON file."""
        self._memory["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.storage_path, 'w') as f:
            json.dump(self._memory, f, indent=2)
    
    def store_question(
        self,
        question: str,
        answer: str,
        context: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Stores a question and its answer.
        
        Args:
            question: The question asked
            answer: The answer provided
            context: Optional context dictionary (file paths, code snippets, etc.)
            tags: Optional tags for categorization
            
        Returns:
            ID of the stored question
        """
        question_id = f"q_{len(self._memory['questions'])}"
        
        entry = {
            "id": question_id,
            "question": question,
            "answer": answer,
            "context": context or {},
            "tags": tags or [],
            "timestamp": datetime.now().isoformat()
        }
        
        self._memory["questions"].append(entry)
        self._save_memory()
        
        return question_id
    
    def store_explanation(
        self,
        topic: str,
        explanation: str,
        related_files: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Stores an explanation for future reference.
        
        Args:
            topic: Topic/subject of the explanation
            explanation: The explanation text
            related_files: Optional list of related file paths
            tags: Optional tags for categorization
            
        Returns:
            ID of the stored explanation
        """
        explanation_id = f"e_{len(self._memory['explanations'])}"
        
        entry = {
            "id": explanation_id,
            "topic": topic,
            "explanation": explanation,
            "related_files": related_files or [],
            "tags": tags or [],
            "timestamp": datetime.now().isoformat()
        }
        
        self._memory["explanations"].append(entry)
        self._save_memory()
        
        return explanation_id
    
    def store_design_decision(
        self,
        decision: str,
        rationale: str,
        alternatives: Optional[List[str]] = None,
        related_files: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Stores a design decision with rationale.
        
        Args:
            decision: Description of the decision made
            rationale: Why this decision was made
            alternatives: Optional list of alternatives considered
            related_files: Optional list of related file paths
            tags: Optional tags for categorization
            
        Returns:
            ID of the stored decision
        """
        decision_id = f"d_{len(self._memory['design_decisions'])}"
        
        entry = {
            "id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "alternatives": alternatives or [],
            "related_files": related_files or [],
            "tags": tags or [],
            "timestamp": datetime.now().isoformat()
        }
        
        self._memory["design_decisions"].append(entry)
        self._save_memory()
        
        return decision_id
    
    def store_change_context(
        self,
        file_path: str,
        change_summary: str,
        change_details: Dict,
        related_questions: Optional[List[str]] = None
    ) -> str:
        """
        Stores context about a code change.
        
        Args:
            file_path: Path to the file that changed
            change_summary: Summary of the change
            change_details: Dictionary with detailed change information
            related_questions: Optional list of question IDs related to this change
            
        Returns:
            ID of the stored change context
        """
        change_id = f"c_{len(self._memory['change_contexts'])}"
        
        entry = {
            "id": change_id,
            "file_path": file_path,
            "change_summary": change_summary,
            "change_details": change_details,
            "related_questions": related_questions or [],
            "timestamp": datetime.now().isoformat()
        }
        
        self._memory["change_contexts"].append(entry)
        self._save_memory()
        
        return change_id
    
    def get_all_questions(self) -> List[Dict]:
        """Returns all stored questions."""
        return self._memory.get("questions", [])
    
    def get_all_explanations(self) -> List[Dict]:
        """Returns all stored explanations."""
        return self._memory.get("explanations", [])
    
    def get_all_design_decisions(self) -> List[Dict]:
        """Returns all stored design decisions."""
        return self._memory.get("design_decisions", [])
    
    def get_all_change_contexts(self) -> List[Dict]:
        """Returns all stored change contexts."""
        return self._memory.get("change_contexts", [])
    
    def get_recent_items(self, limit: int = 10) -> Dict:
        """
        Returns recent items from all categories.
        
        Args:
            limit: Maximum number of items to return per category
            
        Returns:
            Dictionary with recent items from each category
        """
        def get_recent(items: List[Dict], limit: int) -> List[Dict]:
            """Helper to get recent items sorted by timestamp."""
            sorted_items = sorted(
                items,
                key=lambda x: x.get("timestamp", ""),
                reverse=True
            )
            return sorted_items[:limit]
        
        return {
            "questions": get_recent(self._memory.get("questions", []), limit),
            "explanations": get_recent(self._memory.get("explanations", []), limit),
            "design_decisions": get_recent(self._memory.get("design_decisions", []), limit),
            "change_contexts": get_recent(self._memory.get("change_contexts", []), limit)
        }
    
    def search_by_tags(self, tags: List[str]) -> Dict:
        """
        Searches for items matching any of the given tags.
        
        Args:
            tags: List of tags to search for
            
        Returns:
            Dictionary with matching items from each category
        """
        def matches_tags(item: Dict, tags: List[str]) -> bool:
            """Check if item has any of the given tags."""
            item_tags = item.get("tags", [])
            return any(tag in item_tags for tag in tags)
        
        return {
            "questions": [q for q in self._memory.get("questions", []) if matches_tags(q, tags)],
            "explanations": [e for e in self._memory.get("explanations", []) if matches_tags(e, tags)],
            "design_decisions": [d for d in self._memory.get("design_decisions", []) if matches_tags(d, tags)],
            "change_contexts": [c for c in self._memory.get("change_contexts", []) if matches_tags(c, tags)]
        }
    
    def clear_memory(self):
        """Clears all stored memory (use with caution!)."""
        self._memory = {
            "questions": [],
            "explanations": [],
            "design_decisions": [],
            "change_contexts": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        }
        self._save_memory()


# Convenience function for creating a default instance
_default_store: Optional[MemoryStore] = None

def get_default_store(storage_path: str = "./memory_data.json") -> MemoryStore:
    """Gets or creates the default memory store instance."""
    global _default_store
    if _default_store is None:
        _default_store = MemoryStore(storage_path)
    return _default_store

#allthebest
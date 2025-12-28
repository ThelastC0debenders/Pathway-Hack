"""
Change Detector - Detects and explains code changes between two versions.

Uses difflib for text comparison and generates plain-English summaries.
Returns structured JSON for consumption by the Agent layer.
"""

import difflib
import re
from typing import Dict, List, Optional


class ChangeDetector:
    """Detects changes between old and new versions of code files."""
    
    def detect_changes(
        self,
        old_content: str,
        new_content: str,
        file_path: str = "unknown"
    ) -> Dict:
        """
        Compares old and new file content and returns structured change information.
        
        Args:
            old_content: Content of the file in the old version
            new_content: Content of the file in the new version
            file_path: Path to the file being compared (for context)
            
        Returns:
            Dictionary with change information:
            {
                "changed": bool,
                "files_changed": [str],
                "reason": str,
                "change_summary": str,
                "added_lines": int,
                "removed_lines": int,
                "modified_lines": int
            }
        """
        # Normalize line endings
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        # Use difflib to compute differences
        diff = list(difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"{file_path} (old)",
            tofile=f"{file_path} (new)",
            lineterm=''
        ))
        
        if not diff:
            return {
                "changed": False,
                "files_changed": [],
                "reason": "No changes detected",
                "change_summary": "The file content is identical.",
                "added_lines": 0,
                "removed_lines": 0,
                "modified_lines": 0
            }
        
        # Analyze the diff to extract meaningful information
        added_count = 0
        removed_count = 0
        modified_blocks = []
        context_lines = []
        
        # Skip the header lines (---, +++, @@)
        diff_lines = [line for line in diff if not line.startswith(('---', '+++', '@@'))]
        
        for line in diff_lines:
            if line.startswith('+') and not line.startswith('+++'):
                added_count += 1
                # Store context (remove the + prefix)
                context_lines.append(line[1:].strip())
            elif line.startswith('-') and not line.startswith('---'):
                removed_count += 1
                context_lines.append(line[1:].strip())
        
        # Generate plain-English summary
        reason = self._generate_reason(
            old_content,
            new_content,
            added_count,
            removed_count,
            context_lines
        )
        
        change_summary = self._generate_summary(
            file_path,
            added_count,
            removed_count,
            context_lines[:5]  # First 5 lines for context
        )
        
        return {
            "changed": True,
            "files_changed": [file_path],
            "reason": reason,
            "change_summary": change_summary,
            "added_lines": added_count,
            "removed_lines": removed_count,
            "modified_lines": removed_count + added_count  # Approximate
        }
    
    def _generate_reason(
        self,
        old_content: str,
        new_content: str,
        added_lines: int,
        removed_lines: int,
        context_lines: List[str]
    ) -> str:
        """
        Generates a plain-English reason for the changes.
        
        Analyzes the type of changes (functions, imports, logic, etc.)
        and creates a human-readable explanation.
        """
        reasons = []
        
        # Detect function additions/removals
        old_functions = self._extract_functions(old_content)
        new_functions = self._extract_functions(new_content)
        
        added_functions = set(new_functions) - set(old_functions)
        removed_functions = set(old_functions) - set(new_functions)
        
        if added_functions:
            reasons.append(f"Added {len(added_functions)} function(s): {', '.join(list(added_functions)[:3])}")
        if removed_functions:
            reasons.append(f"Removed {len(removed_functions)} function(s): {', '.join(list(removed_functions)[:3])}")
        
        # Detect import changes
        old_imports = self._extract_imports(old_content)
        new_imports = self._extract_imports(new_content)
        
        if old_imports != new_imports:
            added_imports = new_imports - old_imports
            removed_imports = old_imports - new_imports
            if added_imports:
                reasons.append(f"Added imports: {', '.join(list(added_imports)[:3])}")
            if removed_imports:
                reasons.append(f"Removed imports: {', '.join(list(removed_imports)[:3])}")
        
        # Detect class changes
        old_classes = self._extract_classes(old_content)
        new_classes = self._extract_classes(new_content)
        
        added_classes = set(new_classes) - set(old_classes)
        removed_classes = set(old_classes) - set(new_classes)
        
        if added_classes:
            reasons.append(f"Added {len(added_classes)} class(es): {', '.join(list(added_classes)[:2])}")
        if removed_classes:
            reasons.append(f"Removed {len(removed_classes)} class(es): {', '.join(list(removed_classes)[:2])}")
        
        # General statistics
        if not reasons:
            if added_lines > removed_lines:
                reasons.append(f"Code expanded: {added_lines - removed_lines} net new lines")
            elif removed_lines > added_lines:
                reasons.append(f"Code reduced: {removed_lines - added_lines} net removed lines")
            else:
                reasons.append(f"Code modified: {added_lines} lines added, {removed_lines} lines removed")
        
        # Check for logic changes in context
        logic_keywords = ['if', 'elif', 'else', 'for', 'while', 'return', 'raise', 'except']
        if any(keyword in ' '.join(context_lines).lower() for keyword in logic_keywords):
            reasons.append("Logic flow or control structures were modified")
        
        return "; ".join(reasons) if reasons else "Content changed (no specific patterns detected)"
    
    def _generate_summary(
        self,
        file_path: str,
        added_lines: int,
        removed_lines: int,
        sample_lines: List[str]
    ) -> str:
        """Generates a brief summary of changes."""
        summary_parts = [f"File {file_path} was modified."]
        
        if added_lines > 0 or removed_lines > 0:
            summary_parts.append(f"{added_lines} line(s) added, {removed_lines} line(s) removed.")
        
        if sample_lines:
            summary_parts.append("Sample changes include:")
            for line in sample_lines[:3]:
                if line.strip():
                    # Truncate long lines
                    display_line = line[:80] + "..." if len(line) > 80 else line
                    summary_parts.append(f"  - {display_line}")
        
        return " ".join(summary_parts)
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extracts function names from Python code using regex."""
        # Match function definitions: def function_name(...)
        pattern = r'^\s*def\s+(\w+)\s*\('
        functions = re.findall(pattern, content, re.MULTILINE)
        return functions
    
    def _extract_classes(self, content: str) -> List[str]:
        """Extracts class names from Python code using regex."""
        # Match class definitions: class ClassName(...)
        pattern = r'^\s*class\s+(\w+)'
        classes = re.findall(pattern, content, re.MULTILINE)
        return classes
    
    def _extract_imports(self, content: str) -> set:
        """Extracts import statements from Python code."""
        imports = set()
        # Match import statements
        patterns = [
            r'^import\s+([^\s]+)',
            r'^from\s+([^\s]+)\s+import'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            imports.update(matches)
        return imports
    
    def compare_multiple_files(
        self,
        file_changes: Dict[str, Dict[str, str]]
    ) -> Dict:
        """
        Compares multiple files at once.
        
        Args:
            file_changes: Dict mapping file_path to {"old": old_content, "new": new_content}
            
        Returns:
            Combined change information for all files
        """
        all_results = []
        changed_files = []
        
        for file_path, versions in file_changes.items():
            result = self.detect_changes(
                versions.get("old", ""),
                versions.get("new", ""),
                file_path
            )
            all_results.append(result)
            if result["changed"]:
                changed_files.append(file_path)
        
        # Aggregate results
        total_added = sum(r["added_lines"] for r in all_results)
        total_removed = sum(r["removed_lines"] for r in all_results)
        
        # Combine reasons
        reasons = [r["reason"] for r in all_results if r["changed"]]
        combined_reason = "; ".join(set(reasons))  # Deduplicate
        
        return {
            "changed": len(changed_files) > 0,
            "files_changed": changed_files,
            "reason": combined_reason if combined_reason else "No changes detected",
            "change_summary": f"{len(changed_files)} file(s) modified. {total_added} lines added, {total_removed} lines removed.",
            "added_lines": total_added,
            "removed_lines": total_removed,
            "modified_lines": total_added + total_removed,
            "file_details": {r["files_changed"][0] if r["files_changed"] else "unknown": r 
                           for r in all_results if r["changed"]}
        }


# Convenience function for direct use
def detect_changes(old_content: str, new_content: str, file_path: str = "unknown") -> Dict:
    """
    Convenience function to detect changes between two file versions.
    
    Args:
        old_content: Old version of the file
        new_content: New version of the file
        file_path: Path to the file
        
    Returns:
        Dictionary with change information
    """
    detector = ChangeDetector()
    return detector.detect_changes(old_content, new_content, file_path)


"""
Impact Analysis - Analyzes downstream effects of code changes.

Explains:
- Which modules may be affected
- Which docs or behaviors might be outdated
- Who might be impacted (developers/users)

Returns structured JSON for consumption by the Agent layer.
"""

import re
from typing import Dict, List, Set, Optional
from .breaking_change import BreakingChangeDetector
from .change_detector import ChangeDetector


class ImpactAnalyzer:
    """Analyzes the impact of code changes."""
    
    def __init__(self):
        self.change_detector = ChangeDetector()
        self.breaking_detector = BreakingChangeDetector()
    
    def analyze_impact(
        self,
        old_content: str,
        new_content: str,
        file_path: str = "unknown",
        project_structure: Optional[List[str]] = None
    ) -> Dict:
        """
        Analyzes the downstream impact of code changes.
        
        Args:
            old_content: Old version of the code
            new_content: New version of the code
            file_path: Path to the file being analyzed
            project_structure: Optional list of other file paths in the project
            
        Returns:
            Dictionary with impact analysis:
            {
                "impact": [str],  # List of impact descriptions
                "affected_modules": [str],  # Files/modules that may be affected
                "outdated_docs": [str],  # Documentation that may need updates
                "affected_users": [str],  # Who might be impacted
                "recommendations": [str]  # Recommended actions
            }
        """
        impacts = []
        affected_modules = []
        outdated_docs = []
        affected_users = []
        recommendations = []
        
        # First, detect what changed
        change_info = self.change_detector.detect_changes(old_content, new_content, file_path)
        breaking_info = self.breaking_detector.detect_breaking_changes(old_content, new_content, file_path)
        
        # Extract exported functions/classes that might be imported elsewhere
        old_exports = self._extract_exports(old_content)
        new_exports = self._extract_exports(new_content)
        removed_exports = old_exports - new_exports
        changed_exports = self._find_changed_exports(old_content, new_content, old_exports & new_exports)
        
        # 1. Analyze breaking changes impact
        if breaking_info["breaking_change"]:
            impacts.append("Breaking changes detected - may affect dependent code")
            affected_users.append("Developers using this module/API")
            recommendations.append("Update dependent code before deploying")
            recommendations.append("Consider version bump if this is a library")
        
        # 2. Analyze removed exports
        if removed_exports:
            impacts.append(f"Removed {len(removed_exports)} exported item(s): {', '.join(list(removed_exports)[:3])}")
            affected_users.append("Code that imports these items")
            
            # Try to find potential dependents (if project_structure provided)
            if project_structure:
                potential_dependents = self._find_potential_dependents(
                    file_path,
                    removed_exports,
                    project_structure
                )
                affected_modules.extend(potential_dependents)
                if potential_dependents:
                    impacts.append(f"Potentially affects {len(potential_dependents)} dependent file(s)")
        
        # 3. Analyze function signature changes
        if changed_exports:
            impacts.append(f"Signature changes in {len(changed_exports)} exported function(s)")
            affected_users.append("Code calling these functions")
            recommendations.append("Review call sites for compatibility")
        
        # 4. Detect API/public interface changes
        api_changes = self._detect_api_changes(old_content, new_content)
        if api_changes:
            impacts.extend(api_changes)
            affected_users.append("API consumers")
            outdated_docs.append(f"API documentation for {file_path}")
        
        # 5. Detect configuration or constant changes
        config_changes = self._detect_config_changes(old_content, new_content)
        if config_changes:
            impacts.extend(config_changes)
            affected_users.append("Users relying on default configuration")
        
        # 6. Detect error handling changes
        error_changes = self._detect_error_handling_changes(old_content, new_content)
        if error_changes:
            impacts.extend(error_changes)
            affected_users.append("Code handling exceptions from this module")
            recommendations.append("Review error handling in dependent code")
        
        # 7. General recommendations based on change type
        if change_info["added_lines"] > 100:
            recommendations.append("Large change - consider code review and testing")
        if change_info["removed_lines"] > change_info["added_lines"] * 2:
            recommendations.append("Significant code removal - verify functionality is preserved")
        
        # Default impact if nothing specific detected
        if not impacts and change_info["changed"]:
            impacts.append("Code modified - may require testing and review")
            affected_users.append("Developers and QA team")
        
        return {
            "impact": impacts if impacts else ["No significant impact detected"],
            "affected_modules": list(set(affected_modules)) if affected_modules else [],
            "outdated_docs": outdated_docs if outdated_docs else [],
            "affected_users": list(set(affected_users)) if affected_users else ["Developers"],
            "recommendations": recommendations if recommendations else ["Review changes and test"],
            "file": file_path,
            "has_breaking_changes": breaking_info["breaking_change"]
        }
    
    def _extract_exports(self, content: str) -> Set[str]:
        """
        Extracts potentially exported items (functions, classes) from code.
        
        This is a heuristic - looks for top-level definitions.
        """
        exports = set()
        
        # Extract function names (public functions)
        func_pattern = r'^\s*def\s+([a-zA-Z]\w+)\s*\('
        functions = re.findall(func_pattern, content, re.MULTILINE)
        exports.update(functions)
        
        # Extract class names
        class_pattern = r'^\s*class\s+([a-zA-Z]\w+)'
        classes = re.findall(class_pattern, content, re.MULTILINE)
        exports.update(classes)
        
        # Extract constants (UPPER_CASE at module level)
        const_pattern = r'^\s*([A-Z][A-Z0-9_]+)\s*='
        constants = re.findall(const_pattern, content, re.MULTILINE)
        exports.update(constants)
        
        return exports
    
    def _find_changed_exports(
        self,
        old_content: str,
        new_content: str,
        common_exports: Set[str]
    ) -> Set[str]:
        """Finds exports that still exist but have changed signatures."""
        changed = set()
        
        # Extract function signatures for common functions
        old_funcs = self.change_detector._extract_functions(old_content)
        new_funcs = self.change_detector._extract_functions(new_content)
        
        # If a function exists in both, we'll consider it potentially changed
        # More detailed signature comparison is done by breaking_change detector
        for export in common_exports:
            if export in old_funcs and export in new_funcs:
                # Check if signature might have changed (simple heuristic)
                old_sigs = self._get_function_signature_string(old_content, export)
                new_sigs = self._get_function_signature_string(new_content, export)
                if old_sigs != new_sigs:
                    changed.add(export)
        
        return changed
    
    def _get_function_signature_string(self, content: str, func_name: str) -> str:
        """Gets the signature line for a function (for comparison)."""
        pattern = rf'^\s*def\s+{re.escape(func_name)}\s*\((.*?)\)\s*:'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        return match.group(1) if match else ""
    
    def _find_potential_dependents(
        self,
        source_file: str,
        removed_exports: Set[str],
        project_files: List[str]
    ) -> List[str]:
        """
        Finds files that might depend on the removed exports.
        
        This is a simplified heuristic - looks for imports of the source file
        or direct references to the removed exports.
        """
        dependents = []
        module_name = source_file.replace('/', '.').replace('\\', '.').rstrip('.py')
        
        # Simple heuristic: look for import statements
        # In a real system, you'd parse imports more carefully
        for file_path in project_files:
            if file_path == source_file:
                continue
            
            # This is a placeholder - in reality, you'd need to read the file
            # and check for imports. For now, we return empty list.
            # A real implementation would:
            # 1. Read each file
            # 2. Parse import statements
            # 3. Check if they import from source_file or use removed_exports
            pass
        
        return dependents
    
    def _detect_api_changes(self, old_content: str, new_content: str) -> List[str]:
        """Detects changes to public API (function signatures, return types, etc.)."""
        changes = []
        
        # Look for docstring changes (might indicate API changes)
        old_docstrings = len(re.findall(r'""".*?"""', old_content, re.DOTALL))
        new_docstrings = len(re.findall(r'""".*?"""', new_content, re.DOTALL))
        
        if old_docstrings != new_docstrings:
            changes.append("Documentation/docstrings were modified")
        
        # Look for type hints changes (simplified)
        old_type_hints = len(re.findall(r'->\s*\w+', old_content))
        new_type_hints = len(re.findall(r'->\s*\w+', new_content))
        
        if old_type_hints != new_type_hints:
            changes.append("Type hints were added, removed, or modified")
        
        return changes
    
    def _detect_config_changes(self, old_content: str, new_content: str) -> List[str]:
        """Detects changes to configuration or constants."""
        changes = []
        
        # Look for constant definitions (UPPER_CASE)
        old_constants = set(re.findall(r'^\s*([A-Z][A-Z0-9_]+)\s*=', old_content, re.MULTILINE))
        new_constants = set(re.findall(r'^\s*([A-Z][A-Z0-9_]+)\s*=', new_content, re.MULTILINE))
        
        removed_constants = old_constants - new_constants
        added_constants = new_constants - old_constants
        
        if removed_constants:
            changes.append(f"Removed constant(s): {', '.join(list(removed_constants)[:3])}")
        if added_constants:
            changes.append(f"Added constant(s): {', '.join(list(added_constants)[:3])}")
        
        return changes
    
    def _detect_error_handling_changes(
        self,
        old_content: str,
        new_content: str
    ) -> List[str]:
        """Detects changes to error handling (exceptions raised, etc.)."""
        changes = []
        
        # Count raise statements
        old_raises = len(re.findall(r'\braise\s+', old_content))
        new_raises = len(re.findall(r'\braise\s+', new_content))
        
        if old_raises != new_raises:
            if new_raises > old_raises:
                changes.append("Additional exceptions may be raised")
            else:
                changes.append("Exception handling was modified")
        
        # Look for exception type changes (simplified)
        old_exceptions = set(re.findall(r'\braise\s+(\w+Exception|\w+Error)', old_content))
        new_exceptions = set(re.findall(r'\braise\s+(\w+Exception|\w+Error)', new_content))
        
        if old_exceptions != new_exceptions:
            changes.append("Exception types changed")
        
        return changes


# Convenience function
def analyze_impact(
    old_content: str,
    new_content: str,
    file_path: str = "unknown",
    project_structure: Optional[List[str]] = None
) -> Dict:
    """
    Convenience function to analyze impact of changes.
    
    Args:
        old_content: Old version of the code
        new_content: New version of the code
        file_path: Path to the file
        project_structure: Optional list of project files
        
    Returns:
        Dictionary with impact analysis
    """
    analyzer = ImpactAnalyzer()
    return analyzer.analyze_impact(old_content, new_content, file_path, project_structure)


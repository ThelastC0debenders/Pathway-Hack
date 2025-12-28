"""
Breaking Change Detector - Detects potential breaking changes in code.

Uses regex and simple AST parsing to detect:
- Function signature changes
- Removed/renamed functions
- Behavior-altering logic changes

Returns structured JSON for consumption by the Agent layer.
"""

import re
import ast
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class FunctionSignature:
    """Represents a function signature."""
    name: str
    args: List[str]  # Parameter names
    defaults_count: int  # Number of parameters with defaults
    varargs: bool  # Has *args
    kwargs: bool  # Has **kwargs
    line_number: int


class BreakingChangeDetector:
    """Detects potential breaking changes in code."""
    
    def detect_breaking_changes(
        self,
        old_content: str,
        new_content: str,
        file_path: str = "unknown"
    ) -> Dict:
        """
        Detects potential breaking changes between old and new code.
        
        Args:
            old_content: Old version of the code
            new_content: New version of the code
            file_path: Path to the file being analyzed
            
        Returns:
            Dictionary with breaking change information:
            {
                "breaking_change": bool,
                "details": str,
                "severity": str,  # "high", "medium", "low"
                "changes": [
                    {
                        "type": str,  # "function_removed", "signature_changed", etc.
                        "description": str,
                        "location": str
                    }
                ]
            }
        """
        changes = []
        
        # Extract function signatures from both versions
        old_functions = self._extract_function_signatures(old_content)
        new_functions = self._extract_function_signatures(new_content)
        
        old_func_names = {f.name for f in old_functions}
        new_func_names = {f.name for f in new_functions}
        
        # 1. Detect removed functions
        removed_functions = old_func_names - new_func_names
        for func_name in removed_functions:
            changes.append({
                "type": "function_removed",
                "description": f"Function '{func_name}' was removed",
                "location": file_path,
                "severity": "high"
            })
        
        # 2. Detect renamed functions (heuristic: same signature, different name)
        # This is a simple heuristic - might have false positives
        # We'll check if a function disappeared and a new similar one appeared
        added_functions = new_func_names - old_func_names
        
        # 3. Detect signature changes for existing functions
        old_func_dict = {f.name: f for f in old_functions}
        new_func_dict = {f.name: f for f in new_functions}
        
        for func_name in old_func_names & new_func_names:
            old_sig = old_func_dict[func_name]
            new_sig = new_func_dict[func_name]
            
            sig_changes = self._compare_signatures(old_sig, new_sig)
            if sig_changes:
                changes.append({
                    "type": "signature_changed",
                    "description": f"Function '{func_name}' signature changed: {sig_changes}",
                    "location": f"{file_path}:{new_sig.line_number}",
                    "severity": "high"
                })
        
        # 4. Detect removed classes
        old_classes = self._extract_classes(old_content)
        new_classes = self._extract_classes(new_content)
        removed_classes = old_classes - new_classes
        
        for class_name in removed_classes:
            changes.append({
                "type": "class_removed",
                "description": f"Class '{class_name}' was removed",
                "location": file_path,
                "severity": "high"
            })
        
        # 5. Detect removed public attributes/methods (heuristic)
        removed_public_attrs = self._detect_removed_public_attributes(old_content, new_content)
        changes.extend(removed_public_attrs)
        
        # Determine overall breaking change status
        has_breaking_change = len(changes) > 0
        severity = "high" if any(c.get("severity") == "high" for c in changes) else \
                  "medium" if any(c.get("severity") == "medium" for c in changes) else \
                  "low" if changes else "none"
        
        details = "; ".join([c["description"] for c in changes]) if changes else "No breaking changes detected"
        
        return {
            "breaking_change": has_breaking_change,
            "details": details,
            "severity": severity,
            "changes": changes,
            "file": file_path
        }
    
    def _extract_function_signatures(self, content: str) -> List[FunctionSignature]:
        """
        Extracts function signatures from Python code.
        
        Uses both AST parsing (preferred) and regex fallback.
        """
        functions = []
        
        # Try AST parsing first (more accurate)
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    defaults_count = len(node.args.defaults)
                    varargs = node.args.vararg is not None
                    kwargs = node.args.kwarg is not None
                    
                    functions.append(FunctionSignature(
                        name=node.name,
                        args=args,
                        defaults_count=defaults_count,
                        varargs=varargs,
                        kwargs=kwargs,
                        line_number=node.lineno
                    ))
        except SyntaxError:
            # Fallback to regex if AST parsing fails
            functions = self._extract_functions_regex(content)
        
        return functions
    
    def _extract_functions_regex(self, content: str) -> List[FunctionSignature]:
        """Fallback regex-based function extraction."""
        functions = []
        lines = content.split('\n')
        
        # Pattern: def function_name(param1, param2=default, *args, **kwargs):
        pattern = r'^\s*def\s+(\w+)\s*\((.*?)\)\s*:'
        
        for i, line in enumerate(lines, 1):
            match = re.match(pattern, line)
            if match:
                func_name = match.group(1)
                params_str = match.group(2)
                
                # Parse parameters (simple heuristic)
                if params_str.strip():
                    params = [p.strip().split('=')[0].strip() for p in params_str.split(',')]
                    defaults_count = params_str.count('=')
                    varargs = '*args' in params_str or '*args,' in params_str
                    kwargs = '**kwargs' in params_str or '**kwargs,' in params_str
                    
                    # Clean up params (remove * and **)
                    params = [p.replace('*', '').replace('**', '') for p in params if p]
                else:
                    params = []
                    defaults_count = 0
                    varargs = False
                    kwargs = False
                
                functions.append(FunctionSignature(
                    name=func_name,
                    args=params,
                    defaults_count=defaults_count,
                    varargs=varargs,
                    kwargs=kwargs,
                    line_number=i
                ))
        
        return functions
    
    def _compare_signatures(
        self,
        old_sig: FunctionSignature,
        new_sig: FunctionSignature
    ) -> Optional[str]:
        """
        Compares two function signatures and returns description of changes.
        
        Returns None if signatures are compatible, otherwise a description string.
        """
        changes = []
        
        # Check if required parameters changed (parameters without defaults)
        old_required = len(old_sig.args) - old_sig.defaults_count
        new_required = len(new_sig.args) - new_sig.defaults_count
        
        if new_required > old_required:
            changes.append(f"added {new_required - old_required} required parameter(s)")
        
        # Check if parameters were removed (excluding those with defaults)
        if len(old_sig.args) > len(new_sig.args):
            removed_params = old_sig.args[len(new_sig.args):]
            changes.append(f"removed parameter(s): {', '.join(removed_params)}")
        
        # Check if parameter order changed (simplified check)
        common_params = set(old_sig.args) & set(new_sig.args)
        if common_params and old_sig.args[:len(common_params)] != new_sig.args[:len(common_params)]:
            changes.append("parameter order changed")
        
        # Check varargs/kwargs changes
        if old_sig.varargs and not new_sig.varargs:
            changes.append("removed *args")
        if old_sig.kwargs and not new_sig.kwargs:
            changes.append("removed **kwargs")
        
        return "; ".join(changes) if changes else None
    
    def _extract_classes(self, content: str) -> Set[str]:
        """Extracts class names from Python code."""
        classes = set()
        
        # Try AST first
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.add(node.name)
        except SyntaxError:
            # Fallback to regex
            pattern = r'^\s*class\s+(\w+)'
            matches = re.findall(pattern, content, re.MULTILINE)
            classes.update(matches)
        
        return classes
    
    def _detect_removed_public_attributes(
        self,
        old_content: str,
        new_content: str
    ) -> List[Dict]:
        """
        Detects removed public attributes/methods using simple heuristics.
        
        This is a simplified check - looks for public methods/attributes
        (those not starting with _) that appear in old but not new.
        """
        changes = []
        
        # Extract public method definitions (def method_name, not def _private)
        old_pattern = r'^\s*def\s+([a-zA-Z]\w+)\s*\('
        old_methods = set(re.findall(old_pattern, old_content, re.MULTILINE))
        new_methods = set(re.findall(old_pattern, new_content, re.MULTILINE))
        
        removed_methods = old_methods - new_methods
        for method in removed_methods:
            changes.append({
                "type": "method_removed",
                "description": f"Public method '{method}' was removed",
                "location": "unknown",
                "severity": "medium"
            })
        
        return changes


# Convenience function
def detect_breaking_changes(old_content: str, new_content: str, file_path: str = "unknown") -> Dict:
    """
    Convenience function to detect breaking changes.
    
    Args:
        old_content: Old version of the code
        new_content: New version of the code
        file_path: Path to the file
        
    Returns:
        Dictionary with breaking change information
    """
    detector = BreakingChangeDetector()
    return detector.detect_breaking_changes(old_content, new_content, file_path)


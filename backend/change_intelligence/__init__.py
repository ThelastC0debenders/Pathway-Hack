"""
Change Intelligence Module

Provides change detection, breaking change analysis, and impact analysis.
"""

from .change_detector import ChangeDetector, detect_changes
from .breaking_change import BreakingChangeDetector, detect_breaking_changes
from .impact_analysis import ImpactAnalyzer, analyze_impact


def analyze_code_changes(
    old_content: str,
    new_content: str,
    file_path: str = "unknown",
    project_structure: list = None
) -> dict:
    """
    Combined analysis function that runs all change intelligence checks.
    
    This is the main entry point for the Agent layer to get complete
    change intelligence information in one structured response.
    
    Args:
        old_content: Old version of the file content
        new_content: New version of the file content
        file_path: Path to the file being analyzed
        project_structure: Optional list of other files in the project
        
    Returns:
        Combined dictionary with all change intelligence information:
        {
            "changed": bool,
            "files_changed": [str],
            "reason": str,
            "breaking_change": bool,
            "breaking_details": str,
            "severity": str,
            "impact": [str],
            "affected_modules": [str],
            "outdated_docs": [str],
            "affected_users": [str],
            "recommendations": [str],
            "change_summary": str,
            "added_lines": int,
            "removed_lines": int
        }
    """
    # Run all analyses
    change_detector = ChangeDetector()
    breaking_detector = BreakingChangeDetector()
    impact_analyzer = ImpactAnalyzer()
    
    change_info = change_detector.detect_changes(old_content, new_content, file_path)
    breaking_info = breaking_detector.detect_breaking_changes(old_content, new_content, file_path)
    impact_info = impact_analyzer.analyze_impact(
        old_content, new_content, file_path, project_structure
    )
    
    # Combine results
    return {
        "changed": change_info["changed"],
        "files_changed": change_info["files_changed"],
        "reason": change_info["reason"],
        "breaking_change": breaking_info["breaking_change"],
        "breaking_details": breaking_info["details"],
        "severity": breaking_info["severity"],
        "impact": impact_info["impact"],
        "affected_modules": impact_info["affected_modules"],
        "outdated_docs": impact_info["outdated_docs"],
        "affected_users": impact_info["affected_users"],
        "recommendations": impact_info["recommendations"],
        "change_summary": change_info["change_summary"],
        "added_lines": change_info["added_lines"],
        "removed_lines": change_info["removed_lines"],
        "file": file_path
    }


__all__ = [
    "ChangeDetector",
    "detect_changes",
    "BreakingChangeDetector",
    "detect_breaking_changes",
    "ImpactAnalyzer",
    "analyze_impact",
    "analyze_code_changes",
]

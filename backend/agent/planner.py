class Plan:
    def __init__(self, strategy, tools_needed, reasoning, confidence_threshold):
        self.strategy = strategy
        self.tools_needed = tools_needed
        self.reasoning = reasoning
        self.confidence_threshold = confidence_threshold


class Planner:
    def plan(self, query: str, context: str, metadata: dict) -> Plan:
        quality = metadata.get("context_quality", "limited")

        if quality == "limited":
            return Plan("uncertain", ["express_uncertainty"], "Context limited", 0.4)

        if "summary" or "summarize" in query.lower():
            return Plan("summarize", ["extract_key_points"], "Summary requested", 0.7)

        if "change" in query.lower() or "changed" in query.lower() or "difference" in query.lower():
            return Plan("explain_change", ["extract_changes", "analyze_code_changes", "detect_breaking_changes", "analyze_impact"], "Change explanation with intelligence", 0.75)
        
        if "breaking" in query.lower() or "break" in query.lower():
            return Plan("detect_breaking", ["detect_breaking_changes", "analyze_impact"], "Breaking change detection", 0.75)
        
        if "impact" in query.lower() or "affect" in query.lower() or "downstream" in query.lower():
            return Plan("impact_analysis", ["analyze_impact"], "Impact analysis", 0.75)

        return Plan("direct", [], "Direct answer", 0.8)

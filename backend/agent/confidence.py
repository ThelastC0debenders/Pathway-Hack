class ConfidenceResult:
    def __init__(self, score, level, reasoning, should_hedge, factors):
        self.score = score
        self.level = level
        self.reasoning = reasoning
        self.should_hedge = should_hedge
        self.factors = factors


class ConfidenceAssessor:
    def assess(self, query, context, answer, metadata):
        score = min(len(context) / 1500, 1.0)
        level = "high" if score > 0.8 else "medium" if score > 0.5 else "low"

        return ConfidenceResult(
            score,
            level,
            "Based on context coverage",
            level != "high",
            {"context": score}
        )

    def get_hedge_phrase(self, level):
        return "I might be mistaken, but " if level != "high" else ""

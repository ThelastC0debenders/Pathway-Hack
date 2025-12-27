def estimate_confidence(answer: str) -> float:
    if len(answer) > 300:
        return 0.9
    if len(answer) > 100:
        return 0.7
    return 0.5

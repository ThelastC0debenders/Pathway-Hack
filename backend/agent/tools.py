class Tools:
    def summarize(self, text: str, max_length: int):
        return text[:max_length] + "..." if len(text) > max_length else text

    def extract_key_points(self, text: str, num_points: int):
        lines = [l for l in text.split("\n") if l.strip()]
        return lines[:num_points]

    def extract_changes(self, text: str):
        changes = []
        for line in text.split("\n"):
            if line.startswith("+"):
                changes.append({"type": "add", "file": "unknown"})
            elif line.startswith("-"):
                changes.append({"type": "remove", "file": "unknown"})
        return changes

    def compare_versions(self, old: str, new: str):
        return "Differences detected" if old != new else "No differences"

    def express_uncertainty(self, query: str, context: str, reason: str):
        return f"I may be mistaken, but {reason.lower()}.\n\n"

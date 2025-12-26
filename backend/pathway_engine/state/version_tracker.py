from pathway_engine.indexing.embeddings import content_hash


class VersionTracker:
    def __init__(self):
        self.latest_hash = None

    def update(self, content: str) -> bool:
        h = content_hash(content)
        changed = h != self.latest_hash
        self.latest_hash = h
        return changed

    def get_version(self):
        return self.latest_hash

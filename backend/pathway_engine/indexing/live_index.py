from pathway_engine.indexing.embeddings import content_hash
class LiveIndex:
    def __init__(self):
        self.store = {}

    def update(self, content: str):
        self.store[content_hash(content)] = content

    def all(self):
        return list(self.store.values())


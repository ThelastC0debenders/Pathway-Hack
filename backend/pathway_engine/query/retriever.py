from typing import List, Dict
import time

class LiveRetriever:
    def __init__(self, live_table):
        self.live_table = live_table

    def fetch_documents(self):
        rows = self.live_table.snapshot()  # 👈 correct
        docs = []

        for r in rows:
            docs.append({
                "content": r["content"],
                "source": r.get("path", "unknown"),
            })

        return docs

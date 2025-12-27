from typing import List, Dict
import time

class LiveRetriever:
    def __init__(self, live_table):
        """
        live_table: Pathway table from Person-1
        """
        self.live_table = live_table

    def fetch_documents(self) -> List[Dict]:
        """
        Convert Pathway rows into simple documents.
        """
        docs = []

        for row in self.live_table.to_pandas().itertuples():
            docs.append({
                "content": row.content,
                "source": getattr(row, "path", "unknown"),
                "timestamp": int(time.time())
            })

        return docs

from typing import List, Dict
import pathway as pw
import time

class LiveRetriever:
    def __init__(self, live_table):
        self.live_table = live_table

    def fetch_documents(self):
        df = pw.debug.table_to_pandas(self.live_table)
        rows = df.to_dict(orient="records")
        docs = []

        for r in rows:
            print(f"DEBUG: Processing row: {r}")
            docs.append({
                "content": r["content"],
                "source": r.get("path", "unknown"),
            })

        return docs

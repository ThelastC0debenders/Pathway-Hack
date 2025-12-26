import hashlib
from typing import List


def content_hash(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8", errors="ignore")
    ).hexdigest()


def embed_text(text: str) -> List[float]:
    h = int(content_hash(text), 16)
    return [(h >> i) & 1 for i in range(128)]

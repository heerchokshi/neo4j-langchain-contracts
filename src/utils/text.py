import re
from typing import List

def simple_clause_split(text: str) -> List[str]:
    if not text:
        return []
    text = re.sub(r'\r\n?', '\n', text)
    parts = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    if len(parts) < 3:
        parts = re.split(r'(?<=[.!?])\s+(?=[A-Z(])', text)
        parts = [p.strip() for p in parts if p.strip()]
    return parts
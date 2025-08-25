"""
Optional helper to quickly ingest a few CUAD samples.
Usage:
  python -m src.data.cuad_loader
"""
from datasets import load_dataset

def sample_cuad(n=5):
    ds = load_dataset("cuad")
    out = []
    for i, ex in enumerate(ds["train"]):
        if i >= n:
            break
        # Use 'text' if present, otherwise join available fields
        text = ex.get("text") or ex.get("question_text") or ""
        if not text:
            continue
        out.append(text)
    return out

if __name__ == "__main__":
    for t in sample_cuad(3):
        print("---")
        print(t[:500], "...")
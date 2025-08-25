from typing import List, Dict
from transformers import pipeline
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from src.config import HF_API_TOKEN, HF_SUMMARIZATION_MODEL

# Summarization via HF endpoint
def get_summarization_chain():
    if not HF_API_TOKEN:
        raise ValueError("HF_API_TOKEN is not set. Add it to .env")

    llm = HuggingFaceEndpoint(
        repo_id=HF_SUMMARIZATION_MODEL,
        task="summarization",
        temperature=0.1,
        huggingfacehub_api_token=HF_API_TOKEN,
        max_new_tokens=220
    )

    template = """You are a helpful assistant. Summarize the following contract text in plain English, focusing on obligations, risks, and key terms.

TEXT:
{contract_text}

SUMMARY:"""
    prompt = PromptTemplate.from_template(template)
    return prompt | llm

# Zero-shot classification (local)
_ZS_MODEL = "facebook/bart-large-mnli"
_CANDIDATE_LABELS = [
    "Confidentiality", "Liability", "Termination", "Payment", "Governing Law",
    "Intellectual Property", "Assignment", "Warranties", "Indemnification",
    "Limitation of Liability", "Privacy", "Data Protection", "Non-Compete",
    "Non-Solicitation", "Dispute Resolution", "Force Majeure"
]
_zs = None

def _get_zs():
    global _zs
    if _zs is None:
        _zs = pipeline("zero-shot-classification", model=_ZS_MODEL)
    return _zs

def classify_clauses_zero_shot(clauses: List[str]) -> List[Dict]:
    clf = _get_zs()
    res = []
    for c in clauses:
        out = clf(c, candidate_labels=_CANDIDATE_LABELS, multi_label=False)
        res.append({"clause": c, "label": out["labels"][0], "score": float(out["scores"][0])})
    return res
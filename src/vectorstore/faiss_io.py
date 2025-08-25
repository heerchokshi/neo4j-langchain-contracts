import os
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from src.llm.embeddings import get_embeddings
from src.config import FAISS_DIR

def ensure_dir():
    os.makedirs(FAISS_DIR, exist_ok=True)

def create_or_load_faiss() -> FAISS:
    ensure_dir()
    if os.path.exists(os.path.join(FAISS_DIR, "index.faiss")):
        return FAISS.load_local(FAISS_DIR, get_embeddings(), allow_dangerous_deserialization=True)
    return None

def save_faiss(store: FAISS):
    ensure_dir()
    store.save_local(FAISS_DIR)

def add_documents(store: FAISS | None, docs: List[Document]) -> FAISS:
    if store is None:
        store = FAISS.from_documents(docs, get_embeddings())
    else:
        store.add_documents(docs)
    save_faiss(store)
    return store
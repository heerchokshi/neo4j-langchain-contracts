from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from langchain.docstore.document import Document

from src.llm.chains import get_summarization_chain, classify_clauses_zero_shot
from src.graph.neo4j_client import Neo4jClient
from src.utils.text import simple_clause_split
from src.vectorstore.faiss_io import create_or_load_faiss, add_documents
from src.config import API_HOST, API_PORT

app = FastAPI(title="Contracts LLM + Neo4j API")

_vectorstore = create_or_load_faiss()
_graph = Neo4jClient()
_graph.init_schema()

class IngestRequest(BaseModel):
    contract_id: str
    contract_text: str

class SummarizeRequest(BaseModel):
    text: str

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(req: IngestRequest):
    global _vectorstore
    if not req.contract_text.strip():
        raise HTTPException(status_code=400, detail="Empty contract_text")

    clauses = simple_clause_split(req.contract_text)
    if not clauses:
        raise HTTPException(status_code=400, detail="Could not split into clauses")

    labeled = classify_clauses_zero_shot(clauses)
    _graph.create_contract_with_clauses(req.contract_id, labeled)

    docs = [Document(page_content=it["clause"],
                     metadata={"label": it["label"], "contract_id": req.contract_id})
            for it in labeled]

    _vectorstore = add_documents(_vectorstore, docs)
    return {"contract_id": req.contract_id, "num_clauses": len(clauses), "labels_preview": labeled[:3]}

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")
    chain = get_summarization_chain()
    summary = chain.invoke({"contract_text": req.text})
    return {"summary": str(summary)}

@app.post("/ask")
def ask(req: AskRequest):
    global _vectorstore
    if _vectorstore is None:
        raise HTTPException(status_code=400, detail="Vector store empty. Ingest a contract first.")

    retriever = _vectorstore.as_retriever(search_kwargs={"k": req.top_k})
    docs = retriever.get_relevant_documents(req.question)
    if not docs:
        return {"answer": "No relevant context found.", "context_count": 0}

    context = "\n\n".join([f"[{i+1}] {d.page_content}" for i, d in enumerate(docs)])
    prompt = f"""You are a contract analyst. Using only the CONTEXT below, answer the QUESTION concisely.
CONTEXT:
{context}

QUESTION: {req.question}
ANSWER:"""

    chain = get_summarization_chain()
    answer = chain.invoke({"contract_text": prompt})
    return {"answer": str(answer), "context_count": len(docs)}
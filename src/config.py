import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_SUMMARIZATION_MODEL = os.getenv("HF_SUMMARIZATION_MODEL", "facebook/bart-large-cnn")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

DEVICE = os.getenv("DEVICE", "cpu")  # 'cpu' or 'mps'
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

FAISS_DIR = os.getenv("FAISS_DIR", "faiss_index")
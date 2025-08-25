from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBEDDINGS_MODEL

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
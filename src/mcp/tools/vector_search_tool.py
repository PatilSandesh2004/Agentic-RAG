from src.vectorstore.milvus_client import MilvusClient
from src.llm.gemini_client import embed_texts


def vector_search_tool(query: str, top_k: int = 5):
    """
    Search vector database for relevant chunks.
    """
    embedding = embed_texts([query])[0]
    milvus = MilvusClient()
    return milvus.search(embedding, top_k)

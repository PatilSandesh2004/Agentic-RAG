from src.ingestion.loader import load_document
from src.ingestion.chunker import semantic_chunk_text
from src.llm.gemini_client import embed_texts
from src.vectorstore.milvus_client import MilvusClient


def ingest_tool(file_path: str, document_name: str):
    """
    Ingest document into vector DB (overwrite mode).
    """
    text = load_document(file_path)

    if not text.strip():
        return {"status": "failed", "reason": "No text extracted"}

    chunks = semantic_chunk_text(text)
    embeddings = embed_texts(chunks)

    milvus = MilvusClient()
    milvus.reset_collection()   # overwrite old document
    milvus.insert(embeddings, chunks)

    return {
        "status": "success",
        "document_name": document_name,
        "chunks_ingested": len(chunks),
    }

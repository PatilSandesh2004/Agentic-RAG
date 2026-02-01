from src.ingestion.preocr import analyze_document

from src.ingestion.loader import load_document
from src.ingestion.chunker import chunk_text
from src.llm.gemini_client import embed_texts
from src.vectorstore.milvus_client import MilvusClient


def ingest_file(file_path: str):
    """
    Ingest a single document into Milvus.
    """

    # 1. PreOCR decision
    decision = analyze_document(file_path)
    print(f"[PreOCR] {decision}")

    if decision.get("needs_ocr"):
        raise RuntimeError("OCR required but OCR execution is not implemented.")

    # 2. Load document text
    text = load_document(file_path)

    # 3. Chunk text
    chunks = chunk_text(text)
    print(f"[Chunking] Created {len(chunks)} chunks")

    if not chunks:
        raise RuntimeError("No text chunks generated")

    # 4. Generate embeddings
    embeddings = embed_texts(chunks)
    print("[Embedding] Embeddings generated")

    # 5. Store in Milvus
    milvus = MilvusClient()
    milvus.insert(embeddings, chunks)
    print("[Milvus] Data inserted successfully")


if __name__ == "__main__":
    ingest_file("data/samples/sample.txt")

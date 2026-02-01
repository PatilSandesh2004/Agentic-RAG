from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid
from pydantic import BaseModel

from src.ingestion.preocr import analyze_document
from src.ingestion.loader import load_document
from src.ingestion.chunker import semantic_chunk_text
from src.llm.gemini_client import embed_texts
from src.vectorstore.milvus_client import MilvusClient
from src.Query.query_engine import answer_question
from src.utils.logger import logger


# -------------------------------------------------
# App setup
# -------------------------------------------------
app = FastAPI(title="Agentic RAG API (Overwrite Mode)")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# Ingest Endpoint (OVERWRITE MODE)
# -------------------------------------------------
@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    """
    Upload a document.
    This DROPS the previous document and replaces it.
    """

    ext = Path(file.filename).suffix.lower()
    # if ext not in [".txt", ".pdf", ".docx",".pptx"]:
    #     raise HTTPException(status_code=400, detail="Unsupported file type")

    if ext not in [
    ".txt", ".md",
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx", ".xls",
    ".csv",
    ".html", ".htm",
]:
        raise HTTPException(status_code=400, detail="Unsupported file type")



    file_id = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / file_id

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    logger.info(f"INGEST STARTED | file={file.filename}")

    # PreOCR (agentic decision)
    preocr = analyze_document(str(file_path))

    # Load text
    text = load_document(str(file_path))
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text extracted")

    # Semantic chunking + overlap
    chunks = semantic_chunk_text(text)

    for i, chunk in enumerate(chunks, start=1):
        logger.info(f"[INGESTED CHUNK {i}]\n{chunk}")

    # Embeddings
    embeddings = embed_texts(chunks)

    # 🔥 OVERWRITE MODE
    milvus = MilvusClient()
    milvus.reset_collection()

    milvus.insert(
        embeddings=embeddings,
        texts=chunks,
        document_id=file_id,
        document_name=file.filename,
    )

    logger.info(
        f"INGEST COMPLETED | file={file.filename} | chunks={len(chunks)}"
    )

    return {
        "status": "success",
        "active_document": file.filename,
        "chunks_ingested": len(chunks),
        "needs_ocr": preocr.get("needs_ocr"),
        "reason_code": preocr.get("reason_code"),
        "mode": "overwrite",
    }


# -------------------------------------------------
# Query Endpoint
# -------------------------------------------------
class QueryRequest(BaseModel):
    question: str


@app.post("/query")
async def query_rag(request: QueryRequest):
    """
    Ask a question about the CURRENT document only.
    """

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer,
    }


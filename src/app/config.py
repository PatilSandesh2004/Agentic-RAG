import os
from dotenv import load_dotenv

load_dotenv()

def require(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is required but not set.")
    return value


class Settings:

   

    # -------- LLM (Generation) --------
    LLM_PROVIDER = require("LLM_PROVIDER")
    GROQ_MODEL = require("GROQ_MODEL")

    # -------- Embeddings --------
    EMBEDDING_PROVIDER = require("EMBEDDING_PROVIDER")
    EMBEDDING_MODEL = require("EMBEDDING_MODEL")

    # -------- Vector Database --------
    VECTOR_DB = require("VECTOR_DB")
    MILVUS_URI = require("MILVUS_URI")
    MILVUS_TOKEN = require("MILVUS_TOKEN")
    MILVUS_COLLECTION = os.getenv("MILVUS_COLLECTION", "documents")

    # -------- Agent Settings --------
    TOP_K = int(os.getenv("TOP_K", "5"))
    MAX_AGENT_RETRIES = int(os.getenv("MAX_AGENT_RETRIES", "1"))

    GROQ_API_KEY = require("GROQ_API_KEY")
    # -------- PreOCR --------
    ENABLE_PREOCR = os.getenv("ENABLE_PREOCR", "true").lower() == "true"
    PREOCR_PAGE_LEVEL = os.getenv("PREOCR_PAGE_LEVEL", "true").lower() == "true"
    PREOCR_LAYOUT_AWARE = os.getenv("PREOCR_LAYOUT_AWARE", "true").lower() == "true"

    # -------- Embeddings --------
    EMBEDDING_PROVIDER = require("EMBEDDING_PROVIDER")
    EMBEDDING_MODEL = require("EMBEDDING_MODEL")
    GEMINI_API_KEY = require("GEMINI_API_KEY")


# Singleton settings object
settings = Settings()
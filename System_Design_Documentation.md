# Agentic-RAG System Documentation

## 1. System Architecture

The Agentic-RAG system is designed as a modular, agent-driven Retrieval-Augmented Generation (RAG) platform. The architecture consists of the following main components:

- **UI Layer**: Streamlit-based chat interface for document upload and conversational querying.
- **API Layer**: FastAPI backend (`src/api/main.py`) exposes endpoints for document ingestion and querying.
- **Agent Layer**: Orchestrates workflows using MCP tools and LLMs.
- **MCP (Model Context Protocol)**: Modular tool registry (`src/mcp/registry.py`) and server (`src/mcp/server.py`) for document processing, vector search, and pre-OCR checks.
- **Ingestion Pipeline**: Handles document loading, chunking, embedding, and storage in vector DB (Milvus).
- **LLM Layer**: Integrates Gemini and Groq clients for embedding and answering queries.
- **Vector Store**: Milvus client for semantic search and retrieval.
- **Utils**: Logging and configuration utilities.

```
[User]
   |
[Streamlit UI] <--> [FastAPI API]
   |                    |
   |                [Agent Layer]
   |                    |
   |                [MCP Tools]
   |                    |
   |                [Ingestion/LLM/VectorStore]
   |                    |
   |                [Milvus DB]
```

## 2. Agentic Workflow Design

- **Document Upload**: User uploads a document via UI → API endpoint `/ingest` → Agent triggers MCP tools for pre-OCR, ingestion, chunking, embedding, and storage.
- **Query**: User submits a question → API endpoint `/query` → Agent retrieves context from vector DB using semantic search → LLM generates answer → Response returned to UI.
- **Tool Registry**: MCP registry maps tool names to implementations, enabling flexible orchestration.

## 3. Context Construction Strategy

- **Chunking**: Documents are split into semantic chunks for efficient retrieval.
- **Embedding**: Chunks are embedded using LLMs (Gemini/Groq) for vector search.
- **Retrieval**: Queries are embedded and matched against stored vectors in Milvus.
- **Context Assembly**: Top relevant chunks are assembled as context for LLM answer generation.

## 4. Technology Choices & Rationale

- **FastAPI**: High-performance, async API for backend logic.
- **Streamlit**: Rapid prototyping and interactive UI for chat and document upload.
- **Milvus**: Scalable vector database for semantic search.
- **Gemini/Groq**: Advanced LLMs for embedding and answer generation.
- **MCP**: Modular tool orchestration for extensibility and maintainability.

## 5. Key Design Decisions

- **Agentic Orchestration**: Central agent coordinates all workflows, enabling modularity and future extensibility.
- **Tool Registry**: MCP registry allows easy addition/replacement of tools.
- **Separation of Concerns**: UI, API, agent, and tool layers are decoupled for clarity and scalability.
- **Semantic Chunking**: Improves retrieval accuracy and LLM context relevance.

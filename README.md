# Agentic-RAG

## Overview
Agentic-RAG is a modular Retrieval-Augmented Generation (RAG) system that lets you upload documents and chat with them using advanced LLMs and semantic search. It is designed for extensibility, clarity, and agentic orchestration.

---

## System Components

### 1. Streamlit UI
- Chatbot interface for document upload and conversational querying.
- Sidebar for document management and chat clearing.

### 2. FastAPI Backend
- Exposes `/ingest` (document upload) and `/query` (question answering) endpoints.
- Handles file saving, chunking, embedding, and vector DB operations.

### 3. Agent Layer
- Orchestrates workflows using MCP tools and LLMs.
- Decides which tool to use for each step (preOCR, ingest, search, answer).

### 4. MCP (Model Context Protocol)
- Modular tool registry (`src/mcp/registry.py`) and server (`src/mcp/server.py`).
- Tools for pre-OCR, ingestion, and vector search.

### 5. Ingestion Pipeline
- Loads documents, splits into semantic chunks, embeds, and stores in Milvus.

### 6. LLM Layer
- Integrates Gemini and Groq clients for embedding and answering queries.

### 7. Vector Store
- Milvus client for semantic search and retrieval.

### 8. Utils
- Logging and configuration utilities.

---

## How It Works

### Document Upload
1. User uploads a document in the UI.
2. Backend saves the file and runs `preocr_tool` to check if OCR is needed.
3. Document is loaded, chunked, embedded, and stored in Milvus (overwriting previous data).

### Querying
1. User asks a question in the chat.
2. Agent uses `vector_search_tool` to find relevant chunks in Milvus.
3. Chunks are assembled as context.
4. Question and context are sent to an LLM (Gemini/Groq) for answer generation.
5. Answer is returned to the UI.

---

## Extensibility & Design Decisions
- **Modular MCP registry**: Easily add or swap tools for new workflows.
- **Agentic orchestration**: Central agent coordinates all steps, enabling future extensibility.
- **Separation of concerns**: UI, API, agent, and tools are decoupled for clarity and scalability.
- **Semantic chunking**: Improves retrieval accuracy and LLM context relevance.

---

## Example Workflow
1. Upload `resume.pdf` in the UI.
2. Ask: “What is the candidate’s name?”
3. System finds the relevant chunk (“SANDESH PATIL”) and returns it as the answer.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/PatilSandesh2004/Agentic-RAG.git
cd agentic-rag
```

### 2. Install Python Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Edit `.env` with your API keys and Milvus credentials:
```
LLM_PROVIDER=groq
EMBEDDING_PROVIDER=gemini
VECTOR_DB=milvus
GROQ_API_KEY=...
GROQ_MODEL=...
GEMINI_API_KEY=...
EMBEDDING_MODEL=...
MILVUS_URI=...
MILVUS_TOKEN=...
MILVUS_COLLECTION=documents
```

### 4. Start the Backend
```bash
uvicorn src.api.main:app --reload
```

### 5. Launch the UI
```bash
streamlit run src/ui/streamlit_app.py
```

---

## Usage
1. Upload a document using the sidebar in the Streamlit UI.
2. Ask questions in the chat input box.
3. Download your chat history if needed.

---

## Folder Structure
```
src/
	api/         # FastAPI backend
	mcp/         # MCP tool registry & server
	ingestion/   # Document loading, chunking, preOCR
	llm/         # LLM clients (Gemini, Groq)
	vectorstore/ # Milvus client
	ui/          # Streamlit UI
	utils/       # Logging, config
```

---

## Testing
- Run scripts in `src/scripts/` to check Milvus connectivity and preview stored data.
- Use the UI and API endpoints to test document ingestion and querying.

---

## Limitations
- Only one document is active at a time (overwrite mode)
- LLM calls may incur cost/latency
- UI is for demo purposes; not production-grade

---

---

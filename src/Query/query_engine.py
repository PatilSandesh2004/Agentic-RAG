# from src.llm.gemini_client import embed_texts
# from src.llm.groq_client import call_llm
# from src.vectorstore.milvus_client import MilvusClient
# from src.app.config import settings
# from src.utils.logger import logger


# def answer_question(question: str) -> str:
#     logger.info(f"QUERY | {question}")

#     query_embedding = embed_texts([question])[0]
#     milvus = MilvusClient()
#     results = milvus.search(query_embedding, settings.TOP_K)

#     if not results or all(r["score"] < 0.15 for r in results):
#         logger.warning("LOW CONFIDENCE | returning I don't know")
#         return "I don’t know. The document does not contain this information."

#     context = "\n\n".join(r["text"] for r in results)

#     prompt = f"""
# You are an AI assistant.
# Answer ONLY using the context below.

# Context:
# {context}

# Question:
# {question}

# If the answer is not present, say "I don't know".
# """

#     answer = call_llm(prompt)
#     logger.info(f"ANSWER | {answer}")

#     return answer.strip()


import logging
from src.llm.groq_client import call_llm
from src.mcp.registry import MCP_TOOLS

logger = logging.getLogger(__name__)


def answer_question(question: str) -> str:
    """
    Simple agent loop using MCP tools.
    """

    logger.info(f"[QUERY] {question}")

    # Step 1: Retrieve context via MCP tool
    search_tool = MCP_TOOLS["vector.search"]
    results = search_tool(query=question, top_k=5)

    if not results:
        return "I could not find relevant information in the document."

    context = "\n\n".join(r["text"] for r in results)

    prompt = f"""
You are answering questions from a document.

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""

    answer = call_llm(prompt)

    logger.info("[ANSWER GENERATED]")
    return answer

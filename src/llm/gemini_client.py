from google import genai
from src.app.config import settings

# Create Gemini client once
_client = genai.Client(api_key=settings.GEMINI_API_KEY)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings using the new Google GenAI SDK.
    Returns 768-dim vectors (compatible with Milvus schema).
    """
    embeddings = []

    for text in texts:
        response = _client.models.embed_content(
            model=settings.EMBEDDING_MODEL,
            contents=text,
        )
        embeddings.append(response.embeddings[0].values)

    return embeddings

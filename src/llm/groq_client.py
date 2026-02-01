from groq import Groq
from src.app.config import Settings

_client = Groq(api_key=Settings.GROQ_API_KEY)


def call_llm(
    prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 512
) -> str:
    
    response = _client.chat.completions.create(
        model=Settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()

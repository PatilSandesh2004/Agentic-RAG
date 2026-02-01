import re
from typing import List


def semantic_chunk_text(
    text: str,
    max_chars: int = 800,
    overlap_chars: int = 150,
) -> List[str]:

    if not text:
        return []

    # Normalize whitespace
    text = re.sub(r"\r", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # -------- STEP 1: Smarter semantic splits --------
    # Split on:
    # - blank lines
    # - headings
    # - bullet points
    semantic_units = re.split(
        r"\n\n|(?=\n[A-Z][A-Z\s]{3,}\n)|(?=\n●)|(?=\n- )",
        text,
    )

    semantic_units = [u.strip() for u in semantic_units if u.strip()]

    # -------- STEP 2: Merge into chunks --------
    chunks = []
    current = ""

    for unit in semantic_units:
        if len(current) + len(unit) <= max_chars:
            current += ("\n\n" if current else "") + unit
        else:
            chunks.append(current)
            current = unit

    if current:
        chunks.append(current)

    # -------- STEP 3: Add overlap --------
    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            final_chunks.append(chunk)
        else:
            overlap = chunks[i - 1][-overlap_chars:]
            final_chunks.append(overlap + "\n\n" + chunk)

    return final_chunks


# backward compatibility
chunk_text = semantic_chunk_text

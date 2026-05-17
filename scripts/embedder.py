"""Gemini Embedding v2 integration."""
import os

import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_EMBEDDING_MODEL

if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=GEMINI_API_KEY)


def embed_text(text, task_type="retrieval_document"):
    """Embed text using Gemini. Truncates if needed."""
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text.")

    # Hard truncate to avoid API errors
    if len(text) > 8000:
        text = text[:8000]

    result = genai.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        content=text,
        task_type=task_type,
    )
    return result["embedding"]

"""LLM module for provider abstraction and prompts."""

from src.llm.prompts import (
    CONDENSE_QUESTION_PROMPT,
    RAG_CHAT_PROMPT,
    RAG_PROMPT,
    RAG_SYSTEM_PROMPT,
    format_documents,
)
from src.llm.providers import (
    LLMProvider,
    LLMSettings,
    get_llm,
    list_providers,
)

__all__ = [
    # Providers
    "LLMProvider",
    "LLMSettings",
    "get_llm",
    "list_providers",
    # Prompts
    "RAG_SYSTEM_PROMPT",
    "RAG_PROMPT",
    "RAG_CHAT_PROMPT",
    "CONDENSE_QUESTION_PROMPT",
    "format_documents",
]

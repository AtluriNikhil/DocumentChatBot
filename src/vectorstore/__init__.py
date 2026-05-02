"""Vector store module for embeddings and document storage."""

from src.vectorstore.embeddings import (
    EmbeddingProvider,
    EmbeddingSettings,
    embed_query,
    embed_texts,
    get_embeddings,
)
from src.vectorstore.store import ChromaStore, VectorStoreError

__all__ = [
    # Embeddings
    "EmbeddingProvider",
    "EmbeddingSettings",
    "get_embeddings",
    "embed_texts",
    "embed_query",
    # Store
    "ChromaStore",
    "VectorStoreError",
]

"""Embedding providers for vector generation."""

from enum import Enum
from pathlib import Path
from typing import List, Union

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class EmbeddingProvider(str, Enum):
    """Available embedding providers."""
    NOVITA = "novita"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"


class EmbeddingSettings(BaseSettings):
    """Settings for embedding configuration."""
    
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")
    
    novita_api_key: str = ""
    novita_base_url: str = "https://api.novita.ai/openai"
    openai_api_key: str = ""
    embedding_provider: EmbeddingProvider = EmbeddingProvider.NOVITA
    embedding_model: str = "baai/bge-m3"
    huggingface_model: str = "intfloat/multilingual-e5-large"


def get_embeddings(settings: EmbeddingSettings | None = None) -> Embeddings:
    """Get configured embedding model.
    
    Args:
        settings: Embedding settings. Loads from environment if None.
        
    Returns:
        Configured embedding model instance.
        
    Raises:
        ValueError: If API key not configured (for OpenAI).
    """
    if settings is None:
        settings = EmbeddingSettings()
    
    if settings.embedding_provider == EmbeddingProvider.HUGGINGFACE:
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError as exc:
            raise ValueError(
                "HuggingFace embeddings require 'langchain-huggingface' and "
                "'sentence-transformers' to be installed"
            ) from exc
        
        return HuggingFaceEmbeddings(
            model_name=settings.huggingface_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    
    if settings.embedding_provider == EmbeddingProvider.NOVITA:
        if not settings.novita_api_key:
            raise ValueError("NOVITA_API_KEY not set in environment")

        return OpenAIEmbeddings(
            api_key=settings.novita_api_key,
            base_url=settings.novita_base_url,
            model=settings.embedding_model,
        )

    if settings.embedding_provider == EmbeddingProvider.OPENAI:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        return OpenAIEmbeddings(
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
        )
    
    raise ValueError(f"Unknown embedding provider: {settings.embedding_provider}")


def embed_texts(texts: List[str], settings: EmbeddingSettings | None = None) -> List[List[float]]:
    """Generate embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed.
        settings: Embedding settings. Loads from environment if None.
        
    Returns:
        List of embedding vectors.
    """
    embeddings = get_embeddings(settings)
    return embeddings.embed_documents(texts)


def embed_query(query: str, settings: EmbeddingSettings | None = None) -> List[float]:
    """Generate embedding for a single query.
    
    Args:
        query: Query text to embed.
        settings: Embedding settings. Loads from environment if None.
        
    Returns:
        Embedding vector for the query.
    """
    embeddings = get_embeddings(settings)
    return embeddings.embed_query(query)

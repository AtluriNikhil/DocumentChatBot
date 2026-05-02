"""API module for FastAPI backend."""

from src.api.main import app, get_vector_store
from src.api.models import (
    HealthResponse,
    IngestRequest,
    IngestResponse,
    ModelsResponse,
    ProviderInfo,
    QueryRequest,
    QueryResponse,
    SourceDocument,
)

__all__ = [
    "app",
    "get_vector_store",
    "HealthResponse",
    "IngestRequest",
    "IngestResponse",
    "ModelsResponse",
    "ProviderInfo",
    "QueryRequest",
    "QueryResponse",
    "SourceDocument",
]

"""Document ingestion module for loading and chunking documents."""

from src.ingestion.chunking import ChunkingConfig, chunk_documents, chunk_text
from src.ingestion.loaders import (
    DocumentLoaderError,
    load_directory,
    load_document,
    load_markdown,
    load_pdf,
    load_text,
)

__all__ = [
    # Loaders
    "load_pdf",
    "load_markdown",
    "load_text",
    "load_document",
    "load_directory",
    "DocumentLoaderError",
    # Chunking
    "ChunkingConfig",
    "chunk_documents",
    "chunk_text",
]

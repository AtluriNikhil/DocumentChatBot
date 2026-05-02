"""Vector store implementations for document storage and retrieval."""

from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from src.vectorstore.embeddings import EmbeddingSettings, get_embeddings


class VectorStoreError(Exception):
    """Raised when vector store operations fail."""


class ChromaStore:
    """Compatibility wrapper around a persisted in-memory vector store.

    The original project used ChromaDB here, but the Windows environment this
    app runs in has been crashing inside Chroma's native layer during document
    ingestion. This wrapper keeps the same public API while using a pure-Python
    vector store underneath.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        persist_directory: Optional[Path] = None,
        embedding_settings: Optional[EmbeddingSettings] = None,
    ):
        """Initialize the vector store.

        Args:
            collection_name: Name for the collection.
            persist_directory: Path for persisted JSON storage.
            embedding_settings: Embedding configuration. Loads from env if None.
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self._embedding_settings = embedding_settings
        self._store: Optional[InMemoryVectorStore] = None

    @property
    def _persist_path(self) -> Optional[Path]:
        """Get the JSON persistence path, if persistence is enabled."""
        if self.persist_directory is None:
            return None
        return self.persist_directory / f"{self.collection_name}.json"

    @property
    def store(self) -> InMemoryVectorStore:
        """Lazy initialization of the vector store."""
        if self._store is None:
            embeddings = get_embeddings(self._embedding_settings)
            persist_path = self._persist_path

            if persist_path and persist_path.exists():
                self._store = InMemoryVectorStore.load(
                    str(persist_path),
                    embedding=embeddings,
                )
            else:
                self._store = InMemoryVectorStore(embedding=embeddings)

        return self._store

    def _persist(self) -> None:
        """Persist the current store to disk if configured."""
        persist_path = self._persist_path
        if persist_path is None or self._store is None:
            return
        self._store.dump(str(persist_path))

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the vector store.

        Args:
            documents: List of documents to add.

        Returns:
            List of document IDs.

        Raises:
            VectorStoreError: If adding documents fails.
        """
        if not documents:
            return []

        try:
            ids = self.store.add_documents(documents)
            self._persist()
            return ids
        except Exception as e:
            error_name = type(e).__name__
            raise VectorStoreError(f"Failed to add documents ({error_name}): {e}")

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> List[Document]:
        """Search for similar documents.

        Args:
            query: Search query text.
            k: Number of results to return.
            filter: Optional metadata filter. Currently unsupported.

        Returns:
            List of similar documents, ordered by relevance.
        """
        if filter is not None:
            raise VectorStoreError("Metadata filtering is not supported by this store")

        return self.store.similarity_search(query, k=k)

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> List[tuple[Document, float]]:
        """Search for similar documents with relevance scores.

        Args:
            query: Search query text.
            k: Number of results to return.
            filter: Optional metadata filter. Currently unsupported.

        Returns:
            List of (document, score) tuples, ordered by relevance.
        """
        if filter is not None:
            raise VectorStoreError("Metadata filtering is not supported by this store")

        return self.store.similarity_search_with_score(query, k=k)

    def delete(self, ids: List[str]) -> None:
        """Delete documents by ID."""
        self.store.delete(ids)
        self._persist()

    def count(self) -> int:
        """Get number of documents in store."""
        return len(self.store.store)

    def clear(self) -> None:
        """Remove all documents from store."""
        ids = list(self.store.store.keys())
        if ids:
            self.store.delete(ids)
            self._persist()

"""Tests for vector store module."""

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from src.vectorstore import (
    ChromaStore,
    EmbeddingProvider,
    EmbeddingSettings,
    VectorStoreError,
)


# Fixtures
@pytest.fixture
def mock_embeddings():
    """Mock embedding function that returns fixed vectors."""
    mock = MagicMock()
    mock.embed_documents.return_value = [[0.1, 0.2, 0.3]] * 10
    mock.embed_query.return_value = [0.1, 0.2, 0.3]
    return mock


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        Document(page_content="First document about cats", metadata={"source": "doc1.txt"}),
        Document(page_content="Second document about dogs", metadata={"source": "doc2.txt"}),
        Document(page_content="Third document about birds", metadata={"source": "doc3.txt"}),
    ]


# Embedding Settings Tests
class TestEmbeddingSettings:
    """Tests for embedding configuration."""

    def test_default_provider(self):
        settings = EmbeddingSettings()
        assert settings.embedding_provider == EmbeddingProvider.NOVITA

    def test_default_model(self):
        settings = EmbeddingSettings()
        assert settings.embedding_model == "baai/bge-m3"

    def test_custom_settings(self):
        settings = EmbeddingSettings(
            openai_api_key="test-key",
            embedding_model="text-embedding-3-small",
        )
        assert settings.openai_api_key == "test-key"
        assert settings.embedding_model == "text-embedding-3-small"

    def test_huggingface_provider(self):
        settings = EmbeddingSettings(embedding_provider=EmbeddingProvider.HUGGINGFACE)
        assert settings.embedding_provider == EmbeddingProvider.HUGGINGFACE
        assert settings.huggingface_model == "intfloat/multilingual-e5-large"


# ChromaStore Tests
class TestChromaStore:
    """Tests for ChromaDB vector store."""

    @patch("src.vectorstore.store.get_embeddings")
    def test_init_creates_store(self, mock_get_embeddings, mock_embeddings):
        mock_get_embeddings.return_value = mock_embeddings
        
        store = ChromaStore(collection_name="test")
        # Access store property to trigger initialization
        _ = store.store
        
        assert store.collection_name == "test"
        mock_get_embeddings.assert_called_once()

    @patch("src.vectorstore.store.get_embeddings")
    def test_add_documents(self, mock_get_embeddings, mock_embeddings, sample_documents):
        mock_get_embeddings.return_value = mock_embeddings
        
        store = ChromaStore(collection_name="test_add")
        ids = store.add_documents(sample_documents)
        
        assert len(ids) == 3
        assert store.count() == 3

    @patch("src.vectorstore.store.get_embeddings")
    def test_add_empty_documents(self, mock_get_embeddings, mock_embeddings):
        mock_get_embeddings.return_value = mock_embeddings
        
        store = ChromaStore(collection_name="test_empty")
        ids = store.add_documents([])
        
        assert ids == []

    @patch("src.vectorstore.store.get_embeddings")
    def test_similarity_search(self, mock_get_embeddings, mock_embeddings, sample_documents):
        mock_get_embeddings.return_value = mock_embeddings
        
        store = ChromaStore(collection_name="test_search")
        store.add_documents(sample_documents)
        
        results = store.similarity_search("cats", k=2)
        
        assert len(results) <= 2
        assert all(isinstance(doc, Document) for doc in results)

    @patch("src.vectorstore.store.get_embeddings")
    def test_similarity_search_with_score(self, mock_get_embeddings, mock_embeddings, sample_documents):
        mock_get_embeddings.return_value = mock_embeddings
        
        store = ChromaStore(collection_name="test_search_score")
        store.add_documents(sample_documents)
        
        results = store.similarity_search_with_score("dogs", k=2)
        
        assert len(results) <= 2
        assert all(isinstance(r, tuple) for r in results)
        assert all(isinstance(r[0], Document) for r in results)
        assert all(isinstance(r[1], float) for r in results)

    @patch("src.vectorstore.store.get_embeddings")
    def test_delete_documents(self, mock_get_embeddings, mock_embeddings, sample_documents):
        mock_get_embeddings.return_value = mock_embeddings
        
        store = ChromaStore(collection_name="test_delete")
        ids = store.add_documents(sample_documents)
        
        assert store.count() == 3
        
        store.delete([ids[0]])
        
        assert store.count() == 2

    @patch("src.vectorstore.store.get_embeddings")
    def test_clear_store(self, mock_get_embeddings, mock_embeddings, sample_documents):
        mock_get_embeddings.return_value = mock_embeddings
        
        store = ChromaStore(collection_name="test_clear")
        store.add_documents(sample_documents)
        
        assert store.count() == 3
        
        store.clear()
        
        assert store.count() == 0

    @patch("src.vectorstore.store.get_embeddings")
    def test_count_empty_store(self, mock_get_embeddings, mock_embeddings):
        mock_get_embeddings.return_value = mock_embeddings
        
        store = ChromaStore(collection_name="test_count_empty")
        
        assert store.count() == 0


# Integration test (requires API key, skip in CI)
class TestEmbeddingsIntegration:
    """Integration tests for embeddings (require API key)."""

    @pytest.mark.skipif(
        not EmbeddingSettings().novita_api_key,
        reason="NOVITA_API_KEY not set"
    )
    def test_get_embeddings_returns_model(self):
        from src.vectorstore import get_embeddings
        
        embeddings = get_embeddings()
        assert embeddings is not None

    def test_get_embeddings_raises_without_novita_key(self):
        from src.vectorstore import get_embeddings

        settings = EmbeddingSettings(
            embedding_provider=EmbeddingProvider.NOVITA,
            novita_api_key="",
        )

        with pytest.raises(ValueError, match="NOVITA_API_KEY not set"):
            get_embeddings(settings)

    def test_get_embeddings_raises_without_openai_key(self):
        from src.vectorstore import get_embeddings
        
        settings = EmbeddingSettings(
            embedding_provider=EmbeddingProvider.OPENAI,
            openai_api_key="",
        )
        
        with pytest.raises(ValueError, match="OPENAI_API_KEY not set"):
            get_embeddings(settings)

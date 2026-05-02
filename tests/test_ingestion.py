"""Tests for document ingestion module."""

from pathlib import Path

import pytest
from langchain_core.documents import Document

from src.ingestion import (
    ChunkingConfig,
    DocumentLoaderError,
    chunk_documents,
    chunk_text,
    load_directory,
    load_document,
    load_markdown,
    load_text,
)


# Fixtures
@pytest.fixture
def sample_docs_dir() -> Path:
    """Path to sample documents directory."""
    return Path(__file__).parent.parent / "data" / "sample_docs"


@pytest.fixture
def sample_text_file(sample_docs_dir) -> Path:
    """Path to sample text file."""
    return sample_docs_dir / "sample.txt"


@pytest.fixture
def sample_markdown_file(sample_docs_dir) -> Path:
    """Path to sample markdown file."""
    return sample_docs_dir / "sample.md"


# Loader Tests
class TestTextLoader:
    """Tests for text file loading."""

    def test_load_text_returns_documents(self, sample_text_file):
        docs = load_text(sample_text_file)
        assert len(docs) == 1
        assert isinstance(docs[0], Document)

    def test_load_text_contains_content(self, sample_text_file):
        docs = load_text(sample_text_file)
        assert "sample text document" in docs[0].page_content.lower()

    def test_load_text_has_metadata(self, sample_text_file):
        docs = load_text(sample_text_file)
        assert docs[0].metadata["source"] == str(sample_text_file)
        assert docs[0].metadata["file_type"] == "text"

    def test_load_text_file_not_found(self):
        with pytest.raises(DocumentLoaderError, match="File not found"):
            load_text(Path("/nonexistent/file.txt"))


class TestMarkdownLoader:
    """Tests for markdown file loading."""

    def test_load_markdown_returns_documents(self, sample_markdown_file):
        docs = load_markdown(sample_markdown_file)
        assert len(docs) >= 1
        assert isinstance(docs[0], Document)

    def test_load_markdown_contains_content(self, sample_markdown_file):
        docs = load_markdown(sample_markdown_file)
        content = docs[0].page_content.lower()
        assert "sample" in content or "markdown" in content

    def test_load_markdown_has_metadata(self, sample_markdown_file):
        docs = load_markdown(sample_markdown_file)
        assert docs[0].metadata["source"] == str(sample_markdown_file)
        assert docs[0].metadata["file_type"] == "markdown"


class TestLoadDocument:
    """Tests for generic document loading."""

    def test_load_document_txt(self, sample_text_file):
        docs = load_document(sample_text_file)
        assert len(docs) >= 1
        assert docs[0].metadata["file_type"] == "text"

    def test_load_document_md(self, sample_markdown_file):
        docs = load_document(sample_markdown_file)
        assert len(docs) >= 1
        assert docs[0].metadata["file_type"] == "markdown"

    def test_load_document_unsupported(self, tmp_path):
        unsupported = tmp_path / "file.xyz"
        unsupported.write_text("content")
        with pytest.raises(DocumentLoaderError, match="Unsupported file type"):
            load_document(unsupported)


class TestLoadDirectory:
    """Tests for directory loading."""

    def test_load_directory_all_files(self, sample_docs_dir):
        docs = load_directory(sample_docs_dir)
        assert len(docs) >= 2  # At least txt and md

    def test_load_directory_filter_extension(self, sample_docs_dir):
        docs = load_directory(sample_docs_dir, extensions=[".txt"])
        assert len(docs) >= 1
        assert all(d.metadata["file_type"] == "text" for d in docs)

    def test_load_directory_not_found(self):
        with pytest.raises(DocumentLoaderError, match="Directory not found"):
            load_directory(Path("/nonexistent/directory"))


# Chunking Tests
class TestChunkingConfig:
    """Tests for chunking configuration."""

    def test_default_config(self):
        config = ChunkingConfig()
        assert config.chunk_size == 1000
        assert config.chunk_overlap == 200

    def test_custom_config(self):
        config = ChunkingConfig(chunk_size=500, chunk_overlap=50)
        assert config.chunk_size == 500
        assert config.chunk_overlap == 50

    def test_invalid_chunk_size(self):
        with pytest.raises(ValueError, match="chunk_size must be positive"):
            ChunkingConfig(chunk_size=0)

    def test_invalid_overlap(self):
        with pytest.raises(ValueError, match="chunk_overlap cannot be negative"):
            ChunkingConfig(chunk_overlap=-1)

    def test_overlap_exceeds_size(self):
        with pytest.raises(ValueError, match="chunk_overlap must be less than"):
            ChunkingConfig(chunk_size=100, chunk_overlap=100)


class TestChunkDocuments:
    """Tests for document chunking."""

    def test_chunk_documents_returns_list(self, sample_text_file):
        docs = load_text(sample_text_file)
        chunks = chunk_documents(docs)
        assert isinstance(chunks, list)
        assert all(isinstance(c, Document) for c in chunks)

    def test_chunk_documents_preserves_metadata(self, sample_text_file):
        docs = load_text(sample_text_file)
        chunks = chunk_documents(docs)
        for chunk in chunks:
            assert "source" in chunk.metadata
            assert "chunk_index" in chunk.metadata

    def test_chunk_documents_with_config(self, sample_text_file):
        docs = load_text(sample_text_file)
        config = ChunkingConfig(chunk_size=50, chunk_overlap=10)
        chunks = chunk_documents(docs, config)
        # Smaller chunks should produce more documents
        assert len(chunks) >= 1


class TestChunkText:
    """Tests for raw text chunking."""

    def test_chunk_text_returns_documents(self):
        text = "This is a test. " * 100
        chunks = chunk_text(text)
        assert len(chunks) >= 1
        assert all(isinstance(c, Document) for c in chunks)

    def test_chunk_text_with_metadata(self):
        text = "Test content. " * 50
        metadata = {"source": "test", "custom": "value"}
        chunks = chunk_text(text, metadata=metadata)
        for chunk in chunks:
            assert chunk.metadata["source"] == "test"
            assert chunk.metadata["custom"] == "value"
            assert "chunk_index" in chunk.metadata

    def test_chunk_text_respects_config(self):
        text = "Word " * 500  # ~2500 chars
        small_config = ChunkingConfig(chunk_size=100, chunk_overlap=20)
        large_config = ChunkingConfig(chunk_size=1000, chunk_overlap=100)
        
        small_chunks = chunk_text(text, config=small_config)
        large_chunks = chunk_text(text, config=large_config)
        
        assert len(small_chunks) > len(large_chunks)

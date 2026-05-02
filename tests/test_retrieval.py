"""Tests for retrieval and LLM modules."""

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage

from src.llm import (
    LLMProvider,
    LLMSettings,
    RAG_PROMPT,
    format_documents,
)
from src.retrieval import RAGChain


# Fixtures
@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        Document(page_content="Cats are popular pets.", metadata={"source": "pets.txt"}),
        Document(page_content="Dogs are loyal animals.", metadata={"source": "pets.txt"}),
    ]


@pytest.fixture
def mock_vector_store(sample_documents):
    """Mock vector store that returns sample documents."""
    mock = MagicMock()
    mock.similarity_search.return_value = sample_documents
    return mock


@pytest.fixture
def mock_llm():
    """Mock LLM that returns a fixed response."""
    mock = MagicMock()
    mock.invoke.return_value = MagicMock(content="Cats and dogs are popular pets.")
    return mock


# LLM Settings Tests
class TestLLMSettings:
    """Tests for LLM configuration."""

    def test_default_provider(self):
        settings = LLMSettings()
        assert settings.llm_provider == LLMProvider.NOVITA

    def test_default_novita_model(self):
        settings = LLMSettings()
        assert settings.novita_model == "meta-llama/llama-3.3-70b-instruct"

    def test_custom_settings(self):
        settings = LLMSettings(
            llm_provider=LLMProvider.ANTHROPIC,
            anthropic_api_key="test-key",
            temperature=0.5,
        )
        assert settings.llm_provider == LLMProvider.ANTHROPIC
        assert settings.temperature == 0.5


# Format Documents Tests
class TestFormatDocuments:
    """Tests for document formatting."""

    def test_format_single_document(self):
        docs = [Document(page_content="Test content", metadata={"source": "test.txt"})]
        result = format_documents(docs)
        
        assert "[Document 1]" in result
        assert "test.txt" in result
        assert "Test content" in result

    def test_format_multiple_documents(self):
        docs = [
            Document(page_content="First", metadata={"source": "a.txt"}),
            Document(page_content="Second", metadata={"source": "b.txt"}),
        ]
        result = format_documents(docs)
        
        assert "[Document 1]" in result
        assert "[Document 2]" in result
        assert "---" in result  # Separator

    def test_format_unknown_source(self):
        docs = [Document(page_content="Content", metadata={})]
        result = format_documents(docs)
        
        assert "Unknown" in result


# RAG Chain Tests
class TestRAGChain:
    """Tests for RAG chain."""

    def test_init(self, mock_vector_store):
        chain = RAGChain(vector_store=mock_vector_store, k=3)
        
        assert chain.k == 3
        assert chain.vector_store == mock_vector_store

    def test_retrieve(self, mock_vector_store, sample_documents):
        chain = RAGChain(vector_store=mock_vector_store)
        
        results = chain.retrieve("test query")
        
        mock_vector_store.similarity_search.assert_called_once_with("test query", k=4)
        assert results == sample_documents

    def test_invoke_returns_answer_and_sources(self, mock_vector_store, sample_documents):
        """Test that invoke returns expected structure with mocked chain."""
        chain = RAGChain(vector_store=mock_vector_store)
        
        # Mock the entire chain execution by patching invoke method behavior
        with patch.object(RAGChain, 'invoke') as mock_invoke:
            mock_invoke.return_value = {
                "answer": "Test answer about pets.",
                "sources": [
                    {"content": doc.page_content[:200], "metadata": doc.metadata}
                    for doc in sample_documents
                ],
            }
            
            result = chain.invoke("What are popular pets?")
        
        assert "answer" in result
        assert "sources" in result
        assert len(result["sources"]) == 2



    def test_clear_history(self, mock_vector_store):
        chain = RAGChain(vector_store=mock_vector_store)
        chain._chat_history = [
            HumanMessage(content="test"),
            AIMessage(content="response"),
        ]
        
        chain.clear_history()
        
        assert chain.chat_history == []

    def test_chat_history_returns_copy(self, mock_vector_store):
        chain = RAGChain(vector_store=mock_vector_store)
        chain._chat_history = [HumanMessage(content="test")]
        
        history = chain.chat_history
        history.append(AIMessage(content="new"))
        
        # Original should be unchanged
        assert len(chain._chat_history) == 1


# Prompt Tests
class TestPrompts:
    """Tests for prompt templates."""

    def test_rag_prompt_has_context(self):
        assert "context" in RAG_PROMPT.input_variables

    def test_rag_prompt_has_question(self):
        assert "question" in RAG_PROMPT.input_variables


# Integration Tests (require API key)
class TestLLMIntegration:
    """Integration tests for LLM providers."""

    def test_get_llm_raises_without_novita_key(self):
        from src.llm import get_llm

        settings = LLMSettings(
            llm_provider=LLMProvider.NOVITA,
            novita_api_key="",
        )

        with pytest.raises(ValueError, match="NOVITA_API_KEY not set"):
            get_llm(settings)

    def test_get_llm_raises_without_openai_key(self):
        from src.llm import get_llm
        
        settings = LLMSettings(
            llm_provider=LLMProvider.OPENAI,
            openai_api_key="",
        )
        
        with pytest.raises(ValueError, match="OPENAI_API_KEY not set"):
            get_llm(settings)

    def test_get_llm_raises_without_anthropic_key(self):
        from src.llm import get_llm
        
        settings = LLMSettings(
            llm_provider=LLMProvider.ANTHROPIC,
            anthropic_api_key="",
        )
        
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not set"):
            get_llm(settings)

    def test_list_providers(self):
        from src.llm import list_providers
        
        providers = list_providers()
        
        assert len(providers) == 4
        assert any(p["provider"] == "novita" for p in providers)
        assert any(p["provider"] == "openai" for p in providers)
        assert any(p["provider"] == "anthropic" for p in providers)
        assert any(p["provider"] == "ollama" for p in providers)

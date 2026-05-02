"""Pydantic models for API request/response validation."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# Enums
class LLMProviderEnum(str, Enum):
    """Available LLM providers."""
    NOVITA = "novita"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


# Request Models
class QueryRequest(BaseModel):
    """Request model for RAG queries."""
    
    question: str = Field(..., min_length=1, description="The question to ask")
    k: int = Field(default=4, ge=1, le=10, description="Number of documents to retrieve")
    use_history: bool = Field(default=False, description="Include conversation history")
    provider: Optional[LLMProviderEnum] = Field(default=None, description="LLM provider override")
    
    model_config = {"json_schema_extra": {
        "example": {
            "question": "What is the warranty policy?",
            "k": 4,
            "use_history": False,
        }
    }}


class IngestRequest(BaseModel):
    """Request model for document ingestion."""
    
    collection_name: str = Field(default="documents", description="Vector store collection name")
    chunk_size: int = Field(default=1000, ge=100, le=4000, description="Chunk size in characters")
    chunk_overlap: int = Field(default=200, ge=0, le=1000, description="Chunk overlap in characters")
    
    model_config = {"json_schema_extra": {
        "example": {
            "collection_name": "documents",
            "chunk_size": 1000,
            "chunk_overlap": 200,
        }
    }}


# Response Models
class SourceDocument(BaseModel):
    """A source document returned with query results."""
    
    content: str = Field(..., description="Document content snippet")
    metadata: dict = Field(default_factory=dict, description="Document metadata")


class QueryResponse(BaseModel):
    """Response model for RAG queries."""
    
    answer: str = Field(..., description="Generated answer")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents")
    
    model_config = {"json_schema_extra": {
        "example": {
            "answer": "The warranty policy covers defects for 2 years.",
            "sources": [
                {"content": "Warranty covers defects...", "metadata": {"source": "policy.pdf"}}
            ],
        }
    }}


class IngestResponse(BaseModel):
    """Response model for document ingestion."""
    
    message: str = Field(..., description="Status message")
    documents_processed: int = Field(..., description="Number of documents processed")
    chunks_created: int = Field(..., description="Number of chunks created")


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")


class ProviderInfo(BaseModel):
    """Information about an LLM provider."""
    
    provider: str = Field(..., description="Provider name")
    default_model: str = Field(..., description="Default model")
    requires_api_key: bool = Field(..., description="Whether API key is required")


class ModelsResponse(BaseModel):
    """Response model for available models."""
    
    providers: List[ProviderInfo] = Field(..., description="Available LLM providers")

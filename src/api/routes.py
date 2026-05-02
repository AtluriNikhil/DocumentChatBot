"""API route definitions."""

from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.api.models import (
    IngestRequest,
    IngestResponse,
    ModelsResponse,
    ProviderInfo,
    QueryRequest,
    QueryResponse,
    SourceDocument,
)
from src.ingestion import ChunkingConfig, chunk_documents, load_document
from src.llm import LLMProvider, LLMSettings, list_providers
from src.retrieval import RAGChain
from src.vectorstore import ChromaStore, EmbeddingSettings

router = APIRouter()


def get_vector_store() -> ChromaStore:
    """Get or create vector store instance."""
    from src.api.main import app_state
    
    if app_state.vector_store is None:
        persist_dir = Path("data/chroma_db")
        persist_dir.mkdir(parents=True, exist_ok=True)
        app_state.vector_store = ChromaStore(
            collection_name="documents",
            persist_directory=persist_dir,
        )
    return app_state.vector_store


@router.post("/ingest", response_model=IngestResponse, tags=["Documents"])
async def ingest_documents(
    files: List[UploadFile] = File(...),
    collection_name: str = "documents",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
):
    """Ingest documents into the vector store.
    
    Upload PDF, Markdown, or TXT files to be processed and indexed.
    """
    if chunk_overlap >= chunk_size:
        raise HTTPException(
            status_code=400,
            detail="chunk_overlap must be less than chunk_size",
        )
    
    # Create temp directory for uploads
    temp_dir = Path("data/temp_uploads")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    all_documents = []
    processed_count = 0
    
    try:
        for file in files:
            # Validate file type
            suffix = Path(file.filename).suffix.lower()
            if suffix not in [".pdf", ".md", ".markdown", ".txt"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {suffix}. Supported: .pdf, .md, .txt",
                )
            
            # Save temporarily
            temp_path = temp_dir / file.filename
            content = await file.read()
            temp_path.write_bytes(content)
            
            try:
                # Load and chunk
                documents = load_document(temp_path)
                all_documents.extend(documents)
                processed_count += 1
            finally:
                # Clean up temp file
                temp_path.unlink(missing_ok=True)
        
        # Chunk all documents
        config = ChunkingConfig(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = chunk_documents(all_documents, config)
        
        # Add to vector store
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        
        return IngestResponse(
            message="Documents ingested successfully",
            documents_processed=processed_count,
            chunks_created=len(chunks),
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse, tags=["Query"])
async def query_documents(request: QueryRequest):
    """Query the RAG system with a question.
    
    Retrieves relevant documents and generates an answer using the configured LLM.
    """
    try:
        vector_store = get_vector_store()
        
        # Check if there are documents
        if vector_store.count() == 0:
            raise HTTPException(
                status_code=400,
                detail="No documents in the vector store. Please ingest documents first.",
            )
        
        # Configure LLM settings
        llm_settings = None
        if request.provider:
            llm_settings = LLMSettings(
                llm_provider=LLMProvider(request.provider.value)
            )
        
        # Create RAG chain and query
        chain = RAGChain(
            vector_store=vector_store,
            llm_settings=llm_settings,
            k=request.k,
        )
        
        result = chain.invoke(request.question, use_history=request.use_history)
        
        return QueryResponse(
            answer=result["answer"],
            sources=[
                SourceDocument(content=s["content"], metadata=s["metadata"])
                for s in result["sources"]
            ],
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models", response_model=ModelsResponse, tags=["Models"])
async def get_available_models():
    """Get list of available LLM providers."""
    providers = list_providers()
    return ModelsResponse(
        providers=[
            ProviderInfo(
                provider=p["provider"],
                default_model=p["default_model"],
                requires_api_key=p["requires_api_key"],
            )
            for p in providers
        ]
    )


@router.get("/documents/count", tags=["Documents"])
async def get_document_count():
    """Get the number of documents in the vector store."""
    vector_store = get_vector_store()
    return {"count": vector_store.count()}


@router.delete("/documents", tags=["Documents"])
async def clear_documents():
    """Clear all documents from the vector store."""
    vector_store = get_vector_store()
    vector_store.clear()
    return {"message": "All documents cleared"}

"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.models import HealthResponse
from src.api.routes import router
from src.vectorstore import ChromaStore


# Global state
class AppState:
    """Application state container."""
    vector_store: Optional[ChromaStore] = None


app_state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup: Initialize vector store
    persist_dir = Path("data/chroma_db")
    persist_dir.mkdir(parents=True, exist_ok=True)
    app_state.vector_store = ChromaStore(
        collection_name="documents",
        persist_directory=persist_dir,
    )
    yield
    # Shutdown: Cleanup if needed
    app_state.vector_store = None


app = FastAPI(
    title="RAG Document Assistant",
    description="Production-ready RAG system with multi-provider LLM support",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health status."""
    return HealthResponse(status="healthy", version="0.1.0")


def get_vector_store() -> ChromaStore:
    """Get the application vector store instance."""
    if app_state.vector_store is None:
        raise RuntimeError("Vector store not initialized")
    return app_state.vector_store

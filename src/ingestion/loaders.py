"""Document loaders for PDF, Markdown, and TXT files."""

from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)
from langchain_core.documents import Document


class DocumentLoaderError(Exception):
    """Raised when document loading fails."""
    pass


def load_pdf(file_path: Path) -> List[Document]:
    """Load a PDF file and return documents (one per page).
    
    Args:
        file_path: Path to PDF file.
        
    Returns:
        List of Document objects with page content and metadata.
        
    Raises:
        DocumentLoaderError: If file doesn't exist or loading fails.
    """
    if not file_path.exists():
        raise DocumentLoaderError(f"File not found: {file_path}")
    
    try:
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()
        
        # Ensure consistent metadata
        for doc in documents:
            doc.metadata["source"] = str(file_path)
            doc.metadata["file_type"] = "pdf"
        
        return documents
    except Exception as e:
        raise DocumentLoaderError(f"Failed to load PDF {file_path}: {e}")


def load_markdown(file_path: Path) -> List[Document]:
    """Load a Markdown file and return as document.
    
    Args:
        file_path: Path to Markdown file.
        
    Returns:
        List containing single Document with full content.
        
    Raises:
        DocumentLoaderError: If file doesn't exist or loading fails.
    """
    if not file_path.exists():
        raise DocumentLoaderError(f"File not found: {file_path}")
    
    try:
        # Use TextLoader for markdown - simpler and no extra dependencies
        loader = TextLoader(str(file_path))
        documents = loader.load()
        
        for doc in documents:
            doc.metadata["source"] = str(file_path)
            doc.metadata["file_type"] = "markdown"
        
        return documents
    except Exception as e:
        raise DocumentLoaderError(f"Failed to load Markdown {file_path}: {e}")


def load_text(file_path: Path) -> List[Document]:
    """Load a plain text file and return as document.
    
    Args:
        file_path: Path to text file.
        
    Returns:
        List containing single Document with full content.
        
    Raises:
        DocumentLoaderError: If file doesn't exist or loading fails.
    """
    if not file_path.exists():
        raise DocumentLoaderError(f"File not found: {file_path}")
    
    try:
        loader = TextLoader(str(file_path))
        documents = loader.load()
        
        for doc in documents:
            doc.metadata["source"] = str(file_path)
            doc.metadata["file_type"] = "text"
        
        return documents
    except Exception as e:
        raise DocumentLoaderError(f"Failed to load text file {file_path}: {e}")


def load_document(file_path: Path) -> List[Document]:
    """Load a document based on file extension.
    
    Supports: .pdf, .md, .markdown, .txt
    
    Args:
        file_path: Path to document file.
        
    Returns:
        List of Document objects.
        
    Raises:
        DocumentLoaderError: If file type unsupported or loading fails.
    """
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()
    
    loaders = {
        ".pdf": load_pdf,
        ".md": load_markdown,
        ".markdown": load_markdown,
        ".txt": load_text,
    }
    
    if suffix not in loaders:
        raise DocumentLoaderError(
            f"Unsupported file type: {suffix}. Supported: {list(loaders.keys())}"
        )
    
    return loaders[suffix](file_path)


def load_directory(
    directory: Path,
    extensions: Optional[List[str]] = None,
) -> List[Document]:
    """Load all supported documents from a directory.
    
    Args:
        directory: Path to directory containing documents.
        extensions: Optional list of extensions to filter (e.g., [".pdf", ".md"]).
                   If None, loads all supported types.
        
    Returns:
        List of all Document objects from directory.
        
    Raises:
        DocumentLoaderError: If directory doesn't exist.
    """
    if not directory.exists():
        raise DocumentLoaderError(f"Directory not found: {directory}")
    
    if not directory.is_dir():
        raise DocumentLoaderError(f"Not a directory: {directory}")
    
    supported = {".pdf", ".md", ".markdown", ".txt"}
    if extensions:
        extensions = [e.lower() if e.startswith(".") else f".{e.lower()}" for e in extensions]
        extensions = [e for e in extensions if e in supported]
    else:
        extensions = list(supported)
    
    documents = []
    for ext in extensions:
        for file_path in directory.glob(f"*{ext}"):
            try:
                docs = load_document(file_path)
                documents.extend(docs)
            except DocumentLoaderError as e:
                # Log warning but continue with other files
                print(f"WARNING: {e}")
    
    return documents

"""Text chunking strategies for document processing."""

from typing import List, Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingConfig:
    """Configuration for text chunking.
    
    Attributes:
        chunk_size: Maximum characters per chunk (default: 1000).
        chunk_overlap: Characters to overlap between chunks (default: 200).
        separators: List of separators to split on, in order of priority.
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]


def create_text_splitter(config: Optional[ChunkingConfig] = None) -> RecursiveCharacterTextSplitter:
    """Create a text splitter with the given configuration.
    
    Args:
        config: Chunking configuration. Uses defaults if None.
        
    Returns:
        Configured RecursiveCharacterTextSplitter.
    """
    if config is None:
        config = ChunkingConfig()
    
    return RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=config.separators,
        length_function=len,
        is_separator_regex=False,
    )


def chunk_documents(
    documents: List[Document],
    config: Optional[ChunkingConfig] = None,
) -> List[Document]:
    """Split documents into smaller chunks.
    
    Args:
        documents: List of documents to chunk.
        config: Chunking configuration. Uses defaults if None.
        
    Returns:
        List of chunked documents with preserved metadata.
    """
    splitter = create_text_splitter(config)
    chunked = splitter.split_documents(documents)
    
    # Add chunk index to metadata
    for i, doc in enumerate(chunked):
        doc.metadata["chunk_index"] = i
    
    return chunked


def chunk_text(
    text: str,
    config: Optional[ChunkingConfig] = None,
    metadata: Optional[dict] = None,
) -> List[Document]:
    """Split raw text into document chunks.
    
    Args:
        text: Raw text to chunk.
        config: Chunking configuration. Uses defaults if None.
        metadata: Optional metadata to attach to all chunks.
        
    Returns:
        List of Document objects from chunked text.
    """
    splitter = create_text_splitter(config)
    texts = splitter.split_text(text)
    
    base_metadata = metadata or {}
    documents = []
    
    for i, chunk_text in enumerate(texts):
        doc_metadata = {**base_metadata, "chunk_index": i}
        documents.append(Document(page_content=chunk_text, metadata=doc_metadata))
    
    return documents

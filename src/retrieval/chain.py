"""RAG retrieval chain implementation."""

from typing import AsyncIterator, Iterator, List, Optional

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.llm import format_documents, get_llm, RAG_CHAT_PROMPT, RAG_PROMPT
from src.llm.providers import LLMSettings
from src.vectorstore import ChromaStore


class RAGChain:
    """Retrieval-Augmented Generation chain.
    
    Combines document retrieval with LLM generation for question answering.
    """
    
    def __init__(
        self,
        vector_store: ChromaStore,
        llm_settings: Optional[LLMSettings] = None,
        k: int = 4,
    ):
        """Initialize RAG chain.
        
        Args:
            vector_store: Vector store for document retrieval.
            llm_settings: LLM configuration. Loads from env if None.
            k: Number of documents to retrieve.
        """
        self.vector_store = vector_store
        self.llm_settings = llm_settings
        self.k = k
        self._llm = None
        self._chat_history: List[BaseMessage] = []
    
    @property
    def llm(self):
        """Lazy initialization of LLM."""
        if self._llm is None:
            self._llm = get_llm(self.llm_settings)
        return self._llm
    
    def retrieve(self, query: str) -> List[Document]:
        """Retrieve relevant documents for a query.
        
        Args:
            query: User question.
            
        Returns:
            List of relevant documents.
        """
        return self.vector_store.similarity_search(query, k=self.k)
    
    def invoke(self, query: str, use_history: bool = False) -> dict:
        """Run RAG chain and return response with sources.
        
        Args:
            query: User question.
            use_history: Whether to include conversation history.
            
        Returns:
            Dict with 'answer' and 'sources' keys.
        """
        # Retrieve documents
        documents = self.retrieve(query)
        context = format_documents(documents)
        
        # Select prompt
        if use_history and self._chat_history:
            prompt = RAG_CHAT_PROMPT
            chain_input = {
                "context": context,
                "question": query,
                "chat_history": self._chat_history,
            }
        else:
            prompt = RAG_PROMPT
            chain_input = {
                "context": context,
                "question": query,
            }
        
        # Build and run chain
        chain = prompt | self.llm | StrOutputParser()
        answer = chain.invoke(chain_input)
        
        # Update history
        if use_history:
            self._chat_history.append(HumanMessage(content=query))
            self._chat_history.append(AIMessage(content=answer))
        
        return {
            "answer": answer,
            "sources": [
                {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata,
                }
                for doc in documents
            ],
        }
    
    def stream(self, query: str, use_history: bool = False) -> Iterator[str]:
        """Stream RAG chain response.
        
        Args:
            query: User question.
            use_history: Whether to include conversation history.
            
        Yields:
            Response chunks as they're generated.
        """
        # Retrieve documents
        documents = self.retrieve(query)
        context = format_documents(documents)
        
        # Select prompt
        if use_history and self._chat_history:
            prompt = RAG_CHAT_PROMPT
            chain_input = {
                "context": context,
                "question": query,
                "chat_history": self._chat_history,
            }
        else:
            prompt = RAG_PROMPT
            chain_input = {
                "context": context,
                "question": query,
            }
        
        # Build and stream chain
        chain = prompt | self.llm | StrOutputParser()
        
        full_response = ""
        for chunk in chain.stream(chain_input):
            full_response += chunk
            yield chunk
        
        # Update history after streaming completes
        if use_history:
            self._chat_history.append(HumanMessage(content=query))
            self._chat_history.append(AIMessage(content=full_response))
    
    async def astream(self, query: str, use_history: bool = False) -> AsyncIterator[str]:
        """Async stream RAG chain response.
        
        Args:
            query: User question.
            use_history: Whether to include conversation history.
            
        Yields:
            Response chunks as they're generated.
        """
        # Retrieve documents
        documents = self.retrieve(query)
        context = format_documents(documents)
        
        # Select prompt
        if use_history and self._chat_history:
            prompt = RAG_CHAT_PROMPT
            chain_input = {
                "context": context,
                "question": query,
                "chat_history": self._chat_history,
            }
        else:
            prompt = RAG_PROMPT
            chain_input = {
                "context": context,
                "question": query,
            }
        
        # Build and stream chain
        chain = prompt | self.llm | StrOutputParser()
        
        full_response = ""
        async for chunk in chain.astream(chain_input):
            full_response += chunk
            yield chunk
        
        # Update history after streaming completes
        if use_history:
            self._chat_history.append(HumanMessage(content=query))
            self._chat_history.append(AIMessage(content=full_response))
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self._chat_history = []
    
    @property
    def chat_history(self) -> List[BaseMessage]:
        """Get current conversation history."""
        return self._chat_history.copy()

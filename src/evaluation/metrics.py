"""Evaluation metrics for RAG system quality assessment."""

import time
from dataclasses import dataclass
from typing import List, Optional

from langchain_core.documents import Document


@dataclass
class EvaluationResult:
    """Container for evaluation metrics."""
    
    question: str
    answer: str
    expected_answer: Optional[str]
    sources: List[dict]
    latency_seconds: float
    relevance_score: Optional[float] = None
    faithfulness_score: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for logging."""
        return {
            "question": self.question,
            "answer": self.answer,
            "expected_answer": self.expected_answer,
            "num_sources": len(self.sources),
            "latency_seconds": self.latency_seconds,
            "relevance_score": self.relevance_score,
            "faithfulness_score": self.faithfulness_score,
        }


def measure_latency(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, end - start
    return wrapper


def calculate_relevance_score(
    question: str,
    retrieved_docs: List[Document],
    expected_keywords: Optional[List[str]] = None,
) -> float:
    """Calculate relevance score based on keyword overlap.
    
    Simple heuristic: checks if expected keywords appear in retrieved documents.
    For production, use embedding similarity or LLM-as-judge.
    
    Args:
        question: The user question.
        retrieved_docs: Documents retrieved for the question.
        expected_keywords: Keywords expected to appear in relevant documents.
        
    Returns:
        Score between 0.0 and 1.0.
    """
    if not retrieved_docs:
        return 0.0
    
    if not expected_keywords:
        # If no keywords provided, assume docs are relevant if retrieved
        return 1.0
    
    # Check how many keywords appear in any retrieved document
    combined_content = " ".join(doc.page_content.lower() for doc in retrieved_docs)
    matches = sum(1 for kw in expected_keywords if kw.lower() in combined_content)
    
    return matches / len(expected_keywords)


def calculate_faithfulness_score(
    answer: str,
    retrieved_docs: List[Document],
) -> float:
    """Calculate faithfulness score based on source coverage.
    
    Simple heuristic: checks if answer terms appear in sources.
    For production, use LLM-as-judge or NLI model.
    
    Args:
        answer: The generated answer.
        retrieved_docs: Source documents used for generation.
        
    Returns:
        Score between 0.0 and 1.0.
    """
    if not answer or not retrieved_docs:
        return 0.0
    
    # Get significant words from answer (skip common words)
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", 
                  "being", "have", "has", "had", "do", "does", "did", "will",
                  "would", "could", "should", "may", "might", "must", "shall",
                  "can", "need", "dare", "ought", "used", "to", "of", "in",
                  "for", "on", "with", "at", "by", "from", "as", "into", "through",
                  "during", "before", "after", "above", "below", "between", "under",
                  "again", "further", "then", "once", "here", "there", "when", "where",
                  "why", "how", "all", "each", "few", "more", "most", "other", "some",
                  "such", "no", "nor", "not", "only", "own", "same", "so", "than",
                  "too", "very", "just", "and", "but", "if", "or", "because", "until",
                  "while", "this", "that", "these", "those", "i", "it", "its"}
    
    answer_words = set(word.lower().strip(".,!?") for word in answer.split() 
                       if len(word) > 2 and word.lower() not in stop_words)
    
    if not answer_words:
        return 1.0  # No significant words to check
    
    # Check how many answer words appear in sources
    combined_sources = " ".join(doc.page_content.lower() for doc in retrieved_docs)
    matches = sum(1 for word in answer_words if word in combined_sources)
    
    return matches / len(answer_words)


def evaluate_response(
    question: str,
    answer: str,
    sources: List[dict],
    latency: float,
    expected_answer: Optional[str] = None,
    expected_keywords: Optional[List[str]] = None,
) -> EvaluationResult:
    """Evaluate a RAG response.
    
    Args:
        question: The user question.
        answer: Generated answer.
        sources: Source documents used.
        latency: Response time in seconds.
        expected_answer: Optional ground truth answer.
        expected_keywords: Optional keywords for relevance scoring.
        
    Returns:
        EvaluationResult with all metrics.
    """
    # Convert sources to Documents for scoring
    docs = [
        Document(page_content=s.get("content", ""), metadata=s.get("metadata", {}))
        for s in sources
    ]
    
    relevance = calculate_relevance_score(question, docs, expected_keywords)
    faithfulness = calculate_faithfulness_score(answer, docs)
    
    return EvaluationResult(
        question=question,
        answer=answer,
        expected_answer=expected_answer,
        sources=sources,
        latency_seconds=latency,
        relevance_score=relevance,
        faithfulness_score=faithfulness,
    )

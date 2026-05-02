"""Evaluation runner for RAG system."""

import json
import time
from pathlib import Path
from typing import List, Optional

from src.evaluation.metrics import EvaluationResult, evaluate_response
from src.evaluation.tracker import ExperimentTracker
from src.retrieval import RAGChain
from src.vectorstore import ChromaStore


def load_test_questions(file_path: Path) -> List[dict]:
    """Load test questions from JSON file.
    
    Args:
        file_path: Path to test questions JSON.
        
    Returns:
        List of question dictionaries.
    """
    with open(file_path) as f:
        data = json.load(f)
    return data.get("questions", [])


def run_evaluation(
    vector_store: ChromaStore,
    questions: List[dict],
    tracker: Optional[ExperimentTracker] = None,
    k: int = 4,
) -> List[EvaluationResult]:
    """Run evaluation on a set of questions.
    
    Args:
        vector_store: Initialized vector store with documents.
        questions: List of test questions.
        tracker: Optional MLflow tracker for logging.
        k: Number of documents to retrieve.
        
    Returns:
        List of EvaluationResult objects.
    """
    chain = RAGChain(vector_store=vector_store, k=k)
    results = []
    
    for i, q in enumerate(questions):
        question = q["question"]
        expected_keywords = q.get("expected_keywords", [])
        expected_answer = q.get("expected_answer")
        
        # Time the query
        start = time.perf_counter()
        response = chain.invoke(question)
        latency = time.perf_counter() - start
        
        # Evaluate
        result = evaluate_response(
            question=question,
            answer=response["answer"],
            sources=response["sources"],
            latency=latency,
            expected_answer=expected_answer,
            expected_keywords=expected_keywords,
        )
        
        results.append(result)
        
        # Log to MLflow if tracker provided
        if tracker:
            tracker.log_evaluation(result, step=i)
    
    return results


def run_full_evaluation(
    documents_dir: Path,
    test_questions_path: Path,
    experiment_name: str = "rag-evaluation",
    run_name: Optional[str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    k: int = 4,
) -> List[EvaluationResult]:
    """Run full evaluation pipeline with document ingestion.
    
    Args:
        documents_dir: Directory containing documents to ingest.
        test_questions_path: Path to test questions JSON.
        experiment_name: MLflow experiment name.
        run_name: Optional run name.
        chunk_size: Document chunk size.
        chunk_overlap: Chunk overlap.
        k: Number of documents to retrieve.
        
    Returns:
        List of EvaluationResult objects.
    """
    from src.ingestion import ChunkingConfig, chunk_documents, load_directory
    
    # Initialize tracker
    tracker = ExperimentTracker(experiment_name=experiment_name)
    tracker.start_run(run_name=run_name)
    
    try:
        # Log configuration
        tracker.log_config(
            llm_provider="novita",
            llm_model="meta-llama/llama-3.3-70b-instruct",
            embedding_model="baai/bge-m3",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            k=k,
        )
        
        # Load and chunk documents
        documents = load_directory(documents_dir)
        config = ChunkingConfig(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = chunk_documents(documents, config)
        
        tracker.log_params({
            "num_documents": len(documents),
            "num_chunks": len(chunks),
        })
        
        # Create vector store and add documents
        vector_store = ChromaStore(collection_name="eval_collection")
        vector_store.add_documents(chunks)
        
        # Load questions and run evaluation
        questions = load_test_questions(test_questions_path)
        results = run_evaluation(vector_store, questions, tracker, k)
        
        # Log batch results
        tracker.log_batch_results(results)
        
        # Log detailed results as artifact
        results_data = {
            "results": [r.to_dict() for r in results],
        }
        tracker.log_dict_artifact(results_data, "evaluation_results.json")
        
        return results
        
    finally:
        tracker.end_run()


if __name__ == "__main__":
    # Example usage
    results = run_full_evaluation(
        documents_dir=Path("data/sample_docs"),
        test_questions_path=Path("data/eval/test_questions.json"),
        run_name="sample-evaluation",
    )
    
    print(f"\nEvaluation Results ({len(results)} queries):")
    print("-" * 50)
    
    for r in results:
        print(f"Q: {r.question[:50]}...")
        print(f"  Latency: {r.latency_seconds:.2f}s")
        print(f"  Relevance: {r.relevance_score:.2f}")
        print(f"  Faithfulness: {r.faithfulness_score:.2f}")
        print()

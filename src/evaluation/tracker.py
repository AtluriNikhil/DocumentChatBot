"""MLflow experiment tracking for RAG evaluation."""

import os
from pathlib import Path
from typing import Dict, List, Optional

import mlflow
from mlflow.tracking import MlflowClient

from src.evaluation.metrics import EvaluationResult


class ExperimentTracker:
    """MLflow experiment tracker for RAG evaluation.
    
    Tracks metrics, parameters, and artifacts for RAG experiments.
    """
    
    def __init__(
        self,
        experiment_name: str = "rag-evaluation",
        tracking_uri: Optional[str] = None,
    ):
        """Initialize experiment tracker.
        
        Args:
            experiment_name: Name of the MLflow experiment.
            tracking_uri: MLflow tracking server URI. Defaults to local ./mlruns.
        """
        self.experiment_name = experiment_name
        
        # Set tracking URI
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        else:
            # Default to local directory
            mlruns_path = Path("mlruns").absolute()
            mlflow.set_tracking_uri(f"file://{mlruns_path}")
        
        # Create or get experiment
        self.client = MlflowClient()
        experiment = self.client.get_experiment_by_name(experiment_name)
        
        if experiment is None:
            self.experiment_id = self.client.create_experiment(experiment_name)
        else:
            self.experiment_id = experiment.experiment_id
        
        mlflow.set_experiment(experiment_name)
        self._active_run = None
    
    def start_run(self, run_name: Optional[str] = None, tags: Optional[Dict] = None) -> str:
        """Start a new MLflow run.
        
        Args:
            run_name: Optional name for the run.
            tags: Optional tags to attach to the run.
            
        Returns:
            Run ID.
        """
        self._active_run = mlflow.start_run(run_name=run_name, tags=tags)
        return self._active_run.info.run_id
    
    def end_run(self):
        """End the current MLflow run."""
        if self._active_run:
            mlflow.end_run()
            self._active_run = None
    
    def log_params(self, params: Dict):
        """Log parameters for the current run.
        
        Args:
            params: Dictionary of parameter names and values.
        """
        mlflow.log_params(params)
    
    def log_config(
        self,
        llm_provider: str,
        llm_model: str,
        embedding_model: str,
        chunk_size: int,
        chunk_overlap: int,
        k: int,
    ):
        """Log RAG configuration parameters.
        
        Args:
            llm_provider: LLM provider name.
            llm_model: LLM model name.
            embedding_model: Embedding model name.
            chunk_size: Document chunk size.
            chunk_overlap: Chunk overlap size.
            k: Number of documents to retrieve.
        """
        self.log_params({
            "llm_provider": llm_provider,
            "llm_model": llm_model,
            "embedding_model": embedding_model,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "retrieval_k": k,
        })
    
    def log_evaluation(self, result: EvaluationResult, step: Optional[int] = None):
        """Log evaluation metrics for a single query.
        
        Args:
            result: EvaluationResult containing metrics.
            step: Optional step number for the metric.
        """
        metrics = {
            "latency_seconds": result.latency_seconds,
            "num_sources": len(result.sources),
        }
        
        if result.relevance_score is not None:
            metrics["relevance_score"] = result.relevance_score
        
        if result.faithfulness_score is not None:
            metrics["faithfulness_score"] = result.faithfulness_score
        
        mlflow.log_metrics(metrics, step=step)
    
    def log_batch_results(self, results: List[EvaluationResult]):
        """Log aggregated metrics for a batch of evaluations.
        
        Args:
            results: List of EvaluationResult objects.
        """
        if not results:
            return
        
        # Calculate aggregates
        avg_latency = sum(r.latency_seconds for r in results) / len(results)
        avg_relevance = sum(r.relevance_score or 0 for r in results) / len(results)
        avg_faithfulness = sum(r.faithfulness_score or 0 for r in results) / len(results)
        
        mlflow.log_metrics({
            "avg_latency_seconds": avg_latency,
            "avg_relevance_score": avg_relevance,
            "avg_faithfulness_score": avg_faithfulness,
            "total_queries": len(results),
        })
    
    def log_artifact(self, file_path: str, artifact_path: Optional[str] = None):
        """Log a file as an artifact.
        
        Args:
            file_path: Path to the file to log.
            artifact_path: Optional subdirectory in artifacts.
        """
        mlflow.log_artifact(file_path, artifact_path)
    
    def log_dict_artifact(self, data: Dict, filename: str):
        """Log a dictionary as a JSON artifact.
        
        Args:
            data: Dictionary to log.
            filename: Name for the artifact file.
        """
        import json
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f, indent=2)
            temp_path = f.name
        
        try:
            mlflow.log_artifact(temp_path, "results")
        finally:
            os.unlink(temp_path)
    
    @property
    def run_id(self) -> Optional[str]:
        """Get current run ID."""
        return self._active_run.info.run_id if self._active_run else None

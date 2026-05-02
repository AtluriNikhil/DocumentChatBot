"""Tests for evaluation module."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from src.evaluation import (
    EvaluationResult,
    ExperimentTracker,
    calculate_faithfulness_score,
    calculate_relevance_score,
    evaluate_response,
    load_test_questions,
)


# Fixtures
@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        Document(page_content="Cats are popular pets that require care.", metadata={"source": "pets.txt"}),
        Document(page_content="Dogs are loyal companions and need exercise.", metadata={"source": "pets.txt"}),
    ]


@pytest.fixture
def test_questions_file(tmp_path):
    """Create a temporary test questions file."""
    questions = {
        "description": "Test questions",
        "questions": [
            {"id": "q1", "question": "What pets are mentioned?", "expected_keywords": ["cats", "dogs"]},
            {"id": "q2", "question": "What do dogs need?", "expected_keywords": ["exercise"]},
        ]
    }
    file_path = tmp_path / "test_questions.json"
    file_path.write_text(json.dumps(questions))
    return file_path


# Metrics Tests
class TestCalculateRelevanceScore:
    """Tests for relevance score calculation."""

    def test_relevance_with_matching_keywords(self, sample_documents):
        score = calculate_relevance_score(
            question="What about cats?",
            retrieved_docs=sample_documents,
            expected_keywords=["cats", "dogs"],
        )
        assert score == 1.0  # Both keywords found

    def test_relevance_with_partial_keywords(self, sample_documents):
        score = calculate_relevance_score(
            question="What about birds?",
            retrieved_docs=sample_documents,
            expected_keywords=["cats", "birds"],
        )
        assert score == 0.5  # Only "cats" found

    def test_relevance_with_no_keywords(self, sample_documents):
        score = calculate_relevance_score(
            question="Test question",
            retrieved_docs=sample_documents,
            expected_keywords=None,
        )
        assert score == 1.0  # No keywords = assume relevant

    def test_relevance_with_empty_docs(self):
        score = calculate_relevance_score(
            question="Test",
            retrieved_docs=[],
            expected_keywords=["test"],
        )
        assert score == 0.0


class TestCalculateFaithfulnessScore:
    """Tests for faithfulness score calculation."""

    def test_faithfulness_with_grounded_answer(self, sample_documents):
        answer = "Cats are popular pets."
        score = calculate_faithfulness_score(answer, sample_documents)
        assert score > 0.5  # Most words from sources

    def test_faithfulness_with_ungrounded_answer(self, sample_documents):
        answer = "Elephants live in Africa and Asia."
        score = calculate_faithfulness_score(answer, sample_documents)
        assert score < 0.5  # Few words from sources

    def test_faithfulness_with_empty_answer(self, sample_documents):
        score = calculate_faithfulness_score("", sample_documents)
        assert score == 0.0

    def test_faithfulness_with_empty_docs(self):
        score = calculate_faithfulness_score("Some answer", [])
        assert score == 0.0


class TestEvaluationResult:
    """Tests for EvaluationResult dataclass."""

    def test_to_dict(self):
        result = EvaluationResult(
            question="Test question?",
            answer="Test answer",
            expected_answer=None,
            sources=[{"content": "source", "metadata": {}}],
            latency_seconds=0.5,
            relevance_score=0.8,
            faithfulness_score=0.9,
        )
        
        d = result.to_dict()
        
        assert d["question"] == "Test question?"
        assert d["latency_seconds"] == 0.5
        assert d["relevance_score"] == 0.8
        assert d["num_sources"] == 1


class TestEvaluateResponse:
    """Tests for evaluate_response function."""

    def test_evaluate_response_returns_result(self):
        result = evaluate_response(
            question="What is this?",
            answer="This is a test.",
            sources=[{"content": "This is a test document.", "metadata": {}}],
            latency=0.3,
        )
        
        assert isinstance(result, EvaluationResult)
        assert result.question == "What is this?"
        assert result.latency_seconds == 0.3
        assert result.relevance_score is not None
        assert result.faithfulness_score is not None


# Runner Tests
class TestLoadTestQuestions:
    """Tests for loading test questions."""

    def test_load_questions(self, test_questions_file):
        questions = load_test_questions(test_questions_file)
        
        assert len(questions) == 2
        assert questions[0]["id"] == "q1"
        assert "expected_keywords" in questions[0]


# Tracker Tests
class TestExperimentTracker:
    """Tests for MLflow experiment tracker."""

    @patch("src.evaluation.tracker.mlflow")
    @patch("src.evaluation.tracker.MlflowClient")
    def test_init_creates_experiment(self, mock_client_class, mock_mlflow):
        mock_client = MagicMock()
        mock_client.get_experiment_by_name.return_value = None
        mock_client.create_experiment.return_value = "exp-123"
        mock_client_class.return_value = mock_client
        
        tracker = ExperimentTracker(experiment_name="test-exp")
        
        assert tracker.experiment_name == "test-exp"
        mock_client.create_experiment.assert_called_once_with("test-exp")

    @patch("src.evaluation.tracker.mlflow")
    @patch("src.evaluation.tracker.MlflowClient")
    def test_start_and_end_run(self, mock_client_class, mock_mlflow):
        mock_client = MagicMock()
        mock_client.get_experiment_by_name.return_value = MagicMock(experiment_id="exp-123")
        mock_client_class.return_value = mock_client
        
        mock_run = MagicMock()
        mock_run.info.run_id = "run-456"
        mock_mlflow.start_run.return_value = mock_run
        
        tracker = ExperimentTracker()
        run_id = tracker.start_run(run_name="test-run")
        
        assert run_id == "run-456"
        mock_mlflow.start_run.assert_called_once()
        
        tracker.end_run()
        mock_mlflow.end_run.assert_called_once()

    @patch("src.evaluation.tracker.mlflow")
    @patch("src.evaluation.tracker.MlflowClient")
    def test_log_evaluation(self, mock_client_class, mock_mlflow):
        mock_client = MagicMock()
        mock_client.get_experiment_by_name.return_value = MagicMock(experiment_id="exp-123")
        mock_client_class.return_value = mock_client
        
        tracker = ExperimentTracker()
        
        result = EvaluationResult(
            question="Test?",
            answer="Answer",
            expected_answer=None,
            sources=[],
            latency_seconds=0.5,
            relevance_score=0.8,
            faithfulness_score=0.9,
        )
        
        tracker.log_evaluation(result, step=0)
        
        mock_mlflow.log_metrics.assert_called_once()

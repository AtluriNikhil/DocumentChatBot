"""Tests for prompt templates."""

import pytest

from src.llm.prompts import get_prompts, RAG_PROMPT, RAG_PROMPT_DE


class TestPromptSelection:
    """Tests for language-based prompt selection."""

    def test_get_english_prompts(self):
        prompts = get_prompts("en")
        assert prompts["rag"] == RAG_PROMPT
        assert "context" in prompts["system"]

    def test_get_german_prompts(self):
        prompts = get_prompts("de")
        assert prompts["rag"] == RAG_PROMPT_DE
        assert "Kontext" in prompts["system"]

    def test_default_to_english(self):
        # Unsupported language defaults to English
        prompts = get_prompts("fr")
        assert prompts["rag"] == RAG_PROMPT

    def test_prompts_contain_all_keys(self):
        for lang in ["en", "de"]:
            prompts = get_prompts(lang)
            assert "system" in prompts
            assert "rag" in prompts
            assert "chat" in prompts
            assert "condense" in prompts

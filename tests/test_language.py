"""Tests for language detection utilities."""

import pytest

from src.vectorstore.utils.language import detect_language


class TestLanguageDetection:
    """Tests for language detection."""

    def test_detect_english(self):
        assert detect_language("Hello, how are you?") == "en"
        assert detect_language("The cat sits on the table") == "en"

    def test_detect_german(self):
        assert detect_language("Was ist das?") == "de"
        assert detect_language("Die Katze sitzt auf dem Tisch") == "de"
        assert detect_language("Ich habe eine Frage") == "de"

    def test_default_to_english(self):
        # Short/ambiguous text defaults to English
        assert detect_language("OK") == "en"
        assert detect_language("") == "en"

    def test_mixed_language_detection(self):
        # German-heavy mixed text should detect as German
        assert detect_language("Das ist ein Test mit some English words") == "de"

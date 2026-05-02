"""Language detection utilities."""

from typing import Optional


def detect_language(text: str) -> str:
    """Detect the language of input text.
    
    Uses langdetect library if available, falls back to simple heuristics.
    
    Args:
        text: Input text to analyze.
        
    Returns:
        Language code ("en", "de", etc.). Defaults to "en".
    """
    try:
        from langdetect import detect
        lang = detect(text)
        # Map to supported languages
        if lang == "de":
            return "de"
        return "en"
    except ImportError:
        # Fallback: simple German word detection
        german_indicators = [
            "der", "die", "das", "und", "ist", "sind", "ein", "eine",
            "für", "mit", "auf", "nicht", "ich", "du", "wir", "sie",
            "kann", "wird", "haben", "werden", "über", "nach"
        ]
        words = text.lower().split()
        german_count = sum(1 for w in words if w in german_indicators)
        if german_count >= 2 or (len(words) > 0 and german_count / len(words) > 0.2):
            return "de"
        return "en"
    except Exception:
        return "en"

"""LLM provider implementations for multi-provider support."""

from enum import Enum
from pathlib import Path
from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class LLMProvider(str, Enum):
    """Available LLM providers."""
    NOVITA = "novita"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class LLMSettings(BaseSettings):
    """Settings for LLM configuration."""
    
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")
    
    # Provider selection
    llm_provider: LLMProvider = LLMProvider.NOVITA

    # Novita settings
    novita_api_key: str = ""
    novita_model: str = "meta-llama/llama-3.3-70b-instruct"
    novita_base_url: str = "https://api.novita.ai/openai"
    
    # OpenAI settings
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    
    # Anthropic settings
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    # Ollama settings
    ollama_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"
    
    # Common settings
    temperature: float = 0.0
    max_tokens: int = 1024


def get_llm(settings: Optional[LLMSettings] = None) -> BaseChatModel:
    """Get configured LLM instance.
    
    Args:
        settings: LLM settings. Loads from environment if None.
        
    Returns:
        Configured chat model instance.
        
    Raises:
        ValueError: If required API key not set or provider unknown.
    """
    if settings is None:
        settings = LLMSettings()
    
    if settings.llm_provider == LLMProvider.NOVITA:
        if not settings.novita_api_key:
            raise ValueError("NOVITA_API_KEY not set in environment")

        return ChatOpenAI(
            api_key=settings.novita_api_key,
            base_url=settings.novita_base_url,
            model=settings.novita_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )

    if settings.llm_provider == LLMProvider.OPENAI:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        return ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )
    
    elif settings.llm_provider == LLMProvider.ANTHROPIC:
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")
        
        return ChatAnthropic(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )
    
    elif settings.llm_provider == LLMProvider.OLLAMA:
        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.temperature,
        )
    
    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")


def list_providers() -> list[dict]:
    """List available LLM providers with their default models.
    
    Returns:
        List of provider info dictionaries.
    """
    return [
        {
            "provider": LLMProvider.NOVITA.value,
            "default_model": "meta-llama/llama-3.3-70b-instruct",
            "requires_api_key": True,
        },
        {
            "provider": LLMProvider.OPENAI.value,
            "default_model": "gpt-4o-mini",
            "requires_api_key": True,
        },
        {
            "provider": LLMProvider.ANTHROPIC.value,
            "default_model": "claude-3-5-sonnet-20241022",
            "requires_api_key": True,
        },
        {
            "provider": LLMProvider.OLLAMA.value,
            "default_model": "llama3.2",
            "requires_api_key": False,
        },
    ]

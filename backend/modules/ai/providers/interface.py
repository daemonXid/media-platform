"""
🤖 AI Providers Interface - Public API

This is the ONLY file that should be imported from outside this module.
Implements the provider switching strategy:

    HuggingFace (Free) → DeepSeek (Quality/Korean) → OpenRouter (Multi)

Usage:
    from modules.ai.providers.interface import get_ai_client, AIResponse

    client = get_ai_client()
    response = client.complete("Hello!")
    print(response.text)

    # Or with specific provider
    from modules.ai.providers.interface import get_provider
    hf = get_provider("huggingface")
    ds = get_provider("deepseek")

Environment:
    AI_PROVIDER: Active provider (huggingface | deepseek | openrouter)
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import TypeVar

from pydantic import BaseModel

from .base import AIProviderBase, AIResponse, StructuredResponse
from .deepseek import DeepSeekProvider
from .huggingface import HuggingFaceProvider
from .openrouter import OpenRouterProvider

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

# Available providers
PROVIDERS: dict[str, type[AIProviderBase]] = {
    "huggingface": HuggingFaceProvider,
    "deepseek": DeepSeekProvider,
    "openrouter": OpenRouterProvider,
}


@lru_cache(maxsize=3)
def get_provider(name: str) -> AIProviderBase:
    """
    Get a specific AI provider by name.

    Args:
        name: Provider name (huggingface, deepseek, openrouter)

    Returns:
        AIProviderBase instance

    Raises:
        ValueError: If provider name is unknown
    """
    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {name}. Available: {list(PROVIDERS.keys())}")

    provider_class = PROVIDERS[name]
    return provider_class()


def get_ai_client() -> AIProviderBase:
    """
    Get the currently configured AI client.

    Uses AI_PROVIDER environment variable to determine which provider to use.
    Falls back through providers if the primary is not available.

    Strategy:
        1. Try configured provider (AI_PROVIDER env var)
        2. Fallback to HuggingFace (free)
        3. Final fallback to any available provider

    Returns:
        AIProviderBase instance
    """
    configured = os.getenv("AI_PROVIDER", "huggingface").lower()

    # Try configured provider first
    if configured in PROVIDERS:
        provider = get_provider(configured)
        if provider.is_available():
            logger.info(f"Using AI provider: {configured}")
            return provider
        logger.warning(f"Configured provider '{configured}' is not available")

    # Fallback chain
    fallback_order = ["huggingface", "deepseek", "openrouter"]

    for name in fallback_order:
        if name == configured:
            continue  # Already tried
        try:
            provider = get_provider(name)
            if provider.is_available():
                logger.info(f"Falling back to AI provider: {name}")
                return provider
        except Exception:
            continue

    # Return configured provider even if not available (will return empty responses)
    logger.error("No AI providers available. Returning dummy provider.")
    return get_provider("huggingface")


# Convenience function for quick completions
def complete(
    prompt: str,
    model: str | None = None,
    provider: str | None = None,
    temperature: float = 0.7,
) -> AIResponse:
    """
    Quick text completion using configured or specified provider.

    Args:
        prompt: Input prompt
        model: Optional model name
        provider: Optional provider name
        temperature: Creativity (0.0-1.0)

    Returns:
        AIResponse
    """
    client = get_provider(provider) if provider else get_ai_client()
    return client.complete(prompt=prompt, model=model, temperature=temperature)


def complete_structured(
    prompt: str,
    schema: type[T],
    provider: str | None = None,
    temperature: float = 0.3,
) -> StructuredResponse[T]:
    """
    Quick structured completion using configured or specified provider.

    Args:
        prompt: Input prompt
        schema: Pydantic model class for validation
        provider: Optional provider name
        temperature: Creativity (lower recommended)

    Returns:
        StructuredResponse[T]
    """
    client = get_provider(provider) if provider else get_ai_client()
    return client.complete_structured(prompt=prompt, schema=schema, temperature=temperature)


# --- Pydantic AI Agents (v4.0) ---
from .agents.architect import get_architect_agent
from .agents.base import AgentContext

# Re-export for convenience
__all__ = [
    "PROVIDERS",
    "AIProviderBase",
    "AIResponse",
    "AgentContext",
    "DeepSeekProvider",
    "HuggingFaceProvider",
    "OpenRouterProvider",
    "StructuredResponse",
    "complete",
    "complete_structured",
    "get_ai_client",
    "get_architect_agent",
    "get_provider",
]

"""
🌐 OpenRouter Provider - Multi-Model Gateway

Tertiary provider for accessing multiple AI models through one API.
Access GPT-4, Claude, Gemini, Llama, and more via unified interface.

Environment:
    OPENROUTER_API_KEY: Your OpenRouter API key

Models (examples):
    - openai/gpt-4-turbo
    - anthropic/claude-3-opus
    - google/gemini-pro
    - meta-llama/llama-3-70b-instruct
    - mistralai/mistral-medium

See full list: https://openrouter.ai/models
"""

from __future__ import annotations

import json
import logging
import os
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from .base import AIProviderBase, AIResponse, StructuredResponse

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class OpenRouterProvider(AIProviderBase):
    """
    OpenRouter API provider.

    Access multiple AI models through one unified API.
    Great for testing different models and production flexibility.
    """

    provider_name = "openrouter"
    base_url = "https://openrouter.ai/api/v1"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = "mistralai/mistral-7b-instruct",
        site_url: str = "https://daemon-one.dev",
        site_name: str = "DAEMON-ONE",
    ):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.default_model = default_model
        self.site_url = site_url
        self.site_name = site_name
        self._client = None

    def _get_client(self):
        """Lazy-load OpenAI-compatible client for OpenRouter."""
        if self._client is None and self.api_key:
            try:
                from openai import OpenAI

                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    default_headers={
                        "HTTP-Referer": self.site_url,
                        "X-Title": self.site_name,
                    },
                )
            except ImportError:
                logger.warning("openai not installed. Run: uv add openai")
        return self._client

    def is_available(self) -> bool:
        return bool(self.api_key)

    def complete(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> AIResponse:
        """Generate text using OpenRouter API."""
        client = self._get_client()
        if not client:
            return AIResponse(
                text="",
                model=model or self.default_model,
                provider=self.provider_name,
            )

        model = model or self.default_model

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return AIResponse(
                text=response.choices[0].message.content or "",
                model=response.model,
                provider=self.provider_name,
                usage={
                    "input": response.usage.prompt_tokens if response.usage else 0,
                    "output": response.usage.completion_tokens if response.usage else 0,
                },
                raw=response,
            )
        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
            return AIResponse(text="", model=model, provider=self.provider_name)

    def complete_structured(
        self,
        prompt: str,
        schema: type[T],
        model: str | None = None,
        temperature: float = 0.3,
    ) -> StructuredResponse[T]:
        """Generate structured JSON output."""
        schema_json = schema.model_json_schema()
        enhanced_prompt = f"""
{prompt}

Respond ONLY with valid JSON matching this schema:
{json.dumps(schema_json, indent=2)}

Do not include any text before or after the JSON.
"""
        response = self.complete(prompt=enhanced_prompt, model=model, temperature=temperature)

        if response.is_empty:
            return StructuredResponse(
                data=None,
                raw_text=response.text,
                error="Empty response from AI",
            )

        try:
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            json_data = json.loads(text)
        except json.JSONDecodeError as e:
            return StructuredResponse(
                data=None,
                raw_text=response.text,
                error=f"Invalid JSON: {e}",
            )

        try:
            validated = schema.model_validate(json_data)
            return StructuredResponse(data=validated, raw_text=response.text)
        except ValidationError as e:
            return StructuredResponse(
                data=None,
                raw_text=response.text,
                error=f"Schema validation failed: {e}",
            )

    def embed(self, text: str) -> list[float]:
        """Generate text embedding using OpenRouter."""
        client = self._get_client()
        if not client:
            return []

        try:
            response = client.embeddings.create(
                model="openai/text-embedding-3-small",
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenRouter embedding error: {e}")
            return []


# Convenience aliases for popular models
MODELS = {
    "gpt4": "openai/gpt-4-turbo",
    "gpt35": "openai/gpt-3.5-turbo",
    "claude3": "anthropic/claude-3-opus",
    "claude3_sonnet": "anthropic/claude-3-sonnet",
    "gemini": "google/gemini-pro",
    "llama3": "meta-llama/llama-3-70b-instruct",
    "mistral": "mistralai/mistral-medium",
    "mixtral": "mistralai/mixtral-8x22b-instruct",
}

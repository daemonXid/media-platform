"""
🇨🇳 DeepSeek Provider - High Quality & Korean Support

Secondary provider for high-quality responses and Korean language.
Cost-effective alternative to GPT-4 with excellent Korean support.

Environment:
    DEEPSEEK_API_KEY: Your DeepSeek API key

Models:
    - deepseek-chat (default, best for Korean)
    - deepseek-coder (for code generation)
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


class DeepSeekProvider(AIProviderBase):
    """
    DeepSeek API provider.

    Excellent for Korean language and high-quality responses.
    More cost-effective than OpenAI GPT-4.
    """

    provider_name = "deepseek"
    base_url = "https://api.deepseek.com/v1"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = "deepseek-chat",
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.default_model = default_model
        self._client = None

    def _get_client(self):
        """Lazy-load OpenAI-compatible client for DeepSeek."""
        if self._client is None and self.api_key:
            try:
                from openai import OpenAI

                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
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
        """Generate text using DeepSeek API."""
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
            logger.error(f"DeepSeek error: {e}")
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
        """DeepSeek does not provide embedding API. Returns empty list."""
        logger.warning("DeepSeek does not support embeddings. Use HuggingFace instead.")
        return []

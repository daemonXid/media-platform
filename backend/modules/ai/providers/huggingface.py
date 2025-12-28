"""
🤗 HuggingFace Provider - Free Tier AI

Primary provider for cost-effective AI operations.
Uses HuggingFace Inference API (free tier available).

Environment:
    HUGGINGFACE_API_KEY: Your HuggingFace API token

Models:
    - mistralai/Mistral-7B-Instruct-v0.3 (default)
    - google/gemma-7b-it
    - meta-llama/Llama-2-7b-chat-hf
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


class HuggingFaceProvider(AIProviderBase):
    """
    HuggingFace Inference API provider.

    Free tier with rate limits. Good for development and low-cost operations.
    """

    provider_name = "huggingface"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = "mistralai/Mistral-7B-Instruct-v0.3",
    ):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.default_model = default_model
        self._client = None

    def _get_client(self):
        """Lazy-load the HuggingFace client."""
        if self._client is None and self.api_key:
            try:
                from huggingface_hub import InferenceClient

                self._client = InferenceClient(token=self.api_key)
            except ImportError:
                logger.warning("huggingface_hub not installed. Run: uv add huggingface_hub")
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
        """Generate text using HuggingFace Inference API."""
        client = self._get_client()
        if not client:
            return AIResponse(
                text="",
                model=model or self.default_model,
                provider=self.provider_name,
            )

        model = model or self.default_model

        try:
            response = client.text_generation(
                prompt,
                model=model,
                max_new_tokens=max_tokens,
                temperature=temperature,
                return_full_text=False,
            )
            return AIResponse(
                text=response,
                model=model,
                provider=self.provider_name,
            )
        except Exception as e:
            logger.error(f"HuggingFace error: {e}")
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
        """Generate text embedding using HuggingFace."""
        client = self._get_client()
        if not client:
            return []

        try:
            result = client.feature_extraction(
                text,
                model="sentence-transformers/all-MiniLM-L6-v2",
            )
            # Result is nested, flatten if needed
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], list):
                    return result[0]
                return result
            return []
        except Exception as e:
            logger.error(f"HuggingFace embedding error: {e}")
            return []

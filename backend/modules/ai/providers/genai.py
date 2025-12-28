"""
🤖 Gen AI Client - Generative AI Integration

"Data-Driven UI" Pattern implementation.
AI generates ONLY structured data (JSON), never raw HTML.

Supports:
- Google Gemini (Primary)
- OpenAI GPT (Secondary)

Usage:
    from modules.cortex.interface import GenAIClient, GenAIResponse

    client = GenAIClient()

    # Simple completion
    response = client.complete("Explain HTMX in 3 sentences")
    print(response.text)

    # Structured output with Pydantic
    from pydantic import BaseModel

    class AnalysisResult(BaseModel):
        score: float
        summary: str
        tags: list[str]

    result = client.complete_structured(
        "Analyze this biomechanics video",
        schema=AnalysisResult,
    )
    print(result.score, result.summary)

Security:
    - AI output is UNTRUSTED DATA
    - Always validate with strict Pydantic schema
    - Never render AI output as raw HTML
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


# ============================================
# 📊 Response Types
# ============================================


@dataclass
class GenAIResponse:
    """Response from Gen AI API."""

    text: str
    model: str
    usage: dict[str, int] = field(default_factory=dict)
    raw: Any = None

    @property
    def is_empty(self) -> bool:
        return not self.text.strip()

    def to_json(self) -> dict | None:
        """Try to parse response as JSON."""
        try:
            return json.loads(self.text)
        except json.JSONDecodeError:
            return None


@dataclass
class StructuredResponse(Generic[T]):
    """Structured response with Pydantic validation."""

    data: T | None
    raw_text: str
    error: str | None = None

    @property
    def is_valid(self) -> bool:
        return self.data is not None and self.error is None


# ============================================
# 🤖 Gen AI Client
# ============================================


class GenAIClient:
    """
    Unified Generative AI client.

    Supports Google Gemini and OpenAI with automatic fallback.
    Implements "Data-Driven UI" pattern with strict schema validation.

    Environment Variables:
        GEMINI_API_KEY: Google Gemini API key (primary)
        OPENAI_API_KEY: OpenAI API key (fallback)

    Example:
        client = GenAIClient()

        # Simple text
        response = client.complete("Hello!")

        # With schema
        result = client.complete_structured(
            "Analyze...",
            schema=MySchema,
        )
    """

    def __init__(
        self,
        gemini_key: str | None = None,
        openai_key: str | None = None,
        default_model: str = "gemini-1.5-flash",
    ):
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY")
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        self.default_model = default_model

        self._gemini_client = None
        self._openai_client = None

    def _get_gemini(self) -> Any:
        """Get or create Gemini client."""
        if self._gemini_client is None and self.gemini_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.gemini_key)
                self._gemini_client = genai
            except ImportError:
                logger.warning("google-generativeai not installed. Run: uv add google-generativeai")
        return self._gemini_client

    def _get_openai(self) -> Any:
        """Get or create OpenAI client."""
        if self._openai_client is None and self.openai_key:
            try:
                from openai import OpenAI

                self._openai_client = OpenAI(api_key=self.openai_key)
            except ImportError:
                logger.warning("openai not installed. Run: uv add openai")
        return self._openai_client

    def complete(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> GenAIResponse:
        """
        Generate text completion.

        Args:
            prompt: Input prompt
            model: Model name (defaults to gemini-1.5-flash)
            temperature: Creativity (0.0-1.0)
            max_tokens: Maximum response length

        Returns:
            GenAIResponse with text
        """
        model = model or self.default_model

        # Try Gemini first
        if "gemini" in model.lower():
            gemini = self._get_gemini()
            if gemini:
                try:
                    gen_model = gemini.GenerativeModel(model)
                    response = gen_model.generate_content(
                        prompt,
                        generation_config={
                            "temperature": temperature,
                            "max_output_tokens": max_tokens,
                        },
                    )
                    return GenAIResponse(
                        text=response.text,
                        model=model,
                        usage={},
                        raw=response,
                    )
                except Exception as e:
                    logger.error(f"Gemini error: {e}")

        # Fallback to OpenAI
        openai = self._get_openai()
        if openai:
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo" if "gemini" in model.lower() else model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return GenAIResponse(
                    text=response.choices[0].message.content or "",
                    model=response.model,
                    usage={
                        "input": response.usage.prompt_tokens if response.usage else 0,
                        "output": response.usage.completion_tokens if response.usage else 0,
                    },
                    raw=response,
                )
            except Exception as e:
                logger.error(f"OpenAI error: {e}")

        return GenAIResponse(text="", model=model, usage={})

    def complete_structured(
        self,
        prompt: str,
        schema: type[T],
        model: str | None = None,
        temperature: float = 0.3,  # Lower for structured output
    ) -> StructuredResponse[T]:
        """
        Generate structured output validated by Pydantic schema.

        This implements the "Data-Driven UI" pattern:
        - AI generates JSON only
        - Output is validated against strict schema
        - Invalid output is rejected, not rendered

        Args:
            prompt: Input prompt
            schema: Pydantic model class for validation
            model: Model name
            temperature: Creativity (lower recommended)

        Returns:
            StructuredResponse with validated data or error

        Example:
            class ArticleSummary(BaseModel):
                title: str
                summary: str
                keywords: list[str]

            result = client.complete_structured(
                "Summarize this article...",
                schema=ArticleSummary,
            )

            if result.is_valid:
                print(result.data.title)
        """
        # Generate schema description
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

        # Parse JSON
        try:
            # Handle potential markdown code blocks
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

        # Validate with Pydantic
        try:
            validated = schema.model_validate(json_data)
            return StructuredResponse(
                data=validated,
                raw_text=response.text,
            )
        except ValidationError as e:
            return StructuredResponse(
                data=None,
                raw_text=response.text,
                error=f"Schema validation failed: {e}",
            )

    def embed(self, text: str) -> list[float]:
        """
        Generate text embedding.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        gemini = self._get_gemini()
        if gemini:
            try:
                result = gemini.embed_content(
                    model="models/embedding-001",
                    content=text,
                )
                return result["embedding"]
            except Exception as e:
                logger.error(f"Embedding error: {e}")

        return []

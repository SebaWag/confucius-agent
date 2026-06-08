"""Qwen Cloud API Client — with automatic fallback for development.

Uses OpenAI-compatible SDK. Switches between Qwen Cloud and fallback
APIs based on configuration. Drop-in compatible with any OpenAI endpoint.
"""

from typing import Optional
from openai import OpenAI
from confucius.config import settings


class QwenClient:
    """Unified client: Qwen Cloud (production) or fallback API (development)."""

    def __init__(self):
        self._client = None
        self._current_mode = None

    @property
    def client(self) -> OpenAI:
        """Get or recreate the OpenAI-compatible client."""
        mode = settings.api_mode
        api_key = settings.active_api_key
        base_url = settings.active_base_url

        if (self._client is None or self._current_mode != mode):
            self._client = OpenAI(api_key=api_key, base_url=base_url)
            self._current_mode = mode
        return self._client

    @property
    def model(self) -> str:
        return settings.active_model

    def chat(self, messages: list[dict], temperature: float = 0.3,
             max_tokens: Optional[int] = None, tools: Optional[list] = None):
        """Send a chat completion request."""
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        return self.client.chat.completions.create(**kwargs)

    def embed(self, text: str) -> list[float]:
        """Generate text embeddings."""
        resp = self.client.embeddings.create(
            model=settings.qwen_embedding_model,
            input=text,
        )
        return resp.data[0].embedding

    def switch_to_qwen(self):
        """Switch to Qwen Cloud API."""
        if settings.qwen_api_key:
            settings.api_mode = "qwen"
            self._client = None  # Will recreate on next call
            return True
        return False

    def switch_to_fallback(self):
        """Switch to fallback API (for development)."""
        settings.api_mode = "fallback"
        self._client = None
        return True


# Singleton instance
qwen = QwenClient()

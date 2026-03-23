"""
openrouter_client.py — OpenRouter API wrapper with streaming support.

OpenRouter exposes an OpenAI-compatible API, so we use the openai SDK
with a custom base_url and the required extra headers.
"""

from typing import Iterator

import openai


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1"
    SITE_URL = "https://github.com/ahmedvirani010-art/Investments-"
    SITE_NAME = "PSX Investment Agent"

    def __init__(self, api_key: str) -> None:
        self.client = openai.OpenAI(
            base_url=self.BASE_URL,
            api_key=api_key,
            default_headers={
                "HTTP-Referer": self.SITE_URL,
                "X-Title": self.SITE_NAME,
            },
        )

    def stream_chat(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.7,
    ) -> Iterator[str]:
        """
        Stream response tokens from OpenRouter.

        Args:
            model: OpenRouter model ID (e.g. 'anthropic/claude-3.5-sonnet')
            messages: List of {"role": ..., "content": ...} dicts
            temperature: Sampling temperature (0.0–1.0)

        Yields:
            Text delta strings as they arrive.
        """
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield delta

    def list_models(self) -> list[dict]:
        """Fetch available models from OpenRouter (optional utility)."""
        response = self.client.models.list()
        return [{"id": m.id} for m in response.data]

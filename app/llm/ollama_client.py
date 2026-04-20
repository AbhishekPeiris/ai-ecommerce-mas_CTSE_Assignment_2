from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from app.llm.model_config import ModelConfig, get_model_config
from app.utils.error_handler import LLMConnectionError, LLMResponseError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """
    Minimal Ollama HTTP client for local model interaction.
    """

    def __init__(self, config: ModelConfig | None = None) -> None:
        self.config = config or get_model_config()

    def health_check(self) -> bool:
        """
        Check whether the Ollama server is reachable.

        Returns:
            bool: True if reachable, otherwise False.
        """
        try:
            url = f"{self.config.base_url}/api/tags"
            request = urllib.request.Request(url=url, method="GET")
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                return response.status == 200
        except Exception as exc:
            logger.error("Ollama health check failed: %s", exc)
            return False

    def generate(self, prompt: str, system: str | None = None) -> str:
        """
        Generate a response from the Ollama model.

        Args:
            prompt: User/content prompt.
            system: Optional system prompt.

        Returns:
            str: Model response text.

        Raises:
            LLMConnectionError: If the Ollama server cannot be reached.
            LLMResponseError: If the response is invalid.
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        payload: dict[str, Any] = {
            "model": self.config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
            },
        }

        if system and system.strip():
            payload["system"] = system.strip()

        url = f"{self.config.base_url}/api/generate"
        request = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            logger.info("Calling Ollama model '%s'", self.config.model_name)
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                raw_body = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            logger.error("Failed to connect to Ollama: %s", exc)
            raise LLMConnectionError("Could not connect to Ollama server.") from exc
        except Exception as exc:
            logger.error("Unexpected Ollama connection error: %s", exc)
            raise LLMConnectionError("Unexpected error while connecting to Ollama.") from exc

        try:
            parsed = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON from Ollama: %s", raw_body)
            raise LLMResponseError("Ollama returned invalid JSON.") from exc

        response_text = parsed.get("response", "")
        if not isinstance(response_text, str) or not response_text.strip():
            raise LLMResponseError("Ollama response text is missing or empty.")

        return response_text.strip()
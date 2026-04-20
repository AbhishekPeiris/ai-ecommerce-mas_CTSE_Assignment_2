from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Optional

from app.llm.model_config import ModelConfig, get_model_config
from app.utils.error_handler import LLMConnectionError, LLMResponseError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """
    Production-ready Ollama HTTP client for local LLM interaction.
    """

    def __init__(self, config: Optional[ModelConfig] = None) -> None:
        self.config = config or get_model_config()
        self.base_url = self.config.base_url.rstrip("/")

    # -------------------------------
    # Health Check
    # -------------------------------
    def health_check(self) -> bool:
        """
        Check whether the Ollama server is reachable.
        """
        try:
            url = f"{self.base_url}/api/tags"
            request = urllib.request.Request(url=url, method="GET")

            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                if response.status == 200:
                    logger.info("Ollama server is healthy.")
                    return True

        except Exception as exc:
            logger.error("Ollama health check failed: %s", exc)

        return False

    # -------------------------------
    # Generate Response
    # -------------------------------
    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Generate response from Ollama model with retry logic.
        """

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        payload: dict[str, Any] = {
            "model": self.config.model_name,
            "prompt": prompt.strip(),
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
            },
        }

        if system and system.strip():
            payload["system"] = system.strip()

        url = f"{self.base_url}/api/generate"

        # Retry mechanism
        retries = 2
        for attempt in range(retries + 1):

            try:
                logger.info(
                    "Calling Ollama model='%s' (attempt %d)",
                    self.config.model_name,
                    attempt + 1,
                )

                request = urllib.request.Request(
                    url=url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )

                with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                    raw_body = response.read().decode("utf-8")

                # Parse response
                parsed = json.loads(raw_body)

                response_text = parsed.get("response", "")

                if not isinstance(response_text, str) or not response_text.strip():
                    raise LLMResponseError("Ollama returned empty response.")

                logger.info("Ollama response received successfully.")
                return response_text.strip()

            except urllib.error.URLError as exc:
                logger.warning("Connection attempt %d failed: %s", attempt + 1, exc)

                if attempt == retries:
                    logger.error("All retries failed. Ollama unreachable.")
                    raise LLMConnectionError(
                        "Could not connect to Ollama server."
                    ) from exc

                time.sleep(1)  # retry delay

            except json.JSONDecodeError as exc:
                logger.error("Invalid JSON response from Ollama.")
                raise LLMResponseError("Invalid JSON returned by Ollama.") from exc

            except Exception as exc:
                logger.error("Unexpected error during Ollama call: %s", exc)
                raise LLMResponseError("Unexpected error from Ollama.") from exc

        # fallback (should never reach)
        raise LLMResponseError("Failed to generate response from Ollama.")

    # -------------------------------
    # ⚡ Quick Generate (No System Prompt)
    # -------------------------------
    def quick_generate(self, prompt: str) -> str:
        """
        Shortcut method for simple generation.
        """
        return self.generate(prompt=prompt)
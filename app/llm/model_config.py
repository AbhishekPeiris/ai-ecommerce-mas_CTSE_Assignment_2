from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    """
    Immutable configuration for the local Ollama model.
    """

    base_url: str
    model_name: str
    temperature: float
    top_p: float
    timeout_seconds: int


def get_model_config() -> ModelConfig:
    """
    Read model configuration from environment variables.

    Returns:
        ModelConfig: Parsed model configuration.
    """
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()
    model_name = os.getenv("OLLAMA_MODEL", "llama3").strip()
    temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.2"))
    top_p = float(os.getenv("OLLAMA_TOP_P", "0.9"))
    timeout_seconds = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))

    return ModelConfig(
        base_url=base_url,
        model_name=model_name,
        temperature=temperature,
        top_p=top_p,
        timeout_seconds=timeout_seconds,
    )
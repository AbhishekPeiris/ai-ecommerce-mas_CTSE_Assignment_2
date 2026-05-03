from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# This module defines custom exceptions and error handling utilities for the MAS application.
class AppError(Exception):
    """
    Base application exception.
    """


class ConfigurationError(AppError):
    """
    Raised when application configuration is invalid.
    """


class DataLoadError(AppError):
    """
    Raised when dataset loading fails.
    """


class ValidationError(AppError):
    """
    Raised when user input or internal data fails validation.
    """


class LLMConnectionError(AppError):
    """
    Raised when connection to Ollama fails.
    """


class LLMResponseError(AppError):
    """
    Raised when Ollama returns an invalid response.
    """


@dataclass
class ErrorResponse:
    """
    Structured error response container.
    """

    error_type: str
    message: str
    details: dict[str, Any] | None = None


def build_error_response(
    error_type: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> ErrorResponse:
    """
    Build a structured error response.

    Args:
        error_type: Error category name.
        message: Human-readable error message.
        details: Optional contextual details.

    Returns:
        ErrorResponse: Structured error payload.
    """
    return ErrorResponse(
        error_type=error_type,
        message=message,
        details=details,
    )


def format_exception_message(exc: Exception) -> str:
    """
    Convert an exception into a safe readable message.

    Args:
        exc: Exception instance.

    Returns:
        str: Readable error message.
    """
    return f"{exc.__class__.__name__}: {str(exc)}".strip()
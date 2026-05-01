from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from app.utils.constants import ERROR_LOG_FILE, LOG_DIR, SYSTEM_LOG_FILE

_LOGGING_INITIALIZED = False


def _ensure_log_files_exist() -> None:
    """
    Ensure the logs directory and files exist.
    """
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    Path(SYSTEM_LOG_FILE).touch(exist_ok=True)
    Path(ERROR_LOG_FILE).touch(exist_ok=True)


def setup_logging() -> None:
    """
    Configure application logging once.
    """
    global _LOGGING_INITIALIZED
    if _LOGGING_INITIALIZED:
        return

    _ensure_log_files_exist()

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
            "file_system": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "detailed",
                "filename": SYSTEM_LOG_FILE,
                "encoding": "utf-8",
            },
            "file_error": {
                "class": "logging.FileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": ERROR_LOG_FILE,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file_system", "file_error"],
        },
    }

    logging.config.dictConfig(logging_config)
    _LOGGING_INITIALIZED = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.

    Args:
        name: Logger name.

    Returns:
        logging.Logger: Configured logger.
    """
    setup_logging()
    return logging.getLogger(name)


def log_agent_event(agent_name: str, action: str, details: str) -> None:
    """
    Log a standardized agent event.

    Args:
        agent_name: Name of the agent.
        action: Action being performed.
        details: Event details.
    """
    logger = get_logger(f"agent.{agent_name}")
    logger.info("[AGENT] %s | %s | %s", agent_name, action, details)


def log_tool_event(tool_name: str, action: str, details: str) -> None:
    """
    Log a standardized tool event.

    Args:
        tool_name: Name of the tool.
        action: Tool action.
        details: Event details.
    """
    logger = get_logger(f"tool.{tool_name}")
    logger.info("[TOOL] %s | %s | %s", tool_name, action, details)
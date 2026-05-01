from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def ensure_directory(path: str | Path) -> Path:
    """
    Ensure a directory exists.

    Args:
        path: Directory path.

    Returns:
        Path: Resolved directory path.
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def load_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    """
    Load a JSON file containing a list of records.

    Args:
        file_path: Path to the JSON file.

    Returns:
        list[dict[str, Any]]: Parsed records.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If JSON is invalid or not a list.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"Expected a list of records in: {path}")

    return data


def save_json_file(file_path: str | Path, data: Any) -> None:
    """
    Save serializable data to a JSON file.

    Args:
        file_path: Destination file path.
        data: JSON serializable data.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def normalize_text(text: str) -> str:
    """
    Normalize text for easier matching.

    Args:
        text: Input text.

    Returns:
        str: Lowercased normalized text.
    """
    return re.sub(r"\s+", " ", text.strip().lower())


def extract_budget(text: str) -> int | None:
    """
    Extract a likely budget from text.

    Supports examples like:
    - under 150000
    - below 120000
    - 100000 budget
    - 150k

    Args:
        text: Input query.

    Returns:
        int | None: Extracted budget if found.
    """
    normalized = normalize_text(text)

    match_k = re.search(r"(\d+)\s*k\b", normalized)
    if match_k:
        return int(match_k.group(1)) * 1000

    numbers = re.findall(r"\d{4,7}", normalized)
    if numbers:
        return int(numbers[0])

    return None


def detect_category(text: str) -> str | None:
    """
    Detect product category from text.

    Args:
        text: User query text.

    Returns:
        str | None: 'laptop', 'phone', or None.
    """
    normalized = normalize_text(text)

    if any(keyword in normalized for keyword in ["laptop", "notebook", "pc"]):
        return "laptop"

    if any(keyword in normalized for keyword in ["phone", "mobile", "smartphone"]):
        return "phone"

    return None


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float.

    Args:
        value: Input value.
        default: Fallback value.

    Returns:
        float: Parsed float or default.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to int.

    Args:
        value: Input value.
        default: Fallback value.

    Returns:
        int: Parsed int or default.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
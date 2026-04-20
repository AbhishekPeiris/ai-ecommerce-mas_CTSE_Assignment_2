from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.utils.helpers import detect_category, extract_budget, normalize_text


@dataclass
class ParsedQuery:
    raw_query: str
    normalized_query: str
    category: str | None
    budget: int | None
    keywords: list[str]


class QueryParser:
    """
    Parses user input into structured query components.
    """

    def parse(self, query: str) -> ParsedQuery:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        normalized = normalize_text(query)

        category = detect_category(normalized)
        budget = extract_budget(normalized)

        keywords = self._extract_keywords(normalized)

        return ParsedQuery(
            raw_query=query,
            normalized_query=normalized,
            category=category,
            budget=budget,
            keywords=keywords,
        )

    def _extract_keywords(self, text: str) -> list[str]:
        """
        Extract simple keywords from text.

        NOTE: This can later be replaced with NLP or embeddings.
        """
        tokens = text.split()
        stop_words = {"a", "the", "for", "with", "and", "or", "under"}

        return [t for t in tokens if t not in stop_words and len(t) > 2]
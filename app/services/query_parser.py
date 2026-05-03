from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from app.utils.helpers import detect_category, extract_budget, normalize_text


@dataclass
class ParsedQuery:
    raw_query: str
    normalized_query: str
    category: str | None
    budget: int | None
    keywords: list[str]

# Heuristic parser for category, budget, and keyword extraction.
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
        stop_words = {
            "a",
            "an",
            "the",
            "for",
            "with",
            "and",
            "or",
            "under",
            "below",
            "best",
            "top",
            "good",
            "cheap",
            "budget",
            "find",
            "show",
            "need",
            "want",
            "me",
        }
        category_terms = {"laptop", "notebook", "pc", "phone", "mobile", "smartphone"}

        cleaned: list[str] = []
        for token in tokens:
            if token in stop_words or token in category_terms:
                continue
            if re.fullmatch(r"\d+k?", token):
                continue
            if len(token) <= 2:
                continue
            cleaned.append(token)

        return cleaned
from __future__ import annotations

import re
from typing import Any, List

from app.utils.helpers import load_json_file
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProductSearchTool:
    """
    Handles product retrieval and filtering.
    """

    def __init__(self, data_path: str) -> None:
        self.data_path = data_path

    def search(
        self,
        category: str | None = None,
        budget: int | None = None,
        keywords: List[str] | None = None,
    ) -> List[dict[str, Any]]:
        logger.info("Searching products")

        products = load_json_file(self.data_path)

        filtered = []

        for product in products:
            if category and product.get("category") != category:
                continue

            if budget and product.get("price", 0) > budget:
                continue

            if keywords and not self._match_keywords(product, keywords):
                continue

            filtered.append(product)

        # If no products found using the budget filter, relax the budget
        # constraint and return the cheapest matching items (up to 5).
        if not filtered and budget is not None:
            logger.info("No products matched budget=%s — relaxing budget filter", budget)
            relaxed: List[dict[str, Any]] = []
            for product in products:
                if category and product.get("category") != category:
                    continue
                if keywords and not self._match_keywords(product, keywords):
                    continue
                relaxed.append(product)

            # sort by price ascending and return top 5
            relaxed.sort(key=lambda p: p.get("price", float("inf")))
            logger.info("Found %d matching products after relaxing budget", len(relaxed))
            return relaxed[:5]

        # If no products found and keywords were provided, relax keyword filter
        if not filtered and keywords:
            logger.info("No products matched keywords=%s — relaxing keyword filter", keywords)
            relaxed: List[dict[str, Any]] = []
            for product in products:
                if category and product.get("category") != category:
                    continue
                if budget and product.get("price", 0) > budget:
                    continue
                relaxed.append(product)

            # sort by price ascending and return top 5
            relaxed.sort(key=lambda p: p.get("price", float("inf")))
            logger.info("Found %d matching products after relaxing keywords", len(relaxed))
            return relaxed[:5]

        logger.info("Found %d matching products", len(filtered))
        return filtered

    def _match_keywords(self, product: dict, keywords: List[str]) -> bool:
        meaningful_keywords = self._sanitize_keywords(keywords)
        if not meaningful_keywords:
            return True

        text = " ".join(
            [
                str(product.get("category", "")),
                str(product.get("brand", "")),
                str(product.get("model", "")),
                str(product.get("processor", "")),
                str(product.get("storage_type", "")),
                " ".join(product.get("use_case", [])),
            ]
        ).lower()

        return any(k in text for k in meaningful_keywords)

    def _sanitize_keywords(self, keywords: List[str]) -> List[str]:
        noise_terms = {
            "best",
            "top",
            "good",
            "cheap",
            "budget",
            "under",
            "below",
            "laptop",
            "notebook",
            "pc",
            "phone",
            "mobile",
            "smartphone",
        }

        cleaned: List[str] = []
        for keyword in keywords:
            token = keyword.lower().strip()
            if not token or token in noise_terms:
                continue
            if re.fullmatch(r"\d+k?", token):
                continue
            cleaned.append(token)

        return cleaned
from __future__ import annotations

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

        logger.info("Found %d matching products", len(filtered))
        return filtered

    def _match_keywords(self, product: dict, keywords: List[str]) -> bool:
        text = " ".join(
            [
                str(product.get("brand", "")),
                str(product.get("model", "")),
                str(product.get("processor", "")),
                " ".join(product.get("use_case", [])),
            ]
        ).lower()

        return any(k in text for k in keywords)
from __future__ import annotations

from typing import Any, List, Tuple

from app.utils.logger import get_logger
from app.utils.constants import SORT_WEIGHTS

logger = get_logger(__name__)


class ComparisonTool:
    """
    Compares products and selects best option.
    """

    def compare(self, products: List[dict[str, Any]]) -> Tuple[dict, list, str]:
        if not products:
            raise ValueError("No products to compare.")

        logger.info("Comparing %d products", len(products))

        scored = [(p, self._score(p)) for p in products]

        scored.sort(key=lambda x: x[1], reverse=True)

        best_product = scored[0][0]
        alternatives = [p for p, _ in scored[1:3]]

        reasoning = self._generate_reasoning(best_product)

        return best_product, alternatives, reasoning

    def _score(self, product: dict) -> float:
        score = 0.0

        score += SORT_WEIGHTS["rating"] * product.get("rating", 0)
        score += SORT_WEIGHTS["ram_gb"] * product.get("ram_gb", 0)
        score += SORT_WEIGHTS["storage_gb"] * product.get("storage_gb", 0)

        # lower price = better
        price = product.get("price", 1)
        score += SORT_WEIGHTS["price"] * (1 / price)

        return score

    def _generate_reasoning(self, product: dict) -> str:
        return (
            f"{product['brand']} {product['model']} selected due to high rating "
            f"({product.get('rating')}) and strong specs "
            f"({product.get('ram_gb')}GB RAM, {product.get('storage_gb')}GB storage)."
        )
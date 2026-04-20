from __future__ import annotations

from typing import Any

from app.agents.search.search_config import SEARCH_CONFIG
from app.agents.search.search_prompt import SEARCH_SYSTEM_PROMPT
from app.tools.search.product_search_tool import ProductSearchTool
from app.utils.logger import get_logger, log_agent_event

logger = get_logger(__name__)


class SearchAgent:
    """
    Search agent responsible for product retrieval.
    """

    def __init__(self, data_path: str) -> None:
        self.name = SEARCH_CONFIG["name"]
        self.role = SEARCH_CONFIG["role"]
        self.goal = SEARCH_CONFIG["goal"]
        self.allow_delegation = SEARCH_CONFIG["allow_delegation"]
        self.verbose = SEARCH_CONFIG["verbose"]
        self.system_prompt = SEARCH_SYSTEM_PROMPT
        self.product_search_tool = ProductSearchTool(data_path)

    def search(
        self,
        category: str | None = None,
        budget: int | None = None,
        keywords: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search products using category, budget, and keywords.

        Args:
            category: Product category.
            budget: Maximum allowed budget.
            keywords: Query keywords.

        Returns:
            list[dict[str, Any]]: Matching products.
        """
        log_agent_event(
            self.name,
            "search_started",
            f"category={category}, budget={budget}, keywords={keywords}",
        )

        results = self.product_search_tool.search(
            category=category,
            budget=budget,
            keywords=keywords,
        )

        log_agent_event(self.name, "search_completed", f"Found {len(results)} products")
        return results
from __future__ import annotations

from app.state.state_schema import GlobalState
from app.utils.logger import get_logger

logger = get_logger(__name__)


class StateManager:
    """
    Centralized state mutation manager.
    """

    def __init__(self, state: GlobalState) -> None:
        self.state = state

    def update_query(self, category: str | None, budget: int | None, keywords: list[str]) -> None:
        logger.info("Updating query state")
        self.state.user_query.category = category
        self.state.user_query.budget = budget
        self.state.user_query.keywords = keywords

    def update_products(self, products: list[dict]) -> None:
        logger.info("Updating product state with %d items", len(products))
        self.state.product_state.products = products

    def update_analysis(self, best_product: dict, alternatives: list[dict], reasoning: str) -> None:
        logger.info("Updating analysis state")
        self.state.analysis_state.best_product = best_product
        self.state.analysis_state.alternatives = alternatives
        self.state.analysis_state.reasoning = reasoning

    def add_error(self, message: str) -> None:
        logger.error("State error: %s", message)
        self.state.errors.append(message)

    def get_state(self) -> GlobalState:
        return self.state
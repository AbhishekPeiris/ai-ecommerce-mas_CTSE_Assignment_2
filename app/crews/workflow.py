from __future__ import annotations

from app.services.query_parser import QueryParser
from app.services.validator import RequestValidator
from app.services.budget_extractor import BudgetExtractor
from app.state.state_manager import StateManager
from app.utils.logger import get_logger
from app.utils.helpers import load_json_file

logger = get_logger(__name__)


class Workflow:
    """
    End-to-end pipeline execution.
    """

    def __init__(self, config: dict, data_path: str) -> None:
        self.config = config
        self.data_path = data_path

        self.parser = QueryParser()
        self.validator = RequestValidator(config)
        self.budget_extractor = BudgetExtractor()

    def run(self, state_manager: StateManager) -> None:
        try:
            self._parse(state_manager)
            self._search(state_manager)
            self._analyze(state_manager)
        except Exception as exc:
            state_manager.add_error(str(exc))

    def _parse(self, sm: StateManager) -> None:
        query = sm.state.user_query.query

        parsed = self.parser.parse(query)

        self.validator.validate_category(parsed.category)
        self.validator.validate_budget(parsed.budget)

        sm.update_query(parsed.category, parsed.budget, parsed.keywords)

    def _search(self, sm: StateManager) -> None:
        products = load_json_file(self.data_path)

        category = sm.state.user_query.category
        budget = sm.state.user_query.budget

        filtered = [
            p for p in products
            if (not category or p["category"] == category)
            and (not budget or p["price"] <= budget)
        ]

        sm.update_products(filtered)

    def _analyze(self, sm: StateManager) -> None:
        products = sm.state.product_state.products

        if not products:
            raise ValueError("No products found.")

        best = sorted(products, key=lambda x: (-x["rating"], x["price"]))[0]

        alternatives = sorted(products, key=lambda x: (-x["rating"], x["price"]))[1:3]

        reasoning = f"Selected {best['brand']} {best['model']} due to best rating and value."

        sm.update_analysis(best, alternatives, reasoning)
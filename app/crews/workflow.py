from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from app.agents.analysis_agent import AnalysisAgent
from app.agents.coordinator_agent import CoordinatorAgent
from app.agents.delegator_agent import DelegatorAgent
from app.agents.search_agent import SearchAgent
from app.services.query_parser import QueryParser
from app.services.validator import RequestValidator
from app.state.state_manager import StateManager
from app.utils.logger import get_logger, log_agent_event

logger = get_logger(__name__)


class Workflow:
    """
    End-to-end MAS workflow.

    Flow:
    1. Parse user query
    2. Validate extracted constraints
    3. Delegator creates task plan
    4. Select dataset path based on category
    5. Search agent retrieves products
    6. Analysis agent selects best result
    7. Coordinator formats final output
    """

    def __init__(self, config: dict[str, Any], project_root: Path) -> None:
        self.config = config
        self.project_root = project_root

        self.parser = QueryParser()
        self.validator = RequestValidator(config)

        self.coordinator_agent = CoordinatorAgent()
        self.delegator_agent = DelegatorAgent()
        self.analysis_agent = AnalysisAgent()

    def run(self, state_manager: StateManager) -> str:
        """
        Execute the full workflow.

        Args:
            state_manager: Shared state manager.

        Returns:
            str: Final formatted response.
        """
        try:
            self._parse_and_validate(state_manager)
            self._plan_tasks(state_manager)
            search_agent = self._build_search_agent(state_manager)
            self._search_products(state_manager, search_agent)
            self._analyze_products(state_manager)
            return self._finalize_response(state_manager)

        except Exception as exc:  # pylint:  disable=broad-except 
            logger.exception("Workflow execution failed: %s", exc)
            state_manager.add_error(str(exc))
            return self._fallback_response()

    def _parse_and_validate(self, state_manager: StateManager) -> None:
        """
        Parse the raw user query and validate extracted values.
        """
        query = state_manager.state.user_query.query
        log_agent_event("Workflow", "parse_started", f"query={query}")

        parsed = self.parser.parse(query)

        self.validator.validate_category(parsed.category)
        self.validator.validate_budget(parsed.budget)

        state_manager.update_query(
            category=parsed.category,
            budget=parsed.budget,
            keywords=parsed.keywords,
        )

        log_agent_event(
            "Workflow",
            "parse_completed",
            f"category={parsed.category}, budget={parsed.budget}, keywords={parsed.keywords}",
        )

    def _plan_tasks(self, state_manager: StateManager) -> None:
        """
        Delegator creates a task plan.
        """
        query = state_manager.state.user_query.query
        plan = self.delegator_agent.create_plan(query)

        details = f"Generated task plan: {plan}"
        log_agent_event("Workflow", "plan_completed", details)

    def _build_search_agent(self, state_manager: StateManager) -> SearchAgent:
        """
        Build the search agent with the correct dataset path.
        """
        category = state_manager.state.user_query.category or self.config["runtime"]["default_category"]
        data_path = self._resolve_data_path(category)

        log_agent_event("Workflow", "search_agent_ready", f"category={category}, data_path={data_path}")
        return SearchAgent(data_path=str(data_path))

    def _search_products(self, state_manager: StateManager, search_agent: SearchAgent) -> None:
        """
        Search products using category, budget, and keywords.
        """
        category = state_manager.state.user_query.category or self.config["runtime"]["default_category"]
        budget = state_manager.state.user_query.budget
        keywords = state_manager.state.user_query.keywords

        results = search_agent.search(
            category=category,
            budget=budget,
            keywords=keywords,
        )

        state_manager.update_products(results)

        log_agent_event("Workflow", "search_completed", f"results_count={len(results)}")

    def _analyze_products(self, state_manager: StateManager) -> None:
        """
        Analyze search results and select best product.
        """
        products = state_manager.state.product_state.products

        if not products:
            raise ValueError("No products found for the given request.")

        best_product, alternatives, reasoning = self.analysis_agent.analyze(products)

        state_manager.update_analysis(
            best_product=best_product,
            alternatives=alternatives,
            reasoning=reasoning,
        )

        log_agent_event(
            "Workflow",
            "analysis_completed",
            f"best_product={best_product.get('brand')} {best_product.get('model')}",
        )

    def _finalize_response(self, state_manager: StateManager) -> str:
        """
        Finalize the response using the coordinator agent.
        """
        response = self.coordinator_agent.finalize(state_manager.get_state())
        log_agent_event("Workflow", "finalize_completed", "Final response created")
        return response

    def _resolve_data_path(self, category: str) -> Path:
        """
        Resolve the dataset path from config based on category.

        Args:
            category: Product category.

        Returns:
            Path: Absolute dataset path.
        """
        files = self.config["files"]

        if category == "phone":
            relative_path = files["phones_data"]
        else:
            relative_path = files["laptops_data"]

        return self.project_root / relative_path

    def _fallback_response(self) -> str:
        """
        Return configured fallback response.
        """
        return self.config["output"]["fallback_message"]
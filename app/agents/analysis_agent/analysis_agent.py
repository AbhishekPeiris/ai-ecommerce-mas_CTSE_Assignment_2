from __future__ import annotations

from typing import Any

from app.agents.analysis.analysis_config import ANALYSIS_CONFIG
from app.agents.analysis.analysis_prompt import ANALYSIS_SYSTEM_PROMPT
from app.tools.analysis.comparison_tool import ComparisonTool
from app.utils.logger import get_logger, log_agent_event

logger = get_logger(__name__)


class AnalysisAgent:
    """
    Analysis agent responsible for comparing products and selecting the best one.
    """

    def __init__(self) -> None:
        self.name = ANALYSIS_CONFIG["name"]
        self.role = ANALYSIS_CONFIG["role"]
        self.goal = ANALYSIS_CONFIG["goal"]
        self.allow_delegation = ANALYSIS_CONFIG["allow_delegation"]
        self.verbose = ANALYSIS_CONFIG["verbose"]
        self.system_prompt = ANALYSIS_SYSTEM_PROMPT
        self.comparison_tool = ComparisonTool()

    def analyze(self, products: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
        """
        Compare products and return best product, alternatives, and reasoning.

        Args:
            products: Search results to compare.

        Returns:
            tuple: (best_product, alternatives, reasoning)
        """
        log_agent_event(self.name, "analysis_started", f"Comparing {len(products)} products")
        best_product, alternatives, reasoning = self.comparison_tool.compare(products)
        log_agent_event(self.name, "analysis_completed", "Best product selected successfully")
        return best_product, alternatives, reasoning
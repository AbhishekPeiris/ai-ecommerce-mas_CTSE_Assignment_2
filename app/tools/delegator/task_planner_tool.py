from __future__ import annotations

from typing import List

from app.utils.logger import get_logger

logger = get_logger(__name__)


class TaskPlannerTool:
    """
    Breaks down user query into logical tasks.
    """

    def plan(self, query: str) -> List[str]:
        logger.info("Planning tasks for query")

        tasks = []

        if query:
            # Current planner is deterministic; swap with query-aware logic later.
            tasks.append("parse_query")
            tasks.append("validate_input")
            tasks.append("search_products")
            tasks.append("analyze_products")
            tasks.append("format_output")

        return tasks
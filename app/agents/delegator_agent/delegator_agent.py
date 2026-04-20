from __future__ import annotations

from app.agents.delegator.delegator_config import DELEGATOR_CONFIG
from app.agents.delegator.delegator_prompt import DELEGATOR_SYSTEM_PROMPT
from app.tools.delegator.task_planner_tool import TaskPlannerTool
from app.utils.logger import get_logger, log_agent_event

logger = get_logger(__name__)


class DelegatorAgent:
    """
    Delegator agent responsible for creating a task plan.
    """

    def __init__(self) -> None:
        self.name = DELEGATOR_CONFIG["name"]
        self.role = DELEGATOR_CONFIG["role"]
        self.goal = DELEGATOR_CONFIG["goal"]
        self.allow_delegation = DELEGATOR_CONFIG["allow_delegation"]
        self.verbose = DELEGATOR_CONFIG["verbose"]
        self.system_prompt = DELEGATOR_SYSTEM_PROMPT
        self.task_planner_tool = TaskPlannerTool()

    def create_plan(self, query: str) -> list[str]:
        """
        Create a logical execution plan from the user query.

        Args:
            query: User query text.

        Returns:
            list[str]: Ordered list of workflow tasks.
        """
        log_agent_event(self.name, "planning_started", f"Planning tasks for query: {query}")
        tasks = self.task_planner_tool.plan(query)
        log_agent_event(self.name, "planning_completed", f"Generated {len(tasks)} tasks")
        return tasks
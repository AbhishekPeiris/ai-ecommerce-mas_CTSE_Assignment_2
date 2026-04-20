from __future__ import annotations

from typing import Any

from app.agents.coordinator.coordinator_config import COORDINATOR_CONFIG
from app.agents.coordinator.coordinator_prompt import COORDINATOR_SYSTEM_PROMPT
from app.tools.coordinator.formatter_tool import FormatterTool
from app.utils.logger import get_logger, log_agent_event

logger = get_logger(__name__)


class CoordinatorAgent:
    """
    Main controller agent.

    Responsibilities:
    - Accept final workflow state
    - Produce user-facing final response
    - Return fallback response when no recommendation is available
    """

    def __init__(self) -> None:
        self.name = COORDINATOR_CONFIG["name"]
        self.role = COORDINATOR_CONFIG["role"]
        self.goal = COORDINATOR_CONFIG["goal"]
        self.allow_delegation = COORDINATOR_CONFIG["allow_delegation"]
        self.verbose = COORDINATOR_CONFIG["verbose"]
        self.system_prompt = COORDINATOR_SYSTEM_PROMPT
        self.formatter_tool = FormatterTool()

    def finalize(self, state: Any) -> str:
        """
        Convert final workflow state into a user-facing response.

        Args:
            state: Global state object.

        Returns:
            str: Final formatted response.
        """
        log_agent_event(self.name, "finalize_started", "Generating final user response")

        if getattr(state.analysis_state, "best_product", None) is None:
            log_agent_event(self.name, "finalize_fallback", "No best product available")
            return "Sorry, I could not find a suitable recommendation for your request."

        response = self.formatter_tool.format(state)
        log_agent_event(self.name, "finalize_completed", "Final response generated successfully")
        return response
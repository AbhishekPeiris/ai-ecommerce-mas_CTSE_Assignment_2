from __future__ import annotations

from pathlib import Path
from typing import Any

from app.crews.workflow import Workflow
from app.state.global_state import create_initial_state
from app.state.state_manager import StateManager
from app.utils.logger import get_logger, log_agent_event

logger = get_logger(__name__)


class EcommerceCrew:
    """
    Main orchestrator for the AI Smart E-Commerce MAS.
    """

    def __init__(self, config: dict[str, Any], project_root: Path) -> None:
        self.config = config
        self.project_root = project_root
        self.workflow = Workflow(config=config, project_root=project_root)

    def run(self, query: str) -> dict[str, Any]:
        """
        Run the crew for a single user query.

        Args:
            query: User input query.

        Returns:
            dict[str, Any]: Final response and state snapshot.
        """
        log_agent_event("EcommerceCrew", "run_started", f"query={query}")

        state = create_initial_state(query)
        state_manager = StateManager(state)

        final_response = self.workflow.run(state_manager)
        final_state = state_manager.get_state()

        log_agent_event("EcommerceCrew", "run_completed", "Workflow finished successfully")

        return {
            "response": final_response,
            "state": final_state,
        }
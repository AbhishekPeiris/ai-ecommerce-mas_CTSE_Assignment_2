from __future__ import annotations

from app.state.global_state import create_initial_state
from app.state.state_manager import StateManager
from app.crews.workflow import Workflow


class EcommerceCrew:
    """
    Main orchestrator for the MAS system.
    """

    def __init__(self, config: dict, data_path: str) -> None:
        self.workflow = Workflow(config, data_path)

    def run(self, query: str):
        state = create_initial_state(query)
        state_manager = StateManager(state)

        self.workflow.run(state_manager)

        return state_manager.get_state()
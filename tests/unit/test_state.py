from app.state.global_state import create_initial_state
from app.state.state_manager import StateManager


def test_state_update():
    state = create_initial_state("test query")
    manager = StateManager(state)

    manager.update_query("laptop", 100000, ["coding"])

    assert state.user_query.category == "laptop"
    assert state.user_query.budget == 100000
from __future__ import annotations

from app.state.state_schema import GlobalState, UserQueryState


def create_initial_state(query: str) -> GlobalState:
    """
    Initialize global state for a new request.
    """
    return GlobalState(
        user_query=UserQueryState(query=query)
    )
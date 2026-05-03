from __future__ import annotations

from app.state.state_schema import GlobalState, UserQueryState

# This module defines the global state management for the MAS application, including the structure of the global state and a helper function to create an initial state from a user query. 
def create_initial_state(query: str) -> GlobalState:
    """
    Initialize global state for a new request.
    """
    return GlobalState(
        user_query=UserQueryState(query=query)
    )
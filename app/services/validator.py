from __future__ import annotations

from typing import Any

from app.utils.error_handler import ValidationError


class RequestValidator:
    """
    Validate parsed user input and constraints.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def validate_budget(self, budget: int | None) -> None:
        if budget is None:
            return

        min_budget = self.config["validation"]["min_budget"]
        max_budget = self.config["validation"]["max_budget"]

        if budget < min_budget:
            raise ValidationError(f"Budget too low. Minimum is {min_budget}")

        if budget > max_budget:
            raise ValidationError(f"Budget too high. Maximum is {max_budget}")

    def validate_category(self, category: str | None) -> None:
        if category is None:
            return

        allowed = self.config["validation"]["allowed_categories"]

        if category not in allowed:
            raise ValidationError(f"Invalid category: {category}")
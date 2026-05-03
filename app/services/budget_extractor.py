from __future__ import annotations

from dataclasses import dataclass

# This module defines the BudgetExtractor, which extracts and normalizes budget constraints from user input for use in product recommendation analysis.
@dataclass
class BudgetResult:
    min_budget: int | None
    max_budget: int | None
    detected_budget: int | None


class BudgetExtractor:
    """
    Extract and normalize budget constraints.
    """

    def extract(self, budget: int | None) -> BudgetResult:
        if budget is None:
            return BudgetResult(None, None, None)

        return BudgetResult(
            min_budget=None,
            max_budget=budget,
            detected_budget=budget,
        )
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class UserQueryState:
    query: str
    category: str | None = None
    budget: int | None = None
    keywords: list[str] = field(default_factory=list)


@dataclass
class ProductState:
    products: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AnalysisState:
    best_product: dict[str, Any] | None = None
    alternatives: list[dict[str, Any]] = field(default_factory=list)
    reasoning: str | None = None


@dataclass
class GlobalState:
    user_query: UserQueryState
    product_state: ProductState = field(default_factory=ProductState)
    analysis_state: AnalysisState = field(default_factory=AnalysisState)
    errors: list[str] = field(default_factory=list)
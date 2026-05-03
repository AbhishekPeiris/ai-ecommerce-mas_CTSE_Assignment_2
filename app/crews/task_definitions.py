from __future__ import annotations

from dataclasses import dataclass

# This module defines task definitions for the MAS application, including parsing user queries, searching products, and analyzing results to select the best product recommendation.
@dataclass
class Task:
    name: str
    description: str


PARSE_TASK = Task(
    name="parse_query",
    description="Parse user query into structured format"
)

SEARCH_TASK = Task(
    name="search_products",
    description="Retrieve relevant products"
)

ANALYZE_TASK = Task(
    name="analyze_products",
    description="Select best product"
)
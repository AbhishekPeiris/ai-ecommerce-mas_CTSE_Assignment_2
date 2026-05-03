from __future__ import annotations

from typing import Any

from app.utils.logger import get_logger

logger = get_logger(__name__)

# This module defines the FormatterTool, which formats the final output for user display based on the analysis results.
class FormatterTool:
    """
    Formats the final output for user display.
    """

    def format(self, state: Any) -> str:
        try:
            analysis = state.analysis_state
            best = analysis.best_product
            alternatives = analysis.alternatives

            if not best:
                return "No recommendation available."

            result = []
            result.append("Recommended Product:\n")
            result.append(self._format_product(best))

            if alternatives:
                result.append("\n Alternatives:\n")
                for alt in alternatives:
                    result.append(self._format_product(alt))

            if analysis.reasoning:
                result.append("\n Reasoning:\n")
                result.append(analysis.reasoning)

            return "\n".join(result)

        except Exception as exc:
            logger.error("Formatting failed: %s", exc)
            return "Error formatting output."

    def _format_product(self, product: dict) -> str:
        return (
            f"- {product['brand']} {product['model']} | "
            f"LKR {product['price']} | "
            f"RAM: {product.get('ram_gb', '-') }GB | "
            f"Rating: {product.get('rating', '-')}"
        )
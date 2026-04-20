def simple_quality_check(response: str) -> bool:
    """
    Basic evaluation: check if response contains recommendation.
    """
    return "Recommended" in response or "Product" in response
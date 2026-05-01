from app.crews.ecommerce_crew import EcommerceCrew
from tests.evaluation.llm_judge import simple_quality_check
from pathlib import Path


def test_recommendation_quality(tmp_path):
    config = {
        "runtime": {"default_category": "laptop"},
        "files": {
            "laptops_data": "data.json",
            "phones_data": "data.json"
        },
        "output": {"fallback_message": "No result"},
        "validation": {
            "min_budget": 10000,
            "max_budget": 1000000,
            "allowed_categories": ["laptop", "phone"]
        }
    }

    data = [
        {"category": "laptop", "price": 100000, "rating": 4.8, "brand": "Best", "model": "Pro"}
    ]

    file = tmp_path / "data.json"
    import json
    file.write_text(json.dumps(data))

    crew = EcommerceCrew(config, tmp_path)
    result = crew.run("best laptop")

    assert simple_quality_check(result["response"])
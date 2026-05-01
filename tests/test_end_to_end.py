from app.crews.ecommerce_crew import EcommerceCrew
from pathlib import Path
import json


def test_end_to_end(tmp_path):
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
        {"category": "laptop", "price": 90000, "rating": 4.5, "brand": "Test", "model": "One"}
    ]

    file = tmp_path / "data.json"
    file.write_text(json.dumps(data))

    crew = EcommerceCrew(config, tmp_path)

    result = crew.run("cheap laptop")

    assert result["response"] is not None
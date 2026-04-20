from pathlib import Path
import yaml

from app.crews.ecommerce_crew import EcommerceCrew


def test_workflow_integration(tmp_path):
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
        {"category": "laptop", "price": 100000, "rating": 4.5, "brand": "A", "model": "X"}
    ]

    file = tmp_path / "data.json"
    import json
    file.write_text(json.dumps(data))

    crew = EcommerceCrew(config, tmp_path)

    result = crew.run("laptop under 150000")

    assert "response" in result
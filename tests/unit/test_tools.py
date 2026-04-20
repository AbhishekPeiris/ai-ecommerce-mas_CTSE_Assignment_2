from app.tools.search.product_search_tool import ProductSearchTool
from app.tools.analysis.comparison_tool import ComparisonTool
from app.tools.delegator.task_planner_tool import TaskPlannerTool
from app.tools.coordinator.formatter_tool import FormatterTool

import json


def test_product_search_tool(tmp_path):
    data = [
        {"category": "laptop", "price": 100000, "brand": "A", "model": "X"},
        {"category": "laptop", "price": 200000, "brand": "B", "model": "Y"},
    ]

    file = tmp_path / "data.json"
    file.write_text(json.dumps(data))

    tool = ProductSearchTool(str(file))
    results = tool.search(category="laptop", budget=150000)

    assert len(results) == 1
    assert results[0]["brand"] == "A"


def test_comparison_tool():
    tool = ComparisonTool()

    products = [
        {"brand": "A", "model": "X", "rating": 4.5, "price": 100000, "ram_gb": 8, "storage_gb": 512},
        {"brand": "B", "model": "Y", "rating": 4.7, "price": 120000, "ram_gb": 16, "storage_gb": 512},
    ]

    best, alternatives, reasoning = tool.compare(products)

    assert best is not None
    assert isinstance(alternatives, list)
    assert isinstance(reasoning, str)


def test_task_planner_tool():
    tool = TaskPlannerTool()

    tasks = tool.plan("find laptop under 100000")

    assert isinstance(tasks, list)
    assert "parse_query" in tasks
    assert "search_products" in tasks


def test_formatter_tool():
    tool = FormatterTool()

    class MockState:
        class Analysis:
            best_product = {"brand": "A", "model": "X", "price": 100000, "ram_gb": 8, "rating": 4.5}
            alternatives = []
            reasoning = "Best choice"

        analysis_state = Analysis()

    output = tool.format(MockState())

    assert "Recommended" in output or "A X" in output
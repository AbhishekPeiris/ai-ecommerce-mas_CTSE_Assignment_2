from app.agents.analysis.analysis_agent import AnalysisAgent


def test_analysis_agent():
    agent = AnalysisAgent()

    products = [
        {"brand": "A", "model": "X", "rating": 4.5, "price": 100000, "ram_gb": 8, "storage_gb": 512},
        {"brand": "B", "model": "Y", "rating": 4.7, "price": 120000, "ram_gb": 16, "storage_gb": 512},
    ]

    best, alternatives, _ = agent.analyze(products)

    assert best is not None
    assert isinstance(alternatives, list)
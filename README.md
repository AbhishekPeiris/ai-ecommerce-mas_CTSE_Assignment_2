# AI Smart E-Commerce Multi-Agent System (MAS)

## Overview

This project implements a **Multi-Agent System (MAS)** for intelligent product recommendations using a structured architecture with agents, tools, shared state, and workflows.

The system processes user queries and returns the most suitable product based on:

- Budget
- Category (Laptop / Phone)
- Keywords (use case, features)
- Dataset-based filtering and scoring

---

## Key Features

- Multi-Agent Architecture
- Custom Tool-based Execution
- Shared Global State Management
- Query Parsing and Validation
- Ranking & Recommendation Engine
- Logging & Error Handling
- Fully Local Execution (No paid APIs required)
- Extensible for LLM (Ollama ready)

---

## Architecture

### Agents

- **Coordinator Agent** → Final response generation
- **Delegator Agent** → Task planning
- **Search Agent** → Product retrieval
- **Analysis Agent** → Product comparison

### Tools

- Formatter Tool
- Task Planner Tool
- Product Search Tool
- Comparison Tool

### Flow

1. User enters query
2. Query is parsed
3. Delegator creates task plan
4. Search Agent retrieves products
5. Analysis Agent selects best product
6. Coordinator formats output

---

## Project Structure

```bash
app/
├── agents/
├── tools/
├── services/
├── state/
├── crews/
├── llm/
├── utils/
├── data/
└── main.py

configs/
logs/
scripts/
tests/

Setup Instructions
1. Create Virtual Environment
python -m venv venv
2. Activate Environment

PowerShell:

.\venv\Scripts\Activate.ps1
3. Install Dependencies
pip install -r requirements.txt
Load Sample Data
python scripts/load_data.py
Run the Application
python scripts/run_app.py

OR

python app/main.py
Example Queries
Best laptop under 150000
Student laptop for coding
Best phone under 100000
Logs

Logs are stored in:

logs/system.log
logs/errors.log
Run Tests
python scripts/run_tests.py
Evaluation

Includes:

Unit tests
Integration tests
End-to-end tests
Recommendation quality evaluation
Future Improvements
API integration (real product data)
Web UI (Streamlit / React)
LLM-powered reasoning (Ollama)
Multi-category expansion
Notes
Fully local system (no API keys required)
Designed for academic MAS assignment
Clean modular architecture


---

# TESTS

---

## `tests/unit/test_tools.py`

```python
from app.tools.search.product_search_tool import ProductSearchTool


def test_product_search_basic(tmp_path):
    data = [
        {"category": "laptop", "price": 100000, "brand": "A"},
        {"category": "laptop", "price": 200000, "brand": "B"},
    ]

    file = tmp_path / "data.json"
    import json
    file.write_text(json.dumps(data))

    tool = ProductSearchTool(str(file))
    results = tool.search(category="laptop", budget=150000)

    assert len(results) == 1
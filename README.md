# Create Python virtual environment
python -m venv venv

# Active Environment
.\venv\Scripts\Activate.ps1

# Install Command
pip install crewai pydantic python-dotenv pytest

# Start manually
ollama serve

# Ollama Installation
ollama pull llama3

# To run the model, use the command
ollama run llama3

# Check litning ports
netstat -ano | findstr 11434

# Kill ports
taskkill /PID 25036 /F
taskkill /IM ollama.exe /F

# Folder Structure
AI-ECOMMERCE-MAS/

├── app/
│   ├── agents/
│   │   ├── coordinator/
│   │   │   ├── coordinator_agent.py
│   │   │   ├── coordinator_prompt.py
│   │   │   └── coordinator_config.py
│   │   │
│   │   ├── delegator/
│   │   │   ├── delegator_agent.py
│   │   │   ├── delegator_prompt.py
│   │   │   └── delegator_config.py
│   │   │
│   │   ├── search/
│   │   │   ├── search_agent.py
│   │   │   ├── search_prompt.py
│   │   │   └── search_config.py
│   │   │
│   │   ├── analysis/
│   │   │   ├── analysis_agent.py
│   │   │   ├── analysis_prompt.py
│   │   │   └── analysis_config.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── tools/
│   │   ├── coordinator/
│   │   │   └── formatter_tool.py
│   │   │
│   │   ├── delegator/
│   │   │   └── task_planner_tool.py
│   │   │
│   │   ├── search/
│   │   │   └── product_search_tool.py
│   │   │
│   │   ├── analysis/
│   │   │   └── comparison_tool.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── crews/
│   │   ├── ecommerce_crew.py
│   │   ├── workflow.py
│   │   └── task_definitions.py
│   │
│   ├── state/
│   │   ├── global_state.py
│   │   ├── state_manager.py
│   │   └── state_schema.py
│   │
│   ├── data/
│   │   ├── laptops.json
│   │   └── phones.json   # future extension
│   │
│   ├── llm/
│   │   ├── ollama_client.py
│   │   └── model_config.py
│   │
│   ├── services/
│   │   ├── query_parser.py
│   │   ├── budget_extractor.py
│   │   └── validator.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── error_handler.py
│   │   ├── constants.py
│   │   └── helpers.py
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   │   ├── test_tools.py
│   │   ├── test_agents.py
│   │   └── test_state.py
│   │
│   ├── integration/
│   │   └── test_workflow.py
│   │
│   ├── evaluation/
│   │   ├── test_recommendation_quality.py
│   │   └── llm_judge.py
│   │
│   └── test_end_to_end.py
│
├── logs/
│   ├── system.log
│   └── errors.log
│
├── configs/
│   ├── app_config.yaml
│   ├── agent_config.yaml
│   └── logging_config.yaml
│
├── scripts/
│   ├── run_app.py
│   ├── run_tests.py
│   └── load_data.py
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore
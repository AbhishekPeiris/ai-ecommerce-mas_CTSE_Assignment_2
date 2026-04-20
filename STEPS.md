# AI E-Commerce Multi-Agent System — Step-by-Step Run Guide

This guide explains how to **setup, run, test, and verify** the complete system locally.

---

## Step 1: Clone / Open Project

Navigate to your project folder:

```bash
cd your-project-folder

Step 2: Create Virtual Environment
python -m venv venv
⚡ Step 3: Activate Virtual Environment
PowerShell (Windows)
.\venv\Scripts\Activate.ps1
CMD (Windows)
venv\Scripts\activate
Step 4: Install Dependencies
pip install -r requirements.txt
⚙️ Step 5: Setup Environment Variables

Create a .env file in the root directory:

APP_ENV=development
LOG_LEVEL=INFO
DATA_PATH=app/data/
Step 6: Load Sample Data
python scripts/load_data.py

This will create:

app/data/laptops.json
app/data/phones.json
Step 7: Run the Application
Option 1 (Recommended)
python scripts/run_app.py
Option 2
python app/main.py
Step 8: Try Sample Queries

Enter queries like:

Best laptop under 150000
Student laptop for coding
Best phone under 100000
Step 9: Run All Tests
Option 1 (Script)
python scripts/run_tests.py
Option 2 (Direct Pytest)
pytest tests/ -v
Expected Test Output

You should see:

test_tools.py ........ PASSED
test_agents.py ....... PASSED
test_state.py ........ PASSED
test_workflow.py ..... PASSED
test_end_to_end.py ... PASSED
Step 10: Verify System Output

Successful run should return:

Recommended product
Alternative products
Reasoning for selection
Troubleshooting
ModuleNotFoundError: No module named 'app'

Fix:

set PYTHONPATH=.

PowerShell:

$env:PYTHONPATH="."
Port 11434 already in use (Ollama)

Check:

netstat -ano | findstr 11434

Kill process:

taskkill /PID <PID> /F
taskkill /IM ollama.exe /F
Data files not found

Ensure:

app/data/laptops.json
app/data/phones.json

If missing:

python scripts/load_data.py
Pytest not found

Install:

pip install pytest
# COMPLETE SYSTEM RUN

## Step 1: Project setup
python -m venv venv
.\venv\Scripts\Activate.ps1

## Step 2: Dependencies instal
pip install -r requirements.txt

## Step 3: Sample data load
python -m scripts/load_data.py

## Step 4: Application run
python scripts/run_app.py
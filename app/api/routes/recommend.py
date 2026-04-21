from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path

from app.crews.ecommerce_crew import EcommerceCrew
from app.main import build_app_config

router = APIRouter()

class QueryRequest(BaseModel):
    query: str


@router.post("/recommend")
def recommend(req: QueryRequest):
    project_root = Path(__file__).resolve().parents[3]
    config = build_app_config(project_root)

    crew = EcommerceCrew(config=config, project_root=project_root)
    result = crew.run(req.query)
    state = result["state"]

    return {
        "response": result["response"],
        "best_product": state.analysis_state.best_product,
        "alternatives": state.analysis_state.alternatives,
        "reasoning": state.analysis_state.reasoning,
        "errors": state.errors,
    }
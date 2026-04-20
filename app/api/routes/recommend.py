from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import yaml

from app.crews.ecommerce_crew import EcommerceCrew

router = APIRouter()

class QueryRequest(BaseModel):
    query: str


@router.post("/recommend")
def recommend(req: QueryRequest):
    config = {
        "runtime": {"default_category": "laptop"},
        "files": {
            "laptops_data": "laptops.json",
            "phones_data": "phones.json"
        },
        "output": {"fallback_message": "No result"},
        "validation": {
            "min_budget": 10000,
            "max_budget": 1000000,
            "allowed_categories": ["laptop", "phone"]
        }
    }

    crew = EcommerceCrew(config, Path("app/data"))
    result = crew.run(req.query)

    return {
        "best_product": result["best_product"],
        "alternatives": result["alternatives"],
        "reasoning": result["reasoning"]
    }
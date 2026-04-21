from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.crews.ecommerce_crew import EcommerceCrew
from app.main import build_app_config

st.set_page_config(page_title="AI E-Commerce Assistant")

st.title("🛍️ Smart Product Recommender")


def _run_local_recommendation(query: str) -> dict[str, Any]:
    config = build_app_config(PROJECT_ROOT)

    crew = EcommerceCrew(config=config, project_root=PROJECT_ROOT)
    result = crew.run(query)
    state = result["state"]

    return {
        "response": result["response"],
        "best_product": state.analysis_state.best_product,
        "alternatives": state.analysis_state.alternatives,
        "reasoning": state.analysis_state.reasoning,
        "errors": state.errors,
        "source": "local",
    }


def _render_result(data: dict[str, Any]) -> None:
    if data.get("response"):
        st.subheader("Final Recommendation")
        st.write(data["response"])

    st.subheader("Recommended Product")
    st.write(data.get("best_product"))

    st.subheader("Alternatives")
    st.write(data.get("alternatives", []))

    st.subheader("Reasoning")
    st.write(data.get("reasoning"))

    errors = data.get("errors") or []
    if errors:
        st.warning("Issues:")
        for error in errors:
            st.write(f"- {error}")

query = st.text_input("Enter your query")

if st.button("Search") and query:
    with st.spinner("Processing..."):
        try:
            res = requests.post(
                "http://localhost:8000/recommend",
                json={"query": query},
                timeout=10,
            )
            res.raise_for_status()
            data = res.json()

            st.success("Recommendation Ready!")
            _render_result(data)

        except requests.exceptions.RequestException:
            st.info("API server is not reachable. Using local recommendation engine...")
            data = _run_local_recommendation(query)
            st.success("Recommendation Ready! (local mode)")
            _render_result(data)

        except Exception as e:
            st.error(f"Error: {e}")
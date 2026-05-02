from __future__ import annotations

from pathlib import Path
import sys
import time
from typing import Any
from uuid import uuid4

import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.crews.ecommerce_crew import EcommerceCrew
from app.main import build_app_config

st.set_page_config(page_title="AI E-Commerce Assistant")

QUICK_QUESTIONS =  [
        "Best laptop under 150000",
        "Student phone under 100000",
        "Gaming laptop under 220000",
        "Camera phone under 160000",
        "Laptop for coding and office",
        "Best Samsung phone under 200000",
]

NEW_CHAT_TITLE = "New Chat"


def _init_state() -> None:
        if "theme_mode" not in st.session_state:
                st.session_state.theme_mode = "Dark"

        if "chats" not in st.session_state:
                st.session_state.chats = [
                        {
                                "id": str(uuid4()),
                        "title": NEW_CHAT_TITLE,
                                "messages": [],
                        }
                ]

        if "active_chat_id" not in st.session_state:
                st.session_state.active_chat_id = st.session_state.chats[0]["id"]


def _get_theme_css() -> str:
        dark = st.session_state.theme_mode == "Dark"
        if dark:
                background = "#070b14"
                panel = "#0f1628"
                panel_alt = "#141f36"
                text = "#eef4ff"
                muted = "#98a7c2"
                border = "#24324f"
                accent = "#17b890"
                accent_soft = "#1e7b65"
        else:
                background = "#f4f8ff"
                panel = "#ffffff"
                panel_alt = "#eaf1ff"
                text = "#0d1b2a"
                muted = "#4f627d"
                border = "#d4e0f5"
                accent = "#0e9f7f"
                accent_soft = "#0e7c63"

        return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

:root {{
    --bg: {background};
    --panel: {panel};
    --panel-alt: {panel_alt};
    --text: {text};
    --muted: {muted};
    --border: {border};
    --accent: {accent};
    --accent-soft: {accent_soft};
}}

.stApp {{
    background:
        radial-gradient(circle at 10% 10%, rgba(23, 184, 144, 0.14), transparent 32%),
        radial-gradient(circle at 90% 0%, rgba(30, 123, 101, 0.14), transparent 36%),
        var(--bg);
    color: var(--text);
    font-family: 'Manrope', sans-serif;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, var(--panel), var(--panel-alt));
    border-right: 1px solid var(--border);
}}

h1, h2, h3 {{
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}}

.hero-box {{
    background: linear-gradient(130deg, var(--panel), var(--panel-alt));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.2rem 1.3rem;
    margin: 0.2rem 0 1rem 0;
}}

.hero-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}}

.hero-sub {{
    color: var(--muted);
    font-size: 0.98rem;
}}

.brand-chip {{
    display: inline-block;
    background: rgba(23, 184, 144, 0.18);
    color: var(--text);
    border: 1px solid rgba(23, 184, 144, 0.35);
    border-radius: 999px;
    padding: 0.35rem 0.8rem;
    font-size: 0.84rem;
    margin-bottom: 0.5rem;
}}

.product-card {{
    background: linear-gradient(145deg, var(--panel), var(--panel-alt));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-top: 0.4rem;
}}

.label {{
    color: var(--muted);
    font-weight: 600;
    font-size: 0.84rem;
}}

.value {{
    color: var(--text);
    font-size: 0.93rem;
    margin-bottom: 0.3rem;
}}

.chat-tag {{
    color: var(--muted);
    font-size: 0.8rem;
    margin-top: 0.2rem;
}}

div.stButton > button {{
    border-radius: 12px;
    border: 1px solid var(--border);
}}

div.stButton > button:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

[data-testid="stChatInput"] textarea {{
    border-radius: 16px !important;
}}
</style>
"""


def _active_chat() -> dict[str, Any]:
        for chat in st.session_state.chats:
                if chat["id"] == st.session_state.active_chat_id:
                        return chat

        st.session_state.active_chat_id = st.session_state.chats[0]["id"]
        return st.session_state.chats[0]


def _start_new_chat() -> None:
        new_chat = {
                "id": str(uuid4()),
            "title": NEW_CHAT_TITLE,
                "messages": [],
        }
        st.session_state.chats.insert(0, new_chat)
        st.session_state.active_chat_id = new_chat["id"]


def _product_image(product: dict[str, Any] | None) -> str | None:
    if not product:
        return None

    image_url = product.get("image_url")
    if isinstance(image_url, str) and image_url.strip():
        return image_url

    image = product.get("image")
    if isinstance(image, str) and image.strip():
        return image

    return None


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


def _fetch_recommendation(query: str) -> dict[str, Any]:
    try:
        res = requests.post(
            "http://localhost:8000/recommend",
            json={"query": query},
            timeout=12,
        )
        res.raise_for_status()
        payload = res.json()
        payload["source"] = "api"
        return payload

    except requests.exceptions.RequestException:
        return _run_local_recommendation(query)


def _render_product_card(product: dict[str, Any] | None, heading: str) -> None:
    st.markdown(f"### {heading}")
    if not product:
        st.info("No product details available.")
        return

    col_image, col_info = st.columns([1, 1.35])
    with col_image:
        image_url = _product_image(product)
        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.info("Image not available for this product.")

    with col_info:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.markdown(f"## {product.get('brand', '-') } {product.get('model', '-')}")
        st.markdown(f"<div class='label'>Price</div><div class='value'>{product.get('currency', 'LKR')} {product.get('price', '-')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='label'>Rating</div><div class='value'>{product.get('rating', '-')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='label'>RAM</div><div class='value'>{product.get('ram_gb', '-')} GB</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='label'>Storage</div><div class='value'>{product.get('storage_gb', '-')} GB</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='label'>Processor</div><div class='value'>{product.get('processor', '-')}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_assistant_payload(data: dict[str, Any], animate: bool = False) -> None:
    source = data.get("source", "local")
    source_tag = "API" if source == "api" else "Local Engine"
    st.markdown(f"<div class='chat-tag'>Source: {source_tag}</div>", unsafe_allow_html=True)

    response_text = str(data.get("response") or "No response available.")
    st.markdown("### Recommendation Summary")

    if animate:
        chunks = response_text.split(" ")
        progressive = st.empty()
        buffer = ""
        for word in chunks:
            buffer = (buffer + " " + word).strip()
            progressive.markdown(buffer + " ▌")
            time.sleep(0.01)
        progressive.markdown(buffer)
    else:
        st.markdown(response_text)

    _render_product_card(data.get("best_product"), "Top Pick")

    alternatives = data.get("alternatives") or []
    if alternatives:
        st.markdown("### Alternatives")
        for index, item in enumerate(alternatives, start=1):
            with st.expander(f"Alternative {index}: {item.get('brand', '-')} {item.get('model', '-')}"):
                _render_product_card(item, "Product Details")

    reasoning = data.get("reasoning")
    if reasoning:
        st.markdown("### Why This Recommendation")
        st.markdown(reasoning)

    errors = data.get("errors") or []
    if errors:
        st.warning("Some issues were detected while generating this recommendation:")
        for error in errors:
            st.write(f"- {error}")


def _update_chat_title(chat: dict[str, Any], query: str) -> None:
    if chat.get("title") == NEW_CHAT_TITLE:
        shortened = query.strip()
        chat["title"] = shortened[:35] + ("..." if len(shortened) > 35 else "")


def _handle_user_query(query: str) -> None:
    chat = _active_chat()
    _update_chat_title(chat, query)

    chat["messages"].append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching the best options for you..."):
            payload = _fetch_recommendation(query)

        _render_assistant_payload(payload, animate=True)

    chat["messages"].append({"role": "assistant", "payload": payload})


_init_state()
st.markdown(_get_theme_css(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🛍️ ShopGenius AI")
    st.caption("Find the best laptops and phones in seconds.")

    if st.button("＋ Start New Chat", use_container_width=True):
        _start_new_chat()
        st.rerun()

    st.markdown("### Recent Chats")
    for chat in st.session_state.chats[:12]:
        active = chat["id"] == st.session_state.active_chat_id
        label = f"● {chat['title']}" if active else chat["title"]
        if st.button(label, key=f"chat-{chat['id']}", use_container_width=True):
            st.session_state.active_chat_id = chat["id"]
            st.rerun()

main_col, new_chat_col = st.columns([5, 1])
with main_col:
    st.markdown("<div class='brand-chip'>AI Product Discovery Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-box'><div class='hero-title'>Smart Product Recommender</div><div class='hero-sub'>Ask in natural language and get ranked recommendations with visual product cards and detailed reasoning.</div></div>", unsafe_allow_html=True)
with new_chat_col:
    if st.button("New Chat", key="new-chat-main"):
        _start_new_chat()
        st.rerun()

active_chat = _active_chat()
messages = active_chat.get("messages", [])

if not messages:
    st.markdown("### Quick Questions")
    q_cols = st.columns(3)
    pending_from_quick: str | None = None
    for index, question in enumerate(QUICK_QUESTIONS):
        with q_cols[index % 3]:
            if st.button(question, key=f"quick-{index}", use_container_width=True):
                pending_from_quick = question

    if pending_from_quick:
        _handle_user_query(pending_from_quick)

for message in messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            _render_assistant_payload(message["payload"], animate=False)

chat_input = st.chat_input("Ask for a laptop or phone recommendation...")
if chat_input:
    _handle_user_query(chat_input)
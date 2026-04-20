import streamlit as st
import requests

st.set_page_config(page_title="AI E-Commerce Assistant")

st.title("🛍️ Smart Product Recommender")

query = st.text_input("Enter your query")

if st.button("Search"):
    if query:
        with st.spinner("Processing..."):
            try:
                res = requests.post(
                    "http://localhost:8000/recommend",
                    json={"query": query}
                )
                data = res.json()

                st.success("Recommendation Ready!")

                st.subheader("Recommended Product")
                st.write(data["best_product"])

                st.subheader("Alternatives")
                st.write(data["alternatives"])

                st.subheader("Reasoning")
                st.write(data["reasoning"])

            except Exception as e:
                st.error(f"Error: {e}")
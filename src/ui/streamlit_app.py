import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Contracts LLM + Neo4j", layout="wide")
st.title("Contracts Assistant (LangChain + Hugging Face + Neo4j)")

tab1, tab2, tab3 = st.tabs(["Ingest Contract", "Ask", "Summarize Any Text"])

with tab1:
    st.subheader("Upload a .txt contract")
    contract_id = st.text_input("Contract ID", value="demo-contract-001")
    file = st.file_uploader("Choose a .txt file", type=["txt"])

    if file and st.button("Ingest"):
        text = file.read().decode("utf-8")
        with st.spinner("Ingesting and classifying..."):
            resp = requests.post(API_BASE + "/ingest", json={"contract_id": contract_id, "contract_text": text})
        st.success("Ingested!")
        st.json(resp.json())

with tab2:
    st.subheader("Ask about your ingested contracts")
    q = st.text_input("Your question", value="What are the termination terms?")
    top_k = st.slider("Top-K passages", 1, 10, 5)
    if st.button("Ask"):
        with st.spinner("Retrieving + answering..."):
            resp = requests.post(API_BASE + "/ask", json={"question": q, "top_k": top_k})
        st.write(resp.json().get("answer"))
        st.caption(f"Context passages used: {resp.json().get('context_count', 0)}")

with tab3:
    st.subheader("Summarize any text")
    txt = st.text_area("Paste text to summarize", height=220)
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            resp = requests.post(API_BASE + "/summarize", json={"text": txt})
        st.write(resp.json().get("summary"))
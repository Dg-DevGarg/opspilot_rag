import streamlit as st
from rag_engine import investigate_incident, index_documents

st.set_page_config(
    page_title="OpsPilot | AI Incident Investigator",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 OpsPilot – Production Incident Investigation Assistant")
st.caption("Powered by ChromaDB, Sentence-Transformers (all-MiniLM-L6-v2), and OpenAI GPT-OSS-120B")

# Sidebar with sample quick-select alerts and settings
with st.sidebar:
    st.header("⚙️ Configuration")
    top_k = st.slider("Retrieved Chunks (Top-K)", min_value=1, max_value=6, value=4)
    if st.button("🔄 Re-index Knowledge Base"):
        with st.spinner("Re-indexing 25 markdown documents..."):
            index_documents(force_reindex=True)
        st.success("Knowledge base re-indexed!")

    st.divider()
    st.subheader("📋 Sample Production Alerts")
    sample_queries = {
        "Select a sample alert...": "",
        "1. Payment 503 & DB Timeout": "Payment API is returning HTTP 503 errors. Database connections are timing out after deployment.",
        "2. Redis OOM & Random Logouts": "Users are being logged out randomly. Auth cache cluster is throwing OOM command not allowed errors.",
        "3. Kafka Notification Delay": "Order confirmation emails are delayed by 2 hours. Kafka consumer group lag is above 100,000.",
        "4. Pod CrashLoop (Exit Code 137)": "pdf-export-worker pods are stuck in CrashLoopBackOff with exit code 137.",
        "5. Unrelated Query (Hallucination Test)": "How do I bake a chocolate sourdough cake from scratch?"
    }
    selected_sample = st.selectbox("Load Preset Scenario:", list(sample_queries.keys()))

# Main Input Area
default_text = sample_queries[selected_sample] if selected_sample != "Select a sample alert..." else ""
query = st.text_area(
    "Paste Incoming Incident Alert / PagerDuty Log:",
    value=default_text,
    height=100,
    placeholder="e.g., Stripe webhooks are failing with 400 Bad Request and subscriptions aren't activating..."
)

if st.button("🔍 Investigate Incident", type="primary"):
    if not query.strip():
        st.warning("Please enter an incident description first.")
    else:
        with st.spinner("Retrieving runbooks & synthesizing root cause via GPT-OSS-120B..."):
            result = investigate_incident(query, top_k=top_k)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📑 Investigation Report")
            st.markdown(result["report"])

        with col2:
            st.subheader("📚 Retrieved Context & Distances")
            st.caption("Lower vector distance = higher semantic similarity")
            for i, (chunk, dist) in enumerate(zip(result["chunks"], result["distances"])):
                with st.expander(f"Chunk {i+1} (Distance: {dist:.3f})", expanded=(i == 0)):
                    st.code(chunk, language="markdown")
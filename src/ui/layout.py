import streamlit as st

def render_page_config():
    st.set_page_config(
        page_title="MedGraph-AI | Health Timeline",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_header():
    st.title("🧬 MedGraph-AI")
    st.markdown(
        help="Upload patient files below to extract vital signs, diagnoses, and chronological timelines."
    )
    st.markdown("---")

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Settings & Status")
        st.markdown("Manage system configurations and agent states here.")
        
        # Placeholders for Day 2/3 when we connect LangGraph and database states
        st.divider()
        st.metric(label="System Status", value="Ready 🟢")
        st.metric(label="Loaded Records", value="0")
        
        st.divider()
        st.caption("Architecture: LangGraph + Streamlit")
        st.caption("Active Repo: MedGraph-AI")
import streamlit as st
from src.database import get_all_patients

def render_page_config():
    st.set_page_config(
        page_title="MedGraph-AI | Health Timeline",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_header():
    st.title("🧬 MedGraph-AI")
    
    # Notice the text string comes first, followed by the help parameter
    st.markdown(
        "**An agentic pipeline for structuring unstructured medical documents.**", 
        help="Upload patient files below to extract vital signs, diagnoses, and chronological timelines."
    )
    st.markdown("---")

def render_sidebar():
    """Renders the sidebar navigation, settings, and patient selection."""
    with st.sidebar:
        st.header("⚙️ Settings & Status")
        st.markdown("Manage system configurations and patient contexts here.")
        st.divider()
        
        # 1. Fetch existing patients from the database
        existing_patients = get_all_patients()
        
        st.subheader("👤 Active Patient Context")
        
        # 2. Allow selecting an existing patient or creating a new one
        patient_mode = st.radio("Patient Selection", ["Select Existing", "Add New Patient"], label_visibility="collapsed")
        
        if patient_mode == "Select Existing":
            if existing_patients:
                selected = st.selectbox("Select Patient", existing_patients)
                st.session_state.current_patient = selected
            else:
                st.info("No patients found. Add a new one.")
                st.session_state.current_patient = None
        else:
            new_patient = st.text_input("Enter New Patient Name")
            if new_patient:
                st.session_state.current_patient = new_patient.strip()
            else:
                st.session_state.current_patient = None
                
        if st.session_state.get("current_patient"):
            st.success(f"Active: **{st.session_state.current_patient}**")
        else:
            st.warning("⚠️ No patient selected.")
            
        st.divider()
        
        # 3. System Status Indicators
        st.caption("System Status")
        st.markdown("<h2>Ready 🟢</h2>", unsafe_allow_html=True)
        
        st.divider()
        st.caption("Architecture: LangGraph + Streamlit")
        st.caption("Active Repo: MedGraph-AI")
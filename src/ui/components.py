import streamlit as st
from typing import Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile

def render_file_uploader() -> Optional[UploadedFile]:
    st.subheader("📄 Upload Medical Record")
    st.markdown("Upload a PDF, JPG, or PNG to extract structured health data.")
    
    # The uploader returns a BytesIO buffer, not a local file path
    uploaded_file = st.file_uploader(
        label="Select a medical document",
        type=["pdf", "jpg", "jpeg", "png"],
        accept_multiple_files=False,
        help="Maximum file size is typically 200MB depending on server configuration."
    )
    
    # Handle the immediate UI state feedback right here in the component
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' loaded successfully.")
        
    # Return the object so the LangGraph backend can ingest it later
    return uploaded_file
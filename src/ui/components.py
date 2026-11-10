import streamlit as st
from typing import Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import List, Dict, Any

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

def render_timeline(events: List[Dict[str, Any]]):
    st.subheader("📅 Patient Health Timeline")
    
    if not events:
        st.info("No timeline events found. Upload a medical document to begin.")
        return

    # Iterate through the database records and build the UI cards
    for event in events:
        date = event.get("event_date", "Unknown Date")
        event_type = event.get("event_type", "Medical Event")
        desc = event.get("description", "No description provided.")
        metrics = event.get("metrics", {})
        source = event.get("source_file", "Unknown source")

        # Create a visually distinct card for each event
        with st.expander(f"**{date}** — {event_type}", expanded=True):
            st.markdown(f"*{desc}*")
            
            # Display metrics beautifully using Streamlit columns
            if metrics:
                st.markdown("**Extracted Metrics:**")
                cols = st.columns(len(metrics) if len(metrics) < 5 else 4)
                
                col_idx = 0
                for key, value in metrics.items():
                    clean_key = key.replace("_", " ").title()
                    
                    # FIX: Force the value into a string format so st.metric doesn't crash on lists/dicts
                    if isinstance(value, (list, dict)):
                        display_value = ", ".join(value) if isinstance(value, list) else str(value)
                    else:
                        display_value = str(value)
                        
                    cols[col_idx % len(cols)].metric(label=clean_key, value=display_value)
                    col_idx += 1
            
            st.caption(f"Source Document: {source}")
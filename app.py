import streamlit as st
from src.ui import render_page_config, render_header, render_sidebar, render_file_uploader, render_timeline , render_review_ui
from src.database import init_db, save_timeline_events, get_timeline_events
from src.utils import process_medical_file
from src.agents import compiled_graph

def main():
    render_page_config()
    init_db()
    
    # Render the sidebar FIRST so the patient is selected before file upload
    render_sidebar()
    render_header()

    # Halt execution if no patient is selected
    if not st.session_state.get("current_patient"):
        st.info("👈 Please select or add a patient in the sidebar to begin.")
        return

    active_patient = st.session_state.current_patient

    uploaded_file = render_file_uploader()

    if uploaded_file is not None:
        if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
            with st.spinner(f"Analyzing {uploaded_file.name} for {active_patient}..."):
                try:
                    file_bytes = uploaded_file.getvalue()
                    mime_type = uploaded_file.type
                    raw_vision_data = process_medical_file(uploaded_file.name, file_bytes, mime_type)

                    initial_state = {
                        "file_name": uploaded_file.name, "mime_type": mime_type,
                        "raw_data": raw_vision_data, "extracted_text": "",
                        "timeline_events": [], "status": "started", "errors": []
                    }

                    final_state = compiled_graph.invoke(initial_state)

                    if final_state.get("status") == "failed":
                        st.error(f"Processing failed: {final_state.get('errors')}")
                    else:
                        st.session_state.pending_events = final_state.get("timeline_events", [])
                        st.session_state.processed_file = uploaded_file.name

                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
        
        # --- DOCTOR-FRIENDLY REVIEW UI ---
        if "pending_events" in st.session_state and st.session_state.pending_events:
            
            # Use our new custom form component
            submitted, edited_events = render_review_ui(st.session_state.pending_events)
            
            if submitted:
                save_timeline_events(edited_events, uploaded_file.name, active_patient)
                st.session_state.pending_events = []
                st.success(f"Stored verified medical events for {active_patient}!")
                st.rerun() # Refresh to clear the form and update the timeline

    st.divider()
    
    patient_events = get_timeline_events(active_patient)
    render_timeline(patient_events)

if __name__ == "__main__":
    main()
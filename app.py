import streamlit as st
from src.ui import (
    render_page_config,
    render_header,
    render_sidebar,
    render_file_uploader
)
from src.database import init_db, save_timeline_events
from src.utils import process_medical_file
from src.agents import compiled_graph

def main():
    # 1. Boot up configurations and database schema
    render_page_config()
    init_db()

    # 2. Render UI shells
    render_sidebar()
    render_header()

    # 3. Capture file upload
    uploaded_file = render_file_uploader()

    # 4. The Execution Pipeline
    if uploaded_file is not None:
        # Prevent Streamlit from re-running the AI on every UI interaction
        if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
            
            # Show a loading spinner while the graph runs
            with st.spinner(f"Agent pipeline is analyzing {uploaded_file.name}..."):
                try:
                    # A. Deterministic Pre-processing (Day 1 utilities)
                    file_bytes = uploaded_file.getvalue()
                    mime_type = uploaded_file.type
                    raw_vision_data = process_medical_file(
                        file_name=uploaded_file.name, 
                        file_bytes=file_bytes, 
                        mime_type=mime_type
                    )

                    # B. Initialize the LangGraph State (Day 2 data structure)
                    initial_state = {
                        "file_name": uploaded_file.name,
                        "mime_type": mime_type,
                        "raw_data": raw_vision_data,
                        "extracted_text": "",
                        "timeline_events": [],
                        "status": "started",
                        "errors": []
                    }

                    # C. Execute the Multi-Agent State Machine (Day 2 graph)
                    final_state = compiled_graph.invoke(initial_state)

                    # D. Handle Output and Persistence (Day 3 DB operations)
                    if final_state.get("status") == "failed":
                        st.error(f"Processing failed: {final_state.get('errors')}")
                    else:
                        events = final_state.get("timeline_events", [])
                        
                        # Save the structured AI output to local SQLite
                        save_timeline_events(events, uploaded_file.name)
                        
                        # Lock the session state so it doesn't run again
                        st.session_state.processed_file = uploaded_file.name
                        st.success(f"Successfully processed and stored {len(events)} medical events!")

                except Exception as e:
                    st.error(f"An unexpected error occurred during execution: {str(e)}")
        else:
            st.info(f"File '{uploaded_file.name}' has already been processed and saved to the database.")

if __name__ == "__main__":
    main()
import streamlit as st
from src.ui import (
    render_page_config,
    render_header,
    render_sidebar,
    render_file_uploader,
    render_timeline
)
from src.database import init_db, save_timeline_events, get_all_timeline_events
from src.utils import process_medical_file
from src.agents import compiled_graph

def main():
    render_page_config()
    init_db()
    render_sidebar()
    render_header()

    uploaded_file = render_file_uploader()

    if uploaded_file is not None:
        if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
            with st.spinner(f"Agent pipeline is analyzing {uploaded_file.name}..."):
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
                        events = final_state.get("timeline_events", [])
                        save_timeline_events(events, uploaded_file.name)
                        st.session_state.processed_file = uploaded_file.name
                        st.success(f"Successfully processed and stored {len(events)} medical events!")

                except Exception as e:
                    st.error(f"An unexpected error occurred during execution: {str(e)}")
        else:
            st.info(f"File '{uploaded_file.name}' has already been processed and saved to the database.")

    # 3. Add the visual separation and render the persistent timeline
    st.divider()
    
    # Fetch all historical events from the local SQLite database
    historical_events = get_all_timeline_events()
    
    # Pass the database rows to the UI component to draw the cards
    render_timeline(historical_events)

if __name__ == "__main__":
    main()
import streamlit as st
from src.ui import (
    render_page_config,
    render_header,
    render_sidebar,
    render_file_uploader
)
# Import the new DB initializer
from src.database import init_db

def main():
    # 1. Page configuration must be the first Streamlit command run
    render_page_config()
    
    # 2. Initialize the database schema (creates the .db file if missing)
    init_db()

    # 3. Render UI shells
    render_sidebar()
    render_header()
    
    # 4. Render and capture file input
    uploaded_file = render_file_uploader()

    # 5. State management placeholder for agent execution
    if uploaded_file:
        st.info("Document loaded into application buffer. Ready for agent processing.")
        
        # Display file metadata
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type,
        }
        st.json(file_details)

if __name__ == "__main__":
    main()
#Reusable ui widgets (file uploader, chat bubbles)

import streamlit as st

def render_file_uploader():
    upload_file = st.file_uploader("Upload", type = ["pdf","jpg","png"])

    if upload_file is not None:
        st.success("File successfully uploaded!")
    
    return upload_file
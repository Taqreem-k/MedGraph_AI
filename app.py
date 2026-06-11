import streamlit as st
from src.ui import render_file_uploader

st.set_page_config(
    page_title="MedGraph AI",
    layout = "wide",
    
)

st.title("MedGraph AI")

st.subheader("An AI EMR System for medical data in a graphical way")

st.subheader("Input the medical file:")

medical_file = render_file_uploader()